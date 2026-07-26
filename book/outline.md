# Agentic Geodesic Lair Design for Supervillains
### Computational Geometry and Agentic AI with pyLair
**Proposed Outline**

---

## About This Outline

This is a chapter-by-chapter proposal for the book, not the book itself — the
same kind of document as [the outline for *Agentic Time Series Forecasting
for Supervillains*](../../omen-agentic-time-series-forecasting/book/outline.md),
this series' companion volume, whose structure and conventions this outline
deliberately follows. Every chapter below uses the same template:

- **Concept(s) taught** — the geometry/engineering idea(s) at the center of the chapter.
- **pyLair interfaces used** — the actual CLI flags, Python API calls, and/or
  MCP tools the chapter's exercises use, by name.
- **Learning objectives** — what the reader should be able to do afterward.
- **The villainous example** — the running dome design for the chapter, and why its shape fits the lesson.
- **Gotchas & rationale** — the specific "here's why this isn't as simple as it looks" content the book promises, grounded in real, documented behavior of pyLair (its README caveats, its test suite, and its git history) — not invented for the outline.
- **Sample prompts** — 2–3 representative prompts in the book's prompt-based instructional style, in the same voice as Part VI's agentic-prompting chapters.

Chapters follow the actual shape of a dome moving through pyLair's pipeline —
pick a polyhedron, subdivide it, project it onto a sphere, shape it
(elongate, truncate), then account for it (bill of materials, cutting
templates, export) — because that's also the order in which each stage's
correctness *depends* on the one before it: you can't honestly truncate a
sphere whose projection is wrong, and you can't honestly report a bevel
angle for a face whose truncation clipped it incorrectly.

Two dome designs recur across multiple chapters as a light narrative
through-line, the same way the companion blog post ("Introducing pyLair, or,
How Our Heroine Designed Her Geodesic Secret Lair") keeps returning to one
heroine's Ultimate Cunning Master Plan&trade;:

- **The Proof-of-Concept Yurt** — a tiny, deliberately unambitious Class I
  icosahedral dome (frequency 2, radius 1, no truncation), introduced in
  Chapter 2 purely to prove the CLI/MCP wiring works, the same way the Omen
  book's own install chapter uses a 5-point toy series too small to mean
  anything statistically.
- **The Actual Secret Lair** — a full-scale Class III (chiral) dome,
  elongated for extra ceiling height, truncated on multiple axes for a
  ground-flush footprint with room for a door, finally exported for real in
  Part V. This is the dome the blog post's heroine is actually building, and
  the one this book's chapters slowly earn the right to export.

A third, smaller example — **The Under-the-Ocean Prototype** — appears where
a chapter specifically needs a second, contrasting shape (a squashed
ellipsoid built for pressure symmetry rather than headroom, name and framing
lifted directly from the blog post's own opening joke about where a secret
laboratory really belongs), and gets a full dedicated tour alongside four
new siblings — an orbital station, a volcano lair, an arctic cache, and one
deliberately un-hidden mountain spire — in Chapter 11, once Part III has
given readers every shaping tool those examples actually use.

---

## Front Matter

- **Title Page** — title, subtitle, "as told by our heroine," and a
  one-paragraph framing note connecting this book to
  [`blog-posts/introducing-pylair.md`](../blog-posts/introducing-pylair.md),
  which readers are encouraged to treat as companion reading, not a
  prerequisite — the same relationship the Omen book has with its own blog
  series.
- **About the "for Supervillains" Series** — this volume *is* the
  "*Geodesic Lair Design for Supervillains*" the Omen book's own
  `about_the_series.md` already promised was coming, several NDAs later than
  planned. Notes the shared universe (same heroine, same Ultimate Cunning
  Master Plan&trade;, mojitos optional but encouraged) without requiring the
  other book as a prerequisite.
- **How to Use This Book**
  - Who this book assumes you are: comfortable with basic 3D coordinate
    geometry (vertices, planes, angles) and command-line tools; new to
    geodesic subdivision specifically and to agentic tool-use generally.
  - The prompt-based convention used throughout: every worked example shows
    a boxed **Prompt** (what you'd actually type to your agent) followed by
    **What Comes Back** (the tool's real JSON/CLI output, trimmed for
    space) and **What It Means** (the plain-language interpretation).
  - A note that every number, error message, and file shown in this book is
    from a *real* `pylair`/`pylair-mcp` run against real parameters — not a
    hand-typed mockup — and that every named dome design (the
    Proof-of-Concept Yurt, the Actual Secret Lair, and the rest) can be
    regenerated exactly by running `book/examples/generate_book_domes.py`
    (see `book/examples/README.md`), the same reproducibility convention
    the Omen book established for its datasets.
  - Pointers to `README.md` (the full CLI/MCP reference and caveats list)
    and `AGENTS.md` (the toolkit's own agent-facing engineering notes,
    including the geometry pipeline's historical footguns) for readers who
    want to go deeper than any one chapter.
- **A Word on AI Use** — matches the convention already established in the
  blog post's own AI Use Statement: the original pyLair implementation was
  hand-written from scratch, then extended feature-by-feature in
  collaboration with an AI coding assistant (Class II/III subdivision,
  elongation, STL/OBJ/PNG output, face-aware truncation); this book's prose
  follows the same pattern — drafted collaboratively, checked line-by-line
  against the actual codebase, test suite, and git history, not invented.
- **Dedication** — short, in the same register as the Omen book's own.

---

## Part I — Meet Your New Design Engineer

### Chapter 1: Introducing pyLair and the Agentic Interface

**Concept(s) taught:** What pyLair actually computes (vertices, chords, and
faces of a geodesic dome or sphere) and what it doesn't (it is not a
structural engineering tool — it reports lengths and angles, not load
ratings); the same "agentic AI" distinction the Omen book opens with,
applied to CAD instead of statistics — an agent driving pyLair's typed
tools and reasoning between calls, as opposed to an LLM free-handing
`numpy` trigonometry from scratch and hoping it's right.

**pyLair interfaces used:** None yet — conceptual scaffolding. Previews
`design_dome`'s output shape as a teaser without explaining it.

**Learning objectives:**
- Describe, at a high level, what a geodesic subdivision *is* (a polyhedron
  face divided into a triangular grid, then projected onto a sphere) and
  why it distributes structural stress more evenly than a dome with large
  flat panels.
- Distinguish the four things pyLair actually hands back — a shape
  (vertices/chords/faces), export files (DXF/VRML/STL/OBJ), a bill of
  materials, and cutting templates — from the physical build itself, which
  remains entirely the reader's problem.
- Explain why "just ask the AI to design a dome" without a real geometry
  engine underneath it fails silently: an LLM asked to compute hub angles
  freehand will produce *plausible-looking* numbers with no guarantee they
  close correctly in 3D.

**The villainous example:** A cold open, borrowed directly from the blog
post — our heroine's secret laboratory has outgrown her studio apartment,
and whatever she builds next needs to (a) look cool, and (b) handle
pressure gradients gracefully, because a proper secret lab belongs deep
underwater or in circumpolar orbit, not in an unassuming San Diego
neighborhood. This is the problem the book solves, not yet with geometry —
just a promise that Chapter 3 picks this back up.

**Gotchas & rationale:**
- Why hand-rolled dome math is dangerous specifically at the *hub*, not the
  *chord*: a chord length is forgiving of small errors (the strut is just
  slightly the wrong length), but a wrong hub angle compounds — every strut
  meeting at that hub inherits the error, and the dome may not physically
  close.
- The core tension this book keeps returning to: pyLair deliberately keeps
  its geometry engine's validation rule-based and shared (`api.py`, used
  identically by the CLI and every MCP tool) rather than letting an agent
  freelance the math per request — the same "deterministic gates around
  agentic judgment" idea the Omen book centers, applied here to geometric
  correctness instead of a deploy decision.

**Sample prompts:**
- "Explain, in your own words, why pyLair computes the geometry itself
  instead of just asking you to describe what a geodesic dome would look
  like."
- "What's the difference between asking for a dome's vertex/edge/face
  counts and asking for its full bill of materials?"

---

### Chapter 2: Installing pyLair (CLI, MCP, and Your Agent of Choice)

**Concept(s) taught:** Python packaging extras as an install-time choice
(`[test]`, `[mcp]`, `[verify]`) rather than one monolithic dependency list;
how an MCP (Model Context Protocol) server connects to an agentic client —
stdio transport, tool discovery, the console-script pattern — enough to
install pyLair on whatever platform the reader is actually using.

**pyLair interfaces used:** `pip install -e ".[mcp]"`, the `pylair-mcp`
console command; the chapter ends with a real smoke test calling
`design_dome` once, successfully, as proof of life.

**Learning objectives:**
- Install pyLair (`pip install -e .` for the CLI alone, `.[mcp]` to add the
  agentic interface) into a clean environment.
- Register the `pylair-mcp` server with at least one MCP-speaking client.
- Confirm installation success via a live tool call, not just "the install
  command didn't error."
- Know which extra to reach for later: `[test]` for the test suite,
  `[verify]` for the independent geometry oracle used in Part II and Part
  IV (and, as this book's own real history proves in Chapter 21, worth
  double-checking on whatever Python version you're actually running).

**The villainous example:** **The Proof-of-Concept Yurt** — `pylair -o
poc-yurt -f 2 -r 1.0`, a tiny, unremarkable Class I dome, deliberately
too small and plain to be anyone's actual secret lair. The point isn't the
shape; it's proving the wiring works before anything ambitious is
attempted.

**Gotchas & rationale:**
- The CLI and the MCP server share one validation engine
  (`pylair/api.py:validate_geometry_params`) — demonstrated live by
  triggering the same error (an invalid Class II odd frequency) through
  both interfaces and getting the identical message back, proof this isn't
  two implementations that happen to agree today.
- A live, narrated example of a real class of MCP install failure: a
  subprocess launched by a bare command name can fail to find `pylair-mcp`
  if it doesn't inherit the parent process's activated-environment `PATH`
  — fixed by pointing the client config at the console script's absolute
  path instead.

**Sample prompts:**
- "Confirm the pyLair MCP server is running and list every tool it
  exposes."
- "Run `design_dome` on the smallest, cheapest configuration you can, just
  to prove the connection works end to end."

---

## Part II — From Polyhedron to Sphere

### Chapter 3: Picking a Polyhedron

**Concept(s) taught:** Why geodesic subdivision starts from an existing
near-spherical, symmetric solid rather than an arbitrary shape; the
icosahedron (20 faces, 12 vertices) versus the octahedron (8 faces, 6
vertices) as pyLair's two starting points, and how that choice ripples
through every later vertex/face count.

**pyLair interfaces used:** `-p/--polyhedron`, `pylair.polyhedral.Icosahedron`
/ `Octahedron`.

**Learning objectives:**
- Explain, geometrically, why starting closer to a sphere means fewer
  distinct strut/hub types are needed to approximate one well at a given
  frequency.
- Read the golden-value vertex/edge/face count formulas for each base
  polyhedron (`20f²` faces for an icosahedron, `8f²` for an octahedron,
  before any subdivision-class multiplier is applied) as a sanity check,
  not folklore.
- Choose a base polyhedron appropriate to a real design goal (more
  faces-per-frequency for a rounder look at low frequency, versus an
  octahedron's natural fit for a design that wants a flat "equator" ring at
  Z=0 already present in the base shape).

**The villainous example:** **The Under-the-Ocean Prototype** — evaluated
here specifically for base-polyhedron choice: an icosahedron's already-flatter
near-equatorial ring of vertices turns out to matter once Chapter 9 needs to
truncate this exact shape for a pressure-symmetric hull.

**Gotchas & rationale:**
- The two base polyhedra are not interchangeable at "the same" frequency —
  an octahedron-based Class I dome at frequency `f` has `8f²` faces where
  an icosahedron-based one has `20f²`; a reader who swaps polyhedron
  without adjusting frequency to compensate will get a very differently
  detailed structure than they expected.
- pyLair's internal indexing is 0-indexed throughout — worth mentioning
  here as a "boring but real" note, since an earlier version of the
  codebase numbered vertices 1-indexed and subtracted 1 at every point of
  use, a class of bug this book will return to in Part VI as an example of
  why "modernize it if you're in the area" is real, standing engineering
  guidance in this codebase (`AGENTS.md`), not just a stylistic nicety.

**Sample prompts:**
- "Using `design_dome`, compare an icosahedron and an octahedron at the
  same frequency. How different are the resulting face counts, and why?"
- "I want a natural flat ring near the equator before any truncation
  happens — which base polyhedron gets me closer to that for free?"

---

### Chapter 4: Class I — The Default Subdivision

**Concept(s) taught:** The "symmetry triangle" as the one piece of geometry
pyLair actually has to solve directly — everything else is replication —
and the Class I ("Alternate") method's grid, drawn parallel to each face's
own edges, as the simplest case to build intuition on before Classes II and
III complicate it.

**pyLair interfaces used:** default `-c 1`,
`pylair.symmetry_triangle.ClassOneMethodOneSymmetryTriangle`.

**Learning objectives:**
- Describe how one computed symmetry triangle gets replicated (rotated,
  not recomputed) across every face of the base polyhedron.
- Read the golden-value formula `10f²+2` vertices / `30f²` edges / `20f²`
  faces for a Class I icosahedral sphere, and use it to sanity-check a
  `design_dome` result before trusting anything downstream.
- Explain why frequency has no upper or lower structural requirement in
  Class I the way it does in Class II — any positive integer is valid.

**The villainous example:** **The Actual Secret Lair**, first appearance —
introduced here at a modest frequency purely to establish its baseline
shape, before Part III starts reshaping it.

**Gotchas & rationale:**
- Chord/vertex counts grow with the *square* of frequency, not linearly — a
  reader doubling frequency expecting roughly double the strut count will
  instead get roughly four times as many, with real consequences for
  fabrication time and file size at high frequency.
- The default vertex-deduplication threshold (`-v`, `1e-7`) is tuned for
  the default unit radius; a reader who scales `-r` up or down by orders of
  magnitude without adjusting `-v` proportionally can end up with either
  falsely-merged or falsely-duplicated vertices at the seams between
  faces — demonstrated with a deliberately mismatched radius/threshold pair.

**Sample prompts:**
- "Build a Class I icosahedral dome at frequency 4. Does the reported
  vertex count match the golden-value formula?"
- "If I double the frequency, how much does the face count actually grow —
  and is that what you expected before I told you?"

---

### Chapter 5: Class II — Triacon and the Even-Frequency Requirement

**Concept(s) taught:** The Class II ("Triacon") method's extra step — each
face first split into 6 sub-triangles around its centroid, *then* frequency
subdivides those — as a genuinely different construction, not just a
different-looking grid; the real historical bug this construction exposed
in an earlier version of pyLair, and how Euler's formula caught it.

**pyLair interfaces used:** `-c 2`, `pylair.polyhedral.build_lcd_faces`,
`pylair.symmetry_triangle.ClassTwoMethodOneSymmetryTriangle`.

**Learning objectives:**
- Explain why Class II requires an even `-f/--frequency` (the frequency is
  implicitly divided by 2 internally, since each face is already split
  6 ways before the frequency grid applies) and predict the clear
  validation error an odd frequency produces.
- Read the Class II golden-value formula (`60m²+2` vertices, `120m²`
  faces, where `m=f/2`) and notice it produces *more* faces than Class I at
  the same nominal frequency, not fewer.
- Use Euler's formula (`V-E+F=2`) and the closed-triangulated-mesh identity
  (`2E=3F`) as an independent correctness check on any subdivision's raw
  vertex/edge/face counts — a technique this chapter teaches specifically
  because it once caught a real bug here.

**The villainous example:** Continues **The Actual Secret Lair**, rebuilt
at the same nominal frequency under Class II for direct visual/structural
comparison against Chapter 4's Class I version.

**Gotchas & rationale:**
- The real, documented bug: an earlier `ClassTwoMethodOneSymmetryTriangle`
  assumed an orthogonal local coordinate basis that only happens to hold
  for Class I's equilateral triangle — silently wrong for Class II's actual
  triangle shape. It passed casual inspection; it failed Euler's formula
  immediately once checked, which is why that identity check, not just
  "does it look like a dome," is worth teaching as a habit.
- Because Class II is already 6-way subdivided *before* the frequency grid
  applies, its strut-type variety at a given nominal frequency is
  meaningfully different from Class I's — a reader expecting "same
  frequency number, similar bill of materials" between the two classes
  will be wrong, and this chapter shows by how much.

**Sample prompts:**
- "Try building a Class II dome at frequency 3. What error do you get, and
  why does frequency have to be even here specifically?"
- "Check this Class II result against Euler's formula by hand. Does
  `V - E + F` actually equal 2?"

---

### Chapter 6: Class III — Going Chiral

**Concept(s) taught:** The Class III ("Skew") method's angled grid as a
genuinely chiral construction — `(m,n)` and `(n,m)` are mirror-image domes
of the same size, not the same dome rotated — introduced via the
Caspar-Klug/Goldberg-Coxeter `T = m² + mn + n²` triangulation number that
all three of pyLair's subdivision classes turn out to be special cases of.

**pyLair interfaces used:** `-c 3 -n`, `pylair.class_three.py`
(`cross_face_matches`, `local_priority`), `pylair.geodesic_sphere.GeodesicSphere`.

**Learning objectives:**
- State what makes `(m,n)` and `(n,m)` genuinely different physical strut
  patterns rather than the same dome viewed differently, and choose between
  them deliberately rather than arbitrarily.
- Explain, at a conceptual level, why a chiral lattice can't be stitched
  together across adjacent polyhedron faces by 3D proximity alone the way
  Class I and Class II can.
- Read the Class III golden-value formula (`10T+2` vertices, `20T` faces,
  where `T = m²+mn+n²`) and connect it back to Chapter 4/5's formulas as
  instances of the same general family.

**The villainous example:** **The Actual Secret Lair**'s final subdivision
choice — Class III, `(m,n)` chosen deliberately over its mirror `(n,m)` for
a specific strut-pattern aesthetic, carried forward as the flagship shape
for the rest of the book.

**Gotchas & rationale:**
- The real, documented bug, told as a full story: a first Class III
  implementation computed each face's grid independently and merged only
  by 3D proximity, like Class I/II — it satisfied Euler's formula *and* the
  golden-value counts while still being wrong, leaving all 30 of the base
  icosahedron's original edges as long, unsubdivided chords, because a
  chiral (`m≠n`) lattice has no reflection symmetry and neighboring faces'
  independently-computed grid points don't land at coincident 3D positions.
  Two structural identities agreed and the dome was still broken — the
  chapter's central lesson that golden-value checks catch *count* errors,
  not *shape* errors.
- The fix (`pylair/class_three.py`) stitches adjacent faces together
  combinatorially — matching grid points by an integer index derived from
  the lattice's own structure, not 3D coordinates — and was cross-checked
  against the independent [`antitile`](https://github.com/brsr/antitile)
  library bit-for-bit (mean-normalized edge-length distributions matching
  to `1e-15`) across several `(m,n)` pairs on both base polyhedra, not
  trusted on the strength of the golden-value counts alone.

**Sample prompts:**
- "Build a Class III dome with `f=4, n=1`. Then build one with `f=1, n=4`.
  Are these the same dome, or mirror images?"
- "Why can't Class III rely on the same vertex-deduplication-by-distance
  trick that Class I and II use across face boundaries?"

---

### Chapter 7: Projecting Onto the Sphere

**Concept(s) taught:** The final geometric step common to all three
classes — pushing every still-flat symmetry-triangle point outward onto an
actual sphere of the requested radius, while deduplicating vertices shared
along adjacent-face edges — and the KD-tree as the practical tool that
makes that deduplication scale.

**pyLair interfaces used:** `pylair.geodesic_sphere.GeodesicSphere`
(`.project_onto_sphere()`, `.locate_duplicate_vertices()`,
`.remove_duplicate_chords()`), `-v/--vthreshold`.

**Learning objectives:**
- Explain the two-step "flat, then push outward" process and why chord
  connectivity has to be computed *before* projection, not after.
- Describe why vertex deduplication needs a spatial index at realistic
  frequencies rather than an all-pairs distance check.
- Diagnose, from symptoms alone, whether a "cracked" seam between faces in
  an exported file is a `-v/--vthreshold` problem versus a genuine Class
  III stitching gap.

**The villainous example:** Continues **The Actual Secret Lair**,
specifically at a high enough frequency that an all-pairs vertex comparison
would visibly slow down, motivating the KD-tree without hand-waving.

**Gotchas & rationale:**
- Class III supplies its own combinatorial cross-face matches (Chapter 6)
  *in addition to* KD-tree proximity matching, not instead of it — proximity
  alone still handles the ordinary within-face duplicate case, while the
  combinatorial matches handle the case proximity can't.
- A too-loose `-v/--vthreshold` at high frequency can falsely merge two
  genuinely distinct, closely-spaced vertices — shown as a real, deliberately
  provoked failure, alongside the opposite (too-tight) failure from Chapter
  4, so readers recognize both directions of this same tradeoff.

**Sample prompts:**
- "At a high frequency, how many vertices get deduplicated during
  projection, and does that number make sense given the face count?"
- "If two hubs that should be identical show up as separate points in the
  output, what's the first setting you'd check?"

---

## Part III — Shaping the Lair

### Chapter 8: Squash and Stretch — Ellipsoid Elongation

**Concept(s) taught:** Independent per-axis scaling (`-e/--elongation`) as
the step that turns a sphere into a general axis-aligned ellipsoid; why
every downstream angle calculation has to use the *true* ellipsoid surface
normal (the gradient of the ellipsoid equation) rather than naively
treating a vertex's position vector as its own normal.

**pyLair interfaces used:** `-e`, `pylair.elongation.elongate()`.

**Learning objectives:**
- Apply independent X/Y/Z elongation factors to raise ceiling height,
  widen a footprint, or both, without distorting the other axes.
- Explain why the naive "position vector as normal" approximation is exact
  only for a true sphere (`1.0,1.0,1.0`) and silently wrong for any other
  elongation.
- Recognize elongation as a step that happens *before* truncation in
  pyLair's pipeline, and explain why that ordering matters for what a
  truncation cutoff fraction actually means.

**The villainous example:** **The Under-the-Ocean Prototype** returns —
here elongated slightly *inward* along Z (a gentle squash, `"1.0,1.0,0.9"`)
for pressure-symmetric hull reasons, contrasted directly against **The
Actual Secret Lair**'s opposite choice: stretched upward
(`"1.0,1.0,1.8"`) purely for headroom.

**Gotchas & rationale:**
- A real, verifiable formula check: pyLair's true-ellipsoid-normal
  implementation was double-checked against an independent numerical
  approximation of the same gradient before being trusted on more than one
  axis at a time — worth walking through the same verification by hand on
  one hub, so readers see *why* the naive approximation would have given a
  visibly wrong tangent-plane deflection angle.
- Elongation factors must all be strictly greater than zero — a reader
  reaching for `0` to "flatten an axis completely" gets a clear validation
  error instead of a degenerate, zero-thickness dome.

**Sample prompts:**
- "Elongate this dome upward by 1.8x on Z only. How much does that change
  the reported hub tangent-plane angles compared to the unelongated
  version?"
- "Why would using the naive position-vector-as-normal shortcut here give
  a wrong answer, specifically?"

---

### Chapter 9: Cutting a Dome From a Sphere — Truncation

**Concept(s) taught:** Slicing a sphere/ellipsoid along a chosen axis at a
cutoff fraction to produce a proper flat-bottomed dome; sequential
multi-axis truncation (X, then Y, then Z) and why each axis's cutoff is
computed against that axis's *already-trimmed* range, not the original
sphere's.

**pyLair interfaces used:** `-t/-x/-y`, `pylair.truncation.truncate()`.

**Learning objectives:**
- Truncate along a single axis and explain what the cutoff fraction
  actually measures (the portion above the cutoff is kept).
- Combine truncation on 2 or 3 axes and predict, correctly, that the second
  and third axes' cutoffs apply to already-clipped geometry, not the
  original full sphere/ellipsoid.
- Recognize and safely respond to `truncate()`'s flat-chord `ValueError`,
  including why the documented "safe" cutoffs (`0.499999`, `0.333333`)
  exist and why they're a mitigation, not a guarantee.

**The villainous example:** Continues **The Actual Secret Lair** — sliced
along Z at `0.499999` for a ground-flush floor, exactly the documented safe
default and exactly why that specific number, not a rounder one, is
recommended.

**Gotchas & rationale:**
- **The flat-chord failure, reproduced live:** a truncation cutoff landing
  exactly on a chord lying flat against the cutoff plane raises a clear,
  named `ValueError` rather than silently producing a corrupted vertex —
  demonstrated by deliberately choosing an unsafe round-number cutoff (e.g.
  `0.5` at a frequency where that lands on a vertex ring) and watching it
  fail loudly, then nudging to `0.499999` and watching it succeed.
- Axis order is fixed (X, then Y, then Z) and matters: this chapter shows,
  with real numbers, that truncating Z-then-X on the same dome as X-then-Z
  is not equivalent to swapping the order of the flags — because each
  later axis's cutoff fraction is computed against whatever range the
  earlier axis's cut already left behind.

**Sample prompts:**
- "Truncate this dome at the equator on Z only, using the documented safe
  cutoff. Then try `0.5` exactly — what happens, and why?"
- "Now truncate on X and Z together. Does the order I specify the flags in
  change the resulting shape?"

---

### Chapter 10: Faces, Diagonals, and the Case of the Un-strutted Seam

**Concept(s) taught:** Why truncation needs to correctly preserve *face*
data (not just chords) to support STL/OBJ/face-template output; the
specific case of a quad-shaped boundary panel — created when a single
original triangle's corner is clipped — being split into two triangles
along a diagonal seam, and what "correctly account for that seam" actually
requires.

**pyLair interfaces used:** `-F/--face`, `-s/--stl`, `-O/--obj`,
`-T/--face-templates`; the same `truncate()` face-clipping path as Chapter
9.

**Learning objectives:**
- Explain why a clipped panel's new corner and the strut running along that
  same cut need to land on the *identical* point, not two independently-
  rounded near-duplicates, and why reusing the same edge-intersection
  points for both accomplishes that.
- Describe what happens to a quad-shaped boundary panel in pyLair's report
  (reported as 2 triangles sharing a strutted seam, not 1 physical quad)
  and why that seam is a real, load-bearing chord rather than a rendering
  artifact.
- Recognize a flat (~180° dihedral, ~0° bevel) bevel-angle reading on that
  seam as expected and correct, not a bug — the two sub-panels it joins are
  coplanar by construction.

**The villainous example:** Continues **The Actual Secret Lair**, now
truncated on 2+ axes through the same original triangle specifically to
produce this exact case, so the diagonal seam shows up honestly in the
data rather than as a contrived example.

**Gotchas & rationale:**
- **A real, corrected piece of this project's own history, told straight:**
  this diagonal was originally a data-format-only seam — real for area/
  edge-length bookkeeping but never added to the actual chord list, so it
  got no strut length and no bevel angle in the report. A later change
  (`pylair`'s `26de45e` commit) made `_clip_face` report it as a genuine
  new chord, so it now flows through the same strut/BOM/bevel-angle
  machinery as any other edge — and this book's own outline process is
  what caught a stale blog post still describing the *old*, pre-fix
  behavior as an open problem (see Chapter 20), which is as good a
  real-world argument for keeping documentation and code in sync as this
  project has.
- Sequential multi-axis truncation composes correctly across this exact
  case too: each axis's `truncate()` call computes crossing points fresh
  from whatever geometry the previous axis's call produced, including any
  diagonal seam a previous axis's quad-split already introduced.

**Sample prompts:**
- "Truncate this dome on two axes through the same triangle. Does the
  resulting diagonal seam show up in the bill of materials as a real
  strut?"
- "What bevel angle would you expect for that seam, and why does a
  ~180° dihedral reading there mean the geometry is correct, not broken?"

---

### Chapter 11: Location, Location, Location — Designing for Hostile (and Ridiculous) Environments

**Concept(s) taught:** A practicum, not a new pyLair feature — this chapter
teaches nothing Chapters 3–10 didn't already introduce, and instead asks
readers to *apply* polyhedron choice, subdivision class, elongation, and
truncation together, deliberately, against a real environmental design
goal, the way an actual commission would arrive (not "build a Class III
dome" but "build a dome that survives down there / up there / in there").
Equally central: the hard boundary between what pyLair's geometry engine
actually validates (does the shape close correctly, are its own angles and
lengths internally consistent) and what it flatly does not (whether any of
this survives contact with real water pressure, vacuum, magma, or a
building inspector).

**pyLair interfaces used:** `design_dome` and `preview_dome` for rapid
comparison-shopping across configurations; `-p/--polyhedron`, `-c/--class`,
`-e/--elongation`, `-t/-x/-y` truncation, and `-w/--panel-density`/
`-a/--area-cost` for the material-budget side of each environment's
tradeoffs — no new flags, only new *combinations* of Chapters 3–10's own.

**Learning objectives:**
- Translate a stated environmental constraint into a concrete, specific
  choice of polyhedron, subdivision class, elongation ratios, and
  truncation axes — and articulate *why* that combination serves the stated
  goal, not just that it does.
- Use `design_dome`'s cheap summary stats (footprint, height, total strut
  length) to comparison-shop between several environment-driven
  configurations before committing to a full bill of materials for any of
  them.
- State plainly which of a design's environmental claims pyLair's geometry
  engine actually checked (internal consistency) versus which remain
  entirely the reader's own engineering research (material rating under
  the real load in question) — and explain why conflating the two is the
  single most dangerous mistake this book warns against.

**The villainous examples:** This chapter is structured as a tour, each
stop reusing the same design lens on a different environment:

- **The Under-the-Ocean Prototype** (returning from Chapters 3 and 8) —
  revisited here as the complete case: base polyhedron chosen for its
  already-flatter near-equatorial vertex ring (Chapter 3), elongation kept
  close to `1.0,1.0,1.0` for pressure symmetry (Chapter 8), no truncation
  at all if the whole point is a pressure-resistant closed shell, versus a
  small, carefully-flat-avoiding cutoff (Chapter 9) if a real airlock
  needs a flat mounting face.
- **The Orbital Panopticon** — a space-station lair with no floor to speak
  of (zero gravity makes "which way is down" a design choice, not a
  constraint), so truncation becomes optional rather than default, and the
  driving cost isn't material price but launch mass: this stop uses
  `-w/--panel-density` and total strut length, compared across several
  elongation ratios that all produce the same footprint diameter, to find
  the cheapest-to-launch silhouette rather than the prettiest one.
- **The Magma Redoubt** — a volcano lair built into (or just under) a
  caldera rim, where the interesting design decision is a large Z
  truncation cutoff that keeps most of the structure below the rim line
  with only a small dome cap exposed to the heat — and where this chapter
  is explicit that pyLair's flat, axis-aligned cutoff plane is a starting
  silhouette, not a terrain-conforming survey.
- **The Permafrost Cache** — a glacial/arctic lair using the same
  "mostly submerged, small cap exposed" logic as the Magma Redoubt but for
  the opposite reason (staying hidden under snow rather than clear of
  heat), paired with a heavier `-w` figure for insulated panel material and
  a discussion of even structural load distribution under snow weight —
  the same "geodesic domes distribute stress evenly" pitch the blog post
  opens with, applied to a specific real load direction instead of stated
  in the abstract.
- **The Ostentatious Mesa Spire** — the deliberate opposite design
  philosophy: a supervillain who *wants* to be seen, using aggressive
  vertical elongation (tall, narrow silhouette) rather than the flattened,
  low-profile shapes every other stop in this chapter reaches for — included
  specifically so readers see that "what does this environment demand"
  and "what does this villain want" are two different, sometimes opposed,
  real inputs to the same design tool.
- **A callback to the studio apartment** — a one-paragraph coda revisiting
  the blog post's own opening problem (a lair too small for the Ultimate
  Cunning Master Plan&trade;) at true-to-life scale, side by side with the
  five ambitious stops above, purely for the joke, and to underline that
  every one of pyLair's parameters — frequency, class, elongation,
  truncation — is exactly as usable for a modest home addition as for a
  volcano lair.

**Gotchas & rationale:**
- **pyLair's truncation is always an axis-aligned plane, never a
  terrain-conforming surface.** The Magma Redoubt's caldera rim, in
  reality, is not a flat plane at a fixed Z — it's an irregular, surveyed
  rock edge. `truncate()` gives a flat cut at a chosen fraction of an axis,
  full stop; reconciling that flat cut against an actual site survey is
  entirely outside pyLair's scope and stays the reader's own problem, the
  same honest boundary Chapter 1 draws around "pyLair reports geometry, not
  a validated build."
- **Elongation is one uniform `(fx, fy, fz)` triple applied to the whole
  dome — pyLair has no notion of regional or local deformation.** A design
  that wants, say, a bulging equatorial ring for a spin-gravity station (the
  Orbital Panopticon's more ambitious version) can only get pyLair's
  general-ellipsoid approximation as a starting silhouette; anything more
  locally shaped than a single ellipsoid is beyond what `elongate()` computes,
  full stop, not a missing flag waiting to be discovered.
- **`-w/--panel-density` and `-a/--area-cost` are one plain number each,
  supplied by the reader — pyLair has no per-environment materials
  database.** Figuring out what areal density and unit cost actually apply
  to an underwater-rated composite versus an orbital-rated alloy versus
  volcanic-heat-rated ceramic is real research the tool has no opinion on;
  it will multiply whatever number it's given with complete indifference to
  whether that number was researched or guessed.
- **The chapter's central, load-bearing caveat, stated as plainly as the
  rest of the book states its others:** every check this book has taught so
  far — Euler's formula, the antitile/trimesh/ezdxf oracles, the flat-chord
  `ValueError`, the truncation-artifact sliver flags — validates that
  pyLair's own geometry is *internally* correct. None of them, individually
  or together, validate that a design survives real water pressure, orbital
  debris, magma heat, or snow load. A `preview_dome` image that looks
  plausible is a sanity check on the shape, not engineering sign-off on the
  environment — and a reader who conflates the two is the one mistake this
  entire chapter exists to head off.

**Sample prompts:**
- "Compare a frequency-4 and a frequency-8 Class I icosahedral dome for The
  Under-the-Ocean Prototype. Which one produces fewer distinct panel
  types, and why might that matter for a pressure-rated build?"
- "For the Orbital Panopticon, hold the footprint diameter fixed and try
  three different elongation ratios. Which one minimizes total strut
  length — and therefore launch mass?"
- "Design a dome meant to sit mostly below a caldera rim, using a single Z
  truncation. What has pyLair actually checked for you here, and what
  hasn't it checked at all before I try to fit this into an actual
  volcano?"

---

## Part IV — The Bill of Materials

### Chapter 12: Hub Angles — Tangent Deflection and Spoke Angles

**Concept(s) taught:** The two angle types pyLair reports for every hub —
tangent-plane deflection (how far a connector bends inward to receive a
given strut) and spoke angle (how far around the hub each strut sits
relative to a chosen reference strut) — as together sufficient to fabricate
every joint in the structure.

**pyLair interfaces used:** `get_bill_of_materials` /
`pylair.bill_of_materials.compute_dihedral_angles`,
`compute_spoke_angles`, `compute_hub_data`.

**Learning objectives:**
- Interpret a tangent-plane deflection angle and a spoke angle for a real
  hub, and explain what physical cut or bend each one describes.
- Explain why these angle calculations must use the *true* ellipsoid
  surface normal from Chapter 8, not the sphere's simpler radial one, once
  any elongation is in play.
- Recognize that these two angle types, taken together, are what actually
  makes the bill of materials buildable — not just a strut-length list.

**The villainous example:** Continues **The Actual Secret Lair**, now
elongated *and* truncated (Chapters 8–10 combined), specifically so its hub
angles reflect the true ellipsoid normal, not the simpler sphere case.

**Gotchas & rationale:**
- A hub's spoke angles are relative to an arbitrarily *chosen* reference
  strut, not an absolute compass direction — two hubs with "the same"
  physical shape can report different raw spoke-angle numbers depending
  purely on which connecting strut pyLair happened to pick as the
  reference, which matters when comparing hubs by eye rather than by the
  hub-template clustering in Chapter 15.

**Sample prompts:**
- "For one hub on this dome, report both the tangent-plane deflection
  angles and the spoke angles for every strut meeting there."
- "This dome is elongated. Show me how much the reported hub angles would
  differ if it were a plain sphere instead."

---

### Chapter 13: Counting Struts — Clustering, Rounding, and the Merge Tradeoff

**Concept(s) taught:** Why chords are grouped into bill-of-materials rows
by *clustering* their lengths rather than independently rounding each one;
`-b/--bom-rounding` as a single setting that controls two different things
at once (display precision and merge granularity) and why that dual role
is a deliberate, if slightly surprising, design choice.

**pyLair interfaces used:** `-b/--bom-rounding`,
`pylair.bill_of_materials` chord-clustering logic.

**Learning objectives:**
- Explain why independently rounding each chord length risks splitting one
  true strut length into multiple report rows due to floating-point noise.
- Predict what a coarser `-b` value does (intentionally merges strut
  lengths that are close but not identical) and when that's actually
  useful (fabrication tools that can't distinguish sub-millimeter
  differences) versus dangerous (merging lengths that were meant to be
  different).
- Choose an appropriate `-b` for a given fabrication tolerance and justify
  the choice.

**The villainous example:** Continues **The Actual Secret Lair** at a high
enough frequency that its strut-length list is long enough for merge
granularity to actually matter, contrasted against a deliberately
lowered `-b` to show real strut lengths merging that shouldn't have.

**Gotchas & rationale:**
- The documented default (`-b 9`) stays exact — no unintended merging — at
  any practical dome frequency; this chapter demonstrates *why* by
  deliberately lowering `-b` on the same dome and watching genuinely
  distinct strut lengths collapse into one row, then recommends checking
  the DXF/report before cutting material to a merged length whenever `-b`
  is lowered deliberately.

**Sample prompts:**
- "Generate the bill of materials at the default rounding, then again at
  `-b 2`. Do any distinct strut lengths get merged together at the coarser
  setting?"
- "Given my laser cutter can't reliably distinguish lengths under 0.5mm
  apart, what `-b` value should I actually use?"

---

### Chapter 14: Skinning the Dome — Panel Shapes and the Chirality Trap

**Concept(s) taught:** Grouping triangular panels by their 3 edge lengths
(SSS) the same way struts are grouped by length; the specific ambiguity
this creates — two panels with identical edge lengths can still be mirror
images of each other, not true duplicates — and why that matters for
directional materials.

**pyLair interfaces used:** `pylair.bill_of_materials.group_face_types`,
`_face_type_signature`, `_face_chirality_key`.

**Learning objectives:**
- Group a dome's faces into shape "types" by edge length and read the
  reported panel counts per type.
- Explain why SSS grouping alone can't distinguish a triangle from its
  mirror image, and check a group's `chiral` flag and orientation
  breakdown before ordering directional material.
- Recognize that this is a *structurally common* case, not a rare
  edge case exclusive to Class III's inherently chiral construction — it
  shows up on ordinary Class I domes too, once elongation or truncation is
  in play.

**The villainous example:** Continues **The Actual Secret Lair** — its
panel report is checked specifically for mirror-image pairs, framed as "you
were about to order wood-grain paneling; here's what would have gone wrong
without this check."

**Gotchas & rationale:**
- A worked, real example where two panels report identical edge-length
  triples but opposite orientation — visually obvious once flagged, easy to
  miss in a raw length-sorted table without the `chiral` flag doing the
  work.
- A DXF cutting template still only needs one file per shape group, not per
  orientation, since a physical template can always be flipped over on the
  material — the chirality flag is about *awareness*, not about needing
  twice as many templates.

**Sample prompts:**
- "Group this dome's panels by shape. Are any of the groups flagged as
  chiral, and what does that mean for a one-sided material?"
- "If I'm using plain plywood with no grain direction, does the chirality
  flag actually matter for my build?"

---

### Chapter 15: Cutting Templates — Hubs, Panels, and a Clustering-Tolerance Gotcha

**Concept(s) taught:** Rotation-invariant shape clustering for hub
connectors (`-H`) and panels (`-T`) — grouping by a genuine geometric
signature (valence and the cyclic pattern of angular gaps, or edge lengths)
rather than by symmetry-group membership — so the reader gets one DXF
template per truly distinct shape, not one per hub/panel instance.

**pyLair interfaces used:** `-H/--hub-templates`, `-T/--face-templates`,
`pylair.bill_of_materials.group_hub_types`, `_hub_type_signature`.

**Learning objectives:**
- Generate hub and panel cutting templates for a real dome and interpret
  the resulting template count as "genuinely distinct shapes," not "total
  hubs/panels."
- Explain what a rotation-invariant shape signature actually compares (the
  cyclic pattern of angular gaps and tangential angles around a hub) and
  why "same shape, different rotation" correctly collapses to one
  template.
- Recognize the specific floating-point noise floor this clustering has to
  tolerate, and why the tolerance is tuned where it is.

**The villainous example:** Continues **The Actual Secret Lair**, generating
its full set of hub and panel templates as the payoff for four chapters of
geometry work.

**Gotchas & rationale:**
- **A real, empirically-tuned number, explained rather than just stated:**
  hub clustering uses 3 decimal places on angle values because the
  geometry pipeline's own floating-point noise was observed to reach the
  6th decimal place on otherwise-identical hubs — a precision of 6
  correctly-tighter-sounding decimal places actually *failed* to merge
  them, silently doubling the reported template count. A reader working at
  a much higher frequency than has been tested (up to 16) and seeing a
  suspiciously large template count is told, explicitly, to suspect this
  noise floor first.
- Panel templates cover both orientations of a shape in one file (Chapter
  13's chirality point, paid off here concretely) — `-T` writes one file
  per shape group, never per orientation.

**Sample prompts:**
- "Generate hub connector templates for this dome. How many genuinely
  distinct hub shapes are there, versus the total number of hubs?"
- "If that template count looks suspiciously high for how symmetric this
  dome should be, what's the first thing you'd check?"

---

### Chapter 16: Spotting the Slivers — Truncation-Artifact Chords and Panels

**Concept(s) taught:** Why a truncation cutoff landing extremely close to
(but not exactly on) an existing vertex ring produces mathematically valid
but practically useless slivers — a chord shortened to near-zero length, or
a panel clipped to a near-zero-area triangle — and why pyLair flags rather
than drops them.

**pyLair interfaces used:** the `Possible truncation-artifact
chords`/`panels` sections of the `get_bill_of_materials` report.

**Learning objectives:**
- Recognize a truncation-artifact sliver in a bill-of-materials report and
  distinguish it from a genuine short strut/small panel.
- Explain why the "safe" cutoffs from Chapter 9 (`0.499999`, `0.333333`)
  reduce but don't eliminate this risk, and why a barely-different cutoff
  (`0.4999999` vs. the documented `0.499999`) can flip a design from safely
  clear of a vertex ring to practically on top of it.
- Justify the specific flagging threshold (anything under 0.1% of the
  dome's largest strut length) as chosen because legitimate strut classes
  in a real subdivision essentially never differ by more than about an
  order of magnitude from each other.

**The villainous example:** Continues **The Actual Secret Lair**, this time
deliberately truncated at an unsafe near-vertex-ring cutoff to provoke real
sliver artifacts on purpose, then re-cut at the documented safe value for
comparison.

**Gotchas & rationale:**
- Nothing crashes when a sliver appears — the geometry is mathematically
  fine, just absurdly small — which is exactly why the flagging exists:
  a builder shouldn't have to eyeball a hundred-row JSON report looking for
  the one entry that's secretly a rounding artifact.
- This flagging is a genuinely different safety net than the flat-chord
  `ValueError` from Chapter 9 — that one refuses outright on an *exact*
  degenerate case; this one surfaces a *near*-degenerate case that's still
  technically valid, because refusing outright there would reject a lot of
  perfectly fine designs along with the occasional real problem.

**Sample prompts:**
- "Truncate this dome at a cutoff suspiciously close to a vertex ring. Does
  the report flag any artifact chords or panels?"
- "Now re-cut at the documented safe cutoff instead. Did the flagged list
  shrink, and did it disappear entirely?"

---

## Part V — Output, Interfaces, and Agentic Use

### Chapter 17: Getting It Out the Door — DXF, VRML, STL, OBJ

**Concept(s) taught:** pyLair's export formats and what each is actually
for — DXF for CAD import, VRML for 3D display, STL/OBJ for 3D printing —
and how face-aware truncation (Part III) is the prerequisite that makes the
face-dependent formats (`-F`, `-s`, `-O`) work correctly on a truncated
dome at all.

**pyLair interfaces used:** default DXF/VRML output, `-F/--face`,
`-s/--stl`, `-O/--obj`, `-P/--preview`,
`pylair.output.OutputDXF/OutputFaceVRML/OutputSTL/OutputOBJ`.

**Learning objectives:**
- Choose the right export format(s) for a given downstream use (CAD
  import, quick visual sanity check, 3D-printed scale model).
- Explain why `-F/--face` skips DXF entirely in favor of face-inclusive
  VRML, and plan a workflow that gets both a wireframe DXF *and* face-based
  files from the same design.
- Generate a preview PNG (`-P`) as a fast sanity check before committing to
  a full multi-format export.

**The villainous example:** **The Actual Secret Lair**'s full export — the
payoff of Parts II–IV, written out in every format at once.

**Gotchas & rationale:**
- `-F`, `-s`, `-O`, `-T`, `-a`, `-w` all require face data, and — thanks to
  Chapter 10's fix — now correctly work with truncation on any combination
  of axes, not just an untruncated sphere; this chapter demonstrates the
  full combination (multi-axis-truncated, face-exported, STL'd) as proof.
- STL/OBJ export is for the dome's *surface*, not its strut skeleton — a
  reader expecting a 3D-printable strut lattice from `-s`/`-O` directly
  will instead get a printable model of the panel skin, which is correct
  but worth stating plainly before anyone wastes filament.

**Sample prompts:**
- "Export this dome as DXF, VRML with face data, STL, and OBJ all at once.
  Which files actually require the face data to have been preserved
  correctly through truncation?"
- "Generate just a quick preview PNG first — does the shape look right
  before I commit to a full export?"

---

### Chapter 18: Talking to pyLair — The Four MCP Tools in Practice

**Concept(s) taught:** `design_dome`, `preview_dome`, `get_bill_of_materials`,
and `export_dome` as four genuinely different questions about the same
design — cheap sanity check, visual check, cost/build check, and
commitment — built for the iterate-then-commit workflow the blog post
describes as "try a shape, look at it, check what it costs, adjust, and
only export once it's actually right."

**pyLair interfaces used:** all four MCP tools, each sharing the one
geometry parameter schema described in `README.md`.

**Learning objectives:**
- Use `design_dome` to cheaply try several configurations (frequency, class,
  truncation) before ever writing a file.
- Use `preview_dome` to see a wireframe inline, and `get_bill_of_materials`
  to interrogate strut counts and connector angles, before deciding a
  design is worth building.
- Only call `export_dome` once satisfied, and explain why that ordering —
  not any technical restriction — is the whole point of having four tools
  instead of one.

**The villainous example:** **The Actual Secret Lair**'s full iterate-then-
commit design session, narrated end to end: several `design_dome` calls
trying different frequency/truncation combinations, one `preview_dome`
check, one `get_bill_of_materials` cost interrogation, and finally one
`export_dome` call — the same shape Chapter 17 exported, but shown here as
a *process*, not a single command.

**Gotchas & rationale:**
- All four tools enforce the exact same validation rules as the CLI,
  because a single geometry engine (`pylair/api.py`) underlies both
  interfaces — demonstrated by triggering an invalid parameter combination
  through `design_dome` and getting the identical error `export_dome` (or
  the CLI) would give.
- `design_dome` and `get_bill_of_materials` write no files at all — a
  reader worried about cluttering a directory while iterating on ten
  candidate frequencies can iterate freely through those two tools alone.

**Sample prompts:**
- "Try three different frequencies for this dome using `design_dome` only
  — don't write any files yet. Which one gives a strut count closest to my
  budget?"
- "Now preview the one you picked, then check its bill of materials before
  we export anything for real."

---

### Chapter 19: Prompting pyLair Like You Mean It

**Concept(s) taught:** Practical prompt craft for pyLair's four-tool
agentic interface: being specific about which tool's answer you actually
want, carrying forward settled findings (a chosen frequency, a validated
cutoff) instead of re-deriving them, and recognizing when a tool's own
output is telling you something the prompt didn't ask for.

**pyLair interfaces used:** A deliberate mixed review across all four MCP
tools plus the CLI.

**Learning objectives:**
- Write prompts that carry an earlier chapter's findings (a safe truncation
  cutoff, a chosen subdivision class) into a later request, rather than
  starting from scratch.
- Recognize the difference between a prompt that under-specifies (leading
  to arbitrary defaults) and one that over-specifies (defeating the point
  of asking an agent to reason at all).
- Distinguish which of pyLair's four tools actually answers a given
  real-world question, rather than guessing.

**The villainous example:** A "clinic" chapter, following the Omen book's
own Chapter 20 pattern directly — three real submitted prompts, each with a
real flaw, rewritten and explained, reusing dome designs this book has
already built rather than introducing a new one.

**Gotchas & rationale:**
- **Prompt one, too vague to carry anything forward:** *"Design me a
  dome."* — with no radius, frequency, class, or intended use specified,
  an agent has no reason to route around pyLair's plain numeric defaults
  (`icosahedron`, Class I, frequency 4, radius 1.0) toward anything
  resembling an actual secret lair. **Rewritten:** "Using the `(m,n)=(4,1)`
  Class III configuration from Chapter 6, at the elongation and truncation
  from Chapters 8–9, run `design_dome` and confirm the vertex/face counts
  still match what we found there before we export." What changed: it
  names the actual settled parameters instead of letting the agent
  rediscover — or silently default past — them.
- **Prompt two, so specific it leaves nothing to reason about:** hard-coding
  every CLI flag from a previous chapter's exact winning configuration and
  asking only for one number back, foreclosing the agent from noticing that
  a design goal has since changed (a taller elongation factor, say) that
  would make the old cutoff unsafe again per Chapter 9's flat-chord
  warning. **Rewritten:** keep only the constraint that's actually settled
  (the subdivision class and `(m,n)` pair), and leave cutoff selection
  open for the agent to re-derive safely against the *current* elongation.
- **Prompt three, right question, wrong tool:** *"Is this dome design good
  enough to build?"* maps onto at least three different real questions —
  a **`design_dome`** sanity check (do the counts and strut total fit a
  budget), a **`get_bill_of_materials`** audit (does the flagged-artifact
  list contain anything real, per Chapter 16), or a **`preview_dome`**
  visual check (does it look like what was intended) — each answered by a
  different tool, and a plausible-sounding answer to the wrong one of the
  three is worse than an agent that asks which was meant.

**Sample prompts:**
- (This chapter's exercises *are* prompt-rewriting exercises, matching the
  Omen book's own Chapter 20 structure — readers draft, then critique,
  their own.)

---

## Part VI — Keeping the Lair's Paperwork Honest

### Chapter 20: When the Docs Lie — Catching Documentation Drift with a Knowledge Graph

**Concept(s) taught:** README, blog post, and method-walkthrough
documentation as independent artifacts that can silently drift out of sync
with each other and with the code — and a knowledge-graph tool
(`graphify`) as a concrete, general technique for catching that drift by
surfacing an AMBIGUOUS edge between two contradictory claims, rather than
relying on a human to notice by chance.

**pyLair interfaces used:** None of pyLair's own — this chapter is about
the surrounding agentic tooling (`/graphify`), applied to pyLair's own
`README.md`/`blog-posts/` as the worked example.

**Learning objectives:**
- Explain what an EXTRACTED/INFERRED/AMBIGUOUS confidence label means on a
  knowledge-graph edge, and why AMBIGUOUS is a feature (flag for review),
  not a failure to classify.
- Trace a flagged AMBIGUOUS edge back to its two source documents and
  determine which one is actually current, using git history as the
  tiebreaker.
- Recognize this as a general pattern applicable to any project with more
  than one place the same fact gets documented, not a pyLair-specific
  trick.

**The villainous example:** A real, previously-unresolved documentation bug
in this exact repository: the blog post's own "Next Steps" section
described the diagonal-seam chord from Chapter 10 as still unstrutted, an
open problem — while `README.md`'s caveats section, updated by a later
commit (`26de45e`, "Strut the diagonal seam left over from corner-clipped
panels"), already documented it as fixed, shipped behavior. The two
documents flatly disagreed.

**Gotchas & rationale:**
- This isn't a hypothetical for the outline — it's the real graph output
  from running `/graphify` on this repository, which surfaced exactly this
  contradiction as an AMBIGUOUS `references` edge between the two nodes,
  with a specific confidence score reflecting genuine uncertainty about
  which side was current.
- The resolution required git history, not just re-reading the two
  documents more carefully: `26de45e`'s commit date, cross-referenced
  against when the blog post file was last substantively touched (as
  opposed to a later project-rename commit that recreated it verbatim,
  carrying the stale text forward unnoticed), was what actually settled
  which document was telling the truth.

**Sample prompts:**
- "Run a knowledge-graph pass over this repository's docs. Does it flag any
  contradictions between the README and the blog post?"
- "For any AMBIGUOUS edge it finds, check git history for both source
  files — which one is actually current?"

---

### Chapter 21: Letting the Agent Write Your CI (Carefully)

**Concept(s) taught:** An agent authoring a GitHub Actions pipeline as a
genuine test of the pipeline's own honesty — not "does the YAML parse,"
but "does it actually catch a real bug the author didn't know about yet" —
using this project's own real CI-authoring session as the worked example.

**pyLair interfaces used:** `pip install -e ".[test,mcp,verify]"` across a
Python version matrix; none of pyLair's own tools directly.

**Learning objectives:**
- Explain why testing across multiple Python versions matters even for a
  project with modest runtime dependencies, using a real example where it
  wasn't obvious in advance.
- Diagnose a CI failure by reading the actual installer error rather than
  guessing, and distinguish "my code is wrong" from "my dependency
  declaration is wrong."
- Recognize verifying a CI fix *locally*, in a clean environment, before
  re-pushing, as the same discipline Part II's geometry oracle checks
  teach — don't trust a fix you haven't independently confirmed.

**The villainous example:** No dome this time — the CI pipeline itself,
treated as the exercise, using two real, documented bugs this exact
project's CI run caught on its very first execution.

**Gotchas & rationale:**
- **Bug one, real and reproducible:** the `verify` extra's own declared
  dependencies (`trimesh`, `ezdxf`) were incomplete — `trimesh`'s
  `slice_mesh_plane` (used by `test_geometry_oracle.py`'s truncation
  cross-checks) needs `shapely` as a transitive dependency that `trimesh`
  itself doesn't pull in as a hard requirement, so `pip install -e
  ".[verify]"` was silently missing a piece and 9 real tests failed with
  `ModuleNotFoundError` until `shapely` was added to `pyproject.toml`'s
  `verify` extra explicitly.
- **Bug two, caught by the matrix itself:** the `mcp` package has no
  published release supporting Python 3.9 — every version on PyPI requires
  3.10+ — so a naive "install every extra on every supported Python
  version" CI matrix failed outright on 3.9 with a real, unambiguous
  installer error, fixed by scoping the `mcp` extra to Python 3.10+ in the
  matrix while confirming `test`/`verify` still install cleanly on 3.9
  first.
- The general lesson, stated plainly: an agent-authored CI pipeline that
  goes green on the *first* try, on a project that had never had one
  before, is more likely to indicate an undertested pipeline than a
  bug-free one — real coverage tends to find something.

**Sample prompts:**
- "Set up a CI matrix testing every supported Python version with every
  optional extra installed. If any leg fails, show me the actual installer
  error, not just 'it failed.'"
- "Before trusting this fix, reproduce the original failure locally in a
  clean environment first — does it actually fail the way CI said it
  would?"

---

### Chapter 22: When to Trust the Agent, and When Not To

**Concept(s) taught:** A retrospective, cross-cutting look at every
deliberately rule-based or independently-verified decision point this book
has encountered — golden-value formulas, the `antitile`/`trimesh`/`ezdxf`
oracles, the flat-chord `ValueError`, the CI matrix's own real failures —
generalized into a checklist readers can apply to their *own* geometry or
agentic tools, not just pyLair.

**pyLair interfaces used:** None new — a synthesis chapter.

**Learning objectives:**
- Articulate a general rule for "when does a geometric claim need
  independent verification, not just internal self-consistency" and test
  it against several examples from the book (Class II's Euler-formula
  catch, Class III's antitile cross-check, the panel oracle's trimesh/ezdxf
  round-trip).
- Recognize the pattern in pyLair's own repeated use of *external,
  independently-implemented* oracles — never validating its own math only
  against itself — as evidence for that rule, not just this project's
  arbitrary house style.

**The villainous example:** No new dome — a structured retrospective across
every design used so far, framed as the after-action review our heroine
holds after any operation.

**Gotchas & rationale:**
- The chapter's central thesis, stated directly: a check that only compares
  a result against its own internal assumptions (Euler's formula on a
  construction that itself defines the vertex/edge/face relationship) can
  catch a *count* bug but not a *shape* bug — Class III's own real history
  (Chapter 6) is the sharpest illustration in the whole book, because it
  passed exactly that kind of internal check while still being wrong, and
  only an independent, differently-implemented library caught it.
- Applied one level up: this same principle is why the book itself insists
  every gotcha be traceable to a real commit, a real test, or a real CI
  log — an outline that only checks its own internal consistency has
  exactly the same blind spot Class III's first implementation did.

**Sample prompts:**
- "Looking back at everything this book covered, list every point where
  pyLair checked a result against an independent, differently-implemented
  source rather than just its own internal consistency. What do they have
  in common?"

---

### Chapter 23: Conclusion

**Concept(s) taught:** A wrap-up, not a new concept — consolidates the
book's arc from "pick a polyhedron" through "should you even trust this
number" in light of everything the reader now knows.

**Content:**
- A full recap of pyLair's pipeline (polyhedron → subdivision → projection
  → shaping → bill of materials → export → agentic interface) in light of
  the real gotchas each stage turned out to hide.
- A pointer back to the companion blog post
  (`blog-posts/introducing-pylair.md`) for readers who want the same
  material in a shorter, funnier form, plus a pointer to `AGENTS.md` for
  readers who want to go build on pyLair directly.
- A closing status update on the running examples: the Actual Secret Lair
  is designed, verified, and exported; the Under-the-Ocean Prototype
  remains, honestly, just a prototype — a secret lab's actual construction
  is (of course) kept secret, exactly as the blog post promised.
- A short "where pyLair itself goes next" section, pulled honestly from the
  blog post's own real, currently-open "Next Steps" items (proactive
  truncation-risk warnings before export, an optional boundary cap for
  fully enclosed structures, door-frame design assistance) rather than
  invented future features — noting, honestly, that the diagonal-seam item
  once on that same list is now done (Chapter 10), which is exactly the
  kind of status update Chapter 20 exists to keep honest.

**Sample prompts:**
- "Summarize everything you now know about the Actual Secret Lair's design
  across every stage of the pipeline, as if handing off to whoever
  actually builds it."

---

## Appendices

- **Appendix A — Glossary.** Every geometry and engineering term introduced
  across the book (symmetry triangle, chord, hub, frequency, triangulation
  number `T`, chirality, dihedral/bevel angle, Goldberg-Coxeter
  construction, etc.), defined in one or two sentences each, cross-referenced
  to the chapter that introduced it.
- **Appendix B — CLI and MCP Tool Reference.** Every CLI flag and every MCP
  tool used in the book, with a one-line description and the chapter(s)
  that cover it — a fast lookup companion once readers start designing
  their own domes instead of the book's examples.
- **Appendix C — Further Reading.** The real sources pyLair's own
  construction is drawn from and verified against: Kenner, H. (1976),
  *Geodesic math and how to use it*; Šiber, A. (2007), "Icosadeltahedral
  geometry of fullerenes, viruses and geodesic domes" (arXiv:0711.3527);
  [`antitile`](https://github.com/brsr/antitile); [`trimesh`](https://trimesh.org/);
  [`ezdxf`](https://ezdxf.readthedocs.io/) — plus the companion blog post
  and `README.md`'s own "Caveats and known limitations" section for
  continued reference.
