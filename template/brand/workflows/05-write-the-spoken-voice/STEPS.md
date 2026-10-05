---
workflow: 05-write-the-spoken-voice
phase: author
skills: []
model: opus
---

# STEPS.md — write the spoken voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for deciding how the brand sounds aloud and who says it. Each step names the
skill and guide it uses. **Run in order** (the written voice before the spoken one, consent before
any clone, and nothing heard before its cost is agreed) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No media skill
> runs this procedure: the grill-with-docs skill (syntek-author), where present, settles each
> decision with the author, and any trial runs through the voiceover procedure.

## 1. Grill the spoken voice with the author

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Check that the companion's `.claude/skills/<skill>/SKILL.md` exists for grill-with-docs; where it
does not, say so, and ask the same questions in rounds yourself, each with a recommended answer
(`.claude/rules/syntek-media/06-global-rules.md` Section 8). First read the written voice, where
syntek-author's voice notes or brand voice are present. Then settle the pace in words a minute,
the register, how the brand's name is said, the words never said aloud, which uses need a
narrator, and whether any narrator will be a cloned voice, and whose. _Substantive._

## 2. Write the spoken style

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Write the decisions under `## Spoken style` in `brand/src/voice/voice.md`, one sentence per line,
and add the brand's name to `## Pronunciations` with its respelling. Remove the section's flag.
_Mechanical (writing); the decisions are the author's._

## 3. Check the server

> **Skill:** none · **Guide:** `production/docs/reference/elevenlabs.md`

Load the ElevenLabs tools with ToolSearch (searching 'elevenlabs'). If they are absent, say so
and give the setup in `production/docs/reference/elevenlabs.md`; espeak-ng is a scratch track,
never a narrator. Where `brand/workflows/06-check-the-setup/` has not run, run it now: its
ElevenLabs lines must be clean before any credit is spent. _Mechanical._

## 4. Find the model, and list candidate voices

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Call `mcp__elevenlabs__list_models` and note the model the brand will use, never assuming one.
List candidate voices for each use with `mcp__elevenlabs__search_voices` (the account's own) and
`mcp__elevenlabs__search_voice_library` (the shared library); all three calls are free. Present a
short list per use with a recommendation, and say which output format each deliverable needs and
which ElevenLabs tier it requires. _Substantive._

## 5. Consent before any clone

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

For every use the author wants in a cloned voice, the owner's own included: the person's recorded
consent is a `voice-consent` row in `production/src/rights-register.md`, cleared through
`production/workflows/07-clear-the-rights/`, before the clone is made or used. No consent, no
clone. A clone is made only on the author's explicit request, and making one spends credits.
_Substantive._

## 6. Hear candidates only on the author's word

> **Skill:** none · **Guide:** `production/docs/reference/elevenlabs.md`

Hearing a candidate costs credits: say so before any trial. If the author asks for one, run it
through `production/workflows/02-make-a-voiceover/` and its `voiceover` skill, which state the
characters, calls and credits, wait for a yes, call one at a time and log the credits. No piece
owns a trial: its `output_directory` is `production/src/voiceover/generated/voice-trials/<name>/`
(`<name>` a kebab slug for the trial, such as `warm-narrator`), which
`python3 toolkit/media.py speak plan --trial <name>` makes before the first call; never make it
with `mkdir`. A trial is never a take: it keeps the server's name, enters no register, and its
credits-log row has `—` for the piece. Never generate from this procedure directly.
_Substantive._

## 7. Record each narrator

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

For each use the author settles, add one row under `## Narrators`: use, service, voice, voice ID,
model ID, the stability, similarity, style and speed to send on every call, the output format,
the consent ID or a dash, and the date chosen. Remove the section's flag once every use the
project needs has its row. _Mechanical._

## 8. Record the pronunciations

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Add a row for every word known to need one: the brand's name first, then people, places,
products and borrowed words. Take each pronunciation from its owner or an authoritative
reference; an invented name takes its IPA from syntek-author's names register or lexicon, where
present, and the pronounce skill (syntek-author), where present, is never run from here. Name
the source in each row. _Substantive._

## 9. Clear the flags, and record

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Run `python3 toolkit/media.py flags brand/src/voice/` and confirm no flag is left in a section
`voiceover` reads. Record each narrator choice in `.claude/MEMORY.md`, dated, by use and voice
name (never by ID), under the heading syntek-author's 00-project.md Memory headings map it to,
where present. _Mechanical._

## 10. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/the-spoken-voice.md`

Report the spoken style, each narrator by use, any consent row still open, the credits spent on
trials (from `production/src/credits-log.md`), and the pronunciations still to settle.
_Substantive._
