#    pyLair:  A geodesic dome calculator
#    Copyright (c) 2013 Emily Williams
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.

import numpy as np

from .polyhedral import Vertex, compute_face_adjacency

PI = np.pi


def _lattice_to_xy(p, q):
  # The same 60-degree-rhombic lattice basis SymmetryTriangle already uses
  # for Class I (x grows along the "c" direction, y grows along the "r"
  # direction at 60 degrees from it): x = p + q/2, y = q*sqrt(3)/2.
  return np.array([p + q / 2., q * np.sqrt(3.) / 2.])


def _same_side_sign(a, b, c):
  # Twice the signed area of triangle (a, b, c); its sign tells you which
  # side of line a-b point c is on.
  return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def _roll3(t, shift):
  # Cyclically rotate a 3-tuple, matching numpy.roll's convention
  # (result[i] = t[i - shift mod 3]): shift=1 moves the last element to
  # the front. See ClassThreeSymmetryTriangle's cross-face stitching
  # comment for what this is used for.
  shift = shift % 3
  if shift == 0:
    return t
  return t[-shift:] + t[:-shift]


class ClassThreeSymmetryTriangle(object):
  # Class III ("skew") subdivision, using the general (m, n) Goldberg-
  # Coxeter construction: m != n, and unlike Class I (n=0) or Class II
  # (n=m), this pattern has no reflection symmetry within a face, so it
  # can't reuse SymmetryTriangle's row/column grid -- the face boundary
  # itself is skewed relative to the lattice basis. This class does not
  # inherit from SymmetryTriangle; it builds .vertices/.chord_list/
  # .face_list directly, matching GeodesicSphere's expected duck-typed
  # interface (a full polyhedron face is still the fundamental domain,
  # same as Class I -- the "big triangle" described below has the same
  # 3 corners as the actual face, just a skewed internal grid).
  #
  # Construction: take the vector from one face vertex to the next
  # (represented in the lattice as (m, n)), and two more copies of it
  # rotated 60 degrees each time, to form a triangle with the same 3
  # corners as the actual polyhedron face but expressed in the finer
  # (m,n)-lattice's own coordinates. Enumerate every lattice point in a
  # bounding region, keep the ones inside (or on the boundary of) that
  # triangle, and mesh them via Delaunay triangulation (see the comment
  # above the Delaunay call below for why that's the correct choice
  # here, rather than a simpler axis-aligned grid check).
  def __init__(self, m, n, polyhedral):
    CL = polyhedral.ppt_side_length
    T = m * m + m * n + n * n
    scale = CL / np.sqrt(np.float64(T))

    # triangle corners in lattice (p,q) coordinates: the origin, the
    # (m,n) "jump", and that jump rotated 60 degrees -- (p,q) -> (-q,p+q)
    # is the standard 60-degree-rotation identity in this lattice basis
    A_pq = (0, 0)
    B_pq = (m, n)
    C_pq = (-n, m + n)

    A_xy = _lattice_to_xy(*A_pq)
    B_xy = _lattice_to_xy(*B_pq)
    C_xy = _lattice_to_xy(*C_pq)

    def inside_or_on_boundary(p, q):
      P = _lattice_to_xy(p, q)
      d1 = _same_side_sign(A_xy, B_xy, P)
      d2 = _same_side_sign(B_xy, C_xy, P)
      d3 = _same_side_sign(C_xy, A_xy, P)
      eps = 1e-9 * T
      has_neg = (d1 < -eps) or (d2 < -eps) or (d3 < -eps)
      has_pos = (d1 > eps) or (d2 > eps) or (d3 > eps)
      return not (has_neg and has_pos)

    # a bounding box comfortably containing the (possibly negative-p)
    # skewed triangle
    p_lo, p_hi = min(0, m, -n) - 1, max(0, m, -n) + 1
    q_lo, q_hi = min(0, n, m + n) - 1, max(0, n, m + n) + 1

    kept = {}
    for q in range(q_lo, q_hi + 1):
      for p in range(p_lo, p_hi + 1):
        if inside_or_on_boundary(p, q):
          kept[(p, q)] = None

    # Face.transfer_matrix (see polyhedral.py) places a flat local point
    # (a, b, 0) at 3D position origin + a*x_dir + b*y_dir, where
    # x_dir=unit(v2-v1) and y_dir=unit(v3-origin) come from the ACTUAL
    # face's 3 corners -- a basis that is not generally orthogonal (only
    # Class I's equilateral case happens to make it so). Rather than
    # hand-derive a closed-form local (a,b) formula for this basis and
    # risk the same bug that turned up in Class II, solve for it
    # directly: build the same face in an "unshifted" local layout
    # (v1 at the origin, v2 along the local x-axis), and solve the
    # actual oblique 2x2 system relating that layout to the origin-
    # centered (a,b) coordinates Face expects.
    unshifted_v1 = scale * A_xy
    unshifted_v2 = scale * B_xy
    unshifted_v3 = scale * C_xy
    centroid_unshifted = (unshifted_v1 + unshifted_v2 + unshifted_v3) / 3.

    x_dir_local = unshifted_v2 - unshifted_v1
    x_dir_local = x_dir_local / np.linalg.norm(x_dir_local)
    y_dir_local = unshifted_v3 - centroid_unshifted
    y_dir_local = y_dir_local / np.linalg.norm(y_dir_local)
    basis = np.transpose(np.array([x_dir_local, y_dir_local]))

    kept_list = sorted(kept)
    corners = {A_pq, B_pq, C_pq}

    # A "halo" of lattice points just outside the triangle is needed for
    # two things below: (1) cross-face stitching, and (2) properly
    # meshing right up to a chiral triangle's jagged (non-edge-aligned)
    # boundary. Both needs, and the precise halo membership rule, were
    # reverse-engineered against the antitile library's Goldberg-Coxeter
    # implementation (used as an independent oracle -- see
    # tests/test_class_three.py) after a first attempt (Delaunay
    # triangulation of the strict interior/boundary points alone)
    # produced a mesh with the right V/E/F counts but 30 edges (exactly
    # the base icosahedron's own edge count) at the full, unsubdivided
    # polyhedron edge length -- proof the *topology*, not just the
    # counts, was wrong.
    #
    # A halo point is a non-kept lattice point that is outside exactly
    # one of the triangle's 3 boundary lines (not two, which would put
    # it beyond a corner, in territory that belongs to neither this
    # face nor its immediate neighbor) AND is adjacent to a kept point
    # that is NOT itself a corner. Points adjacent only to a corner are
    # deliberately excluded even when they pass the "outside exactly
    # one line" test -- verified empirically (against the oracle, across
    # several (m,n) pairs) to be necessary: including them produces 6
    # spurious extra faces per polyhedron face, all sitting just past a
    # corner.
    _NEIGHBOR_STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

    def outside_exactly_one_side(p, q):
      P = _lattice_to_xy(p, q)
      d1 = _same_side_sign(A_xy, B_xy, P)
      d2 = _same_side_sign(B_xy, C_xy, P)
      d3 = _same_side_sign(C_xy, A_xy, P)
      eps = 1e-9 * T
      return sum(1 for d in (d1, d2, d3) if d < -eps) == 1

    halo = {}
    for (p, q) in kept_list:
      if (p, q) in corners:
        continue
      for dp, dq in _NEIGHBOR_STEPS:
        neighbor = (p + dp, q + dq)
        if neighbor in kept:
          continue
        if outside_exactly_one_side(*neighbor):
          halo[neighbor] = None
    halo_list = sorted(halo)

    full_list = kept_list + halo_list
    valid = set(full_list)
    n_genuine = len(kept_list)
    self.local_priority = [0] * n_genuine + [1] * len(halo_list)

    self.vertices = []
    for (p, q) in full_list:
      target_unshifted = scale * _lattice_to_xy(p, q)
      a, b = np.linalg.solve(basis, target_unshifted - centroid_unshifted)
      self.vertices.append(Vertex(a, b, 0.))

    index_of = {pq: i for i, pq in enumerate(full_list)}

    # Mesh generation: tile the (p,q) plane with the lattice's 2
    # elementary triangle orientations (a "unit rhombus" (p,q),(p+1,q),
    # (p,q+1),(p+1,q+1) split along its (p+1,q)-(p,q+1) diagonal), and
    # keep a triangle if all 3 corners are in the genuine-or-halo set.
    # This -- not Delaunay triangulation of the strict interior points,
    # tried first -- is what correctly meshes right up to the jagged
    # boundary using halo points as placeholders for the neighboring
    # face's real vertices (which cross-face stitching, below, then
    # resolves them to). Some of these triangles straddle the boundary
    # and get independently regenerated by the neighboring face too;
    # GeodesicSphere deduplicates identical post-merge faces.
    self.face_list = []
    p_lo, p_hi = min(0, m, -n) - 1, max(0, m, -n) + 1
    q_lo, q_hi = min(0, n, m + n) - 1, max(0, n, m + n) + 1
    for q in range(q_lo, q_hi):
      for p in range(p_lo, p_hi):
        up = [(p, q), (p + 1, q), (p, q + 1)]
        down = [(p + 1, q), (p + 1, q + 1), (p, q + 1)]
        for tri in (up, down):
          if all(v in valid for v in tri):
            self.face_list.append([index_of[v] for v in tri])

    # chords: every edge of every retained face, deduplicated
    chord_set = set()
    for face in self.face_list:
      for i in range(3):
        edge = tuple(sorted((face[i], face[(i + 1) % 3])))
        chord_set.add(edge)
    self.chord_list = [list(edge) for edge in sorted(chord_set)]

    # Cross-face stitching: a chiral (m != n) lattice has no reflection
    # symmetry, so -- unlike Class I/II -- a point that lies near (but
    # not exactly on) a face's edge generally does NOT land at the same
    # 3D position when computed independently from the neighboring
    # face's own local basis. 3D-proximity matching (GeodesicSphere's
    # usual approach) only catches the 3 face corners, leaving every
    # original polyhedron edge as one long, unsubdivided chord -- a real
    # bug caught empirically (30 anomalously long edges, exactly the
    # icosahedron's own 30 edges, for (m,n)=(3,2)).
    #
    # The fix (matching the combinatorial approach used by the antitile
    # library's Goldberg-Coxeter implementation, verified against it as
    # an independent oracle -- see class_three.py's test suite): encode
    # each point's (p,q) position as a redundant 3-tuple "lindex" (u,
    # v, w) = (p+q, m-p, m+n-q). For two faces sharing edge k0 (on face
    # 0) / k1 (on face 1) -- local edge index 0/1/2 meaning corners
    # (v1,v2)/(v2,v3)/(v3,v1) -- cyclically rolling face 0's lindex by
    # (-k0)%3 and face 1's by (-k1)%3 brings both faces' view of the
    # shared edge into a common frame; in that frame, a point on face 0
    # and a point on face 1 are the SAME physical vertex exactly when
    # their rolled lindexes sum to the constant (m+n, m, 2m+n). This
    # correctly identifies matches that are nowhere near coincident in
    # 3D, because it's driven by the lattice's own combinatorial
    # structure rather than any assumption about 3D position.
    lindex_list = [(p + q, m - p, m + n - q) for (p, q) in full_list]
    roll_dicts = {}
    for roll_amount in (0, 1, 2):
      d = {}
      for local_idx, lindex in enumerate(lindex_list):
        d[_roll3(lindex, roll_amount)] = local_idx
      roll_dicts[roll_amount] = d

    offset = (m + n, m, 2 * m + n)
    n_points = len(full_list)
    adjacency = compute_face_adjacency(polyhedral.faces)
    self.cross_face_matches = []
    seen_face_pairs = set()
    for face_i, row in enumerate(adjacency):
      for k_i, (face_j, k_j) in enumerate(row):
        pair_key = frozenset(((face_i, k_i), (face_j, k_j)))
        if pair_key in seen_face_pairs:
          continue
        seen_face_pairs.add(pair_key)
        roll_i = (-k_i) % 3
        roll_j = (-k_j) % 3
        dict_j = roll_dicts[roll_j]
        for local_idx, lindex in enumerate(lindex_list):
          rolled = _roll3(lindex, roll_i)
          target = tuple(offset[t] - rolled[t] for t in range(3))
          match = dict_j.get(target)
          if match is not None:
            self.cross_face_matches.append(
              (face_i * n_points + local_idx, face_j * n_points + match))
