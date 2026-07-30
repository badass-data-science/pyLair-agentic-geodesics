# Chapter 23: Prompting pyLair and pyFit Like You Mean It

Twenty-one chapters have taught two toolkits, eight tools between them, and a long list of real gotchas. This chapter is a clinic, not a lesson: four real, flawed prompts, rewritten and explained — reusing designs this book has already built rather than inventing new ones, because the whole point is practicing on material you already understand.

## Prompt One: Too Vague to Carry Anything Forward

> *"Design me a dome."*

No radius, no frequency, no class, no intended use. An agent handed this prompt has no reason to route around pyLair's own plain numeric defaults — `icosahedron`, Class I, frequency `4`, radius `1.0`, exactly what `design_dome`'s own signature falls back to when nothing else is specified — toward anything resembling the Actual Secret Lair this book actually built.

**Rewritten:**
> "Using the `(m,n)=(4,1)` Class III configuration from Chapter 6, at the elongation and truncation from Chapters 8–9, run `design_dome` and confirm the vertex/face counts still match what we found there before we export."

What changed: it names the actual settled parameters instead of letting the agent rediscover — or silently default past — them. The rewrite isn't longer because more words are better; it's longer because it replaces four unstated assumptions with four stated facts.

## Prompt Two: So Specific It Leaves Nothing to Reason About

> "Build a Class III `(4,1)` dome, icosahedron, radius 1.0, elongation `1.0,1.0,1.8`, truncate Z at exactly `0.499999`. Just tell me the total strut length."

Every value hard-coded, nothing left for the agent to actually verify. This looks careful, but it forecloses something real: an agent handed this exact recipe has no occasion to re-check whether `0.499999` is *still* a safe cutoff for *this specific* configuration — it's just told to use it.

Here's why that matters concretely, verified rather than assumed: changing the subdivision entirely — not the elongation factor, which this book directly tested and found makes no difference at all to a cutoff's safety, since elongation is a uniform per-axis scale and `truncate()`'s cutoff fraction is computed *relative to* the already-elongated range, so a vertex ring sitting exactly at the fractional midpoint stays at that same fractional midpoint no matter how hard you stretch or squash any axis. What genuinely *does* change a cutoff's safety is switching which subdivision produced the dome in the first place. Chapter 9's own plain Class I sphere at frequency 6 has a real vertex ring exactly at its equator, and `0.499999` there still leaves small flagged artifacts (Chapter 16). Class III `(4,1)`, the dome this book actually built, has no such ring at all — `0.5` exactly works cleanly on it (also Chapter 9). Hard-code the cutoff instead of re-deriving it, and a design change that swaps subdivision class silently keeps an assumption that was only ever true for the *previous* dome.

**Rewritten:**
> "Keep the Class III `(4,1)` subdivision and this dome's own elongation. Re-derive a safe truncation cutoff for it rather than assuming `0.499999` still applies, and tell me whether it actually does."

What changed: it keeps the parts that are genuinely settled (subdivision class, elongation) and leaves open exactly the one thing this book already proved isn't safe to assume across a design change — cutoff safety — so the agent has a real reason to check rather than a number to obey.

## Prompt Three: Right Question, Wrong Tool (Or Three Different Right Ones)

> "Is this dome design good enough to build?"

This single sentence maps onto at least three different real questions, each answered by a different tool, and a plausible-sounding answer to the wrong one is worse than an agent that asks which was meant:

- A **`design_dome`** sanity check — do the vertex/face counts and total strut length fit a stated material or budget constraint.
- A **`get_bill_of_materials`** audit — does the flagged-artifact list (Chapter 16) contain anything real, and do the panel chirality flags (Chapter 14) matter for the chosen material.
- A **`preview_dome`** visual check — does the rendered shape actually look like what was intended, independent of any number in a report.

**Rewritten:** name which of the three is actually being asked — "does the strut count fit my budget," "is the bill of materials clean," or "does it look right" — rather than one word ("good enough") standing in for all three at once.

## Prompt Four: A Two-Toolkit Question, Mistaken for a One-Toolkit One

> "How much material will this dome actually cost me?"

This is the sharpest trap in this chapter, because the prompt sounds perfectly answerable by a single tool, and isn't. `cost_per_unit_area` gives a real number — but it's a *theoretical* one: total panel area times unit price, assuming every panel is cut with zero wasted material anywhere on the sheet. Real sheet stock doesn't work that way, and this book has the real numbers to prove exactly how far apart the two figures actually are.

Take four of the Actual Secret Lair's own real panel shapes — 20 panels, the same subset Chapter 21 nested for real:

```json
{"theoretical_panel_area": 0.79, "real_sheet_area_purchased": 1.80, "ratio": 2.28}
```

**What It Means:** pyLair's own theoretical figure — the honest sum of those 20 panels' real areas — is `0.79` square units. The *actual* material a builder has to buy is `6` whole sheets at `0.6×0.5` each, `1.80` square units total, because sheet stock is only ever sold in whole sheets and nesting never achieves perfect utilization (Chapter 20's own real result on this exact batch: `6` sheets at utilizations ranging from `11%` to `58%`). The real cost is **more than double** the theoretical one — not a rounding difference, a fundamentally different number, because the two figures are answering genuinely different questions.

**Rewritten:**
> "Give me pyLair's theoretical panel-area cost first. Then nest the actual templates with `design_nest` and tell me the real sheet count and utilization. How far apart are the two cost figures?"

What changed: the fix isn't a cleverer single prompt — it's recognizing the question needs both toolkits' tools, in sequence, to answer honestly at all. A prompt that only ever reaches for `cost_per_unit_area` will always underestimate, confidently, and never say so unless asked to check.

## What's Next

Chapter 24 is the retrospective this book has been quietly building toward since its very first gotcha: every point where either toolkit checked its own work against something genuinely independent, gathered into one general habit worth taking well beyond these two projects. Chapter 25 closes the book.
