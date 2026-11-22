---
name: storyboard
description: >-
  Turn one approved script into a storyboard and a shot list: a picture for every spoken line, the
  framing for every vertical deliverable, the on-screen text, the sound, and a source for every
  shot (footage, a still, a card, a scene, or a shot still to film), opening a needed rights row
  for every licensed or identifiable item, then rendering the board sheet and animatic the author
  sees before M3. Use when the author says 'storyboard the explainer', 'what do we show over this
  line?', 'make a shot list for the shoot', 'show me the boards' or 'how will this crop for a
  vertical short?'. Never run for a recorded piece or a piece with no picture: M3 does not apply.
  Not for writing or changing the script (`write-script`). Not for the edit decision list or the
  master: this renders only the board sheet and animatic (`cut-for-platform`). Not for planning
  cut-downs (`repurpose`). Not for a thumbnail (`thumbnail-brief`).
---

# Skill: Storyboard (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

A storyboard is the script made visible: each spoken line is given a picture, each picture a
source, and each source that someone else owns, or that shows someone, a row in the rights register
before a frame is cut. This skill boards **one** approved script, row by row, and writes the shot
list the shoot and the edit work from. **No spoken line is left without a picture, and no shot
without a source**: 'something to be decided' is the gap that stops an edit on the day.

The board plans only what the edit can make. In this template that is footage cut frame-accurately,
stills and cards held for a set time, colour clips, cuts, cross-fades and a slow push-in on a still
(`production/docs/reference/edit-decision-lists.md`), or a code-animated scene with native
aspects. Anything smoother (a moving or eased push-in or pan, parallax, a build-up animated word
by word, an animated lower third, a speed ramp, a composite of layers, a transition beyond a
cross-fade) is an `edited` shot, made in an outside editor and logged as footage
(`production/docs/reference/complex-shots.md`). Recorded video inside a scene is deferred. <%OWNER_FIRST_NAME%> approves the board
having seen it as a board sheet and, where it moves, an animatic, and the approval is what M3
records.

## Governing procedures (route here — do not restate at length)

- `scripts/workflows/03-storyboard-a-piece/` — this skill is that procedure in skill form. Run its
  `STEPS.md` with `CHECKLIST.md` open.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `scripts/docs/reference/storyboards-and-shot-lists.md` — the two tables, their columns and their
  vocabularies.
- `scripts/docs/reference/the-piece-ladder.md` — M3 (scripted → storyboarded), and when it is
  `n/a`; never restated here.
- `.claude/rules/syntek-media/03-production-ethics.md` Section 6 and
  `production/docs/reference/rights-and-consent.md` — rights before publishing, consent before a
  likeness or a voice, and what each rights row records.
- `production/docs/reference/edit-decision-lists.md` — what a shot becomes in the edit.
- `publishing/docs/reference/cut-downs.md` — reframing and safe zones for vertical deliverables.
- `brand/docs/reference/the-brand-kit.md` — the tokens and the card layout every card is built on.
- `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 2 — `media.py boards`, its outputs
  and exit codes; `.claude/rules/syntek-media/06-global-rules.md` Section 12 — opening a still by
  its printed path, never by listing its folder.

The mode file adds this project's kinds of picture, its sources and its domain rules.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece.** Confirm the piece with the author: its folder in `scripts/src/pieces/` and
   its `brief.md`. If the brief has `origin: recorded`, stop: M3 is `n/a — recorded`, recorded by
   `production/workflows/08-bring-in-a-recording/`, and the master is cut from the recording. If
   it has `picture: false`, stop: M3 is `n/a — no picture`. If its `status` is `briefed` (M2 not
   dated), stop: the script comes first (`scripts/workflows/02-write-a-script/`). If
   `storyboard.md` already exists, the request is a revision: change only what the author asks,
   and go to step 8. A timing-only re-time follows `production/workflows/09-time-the-voice/`:
   run `python3 toolkit/media.py cues <piece>`, review the printed table, accept the cue index
   with `-o production/src/scenes/<piece>.cues.json`, and update Time and shot Seconds.
   Raise `version`, keep approval and M3 (no new board sheet), and clear `M4.cues`, `M4.stills`,
   M4 and later gates; date cues again only after the author accepts the re-time. A word or shot
   change clears M3.
   *Complete when:* the piece is confirmed as scripted, with a picture, its M2 dated, and the run is
   known to be a first board or a revision.

2. **Read the script, the brief and the deliverables.** Read the approved `script.md` whole,
   counting its spoken lines by `beat.line`, and its `TEXT:`, `SFX:` and `MUSIC:` cues. Read the
   brief's `deliverables`, `## Rights needs`, `ai_visuals` and `music`. For each deliverable, run
   `python3 toolkit/media.py presets <key>` and note its size, aspect and safe zone. Read
   `production/src/footage/manifest.toml`, `production/src/assets/` and
   `production/src/rights-register.md` for what the project already holds and has cleared, and the
   brand's tokens and card layout in `brand/src/design-system/`.
   *Complete when:* the spoken lines are counted, every deliverable's frame and safe zone are
   written down, and what already exists is known.

3. **Confirm nothing will be clobbered.** Check that the piece folder holds no `storyboard.md` and
   no `shot-list.md`, or that the author has confirmed, in this conversation, a rewrite over them.
   *Complete when:* both paths are free, or the author has confirmed a rewrite over them.

4. **Board every spoken line.** Write `storyboard.md`: frontmatter `piece`, `version: 1` and an
   empty `approved:`, the H1 `# <Title> — storyboard`, then the table
   `| # | Beat | Time | Picture | Spoken | On screen | Sound | Vertical framing | Timing notes |`. One row per
   picture, numbered `B01` onwards: Beat is the script's beat number; Time is `MM:SS–MM:SS`, from
   the beat targets and the script's timing; Picture says what is seen, in a phrase; Spoken cites
   the lines the picture carries (`2.1–2.3`); On screen carries the script's `TEXT:` cues and any
   name caption; Sound carries the voice, the `SFX:` and `MUSIC:` cues and room tone. Every spoken
   line sits in exactly one row. A board that moves names `push-in`, `pan`, `zoom` or `fade` in
   its Picture cell, and a build-up says `build-up` there or holds two or more `TEXT:` cues: the
   animatic reads both. Timing notes are `—` until the author has timing feedback. Apply the mode file's additions.
   *Complete when:* `storyboard.md` exists, and every spoken line of the script is cited by exactly
   one row.

5. **Frame every row for the vertical deliverables.** Fill each row's Vertical framing with
   `native` for a scene rendered at its own aspect, or `centre`, `crop x=<px>` or `pad`, chosen so that faces, hands
   and on-screen text sit inside the safe zone of every vertical deliverable of the brief; where
   the brief has none, frame for a 9:16 cut-down all the same, because the cut-down plan reads this
   column. A row that no single framing can serve gets a note and a question for the author. Text
   on the picture stays inside the safe zone of every deliverable that shows it.
   *Complete when:* every row carries a framing, and every conflict is a question.

6. **Give every shot a source.** Write `shot-list.md`: the H1 `# <Title> — shot list`, then the
   table `| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |`, one row per
   shot, numbered `S01` onwards, every board row covered by at least one shot. Type is one of
   `camera`, `screen`, `stock`, `still`, `card`, `colour`, `generated`, `scene` or `edited`.
   Source is a footage ID from the manifest (`F0007`), an image or text capture under
   `production/src/assets/`, a card under `production/src/cards/` named `<piece>.<card>.html`
   (made later from the brand's card layout), a colour as `#RRGGBB`,
   `production/src/scenes/<piece>.scene.py`, `to shoot`, or `to render` for an `edited` shot
   until its export is logged; an `edited` shot's Picture names the editor and the motion. Every board
   of a scene piece is Type `scene`; other sources are images or `.txt`, `.ansi`, `.html` captures,
   never video or sound. `cut-for-platform` accepts their hashes with `real` through `-o`.
   Its brief records `ai_visuals: assisted`. Seconds is set for stills, cards and colour clips. Status is
   `needed`, `captured`, `logged` or `cleared`. Never take an image, a clip or a track from the web
   because it is only a draft. Apply the mode file's additions.
   *Complete when:* `shot-list.md` exists, every board row has a shot, and every shot has a type
   and a source.

7. **Open a rights row for everything owned or identifiable.** For every item someone else owns,
   or that shows someone (music, stock, footage of people or private places, a likeness, a cloned
   voice, quoted text, a scripture translation, a font, artwork, a generated image), find its row
   in `production/src/rights-register.md`, or append one with the next permanent ID (`RR0001`
   onwards), its Kind from the register's vocabulary, this piece under Pieces, Status `needed`, and
   every field not yet known written as an `AUTHOR TO CONFIRM` flag. Put the ID in the shot's
   Rights column; a shot needing none reads `—`. Never mark a row `cleared` here: clearing needs
   its evidence (`production/workflows/07-clear-the-rights/`). A generated image or a synthetic
   voice is also noted for the brief's disclosure.
   *Complete when:* every licensed or identifiable shot carries a rights ID, and each of those rows
   exists with Status `needed` or better.

8. **See the boards.** Run `python3 toolkit/media.py boards <piece>`: one still per board at the
   master's size (the edit decision list's size where one exists, else `1920x1080`), a step still
   per build-up, the contact sheet `<piece>.boards.html` and, where a board has motion or a
   build-up, the animatic (silent unless the joined voice exists or `--sound FILE` is given), all
   in `production/src/renders/<piece>/boards/`, never tracked. A real
   card is used only where its `production/src/cards/` HTML already exists; otherwise, and for a
   shot `to shoot` or `to render`, a labelled placeholder held for its time, never an invented image. Open each still by the path
   it printed, never by listing the folder, and report what it shows: framing, safe areas, text
   laid out for its purpose. Report every finding. Fix what the author asks, as a board revision,
   and run it again. Then the author opens the contact sheet in a browser and plays the animatic.
   A scene piece needs the sheet only. Exit 2 (no storyboard, no uv or Chromium, no ffmpeg) names
   what is missing: M3 waits, or the author waives this check on their explicit word, recorded in
   `verified:` with the date and reason. Never report it as seen when it could not run.
   *Complete when:* the author says they have seen the contact sheet and, where one was made, the
   animatic, or has waived the check in their own words.

9. **Check M3 with the author, and record it.** Check the board against M3 as
   `scripts/docs/reference/the-piece-ladder.md` gives it: every spoken line in a row, every row a
   shot with a source, framing for every vertical deliverable, a `needed` rights row for every
   licensed or identifiable item, and the board sheet and any animatic seen (step 8). Show the
   author the board and the shot list, and apply only the changes they agree, raising `version`
   and clearing `approved:` on each revision; a revision that clears M3 needs a new board sheet.
   Only when the author approves, set `approved:` in `storyboard.md` to today's date (DD/MM/YYYY), then set the
   brief's `status: storyboarded`, date `M3` in `verified`, add the new rights IDs to its `rights`
   list, and set `last_updated`. For every non-scene piece, record all four `M4.*` sub-checks
   as `n/a — footage` (or `n/a — no picture` when M3 does not apply). Where M3 does not pass, leave the status at `scripted` and say
   which check failed.
   *Complete when:* the author has approved the board and M3 is dated, or the run has stopped on the
   check that failed.

10. **Hand back.** Report both paths, the contact sheet's and the animatic's paths, the number of
    rows and shots, every shot still `to shoot` (grouped by place, as a shoot list), every shot
    `to render` with its editor, every card to make, every rights row opened, every generated
    picture for the disclosure, every open question, and the next moves: `production/workflows/01-log-source-media/` for footage still
    to log, `production/workflows/02-make-a-voiceover/` where the script has generated lines,
    `production/workflows/07-clear-the-rights/` for the open rows, and then
    `production/workflows/03-assemble-the-master/` (`cut-for-platform`) for footage; a scene
    goes through `production/workflows/09-time-the-voice/` and then
    production/workflows/10-animate-a-scene/.
    *Complete when:* the author has the report, and the brief's status matches the gate that
    passed.

## Anti-patterns

- A spoken line with no picture, or a picture 'to be decided'.
- A shot whose source is 'some stock' with no file, no licence and no rights row.
- Taking an image, a clip or a track from the web because the board is 'only a plan'.
- Framing for the landscape master and hoping the vertical crop will work in the edit.
- Text or a face outside the safe zone of a deliverable that shows it.
- Boarding a recorded piece or an audio-only one, whose M3 does not apply.
- Changing a spoken line to fit a picture: the script is approved, and a change goes back to
  `write-script` with the author.
- Marking a rights row `cleared`, or an identifiable person as consented, without the evidence.
- Planning a motion the edit cannot make, as though the render will find a way.
- Approving a board unseen: M3 is dated only after the author has seen the board sheet and any
  animatic.

## Cross-references

- `write-script` — the approved script this boards, and where a needed change to it goes.
- `cut-for-platform` — turns the shot list into the edit decision list, makes the cards and
  renders the master; the animatic's own list is a working copy it never reads.
- `voiceover` — voices the `VO:` lines the board pictures.
- `repurpose` — the cut-downs, which reuse the vertical framing set here.
- `thumbnail-brief` — the thumbnail, which often starts from a frame this board names.
- `production/src/rights-register.md` — the rows this skill opens;
  `production/workflows/07-clear-the-rights/` clears them.
- `production/src/footage/manifest.toml` — the footage IDs a shot's source names.
