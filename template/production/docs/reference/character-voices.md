---
type: guide
skills: [voiceover]
model: opus
---

# Character voices — a voice of its own, remixed from the author's

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A character's voice is designed from the author's own cloned voice: ElevenLabs
remixes the clone to a written description and returns a few previews, the author chooses one,
and it is saved as a voice of its own. It is the one ElevenLabs call the toolkit makes directly,
because the MCP server has no remix tool; saving, speaking and every other call stay on the
server. A remix is still the author's voice, so it carries the clone's consent and is disclosed.

## The description

- One description per character, drafted from the source: syntek-author's character files and
  their voice markers, and its manuscript, where present, or the approved script and the brief.
- Describe what a listener hears: age, pace, pitch, texture, accent, manner. The request takes
  5 to 1000 characters (`VERIFY`, checked 15/10/2026).
- Never name or imitate a real actor, reader or public figure.
- An optional preview text, 100 to 1000 characters (`VERIFY`), is a line the character says in
  an approved source; without one, ElevenLabs writes its own.
- The author agrees every word before anything is planned.

## Plan, then run

- `python3 toolkit/media.py voice remix plan NAME --from VOICE --describe TEXT [--text TEXT]` is
  offline: it prints the request, one call and its characters, and no credit rate. `NAME` is a
  new voice-trial name, as `speak plan --trial` takes one: letters, digits, `.`, `_` and `-`,
  starting with a letter or digit, up to 64 characters. `VOICE` is the author's clone, a voice
  the account owns.
- State the plan and wait for a yes. `voice remix run`, with the same arguments and
  `--approve-call`, sends that one request: no retry, no redirect, a 30-second timeout. The
  project's ask rule prompts for it, because the toolkit's allow would otherwise let it run.
- The key comes only from `ELEVENLABS_API_KEY` exported in the shell at user scope; the toolkit
  never writes or prints it.
- The run writes `<name>.pNN.mp3` for each preview and `<name>.remix.json` (the date, the
  source voice, the description, the text, and each preview's `generated_voice_id`, media type
  and duration) into a staging folder, moves them whole into
  `production/src/voiceover/generated/voice-trials/<name>/`, and appends its own credits-log row,
  Tool `voice remix`, with `—` for the piece; without `--text`, it counts the characters of the
  preview text ElevenLabs wrote. It refuses a used name.

## Choose, save, record

- The author listens to every preview. Another attempt is a new description or text, planned
  again under a new trial name; an old trial is never reused or deleted.
- Saving is an MCP call on the ask list: `mcp__elevenlabs__create_voice_from_preview` with the
  chosen `generated_voice_id` (`VERIFY` on first use that it accepts a remix's), after a yes.
- The saved voice gets a `character:<name>` row in `brand/src/voice/voice.md`. Its Consent is
  the source clone's `voice-consent` rights ID: the remix is the author's voice, re-described.
- A trial of the saved voice on a few lines is an ordinary voice trial, made through
  `speak plan --trial`: it keeps the server's name and is never a take.

## How we apply it here

- `production/workflows/11-design-character-voices/` runs it, through `voiceover`, in every
  project; the mode file says which characters and uses a brand voices.
- A character's lines are voiced as a piece through `production/workflows/02-make-a-voiceover/`,
  whose register names one voice by its Use. A piece in several voices in one register is not
  supported yet: raise it with the author rather than working round it.
- Previews and trials stay git-ignored and are never archived as takes.
- Audiobook narration, where the project makes audiobooks, gives a character's lines the voice
  of a saved `character:<name>` row, never a remix made mid-chapter.

## Who implements it

- **Workflows:** `production/workflows/11-design-character-voices/` designs the voice, and
  `production/workflows/02-make-a-voiceover/` voices a character's lines.
- **Skill:** `voiceover` drafts with the author, plans, runs, saves and records.
- **Toolkit:** `voice remix plan` and `voice remix run` in `toolkit/media.py`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns consent before a voice is
used, and Section 4 never spending unasked; `.claude/rules/syntek-media/06-global-rules.md`
Section 10 keeps the key at user scope. This guide owns how a character's voice is designed.
