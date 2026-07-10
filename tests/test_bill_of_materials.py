import json

import numpy as np

from Polyhedral import Icosahedron
from SymmetryTriangle import ClassOneMethodOneSymmetryTriangle
from GeodesicSphere import GeodesicSphere
from BillOfMaterials import get_bill_of_materials


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


def test_bill_of_materials_does_not_merge_distinct_strut_lengths_at_high_frequency(capsys):
    # at frequency 20, some genuinely distinct strut-length classes differ
    # by less than a naive round(x, 5) grouping's granularity and used to
    # get silently merged into one BOM entry. The clustering approach
    # should separate them by their true geometric gaps instead.
    V, C = build_sphere(frequency=20)

    raw_lengths = [np.linalg.norm(V[c[0]] - V[c[1]]) for c in C]
    tolerance = max(raw_lengths) * 1e-9
    sorted_lengths = sorted(raw_lengths)
    true_distinct_count = 1
    for i in range(1, len(sorted_lengths)):
        if sorted_lengths[i] - sorted_lengths[i - 1] > tolerance:
            true_distinct_count += 1

    get_bill_of_materials(V, C, 5)

    captured = capsys.readouterr()
    report = json.loads(captured.out)["pyDome report"]
    rows = report["Bill of materials"]["Chord Lengths and Counts"]

    assert len(rows) == true_distinct_count
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
