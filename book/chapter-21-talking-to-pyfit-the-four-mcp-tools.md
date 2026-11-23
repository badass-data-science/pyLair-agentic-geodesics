# Chapter 21: Talking to pyFit — The Four MCP Tools, Progress Notifications, and a Combined Workflow

The first time the AI Henchman ran a large nesting job, it went quiet for a minute and a half. Our Heroine, who had watched the Rival's chatbot confidently produce nonsense, found an agent that said *nothing* even more unsettling. Was it working? Was it stuck? Had it, in some sense, left? pyFit's answer to that question is the new idea in this chapter.

Chapter 18 taught pyLair's iterate-then-commit loop. pyFit has the same shape, `design_nest`, `preview_nest`, `get_nest_report`, and `export_nest`, for the same reason: cheap sanity check, visual check, full report, then commitment. This chapter teaches pyFit's version, one idea no dome design ever needed, and then one continuous session spanning both toolkits.

## The Same Four-Tool Shape, on the Nesting Side

`design_nest` answers the cheapest question: sheets used and utilization per sheet, no files written. `preview_nest` renders each sheet's layout inline. `get_nest_report` returns every placement (sheet, position, rotation, and mirror flag for each part), still with no files. `export_nest` is the only one that writes anything: one DXF per sheet and, optionally, a preview PNG of each. Here they are on a deliberately small batch of the Actual Secret Lair's panels, four of its 52 shapes, five panels each, on small `0.6 × 0.5` sheets:

**Prompt:**
> Nest these four panel templates, five of each, on 0.6 by 0.5 sheets. Summarize first, then give me the full report, then export.

**What Comes Back** (from `design_nest`, `get_nest_report`, and `export_nest` in turn; utilizations rounded, the report and file list summarized):

```json
{"tool": "design_nest", "sheets_used": 5,
 "utilization_by_sheet": [0.580, 0.598, 0.550, 0.577, 0.343]}
```

```json
{"tool": "get_nest_report", "sheets_used": 5, "placements_returned": 20}
```

```json
{"tool": "export_nest", "files_written": ["lair_sheet1.dxf", "lair_sheet1.png", "...", "lair_sheet5.dxf", "lair_sheet5.png"]}
```

**What It Means:** Two free calls and one that writes: five sheets, twenty placements (one per panel), ten files. Chapter 23 uses this batch to measure how far real sheet use departs from pyLair's theoretical panel area.

**Prompt:**
> Try two other rotation steps for this job using `design_nest` only; don't write any files yet. Do they change the sheet count?

**What Comes Back** (from `design_nest` at the default 15° step and at 30° and 45°):

```json
{"rotation_step_degrees": 15, "sheets_used": 5}
{"rotation_step_degrees": 30, "sheets_used": 6}
{"rotation_step_degrees": 45, "sheets_used": 5}
```

**What It Means:** It's the same discipline as Chapter 18's `design_dome`: try as many settings as you like through `design_nest`, and nothing touches disk until you're satisfied. Notice, too, that the coarser 30° step needed a sixth sheet while the even coarser 45° didn't. A greedy heuristic doesn't get steadily better or worse as you give it more or fewer options; Chapter 20 meets the same effect with mirroring. Try, and read the numbers.

## A New Idea: Progress on a Call Long Enough to Need It

Nothing in pyLair's tools needed this, because nothing pyLair computes takes long enough to matter. Nesting does: the whole Actual Secret Lair, in Chapter 20, takes minutes. So pyFit's tools send **MCP progress notifications**, a placement heartbeat while a long call is still running, so a slow job never looks like a hung one.

That's harder than it sounds. An MCP server handles requests on an event loop, and a tool written as an ordinary (synchronous) function blocks that loop for the whole call. If the packer ran inside a plain `def design_nest(...)`, the server couldn't send a single progress message until the function returned, when there'd be nothing left to report. pyFit's tools are declared `async def` for this reason: the packing runs in a worker thread (`asyncio.to_thread`), and the event loop stays free to relay the thread's progress callback as MCP notifications while the work is still happening.

That's worth confirming rather than trusting as a description. Here is a reproduction: a 40-panel job (eight of the Lair's shapes on the same small sheets), called through an MCP client that timestamps each notification as it arrives:

```
elapsed: 23.03s, 214 progress notifications
first: t=0.008s (placed 0/40 parts, checking sheet 1)
last:  t=23.026s (placed 39/40 parts, checking sheet 10)
```

**What It Means:** 214 notifications, arriving continuously from eight milliseconds after the call began to its final moment, not bunched at the end, which is what a blocked event loop would produce. pyFit's `AGENTS.md` records the same behavior on a different, shorter job (about 33 notifications over 5.6 seconds): a different run, the same mechanism. Timings depend on the machine; the shape of the arrivals doesn't. The AI Henchman, given a client that displayed them, stopped going quiet.

And with no progress-reporting client at all, as when a test suite or a script calls the function directly:

```python
await design_nest(sheet_width=0.6, sheet_height=0.5, parts=parts)  # ctx defaults to None
# -> {'sheets_used': 5, 'utilization_by_sheet': [0.5796, 0.5984, 0.5502, 0.5771, 0.3434]}
```

**What It Means:** No client, or no progress token, means no notifications and nothing else different: the packing runs in its worker thread the same way, the result is identical, and nothing has to opt out to get correct behavior.

## Same Validation, Every Interface, Again

**Prompt:**
> Try a malformed job spec, a part missing its required `"name"` field, through `design_nest`. What happens?

**What Comes Back** (the same message the `pyfit` CLI gives for the same spec; through MCP it carries the "Error executing tool" prefix):

```
Part spec is missing required field "name".
```

**What It Means:** One engine, `pyfit/api.py`, sits under all four of pyFit's MCP tools and its CLI, as Chapter 18 showed for pyLair. Neither project has a separate, looser validation path for agents.

## One Continuous Session, Start to Finish

Here, as one transcript, is the arc the book has built since Chapter 1. Every number below comes from the chapter that first produced it:

1. **`design_dome`**, three times (Chapter 18): Class III `(3,1)`, `(4,1)`, `(5,1)`, at `97.99`, `121.08`, and `144.02` units of strut, settling on `(4,1)` against the Chief Financial Villain's budget. No files written.
2. **`preview_dome`** (Chapter 18): one inline look at the shape.
3. **`get_bill_of_materials`** (Chapters 12 through 16, 18): hub angles, strut clustering, panel shapes, chirality flags, empty artifact lists. Still no files.
4. **`export_dome`** with templates (Chapters 15, 17, 18): the only pyLair call that writes files: `52` panel templates, `32` hub templates, a DXF, a VRML, an STL, an OBJ.
5. **A job spec built with no hand-typing** (Chapter 20): the 52 templates' paths and panel counts, from pyLair's "Panel Cutting Templates" report, into a pyFit job spec's `"dxf"` and `"quantity"` fields.
6. **`design_nest`**, several times (this chapter and Chapter 20): rotation steps and sheet sizes, no files, until the layout is worth keeping.
7. **`preview_nest`** and **`get_nest_report`** (this chapter): one visual check, one full placement report.
8. **`export_nest`** (this chapter): the second and last file-writing call of the session, numbered `_sheetN.dxf` files ready for a laser cutter.

**Prompt:**
> Walk me through this whole dome, from picking a polyhedron to a ready-to-cut sheet layout, as one continuous session.

**What Comes Back:** The eight steps above, in that order: two toolkits, eight different tools, and only two moments in the session when anything was written to disk. Everything else was free to try, reconsider, and try again.

**What It Means:** It's the discipline both toolkits have taught since Chapter 1, as one uninterrupted arc instead of two lessons: iterate freely with the tools that cost nothing, commit once, and never confuse "the design looks right" with "the build is validated."

## What's Next

That session leaves one question deliberately open. A pyFit nest report says which sheet and position each *part* landed at, but with one part per panel *shape*, it can't say which specific panel of the dome a given cut piece is. Chapter 22 answers that: a per-instance assembly manifest, a job spec whose parts keep their identity through pyFit, and a bug that work caught along the way.

Part VII closes the book after that: a prompting clinic across both toolkits (Chapter 23), the retrospective (Chapter 24), and moving day (Chapter 25).
