"""Chapter 9: where truncation cutoffs land, swept across shapes.

The book makes five claims, each checked here:
- the frequency-6 Class I icosahedral sphere has 30 vertices at exactly Z=0,
  where a cutoff of 0.5 lands, and 0.499999 clears that ring by 2e-6;
- on the icosahedral Class I sphere, truncation_z=0.5 is refused at every
  even frequency from 2 through 10 and succeeds at every odd one;
- neither documented safe cutoff (0.499999, 0.333333) fails on any base
  polyhedron at frequencies 1 through 20, Classes I and II;
- the truncated frequency-6 sphere at 0.499999 keeps 256 vertices;
- cutting X (0.9) then Z (0.4) differs from Z then X: 60 vertices and 138
  edges against 72 and 169, with the bottom at -0.1157 against -0.2000.
pyLair always cuts X, then Y, then Z; the reverse order is run here by
calling truncate() directly.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from book_check import check, done
from pylair.api import build_dome
from pylair.truncation import truncate

print("Chapter 9: truncation cutoffs")
sphere = build_dome(frequency=6)
zs = [v[2] for v in sphere.V]
check("vertices at exactly Z=0, frequency 6", sum(1 for z in zs if abs(z) < 1e-12), 30)
cut = min(zs) + 0.499999 * (max(zs) - min(zs))
check("0.499999 clears the Z=0 ring by", round(-cut, 9), 2e-6, tol=1e-12)
check("vertices kept at 0.499999", len(build_dome(frequency=6, truncation_z=0.499999).V), 256)


def refused(**kw):
    try:
        build_dome(**kw)
        return False
    except Exception as e:  # the flat-chord refusal
        assert "flat along" in str(e), e
        return True


fails = [f for f in range(2, 11) if refused(frequency=f, truncation_z=0.5)]
check("frequencies 2-10 where 0.5 is refused (icosahedron, Class I)", fails, [2, 4, 6, 8, 10])

bad = []
for poly in ("icosahedron", "octahedron", "tetrahedron"):
    for f in range(1, 21):
        for cls in (1, 2):
            if cls == 2 and f % 2:
                continue   # Class II needs an even frequency (Chapter 5)
            for t in (0.499999, 0.333333):
                if refused(frequency=f, polyhedron=poly, dome_class=cls, truncation_z=t):
                    bad.append((poly, f, cls, t))
check("safe-cutoff failures, all base polyhedra, f 1-20, Classes I and II", bad, [])

V, C, F = sphere.V, sphere.C, sphere.F_sphere
x_then_z = build_dome(frequency=6, truncation_x=0.9, truncation_z=0.4)
V2, C2, F2 = truncate(V, C, 0.4, axis=2, F_sphere=F)
V2, C2, F2 = truncate(V2, C2, 0.9, axis=0, F_sphere=F2)
check("X then Z: vertices", len(x_then_z.V), 60)
check("X then Z: edges", len(x_then_z.C), 138)
check("X then Z: bottom", round(min(v[2] for v in x_then_z.V), 4), -0.1157)
check("Z then X: vertices", len(V2), 72)
check("Z then X: edges", len(C2), 169)
check("Z then X: bottom", round(min(v[2] for v in V2), 4), -0.2)
check("both: top", round(max(v[2] for v in x_then_z.V), 4), 0.6031)
done()
