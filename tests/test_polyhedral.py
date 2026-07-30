import numpy as np
import pytest

from pylair.polyhedral import Vertex, Face, Chord, Octahedron, Icosahedron, Tetrahedron, build_lcd_faces


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
        (Tetrahedron, 4, 4, 6),
        (Octahedron, 6, 8, 12),
        (Icosahedron, 12, 20, 30),
    ],
)
def test_polyhedron_counts(polyhedron_cls, expected_vertices, expected_faces, expected_chords):
    poly = polyhedron_cls()
    assert len(poly.vertices) == expected_vertices
    assert len(poly.faces) == expected_faces
    assert len(poly.chords) == expected_chords


@pytest.mark.parametrize("polyhedron_cls", [Tetrahedron, Octahedron, Icosahedron])
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


@pytest.mark.parametrize(
    "polyhedron_cls,expected_lcd_count",
    [(Tetrahedron, 24), (Octahedron, 48), (Icosahedron, 120)],
)
def test_build_lcd_faces_produces_six_per_original_face(polyhedron_cls, expected_lcd_count):
    poly = polyhedron_cls()
    lcd_faces = build_lcd_faces(poly)
    assert len(lcd_faces) == expected_lcd_count == 6 * len(poly.faces)


def test_lcd_face_is_a_30_60_90_triangle_with_the_right_angle_at_the_midpoint():
    poly = Icosahedron()
    lcd_faces = build_lcd_faces(poly)
    CL = poly.ppt_side_length

    for face in lcd_faces[:6]:
        # v1=original vertex, v2=edge midpoint (right angle), v3=centroid
        leg_v1v2 = face.v1.distance_to(face.v2)
        leg_v2v3 = face.v2.distance_to(face.v3)
        hyp_v1v3 = face.v1.distance_to(face.v3)

        assert leg_v1v2 == pytest.approx(CL / 2.)
        assert leg_v2v3 == pytest.approx(CL * np.sqrt(3.) / 6.)
        assert hyp_v1v3 == pytest.approx(CL / np.sqrt(3.))
        # right angle at v2: (v1-v2) . (v3-v2) should be 0
        a = face.v1.xyz - face.v2.xyz
        b = face.v3.xyz - face.v2.xyz
        assert np.dot(a, b) == pytest.approx(0., abs=1e-9)


def test_lcd_faces_centroid_is_shared_original_face_centroid():
    poly = Icosahedron()
    lcd_faces = build_lcd_faces(poly)
    # the first 6 LCD faces come from the same original face and should
    # all share the exact same centroid (v3, per build_lcd_faces's
    # (vertex, midpoint, centroid) argument order)
    centroids = [f.v3.xyz for f in lcd_faces[:6]]
    for c in centroids[1:]:
        assert c == pytest.approx(centroids[0])
    assert centroids[0] == pytest.approx(poly.faces[0].origin)
