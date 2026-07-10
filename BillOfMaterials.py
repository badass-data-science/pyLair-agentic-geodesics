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

def get_bill_of_materials(vertices, chords, rounding_precision):

  report = {'pyDome report' : {}}
  
  #
  # compute Bill of Materials
  #
  # Chords belonging to the same strut class can differ by tiny amounts of
  # floating-point noise from the geometry pipeline. Group them by sorting
  # and splitting on gaps larger than a small tolerance relative to the
  # largest chord, rather than independently rounding each length to
  # rounding_precision and bucketing by the rounded value: at high
  # frequency, two genuinely distinct strut lengths can differ by less
  # than rounding_precision's granularity and be silently merged by
  # per-value rounding, or a single true length whose floating-point
  # noise straddles a rounding boundary can be incorrectly split in two.
  # rounding_precision is applied only to the displayed length below, not
  # to the grouping decision itself.
  #
  raw_lengths = [np.linalg.norm(vertices[c[0]] - vertices[c[1]]) for c in chords]

  list_bom = []
  if raw_lengths:
    scale = max(raw_lengths)
    cluster_tolerance = scale * 1e-9

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
  # data structure to store hub information
  #
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
    for c in hubs[h]['connected_vertices']:
      A = vertex
      B = vertex - hubs[h]['connected_vertices'][c]['vertex']
      angle = (np.pi/2) - np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))
      angle_in_degrees = 180. * angle / np.pi
      hubs[h]['connected_vertices'][c]['tangential_angle'] = angle_in_degrees

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
  # spoke angles 
  #
  for hub in hubs.keys():
    normal_vector = hubs[hub]['vertex'] / np.linalg.norm(hubs[hub]['vertex'])
    point_on_plane = hubs[hub]['vertex']
    line_origin = np.array([0., 0., 0.])
    for spoke in hubs[hub]['connected_vertices']:
      line = hubs[hub]['connected_vertices'][spoke]['vertex'] / np.linalg.norm(hubs[hub]['connected_vertices'][spoke]['vertex'])
      d = np.dot((point_on_plane - line_origin), normal_vector) / np.dot(line, normal_vector)   # http://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
      hubs[hub]['connected_vertices'][spoke]['point_of_tangential_plane_intersection'] = d * line

  #
  # display spoke angles
  #
  list_spoke_angles = []
  for hub in hubs.keys():
    spoke_list = sorted(hubs[hub]['connected_vertices'])
    vertex = hubs[hub]['vertex']
    point = hubs[hub]['connected_vertices'][spoke_list[0]]['point_of_tangential_plane_intersection']
    reference_vector = point - vertex

    list_spoke_angles.append(
      {
        'hub' : hub,
        'connecting hub' : spoke_list[0],
        'angle (degrees)' : 0.,
      }
    )
    
    for spoke in spoke_list[1:]:
      point = hubs[hub]['connected_vertices'][spoke]['point_of_tangential_plane_intersection']
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
