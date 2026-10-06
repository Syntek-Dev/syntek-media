@./CONTEXT.md

# CLAUDE.md — production/src/edits/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → `production/src/CONTEXT.md` → `production/src/CLAUDE.md` → this
folder's `CONTEXT.md` (imported above) → this file.

## Purpose (one line)

Record every decision a master is cut from, so it can be rebuilt, changed and checked without
anyone touching a render.

## How to work here

- **Routing:** skill `cut-for-platform`; workflow `production/workflows/03-assemble-the-master/`
  (an episode's audio master has its own procedure where the project makes podcasts); guides
  `production/docs/reference/edit-decision-lists.md` and
  `production/docs/reference/sound-and-loudness.md`.
- **Model:** **Opus** for every cut, hold, fade and level, with the author; the mechanical tier
  for running `assemble` and `probe` (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the storyboard and shot list, or a recorded piece's transcript →
  check every source is logged and verifies → write the clips in timeline order → add overlays
  and sound → `assemble` → probe and measure → watch it through with the author.
- **Definition of done:** `assemble` exits 0, the master probes clean and lands on its loudness
  target, and the author has approved this `version`.

## Guardrails

- **One list per piece.** A new cut of the same piece is a new `version` of the same list, raised
  when the author approves it.
- **Sources by ID.** Footage is cited by its footage ID, never by a path into the mirror.
- **Frame-accurate, always.** The toolkit re-encodes a cut; never ask it to stream-copy one.
- **Never hand-edit a render.** Change the list and assemble again.
- **Never overwrite a list** the author approved without confirming; a rejected change is undone
  in the list, never patched in the master.

## Output & naming

- **Written by skills (with the author):** `<piece>.toml`, by `cut-for-platform`, named for the
  piece's folder:

```toml
[edit]
piece = "<piece>"           # equals the piece folder's name
version = 1                 # raised when the author approves a new cut
size = "1920x1080"          # the master's frame; "" for an audio master (.wav), sound only
audio_rate = 48000
loudness = "social"         # social | podcast | none

[[clip]]                    # one per clip, in timeline order
id = "c01"
source = "F0001"            # a footage ID · an asset path · a card path
in = "00:00:00.000"         # video and audio sources: the range used
out = "00:00:00.000"
seconds = 0.0               # stills, cards and colour clips: how long it holds
colour = ""                 # "#RRGGBB" with no source: a blank clip of `seconds`
frame = "fit"               # fit | crop | pad
x = 0                       # crop offset in source pixels
mute = false                # true drops the clip's own sound
motion = "none"             # stills and cards: none | push-in
transition = "cut"          # how this clip enters: cut | fade
transition_seconds = 0.0

[[overlay]]                 # a card rendered with a transparent background, over the picture
source = "production/src/cards/<piece>.<card>.html"
at = "00:00:00.000"
until = "00:00:00.000"

[[audio]]
source = "vo:<piece>"       # vo:<piece> · a footage ID · an asset path
cue = ""                   # optional e02: the script's SFX or MUSIC event ID
at = "00:00:00.000"         # where it starts on the timeline
in = ""                     # optional source range
out = ""
gain_db = 0.0
fade_in = 0.0               # seconds
fade_out = 0.0
role = "voice"              # voice | music | effect
duck = false                # music: true ducks it under the voice
```

- **Generated (never hand-edit):** nothing here; the master lands in
  `production/src/renders/<piece>/`, and its card PNGs in that folder's `cards`.
