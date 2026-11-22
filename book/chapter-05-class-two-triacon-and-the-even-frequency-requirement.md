# Chapter 5: Class II — Triacon and the Even-Frequency Requirement

A copy of the Rival's vertex list reached the Secret Lab™ by the usual channels: a disgruntled henchman, a USB stick, a modest fee. The Foreman counted its vertices, edges, and faces with the patience of a man who had been lied to by spreadsheets before, and wrote the arithmetic on the whiteboard: vertices minus edges plus faces came to 14. "For a closed dome," he said, "that number is 2. It is always 2." The Rival's dome had failed before a single strut was cut. Nobody had done the subtraction.

Chapter 4 taught the simplest symmetry triangle: a grid drawn parallel to a face's edges. This chapter's subdivision, Class II, historically called the "Triacon" method, starts from a different idea, not just a different-looking grid. It's also where the book teaches its first correctness check worth carrying well beyond pyLair: using Euler's formula to catch a bug a glance at a rendered dome would never reveal.

## A Different Construction, Not a Different Decoration

Class I subdivides a polyhedron face directly. Class II does something else first: before any frequency grid is laid down, **each face is split into 6 smaller right triangles around its centroid**, one for each pairing of a face vertex with the midpoint of an adjacent edge. pyLair calls these the face's LCD (lowest common denominator) triangles. Here is that split on one icosahedron face:

**[IMAGE: examples/images/class2_symmetry_triangle.png | Two panels. Left: an equilateral triangle divided into six right triangles that meet at its center. Right: one of those right triangles, divided by a frequency-3 grid into small, skewed triangles.]**
**[CAPTION: Class II's construction. Left: one polyhedron face split into its 6 LCD sub-triangles, before any frequency grid is applied. Right: one sub-triangle with its frequency-3 grid, the symmetry triangle Class II computes and replicates 6 times per original face. Compare its skewed shape with Class I's equilateral grid in Figure 4.1: the two classes' symmetry triangles are differently *shaped* triangles to begin with.]**

Each of the 6 wedges is a right triangle, with legs running from a face vertex to an adjacent edge's midpoint, and from that midpoint to the centroid. The right angle sits at the midpoint because, in an equilateral triangle, the line from a vertex to the midpoint of the opposite side (the median) is also perpendicular to that side (the altitude). pyLair's `build_lcd_faces` builds these 6 triangles per face; `ClassTwoMethodOneSymmetryTriangle` then computes a frequency-`m` grid for **one** of them. It's the same "compute one, replicate the rest" principle as Chapter 4, with 6 copies per original face instead of 1.

This is why Class II's frequency behaves differently from Class I's. **Each original polyhedron edge is already split once, at its midpoint, by the LCD construction itself**, before the frequency-`m` grid subdivides anything. Ask for the same nominal frequency `f` in both classes, and Class II starts one subdivision step ahead. pyLair accounts for this by treating the requested `frequency` as `2m` for Class II, which is also why Class II frequencies must be even.

## Why Frequency Must Be Even

An odd frequency has no valid `m` for Class II to use, and pyLair refuses rather than guessing:

**Prompt:**
> Try building a Class II dome at frequency 3. What error do you get, and why does frequency have to be even here?

**What Comes Back** (the same error through the CLI or through `design_dome`, since both share `pylair/api.py`'s validation; through MCP it carries Chapter 2's "Error executing tool" prefix):

```
-c 2 (Class II / Triacon) requires an even --frequency. Exiting.
```

**What It Means:** Frequency 3 has no integer `m` (`m = f/2 = 1.5`), and there's no sensible way to lay a fractional grid over an LCD triangle. The fix is never to round. Pick the even frequency that reflects the detail you want (2 or 4, not 3), knowing Class II's `m` will be half of it.

## The Golden-Value Formulas, and a Surprise

With `m = f/2`, Class II's golden values for an icosahedral sphere are:

| | Formula (in terms of `m`) | At `f=6` (`m=3`) |
|---|---|---|
| Vertices | `60m²+2` | 542 |
| Edges | `180m²` | 1620 |
| Faces | `120m²` | 1080 |

Compare Chapter 4's Class I table at the *same nominal frequency*, `f=6`: Class I gives `20(6)² = 720` faces; Class II gives `120(3)² = 1080`. **Class II produces more faces than Class I at the same stated frequency, not fewer.** It's easy to get backwards, because "same frequency number" sounds like "same amount of detail," to a reader or an agent, between two classes that happen to share one parameter name.

**Prompt:**
> Check this Class II result against Euler's formula by hand. Does `V - E + F` equal 2?

**What Comes Back** (a `design_dome` result, Class II, `f=6`, trimmed to the counts):

```json
{"vertex_count": 542, "edge_count": 1620, "face_count": 1080}
```

**What It Means:** `542 - 1620 + 1080 = 2`. **Euler's formula**, published by Leonhard Euler in the 1750s, says that for any closed surface topologically equivalent to a sphere, vertices minus edges plus faces equals 2, and it holds here exactly. A second, independent identity is worth checking beside it: every face is a triangle with 3 edges, and every edge borders exactly 2 faces, so a closed triangulated mesh must have `2 × edges = 3 × faces`. Here, `2(1620) = 3240` and `3(1080) = 3240`. Neither check is specific to pyLair or to domes. They're general facts about closed triangulated surfaces, which is what makes them useful: a bug that fools pyLair's own bookkeeping still has to fool two independent mathematical facts.

## The Bug These Two Checks Caught

That isn't hypothetical for this codebase. An earlier version of `ClassTwoMethodOneSymmetryTriangle` had a real bug, and how it was found shows *why* Euler's formula is worth checking rather than trusting a rendered preview.

Here is the comment that now sits in `ClassTwoMethodOneSymmetryTriangle` (`pylair/symmetry_triangle.py`):

> Unlike Class I's equilateral triangle (where vertex-to-centroid happens to be perpendicular to the opposite edge, since median=altitude there), this LCD triangle's x_dir/y_dir are NOT orthogonal, so solve for each point's (a, b) in that actual oblique basis rather than assuming an orthonormal one.

pyLair places each grid point by moving along two direction vectors from an origin. In Class I's equilateral triangle, the two natural directions happen to be at right angles, so placing points as if they were independent, perpendicular axes just works. Class II's LCD triangle is a 30-60-90 right triangle, and its two natural directions are *not* perpendicular. An earlier implementation reused Class I's perpendicular-axes approach anyway, assuming the same convenient coincidence would hold. It doesn't.

The result wasn't a crash or a visibly mangled shape; a preview would have looked plausible enough to wave through. What it failed was **Euler's formula** and `2E = 3F`, immediately, the moment anyone checked, as the repository's README records, before the golden-value formulas above were even known. That's why this chapter teaches the check as a habit rather than a footnote: a construction can be wrong in a way that looks fine and still fail a five-second arithmetic check, and the only way to catch it is to run the check.

The fix replaced the assumption with the real geometry: build the LCD triangle's two direction vectors as they are, and solve a 2×2 linear system (`np.linalg.solve(basis, ...)`) for each grid point's position in that oblique basis. Euler's formula has held on every Class II configuration checked since, a stronger claim than "it held once."

## Continuing the Actual Secret Lair

The dome from Chapter 4 is rebuilt here, at the same nominal frequency, under Class II.

**Prompt:**
> Rebuild that same dome (frequency 6, icosahedron, radius 1.0), but switch it to Class II and preview it.

**What Comes Back** (a `preview_dome` render, `dome_class=2`, `frequency=6`):

**[IMAGE: examples/images/class2-secret-lair.png | A depth-cued wireframe sphere, visibly denser than the Class I sphere at the same frequency, with clusters of triangles radiating from points where six or five struts meet.]**
**[CAPTION: The Actual Secret Lair, same nominal frequency as Figure 4.2, rebuilt under Class II: 1,080 faces against 720, the "same frequency number, more detail" surprise the golden-value table predicts.]**

Neither version is more correct; they're two valid subdivision strategies for the same polyhedron. Which one the Actual Secret Lair ships with isn't settled until Chapter 6 offers a third.

## What's Next

The Foreman added a line to the whiteboard under the Rival's 14: "V − E + F = 2, and 2E = 3F. Check both. Every time." The AI Henchman, asked to add both checks to its routine, did so without being told twice, and then, unprompted, checked Chapter 4's dome as well.

Chapter 6 introduces Class III, a subdivision whose grid is **handed**: its mirror image is a different, equally valid dome, not the same one rotated. It's also home to the book's most important gotcha, one that passes both of this chapter's checks and is still wrong.
