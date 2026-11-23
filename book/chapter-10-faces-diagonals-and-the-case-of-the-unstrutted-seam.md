# Chapter 10: Faces, Diagonals, and the Case of the Un-strutted Seam

The disgruntled henchman who had sold the Secret Lab™ the Rival's vertex list came back with photographs, at a slightly higher fee. The Rival's crew had at least got the bottom ring of his dome standing for a while. Where his chatbot's cut had sliced through triangles, it had left four-sided panels, and the crew had bolted them in as they were, unbraced. A triangle can't change shape without changing a side's length; a four-sided frame folds like a garden gate. The photographs showed the gates folding.

Chapter 9 treated truncation as chord clipping: a strut crossing the cutoff plane is shortened to the crossing point, and for a wireframe that's the whole story. But pyLair's face-aware outputs (`face_output`, `stl`, `obj`, `hub_templates`, `face_templates`, `cost_per_unit_area`, `panel_areal_density`) need more: every clipped *panel* must still be a valid, correctly counted shape. This chapter covers the one easy-to-get-wrong case that requirement creates, and how pyLair's authors check that it comes out right.

## When a Triangle Loses a Corner

Every face on a geodesic sphere is a triangle, and a cutoff plane can leave it three ways: all three corners kept (untouched), none kept (discarded), or one or two kept. The interesting case is keeping **two**. Cut off a single corner and what remains is no longer a triangle; it's a quadrilateral, four sides where there were three.

pyLair's bill of materials, its DXF, STL, and OBJ exports, and its cutting templates all assume every panel is a triangle, so a clipped quadrilateral can't be reported as is. pyLair's `_clip_face` splits it into two triangles along a diagonal drawn from one of the two new crossing points:

**[IMAGE: examples/images/diagonal_seam.png | Two diagrams of one triangle. Left: a horizontal cutoff line about to clip off one corner. Right: the four-sided remainder divided into two triangles by a diagonal running from one new corner point to the opposite kept corner.]**
**[CAPTION: One triangular panel, magnified. Left: a cutoff plane about to clip one corner. Right: the resulting quadrilateral, split into two triangles along a new diagonal, the seam this chapter is about.]**

Two details matter here, because getting either wrong would quietly corrupt the output. First, the two new corner points (`Pa` and `Pb` in the figure) come from the same crossing function Chapter 9's chord clipping uses, `_edge_crossing`, shared between the chord path and the face path so that a strut along the cut and the panel corner at the same physical point land on *identical* coordinates, not two separately rounded near-duplicates. Second, the diagonal (`Pa` to `kept2` in the figure) isn't a drawing convenience. Both sub-triangles lie in the same plane as the original triangle (a straight cut through a flat shape can only produce flat shapes), so the diagonal is a real, buildable edge, and bracing it is exactly what keeps the Rival's garden gate from folding.

## The Seam Is a Strut, Not Just a Panel Edge

A diagonal that exists only in the panel data is an easy thing to get wrong, because leaving it out breaks nothing visible. The split's areas and edge lengths would still be right, and the panels would still look right in a preview. But the seam would have no strut length in the bill of materials, no bevel angle in the panel-edge report, nothing a builder would see as a part to cut and install: the Rival's garden gate, in data form.

So `_clip_face` reports the diagonal as a new chord alongside the panel split, and it flows through the same strut-length, bill-of-materials, and bevel-angle machinery as every other edge (the machinery Chapters 12 and 13 cover). pyLair's tests check this from two directions that don't share code. One clips a single triangle and requires the diagonal to appear in the chord list. The other builds a whole truncated dome, then requires every edge of every panel to name a real strut (the strut–panel cross-reference Chapter 22 introduces). A third check, run when the optional `verify` extra is installed, compares pyLair's clipped panels with an independent library's own mesh-slicing routine, `trimesh`.

## Seeing It: Two Cuts on One Sphere

The honest way to produce this case, rather than contrive one, is to truncate aggressively enough on two axes that plenty of triangles lose a corner: a frequency-6 Class I sphere cut on X (`0.9`) and Z (`0.4`) together, the same dome Chapter 9 used to show truncation order.

**Prompt:**
> Truncate this dome with `truncation_x=0.9` and `truncation_z=0.4` and check its bill of materials. Do the diagonal seams show up as real struts?

**What Comes Back** (a snapshot of the `get_bill_of_materials` report; the bevel-angle section shows its first entry and the entry for the seam between hubs `24` and `2`):

```json
{
  "pyLair report": {
    "Bill of materials": {
      "Chord Lengths and Counts": [
        {"length": 0.2159, "count": 2,
         "chord_indices": [81, 92]},
        ...
      ],
      "Warning": "Small length chords...",
      "Possible truncation-artifact chords": []
    },
    "Total material": {
      "Total strut length": 20.2514
    },
    "Angles at hub between outbound cords and tangential plane": [
      {"hub": 0, "connecting hub": 1,
       "angle (degrees)": 4.6624, ...},
      ...
    ],
    "Spoke angles": [
      {"index": 0, "hub": 0, "connecting hub": 1,
       ...},
      ...
    ],
    "Panel shapes and counts": {
      "Panel Types and Counts": [
        {"edge_lengths": [0.198, 0.203, 0.206],
         "area": 0.018, "count": 8, ...},
        ...
      ],
      "Warning": "Panels sharing the same...",
      "Possible truncation-artifact panels": []
    },
    "Total panel material": {
      "Total panel area": 0.7734
    },
    "Bevel angles at panel edges": [
      {"vertex 1": 0, "vertex 2": 1, "face 1": 0,
       "face 2": 6,
       "dihedral angle (degrees)": 173.2405,
       "bevel angle (degrees)": 3.3797},
      ...,
      {"vertex 1": 24, "vertex 2": 2, "face 1": 2,
       "face 2": 3,
       "dihedral angle (degrees)": 180.0,
       "bevel angle (degrees)": 0.0},
      ...
    ]
  }
}
```

**What It Means:** Yes. Chord `(24, 2)` is an ordinary entry in this dome's chord list, with a strut length (`0.170` units at radius 1) computed like every other strut's. It isn't flagged, hidden, or treated specially in the report, and neither are the other 16 seams like it in this dome. That's the design: a builder reading the bill of materials never needs to know that this strut came from a clipped panel's diagonal rather than the original subdivision.

## Why a 180° Reading Here Is Correct, Not a Bug

**Prompt:**
> What bevel angle would you expect for that seam, and why does a 180° dihedral reading there mean the geometry is correct, not broken?

**What Comes Back:**
> A `180°` dihedral angle and a `0°` bevel, and that's the geometrically necessary answer, not a coincidence. The dihedral angle is the angle between two panels at their shared edge, and the bevel is how far they bend away from lying flat against each other; `180°` means coplanar, needing no bevel cut to sit flush. Both of this diagonal's sub-triangles were carved from the *same* original triangle by one straight cut. They were flat against each other before the cut, and a straight cut can't introduce a bend. Any reading other than `180°` here would mean something had gone wrong.

**What It Means:** Hold on to this as a habit: an unusual-*looking* number, like a `0°` bevel when most of this dome's struts bevel by several degrees, isn't automatically a red flag. Chapter 16 teaches the opposite case, a near-zero value that *is* wrong (a truncation-artifact sliver), and the two are worth telling apart on sight. A `0°` bevel on a diagonal between two coplanar sub-triangles is guaranteed correct; a near-zero panel area or strut length elsewhere in the same report deserves a second look.

## Multi-Axis Truncation Still Composes Correctly

One more thing to confirm rather than assume. Chapter 9 showed that sequential cuts matter because each later axis measures its cutoff against the range the earlier cut left. The same sequential logic handles a face that an earlier cut already split. When the second axis's `truncate()` runs, it doesn't know or care that a triangle in front of it used to be half of a quadrilateral; it clips whatever triangle it's given, computing fresh crossing points against the *current* geometry, diagonal seams included, with the same `_edge_crossing` and `_clip_face`. There's no separate code path for "a face that has already been through one cut"; it's the same function, called again, on what the previous call produced.

## What's Next

The Unbending Foreman pinned the Rival's photographs beside the whiteboard, under a new line: "Every quad gets a diagonal. pyLair already knows." The Actual Secret Lair's own base, cut once on Z, has its clipped triangles split the same way.

Chapter 11 is a practicum rather than a new feature: applying everything from Chapters 3 through 10 (polyhedron, subdivision class, elongation, truncation) to a run of design commissions from other villains, each with its own environment. Part IV then returns to the bill of materials in full, starting with the angles at the hubs.
