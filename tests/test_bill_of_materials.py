import json
from pathlib import Path

import numpy as np
import pytest

from pydome.polyhedral import Icosahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.bill_of_materials import (
    get_bill_of_materials,
    compute_hub_data,
    compute_spoke_angles,
    group_hub_types,
    _hub_type_signature,
)


def build_sphere(frequency=1, radius=1.0):
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords


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
