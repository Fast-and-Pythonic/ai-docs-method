# Corpus — run configurations

The key to every measurement. Two numbers may be compared only when their configurations
differ in exactly one component. Research profile.

**Registered** configurations are `## <id>` headings. **Planned** ones are prose only —
a heading would make the harness accept a configuration that has no data and no
baseline.

## Registered

- **<id>** — <one line: what it measures>
- **<id>** — <one line>

## Planned

<Prose. Not headings. What is missing before each can be registered.>

---

## <id>

**Components:** <the exact set that must match — e.g. input corpus + reference data +
code version; or workload + device + build>
**Why this one:** <what it is representative of, and what it deliberately excludes>
**Baseline:** `<path>.json`
**Established:** YYYY-MM-DD
**Caveats:** <the misreading this configuration invites, stated where the reader will
hit it>
