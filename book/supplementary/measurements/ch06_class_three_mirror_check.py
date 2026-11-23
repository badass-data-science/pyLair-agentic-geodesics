"""Chapter 6: (m,n) = (4,1) and (1,4) are mirror images, point by point.

The book: every point of the (4,1) symmetry triangle has a partner in the
(1,4) triangle at the position you get by negating one local coordinate,
with a residual of floating-point roundoff (about 1e-16), while without the
reflection the points miss by about 0.15.
"""
import os
import sys

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair.class_three import ClassThreeSymmetryTriangle
from pylair.polyhedral import Icosahedron


def local_points(m, n):
    """The symmetry triangle's flat, local (x, y, 0) points."""
    return np.array([v.xyz for v in ClassThreeSymmetryTriangle(m, n, Icosahedron()).vertices])


a, b = local_points(4, 1), local_points(1, 4)
reflected, _ = cKDTree(b * np.array([-1.0, 1.0, 1.0])).query(a)
unreflected, _ = cKDTree(b).query(a)

print("Chapter 6: the (4,1) triangle against the (1,4) triangle")
check("same number of points", len(a), len(b))
check("worst match after negating local x (roundoff, ~1e-16)", float(reflected.max()), 0.0, tol=1e-15)
check("worst miss without the reflection (about 0.15)", round(float(unreflected.max()), 2), 0.15)
done()
