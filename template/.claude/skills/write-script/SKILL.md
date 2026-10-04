---
name: write-script
description: >-
  Write the spoken script for one scripted piece from its agreed brief: the hook in the first
  seconds, one beat per heading, one spoken sentence per line with speaker tags, cue lines and
  braced directions, timed with media.py script time against the brief's target and every
  deliverable's limit, then revised on the author's notes until the author approves it (M2).
  Adapts written work the brief names, reading it and never editing it. Use when the author says
  'write the script for the explainer', 'script the trailer', 'turn chapter 3 into a two-minute
  talk', 'give me a 30-second hook', 'cut the script to 45 seconds' or 'revise the script with
  these notes'. Not for a recorded piece's transcript (`captions`). Not for the storyboard or shot
  list (`storyboard`). Not for proofreading (the spelling and grammar skills of
  syntek-author, where present). Not for a text-only post (the social-media-documents skill
  (syntek-author), where present).
---

# Skill: Write Script (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

A script is written for the ear. Every line is one spoken sentence, heard once and at speed by the
viewer or listener of the audience test (`.claude/rules/syntek-media/01-layout-and-routing.md`
Section 1), and every word in it is something a voice will say, a caption will show and a
storyboard will have to picture. This skill writes the script for **one** scripted piece from its
agreed brief, times it against the brief and the deliverables, and revises it on
<%OWNER_FIRST_NAME%>'s notes. **Nothing in a script is settled until the author approves it**: the
approval date is the record M2 reads, and only the author gives it.

A recorded piece has no script. Its transcript, made from the recording, stands in for one, and
`captions` makes it in `production/workflows/08-bring-in-a-recording/`. Nor has an audiobook: its
chapter register is its plan and its M2, and its text is read from the book, both through the
audiobook procedures, where the project makes audiobooks.

## Governing procedures (route here — do not restate at length)

- `scripts/workflows/02-write-a-script/` — this skill is that procedure in skill form. Run its
  `STEPS.md` with `CHECKLIST.md` open.
- If the layer's `workflows/local/` holds a folder with the same `NN-name` as the procedure above,
  follow that procedure instead: the author's local procedure replaces the template's
  (`run-media-workflow`, step 2).
- `scripts/docs/reference/writing-for-the-ear.md` — the script format (beat headings, speaker
  tags, cue lines, braced directions, `beat.line` citations) and timing.
- `scripts/docs/reference/the-piece-ladder.md` — M2 (briefed → scripted), what approval needs;
  never restated here.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 1, 7 and 8 — who decides what,
  never fabricate, and the two flags.
- `.claude/rules/syntek-media/02-skills.md` Section 4 — how each companion of syntek-author
  applies to a script: as a report, with agreed edits only and no ledger entry.
- `brand/src/voice/voice.md` — the spoken style, the pace, how the brand name is said, the words
  never said aloud, and every pronunciation, which never goes in the script.
- The guide in `scripts/docs/reference/` for each kind of piece this project makes (short video,
  long video, podcast episodes, trailers, standalone voiceovers), named here in prose because
  each ships only with its kind.

The mode file adds this project's kinds of piece, what each draws on, and its domain rules.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece.** Confirm the piece with the author: its folder in `scripts/src/pieces/`, its
   `brief.md` and its `kind`. The brief's `origin` must be `scripted`; for `origin: recorded`,
   stop and route to `production/workflows/08-bring-in-a-recording/`. For `kind: audiobook`, stop
   and route to the audiobook narration procedure, where the project makes audiobooks: this skill
   never writes an audiobook's credits, chapter plan or text. If the brief's `status` is
   `idea` (M1 not dated in `verified`), stop: the brief comes first
   (`scripts/workflows/01-brief-a-piece/`). If `script.md` already exists, the request is a
   revision: confirm which notes the author wants applied, and go to step 9. If the author has
   written the script themselves, it is put on record at step 5, word for word.
   *Complete when:* the piece, its kind and its origin are confirmed, M1 is dated, and the run is
   known to be a first script, the author's own script or a revision.

2. **Read the brief, the voice and the guides.** Read the brief whole: its `## Purpose`,
   `## Audience`, `## Hook`, `## Key points`, `## Call to action`, `## Disclosure plan`,
   `## Rights needs`, `## Draws on` and `## Notes`, and its `deliverables`, `target_seconds`,
   `words_per_minute`, `source` and `synthetic_voice`. Read `brand/src/voice/voice.md`, and the
   written voice it points to where syntek-author's is present. Read
   `scripts/docs/reference/writing-for-the-ear.md` and the guide for the piece's kind, where this
   project ships it. For each deliverable, run `python3 toolkit/media.py presets <key>` and note
   its `max_seconds`.
   *Complete when:* each is read, and the target in seconds, the words it allows at the brief's
   pace and every deliverable's limit are written down.

3. **Gather the material and check every claim.** Read what the brief draws on, and its `source`
   where it names one: written work is read where it lies and never edited, in syntek-author's
   layers as anywhere else. List every factual claim, figure, date, name and quotation the script
   will make, and take each from its source, never from memory. Run each checkable claim through
   the fact-check skill (syntek-author), where present: check that `.claude/skills/<skill>/SKILL.md`
   exists before naming it, and where it does not, say so. A claim that cannot be settled now goes
   into the script carrying `VERIFY`, or stays out; decide which against the brief. List, too,
   everything spoken that someone else owns (a quoted line, a lyric, a translation), so its
   rights row can be opened.
   *Complete when:* every claim has a verdict or a decision to flag it or leave it out, and the
   list of owned material is written down.

4. **Confirm nothing will be clobbered.** Check that the piece folder holds no `script.md`, or that
   the author has confirmed, in this conversation, a rewrite over it. A script is never overwritten
   without that word.
   *Complete when:* the path is free, or the author has confirmed a rewrite over it.

5. **Write the script.** Write the frontmatter: `piece` (the folder name), `version: 1`, an empty
   `approved:`, and `words` and `estimated_seconds`, which step 7 fills. Then the H1
   `# <Title> — script`, and one H2 per beat, `## N. <Beat name> (target MM:SS)`, the target being
   that beat's own running time, so the beats' targets add up to the brief's `target_seconds`: the
   hook first; one beat per key point of the brief; the call to action last. Under each beat write
   one spoken sentence per line, opening with an upper-case speaker tag and a colon (`VO:`, `ON:`,
   `HOST:`, `GUEST:`, `NARRATOR:` or a character's name); cue lines for what is shown or heard but
   never spoken (`TEXT:`, `SFX:`, `MUSIC:`, `NOTE:`); and delivery directions in braces at the
   start of a line or before a phrase (`{softly}`, `{pause 0.6}`). No IPA and no respelling
   (pronunciations live in `voice.md`), and no stage direction outside braces or cue lines. The
   author's own script is put into this format without changing a spoken word; every other change
   to it is a proposal at step 9. Apply the mode file's additions.
   *Complete when:* `script.md` exists, every key point of the brief has its beat, the hook and the
   call to action are where the brief puts them, and every line is a heading, a spoken line or a
   cue.

6. **Flag what is unchecked or undecided.** Put `<!-- VERIFY: … -->` at each claim not yet
   checked, saying what needs checking, and `<!-- AUTHOR TO CONFIRM: … -->` at each decision only
   the author can make, worded so it can be answered cold. A deviation the author has authorised
   goes in `<!-- INTERNAL NOTE: … -->` under the frontmatter. Every name or term whose
   pronunciation `voice.md` does not yet record is listed for the hand-back, never respelled in
   the script.
   *Complete when:* nothing uncertain in the script reads as settled.

7. **Time it.** Run `python3 toolkit/media.py script time <script> --write`. It reads the brief's
   `words_per_minute` itself (150 where the brief sets none; `--wpm` overrides both) and reports
   each beat against its own target. Exit 0 records `words` and `estimated_seconds` in the
   frontmatter. Exit 1 means the total misses the brief's target by more than 10%, or runs past a
   deliverable's limit: cut or add where the per-beat timings show the weight, and run it again,
   never by asking for a faster read. Where pictures carry a beat (a trailer of stills and cards),
   hold them with a `{pause S}` at the end of a line, which the count includes, never with words. If the script cannot fit without losing something the brief
   asked for, say which key point would go and let the author choose, or change the brief's target.
   Exit 2 means it could not run: say why, and stop.
   *Complete when:* `script time` exits 0, and the frontmatter holds its `words` and
   `estimated_seconds`.

8. **Run the companions, as reports.** For each of these, check that its
   `.claude/skills/<skill>/SKILL.md` exists first, and name any that is missing: the spelling and
   grammar skills (syntek-author), where present, as one supportive report; the comprehension
   skill (syntek-author), where present, read as the audience test's viewer or listener; and the
   flow skill (syntek-author), where present, on order, rhythm and repetition across the beats.
   Present every finding numbered, with its line (`beat.line`) and a proposed fix, and apply only
   what the author accepts; a companion's own ledger or status step is skipped, and said so
   before it runs. Where none is present, say so, and offer a read-aloud check only if the author
   asks.
   *Complete when:* every present companion has reported, every finding is accepted or declined,
   and every missing one is named.

9. **Revise on the author's notes.** The author reads the script, aloud where they can, and gives
   notes. Apply each note as an agreed edit, one sentence per line, and show the changed lines.
   For a fuller pass, the improve-section skill (syntek-author), where present, runs on a script
   the author wrote and the adapt-section skill (syntek-author), where present, on notes, each as
   report-then-agreed-edit with no ledger entry and no status change, said so before it runs;
   where neither is present or one refuses a file that is not a section draft, this step is the
   route. Never change a figure, a quotation, a commitment or the call to action without the
   author's word. Raise `version` on each revision, clear `approved:` if it was set, and time it
   again (step 7).
   *Complete when:* every note is applied or answered, the script is timed again, and the author
   has seen every changed line.

10. **Record the approval and hand back.** Only when the author says the script is approved, set
    `approved:` to today's date (DD/MM/YYYY), then check M2 as
    `scripts/docs/reference/the-piece-ladder.md` gives it: `python3 toolkit/media.py flags` on the
    script finds nothing, `script time` exits 0, every companion finding is decided and every claim
    is verified or cut. Where M2 passes, set the brief's `status: scripted`, date `M2` in
    `verified` and set `last_updated`; where the brief has `picture: false` (no deliverable
    carries a picture), record `M3: 'n/a — no picture'` in `verified` at the same time and say so,
    because no storyboard will ever be made for it. Where M2 does not pass, leave the status at
    `briefed` and say which check failed. Report the path, the words and estimated seconds against
    the target and each deliverable's limit, every flag with its question, the sources used, the
    names for `voice.md`, the owned material for the rights register, any step waived and why, and
    the next move: `scripts/workflows/03-storyboard-a-piece/` (`storyboard`), or, for a piece with
    `picture: false`, `production/workflows/02-make-a-voiceover/` and then
    `production/workflows/03-assemble-the-master/` (an audio master), or the podcast procedure,
    where the project makes podcasts.
    *Complete when:* the author has the report, and the brief's status matches the gate that
    passed.

## Anti-patterns

- Writing a script for a recorded piece, or for a piece whose brief is not agreed.
- Writing for the eye: a sentence that needs a second reading, a parenthesis, a list read aloud,
  or a figure the ear cannot hold.
- Writing a quotation, figure, date, name or result from memory, however sure it feels.
- Filling a gap with a plausible line instead of a flag. A fluent invention survives every pass.
- Putting IPA or a respelling in the script, or a direction outside braces, so the captions and the
  voice both say it.
- Meeting the time by asking for a faster read, or by quietly dropping a key point the brief needs.
- Editing the written work the script adapts, or scripting an audiobook, whose plan and text
  belong to its narration procedure.
- Applying a companion's findings, or a revision, before the author has answered.
- Setting `approved:` or the brief's status because the author said the script 'looks fine'
  rather than that it is approved.

## Cross-references

- `storyboard` — the next move on an approved script: a picture for every spoken line.
- `voiceover` — voices the approved `VO:` lines, one segment per sentence or beat.
- `captions` — a recorded piece's transcript, and the captions whose words must match the script.
- `repurpose` — plans cut-downs by the script's `beat.line` citations.
- `run-media-workflow` — routes here from 'what's next?' when a briefed piece waits for its script.
- The fact-check, spelling, grammar, comprehension, flow, improve-section and adapt-section skills
  (syntek-author), where present — the reports in steps 3, 8 and 9.
- `scripts/src/pieces/` — the piece folders; each holds its brief and, once written, its script.
