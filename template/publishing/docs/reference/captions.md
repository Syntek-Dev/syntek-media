---
type: guide
skills: [captions]
model: opus
---

# Captions — the words on screen, timed, readable and true to what was said

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Most short video is watched with the sound off, so for most viewers the captions
are the piece. A caption file holds the spoken words of one deliverable, timed to its picture, in
SRT (WebVTT is generated from it). The words are the script's, or a recorded piece's approved
transcript's, never retyped; only the timing is made here, and `captions check --script` compares
the words with their source, which is how M6 is passed.

## House limits

| Limit | House value |
|---|---|
| Line length | at most 42 characters landscape or square; at most 32 vertical |
| Lines per cue | at most 2 |
| Reading speed | at most 17 characters a second |
| Cue length | 1.0 to 7.0 seconds, with at least 0.08 seconds between cues |

These are house values, not platform rules; `python3 toolkit/media.py captions check` enforces
them. Break at a sentence or clause, never inside a name. A speaker change inside one cue opens
each line with `- `. Non-speech sounds go in square brackets, lower case, only when they matter.
No braced direction or audio tag ever reaches a caption, and words are spelt as the script spells
them, in en_GB.

## Names

In `publishing/src/captions/`: `<piece>.en-GB.srt` is timed to the master,
`<piece>--cNN.en-GB.srt` to one cut and `<piece>.<FID>.en-GB.srt` to a recording. A deliverable
with its own line width adds `.<platform>-<format>` before `.en-GB`, the key's dot and underscores
as hyphens (`.linkedin-video-vertical`); a `.vtt` sits beside an `.srt` that needs one.

## Three timing routes

1. **Generated voiceover**: `captions from-segments` reads the segment register in
   `production/src/voiceover/`, splits each approved segment's measured length across its cues by
   character share, and is exact at every segment join, at no cost.
2. **Recorded speech**, and speech on camera: `captions align` spreads the script's or
   transcript's cues over the speech ffmpeg finds. A whole recording is aligned beat by beat
   (`--anchors`, so drift never crosses a beat); one cut is aligned on its own audio and lines
   (`extract-audio --in --out`, then `--lines`). `captions retime` carries recording timing to the
   master, and master timing to each cut. It is a heuristic: check it by eye in a burned preview.
   `align`, `retime`, `rewrap` and `vtt` write to the terminal unless `-o` names the caption file.
3. **By hand**, when neither fits. Speech-to-text is never a default step: it spends credits, so
   it runs only when the author asks (`production/docs/reference/elevenlabs.md`).

## Burned or sidecar

- A deliverable whose table has `caption_formats = []` takes no sidecar: burn the captions in.
  Otherwise upload the SRT, unless the brief asks for burned captions. A `caption_formats` named
  in the table's `verify` is unconfirmed: check the platform, or burn.
- Captions made before the cut let `media.py cut --captions` burn them in the cutting pass, so M5
  and M6 pass together; both dates are recorded.
- A burn writes an ASS file sized to the output, styled from the `--caption-*` tokens of
  `brand/src/design-system/tokens.css`, its bottom margin the preset's `safe_zone`, or 8% of the
  height (a house value) where none is published. It fails when the caption font falls back.

## How we apply it here

- Every deliverable with speech and picture is captioned; an audiobook, a podcast (unless the
  brief asks for a transcript) and a deliverable without speech are `n/a`, with the reason.
- Fix a mis-transcription only; a caption never improves on what was said. Watch a burned
  preview before M6 is recorded.

## Who implements it

- **Workflows:** `publishing/workflows/03-caption-a-piece/` for every deliverable;
  `production/workflows/08-bring-in-a-recording/` for a recording's own captions.
- **Skill:** `captions` times, checks, rewraps, converts and burns them.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder and M6, and Section
4 owns credits; `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns renders. The
rules own the requirement; this guide owns how captions are timed, written and delivered.
