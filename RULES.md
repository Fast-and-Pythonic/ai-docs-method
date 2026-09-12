# RULES — the normative part

What is mandatory, when to write it, and what checks it. Principles are in
[METHODOLOGY.md](METHODOLOGY.md); entry anatomy is in [FORMATS.md](FORMATS.md).

Rows marked **[R]** belong to the [research profile](profiles/research.md) and are
inactive in a project that has not enabled it; rows marked **[E]** belong to the
[engineering profile](profiles/engineering.md). Everything else is core.

---

## 1. Target inventory of `ai_docs/`

| File | Size | Role | |
|------|------|------|--|
| `start.md` | ≤100 | Entry point: map, situational guide, critical facts | |
| `overview.md` | ≤200 | Purpose, **invariants**, stack, structure, phases | |
| `status.md` | **≤80** | State only: Working / Fragile points / Blocked / Deferred. Rewritten in place | |
| `journal.md` | grows | Chronicle, append-only, newest on top, with an index | |
| `gotchas.md` | grows | `G##` plus index | |
| `architecture.md` | grows | `A##` plus index (create on the first `A`) | |
| `_meta.md` | ≤100 | Pointer to the rules; per-project settings | |
| `conventions.md` | ≤300 | Code style, build, test, what must not be auto-formatted | **[E]** |
| `subsystems/*.md` | grows | Compiled knowledge about one part of the tree | **[E]** |
| `references/*.md` | — | External specs, upstream state, third-party formats | **[E]** |
| `experiments.md` | grows | `E##` plus index | **[R]** |
| `corpus.md` | grows | Register of run configurations — the key to every measurement | **[R]** |
| `plan/*.md` | — | Tasks with acceptance criteria, plus `backlog.md` | **[R]** |

**A file is created on its first real entry, not in advance.**

`corpus.md` may live beside the measurement data instead of in `ai_docs/` — set the
path in `tools/lint_docs.toml`. Put it wherever the person taking a measurement will
actually look.

**Task format in `plan/*.md`:** Context → What to do → How to verify → Acceptance
criterion → Owner. A task without a checkable acceptance criterion does not enter the
plan; tasks of the form "figure it out and improve it" are forbidden.

**The Fragile points section of `status.md` is mandatory.** Phrase entries as "looks
like X, is actually Y, breaks this way", not "be careful here".

---

## 2. Update triggers

The table is the process. Without it the structure sits empty.

| What happened | Action | |
|---------------|--------|--|
| Debugging > 30 min with a non-obvious cause | `gotchas.md`: a `G##` — **now**, not "later" | |
| A quirk of an external dependency | `gotchas.md`: a `G##` with the dependency named in the title | |
| A decision settled | `architecture.md`: an `A##` | |
| A fragile point was identified | `status.md`: Fragile points | |
| A feature was deliberately deferred | `status.md`: Deferred, **with the reason** | |
| A feature was finished | `status.md`: Working; `journal.md`: an entry | |
| Knowledge not tied to this project | Mark the entry **Portable: yes** | |
| **A research answer to the user that outlives the session** | Into the matching file; the chat gets the short version with a link | |
| A new file or subsystem appeared | `start.md`: the map | |
| The method itself changed | The project's `DELTA.md`, and `_meta.md` if needed | |
| Code style, build or workflow changed | `conventions.md` | **[E]** |
| A deep dive into one part of the tree | `subsystems/<name>.md` — create or extend | **[E]** |
| Checked against upstream | `references/upstream-watch.md`: date, range reviewed, verdict | **[E]** |
| A hypothesis was formed | `experiments.md`: an `E##`, status `open`, **prediction written BEFORE the run** | **[R]** |
| A measurement was taken | JSON into the baseline tree; headline line in the `E##`; line in `journal.md` | **[R]** |
| A hypothesis was refuted | Verdict in the `E##` (**never deleted**) plus "do not do this — `[[E##]]`" in the task | **[R]** |
| A backlog task finished | `backlog.md`: status; `journal.md`: entry; `status.md`: Working or Fragile | **[R]** |
| The run configuration changed | `corpus.md`: a new configuration; old baselines are not rewritten | **[R]** |

The trigger on *conversation* is easy to overlook and is one of the most productive.
The commonest way to lose knowledge is to work it out in a discussion and never write
it down; a chat log is not a document, and the next session cannot read it.

---

## 3. Session protocol

1. **Always:** `start.md` → `status.md` → the top 3–5 entries of `journal.md`.
2. Your task in full, including every `[[E##]]` and `[[G##]]` it links to.
3. The **indexes** of the growing registers — indexes only; bodies by link.
4. Working on a subsystem → `subsystems/<name>.md`. If the page does not exist, create
   it from what you learn. **[E]**
5. About to measure → [MEASUREMENT.md](MEASUREMENT.md) and `corpus.md` **before** the
   run, not after. **[R]**
6. **Stop and ask the user** when: a doubt touches the invariants in `overview.md`; a
   contract or the architecture would have to change; the method contradicts reality.
7. At the end, work through the triggers above and run `python tools/lint_docs.py`.

Step 6 is not politeness. An invariant is a rule of the project rather than of its
documentation, and no linter can check one; stop-and-ask is its only mechanism, which
is exactly why it is written down as a step rather than assumed.

---

## 4. Hard rules

A violation is an error, not a stylistic blemish. **Every hard rule names its checking
mechanism in the same row.** A rule without one is demoted to advice or removed —
otherwise it is a dead letter within three sessions.

| # | Rule | Mechanism | |
|---|------|-----------|--|
| H1 | Every register entry has an index line, and every index line has an entry | lint: the set of headings equals the set of index IDs | |
| H2 | Every `[[link]]` resolves | lint: an unresolved id-shaped link (`G05`, `E01`, `D5`) is an **error** — it is a typo, not a forward reference. Links to planned pages and configurations are warnings | |
| H3 | `status.md` ≤ 80 lines, `start.md` ≤ 100 | lint: line count | |
| H4 | Numbering has no gaps; a refuted or cancelled entry is never deleted | lint: gap-free numbering. A gap only appears when an entry is removed from the middle; deleting the **last** entry is invisible to lint and is caught by git history instead | |
| H5 | An absolute path written in prose points at something that exists | lint: existence check. Depends on the convention below | |
| H6 | Measure only on a configuration registered in `corpus.md` | lint: every report's `corpus_id` exists in the register and matches its directory | **[R]** |
| H7 | An `E##` whose status is not `open` has a filled-in Prediction | `new_experiment.py` refuses to open an entry without one; lint checks the field is non-empty. Ordering ("before the run") is enforced by using the tool instead of editing by hand — nothing can verify it after the fact, which is why a reconstructed entry must be marked `retro` | **[R]** |
| H8 | A measurement number appears only as a headline line linking to its report | lint: a number with a unit in a line with no path ending in `.json` | **[R]** |
| H9 | A refuted `E##` has a back-link from the task that tempted it | lint: presence of the back-link | **[R]** |

**The convention H5 depends on:** an absolute path written in prose goes in backticks,
and only then may it contain spaces — where an unquoted path with spaces ends is not
decidable. Fenced blocks are skipped; they hold examples.

**Standing apart** are the project's own invariants, stated once in `overview.md` and
repeated nowhere. Those are rules of the project rather than of its documentation, and
their only mechanism is step 6 of the protocol.

---

## 5. What lint checks

**Scope:** `ai_docs/`, the run-configuration register, and the measurement reports.
`[[wikilinks]]` inside your method folder are **not** checked — it holds placeholders
such as `[[E##]]`, which are samples. Its **file** links and absolute paths are checked
all the same: a rotting path is no less broken for living in the method folder. Fenced
blocks and HTML comments are skipped everywhere: both hold examples, and a template
ships its entry skeleton inside one.

**Documents written in another language.** The checks that look for a field —
`Prediction`, `Status`, `Acceptance criterion` — match a literal label, and so does the
list of metric names. Set them under `[labels]` and `[numbers]` in the config if your
documents are not in English. Leaving the defaults does not produce errors; it produces
silence, which is indistinguishable from passing.

Each check backs a hard rule above, or catches rot that has actually happened in the
projects this standard came from.

| # | Check | |
|---|-------|--|
| 1 | Broken `[[links]]` and broken markdown links to files | |
| 2 | Index against headings in every register; gaps in numbering. A register with entries and no index at all is reported once, not once per entry; a register whose entries are numbered under some other scheme (`## 7.` rather than `## G07.`) is a warning, because otherwise every check below passes by finding nothing. Once a register is split by area (§6), the bodies are read from every file under `register_bodies`, and an id with an entry in two files is an error | |
| 3 | Index line and heading that share no words — a warning; a rename probably went halfway | |
| 4 | Line limits for `start.md` and `status.md`; as a warning, for any glob the config names (`subsystems/*.md`) | |
| 5 | Absolute paths in prose, checked for existence | |
| 6 | Repo-relative paths in backticks, checked against a small set of roots | |
| 7 | `journal.md` index against its entries, counted **per date** | |
| 8 | A register grown past 60 entries — a warning that its index has stopped being scannable | |
| 9 | Backlog statuses belong to the legend that file declares | **[R]** |
| 10 | Backlog tasks marked `done` with no `journal.md` entry **headed** with that id | **[R]** |
| 11 | Every measurement report: required fields present, `corpus_id` registered and matching its directory | **[R]** |
| 12 | The `corpus.md` index against the configurations that actually parse as registered | **[R]** |
| 13 | Numbers with no link to a source | **[R]** |
| 14 | An `E##` with status `refuted` and no back-link from a task | **[R]** |
| 15 | An `E##` whose status is not `open` with an empty prediction | **[R]** |
| 16 | An acceptance criterion that hedges (`noticeably`, `measurable`, `faster than`) without a figure — a warning | **[R]** |
| 17 | In a split register whose index is grouped under headings that link to each area's file, every id sits under the section of the file its entry is in. Silent for a flat index. This is what breaks when an entry moves between files and the index is not updated to match | |

Three of these are subtler than they look, and the subtlety is load-bearing. Do not
simplify them away:

- **Check 13 works per line, not per paragraph, and verifies relevance.** A
  paragraph-wide test lets one allow-phrase or one unrelated link excuse every number in
  a bullet list. And presence alone is not enough: the defect this exists for was a
  figure about one configuration backed by a link to a different configuration's
  baseline. If a line names a registered configuration, the report it cites must belong
  to that configuration. The Prediction block of an `E##` is exempt — by H7 it is
  written before any report exists.
- **Check 7 counts per date rather than comparing sets.** Comparing sets makes a missing
  index line invisible whenever two entries share a date.
- **Check 12 treats planned configurations as prose, not headings.** A heading would make
  the measurement harness accept a configuration that has no data and no baseline, so
  the register deliberately writes planned ones as prose and the index distinguishes
  them.

**Rules enforced outside the linter**, in the tools that produce the evidence, because
no amount of markdown checking can catch them: a comparison tool that refuses a verdict
when the sweep ran in one direction only, refuses when a report carries no observed
spread, and derives its threshold from the runs being compared rather than from a number
written down once. See [MEASUREMENT.md](MEASUREMENT.md).

---

## 6. Scaling

When check 8 fires, the register becomes a directory with one file per area under a
single top-level index. **Numbering stays sequential across the whole register**, so no
existing `[[G17]]` breaks.

The linter follows the split: name the directory in `register_bodies` in
`lint_docs.toml`, keep the index in the register file, and group it under headings that
link to each area's file — `## Build — [subsystems/build.md](subsystems/build.md)`.
Checks 2 and 17 then hold the index to the files, which is the part a hand-made split
gets wrong first.

That fixes the actual bottleneck — the size of the chunk you must read to know what
exists. Heavier retrieval machinery (tags, semantic search, an embedding index) waits
for evidence, because building it now is optimising before measuring.

Revisit if: a split register still passes ~80 entries; a session fails to find an entry
that exists and writes a duplicate (record *that* as a `G##` — it is the first real
evidence); cross-cutting queries become routine; or an external document corpus appears.

---

## 7. What we do not write

Beyond the anti-patterns in [METHODOLOGY.md §6](METHODOLOGY.md#6-anti-patterns--what-does-not-go-in-ai_docs):

- **Retelling the code of a dependency or an upstream tree.** What goes into
  `subsystems/` is what cannot be derived from the source in reasonable time: who owns
  what, where the boundaries are, which invariants hold, where it is fragile.
- **Speculation about performance or quality.** Either an `E##` with a prediction and a
  check, or nothing.
- **Caveats instead of structure.** If you are writing "do not take these numbers
  seriously", the numbers are in the wrong place.
