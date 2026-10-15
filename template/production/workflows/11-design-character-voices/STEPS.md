---
workflow: 11-design-character-voices
phase: produce
skills: [voiceover]
model: opus
---

# STEPS.md — design character voices

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for designing a character's voice from the author's own cloned voice, on
the author's request. Each step names the skill and guide it uses. **Run in order** (nothing is
sent before the request is planned, stated and agreed) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The `voiceover`
> skill runs this procedure; its mode file adds this project's characters and rules.

## 1. Confirm the request

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

Confirm that the author asked for a character's voice, and for which characters. Read the
`## Narrators` table of `brand/src/voice/voice.md`: a character who already has a
`character:<name>` row keeps it unless the author says to replace it, recorded in
`.claude/MEMORY.md` with the date. If nothing was asked, stop. _Substantive._

## 2. Check the setup

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Load the `elevenlabs` tools with ToolSearch (searching 'elevenlabs'). Run
`python3 toolkit/media.py check --setup` and read its ElevenLabs lines: the server's base path
must contain this repository, every credit-spending tool must be an ask rule, and so must
`voice remix run`. If any line fails, give the fix it prints and stop. Ask the author to confirm
that `ELEVENLABS_API_KEY` is exported in the shell at user scope; never print it, echo it or type
it on a command line. _Mechanical._

## 3. Confirm the source clone and its consent

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

The source is the author's own cloned voice, recorded in a `voice.md` row whose Consent column
names a `voice-consent` row in `production/src/rights-register.md`. Read that row: it must be
`cleared`, and it must cover the author's clone, not anyone else's. Confirm the voice ID with
`mcp__elevenlabs__search_voices` if the author wants it; the call is free. A Voice Library or
stock voice cannot be remixed, and another person's voice is never used. With no cleared clone,
stop and point to `brand/workflows/05-write-the-spoken-voice/`. _Substantive._

## 4. Draft one description per character

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

For each character, draft a description of how they sound (age, pace, pitch, texture, accent
and manner) from the manuscript or the script: syntek-author's character files and their voice
markers, and its manuscript, where present, or the approved script's lines and the brief. Keep it
within the length the guide gives, and never name or imitate a real actor, reader or public
figure. Offer a preview text, a line the character says in an approved source, or leave it
to ElevenLabs to write one. The author agrees every word of each description. _Substantive._

## 5. Plan the remix and wait

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

Choose a new trial name per character and attempt, in kebab-case. Run
`python3 toolkit/media.py voice remix plan NAME --from VOICE --describe "TEXT"`, adding
`--text "TEXT"` for an agreed preview text. It is offline: it prints the request, one call and
its characters, and no credit rate. Show the plan to the author, say that every further remix is a
new call, give the balance from `mcp__elevenlabs__check_subscription` if the
author wants it, and wait for a yes. _Mechanical._

## 6. Run the remix

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

On the author's yes, run `python3 toolkit/media.py voice remix run` with exactly the planned
arguments and `--approve-call`; the project's ask rule prompts for it. It sends one request,
writes each preview into `production/src/voiceover/generated/voice-trials/<name>/` as
`<name>.pNN.mp3` beside `<name>.remix.json`, and appends the credits-log row itself, with `—`
for the piece. It refuses a name already used. Stop at the first error and report it; never
retry. _Mechanical._

## 7. Listen and choose, or plan again

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

The author plays every preview. If one is right, note its `generated_voice_id` from
`<name>.remix.json`. If none is, agree what to change in the description or the text, and go
back to step 5 with a new trial name: never reuse or delete an old trial. Never choose for the
author. _Substantive._

## 8. Save the chosen voice

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

Ask before saving: `mcp__elevenlabs__create_voice_from_preview` is on the ask list. Call it with
the chosen preview's `generated_voice_id`, a voice name the author agrees and the agreed
description (`VERIFY` on first use that it accepts a remix's ID). Write its credits-log row with
`—` for the piece. Stop at the first error and report it. _Mechanical._

## 9. Record the character's row

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

Add a row to `## Narrators` in `brand/src/voice/voice.md`: Use `character:<name>`, Service
`ElevenLabs`, the saved voice's name and ID exactly as ElevenLabs gives them, the model ID from
`mcp__elevenlabs__list_models`, the settings and output format the author agrees, the source
clone's `voice-consent` rights ID in Consent, and today's date in Chosen. _Mechanical._

## 10. Try the saved voice on a few lines, if asked

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/elevenlabs.md`

Only on the author's word, and after stating the characters and calls and hearing a yes: run
`python3 toolkit/media.py speak plan --trial NAME` with a new trial name, then call
`mcp__elevenlabs__text_to_speech` with the saved voice and its recorded model and settings, and an
absolute `output_directory` from `git rev-parse --show-toplevel`. A trial is never a take: it
keeps the server's name, enters no register, and its credits-log row reads `—` for the piece.
_Substantive._

## 11. Hand back

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/character-voices.md`

Report each character's description, the remixes run and the credits spent, the voice saved and
the row written. Lines in a character's voice are voiced as a piece, through
`production/workflows/02-make-a-voiceover/`, whose register names one voice by its Use; a piece
that needs several voices in one register cannot be voiced that way yet, so raise it with the
author rather than working round it. _Substantive._
