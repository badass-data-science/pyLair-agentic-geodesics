import pytest

from pylair.polyhedral import Icosahedron, build_lcd_faces
from pylair.symmetry_triangle import ClassOneMethodOneSymmetryTriangle, ClassTwoMethodOneSymmetryTriangle


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


@pytest.mark.parametrize("m", [1, 2, 3, 4])
def test_class_two_symmetry_triangle_counts_match_triangulation_formulas(m):
    # ClassTwoMethodOneSymmetryTriangle reuses SymmetryTriangle's generic
    # row/col chord_list and face_list construction unchanged, so it
    # must satisfy the exact same combinatorial formulas as Class I,
    # regardless of the LCD triangle's different (non-equilateral) shape.
    poly = Icosahedron()
    st = ClassTwoMethodOneSymmetryTriangle(m, poly)

    expected_vertices = (m + 1) * (m + 2) // 2
    expected_faces = m ** 2
    expected_chords = expected_vertices + expected_faces - 1

    assert len(st.vertices) == expected_vertices
    assert len(st.face_list) == expected_faces
    assert len(st.chord_list) == expected_chords


def test_class_two_symmetry_triangle_vertices_are_planar_at_z_zero():
    poly = Icosahedron()
    st = ClassTwoMethodOneSymmetryTriangle(3, poly)
    for v in st.vertices:
        assert v.xyz[2] == 0.


def test_class_two_local_corners_reconstruct_the_true_3d_lcd_triangle_corners():
    # Regression test for a real bug: the LCD triangle's x_dir/y_dir
    # basis (from Face.transfer_matrix) is NOT orthogonal, unlike Class
    # I's equilateral case, so an earlier version of this class (which
    # assumed orthogonality) silently produced wrong geometry -- valid
    # per-LCD-triangle shape, but positioned incorrectly in 3D, which
    # broke vertex merging across the whole sphere (detected via Euler's
    # formula V-E+F=2 and 2E=3F failing). Verify the 3 corners map back
    # to the LCD face's actual v1/v2/v3 exactly.
    poly = Icosahedron()
    lcd_faces = build_lcd_faces(poly)
    m = 3
    st = ClassTwoMethodOneSymmetryTriangle(m, poly)

    idx_A = st.convertRCNotationToVertexIndex(0, 0)
    idx_M = st.convertRCNotationToVertexIndex(0, m)
    idx_G = st.convertRCNotationToVertexIndex(m, 0)

    for face in lcd_faces[:6]:
        origin = face.origin
        matrix = face.transfer_matrix
        computed_A = matrix @ st.vertices[idx_A].xyz + origin
        computed_M = matrix @ st.vertices[idx_M].xyz + origin
        computed_G = matrix @ st.vertices[idx_G].xyz + origin

        assert computed_A == pytest.approx(face.v1.xyz)
        assert computed_M == pytest.approx(face.v2.xyz)
        assert computed_G == pytest.approx(face.v3.xyz)
