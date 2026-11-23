# Chapter 8: Squash and Stretch — Ellipsoid Elongation

The particle accelerator's shipping crate was 3.4 meters tall. The Chief Financial Villain had measured it twice, because the moving company charged by the cubic meter, and she brought the number to the design meeting with the air of someone delivering bad news. A sphere wide enough to fit on the crater floor wasn't tall enough to hold the crate standing up. "Then the sphere," said our Heroine, "will stop being a sphere."

Part II built a sphere. Part III turns it into a building. This chapter is the first of the shaping tools (elongation here, truncation in Chapter 9, the quadrilateral panels their combination produces in Chapter 10), and it brings back **the Under-the-Ocean Prototype** from Chapter 3, whose design philosophy is the opposite of the Actual Secret Lair's.

## One Setting, Three Independent Axes

`design_dome`, `preview_dome`, `export_dome`, and the other tools all take three elongation factors, `elongation_x`, `elongation_y`, and `elongation_z`, and scale every vertex of the finished sphere by them, one axis at a time. The implementation (`pylair/elongation.py`) is about as simple as geometry gets:

```python
def elongate(vertices, factors):
  scale = np.array(factors, dtype=float)
  return [v * scale for v in vertices]
```

A per-vertex multiply, nothing more. Chord and face connectivity are untouched, since scaling changes where vertices sit, never which are connected. A factor above 1 stretches that axis; below 1 squashes it; `1.0` leaves it alone. Once more than one axis differs, the result is a general **triaxial ellipsoid**: three independent semi-axes, no two of which need match.

**Prompt:**
> Preview the same frequency-6 Class I sphere three ways: unelongated, squashed to `(1.0, 1.0, 0.9)`, and stretched to `(1.0, 1.0, 1.8)`.

**What Comes Back** (three `preview_dome` renders):

**[IMAGE: examples/images/elongation_triptych.png | Three wireframe domes side by side: a sphere; a slightly flattened sphere labeled as the Under-the-Ocean Prototype; and a tall egg shape labeled as the Actual Secret Lair, stretched for headroom.]**
**[CAPTION: A frequency-6 Class I sphere, unelongated (left), with the Under-the-Ocean Prototype's gentle squash, `elongation_z=0.9` (center), and with the Actual Secret Lair's stretch, `elongation_z=1.8` (right). Each panel is scaled to fit, so compare shapes, not sizes. The center shape's subtlety is not a rendering error; it's what a 10% squash looks like beside an 80% stretch.]**

**[IMAGE: ../blog-posts/ellipsoid.png | A smooth, shaded ellipsoid with three unequal axes.]**
**[CAPTION: A general axis-aligned ellipsoid, the shape elongation approximates, from pyLair's earlier documentation.]**

## Two Opposite Design Philosophies, One Parameter

**The Under-the-Ocean Prototype** stays as close to a sphere as elongation ever gets: `(1.0, 1.0, 0.9)`, a gentle squash on Z alone. That isn't indecision; it's the right instinct for a pressure hull. A sphere meets external pressure equally from every direction, and any elongation trades some of that away. `0.9` is as far from `1.0` as the design will go, because pressure resistance, not headroom, is the goal.

**The Actual Secret Lair** wants the opposite: `(1.0, 1.0, 1.8)`, a dramatic upward stretch, because a laboratory with a particle accelerator in it needs ceiling height and a sphere of a sensible footprint doesn't have much. Nothing about the stretch improves structural performance. It's a livability decision, made knowingly at the cost of the symmetry the Prototype refuses to give up.

The same parameter, pushed in opposite directions for opposite reasons: that's why the two designs are introduced side by side rather than through a single generic dome.

## Why the Angle Math Needs More Than a Position Vector

Here's a fact worth pinning down before it becomes a problem in Chapter 12: **on a sphere, the outward surface normal at any point is that point's position vector, normalized.** It's exact, not an approximation: a sphere is every point equidistant from its center, so "straight out" from any point always points directly away from the center. Chapter 12's hub angles measure how far a strut deflects from the surface at its hub, and they lean on this normal vector to do it.

Elongate the sphere into an ellipsoid and that convenient fact stops being true. An ellipsoid's outward normal is generally *not* parallel to its position vector, except at the six points where it crosses its own axes, where symmetry makes the two coincide. Here is the difference in numbers, using the hand-computable case pyLair's test suite checks: a point on an ellipsoid stretched by `2.0` along `z`, at 45°, position `(0.7071, 0, 1.4142)`.

```
True ellipsoid normal (gradient of x²/a² + z²/c² = 1):  (0.8944, 0, 0.4472)
Naive normal (just the position vector, normalized):    (0.4472, 0, 0.8944)
```

The two vectors aren't just different; their components are **swapped**. The true normal leans toward x, the naive one toward z, in exactly reversed proportion. That's a qualitatively wrong direction, not a rounding difference, and any calculation that treats it as "straight out from the surface," a strut's deflection angle, say, inherits the error.

The correct formula (`_ellipsoid_normal` in `pylair/bill_of_materials.py`) comes from the ellipsoid's implicit equation, `x²/fx² + y²/fy² + z²/fz² = 1` (with the radius factored out, only the three elongation factors matter). The true normal is proportional to the equation's gradient, `(x/fx², y/fy², z/fz²)`, which reduces to the plain position vector when all three factors are `1.0`. The sphere was never a separate formula, only this one's special case.

## Verified Two Ways, Not Just Derived Once

A formula right on paper and a formula right in running code are different claims, and pyLair checks them separately. Besides the hand-computed 45° case above (and a matching case on the X axis, to make sure the formula wasn't correct only for the axis it was first derived on), the general **triaxial** case, with three different factors at once, is checked against a different method entirely: a numerical, finite-difference estimate of the same gradient, computed without `_ellipsoid_normal`'s formula. At a test point with factors `(2.0, 3.0, 0.5)`, the two agree to within 10⁻⁵. Either both are right or both are wrong in the same way, the same style of independent cross-check Chapter 6 used for Class III, applied to a different piece of geometry.

**Prompt:**
> Why would using the position vector as the surface normal give a wrong answer here, specifically?

**What Comes Back:**
> Because a sphere's defining property, every point equidistant from the center, is exactly what makes its position vector and its normal coincide, and elongating more than one axis differently breaks that property. The correct normal is the gradient of the ellipsoid's implicit equation, `(x/fx², y/fy², z/fz²)`, normalized, which reduces to the position vector only when every factor is `1.0`. Anywhere else, the position vector can point in a qualitatively wrong direction: in the 45° case above, its two components are exactly swapped.

## Seeing the Difference on a Real Hub

Take hub 0 of the frequency-6 Class I sphere, which sits off the axis, at `Z ≈ 0.447`, and compare the tangent-plane angles of its five struts before and after a 1.8× stretch on Z:

**Prompt:**
> Elongate this dome upward by 1.8× on Z only. How much does that change hub 0's tangent-plane angles compared to the unelongated version?

**What Comes Back** (from two `get_bill_of_materials` calls, in the order the report lists hub 0's five struts):

```json
{"elongation": "1.0,1.0,1.0", "hub_0_tangent_angles_degrees": [4.6624, 4.6624, 4.6624, 4.6624, 4.6624]}
{"elongation": "1.0,1.0,1.8", "hub_0_tangent_angles_degrees": [4.7289, 3.0904, 4.7289, 3.3204, 3.3204]}
```

**What It Means:** Unelongated, all five struts at this hub report the same angle: on a sphere, the hub sits at a point of five-fold symmetry. Stretched, the symmetry is gone and the five split into three values (`4.73°` twice, `3.32°` twice, `3.09°` once), because the true normal now depends on which direction the stretch pulled relative to each strut, not just on the hub's distance from the center.

Now the Actual Secret Lair itself, Class III `(4,1)`. Its hub 0 sits exactly on the Z axis, at the crown, one of the six points where the normal still matches the position vector. Its five struts report `6.1061°` each unelongated and `10.8994°` each after the 1.8× stretch: still equal to one another, because the stretch pulls symmetrically around the axis, but nearly twice as steep, because stretching makes the crown more pointed. Elongation doesn't rescale every angle by one fixed factor. Off the axis it changes the pattern; on the axis it changes the size. Either way, the connector for that hub is a different part.

## The Other Way to Get This Wrong: A Zero Factor

Every elongation factor must be strictly greater than zero. Reach for `0` hoping to flatten an axis into a disc and you get a refusal, not a zero-thickness dome.

**Prompt:**
> Try elongating this dome with a Z factor of `0.0`. I want to see what happens if I flatten it completely.

**What Comes Back** (a tool error):

```
-e or --elongation arguments must each be greater than zero. Exiting.
```

There's no meaningful ellipsoid with a zero semi-axis: the implicit equation this chapter rests on divides by each factor squared, and pyLair refuses before that division can produce nonsense.

## One More Ordering Fact, for Chapter 9

Elongation always happens **before** truncation in pyLair's pipeline: every axis is stretched or squashed first, and only then is a truncation cutoff (Chapter 9) computed against whatever range the stretching left behind. That matters more than it sounds. A truncation cutoff says "keep this fraction of the *current* range on this axis," and "current" means after elongation, not the unit sphere's range. Chapter 9 picks this up once there's a cutoff to reason about; for now, hold on to the order.

## What's Next

At a radius of 2.5 meters, a 1.8× stretch makes the Actual Secret Lair 9 meters from top to bottom of the full ellipsoid. The Chief Financial Villain checked the crate against it and withdrew her bad news. She noted, however, that the bottom half of the ellipsoid was underground, and asked who was paying for that.

Chapter 9 answers her: it slices the shape into a dome that stands on the crater floor, and introduces pyLair's most dramatic failure mode, a cutoff that lands exactly wrong and is refused rather than silently producing something broken.
