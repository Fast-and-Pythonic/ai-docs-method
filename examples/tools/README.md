# Evidence tools — the rules, not the code

[MEASUREMENT.md](../../MEASUREMENT.md) states rules that **no markdown linter can
enforce**. They have to live in the tools that produce the evidence, at the moment a
verdict is being formed.

This page describes what those tools must refuse to do. The reference implementations
come from a project measuring performance on live hardware; they are tied to that
project's report schema and are GPL-licensed, so they are described here rather than
copied in. What transfers is the list of refusals, and that is the part worth stealing.

## A comparison tool

Decides whether a difference counts. It must:

1. **Refuse a verdict when the sweep ran in one direction only.** A back-to-back A/B is
   biased by order — whichever ran first was measured on a cooler device, and it wins.
   Run both directions, score within pairs, record the real order in the report.
2. **Refuse when a report carries no observed spread.** A single run has nothing to vary
   against, and three times zero certifies anything.
3. **Derive the threshold from the runs being compared**, not from a number written down
   once. In the source project the threshold was a constant, 1.3%, derived from one lucky
   session whose spread was 0.42%. The same configuration on the same build the same day
   also produced 0.84%. A fixed threshold from the luckier session certifies noise as a
   result.

The third point is the one people argue with, so it is worth restating: nothing about the
threshold may be settled before the runs exist, and nothing about it may be chosen after
seeing the delta. Computing it from the spreads satisfies both.

## A curation tool

Turns one raw report into a baseline. It must:

1. **Build a baseline from exactly one session.** The first canonical baseline in the
   source project blended two — its frame time and spread came from one run, its
   subsystem counters from another whose spread was twice as large. The file the
   documentation called the source of truth was reporting a spread that did not belong to
   half its contents.
2. **Commit the raw report beside the curated one**, so the numbers can be re-derived
   rather than trusted.
3. **Disambiguate field names during curation** — a percentage must not be readable as a
   duration. Before the tool existed, this renaming was a person retyping numbers between
   two schemas, which is exactly where the blending in point 1 came from.

## If you are in regime B

A deterministic pipeline has no spread, so none of the above applies and copying it would
be cargo cult. What you need instead is a comparison step that refuses a verdict unless at
least two indicators agree, at least one of which does not depend on your reference data.
See [MEASUREMENT.md §5](../../MEASUREMENT.md).
