@./CONTEXT.md

# CLAUDE.md — production/workflows/08-bring-in-a-recording/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/workflows/CONTEXT.md` → `production/workflows/CLAUDE.md`
→ this folder's `CONTEXT.md` (imported above) → this file → `STEPS.md` (with `CHECKLIST.md`
open).

## Purpose (one line)

Give a recorded piece a transcript the author has approved, anchored to the recording beat by
beat, so its master, captions and cut-downs all start from what was actually said.

## How to work here

- **Routing:** skill `captions`; guides `production/docs/reference/recorded-pieces.md` and
  `production/docs/reference/elevenlabs.md`; tool `mcp__elevenlabs__speech_to_text` from the
  user-scope server `elevenlabs`, loaded with ToolSearch, only when the author asks; commands
  `python3 toolkit/media.py footage add`, `extract-audio`, `check --setup` and `captions align`.
- **Model:** **Opus** for the transcript, its beats and every judgement about what was said; the
  mechanical tier for logging, extracting, aligning and recording the gates
  (`.claude/rules/syntek-media/05-model-allocation.md`). The checklist tags are authoritative.
- **Concrete steps:** follow `STEPS.md` in order and tick `CHECKLIST.md` as you go: confirm the
  piece → log the recording → extract its audio → choose how the transcript is made → make the
  words → write the transcript with its anchors → run the companions as reports → get the
  author's approval → align the recording-timed captions → hand back.
- **Definition of done:** the recording is logged and named in the brief's `source_media`; the
  transcript is approved, every beat anchored and no flag left in it; M2 is dated and M3 recorded
  as `n/a — recorded`; the recording-timed captions exist.

## Guardrails

- **Speech-to-text only when asked.** It spends credits: state the audio minutes, the calls and
  the credits, and wait for a yes. Its words are a draft for the author, never the record.
- **The base path must contain the project.** On 'outside of allowed directory', give the re-add
  command from `production/docs/reference/elevenlabs.md` with a base path that contains
  `git rev-parse --show-toplevel`; never copy the recording somewhere else to get round it.
- **The words are what was said.** Fix only a mis-transcription; a word nobody can settle is
  `[unclear]` and flagged `VERIFY`.
- **Copy, never move, the recording.** `footage add` copies it into the mirror; the original
  stays where it was.
- **Never overwrite** an approved transcript without confirming with the author.

## Output & naming

- **Produces:** `scripts/src/pieces/<piece>/transcript.md` and
  `publishing/src/captions/<piece>.<FID>.en-GB.srt`.
- **Also writes:** the recording's footage row; a credits-log row when speech-to-text ran; the
  brief's `source_media`, its `verified` entries for M2 and M3, and its `status`.
- **Does not touch:** the recording itself, the edit decision list, or any cut.
