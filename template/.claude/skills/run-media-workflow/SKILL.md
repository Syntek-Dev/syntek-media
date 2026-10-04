---
name: run-media-workflow
description: >-
  The media router: turn what the author asks for into one media workflow and run it as written.
  Resolves syntek-author's Workflow aliases first, where present, then each media layer's
  workflows/local/ (a same-named local folder replaces the template's), then its 'You want to… |
  Procedure' table or, without one, its workflow folders; loads STEPS.md with CHECKLIST.md open,
  obeys every M-gate, and hands back with the next deliverable. Use when the author says 'what's
  next for the trailer?', 'carry on with the launch video', 'resume the voiceover', 'resume the
  media work from the handoff', 'run 03-caption-a-piece' or describes video, audio, caption or
  posting work no skill claims. Not for a job a media skill claims by its own triggers
  (`write-script`). Not for writing work (the writing router of syntek-author, where present). Not
  for a social media plan, calendar or bios (the social-media-documents skill (syntek-author),
  where present).
---

# Skill: Run Media Workflow (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

<%OWNER_FIRST_NAME%> rarely names a procedure; they say what they want made. This skill turns the
request into **one** media workflow, looks in the project's own procedures before the template's,
and then runs that workflow exactly as written: `STEPS.md` in order, `CHECKLIST.md` open and ticked
as each item passes, every gate obeyed. It owns no domain and carries no mode file; the workflows,
and the skills each step names, carry the domain. It routes the four media layers only, `brand/`,
`scripts/`, `production/` and `publishing/`; writing work belongs to the writing router of
syntek-author, where present.

Its one bias is towards finished pieces. A session that ends with new folders, briefs and register
rows but no approved script, no approved take, no cut and nothing scheduled has not moved the work:
**scaffolding is not progress**. When two procedures would both serve, the one that brings an
approved deliverable nearer is offered first.

## Governing procedures (route here — do not restate at length)

This skill runs procedures; it never replaces one, and it never paraphrases one from memory.

- syntek-author's project settings file, 00-project.md, where present — its Workflow aliases (a
  template workflow, named by its full folder path, and the project procedure to run instead),
  resolved before anything else; its Memory headings (where the memory headings this skill reads
  live in this project); its Paths (the handoffs folder). It is read at run time, never assumed.
- Each media layer's `workflows/CONTEXT.md` and `workflows/CLAUDE.md` — that layer's index of
  procedures and, in a template index, its 'You want to… | Procedure' table. The layers are listed
  in `.claude/rules/syntek-media/01-layout-and-routing.md` Section 2.
- Each layer's `workflows/local/CONTEXT.md` — the author's own procedures and their overrides,
  read before the template's.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Sections 4, 7 and 10 — local first, frozen
  numbering and full folder names; the routing frontmatter every `STEPS.md` and `CHECKLIST.md`
  carries; and the project settings that outrank these rules.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 1 to 4 — who decides what, the
  production loop the layers' procedures implement, the piece ladder, and credits.
- `scripts/docs/reference/the-piece-ladder.md` — the gates M1 to M7 a procedure cites; never
  restated here.
- `.claude/rules/syntek-media/05-model-allocation.md` — what the checklist model tags mean.

## Steps

1. **Restate the request as one job.** Read the `Status` and `Open questions` headings of
   `.claude/MEMORY.md` (under the headings syntek-author's Memory headings map gives them, where
   present). Where the project keeps handoffs (the folder syntek-author's 00-project.md Paths
   names, where present, otherwise the one `.claude/rules/syntek-media/07-session-boundaries.md`
   Section 2 gives) and holds one newer than the latest `Status` line, read the newest first: its
   In flight anchors and its Next action outrank the briefs; offer to prune it once the work
   lands. Then name the job, the piece and, where it applies, the deliverable or the cut in one
   sentence: 'caption cut c02 of the ferry explainer for Shorts', 'storyboard the next trailer'.
   If the request could be two different jobs, ask one question with your recommended reading and
   its reason, and wait. If the job is writing work, or a social media plan, a content calendar or
   bios, say which skill owns it (the boundaries in this skill's description) and stop.
   *Complete when:* the job is one sentence the author has not contradicted, and any newer
   handoff has been read.

2. **Read the indexes, aliases and local first.** Where syntek-author's 00-project.md is present,
   read its Workflow aliases first: a row whose template workflow is the media procedure that
   matches the job (named by its full folder path, such as `scripts/workflows/02-write-a-script/`)
   names the project procedure to run instead, and that procedure is a candidate ahead of the
   template's, marked as an alias. Then, for each of `brand/`, `scripts/`, `production/` and
   `publishing/`, read `workflows/local/CONTEXT.md`, then `workflows/CONTEXT.md` and
   `workflows/CLAUDE.md`, and list every procedure whose row in the 'You want to… | Procedure'
   table matches the job, with its layer and full folder name. **Where an index has no such
   table** (an index the project rewrote, or one another template wrote), list that layer's
   workflow folders directly, every `NN-name` folder in `workflows/` and in `workflows/local/`,
   and read each one's `CONTEXT.md` for what it does.
   *Complete when:* every candidate is listed by layer and full folder name, aliases and local
   procedures are marked as such, and any layer read by its folders rather than its table is
   named.

3. **Resolve to one procedure.** An alias replaces the template workflow it names. A local folder
   with the same name as a template folder, number included
   (`workflows/local/02-make-a-voiceover/` over `workflows/02-make-a-voiceover/`), replaces it
   entirely. A local procedure with a
   number of its own competes on its row like any other. A workflow is named by its full folder
   name, never by its number alone: where a number the author gives matches more than one folder
   in a layer (a template workflow beside a project's own), list each by full name and ask. If two
   still fit, offer the one that brings an approved deliverable nearer and say why. If none fits,
   say so and stop: never improvise a procedure or stitch two together, and never write a new one
   without the author's agreement (`workflows/local/CLAUDE.md` in the layer says how).
   *Complete when:* one procedure is chosen by its full name, and you can say whether it is an
   alias, local or the template's.

4. **Resolve 'next' from the record, never from memory.** 'What's next?' is answered from a newer
   handoff's Next action (step 1), else from the `Status` heading of `.claude/MEMORY.md`, the
   pieces in `scripts/src/piece-register.md` that are not retired, and each piece's brief: its
   `status` and its `verified` dates. A piece's next move is the procedure that serves the gate
   its `status` reaches next, as `scripts/docs/reference/the-piece-ladder.md` defines the gates:
   - `idea`: `scripts/workflows/01-brief-a-piece/` (M1).
   - `briefed`: `scripts/workflows/02-write-a-script/` for a scripted piece, or
     `production/workflows/08-bring-in-a-recording/` for a recorded one (M2); an audiobook has no
     script, and its plan (the chapter register) and M2 go through the audiobook narration
     procedure, where the project makes audiobooks.
   - `scripted`: `scripts/workflows/03-storyboard-a-piece/` (M3); a piece with `picture: false`
     or `origin: recorded` has M3 `n/a`, recorded with its M2, and goes straight on to its master
     (an audiobook's chapters through the audiobook procedures, where the project makes them).
   - `storyboarded`: `production/workflows/02-make-a-voiceover/` where the script has generated
     lines, `production/workflows/01-log-source-media/` for footage not yet logged, then
     `production/workflows/03-assemble-the-master/` (M4); a podcast episode's master comes from
     the podcast procedure, where the project makes podcasts.
   - `produced`: `publishing/workflows/01-plan-the-cut-downs/`, then
     `publishing/workflows/02-cut-for-a-platform/` (M5).
   - `cut`: `publishing/workflows/03-caption-a-piece/` (M6); a piece whose M6 is `n/a` (an
     audiobook, a podcast without a transcript) goes straight on to M7.
   - `captioned`: `production/workflows/07-clear-the-rights/`,
     `publishing/workflows/04-brief-a-thumbnail/` and `publishing/workflows/05-prepare-a-post/`
     (M7).
   - `scheduled`: `publishing/workflows/06-record-a-publication/`, once the author reports a post.
   The first move offered is the one that brings a finished piece nearer: approve a script or a
   take the author has heard, cut a produced master, caption a cut, or package a captioned piece,
   before opening another piece. If a brief and its files disagree (an approved `script.md` under
   a brief still at `briefed`, a `verified` date with no matching status), report the
   disagreement rather than guess.
   *Complete when:* the target is a named piece (or the brand, for a brand procedure) and the
   gate it is moving towards, read from its brief.

5. **Load the procedure whole.** Read its `CONTEXT.md` and `CLAUDE.md`, then `STEPS.md` with
   `CHECKLIST.md` open beside it. Obey the routing frontmatter: load every skill its `skills:`
   list names, each with its mode file, and note the `model:` tier. A step whose `> **Skill:**`
   line names a companion of syntek-author runs it only where `.claude/skills/<skill>/SKILL.md`
   exists; where it does not, say which skill is missing and follow the step's own fallback. A
   project procedure an alias names may not have the template's four files: read what it has, and
   follow it as written.
   *Complete when:* every file the procedure has is read, every skill named is loaded, and every
   missing companion is named.

6. **Check the pre-conditions and the gates.** Tick each `## Pre-Conditions` item or stop on it.
   Before any step that moves a piece's status, check the gate its `> **See**` line cites in
   `scripts/docs/reference/the-piece-ladder.md`, with any check a same-named guide in
   `scripts/docs/project/` adds (it may add a check, never remove or weaken one); a gate that does
   not pass stops the run there. A gate that does not apply to the piece is recorded `n/a` with
   its reason in the brief's `verified`, never skipped silently. A gate is waived only on the
   author's explicit word, recorded in `verified` as `waived DD/MM/YYYY — reason`.
   *Complete when:* every pre-condition is ticked, or the run has stopped and said why.

7. **Work the steps in order.** Run each step with the skill and the guide its `> **Skill:**` line
   names, at the tier its checklist tag gives, and tick the item only when its test passes. Never
   reorder, merge or skip a step to save time; a step that needs the author's decision asks and
   waits. A step that spends credits states the cost and waits for a yes, every time
   (`.claude/rules/syntek-media/03-production-ethics.md` Section 4). Where a skill's mode file
   disagrees with the procedure, the procedure wins and the disagreement is reported.
   *Complete when:* every step is done, or waived with its reason stated.

8. **Hand back, and point at the next deliverable.** Report the procedure run (alias, local or
   template) by its full folder name, every artefact written with its path, every render made
   (git-ignored and regenerable), any credits spent (from `production/src/credits-log.md`), every
   approved take not yet archived, every item waived and why, every open flag and question, and
   the next procedure: the one the layer's `workflows/CLAUDE.md` gives as usually following, the
   one the last step names, or the one that serves the piece's next gate (step 4), each by its
   full folder name; where none names one, say so. Offer the move that brings the next approved
   deliverable nearer.
   *Complete when:* the hand-back names what changed, what is open and the next move, and nothing
   was approved, spent, scheduled or changed in a guide or a rules file without the author's
   word.

## Anti-patterns

- **Scaffolding as progress.** Opening pieces, briefs, platform profiles, register rows or index
  rows the procedure did not ask for, or re-briefing a piece whose M1 passed while its script
  waits to be written.
- Running a template procedure when an alias or a same-named local one replaces it, or the reverse.
- Naming a workflow by its number alone, or stopping because a layer's index has no table when its
  folders can be listed.
- Working from a remembered version of `STEPS.md`. A remembered procedure is an old procedure.
- Improvising a procedure when none matches, or quietly merging two because each covers half.
- Treating a gate as advice. A gate that 'nearly passes' has not passed, and a gate that does not
  apply is recorded `n/a`, never skipped in silence.
- Ticking checklist items in a batch at the end, or before their tests pass.
- Spending credits, approving a take or a cut, or scheduling a post because the procedure
  'obviously' leads there; each waits for the author's explicit word, and nothing is ever posted
  from here.
- Answering 'what's next?' from the renders and generated audio on disk instead of from the
  handoff, the briefs and memory, or leaving a resumed handoff unpruned once its work has landed.
- Routing writing work, a social media plan or a content calendar through a media procedure.

## Cross-references

- `.claude/rules/syntek-media/02-skills.md` — the media skills that ship in this project, which
  carry a mode file, and the companions of syntek-author.
- `write-script` · `storyboard` · `voiceover` · `cut-for-platform` · `captions` · `repurpose` ·
  `thumbnail-brief` · `prepare-post` — the skills the media procedures name, each that procedure
  in skill form; the audiobook skill ships only where the project makes audiobooks.
- `scripts/docs/reference/the-piece-ladder.md` — the gates M1 to M7, which 'next' follows.
- `scripts/src/piece-register.md` — every piece by number; each brief holds its status.
- `.claude/MEMORY.md` — the `Status` heading, which 'what's next?' reads first.
- The grill-with-docs skill (syntek-author), where present — the interview that opens
  `scripts/workflows/01-brief-a-piece/` and the brand procedures.
- The handoff skill (syntek-author), where present — when a procedure has to stop mid-way at a
  session boundary (`.claude/rules/syntek-media/07-session-boundaries.md`).
