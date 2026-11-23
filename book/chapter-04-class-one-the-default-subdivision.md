# Chapter 4: Class I — The Default Subdivision

The Unbending Foreman had one question about any dome, and he asked it before he asked anything else: "Does it close?" The Rival's didn't. Our Heroine's answer, by the end of this chapter, is a number you can compute on a napkin before pyLair says a word, and a habit of checking it every time.

Chapter 3 picked a starting shape. This chapter is where pyLair starts *computing* something: the first and simplest of the three subdivision methods this book teaches, the one every more complicated version is compared against. It's also where **the Actual Secret Lair**, the dome destined for the volcano's crater and the flagship design of Parts II through V, makes its first appearance, in the plainest form it will ever take.

## The One Thing pyLair Has to Solve

Here is a fact worth sitting with before touching a single parameter: pyLair does not compute a separate subdivision for each of an icosahedron's 20 faces. It computes **one**, for a single face, and copies rotated versions of that result onto every other face. That single computed piece, a triangular grid subdividing one flat face, is called the **symmetry triangle**, and it is the only new geometry any of pyLair's three subdivision classes has to work out. The rest of the dome is replication.

This matters for more than efficiency. Whatever is *true* of one symmetry triangle (its vertex count, its grid pattern, any subtlety in where its points sit) is true of every face on the finished sphere. Get the symmetry triangle right once and the whole dome inherits that correctness. Get it wrong once and the whole dome inherits that too, which is the shape of the historical bug Chapter 6 walks through, once Class III makes the symmetry triangle harder to get right.

## Class I: The Simplest Grid There Is

pyLair's default subdivision, the one you get if you don't specify `dome_class` or pass `dome_class=1`, is **Class I**, historically also called the "Alternate" method. Its symmetry triangle is built the most straightforward way imaginable: draw lines parallel to the face's three edges, evenly spaced according to the requested frequency. Here is that grid as pyLair's `ClassOneMethodOneSymmetryTriangle` computes it for one face at frequency 4, the internal vertex and chord data plotted flat before it's replicated or projected:

**[IMAGE: examples/images/class1_symmetry_triangle.png | A single flat triangle divided by lines parallel to its three edges into 16 small equilateral triangles, with 15 grid points marked.]**
**[CAPTION: One bare Class I symmetry triangle at frequency 4, the only piece of geometry pyLair computes directly. Chapters 5 and 6 give their classes the same figure, so the three grids can be compared.]**

Count what's there: 15 vertices, 30 chords, 16 small triangular faces. In general, a Class I symmetry triangle at frequency `f` has `(f+1)(f+2)/2` vertices and `f²` small faces (16 at `f=4`). Once this triangle exists, pyLair's `GeodesicSphere` takes over: it copies a rotated version of the grid onto every face of the base polyhedron, merges the vertices that land on edges shared between faces (Chapter 7 covers how), and projects the result outward onto a sphere of the requested radius.

## The Golden-Value Formula, for a Whole Sphere

Chapter 3's table gave the counts for Class I on all three base shapes. For the icosahedron, the one this book uses most, a Class I sphere at frequency `f` has:

| | Formula | At `f=4` |
|---|---|---|
| Vertices | `10f²+2` | 162 |
| Edges | `30f²` | 480 |
| Faces | `20f²` | 320 |

Use these as the first sanity check on any Class I result before trusting anything downstream. A result that doesn't match means something upstream is already wrong, before a single strut length or hub angle has been computed. This is the Unbending Foreman's napkin.

**Prompt:**
> Build a Class I icosahedral dome at frequency 4. Does the reported vertex count match the golden-value formula?

**What Comes Back** (a snapshot of the `design_dome` result):

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

**What It Means:** `10(4)²+2 = 162`. `30(4)² = 480`. `20(4)² = 320`. All three match with no rounding, which is the point of a golden-value check: not "does this look about right," but "does this equal a number computed independently of the tool being checked."

## Any Positive Frequency Works

Class II, Chapter 5 shows, requires an even frequency; Class III needs two distinct frequency parameters. Class I asks only that frequency be a positive integer. Frequency 1, 2, or 200 all produce a valid, closed Class I dome, because "draw a grid parallel to the edges" never depended on frequency having any particular property. That makes Class I the baseline this book reaches for whenever a chapter needs *a* dome to demonstrate something unrelated to subdivision class; several later chapters use it for exactly that reason, so that projection, truncation, or the environment is the only variable being taught.

## Introducing the Actual Secret Lair

The dome Part V exports and Part VI nests onto plywood starts here, as an unremarkable Class I icosahedral sphere.

**Prompt:**
> Preview a Class I icosahedral dome at frequency 6, radius 1.0, no elongation or truncation yet, and give me its summary. This is going to be our running example.

**What Comes Back** (a `preview_dome` render, `dome_class=1`, `frequency=6`, `polyhedron="icosahedron"`, `radius=1.0`, captioned "362 vertices, 1080 struts"; then a snapshot of `design_dome`'s JSON):

**[IMAGE: examples/images/class1-secret-lair.png | A depth-cued wireframe of a geodesic sphere made of 720 small triangles, with nearer struts drawn darker.]**
**[CAPTION: The Actual Secret Lair's first appearance: a plain Class I icosahedral sphere at frequency 6. Chapter 5 rebuilds the same nominal frequency under Class II, Chapter 6 replaces this subdivision with a chiral one, and Chapters 8 and 9 stretch and truncate whatever survives.]**

```json
{
  "vertex_count": 362,
  "edge_count": 1080,
  "face_count": 720,
  "truncated": false,
  "bounding_box": {"x": [-0.9942, 0.9942],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 215.7794,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 6,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

Nothing here is the final design, which is the point of introducing it early. Each later chapter that reshapes this dome reshapes *this* shape, so the running example accumulates decisions instead of resetting to a fresh dome each time.

**Prompt:**
> If I double the frequency, how much does the face count grow, and is that what you expected before I told you?

**What Comes Back** (two `design_dome` results, Class I icosahedron, `f=4` and `f=8`: a snapshot of the `f=8` result, since `f=4`'s is above, then the two face counts):

```json
{
  "vertex_count": 642,
  "edge_count": 1920,
  "face_count": 1280,
  "truncated": false,
  "bounding_box": {"x": [-1.0, 1.0],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 288.1616,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 8,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

```json
{"frequency": 4, "face_count": 320}
{"frequency": 8, "face_count": 1280}
```

**What It Means:** `1280 / 320 = 4`, not 2. Doubling the frequency quadruples the face count, because faces scale with `f²`: the symmetry triangle is a two-dimensional grid, not a list. Expect "twice the frequency, twice the detail" and you're off by a factor of two, with consequences once the same growth reaches strut counts, file sizes (Chapter 17), and the size of the nesting job Part VI has to pack onto sheet stock. The Chief Financial Villain, shown these two lines, asked that nobody double anything without telling her.

## What `vertex_equal_threshold` Measures

One parameter deserves a closer look now rather than a footnote, because getting it wrong produces a dome that looks fine in a summary and is broken at the seams. `design_dome`'s `vertex_equal_threshold` (default `1e-7`) sets the distance below which two computed vertices count as the same point during the merging step Chapter 7 covers. What matters now is *where* that distance is measured: on the flat, unprojected construction (the symmetry triangle replicated across the base polyhedron's faces, at the polyhedron's natural unit scale), **before** projection scales everything to the requested `radius`. The threshold compares against the same small-scale coordinate system whatever radius you asked for.

It exists to catch one narrow situation: two vertices that are supposed to be the *same* physical point, one edge computed independently by each of the two faces that share it, landing at slightly different floating-point positions instead of coinciding.

**Prompt:**
> Set `vertex_equal_threshold` to `0.0` on this frequency-6 dome and tell me the resulting vertex count.

**What Comes Back** (a snapshot of the `design_dome` result):

```json
{
  "vertex_count": 552,
  "edge_count": 1257,
  "face_count": 720,
  "truncated": false,
  "bounding_box": {"x": [-0.9942, 0.9942],
                   "y": [-1.0, 1.0],
                   "z": [-1.0, 1.0]},
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 248.3526,
  "resolved_parameters": {
    "radius": 1.0, "frequency": 6,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

**What It Means:** Too tight. The seam duplicates, which differ by a tiny amount of floating-point roundoff, no longer count as close enough to merge. Instead of the golden `10(6)²+2 = 362`, the dome has `552` vertices, and `1257` edges instead of `1080`: seams left cracked open, each side keeping its own copy of what should be one point, and its own copy of the struts along it.

**Prompt:**
> Now try `vertex_equal_threshold=0.2` on the same dome.

**What Comes Back** (a snapshot of the `design_dome` result):

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
    "radius": 1.0, "frequency": 6,
    "polyhedron": "icosahedron", "dome_class": 1,
    ...
  }
}
```

**What It Means:** Too loose, the other way. The threshold now catches far more than seam duplicates: every vertex on the sphere collapses into one, and the dome stops existing as a shape: one vertex, a height of `0.0`, and a total strut length of `0.0`. Between the extremes sits a wide range (this dome stays at `362` vertices from about `1e-15` up through `0.15`) with the default comfortably inside it. That's why the parameter almost never needs touching, and why it's worth knowing what happens on the rare occasion you're tempted.

## What's Next

362 vertices, 1,080 edges, 720 faces: the Unbending Foreman checked all three on his napkin and declared the sphere closed. He did not yet declare it a building.

Chapter 5 rebuilds this dome, at the same nominal frequency, under a different construction, Class II, the "Triacon" method, and shows why "same frequency number" between classes doesn't mean "same amount of detail." Chapter 6 goes further, into a subdivision with a handedness, and the instructive bug pyLair's git history has to show for it.
