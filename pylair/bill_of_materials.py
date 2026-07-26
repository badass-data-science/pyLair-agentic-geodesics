#    pyLair:  A geodesic dome calculator
#    Copyright (C) 2013  Emily Williams
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# Load useful libraries
#
import numpy as np
import pandas as pd
import json

from .output import OutputHubConnectorTemplateDXF, OutputFaceTemplateDXF

# Below this fraction of the dome's largest strut length, a chord (or a
# panel with an edge that short) is flagged as a likely truncation-
# boundary artifact rather than a genuine distinct class. Real geodesic
# subdivisions essentially never produce legitimate strut-length classes
# differing by more than roughly one order of magnitude from each other
# (e.g. a frequency-6 Class I icosahedron's longest and shortest struts
# differ by well under 2x) -- so a strut three orders of magnitude
# below the dome's largest is overwhelmingly more likely to be a sliver
# left over from a truncation cutoff landing extremely close to (but
# not exactly on) a vertex ring, as observed for e.g. -t 0.4999999.
SMALL_CHORD_ARTIFACT_RATIO = 1e-3


def _ellipsoid_normal(vertex, elongation_factors):
  # The outward surface normal of a general axis-aligned ellipsoid
  # (semi-axes a*fx, a*fy, a*fz -- see pylair.elongation) at a point on
  # its surface, from the gradient of its implicit equation
  # x^2/(a*fx)^2 + y^2/(a*fy)^2 + z^2/(a*fz)^2 = 1: proportional to
  # (x/fx^2, y/fy^2, z/fz^2). The absolute scale `a` cancels out in the
  # normalization below, so only the per-axis factors matter. Reduces
  # exactly to the ordinary sphere normal (the normalized position
  # vector) when all three factors are 1 -- a sphere's surface normal
  # is always radial, but an ellipsoid's generally is not, except where
  # it crosses its own axes.
  fx, fy, fz = elongation_factors
  direction = np.array([vertex[0] / (fx ** 2), vertex[1] / (fy ** 2), vertex[2] / (fz ** 2)])
  return direction / np.linalg.norm(direction)


def compute_hub_data(vertices, chords, elongation_factors=(1.0, 1.0, 1.0)):
  # For every hub (vertex where 1+ chords meet): the vertex position,
  # each connected vertex, the tangential-plane deflection angle of
  # that chord, and the point where that chord (projected radially
  # from the origin) crosses the hub's own tangent plane -- the latter
  # is what spoke angles (computed separately, see compute_spoke_angles)
  # are measured from. Shared by get_bill_of_materials and the hub
  # connector template clustering below.
  hubs = {}
  for c in chords:
    if not c[0] in hubs:  hubs[c[0]] = {'connected_vertices': {}, 'vertex' : None}
    hubs[c[0]]['connected_vertices'][c[1]] = {'vertex' : vertices[c[1]]}
    hubs[c[0]]['vertex'] = vertices[c[0]]
    if not c[1] in hubs:  hubs[c[1]] = {'connected_vertices' : {}, 'vertex' : None}
    hubs[c[1]]['connected_vertices'][c[0]] = {'vertex' : vertices[c[0]]}
    hubs[c[1]]['vertex'] = vertices[c[1]]

  #
  # compute angles at hub between outbound chords and tangential plane
  #
  for h in hubs.keys():
    vertex = hubs[h]['vertex']
    normal = _ellipsoid_normal(vertex, elongation_factors)
    for c in hubs[h]['connected_vertices']:
      A = normal
      B = vertex - hubs[h]['connected_vertices'][c]['vertex']
      angle = (np.pi/2) - np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))
      angle_in_degrees = 180. * angle / np.pi
      hubs[h]['connected_vertices'][c]['tangential_angle'] = angle_in_degrees

  #
  # find where each outbound chord crosses the hub's own tangent plane
  #
  for hub in hubs.keys():
    normal_vector = _ellipsoid_normal(hubs[hub]['vertex'], elongation_factors)
    point_on_plane = hubs[hub]['vertex']
    line_origin = np.array([0., 0., 0.])
    for spoke in hubs[hub]['connected_vertices']:
      line = hubs[hub]['connected_vertices'][spoke]['vertex'] / np.linalg.norm(hubs[hub]['connected_vertices'][spoke]['vertex'])
      d = np.dot((point_on_plane - line_origin), normal_vector) / np.dot(line, normal_vector)   # http://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
      hubs[hub]['connected_vertices'][spoke]['point_of_tangential_plane_intersection'] = d * line

  return hubs


def compute_spoke_angles(hub_entry):
  # Given one hub's entry from compute_hub_data (already populated with
  # point_of_tangential_plane_intersection), return {connecting_hub:
  # signed angle in degrees}, measured from the first (lowest-index)
  # connecting hub as the 0-degree reference -- exactly the convention
  # used by the Bill of Materials "Spoke angles" report.
  spoke_list = sorted(hub_entry['connected_vertices'])
  vertex = hub_entry['vertex']
  point = hub_entry['connected_vertices'][spoke_list[0]]['point_of_tangential_plane_intersection']
  reference_vector = point - vertex

  angles = {spoke_list[0]: 0.}

  for spoke in spoke_list[1:]:
    point = hub_entry['connected_vertices'][spoke]['point_of_tangential_plane_intersection']
    comparison_vector = point - vertex

    normalized_dot_product = np.dot(reference_vector, comparison_vector) / (np.linalg.norm(reference_vector) * np.linalg.norm(comparison_vector))

    if normalized_dot_product < -1.0:
      normalized_dot_product = -1.0

    angle = np.arccos(normalized_dot_product)
    angle_in_degrees = 180. * angle / np.pi

    # http://www.opengl.org/discussion_boards/showthread.php/159385-Deriving-angles-from-0-to-360-from-Dot-Product
    C = np.cross(reference_vector, comparison_vector)
    direction = np.dot(C, vertex)
    if direction < 0.:  angle_in_degrees = -1 * angle_in_degrees

    angles[spoke] = angle_in_degrees

  return angles


def _hub_type_signature(hub_entry, angle_precision):
  # A rotation-invariant fingerprint of a hub's connector shape: valence,
  # plus the cyclic sequence of (angular gap to the next strut, that
  # strut's tangential angle) going around the hub in true angular order.
  # Two hubs that are the same shape just rotated relative to each other
  # -- which is the overwhelming majority of same-valence hubs in a
  # geodesic dome -- must get the identical signature, since a laser-cut
  # flat template's absolute rotation on the page doesn't matter, only
  # the angles *between* struts. compute_spoke_angles measures every
  # spoke relative to whichever connecting hub happens to sort first by
  # index, which is an arbitrary reference with no geometric meaning, so
  # the signature can't just use those angles directly: it re-sorts by
  # true angle and then tries every possible rotation of the resulting
  # cyclic sequence, keeping the lexicographically smallest one, so the
  # arbitrary starting point cancels out.
  spoke_list = sorted(hub_entry['connected_vertices'])
  n = len(spoke_list)
  if n <= 1:
    return (n,)

  spoke_angles = compute_spoke_angles(hub_entry)
  entries = []
  for s in spoke_list:
    angle = spoke_angles[s] % 360.
    tangential = round(hub_entry['connected_vertices'][s]['tangential_angle'], angle_precision)
    entries.append((angle, tangential))
  entries.sort(key=lambda e: e[0])

  angles_sorted = [e[0] for e in entries]
  tangentials_sorted = [e[1] for e in entries]
  gaps = [round((angles_sorted[(i + 1) % n] - angles_sorted[i]) % 360., angle_precision) for i in range(n)]

  best = None
  for start in range(n):
    candidate = tuple((gaps[(start + i) % n], tangentials_sorted[(start + i) % n]) for i in range(n))
    if best is None or candidate < best:
      best = candidate

  return (n, best)


def group_hub_types(hubs, angle_precision=3):
  # Cluster hubs into connector-plate "types": hubs whose rotation-
  # invariant signature matches exactly (see _hub_type_signature) share
  # a single template. Groups are sorted largest-first, matching the
  # Bill of Materials' own biggest-group-first convention.
  #
  # angle_precision (decimal places) must be coarse enough to absorb
  # floating-point noise from the geometry pipeline while still
  # distinguishing genuinely different hub shapes: two hubs from the
  # exact same symmetry orbit were observed differing by ~2e-6 degrees
  # (e.g. 64.465668 vs 64.465666), which a precision of 6 does not
  # absorb but 3 comfortably does. Verified empirically across
  # frequencies 4-16: precision 1-3 all produce the identical, stable
  # grouping (a "plateau"), while precision >= 4 sometimes still
  # over-splits on noise -- 3 is used as a safety margin above the
  # observed noise floor rather than the loosest value that happened
  # to work.
  groups = {}
  for hub_idx in sorted(hubs.keys()):
    sig = _hub_type_signature(hubs[hub_idx], angle_precision)
    groups.setdefault(sig, []).append(hub_idx)

  result = []
  for sig, hub_indices in groups.items():
    result.append({
      'valence': sig[0],
      'representative_hub': hub_indices[0],
      'hub_indices': hub_indices,
      'count': len(hub_indices),
    })
  result.sort(key=lambda g: (-g['count'], -g['valence']))
  return result


def compute_face_data(vertices, faces):
  # Per face (triangle vertex indices [a, b, c]): vertex order corrected
  # to outward-consistent winding, the 3 edge lengths in that winding
  # order (AB, BC, CA), the unit outward normal, area, and centroid.
  # Faces only ever exist for an untruncated dome, whose vertices sit
  # roughly on a sphere/ellipsoid centered near the origin, so "outward"
  # is resolved by checking whether cross(B-A, C-A) points away from the
  # face's own centroid (a stand-in for the dome's center) and swapping
  # B/C if not. Returned list is aligned by index with `faces`, which
  # compute_dihedral_angles relies on to relate a shared edge back to
  # its two bordering faces.
  face_data = []
  for f in faces:
    a, b, c = f[0], f[1], f[2]
    A, B, C = vertices[a], vertices[b], vertices[c]
    normal = np.cross(B - A, C - A)
    centroid = (A + B + C) / 3.
    if np.dot(normal, centroid) < 0:
      a, b, c = a, c, b
      A, B, C = vertices[a], vertices[b], vertices[c]
      normal = np.cross(B - A, C - A)

    norm = np.linalg.norm(normal)
    unit_normal = normal / norm if norm != 0 else normal
    edge_lengths = (
      np.linalg.norm(B - A),
      np.linalg.norm(C - B),
      np.linalg.norm(A - C),
    )
    face_data.append({
      'vertices': (a, b, c),
      'edge_lengths': edge_lengths,
      'normal': unit_normal,
      'area': 0.5 * norm,
      'centroid': centroid,
    })
  return face_data


def _face_type_signature(face_entry, length_precision=3):
  # SSS shape fingerprint: sorted, rounded edge lengths. Two faces
  # sharing this signature have an identical cutting outline -- mirror
  # images included, since SSS alone can't distinguish those (see
  # _face_chirality_key).
  return tuple(sorted(round(l, length_precision) for l in face_entry['edge_lengths']))


def _face_chirality_key(face_entry, length_precision=3):
  # Rotation-invariant (NOT reflection-invariant) fingerprint: the
  # winding-order edge-length triple, canonicalized over its 3 rotations
  # by keeping the lexicographically smallest. Two faces that share a
  # _face_type_signature but differ here are mirror images of each
  # other -- for a scalene triangle, reversing the winding direction
  # produces a cyclic sequence that is not a rotation of the original,
  # while an isosceles/equilateral triangle's sequence always re-
  # canonicalizes to itself either way (no meaningful chirality).
  lengths = tuple(round(l, length_precision) for l in face_entry['edge_lengths'])
  n = len(lengths)
  return min(tuple(lengths[(start + i) % n] for i in range(n)) for start in range(n))


def group_face_types(faces_data, length_precision=3):
  # Cluster faces into panel "types": faces whose edge-length signature
  # matches exactly (see _face_type_signature) share a single cutting
  # template. Groups are sorted largest-first, matching the Bill of
  # Materials' own biggest-group-first convention (see group_hub_types).
  groups = {}
  for idx, fd in enumerate(faces_data):
    sig = _face_type_signature(fd, length_precision)
    groups.setdefault(sig, []).append(idx)

  result = []
  for sig, face_indices in groups.items():
    is_scalene = len(set(sig)) == 3

    chirality_buckets = {}
    for idx in face_indices:
      key = _face_chirality_key(faces_data[idx], length_precision)
      chirality_buckets.setdefault(key, []).append(idx)

    chiral = is_scalene and len(chirality_buckets) > 1
    orientations = None
    if chiral:
      orientations = [
        {
          'edge_lengths': faces_data[idxs[0]]['edge_lengths'],
          'count': len(idxs),
        }
        for idxs in chirality_buckets.values()
      ]

    representative_face = face_indices[0]
    result.append({
      'edge_lengths': sig,
      'representative_face': representative_face,
      'face_indices': face_indices,
      'count': len(face_indices),
      'area': round(faces_data[representative_face]['area'], length_precision),
      'chiral': chiral,
      'orientations': orientations,
    })
  result.sort(key=lambda g: -g['count'])
  return result


def compute_dihedral_angles(face_data, chords):
  # Every chord in an untruncated dome (the only case faces exist for)
  # borders exactly 2 triangular faces -- a closed 2-manifold
  # triangulation, verified across Class I/II/III on both polyhedra at
  # multiple frequencies. For each chord, the angle needed to bevel each
  # bordering panel's edge so the two flat panels meet flush at the
  # true (interior) dihedral angle:
  #   normal_angle = angle between the two faces' outward unit normals
  #   dihedral (interior) = 180 - normal_angle
  #   bevel = normal_angle / 2  -- the cut angle away from a flat
  #     (perpendicular, 90-degree) reference edge, on each panel, so
  #     that placed together they reproduce the true dihedral angle
  # This formula was verified against the textbook icosahedron
  # (138.19 degrees) and octahedron (109.47 degrees) dihedral angles on
  # a frequency-1 dome of each.
  edge_to_faces = {}
  for idx, fd in enumerate(face_data):
    a, b, c = fd['vertices']
    for u, v in ((a, b), (b, c), (c, a)):
      edge_to_faces.setdefault(frozenset((u, v)), []).append(idx)

  results = []
  for chord in chords:
    bordering = edge_to_faces.get(frozenset((chord[0], chord[1])), [])
    if len(bordering) != 2:
      continue
    n1 = face_data[bordering[0]]['normal']
    n2 = face_data[bordering[1]]['normal']
    normal_angle = 180. * np.arccos(np.clip(np.dot(n1, n2), -1., 1.)) / np.pi
    results.append({
      'vertex 1': chord[0],
      'vertex 2': chord[1],
      'face 1': bordering[0],
      'face 2': bordering[1],
      'dihedral angle (degrees)': 180. - normal_angle,
      'bevel angle (degrees)': normal_angle / 2.,
    })
  return results


def get_bill_of_materials(vertices, chords, rounding_precision, cost_per_unit_length=None, hub_template_output_path=None, elongation_factors=(1.0, 1.0, 1.0), print_report=True, faces=None, cost_per_unit_area=None, panel_areal_density=None, face_template_output_path=None):

  report = {'pyLair report' : {}}
  
  #
  # compute Bill of Materials
  #
  # Chords belonging to the same strut class can differ by tiny amounts of
  # floating-point noise from the geometry pipeline. Group them by sorting
  # and splitting on gaps larger than a tolerance, rather than
  # independently rounding each length to rounding_precision and
  # bucketing by the rounded value: naive per-value rounding can
  # incorrectly split a single true length whose floating-point noise
  # straddles a rounding boundary. The tolerance is derived from
  # rounding_precision (matching its original role of letting a builder
  # deliberately merge near-identical strut lengths that aren't worth
  # distinguishing for fabrication purposes -- a coarse rounding_precision
  # merges more aggressively), floored by a tiny noise-only tolerance so
  # that even a very fine rounding_precision still merges pure
  # floating-point noise rather than reporting spurious near-duplicate
  # lengths as distinct struts.
  #
  raw_lengths = [np.linalg.norm(vertices[c[0]] - vertices[c[1]]) for c in chords]

  list_bom = []
  scale = max(raw_lengths) if raw_lengths else 0.
  if raw_lengths:
    cluster_tolerance = max(scale * 1e-9, 0.5 * 10 ** (-rounding_precision))

    order = sorted(range(len(raw_lengths)), key=lambda i: raw_lengths[i])
    clusters = [[order[0]]]
    for prev_idx, idx in zip(order, order[1:]):
      if raw_lengths[idx] - raw_lengths[prev_idx] > cluster_tolerance:
        clusters.append([])
      clusters[-1].append(idx)

    for cluster in clusters:
      cluster_lengths = [raw_lengths[i] for i in cluster]
      list_bom.append({
        'length': round(sum(cluster_lengths) / len(cluster_lengths), rounding_precision),
        'count': len(cluster),
      })
  df_bom = pd.DataFrame(list_bom).sort_values(by = ['length'], ascending = False).reset_index(drop = True)

  # a chord under SMALL_CHORD_ARTIFACT_RATIO of the dome's largest strut
  # is almost certainly a truncation-boundary sliver (e.g. from a cutoff
  # landing extremely close to, but not exactly on, a vertex ring) --
  # see module docstring for why this ratio was chosen
  chord_lengths_and_counts = df_bom.to_dict(orient = 'records')
  artifact_length_threshold = scale * SMALL_CHORD_ARTIFACT_RATIO
  artifact_chords = [row for row in chord_lengths_and_counts if row['length'] < artifact_length_threshold]

  dict_bom = {
    'Chord Lengths and Counts' : chord_lengths_and_counts,
    'Warning' : 'Small length chords could be real but unusually short struts, or truncation-'
                'boundary artifacts -- see "Possible truncation-artifact chords" below, and '
                'check any of them with a DXF viewer before you build anything!',
    'Possible truncation-artifact chords' : artifact_chords,
    }

  #
  # display Bill of Materials
  #
  report['pyLair report']['Bill of materials'] = dict_bom

  #
  # total material length/cost, summed from the raw (unclustered,
  # unrounded) lengths to avoid compounding the display rounding
  # already applied above
  #
  total_length = sum(raw_lengths)
  dict_total_material = {
    'Total strut length' : round(total_length, rounding_precision),
    }
  if cost_per_unit_length is not None:
    dict_total_material['Total estimated material cost'] = round(total_length * cost_per_unit_length, 2)
  report['pyLair report']['Total material'] = dict_total_material


  #
  # data structure to store hub information
  #
  hubs = compute_hub_data(vertices, chords, elongation_factors)

  #
  # hub connector templates: one DXF cutting template per unique hub
  # "shape" (see group_hub_types), skipping single-strut hubs (a
  # truncated dome's base row) since there's no angular pattern to
  # draw for those
  #
  if hub_template_output_path is not None:
    hub_groups = group_hub_types(hubs)
    list_hub_templates = []
    template_number = 0
    for group in hub_groups:
      if group['valence'] <= 1:
        continue
      template_number += 1
      template_filename = '%s_hubtype%d.dxf' % (hub_template_output_path, template_number)
      representative = hubs[group['representative_hub']]
      spoke_angles = compute_spoke_angles(representative)
      tangential_angles = {
        s: representative['connected_vertices'][s]['tangential_angle']
        for s in representative['connected_vertices']
        }
      OutputHubConnectorTemplateDXF(spoke_angles, tangential_angles, template_filename)
      list_hub_templates.append({
        'template_file': template_filename,
        'struts_per_hub': group['valence'],
        'hub_count': group['count'],
        })
    report['pyLair report']['Hub Connector Templates'] = list_hub_templates

  #
  # display the tangential plane angles we just calculated
  #
  list_tangential_plane_angles = []
  for h in hubs.keys():
    number_of_connected_vertices = len(hubs[h]['connected_vertices'])
    for c in hubs[h]['connected_vertices']:
      if number_of_connected_vertices == 1:
        angle = np.nan
        note = 'Base hub of truncated sphere, no angle to report'
      else:
        angle = hubs[h]['connected_vertices'][c]['tangential_angle']
        note = ''
        
      list_tangential_plane_angles.append(
        {
          'hub' : h,
          'connecting hub' : c,
          'angle (degrees)' : angle,
          'note' : note,
        }
      )

  df_tangential_plane_angles = pd.DataFrame(list_tangential_plane_angles).sort_values(by = ['hub', 'connecting hub']).reset_index(drop = True)
  dict_tangential_plane_angles = df_tangential_plane_angles.to_dict(orient = 'records')
  report['pyLair report']['Angles at hub between outbound cords and tangential plane'] = dict_tangential_plane_angles

  #
  # display spoke angles
  #
  list_spoke_angles = []
  for hub in hubs.keys():
    spoke_angles = compute_spoke_angles(hubs[hub])
    for spoke, angle_in_degrees in spoke_angles.items():
      list_spoke_angles.append(
        {
          'hub' : hub,
          'connecting hub' : spoke,
          'angle (degrees)' : angle_in_degrees,
        }
      )

  df_spoke_angles = pd.DataFrame(list_spoke_angles).sort_values(by = ['hub', 'connecting hub']).reset_index()
  dict_spoke_angles = df_spoke_angles.to_dict(orient = 'records')
  report['pyLair report']['Spoke angles'] = dict_spoke_angles

  #
  # panel (face) sections: present whenever the caller has face data,
  # which build_dome() always provides -- truncate() clips faces
  # correctly on any combination of axes, see truncation.py
  #
  if faces is not None:
    face_data = compute_face_data(vertices, faces)
    face_groups = group_face_types(face_data)

    list_face_types = [
      {
        'edge_lengths': g['edge_lengths'],
        'area': g['area'],
        'count': g['count'],
        'chiral': g['chiral'],
        'orientations': g['orientations'],
      }
      for g in face_groups
    ]
    # a panel with an edge under SMALL_CHORD_ARTIFACT_RATIO of the
    # dome's largest strut is the panel-side symptom of the same
    # truncation-boundary sliver flagged above for chords -- a
    # near-zero-length edge means a near-zero-area (degenerate) panel
    artifact_panels = [g for g in list_face_types if min(g['edge_lengths']) < artifact_length_threshold]
    report['pyLair report']['Panel shapes and counts'] = {
      'Panel Types and Counts': list_face_types,
      'Warning': 'Panels sharing the same edge lengths can still be mirror images of each '
                 'other (see "chiral") -- check "orientations" before cutting from a '
                 'directional material such as wood grain or printed film.',
      'Possible truncation-artifact panels': artifact_panels,
    }

    total_area = sum(fd['area'] for fd in face_data)
    dict_total_panel_material = {
      'Total panel area': round(total_area, rounding_precision),
    }
    if cost_per_unit_area is not None:
      dict_total_panel_material['Total estimated panel material cost'] = round(total_area * cost_per_unit_area, 2)
    if panel_areal_density is not None:
      dict_total_panel_material['Total estimated panel weight'] = round(total_area * panel_areal_density, 2)
    report['pyLair report']['Total panel material'] = dict_total_panel_material

    report['pyLair report']['Bevel angles at panel edges'] = compute_dihedral_angles(face_data, chords)

    if face_template_output_path is not None:
      list_face_templates = []
      for template_number, group in enumerate(face_groups, start=1):
        template_filename = '%s_facetype%d.dxf' % (face_template_output_path, template_number)
        representative_edges = face_data[group['representative_face']]['edge_lengths']
        OutputFaceTemplateDXF(representative_edges, template_filename)
        list_face_templates.append({
          'template_file': template_filename,
          'edge_lengths': group['edge_lengths'],
          'panel_count': group['count'],
        })
      report['pyLair report']['Panel Cutting Templates'] = list_face_templates

  if print_report:
    print(json.dumps(report, indent = 2))

  return report



  ##
  ## display unprojected spoke angles
  ##
  #print()
  #print('Unprojected spoke angles:')
  #print()
  #print('\thub\tconnecting hub\tangle (degrees)')
  #for hub in hubs.keys():
  #  print('\t' + str(hub))
  #  spoke_list = sorted(hubs[hub]['connected_vertices'])
  #  vertex = hubs[hub]['vertex']
  #  point = hubs[hub]['connected_vertices'][spoke_list[0]]['vertex']
  #  reference_vector = point - vertex
  #  
  #  print('\t\t' + str(spoke_list[0]) + '\t0.0')
  #  
  #  for spoke in spoke_list[1:]:
  #    point = hubs[hub]['connected_vertices'][spoke]['vertex']
  #    comparison_vector = point - vertex

  #    normalized_dot_product = np.dot(reference_vector, comparison_vector) / (np.linalg.norm(reference_vector) * np.linalg.norm(comparison_vector))

  #    if normalized_dot_product < -1.0:
  #      normalized_dot_product = -1.0

  #    angle = np.arccos(normalized_dot_product)
  #    angle_in_degrees = 180. * angle / np.pi

  #    # http://www.opengl.org/discussion_boards/showthread.php/159385-Deriving-angles-from-0-to-360-from-Dot-Product
  #    C = np.cross(reference_vector, comparison_vector)
  #    direction = np.dot(C, vertex)
  #    if direction < 0.:  angle_in_degrees = -1 * angle_in_degrees

  #    print('\t\t' + str(spoke) + '\t' +  str(angle_in_degrees))
