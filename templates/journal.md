# Journal

Append-only, newest on top. Details live in the registers and in the data; the journal
does not restate them. Each entry is 5–10 lines.

## Index

*(empty)*

<!--
One line per entry, newest on top:

- **2026-08-14** — T-4: pinned the hot thread, measured, kept
- **2026-08-07** — T-2: skipped the redundant load, refuted

Entry skeleton — copy below the separator:

## YYYY-MM-DD — <task id>: what was done, one line

Done: the substance of the change, 1-2 lines
Measured: <metric: before → after> on [[corpus:<id>]] → `<path>.json`
Experiments: [[E##]] refuted
Gotchas: [[G##]] | Decisions: [[A##]]
Status: Working / Fragile — if Fragile, in what way

When a later entry overrides an earlier one, add this at the head of the earlier entry.
Do not edit or delete the entry itself:

> **Superseded YYYY-MM-DD** — current state is in the YYYY-MM-DD entry.
> The reasoning below is kept: it explains why the earlier approach was rejected.

Without the marker the journal cannot be read top-down: some of its statements are
already false, and the reader only finds out on reaching the entry that overturns them.
-->
