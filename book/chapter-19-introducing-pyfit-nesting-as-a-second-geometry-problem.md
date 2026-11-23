# Chapter 19: Introducing pyFit — Nesting as a Second Geometry Problem

The Junior Henchman stood in front of the first sheet of plywood with 52 panel templates, a pencil, and a question nobody in Parts II through V had answered: where does each piece *go*? They tried laying the templates out by hand. The first sheet held nine panels and a great deal of offcut. The Chief Financial Villain, passing through, did the arithmetic for 260 panels and stopped passing through.

Every dome in this book now has an answer for its shape, its subdivision, its struts and panels, and its files. What none of that answers is the question a henchman in front of a sheet of plywood has. This part of the book is about **pyFit**, a separate project from pyLair that shares nothing with it but a file format, built to answer that question.

## A Standalone Tool That Happens to Read pyLair's Files

pyFit has no code dependency on pyLair. It reads DXF files (pyLair's panel templates, another program's, or a hand-drawn shape) or plain lists of corner points, and arranges however many copies of each you need onto rectangular sheets, wasting as little material as it can. A henchman payroll generates plenty of 2D cutting problems unrelated to domes (uniform patches need cutting in bulk, and a good throwing-star stencil doesn't lay itself out), and pyFit doesn't care what the shapes are. Before touching a dome panel, here is pyFit on something that has nothing to do with domes.

**Prompt:**
> Nest a batch of henchman-uniform patch blanks and throwing-star stencils, two shapes and ten parts in all, on a 12×8 sheet, and preview the result.

**What Comes Back** (a `preview_nest` render):

**[IMAGE: examples/images/standalone_patch_stencil_nest.png | A 12-by-8 sheet with ten shapes packed against its left edge, four pentagonal patch blanks and six triangular stencil blanks, leaving most of the sheet empty.]**
**[CAPTION: A pyFit nesting result with nothing to do with domes: pentagonal henchman-uniform patches and triangular throwing-star stencil blanks on a `12×8` sheet, at `23.7%` utilization. pyFit owes nothing to pyLair's geometry.]**

## The Question Underneath: The No-Fit Polygon

Nesting comes down to one geometric question, asked over and over: with one shape already placed, where may a *second* shape go without overlapping it? The **no-fit polygon** (NFP) answers it: the region the moving shape's reference point must stay *outside* to avoid overlapping the fixed one. Inside the NFP, the shapes overlap; on its boundary, they touch; outside, they're clear.

pyFit computes the NFP as a **Minkowski sum**, `NFP(A, B) = A ⊕ (−B)`: the fixed shape swept around by the moving shape reflected through its own reference point. The hand-checkable case this book keeps promising is worth computing rather than taking on trust:

**Prompt:**
> Show me the no-fit polygon of two unit squares. Does it match what you'd expect by hand?

**What Comes Back** (pyFit's `no_fit_polygon` function, called directly on two unit squares):

```python
no_fit_polygon([(0,0),(1,0),(1,1),(0,1)], [(0,0),(1,0),(1,1),(0,1)])
# -> [[(1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0), (1.0, -1.0)]]
```

**[IMAGE: examples/images/nfp_unit_squares.png | A fixed unit square at the center of a larger 2-by-2 square outline, the no-fit polygon, with a second unit square drawn touching it from outside.]**
**[CAPTION: The computed no-fit polygon of two unit squares: the 2×2 square from `(-1,-1)` to `(1,1)`, with the moving square shown touching the boundary at one legal position.]**

**What It Means:** By hand: if the moving square's reference corner is anywhere inside the 2×2 square around the fixed square, the two overlap; on its boundary, they touch edge to edge; outside it, they're clear. The code's output matches exactly, with no rounding: the same kind of hand-checkable test Chapter 4's golden values gave pyLair, applied to a different geometric tool.

## Bottom-Left Fill, Watched in Action

On top of the NFP, pyFit runs a **bottom-left-fill** heuristic: take the largest remaining part first; try a range of rotations (and mirrored versions, unless the part's `allow_mirror` is `false`); find every legal position against everything already placed; and choose the one furthest left, breaking ties by lowest. Here is the loop, watched rather than described.

**Prompt:**
> Nest five identical unit squares on a 3×2 sheet, and give me the full placement report so I can see the order they were placed in.

**What Comes Back** (a `get_nest_report` result, plotted in placement order; the report lists positions `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`, `(2,0)`):

**[IMAGE: examples/images/bottom_left_fill_order.png | Five unit squares on a 3-by-2 sheet, numbered 1 to 5: 1 and 2 stacked in the left column, 3 and 4 in the middle column, 5 at the bottom right; the top-right cell is empty.]**
**[CAPTION: A placement sequence: five unit squares, numbered in the order pyFit placed them, red dots marking each part's reference point. Leftmost first, then lowest: pyFit fills the left column bottom to top, then the next column.]**

Notice that "bottom-left" here means *left first*: square 2 goes on top of square 1 rather than beside it, because a position at `x = 0` beats any position at `x = 1`, however low. It's the kind of detail worth checking against the report rather than assuming from the name.

**Prompt:**
> Explain, in your own words, why nesting a set of triangles onto plywood is a harder problem than computing their shapes in the first place.

**What Comes Back:**
> Computing a triangle's shape is a closed-form calculation: given the inputs, there's one correct answer, computed directly. Deciding where a *set* of shapes goes on a sheet is a combinatorial search. Every part's position depends on every part already placed, the number of possible arrangements grows explosively with the part count, and irregular 2D nesting is NP-hard: no known algorithm finds a provably optimal layout in reasonable time as the problem grows. pyFit doesn't pretend otherwise. Its README calls it a heuristic in the same family as tools like SVGnest and DeepNest, built to find a *good* layout quickly, not to search every possibility for the *best*.

**What It Means:** It's a different kind of correctness claim from anything pyLair makes. A pyLair dome matches its golden values or it doesn't: closed-form, checkable, unambiguous. A pyFit layout is never "the" correct layout, only *a* legal one. Every placement is re-checked for overlap and containment before it's accepted, so pyFit's guarantee is "this layout is valid," never "this layout is optimal." Chapter 24 compares the two kinds of correctness side by side.

## A Documented Gotcha, Told the Way pyLair's Are

`pyclipper.MinkowskiSum` doesn't return one clean polygon. It returns the *raw* swept outlines, and when a small shape is swept around a larger one, one of those outlines can wind the opposite way and *look* like it marks a hole. It can't: the Minkowski sum of two convex, filled shapes is itself convex, and a convex shape has no holes. pyFit's fix (`pyfit/nfp.py`) treats every returned outline as a solid region and merges them with the `shapely` library, ignoring the winding direction.

What makes it worth telling, the way this book has told pyLair's bugs: **this issue passed its first hand-computable test, the two unit squares, cleanly**, and appeared only on a second case with shapes of different sizes (pyFit's `AGENTS.md` records it). One verified case is not a verified method. Chapter 24 sets this beside Class III's stitching bug, which passed checks that were too few in the same way, in an unrelated part of an unrelated codebase.

## What the Search Doesn't Try

One more scope decision, stated as a decision rather than an apology: pyFit's search for candidate positions isn't a full trace of every NFP boundary. It considers the sheet's corners, every NFP corner, and every point where an NFP crosses the sheet's edge or another NFP. That's enough to tile six unit squares onto a `3×2` sheet with no waste, as Chapter 2 showed, which is a tight result. It can still miss an even tighter placement that a full trace might find. The guarantee that never bends: every candidate is re-checked for overlap and containment before acceptance, so the limitation can only produce a *less-than-optimal* layout, never an *invalid* one.

## What's Next

The Junior Henchman's patch blanks came off the laser cutter in one run, and the throwing-star stencils were distributed to the security detail, who had not asked for them.

Chapter 20 builds a job spec directly from the Actual Secret Lair's bill of materials (pyLair's panel templates from `face_templates=True` and their counts become a pyFit job spec's `"dxf"` and `"quantity"` fields with no hand-typing) and nests the Lair's panels for the first time.
