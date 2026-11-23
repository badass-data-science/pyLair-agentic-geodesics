**You just purchased a dormant volcano through three shell companies. Now you need to build your villainous geodesic lair on top of it.**

Your Rival already attempted this by asking a general-purpose AI chatbot to design his geodesic dome. The answer came back fluent, confident, and finished-looking: vertex lists, strut lengths, a parts order. However, the struts didn't meet. The four-sided panels folded like garden gates. His crew is still standing in the field, holding a pile of plausible numbers.

The trouble isn't that he used AI. It's that he let the AI do the geometry from memory, and never checked it. Hand the same job to an agent that calls real, typed, specifically designed geometry tools and shows you their raw output, and the dome closes. Correctly.

*Agentic Geodesic Lair Design for Supervillains* teaches geodesic computational geometry and agentic AI together, through two free, open-source Python toolkits driven by an AI agent over the Model Context Protocol (MCP): **pyLair**, which designs geodesic domes, and **pyFit**, which nests their panels onto sheets of your building material. You'll follow one dome, the Actual Secret Lair, from its first prompt to its last cut panel. Along the way you'll learn why each design decision matters, what the numbers coming back mean, and how to tell when to trust them. Every teaching example is comically villainous. None of the geometry is.

**Design a dome that closes**

- Pick a base polyhedron on purpose, then subdivide it three ways: the default Class I grid, Class II's even-frequency Triacon, and Class III's chiral "skew" lattice, where a dome and its mirror image share every count and still aren't the same building
- Check every build against golden-value formulas and Euler's formula, and learn why a count can be right while the shape is wrong
- Stretch a sphere into an ellipsoid for headroom, then cut it into a dome that stands on a crater floor, without landing the cut on a ring of vertices
- Compute the hub angles a connector needs, cluster hundreds of struts into a short cutting list, and catch the near-zero "sliver" struts and panels that a careless cut leaves behind
- Export DXF drawings, VRML and 3D-printable STL and OBJ models, and a cutting template for every distinct hub and panel shape

**Cut it, nest it, build it**

- Turn the bill of materials into a nesting job with no number typed by hand, and pack 260 panels onto real sheet stock (fewer sheets means fewer plywood trucks, and less Interpol heat)
- Understand the no-fit polygon and the bottom-left-fill heuristic behind 2D nesting, and why "valid" and "optimal" are different promises
- Handle chirality where it costs money: mirror-image panels, one-sided materials, and the surprising day forbidding a flip saved a sheet
- Get a per-piece assembly manifest that says which strut joins which hubs, and which panel goes where

**Put your agent to work, and keep it honest**

- Install both toolkits for Claude Code, OpenClaw, Hermes, Claude Desktop, or any MCP client, and fix the one configuration gotcha that breaks most setups
- Work the way the tools are built: cheap checks first, files written only at the end
- Write prompts that ask the right tool the right question, and spot a two-tool question disguised as a one-tool one
- Learn when to trust an agent and when not to: every independent check the book uses, gathered into one habit worth taking to any tool

**Built for practice, not just nodding along**

Seventy-four worked examples, each shown as the prompt you'd type, the tool's real JSON or output (what comes back), and what it means. Every number, error message, and file in the book came from a real run of the tools; none is a mockup. Forty-one figures are real tool renders or plots of real computed data, with no AI-generated art. Twenty-five chapters follow the build from first prompt to moving day. Appendices include a glossary, a complete command-line and MCP tool reference, and a reading list running from Euler, Goldberg, and Kenner to the open-source libraries behind 2D nesting.

You'll need some comfort with basic 3D coordinates and the command line. No background in geodesic geometry, nesting, or AI agents is required. This book is part of the *...for Supervillains* series, and it stands entirely on its own. A dormant volcano is recommended but not required.

**Your rival's chatbot gave him a dome that looked finished. Yours will close.**
