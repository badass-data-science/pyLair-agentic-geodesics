# Chapter 18: Talking to pyLair — The Four MCP Tools in Practice

Every real number this book has shown you so far came from calling pyLair's underlying functions directly or through its CLI. This chapter is about the other real interface: `design_dome`, `preview_dome`, `get_bill_of_materials`, and `export_dome`, the four MCP tools an agent actually calls — and why there are four of them instead of one. The blog post that started this whole project put it plainly: try a shape, look at it, check what it costs, adjust, and only export once it's actually right. This chapter narrates exactly that workflow, end to end, on the real Actual Secret Lair.

## Four Tools, Four Different Questions

`design_dome` answers the cheapest question: given these parameters, what does the resulting shape look like in summary — vertex/edge/face counts, footprint, height, total strut length — with **no file written at all**. `preview_dome` answers a visual question: does this actually look right, rendered inline, before committing to anything on disk. `get_bill_of_materials` answers the cost/build question: strut lengths and counts, hub angles, panel shapes, chirality flags, artifact warnings — again, **no file written**. `export_dome` is the only one of the four that commits anything to disk at all. Two tools free to call as many times as you like; one to look at; one to actually pull the trigger.

## A Real Iterate-Then-Commit Session

Here's that whole session, narrated as it actually happened rather than assumed — three `design_dome` calls comparing candidate Class III configurations, one `preview_dome` check, one `get_bill_of_materials` interrogation, and finally one `export_dome` commitment.

**Prompt:**
> Try three different frequencies for this dome using `design_dome` only — don't write any files yet. Which one gives a strut count closest to my budget?

**What Comes Back** (three real `design_dome` results, all Class III on an icosahedron, elongated `1.8`× on Z, truncated at `0.499999`, differing only in `(m,n)`):

```json
{"m": 3, "n": 1, "vertex_count": 106, "face_count": 170, "total_strut_length": 91.79}
{"m": 4, "n": 1, "vertex_count": 156, "face_count": 260, "total_strut_length": 114.85}
{"m": 5, "n": 1, "vertex_count": 216, "face_count": 370, "total_strut_length": 137.77}
```

**What It Means:** Nothing was written to disk for any of these three — just three cheap summary calls, exactly the kind of comparison-shopping `design_dome` exists for. Against a strut-length budget in the neighborhood of `110`–`120` units, `(m,n)=(4,1)` is the clear fit — not coincidentally the same configuration this book settled on back in Chapter 6, but arrived at here through the tool this chapter is actually teaching, not assumed from memory.

**Prompt:**
> Now preview the one you picked, then check its bill of materials before we export anything for real.

**What Comes Back** (a real `preview_dome` render, then a real `get_bill_of_materials` result on the same `(4,1)` configuration):

The preview matches Figure 9-2 from several chapters back — the same elongated, truncated Class III dome, still no file written by this call either.

```json
{
  "Total material": {"Total strut length": 114.848689744},
  "Total panel material": {"Total panel area": 9.676572145},
  "strut_length_rows": 69,
  "panel_shape_groups": 52,
  "artifact_chords": 0,
  "artifact_panels": 0
}
```

**What It Means:** `114.85` matches the `design_dome` estimate from the first prompt almost exactly (small differences in later decimal places are expected — `design_dome`'s own strut-length figure and `get_bill_of_materials`'s are computed the same way, just packaged differently). Zero flagged artifact chords or panels confirms Chapter 16's own check comes back clean on this specific configuration — worth actually seeing in this session rather than assumed from that earlier chapter's own finding. Only now, with a shape chosen, previewed, and cost-checked, does exporting for real make sense.

**Prompt:**
> Export this configuration for real — DXF, face data, STL, hub and panel templates, all of it.

**What Comes Back** (a real `export_dome` call, files actually written this time):

```json
{
  "files_written": [
    "lair.wrl", "lair.stl", "lair.obj", "lair.png",
    "lair_facetype1.dxf", "... 51 more facetype files (52 total, matching the panel_shape_groups above) ...",
    "lair_hubtype1.dxf", "... 26 more hubtype files (27 total, per Chapter 15's own count for this exact dome) ..."
  ],
  "bill_of_materials": { "...": "the same report just interrogated above" }
}
```

**What It Means:** This is the only one of the four calls in this entire session that touched the filesystem. Everything before it — three shape comparisons, one visual check, one full cost interrogation — cost nothing but compute, and could have been repeated ten more times with ten more candidate configurations without a single stray file to clean up afterward.

## Same Validation, Every Interface

**Prompt:**
> Try building this with an invalid Class III configuration — say, `m` and `n` equal — through `design_dome`. What happens?

**What Comes Back** (a real error, identical whether triggered through `design_dome`, `export_dome`, or the CLI):

```
-c 3 (Class III / Skew) requires --n-frequency to differ from --frequency
(equal values are Class II -- use -c 2 instead). Exiting.
```

**What It Means:** All four MCP tools, and the CLI, funnel through the exact same `pylair/api.py:validate_geometry_params` — there is no interface-specific validation anywhere in this project, which is why an agent using `design_dome` to explore configurations gets exactly the same guardrails a human typing CLI flags does, word for word, not a looser or differently-worded approximation of them.

## Iterate Freely, Commit Once

`design_dome` and `get_bill_of_materials` write nothing at all — a reader worried about cluttering a directory while comparing ten candidate `(m,n)` pairs, five truncation cutoffs, and three elongation ratios can run all eighteen combinations through those two tools alone and end the session with a clean working directory and zero wasted files. `export_dome` is the one tool in this four-tool set that ever touches disk, and the entire discipline this chapter teaches reduces to one habit: reach for the free tools until you're actually satisfied, and only then reach for the one that isn't.

## What's Next

Part VI turns to a second toolkit entirely: pyFit, and the question none of this chapter's four tools has ever answered — once a design is exported, how do its panels actually get laid out on real sheet stock? Chapter 19 starts there, with a problem that turns out to be harder, in a genuinely different way, than anything Parts II through V had to solve.
