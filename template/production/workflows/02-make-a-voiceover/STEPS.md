---
workflow: 02-make-a-voiceover
phase: produce
skills: [voiceover]
model: opus
---

# STEPS.md — make a voiceover

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for voicing an approved script through ElevenLabs on the author's request.
Each step names the skill and guide it uses. **Run in order** (nothing is generated before the
cost is stated and agreed) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The `voiceover`
> skill is this procedure in skill form.

## 1. Confirm the request

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Confirm that the author asked for a voiceover, and for exactly what: which piece, and the whole
script or which lines. Read the brief: M2 must be dated (the script approved), and
`synthetic_voice` must name the kind of voice the piece uses. If nothing was asked, stop.
_Substantive._

## 2. Check the setup

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Load the `elevenlabs` tools with ToolSearch (searching 'elevenlabs'). Run
`python3 toolkit/media.py check --setup` and read its ElevenLabs lines: the server's base path
must contain this repository, and every credit-spending tool must be an ask rule. If either
fails, give the fix it prints and stop. If the tools are absent, run `command -v espeak-ng`: if
it finds the program, offer the fallback at step 8, or stop; with neither route, give the install
hint (the system package `espeak-ng`) and the server's setup command from
`production/docs/reference/elevenlabs.md`, and stop. _Mechanical._

## 3. Check the narrator, or choose one with the author

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Read `## Narrators` in `brand/src/voice/voice.md`. If the voiceover use has a voice and model,
use them. If not: find the model with `mcp__elevenlabs__list_models` (currently `eleven_v4`),
list candidate voices with `mcp__elevenlabs__search_voices`, and let the author choose. Record
the voice, its ID, the model ID, the settings, the output format and the date; a cloned voice
also needs its `cleared` voice-consent row in `production/src/rights-register.md`, cited in the
narrator's row, before it speaks. Choosing a voice by listening costs credits too; say so before
any trial. _Substantive._

## 4. Split the script into segments

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Make one segment per spoken sentence, or per beat short enough to stay under the recorded
model's character limit; never one per caption cue, unless the author asks for a kinetic-caption
short (`per_cue = true`). Write `production/src/voiceover/<piece>.toml`: the `[voiceover]` table,
then one `[[segment]]` per segment with its `script_lines`, its `text` as spoken (braces removed)
and its `pause_after`. Agree the split with the author. _Substantive._

## 5. Build the request text

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

For each segment, write `request`: pronunciations substituted from `brand/src/voice/voice.md`,
braced directions turned into audio tags only where the recorded model takes them and dropped
otherwise, cue lines left out. The script itself is never changed. _Mechanical._

## 6. State the cost and wait

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Count the characters of every request exactly as it will be sent, the number of calls and the
estimated credits, and say whether the output format needs a higher ElevenLabs tier. Give the
balance from `mcp__elevenlabs__check_subscription` if the author wants it. Wait for a yes.
_Mechanical._

## 7. Generate, one call at a time

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

For each segment in turn, call `mcp__elevenlabs__text_to_speech` with the recorded voice,
`model_id`, settings and `output_format`, and an absolute `output_directory`: the output of
`git rev-parse --show-toplevel` followed by `/production/src/voiceover/generated`. Straight after
the call, and before the next, run `python3 toolkit/media.py take add` on the file the result
names, with `--piece` and `--segment`: it renames the take, writes the register's `take` and
`file`, and appends the credits-log row. Never rename a take with a shell `mv`. Stop at the first
error and report it, rather than retrying into spent credits. _Mechanical._

## 8. Fall back to espeak-ng when ElevenLabs is unavailable

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Only if the author agrees and step 2 found `espeak-ng` installed: make a scratch track from each
segment's `text`, for timing only, in `production/src/voiceover/generated/`, and label it
approximate. It is never approved and never reaches a deliverable. _Mechanical._

## 9. Listen, approve and archive

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

The author listens to every take. Set each segment's `status` to `approved` or `rejected`; a
rejected segment is regenerated only on the author's word, as a new take, through steps 6 and 7.
For each approved take, offer to archive it with
`python3 toolkit/media.py footage add FILE --kind generated --location LABEL`, and record the
footage ID in `archived`. The audio stays out of Git; never force it in. _Substantive._

## 10. Hand back

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Report the segments voiced, the characters and credits spent, the voice and model used, which
takes are approved and archived, and anything the voice got wrong. Confirm that the script was
not changed, and point to `production/workflows/03-assemble-the-master/`. _Substantive._
