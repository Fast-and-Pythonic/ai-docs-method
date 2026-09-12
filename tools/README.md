# tools

## `lint_docs.py`

Checks what can be checked about a document set. Backs the hard rules in
[RULES.md](../RULES.md); the full list of checks is there, with the reason each exists.

```bash
python tools/lint_docs.py                                  # uses lint_docs.toml
python tools/lint_docs.py --docs ai_docs --profile research
python tools/lint_docs.py --docs /path/to/other/ai_docs    # audit another project
```

Exit code 0 means clean; warnings are allowed. Exit code 1 means at least one error.

If the configured document set does not exist yet, the linter says so and exits 0 — that
is the normal state of a project on its first day, and of any repository that installed
the pre-commit hook before writing anything. A path passed explicitly with `--docs` is
held to a stricter standard and fails, because there a missing directory is a typo. The
distinction matters: a hook that blocks a commit for having nothing to check teaches
people to pass `--no-verify`, and that disables it for good.

Requires Python 3.11+ for `tomllib`. On an older interpreter it still runs, using the
built-in defaults plus command-line flags, and says so.

**Configuration** is [lint_docs.toml](lint_docs.toml), beside the script. It exists to
teach the linter your layout and the metric names your project uses; every value has a
default.

**Documents not in English.** The checks that look for a field — `Prediction`,
`Status`, `Acceptance criterion` — match a literal label. Set them under `[labels]` in
the config if your documents are written in another language. Leaving the defaults does
not produce errors; it produces silence, which looks exactly like passing. The same goes
for `numbers.metric_names`: a metric the linter does not know is a number it will not ask
for a source for.

**A split register.** When a register has outgrown one file (RULES.md, "Scaling"), keep
the index in the register file, move the bodies into a directory and name it in
`register_bodies`. Group the index under headings that link to each area's file —
`## Build — [subsystems/build.md](subsystems/build.md)` — and check 17 holds every index
line to the file its entry is in. A prefix may be longer than one letter (`EG`), and the
`[registers]` table replaces the defaults rather than extending them, so a document set
with its own prefixes lists only those.

**Another document set.** `--config path/to/lint_docs.toml` points the linter at a
config kept beside the documents rather than beside the script. A relative `root` in a
config is resolved against the config file, so the command works from any directory.

**Adding a check.** The bar is that it backs a hard rule or catches rot that has already
happened. A check nobody's documentation has ever failed is a check that will fire on a
false positive first and be disabled second.

## `new_experiment.py`

Opens an `E##` entry: allocates the number, writes the index line, and **refuses to
proceed without a prediction**. Research profile.

```bash
python tools/new_experiment.py --task T-2 \
  --title "Skip the load on fully overwritten targets" \
  --hypothesis "The tiler can drop the load for targets the frame rewrites entirely." \
  --predict "[[corpus:scene-a]]: frame time p50 down 5% or more"
```

This tool is the mechanism behind hard rule H7. Nothing can verify after the fact that a
prediction was written before its run, so the enforcement has to happen at the moment of
creation — which means the entry must be cheaper to create with the tool than by hand.
That is the whole design goal. An entry written by hand afterwards must carry the `retro`
marker.

## `hooks/pre-commit`

Runs the linter before every commit. Install once:

```bash
git config core.hooksPath tools/hooks
```

Finding a problem before you write the commit message is cheaper than after. If the
project is not under version control, say so in `_meta.md` and record which hard rules
are consequently demoted to advice — see [DEVIATIONS.md](../DEVIATIONS.md).
