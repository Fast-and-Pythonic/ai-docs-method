# Example: a status snapshot

`status.md` from a browser-extension project of middling maturity, in the shape this
standard asks for: **state only**, rewritten in place, under 80 lines.

---

```markdown
# Status

**Updated:** 2026-05-04

## Working

- Karaoke mode: word-level highlighting on auto-generated subtitles (en, ru verified)
- Normal mode: line-by-line display, toggled from the popup
- SPA navigation: moving between videos without reloading the extension is stable
- Multi-language: subtitle language switches from the popup, applied live
- Settings persistence: `chrome.storage.sync`, synced across devices

## Fragile points

- `background.ts: patchFetch()` — looks like an ordinary fetch wrapper, is actually a
  MAIN-world patch that must be tested against a production build. Breaks silently if
  sourcemaps come back on ([[G07]]) or if the patch stacks ([[G04]]).
- `youtube.ts: fetchCaptionTracks()` — looks like a stable API call, is actually reading
  YouTube's internal `playerResponse`. Breaks whenever they change the shape. See [[A03]].
- `widget.ts: rAF loop` — looks frame-accurate, is actually synced to `video.currentTime`.
  Drifts on slow devices.
- `parser.ts: parseJson3()` — the format is undocumented; the parser handles observed
  cases only. Breaks on an unobserved case, silently, by rendering nothing.

## Blocked

- Store submission: waiting on the reviewer's response to the host-permissions question.

## Deferred

- **YouTube Shorts** — different player markup (`#shorts-player`), needs its own code
  path. Deferred until the Shorts player settles.
- **Bilingual subtitles** — two tracks at once. Technically possible; needs the widget
  reworked. Not a priority.
- **Persistent injector** — the patch is currently re-injected on every navigation and
  could be done once. Deferred: the current version is more stable.
```

---

## What makes this good

**The date is at the top.** An agent immediately knows how much to trust it. On an
active project, a snapshot more than two or three weeks old is a reason to verify before
acting.

**Working lists specific features and their conditions.** "auto-generated subtitles, en
and ru verified" is a claim someone can check. "Everything works" is not.

**Fragile points use the required phrasing.** Every entry says what it *looks* like, what
it *is*, and how it breaks — and links the register entry with the detail. "Be careful
here" would carry none of that.

**Deferred entries carry their reason.** Not "do Shorts" but "deferred until the Shorts
player settles". Six months later that is still legible, and still checkable.

**Nothing is duplicated from elsewhere.** No stack, no directory tree — that is
`overview.md`. No numbers — those live in their reports.

## What is deliberately absent

**No decision log.** In an earlier version of this standard, `status.md` also carried a
dated log of decisions. In practice the log crowded out the snapshot: on one project it
grew to 68% of a 349-line file, against a limit of 150, with individual entries running
to 34 lines because one line genuinely cannot hold a decision, its measurements and its
rejected alternatives. The two are different volatility classes — a rewritten snapshot
and a growing chronicle — so the chronicle now lives in `journal.md` and the decisions
that settled become `A##` entries.

**No task list.** Tasks belong in a tracker. `Deferred` is not a backlog: it is a record
of things put down on purpose, with the reason.

**No reassurance.** "The project is in good shape" is not a status.
