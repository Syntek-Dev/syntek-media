@./CONTEXT.md

# CLAUDE.md — brand/src/platforms/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/src/CONTEXT.md` → `brand/src/CLAUDE.md` → this folder's `CONTEXT.md` (imported above)
→ this file.

## Purpose (one line)

Record what the brand decides for each platform, apart from what the platform itself decides, so
every post package starts from the brand's own account, deliverables and choices.

## How to work here

- **Routing:** workflow `brand/workflows/04-set-up-a-platform/`; guide
  `brand/docs/reference/platform-profiles.md`; skill `prepare-post` reads the profiles. A field
  of the platform data that has changed is re-checked through
  `publishing/workflows/07-refresh-the-platform-specs/`, then recorded as an override here.
- **Model:** **Opus** for every choice the brand makes on a platform and for judging whether a
  platform's change is confirmed; the mechanical tier for writing a value the author has given
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** check for syntek-author's social media plan, where present → the account,
  from the author → the deliverables used, chosen from `python3 toolkit/media.py presets` →
  cadence, tone, call to action and hashtag sets, only where no plan owns them → an override
  only for a confirmed difference → clear each flag as its decision is made.
- **Definition of done:** the profile's account and deliverables are filled; every other section
  is either filled or cites the social media plan; no flag remains in a section `prepare-post`
  reads; every override carries its why, source and date.

## Guardrails

- **Never guess a handle or a URL.** They come from the author, exactly as the platform shows
  them; until then the flag stays.
- **Never write a platform number in a profile.** Limits are cited by their key in
  `toolkit/data/platforms.toml`; an unconfirmed value is cited by its key, never by a figure.
- **Never edit `toolkit/data/platforms.toml`.** It is template-owned; a confirmed difference is
  an `[[override]]` here, with the platform's own words, where it says them and the date checked.
- **The social media plan wins where it is present.** Never restate its cadence, tone, call to
  action, hashtags or bios in a profile; cite it (`.claude/rules/syntek-media/02-skills.md`
  Section 4).
- **Removing a platform deletes its profile.** Copy out anything the author wants to keep before
  the answers change.
- **Never overwrite** a profile or an override without confirming with the author.

## Output & naming

- **Hand-written (with the author):** `<platform>.md`, one per selected platform, its sections
  fixed; `overrides.toml`, one table per confirmed correction:

```toml
[[override]]
key = "<platform>.<format>.<field>"   # a field of toolkit/data/platforms.toml
value = 0                             # a TOML value of the field's own type
why = ""                              # what the platform now says
source = ""                           # where it says it
checked = ""                          # DD/MM/YYYY
```

- **Generated (never hand-edit):** nothing here.
