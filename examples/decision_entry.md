# Example: an architecture decision

A real `A##` from a browser-extension project.

---

## A03. Intercept the player's own request instead of fetching subtitles directly

**Context:** the extension needs YouTube's subtitle data. The obvious route is a fetch
against the player endpoint or the `timedtext` URL directly, which is what most
extensions in this space do.

**Alternatives:**

1. **Direct fetch of `timedtext`.** The simplest option. Does not work: YouTube requires
   a fresh PoToken and single-use request parameters that burn after first use. Obtaining
   them outside the player is not possible without reversing a mechanism that MV3 does
   not permit anyway.
2. **Parsing rendered subtitles from the DOM.** YouTube renders captions into
   `.ytp-caption-segment`. Not usable: only the currently visible phrase exists in the
   DOM, there are no word-level timings, and there is no full text.
3. **Intercepting the player's own request.** Patch `window.fetch` and
   `XMLHttpRequest.prototype.open` in the MAIN world. When the player itself requests
   `timedtext`, capture the response and parse it.

**Decision:** option 3. The patch is installed in the MAIN world through an injected
script; all fetch/XHR traffic is filtered by URL and the response parsed into our own
`SubtitleLine[]`.

**Consequences:**

- ✓ Works with every subtitle type — auto-generated, manual, multi-language.
- ✓ Delivers all timings, including word-level, which the karaoke mode needs.
- ✓ No PoToken problem at all: the player signs its own requests.
- ✗ Hard dependency on YouTube's internals. If they change the request format, the
  extension breaks — this is the single largest fragility in the project.
- ✗ Sourcemaps must be off, or the patch never installs. See [[G07]].
- ✗ Only the first `timedtext` request of a player session carries a fresh PoToken;
  everything after it arrives with stale parameters, so a retry path is required.

---

## What makes this entry good

**The alternatives carry their rejection reasons.** This is the field that earns its
keep: when someone — a person or an agent — later proposes "why not just fetch
`timedtext`?", the answer already exists and nobody re-derives it.

**The decision names the mechanism and where it lives.** Patch fetch and XHR in the MAIN
world, filter by URL, parse the response. Enough to find the code; not a retelling of it.

**Consequences run both ways, and the bad ones link out.** The dependency on YouTube's
internals is stated as the project's largest fragility, and it belongs in `status.md`
under Fragile points as well — as a link, not a copy.

**It is citable.** A commit reading "fix the retry path, last bullet of A03" is
immediately legible.

**It was opened only once the investigation had settled.** While three approaches were
still live, this was not a decision — it was an open question, and an open question
belongs in an `E##`.
