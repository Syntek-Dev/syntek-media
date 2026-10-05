@./CONTEXT.md

# CLAUDE.md — brand/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md` (imported
above) → this file → the target folder's `CONTEXT.md` and `CLAUDE.md`.

## Purpose (one line)

Keep one record of how the brand looks and sounds, so that every thumbnail, card, caption and
voice is drawn from it and nothing about the brand is invented piece by piece.

## How to work here

- **Routing:** start every job from the matching procedure in `brand/workflows/` (the index is
  `brand/workflows/CLAUDE.md`; the `run-media-workflow` skill resolves `workflows/local/`
  first). Tokens, fonts and layouts → `brand/workflows/01-set-up-the-brand-kit/`; Claude Design →
  `brand/workflows/02-sync-with-claude-design/`; an exported asset →
  `brand/workflows/03-record-a-design-export/`; a platform →
  `brand/workflows/04-set-up-a-platform/`; the spoken voice →
  `brand/workflows/05-write-the-spoken-voice/`; tools, permissions and the ElevenLabs server →
  `brand/workflows/06-check-the-setup/`. Guides: `brand/docs/reference/`,
  overridden by same-named files in `brand/docs/project/`.
- **Model:** **Opus** for every brand decision and every judgement of a proof; the mechanical
  tier for running checks, renames and register rows the author has dictated
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Identify the sublayer and read its `CONTEXT.md` and `CLAUDE.md`.
  2. For anything in `src/`, read the guide that governs it first (indexed in
     `brand/docs/reference/CONTEXT.md`).
  3. Change the brand file with the author, then run the checks its guide names and say what
     they found.
- **Definition of done:** every brand fact a layout, a caption or a voice reads is recorded once,
  in its one file, decided by the author; the checks pass; and any decision still open is flagged
  `AUTHOR TO CONFIRM` rather than guessed.

## Guardrails

- **The author decides every brand fact.** Never pick a colour, a typeface, a narrator or a
  handle on the author's behalf: offer options with a recommendation, and flag the gap until the
  author decides (`.claude/rules/syntek-media/03-production-ethics.md` Section 1).
- **One source for every token.** Layouts read `brand/src/design-system/tokens.css`; never type
  a colour value or a font name into a piece's thumbnail or card.
- **Cite the written brand; never copy it.** Where syntek-author's brand guide and voice files are
  present (its standards/brand/ folder, or the Brand folder its 00-project.md Paths name, and
  standards/style/voice-notes.md), this layer agrees with them and cites them. A disagreement is
  reported to the author with both values, never resolved silently.
- **Credits and consent come first.** Trying a voice spends credits, and a cloned voice needs the
  person's recorded consent (`.claude/rules/syntek-media/03-production-ethics.md` Sections 4
  and 6).
- **Voice IDs, handles and Claude Design links live only in this layer's own files**, never in a
  guide, a procedure, a post or `.claude/MEMORY.md`
  (`.claude/rules/syntek-media/06-global-rules.md` Section 10).
- **Never overwrite** the tokens, a preview card, an exported asset, the voice or a profile
  without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `tokens.css`, the preview cards, `voice.md`, the platform
  profiles, `overrides.toml` and the design register's rows.
- **Written by skills:** a narrator row in `voice.md` the first time `voiceover` needs one.
- **Template-owned:** every pair, and `brand/src/exports/large/.gitattributes`.
- **Generated (never hand-edit):** nothing in this layer; a proof rendered from a preview card
  goes, through `-o`, to the git-ignored `production/src/renders/proofs/<what>-DD-MM-YYYY/`, and
  a voice trial's audio to the git-ignored
  `production/src/voiceover/generated/voice-trials/<name>/`, made by `speak plan --trial <name>`;
  no piece owns either.
- Filenames kebab-case; dates DD/MM/YYYY in prose and DD-MM-YYYY in filenames.
