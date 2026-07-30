# Chapter 17: Getting It Out the Door — DXF, VRML, STL, OBJ

Everything from Chapter 3 onward has been building toward this moment: the Actual Secret Lair, fully subdivided, shaped, and accounted for, finally written to real files a real downstream tool can open. This chapter is about choosing the right file for the right job — four export formats, four genuinely different purposes, and one prerequisite from Part III that makes two of them possible on a truncated dome at all.

## Four Formats, Four Different Jobs

**DXF**, written by default, is for CAD import — the format a fabricator's own software, a CNC controller, or a laser cutter's driver actually expects. **VRML** (`.wrl`), also written by default, is for 3D display — a format built for showing a shape, not manufacturing it. **STL** and **OBJ** (`-s`/`-O`) are for 3D printing — a scale model of the dome's own surface, not its strut skeleton (more on that distinction below). None of the four is a strictly better version of another; each answers a question the others don't.

*(Figure 17-1: A real pyLair DXF export, loaded back into a CAD viewer — the actual output of the default export path, not a mockup.)*

![A pyLair-exported dome loaded into CAD software](../sample_image.png)

*(Figure 17-2: A second real CAD import, from pyLair's own earlier documentation.)*

![Another real CAD-imported dome](../blog-posts/CAD_dome.jpg)

## Why `-F/--face` Skips DXF Entirely

Here's a detail worth knowing precisely rather than discovering by a missing file: pyLair's own export logic treats `-F/--face` as a genuinely different code path, not an additional file alongside the default two. Without `-F`, you get a wireframe VRML plus a DXF — both built from chords alone. With `-F`, you get a **face-inclusive** VRML instead of the wireframe one, and **no DXF file is written at all**. This isn't an oversight; DXF's own wireframe convention here has no natural way to carry face/panel information the way the face VRML path does, so pyLair simply doesn't try to produce one.

This matters practically: if your workflow needs *both* a wireframe DXF for hub/strut reference *and* face data for STL/OBJ/panel templates, that's two separate export runs, not one command with every flag turned on at once — a real distinction worth planning for before assuming `-F -s -O` alongside the default flags gets you a DXF too.

## Multi-Axis Truncation, Face-Exported, Proven Live

Chapter 10 fixed a real historical gap: face-aware export used to only work correctly on an untruncated sphere. Here's that fix, exercised on the hardest real case this book has built — the Actual Secret Lair, truncated on **two** axes at once (`X` at `0.3`, `Z` at the documented safe `0.499999`), with every face-dependent output requested simultaneously:

```
pylair -o lair -f 4 -n 1 -c 3 -p icosahedron -r 1.0 -e "1.0,1.0,1.8" \
       -x 0.3 -t 0.499999 -F -s -O -P -T -H
```

**Prompt:**
> Export this dome as DXF, VRML with face data, STL, and OBJ all at once. Which files actually require the face data to have been preserved correctly through truncation?

**What Comes Back** (a real run, real files, real sizes):

```
lair.wrl              11,448 bytes   (face-inclusive VRML)
lair.stl              60,129 bytes   (3D-printable surface mesh)
lair.obj              10,321 bytes   (3D-printable surface mesh)
lair.png             171,503 bytes   (preview image)
lair_facetype1.dxf ... lair_facetype91.dxf   (91 panel cutting templates)
lair_hubtype1.dxf  ... lair_hubtype54.dxf    (54 hub connector templates)
```

**What It Means:** Every one of these files needed correctly-clipped face data surviving *two* sequential truncation passes (Chapters 9 and 10's own subject) to even exist — `.wrl`, `.stl`, `.obj`, and every `facetype`/`hubtype` template all require face data (`-F`, `-s`, `-O`, `-T`, `-a`, `-w`, per the CLI's own flag table), and none of them errored or produced a visibly broken shape despite two axes of truncation both clipping through real triangles along the way. This is Chapter 10's fix, demonstrated rather than just claimed: 91 distinct panel shapes and 54 distinct hub shapes, from a dome cut on two axes at once, exported without incident.

The plain wireframe DXF, by contrast, needs a *separate* run without `-F`:

```
$ pylair -o lair-wireframe -f 4 -n 1 -c 3 -p icosahedron -r 1.0 -e "1.0,1.0,1.8" -x 0.3 -t 0.499999
```

```
lair-wireframe.dxf   41,457 bytes
lair-wireframe.wrl   10,945 bytes   (wireframe, not face-inclusive)
```

## What STL and OBJ Actually Print

**Prompt:**
> Generate just a quick preview PNG first — does the shape look right before I commit to a full export?

**What Comes Back:** `-P` writes `lair.png` in the same run, a quick wireframe sanity check that costs nothing extra once you're already exporting — worth doing before trusting any of the heavier files, the same iterate-then-commit discipline Chapter 18 formalizes into an actual four-tool workflow.

One more thing worth stating plainly, because it's an easy assumption to get backwards: **STL and OBJ export the dome's surface skin, not its strut skeleton.** `OutputSTL`/`OutputOBJ` both take the dome's *face* list (`F_sphere`), not its chord list — a reader expecting a 3D-printable lattice of individual struts, ready to become a scale model of the actual hub-and-strut structure, will instead get a printable solid model of the panel skin stretched across that structure. That's the geometrically correct output for "3D-print a scale model of this dome's shape" — it's just a different object than "3D-print this dome's actual strut framework," and worth knowing which one you're asking for before a print job finishes looking nothing like what you expected.

## What's Next

Chapter 18 turns this same export logic into an actual agentic workflow: the four MCP tools that let an agent try, preview, and cost-check a design freely before ever calling the one tool that commits it to disk — the same discipline this chapter's own preview-first habit already previewed.
