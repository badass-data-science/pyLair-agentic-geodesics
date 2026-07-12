import numpy as np
import pytest

from pydome.polyhedral import Icosahedron, Octahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.bill_of_materials import compute_face_data, compute_dihedral_angles
from pydome.output import OutputOBJ, OutputFaceTemplateDXF


# Independent, dev-time-only cross-checks of the face-geometry math added
# alongside the panel Bill of Materials -- these libraries are never a
# pyDome runtime dependency (install with `pip install -e ".[verify]"`),
# same role antitile played for verifying Class III (see README).
# pytest.importorskip means the rest of the suite stays green without
# them installed.


def build_sphere_with_faces(frequency, polyhedron):
    st = ClassOneMethodOneSymmetryTriangle(frequency, polyhedron)
    sphere = GeodesicSphere(polyhedron, st, 1e-7, 1.0)
    return sphere.sphere_vertices, sphere.non_duplicate_chords, sphere.non_duplicate_face_nodes


@pytest.mark.parametrize("polyhedron_cls,frequency", [
    (Icosahedron, 1),
    (Icosahedron, 3),
    (Icosahedron, 4),
    (Octahedron, 1),
    (Octahedron, 3),
])
def test_face_areas_and_dihedral_angles_match_trimesh_oracle(tmp_path, polyhedron_cls, frequency):
    # trimesh independently derives face areas and the angle between
    # adjacent faces' normals straight from the OBJ mesh pyDome already
    # exports -- a completely separate implementation from our own
    # compute_face_data/compute_dihedral_angles, run on the OBJ file
    # itself rather than our in-memory arrays, so this exercises the
    # OutputOBJ writer too.
    trimesh = pytest.importorskip("trimesh")

    V, C, F = build_sphere_with_faces(frequency, polyhedron_cls())
    obj_path = tmp_path / "dome.obj"
    OutputOBJ(V, F, str(obj_path))
    mesh = trimesh.load(str(obj_path), process=False)

    face_data = compute_face_data(V, F)
    our_areas = sorted(fd['area'] for fd in face_data)
    trimesh_areas = sorted(mesh.area_faces)
    assert our_areas == pytest.approx(trimesh_areas, abs=1e-9)

    ours = {
        frozenset((row['vertex 1'], row['vertex 2'])): row['dihedral angle (degrees)']
        for row in compute_dihedral_angles(face_data, C)
    }

    # trimesh's face_adjacency_angles is the angle between adjacent
    # faces' outward normals -- our "normal_angle" (180 - our reported
    # interior dihedral angle) -- keyed by face_adjacency_edges, so
    # match on the shared-vertex-pair rather than assuming index
    # alignment with our own chord list.
    trimesh_normal_angles = np.degrees(mesh.face_adjacency_angles)
    checked = 0
    for edge, normal_angle in zip(mesh.face_adjacency_edges, trimesh_normal_angles):
        key = frozenset(int(v) for v in edge)
        if key in ours:
            assert (180. - normal_angle) == pytest.approx(ours[key], abs=1e-6)
            checked += 1
    assert checked == len(ours)


def test_face_template_dxf_geometry_matches_ezdxf_parse(tmp_path):
    # ezdxf reads the generated cutting template back out of the DXF
    # file (not our in-memory edge_lengths) and independently recovers
    # each vertex's 2D position from the parsed LINE entities, which
    # validates OutputFaceTemplateDXF's law-of-cosines placement through
    # a parse-then-measure path rather than re-deriving the same
    # trigonometry in the test.
    ezdxf = pytest.importorskip("ezdxf")

    edge_lengths = (0.4, 0.45, 0.5)
    out_file = tmp_path / "face.dxf"
    OutputFaceTemplateDXF(edge_lengths, str(out_file))

    doc = ezdxf.readfile(str(out_file))
    lines = list(doc.modelspace().query("LINE"))
    assert len(lines) == 3

    points = []
    for line in lines:
        points.append(np.array(line.dxf.start)[:2])
        points.append(np.array(line.dxf.end)[:2])

    unique_vertices = []
    for p in points:
        if not any(np.linalg.norm(p - u) < 1e-9 for u in unique_vertices):
            unique_vertices.append(p)
    assert len(unique_vertices) == 3

    recovered_lengths = sorted(
        np.linalg.norm(unique_vertices[i] - unique_vertices[j])
        for i in range(3) for j in range(i + 1, 3)
    )
    assert recovered_lengths == pytest.approx(sorted(edge_lengths), abs=1e-6)
