# Chapter 3: Picking a Polyhedron

"Icosahedron," said the AI Henchman, before our Heroine had finished typing the question. It was the right answer, as it happens. It was also exactly what the Rival's chatbot had said, for exactly the same reason: every dome tutorial ever written starts from one. Our Heroine asked it to justify the choice without mentioning tutorials. That took longer, and it is what this chapter is about.

Every geodesic dome pyLair builds starts the same way: not with a sphere, but with something that merely *resembles* one, a flat-faced polyhedron, subdivided later into something rounder. This chapter covers that first, easy-to-skip decision, and introduces the first of the book's smaller running examples: **the Under-the-Ocean Prototype**, our Heroine's contingency plan for the day the HOA wins and the Secret Lab™ relocates somewhere the neighbors can't file noise complaints. An HOA has opinions and a strongly worded letterhead; the Pacific Ocean has neither, and settles every disagreement with tons of pressure per square foot of hull. That's why this design goes first: it has the least patience for a shape chosen carelessly.

## Why Start From a Polyhedron at All

A sphere is the shape geodesic design is trying to approximate, and the one shape it never starts from. The reason is practical: a sphere has no natural way to divide itself into a repeating pattern of identical, or nearly identical, flat triangles. A **polyhedron**, a solid built entirely from flat faces, does. Subdivide one face into a fine triangular grid, replicate that grid onto every other face, and project the result outward onto a sphere of the radius you want, and you get a dome built from many small, efficient triangles instead of a few large, weak ones. Chapters 4 through 7 show how the subdivision and projection work. This chapter is about the step before: which polyhedron to start from.

Why the starting shape matters is easy to state: the closer the starting polyhedron already is to a sphere, the less work the subdivision has to do to get the rest of the way, and the less variety in strut length and hub angle results. A polyhedron with many small, evenly arranged faces needs a gentler grid on each one to end up looking spherical; a polyhedron with a few large faces needs a much more aggressive one. pyLair offers three starting points, at different places on that spectrum.

## Three Starting Points: Icosahedron, Octahedron, and Tetrahedron

pyLair's default, and the shape behind nearly every geodesic dome you've seen a photograph of, is the **icosahedron**: 20 triangular faces, 12 vertices, 30 edges.

**Prompt:**
> Preview a bare, frequency-1 icosahedron for me, no subdivision yet, just the base shape, so I can see what pyLair's default polyhedron looks like. Give me its `design_dome` summary too.

**What Comes Back** (a `preview_dome` render, `polyhedron="icosahedron"`, `frequency=1`, `radius=1.0`, captioned "12 vertices, 30 struts"; then a snapshot of `design_dome`'s JSON for the same shape):

**[IMAGE: examples/images/base-icosahedron.png | A wireframe icosahedron: 12 vertices joined by 30 edges into 20 triangles, with nearer edges drawn darker.]**
**[CAPTION: A bare, unsubdivided icosahedron, pyLair's default base polyhedron.]**

```json
{
  "vertex_count": 12,
  "edge_count": 30,
  "face_count": 20,
  "truncated": false,
  "bounding_box": {"x": [-0.8944, 0.8944],
                   "y": [-0.8507, 0.8507],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 1.7889,
  "total_strut_length": 31.5439,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 1,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

The second option is the **octahedron**: 8 triangular faces, 6 vertices, 12 edges, a coarser starting point, selected with `polyhedron="octahedron"`.

**Prompt:**
> Now preview the same thing with the octahedron instead, same frequency and radius, with its summary.

**What Comes Back** (a `preview_dome` render, `polyhedron="octahedron"`, `frequency=1`, `radius=1.0`, captioned "6 vertices, 12 struts"; then a snapshot of `design_dome`'s JSON):

**[IMAGE: examples/images/base-octahedron.png | A wireframe octahedron: two square pyramids joined base to base, 6 vertices and 8 triangular faces.]**
**[CAPTION: A bare octahedron, at the same frequency and radius as Figure 3.1 for direct comparison.]**

```json
{
  "vertex_count": 6,
  "edge_count": 12,
  "face_count": 8,
  "truncated": false,
  "bounding_box": {"x": [-1.0, 1.0],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 16.9706,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 1,
    "polyhedron": "octahedron", "dome_class": 1, ...
  }
}
```

The third and coarsest is the **tetrahedron**: 4 triangular faces, 4 vertices, 6 edges, the fewest of anything pyLair can start from, selected with `polyhedron="tetrahedron"`.

**Prompt:**
> Now preview the tetrahedron, same frequency and radius as the other two, with its summary.

**What Comes Back** (a `preview_dome` render, `polyhedron="tetrahedron"`, `frequency=1`, `radius=1.0`, captioned "4 vertices, 6 struts"; then a snapshot of `design_dome`'s JSON):

**[IMAGE: examples/images/base-tetrahedron.png | A wireframe tetrahedron: 4 vertices and 6 edges forming 4 triangular faces.]**
**[CAPTION: A bare tetrahedron, at the same frequency and radius as Figures 3.1 and 3.2.]**

```json
{
  "vertex_count": 4,
  "edge_count": 6,
  "face_count": 4,
  "truncated": false,
  "bounding_box": {"x": [-0.5774, 0.5774],
                   "y": [-0.5774, 0.5774],
                   "z": [-0.5774, 0.5774]},
  "height": 1.1547,
  "footprint_diameter": 1.1547,
  "total_strut_length": 9.798,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 1,
    "polyhedron": "tetrahedron", "dome_class": 1,
    ...
  }
}
```

Side by side, the three summaries' counts at frequency 1, meaning no subdivision at all, just the base polyhedron, reported through the same pipeline as every other dome in this book:

```json
{"polyhedron": "icosahedron", "vertex_count": 12,
 "edge_count": 30, "face_count": 20}
{"polyhedron": "octahedron", "vertex_count": 6,
 "edge_count": 12, "face_count": 8}
{"polyhedron": "tetrahedron", "vertex_count": 4,
 "edge_count": 6, "face_count": 4}
```

Twenty faces, against eight, against four, before any subdivision. That gap doesn't close as frequency rises; it multiplies.

## The Golden-Value Formulas: A Sanity Check, Not Folklore

Each subdivision class this book teaches (Chapters 4 through 6) has an exact formula for its vertex, edge, and face counts in terms of frequency, built on one of three base counts depending on the starting polyhedron. For Class I at frequency `f`, the simplest case, they are:

| | Icosahedron | Octahedron | Tetrahedron |
|---|---|---|---|
| Faces | `20f²` | `8f²` | `4f²` |
| Edges | `30f²` | `12f²` | `6f²` |
| Vertices | `10f²+2` | `4f²+2` | `2f²+2` |

Practitioners call these **golden values**: counts known in advance, against which any build can be checked. They aren't a rule of thumb. pyLair's test suite checks real builds against them (`tests/test_api.py`), and you can check the `f=1` row against the three results above by hand: `20(1)² = 20` faces for the icosahedron, `8` for the octahedron, `4` for the tetrahedron. Each column also satisfies Euler's formula for a closed polyhedron, vertices − edges + faces = 2 (for the icosahedron, `(10f²+2) − 30f² + 20f² = 2`), which Chapter 5 turns into a bug detector. You'll use the icosahedron column constantly from Chapter 4 on; the other two exist for the same reason their shapes do, the design situations below.

## Choosing Deliberately, Not by Habit

Reaching for the icosahedron (which is also what happens if you don't specify `polyhedron`) is right most of the time. More faces at the same frequency means a gentler grid per face, which generally means a rounder result and less strut-length variety for a given amount of subdivision. But "the default is usually right" is a different claim from "the default is always right," and this chapter's job is teaching you to notice when it isn't.

**The Under-the-Ocean Prototype is a case where it is right.** A pressure hull wants to be as close to uniformly spherical as possible: no weak axis, no flat region where the water can concentrate its argument. Of the three base shapes, the icosahedron starts closest to a sphere and spreads its vertices most evenly, so the Prototype starts from it, as Chapters 8 and 11 continue. That's the justification the AI Henchman eventually produced without mentioning tutorials, and it's a reason, not a habit.

The octahedron earns its place for a different, checkable reason, visible in Figure 3.2. Two of its six vertices sit at the poles, directly above and below the shape along Z, and the other four sit in a ring around the middle, all at exactly `Z=0`: `(±1,0,0)` and `(0,±1,0)` in pyLair's construction (`pylair/polyhedral.py`'s `Octahedron` class). That's not an approximate equator; it's an exact one, present before any subdivision or truncation touches the shape.

The icosahedron's layout (`pylair/polyhedral.py`'s `Icosahedron` class) is different, and worth knowing precisely. One vertex sits at the north pole, one at the south, and the remaining ten form two rings of five at `Z = ±1/√5 ≈ ±0.4472`, offset from each other by 36°. Neither ring sits *on* `Z=0`. Near the equator, the icosahedron is a band of zigzagging triangles between two offset rings; the octahedron is a single square ring at the midline.

Why would a designer care? Because a dome is a sphere cut along a plane (Chapter 9), and where that cutting plane falls relative to a ring of vertices decides what the dome's base looks like: whether the cut runs cleanly along existing struts or slices through panels, and whether it lands so close to a ring that pyLair refuses the cut or produces near-invisible slivers. Chapters 9, 10, and 16 work through those consequences with real cutoff numbers.

Subdivision adds more rings of vertices to every base shape, so the exact `Z=0` ring isn't unique to the octahedron after Chapter 4 (an even-frequency icosahedral sphere has one too, as Chapter 9 shows). The point to fix now is narrower: **where the vertices sit is a property of the base shape you pick, present before a single subdivision step runs, so choose it on purpose.**

The tetrahedron (`pylair/polyhedral.py`'s `Tetrahedron` class) deserves the same precision rather than an analogy to the octahedron. Its four vertices sit at two levels: two at `Z = +1/√3 ≈ +0.5774` and two at `Z ≈ −0.5774`, none on `Z=0`. So it isn't a more extreme version of the octahedron's equatorial ring; it has no equatorial ring at all.

What it offers is the fewest physical pieces pyLair can produce at a given frequency: a frequency-1 tetrahedron is 4 panels and 6 struts, against the octahedron's 8 and 12 and the icosahedron's 20 and 30. When the *count* of pieces matters more than roundness (a rapid-assembly shelter, say, where every extra part is one more thing to label, sort, and match correctly in the field), that's a real reason to start from the tetrahedron, not a consolation prize.

**Prompt:**
> Using `design_dome`, compare an icosahedron, an octahedron, and a tetrahedron at the same frequency. How different are the resulting face counts, and why?

**What Comes Back** (three `design_dome` results, `frequency=4`, all Class I, otherwise identical: a snapshot of the first, then the counts from all three):

```json
{
  "vertex_count": 162,
  "edge_count": 480,
  "face_count": 320,
  "truncated": false,
  "bounding_box": {"x": [-1.0, 1.0],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 143.204,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 4,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

```json
{"polyhedron": "icosahedron", "vertex_count": 162,
 "edge_count": 480, "face_count": 320}
{"polyhedron": "octahedron", "vertex_count": 66,
 "edge_count": 192, "face_count": 128}
{"polyhedron": "tetrahedron", "vertex_count": 34,
 "edge_count": 96, "face_count": 64}
```

**What It Means:** `320` faces against `128` against `64` at the same frequency, a ratio of `20:8:4`, or `5:2:1`, unchanged from frequency 1, because all three scale by the same `f²`. None of the numbers is wrong; each answers "how many faces does *this* base shape have at this frequency," and the three never had the same number to begin with. Swap `polyhedron` expecting "the same dome from a different starting point" and you'll get a much coarser (octahedron, tetrahedron) or finer (icosahedron) structure at the same frequency number. Know that before comparing two designs that only look as if they should match.

**Prompt:**
> I want a ring of vertices sitting exactly on the equator before any subdivision happens. Which base polyhedron gives me that?

**What Comes Back:**
> The octahedron. Its vertex layout places four vertices in an exact ring at `Z=0`, at `(1,0,0)`, `(0,1,0)`, `(-1,0,0)`, and `(0,-1,0)`, with the other two at the poles. The icosahedron has no base vertex on `Z=0`; its closest analogue is two five-vertex rings straddling the equator at `Z=±1/√5`, offset from each other by 36°. The tetrahedron has no ring near the equator at all.

**What It Means:** Notice what didn't happen: no subdivision ran, no frequency was picked, nothing was truncated. This is a question about the base polyhedron alone, answerable from `pylair/polyhedral.py`'s vertex coordinates without calling `design_dome`, and exactly the kind of question to ask *before* reaching for a frequency, not after a dome already looks wrong.

**Prompt:**
> I care more about having the fewest possible struts and panels than about roundness. Which base polyhedron should I start from?

**What Comes Back:**
> The tetrahedron. At any frequency it has fewer faces, and so fewer struts and panels, than the octahedron or the icosahedron: `4f²` faces against `8f²` and `20f²`. At frequency 1 the gap is starkest: 4 panels and 6 struts, against the octahedron's 8 and 12 and the icosahedron's 20 and 30.

**What It Means:** It's the same style of question with a different answer. The octahedron won the last one on a specific geometric property (an exact `Z=0` ring); the tetrahedron wins this one on a different property (fewest pieces). Neither is "the alternative" to the icosahedron in some generic sense. Each of pyLair's three starting points earns its place for a distinct, checkable reason, and the job is knowing which reason applies to the design in front of you.

## A Note to File Away Now

pyLair refers to vertices, chords, and faces internally by 0-indexed position in a Python list: vertex `0`, not vertex `1`. Every vertex index this book shows from here on starts at 0, and it's better to find that unsurprising now than to rediscover it three chapters from now.

## What's Next

The AI Henchman, asked once more why the icosahedron, now gave three sentences about uniformity and pressure and none about tutorials. Our Heroine accepted the answer.

Chapter 4 takes the icosahedron and runs a real subdivision over one of its faces, the first piece of geometry pyLair has to *solve* rather than replicate, and gives the Actual Secret Lair its first shape. The Under-the-Ocean Prototype returns in Chapter 8, where it gets squashed slightly, on purpose.
