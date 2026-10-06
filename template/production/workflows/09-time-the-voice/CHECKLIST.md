---
workflow: 09-time-the-voice
phase: produce
skills: [voiceover, storyboard]
model: opus
---

# CHECKLIST.md — time the voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **See** `production/docs/reference/voiceover.md`, `scripts/docs/reference/storyboards-and-shot-lists.md`
> and the `voiceover` and `storyboard` skills. This procedure works towards M4 (storyboarded → produced),
> through `M4.words` and `M4.cues`, cited from `scripts/docs/reference/the-piece-ladder.md`, never restated here.

## Pre-Conditions

- [ ] Read the read-order files, both skills and their mode files, and this procedure with its checklist open. · _sonnet_
- [ ] Scene route and the timing task confirmed with the author; brief, script, boards, shots and register read. · _opus_
- [ ] At `storyboarded`, with `M4.takes` dated or its explicit `n/a` reason; changed takes/boards have cleared the dependent dates. · _sonnet_

## Execution Checklist

**The voice and the words**

- [ ] Setup checked; WhisperX, cached models and Rhubarb resources ready, or stopped with the fix; no model fetched. · _sonnet_
- [ ] `voice join` ran on approved takes with their pauses, never a scratch track. · _sonnet_
- [ ] Words timed and their check agreed with findings resolved and warnings decided; unchanged accepted words kept for a board-only re-time. · _opus_
- [ ] A skipped cross-check was the author's choice and is explicit in the check. · _opus_
- [ ] Words/check accepted together through `-o`, or existing accepted files kept; tracked check read and `M4.words` dated in order. · _sonnet_
- [ ] Mouths accepted through `-o` after `lipsync` with plain text, or kept for a board-only re-time; mouth review left to `M4.stills`. · _sonnet_

**The boards**

- [ ] `cues` matched every board; findings resolved; its table read with the author. · _opus_
- [ ] Delivery anchors reviewed; each SFX/MUSIC event linked to one logged audio row by `cue`, with placement and mix agreed. · _opus_
- [ ] Accepted cues written through `-o`; Time, shot Seconds and Timing notes proposed and agreed. · _opus_
- [ ] Re-time raised board version and kept approval/M3; a shot or word revision returned to the storyboard procedure instead. · _sonnet_
- [ ] Current board agreed; `M4.cues` dated after `M4.words`, dependent dates cleared and `last_updated` set. · _sonnet_

## Done When

- [ ] **The author agreed the words and the re-timed boards; the next stills can use accepted tracked timing.** · _opus_
- [ ] Accepted data committed, no ignored working copy opened, no credits spent and no model fetched. · _sonnet_
- [ ] Hand-back names the timing files, board version, dated sub-checks and the remaining stills/preview review. · _opus_
