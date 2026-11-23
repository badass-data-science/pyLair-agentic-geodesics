"""Chapter 5: how many struts meet at each hub of the Class II sphere.

The book: at frequency 6, the Class II icosahedral sphere has 12 ten-strut
hubs (where the icosahedron's own vertices were), 30 four-strut hubs (its
edge midpoints), and 500 six-strut hubs. Counted from the chord list.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair.api import build_dome

dome = build_dome(frequency=6, dome_class=2)
valence = collections.Counter()
for a, b in dome.C:
    valence[a] += 1
    valence[b] += 1
by_valence = collections.Counter(valence.values())

print("Chapter 5: struts per hub, Class II icosahedral sphere, frequency 6")
check("ten-strut hubs", by_valence[10], 12)
check("four-strut hubs", by_valence[4], 30)
check("six-strut hubs", by_valence[6], 500)
check("no other kinds of hub", sorted(by_valence), [4, 6, 10])
done()
