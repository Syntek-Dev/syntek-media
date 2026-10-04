@./CONTEXT.md

# CLAUDE.md — scripts/src/pieces/000-example-piece/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `scripts/CONTEXT.md` →
`scripts/CLAUDE.md` → `scripts/src/CONTEXT.md` → `scripts/src/CLAUDE.md` →
`scripts/src/pieces/CONTEXT.md` → `scripts/src/pieces/CLAUDE.md` → this folder's `CONTEXT.md`
(what the example shows, imported above) → this file.

## Purpose (one line)

Show a piece's files from brief to post package before the author makes a real one, then get out
of the way.

## How to work here

- **Routing:** the example is for reading. To start a real piece, open it with
  `scripts/workflows/01-brief-a-piece/`, which takes the next number from
  `scripts/src/piece-register.md`; the example's 000 is never entered there.
- **Model:** **Opus** for any words a viewer would hear or read; the mechanical tier for running
  the toolkit and for deleting the example (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps to practise on it:**
  1. Read `brief.md` beside `scripts/docs/reference/the-piece-ladder.md`: M1 to M3 are dated,
     and its Notes say why M4 cannot pass.
  2. Time the script with
     `python3 toolkit/media.py script time scripts/src/pieces/000-example-piece/script.md`: it
     reports the `words` and `estimated_seconds` the script's frontmatter records.
  3. Check the captions against the script with
     `python3 toolkit/media.py captions check publishing/src/captions/000-example-piece.en-GB.srt --deliverable <: if 'youtube' in PLATFORMS :>youtube.short<: elif 'tiktok' in PLATFORMS :>tiktok.video<: elif 'instagram' in PLATFORMS :>instagram.reel<: elif 'linkedin' in PLATFORMS :>linkedin.video_vertical<: elif 'facebook' in PLATFORMS :>facebook.reel<: else :>youtube.short<: endif :> --script scripts/src/pieces/000-example-piece/script.md`
     (any 9:16 key from `python3 toolkit/media.py presets` will do): they keep the limits of `publishing/docs/reference/captions.md`
     and carry the same words.
  4. Check the title card with
     `uv run toolkit/card.py check production/src/cards/000-example-piece.title.html`, and
     render the thumbnail layout with
     `uv run toolkit/card.py render publishing/src/thumbnails/000-example-piece.html <: if 'youtube' in PLATFORMS :>--deliverable youtube.short_thumbnail<: elif 'instagram' in PLATFORMS :>--deliverable instagram.reel_cover<: elif 'tiktok' in PLATFORMS :>--deliverable tiktok.video<: elif 'linkedin' in PLATFORMS :>--deliverable linkedin.video_vertical<: elif 'facebook' in PLATFORMS :>--deliverable facebook.reel<: else :>--size 1080x1920<: endif :>`.
  5. Try to build the master with
     `python3 toolkit/media.py assemble production/src/edits/000-example-piece.toml`: it exits 2
     and names F0000, the footage no project has. That is where the walk-through ends.
- **Concrete steps to remove it:** with the author's agreement, delete this folder,
  `production/src/edits/000-example-piece.toml`,
  `production/src/cards/000-example-piece.title.html`,
  `publishing/src/cut-downs/000-example-piece.md`,
  `publishing/src/captions/000-example-piece.en-GB.srt`,
  `publishing/src/thumbnails/000-example-piece.md`,
  `publishing/src/thumbnails/000-example-piece.html` and
  `publishing/src/posts/000-example-piece.md`, with any render made while practising.
- **Definition of done:** the author has seen what each of a piece's files looks like and how
  their numbers agree, and the example is gone once it has served that purpose.

## Guardrails

- **Not a real piece.** Never post it, schedule it, spend a credit on it, or enter it in
  `scripts/src/piece-register.md`, `publishing/src/schedule.md` or
  `publishing/src/publish-log.md`.
- **F0000 and RR0000 are placeholders.** Never log footage as F0000, never open a rights row as
  RR0000, and never point a real piece's files at either.
- **Never 'fix' the stop at M4.** `assemble` exits 2 by design; logging footage to make it pass
  turns the example into a piece nobody briefed.
- **Never let it shape the real first piece.** Its words, pictures and hashtags are invented
  placeholders, not suggestions.
- **Deleting it is the author's call**, and once deleted it stays deleted.
- **Never overwrite** this piece's brief, words, storyboard or shot list without confirming with
  the author.

## Output & naming

- **Hand-written (with the author):** nothing new; this folder only demonstrates the naming in
  `scripts/src/pieces/CLAUDE.md`.
- **Written by skills:** nothing; `script.md` and the boards are written as `write-script` and
  `storyboard` would write them.
- **Elsewhere, under this piece's name:** the seven files listed in this folder's `CONTEXT.md`.
- **Generated (never hand-edit):** any render made while practising, in the git-ignored renders
  folders, deleted with the example.
