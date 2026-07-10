import numpy as np
import pytest

from Polyhedral import Vertex, Face, Chord, Octahedron, Icosahedron


def test_vertex_distance_to():
    a = Vertex(0., 0., 0.)
    b = Vertex(3., 4., 0.)
    assert a.distance_to(b) == pytest.approx(5.0)


def test_face_origin_is_centroid():
    v1 = Vertex(0., 0., 0.)
    v2 = Vertex(3., 0., 0.)
    v3 = Vertex(0., 3., 0.)
    face = Face(v1, v2, v3)
    assert face.origin == pytest.approx(np.array([1., 1., 0.]))


def test_face_transfer_matrix_x_axis_is_unit_length():
    v1 = Vertex(0., 0., 0.)
    v2 = Vertex(3., 0., 0.)
    v3 = Vertex(0., 3., 0.)
    face = Face(v1, v2, v3)
    x_axis = np.asarray(face.transfer_matrix)[:, 0]
    assert np.linalg.norm(x_axis) == pytest.approx(1.0)


@pytest.mark.parametrize(
    "polyhedron_cls,expected_vertices,expected_faces,expected_chords",
    [
        (Octahedron, 6, 8, 12),
        (Icosahedron, 12, 20, 30),
    ],
)
def test_polyhedron_counts(polyhedron_cls, expected_vertices, expected_faces, expected_chords):
    poly = polyhedron_cls()
    assert len(poly.vertices) == expected_vertices
    assert len(poly.faces) == expected_faces
    assert len(poly.chords) == expected_chords


@pytest.mark.parametrize("polyhedron_cls", [Octahedron, Icosahedron])
def test_polyhedron_vertices_lie_on_unit_sphere(polyhedron_cls):
    poly = polyhedron_cls()
    for v in poly.vertices:
        assert np.linalg.norm(v.xyz) == pytest.approx(1.0)


def test_ppt_side_length_matches_first_edge():
    poly = Icosahedron()
    expected = poly.vertices[0].distance_to(poly.vertices[1])
    assert poly.ppt_side_length == pytest.approx(expected)


def test_chord_stores_endpoints():
    v1 = Vertex(0., 0., 0.)
    v2 = Vertex(1., 1., 1.)
    c = Chord(v1, v2)
    assert c.v1 is v1
    assert c.v2 is v2
