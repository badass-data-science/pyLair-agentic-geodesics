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


import numpy as np
from scipy.spatial import cKDTree

class GeodesicSphere():
  def __init__(self, polyhedral, symmetry_triangle, vpt, radius):
    self.vertex_proximity_threshold = vpt
    self.polyhedral = polyhedral
    self.symmetry_triangle = symmetry_triangle
    self.radius = radius

    self.assemble_unprojected_vertices()
    self.assemble_unprojected_chords_and_faces()

    node_2_idx, duplicate_vertex_2_correct_vertex = self.locate_duplicate_vertices()
    self.remove_duplicate_chords(node_2_idx, duplicate_vertex_2_correct_vertex)
    self.relabel_face_nodes(node_2_idx, duplicate_vertex_2_correct_vertex)
    self.project_onto_sphere()

  def assemble_unprojected_vertices(self):
    self.unprojected_vertices = []
    for origin, M in [(x.origin, x.transfer_matrix) for x in self.polyhedral.faces]:
      for vi in self.symmetry_triangle.vertices:
        new_vi = M @ vi.xyz + origin

        self.unprojected_vertices.append(new_vi)
    
  def assemble_unprojected_chords_and_faces(self):
    self.unprojected_chords = []
    self.unprojected_faces = []
    for n in range(len(self.polyhedral.faces)):
      self.unprojected_chords.extend([[x[0]+n*len(self.symmetry_triangle.vertices), x[1]+n*len(self.symmetry_triangle.vertices)] for x in self.symmetry_triangle.chord_list])
      self.unprojected_faces.extend([[x[0]+n*len(self.symmetry_triangle.vertices), x[1]+n*len(self.symmetry_triangle.vertices), x[2]+n*len(self.symmetry_triangle.vertices)] for x in self.symmetry_triangle.face_list])
    


  def locate_duplicate_vertices(self):
    # Find every pair of vertices closer than vertex_proximity_threshold
    # (these arise where adjacent polyhedron faces share an edge, so the
    # replicated symmetry triangle produces near-identical points) using a
    # KD-tree instead of an O(n^2) all-pairs scan, then union those pairs
    # into clusters. Each cluster collapses to its lowest-indexed member,
    # matching the original algorithm's "earliest vertex wins" behavior.
    n = len(self.unprojected_vertices)
    points = np.array(self.unprojected_vertices)
    pairs = cKDTree(points).query_pairs(self.vertex_proximity_threshold)

    parent = list(range(n))

    def find(x):
      while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
      return x

    for i, j in pairs:
      root_i, root_j = find(i), find(j)
      if root_i != root_j:
        lo, hi = (root_i, root_j) if root_i < root_j else (root_j, root_i)
        parent[hi] = lo

    clusters = {}
    for idx in range(n):
      clusters.setdefault(find(idx), []).append(idx)

    self.non_duplicate_vertices = []

    duplicate_vertex_2_correct_vertex = {}
    node_2_idx = {}

    for out_idx, root in enumerate(sorted(clusters.keys())):
      canonical_node = root + 1
      node_2_idx[canonical_node] = out_idx + 1
      self.non_duplicate_vertices.append(self.unprojected_vertices[root])
      for member in clusters[root]:
        duplicate_vertex_2_correct_vertex[member + 1] = canonical_node

    return node_2_idx, duplicate_vertex_2_correct_vertex



  def remove_duplicate_chords(self, node_2_idx, duplicate_vertex_2_correct_vertex):
    C = []
    for c in self.unprojected_chords:
      a = c[0]
      b = c[1]
      new_a = node_2_idx[ duplicate_vertex_2_correct_vertex[a]]
      new_b = node_2_idx[ duplicate_vertex_2_correct_vertex[b]]
      C.append( sorted([new_a, new_b]) )

    C_dict = {}
    for c in C:
      a = str(c[0])
      b = str(c[1])
      C_dict[a + '_' + b] = True

    self.non_duplicate_chords = []
    for c in C_dict.keys():
      a = int( c.split('_')[0] )
      b = int( c.split('_')[1] )
      self.non_duplicate_chords.append( [a, b] )


  def relabel_face_nodes(self, node_2_idx, duplicate_vertex_2_correct_vertex):
    self.non_duplicate_face_nodes = []
    for f in self.unprojected_faces:
      a = f[0]
      b = f[1]
      c = f[2]

      new_a = node_2_idx[ duplicate_vertex_2_correct_vertex[a]]
      new_b = node_2_idx[ duplicate_vertex_2_correct_vertex[b]]
      new_c = node_2_idx[ duplicate_vertex_2_correct_vertex[c]]
      self.non_duplicate_face_nodes.append( [new_a, new_b, new_c] )

  def project_onto_sphere(self):
    self.sphere_vertices = []
    for v in self.non_duplicate_vertices:
      unit_v = v / np.linalg.norm(v)
      self.sphere_vertices.append(unit_v * self.radius)
