import numpy as np
import pytest
from scipy.spatial import cKDTree

from pylair.polyhedral import Octahedron, Icosahedron
from pylair.class_three import ClassThreeSymmetryTriangle
from pylair.geodesic_sphere import GeodesicSphere


def build_class_three_sphere(polyhedron_cls, m, n, radius=1.0, vpt=1e-7):
    poly = polyhedron_cls()
    st = ClassThreeSymmetryTriangle(m, n, poly)
    return GeodesicSphere(poly, st, vpt, radius,
                           extra_pairs=st.cross_face_matches,
                           local_priority=st.local_priority)


@pytest.mark.parametrize(
    "polyhedron_cls,m,n,expected_v,expected_e,expected_f",
    [
        # T = m^2 + mn + n^2. Icosahedron: V=10T+2, E=30T, F=20T.
        # Octahedron: V=4T+2, E=12T, F=8T. These match the same family of
        # golden-value formulas as Class I (T=f^2) and Class II (T=3m^2),
        # and were verified two ways: (1) empirically against Euler's
        # formula (V-E+F=2, 2E=3F) and (2) bit-for-bit against the
        # antitile library's independent Goldberg-Coxeter implementation
        # (used as an external oracle during development, not a runtime
        # dependency) -- the full sorted, mean-normalized edge-length
        # distribution matched antitile's to within 1e-15 for several
        # (m,n) pairs on both base polyhedra.
        (Icosahedron, 2, 1, 72, 210, 140),      # T=7
        (Icosahedron, 3, 1, 132, 390, 260),     # T=13
        (Icosahedron, 3, 2, 192, 570, 380),     # T=19
        (Icosahedron, 4, 1, 212, 630, 420),     # T=21
        (Octahedron, 2, 1, 30, 84, 56),         # T=7
        (Octahedron, 3, 2, 78, 228, 152),       # T=19
    ],
)
def test_class_three_sphere_counts_match_verified_formulas(
    polyhedron_cls, m, n, expected_v, expected_e, expected_f
):
    sphere = build_class_three_sphere(polyhedron_cls, m, n)
    assert len(sphere.sphere_vertices) == expected_v
    assert len(sphere.non_duplicate_chords) == expected_e
    assert len(sphere.non_duplicate_face_nodes) == expected_f


@pytest.mark.parametrize("m,n", [(2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 2)])
def test_class_three_sphere_satisfies_euler_formula(m, n):
    sphere = build_class_three_sphere(Icosahedron, m, n)
    V = len(sphere.sphere_vertices)
    E = len(sphere.non_duplicate_chords)
    F = len(sphere.non_duplicate_face_nodes)
    assert V - E + F == 2
    assert 2 * E == 3 * F


@pytest.mark.parametrize("polyhedron_cls,m,n", [(Icosahedron, 3, 2), (Octahedron, 3, 2)])
def test_class_three_no_two_final_vertices_occupy_the_same_location(polyhedron_cls, m, n):
    # Same guarantee GeodesicSphere has always provided for Class I/II:
    # a vertex that's genuinely shared between adjacent faces must
    # collapse to one entry in sphere_vertices, not survive as several
    # near-identical ones. Class III adds "halo" points (see
    # class_three.py) specifically to make this merging possible for a
    # chiral lattice, so this also guards against a halo point that
    # fails to merge and lingers as a stray near-duplicate vertex.
    vpt = 1e-7
    sphere = build_class_three_sphere(polyhedron_cls, m, n, vpt=vpt)
    points = np.array(sphere.sphere_vertices)
    pairs = cKDTree(points).query_pairs(vpt)
    assert pairs == set()


def test_class_three_cross_face_matches_are_necessary_not_just_helpful():
    # Regression guard for the actual bug this feature was built around:
    # proximity-only merging (GeodesicSphere's original Class I/II
    # mechanism, i.e. omitting extra_pairs/local_priority) is NOT enough
    # for a chiral lattice -- it only merges the 3 face corners, leaving
    # every other genuinely-shared edge vertex duplicated once per
    # adjacent face. If this test ever starts passing, it means
    # cross_face_matches stopped doing anything, which would silently
    # reintroduce the original bug (30 unsubdivided icosahedron edges).
    poly = Icosahedron()
    m, n = 3, 2
    T = m * m + m * n + n * n
    st = ClassThreeSymmetryTriangle(m, n, poly)

    proximity_only = GeodesicSphere(poly, st, vpt=1e-7, radius=1.0)
    with_stitching = GeodesicSphere(poly, st, vpt=1e-7, radius=1.0,
                                     extra_pairs=st.cross_face_matches,
                                     local_priority=st.local_priority)

    assert len(proximity_only.non_duplicate_vertices) > len(with_stitching.non_duplicate_vertices)
    assert len(with_stitching.non_duplicate_vertices) == 10 * T + 2


def test_class_three_has_no_anomalously_long_chords():
    # Regression test for the actual bug found and fixed during
    # development: a first (proximity-based-merge-only) implementation
    # left every original icosahedron edge as a single unsubdivided
    # chord -- 30 chords at the full, un-subdivided polyhedron edge
    # length (~4-5x the typical strut length), because a chiral lattice's
    # near-edge points don't coincide in 3D across adjacent faces the
    # way Class I/II's do. A correctly stitched Class III mesh has all
    # strut lengths within a modest ratio of one another (matching the
    # antitile oracle's own ~1.35x max/min ratio for this (m,n)).
    sphere = build_class_three_sphere(Icosahedron, 3, 2)
    verts = np.array(sphere.sphere_vertices)
    lengths = np.array([np.linalg.norm(verts[a] - verts[b])
                         for a, b in sphere.non_duplicate_chords])
    assert lengths.max() / lengths.min() < 2.0


@pytest.mark.parametrize("radius", [1.0, 3.0, 0.5])
def test_class_three_sphere_vertices_lie_at_the_given_radius(radius):
    sphere = build_class_three_sphere(Icosahedron, 3, 2, radius=radius)
    for v in sphere.sphere_vertices:
        assert np.linalg.norm(v) == pytest.approx(radius)


def test_class_three_no_duplicate_chords():
    sphere = build_class_three_sphere(Icosahedron, 3, 2)
    seen = set()
    for c in sphere.non_duplicate_chords:
        key = tuple(sorted(c))
        assert key not in seen
        seen.add(key)


def test_class_three_no_duplicate_faces():
    # Boundary-straddling faces are independently generated by both
    # adjacent polyhedron faces and must be deduplicated after vertex
    # merging (see GeodesicSphere.relabel_face_nodes).
    sphere = build_class_three_sphere(Icosahedron, 3, 2)
    seen = set()
    for f in sphere.non_duplicate_face_nodes:
        key = tuple(sorted(f))
        assert key not in seen
        seen.add(key)


def test_class_three_chords_and_faces_reference_valid_vertex_indices():
    sphere = build_class_three_sphere(Icosahedron, 3, 2)
    num_vertices = len(sphere.sphere_vertices)
    for c in sphere.non_duplicate_chords:
        assert 0 <= c[0] < num_vertices
        assert 0 <= c[1] < num_vertices
        assert c[0] != c[1]
    for f in sphere.non_duplicate_face_nodes:
        for idx in f:
            assert 0 <= idx < num_vertices


def test_class_three_mirror_pair_has_same_counts_and_total_length():
    # (m,n) and (n,m) are mirror-image (chiral) domes of the same size:
    # same T, so same V/E/F and total strut length, but not necessarily
    # the same specific chord-length multiset (a genuine chiral pattern
    # has no reflection symmetry).
    sphere_a = build_class_three_sphere(Icosahedron, 3, 2)
    sphere_b = build_class_three_sphere(Icosahedron, 2, 3)
    assert len(sphere_a.sphere_vertices) == len(sphere_b.sphere_vertices)
    assert len(sphere_a.non_duplicate_chords) == len(sphere_b.non_duplicate_chords)
    assert len(sphere_a.non_duplicate_face_nodes) == len(sphere_b.non_duplicate_face_nodes)

    def total_length(sphere):
        verts = np.array(sphere.sphere_vertices)
        return sum(np.linalg.norm(verts[a] - verts[b])
                   for a, b in sphere.non_duplicate_chords)

    assert total_length(sphere_a) == pytest.approx(total_length(sphere_b))
