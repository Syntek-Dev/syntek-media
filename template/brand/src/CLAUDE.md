@./CONTEXT.md

# CLAUDE.md — brand/src/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → the target subfolder's pair.

## Purpose (one line)

Record, once each, the tokens, layouts, exports, voice and platform choices the brand relies on,
in files the toolkit and the skills can read without asking again.

## How to work here

- **Routing:** each file or folder has one writer and one procedure.

| File or folder | Written by | Procedure |
|---|---|---|
| `design-system/` (`tokens.css`, `design-system/fonts/`, `design-system/previews/`) | the author, with Claude | `brand/workflows/01-set-up-the-brand-kit/`; kept in step with Claude Design by `brand/workflows/02-sync-with-claude-design/` |
| `design-register.md`, `exports/` | the author, with Claude | `brand/workflows/03-record-a-design-export/` |
| `voice/voice.md` | the author, with Claude; `voiceover` adds a narrator the first time it needs one | `brand/workflows/05-write-the-spoken-voice/` |
| `platforms/` | the author, with Claude | `brand/workflows/04-set-up-a-platform/` |

- **Model:** **Opus** for every brand decision and every check a reader or listener will notice;
  the mechanical tier only for running the checks and adding a row the author has already
  decided (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Read the file you are about to change, and its guide in `brand/docs/reference/`.
  2. Change it with the author, one decision at a time, removing each flag once its decision is
     made.
  3. Run the check its guide names and report the result, then hand back the open questions as
     `AUTHOR TO CONFIRM` flags.
- **Definition of done:** the fact exists in exactly one file, nothing it says contradicts
  another brand file or syntek-author's written brand, where present, unreported, and the checks
  its guide names pass.

## Guardrails

- **One fact, one home.** A colour lives in `tokens.css`, a voice ID in `voice.md`, a handle in
  its profile, a Claude Design link in the register. A second copy drifts.
- **Never invent on the author's behalf.** Options are offered; the author chooses. A gap is
  flagged `<!-- AUTHOR TO CONFIRM: … -->` (`/* … */` in CSS), not filled.
- **One sentence per line** in every Markdown file here, applied when a paragraph is edited,
  never by mass reflow (`.claude/rules/syntek-media/06-global-rules.md` Section 5).
- **Registers are append-only.** A replaced export keeps its row, marked superseded with the
  date, and its file stays beside the revision for reference.
- **A platform's facts are not the brand's choices.** Sizes, limits and labels live in
  `toolkit/data/platforms.toml`; a confirmed correction is an override, never an edit to that
  template-owned file.
- **Never overwrite** a brand file or an export without confirming with the author.

## Output & naming

- **Hand-written:** the files in the table above; kebab-case names; dates DD/MM/YYYY.
- **Seeded:** `design-register.md`, `design-system/tokens.css`, the seven preview cards,
  `voice/voice.md`, `platforms/overrides.toml` and one profile per selected platform: each ships
  once and is never replaced by `copier update`; if deleted, the next update restores it empty.
- **Template-owned:** every pair here, and `exports/large/.gitattributes`.
- **Generated (never hand-edit):** nothing in this folder.
