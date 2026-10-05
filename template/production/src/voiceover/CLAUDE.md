@./CONTEXT.md

# CLAUDE.md — production/src/voiceover/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Keep one record per piece of every voiced segment, so a voice track and its captions can be
rebuilt from approved takes without a credit spent twice.

## How to work here

- **Routing:** skill `voiceover`; workflow `production/workflows/02-make-a-voiceover/`; guides
  `production/docs/reference/voiceover.md` and `production/docs/reference/elevenlabs.md`.
- **Model:** **Opus** for splitting the script and judging takes with the author; the mechanical
  tier for building request text, counting characters and logging takes
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** split the approved script into segments → write the register → build each
  request → state the cost and wait → generate one call at a time, `take add` after each → the
  author listens → approve, reject or regenerate → archive each approved take → `voice join`.
- **Definition of done:** every segment has a take the author approved, each approved take is
  archived and named in `archived`, and every call has its credits-log row.

## Guardrails

- **Never generate unasked**, and never before the characters, calls and credits are stated and
  the author has said yes.
- **One segment per spoken sentence or short beat.** Never one per caption cue, unless the author
  asks for a kinetic-caption short (`per_cue = true`).
- **`text` is what is said; `request` is what is sent.** Directions and pronunciations change the
  request, never the text, which is also the caption text.
- **Segment IDs are permanent.** A regenerated segment is a new take of the same ID, never a
  renumbering.
- **A re-roll resets approval and archive.** `take add` sets `status` to `generated` and clears
  `archived`; the new take is unheard and unarchived.
- **Plan offline.** `speak plan` prints requests, characters and calls, creating only the takes
  folder; copy its requests and lengths to this register. It never changes `text` or the script.
- **Never overwrite a take or an approved row** without confirming with the author.

## Output & naming

- **Written by skills and the toolkit:** `<piece>.toml`, by `voiceover`; `take` and `file` by
  `take add`:

```toml
[voiceover]
piece = "<piece>"            # equals the piece folder's name
voice_use = "voiceover"      # a Use row of brand/src/voice/voice.md
model_id = ""                # as mcp__elevenlabs__list_models gave it, and voice.md records it
output_format = ""           # the recorded format; a pcm_* take is named .pcm
per_cue = false              # true only for a kinetic-caption short, on the author's word

[[segment]]
id = "s01"                   # permanent
script_lines = "1.1"         # beat.line, or a range: one sentence or one beat
text = ""                    # as spoken, braces removed: the caption text
request = ""                 # as sent: pronunciations substituted, directions as audio tags
take = 1                     # written by take add
file = ""                    # written by take add, relative to this folder: generated/<piece>/takes/<name>
characters = 0               # of the request, as billed
pause_after = 0.0            # seconds of silence before the next segment
status = "generated"         # generated · approved · rejected
archived = ""                # the footage ID once the approved take is archived
```

- **Generated (never hand-edit):** the takes in `production/src/voiceover/generated/<piece>/takes/`,
  named `<piece>.sNN.tN.mp3` (`.pcm` for a raw format); a row written before the per-piece layout
  keeps its flat `generated/<name>`, which every reader opens as the row names it. A piece's
  folder carries no pair, and a tracked file never sits in it.
