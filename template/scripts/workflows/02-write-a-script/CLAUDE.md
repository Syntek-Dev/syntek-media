@./CONTEXT.md

# CLAUDE.md — scripts/workflows/02-write-a-script/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/workflows/CONTEXT.md` → `scripts/workflows/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Write one piece's script for the ear, from its brief and checked material, and leave it approved,
timed and ready to be voiced, filmed and boarded.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative.

- **Routing:** skill `write-script`, whose mode file adds this brand kind's domain steps; it is
  this procedure in skill form. The fact-check skill (syntek-author), where present, before
  writing; the spelling, grammar, comprehension, flow and fact-check skills (syntek-author), where
  present, as reports on the result. Guides: `scripts/docs/reference/writing-for-the-ear.md`,
  `scripts/docs/reference/the-piece-ladder.md` and the guide for the piece's kind listed in
  `scripts/docs/reference/CONTEXT.md`. Timing: `python3 toolkit/media.py script time`.
- **Model:** **Opus** for every line of the script and every judgement; the mechanical tier only
  for running the timing and the flag check, writing the agreed approval and ticking boxes
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the piece → confirm no clobber → read the brief, the voice and the
  guides → check the claims → write → time → companion reports → revise on the author's notes →
  approval and M2 → hand on.
- **Definition of done:** `script.md` sits in the piece's folder, approved and dated by the
  author, inside its target time and every deliverable's limit, with zero flags; every claim in
  it was checked or cut; the brief records M2.

## Guardrails

- **Check before you write** (step 4). A line written around an unchecked claim tends to survive
  the discovery that the claim was wrong.
- **Never fabricate.** No invented statistic, quotation, testimonial, endorsement, platform rule
  or limit. Flag it `VERIFY` or leave it out, and say which in the hand-back.
- **Written for the ear, timed before it is heard.** Never fit a long script by raising the
  words-a-minute rate; cut or reshape it with the author.
- **Reports, not rewrites.** Companion findings are offered, and the author decides each one.
  Improve-section and adapt-section (syntek-author), where present, run only as
  report-then-agreed-edit, with no ledger entry.
- **The written work is read, never edited.** A script adapted from a chapter or a document
  changes nothing in syntek-author's layers.
- **Nothing is generated here.** No voice, no take and no credit is spent in this procedure.
- **Never overwrite** an approved script. Revise it in place with the author's confirmation,
  knowing that revising it clears M2 and every later gate.

## Output & naming

- **Produces:** `scripts/src/pieces/<piece>/script.md`.
- **Also writes:** the brief's `status`, `verified` and `last_updated`.
- **Does not touch:** the brief's plan (purpose, deliverables, disclosure), a transcript, the
  storyboard, the voice file, or anything in the production or publishing layers.
