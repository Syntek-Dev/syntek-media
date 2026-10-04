---
type: guide
skills: [voiceover, captions]
model: opus
---

# ElevenLabs — the user-scope server, one call at a time, never unasked

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Voiceover, narration and speech-to-text come from ElevenLabs through the
user-scope MCP server `elevenlabs`, and every call spends the author's credits. The server marks
every tool read-only, so only this discipline and the project's ask rules stand between a request
and the bill. The project adds nothing to `.mcp.json`.

## Setting up the server

The base path must **contain the project**: files land there when no `output_directory` is given,
and speech-to-text reads no input file from anywhere else ('outside of allowed directory'; a
symlink does not help). Use `$HOME` when every project lives under it, else the nearest folder
holding them all. Export the key in your shell first (never type it or commit it), then re-add:

```bash
claude mcp remove elevenlabs --scope user
claude mcp add --env ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" --env ELEVENLABS_MCP_BASE_PATH="$HOME" \
  --transport stdio --scope user elevenlabs -- uvx elevenlabs-mcp
```

## Cost before spend

- **Never generate unasked**: not as a demonstration, not to test a setting, not as a helpful
  extra after another job. Trying voices costs credits too.
- Before any batch, state the characters (or audio minutes for speech-to-text), the number of
  calls and the estimated credits, and wait for a yes; `mcp__elevenlabs__check_subscription`
  gives the balance. Stop at the first error, rather than retrying into spent credits, and log
  every call in `production/src/credits-log.md`.

## One call at a time, into the project

- Find the model with `mcp__elevenlabs__list_models` (currently `eleven_v4`) and record it per
  use in `brand/src/voice/voice.md`; never assume it.
- Pass `output_directory` as an **absolute** path to the git-ignored generated folder, built from
  `git rev-parse --show-toplevel`; a relative path resolves against the base path.
- The server names a file by the second and can overwrite one, so run
  `python3 toolkit/media.py take add` straight after each call: it renames the take and writes its
  register and credits-log rows. Never rename a take with a shell `mv`.
- Choose `output_format` for the deliverable and say when it needs a higher tier (`mp3_44100_192`
  needs Creator or above, `pcm_44100` Pro or above). A `pcm_*` take is headerless 16-bit PCM named
  `.mp3`: `take add` names it `.pcm`, read as mono `s16le` at the register's rate (`VERIFY` on
  first use). A 128 kbps take re-encoded to 192 kbps meets ACX's letter, not its intent.

## Speech-to-text, and the scratch fallback

- `mcp__elevenlabs__speech_to_text` returns text, no timestamps. Run it only when asked, on a WAV
  from `media.py extract-audio`, with `save_transcript_to_file: false` and
  `return_transcript_to_client_directly: true`; on 'outside of allowed directory', re-add the
  server with a base path containing `git rev-parse --show-toplevel`, never copying audio away.
- Without ElevenLabs, and only with the author's agreement, `espeak-ng` makes a scratch or timing
  track: check `command -v espeak-ng` first; with neither route, give the install hint (the system
  package `espeak-ng`) and the setup command, and stop. Label it approximate; it never ships.

## How we apply it here

- Run `python3 toolkit/media.py check --setup` before the first batch: it reports whether the
  base path contains this repository and whether `.claude/settings.json` asks before every
  credit-spending tool. No batch runs until its ElevenLabs lines are clean.
- Generated audio stays git-ignored, and an approved take, which cannot be made again, is
  archived with `footage add --kind generated`; voice IDs live only in the brand's own files.

## Who implements it

- **Workflows:** `production/workflows/02-make-a-voiceover/`,
  `production/workflows/08-bring-in-a-recording/` and `publishing/workflows/03-caption-a-piece/`.
- **Skills:** `voiceover` makes takes; `captions` makes transcripts. Narration follows the same
  discipline where the project makes audiobooks.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 4 owns never spending unasked, and
`.claude/rules/syntek-media/06-global-rules.md` Section 10 keeps keys at user scope. This guide
owns how a call is made, and at what cost.
