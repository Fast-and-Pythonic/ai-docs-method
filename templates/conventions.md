# Conventions

How code is written *here* — the part a linter config does not already say, and the part
an agent will otherwise get subtly wrong. Engineering profile.

## Naming

- **Functions / methods:** <style, example>
- **Variables:** <style, example>
- **Constants:** <style, example>
- **Types / classes:** <style, example>
- **Files / modules:** <style, example>

## Formatting

- **Indentation:** <state it explicitly if unusual — three spaces will be "corrected" to
  four by every tool that touches the file>
- **Line length:** <limit, if any>
- **Alignment:** <if group alignment is used>

## Comments

- **Language:** <which natural language>
- **When to write one:** <rule>
- **When not to:** <rule>

## Build and test

```bash
<dev build>
<release build>
<tests>
<lint / type-check>
```

**What counts as broken:**
- <condition>

## Workflow

- **Before a commit:** <what to check>
- **Files to touch carefully:** <path> — <why>
- **Files never edited by hand:** <generated, lock files, vendored trees>
- **Never auto-format:** <path> — <why>

<!-- The last three lines are usually the most valuable in this file: each prevents a
specific expensive mistake, and none of them is visible in the source. -->
