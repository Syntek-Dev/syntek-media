@./CONTEXT.md

# CLAUDE.md — production/workflows/04-master-a-podcast-episode/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Make an episode's one audio master, at the podcast target and with its disclosure in the audio,
and have the author approve it whole.

## How to work here

- **Routing:** skill `cut-for-platform`; guides `scripts/docs/reference/podcast-episodes.md`,
  `production/docs/reference/edit-decision-lists.md` and
  `production/docs/reference/sound-and-loudness.md`; commands
  `python3 toolkit/media.py footage verify`, `assemble`, `probe` and `loudness measure`.
- **Model:** **Opus** for every cut, bed and level, and for judging the episode with the author;
  the mechanical tier for running the toolkit and recording the gates
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  episode → record M3 as not applicable → check every source → write the audio list → assemble →
  measure → listen through and record M4 → hand back.
- **Definition of done:** the master assembles from the list as audio only, lands on the podcast
  target, carries its disclosure where a synthetic voice speaks, and the author has heard it
  through and approved it, with M4 dated in the brief.

## Guardrails

- **Never change what a speaker meant.** Trimming a pause or a false start is an edit; cutting a
  sentence so that it says something else is not, and the author decides every such cut.
- **Disclose in the audio.** An episode with a synthetic voice says so in the episode itself, as
  well as in its episode and show descriptions
  (`.claude/rules/syntek-media/03-production-ethics.md` Section 5).
- **The target comes from the data file.** Read it from `[platform.podcast.apple_rss_audio]`; never
  set it by ear.
- **Never hand-edit a render.** A change goes into the list as a new `version`.
- **Never overwrite** an approved list without confirming with the author.

## Output & naming

- **Produces:** `production/src/edits/<piece>.toml` and, git-ignored,
  `production/src/renders/<piece>/<piece>.master.wav`.
- **Also writes:** the brief's `verified` entries for M3 and M4, and its `status`.
- **Does not touch:** the transcript, the script, the footage or any take.
