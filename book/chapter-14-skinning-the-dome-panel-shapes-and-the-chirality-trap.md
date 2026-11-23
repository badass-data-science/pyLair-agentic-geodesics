# Chapter 14: Skinning the Dome — Panel Shapes and the Chirality Trap

While the Actual Secret Lair's design was being finalized, the Junior Henchman was given a practice job: skin a lobby display model, a plain frequency-6 Class I sphere, in walnut veneer, so the crew could rehearse on something that didn't matter. The bill of materials said the largest panel group had 240 panels, all the same shape. The Junior Henchman made one template, laid it on the veneer with the grain running point-up, and cut 240 panels. When they went on the model, half of them had their grain running sideways relative to their neighbors, in a neat, maddening pattern. Nobody had cut anything wrong. The Unbending Foreman took the LEFT and RIGHT cardboard models down from the shelf.

Chapter 13 grouped struts by length. This chapter groups panels by shape, and runs into Chapter 6's chirality again at a smaller scale: a single flat triangle. The result is an easy-to-miss trap for anyone about to order directional cladding, and it turns up where you might least expect it.

## Grouping Panels the Way You Grouped Struts

Every panel is a triangle, and pyLair groups panels into shape types the way Chapter 13 grouped struts by length, except that a triangle takes three numbers to describe. `_face_type_signature` computes them: the panel's three edge lengths, sorted, an **SSS** (side-side-side) fingerprint. Panels sharing a fingerprint share a cutting template, one DXF file for the whole group, which is the point of grouping them.

## What SSS Alone Can't Tell You

Here is the catch, stated in `_face_type_signature`'s source comment: sorting the three lengths throws away one piece of information, the order in which the edges connect going around the panel. Two triangles with the *same* three lengths can be mirror images of each other, distinguishable only by that winding order. That is Chapter 6's chirality, applied to one flat triangle instead of a whole lattice. pyLair's answer is `_face_chirality_key`, a second fingerprint that keeps the winding order (allowing the three rotations of the sequence, but never a reflection), so two panels with the same SSS signature but opposite winding are flagged as mirror-image shapes, not the same shape counted twice.

## A Surprise on the Plainest Dome in the Book

You don't need Class III, elongation, or truncation to see this. It happens on a plain, untruncated, unelongated Class I icosahedral sphere at frequency 6, the simplest dome the book builds, and the one the Junior Henchman was skinning:

**Prompt:**
> Group this dome's panels by shape. Are any of the groups flagged as chiral, and what does that mean for a one-sided material?

**What Comes Back** (a snapshot of the `get_bill_of_materials` report, its panel table showing the largest group in full except for its long list of panel numbers):

```json
{
  "pyLair report": {
    "Bill of materials": {
      "Chord Lengths and Counts": [
        {"length": 0.2166, "count": 120,
         "chord_indices": [23, ...]},
        ...
      ],
      "Warning": "Small length chords...",
      "Possible truncation-artifact chords": []
    },
    "Total material": {
      "Total strut length": 215.7794
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
        {
          "edge_lengths": [0.198, 0.203, 0.206],
          "area": 0.018,
          "count": 240,
          "chiral": true,
          "orientations": [
            {
              "edge_lengths": [
                0.2028, 0.2059, 0.198
              ],
              "count": 120
            },
            {
              "edge_lengths": [
                0.2028, 0.198, 0.2059
              ],
              "count": 120
            }
          ],
          "face_indices": [3, 4, 5, ...]
        },
        ...
      ],
      "Warning": "Panels sharing the same...",
      "Possible truncation-artifact panels": []
    },
    "Total panel material": {
      "Total panel area": 12.4598
    },
    "Bevel angles at panel edges": [
      {"vertex 1": 0, "vertex 2": 7, "face 1": 0,
       ...},
      ...
    ]
  }
}
```

**What It Means:** Two of this dome's six panel shape groups are flagged `chiral`. The largest, with edge lengths `(0.198, 0.203, 0.206)`, has 240 panels split exactly 120 and 120 between two winding orders. (The other, `(0.182, 0.187, 0.203)`, splits 60 and 60.) Here is one of each, drawn from the dome's panel data:

**[IMAGE: examples/images/panel_chirality_pair.png | Two triangles side by side, each with a 0.203 base; in one the 0.198 edge is on the left and the 0.206 edge on the right, in the other they are swapped.]**
**[CAPTION: The same three edge lengths, `0.203` along the base of both, with the `0.198` and `0.206` edges on opposite sides. Same SSS signature, and the same outline if you may flip the template over; different panels if you can't.]**

Cut all 240 from one template, oriented the same way every time, and 120 of them come out with the grain running the wrong way relative to the other half, because they are not the same shape traced 240 times. They're mirror images, and no amount of care with a single-orientation template fixes that; the template has to be flipped for half the batch. That's exactly what happened to the walnut.

## Why This Isn't a Class III Curiosity

Here is the surprising part, checked rather than assumed. Class III's `(4,1)` construction, the subdivision Chapter 6 spent a whole chapter on because its strut pattern has a handedness, reports **zero** chiral panel groups on every configuration this book tested: plain, stretched, truncated, and the `(3,2)` lattice too. Class I, the *achiral* construction, is where mirror-image panel pairs appear.

It isn't a contradiction; it's two different questions. Chapter 6 asked whether the *whole dome* can be superimposed on its mirror image. A Class I sphere can: it has every symmetry of the icosahedron, reflections included. So any panel shape that isn't itself mirror-symmetric (a triangle with three different side lengths, like the walnut panel) appears on the dome in both hands, each mapped to the other by one of the dome's reflections.

A Class III dome *can't* be superimposed on its mirror; its symmetries are rotations only. Every copy of a given panel is a rotated copy of every other, so they all share one handedness, and the opposite hand exists only on the separate `(1,4)` dome. Put briefly: **an achiral dome contains both hands of each lopsided panel; a chiral dome contains only one.**

**Prompt:**
> If I'm using plain plywood with no grain direction, does the chirality flag matter for my build?

**What Comes Back:**
> Not physically. A `chiral: true` flag matters only when the material has a direction: wood grain, a printed pattern, a one-sided laminate or finish. Plain plywood is the same from either side and in either orientation, so a template that produces a mirror-image panel instead of a direct copy yields an equally usable piece. The flag tells you *when* to check, not that every chiral group is an emergency whatever you cut it from.

## Checking the Actual Secret Lair

The same check on the Actual Secret Lair (Class III `(4,1)`, stretched, truncated at `0.499999`) comes back clean: all 52 of its panel shape groups report `chiral: false`. That fits the mechanism above; a single Class III dome never contains its own mirror-image pairs. It's still worth having run the check rather than inferring the answer from the rule, the "verify, don't assume" habit Chapter 16 teaches next, one chapter early. Our Heroine, who had been planning a lacquered interior finish, was relieved.

## One Template Still Covers Both Orientations

So the flag doesn't get over-corrected into twice the work: a DXF cutting template needs **one file per shape group**, chiral or not, never one per orientation. A physical template can always be turned over on the material, and tracing it face down gives exactly the mirror image needed. The flag is about *awareness*: knowing that "one shape, 240 panels" is really two 120-panel batches that use the template in two orientations. It doesn't mean generating, tracking, or storing twice as many files. Chapter 15 picks this up once templates are the subject, and Chapter 20 meets it again when the panels are laid out on sheets.

## What's Next

The Junior Henchman recut 120 walnut panels with the template turned face down, and wrote "FLIP" on the template's back in large letters. The lobby model looked splendid. The Unbending Foreman added the LEFT and RIGHT cardboard models to the cutting room's wall, at eye level.

Chapter 15 generates cutting templates for both hubs and panels, and shows how this chapter's chirality flag and Chapter 12's spoke-angle reference gotcha are both resolved at the point where a builder needs a finite, correctly deduplicated set of files for a fabricator.
