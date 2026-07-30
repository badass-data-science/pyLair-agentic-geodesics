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
# Programmatic entry point for building a geodesic dome/sphere, shared by
# pylair/cli.py and pylair/mcp_server.py so validation and orchestration
# aren't duplicated between them.
#
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List, Optional, Union

import numpy as np

from .polyhedral import Icosahedron, Octahedron, Tetrahedron, Polyhedron, build_lcd_faces
from .symmetry_triangle import ClassOneMethodOneSymmetryTriangle, ClassTwoMethodOneSymmetryTriangle
from .class_three import ClassThreeSymmetryTriangle
from .geodesic_sphere import GeodesicSphere
from .elongation import elongate
from .truncation import truncate


@dataclass
class DomeResult:
  V: list                       # final vertices (post elongation/truncation)
  C: list                       # final chords
  F_sphere: list                # face-node list, correctly clipped to
                                 # match V/C regardless of which axes
                                 # (X/Y/Z, alone or together) were
                                 # truncated -- build_dome always
                                 # derives face data, so this is never
                                 # None (though truncation can clip it
                                 # down to an empty list at an extreme
                                 # enough cutoff)
  truncated: bool
  radius: float
  frequency: int
  dome_class: int
  n_frequency: Optional[int]
  polyhedron: str                # "icosahedron", "octahedron", or "tetrahedron"
  elongation_factors: tuple      # (fx, fy, fz); needed by bill_of_materials'
                                  # ellipsoid-normal calc; not recoverable
                                  # from V/C alone
  truncation_x: Optional[float]
  truncation_y: Optional[float]
  truncation_z: Optional[float]
  vertex_equal_threshold: float


def validate_geometry_params(radius, frequency, dome_class, n_frequency, elongation_factors):
  # The same domain rules cli.py has always enforced (message text kept
  # verbatim from the CLI so tests/test_cli.py's stdout substring checks
  # -- e.g. "n-frequency", "differ", "even", "1, 2, or 3" -- keep matching
  # unchanged now that cli.py raises these via build_dome instead of
  # inline in its argv-parsing loop).
  if radius <= 0:
    raise ValueError('-r or --radius argument must be greater than zero. Exiting.')
  if frequency < 1:
    raise ValueError('-f or --frequency argument must be a positive integer. Exiting.')
  if dome_class not in (1, 2, 3):
    raise ValueError('-c or --class argument must be 1, 2, or 3. Exiting.')
  if n_frequency is not None and n_frequency < 1:
    raise ValueError('-n or --n-frequency argument must be a positive integer. Exiting.')
  if any(f <= 0 for f in elongation_factors):
    raise ValueError('-e or --elongation arguments must each be greater than zero. Exiting.')
  if dome_class == 2 and frequency % 2 != 0:
    raise ValueError('-c 2 (Class II / Triacon) requires an even --frequency. Exiting.')
  if dome_class == 3:
    if n_frequency is None:
      raise ValueError('-c 3 (Class III / Skew) requires -n or --n-frequency. Exiting.')
    if n_frequency == frequency:
      raise ValueError('-c 3 (Class III / Skew) requires --n-frequency to differ from --frequency (equal values are Class II -- use -c 2 instead). Exiting.')


def build_dome(radius=1.0, frequency=4, polyhedron: Union[str, Polyhedron] = 'icosahedron',
                dome_class=1, n_frequency=None, vertex_equal_threshold=1e-7,
                elongation_factors=(1.0, 1.0, 1.0), truncation_x=None, truncation_y=None,
                truncation_z=None) -> DomeResult:
  # `polyhedron` accepts either a name string ("icosahedron"/"octahedron"/
  # "tetrahedron", for MCP callers) or an already-built
  # Icosahedron()/Octahedron()/Tetrahedron() instance (so cli.py, which
  # already constructs one from -p, needs no translation code at its
  # call site).
  validate_geometry_params(radius, frequency, dome_class, n_frequency, elongation_factors)

  if isinstance(polyhedron, str):
    if polyhedron == 'octahedron':
      polyhedral = Octahedron()
    elif polyhedron == 'tetrahedron':
      polyhedral = Tetrahedron()
    else:
      polyhedral = Icosahedron()
  else:
    polyhedral = polyhedron
  if isinstance(polyhedral, Octahedron):
    polyhedron_name = 'octahedron'
  elif isinstance(polyhedral, Tetrahedron):
    polyhedron_name = 'tetrahedron'
  else:
    polyhedron_name = 'icosahedron'

  if dome_class == 2:
    symmetry_triangle = ClassTwoMethodOneSymmetryTriangle(frequency // 2, polyhedral)
    face_source = SimpleNamespace(faces=build_lcd_faces(polyhedral))
    extra_pairs = None
    local_priority = None
  elif dome_class == 3:
    symmetry_triangle = ClassThreeSymmetryTriangle(frequency, n_frequency, polyhedral)
    face_source = polyhedral
    extra_pairs = symmetry_triangle.cross_face_matches
    local_priority = symmetry_triangle.local_priority
  else:
    symmetry_triangle = ClassOneMethodOneSymmetryTriangle(frequency, polyhedral)
    face_source = polyhedral
    extra_pairs = None
    local_priority = None

  sphere = GeodesicSphere(face_source, symmetry_triangle, vertex_equal_threshold, radius,
                           extra_pairs=extra_pairs, local_priority=local_priority)
  C_sphere = sphere.non_duplicate_chords
  F_sphere = sphere.non_duplicate_face_nodes
  V_sphere = sphere.sphere_vertices

  # elongate before truncation, so a truncation ratio describes the
  # dome's final, possibly-elongated extent along that axis
  if any(f != 1.0 for f in elongation_factors):
    V_sphere = elongate(V_sphere, elongation_factors)

  # each axis is truncated independently and sequentially (X, then Y,
  # then Z) when its cutoff is given, so a later axis's cutoff ratio is
  # computed against that axis's range in the already-trimmed vertex
  # set, not the original sphere/ellipsoid's -- the same "describes the
  # final extent" convention elongation already follows above. Face data
  # is threaded through every active axis: truncate()'s clipping is
  # axis-generic and composes correctly across repeated calls (each
  # pass's crossing points are computed fresh from whatever V/C/F it's
  # handed, including any quad-split diagonal chord a previous pass
  # introduced -- see truncation.py's _register_crossing).
  truncated = any(t is not None for t in (truncation_x, truncation_y, truncation_z))
  if truncated:
    V, C, F = V_sphere, C_sphere, F_sphere
    if truncation_x is not None:
      V, C, F = truncate(V, C, truncation_x, axis=0, F_sphere=F)
    if truncation_y is not None:
      V, C, F = truncate(V, C, truncation_y, axis=1, F_sphere=F)
    if truncation_z is not None:
      V, C, F = truncate(V, C, truncation_z, axis=2, F_sphere=F)
    F_out = F
  else:
    V, C, F_out = V_sphere, C_sphere, F_sphere

  return DomeResult(V=V, C=C, F_sphere=F_out, truncated=truncated, radius=radius,
                     frequency=frequency, dome_class=dome_class, n_frequency=n_frequency,
                     polyhedron=polyhedron_name, elongation_factors=tuple(elongation_factors),
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     vertex_equal_threshold=vertex_equal_threshold)
