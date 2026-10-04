---
name: cut-for-platform
description: >-
  Render every master, cut and deliverable through the toolkit and nothing else: write the
  piece's edit decision list with the author from its storyboard and shot list, or a recorded
  piece's transcript (clips, stills, cards, colour, fades, push-ins, a music bed ducked under the
  voice); copy the brand's card layout for each card; assemble the master with 'python3
  toolkit/media.py assemble'; then cut, reframe and encode each deliverable of the brief and the
  cut-down plan, burning captions in the same pass where they exist, and probe every output
  against its preset before calling it done. Renders are git-ignored, never hand-edited. Use when
  the author says 'assemble the master', 'cut the shorts', 'make the vertical version', 'encode it
  for YouTube', 'master the episode' or 'why did the cut fail?'. Not choosing which moments to cut
  (`repurpose`). Not making or checking the captions (`captions`). Not the thumbnail
  (`thumbnail-brief`).
---

# Skill: Cut for Platform (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

Turns a piece's plan into files, and checks them. **Every render goes through
`python3 toolkit/media.py`**, because its commands carry the frame-accurate seek, the platform
presets with the brand's overrides, the loudness targets and the verification a hand-written
ffmpeg line skips. A render that exited cleanly is not a finished deliverable: this skill probes
each output, reports it against its preset, and counts it done only once the author has seen it.

It never edits a render, never overwrites a master without the author's word, and never changes a
script, a register, the edit decision list or the cut-down plan to make a render pass. Renders are
git-ignored and regenerable from tracked files; the edit decision list and the cards are the
record.

## Governing procedures (route here — do not restate at length)

Route to the one that matches the task and follow its `STEPS.md` against its `CHECKLIST.md`. These
are the procedure of record — do not restate them at length here.

- `production/workflows/03-assemble-the-master/` — the edit decision list, the cards and the
  master.
- `publishing/workflows/02-cut-for-a-platform/` — every deliverable of the brief and the cut-down
  plan, cut, encoded and verified.
- The podcast-mastering workflow in `production/workflows/`, where the project makes podcasts, uses
  this skill for an audio master cut from a recording; an audiobook is mastered by the
  narrate-audiobook skill, where the project makes audiobooks, never here.
- If a layer's `workflows/local/` holds a folder with the same `NN-name` as a procedure named here,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `production/docs/reference/edit-decision-lists.md` — the format: clips, stills, cards, colour,
  fades, the push-in, overlays and audio.
- `production/docs/reference/sound-and-loudness.md` — the loudness targets, ducking, where a music
  bed goes, and fades.
- `production/docs/reference/source-media.md` — footage IDs, the manifest and the local mirror.
- `publishing/docs/reference/cut-downs.md` and `publishing/docs/reference/platform-specs.md` —
  reframing, safe zones and hooks; how a preset is read (`verify`, `chosen`, absent keys,
  overrides).
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` — the pipeline, the commands and their rules;
  where it and `--help` disagree, `--help` is right.

## Steps

1. **Fix the piece, the job and the deliverables.** Name the procedure by its full folder name, the
   piece by its folder name, and the job: an edit decision list, a master, one or more cuts, a
   whole-file encode or a still video. Read the piece's `brief.md` (`deliverables`, `origin`,
   `picture`, `status`, `verified`) and its cut-down plan `publishing/src/cut-downs/<piece>.md`,
   and run `python3 toolkit/media.py presets KEY` for each deliverable (the brand's overrides
   applied, every `verify` key named). A master needs the piece `storyboarded`, or M3 recorded as
   `n/a`; a cut needs the piece `produced` and the cut's row `approved` in the plan.
   *Complete when:* the procedure, the piece, the job, every deliverable key and its preset are
   known, and the gate the job needs has passed.

2. **Write the edit decision list with the author.** Write `production/src/edits/<piece>.toml` in
   the format of `production/docs/reference/edit-decision-lists.md`. `[edit]` sets the master's
   `size` (`""` for an audio master, which takes sound only from its clips), `audio_rate` and
   `loudness`. One `[[clip]]` per shot, in timeline order: from each storyboard row and the source
   its shot-list row names, or, for a recorded piece, from the transcript's beats as ranges of the
   recording. A video or audio source takes `in` and `out`; a still, a card or a `colour` clip
   holds for `seconds`; `motion = "push-in"` goes on a still or a card only; `transition = "fade"`
   where the storyboard asks for one. A card over the picture is an `[[overlay]]`. Sound goes in
   `[[audio]]`: the voice as `vo:<piece>`, a music bed by its footage ID with `role = "music"`,
   `duck = true` under the voice, trimmed with `in` and `out` and faded, and effects. A sound-only
   source never stands as a clip of a picture master. A shot whose source is still `to shoot`, or
   a footage ID the manifest lacks, blocks the list: report it. Raise `version` when an approved
   list changes, and never overwrite an approved list without the author's word.
   *Complete when:* every storyboard row, or every transcript beat the piece uses, has its clip,
   every source resolves, and the author has approved the list.

3. **Make the cards.** For each card the list names, copy
   `brand/src/design-system/previews/card.html`, or `toolkit/templates/card.html` where the
   brand's is absent, to `production/src/cards/<piece>.<card>.html`. Fix its stylesheet link to
   `../../../brand/src/design-system/tokens.css`, and every image path, for its new folder, and
   delete the brand component's own `AUTHOR TO CONFIRM` line about the brand's layout (the brand
   file keeps it, and `media.py flags` reports it there). Put in only the words the storyboard's
   'On screen' column gives. Never change a token or the layout in a card: a change of layout
   belongs to the brand's component, so it reaches every later piece.
   Run `uv run toolkit/card.py check` on each card.
   *Complete when:* every card exists, passes `card.py check`, and holds only approved words.

4. **Check before assembling.** Run `python3 toolkit/media.py footage verify`: it must pass for
   every source the list uses. Every voice segment the master uses must be `approved` and
   `archived` in `production/src/voiceover/<piece>.toml`; route the rest to `voiceover`. Every
   licensed or identifiable source needs its row in `production/src/rights-register.md`: report
   any not yet `cleared` (M7 needs it, not the master). If the master already exists, ask before
   replacing it.
   *Complete when:* every check passes or the run has stopped on it, and the author has agreed to
   any replacement.

5. **Assemble the master.** Run
   `python3 toolkit/media.py assemble production/src/edits/<piece>.toml`. It writes
   `production/src/renders/<piece>.master.mp4` (`.wav` for an audio master), first rendering any
   card that is missing or older than its HTML or `tokens.css` with `uv run toolkit/card.py`, and
   exits 2 naming uv or Chromium when it cannot. If a tool is
   missing, say which one and which command it blocks; never report a command as passed when it
   could not run. Exit 1 is a failed verification: report it, and never run it again with changed
   settings to force a pass. Probe the master (`python3 toolkit/media.py probe`), measure it
   (`python3 toolkit/media.py loudness measure`), and report both against the target. The author
   watches or hears it through.
   *Complete when:* the master exists, probes clean, its loudness is within the target, and the
   author has been through it.

6. **Cut, reframe and encode each deliverable.** For each full-length deliverable of the brief,
   run `python3 toolkit/media.py encode MASTER --deliverable KEY`, with `--frame crop` or
   `--frame pad` where the frame changes. For each approved cut of the plan, run
   `python3 toolkit/media.py cut MASTER --deliverable KEY --in TC --out TC --cut cNN` with the
   plan's Frame: `centre` is `--frame crop`, `crop x=<px>` is `--frame crop --x <px>`, `pad` is
   `--frame pad`. Add `--captions SRT` when the cut's caption file exists and the platform takes no
   sidecar or the brief asks for burned captions, so they burn in the same pass: the deliverable's
   rewrapped `.<platform>-<format>` file where one exists (the key's dot and underscores as
   hyphens), otherwise the cut's own file if `captions check --deliverable KEY` passes. An audio
   deliverable (its table has no width or height) is cut and encoded as audio only, by the same
   commands. For audio meant for a video platform, run
   `still-video IMAGE AUDIO --deliverable KEY`. Outputs land in
   `publishing/src/renders/`, named `<piece>[--cNN].<platform>-<format>[.burned].<ext>`. Never call
   ffmpeg or ffprobe directly to make a deliverable, and never cut with `-c copy`.
   *Complete when:* every deliverable in hand has one output, or a named failure.

7. **Verify every output.** Each command checks its output against the preset (size, codecs,
   duration within `max_seconds`, the index at the front of the file); exit 1 is a finding. Probe
   each output and report it against its preset, naming any `verify` key the result rests on. The
   author sees or hears each deliverable.
   *Complete when:* every output has its probe line and verdict, and the author has seen each.

8. **Report back.** Give every path, the edit decision list's version, the master's probe and
   loudness, each deliverable's probe line and verdict, every failure with its command and its
   reason, the rights rows not yet `cleared`, and any missing tool. The procedure records the gates
   in the brief, on the author's word: M4 (storyboarded → produced) once the master probes clean,
   `footage verify` passes, every take it uses is approved and archived, its loudness is within
   the target and the author has been through it; M5 (produced → cut) once every deliverable of
   the brief and the plan passes and the author has seen each; and M6 with it, where captions were
   burned in the cutting pass and passed their check. Renders are git-ignored: never add one to
   Git.
   *Complete when:* the author has the report, and no render, script, register, list or plan was
   hand-edited to make it look right.

## Anti-patterns

- Calling ffmpeg directly, and so skipping the preset, the overrides and the verification.
- Reporting a render as good because it exited without error. Probe it, and show the author.
- Hand-editing a render, or a token or the layout inside a piece's card.
- Overwriting a master, or an approved edit decision list, without the author's word.
- Assembling with a voice take that is not approved and archived: it cannot be made again.
- Putting a sound-only source in a picture master as a clip.
- Changing the list, the plan, a preset or an override to make a verification pass.
- Rendering a cut the plan has not approved, or one the brief does not name.
- Adding a render to Git, or forcing it past the ignore rule.
- Mastering an audiobook here: its targets and checks belong to the narrate-audiobook skill,
  where the project makes audiobooks.

## Cross-references

- `production/src/edits/` — the edit decision lists, the record every master rebuilds from.
- `production/src/cards/` — each piece's title and end cards, copied from the brand's layout.
- `production/src/renders/` and `publishing/src/renders/` — masters, card images and
  deliverables, all git-ignored and regenerable.
- `production/src/footage/manifest.toml` — every source by its footage ID.
- `toolkit/data/platforms.toml` and `brand/src/platforms/overrides.toml` — the presets, and the
  brand's confirmed corrections to them.
- `repurpose` — decides each cut's lines, In, Out and frame in the cut-down plan.
- `captions` — makes the caption files a cut burns in.
- `voiceover` — the approved, archived segments the master's voice is joined from.
- `thumbnail-brief` — the thumbnails, which this skill never renders.
