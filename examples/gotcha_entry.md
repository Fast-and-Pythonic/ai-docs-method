# Example: a gotcha entry

A real `G##` from a browser-extension project.

---

## G07. Sourcemaps break MAIN-world injection

**Context:** packaging the extension for the store. Worked in dev, failed in production.

**Symptom:** the `window.fetch` patch never applies in a production build, though dev
works correctly. No errors in DevTools, but the patch does not take: `window._yksPatching`
stays `undefined`.

**Cause:** Vite sets `build.sourcemap: true` by default. Chrome MV3 refuses to execute
scripts carrying a sourcemap comment in the MAIN world — the page's own context. This is
extension-specific behaviour and is not documented explicitly anywhere.

**Fix:** set `build.sourcemap: false` explicitly in `vite.config.ts`. This matters:
neither `'inline'` nor `'hidden'` works either.

**How to spot it:** if interception works in dev and not in production, check this first.
Grep the built files in `dist/` for `sourceMappingURL` — if it is there, this is your
problem.

**Portable:** yes — MV3 extension packaging

---

## What makes this entry good

**The symptom is concrete.** Not "it doesn't work" but "the fetch patch does not apply
in production, and DevTools shows no errors". An agent can recognise the situation from
the outside.

**The cause is a mechanism.** Not "Vite adds a sourcemap" but why that specific fact
breaks this specific thing — Chrome blocks MAIN-world scripts with sourcemaps for
extensions. A mechanism generalises; a symptom does not.

**The fix is exact, and says what does not work.** `'inline'` and `'hidden'` look like
reasonable middle grounds and both fail. Recording the near-misses saves the next reader
from trying them.

**How to spot it gives a searchable signature.** `sourceMappingURL` in `dist/` is
something you can grep for in ten seconds. This field is what turns a war story into a
diagnostic.

**The title is an anchor.** "Sourcemaps break MAIN-world injection" is greppable, is
titled by the symptom rather than by the topic ("Notes on the Vite config" would help
nobody), and can be cited from a commit message as `G07`.

**Portable is set.** This is not knowledge about karaoke subtitles; it is knowledge
about packaging MV3 extensions, and it will be worth promoting to a shared layer.
