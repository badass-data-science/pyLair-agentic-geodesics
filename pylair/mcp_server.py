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
# MCP server exposing pyLair as tools for an agentic assistant to design a
# dome interactively: try frequency/class/truncation/elongation
# combinations, see a rendered preview inline, check the bill-of-materials
# cost/complexity tradeoffs -- all without shelling out to the `pylair`
# CLI and parsing stdout. Requires the optional `mcp` dependency
# (`pip install -e ".[mcp]"`); console script `pylair-mcp`.
#
from typing import List, Literal, Optional

from mcp.server.fastmcp import FastMCP, Image

from .api import build_dome
from .bill_of_materials import get_bill_of_materials as compute_bom
from .preview import render_preview_png_bytes, save_preview, render_assembly_schematic_png_bytes
from .output import OutputDXF, OutputWireframeVRML, OutputFaceVRML, OutputSTL, OutputOBJ
from .assembly import (
    build_assembly_manifest,
    build_pyfit_job_spec_for_panels,
    build_pyfit_job_spec_for_hubs,
    bom_template_paths,
)

mcp = FastMCP("pylair")

Polyhedron = Literal["icosahedron", "octahedron"]
DomeClass = Literal[1, 2, 3]

# Shared geometry parameters across all four tools:
#   radius, frequency, polyhedron, dome_class, n_frequency,
#   truncation_x/truncation_y/truncation_z (None = that axis is not
#   truncated), elongation_x/elongation_y/elongation_z,
#   vertex_equal_threshold
# See pylair/api.py:validate_geometry_params for the domain rules (e.g.
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
  counts, hub angles, total strut length/cost, panel shapes and counts
  -- with a chirality flag for mirror-image panels -- total panel
  area/cost/weight, and bevel angles between adjacent panels) as
  structured data, without writing any files. Panel data is included
  regardless of truncation, since truncate() clips faces correctly on
  any combination of axes. Both the chord and panel sections also
  include a "Possible truncation-artifact ..." list flagging entries
  whose length/edges are under 0.1% of the dome's largest strut --
  slivers from a truncation cutoff landing extremely close to (but not
  on) an existing vertex ring, not genuine strut/panel classes."""
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
  """Compute the dome and write output files to disk (mirrors the `pylair`
  CLI): DXF+VRML by default, or face-only VRML with face_output=True
  (required for stl/obj/hub_templates/face_templates/cost_per_unit_area/
  panel_areal_density). Truncation on any combination of axes correctly
  preserves face data, so all of the above work regardless of
  truncation_x/truncation_y/truncation_z. face_templates=True writes one
  DXF cutting template per unique panel shape. Returns the list of files
  written and the Bill of Materials (including panel shapes/counts,
  chirality flags, panel area/cost/weight, bevel angles, and "Possible
  truncation-artifact chords/panels" lists flagging any struts/panels
  under 0.1% of the dome's largest strut -- likely slivers from a
  truncation cutoff landing extremely close to an existing vertex
  ring, not genuine strut/panel classes)."""
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
    files.extend(t['template_file'] for t in report['pyLair report'].get('Hub Connector Templates', []))
  if face_templates:
    files.extend(t['template_file'] for t in report['pyLair report'].get('Panel Cutting Templates', []))

  return {"files_written": files, "bill_of_materials": report}


@mcp.tool()
def get_assembly_manifest(radius: float = 1.0, frequency: int = 4, polyhedron: Polyhedron = "icosahedron",
                           dome_class: DomeClass = 1, n_frequency: Optional[int] = None,
                           truncation_x: Optional[float] = None, truncation_y: Optional[float] = None,
                           truncation_z: Optional[float] = None, elongation_x: float = 1.0,
                           elongation_y: float = 1.0, elongation_z: float = 1.0,
                           vertex_equal_threshold: float = 1e-7,
                           rounding_precision: int = 9, angle_precision: int = 3,
                           length_precision: int = 3) -> dict:
  """Compute the dome and return a per-instance assembly manifest, without
  writing any files -- every hub, strut, and panel gets its own stable
  label (H#/S#/P#, e.g. "H12"/"S77"/"P42") plus its real adjacency to its
  neighbors: which struts meet at a hub and at what tangential/spoke
  angle, which two hubs a strut connects and which panel(s) border it,
  which three hubs bound a panel and the bevel angle at each of its
  edges. This is a different cut of the same geometry
  get_bill_of_materials reports: that tool groups instances into
  cutting-template types and counts (how many to cut); this one keeps
  every individual instance addressable (which specific one goes where),
  which is what an assembly schematic or a per-instance pyFit nesting
  job (see export_assembly_job_spec) needs. Every value is a native
  JSON-safe type (plain float/int/str/bool/None), so the result is
  always a clean JSON document once serialized."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  return build_assembly_manifest(dome.V, dome.C, faces=dome.F_sphere,
                                  elongation_factors=dome.elongation_factors,
                                  rounding_precision=rounding_precision,
                                  angle_precision=angle_precision,
                                  length_precision=length_precision)


@mcp.tool()
def export_assembly_job_spec(output_path: str, kind: Literal["panels", "hubs"] = "panels",
                              sheet_width: float = 48.0, sheet_height: float = 96.0,
                              radius: float = 1.0, frequency: int = 4,
                              polyhedron: Polyhedron = "icosahedron", dome_class: DomeClass = 1,
                              n_frequency: Optional[int] = None, truncation_x: Optional[float] = None,
                              truncation_y: Optional[float] = None, truncation_z: Optional[float] = None,
                              elongation_x: float = 1.0, elongation_y: float = 1.0,
                              elongation_z: float = 1.0, vertex_equal_threshold: float = 1e-7,
                              rounding_precision: int = 9, angle_precision: int = 3,
                              length_precision: int = 3) -> dict:
  """Write real cutting-template DXFs (one per distinct hub or panel
  shape -- the same files export_dome's hub_templates/face_templates=True
  write) and build a pyFit job spec from them with one part entry PER
  PHYSICAL INSTANCE, quantity always 1, named by its own assembly-manifest
  label (H#/P#) -- instead of one entry per shape with a quantity=N --
  so pyFit's own nest report (part_name on every placement) becomes
  addressable back to a specific dome hub/panel, not just "some copy of
  shape type X". A chiral panel group's "other" mirror-orientation
  instances get an inline pre-mirrored polygon rather than trusting
  pyFit's own packer to flip the correct ones (see
  pylair/assembly.py's build_pyfit_job_spec_for_panels docstring for
  why letting the packer decide would risk cutting the wrong-handed
  piece). kind="hubs" does the equivalent for hub connector plates
  instead of panels (no chirality model for those -- pyLair doesn't
  compute one). Returns {"files_written": [...template dxf paths...],
  "job_spec": {...}}; write job_spec to disk yourself (e.g. json.dump)
  to hand it to pyFit's own design_nest/run_nest/export_nest."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  manifest = build_assembly_manifest(dome.V, dome.C, faces=dome.F_sphere,
                                      elongation_factors=dome.elongation_factors,
                                      rounding_precision=rounding_precision,
                                      angle_precision=angle_precision,
                                      length_precision=length_precision)

  if kind == "hubs":
    report = compute_bom(dome.V, dome.C, rounding_precision,
                          hub_template_output_path=output_path,
                          elongation_factors=dome.elongation_factors,
                          print_report=False, faces=dome.F_sphere)
    template_rows = report['pyLair report'].get('Hub Connector Templates', [])
    template_paths = bom_template_paths(template_rows, manifest['hub_groups'], 'hub_ids')
    job_spec = build_pyfit_job_spec_for_hubs(manifest, sheet_width, sheet_height, template_paths)
  else:
    report = compute_bom(dome.V, dome.C, rounding_precision,
                          elongation_factors=dome.elongation_factors,
                          print_report=False, faces=dome.F_sphere,
                          face_template_output_path=output_path)
    template_rows = report['pyLair report'].get('Panel Cutting Templates', [])
    template_paths = bom_template_paths(template_rows, manifest['panel_groups'], 'panel_ids')
    job_spec = build_pyfit_job_spec_for_panels(manifest, sheet_width, sheet_height, template_paths)

  files_written = [row['template_file'] for row in template_rows]
  return {"files_written": files_written, "job_spec": job_spec}


@mcp.tool()
def render_assembly_schematic(radius: float = 1.0, frequency: int = 4,
                               polyhedron: Polyhedron = "icosahedron", dome_class: DomeClass = 1,
                               n_frequency: Optional[int] = None, truncation_x: Optional[float] = None,
                               truncation_y: Optional[float] = None, truncation_z: Optional[float] = None,
                               elongation_x: float = 1.0, elongation_y: float = 1.0,
                               elongation_z: float = 1.0, vertex_equal_threshold: float = 1e-7,
                               show_hub_labels: bool = True, show_strut_labels: bool = False,
                               show_panel_labels: bool = False) -> List:
  """Render the dome's depth-cued wireframe (same rendering preview_dome
  uses) with each hub/strut/panel's own assembly-manifest label (H#/S#/P#)
  optionally drawn at its hub position / strut midpoint / panel centroid,
  and return it inline as an image -- an annotated assembly schematic
  rather than just a shape preview. Labels default to hubs on, since
  that's usually the single most useful view for wiring up connector
  plates; struts and panels default off, since a real dome has far more
  of either and turning all three on past a low frequency produces an
  unreadable smear of text rather than a usable diagram -- turn on only
  the label kind relevant to whatever's being documented."""
  dome = build_dome(radius=radius, frequency=frequency, polyhedron=polyhedron,
                     dome_class=dome_class, n_frequency=n_frequency,
                     truncation_x=truncation_x, truncation_y=truncation_y, truncation_z=truncation_z,
                     elongation_factors=(elongation_x, elongation_y, elongation_z),
                     vertex_equal_threshold=vertex_equal_threshold)
  manifest = build_assembly_manifest(dome.V, dome.C, faces=dome.F_sphere,
                                      elongation_factors=dome.elongation_factors)
  png_bytes = render_assembly_schematic_png_bytes(
      dome.V, dome.C, manifest, show_hub_labels=show_hub_labels,
      show_strut_labels=show_strut_labels, show_panel_labels=show_panel_labels)
  summary = "%d hubs, %d struts, %d panels%s" % (
      len(manifest['hubs']), len(manifest['struts']), len(manifest['panels']),
      " (truncated)" if dome.truncated else "")
  return [summary, Image(data=png_bytes, format="png")]


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
