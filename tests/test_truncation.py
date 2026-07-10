import numpy as np
import pytest

from Polyhedral import Icosahedron
from SymmetryTriangle import ClassOneMethodOneSymmetryTriangle
from GeodesicSphere import GeodesicSphere
from Truncation import truncate


def build_sphere(frequency=3, radius=1.0):
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords


def test_truncate_removes_vertices_below_cutoff():
    V, C = build_sphere()
    V_new, C_new = truncate(V, C, 0.499999)

    min_vy = min(v[2] for v in V)
    max_vy = max(v[2] for v in V)
    cutoff = min_vy + 0.499999 * abs(max_vy - min_vy)

    # a small floating point tolerance accounts for vertices created
    # exactly at the cutoff plane by the chord-splitting logic
    tolerance = 1e-9
    for v in V_new:
        assert v[2] >= cutoff - tolerance

    assert len(V_new) < len(V)
    assert len(C_new) > 0


def test_truncate_chords_reference_valid_vertex_indices():
    V, C = build_sphere()
    V_new, C_new = truncate(V, C, 0.499999)
    for c in C_new:
        assert 1 <= c[0] <= len(V_new)
        assert 1 <= c[1] <= len(V_new)


@pytest.mark.parametrize("truncation_amount", [0.2, 0.333333, 0.499999, 0.75])
def test_truncate_never_adds_chords(truncation_amount):
    # truncation only removes chords entirely below the cutoff or replaces
    # a crossing chord 1:1 with a shortened one, so the chord count can
    # only shrink. Vertex count is not monotonic: a chord that crosses the
    # cutoff contributes a new interpolated vertex, and a shallow cutoff
    # near the pole can cross more chords than it removes vertices for.
    V, C = build_sphere()
    V_new, C_new = truncate(V, C, truncation_amount)
    assert len(C_new) <= len(C)
    assert len(V_new) > 0
