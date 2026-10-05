@./CONTEXT.md

# CLAUDE.md — publishing/workflows/08-publish-the-podcast-feed/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open)
→ **the show register**.

## Purpose (one line)

Take a feed episode through its part of M7, so the feed Apple Podcasts and Spotify read is
written from one reviewed register, checked against what is live, and uploaded in the right
order at the right time.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `prepare-post` for the register's words, the checks and the hand-back;
  skill `cut-for-platform` for `feed tag`, which changes a render. Guide:
  `publishing/docs/reference/podcast-feed.md`. Tools: `python3 toolkit/media.py feed new`,
  `feed add`, `feed tag`, `feed chapters`, `feed check` and `feed write`.
- **Model:** **Opus** for the show's details, every title, description and chapter title, and the
  hand-back; the mechanical tier for the `feed` commands and the row's status
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the episode → open the show, once → add the episode → its words and
  chapters, approved → tag the file → write the chapters → check, and mark it `ready` → write the
  upload copy → hand back the upload list.
- **Definition of done:** the row is `ready` with its words, chapters and `pub_date` approved; the
  render is tagged; `feed check` exits 0; the upload copy is written; the author holds the upload
  list, the tests and the hand steps.

## Guardrails

- **Identity is for life.** Never type or edit a feed URL or a GUID; `feed new` and `feed add`
  write them once, and `feed new --rekey` corrects them only while nothing is published.
- **Never upload, and never write the tracked feed here.** The author uploads; the tracked
  `publishing/src/podcast/<show>.feed.xml` is written by
  `publishing/workflows/06-record-a-publication/` after the author reports the feed live.
- **The feed goes up last, at `pub_date`.** Every file it names first; never before its time.
- **Never re-encode here.** The audio is M5's and the transcript M6's; a missing one goes back to
  its own procedure.
- **A corrected file gets a new URL;** its GUID never changes.
- **Never overwrite** an approved show or an approved row without confirming with the author.

## Output & naming

- **Produces:** the episode's row in `publishing/src/podcast/<show>.toml` (and the register itself,
  once per show); `publishing/src/renders/<piece>/<piece>.chapters.json`;
  `publishing/src/renders/<show>.feed.xml`.
- **Also changes:** `publishing/src/renders/<piece>/<piece>.podcast-feed-audio.mp3`, tagged in place.
- **Does not touch:** the post package, the schedule or the publish log (they are
  `publishing/workflows/05-prepare-a-post/`'s and `publishing/workflows/06-record-a-publication/`'s),
  or the tracked feed.
