@./CONTEXT.md

# CLAUDE.md — scripts/workflows/03-storyboard-a-piece/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/workflows/CONTEXT.md` → `scripts/workflows/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Board one approved script with the author and leave a storyboard and a shot list that the edit
decision list can be written from without guessing.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative.

- **Routing:** skill `storyboard`, whose mode file adds this brand kind's domain steps; it is this
  procedure in skill form. Guides: `scripts/docs/reference/storyboards-and-shot-lists.md`,
  `scripts/docs/reference/the-piece-ladder.md` and the guide for the piece's kind listed in
  `scripts/docs/reference/CONTEXT.md`. Safe zones and aspects from
  `python3 toolkit/media.py presets`; rights rows in `production/src/rights-register.md`.
- **Model:** **Opus** for every picture, framing and rights judgement; the mechanical tier for
  numbering rows, writing the rights rows the author agreed and ticking boxes
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the piece → confirm no clobber → read the script, the brief and the
  guides → board every spoken line → frame every vertical deliverable → give every shot a source
  → open the rights rows → read back and record M3 → hand on.
- **Definition of done:** every spoken line of the approved script sits in a board; every board
  has a shot with a source; every vertical deliverable has its framing; every licensed or
  identifiable item has a `needed` rights row; the author has approved the storyboard and the
  brief records M3.

## Guardrails

- **Board the approved script, never a draft.** A storyboard of words that later change is a
  storyboard to redo.
- **A source for every shot.** `to shoot` is a source; a blank is not. A shot nobody can find or
  make is reported, never papered over.
- **Rights at the first sketch.** Music, stock, people, private places, likenesses, quotations,
  fonts and generated art each open a `needed` row as they are boarded; a voice or a likeness is
  used only with recorded consent (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 6).
- **Generated pictures match the brief.** A board that needs AI-generated visuals the brief does
  not declare goes back to the author before it is kept, because the disclosure plan changes.
- **Not for a recorded piece.** Its M3 is `n/a — recorded`; its edit is cut from its transcript.
- **Never overwrite** an approved storyboard or shot list. Revise in place with the author's
  confirmation, knowing that a replaced shot clears M3 and every later gate.

## Output & naming

- **Produces:** `scripts/src/pieces/<piece>/storyboard.md` and `shot-list.md`.
- **Also writes:** `needed` rows in `production/src/rights-register.md`; the brief's `rights`,
  `status`, `verified` and `last_updated`.
- **Does not touch:** the script, the footage manifest, the cards, the edit decision list or any
  render.
