# Chapter 1: Introducing pyLair, pyFit, and the Agentic Interface

The studio apartment had, by any objective measure, reached capacity.

Not the apartment itself: our Heroine's mid-century furniture and modestly menacing houseplants still fit comfortably. The problem was the sub-basement, home of the Secret Lab™, which now held one particle accelerator (secondhand, mostly functional), four hundred liters of a coolant our Heroine would prefer not to name in writing, a whiteboard labeled "ULTIMATE CUNNING MASTER PLAN™ — DO NOT ERASE" that nobody had erased and everybody had stopped reading, and, as of last Tuesday, a shipping crate the invoice optimistically described as "decorative atmospheric processing equipment, quantity 1." The homeowners' association (HOA) had sent two strongly worded letters. A third seemed imminent, and the third letter, our Heroine had learned, is the one with a lawyer's name at the bottom.

It was time to build somewhere else. Somewhere bigger, somewhere that looked appropriately impressive from a helicopter, and somewhere built to survive wherever "somewhere else" turned out to be. Through three shell companies, our Heroine had already bought it: the crater of a dormant volcano, quiet for eleven thousand years and zoned, as far as anyone could tell, for nothing at all. What the crater needed was a building, and the building she had in mind was a geodesic dome. Domes enclose the most volume for the least material, they shrug off load from every direction, and they look tremendous from a helicopter.

So: something that looks cool, something that stands up, and, a detail our Heroine's growing henchman payroll made unavoidable, something a crew with a laser cutter and a truck full of plywood could *build*, on a schedule, without re-deriving three semesters of solid geometry first.

That last part is the hard part. Her rival had already shown what happens when you skip it.

## The Rival's Dome

The Rival Supervillain had wanted a dome too. He had typed "design me a geodesic dome, 10 meters across" into a general-purpose chatbot, received a confident page of Python and a tidy list of vertex coordinates, handed the list to his henchmen, and gone to lunch. The chatbot had picked an icosahedron, because every dome tutorial it had ever read used one, and computed a subdivision from half-remembered trigonometry. The coordinates looked like a dome. They sat in a JSON file looking finished.

Three weeks later his crew stood in a field holding struts that would not meet. Some hubs had too many sockets; some struts were a few centimeters long; one ring of panels, cut from the list's own numbers, would not close no matter how hard anyone pushed. Nothing in the chatbot's answer had checked that the dome's vertices and edges satisfied Euler's formula, that a hub's angles added up, or that two panels in the cutting plan didn't overlap. It gave him numbers and no reason to trust them, and it never mentioned that he should be worried.

Our Heroine kept a framed photograph of that field on her desk. It is the cautionary tale this book returns to, and the reason she did things differently.

## What This Book Is About

This is a book about **geodesic geometry**: subdividing a polyhedron into a fine triangular grid and projecting that grid onto a sphere, so that a structure built from many small, nearly identical triangles can approximate a dome without any one panel large enough to be weak on its own. In its second half it is a book about **2D nesting**: taking a pile of flat shapes and arranging them on sheets of real material with as little offcut as possible. Both subjects have names, citations, and known-correct formulas, and this book makes sure you understand all three before it lets you near a laser cutter.

It is also a book about doing both *with* an AI agent making the tool calls, because that is how our Heroine built her dome. The dome-design half is called **pyLair**. The sheet-nesting half is called **pyFit**. They are separate projects: pyFit has no code dependency on pyLair and will nest shapes that have nothing to do with any dome. A real fabrication project needs both, in sequence, and so does this book.

If the voice sounds familiar, pyLair has a companion blog post (`blog-posts/introducing-pylair.md`, in pyLair's GitHub repository) and pyFit has its own (`blog-posts/introducing-pyfit.md`, in *its* repository), covering the same ground in shorter form. This book is the long version, with room to teach the mathematics underneath both tools, not just their command-line flags.

## What "Agentic AI" Does Not Mean

"Agentic AI" does not mean "an AI that writes code for you and then you run it." That is what the Rival did, and it is autocomplete with extra confidence. Ask a chat model to lay a hundred triangular panels onto sheets of plywood and you get the same failure one dimension down: something that looks like a packing arrangement, improvised on the fly, with no collision check behind it. Computing a bevel angle or an overlap test correctly inside a wall of improvised code is hard to get right every time, and an LLM improvising geometry won't reliably remember the hard part.

**Agentic AI**, as this book uses the term, means something narrower and less glamorous: an AI model that reasons about *which typed tool to call next*, calls it, reads a structured result back, and decides what to do with that result, in a loop, until it has enough evidence to report something defensible. The geometry and the packing are not improvised. They are pre-built, tested functions a human wrote and verified (`pylair/api.py`'s `build_dome`, `pyfit/api.py`'s `run_nest`), and the agent's job is sequencing and judgment, not arithmetic.

Ask pyLair for a Class III dome at `(m,n)=(4,1)` and the agent calls a construction whose edge lengths were cross-checked against an independently written library to within 10⁻¹⁵. Ask pyFit to nest forty triangles onto three sheets of plywood and it calls a packer that re-checks every placement for overlap before accepting it, however the candidate position was found. That is a much smaller, more achievable ask of an LLM, and it is the architecture both toolkits are built around.

In our Heroine's Secret Lab™, the agent has a name, or at least a job title: **the AI Henchman**. It sits at the lab's terminal, fluent and quick and eager to summarize. What keeps it honest is that it can't make up a strut length. It has to ask pyLair for one.

Concretely, both pyLair and pyFit expose their functions as **MCP servers**, `pylair-mcp` and `pyfit-mcp`. MCP, the Model Context Protocol, is a standard way for an AI agent to discover a set of typed tools and call them. Each project also ships an **OpenClaw skill** for agents that drive the command-line interface (CLI) directly instead. You'll install both in Chapter 2. For now, hold on to the shape of it: typed tools an agent can't get wrong the way it can get free-form code wrong, plus a documented interface for using them well.

## Two Tools, One Discipline

pyLair answers one question: *given a base shape, a subdivision scheme, and some amount of stretching and slicing, what are the exact vertices, struts, and panels of the resulting dome, and what does it cost to build?* It hands back four kinds of things: a shape (vertex, chord, and face counts and positions); export files (DXF for CAD import, VRML for display, STL and OBJ for 3D printing, all defined in Chapter 17); a bill of materials (every strut length and count, every hub angle, every panel shape and cost); and cutting templates (one DXF per distinct hub connector shape and one per distinct panel shape). It knows nothing about water pressure, orbital debris, or building codes. It reports geometry, exactly, and stops there.

pyFit answers a different question, one dimension down: *given a pile of flat 2D shapes, how many of each you need, and the size of your sheet stock, where does each one go, and how many sheets does it take?* It hands back a placement report (sheet, position, rotation, and mirror flag for every part) and, once you're satisfied, one ready-to-cut DXF file per sheet. It has no opinion about where the shapes came from. A pyLair panel template and a stencil for a henchman's uniform patch are the same to it.

Neither tool does the other's job. pyLair has nothing to say about how many sheets of plywood your panels will consume: its `cost_per_unit_area` parameter computes a *theoretical* material cost that assumes zero waste, a number Chapter 23 shows is reliably wrong once real sheet layout is counted. pyFit has no idea what a geodesic dome is; it sees triangles. This book spends Parts II through V inside pyLair's half of the problem and Part VI inside pyFit's, because pretending they're one seamless product would hide a useful fact: the DXF file sitting between them is the whole handoff.

## Why Every Answer Comes Back as JSON, Not Prose

Every result in this book, every "What Comes Back" block in the chapters ahead, is written in a format called **JSON**, not in a sentence. That isn't a stylistic tic. It is part of what makes an agentic geometry tool trustworthy, so if you've never worked with JSON, get comfortable with it now.

**JSON** stands for JavaScript Object Notation. It long ago outgrew JavaScript and became the closest thing computing has to a universal, plain-text way of writing down structured data. The rules fit in your head at once:

- Curly braces `{ }` mark an **object**: an unordered set of `"name": value` pairs, the way a measurement goes with its label.
- Square brackets `[ ]` mark an **array**: an ordered list of values, used when a result is a sequence of things (a list of strut lengths, a list of per-sheet utilizations) rather than one thing.
- Every value has one of a few unambiguous types: a **string** in double quotes (`"icosahedron"`), a bare **number** (`4`, `1.618034`), `true` or `false`, or the literal `null`, which means *there is no value here*: not zero, not "unknown," not "didn't feel like computing it."

Put together, a JSON object looks like this, an excerpt from what pyLair's `design_dome` tool returns for a frequency-4 icosahedral sphere:

```json
{
  "vertex_count": 162,
  "edge_count": 480,
  "face_count": 320,
  "truncated": false,
  "height": 2.0,
  "footprint_diameter": 2.0,
  "total_strut_length": 143.20402572929999
}
```

Seven labeled values, each of a type that isn't in question. There is no ambiguity about what `162` refers to, because it sits next to the label `"vertex_count"`, not three sentences later in a paragraph.

**Why an agent needs this.** Picture the Rival's chatbot at the *output* stage: a tool that answers in a sentence, *"The dome has about 162 vertices and roughly 320 faces, and the struts total somewhere around 143 units."* A human reads that fine. An agent that has to *act* on it (check the vertex count against a golden-value formula, as Chapter 4 teaches; pass the strut total into a cost calculation; compare a panel count against a nesting job) first has to parse English back into numbers, guessing where each value lives. Phrase it differently on the next call ("about 162, give or take") and that parsing can silently break, though nothing about the dome changed.

JSON closes that gap. `"vertex_count"` is spelled the same way and holds a number on every call, from every tool. An agent doesn't interpret pyLair's output; it reads the field by name, the way a spreadsheet formula reads a cell. That is what "typed tool" cashes out to when a result comes back: the *shape* of the answer is promised in advance, and JSON is the checkable form of the promise.

It also explains a habit you'll see in nearly every chapter: this book shows you the JSON a tool returned, not a paraphrase. Reading the raw result, with its exact field names and its exact `null`s, is the discipline an agent should apply every time, and the book holds itself to the same standard.

## The Danger Is at the Joint, Not the Piece

Here is the failure both halves of this book keep circling. In dome design, a strut's length is a forgiving kind of wrong: get one slightly off and you have an annoyance, not a catastrophe. A **hub angle** is not forgiving. Every strut meeting at that hub inherits the error, and a dome with one systematically wrong hub angle may fail to close in three dimensions however careful the rest of the build is. The Rival's field proved it. The danger lives at the *joint*.

Nesting has its own version, and it lives at the **no-fit polygon** (Chapter 19 defines it properly), which describes every position a shape is *not* allowed to occupy relative to its neighbors on a sheet. Get one shape's outline slightly wrong and you waste a little plywood. Get the no-fit polygon itself wrong and the software can approve a placement where two panels overlap, a mistake that shows up the moment the laser cutter tries to cut the same patch of plywood twice.

That is the design tension both toolkits are built around, and the idea worth carrying out of this chapter: **agent judgment is valuable for open-ended reasoning (which polyhedron fits this design goal, which rotation step trades packing quality for speed) and dangerous at the points where a small, plausible error compounds into a structure that doesn't close or a cut plan that overlaps.** Both `pylair/api.py` and `pyfit/api.py` keep their geometry (validation, hub angles, no-fit polygons) in one shared, rule-based engine used identically by the CLI and every MCP tool, rather than letting an agent freelance the math per request.

You'll meet the sharpest illustration in Chapter 6, where a first version of pyLair's own Class III construction passed every count-based check available and was still wrong, and its nesting-side counterpart in Chapter 19, where a first version of pyFit's no-fit-polygon code passed its first hand-checked test and failed the second. Both near-misses happened to careful engineers checking their own work, which is why the checking has to be systematic, not a feeling that the shape looks right.

## A Preview, Not Yet an Answer

Chapter 3 is where you'll pick a polyhedron and get a dome back. Here is the field-name skeleton of what `design_dome` hands back, before Chapter 3 fills in numbers:

```json
{
  "vertex_count": ...,
  "edge_count": ...,
  "face_count": ...,
  "truncated": ...,
  "bounding_box": ...,
  "height": ...,
  "footprint_diameter": ...,
  "total_strut_length": ...,
  "resolved_parameters": {
    "radius": ..., "frequency": ..., "polyhedron": ..., "dome_class": ..., ...
  }
}
```

And here is its counterpart one problem over, the skeleton of `design_nest`, which you'll meet in Part VI:

```json
{
  "sheets_used": ...,
  "utilization_by_sheet": [...]
}
```

The two answer different questions but share a form: flat, labeled, and ready to act on, `vertex_count` next to `face_count`, `sheets_used` next to `utilization_by_sheet`. It is the same rule in both toolkits: **a result worth trusting is one you can name a field in, not a sentence you have to interpret.** You'll see both skeletons filled in as soon as Chapter 2's installation smoke test, and with a real design behind them for the rest of the book.

## The Cast, and the Commissions

Every dome and nesting job in this book belongs to *somebody*, and that somebody wants it for a specific, defensible, only slightly unhinged reason. A design constraint stops being abstract the moment it's *your* pressure hull, *your* launch mass, *your* henchmen waiting on a cutting template. Villainy isn't the garnish here. It's the load case.

The people first. **Our Heroine** designs by prompting and reads the JSON herself. **The AI Henchman** calls the tools. **The Foreman**, head of the construction crew, owns the tape measure and trusts nothing he can't measure; most of the questions a builder asks in this book are his. **The Chief Financial Villain** (CFV) counts struts, sheets, and money. **The Junior Henchman** runs the laser cutter, enthusiastically and literally. And somewhere offstage, **the Rival Supervillain** is still standing in his field.

Then the designs, each introduced properly when it comes up:

- **The Actual Secret Lair.** The dome this book is about, destined for the volcano's crater. It first appears in Chapter 4, goes through every subdivision class, is stretched for headroom in Chapter 8, sliced flat for a foundation in Chapter 9, costed in Part IV, exported in Part V, and nested and labeled for assembly in Part VI.
- **The Proof-of-Concept Yurt.** Not a real design: Chapter 2's installation smoke test, a coarse frequency-2 sphere whose job is proving the wiring works before anyone's reputation depends on the output.
- **The Under-the-Ocean Prototype.** A pressure hull for a contingency the HOA keeps making more attractive (Chapters 3, 8, and 11, with its panels nested in Chapter 20). The ocean does not negotiate, so neither does the shell.
- **Chapter 11's commissions.** Once word of the Secret Lab's™ dome gets around, other villains want one: the **Orbital Panopticon**, a circumpolar station where every kilogram of strut has to survive a rocket first; the **Magma Redoubt** and the **Permafrost Cache**, two lairs that stay buried for opposite reasons; and the **Ostentatious Mesa Spire**, for a client who has no intention of hiding. A coda scales the same tool down to the studio apartment's closet.
- **A henchman's uniform patch and a throwing-star stencil.** pyFit's own running example (Chapter 19), chosen to have nothing to do with any dome, as proof that the nesting half is a standalone tool.

None of these briefs makes the mathematics less rigorous. Euler's formula holds as hard for a volcano lair as for a test sphere, and a no-fit polygon doesn't care whose throwing stars it's nesting. What the briefs do is give every formula, gotcha, and bug story a reason to exist beyond "because the syllabus says so."

**[IMAGE: ../blog-posts/edited_truncated.png | A truncated geodesic dome exported by pyLair and shown shaded in a 3D viewer: a hemisphere of pale blue triangular panels on a flat base.]**
**[CAPTION: Where this is going: a truncated geodesic dome, exported by pyLair and opened in a 3D viewer. Parts II through V earn the right to build one like it.]**

**[IMAGE: examples/images/nest_sheet1_pylair_triangles.png | Triangular dome panels nested onto a rectangular sheet by pyFit, packed edge to edge with small gaps of unused material.]**
**[CAPTION: A pyFit nesting result: pyLair-designed triangular panels laid out on one sheet, ready to cut. Part VI exists to produce this.]**

## What's Next

Chapter 2 installs pyLair and pyFit, connects both to an agentic platform (OpenClaw, Claude Code, Hermes, Claude Desktop, or another MCP client), and proves each connection with one deliberately trivial tool call. The Foreman insisted on that order. "Nobody," he said, looking at the framed photograph on our Heroine's desk, "designs a lair on equipment they haven't tested."

After that, Part II starts the design for real, with the first geometric question: not "does the connection work," but "which shape should this start from, and why."
