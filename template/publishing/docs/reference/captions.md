---
type: guide
skills: [captions]
model: opus
---

# Captions — the words on screen, timed, readable and true to what was said

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A caption file holds one deliverable's spoken words, timed to its picture, in
SRT (WebVTT is generated from it). The script or approved transcript supplies the words;
`captions check --script` compares them with that source (M6).

## House limits

| Limit | House value |
|---|---|
| Line length | at most 42 characters landscape or square; at most 32 vertical |
| Lines per cue | at most 2 |
| Reading speed | at most 17 characters a second |
| Cue length | 1.0 to 7.0 seconds, with at least 0.08 seconds between cues |

`media.py captions check` enforces these house limits. Break at clauses, never inside a name;
a speaker change opens each line with `- `. Relevant sounds go in lower-case square brackets;
no direction or audio tag reaches a caption, and words follow the script's en_GB spelling.

## Names

In `publishing/src/captions/`: `<piece>.en-GB.srt` is timed to the master, `<piece>--cNN.en-GB.srt`
to one cut and `<piece>.<FID>.en-GB.srt` to a recording; a deliverable with its own line width adds
`.<platform>-<format>` before `.en-GB` (`.linkedin-video-vertical`); a `.vtt` sits beside an `.srt`
that needs one; a published transcript is `<piece>[--cNN].transcript.en-GB.md`.

## Four timing routes

1. **Generated voiceover**: `captions from-segments` reads the segment register in
   `production/src/voiceover/`, splits each approved segment's measured length across its cues by
   character share, and is exact at every segment join, at no cost.
2. **Recorded speech**: `captions align` spreads cues over the speech ffmpeg finds, beat by beat
   (`--anchors`) for a recording, or on a cut's own audio and `--lines`. `captions retime` carries
   recording timing to the master, and master timing to cuts. Check this heuristic by eye.
3. **By hand.** Speech-to-text spends credits: only when the author asks
   (`production/docs/reference/elevenlabs.md`).
4. **Aligned words**, for a generated voice: `voice join`, then `transcribe <piece>` aligns the
   approved segments offline with WhisperX 3.8.6, cross-checking heard words by default.
   Read its printed check; untimed or differing words are findings. `--no-cross-check` records
   that choice. The author alone runs `transcribe fetch` once for the models and tokenizer.
   Accept with `transcribe <piece> -o production/src/timing/<piece>.words.json`; its check sits
   beside it, and both must be committed and unchanged before replacement. `captions from-words
   WORDS --deliverable KEY --offset TC -o SRT` uses each cue's first and last word boundaries;
   short gaps are findings, never trimmed words. Times are estimates: watch a burned preview.

## Burned or sidecar

- A deliverable whose table has `caption_formats = []` takes no sidecar: burn the captions in.
  Otherwise upload the SRT, unless the brief asks for burned captions. A `caption_formats` named
  in the table's `verify` is unconfirmed: check the platform, or burn.
- `media.py cut --captions` burns captions in the cutting pass: M5 and M6 dated together.
- A burn writes an ASS file sized to the output, styled from the `--caption-*` tokens of
  `brand/src/design-system/tokens.css`; it fails when the caption font falls back.
- **On a profile site** (of the website or blog profile, whoever owns it) a video's `.vtt` loads
  by `<track>`, never burned; each piece or cut with speech placed there has its published
  transcript of exactly what the page plays (`captions transcript`, `--lines` for a cut), described
  by hand where the picture says more. A feed episode's `.vtt` is master-timed. Page detail: the
  website, blog and podcast-feed guides, where the project has them.

## How we apply it here

- Caption every deliverable with speech and picture; record M6's `n/a` reason where exempt.
- Fix a mis-transcription only, never improve on what was said; watch a burned preview first.

## Who implements it

- **Workflows:** `publishing/workflows/03-caption-a-piece/`; `production/workflows/08-bring-in-a-recording/` for recordings.
- **Skill:** `captions` times, checks, rewraps, converts and burns them.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Sections 3–4 own M6 and credits;
`.claude/rules/syntek-media/04-toolkit-pipeline.md` owns renders; this guide owns caption delivery.
