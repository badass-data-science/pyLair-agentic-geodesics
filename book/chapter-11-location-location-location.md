# Chapter 11: Location, Location, Location — Designing for Hostile (and Ridiculous) Environments

Word travels fast in the villain community, mostly by encrypted newsletter. Within a week of the Actual Secret Lair's first truncated preview, the Secret Lab™ had four commissions from other villains and a fifth from our Heroine's own contingency file. The Chief Financial Villain, who had been wondering how to pay for the plywood, priced the consulting work before anyone could object. "Every client," she observed, "thinks their site is the special case."

Nothing in this chapter is a new pyLair feature. Chapters 3 through 10 supplied every tool it uses: polyhedron choice, subdivision class, elongation, truncation. What this chapter teaches is how a commission arrives: never as "build a Class III dome," always as "build a dome that survives *down there*, or *up there*, or *in there*." Six stops, one design habit applied each time (start from what the site demands and what the client wants, then pick parameters), to show that the habit does the work, not six unrelated tricks. Every dome here is a Class I icosahedron at frequency 6 and radius 1 unless the stop says otherwise.

**[IMAGE: examples/images/environments_gallery.png | Six dome wireframes drawn at one shared scale: a slightly squashed sphere, a wide flattened ellipsoid, two low flat caps, a tall narrow spire, and one tiny dome.]**
**[CAPTION: All six of this chapter's stops, built with `design_dome` and drawn at one shared scale, so their relative sizes and proportions can be compared honestly.]**

## Stop One: The Under-the-Ocean Prototype, Completed

Chapters 3 and 8 made two of this design's three decisions: an icosahedron, the most uniform starting shape for a pressure hull (Chapter 3), and a gentle `(1.0, 1.0, 0.9)` squash, as close to a sphere as the design will go (Chapter 8). The third belongs here: **no truncation at all**, because the goal is a closed, pressure-resistant shell with no flat cut for the water to argue with.

```json
{"footprint_diameter": 2.0000, "height": 1.8000, "total_strut_length": 208.7384}
```

An airlock would change this: a flat mounting face is worth a small cutoff chosen to stay clear of a vertex ring (Chapter 9's lesson, whatever the environment). Without that need, the closed shell is the right default here, and it's worth resisting the urge to truncate just because every other stop in this chapter does.

**Prompt:**
> Compare a frequency-4 and a frequency-8 Class I icosahedral dome for the Under-the-Ocean Prototype. Which one produces fewer distinct panel types, and why might that matter for a pressure-rated build?

**What Comes Back** (from two `get_bill_of_materials` calls, both elongated `(1.0, 1.0, 0.9)`, summarized from the panel section):

```json
{"frequency": 4, "total_panels": 320,  "distinct_panel_shape_groups": 20}
{"frequency": 8, "total_panels": 1280, "distinct_panel_shape_groups": 71}
```

**What It Means:** Frequency 8 doesn't just have four times as many panels; it has more than three times as many *distinct shapes*, each needing its own cutting template (Chapter 15) and its own line in a fabricator's parts list. For a pressure hull, where every seam is a potential weak point and every distinct shape is another chance to install the wrong piece in the wrong slot, 20 shape groups is a meaningfully simpler build than 71. That's a concrete reason to prefer the coarser frequency here, not a vague instinct that smaller numbers are simpler.

## Stop Two: The Orbital Panopticon

A panopticon earns the name only if it can see everything, so this station has no floor: in orbit, "which way is down" is a design choice, not a constraint. It skips truncation and asks a cost question Chapter 8 didn't need to: at a fixed footprint, which elongation is *cheapest to launch*? Total strut length is a fair proxy, since every kilogram sent to orbit costs money whatever it's made of, and a villain funding a circumpolar surveillance station personally cares about launch mass in a way a contractor spending someone else's budget may not.

**Prompt:**
> For the Orbital Panopticon, hold the footprint diameter fixed and try three different elongation ratios. Which one minimizes total strut length, and therefore launch mass?

**What Comes Back** (three `design_dome` builds, all with `elongation_x=elongation_y=1.3` to fix the footprint, varying only `elongation_z`):

```json
{"fz": 0.5, "footprint_diameter": 2.6000, "total_strut_length": 233.2433}
{"fz": 0.7, "footprint_diameter": 2.6000, "total_strut_length": 242.5685}
{"fz": 1.0, "footprint_diameter": 2.6000, "total_strut_length": 260.0654}
```

**What It Means:** All three share a footprint by construction; only `fz` differs. The flattest (`fz=0.5`) is also the cheapest, by about 10% of strut material against the roundest. That's a general pattern, not a quirk of this example: at a fixed horizontal footprint, flattening the vertical axis shrinks the ellipsoid's surface, and the strut total with it. For a launch-mass-limited station it's a real design lever.

## Stops Three and Four: The Magma Redoubt and the Permafrost Cache

These two share one design logic for opposite reasons: bury most of the structure and expose only a small cap. An active volcano and a glacier have little in common as building sites, but they agree on what matters to anyone avoiding satellite photography: the rock or ice does the hiding for free, so only the small exposed fraction needs a stealth budget. pyLair's truncation describes only what to keep *above* a cutoff, so an aggressive `0.85` for both keeps the small top cap; the buried remainder isn't part of either model, a scope boundary this chapter returns to below.

```json
{"stop": "Magma Redoubt",    "elongation": "1.0,1.0,1.0", "truncation_z": 0.85, "height": 0.3000, "footprint_diameter": 1.4135, "total_strut_length": 39.2628}
{"stop": "Permafrost Cache", "elongation": "1.2,1.2,1.0", "truncation_z": 0.85, "height": 0.3000, "footprint_diameter": 1.6962, "total_strut_length": 46.2090}
```

The Permafrost Cache's wider `1.2, 1.2` footprint reflects a different structural argument. Snow accumulates on top, and a wider, shallower cap spreads that load over more area for the same height. It's the "geodesic domes spread stress evenly" pitch from pyLair's companion blog post, applied to one specific load direction instead of stated as a slogan.

## Stop Five: The Ostentatious Mesa Spire

Every other stop reaches for a low, flattened shape. This one doesn't, because the client wants the opposite: to be *seen*. A mesa-top spire visible from the highway, so that every driver understands instantly that someone with resources and a point to prove lives up there. The brief was never concealment; it was a skyline. Aggressive vertical elongation, `(0.6, 0.6, 3.0)`, and a moderate truncation, `0.4`, for a floor:

```json
{"footprint_diameter": 1.2000, "height": 3.6000, "total_strut_length": 223.6843}
```

**[IMAGE: examples/images/environments_comparison_chart.png | A paired bar chart comparing footprint diameter and total strut length for each of the six stops.]**
**[CAPTION: Footprint diameter against total strut length for all six stops, from `design_dome` output. The Mesa Spire pairs the smallest footprint of the five full-size stops with the second-highest strut total. A compact footprint and a cheap build are different claims.]**

That comparison is this stop's lesson. Among the five full-size stops, the Mesa Spire has the *smallest* footprint and the second-highest strut total, more material than the much wider Under-the-Ocean Prototype. "What does this site demand?" and "what does this client want?" are different inputs to the same tool, sometimes opposed ones, and the second can carry measurable material costs the first would never have chosen. The Chief Financial Villain added a vanity surcharge to the invoice.

## A Callback to the Studio Apartment

One last stop, partly for the joke and partly to make a point: the same agent and the same parameters work as well at a scale that matters to no one but our Heroine's former ambitions.

**Prompt:**
> Design a Class I icosahedral dome, frequency 6, radius 0.15, truncated at `truncation_z=0.499999`. Yes, radius 0.15. It's for a closet.

**What Comes Back** (a `design_dome` result, trimmed):

```json
{"footprint_diameter": 0.3000, "height": 0.1500, "total_strut_length": 18.5354}
```

Every parameter used at volcano and orbital scale works as well for a closet. Nothing in pyLair's geometry cares whether `radius` describes a renovation or a circumpolar fortress.

## What pyLair Checked, and What It Didn't

Every stop built cleanly, reported sensible numbers, and rendered a plausible shape. Be as clear about what that proves as the rest of this book has been:

- **Truncation is always an axis-aligned plane, never a terrain-following surface.** A real caldera rim is an irregular, surveyed rock edge, not a flat plane at a fixed Z. `truncate()` makes a flat cut at a chosen fraction of one axis; reconciling that with a site survey is outside pyLair's scope.
- **Elongation is one `(fx, fy, fz)` triple applied to the whole dome; pyLair has no notion of local deformation.** A design that wants, say, a bulging equatorial ring for a spinning station can only get the general-ellipsoid approximation as a starting silhouette. Anything shaped more locally than one ellipsoid is beyond what `elongate()` computes; it isn't a missing flag.
- **`panel_areal_density` and `cost_per_unit_area` are single numbers you supply; pyLair has no materials database.** Which density and price apply to an underwater-rated composite, an orbital alloy, or a heat-rated ceramic is research the tool has no opinion on. It multiplies whatever it's given, researched or guessed.
- **The caveat that matters most:** every check this book teaches (Euler's formula, golden values, the antitile, trimesh, and ezdxf cross-checks, the flat-chord refusal, the sliver flags of Chapter 16) confirms that pyLair's geometry is *internally* correct. None of them, alone or together, confirms that a design survives water pressure, orbital debris, magma heat, or snow load. A plausible `preview_dome` image is a sanity check on the shape, not engineering sign-off on the environment.

**Prompt:**
> Design a dome meant to sit mostly below a caldera rim, using a single Z truncation. What has pyLair checked for you, and what hasn't it checked at all, before I try to fit this into an actual volcano?

**What Comes Back:**
> pyLair has checked that the shape is internally consistent: the counts satisfy the golden-value formulas and Euler's formula, the cutoff didn't land on a flat chord, and every strut length and hub angle is geometrically consistent with the requested radius, elongation, and cutoff. It has checked none of the following: whether the real caldera rim is flat (it almost certainly isn't), whether the panel material behind your `cost_per_unit_area` and `panel_areal_density` is rated for volcanic heat, or whether the site's geology can carry a structure of this footprint. Those are real questions; they just aren't this tool's questions.

## What's Next

The Chief Financial Villain sent out five invoices and one disclaimer, the last bullet list above in a large font. Our Heroine signed the disclaimer herself. A villain who sells someone a dome that collapses gets a reputation; she had a framed photograph of what that looks like.

Part IV returns to the bill of materials in earnest, starting with the two kinds of hub angle every one of these domes already reports. Chapter 12 explains what they mean, why they need the true ellipsoid normal from Chapter 8, and what the Foreman does with them.
