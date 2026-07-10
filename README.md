pyDome
======

A geodesic dome calculator written in Python.

pyDome calculates vertices and chords of Class One geodesic domes of arbitrary size. Domes created by pyDome can be truncated to facilitate structure design. The program produces DXF for easy import into CAD programs, and VRML output for easy display, plus a Bill of Materials report (chord lengths/counts and hub angles) for construction.

For the geometric method (icosahedron/octahedron subdivision, projection, truncation) and reference images, see [METHOD.md](METHOD.md).

## Installation

Requires Python 3.9+.

```
pip install -e .
```

This installs `numpy`, `pandas`, and `scipy` as dependencies, and provides a `pydome` console command. For running the test suite, install the `test` extra instead:

```
pip install -e ".[test]"
pytest
```

## Usage

```
pydome -o output/mydome -f 4 -r 1.0
```

produces `output/mydome.dxf`, `output/mydome.wrl`, and prints a JSON Bill of Materials report to stdout.

### Command-line options

| Flag | Long form | Description | Default |
|---|---|---|---|
| `-o` | `--output` | Output file path; `.dxf`/`.wrl` are appended. Required. | — |
| `-r` | `--radius` | Dome radius. Must be > 0. | `1.0` |
| `-f` | `--frequency` | Subdivision frequency. Must be a positive integer. | `4` |
| `-p` | `--polyhedron` | Base polyhedron: `icosahedron` or `octahedron`. | `icosahedron` |
| `-t` | `--truncation` | Cutoff ratio (0-1) from the bottom of the sphere; passing this enables truncation. Incompatible with `-F`. | off (full sphere) |
| `-v` | `--vthreshold` | Distance below which two computed vertices are treated as the same point. | `0.0000001` |
| `-b` | `--bom-rounding` | Decimal places to display, and merge granularity, for the Bill of Materials (see caveats below). | `9` |
| `-F` | `--face` | Emit face data (not wireframe) in the WRL output; skips DXF entirely. Incompatible with `-t`. | off |
| `-h` | `--help` | Show usage and exit. | — |

## Caveats and known limitations

A few behaviors are worth understanding before relying on the output for a real build.

- **Truncation at an exactly horizontal chord fails loudly.** If the truncation cutoff plane happens to land exactly on a chord that lies flat in that plane, `truncate()` raises a clear `ValueError` naming the chord rather than producing a corrupted vertex. This is why the `-t/--truncation` help text recommends sticking to the default (`0.499999`) or `0.333333` — these ratios are chosen to avoid landing exactly on a vertex ring for typical frequencies. If you hit this error, nudge `-t` slightly.

- **`-b/--bom-rounding` controls two things at once: display precision and merge granularity.** Chords are grouped into Bill-of-Materials rows by clustering their lengths, not by independently rounding each one — this avoids splitting a single true strut length into multiple rows due to floating-point noise. The clustering tolerance is derived from `-b`, so a coarser value (e.g. `-b 2`) intentionally merges strut lengths that are close but not identical, which is useful when your fabrication tools can't distinguish sub-millimeter differences. The default is `9`, which stays exact (no unintended merging) at any practical dome frequency. If you deliberately lower `-b` for a high-frequency dome, be aware it may merge lengths that are actually meant to be different — check the DXF/report before cutting material to a merged length.

- **`-f/--frequency` must be a positive integer and `-r/--radius` must be greater than zero.** Both are validated with a clear error message; there is no dome at frequency 0 or radius 0.

- **`-v/--vthreshold` controls vertex deduplication**, i.e. how close two computed vertices must be to be treated as the same point where polyhedron faces meet. The default (`1e-7`) is tuned for the default unit radius; if you use a very large or very small `-r`, you may need to adjust `-v` proportionally.

- **`-F/--face` (face output) cannot be combined with `-t/--truncation`.** Use one or the other.

- **Chord/vertex counts grow with the square of frequency** (a Class One subdivision of an icosahedron produces `20*f^2` faces). Vertex deduplication uses a KD-tree and scales well even at high frequency, but very high frequencies will still produce large DXF/VRML files and correspondingly large Bill of Materials reports.

- **Small-length chords in the output can be artifacts of the geometry pipeline** rather than intentional struts — the tool already surfaces this as a warning in the Bill of Materials report. Check any unexpectedly short chord in a DXF viewer before building.

## Project structure

`pydome` is a regular Python package (`pyproject.toml` declares it under `[tool.setuptools] packages = ["pydome"]`), not a flat collection of top-level modules.

| File | Responsibility |
|---|---|
| `pydome/__init__.py` | Package marker; intentionally empty besides the license header. |
| `pydome/__main__.py` | Enables `python -m pydome`; delegates to `cli.main()`. |
| `pydome/cli.py` | CLI entry point (`pydome` console command → `cli:main`): argument parsing/validation and orchestration. |
| `pydome/polyhedral.py` | The base polyhedra (`Icosahedron`, `Octahedron`) and the `Vertex`/`Chord`/`Face` primitives. |
| `pydome/symmetry_triangle.py` | Class One subdivision of a single polyhedron face into a triangular vertex/chord/face grid. |
| `pydome/geodesic_sphere.py` | Replicates the symmetry triangle across every polyhedron face, deduplicates the vertices shared along adjacent-face edges (via a KD-tree), and projects the result onto a sphere of the requested radius. |
| `pydome/truncation.py` | Cuts a geodesic sphere at a horizontal plane to produce a dome. |
| `pydome/output.py` | DXF and VRML (wireframe or face) file writers. |
| `pydome/bill_of_materials.py` | Clusters chords into strut-length groups, computes hub tangent-plane and spoke angles, and prints the report as JSON. |
| `tests/` | pytest suite: unit tests per module (importing from `pydome.*`) plus subprocess-level CLI integration tests (invoked via `python -m pydome`). |
| `METHOD.md` | The geometric method walkthrough with reference images (icosahedron subdivision, projection, truncation). |
| `images/` | Diagrams referenced by `METHOD.md`. |

Internally, vertices/chords/faces are referenced by plain integer index into Python lists — 0-indexed throughout, matching how they're actually used (this wasn't always true; earlier versions numbered them 1-indexed and subtracted 1 at every point of use).

## Development

```
pip install -e ".[test]"
pytest
```

The test suite includes golden-value checks against known geodesic-dome vertex/edge/face-count formulas (e.g. an icosahedron-derived sphere at frequency `f` has `10f²+2` vertices, `30f²` edges, `20f²` faces), so a correctness regression in the geometry pipeline should show up as a failing count rather than just an exception.

This codebase was ported from Python 2 to Python 3, and most of the Python 2-isms found along the way (bare `except:` clauses, wildcard imports, a private/deprecated `numpy.linalg.linalg`/`numpy.matrix` API, 1-indexed vertex numbering) have been cleaned up. If you spot code that still looks unusual for modern Python — e.g. the manual dict-based grouping in `pydome/bill_of_materials.py` where a `collections.defaultdict` would read more clearly — it's likely another such holdover rather than an intentional design choice. Feel free to modernize it if you're in the area, just add/update tests alongside.

## License

GPLv3. See [LICENSE](LICENSE).
