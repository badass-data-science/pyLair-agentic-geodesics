# Meet pyDome, or: How Our Heroine Decided a Regular House Was Beneath Her

Somewhere between "I would like a nice backyard structure" and "I have written five hundred lines of Python to compute the precise angle at which forty different steel struts must meet at a single point in three-dimensional space," a decision was made. That decision was made by our heroine, and the resulting software is called **pyDome**.

Most people, faced with the desire for a dome-shaped structure, would consult a tape measure, possibly a friend, and definitely a beverage. Our heroine instead consulted the icosahedron. This is the correct order of operations if you are the sort of person who considers "buy a kit" to be a deeply unsatisfying answer to "how do I build a dome," and who would rather derive the entire thing from first principles, in code, with a bill of materials attached. pyDome is what happens when that instinct is left unsupervised.

## So What Does It Actually Do?

In the most boring possible terms: pyDome computes the vertices and chords of a Class One geodesic dome and writes them out as a DXF file (for your CAD software) and a VRML file (so you can spin it around on screen and feel powerful). It will also, unprompted, hand you a full bill of materials — every strut length, how many of each you need, and the exact angles at which they meet — because our heroine has apparently decided that "I'll figure out the angles later, on site, with a protractor and my dignity" is not an acceptable plan.

You tell it how big you want the dome, how finely subdivided you want its surface (this is called the "frequency," and higher numbers mean smaller, more numerous, more sphere-like triangles), and whether you'd like the whole sphere or just a dome-shaped slice of it. It hands back everything a person would need to actually go and build the thing, which is either extremely convenient or extremely ambitious, depending on how much steel you own.

## How It Actually Works, for People Who Enjoy Geometry as a Spectator Sport

Here is the method, in the order pyDome performs it, narrated at a pace suitable for people who have not thought about polyhedra since a geometry class they resented at the time and now, inexplicably, miss:

**Step one: start with an icosahedron.** Twenty triangular faces, twelve vertices, extremely pleased with itself. This is the scaffolding for everything that follows, on the theory that if you're going to approximate a sphere, you should start from something that already agrees to be reasonably sphere-shaped and symmetric about it.

![An icosahedron](../images/edited_icosahedron1.png)

**Step two: subdivide.** Each of those twenty faces gets chopped up into a neat grid of smaller, equal triangles — pyDome calls this smaller unit the "symmetry triangle," and computes it once, then stamps a copy of it onto every face of the icosahedron like a very geometrically disciplined rubber stamp. This is also the step where the "frequency" setting earns its keep: ask for a higher frequency, and you get a finer grid, more struts, and a dome that looks less like a soccer ball and more like an actual sphere.

![Each face subdivided into a triangular grid](../images/edited_4_unprojected1.png)

**Step three: project onto the sphere.** All those newly created points, still living smugly flat on the faces of the icosahedron, get pushed outward onto the surface of an actual sphere, while pyDome does its best to preserve the chord pattern that connects them. This is the step that turns "a polyhedron with a lot of triangles on it" into "something that reads, to the human eye, as a sphere made of struts." It is also the step where any two points that were sitting on the seam between adjacent icosahedron faces — and were therefore computed twice, once by each face — get quietly noticed and merged back into a single point, so the dome doesn't end up with a bunch of secretly-doubled vertices lurking at every seam.

![The subdivided grid projected onto a sphere](../images/edited_4_projected1.png)

**Step four: truncate, if you're feeling less than fully spherical.** Not everyone wants to live inside a complete sphere — doors are hard to install on the underside of one. So pyDome will happily slice the sphere off at a chosen height, typically somewhere around the equator, and hand you a proper dome instead of a full globe. This is the step that turns a geodesic novelty item into a geodesic dome you could plausibly put a door in.

![The sphere truncated at the equator into a dome](../images/edited_truncated.png)

At this point pyDome writes the whole thing out as a DXF file, which loads into a CAD program looking like an actual, legitimate architectural drawing, rather than the output of someone who spent their weekend deriving polyhedra:

![The dome loaded into a CAD program](../images/CAD_dome.jpg)

**Step five: report the angles, because someone has to.** This is our heroine's favorite part, and arguably the actual point of the whole exercise. For every hub in the structure — every point where multiple struts converge — pyDome computes two kinds of angle.

First, the angle between each strut and the plane tangent to the sphere at that hub, which tells you how far a hub connector has to tilt inward to receive that particular strut:

![The tangent-plane deflection angle at a hub](../images/tangent_angle_image_CROPPED.png)

Second, the "spoke" angles: project all the struts at a hub onto that same tangent plane, pick one as a reference, and measure how far around the hub each of the others sits relative to it:

![The spoke angles around a hub](../images/spoke_angle_image_CROPPED.png)

Put the two together and you know, for every single joint in the entire dome, exactly how to bend metal or cut wood to make it meet correctly. This is the difference between a construction plan and a very expensive pile of triangles.

## Why Any of This Matters

A geodesic dome distributes structural stress across its entire surface rather than concentrating it in walls and a roof, which is the mathematical reason domes are strong for their weight and the practical reason people keep insisting on building them despite the aggravating number of distinct angles involved. pyDome exists so that the aggravating part — the angles, the strut lengths, the "wait, how many of these do I actually need to cut" part — gets handled by a computer instead of by increasingly creative profanity on a job site.

## She Did Not Stop There

A person could reasonably assume that "computes a geodesic dome and reports the angles" would be enough software for one lifetime. Our heroine did not share this assumption. Six new abilities have since arrived, each delivered with the calm insistence of someone who has found a rough edge and will not be talked out of smoothing it.

**A preview you don't need a CAD license to look at.** Add `-P` and pyDome renders a quick 3D wireframe of the dome straight to a PNG, so you can confirm the thing actually looks like a dome — and not, say, a lopsided egg — before you go hunting for software that still knows how to open a VRML file. Considerable stubbornness went into making sure the preview's three axes are scaled honestly relative to one another, on the theory that a tool which quietly lies to you about the shape of your own dome is worse than no tool at all.

**Export formats for people who own more than a protractor.** `-s` and `-O` produce STL and OBJ files, meaning the dome can now go straight into a 3D printer and become a scale model you can hold, judge, and photograph next to a coffee cup for a sense of proportion.

**A second way to cut up a sphere.** The original method (Class I, "Alternate") subdivides each icosahedron face with a grid running parallel to its own edges. `-c 2` switches to Class II, the "Triacon" method, which instead splits each face into six smaller triangles around its center first, producing a visibly different strut pattern — and, not incidentally, a frequency that must be even, a constraint the software enforces rather than politely suggests.

**A running total, because "add it up yourself" is not a feature.** pyDome now reports the total length of every strut in the dome, and if you supply a price per unit length with `-m`, a total estimated cost too — sparing you the specific despair of doing that arithmetic by hand at 11pm the night before a materials run.

**Cutting templates for the part everyone dreads.** The hard part of building one of these domes was never really the struts — it's the connector plates where five or six of them converge at a single point, each arriving at its own particular angle. `-H` now generates a 2D DXF cutting template for every genuinely distinct hub shape in the dome, correctly recognizing that two hubs which are secretly the same shape, just rotated relative to each other, only need one template between them, rather than needlessly multiplying your laser-cutting bill.

**Domes that don't insist on being perfectly round.** `-e` stretches the whole structure along its vertical axis before it gets cut into a dome, for anyone whose ceiling-height ambitions exceed their footprint, or the reverse. Doing this properly required teaching the software that an ellipsoid's surface doesn't point straight outward from its center the way a sphere's does — a distinction most people are never required to think about, and one our heroine now thinks about rather more than she originally planned to.

## Then She Picked a Fight With Chirality, and Chirality Fought Back

Two subdivision methods, one might think, is a perfectly respectable number of subdivision methods. Our heroine, predictably, thought otherwise, and set out to add a third: Class III, sometimes called "Skew," in which the grid on each face is laid down at an angle instead of running parallel or radiating from the center like its two more cooperative siblings. This is the geodesic-dome equivalent of asking for your hardwood floor to be installed on a diagonal — visually striking, mathematically fussier, and apparently nobody's idea of a beginner project.

She built it. She checked it against Euler's formula, the same identity — vertices minus edges plus faces equals two — that had already caught a real bug in Class II earlier in this saga. It passed. She checked the vertex, edge, and face counts against the formulas the mathematics predicted. Those matched too, exactly. By every number our heroine knew to compute, the dome was correct.

It was not correct. Buried among several hundred properly-sized struts were thirty — one for every edge of the original icosahedron — that were roughly four times too long, because nobody had bothered to subdivide them at all. Euler's formula, it turns out, only confirms that a mesh is a valid closed shape; it has no opinion whatsoever on whether it's the *particular* closed shape you meant to build. A perfectly respectable sphere-topology object can still be quietly wearing thirty structural stilts.

The actual problem was one of those facts about chirality that sounds obvious once stated and was not obvious beforehand: a skewed pattern has no mirror symmetry, so a point sitting near the edge of one triangular face, computed independently, does not land on the same spot in space as the "same" point computed from the neighboring face's perspective. The two faces were being glued together only at their three shared corners and shrugging at everything in between, which is exactly how you end up with an edge that never got the memo about being subdivided.

Rather than trust her own second attempt at the math, our heroine went and found someone else's math to check it against — a well-established, independently written geodesic dome library — installed it purely as a private fact-checker (it never touches pyDome's own dependency list), and did not stop until her own dome's edge lengths matched that library's output not approximately, not "close enough," but to fifteen decimal places. `-c 3` and its companion flag `-n` now produce a Class III dome verified with the same paranoia previously reserved for catching floating-point noise in hub connector templates, because apparently that is simply how domes get built around here now.

Our heroine looked at all of this, decided the computer should do the arithmetic, and wrote pyDome so it would. The dome, presumably, is out there somewhere now, standing on the strength of several hundred correctly-computed angles, three distinct ways of getting to a sphere, and not one single argument with a protractor.
