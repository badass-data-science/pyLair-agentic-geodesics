# Chapter 13: Counting Struts — Clustering, Rounding, and the Merge Tradeoff

The Chief Financial Villain had discovered that every distinct strut length meant a separate saw setup, a separate labeled bin, and a separate line on the cutting crew's timesheet. The bill of materials for the Actual Secret Lair had 79 distinct lengths. She found the setting that controlled the count, turned it down, and came back delighted: two. Two strut types for the whole dome. The Foreman read the report over her shoulder and asked, very politely, which of the two lengths she would like the crown built from, since the real struts there came in about seventy varieties.

A bill of materials is useful only if its rows mean what they claim: "cut this many struts to this length." This chapter is about the setting that decides how those rows are formed, `bom_rounding_precision`, and a design choice in how it works that's worth understanding before you ever reach for a non-default value, as the Chief Financial Villain did.

## Why Lengths Are Clustered, Not Rounded One by One

Here is the naive approach `get_bill_of_materials` deliberately avoids: round each strut's length to `bom_rounding_precision` decimal places, then group rows by the rounded value. It sounds reasonable and fails in a specific way. Floating-point geometry produces tiny noise: two struts that are truly the same length might come back as `0.4748131498...` and `0.4748131503...`, different in the tenth decimal place, meaningless to any saw. Round each to 9 places and they can land on opposite sides of a rounding boundary, splitting one real strut length into two rows over a difference that was never real.

The implementation (whose comments in `pylair/bill_of_materials.py` explain this) is more careful. It sorts all the lengths and starts a new cluster wherever the gap between consecutive lengths exceeds a tolerance; it never rounds first. The tolerance comes from `bom_rounding_precision` itself:

```python
cluster_tolerance = max(scale * 1e-9, 0.5 * 10 ** (-rounding_precision))
```

Read two things in that line. First, the tolerance never drops below a tiny, scale-relative floor (`scale * 1e-9`, where `scale` is the dome's longest strut), so even at an extremely fine setting, pure floating-point noise still merges instead of printing spurious near-duplicates. Second, and this is the design decision to understand: **`bom_rounding_precision` isn't only display precision.** The number that decides how many decimal places print also decides how far apart two lengths can be and still share a row. One setting, two jobs, on purpose.

## Both Roles at Once, on a Real Dome

Here is the Actual Secret Lair (Class III `(4,1)`, stretched, truncated at `0.499999`) at four values of `bom_rounding_precision`, all describing the same 415 struts.

**Prompt:**
> Get this dome's bill of materials at `bom_rounding_precision` 9, 3, 2, and 1. How many distinct strut-length rows does each report?

**What Comes Back** (from four `get_bill_of_materials` calls, counting the rows of each one's strut-length table):

```json
{"bom_rounding_precision": 9, "distinct_rows": 79}
{"bom_rounding_precision": 3, "distinct_rows": 61}
{"bom_rounding_precision": 2, "distinct_rows": 20}
{"bom_rounding_precision": 1, "distinct_rows": 2}
```

**[IMAGE: examples/images/strut_clustering_comparison.png | Two bar charts of strut counts by length for the same dome. Left: 79 narrow bars, mostly of height 5. Right: 20 bars, several of them 50 to 60 struts tall.]**
**[CAPTION: The same 415 struts clustered at the default `bom_rounding_precision=9` (left, 79 rows, mostly groups of 5, matching the dome's five-fold symmetry) and at a coarse `bom_rounding_precision=2` (right, 20 rows, some 50 to 60 struts wide). The dome didn't change; only how readily nearby lengths are treated as "the same."]**

**Prompt:**
> Generate the bill of materials at the default rounding, then again at `bom_rounding_precision=2`. Do any distinct strut lengths get merged at the coarser setting?

**What Comes Back** (a case found by comparing the two reports): at the default, two separate rows exist, `0.047485003` (5 struts) and `0.051270148` (5 struts), a difference of about `0.0038` units, nowhere near floating-point noise. At `bom_rounding_precision=2`, both collapse into one row: `length: 0.05, count: 10`.

**What It Means:** That's the merge tradeoff, in numbers. Two lengths differing by nearly 8%, a difference calipers catch instantly, are reported as one strut type at the coarser setting. Every example in this book is computed at radius 1; at the Actual Secret Lair's planned 2.5-meter radius, every length scales by 2.5, and that gap becomes about 9.5 millimeters. Whether the merge is a useful simplification or a mistake depends on what you do next with the number, which is why this isn't a bug to report but a tradeoff to choose.

## When Coarser Helps, and When It Hurts

At the default, `bom_rounding_precision=9`, the closest pair of distinct lengths on this dome is about `4.7×10⁻⁶` apart, roughly 9,400 times the default's cluster tolerance of `5×10⁻¹⁰`, so nothing merges that shouldn't. A coarser value is worth choosing when your tools can't distinguish lengths that close anyway: a saw that can't tell two struts half a millimeter apart isn't helped by a report insisting they differ, and merging them into one row saves a setup and a bin.

It hurts for the same reason, applied to the wrong case. Lower `bom_rounding_precision` far enough to merge lengths that *do* matter for your build, like the 9.5-millimeter pair above, and you've told the bill of materials to lie to you, cheaply and quietly. A merged row doesn't look wrong; it just no longer describes the two different things it used to.

**Prompt:**
> My laser cutter can't reliably distinguish lengths less than 0.5 mm apart. What `bom_rounding_precision` should I use?

**What Comes Back:**
> Choose the value whose `cluster_tolerance` matches your tool's tolerance, in the units your radius is expressed in. For any practical setting, `cluster_tolerance ≈ 0.5 × 10⁻ᵇ` (the noise floor matters only at extremely fine settings), so for a target tolerance `t`, `b ≈ −log₁₀(2t)`. With the radius in meters and a 0.5 mm (`0.0005 m`) tolerance, `b ≈ −log₁₀(0.001) = 3`: `bom_rounding_precision=3` gives a cluster tolerance of exactly `0.0005`. Get the units right first. The formula assumes your `radius` is in the same units as your tolerance; use `3` on a dome whose radius is secretly in centimeters and it will merge lengths ten times further apart than you intended.

**What It Means:** There's no universally correct `bom_rounding_precision`. The right value depends on two things only you can supply: the units your dome is modeled in, and the tolerance your fabrication process can resolve. The default, `9`, is chosen to almost never merge anything, the safe assumption until you have a specific reason to choose otherwise. When you do lower it, check the report before cutting material to a length that used to be two lengths.

## What's Next

The Chief Financial Villain set the precision back to 9 and, after some arithmetic with the Foreman about the saw's real tolerance at a 2.5-meter radius, settled on 3, with the dome modeled at its real radius of 2.5 meters so that the tolerance meant half a millimeter of real strut: 70 rows instead of 79, with nothing merged that the saw could tell apart. She considered it a negotiated victory.

Chapter 14 moves from strut lengths to panel shapes and brings back chirality, Chapter 6's whole-dome mirror-image relationship, now at the scale of a single flat triangle, and the trap it sets for anyone about to order directional cladding.
