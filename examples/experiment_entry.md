# Example: a refuted experiment

A real `E##` from a text-analysis project, in the shape that makes a negative result
worth keeping. Regime B — a deterministic pipeline scored against an unreliable
reference.

---

## E02. Adding colloquial vocabulary will raise the correlation

**Status:** refuted (retro) | **Task:** [[T-1]] | **Opened:** 2026-08-01 |
**Closed:** 2026-08-01

**Hypothesis.** The reference dictionary is built from written sources, so spoken
registers are under-covered. Subtitles are mostly speech. If a large share of the tokens
we fail to score are ordinary colloquial words, extending the dictionary with a
conversational source should lift the correlation against the reference levels.

**Prediction.** Spearman's ρ up by at least 0.03 on `[[corpus:movies-48]]`; the share of
out-of-dictionary tokens down by a third.

**Method.** Same parser, same corpus, dictionary rebuilt with the second source merged
in. Exactly one component of the configuration changed.

**Result.**
- ρ 0.584 → 0.555 → `baseline/movies-48/7c1d92-e02.json`
- out-of-dictionary share 0.31 → 0.19 → same report
- within-group spread of the reference bands: improved → same report
- noise floor on a single series: improved → same report

**Verdict.** Refuted as stated, and instructive. The dictionary did get better — three
indicators say so, including two that do not depend on the reference list — but the
headline correlation **fell**. The reference bands themselves are noisy, and the added
words moved items away from the positions the reference assigns them. Optimising ρ
directly would have meant learning the reference's errors.

**Traces.** "Do not tune against ρ alone — [[E02]]" recorded in `plan/backlog.md`.

---

## What makes this entry good

**It is a failure, and it was kept.** This is the whole point of the register. The
hypothesis was reasonable, the work was done, the answer was no. Deleted, it would be
re-proposed within the month — the reasoning that produced it is genuinely appealing.

**The prediction is numeric and directional.** "ρ up by at least 0.03" can be
contradicted. "The dictionary should get better" cannot, and an unfalsifiable prediction
turns the whole exercise into theatre.

**The `retro` marker is set.** This entry was written after the run, with the prediction
reconstructed. That is honest and it is also a limitation: the entry preserves the result
and the verdict but proves nothing about the quality of the prediction. If some
predictions are written after the fact and it is not visible which, none of them can be
trusted.

**Every number is a headline line with a link.** No tables in the document; four figures,
four links, one report. The question "how did ρ move over the last five changes?" is
answered by reading the reports, not by trusting prose.

**The verdict is more useful than the status.** "Refuted" is the label; the value is in
the explanation of *why* the metric and the goal disagreed. That is the finding, and it
is what the trace line in the task protects.

**The trace exists.** The line in `plan/backlog.md` is what stops the next session from
optimising ρ directly. An archive nobody opens at the moment of temptation is not a
defence.
