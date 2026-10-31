# CONTEXT.md — .claude/skills/

The project's skills: one folder per skill, each the procedure for one kind of job, from writing a
script to cutting a piece for a platform. This file describes how the folder is laid out. The
roster of each template applied to this project (which of its skills ship here, what each does
and which carry a mode file) lives in one place only, that template's
`.claude/rules/<template>/02-skills.md`, so that it cannot drift from a copy kept here.

## Directory Tree

```text
.claude/skills/
├── CONTEXT.md            ← this file
├── CLAUDE.md             ← operating rules for this folder
└── <skill>/              ← one folder per skill, named as the skill (template-owned; see below)
    ├── SKILL.md          ← the procedure: frontmatter, steps, anti-patterns, cross-references
    ├── BUSINESS.md | FICTION.md | NONFICTION.md   ← media's one mode file, for a moded media skill
    ├── MEDIA-BUSINESS.md | MEDIA-FICTION.md | MEDIA-NONFICTION.md   ← media's one mode file, beside a family-shared skill
    └── <SUB-DOCUMENT>.md ← optional, behind SKILL.md when a skill outgrows 300 lines
```

## What's here

- **Template skills** — every folder listed in a template's roster; for this template,
  `.claude/rules/syntek-media/02-skills.md`. They are template-owned: `copier update` replaces
  them, and the inside of a skill folder carries no `CONTEXT.md` or `CLAUDE.md`, because a skill
  is its own manual.
- **Family-shared skills** — seven of them (`grill-me`, `grill-with-docs`, `grilling`, `handoff`,
  `wait-what`, `wayfinder`, `to-questionnaire`) have a `SKILL.md` that every Syntek template ships
  byte for byte, so a project with two templates keeps one copy. A copy writes each one where it
  is absent, and every update that runs the family update script replaces one you never
  changed, writes one the project never had, and keeps and reports one you edited; one you
  delete stays deleted. Each names folders by role, and
  `.claude/rules/syntek-media/02-skills.md` Section 4 gives each role its media path. All seven
  carry the neutral Mode paragraph.
- **Mode files** — a moded skill's `SKILL.md` is the same in every kind of project; the domain
  (paths, the unit, extra reads, domain rules, examples) lives in the mode file that ships
  beside it: for a media skill, `BUSINESS.md`, `FICTION.md` or `NONFICTION.md`; beside a
  family-shared skill, one per template, media's named `MEDIA-BUSINESS.md`, `MEDIA-FICTION.md`
  or `MEDIA-NONFICTION.md`. Another template's mode files there apply only to that template's
  work (`.claude/rules/syntek-media/02-skills.md` Section 2). A mode file applies only beside a
  `SKILL.md` that carries a Mode paragraph: where the project keeps its own skill under a
  template skill's name, that skill ignores the mode file.
- **The author's own skills** — any folder whose name is in no template's roster. They belong to
  the project, and Copier never touches them.
- **Project values** — no skill holds a project's settings. Each reads them where its template's
  rules say: for media skills, the brand brief in Section 1 of
  `.claude/rules/syntek-media/01-layout-and-routing.md`, and project rules and overrides where
  its Section 10 says.

## Cross-references

- `.claude/rules/syntek-media/02-skills.md` — this template's roster, the family-shared skills'
  roles and the mode-file contract.
- `.claude/rules/syntek-media/06-global-rules.md` — never self-edit (Section 3).
- `.claude/rules/syntek-media/01-layout-and-routing.md` — where project rules and overrides live
  (Section 10).
