---
workflow: 05-write-the-spoken-voice
phase: author
skills: []
model: opus
---

# CHECKLIST.md — write the spoken voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `brand/docs/reference/the-spoken-voice.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked to settle or change the spoken voice, and said for which uses.** · _opus_
- [ ] `brand/src/voice/voice.md` read as it stands. · _sonnet_

## Execution Checklist

**The spoken style**

- [ ] Grilling pass run with the grill-with-docs skill (syntek-author), where present, or the same questions in rounds, each with a recommended answer. · _opus_
- [ ] The written voice read first, where syntek-author's voice files are present; any contradiction reported, not resolved silently. · _opus_
- [ ] Pace, register, the brand's name said aloud and words never said aloud written under `## Spoken style`. · _sonnet_

**The narrators**

- [ ] The ElevenLabs tools loaded, or their absence reported with the setup; the setup check's ElevenLabs lines clean before any spend. · _sonnet_
- [ ] Model found with `mcp__elevenlabs__list_models`, never assumed. · _sonnet_
- [ ] Candidates listed free, presented per use with a recommendation, output format and tier stated. · _opus_
- [ ] **Every cloned voice has a cleared `voice-consent` row before it is made or used.** · _opus_
- [ ] No audio generated from this procedure; any trial run through `production/workflows/02-make-a-voiceover/` on the author's word, into `production/src/voiceover/generated/voice-trials/<name>/` made by `speak plan --trial <name>`, never `mkdir`. · _sonnet_
- [ ] One row per use: voice, voice ID, model ID, settings, output format, consent, date chosen. · _sonnet_

**Pronunciations and record**

- [ ] The brand's name and every word known to need it recorded, with IPA, respelling and source. · _opus_
- [ ] `python3 toolkit/media.py flags` shows no flag in a section `voiceover` reads. · _sonnet_
- [ ] Narrator choices dated in `.claude/MEMORY.md` by use and voice name, never by voice ID. · _sonnet_

## Done When

- [ ] **Every use the project needs has one narrator the author chose by listening, recorded with its model and settings.** · _opus_
- [ ] No cloned voice without its cleared consent row. · _opus_
- [ ] Handed back: spoken style, narrators by use, consent still open, credits spent, pronunciations to settle. · _opus_
