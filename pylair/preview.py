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

import io

import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


def equal_axis_limits(vertices):
  # Give every axis the same span, each centered on that axis's own data
  # midpoint. matplotlib's 3D axes scale each axis independently to fill
  # the plot box by default, so without this a dome with a smaller Z
  # range than X/Y (e.g. anything truncated) would render visibly
  # squashed -- a spherical dome must not be mistakable for an
  # elliptical one just because of how it's plotted.
  points = np.array(vertices)
  mins = points.min(axis=0)
  maxs = points.max(axis=0)
  mids = (mins + maxs) / 2.

  half_range = (maxs - mins).max() / 2.
  if half_range == 0:
    half_range = 1.

  return tuple((mids[i] - half_range, mids[i] + half_range) for i in range(3))


def render_preview_png_bytes(V, C):
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')

  segments = [[V[c[0]], V[c[1]]] for c in C]
  ax.add_collection3d(Line3DCollection(segments, colors='steelblue', linewidths=0.8))

  xlim, ylim, zlim = equal_axis_limits(V)
  ax.set_xlim(*xlim)
  ax.set_ylim(*ylim)
  ax.set_zlim(*zlim)
  ax.set_box_aspect((1, 1, 1))

  ax.set_title('pyLair preview')
  buf = io.BytesIO()
  fig.savefig(buf, format='png', dpi=130)
  plt.close(fig)
  return buf.getvalue()


def save_preview(V, C, the_filename):
  with open(the_filename, 'wb') as outfile:
    outfile.write(render_preview_png_bytes(V, C))
