@./CONTEXT.md

# CLAUDE.md — how-to/src/TEMPLATE-GUIDE/syntek-media/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `how-to/CONTEXT.md` →
`how-to/CLAUDE.md` → `how-to/src/CONTEXT.md` → `how-to/src/CLAUDE.md` →
`how-to/src/TEMPLATE-GUIDE/CONTEXT.md` → `how-to/src/TEMPLATE-GUIDE/CLAUDE.md` → this folder's
`CONTEXT.md` (the chapters and the order to read them in, imported above) → this file.

## Purpose (one line)

Answer how the audio and video side of this project works from the chapter that owns the answer,
and route to the rule that decides.

## How to work here

- **Routing:** the table in this folder's `CONTEXT.md` names the chapter for each kind of
  question. Each chapter's 'Where the rules live' names the rules in
  `.claude/rules/syntek-media/`, the guides in `how-to/docs/syntek-media/` and the procedures in
  `how-to/workflows/syntek-media/` behind what it explains, and its 'Next' what to read after
  it.
- **A job a procedure covers** is run from `how-to/workflows/syntek-media/` as that folder says,
  step by step with its checklist open, never through `run-media-workflow`, which does not route
  the guide's procedures.
- **Model:** **Opus**: matching a question to the chapter and the rule that own it is judgement,
  and a wrong answer is acted on with full confidence
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the table → read the chapter → read the rule it routes to → answer
  from the rule, citing the chapter for the explanation → where the answer is a job, run the
  procedure the chapter names.
- **Definition of done:** the question is answered, the deciding rule is cited, and nothing
  under `how-to/` changed except through the template's update, its recovery and the commands
  its update report prints.

## Guardrails

- **Read-only, even when asked.** Never edit, write, move or delete a chapter here, except
  through syntek-media's update, its recovery and the commands its update report prints for a
  file here (taking the template's version, `git add`, removing a `.rej` file). Claude Code's
  deny in `.claude/settings.json` stops it, the guide guard (`.claude/hooks/how-to-read-only.sh`)
  refuses it, and the next update puts the file back
  (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **The rules win over a chapter.** Where a chapter and a rule in `.claude/rules/syntek-media/`
  differ, follow the rule, with syntek-author's project settings file first where it is present,
  and tell the author both locations.
- **Never quote a chapter as a rule.** Cite the rule as the reason for an action; a chapter only
  explains it.
- **Record a departure where the rules say**, never in a chapter: in syntek-author's project
  settings file, under Overrides or Workflow aliases, where it is present, and otherwise in
  `.claude/CLAUDE.md` under the heading 'Project-specific rules'
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).
- **Never add a chapter here.** The author's own guides and notes go in a layer's
  `docs/project/`, and procedures in its `workflows/local/`.

## Output & naming

- **Writes nothing.** Every chapter here is the template's.
- **Names:** `NN-kebab-title.md`, numbered from 01. Numbers are frozen and append-only.
- **Shape:** each chapter opens with its title and a short gloss, carries no header, no
  frontmatter and no template token, holds one sentence per line, and ends with 'Where the rules
  live' and then 'Next'.
