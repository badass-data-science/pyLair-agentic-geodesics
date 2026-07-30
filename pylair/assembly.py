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

#
# Turns pyLair's dome-level vertex/chord/face indices -- already stable
# and already unique the moment build_dome() returns them -- into a
# construction-time identity that survives grouping into cutting
# templates and nesting onto sheet stock. get_bill_of_materials()
# deliberately collapses individual hubs/struts/panels into "type +
# count" for cutting-template purposes (see bill_of_materials.py's own
# group_hub_types/group_face_types/cluster_chord_lengths); this module
# is the layer above that, which keeps every individual instance
# addressable by a stable label from dome geometry through a pyFit
# nesting job and back into a human-readable assembly manifest.
#
# Every dome-level index already IS a stable, unique identity (hub index
# == position in DomeResult.V, strut index == position in DomeResult.C,
# panel index == position in DomeResult.F_sphere, for a given set of
# build_dome() parameters) -- nothing here invents a new ID scheme, it
# just formats those same indices as human-readable labels and threads
# them through grouping, template generation, and nesting.
#
import numpy as np

from .bill_of_materials import (
    compute_hub_data,
    compute_spoke_angles,
    group_hub_types,
    compute_face_data,
    group_face_types,
    compute_dihedral_angles,
    cluster_chord_lengths,
)

HUB_PREFIX = 'H'
STRUT_PREFIX = 'S'
PANEL_PREFIX = 'P'


def hub_label(idx):
  return f'{HUB_PREFIX}{idx}'


def strut_label(idx):
  return f'{STRUT_PREFIX}{idx}'


def panel_label(idx):
  return f'{PANEL_PREFIX}{idx}'


def parse_instance_label(label):
  # Inverse of hub_label/strut_label/panel_label: returns (kind, index)
  # where kind is 'hub', 'strut', or 'panel'. Raises ValueError on
  # anything that isn't one of this module's own labels -- a nest
  # report's part_name that didn't originate from this module (e.g. a
  # hand-typed job spec entry) has no dome instance to resolve to.
  if not label or label[0] not in (HUB_PREFIX, STRUT_PREFIX, PANEL_PREFIX):
    raise ValueError(f'{label!r} is not a hub/strut/panel instance label produced by pylair.assembly.')
  prefix, rest = label[0], label[1:]
  try:
    idx = int(rest)
  except ValueError:
    raise ValueError(f'{label!r} is not a hub/strut/panel instance label produced by pylair.assembly.')
  kind = {'H': 'hub', 'S': 'strut', 'P': 'panel'}[prefix]
  return kind, idx


def _mirrored_triangle_polygon(edge_lengths):
  # The exact same flat A/B/C construction OutputFaceTemplateDXF (see
  # output.py) uses to turn one SSS edge-length triple into a 2D
  # triangle, reflected across the x-axis (y -> -y). Edge lengths alone
  # can't distinguish a chiral panel's two mirror-image instances --
  # that's the whole reason group_face_types has to look past them to a
  # winding-order chirality key -- so OutputFaceTemplateDXF's own output
  # is, without knowing it, already one specific, arbitrary choice of
  # the two. This function produces the *other* one, as plain (x, y)
  # coordinates a pyFit job spec's "polygon" field can use directly,
  # without needing a second DXF file on disk.
  ab, bc, ca = edge_lengths
  cos_a = (ab ** 2 + ca ** 2 - bc ** 2) / (2 * ab * ca)
  angle_a = np.arccos(np.clip(cos_a, -1., 1.))

  A = (0., 0.)
  B = (ab, 0.)
  C = (ca * np.cos(angle_a), -ca * np.sin(angle_a))
  return [A, B, C]


def build_assembly_manifest(vertices, chords, faces=None, elongation_factors=(1.0, 1.0, 1.0),
                             rounding_precision=9, angle_precision=3, length_precision=3):
  """Build a per-instance assembly manifest from a dome's final,
  post-elongation/truncation V/C/F_sphere (i.e. DomeResult.V/.C/.F_sphere,
  or the equivalent arrays get_bill_of_materials already takes). Unlike
  the Bill of Materials, every hub, strut, and panel here keeps its own
  stable instance label (see hub_label/strut_label/panel_label) and its
  real adjacency to its neighbors, instead of being collapsed into a
  type-level count -- this is the data an assembly schematic or a
  per-instance pyFit job spec (see build_pyfit_job_spec_for_panels) is
  built from.

  Returns a dict with keys 'hubs', 'struts', 'panels' (each a label ->
  instance-detail dict) and 'hub_groups'/'strut_groups'/'panel_groups'
  (each a list of per-cutting-template-type summaries, with a labeled
  'hub_ids'/'strut_ids'/'panel_ids' list instead of raw indices).
  'panels' and 'panel_groups' are empty if faces is None.

  Every adjacency direction a builder needs to orient assembly is
  covered, not just half of each pair: a hub's own 'connections' list
  gives hub->strut and hub->hub; a strut's 'hub_1'/'hub_2' gives
  strut->hub back; a panel's 'hub_ids' gives panel->hub and its
  'edges'[i]['strut'] gives panel->strut; a strut's own
  'bordering_panels' gives the reverse, strut->panel (1 entry on a
  truncated dome's open boundary edges, 2 on any interior edge, None
  rather than [] if faces wasn't given at all).
  """
  vertices = [np.asarray(v, dtype=float) for v in vertices]

  chord_index_lookup = {frozenset((c[0], c[1])): idx for idx, c in enumerate(chords)}

  #
  # hubs + struts (always available -- faces are optional, chords never are)
  #
  hubs = compute_hub_data(vertices, chords, elongation_factors)
  hub_groups_raw = group_hub_types(hubs, angle_precision)
  hub_group_of = {idx: gi for gi, g in enumerate(hub_groups_raw) for idx in g['hub_indices']}

  strut_groups_raw = cluster_chord_lengths(vertices, chords, rounding_precision)
  strut_group_of = {idx: gi for gi, g in enumerate(strut_groups_raw) for idx in g['chord_indices']}

  hubs_out = {}
  for h, data in hubs.items():
    valence = len(data['connected_vertices'])
    spoke_angles = compute_spoke_angles(data) if valence > 1 else {}
    connections = []
    for c, cdata in data['connected_vertices'].items():
      strut_idx = chord_index_lookup[frozenset((h, c))]
      connections.append({
        'to_hub': hub_label(c),
        'strut': strut_label(strut_idx),
        'tangential_angle_degrees': cdata['tangential_angle'],
        'spoke_angle_degrees': spoke_angles.get(c),
      })
    hubs_out[hub_label(h)] = {
      'index': h,
      'position': data['vertex'].tolist(),
      'valence': valence,
      'template_group': hub_group_of.get(h),
      'connections': connections,
    }

  struts_out = {}
  for idx, c in enumerate(chords):
    a, b = c[0], c[1]
    length = float(np.linalg.norm(vertices[a] - vertices[b]))
    struts_out[strut_label(idx)] = {
      'index': idx,
      'hub_1': hub_label(a),
      'hub_2': hub_label(b),
      'length': length,
      'template_group': strut_group_of.get(idx),
      # None (not just an empty list) when faces isn't given at all --
      # distinct from "face data exists but this strut genuinely borders
      # no panel", which shouldn't happen for a real triangulated dome
      # but isn't assumed away below.
      'bordering_panels': None,
    }

  hub_groups = [
    {
      'template_group': gi,
      'valence': g['valence'],
      'count': g['count'],
      'hub_ids': [hub_label(idx) for idx in g['hub_indices']],
    }
    for gi, g in enumerate(hub_groups_raw)
  ]
  strut_groups = [
    {
      'template_group': gi,
      'length': g['length'],
      'count': g['count'],
      'strut_ids': [strut_label(idx) for idx in g['chord_indices']],
    }
    for gi, g in enumerate(strut_groups_raw)
  ]

  panels_out = {}
  panel_groups = []
  if faces is not None:
    face_data = compute_face_data(vertices, faces)

    # Every strut's bordering panel(s) -- the reverse of a panel's own
    # 'edges'/'strut' link. Built directly from face_data rather than
    # reusing compute_dihedral_angles' own internal edge_to_faces: that
    # function only keeps edges bordering exactly 2 faces (it has no
    # dihedral angle to report otherwise), which would silently drop a
    # truncated dome's boundary struts -- those border exactly 1 panel,
    # a real and useful fact for assembly, not an edge case to discard.
    edge_to_faces = {}
    for face_idx, fd in enumerate(face_data):
      a, b, c = fd['vertices']
      for u, v in ((a, b), (b, c), (c, a)):
        edge_to_faces.setdefault(frozenset((u, v)), []).append(face_idx)
    for idx, c in enumerate(chords):
      bordering = edge_to_faces.get(frozenset((c[0], c[1])), [])
      struts_out[strut_label(idx)]['bordering_panels'] = [panel_label(i) for i in sorted(bordering)]

    face_groups_raw = group_face_types(face_data, length_precision)
    face_group_of = {idx: gi for gi, g in enumerate(face_groups_raw) for idx in g['face_indices']}

    # orientation_of[face_idx] = which of that group's chirality buckets
    # this specific instance belongs to (0-based) -- only meaningful
    # when the group is chiral; see _face_chirality_key in
    # bill_of_materials.py for why edge lengths alone can't tell two
    # mirror-image instances apart.
    orientation_of = {}
    for g in face_groups_raw:
      if g['chiral']:
        for bucket_i, idxs in enumerate(g['chirality_bucket_face_indices']):
          for idx in idxs:
            orientation_of[idx] = bucket_i

    dihedral_rows = compute_dihedral_angles(face_data, chords)
    dihedral_lookup = {frozenset((r['vertex 1'], r['vertex 2'])): r for r in dihedral_rows}

    for idx, fd in enumerate(face_data):
      a, b, c = fd['vertices']
      edges = []
      for u, v in ((a, b), (b, c), (c, a)):
        strut_idx = chord_index_lookup.get(frozenset((u, v)))
        dr = dihedral_lookup.get(frozenset((u, v)))
        edges.append({
          'hub_pair': [hub_label(u), hub_label(v)],
          'strut': strut_label(strut_idx) if strut_idx is not None else None,
          'dihedral_angle_degrees': dr['dihedral angle (degrees)'] if dr is not None else None,
          'bevel_angle_degrees': dr['bevel angle (degrees)'] if dr is not None else None,
          'note': '' if dr is not None else
                  'boundary edge (borders fewer than 2 panels) -- no dihedral to bevel, '
                  'expected at a truncated dome\'s cut edge',
        })
      gi = face_group_of.get(idx)
      panels_out[panel_label(idx)] = {
        'index': idx,
        'hub_ids': [hub_label(a), hub_label(b), hub_label(c)],
        'centroid': fd['centroid'].tolist(),
        'area': fd['area'],
        'template_group': gi,
        'chiral': face_groups_raw[gi]['chiral'] if gi is not None else False,
        'orientation_bucket': orientation_of.get(idx),
        'edges': edges,
      }

    for gi, g in enumerate(face_groups_raw):
      entry = {
        'template_group': gi,
        'edge_lengths': g['edge_lengths'],
        'count': g['count'],
        'chiral': g['chiral'],
        'panel_ids': [panel_label(idx) for idx in g['face_indices']],
      }
      if g['chiral']:
        entry['chirality_bucket_panel_ids'] = [
          [panel_label(idx) for idx in idxs] for idxs in g['chirality_bucket_face_indices']
        ]
      panel_groups.append(entry)

  return {
    'hubs': hubs_out,
    'struts': struts_out,
    'panels': panels_out,
    'hub_groups': hub_groups,
    'strut_groups': strut_groups,
    'panel_groups': panel_groups,
  }


def build_pyfit_job_spec_for_panels(manifest, sheet_width, sheet_height, template_dxf_paths):
  """Build a pyFit job spec (see pyfit/api.py's run_nest) with one part
  entry per individual panel *instance* -- quantity always 1 -- rather
  than one entry per shape type with quantity=N. pyFit places no
  constraint on what a part's "name" means or how many entries point at
  the same DXF file, so this needs zero pyFit code changes: it just uses
  a stable per-instance label (panel_label(face_index)) as the part
  name, so pyFit's own nest report -- which echoes part_name back on
  every placement -- becomes instance-addressable for free.

  template_dxf_paths must map each panel group's 'template_group' index
  (see build_assembly_manifest's 'panel_groups') to the cutting-template
  DXF file already written for that group (e.g. from
  get_bill_of_materials's "Panel Cutting Templates", matched up by
  group order).

  Chirality is handled explicitly rather than left to pyFit's own
  packer: a chiral group's cutting template is, without saying so, one
  arbitrary specific mirror orientation (see
  bill_of_materials._face_chirality_key). Letting pyFit decide whether
  to mirror a given instance for packing efficiency (allow_mirror=True)
  would silently let it flip an instance into the *wrong* physical
  chirality for this specific dome. Instead: instances in the
  template's own orientation bucket (bucket 0) reference the DXF
  template directly with allow_mirror=False; instances in every other
  bucket get the pre-mirrored polygon (_mirrored_triangle_polygon)
  instead, also with allow_mirror=False -- so pyFit is never the one
  deciding which chirality gets cut, only where it gets placed.
  Non-chiral groups have no such constraint, so allow_mirror=True there
  simply gives pyFit's packer more placement freedom at zero risk.
  """
  parts = []
  for group in manifest['panel_groups']:
    dxf_path = template_dxf_paths[group['template_group']]
    if not group['chiral']:
      for pid in group['panel_ids']:
        parts.append({'name': pid, 'dxf': dxf_path, 'quantity': 1, 'allow_mirror': True})
      continue

    buckets = group['chirality_bucket_panel_ids']
    canonical_ids, mirror_bucket_ids = buckets[0], buckets[1:]
    for pid in canonical_ids:
      parts.append({'name': pid, 'dxf': dxf_path, 'quantity': 1, 'allow_mirror': False})

    mirrored_polygon = _mirrored_triangle_polygon(group['edge_lengths'])
    for bucket in mirror_bucket_ids:
      for pid in bucket:
        parts.append({
          'name': pid,
          'polygon': [list(p) for p in mirrored_polygon],
          'quantity': 1,
          'allow_mirror': False,
        })

  return {'sheet': {'width': sheet_width, 'height': sheet_height}, 'parts': parts}


def build_pyfit_job_spec_for_hubs(manifest, sheet_width, sheet_height, template_dxf_paths):
  """Same idea as build_pyfit_job_spec_for_panels, for hub connector
  plates instead of panels. Hub connector shapes have no chirality
  model in pyLair today -- group_hub_types has no equivalent of
  group_face_types' chirality key -- so every instance is submitted
  with allow_mirror=True. If a real build ever needs directional hub
  connector material, that gap would need closing first; this function
  doesn't invent a distinction pylair.bill_of_materials doesn't compute.
  """
  parts = []
  for group in manifest['hub_groups']:
    dxf_path = template_dxf_paths[group['template_group']]
    for hid in group['hub_ids']:
      parts.append({'name': hid, 'dxf': dxf_path, 'quantity': 1, 'allow_mirror': True})
  return {'sheet': {'width': sheet_width, 'height': sheet_height}, 'parts': parts}


def attach_nest_placements(manifest, nest_report, kind='panels'):
  """Merge a pyFit nest report's placements back onto the manifest
  produced by build_assembly_manifest, given a job spec built by
  build_pyfit_job_spec_for_panels/_for_hubs (so nest_report's
  'part_name' fields are this module's own instance labels). Mutates
  and returns `manifest`; unmatched placements (a part_name this module
  didn't mint) are ignored rather than raising, since a caller may have
  hand-added parts (e.g. non-dome cutting jobs) to the same nest.
  """
  bucket = manifest[kind]
  for placement in nest_report['placements']:
    label = placement['part_name']
    if label not in bucket:
      continue
    bucket[label]['placement'] = {
      'sheet_index': placement['sheet_index'],
      'position': placement['position'],
      'rotation_degrees': placement['rotation_degrees'],
      'mirrored': placement['mirrored'],
    }
  return manifest
