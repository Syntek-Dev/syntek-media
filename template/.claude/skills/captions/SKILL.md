---
name: captions
description: >-
  Make a piece's captions, and a recorded piece's transcript: timed from the voiceover's approved
  segments, aligned to recorded speech beat by beat with 'python3 toolkit/media.py captions
  align' and checked by eye, or made by hand. Speech-to-text through the user-scope ElevenLabs MCP
  server runs only when the author asks, after the audio minutes are stated, and returns text
  without timings; on its base-path error this skill prints the exact fix. Writes SRT and VTT for
  the master and each cut, runs 'captions check' against the script or transcript, and burns
  them in or leaves a sidecar as each platform takes them. Use when the author says 'caption the
  short', 'transcribe the talk', 'time the captions to the voiceover', 'captions for each cut',
  'burn the captions in' or 'the captions drift'. Not the voiceover (`voiceover`). Not the cut
  (`cut-for-platform`). Not proofreading (the spelling and grammar skills of syntek-author, where
  present).
---

# Skill: Captions (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

Captions are the script, or the transcript, timed. The words come from that record and never from
a guess; the timing comes from the cheapest route that is true. The ElevenLabs speech-to-text tool
returns text only, with no timestamps, so it can draft a transcript but never time a caption.
**Timing has three routes, in this order of preference**: the voiceover's approved segments,
whose measured durations make every cue boundary exact at each join; recorded speech, where cues
are spread over the speech intervals ffmpeg finds, beat by beat, a heuristic the author checks by
eye in a burned preview; and by hand.

A recorded piece has no script: its transcript, made here and approved by the author, stands in
for one wherever a script is read. This skill never changes the script or the transcript to fit a
caption, and never spends unasked.

## Governing procedures (route here — do not restate at length)

Route to the one that matches the task and follow its `STEPS.md` against its `CHECKLIST.md`. These
are the procedure of record — do not restate them at length here.

- `publishing/workflows/03-caption-a-piece/` — captions for a piece's master and its cuts, checked,
  and burned in or left as sidecars.
- `production/workflows/08-bring-in-a-recording/` — a recorded piece's transcript, its beat
  anchors and its recording-timed captions.
- If a layer's `workflows/local/` holds a folder with the same `NN-name` as a procedure named here,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `publishing/docs/reference/captions.md` — the house limits, the names, the three routes, and
  captions made before the cut.
- `production/docs/reference/recorded-pieces.md` — the transcript, its anchors, and the chain from
  recording to master to cut.
- `production/docs/reference/elevenlabs.md` — the server's setup, its base path and cost
  discipline for speech-to-text.
- `scripts/docs/reference/the-piece-ladder.md` — M2 for a recorded piece and M6 (cut →
  captioned); never restated here.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 4 — never spend unasked.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 2 — the caption commands; where it
  and `--help` disagree, `--help` is right.

## Steps

1. **Confirm the job and the route.** Name the procedure by its full folder name, the piece by its
   folder name, and the job: a transcript, captions for the master, captions for one or more cuts,
   a check, or burn-in. Choose the timing route from the record: the first route when every spoken
   line of the master comes from approved voiceover segments; the second for speech recorded on
   camera or in a recording, or a piece that mixes the two; the third when the author prefers it,
   or for cues the other two cannot place. Speech-to-text runs only on a request for it,
   confirmed exactly: which recording, and how many minutes.
   If nothing was asked, stop: never generate unasked, including as a 'helpful' extra after another skill.
   *Complete when:* the procedure, the piece, the job and the route are named, and any
   speech-to-text request is restated.

2. **Read the record.** Read the piece's `brief.md` (`origin`, `deliverables`, `status`,
   `verified`) and its `script.md` or `transcript.md` in `scripts/src/pieces/`; the segment
   register `production/src/voiceover/<piece>.toml`, where one exists; the edit decision list
   `production/src/edits/<piece>.toml` (the `at` of its `vo:<piece>` audio row, and the clips of
   each recording); and the cut-down plan `publishing/src/cut-downs/<piece>.md` (each cut's Lines,
   In, Out and deliverables). For each deliverable, run `python3 toolkit/media.py presets KEY`: an
   empty `caption_formats` means the platform takes no sidecar, so the captions are burned in.
   Captions are made from an approved script or transcript only.
   *Complete when:* the source of the words, each timing wanted (recording, master, cut) and each
   deliverable's caption form are known.

3. **Make a recorded piece's transcript, when that is the job.** The recording is logged first
   (`media.py footage add`, which copies it and never moves it). Run
   `python3 toolkit/media.py extract-audio SRC` for a mono 16-bit WAV; it writes
   `production/src/renders/<stem>.wav` (git-ignored) and prints the path. Make the transcript by
   hand with the author, or by speech-to-text when asked (step 4). Write `transcript.md` in the
   piece folder, in the format of `scripts/docs/reference/writing-for-the-ear.md`: frontmatter
   `piece`, `source` (the recording's footage ID), `made` and `approved`; one H2 per beat,
   `## N. <Beat name> (at HH:MM:SS.mmm)`; spoken lines only, as said, with no braces; a word it
   cannot settle written `[unclear]` and flagged `<!-- VERIFY: … -->`. Take each beat's anchor from
   the author's timings, or from a first `captions align` pass without `--anchors` that the author
   checks against the recording; never guess one. Run the fact-check skill (syntek-author), where
   present, over its claims as a report, and the spelling and grammar skills (syntek-author), where
   present, for mis-transcriptions only: a transcript's words are what was said. Check that
   `.claude/skills/<skill>/SKILL.md` exists before naming each, and say which is missing. Set
   `approved:` only on the author's word: that is M2 (briefed → scripted) for a recorded piece.
   *Complete when:* the transcript is approved, every beat is anchored and every finding decided,
   or the run has stopped for the author.

4. **Run speech-to-text, only when asked.** The ElevenLabs tools come from a server the author
   configures once at user scope under the name `elevenlabs`; the project adds nothing to
   `.mcp.json`. They may be deferred: load them with ToolSearch, searching for 'elevenlabs'. Before
   any batch, run `python3 toolkit/media.py check --setup` and stop on any ElevenLabs finding; if
   the tools are absent, say so, give the setup command from
   `production/docs/reference/elevenlabs.md`, and offer the transcript by hand. State the audio
   minutes, the number of calls (one per file) and the credits estimated from them at the rate of
   the author's plan; give the balance from `mcp__elevenlabs__check_subscription` if the author
   wants it, and wait for a yes. Then call `mcp__elevenlabs__speech_to_text` once per file with
   `input_file_path` set to the WAV's **absolute** path (resolve the root with
   `git rev-parse --show-toplevel`), `diarize` when more than one person speaks, and
   `save_transcript_to_file: false` with `return_transcript_to_client_directly: true`; where a
   file is wanted, pass an absolute `output_directory` in a git-ignored folder instead. Never leave
   both at their defaults: the server would save to its own base path or the desktop. **One call
   at a time:** wait for each result and write its credits-log row (tool `speech_to_text`, the
   calls, the minutes, the output) before the next call, never calls in parallel. Stop at the
   first error and report it, rather than retrying into spent credits. The text returned is a
   draft for step 3: an audio event it adds, such as '(laughter)', stays only as a bracketed sound
   that matters, and nothing is timed from it.
   *Complete when:* the draft text is in hand and its credits-log row written, or the first error
   is reported.

5. **Answer the base-path error with the exact fix.** An error saying the file is 'outside of
   allowed directory' means the server's base path does not contain the project. Never copy the
   audio to the desktop, or anywhere else, to get round it. Work out a base path that contains
   `git rev-parse --show-toplevel`: `$HOME` when the root lies under it, otherwise the nearest
   folder that holds this repository and the author's other projects, asked of the author. Print
   exactly this, with `"$HOME"` replaced by that folder where it differs:

   ```bash
   claude mcp remove elevenlabs --scope user
   claude mcp add --env ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" --env ELEVENLABS_MCP_BASE_PATH="$HOME" \
     --transport stdio --scope user elevenlabs -- uvx elevenlabs-mcp
   ```

   Tell the author to export the key in the shell first (never typed on the command line, never
   committed), to restart Claude Code so the server starts with the new path, and to run
   `python3 toolkit/media.py check --setup` again. Then stop.
   *Complete when:* the author has the command with the computed path, and the run has stopped.

6. **Time the captions from the voiceover (the first route).** With every segment `approved`, run
   `python3 toolkit/media.py captions from-segments REGISTER --deliverable KEY --offset TC`, the
   register being `production/src/voiceover/<piece>.toml` and the offset the `at` of the edit
   list's `vo:<piece>` row, with `-o` naming `publishing/src/captions/<piece>.en-GB.srt`. It chunks
   each segment to the deliverable's limits and spreads the segment's measured duration across its
   cues by character share, so every cue boundary is exact at each segment join.
   *Complete when:* the master-timed file exists.

7. **Time the captions to recorded speech (the second route).** For a scripted piece spoken on
   camera, extract the master's audio and run `captions align` with the script and that audio,
   with `-o publishing/src/captions/<piece>.en-GB.srt`: `align`, `retime`, `rewrap` and `vtt`
   write to the terminal unless `-o` names the file, so every one of them here passes `-o` with
   the path given. For a recorded piece, align the approved transcript to the recording with
   `--anchors`, so drift never crosses a beat, writing the recording-timed
   `<piece>.<FID>.en-GB.srt`; then carry it to the master with
   `captions retime SRT --edl production/src/edits/<piece>.toml --source FID`, writing
   `<piece>.en-GB.srt`, whose cue times `repurpose` reads for each cut's In and Out. Where the room
   is noisy, set `--noise` and `--min-silence`. A stretched cue is warned about, and exit 1 lists
   the cues it could not place: those are placed by hand. Burn a preview with `captions burn` and
   have the author watch it before anything aligned is published.
   *Complete when:* the master-timed file exists, every cue is placed, and the author has watched
   the preview.

8. **Make each cut's captions.** For each cut of the approved cut-down plan, run
   `captions retime SRT --in TC --out TC` on the master-timed file with the cut's In and Out,
   writing `<piece>--cNN.en-GB.srt`. Where the author sees drift, extract that cut's audio
   (`extract-audio` with `--in` and `--out`) and run `captions align` on it with `--lines`, the
   cut's Lines. Where a deliverable needs its own line width (a vertical one, typically), run
   `captions rewrap SRT --deliverable KEY`, writing `<piece>--cNN.<platform>-<format>.en-GB.srt`.
   A cut's captions may be made before the cut is rendered, so the cutting pass can burn them in.
   The third route is always open: a cue the commands misplace is set by hand, in the same file.
   *Complete when:* every cut that carries speech has its file, named for its timing and width.

9. **Check every caption file.** Run
   `python3 toolkit/media.py captions check SRT --deliverable KEY --script SCRIPT` on each file,
   SCRIPT being the `script.md` or `transcript.md`: the house limits, overlaps and gaps, and the
   caption words against the spoken words. Fix a finding in the caption file (split, merge or
   retime a cue), never by changing the script or the transcript. Words are spelt as the record
   spells them, en_GB, and no audio tag or braced direction ever reaches a caption. The spelling
   and grammar skills (syntek-author), where present, may report on caption text.
   *Complete when:* every file passes, or each remaining finding has the author's decision.

10. **Write the VTT, and burn in or leave a sidecar.** Run `captions vtt SRT -o VTT` to write a VTT
    of the same name beside every SRT. Where a deliverable's `caption_formats` is empty, or the
    brief asks, the captions are burned in: in the cutting pass (`cut --captions`,
    `cut-for-platform`) when the cut is still to be rendered, otherwise with
    `python3 toolkit/media.py captions burn SRC SRT --deliverable KEY`, which writes the `.burned`
    render to `publishing/src/renders/`. A caption font that fell back to another is a failure:
    report it, and never accept the substitute. Otherwise the file goes up beside the video as a
    sidecar, and `prepare-post` names it in the post package.
    *Complete when:* every deliverable with speech and picture has burned captions or a sidecar,
    and every burn passed.

11. **Hand back.** Report every file made, with its path and what it is timed to; the route used;
    any speech-to-text minutes and credits spent; each check's result; every burned render; and
    every `[unclear]` word and open flag. The procedure records the gate in the brief, on the
    author's word: M6 (cut → captioned) once every deliverable with speech and picture has passed
    captions (with M5 when they were burned in the cutting pass). M6 does not apply to an
    audiobook, to a podcast unless its brief asks for a transcript, or to a deliverable without
    speech: say so rather than making files nobody needs.
    *Complete when:* the author has the report, and no script, transcript or render was edited to
    make a caption pass.

## Anti-patterns

- **Speech-to-text to time captions.** It returns no timestamps; the routes above do the timing.
- **Generating unasked.** Every speech-to-text call spends the author's credits.
- **Copying audio to the desktop** to get past the base path. Fix the base path instead.
- **Leaving speech-to-text at its defaults.** The transcript lands outside the project.
- **One voiceover segment per cue, just for the captions.** The first route chunks segments of any
  size; splitting a sentence over two calls costs its intonation.
- **Aligning a long recording without anchors.** The drift spreads into every clip cut from it.
- **Publishing aligned captions nobody watched.** Alignment is a heuristic; the burned preview is
  the check.
- **Changing the script or the transcript to fit a caption.** The caption follows the record.
- **An audio tag or a direction in a caption.** Only spoken words, and sounds that matter.
- **A file named for the wrong timing.** A cut's captions on the master's clock are wrong from the
  first cue.
- **Accepting a fallback font in a burn.** The burn fails, and the font is installed or changed.
- **Retrying on error.** Stop at the first failure and report it.

## Cross-references

- `publishing/src/captions/` — every SRT and VTT, named for its timing and line width.
- `scripts/src/pieces/` — each piece's script or transcript, the words every caption follows.
- `production/src/voiceover/` — the segment registers the first route reads.
- `production/src/edits/` — the edit decision lists that carry recording time to the master.
- `publishing/src/cut-downs/` — each cut's lines, In and Out.
- `production/src/credits-log.md` — one row per speech-to-text call.
- `voiceover` — the segments the first route times from.
- `cut-for-platform` — burns a cut's captions in the cutting pass.
- `repurpose` — reads the master-timed captions of a recorded piece for each cut's In and Out.
- `prepare-post` — names each sidecar in the post package.
