@./CONTEXT.md

# CLAUDE.md — brand/workflows/02-sync-with-claude-design/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Keep the kit and its Claude Design project in step, one approved component at a time, without
ever letting either side overwrite the other wholesale.

## How to work here

- **Routing:** no media skill; the author's commands `/design-sync` (route one, with its hint)
  or `/design import` and `/design export` (route two), and `/design-login` once; guide
  `brand/docs/reference/claude-design.md`; checks `python3 toolkit/media.py tokens` and
  `uv run toolkit/card.py check`.
- **Model:** **Opus** for judging what a sync proposes and each component with the author; the
  mechanical tier for the checks, the register row and the commit
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm what
  moves → make the kit clean → choose the route → the author starts the sync, or route two
  through a scratch folder → one component at a time → check after each → record → hand back.
- **Definition of done:** every component the author named has come across and been approved,
  the checks pass, nothing else changed, and the sync is recorded with its route and date.

## Guardrails

- **The author starts every sync.** Claude never types or starts `/design-sync`, and never syncs
  a component the author has not named.
- **Never a wholesale replace.** Never delete a card, rename a required token, move a card's
  line 1 or replace the kit in either direction; if a sync proposes any of these, the author
  cancels it.
- **The first `/design-sync` on a plain HTML kit is unproven.** Its converter is built for React
  kits; watch what it does, and record it, dated, before relying on it again.
- **A layout change reaches every later piece.** Say so before `thumbnail.html` or `card.html`
  comes across; copies already made are not changed.
- **No React and no Node in the kit.** If a route needs either, stop and tell the author.
- **The project's link lives in the design register only,** never in a guide, a procedure or
  `.claude/MEMORY.md`.

## Output & naming

- **Produces:** the components that came across, in `brand/src/design-system/`, under their
  existing names.
- **Also writes:** the project's row in `brand/src/design-register.md`, the first time; a dated
  record in `.claude/MEMORY.md`.
- **Does not touch:** any piece's thumbnail or card, `toolkit/templates/`, or anything outside
  `brand/src/design-system/` except the register.
