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
# MCP server exposing pyDome as tools for an agentic assistant to design a
# dome interactively: try frequency/class/truncation/elongation
# combinations, see a rendered preview inline, check the bill-of-materials
# cost/complexity tradeoffs -- all without shelling out to the `pydome`
# CLI and parsing stdout. Requires the optional `mcp` dependency
# (`pip install -e ".[mcp]"`); console script `pydome-mcp`.
#
from typing import List, Literal, Optional

from mcp.server.fastmcp import FastMCP, Image

from .api import build_dome
from .bill_of_materials import get_bill_of_materials as compute_bom
from .preview import render_preview_png_bytes, save_preview
from .output import OutputDXF, OutputWireframeVRML, OutputFaceVRML, OutputSTL, OutputOBJ

mcp = FastMCP("pydome")

Polyhedron = Literal["icosahedron", "octahedron"]
DomeClass = Literal[1, 2, 3]

# Shared geometry parameters across all four tools:
#   radius, frequency, polyhedron, dome_class, n_frequency,
#   truncation_x/truncation_y/truncation_z (None = that axis is not
#   truncated), elongation_x/elongation_y/elongation_z,
#   vertex_equal_threshold
# See pydome/api.py:validate_geometry_params for the domain rules (e.g.
# class 2 needs an even frequency); a bad combination raises ValueError,
# which FastMCP's dispatcher turns into an isError=True tool result.


@mcp.tool()
def design_dome(radius: float = 1.0, frequency: int = 4, polyhedron: Polyhedron = "icosahedron",
                 dome_class: DomeClass = 1, n_frequency: Optional[int] = None,
                 truncation_x: Optional[float] = None, truncation_y: Optional[float] = None,
                 truncation_z: Optional[float] = None, elongation_x: float = 1.0,
                 elongation_y: float = 1.0, elongation_z: float = 1.0,
                 vertex_equal_threshold: float = 1e-7) -> dict:
  """Compute a dome's geometry (no files written) and return summary stats
  -- vertex/edge/face counts, bounding box, height, footprint, total strut
  length -- so an agent can cheaply try configurations before exporting."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  return _design_summary(dome)


@mcp.tool()
def preview_dome(radius: float = 1.0, frequency: int = 4, polyhedron: Polyhedron = "icosahedron",
                  dome_class: DomeClass = 1, n_frequency: Optional[int] = None,
                  truncation_x: Optional[float] = None, truncation_y: Optional[float] = None,
                  truncation_z: Optional[float] = None, elongation_x: float = 1.0,
                  elongation_y: float = 1.0, elongation_z: float = 1.0,
                  vertex_equal_threshold: float = 1e-7) -> List:
  """Render a quick 3D wireframe preview of the dome and return it inline
  as an image, so the dome can be seen in-conversation before committing
  to any file export."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  png_bytes = render_preview_png_bytes(dome.V, dome.C)
  summary = "%d vertices, %d struts%s" % (
      len(dome.V), len(dome.C), " (truncated)" if dome.truncated else "")
  return [summary, Image(data=png_bytes, format="png")]


@mcp.tool()
def get_bill_of_materials(radius: float = 1.0, frequency: int = 4, polyhedron: Polyhedron = "icosahedron",
                           dome_class: DomeClass = 1, n_frequency: Optional[int] = None,
                           truncation_x: Optional[float] = None, truncation_y: Optional[float] = None,
                           truncation_z: Optional[float] = None, elongation_x: float = 1.0,
                           elongation_y: float = 1.0, elongation_z: float = 1.0,
                           vertex_equal_threshold: float = 1e-7,
                           bom_rounding_precision: int = 9,
                           cost_per_unit_length: Optional[float] = None,
                           cost_per_unit_area: Optional[float] = None,
                           panel_areal_density: Optional[float] = None) -> dict:
  """Compute the dome and return its Bill of Materials (strut lengths and
  counts, hub angles, total strut length/cost, and -- when the dome isn't
  truncated -- panel shapes and counts (with a chirality flag for mirror-
  image panels), total panel area/cost/weight, and bevel angles between
  adjacent panels) as structured data, without writing any files."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  return compute_bom(dome.V, dome.C, bom_rounding_precision, cost_per_unit_length,
                      hub_template_output_path=None, elongation_factors=dome.elongation_factors,
                      print_report=False, faces=dome.F_sphere, cost_per_unit_area=cost_per_unit_area,
                      panel_areal_density=panel_areal_density)


@mcp.tool()
def export_dome(output_path: str, radius: float = 1.0, frequency: int = 4,
                 polyhedron: Polyhedron = "icosahedron", dome_class: DomeClass = 1,
                 n_frequency: Optional[int] = None, truncation_x: Optional[float] = None,
                 truncation_y: Optional[float] = None, truncation_z: Optional[float] = None,
                 elongation_x: float = 1.0, elongation_y: float = 1.0, elongation_z: float = 1.0,
                 vertex_equal_threshold: float = 1e-7,
                 face_output: bool = False, preview: bool = False, stl: bool = False,
                 obj: bool = False, hub_templates: bool = False, face_templates: bool = False,
                 bom_rounding_precision: int = 9, cost_per_unit_length: Optional[float] = None,
                 cost_per_unit_area: Optional[float] = None,
                 panel_areal_density: Optional[float] = None) -> dict:
  """Compute the dome and write output files to disk (mirrors the `pydome`
  CLI): DXF+VRML by default, or face-only VRML with face_output=True
  (required for stl/obj/hub_templates/face_templates/cost_per_unit_area/
  panel_areal_density). Truncation on any combination of axes correctly
  preserves face data, so all of the above work regardless of
  truncation_x/truncation_y/truncation_z. face_templates=True writes one
  DXF cutting template per unique panel shape. Returns the list of files
  written and the Bill of Materials (including panel shapes/counts,
  chirality flags, panel area/cost/weight, and bevel angles)."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)

  files = []
  if face_output:
    OutputFaceVRML(dome.V, dome.F_sphere, output_path + '.wrl')
    files.append(output_path + '.wrl')
  else:
    OutputWireframeVRML(dome.V, dome.C, output_path + '.wrl')
    files.append(output_path + '.wrl')
    OutputDXF(dome.V, dome.C, output_path + '.dxf')
    files.append(output_path + '.dxf')

  if preview:
    save_preview(dome.V, dome.C, output_path + '.png')
    files.append(output_path + '.png')
  if stl:
    OutputSTL(dome.V, dome.F_sphere, output_path + '.stl')
    files.append(output_path + '.stl')
  if obj:
    OutputOBJ(dome.V, dome.F_sphere, output_path + '.obj')
    files.append(output_path + '.obj')

  hub_path = output_path if hub_templates else None
  face_template_path = output_path if face_templates else None
  report = compute_bom(dome.V, dome.C, bom_rounding_precision, cost_per_unit_length,
                        hub_template_output_path=hub_path, elongation_factors=dome.elongation_factors,
                        print_report=False, faces=dome.F_sphere, cost_per_unit_area=cost_per_unit_area,
                        panel_areal_density=panel_areal_density,
                        face_template_output_path=face_template_path)
  if hub_templates:
    files.extend(t['template_file'] for t in report['pyDome report'].get('Hub Connector Templates', []))
  if face_templates:
    files.extend(t['template_file'] for t in report['pyDome report'].get('Panel Cutting Templates', []))

  return {"files_written": files, "bill_of_materials": report}


def _design_summary(dome) -> dict:
  V = dome.V
  mins = [min(v[axis] for v in V) for axis in range(3)]
  maxs = [max(v[axis] for v in V) for axis in range(3)]
  total_strut_length = sum(
      sum((V[c[0]][axis] - V[c[1]][axis]) ** 2 for axis in range(3)) ** 0.5
      for c in dome.C
  )
  return {
      "vertex_count": len(dome.V),
      "edge_count": len(dome.C),
      "face_count": (len(dome.F_sphere) if dome.F_sphere is not None else None),
      "truncated": dome.truncated,
      "bounding_box": {"x": [mins[0], maxs[0]], "y": [mins[1], maxs[1]], "z": [mins[2], maxs[2]]},
      "height": maxs[2] - mins[2],
      "footprint_diameter": max(maxs[0] - mins[0], maxs[1] - mins[1]),
      "total_strut_length": total_strut_length,
      "resolved_parameters": {
          "radius": dome.radius,
          "frequency": dome.frequency,
          "polyhedron": dome.polyhedron,
          "dome_class": dome.dome_class,
          "n_frequency": dome.n_frequency,
          "elongation_factors": {"x": dome.elongation_factors[0], "y": dome.elongation_factors[1],
                                  "z": dome.elongation_factors[2]},
          "truncation": {"x": dome.truncation_x, "y": dome.truncation_y, "z": dome.truncation_z},
      },
  }


def main():
  mcp.run(transport="stdio")


if __name__ == "__main__":
  main()
