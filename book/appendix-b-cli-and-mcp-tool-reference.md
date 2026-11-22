# Appendix B: CLI and MCP Tool Reference

Every CLI option and MCP tool in both toolkits, with a one-line description and the chapters that cover it: a quick lookup for when you're designing and nesting your own domes. The CLI options mirror each project's README, which remains the complete reference.

## pyLair CLI (`pylair`)

| Flag | Long form | Description | Chapter(s) |
|---|---|---|---|
| `-o` | `--output` | Output file path; required. | 2 |
| `-r` | `--radius` | Dome radius; must be > 0. | 3 |
| `-f` | `--frequency` | Subdivision frequency; positive integer. | 4 |
| `-p` | `--polyhedron` | Base polyhedron: icosahedron, octahedron, or tetrahedron. | 3 |
| `-c` | `--class` | Subdivision class: `1`, `2`, or `3`. | 4, 5, 6 |
| `-n` | `--n-frequency` | Second frequency for `-c 3`'s `(m,n)` pair. | 6 |
| `-t` | `--truncation` | Z-axis truncation cutoff fraction. | 9 |
| `-x` | `--truncation-x` | X-axis truncation cutoff fraction. | 9, 10, 17 |
| `-y` | `--truncation-y` | Y-axis truncation cutoff fraction. | 9 |
| `-v` | `--vthreshold` | Vertex-deduplication distance threshold. | 4, 7 |
| `-b` | `--bom-rounding` | BOM display precision and merge tolerance. | 13 |
| `-m` | `--material-cost` | Price per unit strut length. | — |
| `-e` | `--elongation` | Per-axis elongation factors `"fx,fy,fz"`. | 8 |
| `-F` | `--face` | Write a VRML of the faces instead of the wireframe, and no DXF. | 17 |
| `-P` | `--preview` | Save a wireframe preview PNG. | 17 |
| `-s` | `--stl` | Save an STL surface mesh. | 17 |
| `-O` | `--obj` | Save an OBJ surface mesh. | 17 |
| `-H` | `--hub-templates` | Save one DXF per distinct hub connector shape. | 15 |
| `-T` | `--face-templates` | Save one DXF per distinct panel shape. | 15, 20 |
| `-a` | `--area-cost` | Price per unit panel area. | 11, 23 |
| `-w` | `--panel-density` | Areal density for panel weight estimates. | 11 |
| — | `--assembly-manifest` | Save a per-instance assembly manifest (every hub/strut/panel with its own stable label and real adjacency). | 22 |
| — | `--pyfit-job-spec=panels\|hubs` | Write real cutting templates and a per-instance pyFit job spec built from them. | 22 |
| — | `--sheet-width`, `--sheet-height` | Sheet dimensions used in the `--pyfit-job-spec` output; default `48`/`96`. | 22 |
| — | `--assembly-schematic` | Save an annotated wireframe with each hub's label drawn at its position. | 22 |
| — | `--schematic-strut-labels`, `--schematic-panel-labels` | Also label struts/panels on the `--assembly-schematic` image. | 22 |
| `-h` | `--help` | Show usage and exit. | — |

## pyLair MCP Tools (`pylair-mcp`)

| Tool | Purpose | Writes files? | Chapter(s) |
|---|---|---|---|
| `design_dome` | Cheap summary (counts, footprint, height, strut length) for comparing configurations. | No | 2–11, 18, 23 |
| `preview_dome` | Inline wireframe render. | No | 2–6, 8, 9, 18 |
| `get_bill_of_materials` | Full bill of materials as structured data (struts, hub angles, panels, chirality flags, artifact warnings). | No | 8, 10–16, 18, 23 |
| `export_dome` | Writes DXF, VRML, STL, OBJ, and template files; the only file-writing tool of the design loop's four. | Yes | 15, 17, 18, 20 |
| `get_assembly_manifest` | Per-instance assembly manifest, no files — every hub/strut/panel with its own stable label and real adjacency, unlike the BOM's type-grouped counts. | No | 22 |
| `export_assembly_job_spec` | Writes cutting templates and returns a per-instance pyFit job spec built from them (`kind="panels"` or `"hubs"`). | Yes | 22 |
| `render_assembly_schematic` | Inline depth-cued wireframe with optional per-hub/strut/panel labels drawn at their positions. | No | 22 |

## pyFit CLI (`pyfit`)

| Flag | Long form | Description | Chapter(s) |
|---|---|---|---|
| `-j` | `--job` | Path to the job spec JSON file; required. | 19, 20 |
| `-o` | `--output` | Output path prefix; required. | 19, 20 |
| `-R` | `--rotation-step` | Degrees between candidate rotation angles; default `15`. | 20, 21 |
| `-P` | `--preview` | Save a 2D preview PNG per sheet. | 19, 20 |
| `-q` | `--quiet` | Suppress the progress heartbeat printed to standard error. | — |

## pyFit MCP Tools (`pyfit-mcp`)

| Tool | Purpose | Writes files? | Chapter(s) |
|---|---|---|---|
| `design_nest` | Cheap summary (sheets used, per-sheet utilization). | No | 2, 20, 21, 23 |
| `preview_nest` | Inline per-sheet layout render. | No | 2, 19, 20, 21 |
| `get_nest_report` | Full placement report as structured data (sheet index, position, rotation, mirror flag per part instance). | No | 19, 21 |
| `export_nest` | Writes one DXF (and optionally PNG) per sheet actually used; the only file-writing tool of the four. | Yes | 21 |

## Job Spec Fields (pyFit)

| Field | Description | Chapter(s) |
|---|---|---|
| `sheet.width`, `sheet.height` | Sheet stock dimensions. | 19, 20 |
| `parts[].name` | Part identifier. | 19, 20 |
| `parts[].dxf` | Path to a DXF file containing exactly one closed loop. | 20 |
| `parts[].polygon` | An inline list of `[x, y]` points, as an alternative to `dxf`. | 2, 22 |
| `parts[].quantity` | How many copies of this shape to nest. | 20, 22 |
| `parts[].allow_mirror` | Whether the packer may flip this shape's template; default `true`. | 20, 22 |
