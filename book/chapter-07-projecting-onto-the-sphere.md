# Chapter 7: Projecting Onto the Sphere

"Where two faces meet," said the Unbending Foreman, "I want one hub. Not two hubs a hair apart." He had seen what happens otherwise: a crew fabricates both, bolts one in, and spends a day looking for where the other goes. In a parts list, a vertex that should have been merged and wasn't is a phantom hub, and every phantom hub is a part somebody will make for nothing.

Every subdivision class so far (Class I's parallel grid, Class II's six centroid-radiating wedges, Class III's slanted chiral lattice) ends in the same place: a set of still-flat points on the flat faces of the original polyhedron, not yet anything resembling a dome. This chapter is the step all three share to finish the job: merge what needs merging, then push every point outward onto a sphere.

## Flat, Then Push Outward, in That Order

The process has two steps. First, pyLair's `GeodesicSphere` replicates the symmetry triangle each class computed onto every face of the base polyhedron, rotated into place by each face's transfer matrix. The result is **not yet a sphere**. It's a subdivided version of the original flat-faced polyhedron: every small triangle still lies in the plane of the face it came from, with visible facets and creases along the original edges. Only *after* that flat assembly is finished (chords and faces wired up, duplicate seam vertices merged) does `project_onto_sphere()` take each surviving vertex, normalize it to a unit vector, and scale it to the requested radius. Here is the transition, from pyLair's internal state at a frequency low enough to see clearly:

**[IMAGE: examples/images/projection_before_after.png | Two wireframes side by side. Left: a subdivided icosahedron with flat facets and visible creases along its original edges. Right: the same points pushed out onto a smooth sphere.]**
**[CAPTION: The same Class I icosahedral construction at frequency 3, before and after `project_onto_sphere()`. Left: every small triangle still lies in its original face's plane, so the icosahedron's 20 facets show. Right: every vertex pushed radially to the same radius; the facets are gone.]**

Notice what has to happen *before* the push: **connectivity is settled while the geometry is still flat.** That's an ordering requirement, not an arbitrary choice. Two symmetry-triangle vertices meant to be the same physical point (on an edge shared by two faces, computed independently by each) are recognizably close together only while they sit near each other in the flat assembly. For Classes I and II, merging after projection would still work in principle, since projection moves nearby points to nearby points. But Class III's combinatorial cross-face matches (Chapter 6) are keyed to the flat construction's lattice coordinates, which only mean something before projection replaces them with positions on a sphere. Merge first, project second, every time.

## Why Merging Needs a Spatial Index

The merging step, `locate_duplicate_vertices()`, has an obvious naive implementation: compare every vertex with every other, and merge any pair closer than `vertex_equal_threshold`. That's a comparison count that grows with the *square* of the number of vertices, and at frequencies worth building it's slow enough to notice. Here is a timed comparison on a Class I icosahedral sphere at frequency 16, comparing a plain Python loop over every pair with a k-d tree, a data structure that sorts points by position so that only nearby points get compared:

```
raw (unprojected) vertex count: 3060
pairwise Python loop: 1.75s,
  found 570 duplicate pairs
k-d tree query_pairs: 0.0016s,
  found 570 duplicate pairs
```

Both find the same 570 pairs, so the faster method isn't cutting a corner. On this machine it's about **1,100 times faster** (your timings will differ, the ratio less so), and the gap widens with frequency, because the pairwise loop's cost grows with the square of the vertex count while the tree's grows close to linearly. That's why `locate_duplicate_vertices()` uses `scipy.spatial.cKDTree`'s `query_pairs`.

**Prompt:**
> At a high frequency, how many vertices get merged during the build, and does that number make sense given the golden values?

**What Comes Back** (a snapshot of `design_dome` at frequency 16, then the arithmetic around it):

```json
{
  "vertex_count": 2562,
  "edge_count": 7680,
  "face_count": 5120,
  "truncated": false,
  "bounding_box": {"x": [-1.0, 1.0],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 577.2039,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 16,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

At frequency 16, Class I icosahedron: `3060` raw vertices (`20` faces × `153` symmetry-triangle vertices each, since a Class I symmetry triangle at frequency `f` has `(f+1)(f+2)/2` of them) collapse to the golden-value `2562` (`10(16)²+2`), a reduction of `498`. That isn't the same as the `570` duplicate *pairs* found above. Each of the icosahedron's 12 original vertices is shared by 5 faces, not 2, so its 5 copies form a cluster with several pairwise links among them, and the whole cluster collapses to one vertex rather than being counted pair by pair. `locate_duplicate_vertices()` handles that by grouping linked pairs into clusters (a union-find structure) and keeping one member of each.

**What It Means:** `498` is a checkable number: raw count minus final count should equal the number of points that needed merging, no more and no less. It's worth checking before trusting a high-frequency result. The Unbending Foreman's phantom hubs live in the gap between those two numbers.

## The Safe Zone Narrows as Frequency Rises

Chapter 4 showed `vertex_equal_threshold`'s two failures at frequency 6: too tight (`0.0`) leaves seams cracked; too loose (`0.2`) collapses the dome to one point. Both exist at frequency 16 too, but the safe range between them is narrower, because higher frequency packs vertices closer together.

**Prompt:**
> Set `vertex_equal_threshold=0.1` on both a frequency-6 and a frequency-16 dome. Does it stay safe at both?

**What Comes Back** (two `design_dome` results: a snapshot of the frequency-16 result, then both vertex counts with the golden value added for comparison):

```json
{
  "vertex_count": 1,
  "edge_count": 1,
  "face_count": 1,
  "truncated": false,
  "bounding_box": {"x": [0.8944, 0.8944],
                   "y": [5.55e-17, 5.55e-17],
                   "z": [0.4472, 0.4472]},
  "height": 0.0,
  "footprint_diameter": 0.0,
  "total_strut_length": 0.0,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 16,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

```json
{"frequency": 6, "vertex_equal_threshold": 0.10,
 "vertex_count": 362, "golden": 362}
{"frequency": 16, "vertex_equal_threshold": 0.10,
 "vertex_count": 1, "golden": 2562}
```

**What It Means:** The same threshold is safe at frequency 6 and catastrophic at frequency 16, where it collapses the sphere to a single vertex, the failure Chapter 4 showed only at the looser `0.2` on the coarser dome. At frequency 16 the collapse starts between `0.06` (still correct) and `0.07` (collapsed). The default, `1e-7`, sits so far below either boundary at any frequency this book has tried that it never needs to move. But "the safe zone is wide" is a weaker claim than "the safe zone is infinitely wide": if you widen the threshold for some reason (there isn't a good one), know that the margin shrinks as frequency grows.

## Diagnosing a Cracked Seam: Two Causes, One Symptom

Here is a practical skill this chapter makes possible. If an exported dome shows two hubs where there should be one, the *symptom* looks the same whatever the cause, but the *fix* depends on which of two very different problems produced it.

**Prompt:**
> If two hubs that should be identical show up as separate points in the output, what's the first setting you'd check?

**What Comes Back:**
> First, check which subdivision class the dome uses. If it's Class I or Class II, this is almost certainly a `vertex_equal_threshold` problem: the threshold is tighter than the two points' floating-point separation, Chapter 4's "too tight" failure. Loosen it slightly and re-check the vertex count against its golden value.
>
> If it's Class III, don't reach for `vertex_equal_threshold` first. A chiral lattice's cross-face points generally don't land near each other in 3D at all (Chapter 6 explains why), so the threshold was never what stitched them together. A cracked Class III seam more likely means the combinatorial `cross_face_matches` are missing or wrong for this `(m,n)` pair: a construction bug in `class_three.py`, not a tuning problem in `geodesic_sphere.py`.

**What It Means:** One visible symptom, two structurally different causes, and only one of them is a threshold problem. Confusing them wastes time nudging a setting that can't fix a Class III construction gap, or, worse, nudging it far enough to cause the opposite failure this chapter just demonstrated.

## What's Next

The Unbending Foreman's count of hubs for the Actual Secret Lair, `(4,1)` at `T=21`, came to 212, the golden value, with no phantoms. He wrote it on the whiteboard under the Euler checks.

The pipeline every subdivision class shares is complete: pick a polyhedron, subdivide one face, replicate it, merge the seams, project outward. Part III reshapes the finished sphere on purpose. Chapter 8 stretches it into an ellipsoid, and Chapter 9 slices it into a dome that can stand on a crater floor.
