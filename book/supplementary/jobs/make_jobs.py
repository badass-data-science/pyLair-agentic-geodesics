"""Write every pyFit job the book nests, as job-spec JSON files.

Each job is the exact input behind a nesting result in the book. Jobs made
of plain polygons need nothing else; jobs made of dome panels point at the
DXF cutting templates pyLair writes, so this script asks pyLair to write
those templates too (with export_dome's face_templates=True), into the same
output directory. Run it, then hand any job to pyFit: through the
`design_nest` tool, or on the command line with
`pyfit -j OUT/<job>.json -o <prefix>`.

Usage:
    python3 make_jobs.py [OUT_DIR]      # default: ./out

The jobs, by chapter:
    ch02_six_squares             six unit squares on a 3x2 sheet
    ch19_patches_and_stencils    four pentagons and six triangles on 12x8
    ch19_five_squares            five unit squares on a 3x2 sheet
    ch20_lair_panels             all 260 of the Actual Secret Lair's panels,
                                 52 templates at its 2.5 m build radius, on
                                 2.44 x 1.22 m sheets
    ch20_ocean_mirror_allowed    the Under-the-Ocean Prototype's first six
    ch20_ocean_mirror_forbidden  chiral panel groups (120 panels) on
                                 0.61 x 0.61 sheets, allow_mirror true/false
    ch21_four_shapes             the Lair's first four panel templates (radius
                                 1), five of each, on 0.6 x 0.5 sheets
    ch21_eight_shapes            the first eight, five of each (the progress-
                                 notification demonstration)
The first three are also committed beside this script as ready-made JSON.
"""
import json
import math
import os
import sys

from pylair import mcp_server as pylair

# The Actual Secret Lair (Chapters 6, 8, and 9) and the Under-the-Ocean
# Prototype's hull (Chapters 8, 11, and 20).
LAIR = dict(frequency=4, n_frequency=1, dome_class=3, elongation_z=1.8, truncation_z=0.499999)
OCEAN = dict(frequency=6, elongation_z=0.9)

UNIT_SQUARE = [[0, 0], [1, 0], [1, 1], [0, 1]]


def regular_pentagon(circumradius):
    """A point-up regular pentagon, sitting on y = 0 (Chapter 19's patch blank)."""
    r = circumradius
    pts = [(r + r * math.cos(math.radians(90 + 72 * k)), r + r * math.sin(math.radians(90 + 72 * k)))
           for k in range(5)]
    low = min(y for _, y in pts)
    return [[round(x, 4), round(y - low, 4)] for x, y in pts]


def equilateral_triangle(side):
    """Chapter 19's throwing-star stencil blank."""
    return [[0.0, 0.0], [side, 0.0], [side / 2, round(side * math.sqrt(3) / 2, 4)]]


def templates(out_dir, prefix, **dome):
    """Ask pyLair to write a dome's panel templates; return its
    "Panel Cutting Templates" rows, with paths relative to out_dir."""
    here = os.getcwd()
    os.chdir(out_dir)
    try:
        report = pylair.export_dome(output_path=prefix, face_templates=True, **dome)
    finally:
        os.chdir(here)
    return report["bill_of_materials"]["pyLair report"]["Panel Cutting Templates"]


def job(width, height, parts):
    return {"sheet": {"width": width, "height": height}, "parts": parts}


def from_templates(rows, quantity=None, allow_mirror=None):
    parts = []
    for row in rows:
        name = os.path.splitext(row["template_file"])[0].split("_")[-1]   # facetypeN
        part = {"name": name, "dxf": row["template_file"],
                "quantity": row["panel_count"] if quantity is None else quantity}
        if allow_mirror is not None:
            part["allow_mirror"] = allow_mirror
        parts.append(part)
    return parts


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    jobs = {
        "ch02_six_squares": job(3, 2, [{"name": "square", "polygon": UNIT_SQUARE, "quantity": 6}]),
        "ch19_patches_and_stencils": job(12, 8, [
            {"name": "patch", "polygon": regular_pentagon(1.25), "quantity": 4},
            {"name": "stencil", "polygon": equilateral_triangle(1.7), "quantity": 6}]),
        "ch19_five_squares": job(3, 2, [{"name": "square", "polygon": UNIT_SQUARE, "quantity": 5}]),
    }

    # Chapter 20: the whole Lair at its 2.5 m build radius. allow_mirror is
    # true: the Lair has no chiral panels (Chapter 14) and plain plywood.
    lair_built = templates(out_dir, "lair_r2.5", radius=2.5, **LAIR)
    jobs["ch20_lair_panels"] = job(2.44, 1.22, from_templates(lair_built, allow_mirror=True))

    # Chapter 20: the Prototype's first six chiral groups, 20 panels each.
    chiral = [r for r in templates(out_dir, "ocean", **OCEAN) if r["chiral"]][:6]
    jobs["ch20_ocean_mirror_allowed"] = job(0.61, 0.61, from_templates(chiral, allow_mirror=True))
    jobs["ch20_ocean_mirror_forbidden"] = job(0.61, 0.61, from_templates(chiral, allow_mirror=False))

    # Chapter 21: the Lair modeled at radius 1, its first four and first
    # eight panel templates, five of each.
    lair_unit = templates(out_dir, "lair", **LAIR)
    jobs["ch21_four_shapes"] = job(0.6, 0.5, from_templates(lair_unit[:4], quantity=5))
    jobs["ch21_eight_shapes"] = job(0.6, 0.5, from_templates(lair_unit[:8], quantity=5))

    for name, spec in jobs.items():
        with open(os.path.join(out_dir, name + ".json"), "w") as f:
            json.dump(spec, f, indent=2)
        print(f"wrote {os.path.join(out_dir, name + '.json')}: "
              f"{sum(p['quantity'] for p in spec['parts'])} parts, {len(spec['parts'])} shapes")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
