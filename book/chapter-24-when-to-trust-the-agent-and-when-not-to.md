# Chapter 24: When to Trust the Agent, and When Not To

Every operation at the Secret Lab™ ends with an after-action review, and the Actual Secret Lair's was held in the half-built dome itself, on folding chairs, under a crown hub the Foreman had welded with his own hands. Our Heroine wrote one question on the whiteboard they'd carried up from the sub-basement: *What did we check, and what did we check it against?* The framed photograph of the Rival's field leaned against the whiteboard's leg.

No new dome and no new nesting job in this chapter: a structured look back at everything Chapters 1 through 23 checked, and the one rule underneath it all, worth taking to any geometry tool this book didn't write.

## The Thesis

A check that compares a result only against its own assumptions can catch a **count** bug. It cannot catch a **shape** bug that happens to preserve the counts. Every gotcha in this book traces back to a moment where that distinction mattered, and the sharpest illustrations, one from each toolkit, made the same point in unrelated code.

## Every Independent Check This Book Used

**Euler's formula and `2E = 3F`** (Chapter 5) caught Class II's perpendicular-axes bug immediately: identities true of *any* closed triangulated surface, not something pyLair's construction gets to define for itself.

**The `antitile` cross-check** (Chapter 6) shows the limit of count checks. Class III's first implementation satisfied Euler's formula *and* its golden-value counts while leaving thirty of the icosahedron's original edges unsubdivided. Only a comparison against an independently written library, sharing no code with pyLair, caught what two internal checks couldn't.

**The finite-difference gradient** (Chapter 8) checked the ellipsoid-normal formula with a different method for computing the same quantity: a numerical approximation, not a restatement of the formula, agreeing within `10⁻⁵` on a general three-axis case.

**`trimesh` and `ezdxf`** (in pyLair's test suite, run when the `verify` extra is installed) recompute panel areas and angles between panels from pyLair's exported files, check truncated panels against `trimesh`'s own mesh-slicing routine, and read a generated cutting template back in to confirm it reproduces the lengths it claims: a round trip through files, not a re-run of the trigonometry under test.

**The strut–panel cross-reference** (Chapter 22) caught the base-ring bug, which no count could, because a truncated dome has no golden value to contradict. Every panel edge had to name its strut; fifty couldn't. It's the one check on this list that wasn't built as a check at all.

**pyFit's hand-checkable no-fit polygon** (Chapter 19), two unit squares giving the `2×2` square from `(-1,-1)` to `(1,1)`, is the same kind of check at a smaller scale: a result compared with an answer a person can compute by hand.

**The convex-hull cross-check** (Chapter 19) verified pyFit's Minkowski-sum fix by a second method, the convex hull of every pairwise sum of corner points, rather than declaring it correct because the unit-square case still passed.

**Reading the report** (Chapter 16) belongs here too, in a humbler way: the documented safe cutoff still left slivers on one dome, and only looking at the artifact lists showed it.

## The Same Bug, Twice, in Two Toolkits That Share No Code

Stated plainly: **Class III's stitching bug and pyFit's Minkowski-sum "hole" are the same lesson, discovered independently in two projects with no code in common.** Both passed their first test cleanly. Both were wrong anyway, in a way that first test couldn't expose. Both were caught only when a second, differently shaped case, or an independent method, was run against them. One verified case is not a verified method, and the book didn't have to invent an example to make the point; its two subjects supplied one each.

**Prompt:**
> Looking back at everything this book covered, list every point where pyLair or pyFit checked a result against an independent, differently implemented source rather than its own internal consistency. What do they have in common?

**What Comes Back:** The list above: Euler's formula, the antitile comparison, the finite-difference gradient, the trimesh and ezdxf checks, the strut–panel cross-reference, the hand-checkable no-fit polygon, and the convex hull. What they share is that none lets either project's code be the only witness to its own correctness. Each is a mathematical fact true of any implementation (Euler's formula), a separately written library (antitile, trimesh, ezdxf), a different method that doesn't rely on the same derivation (finite differences, the convex hull), a second view of the same data that has to agree with the first (struts and panels), or a case simple enough to check by hand (two unit squares).

## Two Honest, Different Correctness Stories

The two toolkits' guarantees differ, and "verified" shouldn't be read as one uniform claim. A pyLair dome matches its golden values or it doesn't: a closed-form, yes-or-no, checkable claim. A pyFit layout is never "the" correct layout, only *a* legal one. Every placement is re-checked for overlap and containment before acceptance, so pyFit guarantees **validity**, by construction, and never **optimality**, which a heuristic can't promise and doesn't pretend to. Chapters 20 and 21 showed what that honesty looks like: a coarser rotation step that sometimes costs a sheet and sometimes doesn't, and a mirroring choice whose effect on the sheet count can't be predicted, only measured.

Neither story is weaker. pyLair's geometry is closed-form because subdivision is. pyFit's packing is a heuristic because 2D nesting is NP-hard, and a tool that claimed otherwise would be dishonest about its problem.

## Applied One Level Up

The principle applies to the book too. Every number, error message, and bug story in these pages is meant to trace to a code change, a test, or a run. The revision that produced this edition re-ran every example against the current code, and the exercise proved the point. Some numbers had drifted as the tools improved: a nesting batch that once needed six sheets now needs five. One figure caption described bottom-left fill as filling rows when the code, and the figure itself, fill columns. One chapter had chosen a different base polyhedron for the Under-the-Ocean Prototype than the two chapters that built it. Each was internally consistent with its own chapter, passed a read-through, and was wrong in a way only an outside check could catch.

So, to answer the question on the whiteboard: trust the agent to sequence tools, read fields, and summarize. Don't trust it, or yourself, or a book, to be the only witness to a number that will be cut, welded, or bolted. The AI Henchman didn't object. It has never claimed to be its own witness; that was always the Rival's mistake, not his chatbot's.

## What's Next

Chapter 25 closes the book: a recap of both pipelines, a status report on every design the book built, and an honest look at what remains open in each toolkit.
