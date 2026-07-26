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


import numpy as np

PI = np.pi

from .polyhedral import Vertex


class SymmetryTriangle(object):

  def convertRCNotationToVertexIndex(self, r, c):
    cnt = 0;
    for i in range(len(self.row_list)):
      for j in range(len(self.row_list[i])):
        if (i == r) and (j == c):
          return cnt
        cnt = cnt + 1;
    return cnt

  def __init__(self, chord_frequency):

    # self.chord_list and self.face_list contain integers indicating local position
    # on the symmetry triangle, and therefore do not use the Chord and Face 
    # classes defined in polyhedral.py

    # specify chords
    self.chord_list = []
    for r in range(len(self.row_list)):
      for c in range(0, len(self.row_list[r])):

        if r + c != chord_frequency:
          the_start = self.convertRCNotationToVertexIndex(r, c)
          the_end = self.convertRCNotationToVertexIndex(r+1, c)
          self.chord_list.append([the_start, the_end])
	
          the_start = self.convertRCNotationToVertexIndex(r, c)
          the_end = self.convertRCNotationToVertexIndex(r, c+1)
          self.chord_list.append([the_start, the_end])

        if c != 0:
          the_start = self.convertRCNotationToVertexIndex(r, c);
          the_end = self.convertRCNotationToVertexIndex(r+1, c-1);
          self.chord_list.append([the_start, the_end])

    # specify faces
    self.face_list = []
    for r in range(len(self.row_list)):
      for c in range(0, len(self.row_list[r]) - 1):
        the_first = self.convertRCNotationToVertexIndex(r, c)
        the_second = self.convertRCNotationToVertexIndex(r, c+1)
        the_third = self.convertRCNotationToVertexIndex(r+1, c)
        self.face_list.append([the_first, the_second, the_third])

        if c != 0 and r + 1 != chord_frequency:
          the_first = self.convertRCNotationToVertexIndex(r+1, c-1)
          the_second = self.convertRCNotationToVertexIndex(r, c)
          the_third = self.convertRCNotationToVertexIndex(r+1, c)
          self.face_list.append([the_first, the_second, the_third])



class ClassOneMethodOneSymmetryTriangle(SymmetryTriangle):
  def __init__(self, f, polyhedral):

    # specify vertices
    CL = polyhedral.ppt_side_length
    self.row_list = []
    self.vertices = []
    for r in range(0, f + 1):
      col_list = []
      for c in range(0, f - r + 1):
        x = ((CL / np.float64(f)) * np.float64(r) * np.cos(PI / 3.)) + (CL / np.float64(f)) * np.float64(c) - (CL / np.float64(2.));
        y = (CL / np.float64(f)) * np.float64(r) * np.sin(PI / 3.) - ((CL / np.float64(3.)) * np.sin(PI / np.float64(3)));
        col_list.append(Vertex(x, y, 0.))
        self.vertices.append(Vertex(x, y, 0.))
      self.row_list.append(col_list)

    super(ClassOneMethodOneSymmetryTriangle, self).__init__(f)


class ClassTwoMethodOneSymmetryTriangle(SymmetryTriangle):
  # Class II ("Triacon") subdivision. polyhedral.build_lcd_faces splits
  # each polyhedron face into six 30-60-90 LCD (lowest common
  # denominator) right triangles around its centroid; this class
  # produces the flat, frequency-m grid for ONE such LCD triangle,
  # which GeodesicSphere then replicates across all of them (one per
  # LCD face rather than one per original polyhedron face).
  #
  # Local corners, matching build_lcd_faces's (vertex, midpoint,
  # centroid) argument order: A = the original face vertex, M = the
  # adjacent edge's midpoint (the right angle -- a triangle's median
  # is also its altitude), G = the face centroid. Leg A-M has length
  # CL/2 (half the original edge); leg M-G has length CL*sqrt(3)/6.
  #
  # m here is half the requested dome frequency: Class II is only
  # defined at even frequencies, since each original edge is already
  # implicitly split once (at its midpoint) by the LCD construction
  # itself, before this grid subdivides each LCD triangle m further.
  def __init__(self, m, polyhedral):
    CL = polyhedral.ppt_side_length
    p = CL / np.float64(2.)
    q = CL * np.sqrt(np.float64(3.)) / np.float64(6.)

    # Local (2D) positions of the LCD triangle's own corners: A at the
    # local origin, M along the local x-axis (a real LCD-triangle edge,
    # length p), G positioned via the actual triangle geometry (leg
    # length q, right angle at M).
    A_local = np.array([0., 0.])
    M_local = np.array([p, 0.])
    G_local = np.array([p, q])
    origin_local = (A_local + M_local + G_local) / np.float64(3.)

    # GeodesicSphere places each grid point via
    # origin_3D + a*x_dir + b*y_dir, where x_dir=unit(v2-v1) and
    # y_dir=unit(v3-origin) come from Face.transfer_matrix. Unlike
    # Class I's equilateral triangle (where vertex-to-centroid happens
    # to be perpendicular to the opposite edge, since median=altitude
    # there), this LCD triangle's x_dir/y_dir are NOT orthogonal, so
    # solve for each point's (a, b) in that actual oblique basis
    # rather than assuming an orthonormal one.
    x_dir_local = (M_local - A_local)
    x_dir_local = x_dir_local / np.linalg.norm(x_dir_local)
    y_dir_local = (G_local - origin_local)
    y_dir_local = y_dir_local / np.linalg.norm(y_dir_local)
    basis = np.transpose(np.array([x_dir_local, y_dir_local]))

    self.row_list = []
    self.vertices = []
    for r in range(0, m + 1):
      col_list = []
      for c in range(0, m - r + 1):
        target_local = A_local + (np.float64(r) / m) * (G_local - A_local) + (np.float64(c) / m) * (M_local - A_local)
        a, b = np.linalg.solve(basis, target_local - origin_local)
        col_list.append(Vertex(a, b, 0.))
        self.vertices.append(Vertex(a, b, 0.))
      self.row_list.append(col_list)

    super(ClassTwoMethodOneSymmetryTriangle, self).__init__(m)

