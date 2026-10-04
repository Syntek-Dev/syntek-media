---
type: guide
skills: [captions, cut-for-platform]
model: opus
---

# Recorded pieces — a recording in, a transcript as its script, captions to every cut

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A talk, an interview or a conversation that already exists as a recording is a
piece like any other, with `origin: recorded` in its brief and the recording's footage IDs in
`source_media`. Its approved transcript stands in for a script wherever one is read: by
`captions check --script`, by `captions align` and by `repurpose`. It is never storyboarded; its
master is cut straight from the recording.

## On the ladder

For a recorded piece, M2 is the transcript approved, and M3 is recorded in `verified` as
`n/a — recorded`, so the piece moves on from `scripted` without a storyboard; M4 onwards are the
same as for any piece. `scripts/docs/reference/the-piece-ladder.md` says what each gate checks.

## The transcript and its anchors

`transcript.md` sits in the piece folder, in the script's format, with frontmatter `piece`,
`source` (the footage ID), `made` (`speech-to-text DD/MM/YYYY` or `by hand`) and `approved`.
Each beat heading carries the beat's start on the recording, as in
`## 2. The question (at 00:04:12.300)`; lines are spoken words only, as said, with no braces,
and a word nobody can settle is written `[unclear]` and flagged `VERIFY`. Speech-to-text runs only when the author asks,
because it spends credits; otherwise the author supplies the words. Only a mis-transcription is
ever corrected: the words are what was said.

## From the recording to every cut

1. `captions align` with the transcript, the recording's audio and `--anchors` spreads the cues
   over the speech it finds, holding each beat's cues inside its anchored interval, and writes
   the recording-timed captions, `<piece>.<FID>.en-GB.srt`.
2. `captions retime --edl` carries those times through every clip of that recording in the edit
   decision list, giving the master-timed captions, `<piece>.en-GB.srt`.
3. `repurpose` takes each cut's In and Out from the master-timed cues.
4. `captions retime --in --out` gives each cut its own timing; where the author sees drift,
   `extract-audio --in --out` and `captions align --lines` align that cut on its own audio.

Alignment is a heuristic: the author checks it by eye in a burned preview.

## Cutting the master

The edit decision list's clips name the recording's footage ID, with `in` and `out` taken from
the transcript's anchors. An audio-only episode is the same list with `size = ""`, under a faded
music bed; a long talk's cut-downs come later, in the publishing layer.

**An episode cut from another piece's recording** is a piece of its own, its `parent` the talk and
its `source_media` the talk's footage IDs, logged once: its transcript copies the parent's
approved beats it keeps, anchors included, and is approved as its own M2; a later correction to
either reopens both. A talk published whole as an episode stays one piece.

## How we apply it here

- Log the recording first, with a rights row if it shows other people
  (`production/docs/reference/source-media.md`).
- Approve the transcript before any caption or cut is made from it.
- Run the spelling and grammar skills (syntek-author), where present, and the fact-check skill
  (syntek-author), where present, as reports; fix only a mis-transcription.
- Never put words in a speaker's mouth: a claim that proves wrong is cut, corrected in a caption
  or a description, or kept on the author's word.

## Who implements it

- **Workflows:** `production/workflows/08-bring-in-a-recording/` (the transcript and the
  recording-timed captions), `production/workflows/03-assemble-the-master/` (the master and its
  captions) and `publishing/workflows/03-caption-a-piece/` (each cut's captions).
- **Skills:** `captions` and `cut-for-platform`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the ladder, including what M2
and M3 mean for a recorded piece. This guide owns how a recording becomes a piece.
