@./CONTEXT.md

# CLAUDE.md — production/workflows/09-time-the-voice/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md`, with `CHECKLIST.md` open.

## Purpose (one line)

Give a scene the timing of the voice the author approved and the boards they agreed before drawing it.

## How to work here

- **Routing:** skills `voiceover` and `storyboard`; guides `production/docs/reference/voiceover.md`
  and `scripts/docs/reference/storyboards-and-shot-lists.md`; `media.py voice join`, `transcribe`, `lipsync` and `cues`.
- **Model:** **Opus** for the words check, the re-time and every judgement with the author;
  the mechanical tier for commands and recording, as the checklist tags specify.
- **Concrete steps:** read progress → check caches/tools → join approved takes → align and agree words
  → make mouth data → match and re-time boards → record sub-checks and hand back.
- **Definition of done:** accepted tracked timing and a re-timed board agreed by the author,
  with current `M4.words` and `M4.cues`, and stills/preview review left to its own procedure.

## Guardrails

- **No spending or fetch.** Every command is offline; missing caches get the author's setup hint.
- **Read printed evidence.** Never open ignored working timing; each command prints what it found.
- **Accept tracked data only through `-o`.** Existing output must be committed and unchanged;
  refuse dirty, staged or untracked existing copies, never bypass the guard.
- **Timing is not new words.** A re-time keeps approval/M3; changed words or a replaced shot return to boarding.
- **Mouth data is not mouth approval.** The author checks the mouths in stills and a preview at `M4.stills`.
- **Keep earned dates only while their inputs still hold.** Follow the ladder's dependent clearing rules.

## Output & naming

- **Writes:** `<piece>.words.json`, `<piece>.words-check.md` and `<piece>.mouth.json` through `-o`
  in `production/src/timing/`; `<piece>.cues.json` through `-o` in `production/src/scenes/`.
- **Edits with the author:** board Time, Timing notes, version and shot Seconds; the brief's `M4.words`, `M4.cues` and `last_updated`.
- **Generated:** the joined voice and working copies in the piece's ignored production renders folder.
