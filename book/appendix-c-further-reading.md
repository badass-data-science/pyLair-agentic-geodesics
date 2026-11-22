# Appendix C: Further Reading

The sources this book's chapters draw on, and the independent tools pyLair and pyFit are checked against. It's a working bibliography, not a survey of the field.

## Geodesic Geometry

- Kenner, Hugh (1976). *Geodesic Math and How to Use It*. Berkeley: University of California Press. The classic practical reference for geodesic subdivision, and the source of the Class I, II, and III vocabulary. (Chapters 4–6)
- Goldberg, Michael (1937). "A Class of Multi-Symmetric Polyhedra." *Tôhoku Mathematical Journal* 43: 104–108. The first description of the `(m,n)` family of polyhedra behind Class III. (Chapter 6)
- Caspar, D. L. D., and A. Klug (1962). "Physical Principles in the Construction of Regular Viruses." *Cold Spring Harbor Symposia on Quantitative Biology* 27: 1–24. https://doi.org/10.1101/sqb.1962.027.001.005. The triangulation number `T` as a classification of virus shells. (Chapter 6)
- Coxeter, H. S. M. (1971). "Virus Macromolecules and Geodesic Domes." In J. C. Butcher, ed., *A Spectrum of Mathematics*, 98–107. Auckland and London: Auckland University Press and Oxford University Press. Connects the Goldberg and Caspar–Klug constructions to geodesic domes. (Chapter 6)
- Šiber, Antonio (2007). "Icosadeltahedral Geometry of Fullerenes, Viruses and Geodesic Domes." arXiv:0711.3527. https://arxiv.org/abs/0711.3527. A readable tutorial on the `(m,n)` framework and `T = m² + mn + n²`; an extended version appeared in *Symmetry* in 2020 as "Icosadeltahedral Geometry of Geodesic Domes, Fullerenes and Viruses: A Tutorial on the T-Number." (Chapter 6)
- Euler, Leonhard (1758). "Elementa doctrinae solidorum." *Novi Commentarii academiae scientiarum Petropolitanae* 4: 109–140 (Eneström number E230; written around 1750). The source of the polyhedron formula `V − E + F = 2`. (Chapter 5)
- [`antitile`](https://github.com/brsr/antitile), by brsr. An independently written, open-source implementation of the general Goldberg–Coxeter construction, used during development to verify pyLair's Class III construction; never a pyLair runtime dependency. (Chapter 6)

## Independent Geometry Checks

- [`trimesh`](https://trimesh.org/). Recomputes panel areas and the angles between panels from pyLair's exported files, and its mesh-slicing routine serves as an independent check on truncated panels. (Chapter 24)
- [`ezdxf`](https://ezdxf.readthedocs.io/). Reads a generated panel cutting template back in to confirm it reproduces the edge lengths it claims. (Chapter 24)

## 2D Nesting

- [`pyclipper`](https://github.com/fonttools/pyclipper). Python bindings to the Clipper polygon-clipping library; pyFit's engine for the Minkowski sums behind its no-fit polygons. (Chapter 19)
- [`shapely`](https://shapely.readthedocs.io/). General-purpose 2D geometry used throughout pyFit: areas, bounds, overlap tests, and the union that resolves the Minkowski-sum "hole" described in Chapter 19.
- [SVGnest](https://github.com/Jack000/SVGnest) and [Deepnest](https://github.com/Jack000/Deepnest). Open-source no-fit-polygon nesting tools whose general approach pyFit's README cites as the family its heuristic belongs to; pyFit's implementation is its own. (Chapter 19)

## Companion Reading

- [`blog-posts/introducing-pylair.md`](https://github.com/badass-data-science/pyLair-agentic-geodesics/blob/main/blog-posts/introducing-pylair.md), "Introducing pyLair (or, How Our Heroine Designed Her Geodesic Secret Lair)": the shorter companion to this book's pyLair half.
- `blog-posts/introducing-pyfit.md`, in the [pyFit repository](https://github.com/badass-data-science/pyFit-agentic-polygon-nesting): the same for the nesting half.
- Each project's `README.md` (its caveats and known limitations) and `AGENTS.md` (its engineering notes), kept current beyond whatever this book covers.
- *Agentic Time Series Forecasting for Supervillains*, *Systems Thinking for Supervillains*, and *Strategy for Supervillains*, the other volumes in the series. None is a prerequisite.
