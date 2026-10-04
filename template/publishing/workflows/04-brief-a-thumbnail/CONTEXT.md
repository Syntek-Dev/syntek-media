# CONTEXT.md — publishing/workflows/04-brief-a-thumbnail/

The procedure for a piece's thumbnails and covers: which deliverables take one, a brief in words
agreed with the author, an HTML layout copied from the brand's own thumbnail component, a PNG for
each deliverable rendered by `uv run toolkit/card.py`, and the checks at the size a viewer will
see it. A cut that needs its own thumbnail gets its own brief and layout (`--cNN`). An approved
thumbnail is one of the things M7 needs; the gate itself is recorded when the post package is
approved, by `publishing/workflows/05-prepare-a-post/`.

## Directory Tree

```text
publishing/workflows/04-brief-a-thumbnail/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- A piece's deliverables include one that takes a thumbnail or cover, and it has none approved.
- The cut-down plan says a cut needs its own thumbnail.
- The author wants a thumbnail remade, for example after a change to the brand's layout.

Reach for a **different** procedure when the task is the brand's thumbnail component itself
(`brand/workflows/01-set-up-the-brand-kit/`), or a title or end card inside the master
(`production/workflows/03-assemble-the-master/`).

## What it produces, and where

- **A brief and a layout** in `publishing/src/thumbnails/`, `<piece>[--cNN].md` and `.html`.
- **A PNG per deliverable** in `publishing/src/renders/`, `<html-stem>.<platform>-<format>.png`.
- **The author's approval,** dated in the brief's `approved`.

## The failure this procedure exists to prevent

A thumbnail that reads well at full size on an editing screen and fails at a fingertip's width:
words too small to read, a title cut off by the profile grid, text under the platform's buttons,
a promise the video does not keep, or a face nobody cleared. Briefing it in words first, then
checking the render at size, against the crop, the safe zone and the rights register, before the
author approves it, prevents every one.

## Cross-references

- `publishing/docs/reference/thumbnails.md` — the brief, the layout, which deliverables take one,
  the checks.
- `brand/docs/reference/the-brand-kit.md` — the tokens and the brand's layout components.
- `.claude/skills/thumbnail-brief/SKILL.md` — this procedure in skill form.
- `publishing/src/thumbnails/CLAUDE.md` — the brief's skeleton.
