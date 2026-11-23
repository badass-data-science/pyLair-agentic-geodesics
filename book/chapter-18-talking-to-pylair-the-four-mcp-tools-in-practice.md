# Chapter 18: Talking to pyLair — The Four Core MCP Tools in Practice

The AI Henchman, left to itself, would have exported a dome on the first prompt. It was quick, it was willing, and it regarded a written file as a job well done. Our Heroine had other rules. Try a shape; look at it; ask what it costs; change it; and write files once, at the end, when the shape is right. The rules weren't new. They were the workflow pyLair's MCP tools were designed around, and this chapter walks through it.

Every number in this book so far came from pyLair's functions, through the CLI or the tools. This chapter is about the tools as an agent uses them: `design_dome`, `preview_dome`, `get_bill_of_materials`, and `export_dome`, the four that make up the design loop, and why there are four of them instead of one. (pyLair's other three tools, for per-piece assembly, come in Chapter 22.) The blog post that started the project put the workflow plainly: try a shape, look at it, check what it costs, adjust, and export only when it's right. Here is that workflow end to end, on the Actual Secret Lair.

## Four Tools, Four Questions

`design_dome` answers the cheapest question: what does this shape come to, in summary (counts, footprint, height, total strut length), with **no file written**. `preview_dome` answers a visual one: does it look right, rendered inline in the conversation, before anything touches disk. `get_bill_of_materials` answers the build-and-cost question (strut lengths and counts, hub angles, panel shapes, chirality flags, artifact warnings), again with **no file written**. `export_dome` is the only one of the four that writes anything. Two tools to call as often as you like, one to look with, and one to pull the trigger.

## An Iterate-Then-Commit Session

Here is the session: three `design_dome` calls comparing Class III configurations, one `preview_dome`, one `get_bill_of_materials`, and one `export_dome`. The Chief Financial Villain had set the budget: about 120 units of strut at the design radius, give or take five.

**Prompt:**
> Try three different frequencies for this dome using `design_dome` only; don't write any files yet. Which one gives a total strut length closest to my budget of 115 to 125 units?

**What Comes Back** (three `design_dome` results, all Class III on an icosahedron, stretched `1.8`× on Z, truncated at `0.499999`, differing only in `(m,n)`; trimmed, with strut totals rounded):

```json
{"m": 3, "n": 1, "vertex_count": 106, "face_count": 170, "total_strut_length": 97.99}
{"m": 4, "n": 1, "vertex_count": 156, "face_count": 260, "total_strut_length": 121.08}
{"m": 5, "n": 1, "vertex_count": 216, "face_count": 370, "total_strut_length": 144.02}
```

**What It Means:** Nothing was written for any of the three: three cheap summary calls, the comparison shopping `design_dome` exists for. Against the budget, `(4,1)` is the clear fit. It's the configuration Chapter 6 chose for its looks; here it's confirmed by the numbers, through the tool, rather than assumed from memory.

**Prompt:**
> Now preview the one you picked, then check its bill of materials before we export anything.

**What Comes Back** (a `preview_dome` render, then a `get_bill_of_materials` result on the same `(4,1)` configuration, summarized: the two totals are quoted from the report, the counts are the lengths of its tables):

The preview matches Figure 9.2: the same stretched, truncated Class III dome, and still no file written.

```json
{
  "Total material": {"Total strut length": 121.081470138},
  "Total panel material": {"Total panel area": 9.676572145},
  "strut_length_rows": 79,
  "panel_shape_groups": 52,
  "artifact_chords": 0,
  "artifact_panels": 0
}
```

**What It Means:** `121.08` matches the `design_dome` figure; the two tools compute it the same way and package it differently. Zero flagged artifacts confirms Chapter 16's check on this configuration, seen in this session rather than remembered from that chapter. Only now, with a shape chosen, previewed, and costed, does writing files make sense.

**Prompt:**
> Export this configuration: the DXF and VRML, a preview image, STL and OBJ, and hub and panel templates.

**What Comes Back** (an `export_dome` call with `preview`, `stl`, `obj`, `hub_templates`, and `face_templates` set and `face_output` left off, so the DXF is kept, as Chapter 17 explained; abbreviated):

```json
{
  "files_written": [
    "lair.wrl", "lair.dxf", "lair.png", "lair.stl", "lair.obj",
    "lair_hubtype1.dxf", "... 32 hubtype files in all, Chapter 15's count for this dome",
    "lair_facetype1.dxf", "... 52 facetype files in all, matching panel_shape_groups above"
  ],
  "bill_of_materials": { "...": "the same report examined above" }
}
```

**What It Means:** This is the only call in the session that touched the filesystem. Everything before it (three shape comparisons, one visual check, one full cost review) cost nothing but compute, and could have been repeated with ten more candidates without leaving a stray file to clean up.

## Same Validation, Every Interface

**Prompt:**
> Try building this with an invalid Class III configuration, `m` and `n` equal, through `design_dome`. What happens?

**What Comes Back** (the same error through `design_dome`, `export_dome`, or the CLI; through MCP it carries the "Error executing tool" prefix):

```
-c 3 (Class III / Skew) requires --n-frequency to differ from --frequency
(equal values are Class II -- use -c 2 instead). Exiting.
```

**What It Means:** All seven MCP tools and the CLI go through the same `build_dome` in `pylair/api.py`, which calls `validate_geometry_params` before building anything. There's no interface-specific validation anywhere, so an agent exploring with `design_dome` gets the same guardrails as a person typing CLI flags, word for word.

## Iterate Freely, Commit Once

`design_dome` and `get_bill_of_materials` write nothing, and neither does `preview_dome`, which returns its image inside the conversation. Compare ten `(m,n)` pairs, five truncation cutoffs, and three elongations, all 150 combinations if you like, with those tools alone, and you finish with a clean working directory. `export_dome` is the one tool in the set that touches disk, and the discipline of this chapter reduces to one habit: use the free tools until you're satisfied, and only then use the one that isn't.

## What's Next

The AI Henchman, asked afterward to summarize the session, reported that it had made five free calls and one expensive one. Our Heroine considered this the first summary it had produced that she didn't need to check, and checked it anyway.

Part VI turns to the second toolkit: pyFit, and the question none of pyLair's tools answers. Once a design is exported, how are its panels laid out on real sheets? Chapter 19 starts there, with a problem harder, in a different way, than anything in Parts II through V.
