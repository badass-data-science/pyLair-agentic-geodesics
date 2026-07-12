import numpy as np

from pydome.output import (
    OutputDXF,
    OutputWireframeVRML,
    OutputFaceVRML,
    OutputSTL,
    OutputOBJ,
    OutputHubConnectorTemplateDXF,
    OutputFaceTemplateDXF,
)


def make_triangle():
    V = [np.array([0., 0., 0.]), np.array([1., 0., 0.]), np.array([0., 1., 0.])]
    C = [[0, 1], [1, 2], [2, 0]]
    F = [[0, 1, 2]]
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
        assert f"{c[0]} {c[1]} -1," in content


def test_output_face_vrml_contains_face_indices(tmp_path):
    V, _, F = make_triangle()
    out_file = tmp_path / "test_face.wrl"
    OutputFaceVRML(V, F, str(out_file))

    content = out_file.read_text()
    assert content.startswith("#VRML V2.0 utf8")
    assert "IndexedFaceSet" in content
    for f in F:
        assert f"{f[0]}, {f[1]}, {f[2]}, -1," in content


def test_output_stl_writes_one_facet_per_face_with_correct_normal(tmp_path):
    V, _, F = make_triangle()
    out_file = tmp_path / "test.stl"
    OutputSTL(V, F, str(out_file))

    content = out_file.read_text()
    assert content.startswith("solid pydome\n")
    assert content.rstrip().endswith("endsolid pydome")
    assert content.count("facet normal") == len(F)
    assert content.count("vertex") == 3 * len(F)

    # the sample triangle lies flat in the XY plane with a
    # counterclockwise winding, so its normal should point along +Z
    assert "facet normal 0.0 0.0 1.0" in content


def test_output_obj_writes_1_indexed_face_references(tmp_path):
    V, _, F = make_triangle()
    out_file = tmp_path / "test.obj"
    OutputOBJ(V, F, str(out_file))

    content = out_file.read_text()
    vertex_lines = [line for line in content.splitlines() if line.startswith("v ")]
    face_lines = [line for line in content.splitlines() if line.startswith("f ")]

    assert len(vertex_lines) == len(V)
    assert len(face_lines) == len(F)
    # OBJ indices are 1-based, so face [0, 1, 2] must be written as "1 2 3"
    assert face_lines[0] == "f 1 2 3"


def test_output_hub_connector_template_dxf_writes_one_line_and_label_per_spoke(tmp_path):
    spoke_angles = {1: 0., 2: 90., 3: 180., 4: 270.}
    tangential_angles = {1: 5.0, 2: 6.0, 3: 7.0, 4: 8.0}
    out_file = tmp_path / "hub.dxf"

    OutputHubConnectorTemplateDXF(spoke_angles, tangential_angles, str(out_file), spoke_length=2.0)

    content = out_file.read_text()
    assert content.startswith("0\nSECTION\n2\nENTITIES\n")
    assert content.rstrip().endswith("0\nENDSEC\n0\nEOF")
    assert content.count("LINE\n") == len(spoke_angles)
    assert content.count("TEXT\n") == len(spoke_angles)

    for tangential in tangential_angles.values():
        assert ("%.2f deg" % tangential) in content


def test_output_face_template_dxf_writes_one_line_and_label_per_edge(tmp_path):
    edge_lengths = (3.0, 4.0, 5.0)
    out_file = tmp_path / "face.dxf"

    OutputFaceTemplateDXF(edge_lengths, str(out_file))

    content = out_file.read_text()
    assert content.startswith("0\nSECTION\n2\nENTITIES\n")
    assert content.rstrip().endswith("0\nENDSEC\n0\nEOF")
    assert content.count("LINE\n") == 3
    assert content.count("TEXT\n") == 3
    for length in edge_lengths:
        assert ("%.4f" % length) in content


def test_output_face_template_dxf_vertex_placement_matches_edge_lengths(tmp_path):
    # a 3-4-5 right triangle: A=(0,0), B=(3,0), and the law-of-cosines
    # placement should put C at exactly (3,4), reproducing |BC|=4 and
    # |CA|=5.
    edge_lengths = (3.0, 4.0, 5.0)
    out_file = tmp_path / "face.dxf"

    OutputFaceTemplateDXF(edge_lengths, str(out_file))

    content = out_file.read_text()
    lines = content.splitlines()
    endpoints = []
    for i, line in enumerate(lines):
        if line == "LINE":
            x0 = float(lines[i + lines[i:].index("10") + 1])
            y0 = float(lines[i + lines[i:].index("20") + 1])
            x1 = float(lines[i + lines[i:].index("11") + 1])
            y1 = float(lines[i + lines[i:].index("21") + 1])
            endpoints.append(((x0, y0), (x1, y1)))

    assert len(endpoints) == 3
    all_points = [p for edge in endpoints for p in edge]
    assert any(abs(x) < 1e-9 and abs(y) < 1e-9 for x, y in all_points)  # A
    assert any(abs(x - 3.0) < 1e-9 and abs(y) < 1e-9 for x, y in all_points)  # B
    assert any(abs(x - 3.0) < 1e-9 and abs(y - 4.0) < 1e-9 for x, y in all_points)  # C


def test_output_hub_connector_template_spoke_endpoints_match_the_given_angles(tmp_path):
    spoke_angles = {1: 0., 2: 90.}
    tangential_angles = {1: 0., 2: 0.}
    out_file = tmp_path / "hub.dxf"

    OutputHubConnectorTemplateDXF(spoke_angles, tangential_angles, str(out_file), spoke_length=1.0)

    content = out_file.read_text()
    # a LINE entity's endpoint is given by group codes 11/21 (x/y);
    # spoke 1 (0 degrees) should end near x=1,y=0; spoke 2 (90 degrees)
    # should end near x=0,y=1
    lines = content.splitlines()
    endpoints = []
    for i, line in enumerate(lines):
        if line == "LINE":
            x = float(lines[i + lines[i:].index("11") + 1])
            y = float(lines[i + lines[i:].index("21") + 1])
            endpoints.append((x, y))

    assert len(endpoints) == 2
    assert any(abs(x - 1.0) < 1e-9 and abs(y) < 1e-9 for x, y in endpoints)
    assert any(abs(x) < 1e-9 and abs(y - 1.0) < 1e-9 for x, y in endpoints)
