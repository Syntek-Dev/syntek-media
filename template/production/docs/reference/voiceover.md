---
type: guide
skills: [voiceover]
model: opus
---

# Voiceover — one segment per spoken sentence or beat, one register per piece

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A voiceover is made from the approved script in segments: one ElevenLabs call per
spoken sentence, or per short beat, and never one per caption cue. Each segment is a row in the
piece's register, `production/src/voiceover/<piece>.toml`, which records the words, the request
as sent, the take, the file and its status. `assemble` joins the approved segments into the voice
track, and `captions from-segments` times the captions from them, exactly, at no cost.

## Why a sentence, not a cue

A sentence split across two calls gets two final intonations, and the server passes no
neighbouring text to smooth the join. So a segment is a whole sentence, or a beat short enough to
stay under the recorded model's character limit. `captions from-segments` in the toolkit then
chunks each approved segment's text to the deliverable's caption limits and spreads the
segment's measured duration across its cues by character share: every join between segments is
exact, and every cue inside one is close. `per_cue = true` makes one segment per cue
instead, only for a kinetic-caption short, on the author's word.

## The register

| Field | Holds |
|---|---|
| `piece`, `voice_use`, `model_id`, `output_format`, `per_cue` | the `[voiceover]` table: the piece, the narrator's Use row in `brand/src/voice/voice.md`, the model and format recorded there, and the cue rule |
| `id` | `s01` onwards: permanent, never renumbered |
| `script_lines` | the script's `beat.line`, or a range: one sentence or one beat |
| `text` | the words as spoken, braces removed: this is also the caption text |
| `request` | the text as sent: pronunciations substituted, directions as audio tags where the model takes them |
| `take`, `file` | written by `take add`; `file` is relative to `production/src/voiceover/`: `generated/<piece>/takes/<name>`, or the flat `generated/<name>` of a row an earlier release wrote, and every reader opens the path the row names |
| `characters` | the request's length, as billed |
| `pause_after` | seconds of silence before the next segment |
| `status` | `generated · approved · rejected` |
| `archived` | the footage ID once the approved take is archived |

## From script to request

- Only spoken lines are voiced: cue lines (`TEXT:`, `SFX:`, `MUSIC:`, `NOTE:`) never are.
- A braced direction (`{softly}`) becomes an audio tag only where the recorded model takes tags,
  and is otherwise dropped from the request. It never reaches `text`.
- `{pause S}` becomes the previous segment's `pause_after`, never words in a request.
- Pronunciations come from `brand/src/voice/voice.md`; the script holds no IPA.

## How we apply it here

- The narrator, model and settings are those recorded for the voiceover use; changing any of them
  is the author's decision, dated.
- Takes are named `<piece>.sNN.tN.mp3` (`.pcm` for a raw format) in
  `production/src/voiceover/generated/<piece>/takes/`; a regenerated segment is a new take,
  numbered after its highest take in either layout, never an overwrite. A scratch track sits in
  the piece's folder itself, never among its takes.
- The author listens to every take; only `approved` takes reach a master, and each is archived.
- A piece with a generated voice says so in its brief's `synthetic_voice`, and is disclosed at
  publish.

## Who implements it

- **Workflow:** `production/workflows/02-make-a-voiceover/`.
- **Skill:** `voiceover` splits, costs, generates, logs and archives, following the call
  discipline of `production/docs/reference/elevenlabs.md`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 4 owns never spending unasked, and
its Section 5 owns disclosure. This guide owns how a voiceover is split, recorded and approved.
