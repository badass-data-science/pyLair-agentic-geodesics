#    pyDome:  A geodesic dome calculator
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

from .output import OutputHubConnectorTemplateDXF


def _ellipsoid_normal(vertex, elongation_factor):
  # The outward surface normal of an axis-aligned ellipsoid (semi-axes
  # a, a, a*elongation_factor, Z being the elongated axis -- see
  # pydome.elongation) at a point on its surface, from the gradient of
  # its implicit equation x^2/a^2 + y^2/a^2 + z^2/(a*elongation_factor)^2
  # = 1: proportional to (x, y, z/elongation_factor^2). The absolute
  # scale `a` cancels out in the normalization below, so only the
  # elongation factor matters. Reduces exactly to the ordinary sphere
  # normal (the normalized position vector) when elongation_factor == 1
  # -- a sphere's surface normal is always radial, but an ellipsoid's
  # generally is not, except at the poles/equator.
  direction = np.array([vertex[0], vertex[1], vertex[2] / (elongation_factor ** 2)])
  return direction / np.linalg.norm(direction)


def compute_hub_data(vertices, chords, elongation_factor=1.0):
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
    normal = _ellipsoid_normal(vertex, elongation_factor)
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
    normal_vector = _ellipsoid_normal(hubs[hub]['vertex'], elongation_factor)
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


def get_bill_of_materials(vertices, chords, rounding_precision, cost_per_unit_length=None, hub_template_output_path=None, elongation_factor=1.0):

  report = {'pyDome report' : {}}
  
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
  if raw_lengths:
    scale = max(raw_lengths)
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

  dict_bom = {
    'Chord Lengths and Counts' : df_bom.to_dict(orient = 'records'),
    'Warning' : 'Small length chords could be artifacts, so check them with a DXF viewer before you build anything!',
    }
  
  #
  # display Bill of Materials
  #
  report['pyDome report']['Bill of materials'] = dict_bom

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
  report['pyDome report']['Total material'] = dict_total_material


  #
  # data structure to store hub information
  #
  hubs = compute_hub_data(vertices, chords, elongation_factor)

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
    report['pyDome report']['Hub Connector Templates'] = list_hub_templates

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
  report['pyDome report']['Angles at hub between outbound cords and tangential plane'] = dict_tangential_plane_angles

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
  report['pyDome report']['Spoke angles'] = dict_spoke_angles

  print(json.dumps(report, indent = 2))


      
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
