# _meta — where the rules for these docs live

The rules for maintaining this documentation are **not copied here**. Two sources of
truth drift apart, which is the disease the method exists to cure.

Standard: <URL of the standard>
<Local method, only if this project deviates: the folder `ai_docs_method/` at the
project root. Where the two disagree, the local method wins. Delete this line if there
is no local method.>

| You need | Read |
|----------|------|
| What is mandatory, triggers, session protocol | `RULES.md` of the standard |
| How to format a `G##` / `A##` / `E##`, links, indexes | `FORMATS.md` |
| How to run and record a measurement | `MEASUREMENT.md` |
| Why this project differs from the standard | `DELTA.md` of the local method |

## Project settings

**Profile:** engineering | research
**Measurement regime** (research only): A (noisy) | B (deterministic)
**Language:** <language of these documents, and when it was decided>. Code identifiers,
file names, JSON keys and log strings stay as they are. Mixing languages inside one
document set is not allowed.

## The three things most often broken here

<A short reminder, not a replacement for RULES.md. Fill in what your project actually
gets wrong — the list is worth rewriting once you know.>

1. <...>
2. <...>
3. <...>

## Checking

```
python tools/lint_docs.py --docs ai_docs --profile <profile>
```

<Run before every commit through a pre-commit hook, or manually as the last step of a
session if the project is not under version control — and if so, say so, and list which
hard rules are demoted to advice as a result.>
