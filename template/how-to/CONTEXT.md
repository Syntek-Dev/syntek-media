# CONTEXT.md — how-to/

The user guide for this project: the chapters, guides and procedures of each template applied
here, which explain how the project works and how to keep it in step with its templates. It is a
shared reference folder, not a production layer: nothing in it is the work. It is read-only:
read it, and never edit it.

## Directory Tree

```text
how-to/
├── CONTEXT.md        ← this file (shared)
├── CLAUDE.md         ← how to read the guide (shared)
├── docs/             ← each template's guides, in a folder named for it
├── src/              ← the chapters: TEMPLATE-GUIDE/ holds the shared ones and each template's folder
└── workflows/        ← each template's procedures, in a folder named for it
```

## What's here

- **Chapters** (`how-to/src/TEMPLATE-GUIDE/`) explain, in plain English, how the project works.
  The shared chapters cover what every template has in common: the coding agents and MCP
  servers, the data root, and updating. Each template's own chapters are numbered from 01.
- **Guides** (`how-to/docs/`) explain one practice each, such as updating, and name the
  procedure that carries it out.
- **Procedures** (`how-to/workflows/`) each give the steps, with every command, for one job about
  the project's template, such as updating it, for you or a session to follow.
- **Naming.** A template's own folder carries its exact name, the name in its answers file
  `.copier-answers.<template>.yml` and in its rules folder under `.claude/rules/`. Shared files
  sit outside every template's folder.
- **Where to start.** The lowest-numbered chapter in your template's folder under
  `how-to/src/TEMPLATE-GUIDE/`; that folder's `CONTEXT.md` gives the reading order.

**Ownership.** Every file here belongs to a template. The shared files (the pairs of this folder,
`docs/`, `src/`, `src/TEMPLATE-GUIDE/` and `workflows/`, and the shared chapters) are the same
bytes in every template of the family that ships them, and the first template applied to the
project writes them. Each template's own files lie only under folders named for it. The guide is
read-only: Claude Code is denied edits here, and a hook refuses them. Every update of a template
puts its files back as it wrote them, the shared ones included, brings back any you deleted, and
lists each in its report; what you had stays in Git. A shared file holding another template's
version waits for that template's update and is never put back to an older version while it
stands unchanged. Only a template's update, its recovery and the commands its report prints
change a file here. A file of yours here belongs to no template and no update touches it, but no
session can edit it either: keep your own notes where your project's rules say. To work
differently from the guide, record the difference where the project's rules in `.claude/rules/`
say a departure from the guide is recorded.

## Cross-references

- `how-to/src/TEMPLATE-GUIDE/CONTEXT.md`: where reading starts.
- `.claude/rules/`: the project's rules, which decide wherever a chapter only explains, and which
  say where a departure from the guide is recorded.
- Every `.claude/syntek-*-agents.md`: the bridge each template ships for the coding agents other
  than Claude Code, which also says the guide is read-only.
- `.claude/hooks/how-to-read-only.sh`: the hook that refuses a session's edits and writes here.
- `.claude/settings.json`: the deny rule that stops Claude Code's file tools editing or writing
  in this folder; reading it stays open.
