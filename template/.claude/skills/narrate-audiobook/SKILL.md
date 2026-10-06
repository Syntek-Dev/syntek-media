---
name: narrate-audiobook
description: >-
  Plan and narrate an audiobook chapter by chapter, only when the author asks: first the chapter
  register and credits, approved as M2; then a route per channel: the author's own recording,
  mastered to the ACX targets; ElevenLabs narration through the user-scope MCP server where a
  channel accepts it; or ElevenLabs' own package, made outside this template. Chapter text comes
  only through 'media.py audiobook text'; the cost is stated before any call; one call at a time,
  each take logged with 'media.py take add'; every master checked, packaged and archived. Use when
  the author says 'narrate chapter 3', 'start the audiobook', 'choose the audiobook's narrator',
  'can this go to Audible?', 'master the chapters I recorded' or 'check the files for ACX'. Not a
  video's voiceover (`voiceover`). Not the book's words (the writing skills of syntek-author,
  where present). Not a constructed word's sound (the pronounce skill (syntek-author), where
  present).
---

# Skill: Narrate Audiobook (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

An audiobook is the book read aloud, chapter by chapter. This skill never changes a word of it,
never copies its text into a tracked file, and never spends unasked. **The route is the author's
choice, channel by channel, and each channel's own rule decides what it accepts.** ACX, and so
Audible, takes a human narrator unless the author is authorised otherwise; a channel that accepts
AI narration only as ElevenLabs' own package gets one the author makes in ElevenLabs' studio,
outside this template. Every other route ends in files the toolkit has mastered and checked, and
every approved master is archived: a lost chapter costs credits to make again, and never comes
back the same. It carries its own call discipline, the same as `voiceover`'s, so it runs alone.

## Governing procedures (route here — do not restate at length)

Route to the one that matches the task and follow its `STEPS.md` against its `CHECKLIST.md`. These
are the procedure of record — do not restate them at length here.

- `production/workflows/05-narrate-an-audiobook/` — the route for each channel, the chapter
  register and its approval (M2), the chapter text and the takes or recordings.
- `production/workflows/06-master-an-audiobook/` — mastering, the check, approval, archiving and
  the package for each channel.
- If a layer's `workflows/local/` holds a folder with the same `NN-name` as a procedure named here,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `production/docs/reference/audiobook-narration.md` — the three routes, the distributors' policies
  as dated `VERIFY` facts, the ACX targets and the recording practice.
- `production/docs/reference/elevenlabs.md` — the server's setup and base path, the absolute
  `output_directory`, cost discipline, model discovery and `take add`.
- `production/src/audiobook/CLAUDE.md` — the register: chapter rows, credit rows `ch00`, `ch99`.
- `scripts/docs/reference/the-piece-ladder.md` — M2 (the register approved), M4 and M5.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 4 to 6 — never spend unasked, AI
  disclosure, and rights and consent.

The mode file adds this kind of book's source, the words it cannot say unaided, and its examples.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Confirm the request.** Confirm that the author asked for this, and for exactly what: the
   plan, narration, the mastering of recorded chapters, or a check; which book (the piece), which
   chapters, for which channels.
   If nothing was asked, stop: never generate unasked, including as a 'helpful' extra after another skill.
   *Complete when:* the author's request is restated chapter by chapter.

2. **Choose the route for each channel, with the author.** Read the piece's `brief.md`
   (`kind: audiobook`, `picture: false`; its deliverables are `audiobook.<store>` keys; M1 dated)
   and `brand/src/voice/voice.md`, then each channel's dated facts in the guide, saying how old they
   are. Agree one route per channel: `human` (the author records; the toolkit masters and checks),
   `ai` (ElevenLabs through the MCP; the toolkit masters and checks), or `external` (a package
   ElevenLabs' own product makes). Say plainly that ACX, and so Audible, requires a human narrator
   unless the author is authorised otherwise, so `ai` is never offered for it without that
   authorisation, recorded; and that INaudio accepts AI narration only as an unmodified package
   made in ElevenLabs' studio, outside this template, so its route is `external`, and this skill
   refuses to generate or master anything for it. AI narration is always disclosed: check that the
   brief's `synthetic_voice` and its disclosure plan say so, and report it where they do not.
   *Complete when:* every channel has the route the author chose.

3. **Write the register and the credits, and record M2.** An audiobook has no `script.md`: its
   chapter register `production/src/audiobook/<piece>.md` is its plan. Where it does not exist,
   write it in the format its folder's pair gives: the routes in `route` and `channels` (each the
   store of an `audiobook.<store>` key); one row per chapter, its Source the chapter's file in
   syntek-author's manuscript layer, where present, or 'provided' with the path the author gives,
   and its Route; plus the credit rows `ch00` (opening credits) and `ch99` (closing credits). An
   `external` row's Master names the export and where it is kept, its Check reads `external`, and
   its disclosure is recorded. Write the credits' spoken words with the author, one sentence per
   line, in `production/src/audiobook/<piece>.ch00.md` and `<piece>.ch99.md`, each the Source of its
   row: the one text this folder holds, never copied from the book. Check that every chapter's
   source is `final` (or that the author has said otherwise, which its Source cell records) and that
   its title is the one the book prints. Put the plan to the author, and only on their approval date
   the register's `approved:`; check M2 as the ladder guide gives it for an audiobook, and where it
   passes set the brief's `status: scripted`, date `M2` in `verified`, record `M3: 'n/a — no
   picture'` beside it and set `last_updated`. Nothing is recorded or generated before M2.
   *Complete when:* every chapter and both credits have a row, a source and a route, the credits
   are written, and M2 is dated, or the author has the plan with what it still lacks.

4. **Check the narrator, or choose one with the author (AI route).** The ElevenLabs tools come
   from a server the author configures once at user scope under the name `elevenlabs`; the project
   adds nothing to `.mcp.json`. Load them with ToolSearch, searching for 'elevenlabs'. Before any
   batch, run `python3 toolkit/media.py check --setup` and stop on any ElevenLabs finding
   (`.claude/rules/syntek-media/03-production-ethics.md` Section 4). If the tools are absent and
   `command -v espeak-ng` finds the program, offer a scratch read of step 5's chunks for timing
   only, labelled approximate and never mastered
   (`espeak-ng -v en-gb -f <chunk> -w <piece>.chNN.pNN.scratch.wav`, in their folder), or stop; if
   neither exists, give the install hint (the system package `espeak-ng`) and the server's setup
   command from `production/docs/reference/elevenlabs.md`, and stop. Read the `narration` row of
   `voice.md` `## Narrators` and use exactly the voice and model it records. If none is recorded:
   find the Eleven v4 model's ID with `mcp__elevenlabs__list_models` (never assume it: without a
   `model_id` the server falls back to its default model), list voices with
   `mcp__elevenlabs__search_voices`, and let the author choose one, saying first that every trial
   listen costs credits too. A cloned voice needs a `cleared` `voice-consent` row in
   `production/src/rights-register.md`, its ID in the Consent column. Record the voice name and ID,
   model ID, settings, output format and the date chosen, and copy the model ID and output format
   into the register's frontmatter, which the toolkit reads.
   *Complete when:* `voice.md` records a voice and a model ID for narration, the author has chosen
   the scratch read or to stop, or the setup steps are given and the run has stopped.

5. **Make the chapter text (AI route).** Run
   `python3 toolkit/media.py audiobook text SOURCE --piece PIECE --chapter chNN`, with
   `--footnotes` as the mode file says and `--limit` under the recorded model's character limit.
   SOURCE is the row's Source (for `ch00` and `ch99`, the credits' own file). The command strips
   syntek-author's section markers, comments, citation keys, and Pandoc divs and spans; applies the
   `voice.md` pronunciations; writes `<piece>.chNN.pNN.txt` chunks at paragraph boundaries into
   `production/src/audiobook/generated/`; and ends a chunk at every pause (a scene break is
   `{pause 2}`), recording each pause in the chapter's `<piece>.chNN.chunks.toml` beside them, the
   chunk files in order, each with its `pause_after` seconds. Exit 1 lists every word or reference
   with no spoken form: settle each with the author as a row of `voice.md` `## Pronunciations`, and
   run it again. Never edit a chunk: fix its source, or `voice.md`, and make it again.
   *Complete when:* every chapter in hand has its chunks, and the command exits 0.

6. **State the cost and wait.** Build each request from its chunk exactly as `audiobook text` wrote
   it. No pause mark is ever in a chunk, so none reaches ElevenLabs as text: the silence comes from
   the sidecar at step 9. Any other braced mark becomes an audio tag only where the recorded model
   supports one, and is otherwise left out and reported. Count the characters of the request text
   exactly as it will be sent and the calls (one per chunk), per chapter and in total, and estimate
   the credits at the rate of the author's plan, saying that it is an estimate. Name the output
   format, chosen for the channel's master, and say when it needs a higher ElevenLabs tier
   (`mp3_44100_192` needs Creator or above, `pcm_44100` Pro or above); say plainly that a 128 kbps
   take re-encoded up to 192 kbps meets the letter of ACX's bitrate rule, not its intent. Agree how
   many chapters go in one batch, give the balance from `mcp__elevenlabs__check_subscription` if
   the author wants it, and wait for a yes.
   *Complete when:* the author has seen the count and said yes.

7. **Generate, one chunk at a time.** Call `mcp__elevenlabs__text_to_speech` once per chunk, in part
   order, with its request, the recorded voice, `model_id` and settings, the `output_format`, and
   `output_directory` set to the **absolute** path of `production/src/audiobook/generated/` under
   the repository root (resolve the root with `git rev-parse --show-toplevel`). Without it the
   server saves to its own base path or the desktop. Straight after each call, before the next,
   run `python3 toolkit/media.py take add FILE --piece PIECE --chapter chNN --part pNN`, FILE being
   the path the result names: it renames the take to `<piece>.chNN.pNN.tN.mp3` (`.pcm` for a
   `pcm_*` format), because chunks that open alike and are made in the same second overwrite each
   other, and writes the register's takes and the credits-log row. Never rename a take with a shell
   `mv`. Set the chapter's Status to `generated` once its parts are made. Stop at the first error
   and report it, rather than retrying into spent credits. If the first part says a name wrongly,
   stop: settle it in `voice.md` with the author before anything more is spent.
   *Complete when:* every part has one named take and a credits-log row, or the first error is
   reported.

8. **Record (human route).** The author records each chapter as the guide describes: one chapter
   per file, its spoken header first, room tone at the head and the tail, and the same channels in
   every file. A narrator other than the author signs a release first: no recording of theirs is
   logged until its row in `production/src/rights-register.md` is `cleared`. Log each recording at
   once with `python3 toolkit/media.py footage add FILE --kind audio --location LABEL`, which
   copies it into the local mirror, never moves it, and gives it its `F` ID; enter that ID in the
   chapter's Takes and set its Status to `recorded`. A recording is never edited in place.
   *Complete when:* every chapter recorded is logged, with its footage ID in the register, and any
   other narrator's release is cleared.

9. **Master and check.** For each chapter, run
   `python3 toolkit/media.py audiobook master CHUNKS… --piece PIECE --chapter chNN`, the chunks
   being the chapter's chosen takes in part order or its recording, with `--head` and `--tail` room
   tone where the guide says; it reads the chapter's `<piece>.chNN.chunks.toml`, where present, and
   puts exactly the pause it records between those parts as room tone, then writes
   `<piece>.chNN.mp3` to `production/src/audiobook/renders/`. The credits are mastered as their own
   files, `ch00` and `ch99`, as ACX asks. Then run `python3 toolkit/media.py audiobook check FILE…`
   over every mastered file, against the `[audiobook.acx]` targets. Exit 1 is a finding: name the
   measure and the chapter, and never master again with changed targets to force a pass. Fill the
   chapter's Master, Duration and Check, and set its Status to `mastered`, then `checked` once it
   passes. If a tool is missing, say which one and which command it blocks.
   *Complete when:* every chapter in hand is mastered and checked, or each failure is reported.

10. **Listen, approve and archive.** The author listens to every chapter through. A part that reads
    wrongly is taken again only on the author's word, from step 6, and the chapter is mastered
    again. The mastered chapter is what is approved and archived: when the author approves one,
    offer to archive it at once with
    `python3 toolkit/media.py footage add FILE --kind generated --location LABEL` (`--kind audio`
    for the master of a human recording), and record its `F` ID in the register beside the master.
    Its chunk takes may be archived too, on the author's word; the archived master is what M4
    reads. Audio is git-ignored (`production/src/.gitignore`): never add it to Git or force it in.
    *Complete when:* every chapter has the author's verdict, and every approved master is
    archived, or the author has declined with the risk said.

11. **Package per channel.** For each channel on the `human` or `ai` route, gather the credits as
    files of their own (`ch00`, `ch99`) and the chapters in order, against the channel's
    `[audiobook.<store>]` table, flagging any key it lists in `verify`. Where the channel takes a
    retail sample, cut it from an approved master with
    `python3 toolkit/media.py cut <piece>.chNN.mp3 --deliverable audiobook.acx --in TC --out TC`,
    a range within the table's `sample_max_seconds`. Note the disclosure each synthetic channel
    asks for (Spotify's digital voice narration box, for one) for the post package, and set each
    packaged row's Status to `packaged`.
    *Complete when:* every channel is packaged, with its sample and its disclosure noted.
12. **Hand back.** Report the chapters made or recorded, mastered and checked; the characters and
    calls spent; the voice and model; every check result; what is archived; each channel's route,
    package and disclosure; and open words and flags. First fill all four `M4.*` as
    `n/a — no picture`, including missing entries in older pieces. The procedure records
    the gates on the author's word: M4 (storyboarded → produced, with M3 `n/a — no picture`)
    once every chapter's master, the credits' included, exists, probes clean, has been heard through,
    is approved and is archived; then M5 (produced → cut) once `audiobook check` passes on every
    file, with `M6: 'n/a — audiobook'` beside it and `status: cut`. The author uploads to each
    channel; this skill never does. M7 still needs every rights row `cleared` and the announcement
    through `prepare-post`.
    *Complete when:* the author has the report, and nothing was generated, mastered or sent
    without the author's word.

## Anti-patterns

- **Generating unasked.** Every call spends the author's credits; a chapter nobody requested is a
  cost nobody agreed.
- **AI narration for ACX or Audible without authorisation, or anything made for an `external`
  channel.** ACX asks for a human narrator; an external channel takes ElevenLabs' own package.
- **Copying chapter text into a tracked file, or editing a chunk.** The source is the record; the
  credits' two files are the only text the audiobook folder holds.
- **Voicing anything before M2, or a chapter that is not `final`** without the author's word.
- **Guessing a word with no spoken form.** Settle it in `voice.md` with the author first.
- **Omitting the model ID or the absolute `output_directory`, or renaming a take later.** The
  default model is not the narrator's, the default folder is outside the project, and `take add`
  runs straight after each call.
- **A second narrator mid-book**, or another person's voice without a cleared release.
- **Forcing the check**, or calling a 128 kbps take a 192 kbps master without saying what the
  re-encode does not fix.
- **Retrying on error**, or offering an espeak-ng read that is not installed or mastering one.
- **Committing audio, or leaving an approved master unarchived.**

## Cross-references

- `production/src/audiobook/` — the chapter registers, with `production/src/audiobook/generated/`
  and `production/src/audiobook/renders/`, which `production/src/.gitignore` keeps out of Git.
- `brand/src/voice/voice.md` — the narrator, its settings, and every pronunciation.
- `production/src/credits-log.md` — one row per call, written by `take add`.
- `production/src/footage/manifest.toml` — recordings and approved masters, archived.
- `production/docs/reference/audiobook-narration.md` — the guide this skill applies.
- `voiceover` — the same call discipline, for a video's or a trailer's voice; `write-script`
  writes a scripted piece's words, never an audiobook's.
- `prepare-post` — the post that announces the audiobook; this skill never uploads it.
