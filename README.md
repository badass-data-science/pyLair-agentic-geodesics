pyDome
======

A geodesic dome calculator written in Python.

pyDome calculates vertices and chords of Class I ("Alternate") and Class II ("Triacon") geodesic domes of arbitrary size. Domes created by pyDome can be truncated to facilitate structure design. The program produces DXF for easy import into CAD programs, and VRML output for easy display, plus a Bill of Materials report (chord lengths/counts, hub angles, and total strut length/cost) for construction.

For the geometric method (icosahedron/octahedron subdivision, projection, truncation) and reference images, see [METHOD.md](METHOD.md).

## Installation

Requires Python 3.9+.

```
pip install -e .
```

This installs `numpy`, `pandas`, `scipy`, and `matplotlib` as dependencies, and provides a `pydome` console command. For running the test suite, install the `test` extra instead:

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
| `-c` | `--class` | Subdivision class: `1` (Alternate) or `2` (Triacon). Class 2 requires an even `-f`. | `1` |
| `-t` | `--truncation` | Cutoff ratio (0-1) from the bottom of the sphere; passing this enables truncation. Incompatible with `-F`. | off (full sphere) |
| `-v` | `--vthreshold` | Distance below which two computed vertices are treated as the same point. | `0.0000001` |
| `-b` | `--bom-rounding` | Decimal places to display, and merge granularity, for the Bill of Materials (see caveats below). | `9` |
| `-m` | `--material-cost` | Price per unit length of strut material. If given, adds an estimated total material cost to the report alongside the total strut length (which is always reported). Must be > 0. | off (length only) |
| `-F` | `--face` | Emit face data (not wireframe) in the WRL output; skips DXF entirely. Incompatible with `-t`. | off |
| `-P` | `--preview` | Also save a quick 3D wireframe preview image (`<output>.png`) for a fast sanity check without opening a CAD/VRML viewer. | off |
| `-s` | `--stl` | Also save an STL file (`<output>.stl`) of the dome's surface triangles, e.g. for 3D-printing a scale model. Requires face data; incompatible with `-t`. | off |
| `-O` | `--obj` | Also save an OBJ file (`<output>.obj`) of the dome's surface triangles. Requires face data; incompatible with `-t`. | off |
| `-H` | `--hub-templates` | Also save one 2D DXF cutting template per unique hub connector shape (`<output>_hubtype1.dxf`, `<output>_hubtype2.dxf`, ...), for laser-cutting/CNC connector plates. | off |
| `-h` | `--help` | Show usage and exit. | — |

## Caveats and known limitations

A few behaviors are worth understanding before relying on the output for a real build.

- **Truncation at an exactly horizontal chord fails loudly.** If the truncation cutoff plane happens to land exactly on a chord that lies flat in that plane, `truncate()` raises a clear `ValueError` naming the chord rather than producing a corrupted vertex. This is why the `-t/--truncation` help text recommends sticking to the default (`0.499999`) or `0.333333` — these ratios are chosen to avoid landing exactly on a vertex ring for typical frequencies. If you hit this error, nudge `-t` slightly.

- **`-b/--bom-rounding` controls two things at once: display precision and merge granularity.** Chords are grouped into Bill-of-Materials rows by clustering their lengths, not by independently rounding each one — this avoids splitting a single true strut length into multiple rows due to floating-point noise. The clustering tolerance is derived from `-b`, so a coarser value (e.g. `-b 2`) intentionally merges strut lengths that are close but not identical, which is useful when your fabrication tools can't distinguish sub-millimeter differences. The default is `9`, which stays exact (no unintended merging) at any practical dome frequency. If you deliberately lower `-b` for a high-frequency dome, be aware it may merge lengths that are actually meant to be different — check the DXF/report before cutting material to a merged length.

- **`-f/--frequency` must be a positive integer and `-r/--radius` must be greater than zero.** Both are validated with a clear error message; there is no dome at frequency 0 or radius 0.

- **`-v/--vthreshold` controls vertex deduplication**, i.e. how close two computed vertices must be to be treated as the same point where polyhedron faces meet. The default (`1e-7`) is tuned for the default unit radius; if you use a very large or very small `-r`, you may need to adjust `-v` proportionally.

- **`-F/--face`, `-s/--stl`, and `-O/--obj` all require face data, and none of them can be combined with `-t/--truncation`.** `truncate()` only recomputes vertices and chords, not the face list, so any face-based output after truncation would be built from stale, mismatched geometry — the CLI rejects the combination outright rather than silently producing a wrong mesh.

- **`-c 2` (Class II / Triacon) requires an even `-f/--frequency`.** Each polyhedron face is first split into 6 LCD (lowest common denominator) sub-triangles around its centroid before the requested frequency subdivides each of those further, so the frequency is implicitly divided by 2 internally; an odd frequency has no valid Class II construction and is rejected with a clear error.

- **Chord/vertex counts grow with the square of frequency.** A Class I subdivision of an icosahedron produces `20*f^2` faces; Class II produces `120*(f/2)^2` faces (more, at a given frequency, since Class II is already 6-way subdivided before the frequency-level grid is applied). Vertex deduplication uses a KD-tree and scales well even at high frequency, but very high frequencies will still produce large DXF/VRML files and correspondingly large Bill of Materials reports.

- **Small-length chords in the output can be artifacts of the geometry pipeline** rather than intentional struts — the tool already surfaces this as a warning in the Bill of Materials report. Check any unexpectedly short chord in a DXF viewer before building.

- **`-H/--hub-templates` clusters hubs by a rotation-invariant "shape" signature** (valence, plus the cyclic pattern of angular gaps and tangential angles going around the hub), not by symmetry group membership — two hubs get the same template if and only if one is a rotation of the other, regardless of *why*. The clustering tolerance (3 decimal places on angle values) was tuned empirically: the geometry pipeline's floating-point noise was observed to reach the 6th decimal place on otherwise-identical hubs, and a precision of 6 failed to merge them, silently doubling the reported template count. If you're working at a much higher frequency than has been tested (up to 16) and the template count looks suspiciously large for the dome's symmetry, that noise floor is the first thing to check.

## Project structure

`pydome` is a regular Python package (`pyproject.toml` declares it under `[tool.setuptools] packages = ["pydome"]`), not a flat collection of top-level modules.

| File | Responsibility |
|---|---|
| `pydome/__init__.py` | Package marker; intentionally empty besides the license header. |
| `pydome/__main__.py` | Enables `python -m pydome`; delegates to `cli.main()`. |
| `pydome/cli.py` | CLI entry point (`pydome` console command → `cli:main`): argument parsing/validation and orchestration. |
| `pydome/polyhedral.py` | The base polyhedra (`Icosahedron`, `Octahedron`), the `Vertex`/`Chord`/`Face` primitives, and `build_lcd_faces` (splits each face into 6 sub-triangles for Class II). |
| `pydome/symmetry_triangle.py` | Subdivides a single polyhedron face (Class I) or LCD sub-triangle (Class II) into a triangular vertex/chord/face grid. |
| `pydome/geodesic_sphere.py` | Replicates the symmetry triangle across every polyhedron face, deduplicates the vertices shared along adjacent-face edges (via a KD-tree), and projects the result onto a sphere of the requested radius. |
| `pydome/truncation.py` | Cuts a geodesic sphere at a horizontal plane to produce a dome. |
| `pydome/output.py` | DXF, VRML (wireframe or face), STL, OBJ, and hub-connector-template file writers. |
| `pydome/preview.py` | Renders a quick 3D wireframe preview PNG (`-P/--preview`), with equal axis scaling so the plot itself never distorts the dome's proportions. |
| `pydome/bill_of_materials.py` | Clusters chords into strut-length groups, computes hub tangent-plane and spoke angles, clusters hubs into connector-plate "types" (`-H/--hub-templates`), and prints the report as JSON. |
| `tests/` | pytest suite: unit tests per module (importing from `pydome.*`) plus subprocess-level CLI integration tests (invoked via `python -m pydome`). |
| `METHOD.md` | The geometric method walkthrough with reference images (icosahedron subdivision, projection, truncation). |
| `images/` | Diagrams referenced by `METHOD.md`. |

Internally, vertices/chords/faces are referenced by plain integer index into Python lists — 0-indexed throughout, matching how they're actually used (this wasn't always true; earlier versions numbered them 1-indexed and subtracted 1 at every point of use).

## Development

```
pip install -e ".[test]"
pytest
```

The test suite includes golden-value checks against known geodesic-dome vertex/edge/face-count formulas (e.g. a Class I icosahedron-derived sphere at frequency `f` has `10f²+2` vertices, `30f²` edges, `20f²` faces; Class II has `60m²+2` vertices, `180m²` edges, `120m²` faces, where `m=f/2`), so a correctness regression in the geometry pipeline should show up as a failing count rather than just an exception. The Class II formulas were verified empirically (via Euler's formula `V-E+F=2` and `2E=3F`, which must hold for any closed triangulated mesh) rather than taken purely from a derivation — an earlier version of `ClassTwoMethodOneSymmetryTriangle` had a real bug (assumed an orthogonal local coordinate basis that only happens to hold for Class I's equilateral triangle) that these identities caught immediately, before the golden-value formulas were even known.

This codebase was ported from Python 2 to Python 3, and most of the Python 2-isms found along the way (bare `except:` clauses, wildcard imports, a private/deprecated `numpy.linalg.linalg`/`numpy.matrix` API, 1-indexed vertex numbering) have been cleaned up. If you spot code that still looks unusual for modern Python — e.g. the manual dict-based grouping in `pydome/bill_of_materials.py` where a `collections.defaultdict` would read more clearly — it's likely another such holdover rather than an intentional design choice. Feel free to modernize it if you're in the area, just add/update tests alongside.

## License

GPLv3. See [LICENSE](LICENSE).
