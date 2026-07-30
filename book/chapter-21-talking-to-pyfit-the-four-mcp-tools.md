# Chapter 21: Talking to pyFit — The Four MCP Tools, Progress Notifications, and a Combined Workflow

Chapter 18 taught pyLair's four-tool iterate-then-commit pattern. pyFit has the identical shape — `design_nest`, `preview_nest`, `get_nest_report`, `export_nest` — for exactly the same reason: cheap sanity check, visual check, full report, commitment, in that order. This chapter teaches that pattern's pyFit version, one genuinely new idea neither dome design ever needed, and then closes Part VI with one continuous session spanning both toolkits.

## The Same Four-Tool Shape, on the Nesting Side

`design_nest` answers the cheapest question — sheets used, per-sheet utilization, no files written. `preview_nest` renders the layout inline. `get_nest_report` returns the full placement detail (sheet index, position, rotation, mirror flag for every part instance) — also no files written. `export_nest` is the only one that commits DXFs (and, optionally, preview PNGs) to disk. Here's all three of the free tools, run for real, on a small, deliberately quick subset of the Actual Secret Lair's own panels — four of its 52 real shapes, `20` panels total:

```json
{"tool": "design_nest", "sheets_used": 6,
 "utilization_by_sheet": [0.464, 0.454, 0.579, 0.464, 0.574, 0.114]}
```

```json
{"tool": "get_nest_report", "placements_returned": 20}
```

```json
{"tool": "export_nest", "files_written": ["lair_sheet1.dxf", "lair_sheet1.png", "...", "lair_sheet6.dxf", "lair_sheet6.png"]}
```

**Prompt:**
> Try two different rotation steps for this nesting job using `design_nest` only — don't write any files yet. Which one gives better utilization for the time it takes?

**What Comes Back:** Exactly the same discipline Chapter 18 taught for pyLair's own `design_dome` — try as many rotation-step/sheet-size combinations as you like through `design_nest` alone, and nothing touches disk until you're actually satisfied. `get_nest_report` costs nothing either, for the same reason `get_bill_of_materials` didn't: both return everything but a file path.

## A Genuinely New Idea: Progress on a Call Long Enough to Need It

Nothing in pyLair's own four tools ever needed this, because nothing pyLair computes takes long enough to matter. Nesting is different — Chapter 20 already showed a real job running for minutes — and pyFit's tools report **MCP progress notifications**: a placement heartbeat, sent while a long call is still running, so a slow job never looks like a hung one.

Here's why that's harder than it sounds, and worth understanding rather than taking for granted: a *synchronous* MCP tool function blocks its server's entire event loop for the whole duration of the call. If `pack()` ran directly inside a plain `def design_nest(...)`, the server couldn't send a single progress message until the function returned — by which point there'd be nothing left to report progress *on*. pyFit's tools are declared `async def` specifically to avoid this: the actual packing work runs in a separate worker thread (`asyncio.to_thread`), while the event loop stays free to relay that thread's own progress callback back out as real MCP notifications, live, while the work is still happening.

This is worth confirming rather than trusting as a design description. Here's a real, independent reproduction — a `40`-part nesting job, run with a stand-in progress-reporting client attached, timestamping every notification as it actually arrives:

```
elapsed: 74.36s, 88 progress notifications
first: t=0.003s (0/40 placed)
last:  t=74.241s (39/40 placed)
```

**What It Means:** `88` notifications, arriving continuously from three milliseconds after the call started to essentially its final moment — not bunched at the end, which is exactly what a genuinely blocked event loop would look like if this mechanism didn't work. This is the same live-progress mechanism this project's own engineering notes report verifying on a shorter job (`~5.6`s, `~33` notifications) — a different real run, a different real duration, the identical real behavior.

One more thing worth confirming rather than assuming: what happens with no progress-reporting client attached at all.

```python
await design_nest(sheet_width=1.0, sheet_height=0.8, parts=parts, rotation_step_degrees=15.0, ctx=None)
# -> {'sheets_used': 1, 'utilization_by_sheet': [0.5625]}  (succeeds normally, no notifications, no error)
```

**What It Means:** No progress token, or a direct function call the way a test suite makes one, is simply a no-op — the packing still runs in its worker thread exactly the same way, nothing about the result changes, and nothing needs to opt out of anything to get correct behavior either way.

## Same Validation, Every Interface — Again

**Prompt:**
> Try a malformed job spec — a part missing its required `"name"` field — through `design_nest`. What happens?

**What Comes Back:** The identical error Chapter 2 already showed you coming from the plain `pyfit` CLI on the same malformed spec:

```
Part spec is missing required field "name".
```

**What It Means:** One engine, `pyfit/api.py`, underlies every one of pyFit's four MCP tools and its CLI, the same way Chapter 18 confirmed for pyLair's own four tools. There is no separate, looser validation path anywhere in either project's agentic interface.

## One Continuous Session, Start to Finish

Here, narrated as one transcript, is the complete arc this book has been building since Chapter 1's cold open — every number below is one this book has already shown you, real, from the chapter that first produced it:

1. **`design_dome`**, several times (Chapter 18): comparing Class III `(3,1)`/`(4,1)`/`(5,1)` — `97.99`/`121.08`/`144.02` total strut length — settling on `(4,1)` against a strut budget, no files written.
2. **`preview_dome`** (Chapter 18): one inline check confirming the shape.
3. **`get_bill_of_materials`** (Chapters 12–16, 18): hub angles, strut clustering, panel shapes, chirality flags, zero flagged artifacts — the full cost and buildability interrogation, still no files written.
4. **`export_dome`** with `face_templates=True` (Chapters 15, 17, 18): the only file-writing pyLair call in the whole session — `52` real panel cutting templates, `32` real hub connector templates, a DXF, a VRML, an STL, an OBJ.
5. **A real job spec, built with zero hand-typing** (Chapter 20): every one of those `52` templates' own file paths and panel counts, straight from pyLair's own `"Panel Cutting Templates"` report, into a pyFit job spec's `"dxf"`/`"quantity"` fields.
6. **`design_nest`**, several times (this chapter): trying rotation steps and sheet sizes, no files written, until the layout looks worth committing to.
7. **`preview_nest`** and **`get_nest_report`** (this chapter): one visual check, one full placement interrogation.
8. **`export_nest`** (this chapter): the second, and last, file-writing call in the entire session — real, numbered `_sheetN.dxf` files, ready to hand to a laser cutter.

**Prompt:**
> Walk me through this entire dome, from picking a polyhedron to a ready-to-cut sheet layout, as one continuous session.

**What Comes Back:** Exactly the eight steps above, in that order — two design toolkits, eight tools total, and only two moments in the whole session where anything was actually written to disk. Everything else was free to try, reconsider, and try again.

**What It Means:** This is the entire discipline both toolkits have been teaching since Chapter 1, now shown as one uninterrupted arc rather than two separate lessons: iterate freely through whichever tool costs nothing, commit only once, and never confuse "the design looks right" with "the build is validated" along the way.

## What's Next

Part VII closes the book. Chapter 22 is a prompting clinic spanning both toolkits at once — real flawed prompts, rewritten, including one that looks like a single question but actually needs both pyLair and pyFit to answer honestly. Chapter 23 is the retrospective this whole book has been setting up since its very first gotcha, and Chapter 24 sends the Actual Secret Lair off to be built.
