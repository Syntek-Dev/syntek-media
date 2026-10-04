@./CONTEXT.md

# CLAUDE.md — brand/workflows/04-set-up-a-platform/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `brand/CONTEXT.md` → `brand/CLAUDE.md`
→ `brand/workflows/CONTEXT.md` → `brand/workflows/CLAUDE.md` → this folder's `CONTEXT.md`
(imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Fill one platform profile with what the brand decides there, and nothing a social media plan or
the platform data already owns.

## How to work here

- **Routing:** no media skill runs this procedure; `prepare-post` reads its result. Guide
  `brand/docs/reference/platform-profiles.md`; the platform's deliverables from
  `python3 toolkit/media.py presets`; the written social plan belongs to the
  social-media-documents skill (syntek-author), where present.
- **Model:** **Opus** for every choice the brand makes on the platform and for judging whether a
  platform's change is confirmed; the mechanical tier for writing values the author has given
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  platform → read the written side's documents → the account, sites or lists → the deliverables used → cadence,
  tone and call to action → hashtag sets → overrides → clear the flags and record → hand back.
- **Definition of done:** the account and the deliverables used are filled; every other section
  is filled or cites the document that sets it; each override carries its why, source and date; no flag is left in
  a section `prepare-post` reads.

## Guardrails

- **Never guess a handle, a domain, a sender or a URL.** They come from the author, exactly as
  the platform or the site shows them. A site's agreement is recorded once, and a slug is frozen
  once a schedule row uses it.
- **The written side's documents win where they set a value.** Never restate a cadence, tone,
  call to action, hashtags or bios that a social media plan, calendar or operating procedure sets;
  cite it.
- **Never write a platform number in a profile.** Cite the key in `toolkit/data/platforms.toml`;
  an unconfirmed value is cited by its key, never by a figure.
- **Never edit `toolkit/data/platforms.toml`.** It is template-owned; a confirmed correction is
  an override, and an unconfirmed one is a re-check
  (`publishing/workflows/07-refresh-the-platform-specs/`).
- **Platforms change through Copier.** A platform the project did not choose is added by
  re-answering the questions, never by hand-making a profile.
- **Never overwrite** a profile or an override without confirming with the author.

## Output & naming

- **Produces:** `brand/src/platforms/<platform>.md`, filled.
- **Also writes:** `[[override]]` tables in `brand/src/platforms/overrides.toml`; dated
  decisions in `.claude/MEMORY.md`.
- **Does not touch:** the platform data, the social media plan or calendar, the schedule, or any
  post.
