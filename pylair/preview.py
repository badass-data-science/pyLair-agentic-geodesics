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
