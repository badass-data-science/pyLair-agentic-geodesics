"""Chapter 16: truncation slivers, counted and measured.

The book, for the frequency-6 Class I icosahedral sphere (which has a ring
of vertices exactly at Z=0):
- at truncation_z=0.4999999, the report flags 6 artifact chord rows and 3
  artifact panel shapes; one chord row is 2.36e-07 long, 10 struts;
- the 3 panel shapes, measured from the dome's face data (the report prints
  panel edges to three decimals, so they show there as 0.0), are
  [2.31e-07, 0.206, 0.206] x40, [2.31e-07, 2.34e-07, 2.35e-07] x30 and
  [2.35e-07, 0.215, 0.215] x20;
- at the documented safe cutoff 0.499999 the lists are 8 and 3, with
  slivers ten times larger (about 2.4e-07 grows to about 2.4e-06);
- at 0.45, well clear of the ring, both lists are empty;
- the Actual Secret Lair at 0.499999 has both lists empty.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair import mcp_server
from pylair.api import build_dome


def flagged(**kw):
    r = mcp_server.get_bill_of_materials(**kw)["pyLair report"]
    return (r["Bill of materials"]["Possible truncation-artifact chords"],
            r["Panel shapes and counts"]["Possible truncation-artifact panels"])


def measured_edges(dome, face_index):
    a, b, c = (dome.V[i] for i in dome.F_sphere[face_index])
    return sorted(math.dist(p, q) for p, q in ((a, b), (b, c), (c, a)))


def sig(x):
    return float(f"{x:.3g}")


print("Chapter 16: truncation-artifact slivers, Class I icosahedral sphere, frequency 6")
chords, panels = flagged(frequency=6, truncation_z=0.4999999)
check("artifact chord rows at 0.4999999", len(chords), 6)
check("artifact panel shapes at 0.4999999", len(panels), 3)
row = [c for c in chords if c["count"] == 10 and abs(float(c["length"]) - 2.36e-07) < 5e-10]
check("chord row 2.36e-07, 10 struts", len(row), 1)

dome = build_dome(frequency=6, truncation_z=0.4999999)
shapes = sorted(([sig(e) for e in measured_edges(dome, p["face_indices"][0])], p["count"]) for p in panels)
book_shapes = sorted([([2.31e-07, 0.206, 0.206], 40), ([2.31e-07, 2.34e-07, 2.35e-07], 30),
                      ([2.35e-07, 0.215, 0.215], 20)])
check("sliver panel shapes, measured from face data", shapes, book_shapes)

chords2, panels2 = flagged(frequency=6, truncation_z=0.499999)
check("artifact chord rows at 0.499999", len(chords2), 8)
check("artifact panel shapes at 0.499999", len(panels2), 3)
# the same 10-strut row (same struts), followed from one cutoff to the other
same_row = [c for c in chords2 if c["chord_indices"] == row[0]["chord_indices"]]
check("that row at 0.4999999 (about)", float(f"{float(row[0]['length']):.1e}"), 2.4e-07)
check("the same row at 0.499999 (about)", float(f"{float(same_row[0]['length']):.1e}") if same_row else None, 2.4e-06)
check("artifact lists at 0.45", tuple(map(len, flagged(frequency=6, truncation_z=0.45))), (0, 0))
check("artifact lists, Actual Secret Lair",
      tuple(map(len, flagged(frequency=4, n_frequency=1, dome_class=3, elongation_z=1.8,
                             truncation_z=0.499999))), (0, 0))
done()
