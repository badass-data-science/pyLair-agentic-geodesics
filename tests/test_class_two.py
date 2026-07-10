from types import SimpleNamespace

import numpy as np
import pytest

from pydome.polyhedral import Octahedron, Icosahedron, build_lcd_faces
from pydome.symmetry_triangle import ClassTwoMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere


def build_class_two_sphere(polyhedron_cls, dome_frequency, radius=1.0, vpt=1e-7):
    poly = polyhedron_cls()
    m = dome_frequency // 2
    st = ClassTwoMethodOneSymmetryTriangle(m, poly)
    face_source = SimpleNamespace(faces=build_lcd_faces(poly))
    return GeodesicSphere(face_source, st, vpt, radius)


@pytest.mark.parametrize(
    "polyhedron_cls,dome_frequency,expected_v,expected_e,expected_f",
    [
        # icosahedron Class II: V = 60m^2 + 2, E = 180m^2, F = 120m^2
        # (m = dome_frequency / 2), verified empirically against Euler's
        # formula (V-E+F=2) and 2E=3F holding exactly, after fixing the
        # oblique-basis bug this feature was built to catch.
        (Icosahedron, 2, 62, 180, 120),
        (Icosahedron, 4, 242, 720, 480),
        (Icosahedron, 6, 542, 1620, 1080),
        # octahedron Class II: V = 24m^2 + 2, E = 72m^2, F = 48m^2
        (Octahedron, 2, 26, 72, 48),
        (Octahedron, 4, 98, 288, 192),
        (Octahedron, 6, 218, 648, 432),
    ],
)
def test_class_two_sphere_counts_match_verified_formulas(
    polyhedron_cls, dome_frequency, expected_v, expected_e, expected_f
):
    sphere = build_class_two_sphere(polyhedron_cls, dome_frequency)
    assert len(sphere.sphere_vertices) == expected_v
    assert len(sphere.non_duplicate_chords) == expected_e
    assert len(sphere.non_duplicate_face_nodes) == expected_f


@pytest.mark.parametrize("dome_frequency", [2, 4, 6, 8])
def test_class_two_sphere_satisfies_euler_formula(dome_frequency):
    # V - E + F = 2 must hold for any closed triangulated sphere-topology
    # mesh; this is what originally caught the oblique-basis bug (it was
    # violated -- 2x too many chords -- before the fix).
    sphere = build_class_two_sphere(Icosahedron, dome_frequency)
    V = len(sphere.sphere_vertices)
    E = len(sphere.non_duplicate_chords)
    F = len(sphere.non_duplicate_face_nodes)
    assert V - E + F == 2
    assert 2 * E == 3 * F


@pytest.mark.parametrize("radius", [1.0, 3.0, 0.5])
def test_class_two_sphere_vertices_lie_at_the_given_radius(radius):
    sphere = build_class_two_sphere(Icosahedron, 4, radius=radius)
    for v in sphere.sphere_vertices:
        assert np.linalg.norm(v) == pytest.approx(radius)


def test_class_two_no_duplicate_chords():
    sphere = build_class_two_sphere(Icosahedron, 4)
    seen = set()
    for c in sphere.non_duplicate_chords:
        key = tuple(sorted(c))
        assert key not in seen
        seen.add(key)


def test_class_two_chords_and_faces_reference_valid_vertex_indices():
    sphere = build_class_two_sphere(Icosahedron, 4)
    num_vertices = len(sphere.sphere_vertices)
    for c in sphere.non_duplicate_chords:
        assert 0 <= c[0] < num_vertices
        assert 0 <= c[1] < num_vertices
        assert c[0] != c[1]
    for f in sphere.non_duplicate_face_nodes:
        for n in f:
            assert 0 <= n < num_vertices
