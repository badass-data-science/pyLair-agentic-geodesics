import numpy as np

from Output import OutputDXF, OutputWireframeVRML, OutputFaceVRML


def make_triangle():
    V = [np.array([0., 0., 0.]), np.array([1., 0., 0.]), np.array([0., 1., 0.])]
    C = [[1, 2], [2, 3], [3, 1]]
    F = [[1, 2, 3]]
    return V, C, F


def test_output_dxf_writes_one_line_entity_per_chord(tmp_path):
    V, C, _ = make_triangle()
    out_file = tmp_path / "test.dxf"
    OutputDXF(V, C, str(out_file))

    content = out_file.read_text()
    assert content.startswith("0\nSECTION\n2\nENTITIES\n")
    assert content.rstrip().endswith("0\nENDSEC\n0\nEOF")
    assert content.count("LINE\n") == len(C)


def test_output_wireframe_vrml_contains_all_points_and_indices(tmp_path):
    V, C, _ = make_triangle()
    out_file = tmp_path / "test.wrl"
    OutputWireframeVRML(V, C, str(out_file))

    content = out_file.read_text()
    assert content.startswith("#VRML V2.0 utf8")
    assert "IndexedLineSet" in content
    for v in V:
        assert f"{v[0]} {v[1]} {v[2]}," in content
    for c in C:
        assert f"{c[0]-1} {c[1]-1} -1," in content


def test_output_face_vrml_contains_face_indices(tmp_path):
    V, _, F = make_triangle()
    out_file = tmp_path / "test_face.wrl"
    OutputFaceVRML(V, F, str(out_file))

    content = out_file.read_text()
    assert content.startswith("#VRML V2.0 utf8")
    assert "IndexedFaceSet" in content
    for f in F:
        assert f"{f[0]-1}, {f[1]-1}, {f[2]-1}, -1," in content
