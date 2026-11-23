# Chapter 16: Spotting the Slivers — Truncation-Artifact Chords and Panels

The Junior Henchman came to the Unbending Foreman with a cutting list for a test dome and one question. Line six asked for ten struts, each 0.000000236 units long. At a 2.5-meter radius that is about six ten-thousandths of a millimeter: well under the width of a human hair, and smaller than the sawdust the cut would make. "Do I cut these," the Junior Henchman asked, "or do I just say I did?"

Chapter 9's flat-chord error refuses outright when a truncation cutoff lands *exactly* on a vertex ring. This chapter is about the case one step away: a cutoff extremely close to a ring but not on it. That's mathematically valid, structurally absurd, and, unlike Chapter 9's failure, something pyLair lets through. Why it lets it through, and how it flags the result instead, is this chapter's subject.

## A Cutoff That's Close, Not Exact

Move a truncation cutoff a hair closer to a vertex ring than the documented safe value (not `0.5`, but `0.4999999`, one more `9` than `0.499999`) and `truncate()` doesn't refuse. It succeeds and produces something real but useless: struts shrunk to almost nothing, panels clipped to slivers. A comment in `pylair/bill_of_materials.py` uses this very cutoff as its example:

> Real geodesic subdivisions essentially never produce legitimate strut-length classes differing by more than roughly one order of magnitude from each other (e.g. a frequency-6 Class I icosahedron's longest and shortest struts differ by well under 2x) -- so a strut three orders of magnitude below the dome's largest is overwhelmingly more likely to be a sliver left over from a truncation cutoff landing extremely close to (but not exactly on) a vertex ring, as observed for e.g. -t 0.4999999.

The threshold, anything under `0.1%` of the dome's longest strut (`SMALL_CHORD_ARTIFACT_RATIO = 1e-3`), is what it sounds like: since real strut classes don't span three orders of magnitude, anything that far below the longest strut is far more likely to be an artifact of the cut than a deliberate tiny strut.

## Reproducing the Slivers

Here is that case on a frequency-6 Class I icosahedral sphere, the construction Chapter 9 showed has a ring of vertices exactly on the equator:

**Prompt:**
> Truncate this dome at a cutoff suspiciously close to a vertex ring. Does the report flag any artifact chords or panels?

**What Comes Back** (counting the "Possible truncation-artifact chords" and "Possible truncation-artifact panels" lists in `get_bill_of_materials`, with a cutoff well clear of the ring for comparison):

```json
{"truncation": 0.4999999, "artifact_chords": 6, "artifact_panels": 3}
{"truncation": 0.45,      "artifact_chords": 0, "artifact_panels": 0}
```

One of the flagged chord rows, the one on the Junior Henchman's cutting list:

```json
{"length": 2.36e-07, "count": 10}
```

Some of the flagged struts close the dome's base ring. Every cut edge gets a strut (Chapter 15), and at a cutoff this close to a ring, several struts leaving one ring vertex downward all cross the cut within a ten-millionth of that vertex. The base-ring segments joining those crossing points are near zero too. It's the same near-degenerate ring causing the same kind of sliver, in one more place.

The three flagged panel shapes are degenerate in two different ways. Their edge lengths, measured from the dome's face data (the report itself prints panel edges to three decimals, so these show there as `0.0`), are:

```json
{"edge_lengths": [2.31e-07, 0.206, 0.206], "count": 40}
{"edge_lengths": [2.31e-07, 2.34e-07, 2.35e-07], "count": 30}
{"edge_lengths": [2.35e-07, 0.215, 0.215], "count": 20}
```

**What It Means:** The second shape is a fully degenerate sliver: all three edges collapsed to almost nothing, a point pretending to be a triangle. The first and third are "needles": two ordinary edges (`0.206` or `0.215`, matching real panels elsewhere on the dome) and a third squeezed to about a millionth of their length, a triangle so thin it would be a slit, not a panel. All three are mathematically valid triangles. None is buildable. The Junior Henchman's answer was "neither": these lines don't describe parts.

**[IMAGE: examples/images/sliver_panels.png | Three triangles at the same scale: an ordinary panel on the left; a needle in the center that is too thin to see; and a degenerate sliver on the right, still invisible even in a 100,000-times zoom.]**
**[CAPTION: An ordinary panel from this dome (left) beside two sliver artifacts at the same scale: a needle (center), invisible at this zoom, and a fully degenerate sliver (right), still invisible at the dome's scale even magnified 100,000×. Nothing is exaggerated; every triangle is a computed panel from the dome.]**

## Even the "Safe" Cutoff Isn't Immune Here

This is a stronger and more honest claim than "use `0.499999` and you're covered": on this frequency-6 dome, the documented safe cutoff still produces flagged artifacts, just ten times larger ones than the unsafe cutoff.

**Prompt:**
> Now re-cut at the documented safe cutoff instead. Did the flagged lists shrink, and did they disappear entirely?

**What Comes Back** (the same two lists, counted, at both cutoffs):

```json
{"truncation": 0.499999,  "artifact_chords": 8, "artifact_panels": 3}
{"truncation": 0.4999999, "artifact_chords": 6, "artifact_panels": 3}
```

**What It Means:** The slivers grew by a factor of ten, from about `2.4×10⁻⁷` to about `2.4×10⁻⁶`, because the safe cutoff sits ten times further from the ring, but they did **not** disappear. Both cutoffs are within a millionth of the range of this frequency's equatorial ring, close enough that slivers survive either way. A clean result, with both lists empty, came only at a cutoff well clear of the ring (`0.45`), and would at an odd frequency, which puts no ring on the equator.

"Reduces the risk" and "eliminates the risk" are different claims, and this book won't blur them, even about its own advice. `0.499999` is a sensible default because it's *usually* far enough from wherever a ring lands, and it reliably avoids Chapter 9's refusal. But "usually" is doing work in that sentence, and this frequency is a reproducible case where it isn't enough. The habit to keep isn't "trust the safe value"; it's "generate the report and look at whether the artifact lists are empty," whatever cutoff got you there.

The Actual Secret Lair passes. At `truncation_z=0.499999`, its Class III `(4,1)` lattice, stretched 1.8×, has no ring near the cut, and both of its artifact lists come back empty. The Unbending Foreman checked them anyway, which was the point.

## Two Safety Nets, Not One

This chapter's flagging and Chapter 9's flat-chord error solve different problems, and neither substitutes for the other. The error refuses an **exact** degenerate case, a chord lying in the cutoff plane, where the math would otherwise divide by zero. The flags surface a **near**-degenerate case that's numerically valid: nothing divides by zero, nothing crashes, the geometry is fine and absurd. Refusing *every* short strut the way Chapter 9 refuses the exact case would reject many legitimate designs (plenty of subdivisions have honestly short struts near a pole or a tight cut) along with the rare artifacts. Flagging is the right compromise: a builder shouldn't have to scan a hundred-row report for the one line that's secretly an artifact, and the tool shouldn't refuse a good design because one strut is short.

## What's Next

Part IV closes here: five chapters on what a bill of materials promises, from hub angles to cutting templates to the artifacts that can hide among them. The Junior Henchman's test dome was re-cut at a cutoff clear of its ring, and line six vanished from the cutting list.

Part V takes the finished, checked Actual Secret Lair out the door: export files, and the MCP tools that turn "design a dome" from one command into the iterate-then-commit workflow this book has been building toward since Chapter 1.
