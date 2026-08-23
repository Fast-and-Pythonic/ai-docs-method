# Example: the situational guide in `start.md`

The highest-value section of an entry point, from a project of middling complexity.

---

```markdown
## What to read when

- **First time here** → overview → conventions → gotchas
- **Working on the widget / subtitle rendering** → [[subsystems/widget]] + [[A02]] (Shadow DOM)
- **Working on subtitle interception** → [[subsystems/intercept]] + [[A03]] + [[G07]] (sourcemaps)
- **Changes to the popup or settings** → [[subsystems/popup]]
- **Build / packaging for the store** → conventions §build + [[G07]]
- **Debugging odd behaviour on the host site** → gotchas index in full; especially
  [[G02]] (PoToken) and [[G05]] (SPA navigation)
- **Before a refactor** → architecture.md + status.md (Fragile points)
- **Before adding a setting** → [[subsystems/popup]] + the Settings schema in `types.ts`
```

---

## What makes this guide good

**Every line is a real situation.** Not "architecture / implementation" but "build and
packaging for the store" — something someone is actually about to do. If you cannot
imagine saying the line out loud at the start of a session, it does not belong here.

**It points at anchors, not just files.** "[[A02]] (Shadow DOM)" costs one entry to read;
"architecture.md" costs the whole file. Naming the anchor is what makes layered loading
work in practice rather than in principle.

**It connects gotchas to the work that triggers them.** The reader about to touch
interception is handed `[[G07]]` by the guide. Without that line they would have to read
the whole gotchas register and notice it themselves — which, at 500 lines, means they
will not.

**It covers the real scenarios and stops.** UI, interception, settings, build, debugging,
refactoring, extension. Seven or eight lines. A guide that tries to be exhaustive stops
being scannable, and a guide that is not scannable is not read.

## What not to put in it

- ❌ Anything already obvious: "when changing code → conventions.md".
- ❌ A line per file, for completeness. The **map** lists files; the **guide** lists
  situations. They are different sections and they answer different questions.
- ❌ Categories nobody works in: "when working with variables", "when naming files".
  Those are `conventions.md`, and they are not situations.
