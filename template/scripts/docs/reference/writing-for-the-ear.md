---
type: guide
skills: [write-script]
model: opus
---

# Writing for the ear — a script is heard once, at the speaker's pace

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A listener cannot re-read a sentence they missed, so a script is written to be
heard once and understood first time: one spoken sentence per line, each line opening with who
says it or what kind of cue it is, every delivery note in braces, so a skill can time, voice and
caption it without guessing. A recorded piece has a transcript instead, holding what was said.

## The script file

Frontmatter `piece`, `version`, `approved` (DD/MM/YYYY, or empty until the author approves),
`words` and `estimated_seconds`; then `# <Title> — script`; then one H2 per beat,
`## N. <Beat name> (target MM:SS)`: that beat's own running time, never a running total, so the
beats' targets add up to the brief's `target_seconds`.

| Mark | Means |
|---|---|
| `VO:` · `ON:` · `HOST:` · `GUEST:` · `NARRATOR:` · a character's name | A spoken line: voiceover, on camera, a host, a guest, a narrator, a character. Upper case, then a colon. |
| `TEXT:` · `SFX:` · `MUSIC:` · `NOTE:` | A cue: words on screen, a sound, music, a note to production. Never spoken, never timed as speech. |
| `{softly}` · `{pause 0.6}` | A direction, at the start of a line or before a phrase; `{pause S}` adds S seconds. |

A line is cited as `beat.line` (`2.1` is the second beat's first spoken line), counting spoken
lines only. The script holds no IPA (how a word is said lives in `brand/src/voice/voice.md`) and
no stage direction outside braces or cue lines. A braced direction becomes an ElevenLabs audio
tag only when the recorded model supports tags, and never reaches a caption. An audiobook has no
script: its chapter register is its plan, through the audiobook procedures, where the project
makes audiobooks.

## Writing for one hearing

- One idea per sentence, and short sentences; the line break is where a breath goes.
- The hook comes first, before any greeting or name, and the promise is kept in the same piece.
- Say numbers, dates and symbols the way they are spoken, and say a key point more than once.
- Lists of more than three, nested clauses and words that sound alike lose a listener.
- Read every line aloud at the brief's pace; the voice file gives the brand's spoken style.

## Timing

`python3 toolkit/media.py script time scripts/src/pieces/<piece>/script.md` counts the spoken
words (tags, braces and cue lines removed), adds every `{pause}`, and reports each beat against
its own target and the total, at the `words_per_minute` it reads from the brief (150 where the
brief sets none; `--wpm` overrides). It compares the total with `target_seconds` (within 10%) and
with each deliverable's `max_seconds` in `toolkit/data/platforms.toml`; `--write` records `words`
and `estimated_seconds`. Cut or reshape a script that runs long; never speed up the rate to fit.

## Transcripts

`transcript.md` has frontmatter `piece`, `source` (the recording's footage ID), `made`
(`speech-to-text DD/MM/YYYY` or `by hand`) and `approved`; then `# <Title> — transcript`; beats as
`## N. <Beat name> (at HH:MM:SS.mmm)`, the beat's start on the recording. It holds spoken lines
only, as said, with no braces. A word it cannot settle is written `[unclear]` and flagged
`VERIFY`; only a mis-transcription is ever corrected.

## How we apply it here

- The author approves every script and transcript, dated only on their word; every checkable
  claim is verified before approval, or cut; adapted written work is read, never edited.
- The spelling, grammar, comprehension, flow and fact-check skills (syntek-author), where
  present, report on the script and the author decides each finding; improve-section and
  adapt-section (syntek-author), where present, run only as report-then-agreed-edit, with no
  ledger entry.

## Who implements it

- **Workflow:** `scripts/workflows/02-write-a-script/` writes, times and approves a script;
  `production/workflows/08-bring-in-a-recording/` makes a recorded piece's transcript.
- **Skills:** `write-script` writes, times and revises the script; `captions` makes the
  transcript and reads either file for caption words.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 1 owns who approves a script, and
Section 7 forbids a fabricated claim, quotation or testimonial; Section 3 makes M2 binding. The
rules own the requirements; this guide owns how a script is written for the ear.
