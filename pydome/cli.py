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
# load useful modules
#
import numpy as np
import getopt
import sys
from types import SimpleNamespace

#
# load pyDome modules
#
from .polyhedral import Icosahedron, Octahedron, build_lcd_faces
from .symmetry_triangle import ClassOneMethodOneSymmetryTriangle, ClassTwoMethodOneSymmetryTriangle
from .geodesic_sphere import GeodesicSphere
from .output import OutputDXF, OutputWireframeVRML, OutputFaceVRML, OutputSTL, OutputOBJ
from .truncation import truncate
from .bill_of_materials import get_bill_of_materials
from .preview import save_preview
from .elongation import elongate


def display_help():
  help_text = """pyDome:  A geodesic dome calculator. Copyright 2013 by Emily Williams

Required Command-Line Input:

\t-o, --output=\tPath to output file(s). Extensions will be added. Generates DXF and WRL files by default, but only WRL file when "-F" option is active. Example:  "-o output/test" produces files output/test.wrl and output/test.dxf.

Options:

\t-r, --radius\tRadius of generated dome. Must be a floating point number greater than zero. Default 1.0.

\t-f, --frequency\tFrequency of generated dome. Must be a positive integer. Default 4.

\t-v, --vthreshold\tDistance required to consider two vertices equal. Default 0.0000001. Must be floating point.

\t-t, --truncation\tDistance (ratio) from the bottom to truncate. Default 0.499999. I advise using only the default or 0.333333. Must be floating point.

\t-b, --bom-rounding\tThe number of decimal places to round chord length output in the generated Bill of Materials. Also controls how aggressively near-identical strut lengths are merged into one entry: a lower value merges more, which is useful for treating fabrication-irrelevant differences as the same length, but can merge genuinely distinct lengths together at high dome frequencies. Default 9, which is fine enough to keep all distinct lengths separate at any practical frequency. Must be an integer.

\t-p, --polyhedron\tEither "octahedron" or "icosahedron". Default icosahedron.

\t-c, --class\tSubdivision class: 1 (Alternate) or 2 (Triacon). Class 2 requires an even --frequency, since each original edge is already implicitly split once by its construction. Default 1.

\t-F, --face\tFlag specifying whether to generate face output in WRL file. Cancels DXF file output and cannot be used with truncation.

\t-P, --preview\tAlso save a quick 3D wireframe preview image ("<output>.png") alongside the usual output files, so you can sanity-check the dome without opening a CAD or VRML viewer.

\t-s, --stl\tAlso save an STL file ("<output>.stl") of the dome's surface triangles, e.g. for 3D-printing a scale model. Requires face data, so cannot be used with truncation.

\t-O, --obj\tAlso save an OBJ file ("<output>.obj") of the dome's surface triangles. Requires face data, so cannot be used with truncation.

\t-m, --material-cost\tPrice per unit length of strut material. If given, adds an estimated total material cost to the Bill of Materials, in addition to the total strut length (which is always reported). Must be a positive floating point number.

\t-H, --hub-templates\tAlso save one 2D DXF cutting template per unique hub connector shape ("<output>_hubtype1.dxf", "<output>_hubtype2.dxf", ...), for laser-cutting/CNC connector plates. Each template shows one radiating line per strut at its spoke angle, labeled with that strut's tangential (out-of-plane) deflection angle.

\t-e, --elongation\tStretches the dome along its vertical (Z) axis by this factor before truncation, turning the sphere into an axis-aligned ellipsoid -- values > 1 raise the ceiling height, values < 1 flatten it for a wider footprint. All angle-based output (Bill of Materials angles, hub connector templates) correctly accounts for the resulting ellipsoid's true surface normal, not just the sphere approximation. Must be a positive floating point number. Default 1.0 (no elongation).
"""
  print(help_text)

def main():

  #
  # default values
  #
  radius = np.float64(1.)
  frequency = 4
  dome_class = 1
  polyhedral = Icosahedron()
  vertex_equal_threshold = 0.0000001
  truncation_amount = 0.499999
  run_truncate = False
  bom_rounding_precision = 9
  face_output = False
  preview_output = False
  stl_output = False
  obj_output = False
  cost_per_unit_length = None
  hub_templates_output = False
  elongation_factor = 1.0
  output_path = None

  #
  # no input arguments
  #
  if len(sys.argv[1:]) == 0:
    display_help()
    sys.exit(-1)

  #
  # parse command line
  #
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:f:v:t:b:p:c:m:e:FPsOHho:', ['truncation=', 'vthreshold=', 'radius=', 'frequency=', 'help', 'bom-rounding=', 'polyhedron=', 'class=', 'material-cost=', 'elongation=', 'face', 'preview', 'stl', 'obj', 'hub-templates', 'output='])
  except getopt.error as msg:
    print(str(msg) + ' (for help use --help)')
    sys.exit(-1)
  for o, a in opts:
    if o in ('-o', '--output'):
      output_path = a
    if o in ('-p', '--polyhedron'):
      if a == 'octahedron':
        polyhedral = Octahedron()
    if o in ('-c', '--class'):
      try:
        dome_class = int(a)
      except ValueError:
        print('-c or --class argument must be an integer (1 or 2). Exiting.')
        sys.exit(-1)
      if dome_class not in (1, 2):
        print('-c or --class argument must be 1 or 2. Exiting.')
        sys.exit(-1)
    if o in ('-b', '--bom-rounding'):
      try:
        bom_rounding_precision = int(a)
      except ValueError:
        print('-b or --bom-rounding argument must be an integer. Exiting.')
        sys.exit(-1)
    if o in ('-m', '--material-cost'):
      try:
        cost_per_unit_length = float(a)
      except ValueError:
        print('-m or --material-cost argument must be a floating point number. Exiting.')
        sys.exit(-1)
      if cost_per_unit_length <= 0:
        print('-m or --material-cost argument must be greater than zero. Exiting.')
        sys.exit(-1)
    if o in ('-e', '--elongation'):
      try:
        elongation_factor = float(a)
      except ValueError:
        print('-e or --elongation argument must be a floating point number. Exiting.')
        sys.exit(-1)
      if elongation_factor <= 0:
        print('-e or --elongation argument must be greater than zero. Exiting.')
        sys.exit(-1)
    if o in ('-h', '--help'):
      display_help()
      sys.exit(0)
    if o in ('-F', '--face'):
      face_output = True
    if o in ('-P', '--preview'):
      preview_output = True
    if o in ('-s', '--stl'):
      stl_output = True
    if o in ('-O', '--obj'):
      obj_output = True
    if o in ('-H', '--hub-templates'):
      hub_templates_output = True
    if o in ('-r', '--radius'):
      try:
        a = float(a)
        radius = np.float64(a)
      except ValueError:
        print('-r or --radius argument must be a floating point number. Exiting.')
        sys.exit(-1)
      if radius <= 0:
        print('-r or --radius argument must be greater than zero. Exiting.')
        sys.exit(-1)
    if o in ('-f', '--frequency'):
      try:
        frequency = int(a)
      except ValueError:
        print('-f or --frequency argument must be an integer. Exiting.')
        sys.exit(-1)
      if frequency < 1:
        print('-f or --frequency argument must be a positive integer. Exiting.')
        sys.exit(-1)
    if o in ('-v', '--vthreshold'):
      try:
        a = float(a)
        vertex_equal_threshold = np.float64(a)
      except ValueError:
        print('-v or --vthreshold argument must be a floating point number. Exiting.')
        sys.exit(-1)
    if o in ('-t', '--truncation'):
      try:
        a = float(a)
        truncation_amount = np.float64(a)
        run_truncate = True
      except ValueError:
        print('-t or --truncation argument must be a floating point number. Exiting.')
        sys.exit(-1)

  #
  # check for required options
  #
  if output_path == None:
    print('An output path and filename is required. Use the -o argument. Exiting.')
    sys.exit(-1)

  #
  # check for mutually exclusive options
  #
  # -F, -s, and -O all require face data, which truncate() does not
  # recompute, so none of them can be combined with truncation without
  # producing stale/incorrect geometry.
  if run_truncate and (face_output or stl_output or obj_output):
    print('Truncation does not work with face-based output (-F/-s/-O) at this time. Use either -t or one of those, but not both.')
    sys.exit(-1)

  if dome_class == 2 and frequency % 2 != 0:
    print('-c 2 (Class II / Triacon) requires an even --frequency. Exiting.')
    sys.exit(-1)

  #
  # generate geodesic sphere
  #
  if dome_class == 2:
    symmetry_triangle = ClassTwoMethodOneSymmetryTriangle(frequency // 2, polyhedral)
    face_source = SimpleNamespace(faces=build_lcd_faces(polyhedral))
  else:
    symmetry_triangle = ClassOneMethodOneSymmetryTriangle(frequency, polyhedral)
    face_source = polyhedral
  sphere = GeodesicSphere(face_source, symmetry_triangle, vertex_equal_threshold, radius)
  C_sphere = sphere.non_duplicate_chords
  F_sphere = sphere.non_duplicate_face_nodes
  V_sphere = sphere.sphere_vertices

  #
  # elongate (before truncation, so a truncation ratio applies to the
  # dome's final, possibly-elongated height range)
  #
  if elongation_factor != 1.0:
    V_sphere = elongate(V_sphere, elongation_factor)

  #
  # truncate
  #
  V = V_sphere
  C = C_sphere
  if run_truncate:
    V, C = truncate(V_sphere, C_sphere, truncation_amount)

  #
  # write model output
  #
  if face_output:
    OutputFaceVRML(V, F_sphere, output_path + '.wrl')
  else:
    OutputWireframeVRML(V, C, output_path + '.wrl')
    OutputDXF(V, C, output_path + '.dxf')

  #
  # preview image
  #
  if preview_output:
    save_preview(V, C, output_path + '.png')

  #
  # mesh export
  #
  if stl_output:
    OutputSTL(V, F_sphere, output_path + '.stl')
  if obj_output:
    OutputOBJ(V, F_sphere, output_path + '.obj')

  #
  # bill of materials
  #
  hub_template_output_path = output_path if hub_templates_output else None
  get_bill_of_materials(V, C, bom_rounding_precision, cost_per_unit_length, hub_template_output_path, elongation_factor)

#
# run the main function
#
if __name__ == "__main__":
  main()
