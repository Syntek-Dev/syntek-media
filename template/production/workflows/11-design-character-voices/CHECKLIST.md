---
workflow: 11-design-character-voices
phase: produce
skills: [voiceover]
model: opus
---

# CHECKLIST.md — design character voices

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/character-voices.md`. No gate in `scripts/docs/reference/the-piece-ladder.md` applies to this procedure.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked for a character's voice, and the characters are confirmed.** · _opus_
- [ ] `brand/src/voice/voice.md` read; a character's existing row replaced only on the author's word, recorded in `.claude/MEMORY.md`. · _sonnet_

## Execution Checklist

**The setup and the source**

- [ ] `elevenlabs` tools loaded with ToolSearch; `media.py check --setup` run, its ElevenLabs lines and the `voice remix run` ask rule clean, or the run stopped with the fix. · _sonnet_
- [ ] The author confirmed `ELEVENLABS_API_KEY` is exported at user scope; the key never printed, echoed or typed. · _sonnet_
- [ ] The source is the author's own clone, its `voice-consent` row in `production/src/rights-register.md` `cleared`; no Voice Library voice and no other person's voice. · _opus_

**Descriptions and the remix**

- [ ] One description per character, drafted from the manuscript or the script, imitating no real actor, reader or public figure, and agreed word for word. · _opus_
- [ ] Any preview text agreed, or left for ElevenLabs to write. · _opus_
- [ ] `voice remix plan` run offline with a new trial name; its request, one call and characters shown, no credit rate invented. · _sonnet_
- [ ] The author said yes. · _opus_
- [ ] `voice remix run` run with the planned arguments and `--approve-call`, once; stopped at the first error, never retried. · _sonnet_
- [ ] Previews and `<name>.remix.json` in `production/src/voiceover/generated/voice-trials/<name>/`, and the credits-log row written by the run. · _sonnet_

**Choosing and saving**

- [ ] The author listened to every preview and chose one, or a new description was agreed and planned under a new trial name. · _opus_
- [ ] The save asked for and agreed; `mcp__elevenlabs__create_voice_from_preview` called with the chosen `generated_voice_id`, and its credits-log row written with `—` for the piece. · _sonnet_
- [ ] The `character:<name>` row recorded in `brand/src/voice/voice.md`, its Consent the source clone's rights ID and its Chosen date today. · _sonnet_
- [ ] Any trial of the saved voice run only on the author's word, made by `speak plan --trial NAME` (never `mkdir`): no take, no register row, its credits-log row with `—` for the piece. · _sonnet_

## Done When

- [ ] **Nothing was sent beyond what the author agreed, and no voice was cloned.** · _opus_
- [ ] Every call has its row in `production/src/credits-log.md`, and nothing generated was committed. · _sonnet_
- [ ] Handed back: descriptions, remixes and credits spent, voices saved, rows written, and how the character's lines are voiced next. · _opus_
