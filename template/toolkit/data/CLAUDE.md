@./CONTEXT.md

# CLAUDE.md — toolkit/data/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `toolkit/CONTEXT.md` →
`toolkit/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Hold every platform's delivery specs once, dated and sourced, so a deliverable, a caption width or
a hashtag limit is read from data and never remembered.

## How to work here

- **Routing:** `cut-for-platform`, `captions`, `thumbnail-brief` and `prepare-post` read it through
  `python3 toolkit/media.py` and `uv run toolkit/card.py`;
  `publishing/workflows/07-refresh-the-platform-specs/` re-checks it; nothing writes here in the
  normal course of work.
- **Model:** **Opus** for any change to the data or a decision about a platform's rule; the
  mechanical tier for running `media.py presets` (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (a platform's value has changed):**
  1. Read the platform's own page with the author, and confirm the new value and its wording.
  2. Add an `[[override]]` to `brand/src/platforms/overrides.toml`: the key, the value in the
     field's own type, why, the source and the date checked.
  3. Run `python3 toolkit/media.py presets <platform>.<format>` and confirm the override is
     printed and applied.
- **Definition of done:** the file parses, every table keeps `checked` and `source`, and
  `media.py presets` runs clean.

## Guardrails

- **Template-owned.** `copier update` refreshes this file; a correction made here is lost or
  conflicts at the next update, so the brand's corrections are overrides, never edits.
- **Never present a `verify` value as fact.** Cite it by its key (`platform.instagram.hashtags_max`)
  and say it is unconfirmed; never copy its number into a guide, a brief or a post.
- **Never invent a value.** An absent key stays absent until an official source publishes it.
- **Dates are DD/MM/YYYY strings**, never TOML dates, and every `source` is re-checked at least
  every six months.

## Output & naming

- **Template-owned:** `platforms.toml`.
- **Generated:** nothing here; `media.py presets` only reports.
