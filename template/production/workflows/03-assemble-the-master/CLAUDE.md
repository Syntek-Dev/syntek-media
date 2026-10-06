@./CONTEXT.md

# CLAUDE.md — production/workflows/03-assemble-the-master/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Make the one master every deliverable of a piece is cut from, from tracked decisions and verified
sources, and have the author approve it whole.

## How to work here

- **Routing:** skill `cut-for-platform`; guides `production/docs/reference/edit-decision-lists.md`,
  `production/docs/reference/sound-and-loudness.md` and, for a recorded piece,
  `production/docs/reference/recorded-pieces.md`; commands `python3 toolkit/media.py assemble`,
  `probe`, `loudness measure`, `footage verify` and `captions retime`; cards rendered through
  `uv run toolkit/card.py`.
- **Model:** **Opus** for every cut, hold, fade and level, and for judging the master with the
  author; the mechanical tier for copying cards, running the toolkit and recording the gate
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  piece is ready → check every source → copy the cards → write the edit decision list → assemble
  → probe and measure → carry a recorded piece's captions to the master → watch it through and
  record M4 → hand back.
- **Definition of done:** the master assembles from the list, probes clean, lands on its loudness
  target, and has been watched or heard through and approved by the author, with M4 dated in the
  brief.

## Guardrails

- **Record the non-scene progress.** Before M4, write all four `M4.*` as `n/a` with a footage
  or no-picture reason, filling missing entries for older boards. A scene piece uses
  production/workflows/10-animate-a-scene/.

- **Sources first.** Every footage ID verifies, every asset is in `production/src/assets/`, and
  every voiceover segment the list uses is approved and archived, before `assemble` runs.
- **Copy the brand's card component; never edit it here.** A layout change belongs to the brand
  layer; a card here changes only its words.
- **Frame-accurate, always.** The toolkit re-encodes every cut; never ask it to stream-copy one.
- **Never hand-edit a render.** A change goes into the list as a new `version`, and the master is
  assembled again.
- **The gate is the author's.** M4 is recorded only after the author has watched or heard the
  whole master and said yes.
- **Never overwrite** an approved list or a card a master already uses without confirming with the
  author.

## Output & naming

- **Produces:** `production/src/edits/<piece>.toml`, `production/src/cards/<piece>.<card>.html`
  and, git-ignored, `production/src/renders/<piece>/<piece>.master.mp4` (or `.wav`) with its
  card PNGs in `production/src/renders/<piece>/cards/`.
- **Also writes:** for a recorded piece, `publishing/src/captions/<piece>.en-GB.srt`; the brief's
  `verified` entry for M4 and its `status`.
- **Does not touch:** the script, the transcript, the storyboard, the footage or any take.
