---
name: storyboard
description: >-
  Turn one approved script into a storyboard and a shot list: a picture for every spoken line, the
  framing for every vertical deliverable, the on-screen text, the sound, and a source for every
  shot (footage, a still, a card, a colour clip, or a shot still to film), opening a needed rights
  row for every licensed or identifiable item (M3). Use when the author says 'storyboard the
  explainer', 'what do we show over this line?', 'make a shot list for the shoot', 'plan the
  trailer's stills and cards' or 'how will this crop for a vertical short?'. Never run for a
  recorded piece or a piece with no picture: M3 does not apply. Not for writing or changing the
  script (`write-script`). Not for the edit decision list or a render (`cut-for-platform`). Not for
  planning cut-downs (`repurpose`). Not for a thumbnail (`thumbnail-brief`).
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
(`production/docs/reference/edit-decision-lists.md`); anything else is a shot to film or a
question for the author. <%OWNER_FIRST_NAME%> approves the board, and the approval is what M3
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

The mode file adds this project's kinds of picture, its sources and its domain rules.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece.** Confirm the piece with the author: its folder in `scripts/src/pieces/` and
   its `brief.md`. If the brief has `origin: recorded`, stop: M3 is `n/a — recorded`, recorded by
   `production/workflows/08-bring-in-a-recording/`, and the master is cut from the recording. If
   it has `picture: false`, stop: M3 is `n/a — no picture`. If its `status` is `briefed` (M2 not
   dated), stop: the script comes first (`scripts/workflows/02-write-a-script/`). If
   `storyboard.md` already exists, the request is a revision: change only what the author asks,
   and go to step 8.
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
   `| # | Beat | Time | Picture | Spoken | On screen | Sound | Vertical framing |`. One row per
   picture, numbered `B01` onwards: Beat is the script's beat number; Time is `MM:SS–MM:SS`, from
   the beat targets and the script's timing; Picture says what is seen, in a phrase; Spoken cites
   the lines the picture carries (`2.1–2.3`); On screen carries the script's `TEXT:` cues and any
   name caption; Sound carries the voice, the `SFX:` and `MUSIC:` cues and room tone. Every spoken
   line sits in exactly one row. Apply the mode file's additions.
   *Complete when:* `storyboard.md` exists, and every spoken line of the script is cited by exactly
   one row.

5. **Frame every row for the vertical deliverables.** Fill each row's Vertical framing with
   `centre`, `crop x=<px>` (the crop offset in source pixels) or `pad`, chosen so that faces, hands
   and on-screen text sit inside the safe zone of every vertical deliverable of the brief; where
   the brief has none, frame for a 9:16 cut-down all the same, because the cut-down plan reads this
   column. A row that no single framing can serve gets a note and a question for the author. Text
   on the picture stays inside the safe zone of every deliverable that shows it.
   *Complete when:* every row carries a framing, and every conflict is a question.

6. **Give every shot a source.** Write `shot-list.md`: the H1 `# <Title> — shot list`, then the
   table `| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |`, one row per
   shot, numbered `S01` onwards, every board row covered by at least one shot. Type is one of
   `camera`, `screen`, `stock`, `still`, `card`, `colour` or `generated`. Source is a footage ID
   from the manifest (`F0007`), an asset under `production/src/assets/`, a card under
   `production/src/cards/` named `<piece>.<card>.html` (made later from the brand's card layout), a
   colour as `#RRGGBB`, or `to shoot`. Seconds is set for stills, cards and colour clips. Status is
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

8. **Check M3 with the author, and record it.** Check the board against M3 as
   `scripts/docs/reference/the-piece-ladder.md` gives it: every spoken line in a row, every row a
   shot with a source, framing for every vertical deliverable, and a `needed` rights row for every
   licensed or identifiable item. Show the author the board and the shot list, and apply only the
   changes they agree, raising `version` and clearing `approved:` on each revision. Only when the
   author approves, set `approved:` in `storyboard.md` to today's date (DD/MM/YYYY), then set the
   brief's `status: storyboarded`, date `M3` in `verified`, add the new rights IDs to its `rights`
   list, and set `last_updated`. Where M3 does not pass, leave the status at `scripted` and say
   which check failed.
   *Complete when:* the author has approved the board and M3 is dated, or the run has stopped on the
   check that failed.

9. **Hand back.** Report both paths, the number of rows and shots, every shot still `to shoot`
   (grouped by place, as a shoot list), every card to make, every rights row opened, every
   generated picture for the disclosure, every open question, and the next moves:
   `production/workflows/01-log-source-media/` for footage still to log,
   `production/workflows/02-make-a-voiceover/` where the script has generated lines,
   `production/workflows/07-clear-the-rights/` for the open rows, and then
   `production/workflows/03-assemble-the-master/` (`cut-for-platform`).
   *Complete when:* the author has the report, and the brief's status matches the gate that passed.

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

## Cross-references

- `write-script` — the approved script this boards, and where a needed change to it goes.
- `cut-for-platform` — turns the shot list into the edit decision list and makes the cards.
- `voiceover` — voices the `VO:` lines the board pictures.
- `repurpose` — the cut-downs, which reuse the vertical framing set here.
- `thumbnail-brief` — the thumbnail, which often starts from a frame this board names.
- `production/src/rights-register.md` — the rows this skill opens;
  `production/workflows/07-clear-the-rights/` clears them.
- `production/src/footage/manifest.toml` — the footage IDs a shot's source names.
