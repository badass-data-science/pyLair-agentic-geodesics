# Chapter 6: Class III — Going Chiral

The Junior Henchman built two cardboard models over the weekend, one from each of two Class III configurations the AI Henchman had printed out, and set them side by side on the Unbending Foreman's workbench. Same number of triangles. Same strut lengths, to the millimeter. They would not line up. Turn one however you liked and its pattern of struts spiraled the wrong way relative to the other, like a pair of gloves. The Unbending Foreman put on his reading glasses, looked for a long time, and said the word this chapter is about.

Every chapter so far has built toward this one. Class I's grid is symmetric under reflection. Class II's is too: six identical wedges around a centroid, with as much mirror symmetry as an equilateral triangle allows. Class III breaks that symmetry on purpose, and with it introduces the idea this book returns to more than any other: **chirality**. This chapter defines it, builds it into a dome, and shows the limit of every check the last two chapters taught you to trust: a dome can pass them all and still be the wrong shape.

## Chirality, Defined

A shape is **chiral** if it cannot be superimposed on its mirror image by rotation and translation alone: no combination of turning it and sliding it makes it coincide with its reflection. A shape that *can* be is **achiral**. The textbook example is your hands: left and right share every length and angle, and neither can be rotated into the other; you'd have to reflect one first. That isn't a metaphor borrowed for convenience. It's the formal definition, and this chapter applies it to a dome's worth of struts.

Class I and Class II domes are both achiral, and it's worth seeing why. Class I's symmetry triangle is equilateral, and reflecting an equilateral triangle across any of its three medians gives back the same shape. Class II's six-wedge construction is built on the same equilateral face, with three-fold rotational symmetry around its centroid; its mirror image, too, is reachable by rotation. Neither grid has a handedness, so neither finished dome does.

## The (m,n) Construction, and Why It Breaks the Symmetry

Class III, historically the "Skew" method, lays its grid at an angle, and it takes two positive integers, `m` and `n` (pyLair's `frequency` and `n_frequency` parameters), rather than one frequency. The pair sets the dome's **triangulation number**:

```
T = m² + mn + n²
```

This number comes from a family of constructions described by the mathematician Michael Goldberg in 1937, rediscovered by Donald Caspar and Aaron Klug in 1962 to explain the shells of viruses, and connected explicitly to geodesic domes by H. S. M. Coxeter in 1971; Appendix C lists all three. An icosahedral sphere built this way has `20T` triangles, `30T` edges, and `10T+2` vertices. Set `n=0` and `T` reduces to `m²`: Class I's counts from Chapter 3. Class III is the general case, `m≠n` with both positive, and it is where the achiral coincidences of the last two chapters stop holding.

(What about `m=n`? In the Goldberg–Coxeter family, that gives `T=3m²`, the family's own "class II." pyLair's Class II from Chapter 5 is built differently, from LCD triangles: its face count is `120m²` rather than `60m²`, and it has the ten-strut hubs Chapter 5 counted, which a Goldberg–Coxeter sphere never has. pyLair still refuses `m=n` for Class III and points you to its Class II, as you'll see below. The two Class IIs are cousins, not twins.)

Here is a bare Class III symmetry triangle, `(m,n)=(4,1)`, computed by pyLair's `ClassThreeSymmetryTriangle`:

**[IMAGE: examples/images/class3_symmetry_triangle.png | A flat triangle overlaid with a triangular grid that runs at a slant to the triangle's edges, so grid lines cut its sides at odd points.]**
**[CAPTION: A bare Class III symmetry triangle, `(m,n)=(4,1)`, the last of the book's three per-class symmetry-triangle figures. Compare its slanted grid with Class I's parallel grid (Figure 4.1) and Class II's centroid-radiating one (Figure 5.1, right panel).]**

Now build the same `T` the other way, with the parameters swapped, `(m,n)=(1,4)`, and set the result beside the first:

**[IMAGE: examples/images/class3_mirror_pair.png | Two slanted-grid triangles side by side, their grids leaning in opposite directions, mirror images of each other.]**
**[CAPTION: `(m,n)=(4,1)` beside `(1,4)`. Reflecting the left triangle's local x-coordinate maps it onto the right one to within about 10⁻¹⁶, floating-point noise; no rotation of either produces the other. Identical lengths, identical angles, opposite handedness.]**

That relationship wasn't assumed from the formula. It was checked point by point against pyLair's vertex data for both configurations: every point of the `(4,1)` triangle has a partner in the `(1,4)` triangle at the position you get by negating one local coordinate and nothing else, with a residual small enough to be pure roundoff, while the unreflected points miss by about 0.15. `(m,n)` and `(n,m)` are mirror-image constructions of the same lattice, not two triangles that happen to share a name.

## Same Size, Different Pattern

Because `T = m²+mn+n²` is unchanged when you swap `m` and `n`, `(m,n)` and `(n,m)` always give the same `T` and therefore the same golden-value counts. A full-sphere comparison confirms it:

```json
{"m": 4, "n": 1, "vertex_count": 212, "edge_count": 630, "face_count": 420, "total_strut_length": 164.278399}
{"m": 1, "n": 4, "vertex_count": 212, "edge_count": 630, "face_count": 420, "total_strut_length": 164.278399}
```

Both match the golden values for `T=21` (`10(21)+2 = 212`; `30(21) = 630`; `20(21) = 420`), and because mirroring never changes a length or an angle, only handedness, even the total strut length agrees to twelve significant figures. That is the trap this prompt is built to expose:

**Prompt:**
> Build a Class III dome with `f=4, n=1`. Then build one with `f=1, n=4`. Are these the same dome, or mirror images? Do their vertex, edge, and face counts differ?

**What Comes Back:** Mirror images, not the same dome, and no, the counts don't differ at all, by construction. Every golden-value check from Chapters 4 and 5 will report the two as identical, because `T` doesn't change when `m` and `n` swap. Only a check of *which* physical strut pattern resulted (the reflection test above, or the chirality flag Chapter 14 introduces) tells them apart.

**What It Means:** A count-based check answers "is the total amount of material right," never "is the shape the one I meant to build." Those are different questions, and the rest of this chapter shows how far apart they can get.

## Stitching a Chiral Lattice: When Every Count Agrees and the Dome Is Still Wrong

Building a chiral lattice means each polyhedron face computes its grid independently, in its own local coordinates. Because a chiral (`m≠n`) lattice has no reflection symmetry, a point near a face's shared edge generally does **not** land at the same 3D position as the matching point computed by the neighboring face. Classes I and II never have this problem: their grids' mirror symmetry means a shared edge's points, computed from either side, coincide automatically.

So Class III can't stitch its faces together the way Classes I and II do, by matching nearby vertices in 3D with the spatial index Chapter 7 describes. Try it on `(m,n)=(3,2)` and the result is unsettling: the mesh reports the right vertex, edge, and face counts, every golden-value formula passes, and so does Euler's formula. And it's wrong. Thirty of its edges are anomalously long: exactly the base icosahedron's 30 original edges, at full, unsubdivided length, inside a mesh that looks correctly subdivided everywhere else. Proximity merging can't see across a chiral face boundary, and each original edge is left as one long chord passing for a finished structure.

This is the sharpest illustration in the book of a distinction worth taking to every geometry tool you use: **a count-based check like Euler's formula or a golden value can only catch a *count* error. It cannot catch a *shape* error that preserves the counts.** Chapter 5's check is a valuable habit, and it would say nothing was wrong here, because nothing about the vertex, edge, and face bookkeeping is. The Rival's chatbot, for the record, had never run either kind of check.

## How pyLair Stitches It, and How Its Authors Check It

pyLair (`pylair/class_three.py`) stitches Class III faces combinatorially instead. Each grid point's position in the lattice is encoded as a three-part integer index; for two faces sharing an edge, the indices are rotated into a common frame, where a point on one face and a point on its neighbor are the *same physical vertex* whenever their rotated indices sum to a fixed constant. The rule comes entirely from the lattice's structure, with no reference to 3D position. That's why Class III supplies its own `cross_face_matches` *in addition to* the ordinary proximity pass of Chapter 7: proximity still handles the ordinary case, and the combinatorial matches handle the case a chiral lattice makes proximity blind to.

Since counts can't vouch for this construction, pyLair's authors checked it against something that isn't pyLair. During development they compared it with [`antitile`](https://github.com/brsr/antitile), an independent, separately written implementation of the same Goldberg–Coxeter construction, matching the full sorted, mean-normalized edge-length distribution for several `(m,n)` pairs on both the icosahedron and the octahedron. The two agreed to within 10⁻¹⁵: close enough that either both are correct or both are wrong in the same way.

The test suite then keeps a shape check alongside the count checks. Beside Euler's formula and the golden values, it requires that a Class III `(3,2)` sphere's longest strut be less than twice its shortest (antitile's own ratio for that pair is about 1.35), a test thirty unsubdivided edges would fail at once, and that every vertex sits at the requested radius. That is the kind of independent verification Chapter 5's Euler check can't provide, and the pattern Chapter 24 asks you to make a habit.

## Class III's Guardrails

Two of Class III's validation rules are worth triggering once, as Chapter 5 did for Class II.

**Prompt:**
> Ask `design_dome` for a Class III dome at frequency 3 without giving it an `n_frequency`. What happens?

**What Comes Back** (a tool error; through MCP it carries the "Error executing tool design_dome:" prefix):

```
-c 3 (Class III / Skew) requires -n or --n-frequency. Exiting.
```

**Prompt:**
> Now give it `n_frequency=3` too, the same as the frequency.

**What Comes Back:**

```
-c 3 (Class III / Skew) requires --n-frequency to differ from --frequency
(equal values are Class II -- use -c 2 instead). Exiting.
```

The second message is worth reading carefully. It isn't only refusing an edge case: `m=n` has no handedness, so there is nothing chiral left to build, and pyLair sends you to its own achiral alternative, the Class II of Chapter 5.

## The Actual Secret Lair, Chiral at Last

The running dome gets its subdivision here: Class III, `(4,1)` rather than its mirror `(1,4)`, a deliberate choice, since this chapter has just shown the two are not interchangeable. Our Heroine liked the way its struts spiral. She also liked that every hub joins five or six struts, with no ten-socket connectors for the Unbending Foreman to dread.

**Prompt:**
> Switch our running dome to Class III with `(m,n)=(4,1)` (frequency 4, n_frequency 1, icosahedron, radius 1.0) and preview it.

**What Comes Back** (a `preview_dome` render, `dome_class=3`, `frequency=4`, `n_frequency=1`):

**[IMAGE: examples/images/class3-secret-lair.png | A depth-cued wireframe sphere whose triangles form gently spiraling bands rather than the straight rows of a Class I sphere.]**
**[CAPTION: The Actual Secret Lair's final subdivision: Class III, `(m,n)=(4,1)`, the shape the rest of the book stretches, truncates, costs, exports, and nests onto sheet stock.]**

## What's Next

The Unbending Foreman labeled the two cardboard models "LEFT" and "RIGHT" in marker and put them on a high shelf, where they would come in handy in Chapter 14. "Same parts list," he said, "different building. Remember that when we order panels."

Chapter 7 finishes the pipeline all three classes share: merging the vertices that adjacent faces duplicate, and pushing every still-flat point outward onto a sphere, with Class III's combinatorial matches running alongside the ordinary proximity pass, not instead of it.
