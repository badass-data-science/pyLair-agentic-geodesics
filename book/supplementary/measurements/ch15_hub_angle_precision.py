"""Chapter 15: the plateau in hub-shape grouping.

group_hub_types fingerprints each hub by its angles, rounded to
angle_precision decimal places (an internal constant, 3, not a tool
parameter). The book, for the Actual Secret Lair: precisions 1 through 4
all give the same 32 hub shapes, while 5 and 6 report 35 and 40, spurious
groups made of floating-point noise. Also: 156 hubs in all, 50 of them on
the base ring, 25 with three struts and 25 with four.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair.api import build_dome
from pylair.bill_of_materials import compute_hub_data, group_hub_types

dome = build_dome(frequency=4, n_frequency=1, dome_class=3, elongation_factors=(1.0, 1.0, 1.8),
                  truncation_z=0.499999)
hubs = compute_hub_data(dome.V, dome.C, dome.elongation_factors)
if isinstance(hubs, tuple):
    hubs = hubs[0]

print("Chapter 15: hub shapes against angle_precision, Actual Secret Lair")
check("hubs", len(hubs), 156)
for precision, book in ((1, 32), (2, 32), (3, 32), (4, 32), (5, 35), (6, 40)):
    check(f"hub shapes at angle_precision={precision}", len(group_hub_types(hubs, precision)), book)

zmin = min(v[2] for v in dome.V)
ring = [i for i, v in enumerate(dome.V) if v[2] - zmin < 1e-4]
valence = collections.Counter()
for a, b in dome.C:
    valence[a] += 1
    valence[b] += 1
ring_valence = collections.Counter(valence[i] for i in ring)
check("hubs on the base ring", len(ring), 50)
check("base-ring hubs with 3 struts", ring_valence[3], 25)
check("base-ring hubs with 4 struts", ring_valence[4], 25)
done()
