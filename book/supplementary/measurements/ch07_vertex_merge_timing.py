"""Chapter 7: merging duplicate seam vertices, and why a k-d tree.

The book, for a Class I icosahedral sphere at frequency 16: 3060 raw
(unprojected) vertices (20 faces x 153 symmetry-triangle points); 570
duplicate pairs within the default threshold, found identically by a plain
pairwise loop and by a k-d tree; 2562 vertices after merging (the golden
value 10f^2+2), a reduction of 498. It timed the loop at about 1.75 s and
the k-d tree at about 0.0016 s; timings depend on the machine, so this
script reports them without checking them.
"""
import itertools
import math
import os
import sys
import time

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done, note
from pylair.geodesic_sphere import GeodesicSphere
from pylair.polyhedral import Icosahedron
from pylair.symmetry_triangle import ClassOneMethodOneSymmetryTriangle

F, THRESHOLD = 16, 1e-7
poly = Icosahedron()
sphere = GeodesicSphere(poly, ClassOneMethodOneSymmetryTriangle(F, poly), THRESHOLD, 1.0)
raw = np.array([getattr(v, "xyz", v) for v in sphere.unprojected_vertices], dtype=float)

points = [tuple(p) for p in raw]   # plain tuples: the naive loop, in plain Python
t0 = time.perf_counter()
loop_pairs = sum(1 for p, q in itertools.combinations(points, 2) if math.dist(p, q) < THRESHOLD)
loop_s = time.perf_counter() - t0
t0 = time.perf_counter()
tree_pairs = len(cKDTree(raw).query_pairs(THRESHOLD))
tree_s = time.perf_counter() - t0

print(f"Chapter 7: merging seam vertices, Class I icosahedral sphere, frequency {F}")
check("raw (unprojected) vertices", len(raw), 3060)
check("symmetry-triangle points per face, (f+1)(f+2)/2", (F + 1) * (F + 2) // 2, 153)
check("duplicate pairs, pairwise loop", loop_pairs, 570)
check("duplicate pairs, k-d tree", tree_pairs, 570)
check("vertices after merging (golden value)", len(sphere.sphere_vertices), 10 * F * F + 2)
check("reduction", len(raw) - len(sphere.sphere_vertices), 498)
note("pairwise loop time on this machine", f"{loop_s:.2f} s (book: about 1.75 s)")
note("k-d tree time on this machine", f"{tree_s:.4f} s (book: about 0.0016 s)")
done()
