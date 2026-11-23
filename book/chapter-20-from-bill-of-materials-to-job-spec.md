# Chapter 20: From Bill of Materials to Job Spec — Nesting the Actual Secret Lair's Panels

The Chief Financial Villain's concern about plywood had sharpened into a concern about trucks. Every sheet had to reach a dormant volcano by road, and a convoy of lumber trucks climbing toward an uninhabited crater is precisely the kind of thing that raises the Interpol heat. "Fewer sheets," she said, "is fewer trucks, is fewer questions." She wanted a number, and she wanted it before anyone ordered anything.

Chapter 19 showed pyFit working on its own terms. This chapter puts it to work on pyLair's: a job spec built straight from the Actual Secret Lair's bill of materials, with no quantity typed by hand, and the numbers that come back once real dome panels, not unit squares, are being nested.

## A Job Spec With No Hand-Typing

Chapter 15 already produces the files pyFit needs: `face_templates=True` writes one DXF per distinct panel shape, and the same report carries a **"Panel Cutting Templates"** section pairing each file with its panel count. Here is the first entry, for the Lair at its build radius of 2.5 meters (one of 52):

```json
{"template_file": "lair_facetype1.dxf",
 "edge_lengths": [0.621, 0.705, 0.843],
 "panel_count": 5,
 "face_indices": [0, 17, 47, 72, 97],
 "chiral": false, "orientations": null}
```

A pyFit job spec's `"parts"` list needs two things per shape, a `"dxf"` path and a `"quantity"`, and the report supplies both, already paired, for all 52 shapes:

```python
report = report["pyLair report"]
templates = report[
    "Panel Cutting Templates"]
parts = [
    {"name": f"facetype{i+1}",
     "dxf": t["template_file"],
     "quantity": t["panel_count"],
     "allow_mirror": True}
    for i, t in enumerate(templates)
]
job = {"sheet": {"width": 2.44,
                 "height": 1.22},
       "parts": parts}
```

**260 panels, 52 shapes, no number typed by hand**: every quantity traces to a count pyLair computed. That's the point of two projects sharing only a file format. pyLair never needs to know pyFit exists, and the job spec needs nothing from pyLair but files it was writing anyway. (`allow_mirror: True` is fine here: the Lair has no chiral panels, Chapter 14 found, and its panels are plain plywood.)

## The Full Job, and a Lesson About Job Size

The sheet is `2.44 m × 1.22 m`, a standard 8-by-4-foot panel in meters. Start with the floor on the answer: the Lair's panels cover about `60.5` square meters (pyLair's total panel area of `9.677` at radius 1, times `2.5²`), and a sheet is about `2.98`, so no layout can use fewer than 21 sheets.

**Prompt:**
> Nest all 260 of the Lair's panels on 2.44 by 1.22 sheets with `design_nest`. Then try a 45-degree rotation step. How many sheets, and how long does each take?

**What Comes Back** (two `design_nest` results, at 15° and then 45°, each a snapshot whose `utilization_by_sheet` shows its first four sheets and its last; the runs took about 1,017 and 318 seconds):

```json
{
  "sheets_used": 30,
  "utilization_by_sheet": [
    0.8953, 0.8548, 0.7995, 0.816, ..., 0.1076
  ]
}
{
  "sheets_used": 32,
  "utilization_by_sheet": [
    0.8407, 0.8262, 0.7562, 0.7211, ..., 0.1849
  ]
}
```

**What It Means:** Thirty sheets at the default step, against a floor of 21: most sheets come out between 55% and 90% full, and the last holds a few stragglers. The default took about 17 minutes (on a machine also running the other job), and the 45° step about 5 minutes for two more sheets. That is the lived version of a warning in pyFit's documentation: every part tries each already-opened sheet before a new one opens, and each try is a full no-fit-polygon search against everything on that sheet, so a big sheet that holds many panels makes every placement more expensive. It's the same shape of tradeoff Chapter 13 taught for `bom_rounding_precision`: more permissive isn't simply better.

**[IMAGE: examples/images/lair_full_nest_sheet1.png | A pyFit preview of one 2.44-by-1.22 sheet packed with large and small triangular dome panels, interlocking point to base; the title reads 89.5 percent utilized.]**
**[CAPTION: The first of 30 sheets for the Actual Secret Lair at its 2.5-meter radius, at the default 15° rotation step: 89.5% utilized, the best sheet of the job.]**

**Prompt:**
> If packing feels slow on this many panels, what's the first setting you'd loosen, and what do I give up?

**What Comes Back:**
> `rotation_step_degrees` is the direct lever. The default, `15°`, tries 24 orientations per part (twice that when mirroring is allowed); `45°` tries 8. You give up packing quality, usually a little: on this job, two extra sheets for about a third of the time. It's not a correctness problem, since every placement is still checked. On a job this size, try a coarser step before assuming something is stuck, and go back to the default for the run you'll actually cut from.

Geometry libraries have edge cases that only irregular, real shapes reach, and pyFit stands on two of them (`pyclipper` and `shapely`). If a nesting run ever fails with an error from inside `no_fit_polygon` rather than a clear message about your job spec, report the job spec that triggered it rather than assuming your design is at fault.

The Chief Financial Villain took the 30. At ten sheets to a truck, that's three trucks, which she could disguise as a hardware delivery. Thirty-two would have needed a fourth truck, and she pointed out that it's always the fourth truck that someone remembers.

## The Chirality Flag, Now a Packing Decision

Chapter 14 flagged panel shapes as chiral, mirror-image orientations sharing one edge-length signature, and promised the flag would matter again once a material's direction was in play. Here it does. `allow_mirror` on a job-spec part asks the same question at nesting time. `true` (the default) lets pyFit flip a shape freely while searching, right for plain plywood, where a flipped template is harmless. `false` forbids it, right for a one-sided pressure coating, a printed pattern, or any material where a mirrored cut is a different, unusable piece.

**The Under-the-Ocean Prototype** is where it matters. Its frequency-6 hull, squashed to `0.9` on Z, has 42 panel shape groups, and 30 of them are chiral; it's a Class I sphere, so it contains both hands of every lopsided panel (Chapter 14). Its hull carries a one-sided pressure coating, so `allow_mirror: false` isn't caution; it's the physically correct setting. Take its first six chiral groups (`facetype1` through `facetype6`, 20 panels each), 120 panels, and nest them both ways on `0.61 × 0.61` sheets (two-foot squares; the Prototype is modeled at radius 1):

**Prompt:**
> Nest it once with mirroring allowed and once without. How much does disallowing mirroring change the sheet count or utilization?

**What Comes Back** (two `design_nest` results, each shown whole: mirroring allowed, then forbidden; the runs took about 835 and 448 seconds):

```json
{
  "sheets_used": 8,
  "utilization_by_sheet": [
    0.657, 0.6859, 0.6484, 0.6354, 0.659, 0.6424,
    0.6405, 0.1564
  ]
}
{
  "sheets_used": 7,
  "utilization_by_sheet": [
    0.6959, 0.6602, 0.7231, 0.7053, 0.7049, 0.6667,
    0.5689
  ]
}
```

**[IMAGE: examples/images/ocean_nest_mirror_true.png | A pyFit preview of one small square sheet packed with about a dozen triangular panels, some of them flipped.]**
**[CAPTION: The first of 8 sheets for six of the Under-the-Ocean Prototype's chiral panel groups with `allow_mirror: true`.]**

**[IMAGE: examples/images/ocean_nest_mirror_false.png | A pyFit preview of one small square sheet packed with triangular panels, none of them flipped.]**
**[CAPTION: The first of 7 sheets for the same 120 panels with `allow_mirror: false`: fewer sheets, though the packer had fewer options.]**

**What It Means:** Here's the surprise: forbidding mirroring used *fewer* sheets, 7 against 8, with higher utilization on most of them, and it finished in about half the time, since there were half as many orientations to try. That's the opposite of the intuition that removing a degree of freedom can only make packing worse.

Chapter 19 explains why it can happen. pyFit is a bottom-left-fill *heuristic*, not an exhaustive search, and its greedy choices go wherever the available options lead at each step. More legal options at every step doesn't guarantee a better *sequence* of greedy choices, only a bigger menu for the next one. The lesson isn't "disallow mirroring to save plywood": another batch, sheet size, or rotation step could flip the result. It's this: **run both, and trust the measured utilization for your job, not an assumption about which way the setting should push it.**

**Prompt:**
> If I'm using plain plywood with no grain direction, does the chirality flag matter for my build?

**What Comes Back:** Not physically; that's Chapter 14's answer, unchanged. Non-directional material can be flipped freely, so `allow_mirror: true` costs nothing physically and gives pyFit its full search. The flag, and this chapter's surprise, matter only when the material has a direction that a flipped cut would violate. Even then, the only way to know what it costs you in sheets is to nest both ways and look.

## What's Next

Three trucks left for the crater on three different days, with three different hardware-store logos on their doors. The Interpol heat, by the Chief Financial Villain's own index, did not move. The Powers That Be™, whose satellites photograph every road that leads to a volcano, filed the convoy under home improvement: an analyst concluded that someone up there was redoing a kitchen. Three trucks of plywood is a kitchen. Four is a question.

Chapter 21 covers pyFit's four MCP tools, the same iterate-then-commit shape Chapter 18 taught for pyLair, plus one idea no dome design ever needed: progress reports on a job long enough to need them, like the 17-minute one above. It closes with one complete session spanning both toolkits, from a bare polyhedron to a ready-to-cut sheet layout.
