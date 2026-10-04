@./CONTEXT.md

# CLAUDE.md — .claude/skills/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `.claude/CONTEXT.md` →
this folder's `CONTEXT.md` (the folder layout, imported above) → this file.

## Purpose (one line)

Run each skill as written, and keep the template's skills unchanged so that `copier update` can
keep improving them.

## How to work here

- **Routing:** to find the right skill, read the roster of the template the job belongs to,
  `.claude/rules/<template>/02-skills.md` (for media work,
  `.claude/rules/syntek-media/02-skills.md`), or let that template's router resolve the job to a
  workflow, which names its skills (for media work, `run-media-workflow`). To change how a
  template skill behaves in this project, write a project rule or an override where that
  template's rules say (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).
- **Model:** **Opus** for any change in this folder; a skill's own steps name their tier
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:** read the whole `SKILL.md`, then its mode file if the `SKILL.md` carries the
  Mode paragraph → take project values from where the template's rules say → follow the steps in
  order, each to its completion test → cite, rather than restate, the procedures it routes to.
- **Definition of done:** the skill's own completion tests pass, and nothing under
  `.claude/skills/` changed unless the author asked for that change.

## Guardrails

- **Never edit a template skill.** The next `copier update` overwrites the edit or turns it into a
  conflict, and a skill changed mid-task to fit the task is a skill nobody can trust.
- **Never self-edit.** No skill rewrites a skill, a guide, a rules file or a `CLAUDE.md` without
  the author's explicit instruction (`.claude/rules/syntek-media/06-global-rules.md` Section 3).
- **Never recreate a skill that does not ship here.** Its absence is deliberate for this kind of
  project, or it belongs to a template that is not applied; say which skill is missing instead.
- **A skill of the author's own** takes a folder name no template skill uses, frontmatter `name`
  equal to the folder, and a `description` of at most 1,024 characters naming its job, its
  triggers and the skills it is not.

## Output & naming

- **Hand-written:** each `SKILL.md`, its mode file and any sub-documents. Nothing here is
  generated.
- Skill folders are kebab-case and named as the skill; the entry file is always `SKILL.md`; mode
  files and sub-documents are `SCREAMING-SNAKE-CASE.md`.
