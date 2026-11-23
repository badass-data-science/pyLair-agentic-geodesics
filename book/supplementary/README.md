# Supplementary Material for *Agentic Geodesic Lair Design for Supervillains*

Everything in the book runs on [pyLair](https://github.com/badass-data-science/pyLair-agentic-geodesics) and [pyFit](https://github.com/badass-data-science/pyFit-agentic-polygon-nesting). Every Prompt works through their tools alone. This folder holds the rest: the exact inputs behind the book's nesting jobs, the scripts behind numbers the book reports without showing the code, and the generator behind its JSON snapshots. Each script prints its results beside the book's own numbers and says whether they agree.

## Setup

Install pyLair and pyFit as Chapter 2 describes, with the `mcp` extra, into the same environment:

```bash
pip install -e ".[mcp]"   # in each repository
```

`scipy` and `numpy` come with pyLair. Nothing else is needed.

## Contents

### `jobs/`: every nesting job in the book

`make_jobs.py OUT_DIR` writes each job as a pyFit job spec, plus the DXF panel templates the dome jobs point at (pyLair writes them with `face_templates=True`). Hand any job to pyFit through `design_nest`, or on the command line with `pyfit -j OUT_DIR/<job>.json -o <prefix>`. The three jobs made of plain polygons are also here, ready to use:

| Job | Chapter | What it nests |
|---|---|---|
| `ch02_six_squares` | 2 | six unit squares on a 3×2 sheet |
| `ch19_patches_and_stencils` | 19 | four regular pentagons and six equilateral triangles on 12×8 |
| `ch19_five_squares` | 19 | five unit squares on 3×2, the bottom-left-fill order |
| `ch20_lair_panels` | 20 | all 260 of the Actual Secret Lair's panels (52 templates, 2.5 m radius) on 2.44×1.22 m sheets |
| `ch20_ocean_mirror_allowed`, `_forbidden` | 20 | the Under-the-Ocean Prototype's first six chiral panel groups, 120 panels, on 0.61×0.61 sheets |
| `ch21_four_shapes` | 21, 23 | the Lair's first four panel templates (radius 1), five of each, on 0.6×0.5 sheets |
| `ch21_eight_shapes` | 21 | the first eight, five of each: the progress-notification demonstration |

### `measurements/`: the numbers behind the prose

| Script | Chapter | Reproduces |
|---|---|---|
| `ch05_class_two_hub_valence.py` | 5 | 12 ten-strut, 30 four-strut, and 500 six-strut hubs on the Class II sphere |
| `ch06_class_three_mirror_check.py` | 6 | `(4,1)` and `(1,4)` match point by point after one reflection |
| `ch07_vertex_merge_timing.py` | 7 | 3060 raw vertices, 570 duplicate pairs, 2562 after merging; loop vs. k-d tree timing |
| `ch09_truncation_sweeps.py` | 9 | the Z=0 ring, the even-frequency refusals, the safe-cutoff sweep, X-then-Z vs. Z-then-X |
| `ch13_strut_length_rows.py` | 13 | 79/61/20/2 strut rows; the closest-pair spacing against the cluster tolerance |
| `ch15_hub_angle_precision.py` | 15 | the 32-shape plateau across angle precisions; the base ring's hubs |
| `ch16_sliver_artifacts.py` | 16 | the flagged slivers, measured from the dome's face data |
| `ch21_progress_notifications.py` | 21 | progress notifications from a real `pyfit-mcp` server, timestamped as they arrive |
| `nesting_jobs.py` | 2, 19, 20, 21, 23 | every nesting result, from the jobs above (`--long` adds Chapter 20's four big jobs, about 45 minutes) |

Run one script, or all of them:

```bash
python3 measurements/ch09_truncation_sweeps.py
python3 run_all.py            # a few minutes
python3 run_all.py --long     # also Chapter 20's big jobs
```

Results that depend on the machine (timings, and the exact number of progress notifications) are reported, not checked.

### `snapshots/snapshot.py`: the book's JSON snapshots

The generator behind every **What Comes Back** snapshot, laid out to the book's 52-character width:

```bash
python3 snapshots/snapshot.py design_dome frequency=4
python3 snapshots/snapshot.py get_bill_of_materials frequency=6 truncation_z=0.499999
```

Some snapshots in the book show more entries from the list a chapter is discussing; each What Comes Back label says what it shows.

## Not yet here

The scripts that drew the book's figures (the plots, diagrams, and nesting layouts in `book/examples/images/`) aren't included yet. Figures that are a tool's own output can be reproduced with the tools: `preview_dome`, `render_assembly_schematic`, and `preview_nest` with the parameters each figure's caption gives.
