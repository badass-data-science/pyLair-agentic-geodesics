# Chapter 17: Getting It Out the Door — DXF, VRML, STL, OBJ

Export day had three customers. The Foreman wanted drawings his fabrication software could open. Our Heroine wanted something she could spin around on a screen and admire. The Junior Henchman wanted a 3D-printed scale model for the CFV's desk, and had promised her "every strut, in miniature." Three different files, it turned out, and one of the three promises was about to be broken.

Everything since Chapter 3 has built toward this: the Actual Secret Lair, subdivided, shaped, and accounted for, written to files that other software can open. This chapter is about matching the file to the job: four export formats with four different purposes, and the one setting that changes which of them you get.

## Four Formats, Four Jobs

**DXF** (Drawing Exchange Format), written by default, is for CAD (computer-aided design) import: the format a fabricator's design software, a CNC (computer numerical control) machine, or a laser cutter's driver expects. **VRML** (Virtual Reality Modeling Language, `.wrl`), also written by default, is for 3D display: built for showing a shape, not manufacturing it. **STL** (stereolithography) and **OBJ** (the Wavefront object format), switched on with `export_dome`'s `stl` and `obj` parameters, are for 3D printing: a model of the dome's surface, not its strut skeleton, a distinction this chapter returns to. None is a better version of another; each answers a question the others don't.

**[IMAGE: ../sample_image.png | A geodesic dome wireframe exported by pyLair, displayed in a CAD program.]**
**[CAPTION: A pyLair DXF export, loaded into a CAD program: the default export path's own output.]**

**[IMAGE: ../blog-posts/CAD_dome.jpg | A geodesic dome model displayed in CAD software, from a different viewpoint.]**
**[CAPTION: A second CAD import of a pyLair dome, from the project's earlier documentation.]**

## What `face_output=True` Changes

Here is a detail to know in advance rather than discover through a missing file. `export_dome`'s `face_output` parameter switches the VRML file from wireframe to panels, and in doing so **drops the DXF**. With `face_output=False` (the default), you get a wireframe VRML plus a DXF, both drawn from the struts. With `face_output=True`, you get a VRML of the dome's faces instead, and no DXF at all; the CLI's `-F` option does the same, and its help text says so ("Cancels DXF file output").

What `face_output` does *not* control is the other face-based outputs. STL, OBJ, panel templates, hub templates, and the panel cost and weight figures all use the dome's face data, which pyLair keeps through truncation on any axis whether or not `face_output` is set. So if you want the wireframe DXF *and* an STL *and* panel templates, one call does it: leave `face_output` off and turn the others on. A test of that on the Actual Secret Lair wrote 95 files in one go: VRML, DXF, STL, OBJ, and 91 panel templates. Turn `face_output` on only when you want the paneled VRML, knowing the DXF goes with it.

## Two-Axis Truncation, Exported

Face-aware export once worked only on an untruncated sphere; the repository's changelog records when truncation on every axis learned to clip faces too, and Chapters 9 and 10 describe how it does so. Here is that capability on the hardest case this book builds: the Actual Secret Lair truncated on **two** axes at once (`X` at `0.3`, perhaps for a flat wall against the crater's side, and `Z` at `0.499999`), with every face-dependent output requested together.

**Prompt:**
> Export this dome (Class III `(4,1)`, stretched `1.8`× on Z, truncated on X at `0.3` and Z at `0.499999`) with `face_output=True`, `stl=True`, `obj=True`, `preview=True`, `hub_templates=True`, and `face_templates=True` all at once. Which of the files that come back depend on the face data surviving truncation?

**What Comes Back** (the `export_dome` result's file list, abbreviated, with sizes):

```json
{
  "files_written": [
    "lair.wrl", "lair.png", "lair.stl", "lair.obj",
    "lair_hubtype1.dxf", "... 71 hubtype files in all",
    "lair_facetype1.dxf", "... 91 facetype files in all"
  ]
}
```

```
lair.wrl              11,448 bytes   (face VRML)
lair.stl              60,129 bytes   (3D-printable surface mesh)
lair.obj              10,321 bytes   (3D-printable surface mesh)
lair.png             180,646 bytes   (preview image)
```

**What It Means:** All but the preview depend on it. The face VRML, the STL, the OBJ, and the 91 panel templates are built from faces that survived *two* sequential cuts, and the hub templates come from struts that include the diagonal seams of Chapter 10. None errored or produced a broken shape, though both cuts clipped through triangles. 166 files from one call: 91 distinct panel shapes and 71 distinct hub shapes, more than the single-cut dome's 52 and 32, because the second cut adds a whole new boundary of clipped pieces.

For the Foreman's wireframe drawing, the same dome without `face_output`:

**Prompt:**
> Export the same dome again without `face_output`. I want the plain wireframe DXF.

**What Comes Back** (the files written, with sizes):

```
lair-wireframe.wrl   11,587 bytes   (wireframe VRML)
lair-wireframe.dxf   50,545 bytes
```

## Preview First, and What STL and OBJ Print

**Prompt:**
> Generate just a quick preview PNG first. Does the shape look right before I commit to a full export?

**What Comes Back:** `export_dome`'s `preview=True` writes `lair.png` in the same run, a wireframe sanity check that costs nothing extra once you're exporting anyway. Better still, call `preview_dome` before exporting at all, which writes nothing to disk; Chapter 18 makes that habit into a workflow.

One more thing worth stating plainly, because it's easy to get backwards: **STL and OBJ export the dome's surface skin, not its strut skeleton.** `OutputSTL` and `OutputOBJ` both take the dome's *face* list, not its chord list. Expect a printable lattice of individual struts and you'll get a printed shell instead: the panels, with no gaps between them. That's the right output for "print a scale model of this dome's shape"; it's a different object from "print this dome's frame," and you should know which you're asking for before the print finishes.

## What's Next

The CFV's desk model arrived as a smooth, faceted shell, handsome and entirely strut-free. The Junior Henchman explained STL files at some length. The CFV said she liked it better this way, since it couldn't collapse, and asked how much the real one would cost to skin.

Chapter 18 turns the export logic into an agentic workflow: the pyLair MCP tools that let an agent try, preview, and cost a design freely before calling the one tool that writes it to disk.
