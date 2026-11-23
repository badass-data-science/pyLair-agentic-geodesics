"""Chapters 2, 19, 20, 21, and 23: run the book's nesting jobs.

Builds every job with ../jobs/make_jobs.py, runs each through pyFit's own
MCP tool functions (the same code an agent reaches), and checks the result
against the numbers the book prints. Chapter 20's four full-size jobs take
about 45 minutes between them, so they run only with --long.

Usage:
    python3 nesting_jobs.py           # quick jobs (about a minute)
    python3 nesting_jobs.py --long    # also Chapter 20's four big jobs
"""
import asyncio
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "jobs"))
import json

import make_jobs
from book_check import check, done, note
from pyfit import mcp_server as pyfit


def run(tool, spec, **kw):
    return asyncio.run(tool(sheet_width=spec["sheet"]["width"], sheet_height=spec["sheet"]["height"],
                            parts=spec["parts"], **kw))


def r4(xs):
    return [round(x, 4) for x in xs]


def main(long):
    out = tempfile.mkdtemp(prefix="book-jobs-")
    make_jobs.main(out)
    os.chdir(out)   # job specs name their DXF templates relative to here
    jobs = {name[:-5]: json.load(open(name)) for name in os.listdir(out) if name.endswith(".json")}

    print("\nChapter 2: six unit squares on a 3x2 sheet")
    r = run(pyfit.design_nest, jobs["ch02_six_squares"])
    check("design_nest", r, {"sheets_used": 1, "utilization_by_sheet": [1.0]})

    print("\nChapter 19: patches and stencils on a 12x8 sheet")
    r = run(pyfit.get_nest_report, jobs["ch19_patches_and_stencils"])
    check("sheets used", r["sheets_used"], 1)
    check("utilization", round(r["utilization_by_sheet"][0], 3), 0.233)
    check("placements", len(r["placements"]), 10)

    print("\nChapter 19: five unit squares, bottom-left fill order")
    r = run(pyfit.get_nest_report, jobs["ch19_five_squares"])
    check("utilization", r4(r["utilization_by_sheet"]), [0.8333])
    check("positions, in placement order", [tuple(round(c, 4) + 0.0 for c in p["position"]) for p in r["placements"]],
          [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0), (2.0, 0.0)])

    print("\nChapter 21: four of the Lair's shapes, five each, on 0.6 x 0.5 sheets")
    four = jobs["ch21_four_shapes"]
    check("design_nest", r4(run(pyfit.design_nest, four)["utilization_by_sheet"]),
          [0.5796, 0.5984, 0.5502, 0.5771, 0.3434])
    report = run(pyfit.get_nest_report, four)
    check("get_nest_report placements", len(report["placements"]), 20)
    exported = run(pyfit.export_nest, four, output_path="lair", preview=True)
    check("export_nest files (a DXF and a PNG per sheet)", len(exported["files_written"]), 10)
    for step, book in ((30.0, 6), (45.0, 5)):
        check(f"sheets at a {step:g} degree rotation step",
              run(pyfit.design_nest, four, rotation_step_degrees=step)["sheets_used"], book)

    print("\nChapter 21: the first eight shapes (the progress demonstration's job)")
    t0 = time.perf_counter()
    r = run(pyfit.design_nest, jobs["ch21_eight_shapes"])
    check("sheets used (its last notification reads 'checking sheet 10')", r["sheets_used"], 10)
    note("time on this machine", f"{time.perf_counter() - t0:.1f} s (book: about 23 s)")

    print("\nChapter 23: theoretical panel area against real sheet area, Chapter 21's batch")
    from pylair import mcp_server as pylair
    rows = pylair.get_bill_of_materials(**make_jobs.LAIR)["pyLair report"]["Panel shapes and counts"]
    areas = [r_["area"] for r_ in rows["Panel Types and Counts"][:4]]
    theoretical = sum(5 * a for a in areas)
    bought = 5 * 0.6 * 0.5
    check("theoretical panel area of the 20 panels", round(theoretical, 2), 0.79)
    check("sheet area bought, 5 sheets of 0.6 x 0.5", round(bought, 2), 1.5)
    check("ratio", round(bought / theoretical, 2), 1.90)

    if not long:
        print("\n(Chapter 20's four big jobs skipped; run with --long for them.)")
        return
    print("\nChapter 20: the whole Lair, 260 panels on 2.44 x 1.22 m sheets")
    for step, sheets, first, last in ((15.0, 30, 0.8953, 0.1076), (45.0, 32, 0.8407, 0.1849)):
        t0 = time.perf_counter()
        r = run(pyfit.design_nest, jobs["ch20_lair_panels"], rotation_step_degrees=step)
        u = r["utilization_by_sheet"]
        check(f"{step:g} degrees: sheets used", r["sheets_used"], sheets)
        check(f"{step:g} degrees: first and last sheets", (round(u[0], 4), round(u[-1], 4)), (first, last))
        note(f"{step:g} degrees: time on this machine", f"{time.perf_counter() - t0:.0f} s")
    print("\nChapter 20: the Prototype's first six chiral groups, mirroring allowed and forbidden")
    for name, book in (("ch20_ocean_mirror_allowed",
                        [0.657, 0.6859, 0.6484, 0.6354, 0.659, 0.6424, 0.6405, 0.1564]),
                       ("ch20_ocean_mirror_forbidden",
                        [0.6959, 0.6602, 0.7231, 0.7053, 0.7049, 0.6667, 0.5689])):
        t0 = time.perf_counter()
        check(name, r4(run(pyfit.design_nest, jobs[name])["utilization_by_sheet"]), book)
        note(f"{name}: time on this machine", f"{time.perf_counter() - t0:.0f} s")


if __name__ == "__main__":
    main("--long" in sys.argv)
    done()
