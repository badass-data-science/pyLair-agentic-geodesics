# Chapter 17: Getting It Out the Door — DXF, VRML, STL, OBJ

Everything from Chapter 3 onward has been building toward this moment: the Actual Secret Lair, fully subdivided, shaped, and accounted for, finally written to real files a real downstream tool can open. This chapter is about choosing the right file for the right job — four export formats, four genuinely different purposes, and one prerequisite from Part III that makes two of them possible on a truncated dome at all.

## Four Formats, Four Different Jobs

**DXF**, written by default, is for CAD import — the format a fabricator's own software, a CNC controller, or a laser cutter's driver actually expects. **VRML** (`.wrl`), also written by default, is for 3D display — a format built for showing a shape, not manufacturing it. **STL** and **OBJ** (`export_dome`'s `stl`/`obj` parameters) are for 3D printing — a scale model of the dome's own surface, not its strut skeleton (more on that distinction below). None of the four is a strictly better version of another; each answers a question the others don't.

*(Figure 17-1: A real pyLair DXF export, loaded back into a CAD viewer — the actual output of the default export path, not a mockup.)*

![A pyLair-exported dome loaded into CAD software](../sample_image.png)

*(Figure 17-2: A second real CAD import, from pyLair's own earlier documentation.)*

![Another real CAD-imported dome](../blog-posts/CAD_dome.jpg)

## Why `face_output=True` Skips DXF Entirely

Here's a detail worth knowing precisely rather than discovering by a missing file: `export_dome` treats its `face_output` parameter as a genuinely different code path, not an additional file alongside the default two. With `face_output=False` (the default), you get a wireframe VRML plus a DXF — both built from chords alone. With `face_output=True`, you get a **face-inclusive** VRML instead of the wireframe one, and **no DXF file is written at all**. This isn't an oversight; DXF's own wireframe convention here has no natural way to carry face/panel information the way the face VRML path does, so `export_dome` simply doesn't try to produce one.

This matters practically: if your workflow needs *both* a wireframe DXF for hub/strut reference *and* face data for STL/OBJ/panel templates, that's two separate `export_dome` calls, not one call with every option turned on at once — a real distinction worth planning for before assuming `face_output=True` alongside `stl`/`obj` gets you a DXF too.

## Multi-Axis Truncation, Face-Exported, Proven Live

Chapter 10 fixed a real historical gap: face-aware export used to only work correctly on an untruncated sphere. Here's that fix, exercised on the hardest real case this book has built — the Actual Secret Lair, truncated on **two** axes at once (`X` at `0.3`, `Z` at the documented safe `0.499999`), with every face-dependent output requested simultaneously.

**Prompt:**
> Export this dome — Class III `(4,1)`, elongated `1.8`× on Z, truncated on X at `0.3` and Z at `0.499999` — with `face_output=True`, `stl=True`, `obj=True`, `preview=True`, `hub_templates=True`, and `face_templates=True` all at once. Which of the files that come back actually require the face data to have been preserved correctly through truncation?

**What Comes Back** (a real `export_dome` result — real files, real sizes):

```json
{
  "files_written": [
    "lair.wrl", "lair.stl", "lair.obj", "lair.png",
    "lair_facetype1.dxf", "... 91 total facetype files",
    "lair_hubtype1.dxf", "... 71 total hubtype files"
  ]
}
```

```
lair.wrl              11,448 bytes   (face-inclusive VRML)
lair.stl              60,129 bytes   (3D-printable surface mesh)
lair.obj              10,321 bytes   (3D-printable surface mesh)
lair.png             180,646 bytes   (preview image)
```

**What It Means:** Every one of these files needed correctly-clipped face data surviving *two* sequential truncation passes (Chapters 9 and 10's own subject) to even exist — `.wrl`, `.stl`, `.obj`, and every `facetype`/`hubtype` template all require face data (`face_output`, `stl`, `obj`, `face_templates`, `cost_per_unit_area`, `panel_areal_density`, per `export_dome`'s own parameter list), and none of them errored or produced a visibly broken shape despite two axes of truncation both clipping through real triangles along the way. This is Chapter 10's fix, demonstrated rather than just claimed: 91 distinct panel shapes and 71 distinct hub shapes, from a dome cut on two axes at once, exported without incident.

The plain wireframe DXF, by contrast, needs a *separate* call with `face_output=False` (or simply omitted):

**Prompt:**
> Export the same dome again, but this time without `face_output` — I want the plain wireframe DXF.

**What Comes Back** (a real `export_dome` result):

```
lair-wireframe.dxf   50,545 bytes
lair-wireframe.wrl   11,587 bytes   (wireframe, not face-inclusive)
```

## What STL and OBJ Actually Print

**Prompt:**
> Generate just a quick preview PNG first — does the shape look right before I commit to a full export?

**What Comes Back:** `export_dome`'s `preview=True` writes `lair.png` in the same run, a quick wireframe sanity check that costs nothing extra once you're already exporting — worth doing before trusting any of the heavier files, the same iterate-then-commit discipline Chapter 18 formalizes into an actual four-tool workflow.

One more thing worth stating plainly, because it's an easy assumption to get backwards: **STL and OBJ export the dome's surface skin, not its strut skeleton.** `OutputSTL`/`OutputOBJ` both take the dome's *face* list (`F_sphere`), not its chord list — a reader expecting a 3D-printable lattice of individual struts, ready to become a scale model of the actual hub-and-strut structure, will instead get a printable solid model of the panel skin stretched across that structure. That's the geometrically correct output for "3D-print a scale model of this dome's shape" — it's just a different object than "3D-print this dome's actual strut framework," and worth knowing which one you're asking for before a print job finishes looking nothing like what you expected.

## What's Next

Chapter 18 turns this same export logic into an actual agentic workflow: the four MCP tools that let an agent try, preview, and cost-check a design freely before ever calling the one tool that commits it to disk — the same discipline this chapter's own preview-first habit already previewed.
