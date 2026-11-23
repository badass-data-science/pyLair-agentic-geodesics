# Chapter 22: Which Piece Goes Where — the Assembly Manifest

The first truckload of cut struts reached the crater on a Tuesday. The Unbending Foreman stood over a bin of seventy-odd struts, all close to the same length, all labeled with the same bill-of-materials row, and asked the question no chapter so far had answered: "Which one of these goes *where*?" The Rival's crew had faced the same bin, the disgruntled henchman reported, and had answered it by trial, error, and a mallet.

Every chapter since Part IV has answered some version of "how many of each thing do I need." Chapter 13 counted struts by length. Chapter 15 counted cutting templates by shape. Chapter 20 turned those counts into a nesting job. None of them answered the Unbending Foreman's question. This chapter is about the one thing the pipeline never tracked: not a type, not a count, but an individual piece's identity, and a bug that tracking it caught.

## Two Questions, Two Shapes of Data

`get_bill_of_materials` and `get_assembly_manifest` compute from the same dome geometry and answer different questions with it. The bill of materials groups: "these five struts share a length; cut them all at one setting." The assembly manifest doesn't group anything. Every hub, strut, and panel keeps its own label (`H12`, `S77`, `P42`), which is just its position in the dome's vertex, chord, or face list, the same lists whose lengths `design_dome` reports as `vertex_count`, `edge_count`, and `face_count`. Nothing new is computed to make a label; the identity was always there, and the bill of materials throws it away on purpose.

An identity is useful only with its neighbors attached: which struts meet at a hub, which hubs bound a panel, which panels border a strut. `get_assembly_manifest` builds exactly that for the Actual Secret Lair (Class III `(4,1)`, stretched `1.8`× on Z, truncated at `0.499999`): `156` hubs, `415` struts, `260` panels, the totals Chapters 13 and 15 gave, now individually addressable instead of collapsed into `79` strut rows and `32` hub shapes.

## Reading One Hub's Connections

**Prompt:**
> Get the assembly manifest for this dome and show me the crown hub's connections: which struts meet there, and at what angles.

**What Comes Back** (a snapshot of the `get_assembly_manifest` result: one entry from each section, with hub `H0`, the apex at `(0, 0, 1.8)`, showing three of its five connections):

```json
{
  "hubs": {
    "H0": {
      "index": 0,
      "position": [0.0, 0.0, 1.8],
      "valence": 5,
      "template_group": 31,
      "connections": [
        {"to_hub": "H1", "strut": "S0",
         "tangential_angle_degrees": 10.8994,
         "spoke_angle_degrees": 0.0},
        {"to_hub": "H2", "strut": "S1",
         "tangential_angle_degrees": 10.8994,
         "spoke_angle_degrees": -72.0},
        {"to_hub": "H3", "strut": "S2",
         "tangential_angle_degrees": 10.8994,
         "spoke_angle_degrees": 72.0},
        ...
      ]
    },
    ...
  },
  "struts": {
    "S0": {"index": 0, "hub_1": "H0", "hub_2": "H1",
           "length": 0.2154, "template_group": 64,
           "bordering_panels": ["P30", "P31"]},
    ...
  },
  "panels": {
    "P0": {
      "index": 0,
      "hub_ids": ["H4", "H5", "H6"],
      "centroid": [0.8342, -0.0456, 0.9612],
      "area": 0.0343,
      "template_group": 0,
      "chiral": false,
      "orientation_bucket": null,
      "edges": [
        {"hub_pair": ["H4", "H5"], "strut": "S3",
         "dihedral_angle_degrees": 170.2831,
         "bevel_angle_degrees": 4.8584, "note": ""},
        ...
      ]
    },
    ...
  },
  "hub_groups": [
    {"template_group": 0, "valence": 7, "count": 5,
     "hub_ids": ["H78", "H84", ...]},
    ...
  ],
  "strut_groups": [
    {"template_group": 0, "length": 0.4748,
     "count": 5,
     "strut_ids": ["S207", "S224", ...]},
    ...
  ],
  "panel_groups": [
    {"template_group": 0,
     "edge_lengths": [0.248, 0.282, 0.337],
     "count": 5, "chiral": false,
     "panel_ids": ["P0", "P17", ...]},
    ...
  ]
}
```

**What It Means:** These are Chapter 12's tilt and spoke angles, unchanged (Chapter 8 met this crown hub's `10.8994°`); the manifest recomputes nothing Chapter 12 didn't teach you to trust. What's new is that each angle is labeled with the neighboring hub and the specific strut it belongs to, instead of being reported per hub in isolation. A henchman holding strut `S0` doesn't need a second report to know it runs from `H0` to `H1`; the manifest says so, and `H1`'s entry says the same thing back.

## The Reverse Link: Which Panels Does a Strut Border?

Each panel entry knows its three edges and the strut along each one. The reverse direction, given a strut, which panels does *it* border, is what `bordering_panels` provides:

```json
{
  "S0": {"hub_1": "H0", "hub_2": "H1",
         "length": 0.215,
         "bordering_panels": ["P30", "P31"]}
}
{
  "S341": {"hub_1": "H106", "hub_2": "H111",
           "length": 0.121,
           "bordering_panels": ["P129"]}
}
```

**What It Means:** `S0` is an ordinary interior strut: it borders two panels, the two triangles that share that edge. `S341` borders *one*, and that isn't a manifest bug. It sits on the truncated dome's base ring, where the cut left an open edge with a panel above and nothing below. Across this dome, 365 struts border two panels and 50 border one. There's no third case, and the next section shows why that simple fact is the strongest check a truncated dome has.

## Checking a Dome That Has No Golden Value

The book's strongest checks so far, the golden values (Chapter 4), Euler's formula (Chapter 5), and the independent-library comparison (Chapter 6), all apply to a **closed** surface, the full, untruncated sphere. A truncated dome isn't closed. Its open base means there's no golden value for what its strut count *should* be, so a missing strut along the cut would have nothing to contradict it. The counts would look fine, the preview would look nearly fine, and the only sign would be a quiet one: Chapter 15's rule that skips any hub shape with valence 1 or less, firing on hubs that had lost their ring neighbors.

The manifest supplies the check the counts can't. Every panel edge has to name the strut running along it, and every strut has to name the panels it borders. On a dome that can be built, those cross-references close: every panel edge has a strut, and every strut borders one panel or two, never zero. A panel edge with no strut is not something a real, built dome can have.

pyLair's `truncate()` (`pylair/truncation.py`) is built to satisfy it: both clipping cases, a triangle that keeps one corner and a quadrilateral that keeps two, report the edge lying in the cutoff plane as a chord, as Chapter 10's diagonal is. pyLair's tests hold it to that on a truncated dome: no panel edge may lack a strut, every strut must border one or two panels, and the number of single-panel struts must equal the number of hubs on the base ring, which is what a closed ring of struts requires. pyLair's own `AGENTS.md` gives future maintainers the rule in one line: on a truncated dome, passing the count checks isn't evidence; check the strut–panel adjacency directly.

**Prompt:**
> Which hubs on this dome sit on the base ring, and how many struts does each have now?

**What Comes Back** (the same manifest, collapsed except for base-ring hub `H106`, shown with all its connections):

```json
{
  "hubs": {
    ...,
    "H106": {
      "index": 106,
      "position": [0.6792, -0.7292, -3.60e-06],
      "valence": 4,
      "template_group": 21,
      "connections": [
        {"to_hub": "H78", "strut": "S290",
         "tangential_angle_degrees": 3.7301,
         "spoke_angle_degrees": 0.0},
        {"to_hub": "H82", "strut": "S340",
         "tangential_angle_degrees": 6.4347,
         "spoke_angle_degrees": 67.5074},
        {"to_hub": "H111", "strut": "S341",
         "tangential_angle_degrees": 6.0821,
         "spoke_angle_degrees": 77.9971},
        {"to_hub": "H107", "strut": "S344",
         "tangential_angle_degrees": 2.189,
         "spoke_angle_degrees": -102.003}
      ]
    },
    ...
  },
  "struts": {...},
  "panels": {...},
  "hub_groups": [...],
  "strut_groups": [...],
  "panel_groups": [...]
}
```

Fifty hubs sit on the cut plane, just below `Z = 0` (at `Z ≈ −0.0000036`, since the cut is at `0.499999` of the range). Hub `H106`, at `(0.679, −0.729, 0.0)`, connects to four hubs: `H78` and `H82` further up the dome, and `H107` and `H111`, its neighbors *around* the ring. Those ring connections are the cut-plane struts Chapter 15 described. Of the 50, `25` have valence `3` (one strut up, two around the ring) and `25` have valence `4` (two up, two around): two ordinary, buildable hub shapes instead of a dead end.

## Chirality, Once More, at the Job-Spec Level

The Actual Secret Lair has no chiral panel groups (Chapter 14), but the lobby display sphere does: the plain Class I sphere at frequency 6, whose `240` panels with edge lengths `(0.198, 0.203, 0.206)` split `120` and `120` between two orientations. A per-instance job spec for that sphere is where the chirality flag stops being an awareness check and becomes a correctness requirement.

**Prompt:**
> Build a per-instance pyFit job spec for the display sphere's panels. Make sure the chiral group's two orientations don't get mixed up.

**What Comes Back** (a snapshot of the `export_assembly_job_spec` result, written with `output_path="sphere"`: the panel templates it wrote, 6 in all, then the job spec, its parts list showing two of its 720 parts, the first and the 121st, both from the chiral group):

```json
{
  "files_written": ["sphere_facetype1.dxf",
                    "sphere_facetype2.dxf", ...],
  "job_spec": {
    "sheet": {"width": 48.0, "height": 96.0},
    "parts": [
      {"name": "P3", "dxf": "sphere_facetype1.dxf",
       "quantity": 1, "allow_mirror": false},
      ...,
      {
        "name": "P4",
        "polygon": [[0.0, 0.0], [0.198, 0.0],
                    [0.1021, -0.1789]],
        "quantity": 1,
        "allow_mirror": false
      },
      ...
    ]
  }
}
```

**What It Means:** Unlike Chapter 20's job spec, this one has one part per physical panel, named by its manifest label, so pyFit's report can say where each *individual* panel landed. `P3` has the group's canonical orientation, the one `OutputFaceTemplateDXF` draws, so it points at that template file. `P4` has the *other* orientation, so it gets an inline `polygon`: the same three lengths, reflected, computed once and handed to pyFit rather than pointing at a second DXF that doesn't exist (180 of the 720 parts are inline like this).

Both go in with `allow_mirror: false`, and that's the point. The template DXF is one arbitrary choice between two mirror-image shapes with the same edge lengths. Let pyFit flip pieces freely for better packing and nothing stops a `P3`-handed piece from being cut where `P4` belongs: a batch that nests perfectly and cuts the wrong hand for its slot. Deciding orientation once, in the job spec, keeps that decision away from a packing heuristic that has no idea the dome cares.

Hub connector plates get no such treatment, and that's a stated gap, not an oversight: `group_hub_types` has no chirality fingerprint the way `group_face_types` does, so `export_assembly_job_spec` with `kind="hubs"` submits every hub with `allow_mirror: true`. A build needing a directional connector material would have to close that gap in `pylair/bill_of_materials.py` first.

## An Annotated Schematic, Not Just a Preview

**Prompt:**
> Render a dome with each hub's label drawn at its position, so a builder can match a physical connector to a spot on the structure, and give me its assembly manifest too. Use a small one, frequency 2, cut at `truncation_z=0.4`, so the labels stay legible.

**What Comes Back** (a `render_assembly_schematic` render, hub labels on, captioned "46 hubs, 115 struts, 70 panels (truncated)"; then a snapshot of `get_assembly_manifest` for the same dome, hub `H0` showing two of its connections):

**[IMAGE: examples/images/assembly_schematic_hub_labels.png | A depth-cued wireframe of a small truncated dome with a label such as H0 or H12 printed beside every hub, and a closed ring of struts at the base.]**
**[CAPTION: A small truncated dome (a frequency-2 icosahedral sphere cut at `0.4`) with every hub's label drawn at its position: the depth-cued wireframe of `preview_dome`, annotated. The struts along the cut close the base into a ring.]**

```json
{
  "hubs": {
    "H0": {
      "index": 0,
      "position": [0.8944, 0.0, 0.4472],
      "valence": 5,
      "template_group": 1,
      "connections": [
        {"to_hub": "H1", "strut": "S0",
         "tangential_angle_degrees": 15.8587,
         "spoke_angle_degrees": 0.0},
        {"to_hub": "H2", "strut": "S1",
         "tangential_angle_degrees": 15.8587,
         "spoke_angle_degrees": -72.0},
        ...
      ]
    },
    ...
  },
  "struts": {
    "S0": {"index": 0, "hub_1": "H0", "hub_2": "H1",
           "length": 0.5465, "template_group": 1,
           "bordering_panels": ["P0", "P17"]},
    ...
  },
  "panels": {
    "P0": {
      "index": 0,
      "hub_ids": ["H0", "H2", "H1"],
      "centroid": [0.7028, 0.1667, 0.6079],
      "area": 0.1393,
      "template_group": 0,
      "chiral": false,
      "orientation_bucket": null,
      "edges": [
        {"hub_pair": ["H0", "H2"], "strut": "S1",
         "dihedral_angle_degrees": 157.5411,
         "bevel_angle_degrees": 11.2295,
         "note": ""},
        ...
      ]
    },
    ...
  },
  "hub_groups": [
    {"template_group": 0, "valence": 6, "count": 10,
     "hub_ids": ["H1", "H2", ...]},
    ...
  ],
  "strut_groups": [
    {"template_group": 0, "length": 0.618,
     "count": 35, "strut_ids": ["S2", "S4", ...]},
    ...
  ],
  "panel_groups": [
    {"template_group": 0,
     "edge_lengths": [0.547, 0.547, 0.618],
     "count": 30, "chiral": false,
     "panel_ids": ["P0", "P1", ...]},
    ...
  ]
}
```

**What It Means:** `render_assembly_schematic` reuses `preview_dome`'s depth-cued renderer (near struts dark, far struts pale) and can draw each hub's, strut's, or panel's label at its position. Hub labels default on; strut and panel labels default off, because a dome has far more struts than hubs and more panels than either, and all three at once past a low frequency is an unreadable smear. The Actual Secret Lair's 156 hubs are already too many to label legibly in one image, so the figure uses a much smaller dome. For a full-size build you'd generate schematics per ring or subassembly, not all at once: a real limitation, stated plainly.

## All Three at Once, From the Command Line

The three tools in this chapter, `get_assembly_manifest` (writes nothing), `export_assembly_job_spec` (writes the cutting templates and returns the job spec), and `render_assembly_schematic` (returns the annotated image), bring pyLair's MCP tools to seven: Chapter 18's four plus these three. The CLI has matching options, `--assembly-manifest`, `--pyfit-job-spec=panels` (or `hubs`), and `--assembly-schematic`, which write files alongside an ordinary `pylair` run:

```
lair_manifest.json
lair_facetype1.dxf ... lair_facetype52.dxf
lair_jobspec.json
```

## What's Next

The Unbending Foreman had every strut stenciled with its `S` number and every hub plate with its `H` number, and printed the schematic one ring at a time. The dome went up ring by ring from the crater floor, the base ring first, all fifty hubs with three or four sockets apiece. Nobody needed a mallet.

Part VI closes here. Chapters 3 through 22 have taken a shape from "pick a polyhedron" to "here is the piece a henchman is holding and where it goes": design, shape, account, export, nest, assemble. Part VII steps back. Chapter 23 is a prompting clinic spanning both toolkits, Chapter 24 is the retrospective the book has been building toward since its first gotcha, and Chapter 25 sends the Actual Secret Lair off to be lived in.
