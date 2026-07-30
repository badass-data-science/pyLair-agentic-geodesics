# Chapter 3: Picking a Polyhedron

Every geodesic dome pyLair will ever build starts the same way: not with a sphere, but with something that merely *resembles* one — a plain, flat-faced polyhedron, subdivided later into something rounder. This chapter is about that first, easy-to-skip decision, and about the first of this book's two smaller running examples: **the Under-the-Ocean Prototype**, our heroine's contingency plan for the day the San Diego lease finally, definitively falls through and the secret laboratory relocates somewhere the neighbors can't file noise complaints about it. A pressure hull doesn't forgive a shape chosen carelessly, and neither, properly, should you.

## Why Start From a Polyhedron At All

A sphere is the one shape geodesic design is trying to approximate, and also the one shape it never actually starts from. The reason is practical, not aesthetic: a true sphere has no natural way to divide itself into a repeating pattern of identical (or nearly identical) flat triangular panels. A **polyhedron** — a solid built entirely from flat faces — does. Subdivide one face into a fine triangular grid, replicate that same grid onto every other face, and project the whole result outward onto a sphere of the radius you want, and you get a dome built from many small, structurally efficient triangles instead of a few enormous, weak ones. Chapters 4 through 7 walk through exactly how that subdivision and projection actually work. This chapter is about the step before all of that: which polyhedron to start from in the first place.

The geometric logic for *why* the starting shape matters is straightforward once stated: the closer your starting polyhedron already is to a sphere, the less work — and the less resulting variety in strut length and hub angle — the subsequent subdivision has to do to get the rest of the way there. A polyhedron with many, more nearly-triangular, more evenly-arranged faces to begin with needs a gentler grid laid over each one to end up looking spherical; a polyhedron with few, large faces needs a much more aggressive one, and pays for it in more distinct part types at a given frequency. pyLair gives you exactly two starting points, and they sit at genuinely different points on that spectrum.

## Two Starting Points: Icosahedron and Octahedron

pyLair's default, and the shape nearly every geodesic dome you've ever seen a photo of actually uses, is the **icosahedron**: 20 triangular faces, 12 vertices, 30 edges. Selected explicitly:

```
pylair -o base-icosahedron -f 1 -p icosahedron -r 1.0 -P
```

*(Figure 3-1: A bare, unsubdivided icosahedron — `pylair`'s default base polyhedron, real `-P` output at frequency 1, before any subdivision is applied.)*

![A bare icosahedron, 12 vertices and 20 triangular faces](examples/images/base-icosahedron.png)

pyLair's other option is the **octahedron**: 8 triangular faces, 6 vertices, 12 edges — a coarser starting point, selected with `-p octahedron`:

```
pylair -o base-octahedron -f 1 -p octahedron -r 1.0 -P
```

*(Figure 3-2: A bare octahedron — pyLair's other base polyhedron, at the same frequency and radius as Figure 3-1 for a direct comparison.)*

![A bare octahedron, 6 vertices and 8 triangular faces](examples/images/base-octahedron.png)

Both of these are real `design_dome` results, at frequency 1 (meaning: no subdivision at all yet, just the base polyhedron itself, reported through the same pipeline as every other dome in this book):

```json
{"polyhedron": "icosahedron", "vertex_count": 12, "edge_count": 30, "face_count": 20}
{"polyhedron": "octahedron",  "vertex_count": 6,  "edge_count": 12, "face_count": 8}
```

Twenty faces against eight, at the exact same frequency, before either shape has been subdivided even once. That gap doesn't close as frequency rises — it multiplies.

## The Golden-Value Formulas, as a Sanity Check, Not Folklore

Every subdivision class this book teaches (Chapters 4 through 6) produces its own exact vertex/edge/face-count formula in terms of frequency, and every one of those formulas is built on top of one of two base counts, depending which polyhedron you started from. For the plain, unsubdivided base shapes themselves — Class I at frequency `f`, before any further multiplier — the counts are:

| | Icosahedron | Octahedron |
|---|---|---|
| Faces | `20f²` | `8f²` |
| Edges | `30f²` | `12f²` |
| Vertices | `10f²+2` | `4f²+2` |

These aren't folklore or a rule of thumb — they're the same identities pyLair's own test suite checks a real build against (`tests/test_api.py`), and you can verify the table's own `f=1` row by hand against the two JSON results above: `20(1)²=20` faces for the icosahedron, `8(1)²=8` for the octahedron, matching exactly. You'll use the icosahedron half of this table constantly starting in Chapter 4; the octahedron half exists for the same reason the octahedron itself does — for the one design situation, below, where it's actually the better starting shape.

## Choosing Deliberately, Not by Habit

Reaching for the icosahedron by default (which is also what happens if you don't pass `-p` at all) is the right call most of the time — more faces at the same frequency means a gentler grid per face, which generally means a rounder-looking result and less strut-length variety for a given amount of subdivision effort. But "the default is usually right" is a different claim from "the default is always right," and this chapter's actual job is teaching you to notice the one case where it isn't.

Look again at Figure 3-2's octahedron. Two of its six vertices sit at the poles — directly "above" and "below" the shape along Z — and the other four sit in an exact ring around the middle, all at `Z=0`: `(±1,0,0)` and `(0,±1,0)`, in pyLair's own coordinate construction (`pylair/polyhedral.py`'s `Octahedron` class). That's not an approximate equator — it's an exact one, present in the base shape before any subdivision or truncation has touched it at all.

The icosahedron's own vertex layout (`pylair/polyhedral.py`'s `Icosahedron` class) is different, and worth understanding precisely rather than by vague impression: one vertex sits at the north pole, one at the south, and the remaining ten split into two rings of five, sitting at `Z = ±1/√5 ≈ ±0.4472` — close to the equator, and considerably flatter than the poles-and-nothing-else arrangement a naive guess might expect, but not sitting exactly *on* `Z=0` the way the octahedron's four-vertex ring does. It's a genuinely different shape near the equator, not just a denser version of the same one: a pentagonal antiprism of two offset five-vertex rings, versus a single square ring sitting exactly at the midline.

This is exactly the distinction **the Under-the-Ocean Prototype** cares about. A pressure hull wants a shape that's as close to uniformly spherical as possible — no single weak axis, no seam the water pressure can concentrate against — and Chapter 9 will need to truncate this exact design along its Z axis to give it a flat mounting face for a real airlock. An octahedron's exact equatorial ring gives that later truncation something clean and already-planned-for to cut along; the icosahedron's offset double ring is closer to what a truncation cut has to fight through less cleanly at the same frequency. Chapter 9 picks this exact tradeoff back up with real cutoff numbers once truncation itself has been taught; for now, the point is narrower and worth fixing firmly before moving on: **this is a real geometric property of the base shape you pick, present before a single subdivision step runs, and it's worth choosing on purpose rather than never noticing it was a choice at all.**

**Prompt:**
> Using `design_dome`, compare an icosahedron and an octahedron at the same frequency. How different are the resulting face counts, and why?

**What Comes Back** (two real `design_dome` results, `frequency=4`, both Class I, otherwise identical parameters):

```json
{"polyhedron": "icosahedron", "vertex_count": 162, "edge_count": 480, "face_count": 320}
{"polyhedron": "octahedron",  "vertex_count": 66,  "edge_count": 192, "face_count": 128}
```

**What It Means:** `320` faces against `128`, at the identical frequency — a ratio of exactly `20:8`, i.e. `5:2`, unchanged from frequency 1, because both counts scale by the same `f²` factor. Neither number is wrong; they're answering "how many faces does *this* base shape have at this frequency," and the two base shapes never had the same number of faces to begin with. A reader who swaps `-p` expecting "the same dome, just from a different starting point" will instead get a meaningfully coarser (octahedron) or finer (icosahedron) structure at that same frequency number — worth knowing before comparing two designs that only look like they should match.

**Prompt:**
> I want a natural flat ring near the equator before any truncation happens — which base polyhedron gets me closer to that for free?

**What Comes Back:**
> The octahedron. Its own vertex layout already places four vertices in an exact ring at `Z=0` — `(1,0,0)`, `(0,1,0)`, `(-1,0,0)`, `(0,-1,0)` — with the remaining two vertices sitting at the poles. The icosahedron has no vertex sitting exactly on `Z=0` at all; its closest analogue is two five-vertex rings straddling the equator at `Z=±1/√5`, offset from each other by 36°. If a flat, already-present equatorial ring matters more to your design than the icosahedron's usual advantage (more faces, and therefore a rounder look, at the same frequency), the octahedron is the deliberate choice — not a fallback for when the default "doesn't work."

**What It Means:** Notice what didn't happen in that answer: no subdivision was run, no frequency was picked, nothing was truncated. This is a question about the base polyhedron alone, answerable from `pylair/polyhedral.py`'s own vertex coordinates before `design_dome` even needs to be called — exactly the kind of question this chapter exists to make sure you know to ask *before* reaching for a frequency number, not after a dome already looks wrong.

## A Note Worth Filing Away Now

pyLair's vertices, chords, and faces are all referenced internally by plain, 0-indexed position in a Python list — vertex `0`, not vertex `1` — matching how every downstream calculation in the codebase actually uses them. This wasn't always true: an earlier version of this exact codebase numbered vertices starting at 1 and subtracted 1 at every point of use instead, a real, since-cleaned-up historical footgun documented in `AGENTS.md`'s standing engineering guidance for this project. Nothing in this chapter depends on that history — but every vertex index this book shows you from here forward starts at 0, and it's worth having that be unsurprising rather than something you re-discover the hard way three chapters from now.

## What's Next

Chapter 4 picks the icosahedron back up as this book's own default and finally runs a real subdivision over one of its faces — the first piece of geometry pyLair actually has to *solve*, rather than just replicate. The Under-the-Ocean Prototype's octahedron detour stays on the shelf until Chapter 8, once there's an actual pressure-symmetric shape worth elongating, and Chapter 9, once there's a real cutoff worth choosing along that exact equatorial ring.
