# Agentic Geodesic Lair Design for Supervillains
### Computational Geometry and Agentic AI with pyLair and pyFit
**Proposed Outline**

---

## About This Outline

This is a chapter-by-chapter proposal for the book, not the book itself — the
same kind of document as [the outline for *Agentic Time Series Forecasting
for Supervillains*](../../omen-agentic-time-series-forecasting/book/outline.md),
this series' companion volume, whose structure and conventions this outline
deliberately follows. Every chapter below uses the same template:

- **Concept(s) taught** — the geometry/engineering idea(s) at the center of the chapter.
- **pyLair/pyFit interfaces used** — the actual CLI flags, Python API calls, and/or
  MCP tools the chapter's exercises use, by name, from whichever of the two
  toolkits (or both) the chapter concerns.
- **Learning objectives** — what the reader should be able to do afterward.
- **The villainous example** — the running dome/nesting design for the chapter, and why its shape fits the lesson.
- **Images** — the figures this chapter needs, and whether each is a real
  rendered output (pyLair's `-P/--preview`, pyFit's own `-P/--preview`) or a
  purpose-drawn conceptual diagram. See "A Note on This Book's Images" below
  for how these get produced consistently.
- **Gotchas & rationale** — the specific "here's why this isn't as simple as it looks" content the book promises, grounded in real, documented behavior of pyLair and pyFit (their READMEs' caveats, their test suites, and their git history) — not invented for the outline.
- **Sample prompts** — 2–3 representative prompts in the book's prompt-based instructional style, in the same voice as Part VII's agentic-prompting chapter.

This book treats geodesic lair design as a book-length subject in its own
right — geodesic mathematics, all three subdivision classes, chirality, and
the engineering tradeoffs of elongation/truncation, taught in far more depth
than the companion blog post or `blog-posts/METHOD.md` have room for — with
the agentic tool-use (pyLair and pyFit, driven through a real MCP or OpenClaw
interface) as the vehicle for actually *doing* the geometry rather than the
book's real subject. Every teaching chapter accordingly pairs its concept
with a **villainous example** worked all the way through, in the book's
running prompt / **What Comes Back** / **What It Means** format, so the
humor stays load-bearing for the pedagogy rather than decorative.

Chapters follow the actual shape of a dome moving through pyLair's pipeline,
and then — new in this revision — the shape a *panel* takes once it leaves
that pipeline and needs to actually get cut from real sheet stock: pick a
polyhedron, subdivide it, project it onto a sphere, shape it (elongate,
truncate), account for it (bill of materials, cutting templates), export it,
then **nest** its cutting templates onto actual plywood/acrylic/aluminum
sheets with pyFit — because that's also the order in which each stage's
correctness *depends* on the one before it: you can't honestly truncate a
sphere whose projection is wrong, you can't honestly report a bevel angle
for a face whose truncation clipped it incorrectly, and you can't honestly
nest a panel shape pyLair never correctly computed in the first place.

pyLair and pyFit are, by design, two genuinely independent projects with no
code dependency on each other — pyFit reads plain DXF files, and doesn't
know or care whether pyLair (or any other CAD tool) produced them. This
book treats that independence honestly rather than pretending the two are
one integrated product: Parts II–V are pyLair-only, Part VI is pyFit's own
subject taught on its own terms (including a standalone pyFit example that
has nothing to do with domes at all), and only where the two toolkits
actually meet — a pyLair panel-template DXF file becoming a pyFit job spec's
`"dxf"` field — does the book show them working together.

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
  ground-flush footprint with room for a door, exported for real in Part V,
  and finally **nested for real** — its cutting templates laid out onto
  actual 96"×48" plywood sheets in the henchmen's fabrication bay — in Part
  VI. This is the dome the blog post's heroine is actually building, and the
  one this book's chapters slowly earn the right to actually cut material
  for.

A third, smaller example — **The Under-the-Ocean Prototype** — appears where
a chapter specifically needs a second, contrasting shape (a squashed
ellipsoid built for pressure symmetry rather than headroom, name and framing
lifted directly from the blog post's own opening joke about where a secret
laboratory really belongs), and gets a full dedicated tour alongside four
new siblings — an orbital station, a volcano lair, an arctic cache, and one
deliberately un-hidden mountain spire — in Chapter 11, once Part III has
given readers every shaping tool those examples actually use. Its panels
return once more in Part VI, specifically because they're chirality-sensitive
(a one-sided pressure coating, per Chapter 14's chirality trap) in a way the
plywood-built Actual Secret Lair's panels aren't — giving pyFit's own
`allow_mirror` flag a real, previously-established reason to matter.

---

## Front Matter

- **Title Page** — title, subtitle, "as told by our heroine," and a
  one-paragraph framing note connecting this book to
  [`blog-posts/introducing-pylair.md`](../blog-posts/introducing-pylair.md)
  and [pyFit's own introductory blog post](https://github.com/badass-data-science/pyFit-agentic-polygon-nesting/blob/main/blog-posts/introducing-pyfit.md),
  which readers are encouraged to treat as companion reading, not a
  prerequisite — the same relationship the Omen book has with its own blog
  series.
- **About the "for Supervillains" Series** — this volume *is* the
  "*Geodesic Lair Design for Supervillains*" the Omen book's own
  `about_the_series.md` already promised was coming, several NDAs later than
  planned. Notes the shared universe (same heroine, same Ultimate Cunning
  Master Plan&trade;, mojitos optional but encouraged) without requiring the
  other book as a prerequisite, and notes that this volume is itself a
  two-toolkit story — pyLair designs the dome, pyFit cuts it — the same way
  a real fabrication project is never just one piece of software.
- **How to Use This Book**
  - Who this book assumes you are: comfortable with basic 3D coordinate
    geometry (vertices, planes, angles) and command-line tools; new to
    geodesic subdivision, 2D nesting/bin-packing, and agentic tool-use
    generally.
  - The prompt-based convention used throughout: every worked example shows
    a boxed **Prompt** (what you'd actually type to your agent) followed by
    **What Comes Back** (the tool's real JSON/CLI output, trimmed for
    space) and **What It Means** (the plain-language interpretation).
  - A note that every number, error message, image, and file shown in this
    book is from a *real* `pylair`/`pylair-mcp`/`pyfit`/`pyfit-mcp` run
    against real parameters — not a hand-typed mockup — and that every
    named dome design (the Proof-of-Concept Yurt, the Actual Secret Lair,
    and the rest) and every named nesting job can be reproduced exactly by
    running the same real CLI command shown inline in the chapter that
    produced it — every such command is the literal one actually run, not
    an illustrative approximation of one.
  - Pointers to pyLair's `README.md`/`AGENTS.md` and pyFit's `README.md`/
    `AGENTS.md` (the full CLI/MCP reference, caveats lists, and each
    toolkit's own agent-facing engineering notes, including the geometry and
    nesting pipelines' historical footguns) for readers who want to go
    deeper than any one chapter.
- **A Note on This Book's Images** — this book is illustration-heavy on
  purpose: every subdivision class, every shaping operation, and every
  nesting concept gets at least one figure, because geodesic geometry and
  2D nesting are both subjects that are much easier to *see* than to read a
  paragraph about. Three sources produce every image in the book, and none
  of them are hand-drawn or AI-generated illustrations dressed up as real
  output:
  - **pyLair's own `-P/--preview` renderer** (`pylair/preview.py`) for every
    dome/sphere wireframe figure — the same equal-axis-scaled 3D wireframe
    a reader gets from their own terminal, so a figure in this book and a
    figure a reader generates themselves from the same parameters are
    pixel-for-pixel comparable in shape (not necessarily in file format).
  - **pyFit's own `-P/--preview` renderer** (`pyfit/preview.py`) for every
    sheet-layout figure — boundary plus every placed part's outline, the
    same convention pyLair's own preview uses one dimension down.
  - **A handful of purpose-built conceptual diagrams**, for the small
    number of ideas neither tool's own preview renders on its own — a bare
    symmetry-triangle grid before it's replicated across a polyhedron, a
    chiral `(m,n)`/`(n,m)` mirror-pair comparison, a no-fit-polygon (NFP)
    construction — plotted directly from the same real, computed coordinate
    data the surrounding prose is discussing (never hand-drawn freehand),
    using a consistent color palette and figure style so a conceptual
    diagram never looks like a different, less trustworthy kind of image
    than a real tool render sitting next to it on the same page. Every
    figure caption in this book names which of the three produced it.
  - No single script generates every figure in this book; each one was
    produced directly from the real tool or real data the surrounding
    prose discusses, and the exact parameters or construction are always
    shown inline rather than hidden behind a script a reader would have to
    go find and run separately.
- **A Word on AI Use** — matches the convention already established in both
  projects' own AI Use Statements: the original pyLair and pyFit
  implementations were hand-written from scratch, then extended
  feature-by-feature in collaboration with an AI coding assistant (pyLair's
  Class II/III subdivision, elongation, STL/OBJ/PNG output, face-aware
  truncation; pyFit's NFP-based nesting engine); this book's prose follows
  the same pattern — drafted collaboratively, checked line-by-line against
  the actual codebases, test suites, and git history of both projects, not
  invented.
- **Dedication** — short, in the same register as the Omen book's own.

---

## Part I — Meet Your New Design Engineers

### Chapter 1: Introducing pyLair, pyFit, and the Agentic Interface

**Concept(s) taught:** What "agentic AI" actually means in a design/fabrication
context, as distinct from "an AI that writes CAD code for you"; what pyLair
and pyFit each actually compute (pyLair: vertices, chords, and faces of a
geodesic dome or sphere; pyFit: where each of a set of 2D shapes should sit
on a sheet of material) and what neither does (neither is a structural
engineering tool, and pyFit has no opinion on whether a shape it nests
*should* exist — it just nests whatever it's given); the same "agentic AI"
distinction the Omen book opens with, applied to CAD and fabrication instead
of statistics — an agent driving typed tools and reasoning between calls, as
opposed to an LLM free-handing `numpy` trigonometry or packing logic from
scratch and hoping it's right; why every single tool result in this book
comes back as **JSON**, and what JSON actually is.

**pyLair/pyFit interfaces used:** None yet — conceptual scaffolding.
Previews `design_dome`'s and `design_nest`'s output shapes as a teaser
without explaining them.

**Learning objectives:**
- Describe, at a high level, what a geodesic subdivision *is* (a polyhedron
  face divided into a triangular grid, then projected onto a sphere) and
  why it distributes structural stress more evenly than a dome with large
  flat panels.
- Describe, at a high level, what 2D nesting/bin-packing *is* (arranging a
  set of shapes onto rectangular stock to minimize wasted material) and why
  it's a genuinely different, and genuinely harder (NP-hard), problem than
  the geometry pyLair solves — knowing where a panel goes on a dome tells
  you nothing about where it should sit on a sheet of plywood next to a
  dozen others.
- Distinguish the things pyLair hands back (a shape, export files, a bill
  of materials, cutting templates) and the things pyFit hands back (a
  per-sheet placement report and DXF files) from the physical build itself,
  which remains entirely the reader's problem in both cases.
- Explain why "just ask the AI to design a dome" or "just ask the AI to
  figure out how to lay these out on plywood" without a real geometry/nesting
  engine underneath fails silently: an LLM asked to compute hub angles or
  pack irregular triangles freehand will produce *plausible-looking* numbers
  or layouts with no guarantee they're correct.
- Read a JSON object confidently: objects (`{ }`) as labeled bags of
  values, arrays (`[ ]`) as ordered lists, and the four value types (string,
  number, boolean, `null`) — and explain why `null` means "genuinely no
  value," not "zero" or "unknown."
- Explain why an agent that needs to *act* on a tool's result (compare a
  number against a threshold, pass a placement into the next call) needs
  that result in a fixed, machine-readable shape rather than a prose
  sentence — and why a sentence that reads fine to a human is exactly the
  failure mode an agentic tool's JSON output exists to close off.

**The villainous example:** A cold open, borrowed directly from the blog
post — our heroine's secret laboratory has outgrown her studio apartment,
and whatever she builds next needs to (a) look cool, (b) handle pressure
gradients gracefully, because a proper secret lab belongs deep underwater or
in circumpolar orbit, not in an unassuming San Diego neighborhood, and (c) —
new to this telling — actually get *built*, which means someone (a henchman,
almost certainly, and definitely not our heroine personally) has to figure
out how to cut every one of that dome's panels out of actual sheet material
without wasting half of it. This is the two-part problem the book solves,
not yet with geometry or nesting — just a promise that Chapter 3 picks the
design half back up, and Part VI picks the cutting half up once there's
something real to cut.

**Images:**
- A single finished-dome photo/render as the chapter's cold-open image
  (`blog-posts/edited_truncated.png` or `blog-posts/CAD_dome.jpg`, both real
  pyLair output already in the repo) — the "this is what we're building
  toward" teaser.
- A single nested-sheet render as the chapter's second teaser
  (`pyFit`'s own `blog-posts/images/nest_sheet1_pylair_triangles.png`,
  already real pyFit output nesting actual pyLair triangles) — "and this is
  what it takes to actually cut it out."
- A small side-by-side conceptual diagram (purpose-drawn, per the image note
  above): a prose sentence describing a mean and confidence interval next to
  the equivalent JSON object, visually underlining the "an agent has to
  re-parse the sentence; it just reads the JSON field" point.

**Gotchas & rationale:**
- Why hand-rolled dome math is dangerous specifically at the *hub*, not the
  *chord*: a chord length is forgiving of small errors (the strut is just
  slightly the wrong length), but a wrong hub angle compounds — every strut
  meeting at that hub inherits the error, and the dome may not physically
  close. Nesting has its own version of this danger at the *no-fit-polygon*,
  not the individual shape: a single wrong NFP computation doesn't just
  misplace one part, it can silently validate an overlapping placement as
  legal.
- The core tension this book keeps returning to: both toolkits deliberately
  keep their core engines rule-based and shared (`pylair/api.py`, used
  identically by pyLair's CLI and every MCP tool; `pyfit/api.py`, used
  identically by pyFit's CLI and every MCP tool) rather than letting an
  agent freelance the math per request — the same "deterministic gates
  around agentic judgment" idea the Omen book centers, applied here to
  geometric and combinatorial correctness instead of a deploy decision.
- A prose answer can silently drift between two phrasings of the same fact
  ("about 244, give or take five" vs. "roughly 240 to 249") in a way an
  agent parsing it back out has no reliable way to detect; a JSON field
  spelled `"mean_ci_lower"` cannot drift the same way without the number
  itself changing.

**Sample prompts:**
- "Explain, in your own words, why pyLair computes the geometry itself
  instead of just asking you to describe what a geodesic dome would look
  like — and why pyFit's nesting works the same way."
- "What's the difference between asking for a dome's vertex/edge/face
  counts and asking for its full bill of materials? And what's the
  difference between that bill of materials and a nesting job's placement
  report?"

---

### Chapter 2: Installing pyLair and pyFit (OpenClaw, Claude Code, Hermes, Claude Desktop, and Any MCP Framework)

**Concept(s) taught:** Python packaging extras as an install-time choice
(`[test]`, `[mcp]`, `[verify]` for pyLair; `[test]`, `[mcp]`, `[lint]` for
pyFit) rather than one monolithic dependency list; how an MCP (Model Context
Protocol) server actually connects to an agentic client — stdio transport,
tool discovery, the console-script pattern — as one underlying contract that
looks different only in configuration-file shape across OpenClaw, Claude
Code, Hermes, Claude Desktop, and any other MCP-speaking framework; how
OpenClaw's *skill* mechanism (a different, CLI-wrapping integration path,
used by both toolkits alongside their MCP servers) fits into the same
picture without being confused for MCP itself.

**pyLair/pyFit interfaces used:** `pip install -e ".[mcp]"` for both
projects, the `pylair-mcp` and `pyfit-mcp` console commands; pyLair's
`SKILL.md` (repo root) and pyFit's `skills/pyfit/SKILL.md` (nested — a real,
documented difference between the two, not a typo) plus each project's
`openclaw.config.snippet.jsonc`; the chapter ends with a real smoke test
calling `design_dome` and `design_nest` once each, successfully, as proof of
life for both.

**Learning objectives:**
- Install pyLair and pyFit (`pip install -e .` for each CLI alone, `.[mcp]`
  to add each agentic interface) into a clean environment.
- Register both `pylair-mcp` and `pyfit-mcp` with at least one MCP-speaking
  client, understanding that "register an MCP server" always reduces to the
  same three things regardless of platform: know the launch command, launch
  it over stdio, let the client discover its tools.
- Install both projects' OpenClaw skills correctly despite their different
  directory conventions — pyLair's `SKILL.md` sits at the repo root; pyFit's
  sits at `skills/pyfit/SKILL.md`, because OpenClaw discovers skills by
  scanning configured roots for `<root>/<skill-name>/SKILL.md` and pyFit's
  own `openclaw.config.snippet.jsonc` adds its `skills/` directory to
  `skills.load.extraDirs` accordingly.
- Confirm installation success via live tool calls to both servers, not
  just "the install command didn't error."
- Know which extra to reach for later in each project: pyLair's `[verify]`
  for the independent geometry oracle used in Part IV (and, as this book's
  own real history proves in an earlier draft, worth double-checking on
  whatever Python version you're actually running); pyFit's `[lint]` is a
  contributor concern this book doesn't otherwise use.

**The villainous example:** **The Proof-of-Concept Yurt** — `pylair -o
poc-yurt -f 2 -r 1.0`, a tiny, unremarkable Class I dome, deliberately
too small and plain to be anyone's actual secret lair, paired with a
matching **Proof-of-Concept Nesting Job** — a `pyfit` job spec nesting
nothing more ambitious than six identical unit squares onto a 3×2 sheet
(the same hand-checkable, README-documented "tiles perfectly" case used
later in the actual chapter), deliberately too trivial to represent real
fabrication work.
The point of both isn't the shape or the layout; it's proving the wiring
works, on both toolkits, before anything ambitious is attempted.

**Images:**
- A single conceptual diagram (purpose-drawn) of the three-step MCP
  contract — client → launch command over stdio → tool discovery — labeled
  generically so it visibly applies to every platform named in the chapter,
  not just one.
- A real preview render of the Proof-of-Concept Yurt (`pylair -P`) and a
  real preview render of the Proof-of-Concept Nesting Job's single sheet
  (`pyfit -P`), side by side as the chapter's "proof of life, and here's
  what it looked like" pair.

**Gotchas & rationale:**
- The CLI and the MCP server share one validation engine in each project
  (`pylair/api.py:validate_geometry_params`; `pyfit/api.py:run_nest`/
  `load_part`) — demonstrated live by triggering the same error (an invalid
  Class II odd frequency for pyLair; a malformed job spec for pyFit)
  through both interfaces of each project and getting the identical message
  back, proof this isn't two implementations that happen to agree today.
- A live, narrated example of a real class of MCP install failure, in the
  same voice as the Omen book's own Chapter 2: a subprocess launched by a
  bare command name can fail to find `pylair-mcp` or `pyfit-mcp` if it
  doesn't inherit the parent process's activated-environment `PATH` — fixed
  by pointing the client config at each console script's absolute path
  instead. Shown once, explicitly, as applying identically to both servers,
  rather than narrated twice.
- Neither `pylair-mcp` nor `pyfit-mcp` has a published release supporting
  Python 3.9 (both projects pin `mcp<2.0` for the same reason: `mcp` 2.0.0
  removed `mcp.server.fastmcp` entirely, which both servers' `FastMCP`/
  `Image` imports depend on) — worth knowing before setting up a CI matrix
  or an older interpreter and wondering why the `mcp` extra alone refuses to
  install.
- OpenClaw's two skills for these projects are genuinely *not* symmetric in
  file layout, and a reader who copies pyLair's flat `SKILL.md`-at-root
  pattern for pyFit will find nothing gets discovered: pyFit's skill lives
  nested at `skills/pyfit/SKILL.md` specifically so its
  `openclaw.config.snippet.jsonc` can point `skills.load.extraDirs` at a
  whole `skills/` directory rather than the repo root itself — a small,
  real difference worth checking explicitly rather than assuming the two
  projects mirror each other exactly.
- Neither skill needs an API key or environment variable — both gate purely
  on their respective CLI binary (`pylair`, `pyfit`) being on `PATH` via
  each `SKILL.md`'s `metadata.openclaw.requires.bins`, so "the skill didn't
  show up" almost always means "the CLI itself isn't installed or isn't on
  `PATH` yet," not a configuration problem in the skill file itself.

**Sample prompts:**
- "Confirm both the pyLair and pyFit MCP servers are running and list every
  tool each one exposes."
- "Run `design_dome` on the smallest, cheapest configuration you can, then
  run `design_nest` on six placeholder squares, just to prove both
  connections work end to end."

---

## Part II — From Polyhedron to Sphere

### Chapter 3: Picking a Polyhedron

**Concept(s) taught:** Why geodesic subdivision starts from an existing
near-spherical, symmetric solid rather than an arbitrary shape; the
icosahedron (20 faces, 12 vertices) versus the octahedron (8 faces, 6
vertices) as pyLair's two starting points, and how that choice ripples
through every later vertex/face count.

**pyLair/pyFit interfaces used:** `-p/--polyhedron`, `pylair.polyhedral.Icosahedron`
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

**Images:**
- A side-by-side pair (real `-P/--preview` renders): a bare icosahedron and
  a bare octahedron at the same scale, so the vertex/face-count contrast is
  visible, not just tabulated.

**Gotchas & rationale:**
- The two base polyhedra are not interchangeable at "the same" frequency —
  an octahedron-based Class I dome at frequency `f` has `8f²` faces where
  an icosahedron-based one has `20f²`; a reader who swaps polyhedron
  without adjusting frequency to compensate will get a very differently
  detailed structure than they expected.
- pyLair's internal indexing is 0-indexed throughout — worth mentioning
  here as a "boring but real" note, since an earlier version of the
  codebase numbered vertices 1-indexed and subtracted 1 at every point of
  use, a real historical footgun documented in `AGENTS.md`'s standing
  guidance to modernize such holdovers on sight rather than leave them be.

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

**pyLair/pyFit interfaces used:** default `-c 1`,
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

**Images:**
- A real, purpose-drawn diagram of one bare, unreplicated Class I symmetry
  triangle (the grid, drawn parallel to the face's own edges) before it's
  copied onto the rest of the polyhedron — the first of the book's three
  required per-class symmetry-triangle images (see Chapters 5 and 6 for the
  other two, and the front-matter image note for how this is drawn
  consistently across all three).
- A real `-P/--preview` render of the fully replicated Class I sphere at a
  frequency high enough to look genuinely dome-like.

**Gotchas & rationale:**
- Chord/vertex counts grow with the *square* of frequency, not linearly — a
  reader doubling frequency expecting roughly double the strut count will
  instead get roughly four times as many, with real consequences for
  fabrication time and file size at high frequency (and, as Part VI will
  show, for how long a nesting job takes to pack).
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

**pyLair/pyFit interfaces used:** `-c 2`, `pylair.polyhedral.build_lcd_faces`,
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

**Images:**
- A real, purpose-drawn diagram of one bare Class II symmetry construction
  — a single polyhedron face first split into its 6 LCD sub-triangles
  around the centroid, then one of those sub-triangles' own frequency grid
  shown — the second of the book's three required per-class symmetry-
  triangle images.
- A real `-P/--preview` side-by-side of the Actual Secret Lair under Class I
  (reused from Chapter 4) versus Class II at the same nominal frequency, so
  the visibly different strut pattern is immediate, not just described.

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

**Concept(s) taught:** **A formal definition of chirality**, established
here before anything else in the chapter: a shape is chiral if it cannot be
superimposed on its own mirror image by any combination of rotation and
translation alone — a left hand and a right hand are the textbook example,
identical in every measurable length and angle, and still not
interchangeable without literally reflecting one of them through a plane.
The Class III ("Skew") method's angled grid as a genuinely chiral
construction — `(m,n)` and `(n,m)` are mirror-image domes of the same size,
not the same dome rotated, which is exactly the left-hand/right-hand
relationship applied to an entire strut pattern — introduced via the
Caspar-Klug/Goldberg-Coxeter `T = m² + mn + n²` triangulation number that all
three of pyLair's subdivision classes turn out to be special cases of
(`m=n` recovers Class II; `n=0` recovers Class I).

**pyLair/pyFit interfaces used:** `-c 3 -n`, `pylair.class_three.py`
(`cross_face_matches`, `local_priority`), `pylair.geodesic_sphere.GeodesicSphere`.

**Learning objectives:**
- State the definition of chirality precisely enough to apply it outside
  this book — "cannot be superimposed on its mirror image by rotation and
  translation alone" — and recognize *why* Class I and Class II domes are
  each achiral (both have at least one mirror-symmetric construction, so
  their own mirror image is just a rotation of themselves) while a Class
  III dome with `m≠n` genuinely is not.
- State what makes `(m,n)` and `(n,m)` genuinely different physical strut
  patterns rather than the same dome viewed differently, and choose between
  them deliberately rather than arbitrarily.
- Explain why chirality matters practically, not just mathematically, for
  geodesic design: a chiral lattice can't be stitched together across
  adjacent polyhedron faces by 3D proximity alone the way Class I and Class
  II can (no reflection symmetry means a point near a face's edge generally
  doesn't land at the same 3D position when computed independently from a
  neighboring face's own basis), and — looking ahead to Chapters 14 and
  20 — it means some of a chiral dome's own *panels* can be mirror images of
  each other despite reporting identical edge lengths, a fact that will
  matter again once those panels need to be cut from directional material.
- Read the Class III golden-value formula (`10T+2` vertices, `20T` faces,
  where `T = m²+mn+n²`) and connect it back to Chapter 4/5's formulas as
  instances of the same general family.

**The villainous example:** **The Actual Secret Lair**'s final subdivision
choice — Class III, `(m,n)` chosen deliberately over its mirror `(n,m)` for
a specific strut-pattern aesthetic, carried forward as the flagship shape
for the rest of the book.

**Images:**
- A real, purpose-drawn diagram of one bare Class III symmetry construction
  — the angled grid, at a deliberately non-square `(m,n)` — the third of the
  book's three required per-class symmetry-triangle images, drawn so its
  angled grid contrasts visually against Chapter 4's parallel-to-edges grid
  and Chapter 5's centroid-radiating one.
- A purpose-drawn `(m,n)` vs. `(n,m)` mirror-pair diagram — two symmetry
  triangles, same `T`, drawn side by side so the reflection relationship is
  immediately visible rather than only algebraic — this book's single most
  important chirality illustration, referenced again in Chapters 14 and 20.
- A real `-P/--preview` render of the full Class III Actual Secret Lair.

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
- A subtlety worth stating precisely: `(m,n)` and `(n,m)` produce the *same*
  total strut length and the *same* vertex/edge/face counts (both share the
  same `T = m²+mn+n²`), because mirroring a shape never changes its lengths
  or angles — only its handedness. A reader checking "did I get the mirror
  image" by comparing golden-value counts alone will find no difference at
  all; only a direct geometric comparison (or the chirality flag Chapters 14
  and 20 introduce) actually distinguishes them.

**Sample prompts:**
- "Build a Class III dome with `f=4, n=1`. Then build one with `f=1, n=4`.
  Are these the same dome, or mirror images? Do their vertex/edge/face
  counts actually differ?"
- "Why can't Class III rely on the same vertex-deduplication-by-distance
  trick that Class I and II use across face boundaries?"
- "In your own words, define chirality — then explain why an achiral Class
  I dome has no equivalent of this `(m,n)`/`(n,m)` distinction at all."

---

### Chapter 7: Projecting Onto the Sphere

**Concept(s) taught:** The final geometric step common to all three
classes — pushing every still-flat symmetry-triangle point outward onto an
actual sphere of the requested radius, while deduplicating vertices shared
along adjacent-face edges — and the KD-tree as the practical tool that
makes that deduplication scale.

**pyLair/pyFit interfaces used:** `pylair.geodesic_sphere.GeodesicSphere`
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

**Images:**
- A purpose-drawn before/after pair: the flat, unprojected symmetry-grid
  faces (reusing the same rendering convention as Chapters 4–6's bare
  symmetry-triangle diagrams) next to the same points pushed outward onto a
  sphere — the "flat, then push outward" idea shown, not just narrated.
- A real `-P/--preview` render of the fully projected sphere at high
  frequency.

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

**pyLair/pyFit interfaces used:** `-e`, `pylair.elongation.elongate()`.

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

**Images:**
- A real `-P/--preview` triptych: the unelongated sphere, the
  Under-the-Ocean Prototype's gentle squash, and the Actual Secret Lair's
  upward stretch, all at the same base frequency so only the elongation
  ratio differs visually.
- pyLair's existing `blog-posts/ellipsoid.png` (real prior output), reused
  as a second, independently-produced reference for the general-ellipsoid
  shape.

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

**pyLair/pyFit interfaces used:** `-t/-x/-y`, `pylair.truncation.truncate()`.

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

**Images:**
- pyLair's existing `blog-posts/edited_truncated.png` and
  `blog-posts/truncated_qcad_focused.png` (real prior output), reused as
  the "here's a correctly truncated dome" reference.
- A purpose-drawn diagram contrasting a safe cutoff (`0.499999`, clear of
  the vertex ring) against an unsafe one (`0.5` exactly, landing on it) —
  the flat-chord failure shown geometrically, not just described.

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

**pyLair/pyFit interfaces used:** `-F/--face`, `-s/--stl`, `-O/--obj`,
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

**Images:**
- A purpose-drawn close-up diagram of a single clipped triangle's corner
  becoming a quad, then that quad split into two triangles along its new
  diagonal seam — a magnified, single-panel version of the whole-dome
  renders elsewhere in the book, since this is a detail no whole-dome
  wireframe shows clearly at normal scale.

**Gotchas & rationale:**
- **A real, corrected piece of this project's own history, told straight:**
  this diagonal was originally a data-format-only seam — real for area/
  edge-length bookkeeping but never added to the actual chord list, so it
  got no strut length and no bevel angle in the report. A later change
  (`pylair`'s `26de45e` commit) made `_clip_face` report it as a genuine
  new chord, so it now flows through the same strut/BOM/bevel-angle
  machinery as any other edge — a good real-world argument, on its own,
  for keeping a project's documentation and its code in sync, since a
  companion blog post once kept describing this exact case as an open
  problem after the fix had already shipped.
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

**pyLair/pyFit interfaces used:** `design_dome` and `preview_dome` for rapid
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

**Images:**
- One real `-P/--preview` render per stop (six total: Under-the-Ocean,
  Orbital Panopticon, Magma Redoubt, Permafrost Cache, Ostentatious Mesa
  Spire, and the studio-apartment coda) — a genuine visual gallery, since
  this chapter's whole premise is comparison-shopping between silhouettes.
- A single comparison chart (purpose-drawn) plotting each stop's footprint
  diameter against its total strut length/cost, so the material-budget
  tradeoff the chapter discusses is visible as data, not just prose.

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

**pyLair/pyFit interfaces used:** `get_bill_of_materials` /
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

**Images:**
- pyLair's existing `blog-posts/tangent_angle_image_CROPPED.png` and
  `blog-posts/spoke_angle_image_CROPPED.png` (real prior diagrams), reused
  as the canonical illustration of each angle type.
- pyLair's existing `blog-posts/STDOUT_tangent_angles.png` and
  `blog-posts/STDOUT_spoke_angles.png` (real prior terminal output), reused
  to show these angles as they actually appear in a report, not just as
  geometry diagrams.

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

**pyLair/pyFit interfaces used:** `-b/--bom-rounding`,
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

**Images:**
- A purpose-drawn bar chart of strut-length groups at the default `-b 9`
  next to the same data re-clustered at a deliberately coarse `-b 2`,
  visually showing distinct bars collapsing into one.

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
images of each other, not true duplicates, exactly Chapter 6's chirality
definition applied to a single flat triangle instead of a whole dome — and
why that matters for directional materials.

**pyLair/pyFit interfaces used:** `pylair.bill_of_materials.group_face_types`,
`_face_type_signature`, `_face_chirality_key`.

**Learning objectives:**
- Group a dome's faces into shape "types" by edge length and read the
  reported panel counts per type.
- Explain why SSS grouping alone can't distinguish a triangle from its
  mirror image — applying Chapter 6's chirality definition at the scale of
  a single flat panel rather than an entire strut lattice — and check a
  group's `chiral` flag and orientation breakdown before ordering
  directional material.
- Recognize that this is a *structurally common* case, not a rare
  edge case exclusive to Class III's inherently chiral construction — it
  shows up on ordinary Class I domes too, once elongation or truncation is
  in play.
- Preview why this same flag matters again in Part VI: pyFit's own
  `allow_mirror` job-spec field is this exact chirality question, asked one
  more time at nesting time rather than design time.

**The villainous example:** Continues **The Actual Secret Lair** — its
panel report is checked specifically for mirror-image pairs, framed as "you
were about to order wood-grain paneling; here's what would have gone wrong
without this check."

**Images:**
- A purpose-drawn pair of triangles: identical edge-length labels, opposite
  orientation, laid side by side (a flat-panel companion to Chapter 6's
  whole-dome `(m,n)`/`(n,m)` mirror-pair diagram) — the chapter's central
  illustration.

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
template per truly distinct shape, not one per hub/panel instance. This
chapter's `-T/--face-templates` output is also this book's bridge into Part
VI: every DXF file it writes is exactly the kind of file a pyFit job spec's
`"dxf"` field expects.

**pyLair/pyFit interfaces used:** `-H/--hub-templates`, `-T/--face-templates`,
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
- State, in one sentence, what a template count and a `panel_count` per
  shape group *don't yet* answer — how many sheets of material it will
  take to actually cut them all out — as the open question Part VI exists
  to close.

**The villainous example:** Continues **The Actual Secret Lair**, generating
its full set of hub and panel templates as the payoff for four chapters of
geometry work.

**Images:**
- A real DXF-derived render of a handful of distinct panel cutting
  templates side by side (shape only, not yet nested on any sheet — Part VI
  is where that happens).

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
  14's chirality point, paid off here concretely) — `-T` writes one file
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

**pyLair/pyFit interfaces used:** the `Possible truncation-artifact
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

**Images:**
- A purpose-drawn close-up of a single sliver panel next to a normal panel
  at the same scale, so the near-zero-area case is visually obvious rather
  than only a suspiciously small number in a table.

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

## Part V — Output, Interfaces, and Agentic Use (pyLair)

### Chapter 17: Getting It Out the Door — DXF, VRML, STL, OBJ

**Concept(s) taught:** pyLair's export formats and what each is actually
for — DXF for CAD import (and, as Part VI will show, for pyFit nesting),
VRML for 3D display, STL/OBJ for 3D printing — and how face-aware
truncation (Part III) is the prerequisite that makes the face-dependent
formats (`-F`, `-s`, `-O`) work correctly on a truncated dome at all.

**pyLair/pyFit interfaces used:** default DXF/VRML output, `-F/--face`,
`-s/--stl`, `-O/--obj`, `-P/--preview`,
`pylair.output.OutputDXF/OutputFaceVRML/OutputSTL/OutputOBJ`.

**Learning objectives:**
- Choose the right export format(s) for a given downstream use (CAD
  import, quick visual sanity check, 3D-printed scale model, and — new as
  of this chapter — feeding a pyFit nesting job).
- Explain why `-F/--face` skips DXF entirely in favor of face-inclusive
  VRML, but why `-T/--face-templates` (Chapter 15) still writes its own
  per-shape DXF files regardless — those, not the whole-dome VRML, are
  what Part VI's nesting job actually needs.
- Generate a preview PNG (`-P`) as a fast sanity check before committing to
  a full multi-format export.

**The villainous example:** **The Actual Secret Lair**'s full export — the
payoff of Parts II–IV, written out in every format at once.

**Images:**
- pyLair's existing `blog-posts/CAD_dome.jpg` and `sample_image.png` (real
  prior CAD-import screenshots), reused as the "here's what a DXF import
  actually looks like" reference.

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

**pyLair/pyFit interfaces used:** all four pyLair MCP tools, each sharing
the one geometry parameter schema described in `README.md`.

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

**Images:** None new — this chapter is a narrated tool-call session, and
reuses the preview images already generated in earlier chapters as its
inline "here's what came back" figures.

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

## Part VI — From Panels to Sheets: Nesting with pyFit

### Chapter 19: Introducing pyFit — Nesting as a Second Geometry Problem

**Concept(s) taught:** pyFit as a genuinely standalone project — no code
dependency on pyLair whatsoever, just a shared file format (DXF) — that
solves a different, and differently hard, geometry problem: given a set of
2D shapes and how many of each you need, arrange them on rectangular sheet
stock with minimal wasted material. The **no-fit-polygon (NFP)**: the
region a moving shape's reference point must stay outside of to avoid
overlapping a fixed shape, computed via a Minkowski-sum technique; the
**bottom-left-fill heuristic** built on top of it (largest parts first, try
a range of rotation/mirror orientations, pick the leftmost-then-bottommost
legal placement); and why this is fundamentally a *combinatorial*, NP-hard
problem in a way pyLair's own geometry (closed-form, once you know the
formula) never was — meaning pyFit's own correctness story is "a good
heuristic, honestly verified," not "the provably optimal layout."

**pyLair/pyFit interfaces used:** `pip install "pyfit-agentic-polygon-nesting[mcp]"`,
`pyfit -j job.json -o output/nest`, `pyfit.nfp`, `pyfit.packer.pack`.

**Learning objectives:**
- Explain what a no-fit-polygon is and why the NFP of two unit squares
  being exactly a 2×2 square centered at the origin is a hand-checkable
  sanity case worth knowing, not an arbitrary example.
- Describe the bottom-left-fill heuristic's basic loop (place the largest
  remaining part, try a set of rotation angles and, unless
  `allow_mirror` is false, mirrored orientations, pick the
  leftmost-then-bottommost legal candidate) well enough to predict, roughly,
  what order a job will place its parts in.
- Explain why 2D irregular nesting is NP-hard, and what that implies about
  pyFit's own honesty: it documents itself as a heuristic in the same
  family as tools like SVGnest/DeepNest, not a globally optimal solver, and
  never claims otherwise.
- Recognize that pyFit is genuinely general-purpose — it will nest any set
  of closed 2D polygons on any rectangular sheet, dome panels or otherwise.

**The villainous example:** Two, deliberately: **a standalone, non-dome
nesting job** — a batch of henchman-uniform patch blanks and throwing-star
stencils, nested purely to prove pyFit owes nothing to pyLair and is happy
nesting shapes that have nothing to do with a geodesic anything — followed
by the chapter's real payoff, **the first real pyFit run on pyLair output**:
a handful of the Actual Secret Lair's own panel-template DXF files
(Chapter 15), nested for the first time, previewed inline, no files written
yet.

**Images:**
- pyFit's existing `blog-posts/images/nest_sheet1_pylair_triangles.png`
  (real prior output), reused as this Part's opening "here's the payoff"
  image.
- A purpose-drawn NFP construction diagram: two unit squares and the
  resulting 2×2 no-fit-polygon, drawn as a hand-checkable geometric proof
  rather than only stated as a formula.
- A purpose-drawn bottom-left-fill placement-order diagram: a handful of
  parts placed in sequence, each one's chosen "leftmost-then-bottommost"
  point marked, so the heuristic's own logic is visible step by step.
- A real `-P/--preview` render of the standalone patch/stencil nesting job.

**Gotchas & rationale:**
- **A real, documented Minkowski-sum bug, told straight, the same way this
  book has told pyLair's own historical bugs:** `pyclipper.MinkowskiSum` on
  a closed path doesn't return one resolved polygon — it returns raw sweep
  contours, which for a small pattern swept around a larger path includes
  an inner contour that *looks* like a hole but mathematically can't be one
  (the Minkowski sum of two convex filled shapes is always itself convex).
  The fix (`pyfit/nfp.py`) treats every returned contour as an independent
  solid region and unions them via `shapely` rather than trusting Clipper's
  own winding-direction-implied fill rule — and, just as importantly, this
  bug passed a first hand-computable test case (two unit squares) cleanly;
  it only showed up on a size-mismatched second case, which is this
  chapter's own concrete argument for testing a geometric primitive against
  more than one shape/size combination before trusting it.
- **Candidate placement points aren't fully exhaustive, on purpose, and this
  is stated as a scope decision, not a bug**: the search considers the
  sheet's corners, every NFP vertex, and every NFP-vs-boundary and
  NFP-vs-NFP crossing — enough to tile, say, six unit squares perfectly
  onto a 3×2 sheet — but it isn't full NFP-boundary tracing, so it can
  occasionally miss an even tighter placement. Every candidate is
  re-validated for overlap/containment before acceptance, though, so this
  can only produce a *non-optimal* placement, never an *invalid* one — the
  same "wrong shape vs. wrong count" distinction Chapter 6 taught, one
  problem domain over.

**Sample prompts:**
- "Explain, in your own words, why nesting a set of triangles onto plywood
  is a harder problem than computing their shapes in the first place."
- "Show me the no-fit-polygon of two unit squares. Does it match what you'd
  expect by hand?"
- "Nest this batch of patch/stencil blanks — nothing to do with any dome —
  just to see pyFit work on its own terms first."

---

### Chapter 20: From Bill of Materials to Job Spec — Nesting the Actual Secret Lair's Panels

**Concept(s) taught:** How a pyFit job spec is actually built from a real
upstream bill of materials — pointing a `"dxf"` field at one of Chapter 15's
`-T/--face-templates` output files and its `"quantity"` at that same shape
group's reported `panel_count` — with zero code coupling between the two
projects, just a shared, plain DXF file; **sheet utilization** as the
metric that actually answers "how much material am I wasting"; and
`allow_mirror` as Chapter 14's chirality flag, encountered again, now as a
decision that changes what pyFit is *allowed to place*, not just what it
reports.

**pyLair/pyFit interfaces used:** a full pyFit job spec built from pyLair's
own `-T` output and BOM `panel_count`s; `-R/--rotation-step`;
`"allow_mirror"`; the utilization figures in `pyfit`'s JSON report.

**Learning objectives:**
- Construct a real job spec from a real bill of materials: one `"parts"`
  entry per distinct panel shape group, `"dxf"` pointing at that group's
  template file, `"quantity"` set from the group's `panel_count` — not
  guessed, not hand-counted.
- Read a per-sheet utilization figure and total sheet count, and connect
  "how many sheets does this dome actually need" back to Chapter 4's own
  point about frequency growing struts (and, now, panels) quadratically.
- Decide `allow_mirror` correctly for a given material: `true` (the
  default) for non-directional stock like plain plywood, `false` for
  anything chirality-sensitive — directly reusing Chapter 14's `chiral`
  flag and orientation breakdown as the actual basis for that decision,
  rather than a guess.
- Use `-R/--rotation-step` as the honest speed/quality tradeoff it is: a
  finer step tries more orientations per candidate (better packing,
  slower), a coarser one is faster at the cost of a somewhat looser layout
  — the exact same kind of tradeoff Chapter 13's `-b/--bom-rounding`
  taught, one problem domain over.

**The villainous example:** Two nesting jobs, deliberately contrasted:
**The Actual Secret Lair**'s panels, built from ordinary plywood
(`allow_mirror: true`, since plain sheet stock has no grain direction to
worry about) — the chapter's main worked example, going from BOM straight
through to a multi-sheet cut plan; and **The Under-the-Ocean Prototype**'s
panels, revisited specifically because Chapter 8 elongated it and Chapter
14's chirality check flagged real mirror-image pairs among its panels —
nested here with `allow_mirror: false`, because its hull uses a one-sided
pressure coating, giving a real, previously-established reason (not an
invented one) for the flag to matter and visibly change the resulting
layout.

**Images:**
- A real `-P/--preview` render of the Actual Secret Lair's full multi-sheet
  nesting result (one image per sheet actually used), annotated with each
  sheet's reported utilization percentage.
- A real `-P/--preview` comparison pair: the Under-the-Ocean Prototype's
  panels nested with `allow_mirror: true` versus `allow_mirror: false` on
  the same sheet, so the flag's practical effect on the layout is visible,
  not just reported as a JSON field.

**Gotchas & rationale:**
- **Reusing scrap across sheets costs real search time on large jobs**,
  documented plainly rather than hidden: every part instance tries each
  already-opened sheet in turn before a new one opens, so leftover scrap
  gets reused — measured, on a real 40-panel, 3-sheet job of small pyLair
  triangles, at about 3x slower than no-reuse at the default rotation step,
  but back to roughly the same speed at a coarser one. `-R/--rotation-step`
  is the direct, honest lever for this tradeoff, the same way `-b` was
  pyLair's own precision/merge lever in Chapter 13.
- **Rectangular sheets only, and no support yet for irregular stock or
  offcuts with existing cutouts** — a real, stated MVP scope cut, not an
  oversight; a reader whose actual plywood has a chunk already missing from
  a prior project has to account for that manually, the same honest
  boundary Chapter 11 drew around pyLair's own terrain-agnostic truncation.
- A subtlety worth stating precisely, echoing Chapter 6's own mirror-pair
  gotcha: `allow_mirror: false` doesn't make a job spec *fail* — it simply
  removes mirrored orientations from the candidate search, which can mean
  more sheets, not an error, is the honest cost of chirality-correctness.

**Sample prompts:**
- "Build a pyFit job spec from this dome's face-template output and panel
  counts directly — don't hand-type any quantities."
- "Nest it once with mirroring allowed, once without. How much does
  disallowing mirroring change the sheet count or utilization?"
- "If packing feels slow on this many panels, what's the first setting
  you'd loosen, and what do I give up by loosening it?"

---

### Chapter 21: Talking to pyFit — The Four MCP Tools, Progress Notifications, and a Combined Workflow

**Concept(s) taught:** `design_nest`, `preview_nest`, `get_nest_report`, and
`export_nest` as pyFit's own version of Chapter 18's four-tool
iterate-then-commit pattern — cheap sanity check, visual check, full
placement report, commitment — plus a genuinely new idea neither pyLair
chapter needed: **MCP progress notifications** on a long-running call, and
why that requires the nesting work to run in a worker thread rather than
block the server's own event loop. The chapter closes by narrating one
complete, combined pyLair-then-pyFit design session end to end.

**pyLair/pyFit interfaces used:** all four pyFit MCP tools
(`design_nest`/`preview_nest`/`get_nest_report`/`export_nest`); MCP progress
notifications (a progress token from the calling client); the full
pyLair→pyFit pipeline, both MCP interfaces used together in one narrated
session.

**Learning objectives:**
- Use `design_nest` to cheaply try a job spec (sheets used, utilization) and
  `preview_nest` to see the layout inline, before committing to
  `export_nest`'s real DXF files — the exact same discipline Chapter 18
  taught for pyLair's own four tools.
- Explain why a *synchronous* MCP tool can never emit a progress
  notification mid-call (it blocks the server's single event loop for its
  entire duration), and why pyFit's tools are instead `async def`,
  running the actual pack in a worker thread and bridging its progress
  callback back onto the event loop — concretely, not just as a stated
  fact: a real ~5.6s job produced roughly 33 progress notifications spread
  across the whole call, not bunched at the end.
- Narrate, end to end, one full design session spanning both toolkits: a
  `design_dome`/`preview_dome` iteration loop (pyLair), a
  `get_bill_of_materials` check and `-T` template export (pyLair), a
  `design_nest`/`preview_nest` iteration loop built from those exact
  templates (pyFit), and a final `export_nest` commitment — the complete
  arc this book has been building toward since Chapter 1's cold open.

**The villainous example:** **The Actual Secret Lair**'s complete
design-to-cut-plan session, narrated as one continuous transcript across
both MCP servers — the same dome Chapters 4–18 built, now actually ready
for a henchman to load material into a laser cutter.

**Images:** None new — this chapter's images are the narrated session's own
inline tool outputs, reusing renders already produced in Chapters 18 and
20.

**Gotchas & rationale:**
- All four pyFit tools enforce the exact same validation as its CLI,
  because one engine (`pyfit/api.py`) underlies both interfaces — echoing
  Chapter 18's identical point about pyLair, now demonstrated on the
  nesting side: a malformed job spec or an out-of-range rotation step
  raises the same clear error through `design_nest` as through the CLI.
- With no progress token supplied (or when a tool function is called
  directly, e.g. in a test), progress reporting is simply a no-op — a
  reader building their own client doesn't need to opt into anything
  special to get correct behavior either way.
- `design_nest` and `get_nest_report` write no files at all, exactly
  mirroring `design_dome`/`get_bill_of_materials`'s own file-free iteration
  loop from Chapter 18 — the same "iterate freely, commit once" discipline,
  taught once per toolkit rather than assumed to transfer automatically.

**Sample prompts:**
- "Try two different rotation steps for this nesting job using `design_nest`
  only — don't write any files yet. Which one gives better utilization for
  the time it takes?"
- "Preview the nesting result, then get the full placement report before we
  export any DXFs for real."
- "Walk me through this entire dome, from picking a polyhedron to a
  ready-to-cut sheet layout, as one continuous session."

---

### Chapter 22: Which Piece Goes Where — the Assembly Manifest

**Concept(s) taught:** The Bill of Materials deliberately collapses individual
hubs/struts/panels into cutting-template *types* and counts — "how many of
each shape to cut." The **assembly manifest** answers a different question:
"which specific physical piece goes where, and what does it connect to."
Every hub, strut, and panel gets its own stable label (`H#`/`S#`/`P#` —
literally its position in the dome's own vertex/chord/face arrays) and its
real adjacency to its neighbors (which struts meet at a hub and at what
angle, which hubs bound a panel, which panel(s) border a strut, the bevel
angle at each panel edge). On top of that: a **per-instance pyFit job spec**
(quantity always 1 per part, named by its manifest label) so a pyFit nest
report becomes traceable back to a specific dome hub/panel, handling a
chiral panel group's mirror orientation explicitly rather than trusting
pyFit's own packer to flip the correct instances; and an **annotated
assembly schematic** — the same depth-cued wireframe Chapter 2 introduced,
with per-instance labels optionally drawn at each hub/strut/panel's
position. The chapter closes with the real historical bug this exact
cross-check caught: a truncated dome's base ring was missing its closing
struts entirely, invisible to every golden-value/Euler's-formula check in
this book so far, because those checks only apply to a *closed* manifold
and a truncated dome isn't one.

**pyLair/pyFit interfaces used:** `get_assembly_manifest`,
`export_assembly_job_spec` (`kind="panels"` or `"hubs"`),
`render_assembly_schematic` (MCP); `--assembly-manifest`,
`--pyfit-job-spec=panels|hubs` (plus `--sheet-width`/`--sheet-height`),
`--assembly-schematic` (plus `--schematic-strut-labels`/
`--schematic-panel-labels`) (CLI).

**Learning objectives:**
- Explain what a per-instance assembly manifest gives you that the Bill of
  Materials' own type-grouped counts structurally can't: which *specific*
  physical piece a builder is holding, and what it connects to.
- Read a real manifest's hub entry and trace one hub's own connections to
  specific neighboring hubs, the struts between them, and each strut's
  tangential/spoke angle.
- Explain why a chiral panel group's "other" mirror-orientation instances
  get an inline pre-mirrored polygon in the job spec, rather than an
  `allow_mirror=True` flag left to pyFit's own packer to resolve.
- Recognize the base-ring-strut bug as a category, not just a fixed
  instance: a bug that passed every closed-manifold check (Euler's formula,
  golden-value counts) because a truncated dome was never a closed manifold
  to begin with, caught instead by a direct strut↔panel adjacency
  cross-check built for an unrelated reason.

**The villainous example:** **The Actual Secret Lair**'s own assembly
manifest and per-instance job spec, picking up exactly where Chapter 20's
nesting session left off — plus a smaller, deliberately coarser example dome
for the annotated schematic image, since a dome at the Actual Secret Lair's
own frequency has far too many hubs to label legibly at once.

**Images:** A real annotated assembly schematic (hub labels drawn at their
positions) on a small, legible example dome — the same depth-cued wireframe
style established in Chapter 2, now with labels.

**Gotchas & rationale:**
- Chiral job-spec construction: a chiral group's cutting template is,
  without saying so, one specific arbitrary mirror orientation; letting
  pyFit's own packer decide whether to flip an instance for packing
  efficiency would risk cutting the wrong-handed piece for this specific
  dome.
- Hub connector plates have no chirality model at all — pyLair doesn't
  compute a chirality signature for hub shapes the way it does for panels,
  so every hub instance is submitted with `allow_mirror=True` unconditionally.
- The base-ring-strut bug: found via the manifest's own `bordering_panels`
  field (a base-ring strut borders exactly 1 panel, an interior strut
  borders exactly 2 — there was, before the fix, no such thing as a
  1-bordering-panel strut at all, because the edge that would have produced
  one was never a chord in the first place).

**Sample prompts:**
- "Get the assembly manifest for this dome and tell me which struts meet at
  hub 12, and at what angles."
- "Build a per-instance pyFit job spec for this dome's panels, and make sure
  the chiral ones keep the correct orientation rather than letting the
  packer decide."
- "Render an annotated schematic of this dome with hub labels so a builder
  knows which connector goes where."

---

## Part VII — Becoming a Better Design Villain

### Chapter 23: Prompting pyLair and pyFit Like You Mean It

**Concept(s) taught:** Practical prompt craft across a two-toolkit, eight-tool
agentic interface: being specific about which tool's answer you actually
want (and, now, which *toolkit's* — a geometry question and a nesting
question are never the same question), carrying forward settled findings
(a chosen frequency, a validated cutoff, a resolved `allow_mirror` choice)
instead of re-deriving them, and recognizing when a tool's own output is
telling you something the prompt didn't ask for.

**pyLair/pyFit interfaces used:** A deliberate mixed review across all four
pyLair MCP tools, all four pyFit MCP tools, and both CLIs.

**Learning objectives:**
- Write prompts that carry an earlier chapter's findings (a safe truncation
  cutoff, a chosen subdivision class, a resolved chirality/`allow_mirror`
  decision) into a later request, rather than starting from scratch.
- Recognize the difference between a prompt that under-specifies (leading
  to arbitrary defaults) and one that over-specifies (defeating the point
  of asking an agent to reason at all).
- Distinguish which of pyLair's four tools, or pyFit's four tools, actually
  answers a given real-world question, rather than guessing — and
  recognize when a question ("is this design good enough to build")
  secretly spans both toolkits at once.

**The villainous example:** A "clinic" chapter, following the Omen book's
own prompting-clinic pattern directly — four real submitted prompts, each
with a real flaw, rewritten and explained, reusing dome and nesting designs
this book has already built rather than introducing new ones.

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
- **Prompt four, a two-toolkit question mistaken for a one-toolkit one:**
  *"How much material will this dome actually cost me?"* — pyLair's own
  `-a/--area-cost` answers the *theoretical* material cost (total panel
  area times unit price, assuming zero waste), which is a genuinely
  different, always-smaller number than the *real* cost once Part VI's
  actual sheet utilization is accounted for. **Rewritten:** "Give me
  pyLair's theoretical panel-area cost, then nest the actual templates with
  `design_nest` and tell me the real sheet count and utilization — how far
  apart are the two cost figures?" — the fix isn't a better single prompt,
  it's recognizing the question needs both toolkits' tools, in sequence, to
  actually answer honestly.

**Sample prompts:**
- (This chapter's exercises *are* prompt-rewriting exercises, matching the
  Omen book's own prompting-clinic structure — readers draft, then
  critique, their own.)

---

### Chapter 24: When to Trust the Agent, and When Not To

**Concept(s) taught:** A retrospective, cross-cutting look at every
deliberately rule-based or independently-verified decision point this book
has encountered across *both* toolkits — pyLair's golden-value formulas,
the `antitile`/`trimesh`/`ezdxf` oracles, the flat-chord `ValueError`; and
pyFit's own NFP correctness story, verified against a hand-computable case
and, once that proved insufficient on its own, a second independent
method — generalized into a checklist readers can apply to their *own*
geometry, nesting, or agentic tools, not just these two.

**pyLair/pyFit interfaces used:** None new — a synthesis chapter.

**Learning objectives:**
- Articulate a general rule for "when does a geometric or combinatorial
  claim need independent verification, not just internal self-consistency"
  and test it against several examples from the book (Class II's
  Euler-formula catch, Class III's antitile cross-check, the panel oracle's
  trimesh/ezdxf round-trip, and pyFit's own Minkowski-sum union fix).
- Recognize the pattern in both toolkits' repeated use of *external,
  independently-implemented* oracles or hand-checkable cases — never
  validating their own math only against themselves — as evidence for that
  rule, not just one project's arbitrary house style.
- Contrast pyLair's closed-form correctness story (a subdivision either
  matches its known golden-value formula or it doesn't) against pyFit's
  honestly probabilistic one (a heuristic that's correct about *validity*
  by construction — every accepted placement is re-checked for overlap —
  but only ever *good*, never provably optimal, about efficiency) as two
  legitimately different, equally honest ways for a geometry tool to state
  what it actually guarantees.

**The villainous example:** No new dome or nesting job — a structured
retrospective across every design used so far, framed as the after-action
review our heroine holds after any operation.

**Gotchas & rationale:**
- The chapter's central thesis, stated directly: a check that only compares
  a result against its own internal assumptions (Euler's formula on a
  construction that itself defines the vertex/edge/face relationship) can
  catch a *count* bug but not a *shape* bug — Class III's own real history
  (Chapter 6) is the sharpest illustration in the pyLair half of the book,
  because it passed exactly that kind of internal check while still being
  wrong, and only an independent, differently-implemented library caught
  it. pyFit's Minkowski-sum bug (Chapter 19) makes the identical point in
  the nesting half: it passed its first hand-computable test case cleanly
  and only failed on a second, differently-shaped one — one verified case
  is not the same claim as a verified method.
- Applied one level up: this same principle is why the book itself insists
  every gotcha be traceable to a real commit, a real test, or a real run
  log across *both* projects — an outline that only checks its own
  internal consistency has exactly the same blind spot Class III's first
  implementation, and pyFit's first NFP test case, each did.

**Sample prompts:**
- "Looking back at everything this book covered, list every point where
  either pyLair or pyFit checked a result against an independent,
  differently-implemented source rather than just its own internal
  consistency. What do they have in common?"

---

### Chapter 25: Conclusion

**Concept(s) taught:** A wrap-up, not a new concept — consolidates the
book's arc from "pick a polyhedron" through "should you even trust this
number" through "and now cut it out of actual plywood," in light of
everything the reader now knows about both toolkits.

**Content:**
- A full recap of the combined pipeline (polyhedron → subdivision →
  projection → shaping → bill of materials → export → nesting → cut plan →
  agentic interface, across both pyLair and pyFit) in light of the real
  gotchas each stage turned out to hide.
- A pointer back to both companion blog posts
  (`blog-posts/introducing-pylair.md` and pyFit's own
  `blog-posts/introducing-pyfit.md`) for readers who want the same material
  in a shorter, funnier form, plus a pointer to each project's `AGENTS.md`
  for readers who want to go build on either tool directly.
- A closing status update on the running examples: the Actual Secret Lair
  is designed, verified, exported, *and* nested — a real, sheet-by-sheet
  cut plan sitting in the henchmen's fabrication queue; the Under-the-Ocean
  Prototype remains, honestly, just a prototype — a secret lab's actual
  construction is (of course) kept secret, exactly as the blog post
  promised.
- A short "where each toolkit itself goes next" section, pulled honestly
  from each project's own real, currently-open items rather than invented
  future features: pyLair's proactive truncation-risk warnings before
  export, an optional boundary cap for fully enclosed structures, and
  door-frame design assistance; pyFit's own stated next steps — a
  refinement pass (simulated annealing or genetic reordering) on top of its
  base bottom-left-fill heuristic, support for irregular stock/offcuts
  beyond plain rectangles, and a PyPI publish that, as of this writing,
  hasn't happened yet for either project.

**Sample prompts:**
- "Summarize everything you now know about the Actual Secret Lair's design
  and its nesting plan across every stage of both pipelines, as if handing
  off to whoever actually builds it."

---

## Appendices

- **Appendix A — Glossary.** Every geometry, engineering, and nesting term
  introduced across the book — symmetry triangle, chord, hub, frequency,
  triangulation number `T`, **chirality**, dihedral/bevel angle,
  Goldberg-Coxeter construction, no-fit-polygon (NFP), Minkowski sum,
  bottom-left-fill, sheet utilization, `allow_mirror`, and more — defined
  in one or two sentences each, cross-referenced to the chapter that
  introduced it.
- **Appendix B — CLI and MCP Tool Reference.** Every CLI flag and every MCP
  tool used in the book, for both pyLair and pyFit, with a one-line
  description and the chapter(s) that cover it — a fast lookup companion
  once readers start designing (and nesting) their own domes instead of
  the book's examples.
- **Appendix C — Further Reading.** The real sources pyLair's and pyFit's
  own constructions are drawn from and verified against: Kenner, H. (1976),
  *Geodesic math and how to use it*; Šiber, A. (2007), "Icosadeltahedral
  geometry of fullerenes, viruses and geodesic domes" (arXiv:0711.3527);
  [`antitile`](https://github.com/brsr/antitile); [`trimesh`](https://trimesh.org/);
  [`ezdxf`](https://ezdxf.readthedocs.io/); [`pyclipper`](https://github.com/fonttools/pyclipper)
  and the underlying Clipper library pyFit's NFP computation is built on;
  [`shapely`](https://shapely.readthedocs.io/); and, for readers who want to
  go further with 2D nesting specifically, the same family of open-source
  bottom-left-fill nesters (SVGnest/DeepNest) pyFit's own documentation
  cites as kin — plus both companion blog posts and both projects'
  `README.md` "Caveats"/"Known limitations" sections for continued
  reference.
