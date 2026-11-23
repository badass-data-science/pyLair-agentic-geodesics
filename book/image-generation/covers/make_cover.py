"""Cover proposal for *Agentic Geodesic Lair Design for Supervillains*.

Follows the series layout used by *Systems Thinking for Supervillains*
(its cover-image/alt-cover.svg) and *Strategy for Supervillains* (its
image-generation/cover-concepts/make_covers.py): a 1600 x 2560 black page,
the title in white Noto Sans Black, "FOR" between two rules, SUPERVILLAINS in
the accent color, a two-line white subtitle, one large piece of line art, and
LADY NAPALM letter-spaced between two rules at the foot.

The color scheme is this volume's own: molten lava orange for the accent
(the second volume used red with light blue, the third hot pink), with the
art in ember-to-amber depth cueing.

The art is real pyLair output, not a drawing of a dome: the Actual Secret
Lair's own Class III (4,1) icosahedral design, built with
pylair.api.build_dome without the book's 1.8x vertical stretch (whose tall,
egg-shaped profile sat awkwardly on the cover) and cut at 0.35 of its height
(186 hubs, 505 struts), a classic dome profile 1.3 radii tall and 2 wide.
Cut below its widest circle, the sphere bulges out past its base ring, so
from a raised viewpoint the bulge's front struts would be drawn below the
ring's front edge; every strut is clipped at the ring's projected outline,
and the ring is drawn on top, whole (author's request, 2026-11-23). It
is projected and drawn far-to-near, so nearer struts are brighter and
thicker, and floats on the page like the third volume's cat skull.

Run:  python3 make_cover.py
Writes geodesic-lair-cover.svg (text converted to outlines with Inkscape, so
it renders the same without Noto Sans installed) and geodesic-lair-cover.png
(rasterized at 1600 px wide) next to this script.
"""

import math
import os
import subprocess
import tempfile

from PIL import ImageFont

from pylair.api import build_dome

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"
OUT_SVG = os.path.join(HERE, "geodesic-lair-cover.svg")
OUT_PNG = os.path.join(HERE, "geodesic-lair-cover.png")

W, H = 1600, 2560
BLACK = "#000000"
WHITE = "#FFFFFF"
LAVA = "#FF6A13"     # accent: title SUPERVILLAINS, rules, author
AMBER = (255, 196, 77)   # nearest struts
EMBER = (110, 32, 8)     # farthest struts

TITLE = ["AGENTIC GEODESIC", "LAIR DESIGN"]
SUBTITLE = ["Computational Geometry and Agentic AI", "with pyLair and pyFit"]
AUTHOR = "LADY NAPALM"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def width(text, name, size, tracking=0):
    return font(name, size).getlength(text) + tracking * (len(text) - 1)


def fit_size(text, name, target_w, start):
    size = start
    while width(text, name, size) > target_w:
        size -= 2
    return size


def text(x, y, s, size, weight, fill, tracking=0):
    # SVG letter-spacing also follows the last letter; shift by half of it
    # so the visible letters stay centered.
    extra = f' letter-spacing="{tracking}"' if tracking else ""
    return (f'<text x="{x + tracking / 2:.1f}" y="{y}" font-family="Noto Sans" '
            f'font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="middle"{extra}>{s}</text>')


def rule(x0, x1, y, color=LAVA):
    return f'<rect x="{x0:.1f}" y="{y - 4}" width="{x1 - x0:.1f}" height="8" fill="{color}"/>'


def lerp(a, b, t):
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# The dome on the cover (see the module docstring).
DOME = dict(radius=1.0, frequency=4, n_frequency=1, dome_class=3,
            polyhedron="icosahedron", truncation_z=0.35)


def base_ring_radius(V):
    """Radius of the cut's base ring (every hub at the lowest z)."""
    zmin = min(v[2] for v in V)
    return max(math.hypot(x, y) for x, y, z in V if z - zmin < 1e-6)


def dome_svg(cx, base_y, scale, elevation_deg=16, azimuth_deg=12):
    """The cover dome, projected and depth-cued, with its base ring's
    center at (cx, base_y). Everything is clipped to the region above the
    base ring's projected outline, so nothing hangs below the line of
    truncation; the ring's own struts and hubs are then drawn again on top,
    unclipped, so the clip doesn't shave them."""
    r = build_dome(**DOME)
    e, a = math.radians(elevation_deg), math.radians(azimuth_deg)
    pts, depth = [], []
    zmin = min(v[2] for v in r.V)   # the cut base, which sits at base_y
    for x, y, z in r.V:
        x1 = x * math.cos(a) - y * math.sin(a)
        y1 = x * math.sin(a) + y * math.cos(a)
        pts.append((cx + scale * x1, base_y - scale * ((z - zmin) * math.cos(e) + y1 * math.sin(e))))
        depth.append(y1 * math.cos(e) - z * math.sin(e))   # larger = farther
    dmin, dmax = min(depth), max(depth)
    near = [1 - (d - dmin) / (dmax - dmin) for d in depth]  # 1 = nearest

    def strut(i, j):
        t = (near[i] + near[j]) / 2
        t = t * t * (3 - 2 * t)   # smoothstep: keep the back faint, the front bright
        (x0, y0), (x1, y1) = pts[i], pts[j]
        return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                f'stroke="{lerp(EMBER, AMBER, t)}" stroke-width="{2.5 + 5 * t:.2f}" '
                f'stroke-linecap="round"/>')

    def hub(k):
        t = near[k]
        return (f'<circle cx="{pts[k][0]:.1f}" cy="{pts[k][1]:.1f}" r="{3 + 5 * t:.1f}" '
                f'fill="{lerp(EMBER, AMBER, t)}"/>')

    on_ring = [z - zmin < 1e-6 for x, y, z in r.V]
    struts = sorted(r.C, key=lambda c: near[c[0]] + near[c[1]])
    hubs = [k for k in sorted(range(len(pts)), key=lambda k: near[k]) if near[k] > 0.55]

    # Clip region: everything above the base ring's center line, plus the
    # ring's projected ellipse (its lower half is the line of truncation).
    rx = scale * base_ring_radius(r.V)
    ry = rx * math.sin(e)
    clip = (f'<clipPath id="above-base"><rect x="0" y="0" width="{W}" height="{base_y:.1f}"/>'
            f'<ellipse cx="{cx}" cy="{base_y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"/></clipPath>')
    out = [clip, '<g clip-path="url(#above-base)">']
    out += [strut(i, j) for i, j in struts] + [hub(k) for k in hubs]
    out.append("</g>")
    # The base ring itself, whole, on top.
    out += [strut(i, j) for i, j in struts if on_ring[i] and on_ring[j]]
    out += [hub(k) for k in hubs if on_ring[k]]
    return "\n".join(out)


def build_svg():
    parts = []

    # Title, two lines, white; the longer line as wide as SUPERVILLAINS's box.
    sv_size = fit_size("SUPERVILLAINS", "NotoSans-Black.ttf", 1420, 220)
    t_size = fit_size(TITLE[0], "NotoSans-Black.ttf", 1420 * 0.94, 200)
    y = 250
    for line in TITLE:
        parts.append(text(W / 2, y, line, t_size, 900, WHITE))
        y += round(t_size * 1.08)
    title_bottom = y - round(t_size * 1.08)

    # FOR between two rules.
    for_y = title_bottom + 125
    for_w = width("FOR", "NotoSans-ExtraBold.ttf", 78)
    parts.append(text(W / 2, for_y, "FOR", 78, 800, WHITE))
    gap, rule_w = 40, 520
    l, r = W / 2 - for_w / 2, W / 2 + for_w / 2
    parts.append(rule(l - gap - rule_w, l - gap, for_y - 28))
    parts.append(rule(r + gap, r + gap + rule_w, for_y - 28))

    sv_y = for_y + 215
    parts.append(text(W / 2, sv_y, "SUPERVILLAINS", sv_size, 900, LAVA))

    sub_y = sv_y + 115
    for i, line in enumerate(SUBTITLE):
        parts.append(text(W / 2, sub_y + i * 86, line, 62, 400, WHITE))

    # Art: the dome, centered in the box between the subtitle and the author
    # line (from the subtitle's last line + 60 to y = 2290, like the third
    # volume's art box). The base ring is the lowest thing drawn; the apex
    # the highest.
    art_top, art_bottom, scale, e = sub_y + 86 + 60, 2290, 600, math.radians(16)
    V = build_dome(**DOME).V
    zs = [v[2] for v in V]
    above = scale * (max(zs) - min(zs)) * math.cos(e)   # apex above the base ring's center
    below = scale * base_ring_radius(V) * math.sin(e)   # base ring's near edge below it
    base_y = (art_top + art_bottom) / 2 + (above - below) / 2
    parts.append(dome_svg(W / 2, base_y, scale))

    # Author, letter-spaced, between two rules.
    a_size, tracking = 104, 26
    a_w = width(AUTHOR, "NotoSans-Bold.ttf", a_size, tracking)
    parts.append(text(W / 2, 2460, AUTHOR, a_size, 700, LAVA, tracking))
    l, r = W / 2 - a_w / 2, W / 2 + a_w / 2
    gap, rule_w = 50, 160
    parts.append(rule(l - gap - rule_w, l - gap, 2412))
    parts.append(rule(r + gap, r + gap + rule_w, 2412))

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{BLACK}"/>\n'
            + "\n".join(parts) + "\n</svg>\n")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "cover-text.svg")
        with open(raw, "w") as f:
            f.write(build_svg())
        subprocess.run(["inkscape", raw, "--export-text-to-path", "--export-plain-svg",
                        f"--export-filename={OUT_SVG}"], check=True, capture_output=True)
    subprocess.run(["inkscape", OUT_SVG, "--export-type=png", f"--export-filename={OUT_PNG}",
                    "--export-width=1600", "--export-background=#000000"],
                   check=True, capture_output=True)
    print("wrote", OUT_SVG)
    print("wrote", OUT_PNG)
