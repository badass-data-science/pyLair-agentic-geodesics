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
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Depth-cue colors: near struts render close to the original opaque
# steelblue, far struts fade toward a pale, low-contrast gray-blue.
_NEAR_RGB = np.array([0.07, 0.25, 0.45])
_FAR_RGB = np.array([0.75, 0.82, 0.88])


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


def add_depth_cued_wireframe(ax, V, C):
  # get_proj() bakes in the current view and axis limits, so this must be
  # called only after the axes' limits/aspect are already set. Lower
  # projected z is nearer the camera in this view (verified empirically,
  # not assumed) -- without this cue, front and back struts are the same
  # color and the wireframe reads as a flat net instead of a sphere.
  segments = [[V[c[0]], V[c[1]]] for c in C]

  proj = ax.get_proj()
  midpoints = np.array([(np.array(a) + np.array(b)) / 2. for a, b in segments])
  depths = np.array([proj3d.proj_transform(*pt, proj)[2] for pt in midpoints])
  depth_range = depths.max() - depths.min()
  t = np.zeros_like(depths) if depth_range == 0 else (depths - depths.min()) / depth_range

  colors = _NEAR_RGB[None, :] * (1 - t)[:, None] + _FAR_RGB[None, :] * t[:, None]
  alphas = 0.95 - 0.55 * t
  rgba = np.concatenate([colors, alphas[:, None]], axis=1)
  linewidths = 1.3 - 0.7 * t

  # Draw farthest-first so nearer struts are painted on top, reinforcing
  # the depth cue instead of leaving draw order to chance.
  order = np.argsort(-t)
  ax.add_collection3d(Line3DCollection(
      [segments[i] for i in order],
      colors=rgba[order],
      linewidths=linewidths[order],
  ))


def render_preview_png_bytes(V, C):
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')

  xlim, ylim, zlim = equal_axis_limits(V)
  ax.set_xlim(*xlim)
  ax.set_ylim(*ylim)
  ax.set_zlim(*zlim)
  ax.set_box_aspect((1, 1, 1))

  add_depth_cued_wireframe(ax, V, C)

  ax.set_title('pyLair preview')
  buf = io.BytesIO()
  fig.savefig(buf, format='png', dpi=130)
  plt.close(fig)
  return buf.getvalue()


def save_preview(V, C, the_filename):
  with open(the_filename, 'wb') as outfile:
    outfile.write(render_preview_png_bytes(V, C))


def render_assembly_schematic_png_bytes(V, C, manifest, show_hub_labels=False,
                                         show_strut_labels=False, show_panel_labels=False,
                                         fontsize=6):
  """Same depth-cued wireframe as render_preview_png_bytes, with each
  instance's own pylair.assembly label (see build_assembly_manifest)
  optionally drawn at its hub position / strut midpoint / panel
  centroid. Every show_*_labels flag defaults to False -- calling this
  with only V, C, manifest renders identically to render_preview_png_bytes,
  and this function is never called by anything that generates the
  book's own preview images, so existing images are unaffected either
  way. Labels are opt-in per kind because a real dome has far more
  struts than hubs and far more panels than either -- turning all three
  on at once past a low frequency produces an unreadable smear of text,
  not a usable schematic; a caller building a real assembly diagram
  should turn on only the label kind relevant to whatever's being
  documented (e.g. hub labels for a connector-wiring diagram, panel
  labels for a skin-panel layout diagram), or pass a manifest that's
  already been filtered down to one ring/subassembly.
  """
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')

  xlim, ylim, zlim = equal_axis_limits(V)
  ax.set_xlim(*xlim)
  ax.set_ylim(*ylim)
  ax.set_zlim(*zlim)
  ax.set_box_aspect((1, 1, 1))

  add_depth_cued_wireframe(ax, V, C)

  if show_hub_labels:
    for label, hub in manifest['hubs'].items():
      x, y, z = hub['position']
      ax.text(x, y, z, label, fontsize=fontsize, color='black')

  if show_strut_labels:
    for label, strut in manifest['struts'].items():
      a = np.array(manifest['hubs'][strut['hub_1']]['position'])
      b = np.array(manifest['hubs'][strut['hub_2']]['position'])
      midpoint = (a + b) / 2.
      ax.text(*midpoint, label, fontsize=fontsize, color='darkgreen')

  if show_panel_labels:
    for label, panel in manifest['panels'].items():
      x, y, z = panel['centroid']
      ax.text(x, y, z, label, fontsize=fontsize, color='darkred')

  ax.set_title('pyLair assembly schematic')
  buf = io.BytesIO()
  fig.savefig(buf, format='png', dpi=130)
  plt.close(fig)
  return buf.getvalue()


def save_assembly_schematic(V, C, manifest, the_filename, **kwargs):
  with open(the_filename, 'wb') as outfile:
    outfile.write(render_assembly_schematic_png_bytes(V, C, manifest, **kwargs))
