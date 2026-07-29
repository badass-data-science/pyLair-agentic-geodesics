# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project has not yet made a tagged/versioned release — everything below
lives under `[Unreleased]` against the `0.1.0` version in `pyproject.toml`.

## [Unreleased]

### Added

- OpenClaw skill (`SKILL.md` + `openclaw.config.snippet.jsonc`) so an
  [OpenClaw](https://openclaw.ai/) agent can drive the `pylair` CLI directly,
  since OpenClaw has no MCP client of its own.
- GitHub Actions CI pipeline (`cli-smoke` job plus a Python 3.9-3.13 test
  matrix).
- `AGENTS.md`, an agent-facing guide to the repo layout, test conventions,
  and geometry-pipeline caveats.
- `graphify-out/` knowledge-graph outputs (`GRAPH_REPORT.md`, `graph.json`,
  `graph.html`) generated via `/graphify`.
- CLI/Python/license badges on the README.
- A book outline proposal, "Agentic Geodesic Lair Design for Supervillains"
  (`book/outline.md`), plus an environment-design practicum chapter.
- MCP server interface (`pylair-mcp`): `design_dome`, `preview_dome`,
  `get_bill_of_materials`, and `export_dome` tools, all built on the same
  `pylair/api.py` engine as the CLI.
- Face-level bill of materials and panel cutting templates.
- `trimesh`/`ezdxf`-based oracle tests (the `verify` extra) that cross-check
  geometry independent of pyLair's own math.
- Class III (Skew/chiral) subdivision via `-c 3`/`-n`.
- Class II (Triacon) subdivision via `-c`/`--class`.
- `-P`/`--preview`: a quick 3D wireframe preview image.
- `-s`/`--stl` and `-O`/`--obj` mesh export.
- `-e`/`--elongation` for independent per-axis stretch/squash.
- `-H`/`--hub-templates`: DXF cutting templates per unique hub shape.
- Total strut length/cost rollup in the bill of materials.
- Full `pytest` test suite.
- A blog post series (`blog-posts/introducing-pylair.md`) walking through the
  project and each major feature as it shipped.

### Changed

- Renamed the project from pyDome to pyLair.
- Relicensed from GPL-3.0-or-later to MIT.
- Restructured the codebase into a proper `pydome/`-then-`pylair/` package.
- Split the original README into `README.md` (usage/caveats) and
  `METHOD.md` (the geometric method itself).
- Moved `METHOD.md` into `blog-posts/METHOD.md` alongside the blog post, and
  fixed the image links inside it that broke from the move.
- Generalized elongation and truncation from the Z axis to all three axes,
  including face-aware truncation on X/Y/Z.
- Made vertex/chord/face indexing consistently 0-indexed throughout.
- Replaced an O(n^2) duplicate-vertex scan with a KD-tree.
- Replaced deprecated `np.matrix` usage with plain `ndarray`.
- Reworked chord-length clustering for the BOM instead of naive per-value
  rounding, and restored `--bom-rounding` as a tunable merge granularity.
- Pinned `mcp<2.0` after `mcp` 2.0.0 removed `mcp.server.fastmcp`, which
  broke CI.

### Fixed

- Fail loudly on a degenerate horizontal chord at the truncation cutoff
  instead of producing silently wrong geometry.
- Validate frequency/radius CLI arguments and narrow bare `except` clauses.
- Strut the diagonal seam left over from corner-clipped quad panels.
- Stale MCP tool docstrings for panel data and truncation-artifact flags.
- Two stale README claims about panel data and the flat-chord error.
- Stale `METHOD.md` links in `AGENTS.md` and `README.md` still pointing at
  the pre-move root path instead of `blog-posts/METHOD.md`.
- Ported the original Python 2-era code to Python 3 and fixed a broken `-h`
  flag.

[Unreleased]: https://github.com/badass-data-science/pyLair-agentic-geodesics
