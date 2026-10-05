---
name: voiceover
description: >-
  Voice a piece through the user-scope ElevenLabs MCP server, only when the author asks: one
  segment per spoken sentence or beat of the approved script, with the narrator, model and
  pronunciations of brand/src/voice/voice.md; the cost stated before any call; one call at a time
  into the piece's ignored takes/ folder, each take logged at once with 'media.py take add' and
  archived once approved; an espeak-ng scratch track as the fallback. Use when the author says
  'voice the script', 'make the voiceover for the trailer', 'take segment 4 again', 'choose a
  narrator for the trailer' or 'archive the approved takes'. Not captions (`captions`). Not the
  master or any render (`cut-for-platform`). Not the script's words (`write-script`). Not an
  audiobook or its narrator (the narrate-audiobook skill, where the project makes audiobooks). Not
  a constructed word's sound or a language's narrator (the pronounce skill (syntek-author), where
  present).
---

# Skill: Voiceover (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

The script is the record; the voiceover is made from it, segment by segment, and only when the
author asks, because every call spends the author's credits and a take cannot be made again: the
server exposes no seed, so a segment generated twice costs twice and sounds different.
**One spoken sentence or beat per call, one call at a time, and every take renamed and logged
before the next call.** A segment is never a caption cue: a sentence split over two calls ends
twice, with two final intonations, and the server passes no neighbouring text to smooth the join.

The author chooses the voice, hears every take and approves it. This skill never changes a word of
the script to suit the voice, and never creates or clones a voice.

## Governing procedures (route here — do not restate at length)

Route to the one that matches the task and follow its `STEPS.md` against its `CHECKLIST.md`. These
are the procedure of record — do not restate them at length here.

- `production/workflows/02-make-a-voiceover/` — this skill is that procedure in skill form.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `production/docs/reference/voiceover.md` — segments per sentence or beat, `per_cue`, and the
  segment register.
- `production/docs/reference/elevenlabs.md` — the server's setup and base path, the absolute
  `output_directory`, cost discipline, model discovery, `take add`, archiving and the fallback.
- `brand/docs/reference/the-spoken-voice.md` — narrators per use, pronunciations and consent.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 4 to 6 — never spend unasked, AI
  disclosure, and rights and consent before a voice is used.

The mode file adds this project's kinds of voiceover, the lines it voices and its domain rules.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Confirm the request.** Confirm that the author asked for a voiceover, and for exactly what:
   which piece, and which segments (the whole script, or named segments to take again).
   If nothing was asked, stop: never generate unasked, including as a 'helpful' extra after another skill.
   *Complete when:* the author's request is restated segment by segment.

2. **Read the piece.** Read the piece's `brief.md` and `script.md` in `scripts/src/pieces/`, its
   segment register `production/src/voiceover/<piece>.toml` where one exists, and
   `brand/src/voice/voice.md`. Voice an approved script only (`approved:` dated); a line from a
   draft is voiced only on the author's explicit word, after saying that a revision wastes the
   credits spent on it. The voiced lines are the ones the mode file names; an `ON:` line is spoken
   on camera, and a cue line (`TEXT:`, `SFX:`, `MUSIC:`, `NOTE:`) is never spoken. If the brief's
   `synthetic_voice` reads `none`, report it: the brief and its disclosure plan must say a
   synthetic voice is used before the piece is published.
   *Complete when:* the lines to voice are listed by `beat.line`, from an approved script or on the
   author's recorded word.

3. **Check the narrator, or choose one with the author.** The ElevenLabs tools come from a server
   the author configures once at user scope under the name `elevenlabs`; the project adds nothing
   to `.mcp.json`. They may be deferred: load them with ToolSearch, searching for 'elevenlabs'.
   Before any batch, run `python3 toolkit/media.py check --setup` and stop on any ElevenLabs
   finding (`.claude/rules/syntek-media/03-production-ethics.md` Section 4). If the tools are
   absent, run `command -v espeak-ng`: if it finds the program, tell the author and offer the
   fallback at step 8, or stop. If neither route exists, say so, give the install hint (the system
   package `espeak-ng`) and the server's setup command from
   `production/docs/reference/elevenlabs.md`, and stop. Read the `## Narrators` row of `voice.md`
   for the use the mode file names. If a voice and model are recorded, use exactly those. If not:
   call `mcp__elevenlabs__list_models` and find the Eleven v4 model's ID (never assume it: without
   a `model_id` the server falls back to its default model); list candidate voices with
   `mcp__elevenlabs__search_voices`; and let the author choose one voice, saying first that every
   trial listen costs credits too. A trial is never a take: its `output_directory` is the absolute
   `production/src/voiceover/generated/voice-trials/<name>/`, it keeps the server's name, enters no
   register, and its credits-log row, written by this skill, reads `—` for the piece. A cloned
   voice, the owner's own included, is chosen only when its `voice-consent` row in
   `production/src/rights-register.md` is `cleared`, and that row's ID goes in the Consent column.
   Record the voice name, voice ID, model ID, settings (stability, similarity, style, speed),
   output format and the date chosen in the row. Keep one narrator per use: a second voice makes
   one brand sound like two.
   *Complete when:* `voice.md` records a voice and a model ID for the use, the author has chosen
   the installed fallback or to stop, or the setup steps are given and the run has stopped.

4. **Write the segments.** Open or update the register in the format the
   `production/src/voiceover/` pair gives: `[voiceover]` with `piece`, `voice_use` (the `voice.md`
   use), `model_id`, `output_format` and `per_cue`; then one `[[segment]]` per spoken sentence, or
   per beat where a short beat reads as one breath, within the recorded model's character limit.
   `per_cue = true`, one segment per caption cue, is for a kinetic-caption short only, on the
   author's word. Each segment carries `id` (`s01`, `s02` and on, permanent), `script_lines` (`2.1`
   or `2.1–2.3`), `text` (the words as spoken, braces removed: this is the caption text) and
   `pause_after` (seconds, from a `{pause S}` before the next line); `take`, `file`, `status` and
   `archived` are filled as each take is made. Never renumber a segment that has a take.
   *Complete when:* every line to voice belongs to exactly one segment, and the register reads.

5. **Build the request text.** For each segment, start from `text` and substitute every word that
   `voice.md` `## Pronunciations` records: its IPA between forward slashes where the recorded model
   takes inline IPA, otherwise its respelling. Turn a braced direction into an audio tag
   (`[whispers]`) only when the recorded model supports tags; otherwise leave it out, and the
   delivery comes from the voice settings. A `{pause S}` inside a sentence is never sent as text:
   report it, and keep the sentence whole. Record the result in `request` and its length in
   `characters`. The request goes to the server only, never back into the script or into `text`.
   *Complete when:* every segment to voice has its `request` and `characters`.

6. **State the cost and wait.** Count the characters of the request text exactly as it will be
   sent, and the number of calls (one per segment), and estimate the credits from them at the rate
   of the author's plan, saying that it is an estimate. Name the output format, chosen for the
   deliverable, and say when it needs a higher ElevenLabs tier (`mp3_44100_192` needs Creator or
   above, `pcm_44100` Pro or above). For a single segment, mention the count in one line; for a
   batch, give the total and, if the author wants it, the balance from
   `mcp__elevenlabs__check_subscription`, then wait for a yes.
   *Complete when:* the author has seen the count and said yes.

7. **Generate, one call at a time.** Call `mcp__elevenlabs__text_to_speech` once per segment with
   its `request`, the recorded voice, `model_id` and settings, the `output_format`, and
   `output_directory` set to the **absolute** path of the piece's takes folder,
   `production/src/voiceover/generated/<piece>/takes/`, under the repository root (resolve the
   root with `git rev-parse --show-toplevel`). Without it the server saves to its own base path or
   the desktop. Straight after each call, before the next, run
   `python3 toolkit/media.py take add FILE --piece PIECE --segment sNN`, FILE being the path the
   result names: it renames the take to `<piece>.sNN.tN.mp3` (`.pcm` for a `pcm_*` format),
   because the server names files by the second and can overwrite one, and writes the segment's
   `take` and `file` and the credits-log row. Never rename a take with a shell `mv`. Set the
   segment's `status` to `generated`. Stop at the first error and report it, rather than retrying
   into spent credits. If the first take says a name or a term wrongly, stop: settle its
   pronunciation in `voice.md` with the author before anything more is spent.
   *Complete when:* each segment has one named take and a credits-log row, or the first error is
   reported.

8. **Fall back to espeak-ng when ElevenLabs is unavailable.** Only if the author agrees and step 3
   found `espeak-ng` installed: with each pronunciation's respelling substituted (espeak-ng takes
   no IPA), write each segment in `production/src/voiceover/generated/<piece>/`, never in its
   takes subfolder, with `espeak-ng -v en-gb -s <wpm> -w <piece>.sNN.scratch.wav "<text>"`, the speed
   being the brief's `words_per_minute`. Label the result approximate: a scratch and timing track
   for hearing the rhythm and checking the length, never a take. It gets no `take`, is never
   approved, and never reaches a master or a deliverable.
   *Complete when:* each file exists and is labelled approximate.

9. **Listen, approve and archive.** The author listens to every take. Set `status` to `approved` or
   `rejected`; a rejected segment is taken again only on the author's word, from step 5 or 6, and
   the old take stays where it is. A take cannot be made again, so when the author approves one,
   offer to archive it at once:
   `python3 toolkit/media.py footage add FILE --kind generated --location LABEL` copies it into
   the local mirror, hashes it and gives it the next `F` ID. Record that ID in the segment's
   `archived`, and the take it archives in that manifest row's `notes`. Audio is git-ignored (the
   rule is in `production/src/.gitignore`): never add it to Git, and never force it past the
   ignore rule.
   *Complete when:* every take has the author's verdict, and every approved take is archived or
   the author has declined with the risk said.

10. **Hand back.** Report the segments voiced, the takes made, the characters and calls spent, the
    voice and model used, anything the voice got wrong, and which takes are approved and archived.
    Name what comes next: captions timed from the register (`captions`, its first route), and the
    master, which joins the approved segments with their pauses (`cut-for-platform`); M4
    (storyboarded → produced) needs every take the master uses approved and archived. Confirm that
    no word of the script changed.
    *Complete when:* the author has the report.

## Anti-patterns

- **Generating unasked.** Every call spends the author's credits; a take nobody requested is a cost
  nobody agreed.
- **Voicing a draft.** A revised line throws away the take made from the old one.
- **One segment per caption cue.** A sentence split over two calls ends twice; the captions are
  timed from the segments whatever their size.
- **Omitting the model ID.** The server's default model is not the one the narrator was chosen with.
- **Audio on the desktop.** Without the absolute `output_directory`, files land outside the project
  and its ignore rule.
- **Renaming later, or by hand.** Two takes made in the same second can overwrite each other: run
  `take add` straight after each call, never a shell `mv`.
- **A second narrator.** One use, one recorded voice.
- **A voice nobody consented to.** No clone without a cleared consent row; the owner's own clone is
  still synthetic, and is disclosed.
- **Committing audio, or leaving an approved take unarchived.** It is too large for plain Git, and
  once lost it cannot be made again.
- **Retrying on error.** Stop at the first failure and report it.
- **Offering a fallback that is not installed.** Check for `espeak-ng` before offering it; with
  neither route, give the setup steps and stop.
- **Passing off a scratch track as a take.** espeak-ng output is approximate, for timing only.

## Cross-references

- `production/src/voiceover/` — the segment registers; takes land in the git-ignored
  `production/src/voiceover/generated/<piece>/takes/`, which `production/src/.gitignore` keeps
  out of Git.
- `brand/src/voice/voice.md` — narrators per use, their settings, and every pronunciation.
- `production/src/credits-log.md` — one row per call, written by `take add`, or by this skill for
  a trial.
- `production/src/footage/manifest.toml` — where approved takes are archived.
- `production/docs/reference/elevenlabs.md` — the guide this skill applies.
- `captions` — its first route times captions from this register's approved segments.
- `cut-for-platform` — assembles the master, joining the approved segments.
- `write-script` — where a wording problem heard in a take is fixed.
- The narrate-audiobook skill, where the project makes audiobooks — chapter narration, which
  carries this skill's call discipline itself.
- The guides to standalone voiceovers and to trailers in `scripts/docs/reference/`, where the
  project makes them.
