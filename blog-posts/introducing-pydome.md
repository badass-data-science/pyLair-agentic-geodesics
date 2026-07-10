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

Our heroine looked at that tradeoff, decided the computer should do the arithmetic, and wrote pyDome so it would. The dome, presumably, is out there somewhere now, standing on the strength of several hundred correctly-computed angles and not one single argument with a protractor.
