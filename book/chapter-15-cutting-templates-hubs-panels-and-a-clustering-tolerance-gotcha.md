# Chapter 15: Cutting Templates — Hubs, Panels, and a Clustering-Tolerance Gotcha

The Unbending Foreman's request was simple: part numbers. He did not want 156 custom connector plates, one per joint, each a snowflake. He wanted a short list of plate *designs*, a count for each, and a drawing he could hand to the cutting crew. The Chief Financial Villain wanted the same list for a different reason: every distinct design was a setup charge.

Four chapters of geometry (subdivision, projection, shaping, and now hub angles, strut clustering, and panel shapes) converge here on the two kinds of file a fabricator needs: one cutting template per distinct hub-connector shape, and one per distinct panel shape. This chapter is also the bridge to Part VI: every panel-template DXF that `export_dome` writes with `face_templates=True` is the kind of file a pyFit nesting job (Chapter 20) takes as input.

## What "Same Shape" Means Here

A geodesic dome has far more hubs and panels than distinct *shapes*, and Chapter 12 showed why comparing hubs is tricky: each hub's spoke angles depend on an arbitrary reference strut. `group_hub_types` removes that arbitrariness. Instead of comparing raw, reference-dependent lists, it builds a fingerprint that doesn't care where you start: the hub's valence (how many struts meet there), plus the sequence of pairs (angular gap to the next strut, that strut's tilt) all the way around the hub in angular order.

It then tries every rotation of that sequence and keeps the one that sorts first alphabetically, so to speak. Two hubs with the same physical shape, rotated relative to each other, are guaranteed the *same* fingerprint, because a flat connector template's rotation on the page never mattered; only the angles *between* struts do. `group_face_types` does the equivalent for panels, with edge lengths (Chapter 14).

## Templates for the Actual Secret Lair

Here is the payoff on the Actual Secret Lair: Class III `(4,1)`, stretched `1.8`× on Z, truncated at `0.499999`.

**Prompt:**
> Export this dome with hub and panel templates, `hub_templates=True` and `face_templates=True`. How many distinct hub shapes are there, against the total number of hubs?

**What Comes Back** (a snapshot of the `export_dome` result, written with `output_path="lair"`: its file list, 86 files in all, the default VRML and DXF, 32 hub templates, and 52 panel templates, then the bill of materials, which gains a section for each kind of template):

```json
{
  "files_written": ["lair.wrl", "lair.dxf",
                    "lair_hubtype1.dxf",
                    "lair_hubtype2.dxf", ...],
  "bill_of_materials": {
    "pyLair report": {
      "Bill of materials": {
        "Chord Lengths and Counts": [
          {"length": 0.4748, "count": 5,
           "chord_indices": [207, ...]},
          ...
        ],
        "Warning": "Small length chords...",
        "Possible truncation-artifact chords": []
      },
      "Total material": {
        "Total strut length": 121.0815
      },
      "Hub Connector Templates": [
        {"template_file": "lair_hubtype1.dxf",
         "struts_per_hub": 7, "hub_count": 5, ...},
        ...
      ],
      "Angles at hub between outbound cords and tangential plane": [
        {"hub": 0, "connecting hub": 1,
         "angle (degrees)": 10.8994, ...},
        ...
      ],
      "Spoke angles": [
        {"index": 0, "hub": 0, "connecting hub": 1,
         ...},
        ...
      ],
      "Panel shapes and counts": {
        "Panel Types and Counts": [
          {"edge_lengths": [0.248, 0.282, 0.337],
           "area": 0.034, "count": 5, ...},
          ...
        ],
        "Warning": "Panels sharing the same...",
        "Possible truncation-artifact panels": []
      },
      "Total panel material": {
        "Total panel area": 9.6766
      },
      "Bevel angles at panel edges": [
        {"vertex 1": 0, "vertex 2": 1, "face 1": 30,
         ...},
        ...
      ],
      "Panel Cutting Templates": [
        {"template_file": "lair_facetype1.dxf",
         "edge_lengths": [0.248, 0.282, 0.337],
         "panel_count": 5, ...},
        ...
      ]
    }
  }
}
```

This dome has `156` hubs. `group_hub_types` finds `32` distinct shapes among them, and all `32` get a `_hubtype*.dxf` file, since every hub has at least two struts and therefore an angular pattern to draw.

"All of them" deserves a footnote. `get_bill_of_materials` skips any hub-shape group with a valence of 1 or less before writing files: a plate with one socket has no angular pattern to draw, so the skip is correct, defensive code. It's also silent, which is why it matters that it never fires here.

The `50` hubs on the dome's cut base ring are where it could. They connect upward into the dome and sideways to their neighbors around the ring, and the sideways connections exist only because `truncate()` gives every clipped triangle's cut-plane edge a strut of its own. With those struts, the `50` hubs are two ordinary shapes, `25` at valence `3` and `25` at valence `4`, each closed into its ring neighbors on both sides. Without them, half the ring would be one-socket hubs, quietly skipped. Chapter 22 shows the check that confirms every cut edge gets its strut.

**What It Means:** `156` physical hubs collapse to `32` connector designs, every one a buildable plate. A builder orders 32 part numbers, in the quantities each group reports, not one custom plate per joint. The Unbending Foreman got his list.

Panels follow the same logic: this dome's `260` panels collapse to `52` distinct `_facetype*.dxf` files.

**[IMAGE: examples/images/panel_templates_gallery.png | Six triangle outlines in a grid, each a slightly different shape, each labeled with how many panels of that shape the dome needs.]**
**[CAPTION: Six of the Actual Secret Lair's distinct panel templates, drawn from their edge-length data. Several look alike at a glance, which is why shape matching, not someone eyeballing a pile of triangles, does the grouping.]**

## The Tuned Number Behind the Clustering

Both `group_hub_types` and `group_face_types` round values before comparing them, for the same reason Chapter 13's strut clustering does: floating-point arithmetic leaves tiny noise between values that should be identical. The tolerance for hub angles, 3 decimal places, is an empirically tuned number, not a habit, and the reason is worth seeing.

Two hubs from the *same symmetry orbit*, physically identical positions related by an exact rotation of the construction, were observed differing by about `2×10⁻⁶` degrees (`64.465668°` against `64.465666°`). Six decimal places do *not* absorb that difference and report the hubs as two shapes; three do, since both round to `64.466°`.

The same pattern shows on the Actual Secret Lair, grouping its hubs at each precision:

```json
{"angle_precision": 1, "distinct_hub_groups": 32}
{"angle_precision": 2, "distinct_hub_groups": 32}
{"angle_precision": 3, "distinct_hub_groups": 32}
{"angle_precision": 4, "distinct_hub_groups": 32}
{"angle_precision": 5, "distinct_hub_groups": 35}
{"angle_precision": 6, "distinct_hub_groups": 40}
```

Precisions 1 through 4 agree on the same count, a stable plateau, while 5 and 6 report spurious extra groups made purely of noise. The code's comments record the same plateau across frequencies 4 through 16, with 4 sometimes over-splitting on other domes, which is why `3` was chosen: a safety margin inside the plateau, not the loosest value that happened to pass one test.

**Prompt:**
> If the hub-template count looks suspiciously high for how symmetric this dome should be, what's the first thing you'd check?

**What Comes Back:**
> This tolerance isn't a CLI option or tool parameter; it's a fixed internal constant, checked empirically across frequencies 4 through 16 according to the code's comments. Within that range, noise inflating the template count is unlikely to be the cause. If you're working well outside that range and the count looks implausibly large for the design's symmetry, this noise floor (identical hubs disagreeing in the fifth or sixth decimal place) is the first thing to suspect. You can't tune it away yourself, so report it as an edge case rather than assuming your dome is less symmetric than it looks.

## Panel Templates and Chirality, Paid Off

Chapter 14 promised to show what the chirality flag means for the template count. Here it is: `face_templates=True` writes **one file per shape group, never one per orientation**. A chiral group of `240` panels split `120` and `120` between mirror images still produces one `_facetypeN.dxf`. That isn't an oversight, since a template can be turned over on the material. The flag stays useful precisely because the file count doesn't show it: a builder still has to know that half the group's panels need the template face down. The Junior Henchman's "FLIP" was written on the template, not the filename.

## What These Numbers Don't Answer Yet

One gap, in one sentence: knowing the dome needs `52` panel shapes in specific quantities says nothing about how many sheets of plywood it takes to cut them, a different question Chapter 20 answers. The Chief Financial Villain underlined it twice.

## What's Next

Chapter 16 covers the last gotcha in this dome's bill of materials: truncation slivers, struts and panels shrunk to almost nothing by an unlucky cutoff, and why pyLair flags them rather than silently dropping them. Part V then writes every template here to disk, and Part VI takes up the Chief Financial Villain's underlined question.
