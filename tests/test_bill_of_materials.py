import json
from pathlib import Path

import numpy as np
import pytest

from pydome.polyhedral import Icosahedron, Octahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.bill_of_materials import (
    get_bill_of_materials,
    compute_hub_data,
    compute_spoke_angles,
    group_hub_types,
    _hub_type_signature,
    _ellipsoid_normal,
    compute_face_data,
    group_face_types,
    compute_dihedral_angles,
)
from pydome.elongation import elongate


def build_sphere(frequency=1, radius=1.0, polyhedron=None):
    poly = polyhedron if polyhedron is not None else Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords


def build_sphere_with_faces(frequency=1, radius=1.0, polyhedron=None):
    poly = polyhedron if polyhedron is not None else Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords, sphere.non_duplicate_face_nodes


def test_bill_of_materials_reports_expected_sections(capsys):
    V, C = build_sphere()
    get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]

    assert "Bill of materials" in report
    assert "Angles at hub between outbound cords and tangential plane" in report
    assert "Spoke angles" in report


def test_bill_of_materials_chord_length_counts_sum_correctly(capsys):
    V, C = build_sphere()
    get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Bill of materials"]["Chord Lengths and Counts"]

    assert sum(row["count"] for row in rows) == len(C)


def test_bill_of_materials_does_not_merge_distinct_strut_lengths_at_fine_precision(capsys):
    # at frequency 20, some genuinely distinct strut-length classes differ
    # by less than 1e-5 -- smaller than pyDome's old default rounding
    # precision (5) used to distinguish. At a precision fine enough to
    # resolve them (9, the tool's current default), clustering should
    # separate every one by its true geometric gap rather than merging any.
    V, C = build_sphere(frequency=20)

    raw_lengths = [np.linalg.norm(V[c[0]] - V[c[1]]) for c in C]
    tolerance = max(raw_lengths) * 1e-9
    sorted_lengths = sorted(raw_lengths)
    true_distinct_count = 1
    for i in range(1, len(sorted_lengths)):
        if sorted_lengths[i] - sorted_lengths[i - 1] > tolerance:
            true_distinct_count += 1

    get_bill_of_materials(V, C, 9)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Bill of materials"]["Chord Lengths and Counts"]

    assert len(rows) == true_distinct_count
    assert sum(row["count"] for row in rows) == len(C)


def test_bill_of_materials_coarse_precision_merges_near_identical_lengths(capsys):
    # a coarse rounding_precision should deliberately merge strut lengths
    # that are close but not identical -- e.g. for a builder whose tools
    # can't distinguish fabrication-irrelevant differences -- collapsing
    # them into fewer, coarser-grained BOM entries rather than reporting
    # a wall of rows that all display the same rounded length.
    V, C = build_sphere(frequency=20)

    get_bill_of_materials(V, C, 2)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Bill of materials"]["Chord Lengths and Counts"]
    displayed_lengths = [row["length"] for row in rows]

    assert len(displayed_lengths) == len(set(displayed_lengths))
    assert sum(row["count"] for row in rows) == len(C)


def test_bill_of_materials_reports_total_strut_length_by_default(capsys):
    V, C = build_sphere()
    get_bill_of_materials(V, C, 9)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]

    assert "Total material" in report
    expected_total = sum(np.linalg.norm(V[c[0]] - V[c[1]]) for c in C)
    assert report["Total material"]["Total strut length"] == pytest.approx(expected_total)
    assert "Total estimated material cost" not in report["Total material"]


def test_bill_of_materials_reports_cost_when_given_a_unit_price(capsys):
    V, C = build_sphere()
    get_bill_of_materials(V, C, 9, cost_per_unit_length=2.5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    total_material = report["Total material"]

    expected_total = sum(np.linalg.norm(V[c[0]] - V[c[1]]) for c in C)
    assert total_material["Total strut length"] == pytest.approx(expected_total)
    assert total_material["Total estimated material cost"] == pytest.approx(expected_total * 2.5, abs=0.01)


def test_hub_type_signature_is_invariant_to_which_connecting_hub_sorts_first():
    # compute_spoke_angles measures every spoke relative to whichever
    # connecting hub happens to sort first by index -- an arbitrary
    # reference with no geometric meaning. Two hubs that are the same
    # shape, just rotated, must still get the identical signature.
    V, C = build_sphere(frequency=4)
    hubs = compute_hub_data(V, C)
    groups = group_hub_types(hubs)

    # every hub within a reported group must actually share that group's
    # signature (i.e. grouping is self-consistent, not just count-based)
    for group in groups:
        expected_sig = _hub_type_signature(hubs[group["representative_hub"]], 3)
        for hub_idx in group["hub_indices"]:
            assert _hub_type_signature(hubs[hub_idx], 3) == expected_sig


def test_group_hub_types_accounts_for_every_hub_exactly_once():
    V, C = build_sphere(frequency=4)
    hubs = compute_hub_data(V, C)
    groups = group_hub_types(hubs)

    all_hub_indices = [idx for g in groups for idx in g["hub_indices"]]
    assert sorted(all_hub_indices) == sorted(hubs.keys())
    assert len(all_hub_indices) == len(set(all_hub_indices))


def test_icosahedron_vertex_hubs_have_five_evenly_spaced_spokes():
    # the 12 original icosahedron vertices are the only 5-valence hubs
    # in a Class I icosahedron-derived dome, and by the icosahedron's
    # own symmetry their 5 spokes must be exactly 72 degrees apart
    V, C = build_sphere(frequency=4)
    hubs = compute_hub_data(V, C)
    groups = group_hub_types(hubs)

    valence_5_groups = [g for g in groups if g["valence"] == 5]
    assert len(valence_5_groups) == 1
    assert valence_5_groups[0]["count"] == 12

    rep = hubs[valence_5_groups[0]["representative_hub"]]
    angles = sorted(a % 360 for a in compute_spoke_angles(rep).values())
    gaps = [(angles[(i + 1) % 5] - angles[i]) % 360 for i in range(5)]
    for gap in gaps:
        assert gap == pytest.approx(72.0)


def test_bill_of_materials_hub_templates_writes_one_dxf_per_type_and_covers_every_hub(tmp_path, capsys):
    V, C = build_sphere(frequency=4)
    output_prefix = str(tmp_path / "dome")

    get_bill_of_materials(V, C, 5, hub_template_output_path=output_prefix)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Hub Connector Templates"]

    hubs = compute_hub_data(V, C)
    multi_strut_hub_count = sum(1 for h in hubs.values() if len(h["connected_vertices"]) > 1)
    assert sum(row["hub_count"] for row in rows) == multi_strut_hub_count

    for row in rows:
        template_path = Path(row["template_file"])
        assert template_path.exists()
        content = template_path.read_text()
        assert content.startswith("0\nSECTION\n2\nENTITIES\n")
        assert content.count("LINE\n") == row["struts_per_hub"]
        assert content.count("TEXT\n") == row["struts_per_hub"]


def test_bill_of_materials_tangential_angles_are_small_for_a_smooth_sphere(capsys):
    # a reasonably fine sphere should have small deflection angles between
    # each chord and the tangent plane at its hub
    V, C = build_sphere(frequency=3)
    get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Angles at hub between outbound cords and tangential plane"]

    for row in rows:
        assert abs(row["angle (degrees)"]) < 45


def test_get_bill_of_materials_returns_the_report_dict(capsys):
    V, C = build_sphere()
    report = get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    assert captured.out != ""  # default print_report=True, unchanged
    assert "Bill of materials" in report["pyDome report"]


def test_get_bill_of_materials_print_report_false_suppresses_stdout(capsys):
    # stdio-transport MCP uses stdout as the JSON-RPC wire, so tool
    # handlers must be able to compute the report without printing
    V, C = build_sphere()
    report = get_bill_of_materials(V, C, 5, print_report=False)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Bill of materials" in report["pyDome report"]


def test_ellipsoid_normal_matches_hand_computed_value():
    # a=1 (x/y semi-axis), c=2 (z semi-axis, elongation factor 2), point
    # at theta=45 degrees on the x-z ellipse (y=0): x=cos(45)=0.7071,
    # z=2*sin(45)=1.4142. True normal (gradient of x^2/a^2+z^2/c^2=1) is
    # proportional to (x/a^2, z/c^2) = (0.7071, 0.3536), normalized to
    # (0.8944, 0.4472) -- the exact opposite ratio of the naive,
    # position-vector-normalized (wrong) answer.
    vertex = np.array([np.cos(np.pi / 4), 0., 2 * np.sin(np.pi / 4)])
    normal = _ellipsoid_normal(vertex, elongation_factors=(1.0, 1.0, 2.0))

    assert normal == pytest.approx(np.array([0.8944271909999159, 0., 0.4472135954999579]))

    naive_wrong_normal = vertex / np.linalg.norm(vertex)
    assert not np.allclose(normal, naive_wrong_normal)


def test_ellipsoid_normal_matches_hand_computed_value_for_x_axis_elongation():
    # same construction as the Z-axis case above, but rotated onto the
    # x-y ellipse instead (b=1 y semi-axis, elongation factor 2 on X) --
    # exercises the same formula on a different axis than the one it was
    # originally derived and verified against, per this project's "vary
    # the case's proportions, not just its identity" verification rule.
    vertex = np.array([2 * np.sin(np.pi / 4), np.cos(np.pi / 4), 0.])
    normal = _ellipsoid_normal(vertex, elongation_factors=(2.0, 1.0, 1.0))

    assert normal == pytest.approx(np.array([0.4472135954999579, 0.8944271909999159, 0.]))


def test_ellipsoid_normal_matches_finite_difference_gradient_for_a_triaxial_ellipsoid():
    # independent numerical check for the fully general (fx != fy != fz)
    # case, which no single-axis hand-computed case above exercises:
    # numerically approximate the gradient of F(x,y,z) = x^2/fx^2 +
    # y^2/fy^2 + z^2/fz^2 - 1 by central differences at a point on that
    # ellipsoid's surface, and compare its normalized direction against
    # _ellipsoid_normal's analytic answer -- a genuinely different
    # method for the same quantity, not a restatement of the formula.
    fx, fy, fz = 2.0, 3.0, 0.5
    factors = np.array([fx, fy, fz])

    # a point on the surface: pick spherical angles, scale by factors
    theta, phi = 0.7, 1.1
    unit = np.array([
        np.sin(theta) * np.cos(phi),
        np.sin(theta) * np.sin(phi),
        np.cos(theta),
    ])
    vertex = unit * factors

    def implicit_surface(v):
        return np.sum((v / factors) ** 2) - 1.

    h = 1e-6
    numerical_gradient = np.array([
        (implicit_surface(vertex + h * np.eye(3)[i]) -
         implicit_surface(vertex - h * np.eye(3)[i])) / (2 * h)
        for i in range(3)
    ])
    numerical_normal = numerical_gradient / np.linalg.norm(numerical_gradient)

    normal = _ellipsoid_normal(vertex, elongation_factors=tuple(factors))

    assert normal == pytest.approx(numerical_normal, abs=1e-5)


def test_ellipsoid_normal_reduces_to_sphere_normal_when_factors_are_one():
    vertex = np.array([0.5, 0.5, 1. / np.sqrt(2)])
    normal = _ellipsoid_normal(vertex, elongation_factors=(1.0, 1.0, 1.0))
    sphere_normal = vertex / np.linalg.norm(vertex)

    assert normal == pytest.approx(sphere_normal)


def test_ellipsoid_normal_is_axis_aligned_at_the_pole_and_equator_regardless_of_elongation():
    # at the pole (0,0,c) and equator (a,0,0), the ellipsoid's true
    # normal happens to coincide with the naive position-vector
    # direction for any elongation factor -- these points don't
    # distinguish a correct implementation from the old, wrong one, but
    # they're still useful as a basic sanity check
    for factor in [0.5, 1.0, 3.0]:
        pole = np.array([0., 0., factor])
        assert _ellipsoid_normal(pole, (1.0, 1.0, factor)) == pytest.approx(np.array([0., 0., 1.]))

        equator = np.array([1., 0., 0.])
        assert _ellipsoid_normal(equator, (1.0, 1.0, factor)) == pytest.approx(np.array([1., 0., 0.]))


def test_compute_face_data_normals_point_outward():
    V, C, F = build_sphere_with_faces(frequency=3)
    face_data = compute_face_data(V, F)

    for fd in face_data:
        assert np.dot(fd['normal'], fd['centroid']) > 0


def test_dihedral_angles_match_known_platonic_values():
    # a frequency-1 dome is just the base polyhedron itself, so every
    # pair of adjacent faces meets at exactly the textbook dihedral
    # angle for that solid.
    V, C, F = build_sphere_with_faces(frequency=1, polyhedron=Icosahedron())
    face_data = compute_face_data(V, F)
    angles = [row['dihedral angle (degrees)'] for row in compute_dihedral_angles(face_data, C)]
    assert len(angles) == len(C)
    for angle in angles:
        assert angle == pytest.approx(138.18968510422, abs=1e-6)

    V, C, F = build_sphere_with_faces(frequency=1, polyhedron=Octahedron())
    face_data = compute_face_data(V, F)
    angles = [row['dihedral angle (degrees)'] for row in compute_dihedral_angles(face_data, C)]
    for angle in angles:
        assert angle == pytest.approx(109.47122063449, abs=1e-6)


def test_group_face_types_flags_chirality_on_scalene_group():
    V, C, F = build_sphere_with_faces(frequency=4)
    face_data = compute_face_data(V, F)
    groups = group_face_types(face_data)

    chiral_groups = [g for g in groups if g['chiral']]
    assert len(chiral_groups) == 1
    chiral_group = chiral_groups[0]
    assert chiral_group['count'] == 120
    assert sorted(o['count'] for o in chiral_group['orientations']) == [60, 60]


def test_group_face_types_isosceles_and_equilateral_never_chiral():
    V, C, F = build_sphere_with_faces(frequency=4)
    face_data = compute_face_data(V, F)
    groups = group_face_types(face_data)

    non_chiral_groups = [g for g in groups if not g['chiral']]
    assert len(non_chiral_groups) == 4
    for g in non_chiral_groups:
        assert g['orientations'] is None
        assert len(set(g['edge_lengths'])) < 3  # isosceles or equilateral


def test_get_bill_of_materials_skips_face_sections_when_faces_is_none(capsys):
    V, C = build_sphere()
    report = get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    assert captured.out != ""
    for key in ('Panel shapes and counts', 'Total panel material',
                'Bevel angles at panel edges', 'Panel Cutting Templates'):
        assert key not in report['pyDome report']


def test_get_bill_of_materials_reports_total_panel_area_and_optional_cost_and_weight(capsys):
    V, C, F = build_sphere_with_faces(frequency=3)
    report = get_bill_of_materials(V, C, 5, faces=F, cost_per_unit_area=2.0, panel_areal_density=0.5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)['pyDome report']

    total_panel_material = report['Total panel material']
    expected_area = sum(fd['area'] for fd in compute_face_data(V, F))
    assert total_panel_material['Total panel area'] == pytest.approx(expected_area, abs=1e-4)
    assert total_panel_material['Total estimated panel material cost'] == pytest.approx(expected_area * 2.0, abs=0.01)
    assert total_panel_material['Total estimated panel weight'] == pytest.approx(expected_area * 0.5, abs=0.01)

    panel_types = report['Panel shapes and counts']['Panel Types and Counts']
    assert sum(g['count'] for g in panel_types) == len(F)

    bevel_rows = report['Bevel angles at panel edges']
    assert len(bevel_rows) == len(C)


def test_bill_of_materials_face_templates_writes_one_dxf_per_shape_and_covers_every_face(tmp_path, capsys):
    V, C, F = build_sphere_with_faces(frequency=4)
    output_prefix = str(tmp_path / "dome")

    get_bill_of_materials(V, C, 5, faces=F, face_template_output_path=output_prefix)

    captured = capsys.readouterr()
    report = json.loads(captured.out)['pyDome report']
    rows = report['Panel Cutting Templates']

    face_data = compute_face_data(V, F)
    groups = group_face_types(face_data)
    assert len(rows) == len(groups)
    assert sum(row['panel_count'] for row in rows) == len(F)

    for row in rows:
        template_path = Path(row['template_file'])
        assert template_path.exists()
        content = template_path.read_text()
        assert content.startswith("0\nSECTION\n2\nENTITIES\n")
        assert content.count("LINE\n") == 3
        assert content.count("TEXT\n") == 3


def test_bill_of_materials_with_elongation_still_produces_valid_report(capsys):
    # end-to-end sanity check: elongating shouldn't break report
    # generation, and chord-length/count totals must still be internally
    # consistent regardless of the (non-uniform) vertex scaling
    V, C = build_sphere(frequency=3)
    V = elongate(V, (1.0, 1.0, 1.8))

    get_bill_of_materials(V, C, 5, elongation_factors=(1.0, 1.0, 1.8))

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]

    rows = report["Bill of materials"]["Chord Lengths and Counts"]
    assert sum(row["count"] for row in rows) == len(C)

    angle_rows = report["Angles at hub between outbound cords and tangential plane"]
    assert len(angle_rows) > 0
    for row in angle_rows:
        assert -90. <= row["angle (degrees)"] <= 90.
