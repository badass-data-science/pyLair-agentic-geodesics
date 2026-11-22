# Chapter 22: Which Piece Goes Where — the Assembly Manifest

The first truckload of cut struts reached the crater on a Tuesday. The Foreman stood over a bin of seventy-odd struts, all close to the same length, all labeled with the same bill-of-materials row, and asked the question no chapter so far had answered: "Which one of these goes *where*?" The Rival's crew had faced the same bin, the disgruntled henchman reported, and had answered it by trial, error, and a mallet.

Every chapter since Part IV has answered some version of "how many of each thing do I need." Chapter 13 counted struts by length. Chapter 15 counted cutting templates by shape. Chapter 20 turned those counts into a nesting job. None of them answered the Foreman's question. This chapter is about the one thing the pipeline never tracked: not a type, not a count, but an individual piece's identity, and a bug that tracking it caught.

## Two Questions, Two Shapes of Data

`get_bill_of_materials` and `get_assembly_manifest` compute from the same dome geometry and answer different questions with it. The bill of materials groups: "these five struts share a length; cut them all at one setting." The assembly manifest doesn't group anything. Every hub, strut, and panel keeps its own label (`H12`, `S77`, `P42`), which is just its position in the dome's vertex, chord, or face list, the same lists whose lengths `design_dome` reports as `vertex_count`, `edge_count`, and `face_count`. Nothing new is computed to make a label; the identity was always there, and the bill of materials throws it away on purpose.

An identity is useful only with its neighbors attached: which struts meet at a hub, which hubs bound a panel, which panels border a strut. `get_assembly_manifest` builds exactly that for the Actual Secret Lair (Class III `(4,1)`, stretched `1.8`× on Z, truncated at `0.499999`): `156` hubs, `415` struts, `260` panels, the totals Chapters 13 and 15 gave, now individually addressable instead of collapsed into `79` strut rows and `32` hub shapes.

## Reading One Hub's Connections

**Prompt:**
> Get the assembly manifest for this dome and show me the crown hub's connections: which struts meet there, and at what angles.

**What Comes Back** (from `get_assembly_manifest`, hub `H0` at the apex, `(0, 0, 1.8)`; angles rounded, other fields and two of its five connections trimmed):

```json
{
  "H0": {
    "position": [0.0, 0.0, 1.8],
    "valence": 5,
    "connections": [
      {"to_hub": "H1", "strut": "S0", "tangential_angle_degrees": 10.899, "spoke_angle_degrees": 0.0},
      {"to_hub": "H2", "strut": "S1", "tangential_angle_degrees": 10.899, "spoke_angle_degrees": -72.0},
      {"to_hub": "H3", "strut": "S2", "tangential_angle_degrees": 10.899, "spoke_angle_degrees": 72.0}
    ]
  }
}
```

**What It Means:** These are Chapter 12's tilt and spoke angles, unchanged (Chapter 8 met this crown hub's `10.8994°`); the manifest recomputes nothing Chapter 12 didn't teach you to trust. What's new is that each angle is labeled with the neighboring hub and the specific strut it belongs to, instead of being reported per hub in isolation. A henchman holding strut `S0` doesn't need a second report to know it runs from `H0` to `H1`; the manifest says so, and `H1`'s entry says the same thing back.

## The Reverse Link: Which Panels Does a Strut Border?

Each panel entry knows its three edges and the strut along each one. The reverse direction, given a strut, which panels does *it* border, is what `bordering_panels` provides:

```json
{"S0":   {"hub_1": "H0",   "hub_2": "H1",   "length": 0.215, "bordering_panels": ["P30", "P31"]}}
{"S341": {"hub_1": "H106", "hub_2": "H111", "length": 0.121, "bordering_panels": ["P129"]}}
```

**What It Means:** `S0` is an ordinary interior strut: it borders two panels, the two triangles that share that edge. `S341` borders *one*, and that isn't a manifest bug. It sits on the truncated dome's base ring, where the cut left an open edge with a panel above and nothing below. Across this dome, 365 struts border two panels and 50 border one. There's no third case, and the history of how that came to be true is this chapter's main story.

## The Bug the Assembly Work Caught

Chapter 15 mentioned that `50` of this dome's `156` hubs sit on the base ring and that, before a fix, `25` of them had a **valence of 1**: one strut running upward and nothing else. `get_bill_of_materials` has a defensive rule for that case, skip any hub shape with valence 1 or less, since a one-socket plate has no angular pattern to draw. That rule fired, silently, on 25 hubs of this dome, and anyone watching only the vertex, edge, and face *counts* had no way to see why.

**[IMAGE: examples/images/base_ring_strut_fix_before_after.png | Two wireframes of the same small truncated dome. Left: the bottom edge is ragged, with gaps between neighboring base points. Right: the bottom edge forms a closed ring of struts.]**
**[CAPTION: A small truncated dome (a frequency-2 icosahedral cap) before and after the fix. Left: the base ring's closing edges were never made into struts, leaving a ragged, open bottom. Right: every one of those edges is a strut, closing the ring. The vertices didn't move; only which pairs of them are joined by a strut changed.]**

**What happened.** `truncate()`'s face clipping (`pylair/truncation.py`) computes two new crossing points for every boundary triangle it clips; that part was always right, and it's the machinery behind Chapter 10's diagonal seam. What it never did was report the segment *between* those two points, the triangle's edge lying in the cutoff plane, as a chord. The other edges of a clipped face are covered by Chapter 9's strut-shortening, but that logic only touches struts that *existed* before the cut, and this edge never did. It was a panel edge from the moment it was created, and no code path gave it a strut.

**Why nothing caught it sooner.** The book's strongest checks, the golden values (Chapter 4), Euler's formula (Chapter 5), and the independent-library comparison (Chapter 6), all apply to a **closed** surface, the full, untruncated sphere they were run against. A truncated dome isn't closed: its open base means there's no golden value for what its strut count *should* be, so an undercount had nothing to contradict. The bug hid exactly where the strongest checks couldn't look.

**What did catch it.** The assembly manifest, built for the unglamorous reason of letting a builder look up a piece's neighbors, not as a bug hunt. Once every panel edge had to name the strut running along it, and every strut the panels it borders, the cross-references didn't close: 50 panel edges on the base ring had no strut at all. A panel edge with no strut is not something a real, built dome can have. The fix (`pylair/truncation.py`) makes both clipping cases, a triangle that keeps one corner and a quadrilateral that keeps two, report that edge as a chord, as Chapter 10's diagonal already was. Every hub on this dome now has a valence of at least 3, the skip rule sits unused, and the 156 hubs collapse to 32 buildable connector shapes, Chapter 15's count, now with its story told. pyLair's own `AGENTS.md` keeps the lesson for future maintainers: on a truncated dome, passing the count checks isn't evidence; check the strut–panel adjacency directly.

**Prompt:**
> Which hubs on this dome sit on the base ring, and how many struts does each have now?

**What Comes Back:** Fifty hubs sit on the cut plane, just below `Z = 0` (at `Z ≈ −0.0000036`, since the cut is at `0.499999` of the range). Hub `H106`, at `(0.679, −0.729, 0.0)`, connects to four hubs: `H78` and `H82` further up the dome, and `H107` and `H111`, its neighbors *around* the ring. Those ring connections are what used to be missing. Of the 50, `25` have valence `3` (one strut up, two around the ring) and `25` have valence `4` (two up, two around): two ordinary, buildable hub shapes instead of a dead end.

## Chirality, Once More, at the Job-Spec Level

The Actual Secret Lair has no chiral panel groups (Chapter 14), but the lobby display sphere does: the plain Class I sphere at frequency 6, whose `240` panels with edge lengths `(0.198, 0.203, 0.206)` split `120` and `120` between two orientations. A per-instance job spec for that sphere is where the chirality flag stops being an awareness check and becomes a correctness requirement.

**Prompt:**
> Build a per-instance pyFit job spec for the display sphere's panels. Make sure the chiral group's two orientations don't get mixed up.

**What Comes Back** (two of the job spec's 720 parts, both from the chiral group, from `export_assembly_job_spec`; the polygon is rounded):

```json
{"name": "P3", "dxf": "sphere_facetype1.dxf", "quantity": 1, "allow_mirror": false}
{"name": "P4", "polygon": [[0.0, 0.0], [0.198, 0.0], [0.102, -0.179]], "quantity": 1, "allow_mirror": false}
```

**What It Means:** Unlike Chapter 20's job spec, this one has one part per physical panel, named by its manifest label, so pyFit's report can say where each *individual* panel landed. `P3` has the group's canonical orientation, the one `OutputFaceTemplateDXF` draws, so it points at that template file. `P4` has the *other* orientation, so it gets an inline `polygon`: the same three lengths, reflected, computed once and handed to pyFit rather than pointing at a second DXF that doesn't exist (180 of the 720 parts are inline like this). Both go in with `allow_mirror: false`, and that's the point. The template DXF is one arbitrary choice between two mirror-image shapes with the same edge lengths. Let pyFit flip pieces freely for better packing and nothing stops a `P3`-handed piece from being cut where `P4` belongs: a batch that nests perfectly and cuts the wrong hand for its slot. Deciding orientation once, in the job spec, keeps that decision away from a packing heuristic that has no idea the dome cares.

Hub connector plates get no such treatment, and that's a stated gap, not an oversight: `group_hub_types` has no chirality fingerprint the way `group_face_types` does, so `export_assembly_job_spec` with `kind="hubs"` submits every hub with `allow_mirror: true`. A build needing a directional connector material would have to close that gap in `pylair/bill_of_materials.py` first.

## An Annotated Schematic, Not Just a Preview

**Prompt:**
> Render this dome with each hub's label drawn at its position, so a builder can match a physical connector to a spot on the structure.

**What Comes Back** (a `render_assembly_schematic` render, hub labels on):

**[IMAGE: examples/images/assembly_schematic_hub_labels.png | A depth-cued wireframe of a small truncated dome with a label such as H0 or H12 printed beside every hub, and a closed ring of struts at the base.]**
**[CAPTION: The small truncated dome from Figure 22.1, after the fix, with every hub's label drawn at its position: the depth-cued wireframe of `preview_dome`, annotated.]**

**What It Means:** `render_assembly_schematic` reuses `preview_dome`'s depth-cued renderer (near struts dark, far struts pale) and can draw each hub's, strut's, or panel's label at its position. Hub labels default on; strut and panel labels default off, because a dome has far more struts than hubs and more panels than either, and all three at once past a low frequency is an unreadable smear. The Actual Secret Lair's 156 hubs are already too many to label legibly in one image, so the figure uses a much smaller dome. For a full-size build you'd generate schematics per ring or subassembly, not all at once: a real limitation, stated plainly.

## All Three at Once, From the Command Line

The three tools in this chapter, `get_assembly_manifest` (writes nothing), `export_assembly_job_spec` (writes the cutting templates and returns the job spec), and `render_assembly_schematic` (returns the annotated image), bring pyLair's MCP tools to seven: Chapter 18's four plus these three. The CLI has matching options, `--assembly-manifest`, `--pyfit-job-spec=panels` (or `hubs`), and `--assembly-schematic`, which write files alongside an ordinary `pylair` run:

```
lair_manifest.json
lair_facetype1.dxf ... lair_facetype52.dxf
lair_jobspec.json
```

## What's Next

The Foreman had every strut stenciled with its `S` number and every hub plate with its `H` number, and printed the schematic one ring at a time. The dome went up ring by ring from the crater floor, the base ring first, all fifty hubs with three or four sockets apiece. Nobody needed a mallet.

Part VI closes here. Chapters 3 through 22 have taken a shape from "pick a polyhedron" to "here is the piece a henchman is holding and where it goes": design, shape, account, export, nest, assemble. Part VII steps back. Chapter 23 is a prompting clinic spanning both toolkits, Chapter 24 is the retrospective the book has been building toward since its first gotcha, and Chapter 25 sends the Actual Secret Lair off to be lived in.
