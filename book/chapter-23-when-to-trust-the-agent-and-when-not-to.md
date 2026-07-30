# Chapter 23: When to Trust the Agent, and When Not To

No new dome, no new nesting job. This chapter is the after-action review our heroine holds after any real operation — a structured look back across everything Chapters 1 through 22 actually checked, and a single, generalizable rule underneath all of it, worth carrying to any geometry tool this book didn't write.

## The Thesis, Stated Directly

A check that only compares a result against its own internal assumptions can catch a **count** bug. It cannot catch a **shape** bug that happens to preserve the right counts. Every gotcha this book called a "real, verified" one traces back to a moment where that distinction actually mattered — and the sharpest illustrations in the whole book, one from each toolkit, made the identical point in two completely different parts of the codebase.

## Every Independent Check This Book Actually Used

**Euler's formula and `2E=3F`** (Chapter 5) caught Class II's real orthonormal-basis bug immediately — a genuinely useful, genuinely independent identity, true of *any* closed triangulated mesh, not something pyLair's own construction gets to define for itself.

**The `antitile` cross-check** (Chapter 6) is the sharpest illustration this book has of the thesis's own limit: Class III's first implementation satisfied Euler's formula *and* its own golden-value vertex/edge/face counts while still being wrong — thirty of the base icosahedron's edges left unsubdivided at full length, hidden behind two count-based checks that both happened to agree. Only a bit-for-bit comparison against an independently-written library, one that never shared a single line of code with pyLair's own construction, caught what two internal-consistency checks couldn't.

**The finite-difference gradient check** (Chapter 8) verified the true-ellipsoid-normal formula against a completely different method for computing the same quantity — not a restatement of the analytic formula, a numerical approximation of it, agreeing to within `1e-5` on a fully general triaxial case no single-axis hand computation alone could exercise.

**`trimesh`/`ezdxf`** (documented in pyLair's own `README.md` and exercised by its real test suite) recompute panel areas and inter-panel angles independently from pyLair's own exported files, cross-check truncated-panel clipping against `trimesh`'s own mesh-slicing routine as an independent ground truth, and parse a generated cutting template back out to confirm it reproduces the exact lengths it claims to — a parse-then-measure round trip, not a re-run of the same trigonometry the test is supposed to be checking.

**pyFit's own hand-checkable NFP case** (Chapter 19) — two unit squares producing exactly the `2×2` square from `(-1,-1)` to `(1,1)` — is the identical style of check as Chapter 6's antitile comparison, at a much smaller scale: a result verified against an answer computable by a human, independent of the code being tested.

**The Minkowski-sum union fix** (Chapter 19) makes Class III's own point a second time, in a different toolkit, solving a completely different problem: the buggy version passed that same hand-checkable unit-square case cleanly, and only failed on a second, differently-shaped and differently-sized case. `nfp.py`'s own real fix was itself checked against a second independent method — the convex hull of every pairwise vertex sum, a genuinely different way to compute the same Minkowski sum — not just declared correct because the unit-square case still passed.

## The Same Bug, Twice, in Two Toolkits That Share No Code

This is worth stating as plainly as the rest of this book states everything else: **Class III's cross-face stitching bug and pyFit's Minkowski-sum hole artifact are the same lesson, independently rediscovered, in two projects with no code in common.** Both passed their first real test case cleanly. Both were wrong anyway, in a way that first test case simply couldn't expose. Both were only actually caught once a second, differently-shaped case — or an entirely independent method — got run against them. One verified case is not the same claim as a verified method, and this book didn't have to invent a second example to make that point; the two projects it's actually about handed it one each, on their own.

**Prompt:**
> Looking back at everything this book covered, list every point where either pyLair or pyFit checked a result against an independent, differently-implemented source rather than just its own internal consistency. What do they have in common?

**What Comes Back:** The list above — Euler's formula, the antitile cross-check, the finite-difference gradient, the trimesh/ezdxf oracle, the hand-checkable NFP case, and the convex-hull cross-check. What they share: none of them ever let either project's own code be the only witness to its own correctness. Every one is either a general mathematical fact true regardless of implementation (Euler's formula), a separately-written library with no shared code (antitile, trimesh, ezdxf), a numerical method that doesn't rely on the same derivation (finite differences, the convex hull), or a case simple enough for a human to check entirely by hand (two unit squares).

## Two Honest, Different Correctness Stories

It's worth being precise about a real difference between the two toolkits' own guarantees, rather than treating "verified" as one uniform claim. A pyLair dome either matches its golden-value formula or it doesn't — a closed-form, binary, checkable claim. A pyFit layout is never "the" correct layout, only ever *a* legal one: every candidate placement is re-validated for overlap and containment before acceptance, so pyFit's honest guarantee is about **validity**, guaranteed by construction, and never about **optimality**, which a heuristic can't promise and doesn't pretend to. Chapter 20's own real, surprising result — disallowing mirroring using *fewer* sheets than allowing it, the opposite of the intuitive assumption — is exactly what that honesty looks like in practice: a heuristic's greedy choices can go either direction, and the tool never claimed otherwise.

Neither correctness story is weaker than the other; they're honest about two different kinds of problem. pyLair's geometry is closed-form because subdivision *is* closed-form. pyFit's packing is a heuristic because 2D nesting is NP-hard, and no tool that claims otherwise is being honest about the problem it's actually solving.

## Applied One Level Up

The same principle applies to this book itself, not just the two toolkits it teaches: every real number, every error message, and every historical bug in these pages is traceable to an actual commit, a real test, or a real run this book's own drafting process performed — not asserted from memory, and not assumed to still be true just because an earlier chapter said so. An outline that only checked its own internal consistency would have exactly the same blind spot Class III's first implementation, and pyFit's first NFP test case, both had: it would read as complete, pass its own review, and still be wrong in a way nothing internal to it could catch.

## What's Next

Chapter 24 closes the book — a full recap of both pipelines, a status update on every named design this book actually built, and an honest look at what each toolkit's own real, currently-open work still is.
