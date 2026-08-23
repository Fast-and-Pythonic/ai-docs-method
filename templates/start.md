# <project> — documentation entry point

<One sentence: what this project is and what it is for.>

**State:** <one line — the single most important thing about where the project stands
right now.>

<Hard limit: 100 lines. If it outgrows that, something is being duplicated here that
belongs elsewhere.>

## Documentation map

| File | What is inside |
|------|----------------|
| [overview.md](overview.md) | Purpose, **invariants**, stack, structure |
| [status.md](status.md) | What works, **fragile points**, what is deferred |
| [journal.md](journal.md) | Chronicle, newest on top |
| [gotchas.md](gotchas.md) | `G##` — traps that have already cost time |
| [architecture.md](architecture.md) | `A##` — settled decisions |
| [conventions.md](conventions.md) | Code style, build, what not to touch |
| [_meta.md](_meta.md) | Where the rules for these documents live |

## What to read when

<Situations, not categories. Point at anchors, not just files.>

- **Start of a session** → this file, then [status.md](status.md), then the top entries
  of [journal.md](journal.md).
- **Working on <area>** → `subsystems/<name>.md` + [[A##]], [[G##]]
- **<A specific recurring debugging situation>** → [[G##]], [[G##]] — both are about
  <the common mechanism>.
- **Before a refactor** → [architecture.md](architecture.md) + status.md (Fragile points)
- **Writing into these documents** → `RULES.md` of the standard

## Three facts to know up front

<The three things that explain most of the non-obvious decisions in this codebase. Not
a summary — the things a newcomer gets wrong.>

1. **<Fact.>** <Why it matters, and which entries carry the detail.>
2. **<Fact.>**
3. **<Fact.>**
