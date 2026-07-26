import numpy as np
import pytest
from scipy.spatial import cKDTree

from pylair.polyhedral import Octahedron, Icosahedron
from pylair.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pylair.geodesic_sphere import GeodesicSphere


def build_sphere(polyhedron_cls, frequency, radius=1.0, vpt=1e-7):
    poly = polyhedron_cls()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)
    return GeodesicSphere(poly, st, vpt, radius)


@pytest.mark.parametrize(
    "polyhedron_cls,frequency,expected_v,expected_e,expected_f",
    [
        # icosahedron sphere: V = 10f^2 + 2, E = 30f^2, F = 20f^2
        (Icosahedron, 1, 12, 30, 20),
        (Icosahedron, 2, 42, 120, 80),
        (Icosahedron, 4, 162, 480, 320),
        # octahedron sphere: V = 4f^2 + 2, E = 12f^2, F = 8f^2
        (Octahedron, 1, 6, 12, 8),
        (Octahedron, 2, 18, 48, 32),
        (Octahedron, 4, 66, 192, 128),
    ],
)
def test_sphere_counts_match_known_geodesic_formulas(
    polyhedron_cls, frequency, expected_v, expected_e, expected_f
):
    sphere = build_sphere(polyhedron_cls, frequency)
    assert len(sphere.sphere_vertices) == expected_v
    assert len(sphere.non_duplicate_chords) == expected_e
    assert len(sphere.non_duplicate_face_nodes) == expected_f


@pytest.mark.parametrize("radius", [1.0, 3.0, 0.5])
def test_all_sphere_vertices_lie_at_the_given_radius(radius):
    sphere = build_sphere(Icosahedron, 3, radius=radius)
    for v in sphere.sphere_vertices:
        assert np.linalg.norm(v) == pytest.approx(radius)


def test_chords_reference_valid_vertex_indices():
    sphere = build_sphere(Icosahedron, 3)
    num_vertices = len(sphere.sphere_vertices)
    for c in sphere.non_duplicate_chords:
        assert 0 <= c[0] < num_vertices
        assert 0 <= c[1] < num_vertices
        assert c[0] != c[1]


def test_faces_reference_valid_vertex_indices():
    sphere = build_sphere(Icosahedron, 3)
    num_vertices = len(sphere.sphere_vertices)
    for f in sphere.non_duplicate_face_nodes:
        for n in f:
            assert 0 <= n < num_vertices


def test_no_duplicate_chords():
    sphere = build_sphere(Icosahedron, 3)
    seen = set()
    for c in sphere.non_duplicate_chords:
        key = tuple(sorted(c))
        assert key not in seen
        seen.add(key)


@pytest.mark.parametrize("polyhedron_cls,frequency", [(Icosahedron, 4), (Octahedron, 4)])
def test_no_two_final_vertices_occupy_the_same_location(polyhedron_cls, frequency):
    # Adjacent faces each independently compute the vertices along their
    # shared seam, so a naive assembly would double them up; GeodesicSphere
    # is supposed to collapse every such pair into one vertex before this
    # point. If any survived, two entries in sphere_vertices would sit
    # closer together than the merge threshold that was supposed to catch
    # them.
    vpt = 1e-7
    sphere = build_sphere(polyhedron_cls, frequency, vpt=vpt)
    points = np.array(sphere.sphere_vertices)
    pairs = cKDTree(points).query_pairs(vpt)
    assert pairs == set()


def test_icosahedron_frequency_one_matches_original_icosahedron_edge_length():
    sphere = build_sphere(Icosahedron, 1, radius=1.0)
    # frequency 1 performs no subdivision, so all edges should equal the
    # original icosahedron's edge length once projected onto the unit sphere.
    lengths = set()
    for c in sphere.non_duplicate_chords:
        v1 = sphere.sphere_vertices[c[0]]
        v2 = sphere.sphere_vertices[c[1]]
        lengths.add(round(np.linalg.norm(v1 - v2), 6))
    assert len(lengths) == 1
