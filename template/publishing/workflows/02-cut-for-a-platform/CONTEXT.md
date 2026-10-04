# CONTEXT.md — publishing/workflows/02-cut-for-a-platform/

The procedure for rendering and verifying every deliverable of a piece: its full-length
deliverables, encoded from the master, and each approved cut of its cut-down plan, trimmed,
reframed and encoded in one pass, with its captions burned in where they already exist. Every
render goes through `python3 toolkit/media.py`, is verified against its preset, and is seen by the
author. When every deliverable passes, the piece moves from produced to cut. An audiobook reaches
that gate in its own mastering workflow in `production/workflows/`, where the project makes
audiobooks, never here.

## Directory Tree

```text
publishing/workflows/02-cut-for-a-platform/
├── CONTEXT.md        ← this file: when to use it, what it produces
├── CLAUDE.md         ← how to run it; guardrails
├── STEPS.md          ← the ordered procedure
└── CHECKLIST.md      ← tick as you go; model-tagged
```

## When to use this

- A piece's brief dates M4 and its deliverables have not been rendered.
- The cut-down plan has `approved` cuts that are not yet `rendered`.
- A render failed its verification, or a preset, an override or a caption file changed, and a
  deliverable must be made again.

Reach for a **different** procedure when the task is choosing the cuts
(`publishing/workflows/01-plan-the-cut-downs/`), making the captions
(`publishing/workflows/03-caption-a-piece/`), or making the master itself
(`production/workflows/03-assemble-the-master/`).

## What it produces, and where

- **Renders** in `publishing/src/renders/`, one per deliverable,
  `<piece>[--cNN].<platform>-<format>[.burned].<ext>`, each verified and seen by the author.
- **The plan's Status** moved to `rendered`, then `checked`, cut by cut.
- **The gate** in the brief: `status: cut` and M5 dated in `verified`; M6 too where every
  deliverable's captions were burned in this pass and passed their check.

## The failure this procedure exists to prevent

A deliverable that looks right on the editing screen and fails on the platform: the wrong size, a
cut a second over its slot, the sound at the wrong level, the file's index at the end, captions
under the platform's buttons. Every one of them is caught by verifying each output against its
preset before anyone calls it done, and a render that fails is remade from its sources, never
patched by hand or posted anyway.

## Cross-references

- `publishing/docs/reference/cut-downs.md` — framing, safe zones and lengths.
- `publishing/docs/reference/platform-specs.md` — reading a preset, its `verify` keys and overrides.
- `.claude/skills/cut-for-platform/SKILL.md` — every render, through the toolkit.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` — the commands, their exit codes and their
  rules.
