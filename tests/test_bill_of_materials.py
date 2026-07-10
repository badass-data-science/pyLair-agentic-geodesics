import json

import numpy as np

from pydome.polyhedral import Icosahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.bill_of_materials import get_bill_of_materials


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
