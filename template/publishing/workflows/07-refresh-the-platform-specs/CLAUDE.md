@./CONTEXT.md

# CLAUDE.md — publishing/workflows/07-refresh-the-platform-specs/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Re-read every stale platform table at its source and record each confirmed difference as an
override, so no render or package trusts a limit that has changed.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** no media skill; this is a review, done by hand against the platforms' own pages,
  with the research skill (syntek-author), where present, for the reading. Guide:
  `publishing/docs/reference/platform-specs.md`. Tools: `python3 toolkit/media.py presets` and
  web fetches of each table's `source`.
- **Model:** **Opus** for reading a platform's page and judging whether it changes a value; the
  mechanical tier for listing stale tables, writing confirmed rows and checking they apply
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** list the stale tables → narrow them to what the project uses → re-read each
  source → propose overrides → record what the author confirms → check each applies → retire
  redundant overrides → re-read the disclosure rules → hand back.
- **Definition of done:** every stale table the project relies on has been re-read and dated;
  every confirmed difference is an override the toolkit prints; every unconfirmed value is still
  in `verify` and named in the hand-back.

## Guardrails

- **Never edit `toolkit/data/platforms.toml`.** It is template-owned: `copier update` replaces
  it, and an edit becomes a conflict. Corrections are overrides.
- **The platform's own page is the source.** A press report, a forum or a third-party guide may
  point to a change; it never confirms one. What only they say stays `VERIFY`.
- **Never fabricate a limit.** A value no source states is left absent or in `verify`, never
  filled from memory or from another platform.
- **The author confirms every override,** and every retirement of one.
- **A changed disclosure rule is never edited into the reference guide.** It goes into a
  same-named project guide, on the author's word.

## Output & naming

- **Produces:** `[[override]]` rows in `brand/src/platforms/overrides.toml`.
- **Also writes:** a same-named project guide in `publishing/docs/project/`, where a disclosure
  rule has changed and the author agrees.
- **Does not touch:** `toolkit/data/platforms.toml`, any reference guide, or any render.
