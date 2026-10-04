@./CONTEXT.md

# CLAUDE.md — production/workflows/07-clear-the-rights/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Make sure every permission a piece relies on exists, covers this use and is on file, before the
piece is scheduled.

## How to work here

- **Routing:** no skill; this is a confirmation-and-record procedure. Guide
  `production/docs/reference/rights-and-consent.md`; register
  `production/src/rights-register.md`. `storyboard` opens rows earlier and `prepare-post` checks
  the result later.
- **Model:** **Opus** for deciding whether a permission covers a use, and for every refusal; the
  mechanical tier for gathering rows and recording answers the author has given
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: list what the
  piece uses → match each item to its row → check the evidence → request what is missing →
  record each answer → resolve what cannot be cleared → hand back.
- **Definition of done:** every item the piece uses has a row naming the piece, and each row is
  `cleared` with its evidence, or the item has been cut or replaced with the author.

## Guardrails

- **The author requests; Claude records.** Draft a request if asked, but never send one, and
  never record a permission as `cleared` without the permission in hand.
- **A permission covers a use, not a file.** Check the platform, the territory, the duration and
  the medium (a print licence is not an audio one) against how the piece will be published.
- **A refusal is final for that piece.** Cut, replace or re-shoot with the author; never publish
  around it.
- **Consent before a likeness or a voice.** A cloned voice, the owner's own included, needs its
  recorded consent; a recognisable person needs a release.
- **Never fabricate** a permission, a holder or a date; a gap is flagged `AUTHOR TO CONFIRM`.
- **Never delete a row.** A refused or expired item keeps its row, with the date and the reason.

## Output & naming

- **Produces:** rows in `production/src/rights-register.md`, IDs `RR0001` onwards.
- **Also writes:** nothing else; a cut or replacement is made through the procedure that owns
  that file.
- **Does not touch:** the evidence documents themselves, which stay where the author files them.
