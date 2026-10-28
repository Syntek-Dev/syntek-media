# CONTEXT.md — how-to/workflows/syntek-media/

syntek-media's procedures in the user guide: the steps, with every command, for keeping this
project in step with the template. Each takes one job about the template from start to finish,
for the author to follow or for a session to run with the author, and carries its own commands,
so it works even where a shared chapter is missing. The procedures are template-owned and
read-only: read them, and never edit them, because every full update of the template puts them
back as it wrote them.

## Directory Tree

```text
how-to/workflows/syntek-media/
├── CONTEXT.md                          ← this file
├── CLAUDE.md                           ← how to run one, and the 'You want to…' table
├── 01-finish-a-copy/                   ← CONTEXT · CLAUDE · STEPS · CHECKLIST: a fresh copy, to its first commit
├── 02-change-the-answers/              ← CONTEXT · CLAUDE · STEPS · CHECKLIST: a changed answer, through an update
├── 03-report-a-template-problem/       ← CONTEXT · CLAUDE · STEPS · CHECKLIST: a template fault, drafted as an issue
├── 04-update-the-template/             ← CONTEXT · CLAUDE · STEPS · CHECKLIST: an update, to a commit
├── 05-recover-a-stopped-update/        ← CONTEXT · CLAUDE · STEPS · CHECKLIST: undo a stopped update, and run it again
└── 06-enable-a-coding-agent-client/    ← CONTEXT · CLAUDE · STEPS · CHECKLIST: add a coding agent's files
```

## What's here

- **Each procedure has the same files:** `CONTEXT.md` (when to reach for it), `CLAUDE.md` (how
  to run it), `STEPS.md` (the steps in order, each with its commands) and `CHECKLIST.md` (what to
  confirm before, during and after, each item tagged with its model tier).
- **Every command runs exactly as written**, from the project's top folder, in bash, zsh or
  another POSIX shell. A value the author chooses is named in the sentence before the command.
- **Numbers are frozen and append-only**, counted from 01 in this folder. There is no
  `workflows/local/` here.
- **`run-media-workflow` never routes these.** A session runs one as this folder says, step by
  step with its checklist open, and stops for the owner at every step that changes the
  template's files or a settings file.

**Ownership.** Every file here is syntek-media's: template-owned, written by Copier, and put back
by every full update where it differs, your edits and deletions included; what you had stays in
Git. This project's own way of doing one of these jobs is recorded in syntek-author's project
settings file, 00-project.md, as a Workflow aliases row naming the procedure by its full folder
path, where that file is present, and otherwise in `.claude/CLAUDE.md` under the heading
'Project-specific rules' (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10),
never as an edit here.

## Cross-references

- `how-to/docs/syntek-media/`: the guides these procedures carry out, and why each step is there.
- `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`,
  `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` and
  `how-to/src/TEMPLATE-GUIDE/the-data-root.md`: the shared chapters, which explain the machinery.
- `.claude/syntek-media-agents.md`: the bridge, which gives the same jobs to a coding agent other
  than Claude Code.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 3: the kinds of layer, and why
  `how-to/` is read and never produced in.
