@./CONTEXT.md

# CLAUDE.md — publishing/workflows/05-prepare-a-post/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `publishing/CONTEXT.md` →
`publishing/CLAUDE.md` → `publishing/workflows/CONTEXT.md` → `publishing/workflows/CLAUDE.md` →
this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md` open).

## Purpose (one line)

Hand the author a post package for every deliverable that is inside every limit, honest about
what is synthetic and cleared for rights, and schedule it, without ever posting anything.

## How to work here

**Follow `STEPS.md` in order and tick `CHECKLIST.md` as you go.** The model tags in the checklist
are authoritative: `opus` items are judgement; `sonnet` items belong to the mechanical tier.

- **Routing:** skill `prepare-post` (this procedure in skill form; its mode file carries the brand
  kind's register for post copy); the spelling, grammar and fact-check skills (syntek-author),
  where present, for the proofread. Guides: `publishing/docs/reference/posting-and-the-log.md`,
  `publishing/docs/reference/ai-disclosure.md` and the guide for each platform a section names.
  Tools: `python3 toolkit/media.py presets` and `flags`.
- **Model:** **Opus** for every word a viewer reads and every disclosure decision; the mechanical
  tier for counting against keys, filling render names and writing schedule rows
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** confirm the piece is ready → read the calendar or the profiles → check the
  rights → decide the disclosure → write each section → count every limit → proofread and check
  the claims → clear the flags → the author approves → schedule rows → record the gate → hand
  back.
- **Definition of done:** an approved package with a section for every deliverable, every count
  inside its key, the disclosure set by each platform's rule with the description line always,
  every rights row cleared, zero flags, a schedule row per deliverable, and M7 recorded.

Title–thumbnail options use `publishing/docs/reference/scoring-options.md` and
`media.py score plan/run`: one approved paid call, retained provenance and author selection.
Jev scores text concepts; actual images still need visual review.

## Guardrails

- **Never post.** No upload, no API call, no scheduling inside a platform's own tools; the author
  posts.
- **The label follows the platform; the line is always there.** Never set a label 'to be safe',
  and never leave the description line out.
- **Rights first.** A deliverable that uses anything not `cleared` is not scheduled; send it to
  `production/workflows/07-clear-the-rights/`.
- **Limits by key.** Every count names its `platforms.toml` key; a `verify` key relied on is named
  in the hand-back.
- **Never invent** a claim, a quotation, a statistic, a testimonial, an endorsement or a link.
- **The calendar is cited, never rewritten.** Where syntek-author's content calendar is present,
  a change to it belongs to the social-media-documents skill (syntek-author), where present.
- **A placement holds only media's words.** A post's, page's or issue's own words, standfirst,
  link text and date are the written side's: read the written piece, never edit it, and give an
  embed or player snippet only in chat, on request.
- **No placement on a site or list the brand does not own is `ready`** without the dated
  agreement in its profile row.
- **Never overwrite** an approved package or a schedule row without confirming with the author.

## Output & naming

- **Produces:** `publishing/src/posts/<piece>.md`; rows in `publishing/src/schedule.md`.
- **Also writes:** the brief's `status` and `verified`.
- **Does not touch:** the publish log (that is `publishing/workflows/06-record-a-publication/`),
  any render, or the content calendar.
