---
workflow: 01-brief-a-piece
phase: plan
skills: []
model: opus
---

# STEPS.md — brief a piece, from idea to an agreed brief

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for taking one piece from an idea to a brief the author has agreed, in a
folder of its own. Each step names the skill and guide it uses. **Run in order** — the ordering
is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No media skill
> runs this procedure. The grill-with-docs skill (syntek-author), where present, runs the
> questioning in steps 3 to 7 and 10: check that its `SKILL.md` is in `.claude/skills/` before
> step 3, and where it is not, say so and ask the same questions in rounds yourself, each with a
> recommended answer (`.claude/rules/syntek-media/06-global-rules.md` Section 8).

## 1. Name the piece and take its number

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Confirm with the author what the piece is, in one sentence, and its working title. Read
`scripts/src/piece-register.md`: a new piece takes the next free number, three digits, and a
kebab-case name, `NNN-kebab-title`. A number is never reused, and number 000 belongs to the
worked example. If the idea is a stretch of a piece that already exists, stop: a cut-down is not
a piece, and it is planned in `publishing/workflows/01-plan-the-cut-downs/`. _Substantive._

## 2. Confirm you will not clobber a brief

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Look for the piece's folder in `scripts/src/pieces/`. If it exists, this run re-briefs it: read
the brief in full, list every gate already dated in `verified`, and confirm with the author
before changing anything. The number and the folder name are kept. A change to something a
dated gate checked clears that gate and every later one, as the ladder guide says; tell the
author which before making it. _Mechanical._

## 3. Read what the repository already knows

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read `.claude/MEMORY.md` (Decisions, Open questions and Sensitivities, under the headings
syntek-author's project settings file, 00-project.md, maps them to, where present); the brand,
its audience test included, in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1;
the platform profiles in `brand/src/platforms/`, and in a business project the social media plan
and content calendar of syntek-author, where present; `brand/src/voice/voice.md`; any parent
piece's brief; and the written work the piece adapts, which is read and never edited. A question
the repository can answer is never put to the author. _Substantive._

## 4. Settle the purpose, the audience and the hook

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Question the author until three slots can be written. **Purpose:** what the viewer or listener
can do, believe or feel at the end that they could not at the start. **Audience:** who it is
for, written only where it differs from the brand's audience test. **Hook:** the first line or
image, in one sentence. _Substantive._

## 5. Settle the kind, the origin and the deliverables

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Fix `kind`, `origin` (`scripted`, or `recorded` for a talk, interview or conversation that
exists as a recording) and `picture`, and read the guide for that kind, where the project makes
it (listed in `scripts/docs/reference/CONTEXT.md`). List `deliverables` as full-length keys of
`toolkit/data/platforms.toml` on the project's platforms (`python3 toolkit/media.py presets`
prints them), or `audiobook.<store>` keys for an audiobook; cut-downs are planned later, never
here. Set `target_seconds` inside every deliverable's `max_seconds`, and `words_per_minute` from
the voice file's spoken style, or 150. For a recorded piece, `source_media` lists the recording's
footage IDs once it is logged, and stays `[]` until then. _Substantive._

## 6. Settle the key points and the call to action

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Under `## Key points`, the points the piece must make, in order, one line each; under
`## Call to action`, the one thing the viewer or listener is asked to do. Under `## Draws on`,
the research, written work and earlier pieces it uses, with `parent` and `source` set where it
has them. A claim the piece will make that is not yet checked goes under `## Notes` as a task for
the script stage, where M2 needs every factual claim verified or cut: the brief carries no flag,
and a point the author cannot yet decide keeps the piece at `idea`. _Substantive._

## 7. Settle the disclosure plan and the rights needs

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `publishing/docs/reference/ai-disclosure.md`

Fix `synthetic_voice`, `ai_visuals` and `music` from the vocabularies in the brief skeleton
(`scripts/src/pieces/CLAUDE.md`). Under `## Disclosure plan`, write for each deliverable what
its platform's rule needs, the description line that is always added, and, for a podcast, the
line spoken in the audio. Under `## Rights needs`, list every licensed or identifiable thing the
piece will use (`production/docs/reference/rights-and-consent.md`); `rights:` lists the
rights-register IDs it reuses, and new rows are opened when it is boarded or its rights are
cleared. A cloned voice, the author's own included, needs the person's recorded consent before
anything is made (`.claude/rules/syntek-media/03-production-ethics.md` Section 6).
_Substantive._

## 8. Open the folder and write the brief

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Create `scripts/src/pieces/<piece>/` with its `CONTEXT.md` and `CLAUDE.md` from the pair
skeleton in `scripts/src/pieces/CLAUDE.md`, every slot filled from what was settled. Write
`brief.md` from the brief skeleton fenced in the same file: every frontmatter field,
`status: idea`, `verified: {}`, `last_updated` today, then the title and the nine H2s, one
sentence per line. Add the register row: number, piece, kind, origin, parent and the date
opened. For a re-brief, change the brief in place and leave the pair and the register row as they
are unless the author says otherwise. _Mechanical._

## 9. Read it back and record M1

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the brief back to the author and apply their corrections. Check M1 (idea → briefed)
against the ladder guide, item by item. When the author agrees the brief, M1 has passed: set
`status: briefed`, record `M1` with today's date in `verified`, and update `last_updated`.
_Mechanical (writing); the read-back is substantive._

## 10. Record what was decided

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Decisions that pass the memory gate (`.claude/rules/syntek-media/08-naming-and-memory.md`
Section 3) go to `.claude/MEMORY.md` Decisions, dated; questions left open go to Open questions,
each under the heading syntek-author's Memory headings map gives, where present. Everything else
stays in the brief. _Substantive._

## 11. Hand on

> **Skill:** none · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Tell the author what is briefed and what is still open. Name the next procedure by its full
folder name: `scripts/workflows/02-write-a-script/` for a scripted piece, or
`production/workflows/08-bring-in-a-recording/` for a recorded one; an audiobook's credits and
chapter plan go through the audiobook procedures, where the project makes audiobooks. Offer to
start it: a brief that never reaches a script or a recording has not done its job.
_Substantive._
