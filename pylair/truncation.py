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

# below this, a chord is considered exactly coincident with the cutoff
# plane: dividing by its near-zero extent along the cutoff axis would
# silently produce an inf/nan vertex (numpy division by zero warns rather
# than raising) instead of failing loudly.
HORIZONTAL_CHORD_EPSILON = 1e-12


def _edge_crossing(v_discarded, v_kept, axis, cutoff):
  # the point on segment (v_discarded, v_kept) where it crosses `cutoff`
  # along `axis`. Shared by both the chord-splitting and face-clipping
  # logic below, so a chord and every face touching it agree on exactly
  # the same cut point rather than two independently-rounded near
  # duplicates. Purely a line/plane intersection -- it has no notion of
  # which side of the plane is "kept", so it serves cuts from either end
  # of the axis unchanged (the argument order only fixes which endpoint
  # the arithmetic starts from, so a given edge always rounds the same
  # way).
  norm = np.linalg.norm(v_discarded - v_kept)
  norm_vec = (v_discarded - v_kept) / norm
  if abs(norm_vec[axis]) < HORIZONTAL_CHORD_EPSILON:
    raise ValueError(
      'Truncation cutoff plane lies exactly on a chord that is flat '
      'along the cutoff axis. Choose a slightly different truncation '
      'value to avoid this degenerate case.'
    )
  scalar = (cutoff - v_kept[axis]) / norm_vec[axis]
  return v_kept + scalar * norm_vec


def _clip_face(face, V_sphere, register_crossing, is_kept):
  # Clip a single triangular face against the same cutoff plane used for
  # chords. `register_crossing(v1_idx, v2_idx)` returns the (possibly
  # newly created) crossing point for ANY edge, not just real chords --
  # this matters once a face has already been through a previous
  # clipping pass on a different axis, since the diagonal edge a
  # quad-split introduces (see below) is backed by a genuine chord (see
  # `new_chords` below), and a second pass still needs a consistent
  # crossing point for it if that diagonal itself straddles the new
  # cutoff.
  # Returns (triangles, new_chords): 0, 1, or 2 triangles (as [a, b, c]
  # index triples, still indexing into the not-yet-renumbered vertex
  # list), depending on how many of the face's 3 vertices survive the
  # cut, plus any new chord the split required. Winding order is
  # preserved in every case: a kept triangle's corner(s) are simply
  # pulled inward along the edges leading to a discarded vertex, which
  # never reverses the cyclic order the original face was given in.
  # `is_kept(vertex)` decides which side of the cutoff plane survives,
  # so the same logic serves a cut from either end of the axis -- below,
  # "above" just means "on the kept side".
  verts = list(face)
  above = [is_kept(V_sphere[v]) for v in verts]
  n_above = sum(above)

  if n_above == 3:
    return [verts], []
  if n_above == 0:
    return [], []

  def crossing(i, j):
    return register_crossing(verts[i], verts[j])

  if n_above == 1:
    i = above.index(True)
    j, k = (i + 1) % 3, (i + 2) % 3
    Pa, Pb = crossing(i, j), crossing(k, i)
    # Pa-Pb is the kept triangle's own third edge -- the one lying
    # exactly on the cutoff plane, i.e. this triangle's own segment of
    # the dome's base ring. Every other edge of every clipped face is
    # already covered by the general chord-clipping loop above (an
    # original chord with one endpoint below cutoff gets shortened to
    # its own crossing point there), but that loop only ever touches
    # *existing* chords -- it has no way to know a face-only edge like
    # this one needs a chord at all, so without reporting it back here
    # a truncated dome's base ring ends up with no closing struts.
    return [[verts[i], Pa, Pb]], [[Pa, Pb]]

  # n_above == 2: cutting off the single discarded corner leaves a
  # (necessarily convex, since a straight line can only cut a triangle
  # into a triangle and a convex quadrilateral) quadrilateral, split
  # here into 2 triangles along a diagonal from one of the new crossing
  # points. Both sub-triangles lie in the same plane as the original
  # (undivided) face, so this diagonal is a real, physically bracable
  # edge -- it is reported back as a new chord so it gets a strut length
  # in the Bill of Materials and a (necessarily flat, ~180 degree) bevel
  # angle from compute_dihedral_angles, same as any other chord bordering
  # exactly 2 faces. Pa-Pb (the quad's own remaining cutoff-plane edge,
  # bordering only the second sub-triangle) is this same face's own
  # base-ring segment, and needs reporting back for exactly the same
  # reason the n_above==1 case's Pa-Pb does, above.
  disc = above.index(False)
  kept1, kept2 = (disc + 1) % 3, (disc + 2) % 3
  Pa = crossing(disc, kept1)
  Pb = crossing(kept2, disc)
  diagonal = [Pa, verts[kept2]]
  base_ring_edge = [Pa, Pb]
  return [
    [Pa, verts[kept1], verts[kept2]],
    [Pa, verts[kept2], Pb],
  ], [diagonal, base_ring_edge]


def truncate(V_sphere, C_sphere, cutoff_from_bottom, axis=2, F_sphere=None, cutoff_from_top=None):
  # Cut the dome along `axis` (0=X, 1=Y, 2=Z).
  #   cutoff_from_bottom: fraction (0-1) of the axis's extent to discard
  #     from its minimum end, keeping everything above (the original,
  #     and still the positional, behavior).
  #   cutoff_from_top: fraction (0-1) of the axis's extent to discard
  #     from its maximum end, keeping everything below.
  # Either may be None; giving both keeps the band between them. Both
  # fractions are measured against this axis's extent *before* either
  # cut is made, so a band of (0.25, 0.25) keeps the middle half of the
  # extent -- not 0.25 of whatever the first cut leaves behind.
  values = [v[axis] for v in V_sphere]
  if not values:
    return list(V_sphere), list(C_sphere), None if F_sphere is None else list(F_sphere)
  min_v, max_v = min(values), max(values)
  v_range = max_v - min_v

  V, C, F = V_sphere, C_sphere, F_sphere
  if cutoff_from_bottom is not None:
    V, C, F = _truncate_one_side(V, C, F, axis, min_v + cutoff_from_bottom * v_range, keep_above=True)
  if cutoff_from_top is not None:
    V, C, F = _truncate_one_side(V, C, F, axis, max_v - cutoff_from_top * v_range, keep_above=False)
  if cutoff_from_bottom is None and cutoff_from_top is None:
    V, C = list(V), list(C)
    F = None if F is None else list(F)
  return V, C, F


def _truncate_one_side(V_sphere, C_sphere, F_sphere, axis, cutoff, keep_above):
  # A single planar cut at absolute coordinate `cutoff` along `axis`.
  # Points lying exactly on the plane are kept from either direction.
  # Only the kept/discarded classification depends on `keep_above`; no
  # coordinate is ever reflected, so face winding is untouched. A band
  # is two calls in a row -- the same composition multi-axis truncation
  # already relies on (see _register_crossing / _clip_face on
  # re-clipping a previous pass's quad-split diagonal).
  if keep_above:
    def is_kept(v):
      return v[axis] >= cutoff
  else:
    def is_kept(v):
      return v[axis] <= cutoff

  #
  # crossing points, computed once per edge and cached regardless of
  # whether that edge is a real chord or a face-only diagonal seam
  # introduced by a previous clipping pass on a different axis -- see
  # _clip_face for why the latter case matters.
  #
  V_new = list(V_sphere)
  edge_to_new_vertex = {}

  def _register_crossing(v1_idx, v2_idx):
    key = frozenset((v1_idx, v2_idx))
    if key not in edge_to_new_vertex:
      v1, v2 = V_sphere[v1_idx], V_sphere[v2_idx]
      if not is_kept(v1):
        point = _edge_crossing(v1, v2, axis, cutoff)
      else:
        point = _edge_crossing(v2, v1, axis, cutoff)
      V_new.append(point)
      edge_to_new_vertex[key] = len(V_new) - 1
    return edge_to_new_vertex[key]

  #
  # find chords to remove or modify
  #
  chords_to_remove = []
  chords_to_add = []
  for c_idx, c in enumerate(C_sphere):
    v1_idx = c[0]
    v2_idx = c[1]
    v1 = V_sphere[v1_idx]
    v2 = V_sphere[v2_idx]

    # both vertices discarded
    if not is_kept(v1) and not is_kept(v2):
      chords_to_remove.append(c_idx)

    # vertex 1 discarded
    elif not is_kept(v1):
      chords_to_remove.append(c_idx)
      chords_to_add.append([c[1], _register_crossing(v1_idx, v2_idx)])

    # vertex 2 discarded
    elif not is_kept(v2):
      chords_to_remove.append(c_idx)
      chords_to_add.append([c[0], _register_crossing(v1_idx, v2_idx)])

  #
  # clip faces against the same cutoff plane (see _clip_face) -- only
  # attempted when the caller actually has face data to begin with.
  # A corner-clipped (quad-split) face contributes a new diagonal chord;
  # collected into chords_to_add *before* chords are consolidated below,
  # so it gets renumbered, strut-lengthed, and bevel-angled like any
  # other chord.
  #
  F_next = None
  if F_sphere is not None:
    F_next = []
    for f in F_sphere:
      triangles, new_chords = _clip_face(f, V_sphere, _register_crossing, is_kept)
      F_next.extend(triangles)
      chords_to_add.extend(new_chords)

  #
  # consolidate chords
  #
  C_next = []
  for c_idx, c in enumerate(C_sphere):
    if chords_to_remove.count(c_idx) == 0:
      C_next.append(c)
  for c in chords_to_add:
    C_next.append(c)

  #
  # re-number nodes, getting ride of unused ones
  #
  old_vidx_2_new_v = {}
  V_final = []

  def _remap(vertex_1_idx, vertex_2_idx=None):
    for vidx in (vertex_1_idx,) if vertex_2_idx is None else (vertex_1_idx, vertex_2_idx):
      if vidx not in old_vidx_2_new_v:
        V_final.append(V_new[vidx])
        old_vidx_2_new_v[vidx] = len(V_final) - 1

  for c in C_next:
    _remap(c[0], c[1])
  if F_next is not None:
    for f in F_next:
      for v in f:
        _remap(v)

  C_final = [[old_vidx_2_new_v[c[0]], old_vidx_2_new_v[c[1]]] for c in C_next]
  F_final = None
  if F_next is not None:
    F_final = [[old_vidx_2_new_v[v] for v in f] for f in F_next]

  return V_final, C_final, F_final
