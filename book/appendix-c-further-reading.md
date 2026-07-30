# Appendix C: Further Reading

The real sources pyLair's and pyFit's own constructions are drawn from and verified against — not a general bibliography, but the specific material this book's own chapters actually relied on.

## Geodesic Geometry

- Kenner, H. (1976). *Geodesic Math and How to Use It*. University of California Press. The foundational reference for the subdivision methods pyLair implements.
- Šiber, A. (2007). ["Icosadeltahedral geometry of fullerenes, viruses and geodesic domes"](https://arxiv.org/abs/0711.3527). arXiv:0711.3527. The source for the `(m,n)` Caspar-Klug/Goldberg-Coxeter framework and the `T = m² + mn + n²` triangulation-number formula that Classes I, II, and III (Chapters 4–6) all turn out to be special cases of.
- [`antitile`](https://github.com/brsr/antitile) (brsr). An independently-written, open-source implementation of the general Goldberg-Coxeter construction. Used as a development-time correctness oracle to verify pyLair's Class III construction bit-for-bit (Chapter 6) — never a pyLair runtime dependency.

## Independent Geometry Oracles

- [`trimesh`](https://trimesh.org/). Independently recomputes panel areas and inter-panel angles from pyLair's own exported files, and serves as an independent ground truth for truncated-panel clipping via its own mesh-slicing routine — referenced in Chapter 17 and pyLair's own `README.md`/test suite.
- [`ezdxf`](https://ezdxf.readthedocs.io/). Parses a generated panel cutting template back out to confirm it reproduces the exact edge lengths it claims to — a parse-then-measure round trip, not a restatement of the same trigonometry (Chapter 15, Chapter 23).

## 2D Nesting

- [`pyclipper`](https://github.com/fonttools/pyclipper). Python bindings to the Clipper polygon-clipping library; the underlying engine for pyFit's no-fit-polygon (Minkowski-sum) computation (Chapter 19).
- [`shapely`](https://shapely.readthedocs.io/). General-purpose 2D geometry used throughout pyFit — polygon area, bounds, intersection tests, and the union operation that resolves the Minkowski-sum hole artifact described in Chapter 19.
- The general family of bottom-left-fill, no-fit-polygon nesting tools — SVGnest and DeepNest — whose shape pyFit's own heuristic follows, per its own documentation, though its implementation is original rather than ported from either (Chapter 19).

## Companion Reading

- [`blog-posts/introducing-pylair.md`](../blog-posts/introducing-pylair.md) — "Introducing pyLair, or, How Our Heroine Designed Her Geodesic Secret Lair," the shorter, funnier companion to this entire book's pyLair half.
- pyFit's own companion blog post, `blog-posts/introducing-pyfit.md`, in the `pyFit-agentic-polygon-nesting` repository — the same treatment for the nesting half.
- Each project's own `README.md` "Caveats and known limitations" / "Known limitations" section, and `AGENTS.md` — the toolkits' own standing engineering notes, kept current well past whatever this book happened to cover.
