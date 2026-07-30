import numpy as np
import pytest

from pylair.polyhedral import Icosahedron
from pylair.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pylair.geodesic_sphere import GeodesicSphere
from pylair.assembly import (
    build_assembly_manifest,
    build_pyfit_job_spec_for_panels,
    build_pyfit_job_spec_for_hubs,
    attach_nest_placements,
    hub_label,
    strut_label,
    panel_label,
    parse_instance_label,
    _mirrored_triangle_polygon,
)


def build_sphere_with_faces(frequency=4, radius=1.0, polyhedron=None):
    poly = polyhedron if polyhedron is not None else Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords, sphere.non_duplicate_face_nodes


def test_labels_round_trip():
    for label_fn, kind, idx in ((hub_label, 'hub', 7), (strut_label, 'strut', 42), (panel_label, 'panel', 0)):
        label = label_fn(idx)
        assert parse_instance_label(label) == (kind, idx)


def test_parse_instance_label_rejects_unknown_labels():
    with pytest.raises(ValueError):
        parse_instance_label("facetype3")
    with pytest.raises(ValueError):
        parse_instance_label("")


def test_manifest_accounts_for_every_hub_strut_and_panel_exactly_once():
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)

    assert len(manifest['hubs']) == len(V)
    assert len(manifest['struts']) == len(C)
    assert len(manifest['panels']) == len(F)

    all_hub_ids_in_groups = [hid for g in manifest['hub_groups'] for hid in g['hub_ids']]
    assert sorted(all_hub_ids_in_groups) == sorted(manifest['hubs'].keys())
    assert len(all_hub_ids_in_groups) == len(set(all_hub_ids_in_groups))

    all_strut_ids_in_groups = [sid for g in manifest['strut_groups'] for sid in g['strut_ids']]
    assert sorted(all_strut_ids_in_groups) == sorted(manifest['struts'].keys())

    all_panel_ids_in_groups = [pid for g in manifest['panel_groups'] for pid in g['panel_ids']]
    assert sorted(all_panel_ids_in_groups) == sorted(manifest['panels'].keys())


def test_manifest_omits_panels_when_faces_not_given():
    V, C, F = build_sphere_with_faces(frequency=3)
    manifest = build_assembly_manifest(V, C, faces=None)

    assert manifest['panels'] == {}
    assert manifest['panel_groups'] == []
    assert len(manifest['hubs']) == len(V)
    assert len(manifest['struts']) == len(C)


def test_every_hub_connection_references_a_real_strut_and_hub():
    V, C, F = build_sphere_with_faces(frequency=3)
    manifest = build_assembly_manifest(V, C, faces=F)

    for hub_id, hub in manifest['hubs'].items():
        assert hub['valence'] == len(hub['connections'])
        for conn in hub['connections']:
            assert conn['to_hub'] in manifest['hubs']
            strut = manifest['struts'][conn['strut']]
            assert {strut['hub_1'], strut['hub_2']} == {hub_id, conn['to_hub']}


def test_every_panel_edge_resolves_to_a_real_strut_on_an_untruncated_dome():
    # every face edge on a closed (untruncated) dome borders a real
    # chord -- no boundary edges to leave unresolved
    V, C, F = build_sphere_with_faces(frequency=3)
    manifest = build_assembly_manifest(V, C, faces=F)

    for panel in manifest['panels'].values():
        assert len(panel['edges']) == 3
        for edge in panel['edges']:
            assert edge['strut'] is not None
            assert edge['bevel_angle_degrees'] is not None
            assert edge['note'] == ''


def test_chiral_panel_group_splits_into_two_orientation_buckets():
    # frequency-4 Class I icosahedron has one genuinely chiral face
    # group (120 faces, 60/60 split) -- see the equivalent
    # bill_of_materials test this mirrors.
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)

    chiral_groups = [g for g in manifest['panel_groups'] if g['chiral']]
    assert len(chiral_groups) == 1
    group = chiral_groups[0]
    assert group['count'] == 120
    buckets = group['chirality_bucket_panel_ids']
    assert sorted(len(b) for b in buckets) == [60, 60]

    # every panel in the group actually has an orientation_bucket set,
    # and it agrees with which bucket list it appears in
    for bucket_i, panel_ids in enumerate(buckets):
        for pid in panel_ids:
            assert manifest['panels'][pid]['orientation_bucket'] == bucket_i
            assert manifest['panels'][pid]['chiral'] is True


def test_non_chiral_panel_groups_have_no_orientation_bucket():
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)

    for group in manifest['panel_groups']:
        if not group['chiral']:
            for pid in group['panel_ids']:
                assert manifest['panels'][pid]['orientation_bucket'] is None
                assert manifest['panels'][pid]['chiral'] is False


def test_mirrored_triangle_polygon_preserves_edge_lengths_but_flips_winding():
    edge_lengths = (3.0, 4.0, 5.0)
    mirrored = _mirrored_triangle_polygon(edge_lengths)
    assert len(mirrored) == 3

    A, B, C = [np.array(p) for p in mirrored]
    mirrored_edges = (
        np.linalg.norm(B - A),
        np.linalg.norm(C - B),
        np.linalg.norm(A - C),
    )
    assert mirrored_edges == pytest.approx(edge_lengths)

    # the un-mirrored construction (see output.OutputFaceTemplateDXF) has
    # C's y-coordinate >= 0 by construction; the mirrored one must not.
    assert C[1] <= 0


def test_pyfit_job_spec_for_panels_has_one_quantity_one_entry_per_instance():
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)
    template_paths = {g['template_group']: f"template_{g['template_group']}.dxf" for g in manifest['panel_groups']}

    job = build_pyfit_job_spec_for_panels(manifest, sheet_width=48, sheet_height=96,
                                          template_dxf_paths=template_paths)

    assert job['sheet'] == {'width': 48, 'height': 96}
    assert len(job['parts']) == len(F)
    names = [p['name'] for p in job['parts']]
    assert len(names) == len(set(names))  # every instance is its own part entry
    assert sorted(names) == sorted(manifest['panels'].keys())
    for part in job['parts']:
        assert part['quantity'] == 1
        assert part['allow_mirror'] is False or part.get('dxf') is not None


def test_pyfit_job_spec_for_panels_forces_chirality_via_dxf_vs_polygon():
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)
    template_paths = {g['template_group']: f"template_{g['template_group']}.dxf" for g in manifest['panel_groups']}

    job = build_pyfit_job_spec_for_panels(manifest, sheet_width=48, sheet_height=96,
                                          template_dxf_paths=template_paths)
    parts_by_name = {p['name']: p for p in job['parts']}

    chiral_group = next(g for g in manifest['panel_groups'] if g['chiral'])
    canonical_ids, mirror_ids = chiral_group['chirality_bucket_panel_ids']

    for pid in canonical_ids:
        part = parts_by_name[pid]
        assert 'dxf' in part and 'polygon' not in part
        assert part['allow_mirror'] is False

    for pid in mirror_ids:
        part = parts_by_name[pid]
        assert 'polygon' in part and 'dxf' not in part
        assert part['allow_mirror'] is False

    non_chiral_group = next(g for g in manifest['panel_groups'] if not g['chiral'])
    for pid in non_chiral_group['panel_ids']:
        assert parts_by_name[pid]['allow_mirror'] is True


def test_pyfit_job_spec_for_hubs_has_one_quantity_one_entry_per_hub():
    V, C, F = build_sphere_with_faces(frequency=4)
    manifest = build_assembly_manifest(V, C, faces=F)
    template_paths = {g['template_group']: f"hubtemplate_{g['template_group']}.dxf" for g in manifest['hub_groups']}

    job = build_pyfit_job_spec_for_hubs(manifest, sheet_width=24, sheet_height=24,
                                        template_dxf_paths=template_paths)

    assert len(job['parts']) == len(V)
    for part in job['parts']:
        assert part['quantity'] == 1
        assert part['allow_mirror'] is True


def test_attach_nest_placements_merges_by_instance_label():
    V, C, F = build_sphere_with_faces(frequency=3)
    manifest = build_assembly_manifest(V, C, faces=F)

    some_panel_id = next(iter(manifest['panels']))
    fake_nest_report = {
        'placements': [
            {
                'part_name': some_panel_id,
                'sheet_index': 0,
                'position': [1.0, 2.0],
                'rotation_degrees': 45.0,
                'mirrored': True,
            },
            {
                'part_name': 'not_a_real_instance_label',
                'sheet_index': 0,
                'position': [0.0, 0.0],
                'rotation_degrees': 0.0,
                'mirrored': False,
            },
        ]
    }

    attach_nest_placements(manifest, fake_nest_report, kind='panels')

    assert manifest['panels'][some_panel_id]['placement'] == {
        'sheet_index': 0,
        'position': [1.0, 2.0],
        'rotation_degrees': 45.0,
        'mirrored': True,
    }
    # every other panel is untouched
    other_panels = [p for pid, p in manifest['panels'].items() if pid != some_panel_id]
    assert all('placement' not in p for p in other_panels)
