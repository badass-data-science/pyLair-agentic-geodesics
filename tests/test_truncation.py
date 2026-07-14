import numpy as np
import pytest

from pydome.polyhedral import Icosahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.truncation import truncate


def build_sphere(frequency=3, radius=1.0):
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    sphere = GeodesicSphere(poly, st, 1e-7, radius)
    return sphere.sphere_vertices, sphere.non_duplicate_chords


def test_truncate_removes_vertices_below_cutoff():
    V, C = build_sphere()
    V_new, C_new, F_new = truncate(V, C, 0.499999)

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
    assert F_new is None  # F_sphere not given -> no face data to return


def test_truncate_chords_reference_valid_vertex_indices():
    V, C = build_sphere()
    V_new, C_new, _ = truncate(V, C, 0.499999)
    for c in C_new:
        assert 0 <= c[0] < len(V_new)
        assert 0 <= c[1] < len(V_new)


@pytest.mark.parametrize("truncation_amount", [0.2, 0.333333, 0.499999, 0.75])
def test_truncate_never_adds_chords(truncation_amount):
    # truncation only removes chords entirely below the cutoff or replaces
    # a crossing chord 1:1 with a shortened one, so the chord count can
    # only shrink. Vertex count is not monotonic: a chord that crosses the
    # cutoff contributes a new interpolated vertex, and a shallow cutoff
    # near the pole can cross more chords than it removes vertices for.
    V, C = build_sphere()
    V_new, C_new, _ = truncate(V, C, truncation_amount)
    assert len(C_new) <= len(C)
    assert len(V_new) > 0


def test_truncate_raises_clearly_on_horizontal_chord_at_cutoff():
    # a chord whose two endpoints straddle the cutoff by less than
    # HORIZONTAL_CHORD_EPSILON in z must fail loudly rather than silently
    # dividing by a near-zero z-extent (numpy warns on divide-by-zero
    # instead of raising, which would otherwise produce an inf/nan vertex).
    V = [
        np.array([0., 0., 0.]),
        np.array([1., 0., 0.5 - 1e-13]),
        np.array([1., 1., 0.5]),
    ]
    C = [[1, 2]]

    with pytest.raises(ValueError):
        truncate(V, C, 1.0)  # cutoff_from_bottom=1.0 -> cutoff = max z = 0.5


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_truncate_removes_vertices_below_cutoff_on_any_axis(axis):
    V, C = build_sphere()
    V_new, C_new, _ = truncate(V, C, 0.499999, axis=axis)

    min_v = min(v[axis] for v in V)
    max_v = max(v[axis] for v in V)
    cutoff = min_v + 0.499999 * abs(max_v - min_v)

    tolerance = 1e-9
    for v in V_new:
        assert v[axis] >= cutoff - tolerance

    assert len(V_new) < len(V)
    assert len(C_new) > 0


def test_truncate_on_x_leaves_full_z_range_untouched_elsewhere():
    # truncating on X shouldn't have anything special to say about Z --
    # this just confirms the axis parameter actually redirects the cut,
    # not that it silently still cuts on Z under the hood.
    V, C = build_sphere()
    V_new, _, _ = truncate(V, C, 0.499999, axis=0)

    min_x = min(v[0] for v in V)
    max_x = max(v[0] for v in V)
    cutoff_x = min_x + 0.499999 * abs(max_x - min_x)
    tolerance = 1e-9

    for v in V_new:
        assert v[0] >= cutoff_x - tolerance

    # both hemispheres along Z should still be represented, since Z was
    # never truncated
    zs = [v[2] for v in V_new]
    assert min(zs) < 0 < max(zs)


#
# face clipping: hand-constructed single triangles covering all 4
# vertex-classification cases (0/1/2/3 vertices surviving the cut),
# checked against exactly-hand-computed crossing points and, for the
# quadrilateral case, an independently-computed (cross-product) area
# rather than just re-deriving the same interpolation formula.
#

def _triangle_areas(V, F):
    areas = []
    for f in F:
        a, b, c = (np.asarray(V[i]) for i in f)
        areas.append(0.5 * np.linalg.norm(np.cross(b - a, c - a)))
    return areas


def test_clip_face_fully_above_cutoff_is_kept_unchanged():
    V = [np.array([0., 0., 2.]), np.array([4., 0., 2.]), np.array([0., 4., 2.])]
    C = [[0, 1], [1, 2], [2, 0]]
    F = [[0, 1, 2]]

    V_new, C_new, F_new = truncate(V, C, 0.0, axis=2, F_sphere=F)

    assert len(F_new) == 1
    coords = [tuple(V_new[i]) for i in F_new[0]]
    assert coords == [tuple(v) for v in V]


def test_clip_face_fully_below_cutoff_is_dropped():
    # z-range is 0..1 here so cutoff_from_bottom=2.0 (cutoff=2) sits
    # strictly above every vertex, rather than degenerately at z=0
    V = [np.array([0., 0., 0.]), np.array([4., 0., 1.]), np.array([0., 4., 0.])]
    C = [[0, 1], [1, 2], [2, 0]]
    F = [[0, 1, 2]]

    _, _, F_new = truncate(V, C, 2.0, axis=2, F_sphere=F)

    assert F_new == []


def test_clip_face_one_vertex_above_cutoff_produces_a_smaller_triangle():
    # A is kept (z=2, above cutoff=1); B and C are discarded (z=0)
    A = np.array([0., 0., 2.])
    B = np.array([4., 0., 0.])
    C = np.array([0., 4., 0.])
    V = [A, B, C]
    edges = [[0, 1], [1, 2], [2, 0]]

    # cutoff = min_z + cutoff_from_bottom * range = 0 + 0.5*2 = 1
    V_new, C_new, F_new = truncate(V, edges, 0.5, axis=2, F_sphere=[[0, 1, 2]])

    assert len(F_new) == 1
    coords = [tuple(V_new[i]) for i in F_new[0]]
    # hand-computed: edge A-B crosses z=1 at its midpoint (2, 0, 1);
    # edge C-A crosses z=1 at its midpoint (0, 2, 1) -- winding order
    # preserved as [kept vertex, crossing on the edge leaving it,
    # crossing on the edge arriving at it]
    expected = [(0., 0., 2.), (2., 0., 1.), (0., 2., 1.)]
    for actual, exp in zip(coords, expected):
        assert actual == pytest.approx(exp)


def test_clip_face_two_vertices_above_cutoff_produces_a_quad_split_into_two_triangles():
    # A is discarded (z=0, below cutoff=1); B and C are kept (z=2)
    A = np.array([0., 0., 0.])
    B = np.array([4., 0., 2.])
    C = np.array([0., 4., 2.])
    V = [A, B, C]
    edges = [[0, 1], [1, 2], [2, 0]]

    V_new, C_new, F_new = truncate(V, edges, 0.5, axis=2, F_sphere=[[0, 1, 2]])

    assert len(F_new) == 2

    original_area = 0.5 * np.linalg.norm(np.cross(B - A, C - A))
    kept_area = sum(_triangle_areas(V_new, F_new))
    # the discarded corner (A, midpoint(A,B), midpoint(C,A)) is similar
    # to the original triangle with a 0.5 side-length ratio (both cut
    # edges are crossed at their exact midpoints here), so it accounts
    # for 0.25 of the original area, independent of the interpolation
    # formula used to place the cut points -- an independently-derived
    # check, not a restatement of the clipping code.
    assert kept_area == pytest.approx(0.75 * original_area)

    # every triangle in the split quad must still be a real, non-
    # degenerate triangle
    for area in _triangle_areas(V_new, F_new):
        assert area > 1e-9


def test_clip_face_reuses_the_same_crossing_point_as_the_bordering_chord():
    # the whole point of building faces and chords from one shared
    # edge_to_new_vertex lookup is that a clipped face's new vertex and
    # the chord running along that same edge land on the exact same
    # point, not two independently-rounded near duplicates
    A = np.array([0., 0., 2.])
    B = np.array([4., 0., 0.])
    C = np.array([0., 4., 0.])
    V = [A, B, C]
    edges = [[0, 1], [1, 2], [2, 0]]

    V_new, C_new, F_new = truncate(V, edges, 0.5, axis=2, F_sphere=[[0, 1, 2]])

    face_crossing_points = {tuple(V_new[i]) for i in F_new[0]} - {tuple(A)}
    chord_endpoint_points = set()
    for c in C_new:
        for idx in c:
            v = V_new[idx]
            if v[2] == pytest.approx(1.0):
                chord_endpoint_points.add(tuple(v))

    assert face_crossing_points <= chord_endpoint_points
