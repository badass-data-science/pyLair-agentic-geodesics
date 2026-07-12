# Introducing pyDome (or, How Our Heroine Designed a Geodesic Secret Lair)

Our heroine's secret laboratory is quickly becoming too big to fit inside her studio apartment, and that issue's now throwing a real grenade into the wheels of her Ultimate Cunning Master Plan&trade;.  She needs more room to house her bold experiments, and, being rather stylish, she wants that additional space to look cool. Our heroine also wants the structure to handle pressure gradients well, because one should deploy a secret laboratory either deep under the ocean's surface or in circumpolar orbit; certainly not within an unassuming San Diego neighborhood!

Enter geodesic design.

Geodesic structures distribute structural stress relatively evenly across their surfaces, rather than concentrate such stress in focal points such as walls and a roof. This makes them strong for their weight, the primary reason individuals keep building them despite the aggravating number of angular calculations involved. This also makes geodesic structures more robust to pressure variation when inserted deep into a water column.

One can buy a geodesic dome kit, of course, but why do that when one wants extreme customization? Therefore, before touching any power tools or even any CAD interface, our heroine requires her own geodesic calculations.

So she built pyDome.
# What It Does

Essentially, pyDome computes the vertices and chords of a geodesic dome (or sphere) and writes them out as both DXF and VRML files (for CAD software and for impressing friends with cool 3D graphics, respectively). Optionally it produces STL and OBJ files to facilitate 3D printing of scale models.

Additionally, pyDome delivers a full **bill of materials** for the user's geodesic project detailing every struct length, how many struts of each length the user needs, the exact angles at which each strut meets at the hubs, and a optional overall cost estimate if the user tells the software how much the user's chosen strut material costs per unit length.

Users tell pyDome how big they want their geodesic dome/sphere to be by setting the radius. They also specify the "frequency" of the structure, i.e., how finely to divided the source polyhedra's faces (see below) into the sub-triangles which later get projected onto the sphere (again, see below). Users select between three different polyhedral face subdivision patterns, specify whether they want a whole sphere or a truncation of the sphere into a dome, and finally whether they want the structure optionally stretched tall or squashed wide. pyDome then returns all the strut and angle information required to actually produce a physical structure.
# How It Works

Here is the basic method pyDome applies:

**Step one: pick a base polyhedron.** pyDome starts from an icosahedron by default (twenty triangular faces, twelve vertices), although it can also start from an octahedron if the user requests it. Either way, the basic idea is that if one is going to approximate a sphere, one should start from an object that is already reasonably sphere-shaped and symmetric.

![An icosahedron](edited_icosahedron1.png)

**Step two: subdivide the polyhedral faces.** pyDome divides one of the faces into a grid of smaller triangles (taken together, the resulting face is called a "symmetry triangle"). After computing the symmetry triangle for one face, the software copies rotated versions of it onto the other faces, replacing those original faces with the new symmetry triangles as shown below:

![Each face subdivided into a triangular grid](edited_4_unprojected1.png)

pyDome's "frequency" setting enables users to specify how finely they want each of the original polyhedron's faces divided; the higher the frequency, the more spherical the final projection. The trade-off though is that the higher the frequency the more distinct strut types and hub angle configurations are required to actually build the structure.

When creating the initial symmetry triangle, pyDome will draw the grid in one of three distinct ways. The Class I, "Alternate" method draws the grid parallel to each face's own edges This is the software's default configuration and the one shown in the image above.

The Class II, "Triacon" method first splits each face into six smaller triangles around its center then divides those smaller triangles instead, producing a strut pattern significantly different from that of Class I. Class II requires an even frequency setting due to the nature of this construction method.

Class III, the "Skew" method, lays its grid down at an angle instead of running it parallel to the original polyhedron's face boundaries or radiating it from the polyhedron faces' centers.

**Step three: project onto a sphere.** By this point, every point still flatly resides on the faces of the polyhedron. pyDome then pushes these points outward onto the surface of an actual sphere, preserving the chord pattern that connects them as it goes. The result appears to the human eye as a sphere composed of struts. As it does this, the software ensures that points computed for different symmetry triangles, but sharing the same physical location, are collapsed into single points, rather than simply duplicated in the structure's manifest.

![The subdivided grid projected onto a sphere](edited_4_projected1.png)

**Step four: optional elliptical stretching.** Not everyone wants a perfect sphere. If the user asks for vertical elongation, pyDome stretches the whole structure along its vertical axis, increasing the ceiling height while maintaining the same equatorial radius. Similarly, the software can, if requested, squish the structure vertically to reduce the ceiling height while maintaining the original base equatorial radius.

![elliptical stretching](ellipsoid.png)

**Step five: optionally truncate the sphere/ellipsoid into a dome.** Doors prove difficult to install on the underside of a full sphere, so pyDome provides the option to slice the bottom of the (possibly now ellipsoidal) shape off at a chosen height, thus producing a dome-like structure. The user can specify exactly how much to take off the bottom; 1/3 and 1/2 the diameter of the sphere are common selections.

![The sphere truncated at the equator into a dome](edited_truncated.png)

**Step six: produce visualizations.** In addition to providing a bill of material (discussed below), pyDome creates a DXF file for import into CAD software, and VRML file to help users impress their friends with archaic 3D web formats. Because VRML players sometimes prove difficult to track down, the software can also optionally produce STL or OBJ output, useful for not just 3D visualization but also 3D printing as well. Users can also ask the software to produce a preview PNG image to facilitate rapid concept iteration.

![The dome loaded into a CAD program](CAD_dome.jpg)

**Step seven: bill of materials.** This is our heroine's favorite part, and arguably the actual point of the whole exercise. For every hub in the structure (every point where two or more struts converge), pyDome reports two kinds of angle:

First, the software reports the angles between each strut and the plane tangent to the sphere at that hub, which tells users how far a hub connector has to deflect inward to receive a given strut:

![The tangent-plane deflection angle at a hub](tangent_angle_image_CROPPED.png)

Second, the software reports the "spoke" angles: pyDome projects all struts entering a given hub onto same tangent plane discussed immediately above, picks one of the struts as the reference strut, and then measures how far around the hub each of the other struts sits relative to it:

![The spoke angles around a hub](spoke_angle_image_CROPPED.png)

Taken together, these two angle types define, for every single joint in the entire structure, exactly how to bend/cut/grow one's source material to fit the whole structure together correctly.

pyDome also produces a list of strut lengths and how many struts of each length are required to build the structure, as well as a summation of the total length of strut material required. If the user provides a price per unit length, then a cost estimate of total strut material required is reported as well.

**Step eight: hub templates.** A geodesic project will likely require multiple (but repeated) distinct hub angle configurations. To assist designers, pyDome optionally creates 2D DXF cutting templates for each genuinely distinct hub shape in the structure, correctly recognizing that two hubs which are actually the same shape, just rotated relative to each other, only require one template between them.
# Talking to pyDome

Mojitos, as it turns out, do not mix well with typing `pydome -o output/lair -f 6 -c 3 -n 4 -t 0.4`, squinting at a JSON wall of hub angles, then opening a CAD program just to check whether frequency 6 actually looks like anything sensible before committing to it. Our heroine wanted to describe the dome she wanted in plain language and have something else handle the fiddly bits, so pyDome now speaks [MCP](https://modelcontextprotocol.io) (Model Context Protocol) as well as command-line flags.

Running `pydome-mcp` starts a small server that hands an AI assistant four tools instead of one command:

* **`design_dome`**, for cheaply asking "what does frequency 6 Class III with n=4 give me?" without writing a single file, just vertex/edge/face counts, a bounding box, and a total strut length to sanity-check against a budget.
* **`preview_dome`**, which is the one pyDome could never do from the command line: it renders the wireframe and hands the picture straight back into the conversation. No CAD viewer, no opening a PNG in a separate window, just "here's your dome" right where you asked for it.
* **`get_bill_of_materials`**, for interrogating strut counts and connector angles before deciding a design is worth building.
* **`export_dome`**, for when the design is actually settled and it's time to write the DXF, VRML, STL, OBJ, and hub-connector-template files to disk for real.

The idea is to let an assistant iterate the way our heroine would iterate herself: try a shape, look at it, check what it costs in struts, adjust, and only export once it's actually right — rather than round-tripping through the command line and a separate viewer for every guess. All four tools enforce the exact same validation rules as the CLI (an odd frequency is still not a valid Class II dome, no matter which door you walked in through), because underneath both interfaces now share one geometry engine instead of two copies of the same logic quietly drifting apart.
# Next Steps

* pyDome is currently strut-centric in its output, but our heroine's practical design requirements might evolve toward face-centric thinking. For example, suppose she decides to assemble her final structure out of 3D-printed symmetry triangles; this would require a face-centric point of view and the bill of materials would have to be enhanced accordingly to facilitate it. Possibly the templates too.
* Our heroine will likely experiment with AI-based interaction with pyDome's source code, such as asking Claude Code to review the existing code and then design a DXF file modification that creates a door-frame design. Our heroine is not sure if this will work, but thinks it worth a try. (Doorways are hell for any geodesic building design; if AI can improve this situation that would be awesome!).
* This is going on PyPI soon!
# Conclusion

Our heroine decided that a computer should perform the geodesic arithmetic necessary for designing her future secret laboratory whilst she drinks Mojitos on the beach. Therefore, she wrote pyDome to make these computations happen.

The actual construction of the forthcoming geodesic secret laboratory will (of course) be kept secret.
# Works Consulted

* Kenner, H. (1976). _Geodesic math and how to use it_. University of California Press.
* [`antitile`](https://github.com/brsr/antitile). A well-established, independently written geodesic dome library used to validate pyDome's computation results. (Our heroine assumed that either both she and this project's authors are simultaneously correct--their results matched to 15 decimal places--or that both are wrong in the exactly same way!).
* Šiber, A. (2007). _Icosadeltahedral geometry of fullerenes, viruses and geodesic domes_. [arXiv](https://arxiv.org/abs/0711.3527). https://arxiv.org/abs/0711.3527
# Code

pyDome is available [here](https://github.com/badass-data-science/Engineering/tree/main/Geodesic-Dome-Design/pyDome).
# AI Use Statement

Our heroine wrote this article about 99% manually, with a small amount of outline assistance from Claude Code.

She wrote the original pyDome implementation from scratch in Python, and then had Claude code refactor it a bit to make it PyPI-ready. She also collaborated with Claude Code to add features missing from her original implementation (Class II and III polyhedra face subdivision methods, sphere elongation functionality, and STL/OBJ/PNG output), and, most recently, to design and build the MCP server described above.
# Tags

geodesic
geodesic math
geodesic dome
pyDome
Python
PyPI
engineering
structural engineering
mechanical engineering
CAD
DXF
STL
OBJ
VRML
3D printing
triacon
symmetry triangle
polyhedron
icosahedron
octahedron
geometry
analytic geometry
NumPy
Claude Code
agentic AI
MCP
Model Context Protocol
Ultimate Cunning Master Plan

