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
# load useful modules
#
import numpy as np
import getopt
import sys

#
# load pyLair modules
#
from .polyhedral import Icosahedron, Octahedron
from .output import OutputDXF, OutputWireframeVRML, OutputFaceVRML, OutputSTL, OutputOBJ
from .bill_of_materials import get_bill_of_materials
from .preview import save_preview
from .api import build_dome


def display_help():
  help_text = """pyLair:  A geodesic dome calculator. Copyright 2013 by Emily Williams

Required Command-Line Input:

\t-o, --output=\tPath to output file(s). Extensions will be added. Generates DXF and WRL files by default, but only WRL file when "-F" option is active. Example:  "-o output/test" produces files output/test.wrl and output/test.dxf.

Options:

\t-r, --radius\tRadius of generated dome. Must be a floating point number greater than zero. Default 1.0.

\t-f, --frequency\tFrequency of generated dome. Must be a positive integer. Default 4.

\t-v, --vthreshold\tDistance required to consider two vertices equal. Default 0.0000001. Must be floating point.

\t-t, --truncation\tDistance (ratio, 0-1) from the minimum Z (vertical) extent to truncate -- keeps the portion above this fraction, discards the rest. Passing this enables Z-axis truncation; if omitted the dome is left whole along Z (see -x/-y for the other two axes). I advise using only 0.499999 or 0.333333. Must be floating point.

\t-x, --truncation-x\tSame truncation rule as -t, but along X instead of Z: keeps the portion of the dome above this fraction (0-1) of its X extent, discards the rest. Off by default. Combine with -t/-y to clip more than one axis; each axis's cutoff is computed against that axis's range *after* any earlier axis has already been trimmed (truncation is applied in X, then Y, then Z order). Must be floating point.

\t-y, --truncation-y\tSame truncation rule as -t, but along Y instead of Z. Off by default. See -x for how combining axes works. Must be floating point.

\t-b, --bom-rounding\tThe number of decimal places to round chord length output in the generated Bill of Materials. Also controls how aggressively near-identical strut lengths are merged into one entry: a lower value merges more, which is useful for treating fabrication-irrelevant differences as the same length, but can merge genuinely distinct lengths together at high dome frequencies. Default 9, which is fine enough to keep all distinct lengths separate at any practical frequency. Must be an integer.

\t-p, --polyhedron\tEither "octahedron" or "icosahedron". Default icosahedron.

\t-c, --class\tSubdivision class: 1 (Alternate), 2 (Triacon), or 3 (Skew/chiral). Class 2 requires an even --frequency, since each original edge is already implicitly split once by its construction. Class 3 requires -n/--n-frequency (a second frequency parameter distinct from --frequency); --frequency and --n-frequency play the roles of m and n in the (m,n) Goldberg-Coxeter construction, with triangle count T = m^2 + mn + n^2. (m,n) and (n,m) are mirror-image (chiral) domes of the same size -- swap --frequency and --n-frequency to get the other one. Default 1.

\t-n, --n-frequency\tSecond frequency parameter for -c 3 (Class III / Skew). Must be a positive integer different from --frequency. Ignored for classes 1 and 2.

\t-F, --face\tFlag specifying whether to generate face output in WRL file. Cancels DXF file output. Requires face data, which truncation on any axis (or combination of axes) now correctly preserves.

\t-P, --preview\tAlso save a quick 3D wireframe preview image ("<output>.png") alongside the usual output files, so you can sanity-check the dome without opening a CAD or VRML viewer.

\t-s, --stl\tAlso save an STL file ("<output>.stl") of the dome's surface triangles, e.g. for 3D-printing a scale model. Requires face data, which truncation on any axis correctly preserves.

\t-O, --obj\tAlso save an OBJ file ("<output>.obj") of the dome's surface triangles. Requires face data, which truncation on any axis correctly preserves.

\t-m, --material-cost\tPrice per unit length of strut material. If given, adds an estimated total material cost to the Bill of Materials, in addition to the total strut length (which is always reported). Must be a positive floating point number.

\t-H, --hub-templates\tAlso save one 2D DXF cutting template per unique hub connector shape ("<output>_hubtype1.dxf", "<output>_hubtype2.dxf", ...), for laser-cutting/CNC connector plates. Each template shows one radiating line per strut at its spoke angle, labeled with that strut's tangential (out-of-plane) deflection angle.

\t-T, --face-templates\tAlso save one 2D DXF cutting template per unique panel (face) shape ("<output>_facetype1.dxf", "<output>_facetype2.dxf", ...), for laser-cutting/CNC panel material. Each template shows the panel's 3 edges labeled with their lengths. Requires face data, which truncation on any axis correctly preserves.

\t-a, --area-cost\tPrice per unit area of panel material. If given, adds an estimated total panel material cost to the Bill of Materials, in addition to the total panel area (both reported whenever face data is available). Must be a positive floating point number.

\t-w, --panel-density\tAreal density (mass per unit area, e.g. kg per square meter) of panel material. If given, adds an estimated total panel weight to the Bill of Materials. Must be a positive floating point number.

\t-e, --elongation\tStretches the dome along all three axes by independent factors "fx,fy,fz", applied before truncation, turning the sphere into a general axis-aligned ellipsoid -- values > 1 stretch that axis, values < 1 squash it (e.g. "1.0,1.0,1.8" raises the ceiling height without touching the footprint; "1.3,1.0,1.0" widens the footprint along X only). All angle-based output (Bill of Materials angles, hub connector templates) correctly accounts for the resulting ellipsoid's true surface normal, not just the sphere approximation. All three factors must be positive floating point numbers. Default "1.0,1.0,1.0" (no elongation).
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
  truncation_x = None
  truncation_y = None
  truncation_z = None
  bom_rounding_precision = 9
  face_output = False
  preview_output = False
  stl_output = False
  obj_output = False
  cost_per_unit_length = None
  hub_templates_output = False
  face_templates_output = False
  cost_per_unit_area = None
  panel_areal_density = None
  elongation_factors = (1.0, 1.0, 1.0)
  output_path = None
  n_frequency = None

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
    opts, args = getopt.getopt(sys.argv[1:], 'r:f:v:t:b:p:c:m:e:n:a:w:x:y:FPsOHTho:', ['truncation=', 'truncation-x=', 'truncation-y=', 'vthreshold=', 'radius=', 'frequency=', 'help', 'bom-rounding=', 'polyhedron=', 'class=', 'material-cost=', 'elongation=', 'n-frequency=', 'area-cost=', 'panel-density=', 'face', 'preview', 'stl', 'obj', 'hub-templates', 'face-templates', 'output='])
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
        print('-c or --class argument must be an integer (1, 2, or 3). Exiting.')
        sys.exit(-1)
    if o in ('-n', '--n-frequency'):
      try:
        n_frequency = int(a)
      except ValueError:
        print('-n or --n-frequency argument must be an integer. Exiting.')
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
    if o in ('-a', '--area-cost'):
      try:
        cost_per_unit_area = float(a)
      except ValueError:
        print('-a or --area-cost argument must be a floating point number. Exiting.')
        sys.exit(-1)
      if cost_per_unit_area <= 0:
        print('-a or --area-cost argument must be greater than zero. Exiting.')
        sys.exit(-1)
    if o in ('-w', '--panel-density'):
      try:
        panel_areal_density = float(a)
      except ValueError:
        print('-w or --panel-density argument must be a floating point number. Exiting.')
        sys.exit(-1)
      if panel_areal_density <= 0:
        print('-w or --panel-density argument must be greater than zero. Exiting.')
        sys.exit(-1)
    if o in ('-e', '--elongation'):
      parts = a.split(',')
      if len(parts) != 3:
        print('-e or --elongation argument must be three comma-separated floating point '
              'numbers "fx,fy,fz". Exiting.')
        sys.exit(-1)
      try:
        elongation_factors = tuple(float(p) for p in parts)
      except ValueError:
        print('-e or --elongation argument must be three comma-separated floating point '
              'numbers "fx,fy,fz". Exiting.')
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
    if o in ('-T', '--face-templates'):
      face_templates_output = True
    if o in ('-r', '--radius'):
      try:
        a = float(a)
        radius = np.float64(a)
      except ValueError:
        print('-r or --radius argument must be a floating point number. Exiting.')
        sys.exit(-1)
    if o in ('-f', '--frequency'):
      try:
        frequency = int(a)
      except ValueError:
        print('-f or --frequency argument must be an integer. Exiting.')
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
        truncation_z = np.float64(float(a))
      except ValueError:
        print('-t or --truncation argument must be a floating point number. Exiting.')
        sys.exit(-1)
    if o in ('-x', '--truncation-x'):
      try:
        truncation_x = np.float64(float(a))
      except ValueError:
        print('-x or --truncation-x argument must be a floating point number. Exiting.')
        sys.exit(-1)
    if o in ('-y', '--truncation-y'):
      try:
        truncation_y = np.float64(float(a))
      except ValueError:
        print('-y or --truncation-y argument must be a floating point number. Exiting.')
        sys.exit(-1)

  #
  # check for required options
  #
  if output_path == None:
    print('An output path and filename is required. Use the -o argument. Exiting.')
    sys.exit(-1)

  #
  # build the geodesic sphere/dome (validation, symmetry-triangle
  # construction, projection, elongation, and truncation all happen
  # inside build_dome -- shared with pylair/mcp_server.py)
  #
  try:
    dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedral,
                       dome_class=dome_class, n_frequency=n_frequency,
                       vertex_equal_threshold=vertex_equal_threshold,
                       elongation_factors=elongation_factors,
                       truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z)
  except ValueError as e:
    print(str(e))
    sys.exit(-1)
  V, C, F_sphere = dome.V, dome.C, dome.F_sphere

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
  face_template_output_path = output_path if face_templates_output else None
  get_bill_of_materials(V, C, bom_rounding_precision, cost_per_unit_length, hub_template_output_path, elongation_factors,
                         faces=F_sphere, cost_per_unit_area=cost_per_unit_area,
                         panel_areal_density=panel_areal_density,
                         face_template_output_path=face_template_output_path)

#
# run the main function
#
if __name__ == "__main__":
  main()
