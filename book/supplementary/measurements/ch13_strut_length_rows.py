"""Chapter 13: how bom_rounding_precision forms strut-length rows.

The book, for the Actual Secret Lair (Class III (4,1), stretched 1.8x on Z,
truncated at 0.499999; 415 struts): 79 distinct rows at the default
precision 9, 61 at 3, 20 at 2, and 2 at 1. At the default, the closest
pair of distinct lengths is about 4.7e-6 apart, roughly 9,400 times the
default's cluster tolerance of 5e-10. At precision 2, the rows 0.047485003
and 0.051270148 (5 struts each, about 0.0038 apart) merge into one row,
0.05 with 10 struts.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair import mcp_server

LAIR = dict(frequency=4, n_frequency=1, dome_class=3, elongation_z=1.8, truncation_z=0.499999)


def rows(precision):
    report = mcp_server.get_bill_of_materials(bom_rounding_precision=precision, **LAIR)
    return report["pyLair report"]["Bill of materials"]["Chord Lengths and Counts"]


print("Chapter 13: strut-length rows for the Actual Secret Lair")
default = rows(9)
check("struts in all", sum(r["count"] for r in default), 415)
for precision, book in ((9, 79), (3, 61), (2, 20), (1, 2)):
    check(f"rows at bom_rounding_precision={precision}", len(rows(precision)), book)

lengths = sorted(float(r["length"]) for r in default)
gap = min(b - a for a, b in zip(lengths, lengths[1:]))
tolerance = max(max(lengths) * 1e-9, 0.5 * 10 ** -9)   # cluster_tolerance, scaled by the longest strut
check("closest distinct lengths, apart by (rounded)", float(f"{gap:.1e}"), 4.7e-6)
check("default cluster tolerance", tolerance, 5e-10, tol=1e-12)
check("ratio, to the nearest hundred", round(gap / tolerance, -2), 9400)

pair = {round(float(r["length"]), 9): r["count"] for r in default}
check("default row 0.047485003 (struts)", pair.get(0.047485003), 5)
check("default row 0.051270148 (struts)", pair.get(0.051270148), 5)
merged = [r for r in rows(2) if abs(float(r["length"]) - 0.05) < 1e-12]
check("precision-2 row 0.05 (struts)", merged[0]["count"] if merged else None, 10)
done()
