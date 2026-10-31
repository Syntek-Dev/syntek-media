# CONTEXT.md — how-to/src/TEMPLATE-GUIDE/

Where reading the user guide starts. The shared chapters here explain what every template of
the family has in common; each template's own chapters, numbered from 01, sit in a folder named
for it. Every chapter is plain English for the person the project belongs to, written one
sentence per line. Like the rest of `how-to/`, this folder is read-only: read it, and never edit
it.

## Directory Tree

```text
how-to/src/TEMPLATE-GUIDE/
├── CONTEXT.md                  ← this file: which chapter to read for what (shared)
├── CLAUDE.md                   ← how to read the chapters (shared)
├── agent-clients-and-mcp.md    ← Claude Code, the other coding agents and the two MCP servers (shared)
├── the-data-root.md            ← where binary files live, and why (shared)
├── updating-and-recovery.md    ← what an update does, and getting back from one that stopped (shared)
└── <template>/                 ← each template's chapters, numbered from 01, with that folder's pair
```

## What's here

| You are… | Read |
|---|---|
| New to the project | the lowest-numbered chapter in your template's folder here |
| Updating, or an update stopped | `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` |
| Adding a coding agent | `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` |
| Keeping binary files on a data root | `how-to/src/TEMPLATE-GUIDE/the-data-root.md` |
| Anything else | your template's folder here |

- **A chapter explains; the rules decide.** Each chapter ends with 'Where the rules live', which
  names the rules that decide what it explains, and 'Next', which names what to read after it.
- **Your template's folder** is named exactly as its answers file
  `.copier-answers.<template>.yml` names it; its `CONTEXT.md` gives that template's reading
  order.
- **The shared chapters** name no template: where a step needs your template's name, they send
  you to your template's own procedure, in its folder under `how-to/workflows/`.

**Ownership.** This pair and the shared chapters are shared, the same bytes in every template of
the family that ships them; each template's folder is that template's. Every update of a
template puts its chapters and the shared ones back as it wrote them, a deleted one included,
and lists each in its report; what you had stays in Git. A shared chapter holding another
template's version waits for that template's update. Only a template's update, its recovery and
the commands its report prints change a file here. To work differently from a chapter, record
the difference where the project's rules in `.claude/rules/` say a departure from the guide is
recorded.

## Cross-references

- `how-to/CONTEXT.md`: the whole guide, and who owns each file in it.
- `how-to/docs/`: each template's guides, which explain one practice each.
- `how-to/workflows/`: each template's procedures, which give the steps and the commands.
- `.claude/rules/`: the project's rules, which decide wherever a chapter only explains.
