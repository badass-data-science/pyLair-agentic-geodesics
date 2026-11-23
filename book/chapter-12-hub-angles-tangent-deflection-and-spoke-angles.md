# Chapter 12: Hub Angles — Tangent Deflection and Spoke Angles

The Unbending Foreman brought a hub connector to the design meeting: a steel disc with six slotted sockets welded around its edge, each one tilted slightly inward. He set it on the table beside the Rival's photographs. "Two numbers per socket," he said. "How far it tilts. Where it sits around the disc. Get either one wrong on one socket and that strut doesn't go in. Get it wrong on every hub, like *he* did," a nod at the photographs, "and you have a field full of sticks."

Every chapter in Part IV answers one question: given a finished, shaped dome, what does a builder need to know to *fabricate* it? This chapter starts at the joints, the hubs where struts meet, and the two angles pyLair reports for each strut there. Together they're what makes a bill of materials buildable rather than a list of lengths with nothing to say about how the pieces come together.

## Two Angles, Two Different Cuts

At every hub, each connecting strut gets two numbers. The **tangent-plane deflection angle** measures how far the connector bends *inward* to receive that strut: the angle between the strut and the plane tangent to the dome's surface at that hub. The **spoke angle** measures how far *around* the hub, within that tangent plane, the strut sits relative to the others, using one connecting strut as the zero-degree reference.

**[IMAGE: ../blog-posts/tangent_angle_image_CROPPED.png | A diagram viewed edge-on to a hub's tangent plane, which appears as a line, with two struts leaving the hub and the small angle between each strut and the plane marked.]**
**[CAPTION: The tangent-plane deflection angle. The view looks along the tangent plane, so the plane appears as a line. Two struts are shown for clarity; a real hub usually has five or six.]**

**[IMAGE: ../blog-posts/spoke_angle_image_CROPPED.png | A diagram looking straight down onto a hub's tangent plane, with each strut projected onto the plane as a spoke and the angle of each spoke measured from a reference spoke.]**
**[CAPTION: The spoke angle, viewed perpendicular to the same tangent plane: each strut projected onto the plane and measured from a chosen reference strut.]**

In the Unbending Foreman's terms: the tangent-plane angle is the tilt that lets a socket meet its strut along the strut's own line instead of at a kink; the spoke angle is the rotation that puts each socket in the right place around the disc. A connector needs both. Tilted right but rotated wrong, it won't accept its struts in the right positions; rotated right but tilted wrong, the struts meet it bent.

## A Worked Example

Here are both angles for one hub on the Actual Secret Lair (Class III `(4,1)`, stretched `1.8`× on Z, truncated at `0.499999`: Chapters 6, 8, and 9 combined), an ordinary six-strut hub:

**Prompt:**
> For one hub on this dome, report both the tangent-plane deflection angles and the spoke angles for every strut meeting there.

**What Comes Back** (a snapshot of the `get_bill_of_materials` report, whose hub-angle and spoke-angle sections show hub `1`'s entries; hub `1` sits at `(0.107, 0.182, 1.759)`, near the crown):

```json
{
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
    "Angles at hub between outbound cords and tangential plane": [
      ...,
      {"hub": 1, "connecting hub": 0,
       "angle (degrees)": 10.3853, "note": ""},
      {"hub": 1, "connecting hub": 2,
       "angle (degrees)": 12.3198, "note": ""},
      {"hub": 1, "connecting hub": 3,
       "angle (degrees)": 12.3198, "note": ""},
      {"hub": 1, "connecting hub": 11,
       "angle (degrees)": 12.1743, "note": ""},
      {"hub": 1, "connecting hub": 14,
       "angle (degrees)": 11.4037, "note": ""},
      {"hub": 1, "connecting hub": 15,
       "angle (degrees)": 11.7717, "note": ""},
      ...
    ],
    "Spoke angles": [
      ...,
      {"index": 5, "hub": 1, "connecting hub": 0,
       "angle (degrees)": 0.0},
      {"index": 6, "hub": 1, "connecting hub": 2,
       "angle (degrees)": 53.3198},
      {"index": 7, "hub": 1, "connecting hub": 3,
       "angle (degrees)": -53.3198},
      {"index": 8, "hub": 1, "connecting hub": 11,
       "angle (degrees)": 115.3563},
      {"index": 9, "hub": 1, "connecting hub": 14,
       "angle (degrees)": 180.0},
      {"index": 10, "hub": 1, "connecting hub": 15,
       "angle (degrees)": -118.5569},
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
    ]
  }
}
```

**What It Means:** Six struts meet here, each with its own inward tilt (about `10` to `12°`, similar magnitudes near the crown) and its own position around the hub (spread around the full circle, as you'd expect). Struts to hubs `2` and `3` share a tilt (`12.3198°`) and have mirror-opposite positions (`±53.3198°`), a visible hint of local symmetry at this hub. Together the two lists are a complete fabrication spec for this joint: six sockets at these six tilts, at these six rotations, and every strut meeting here sits correctly.

The same numbers appear in the text report the `pylair` command line prints, as pyLair's documentation has shown from the start:

**[IMAGE: ../blog-posts/STDOUT_tangent_angles.png | A terminal window listing hub numbers, connecting hub numbers, and tangent-plane angles in degrees, one strut per line.]**
**[CAPTION: The tangent-plane angle section of a pyLair command-line report, from the project's earlier documentation.]**

**[IMAGE: ../blog-posts/STDOUT_spoke_angles.png | A terminal window listing hub numbers, connecting hub numbers, and spoke angles in degrees, one strut per line.]**
**[CAPTION: The spoke angle section of the same kind of report.]**

## Why Elongation Changes the Pattern, Not Just the Numbers

Chapter 8 showed that elongating a sphere breaks the convenient fact that the surface normal equals the position vector, and hub angles are where that matters most, because both angles are measured against the normal. Here is one hub of the Actual Secret Lair's sphere before and after the 1.8× stretch on Z, with truncation left off both so the comparison is clean (hub `1` of the untruncated dome, one of the original icosahedron's twelve vertices; truncation renumbers hubs, so it isn't the hub above):

**Prompt:**
> This dome is elongated. Show me how much one hub's reported angles would differ if it were a plain sphere instead.

**What Comes Back** (two `get_bill_of_materials` calls, untruncated: a snapshot of the stretched dome's report, with hub `1`'s five hub-angle entries shown, then hub `1` from both reports side by side):

```json
{
  "pyLair report": {
    "Bill of materials": {
      "Chord Lengths and Counts": [
        {"length": 0.4854, "count": 10,
         "chord_indices": [217, ...]},
        ...
      ],
      "Warning": "Small length chords...",
      "Possible truncation-artifact chords": []
    },
    "Total material": {
      "Total strut length": 213.2096
    },
    "Angles at hub between outbound cords and tangential plane": [
      ...,
      {"hub": 1, "connecting hub": 2,
       "angle (degrees)": 4.1481, "note": ""},
      {"hub": 1, "connecting hub": 55,
       "angle (degrees)": 5.6306, "note": ""},
      {"hub": 1, "connecting hub": 59,
       "angle (degrees)": 4.7556, "note": ""},
      {"hub": 1, "connecting hub": 67,
       "angle (degrees)": 6.5689, "note": ""},
      {"hub": 1, "connecting hub": 111,
       "angle (degrees)": 4.023, "note": ""},
      ...
    ],
    "Spoke angles": [
      {"index": 0, "hub": 0, "connecting hub": 5,
       ...},
      ...
    ],
    "Panel shapes and counts": {
      "Panel Types and Counts": [
        {"edge_lengths": [0.248, 0.282, 0.337],
         "area": 0.034, "count": 10, ...},
        ...
      ],
      "Warning": "Panels sharing the same...",
      "Possible truncation-artifact panels": []
    },
    "Total panel material": {
      "Total panel area": 19.3531
    },
    "Bevel angles at panel edges": [
      {"vertex 1": 0, "vertex 2": 5, "face 1": 30,
       ...},
      ...
    ]
  }
}
```

```json
{
  "elongation": "1.0,1.0,1.0",
  "vertex": [0.894, 0.0, 0.447],
  "tangent_angles": [6.1061, 6.1061, 6.1061, 6.1061,
                     6.1061]
}
{
  "elongation": "1.0,1.0,1.8",
  "vertex": [0.894, 0.0, 0.805],
  "tangent_angles": [4.1481, 5.6306, 4.7556, 6.5689,
                     4.0230]
}
```

**What It Means:** On the sphere, this hub is a point of five-fold symmetry, and all five struts report the same tilt, `6.1061°`. Stretched, the symmetry is gone: five *different* tilts, from `4.02°` to `6.57°`, because the true ellipsoid normal (Chapter 8's formula) now depends on which way each strut runs relative to the stretch, not just on the hub's distance from the center. That's why Chapter 8 insisted on the true normal. With the position-vector shortcut, this hub would be reported as five identical sockets when it needs five different ones, and the Unbending Foreman would weld a connector that fits a sphere nobody is building.

## The Number That Isn't What It Looks Like

Here is a gotcha to absorb before Chapter 15 clusters hubs by shape: a hub's spoke angles are always measured **from one particular connecting strut, the zero-degree reference**, which `compute_spoke_angles` takes to be the strut to the lowest-numbered connecting hub. That reference is a bookkeeping choice, not a compass direction rooted in the dome's geometry.

The consequence is that two physically identical hubs (same set of tilts, same gaps between neighboring struts) can print completely different-looking spoke-angle lists, just because their neighbors happen to be numbered differently. A hub listed as `0°`, `53°`, `115°`, `180°`, `-119°` and another listed as, say, `0°`, `38°`, `103°`, `165°`, `-134°` could be the same connector, read from a different starting strut.

So comparing two hubs row by row against their raw spoke angles is not a reliable way to tell whether they're the same shape; you'd first have to rotate one list until a strut lines up, then compare. Chapter 15's hub-shape clustering does that automatically, comparing the *cyclic pattern of gaps* between neighboring spoke angles rather than the raw values. Until then, the safe rule: never conclude two hubs differ just because their raw spoke-angle lists don't match number for number.

## What's Next

The Unbending Foreman took the hub-1 numbers to his workbench and welded a test connector. Six struts slid into it. He set it on the shelf beside the cardboard models from Chapter 6, which was becoming a small museum of things that had gone right.

Chapter 13 moves from the joints to the struts: not their angles but how their lengths are grouped into bill-of-materials rows, and the deliberate tradeoff in the one setting that controls both that grouping and how many decimal places print.
