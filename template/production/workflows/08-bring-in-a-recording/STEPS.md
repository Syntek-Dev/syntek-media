---
workflow: 08-bring-in-a-recording
phase: produce
skills: [captions]
model: opus
---

# STEPS.md — bring in a recording

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for making a recorded piece's transcript and its recording-timed captions.
Each step names the skill and guide it uses. **Run in order** (no caption is made from a
transcript the author has not approved) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The `captions`
> skill runs every step.

## 1. Confirm the piece

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Read the piece's brief: `origin: recorded`, and `status` at `briefed` (M1 dated). A recording
with no brief is opened as a piece first, through `scripts/workflows/01-brief-a-piece/`. Confirm
with the author which recording, or recordings, the piece is made from. _Substantive._

## 2. Log the recording

> **Skill:** `captions` · **Guide:** `production/docs/reference/source-media.md`

Run `python3 toolkit/media.py footage add FILE --kind video --location LABEL` (or `--kind audio`),
with `--rights RRNNNN` where it shows other people and their release has a row. It copies the
recording into the mirror and gives it a footage ID; add that ID to the brief's `source_media`.
**A recording already in `production/src/footage/manifest.toml` is not logged again** (the
command refuses a duplicate): skip this step and copy its existing ID into `source_media`, as an
episode cut from a talk another piece recorded does. _Mechanical._

## 3. Extract its audio

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Run `python3 toolkit/media.py extract-audio` on the mirrored recording. It writes a mono WAV to
`production/src/renders/<stem>.wav` (git-ignored, the recording's file stem), which
speech-to-text accepts and `captions align` reads, and prints that path. _Mechanical._

## 4. Choose how the transcript is made

> **Skill:** `captions` · **Guide:** `production/docs/reference/elevenlabs.md`

Ask the author: speech-to-text, which spends credits, or the author's own words (an existing
transcript, the talk's notes as delivered, or typed by hand). **An episode cut from a recording
another piece already transcribed** (its brief's `parent`) takes neither: step 6 copies the
parent's approved beats it keeps, and steps 4 and 5 are skipped and said so. For speech-to-text, load the
`elevenlabs` tools with ToolSearch (searching 'elevenlabs'), run
`python3 toolkit/media.py check --setup` and stop on any ElevenLabs finding, then state the audio
minutes, the number of calls and the estimated credits, and wait for a yes. _Substantive._

## 5. Make the words

> **Skill:** `captions` · **Guide:** `production/docs/reference/elevenlabs.md`

Speech-to-text: call `mcp__elevenlabs__speech_to_text` once, with the extracted WAV's absolute
path as `input_file_path`, `save_transcript_to_file: false` and
`return_transcript_to_client_directly: true`, then add the row to
`production/src/credits-log.md`. On 'outside of allowed directory', stop and give the re-add
command from the guide with a base path that contains `git rev-parse --show-toplevel`. Stop at
the first error and report it. By hand: take the words the author supplies. _Mechanical._

## 6. Write the transcript with its anchors

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Write `scripts/src/pieces/<piece>/transcript.md` in the script's format: frontmatter `piece`,
`source` (the footage ID), `made` (`speech-to-text DD/MM/YYYY` or `by hand`) and `approved`
(empty); one H2 per beat, agreed with the author, each carrying its start on the recording,
`(at HH:MM:SS.mmm)`; spoken lines only, as said, one sentence per line, each opening with its
speaker tag. A word nobody can settle is `[unclear]` and flagged `VERIFY`. For an episode cut
from its parent's recording, copy only the parent's approved beats it keeps, their anchors on the
same recording unchanged, and name the parent in Notes; the copy is approved below as this piece's
own M2, and a later correction to either transcript reopens both. _Substantive._

## 7. Run the companions as reports

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Run the spelling and grammar skills (syntek-author), where present, and the fact-check skill
(syntek-author), where present, as reports; where they are absent, say which is missing. Fix only
a mis-transcription; every finding is the author's to decide, and a claim that proves wrong is
cut, corrected in a caption or description, or kept on the author's word. _Substantive._

## 8. Get the author's approval

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

With every beat anchored, no flag left and every finding decided, the author approves the
transcript. Then, and not before, date `approved` in the transcript, record M2 in the brief's
`verified` with today's date and `M3: 'n/a — recorded'`, and set `status` to `scripted`.
_Substantive._

## 9. Align the recording-timed captions

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Run `python3 toolkit/media.py captions align` with the transcript, the extracted WAV,
`--anchors` and `-o publishing/src/captions/<piece>.<FID>.en-GB.srt` (without `-o` it writes to
the terminal). Report every cue it could
not place or had to stretch; the author checks the timing by eye later, in a burned preview.
_Mechanical._

## 10. Hand back

> **Skill:** `captions` · **Guide:** `production/docs/reference/recorded-pieces.md`

Report the footage ID, the transcript's beats and length, how it was made and what it cost, the
companions' findings and how each was decided, and the captions file. Point to
`production/workflows/03-assemble-the-master/`. _Substantive._
