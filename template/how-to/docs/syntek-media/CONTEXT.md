# CONTEXT.md — how-to/docs/syntek-media/

syntek-media's guides in the user guide. Each explains one practice of keeping this project in
step with the template: what it is, how this project applies it, which procedure carries it out
and which rule governs it. The guides are template-owned and read-only: read them, and never edit
them, because every full update of the template puts them back as it wrote them.

## Directory Tree

```text
how-to/docs/syntek-media/
├── CONTEXT.md                          ← this file
├── CLAUDE.md                           ← how to use these guides
├── finishing-a-copy.md                 ← what a copy leaves to the author, and finishing it
├── changing-the-answers.md             ← changing an answer through an update, and what a removal deletes
├── reporting-a-template-problem.md     ← telling a template fault from a project edit, and reporting it
├── updating-the-template.md            ← taking the template's improvements, and an update that stopped
└── enabling-a-coding-agent-client.md   ← adding a coding agent's files after the project was made
```

## What's here

- `finishing-a-copy.md`: what the copy has already done, and what stays by hand before the first
  session spends anything. `how-to/workflows/syntek-media/01-finish-a-copy/` carries it out.
- `changing-the-answers.md`: why an answer changes only through an update, how a list answer is
  replaced whole, and what removing a platform or a media kind deletes.
  `how-to/workflows/syntek-media/02-change-the-answers/` carries it out.
- `reporting-a-template-problem.md`: how to tell a fault in the template from an edit in the
  project, what to collect and what never to include.
  `how-to/workflows/syntek-media/03-report-a-template-problem/` carries it out.
- `updating-the-template.md`: what an update changes, the user guide put back included, and what
  to do when an update stops part way. `how-to/workflows/syntek-media/04-update-the-template/`
  carries it out, and `how-to/workflows/syntek-media/05-recover-a-stopped-update/` when an
  update stopped.
- `enabling-a-coding-agent-client.md`: why an update records a client but never writes its
  files, and the fresh-render route that adds them by hand.
  `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/` carries it out.

**Ownership.** Every file here is syntek-media's: template-owned, written by Copier, and put back
by every full update where it differs, your edits and deletions included; what you had stays in
Git. There is no `docs/project/` beside these guides. Where this project works differently from a
guide, the difference is recorded in syntek-author's project settings file, 00-project.md, under
Overrides, where that file is present, and otherwise in `.claude/CLAUDE.md` under the heading
'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10),
never as an edit here.

## Cross-references

- `how-to/workflows/syntek-media/`: the procedures these guides name, with every command.
- `how-to/src/TEMPLATE-GUIDE/syntek-media/`: this template's chapters, which explain the same
  ground for a first read.
- `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`,
  `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` and
  `how-to/src/TEMPLATE-GUIDE/the-data-root.md`: the shared chapters, which explain the machinery
  every template of the family has in common.
- `.claude/rules/syntek-media/`: the rules each guide cites, which win wherever a guide only
  explains.
