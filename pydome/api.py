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
# Programmatic entry point for building a geodesic dome/sphere, shared by
# pydome/cli.py and pydome/mcp_server.py so validation and orchestration
# aren't duplicated between them.
#
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List, Optional, Union

import numpy as np

from .polyhedral import Icosahedron, Octahedron, Polyhedron, build_lcd_faces
from .symmetry_triangle import ClassOneMethodOneSymmetryTriangle, ClassTwoMethodOneSymmetryTriangle
from .class_three import ClassThreeSymmetryTriangle
from .geodesic_sphere import GeodesicSphere
from .elongation import elongate
from .truncation import truncate


@dataclass
class DomeResult:
  V: list                       # final vertices (post elongation/truncation)
  C: list                       # final chords
  F_sphere: Optional[list]      # face-node list; None when truncated, since
                                 # truncate() doesn't recompute faces (stale
                                 # w.r.t. the truncated V/C otherwise -- this
                                 # is why cli.py forbids -F/-s/-O with -t)
  truncated: bool
  radius: float
  frequency: int
  dome_class: int
  n_frequency: Optional[int]
  polyhedron: str                # "icosahedron" or "octahedron"
  elongation_factor: float       # needed by bill_of_materials' ellipsoid-
                                  # normal calc; not recoverable from V/C alone
  truncation_amount: Optional[float]
  vertex_equal_threshold: float


def validate_geometry_params(radius, frequency, dome_class, n_frequency, elongation_factor):
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
  if elongation_factor <= 0:
    raise ValueError('-e or --elongation argument must be greater than zero. Exiting.')
  if dome_class == 2 and frequency % 2 != 0:
    raise ValueError('-c 2 (Class II / Triacon) requires an even --frequency. Exiting.')
  if dome_class == 3:
    if n_frequency is None:
      raise ValueError('-c 3 (Class III / Skew) requires -n or --n-frequency. Exiting.')
    if n_frequency == frequency:
      raise ValueError('-c 3 (Class III / Skew) requires --n-frequency to differ from --frequency (equal values are Class II -- use -c 2 instead). Exiting.')


def validate_output_combo(run_truncate, face_output=False, stl_output=False, obj_output=False):
  # -F, -s, and -O all require face data, which truncate() does not
  # recompute, so none of them can be combined with truncation without
  # producing stale/incorrect geometry.
  if run_truncate and (face_output or stl_output or obj_output):
    raise ValueError('Truncation does not work with face-based output (-F/-s/-O) at this time. Use either -t or one of those, but not both.')


def build_dome(radius=1.0, frequency=4, polyhedron: Union[str, Polyhedron] = 'icosahedron',
                dome_class=1, n_frequency=None, vertex_equal_threshold=1e-7,
                elongation_factor=1.0, truncation_amount=None) -> DomeResult:
  # `polyhedron` accepts either a name string ("icosahedron"/"octahedron",
  # for MCP callers) or an already-built Icosahedron()/Octahedron()
  # instance (so cli.py, which already constructs one from -p, needs no
  # translation code at its call site).
  validate_geometry_params(radius, frequency, dome_class, n_frequency, elongation_factor)

  if isinstance(polyhedron, str):
    polyhedral = Octahedron() if polyhedron == 'octahedron' else Icosahedron()
  else:
    polyhedral = polyhedron
  polyhedron_name = 'octahedron' if isinstance(polyhedral, Octahedron) else 'icosahedron'

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
  # dome's final, possibly-elongated height range
  if elongation_factor != 1.0:
    V_sphere = elongate(V_sphere, elongation_factor)

  truncated = truncation_amount is not None
  if truncated:
    V, C = truncate(V_sphere, C_sphere, truncation_amount)
    F_out = None
  else:
    V, C, F_out = V_sphere, C_sphere, F_sphere

  return DomeResult(V=V, C=C, F_sphere=F_out, truncated=truncated, radius=radius,
                     frequency=frequency, dome_class=dome_class, n_frequency=n_frequency,
                     polyhedron=polyhedron_name, elongation_factor=elongation_factor,
                     truncation_amount=truncation_amount, vertex_equal_threshold=vertex_equal_threshold)
