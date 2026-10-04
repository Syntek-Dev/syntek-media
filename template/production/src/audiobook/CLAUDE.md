@./CONTEXT.md

# CLAUDE.md — production/src/audiobook/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep one record per audiobook, its plan and its M2, of every chapter's route, takes, master and
check, so each channel receives what it accepts and nothing is voiced or paid for twice.

## How to work here

- **Routing:** skill `narrate-audiobook`; workflows `production/workflows/05-narrate-an-audiobook/`
  and `production/workflows/06-master-an-audiobook/`; guide
  `production/docs/reference/audiobook-narration.md`.
- **Model:** **Opus** for choosing a route, judging a take and approving a master with the
  author; the mechanical tier for chunking, generating, mastering and checking
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** write the register and the credits with the author → choose the route per
  channel → the author approves the plan (M2) → voice or record each chapter → master → check →
  package.
- **Definition of done:** every chapter row is `checked` or `packaged` (or names its export on
  the `external` route), and every recording and every approved master is archived; a chunk take
  is archived only where the author wants it kept.

## Guardrails

- **The route is chosen per channel, with the author.** ACX and Audible take human narration
  unless the author is authorised otherwise; a channel that takes only ElevenLabs' own package is
  the `external` route, made outside this template.
- **Never generate unasked**, and never for a channel on the `external` route.
- **Chapter text never enters a tracked file.** It is read from its source by
  `python3 toolkit/media.py audiobook text` into the git-ignored generated folder. The credits are
  the one text this folder holds: written here with the author, never copied from the book.
- **Nothing is voiced before M2**: the register approved, every chapter's source `final` unless
  the author says otherwise.
- **Disclosure always.** A synthetic narrator is named as one on every channel.
- **Never overwrite a chapter row, a take or a master** without confirming with the author.

## Output & naming

- **Written by skills (with the author):** `<piece>.md`, by `narrate-audiobook`, one sentence per
  line:

```markdown
---
piece: ""                # equals the piece folder's name
approved: ""             # DD/MM/YYYY once the author approves the plan: the piece's M2
route: ""                # human | ai | external (the main route; a chapter may differ)
channels: []             # store names: acx, google_play, spotify_authors, inaudio
voice_use: narration     # a Use row of brand/src/voice/voice.md
model_id: ""             # as recorded there; empty for a human narrator
output_format: ""        # as recorded there (mp3_44100_192, pcm_44100, …); empty if human
---

| Ch | Title | Source | Route | Takes | Master | Duration | Check | Status |
|---|---|---|---|---|---|---|---|---|
```

- **Channels** are written as the store part of each `[audiobook.<store>]` key of
  `toolkit/data/platforms.toml` (`spotify_authors`, never `spotify-authors`); `audiobook text` and
  `audiobook master` refuse any other name.
- **Rows:** `ch00` (opening credits) first, one row per chapter `ch01` onwards in reading order,
  `ch99` (closing credits) last. Source is the chapter's file, or 'provided' with the path the
  author gives; for `ch00` and `ch99` it is the credits' own file, `<piece>.ch00.md` or
  `<piece>.ch99.md` in this folder, the credits' spoken words one sentence per line.
- **Status** takes `planned · generated · recorded · mastered · checked · packaged`; on the
  `external` route, Master names the export and where it is kept, and Check reads `external`.
- **Generated (never hand-edit):** chunks `<piece>.chNN.pNN.txt`, each chapter's chunk sidecar
  `<piece>.chNN.chunks.toml` (the chunks in order, each with its `pause_after` seconds, which
  `audiobook master` reads) and takes `<piece>.chNN.pNN.tN.mp3` in
  `production/src/audiobook/generated/`; mastered chapters `<piece>.chNN.mp3` in
  `production/src/audiobook/renders/`.
