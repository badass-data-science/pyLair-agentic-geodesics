import numpy as np
import pytest

from pydome.polyhedral import Icosahedron, Octahedron
from pydome.symmetry_triangle import ClassOneMethodOneSymmetryTriangle
from pydome.geodesic_sphere import GeodesicSphere
from pydome.bill_of_materials import compute_face_data, compute_dihedral_angles
from pydome.output import OutputOBJ, OutputFaceTemplateDXF
from pydome.api import build_dome


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


# Z-only face-aware truncation (truncate() clipping F_sphere against the
# cutoff plane): independent ground truth via trimesh's own mesh-slicing
# routine, run against the *untruncated* dome's OBJ export and cut at the
# exact same plane pyDome computes internally, rather than comparing our
# clipping code to itself.

@pytest.mark.parametrize("polyhedron,frequency,cutoff", [
    ("icosahedron", 3, 0.499999),
    ("icosahedron", 4, 0.333333),
    ("octahedron", 3, 0.499999),
    ("octahedron", 4, 0.6),
])
def test_z_truncated_faces_match_trimesh_slice_mesh_plane_oracle(tmp_path, polyhedron, frequency, cutoff):
    trimesh = pytest.importorskip("trimesh")

    truncated = build_dome(frequency=frequency, polyhedron=polyhedron, truncation_z=cutoff)
    assert truncated.F_sphere is not None

    full = build_dome(frequency=frequency, polyhedron=polyhedron)
    obj_path = tmp_path / "full.obj"
    OutputOBJ(full.V, full.F_sphere, str(obj_path))
    mesh = trimesh.load(str(obj_path), process=False)

    # replicate pyDome's own cutoff-plane computation (see truncation.py)
    # so trimesh is asked to cut at exactly the same plane, not an
    # independently-guessed one
    zs = [v[2] for v in full.V]
    min_z, max_z = min(zs), max(zs)
    plane_z = min_z + cutoff * (max_z - min_z)

    sliced = trimesh.intersections.slice_mesh_plane(
        mesh, plane_normal=[0., 0., 1.], plane_origin=[0., 0., plane_z])

    our_area = sum(fd['area'] for fd in compute_face_data(truncated.V, truncated.F_sphere))
    assert our_area == pytest.approx(sliced.area, rel=1e-6)

    # every original triangle contributes 0, 1, or 2 output triangles
    # under a planar cut regardless of which of the two possible
    # diagonals a quad gets split along, so face counts should match
    # exactly even though trimesh's triangulation choice for the
    # straddling case need not match ours vertex-for-vertex
    assert len(truncated.F_sphere) == len(sliced.faces)


@pytest.mark.parametrize("frequency,cutoff", [(3, 0.499999), (4, 0.333333)])
def test_z_truncated_faces_are_watertight_except_at_the_open_cut_boundary(frequency, cutoff):
    # a structural invariant checked independently of any oracle library:
    # every edge of the clipped face set must be shared by exactly 2
    # faces (an interior edge) or exactly 1 (the open boundary ring left
    # by not capping the cut) -- never 0 (a gap/hole) or 3+ (an
    # overlapping/self-intersecting clip).
    dome = build_dome(frequency=frequency, truncation_z=cutoff)
    assert dome.F_sphere is not None

    edge_face_count = {}
    for f in dome.F_sphere:
        a, b, c = f
        for u, v in ((a, b), (b, c), (c, a)):
            key = frozenset((u, v))
            edge_face_count[key] = edge_face_count.get(key, 0) + 1

    assert set(edge_face_count.values()) <= {1, 2}
    assert 1 in edge_face_count.values()  # the open boundary ring exists
    assert 2 in edge_face_count.values()  # and interior edges exist too
