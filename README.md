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

produces `output/mydome.dxf`, `output/mydome.wrl`, and prints a JSON Bill of Materials report to stdout. Run `pydome --help` for the full list of options (radius, frequency, polyhedron, truncation, vertex threshold, BOM rounding, face output).

## Caveats and known limitations

A few behaviors are worth understanding before relying on the output for a real build.

- **Truncation at an exactly horizontal chord fails loudly.** If the truncation cutoff plane happens to land exactly on a chord that lies flat in that plane, `truncate()` raises a clear `ValueError` naming the chord rather than producing a corrupted vertex. This is why the `-t/--truncation` help text recommends sticking to the default (`0.499999`) or `0.333333` — these ratios are chosen to avoid landing exactly on a vertex ring for typical frequencies. If you hit this error, nudge `-t` slightly.

- **`-b/--bom-rounding` controls two things at once: display precision and merge granularity.** Chords are grouped into Bill-of-Materials rows by clustering their lengths, not by independently rounding each one — this avoids splitting a single true strut length into multiple rows due to floating-point noise. The clustering tolerance is derived from `-b`, so a coarser value (e.g. `-b 2`) intentionally merges strut lengths that are close but not identical, which is useful when your fabrication tools can't distinguish sub-millimeter differences. The default is `9`, which stays exact (no unintended merging) at any practical dome frequency. If you deliberately lower `-b` for a high-frequency dome, be aware it may merge lengths that are actually meant to be different — check the DXF/report before cutting material to a merged length.

- **`-f/--frequency` must be a positive integer and `-r/--radius` must be greater than zero.** Both are validated with a clear error message; there is no dome at frequency 0 or radius 0.

- **`-v/--vthreshold` controls vertex deduplication**, i.e. how close two computed vertices must be to be treated as the same point where polyhedron faces meet. The default (`1e-7`) is tuned for the default unit radius; if you use a very large or very small `-r`, you may need to adjust `-v` proportionally.

- **`-F/--face` (face output) cannot be combined with `-t/--truncation`.** Use one or the other.

- **Chord/vertex counts grow with the square of frequency** (a Class One subdivision of an icosahedron produces `20*f^2` faces). Vertex deduplication uses a KD-tree and scales well even at high frequency, but very high frequencies will still produce large DXF/VRML files and correspondingly large Bill of Materials reports.

- **Small-length chords in the output can be artifacts of the geometry pipeline** rather than intentional struts — the tool already surfaces this as a warning in the Bill of Materials report. Check any unexpectedly short chord in a DXF viewer before building.

## License

GPLv3. See [LICENSE](LICENSE).
