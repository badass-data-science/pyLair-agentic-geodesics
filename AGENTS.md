# AGENTS.md

Agent-facing guide to working in this repo. For user-facing docs (CLI flags, MCP
tools, caveats) see [README.md](README.md); for the geometric method itself see
[METHOD.md](blog-posts/METHOD.md).

## What this is

pyLair is a geodesic dome calculator: given a base polyhedron, subdivision
class/frequency, and optional truncation/elongation, it computes vertices/chords/
faces and exports DXF/VRML/STL/OBJ plus a JSON Bill of Materials. There's a CLI
(`pylair`) and an MCP server (`pylair-mcp`) that both go through the same
`pylair/api.py:build_dome` / `validate_geometry_params`. There's also an
[OpenClaw](https://openclaw.ai/) skill (`SKILL.md` + `openclaw.config.snippet.jsonc`
at the repo root) that drives the `pylair` CLI directly — OpenClaw has no MCP
client, so that skill wraps the CLI rather than `pylair-mcp`.

## Setup

```
pip install -e ".[test]"
```

Optional extras: `mcp` (MCP server deps; no published release supports Python
3.9; pinned to `<2.0` because 2.0.0 removed `mcp.server.fastmcp` entirely —
`pylair/mcp_server.py`'s `FastMCP`/`Image` imports and
`tests/test_mcp_server.py`'s `mcp.shared.memory.create_connected_server_and_client_session`
both 404 on 2.0.0's new module layout; migrating to whatever replaces
`FastMCP` there is real, unstarted work, not a version bump), `verify`
(`trimesh`/`shapely`/`ezdxf`, used only by the oracle test below —
`shapely` is a transitive dependency `trimesh.intersections.slice_mesh_plane`
needs but doesn't pull in on its own).

## Test

```
pytest
```

- One test module per `pylair/*.py` source module, plus `tests/test_cli.py`
  (subprocess-level CLI integration tests via `python -m pylair`).
- `tests/test_geometry_oracle.py` cross-checks geometry against `trimesh`/`ezdxf`
  and is auto-skipped unless the `verify` extra is installed — don't treat a skip
  here as a failure.
- Golden-value vertex/edge/face-count formulas exist per subdivision class (see
  README's "Development" section) — if you touch the geometry pipeline
  (`polyhedral.py`, `symmetry_triangle.py`, `class_three.py`, `geodesic_sphere.py`,
  `truncation.py`, `elongation.py`), a correctness regression should show up as a
  failing count, not just an exception. Add/extend golden-value or oracle coverage
  alongside any change there rather than relying on spot-checks.

No linter/formatter is configured — match the surrounding style in whichever file
you're editing.

## Layout

| File | Responsibility |
|---|---|
| `pylair/cli.py` | CLI entry point, arg parsing, orchestration via `api.py`. |
| `pylair/api.py` | Shared programmatic entry point (`build_dome`, validators) used by both CLI and MCP server. |
| `pylair/mcp_server.py` | MCP server: `design_dome`/`preview_dome`/`get_bill_of_materials`/`export_dome`, all built on `api.py`. |
| `pylair/polyhedral.py` | Base polyhedra, `Vertex`/`Chord`/`Face` primitives, `build_lcd_faces`, `compute_face_adjacency`. |
| `pylair/symmetry_triangle.py` | Class I/II single-face subdivision. |
| `pylair/class_three.py` | Class III (chiral) single-face subdivision + cross-face stitching data. |
| `pylair/geodesic_sphere.py` | Replicates the symmetry triangle across all faces, dedupes shared vertices, projects onto the sphere. |
| `pylair/truncation.py` | Cuts the sphere into a dome along X/Y/Z, clipping face data to match. |
| `pylair/elongation.py` | Scales axes independently into a general ellipsoid. |
| `pylair/output.py` | DXF/VRML/STL/OBJ/template file writers. |
| `pylair/preview.py` | Wireframe preview PNG rendering. |
| `pylair/bill_of_materials.py` | Strut/hub/panel clustering, angles, cost/weight, cutting templates, JSON report. |

Internally, vertices/chords/faces are referenced by 0-indexed integer position into
Python lists throughout — don't reintroduce 1-indexing.

## Working in the geometry pipeline

This is the part of the codebase where a plausible-looking change can silently
produce wrong-but-valid-shaped output (right vertex/edge/face *counts*, wrong
positions or angles). Before changing `polyhedral.py` / `symmetry_triangle.py` /
`class_three.py` / `geodesic_sphere.py` / `truncation.py` / `elongation.py` /
`bill_of_materials.py`, read the relevant caveat in README.md's "Caveats and known
limitations" and the corresponding "Development" paragraph — several of these
(Class II's coordinate-basis bug, Class III's cross-face stitching, elongated
surface-normal angles) were real historical bugs that passed a naive smoke test.

Known live ambiguity: `truncate()`'s diagonal-seam handling for quad boundary
panels is the current, correct behavior (see README caveat) —
`blog-posts/introducing-pylair.md` and `blog-posts/METHOD.md` should agree with
README, not the other way around, if you find a discrepancy while editing docs.

## Docs stay in sync

`README.md`, `blog-posts/METHOD.md`, `SKILL.md`, and `blog-posts/introducing-pylair.md` all
describe overlapping behavior. If you change behavior that any of them documents,
check the others — this has drifted before (a blog "Next Steps" item lingered after
the feature shipped and the README was updated). `SKILL.md` in particular mirrors
the CLI flag table in README.md's "Command-line options" section — if you add or
change a flag, update both.

Also add an entry to `CHANGELOG.md` under `[Unreleased]` (Added/Changed/Fixed,
per [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)) whenever you ship
a user-visible change — a new flag, a behavior change, a bug fix. There have been
no tagged releases yet, so everything accumulates under `[Unreleased]` against
the `0.1.0` version in `pyproject.toml`; don't invent a version bump.

## graphify-out/

Generated knowledge-graph artifacts from `/graphify` (see `.claude/skills` if
present). `GRAPH_REPORT.md`, `graph.json`, and `graph.html` are committed and
browsable/queryable without rerunning extraction; `cache/`, `manifest.json`, and
`cost.json` are local tool state and gitignored. Regenerate with `/graphify --update`
after a meaningful change if you want the graph to stay current — it isn't
auto-maintained.

If an agent session isolates work into a git worktree before editing, do not run
`/graphify --update` there: a fresh worktree branches from `origin/<default-branch>`
(missing any commits that only exist on the current branch) and lacks gitignored
local state (`cache/`, `manifest.json`, `.claude/settings.local.json`), so
incremental detection reports false deletions and misses recently added files.
Run `/graphify --update` directly in the working checkout instead.
