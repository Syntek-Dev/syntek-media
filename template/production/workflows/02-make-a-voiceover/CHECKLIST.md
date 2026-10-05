---
workflow: 02-make-a-voiceover
phase: produce
skills: [voiceover]
model: opus
---

# CHECKLIST.md — make a voiceover

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/voiceover.md`, `production/docs/reference/elevenlabs.md` and
> the `voiceover` skill. This procedure works towards M4 (storyboarded → produced); gates are
> cited from `scripts/docs/reference/the-piece-ladder.md` by number and never restated here.

## Pre-Conditions

- [ ] Read `.claude/CLAUDE.md` and `.claude/MEMORY.md`, then this folder's `CONTEXT.md` and `CLAUDE.md`. · _sonnet_
- [ ] **The author asked for this voiceover, and the piece and lines are confirmed.** · _opus_
- [ ] M2 dated in the brief, and `synthetic_voice` names the kind of voice the piece uses. · _sonnet_

## Execution Checklist

**The setup and the narrator**

- [ ] `elevenlabs` tools loaded with ToolSearch; `media.py check --setup` run and its ElevenLabs lines clean, or the run stopped with the fix. · _sonnet_
- [ ] With no `elevenlabs` tools, `command -v espeak-ng` run; with neither route, the install hint and setup command given and the run stopped. · _sonnet_
- [ ] The voiceover narrator read from `brand/src/voice/voice.md`, or chosen by the author after `mcp__elevenlabs__list_models` and a voice search. · _opus_
- [ ] Voice, voice ID, model ID, settings, output format and date recorded the first time. · _sonnet_
- [ ] A cloned voice has its `cleared` voice-consent row, cited in the narrator's row, before it speaks. · _opus_
- [ ] Any trial run only on the author's word, into `production/src/voiceover/generated/voice-trials/<name>/` made by `speak plan --trial <name>` (never `mkdir`): no take, no register row, its credits-log row with `—` for the piece. · _sonnet_

**Segments and cost**

- [ ] One segment per spoken sentence or short beat (per cue only for a kinetic-caption short, on the author's word), agreed with the author. · _opus_
- [ ] Register written: the `[voiceover]` table, and each segment's `script_lines`, `text` (braces removed) and `pause_after`. · _sonnet_
- [ ] Request text built: pronunciations substituted, directions as audio tags only where the model takes them, cue lines left out. · _sonnet_
- [ ] Characters, calls and estimated credits stated, and any higher tier the format needs named. · _sonnet_
- [ ] The author said yes. · _opus_

**Generating**

- [ ] The piece's `production/src/voiceover/generated/<piece>/takes/` made by `speak plan <piece>` before the first call, never with `mkdir`. · _sonnet_
- [ ] One call at a time, each with that folder as its absolute `output_directory`, built from `git rev-parse --show-toplevel`. · _sonnet_
- [ ] `take add` run straight after each call; no take renamed with a shell `mv`. · _sonnet_
- [ ] Stopped and reported at the first error, instead of retrying. · _sonnet_
- [ ] Fallback used only with the author's agreement and `espeak-ng` installed, in `generated/<piece>/` and never among the takes, labelled approximate, never approved. · _sonnet_

**Listening**

- [ ] The author listened; each take `approved` or `rejected`; regeneration only on the author's word, as a new take. · _opus_
- [ ] Each approved take archived with `footage add --kind generated` where the author agreed, its footage ID in `archived`. · _sonnet_

## Done When

- [ ] **Nothing was generated beyond what the author agreed, and the script is unchanged.** · _opus_
- [ ] Every call has its row in `production/src/credits-log.md`, and nothing generated was committed. · _sonnet_
- [ ] Handed back: segments, characters and credits spent, voice and model, approved and archived takes, faults heard. · _opus_
