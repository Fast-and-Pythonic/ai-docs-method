# DEVIATIONS — how to break these rules on purpose

A standard that cannot be departed from is either wrong for most projects or quietly
ignored. This file describes the only sanctioned way to depart from it: **write the
departure down, with its justification, in a file the next session will read.**

Departing "because it suits us better" is not allowed. Once that is permitted, the
standard stops meaning anything and the documents drift back into whatever each session
felt like doing.

---

## 1. The local method folder

A project that departs from the standard keeps its own method folder at the project root:

```
<project>/
├── ai_docs/
│   └── _meta.md          ← thin pointer to the folder below
└── ai_docs_method/
    ├── README.md         ← what is local and why a local method was needed at all
    └── DELTA.md          ← the list of departures, each justified
```

Anything not stated locally comes from this standard. Where something **is** stated
locally, **the local method wins** — and `ai_docs/_meta.md` says so in one line, so a
session never has to guess which document is in charge.

Do not copy rules from the standard into the local folder. Two sources of truth drift
apart, which is the disease the whole method was written to cure. The local folder holds
deltas and nothing else.

If a project has no departures, it needs no method folder: `ai_docs/_meta.md` points
straight at the standard.

---

## 2. The format of a departure

```markdown
## D1. One-line title of the departure

**Standard:** what it says, with the section reference.

**Locally:** what we do instead. Concrete — a file, a format, a limit.

**Why:** the evidence. What went wrong, on which project, at what size. A
justification that could not be falsified is not a justification.

**Side effect:** what else this fixes or costs. Optional, but it is often the most
useful field — it is where you notice that a departure is really two.
```

Number them `D1`, `D2`, … The numbers are link targets: `[[D5]]` resolves here, and lint
checks it.

**The Why field carries the whole thing.** "Our project is different" is not evidence.
"Our `status.md` reached 349 lines against a 150-line limit, 68% of it a decision log
that had nowhere else to go" is evidence — it names the file, the size and the mechanism,
and anyone can check whether it is true.

Write departures against the *evidence you already have*, not against difficulties you
anticipate. A departure invented in advance is a guess, and guesses accumulate faster
than they are removed.

---

## 3. Legitimate exceptions

Separate from departures, and just as important: places where the project's `ai_docs/`
**breaks the standard deliberately** and must be left alone.

```markdown
## Legitimate exceptions

Places where this project's `ai_docs/` breaks the standard on purpose — recorded so a
future session does not "tidy them up".

- **"No task lists in `ai_docs/`".** Ours are `plan/*.md` — a plan with acceptance
  criteria, not a todo list, and the primary carrier of intent. It stays.
- **Decision log inside `status.md`.** Replaced by `journal.md` — see D2.
```

Without this section, a diligent session will eventually find the violation, fix it,
and delete something load-bearing. This has happened. The section costs four lines and
prevents it.

---

## 4. Promotion back into the standard

A departure is a hypothesis about the standard. When the same mechanism has proven
itself on a **second** project, it stops being a local delta and becomes a candidate for
the standard itself.

That is how most of what is now in [RULES.md](RULES.md) arrived: the experiment
register, the `status`/`journal` split, register indexes, checked links, "measurements
are data", portable entries, and the rule that a rule without a mechanism is only advice
— all were `D##` entries in one project's `DELTA.md` before they were rules here.

Two consequences worth planning for:

- **Attribution, not dependency.** When a local method borrows from a sibling project,
  say so in its README — and keep the normative files self-contained, so nothing breaks
  if that project moves or disappears.
- **Two implementations of one idea is a temporary state.** When a mechanism is promoted,
  the local deltas that carried it collapse to genuine differences of substance. If they
  do not collapse, the promotion was premature.

---

## 5. Demotion: when a rule cannot be enforced here

A hard rule whose mechanism does not exist **in this project** must be demoted to advice
explicitly, in writing, rather than silently left in place.

The commonest cause is a project not under version control, where every rule that leans
on commit history or a pre-commit hook loses its mechanism. The honest response is a
short list:

```markdown
### Demoted to advice (this project is not under version control)

- **Lint before commit.** Run manually as the last step of a session.
- **Deleting the last entry of a register.** Caught by git history elsewhere; caught by
  nothing here. A gap in the middle is still a lint error.

If the project is put under version control, all of these return to hard rules unchanged.
```

Pretending a rule is enforced when it is not is worse than admitting it is a suggestion:
it makes the document set look maintained, which is precisely the state this standard
exists to avoid.
