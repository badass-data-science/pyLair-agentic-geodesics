# Chapter 23: Prompting pyLair and pyFit Like You Mean It

With the Actual Secret Lair going up ring by ring, our Heroine handed the AI Henchman's terminal to the Junior Henchman for the next project, the Under-the-Ocean Prototype, and asked to see their prompts first. There were four. Each was reasonable, and each would have produced a confident, tidy, wrong-for-the-purpose answer. She held a clinic.

Twenty-two chapters have taught two toolkits, eleven MCP tools between them, and a long list of gotchas. This chapter is practice, not new material: four flawed prompts, rewritten and explained, using designs the book has already built, because the point is practicing on material you already understand.

## Prompt One: Too Vague to Carry Anything Forward

> "Design me a dome."

No radius, no frequency, no class, no purpose. An agent handed this has no reason to look past pyLair's defaults (icosahedron, Class I, frequency `4`, radius `1.0`, what `design_dome` falls back to when nothing is specified), let alone toward the dome this book built.

**Rewritten:**
> "Using the Class III `(m,n)=(4,1)` configuration we settled on, stretched `1.8`× on Z and truncated at `0.499999`, run `design_dome` and confirm the vertex and face counts still match what we found before we export."

What changed: it names the settled parameters instead of letting the agent rediscover them or silently fall back past them. The rewrite isn't longer because more words are better; it's longer because it replaces four unstated assumptions with four stated facts. (It names the parameters rather than "Chapter 6's configuration," too: the agent hasn't read this book.)

## Prompt Two: So Specific It Leaves Nothing to Check

> "Build a Class III `(4,1)` dome, icosahedron, radius 1.0, elongation `1.0,1.0,1.8`, truncate Z at exactly `0.499999`. Just tell me the total strut length."

Every value is fixed and nothing is left for the agent to verify. It looks careful, but it closes off something real: handed this recipe, an agent has no occasion to ask whether `0.499999` is still a sensible cutoff for *this* configuration. It's told to use it.

Why that matters: the elongation isn't what changes a cutoff's safety. Elongation scales every point along an axis uniformly, and `truncate()` computes its cutoff as a fraction of the already-elongated range, so a vertex ring sitting at a given fraction of the height stays at that fraction however hard you stretch. What *does* change a cutoff's safety is the subdivision. Chapter 9's Class I sphere at frequency 6 has a ring exactly on its equator, and even `0.499999` leaves flagged slivers there (Chapter 16). The Class III `(4,1)` dome has no ring at the equator at all; `design_dome` accepts even `0.5` exactly on it. Hard-code the cutoff and a later change of subdivision silently keeps an assumption that was only ever checked on the *previous* dome.

**Rewritten:**
> "Keep the Class III `(4,1)` subdivision and this dome's elongation. Check whether `0.499999` is still a clean cutoff for it, with no flat-chord error and empty artifact lists in the bill of materials, rather than assuming it, and tell me what you find."

What changed: it keeps what's settled (subdivision, elongation) and leaves open the one thing the book has shown isn't safe to carry across a design change, so the agent has a reason to check rather than a number to obey.

## Prompt Three: Right Question, Wrong Tool (or Three Right Ones)

> "Is this dome design good enough to build?"

This one sentence stands for at least three questions, each answered by a different tool, and a plausible answer to the wrong one is worse than an agent that asks which was meant:

- A **`design_dome`** sanity check: do the counts and total strut length fit a stated material budget?
- A **`get_bill_of_materials`** audit: are the artifact lists (Chapter 16) empty, and do any chirality flags (Chapter 14) matter for the chosen material?
- A **`preview_dome`** visual check: does the shape look like what was intended, apart from any number in a report?

And none of the three answers "will it survive the ocean," which no pyLair tool checks (Chapter 11).

**Rewritten:** name which question you're asking ("does the strut total fit my budget," "is the bill of materials clean," "does it look right") rather than letting "good enough" stand for all three.

## Prompt Four: A Two-Toolkit Question Mistaken for a One-Toolkit One

> "How much material will this dome cost me?"

This is the sharpest trap, because the prompt sounds answerable by one tool and isn't. `cost_per_unit_area` gives a number, but a *theoretical* one: total panel area times unit price, as if every panel were cut with no waste. Sheet stock doesn't work that way, and the gap is measurable.

Take four of the Actual Secret Lair's panel shapes, 20 panels in all, the batch Chapter 21 nests, on small `0.6 × 0.5` sheets:

```json
{"theoretical_panel_area": 0.79, "sheets_used": 5,
 "real_sheet_area_purchased": 1.50, "ratio": 1.90}
```

**What It Means:** pyLair's theoretical figure, the sum of those 20 panels' areas, is `0.79` square units. The material a builder has to buy is `5` whole sheets of `0.6 × 0.5`, or `1.50` square units, because sheets are sold whole and nesting never reaches perfect utilization (`design_nest` reports four sheets between 55% and 60% full and a fifth at 34%). The real figure is **nearly double** the theoretical one: not a rounding difference, but an answer to a different question.

**Rewritten:**
> "Give me pyLair's theoretical panel-area cost first. Then nest the templates with `design_nest` on my sheet size and tell me the real sheet count and utilization. How far apart are the two cost figures?"

What changed: the fix isn't a cleverer single prompt. It's recognizing that the question needs both toolkits, in sequence, to be answered honestly. A prompt that only reaches for `cost_per_unit_area` will always underestimate, confidently, and never say so unless asked. (Chapter 20 showed what the gap looks like for the whole Lair.)

## What's Next

The Junior Henchman rewrote all four prompts and added a fifth of their own: "Before you answer, tell me which tool you'd call and why." Our Heroine adopted it on the spot.

Chapter 24 is the retrospective the book has been building toward since its first gotcha: every point where either toolkit checked its own work against something independent, gathered into one habit worth taking beyond these two projects. Chapter 25 closes the book.
