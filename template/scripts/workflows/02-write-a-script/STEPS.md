---
workflow: 02-write-a-script
phase: produce
skills: [write-script]
model: opus
---

# STEPS.md — write a script, from agreed brief to approved script

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for writing one scripted piece's words, checking them, timing them and
taking them to the author's approval. Each step names the skill and guide it uses. **Run in
order** — the ordering is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The
> `write-script` skill is this procedure in skill form; read it and its mode file before step 1.
> Before naming a companion of syntek-author in any step, check that its `SKILL.md` is in
> `.claude/skills/`; where it is not, say which skill is missing and follow the step's fallback.

## 1. Confirm the piece is ready for a script

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the piece's brief in `scripts/src/pieces/<piece>/`. It is at `briefed` with M1 dated and
`origin: scripted`. A piece still at `idea` goes back to `scripts/workflows/01-brief-a-piece/`;
a recorded piece is never scripted, because its words come from its transcript
(`production/workflows/08-bring-in-a-recording/`); an audiobook has no script, and its plan and
M2 go through the audiobook procedures, where the project makes audiobooks. _Mechanical._

## 2. Confirm you will not clobber a script

> **Skill:** none · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Look for `script.md` in the piece's folder. If it exists, this run revises it: read it in full,
note its `version` and whether it is `approved`, and confirm with the author before changing
anything. Revising an approved script clears M2 and every later gate (the ladder guide); say so
before the first change. _Mechanical._

## 3. Read the brief, the voice and the guides

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Read the brief in full; `brand/src/voice/voice.md` (the spoken style, how the brand name is said,
the words never said aloud, the pronunciations) and the written voice it points to, where
present; this procedure's guide and the guide for the piece's kind, where the project makes that
kind (listed in `scripts/docs/reference/CONTEXT.md`); any parent piece's script; and the written
work named in `source`, which is read and never edited. _Substantive._

## 4. Check the claims before writing

> **Skill:** fact-check (syntek-author), where present · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

List every factual claim the script will make: figures, dates, quotations, names, statements
about a product, a policy or a person. Check each with the fact-check skill (syntek-author),
where present, or against a source the author names. A claim that cannot be checked yet goes in
flagged `<!-- VERIFY: … -->` or stays out, and the hand-back says which. Never invent a
statistic, quotation, testimonial or endorsement
(`.claude/rules/syntek-media/03-production-ethics.md` Section 7). _Substantive._

## 5. Write the script

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Write `script.md` in the guide's format: frontmatter `piece`, `version: 1`, an empty `approved:`,
`words` and `estimated_seconds`; the H1; one H2 per beat with its target (that beat's own
running time, the targets adding up to `target_seconds`); one spoken
sentence per line, every line tagged, every direction in braces. Build the beats from the brief:
the hook in the first line, the key points in order, the call to action last. Anything only the
author can decide is `<!-- AUTHOR TO CONFIRM: … -->`. _Substantive._

## 6. Time it

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Run `python3 toolkit/media.py script time scripts/src/pieces/<piece>/script.md --write`; it
times at the brief's `words_per_minute`. The total sits within 10% of `target_seconds` and inside
every deliverable's `max_seconds`; read the
per-beat figures against each beat's target. A script that runs long is cut or reshaped with the
author, never fitted by raising the rate. If the command cannot run, say why and which tool is
missing; never report a timing it did not produce. _Mechanical (running); the cut is
substantive._

## 7. Run the companion reports

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Run the spelling and grammar skills, the comprehension skill (reading as the brand's audience
test, `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1), the flow skill and the
fact-check skill (syntek-author), where present, as reports on the script. Present the findings
together and let the author decide each one. Where a companion is absent, say which, and offer a
read-aloud check only if the author asks (`.claude/rules/syntek-media/06-global-rules.md`
Section 7). _Substantive._

## 8. Revise on the author's notes

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/writing-for-the-ear.md`

Apply the author's notes and the findings they accepted, and nothing else. The improve-section
and adapt-section skills (syntek-author), where present, help only as report-then-agreed-edit:
say before either runs that it makes no ledger entry and changes no status, and use
`write-script`'s own revise step where one declines a file that is not a section. Raise `version`
on each revision, and run step 6 again after any change to the words. _Substantive._

## 9. Record approval and M2

> **Skill:** `write-script` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Run `python3 toolkit/media.py flags scripts/src/pieces/<piece>/` and resolve every flag with the
author. Check M2 (briefed → scripted) against the ladder guide, item by item, for a scripted
piece. When the author approves the script, date `approved:` in it, set the brief's
`status: scripted`, record `M2` with today's date in `verified`, and update `last_updated`. For a
piece with `picture: false`, record `M3: 'n/a — no picture'` beside it now and say so: M3 never
applies to it, and `storyboard` refuses it. _Mechanical (recording); the approval is the author's._

## 10. Hand on

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Tell the author what is approved, how long it runs, which companions ran and what was waived.
For a piece with pictures, name `scripts/workflows/03-storyboard-a-piece/` next. For a piece
with `picture: false` (its M3 recorded at step 9; the status stays `scripted` until M4), name
`production/workflows/02-make-a-voiceover/` where the script is to be voiced, then
`production/workflows/03-assemble-the-master/` for its audio master, or the podcast procedure,
where the project makes podcasts. Offer to start it. _Substantive._
