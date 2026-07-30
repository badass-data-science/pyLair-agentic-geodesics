---
name: pylair
description: Design and export geodesic domes (Class I/II/III) — vertices, chords, panels, DXF/VRML/STL/OBJ output, a full bill of materials, and a per-instance assembly manifest/pyFit job spec — via the pylair CLI.
metadata: { "openclaw": { "requires": { "bins": ["pylair"] }, "emoji": "🛖" } }
---

pyLair is a geodesic dome calculator. It computes the vertices, chords, and
panels of a geodesic dome (or full sphere) from a base polyhedron, a
subdivision class/frequency, and optional elongation/truncation, then
reports a bill of materials (strut lengths/counts, hub angles, panel
shapes/counts, costs) and can export DXF/VRML/STL/OBJ files plus cutting
templates. On top of that, it can build a per-instance assembly manifest
(every hub/strut/panel with its own stable label and its real adjacency to
its neighbors, not just a type-grouped count), a per-instance pyFit job spec
built from real cutting templates, and an annotated assembly schematic.

This skill runs the `pylair` console command directly (installed via
`pip install -e .` in the pyLair repo, or `pip install pylair` once
published). There is no MCP server involved here — OpenClaw drives the CLI
as a shell tool, the same binary documented in `README.md`.

## When to use this

Reach for `pylair` whenever the user wants to explore, size, or export a
geodesic dome/sphere design — e.g. "how many struts does a frequency-6
dome need", "give me a DXF for a dome I can 3D print", "what's the bill of
materials for a 4-meter dome truncated at the equator", "which hubs does
this specific strut connect to", or "build me a pyFit nesting job from this
dome's panels".

## Basic invocation

```
pylair -o <output-path> -f <frequency> -r <radius> [options]
```

This always prints a JSON Bill of Materials to stdout and writes
`<output-path>.dxf` and `<output-path>.wrl`. Read the JSON report back to
the user rather than just confirming the command succeeded — the report
(strut lengths/counts, hub angles, total strut length, and, if face data
was requested, panel shapes/counts and bevel angles) is the actual answer
to most dome-design questions.

## Useful flags

| Flag | Meaning |
|---|---|
| `-o` | Output path (required). `.dxf`/`.wrl` appended automatically. |
| `-f` | Frequency (positive integer). Higher = more struts, rounder dome. |
| `-r` | Radius. Must be > 0. |
| `-p` | Base polyhedron: `icosahedron` (default), `octahedron`, or `tetrahedron`. |
| `-c` | Subdivision class: `1` (Alternate, default), `2` (Triacon, needs even `-f`), `3` (Skew/chiral, needs `-n`). |
| `-n` | Second Goldberg-Coxeter frequency, required for `-c 3`. |
| `-t`/`-x`/`-y` | Truncation cutoff (0-1) along Z/X/Y. Prefer `0.499999` or `0.333333` over round numbers — see caveat below. |
| `-e` | Elongation `"fx,fy,fz"` — stretch/squash each axis independently before truncation. |
| `-F` | Emit face data (needed for `-s`/`-O`/`-T`/`-a`/`-w`). |
| `-s`/`-O` | Also write STL/OBJ. |
| `-P` | Also save a wireframe preview PNG. |
| `-m`/`-a`/`-w` | Material cost per unit length / area / panel areal density, for cost and weight estimates. |
| `--assembly-manifest` | Also save a per-instance assembly manifest (`<output>_manifest.json`) — see below. |
| `--pyfit-job-spec=panels\|hubs` | Also write real cutting templates and a per-instance pyFit job spec (`<output>_jobspec.json`) built from them. |
| `--assembly-schematic` | Also save an annotated wireframe (`<output>_schematic.png`) with each hub's label drawn at its position. |
| `-h` | Full flag reference. |

For the complete flag table, output formats, and geometry caveats (e.g. why
an exact `0.5` truncation cutoff can fail loudly, or why a coarse
`-b/--bom-rounding` can merge distinct strut lengths), see this repo's
`README.md`, which this skill's behavior always matches — the CLI has one
validation/geometry engine (`pylair/api.py`) shared by every interface.

## Assembly manifest and pyFit job specs

The bill of materials answers "how many of each strut/hub/panel shape do I
need to cut" — it groups instances into cutting-template types and counts.
`--assembly-manifest` answers a different question: "which specific physical
piece goes where, and what does it connect to." Every hub, strut, and panel
gets its own stable label (`H#`/`S#`/`P#`) and its real adjacency to its
neighbors — reach for it when the user asks about a *specific* piece
("what connects to hub 12"), not just totals.

`--pyfit-job-spec=panels` (or `=hubs`) writes real cutting templates and a
pyFit job spec with one part entry per physical instance (`quantity` always
1), so a pyFit nest report can be traced back to a specific dome hub/panel —
use this instead of hand-building a job spec from the bill of materials'
own template list when the user wants that traceability. See README.md's
"Assembly manifest, pyFit job specs, and schematics" section for the full
JSON shapes and how chiral panel groups are handled.

## Iterating on a design

There's no cheap "just compute the numbers" mode from the CLI the way the
MCP server's `design_dome`/`preview_dome` tools provide — every `pylair`
invocation writes DXF/VRML files. When iterating on a design, use a
scratch `-o` path and re-run with adjusted flags rather than treating the
first invocation as final; only settle on a real output path once the
reported bill of materials looks right.
