# Chapter 9: Cutting a Dome From a Sphere — Truncation

The Chief Financial Villain's question from the end of Chapter 8 stood on the whiteboard in her neat capitals: WHO IS PAYING FOR THE BOTTOM HALF? Nobody, was the answer. A crater floor is flat, the Secret Lab™ needs a floor to stand on, and half an ellipsoid buried in volcanic rock is a very expensive way to hold up nothing. The bottom half had to go.

Every dome so far has been a complete sphere or ellipsoid: structurally interesting, not yet a *building*. Nothing in Chapters 3 through 8 has a floor. This chapter adds one with **truncation**, the operation that slices a finished shape at a chosen height and keeps only the part above it. It's also home to the book's most dramatic failure mode so far, a refusal rather than a silent mistake, and an ordering subtlety worth getting right before Chapter 10 complicates it.

## What a Cutoff Fraction Measures

`truncation_z`, and its siblings `truncation_x` and `truncation_y` (covered later in this chapter), each take a number between 0 and 1: the fraction of that axis's range, measured from the bottom, above which everything is kept. `truncate()` makes this precise. For the chosen axis, it finds the lowest and highest vertex coordinate across the whole shape and computes:

```python
cutoff = min_value + (
    cutoff_from_bottom
    * (max_value - min_value))
```

Everything at or above `cutoff` survives; everything below is discarded; and any chord or face straddling the cutoff plane is clipped at the crossing point (Chapter 10 covers what happens to a clipped face). A cutoff of `0.5` keeps the top half of whatever range the axis currently has; `0.0` keeps everything; a cutoff near `1.0` keeps a thin cap at the top.

## The Flat-Chord Failure, Reproduced

Here is the danger this chapter teaches you to recognize, shown as it happens. Take a plain, unelongated Class I icosahedral sphere at frequency 6.

**Prompt:**
> Truncate this dome at exactly `truncation_z=0.5`.

**What Comes Back** (a tool error, not a crash):

```
Truncation cutoff plane lies exactly on a
chord that is flat along the cutoff axis.
Choose a slightly different truncation value
to avoid this degenerate case.
```

This isn't a bug. It's `truncate()` refusing to do something it can't do safely. A chord lying exactly in the cutoff plane, with both endpoints at the same coordinate on the truncation axis, has no single crossing point. Computing one would mean dividing by the chord's zero extent along that axis and silently producing a vertex at infinity or "not a number." `truncate()` checks for this case and refuses instead.

**[IMAGE: examples/images/truncation_safe_vs_unsafe.png | Two scatter plots of vertex heights. Left: all 362 vertices of the sphere by Z-coordinate. Right: a zoom to within one hundred-thousandth of Z=0, showing 30 vertices exactly at zero, the 0.5 cutoff line passing through them, and the 0.499999 cutoff line just below.]**
**[CAPTION: Every vertex of the frequency-6 sphere, plotted by its Z-coordinate. Left: the full range. Right: zoomed to ±10⁻⁵ around Z=0, where 30 vertices sit at *exactly* Z=0, which is where a cutoff of `0.5` lands. The documented safe cutoff, `0.499999`, clears that ring by `2×10⁻⁶`: a hair's breadth, not a generous margin.]**

Why does this sphere have a ring of vertices exactly on its equator? A sweep across frequencies shows the pattern: on the icosahedral Class I sphere, `truncation_z=0.5` fails at every *even* frequency from 2 through 10 and succeeds at every odd one. An even frequency's grid puts a full ring of vertices on the midplane; an odd one doesn't. (Chapter 3 promised this: even without the octahedron's built-in equator, subdivision can create one.) That's why pyLair's documentation recommends `0.499999` or `0.333333` over rounder numbers: both are chosen to miss the vertex rings that typical frequencies produce.

**Prompt:**
> Truncate this dome at the equator on Z only, using the documented safe cutoff. Then try `0.5` exactly. What happens, and why?

**What Comes Back** (a snapshot of the `design_dome` result at `0.499999`, then the error at `0.5`):

```json
{
  "vertex_count": 256,
  "edge_count": 705,
  "face_count": 450,
  "truncated": true,
  "bounding_box": {"x": [-0.9942, 0.9942],
                   "y": [-1.0, 1.0],
                   "z": [-2.00e-06, 1.0]},
  "height": 1.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 123.569,
  "resolved_parameters": {
    "radius": 1.0,
    "frequency": 6,
    "polyhedron": "icosahedron",
    "dome_class": 1,
    "truncation": {"x": null, "y": null,
                   "z": 0.499999},
    ...
  }
}
```

```
Truncation cutoff plane lies exactly on a
chord that is flat along the cutoff axis.
Choose a slightly different truncation value
to avoid this degenerate case.
```

`0.499999` succeeds, leaving 256 vertices. `0.5` raises the flat-chord error above, because this frequency places a ring of vertices exactly on the cutoff plane. Moving the cutoff by `0.000001`, imperceptible on a physical build and decisive to a floating-point comparison, is the whole fix.

**What It Means:** The safe values aren't magic; they're deliberately a little off round, because round fractions are where a symmetric construction's vertex rings are most likely to sit. Be clear about what that guarantees. It's a mitigation earned by testing, not a proof that no shape could ever put a ring at `0.499999`. A sweep of every base polyhedron at frequencies 1 through 20, Classes I and II, found no failure at either safe value: useful evidence, not universal immunity. And clearing a ring by a hair has its own consequence, which Chapter 16 takes up.

## Truncating the Actual Secret Lair

The running dome (Class III `(4,1)` from Chapter 6, stretched `1.8`× on Z in Chapter 8) gets its floor here, sliced at the documented safe value.

**Prompt:**
> Truncate our running dome at `truncation_z=0.499999`, preview it, and give me its summary.

**What Comes Back** (a `preview_dome` render, captioned "156 vertices, 415 struts (truncated)", then a snapshot of `design_dome`'s JSON: 156 vertices, 415 struts, and 260 faces, a height of `1.8` and a footprint diameter of about `1.98` at radius 1):

**[IMAGE: examples/images/truncated-secret-lair.png | A depth-cued wireframe of a tall dome standing on a flat circular base, its triangles spiraling gently up to the crown.]**
**[CAPTION: The Actual Secret Lair, ground-flush at last: Class III `(4,1)`, stretched 1.8× on Z, truncated at the documented safe cutoff. For the first time it looks like a building.]**

```json
{
  "vertex_count": 156,
  "edge_count": 415,
  "face_count": 260,
  "truncated": true,
  "bounding_box": {"x": [-0.9898, 0.9929],
                   "y": [-0.991, 0.991],
                   "z": [-3.60e-06, 1.8]},
  "height": 1.8,
  "footprint_diameter": 1.9826,
  "total_strut_length": 121.0815,
  "resolved_parameters": {
    "radius": 1.0,
    "frequency": 4,
    "polyhedron": "icosahedron",
    "dome_class": 3,
    "n_frequency": 1,
    "elongation_factors": {
      "x": 1.0, "y": 1.0, "z": 1.8
    },
    "truncation": {"x": null, "y": null,
                   "z": 0.499999}
  }
}
```

Notice that the truncated dome is as tall as the full sphere was wide: the 1.8× stretch on the upper half alone gives a height of 1.8 radii on a footprint of 2. That is where the particle accelerator goes.

The DXF export of a truncated dome, opened in a CAD (computer-aided design) program, looks like this; Chapter 17 covers the export itself:

**[IMAGE: ../blog-posts/truncated_qcad_focused.png | A bright green wireframe of a truncated geodesic dome seen from the side on a black CAD canvas, with horizontal rings of struts.]**
**[CAPTION: A truncated dome's DXF export viewed side-on in the QCad drafting program, from pyLair's earlier documentation.]**

## Combining Axes: The Order Is Fixed, and It Matters

`truncation_x`, `truncation_y`, and `truncation_z` can be combined, truncating on two or all three axes at once, and pyLair always applies them in a fixed order: **X, then Y, then Z**, whatever order you list the parameters in. That isn't cosmetic. Each axis's cutoff fraction is computed against *that axis's range at the moment its cut runs*, and an earlier cut can remove the vertices that used to define a later axis's range.

Most of the time this is invisible, because a moderate cut on one axis doesn't remove the vertices that set another axis's extremes. But it's a real effect. Take the same frequency-6 sphere and cut it two ways: X first at a deliberately aggressive `0.9`, keeping only the outermost tenth of the X range, then Z at `0.4`; and the reverse.

```json
{"order": "X (0.9) then Z (0.4)",
 "vertex_count": 60, "edge_count": 138,
 "z_range": [-0.1157, 0.6031]}
{"order": "Z (0.4) then X (0.9)",
 "vertex_count": 72, "edge_count": 169,
 "z_range": [-0.2000, 0.6031]}
```

Same two fractions, different shapes: different vertex and edge counts, and a different bottom (`-0.1157` versus `-0.2000`). Cutting X first leaves only a sliver near `x = 1`, which no longer includes either pole (both poles sit at `x = 0`), so the Z range shrinks to about `[-0.59, 0.60]`, and 40% of *that* puts the Z cutoff at `-0.1157`. Cutting Z first measures against the full `[-1, 1]`, and 40% puts the cutoff at `-0.2`. Because pyLair always applies X, then Y, then Z internally, this ambiguity never reaches you; it's resolved the same way every time, before you see a result. The numbers show why that fixed order is a load-bearing decision rather than a convention.

**Prompt:**
> Now truncate on X and Z together. Does the order I list `truncation_x` and `truncation_z` in my tool call change the resulting shape?

**What Comes Back:**
> No. pyLair always applies truncation in a fixed X, then Y, then Z order, regardless of the order the parameters appear in your request. What *would* change the shape is which axis is cut first, and that's why the internal order is fixed: each later cut is computed against whatever range the earlier cut left, and reversing the order can produce a measurably different dome from the same two fractions.

**What It Means:** "Does parameter order matter?" and "does truncation order matter?" are different questions with different answers. The first is no, by design; the second is yes, which is why the first answer had to be designed.

## What's Next

The Chief Financial Villain crossed out her question on the whiteboard and wrote 260 beside it: faces, which she now understood to mean panels, which she now understood to mean money. The HOA, meanwhile, had sent its president to look at the sub-basement stairs, "for a routine inspection." Our Heroine said the stairs were being renovated, which was nearly true.

Chapter 10 picks up where this chapter's face clipping leaves off: what happens to a triangular panel when the cut takes off one corner and leaves four sides where there were three, and whether the new seam counts as a real, strutted edge or an invisible bookkeeping line.
