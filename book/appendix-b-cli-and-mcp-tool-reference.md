# Appendix B: CLI and MCP Tool Reference

Every CLI flag and MCP tool this book actually used, for both toolkits, with a one-line description and the chapter(s) that cover it — a fast lookup once you're designing and nesting your own domes instead of this book's own examples.

## pyLair CLI (`pylair`)

| Flag | Long form | Description | Chapter(s) |
|---|---|---|---|
| `-o` | `--output` | Output file path; required. | 2 |
| `-r` | `--radius` | Dome radius; must be > 0. | 3 |
| `-f` | `--frequency` | Subdivision frequency; positive integer. | 4 |
| `-p` | `--polyhedron` | Base polyhedron: `icosahedron` or `octahedron`. | 3 |
| `-c` | `--class` | Subdivision class: `1`, `2`, or `3`. | 4, 5, 6 |
| `-n` | `--n-frequency` | Second frequency for `-c 3`'s `(m,n)` pair. | 6 |
| `-t` | `--truncation` | Z-axis truncation cutoff fraction. | 9 |
| `-x` | `--truncation-x` | X-axis truncation cutoff fraction. | 9, 10 |
| `-y` | `--truncation-y` | Y-axis truncation cutoff fraction. | 9 |
| `-v` | `--vthreshold` | Vertex-deduplication distance threshold. | 4, 7 |
| `-b` | `--bom-rounding` | BOM display precision and merge tolerance. | 13 |
| `-m` | `--material-cost` | Price per unit strut length. | 11 |
| `-e` | `--elongation` | Per-axis elongation factors `"fx,fy,fz"`. | 8 |
| `-F` | `--face` | Emit face data (face-inclusive VRML, no DXF). | 10, 17 |
| `-P` | `--preview` | Save a wireframe preview PNG. | throughout |
| `-s` | `--stl` | Save an STL surface mesh. | 17 |
| `-O` | `--obj` | Save an OBJ surface mesh. | 17 |
| `-H` | `--hub-templates` | Save one DXF per distinct hub connector shape. | 15 |
| `-T` | `--face-templates` | Save one DXF per distinct panel shape. | 15, 20 |
| `-a` | `--area-cost` | Price per unit panel area. | 11, 22 |
| `-w` | `--panel-density` | Areal density for panel weight estimates. | 11 |
| `-h` | `--help` | Show usage and exit. | — |

## pyLair MCP Tools (`pylair-mcp`)

| Tool | Purpose | Writes files? | Chapter(s) |
|---|---|---|---|
| `design_dome` | Cheap summary (counts, footprint, height, strut length) for comparing configurations. | No | 2, 18, 22 |
| `preview_dome` | Inline wireframe render. | No | 18 |
| `get_bill_of_materials` | Full BOM as structured data (struts, hub angles, panels, chirality flags, artifact warnings). | No | 18, 22 |
| `export_dome` | Writes DXF/VRML/STL/OBJ/templates to disk; the only file-writing tool of the four. | Yes | 17, 18, 21 |

## pyFit CLI (`pyfit`)

| Flag | Long form | Description | Chapter(s) |
|---|---|---|---|
| `-j` | `--job` | Path to the job spec JSON file; required. | 19, 20 |
| `-o` | `--output` | Output path prefix; required. | 19, 20 |
| `-R` | `--rotation-step` | Degrees between candidate rotation angles; default `15`. | 19, 20 |
| `-P` | `--preview` | Save a 2D preview PNG per sheet. | 19, 20 |
| `-q` | `--quiet` | Suppress the stderr progress heartbeat. | 20, 21 |

## pyFit MCP Tools (`pyfit-mcp`)

| Tool | Purpose | Writes files? | Chapter(s) |
|---|---|---|---|
| `design_nest` | Cheap summary (sheets used, per-sheet utilization). | No | 21, 22 |
| `preview_nest` | Inline per-sheet layout render. | No | 21 |
| `get_nest_report` | Full placement report as structured data (sheet index, position, rotation, mirror flag per part instance). | No | 21 |
| `export_nest` | Writes one DXF (and optionally PNG) per sheet actually used; the only file-writing tool of the four. | Yes | 21 |

## Job Spec Fields (pyFit)

| Field | Description | Chapter(s) |
|---|---|---|
| `sheet.width`, `sheet.height` | Sheet stock dimensions. | 19, 20 |
| `parts[].name` | Part identifier. | 19, 20 |
| `parts[].dxf` | Path to a DXF file containing exactly one closed loop. | 20 |
| `parts[].polygon` | An inline list of `[x, y]` points, as an alternative to `dxf`. | 19 |
| `parts[].quantity` | How many copies of this shape to nest. | 20 |
| `parts[].allow_mirror` | Whether the packer may flip this shape's template; default `true`. | 14, 20 |
