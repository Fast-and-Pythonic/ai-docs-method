# Skeleton: one run configuration

Copy into `corpus.md` under a `## <id>` heading. Registered configurations are headings;
planned ones stay prose.

```markdown
## <id>

**Components:** <the exact set of things that must match for two runs to be comparable>
**Why this one:** <what it represents, and what it deliberately leaves out>
**Baseline:** `<path to the curated baseline>.json`
**Established:** YYYY-MM-DD
**Caveats:** <the most expensive misreading available here>
```

## What makes an id good

Short, stable, and descriptive of the *situation* rather than of the change that
prompted it: `gtasa-ingame`, `movies-48`, `evp-2026-08-07`. It appears in file paths, in
`[[corpus:<id>]]` links and inside every report, so renaming one is expensive.

## What Components must actually list

Everything that, if changed, invalidates a comparison. This is the field the rule exists
for: in one run a parser and a reference dictionary changed together, the report was a
single before/after table, and the two contributions can no longer be separated. Listing
the components forces the question "what am I changing?" **before** the run.
