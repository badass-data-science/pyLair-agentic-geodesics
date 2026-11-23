# Agentic Geodesic Lair Design for Supervillains

A book teaching geodesic dome geometry, 2D nesting, and agentic tool use through two real toolkits, pyLair (this repository) and pyFit (`~/Desktop/projects/pyFit-agentic-polygon-nesting`), driven over MCP. It sits in the "...for Supervillains" series beside *Agentic Time Series Forecasting for Supervillains* (`~/Desktop/projects/omen-agentic-time-series-forecasting/book/`, the closest kin: same MCP framing), *Systems Thinking for Supervillains*, and *Strategy for Supervillains* (both in `~/Desktop/projects/operation-clusterfuck/writing/books/`). Check those books' `AGENTS.md` files when a convention isn't covered here.

`outline.md` is the original plan. The chapter files are canonical; where they differ, the chapters win (see the note at the top of the outline). The repository's own `AGENTS.md` (one directory up) covers the code.

## Voice and house style

These carry over from the series:

- **The author is always "our Heroine"**: capitalized, never named in the prose. The byline is *Lady Napalm*, as in the later volumes; the legal name appears only in the title page's copyright line.
- **Comedic but rigorous.** Every joke sits on a correctly explained idea, never in place of one.
- **MCP framing.** Every worked example is a **Prompt** (what you'd type to your agent), **What Comes Back** (the tool's real output, trimmed where long), and **What It Means**. Keep it.
- **What Comes Back shows JSON.** Every prompt that calls a tool shows that tool's JSON. Long results appear as a **snapshot** (the convention Chapter 2 explains): every top-level field, each list's first entry or two, a bare `...` for anything left out, numbers rounded to four places, but parameters such as `0.499999` never rounded. The three picture tools (`preview_dome`, `render_assembly_schematic`, `preview_nest`) return an image and a one-line caption, not JSON, so an image prompt also asks for the matching JSON tool (`design_dome`, `get_assembly_manifest`, `get_nest_report`) and shows both. Conceptual prompts that call no tool, and error demonstrations, show what really comes back instead.
- **Code fits a Kindle screen.** JSON lines stay within 52 characters, laid out pprint-style by `tools/json_pretty.py` (run it on any chapter after adding or changing a JSON block; it checks the values are unchanged). Python lines stay within 42 (the EPUB doesn't shrink Python to fit), and other code is wrapped by hand at natural breaks. Only an unbreakable token (a URL, a path, the `"Angles at hub between outbound cords and tangential plane"` key) may run over.
- **Every number is real.** Every JSON block, count, and error message must match what the current code returns for the parameters shown. If you change a chapter's parameters, or the code changes, re-run the example (`/home/emily/venvs/core/bin/python` has pylair and pyfit installed; `pylair.mcp_server`'s tool functions can be called directly). Trimmed output is marked as trimmed.
- **Term conventions.** "Secret Lab™" carries the glyph every time ("Secret Lab's™" for the possessive), as do "Powers That Be™" (every reference to the Powers That Be™, no exceptions) and "Ultimate Cunning Master Plan™". Write "Interpol heat," never bare "heat," for the attention an operation draws. The Secret Lab™ is our Heroine's operation; **the Actual Secret Lair** is the dome being designed to house it.
- **No word-wrapping inside paragraphs or bullets.** One paragraph, one physical line.
- **Keep running-prose paragraphs to roughly 130 words or fewer**, split where the argument turns.
- **Go easy on filler intensifiers and dashes** ("actually," "genuinely," "exactly," "real" as an all-purpose intensifier, stand-alone em dashes). Prefer a comma, colon, or full stop.
- **Define every acronym in plain language at its first appearance** (MCP, JSON, DXF, VRML, STL, OBJ, NFP, BLF, BOM, LCD, SSS, CAD, HOA).
- **Favor gender-neutral language** for generic people ("they," "the builder"); "henchman/henchmen" is series vocabulary and stays.
- **Front-matter prose is the author's own.** Change it only to fix facts or bring it in line with conventions she set in the other volumes, and say so in the PR.
- **Figures** are real tool output or plots of real computed data, never generated art. Write each as `**[IMAGE: path | alt-text description]**` then `**[CAPTION: text]**` on the next line; the build numbers them "Figure N.M" per chapter, and prose refers to them that way. Describe what the figure shows in the alt text; it is read aloud on the Kindle.
- **Cross-references** name the chapter by number ("Chapter 9's flat-chord refusal"). `book-assembly/assemble_book.py --check-only` catches out-of-range chapter numbers and missing figures, not wrong ones: when you move material, grep for references to it.

## The running story

Each chapter opens with a short scene (one to three paragraphs) that sets up its concept, and the story moves forward in "What's Next" or a closing beat. A scene must teach or motivate the chapter's idea; no scene stands in for an explanation.

**The arc.** Our Heroine's Secret Lab™ has outgrown the sub-basement of her San Diego studio apartment. The homeowners' association (HOA) has sent two letters; the third, she knows, is the one with a lawyer's name at the bottom. She has bought, through three shell companies, the crater of a dormant volcano, and the Actual Secret Lair, a geodesic dome, will stand on its floor (the series' later volumes find her running a volcanic lair). The book follows the dome from first prompt (Chapter 1) to the last panel cut (Chapter 22) and moving day (Chapter 25), when the third letter finally arrives at an empty sub-basement.

**Cast** (pronouns fixed; balanced):

- **Our Heroine** (she). Designs by prompting; checks the JSON herself.
- **The AI Henchman** (it). The agent at the Secret Lab's™ terminal that calls pyLair's and pyFit's tools. Fluent, quick, eager to summarize; kept honest by typed tools and our Heroine's insistence on raw results.
- **The Unbending Foreman** (he). Always "the Unbending Foreman," never bare "the Foreman" (the adjective is a nod to Chapter 10: triangles don't fold). Head of the construction crew; owns the tape measure and trusts nothing he can't measure. Asks the builder's questions: does it close, what angle, which piece goes where.
- **The Chief Financial Villain** (she). Always spelled out in the prose, never abbreviated "CFV." Counts struts, sheets, and cost; the person Chapter 20's sheet count and Chapter 23's "theoretical cost" are for. (Same office as in *Strategy for Supervillains*.)
- **The Junior Henchman** (they). Runs the laser cutter; enthusiastic, literal, the one who would cut 120 left-handed panels if nobody told them about chirality.
- **The Rival Supervillain** (he). Had a general-purpose chatbot freehand his dome's geometry. It looked finished. It did not close. His dome is the book's running cautionary tale (Chapters 1–6, 10, 12, 21, 22, 24, 25); a disgruntled henchman sells his files and photographs to the Secret Lab™. In Chapter 25 he asks to borrow her templates.
- **The HOA** and its president (she): the ticking clock (Chapters 1, 2, 3, 9, 25).

The Unbending Foreman's shelf of things that went right (the LEFT and RIGHT cardboard models of Chapter 6, the test hub connector of Chapter 12) and the framed photograph of the Rival's field are small recurring props.

**Other running elements.** Interpol heat: a convoy of plywood trucks to a dormant volcano draws attention, so fewer sheets means less Interpol heat (Chapters 20, 21). The Proof-of-Concept Yurt (Chapter 2), the Under-the-Ocean Prototype (Chapters 3, 8, 11, 20, 23, 25), and Chapter 11's commissions from other villains (Orbital Panopticon, Magma Redoubt, Permafrost Cache, Ostentatious Mesa Spire, the studio-apartment coda). The henchman uniform patch and throwing-star stencil (Chapter 19).

## Accuracy and citation rules

- **Every citation must be real and independently verified** (author, title, venue or publisher, year). Unverifiable sources are cut or flagged, never approximated. Appendix C is the bibliography; prose attribution is light.
- **Technical claims about the code** (defaults, error text, tool names, file names) are checked against the source, not memory. pyLair has seven MCP tools; pyFit has four.
- **Historical claims** (Fuller's patent, Kenner's and Clinton's books, Euler's formula) are checked against a real source.

## Building and tools

`book-assembly/assemble_book.py` builds `dist/geodesic-lair-book.{md,pdf,epub}`; see its README. Run `--check-only` after editing figures or cross-references. `tools/json_pretty.py FILE...` re-lays out ```json blocks to the 52-character width (`--check` reports without changing anything). `tools/style_check.py` reports paragraphs over 130 words, filler and dash counts, lower-case "our heroine," and a missing ™; `tools/split_para.py FILE LINE` splits a long paragraph at the sentence nearest its middle (reread the result).

## Decisions log

- **2026-11-22.** Revision pass bringing the book in line with the series' later volumes: added this file and the running story above; replaced `examples/assemble_book.py` with `book-assembly/assemble_book.py` (adapted from *Strategy for Supervillains*); converted figures to IMAGE/CAPTION tags numbered "Figure N.M"; re-ran every example against current pyLair and pyFit; style pass (filler words, dashes, paragraph length, "our Heroine," Secret Lab™).
- **2026-11-23.** At the author's request, the book no longer tells how pyLair's or pyFit's bugs were found or how the code changed over time ("an earlier version," "the fix," before-and-after figures). It still teaches that checks must be independent, by describing what the code does and the independent checks its authors apply (Euler's formula, golden values, `antitile`, `trimesh`/`ezdxf`, the strut–panel cross-reference, the hand-checkable no-fit polygons, the convex hull). Also: "CFV" is always spelled out as "Chief Financial Villain."
- **2026-11-23 (JSON in What Comes Back).** At the author's request, every tool-calling prompt now shows its JSON, as a snapshot when long; image prompts pair the picture with the matching JSON tool; Chapter 2 explains snapshots once and how to save results to disk. Every snapshot was regenerated from the current code, including Chapter 20's four nesting runs, which reproduced the book's sheet counts exactly. Figure 19.1 was regenerated from a now-stated job spec (its original shapes weren't recorded), and Figure 17.3 (`two-axis-secret-lair.png`) was added. All code was then laid out for a Kindle screen with `tools/json_pretty.py`.
