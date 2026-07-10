import pytest

from pydome.polyhedral import Icosahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle


@pytest.mark.parametrize("frequency", [1, 2, 3, 4, 6])
def test_symmetry_triangle_counts_match_triangulation_formulas(frequency):
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(frequency, poly)

    expected_vertices = (frequency + 1) * (frequency + 2) // 2
    expected_faces = frequency ** 2
    # Euler's formula for a triangulated disk: V - E + F = 1
    expected_chords = expected_vertices + expected_faces - 1

    assert len(st.vertices) == expected_vertices
    assert len(st.face_list) == expected_faces
    assert len(st.chord_list) == expected_chords


def test_symmetry_triangle_vertices_are_planar_at_z_zero():
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(4, poly)
    for v in st.vertices:
        assert v.xyz[2] == 0.


def test_convert_rc_notation_to_vertex_index_is_unique_and_0_indexed():
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(3, poly)

    seen = set()
    for r in range(len(st.row_list)):
        for c in range(len(st.row_list[r])):
            n = st.convertRCNotationToVertexIndex(r, c)
            assert n not in seen
            seen.add(n)

    assert seen == set(range(len(st.vertices)))


def test_face_list_references_valid_vertex_indices():
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(4, poly)
    num_vertices = len(st.vertices)
    for face in st.face_list:
        for n in face:
            assert 0 <= n < num_vertices


def test_chord_list_references_valid_vertex_indices():
    poly = Icosahedron()
    st = ClassOneMethodOneSymmetryTriangle(4, poly)
    num_vertices = len(st.vertices)
    for chord in st.chord_list:
        for n in chord:
            assert 0 <= n < num_vertices
