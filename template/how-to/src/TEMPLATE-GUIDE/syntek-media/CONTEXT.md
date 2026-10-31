# CONTEXT.md — how-to/src/TEMPLATE-GUIDE/syntek-media/

The chapters of syntek-media's user guide: how the audio and video side of this project works,
in plain English, for the person whose project it is. They are numbered from 01, frozen and
append-only, and the table under 'What's here' gives the order to read them in. Like the rest of
`how-to/`, this folder is read-only: read it, and never edit it.

## Directory Tree

```text
how-to/src/TEMPLATE-GUIDE/syntek-media/
├── CONTEXT.md                          ← this file: the chapters, and the order to read them in
├── CLAUDE.md                           ← how to answer a question from the chapters
├── 01-overview.md                      ← what syntek-media adds, and how this guide is laid out
├── 02-prerequisites.md                 ← the tools and accounts to have first, and checking them
├── 03-applying-over-syntek-author.md   ← adding syntek-media to a syntek-author project
├── 04-a-standalone-project.md          ← a project made by syntek-media alone
├── 05-the-answers.md                   ← every answer the template keeps, and changing one later
├── 06-what-copier-writes.md            ← the kinds of file, and what a copy and an update do to each
├── 07-a-tour-of-the-project.md         ← the layers, the piece folder, the output folders and this guide
├── 08-skills-and-the-router.md         ← the skills, the router, the mode files and the model tiers
├── 09-your-first-piece.md              ← from a brief to a recorded publication
├── 10-customising.md                   ← making the project work your way without breaking updates
├── 11-platforms-and-media-kinds.md     ← adding or removing a platform or a media kind
├── 12-beside-syntek-author.md          ← sharing the project with syntek-author
└── 13-troubleshooting.md               ← what to do, grouped by when it breaks
```

## What's here

| You are… | Read |
|---|---|
| New to the project | `how-to/src/TEMPLATE-GUIDE/syntek-media/01-overview.md`, then `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md`, then `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md` |
| Just applied over syntek-author | `how-to/src/TEMPLATE-GUIDE/syntek-media/03-applying-over-syntek-author.md`, `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`, then `how-to/workflows/syntek-media/01-finish-a-copy/` |
| Working in a standalone project | `how-to/src/TEMPLATE-GUIDE/syntek-media/04-a-standalone-project.md`, then `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md` |
| Installing the tools | `how-to/src/TEMPLATE-GUIDE/syntek-media/02-prerequisites.md` |
| Choosing or changing answers | `how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md`, then `how-to/workflows/syntek-media/02-change-the-answers/` |
| Asking what a copy or an update writes | `how-to/src/TEMPLATE-GUIDE/syntek-media/06-what-copier-writes.md` |
| Updating | `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`, then `how-to/src/TEMPLATE-GUIDE/syntek-media/06-what-copier-writes.md`, then `how-to/workflows/syntek-media/04-update-the-template/` |
| After an update that stopped | `how-to/workflows/syntek-media/05-recover-a-stopped-update/` |
| Adding a coding agent | `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`, then `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/` |
| Storing binary files | `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md`, then `how-to/src/TEMPLATE-GUIDE/the-data-root.md` |
| Finding your way round | `how-to/src/TEMPLATE-GUIDE/syntek-media/07-a-tour-of-the-project.md` |
| Looking for the skill for a job | `how-to/src/TEMPLATE-GUIDE/syntek-media/08-skills-and-the-router.md` |
| Starting a first piece | `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md` |
| Making the project work your way | `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` |
| Changing platforms or media kinds | `how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md` |
| Working with syntek-author | `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md` |
| Stuck | `how-to/src/TEMPLATE-GUIDE/syntek-media/13-troubleshooting.md`, then `how-to/workflows/syntek-media/03-report-a-template-problem/` |

- **A chapter explains; the rules decide.** Each chapter ends with 'Where the rules live', which
  names the rules, guides and procedures behind what it explains, and 'Next', which names what
  to read after it.
- **Every chapter ships in every project.** None depends on the brand kind, the platforms or the
  media kinds; a chapter names what only some projects have in words, never as a path.
- **Numbers are frozen and append-only**, counted from 01 in this folder, so a chapter keeps its
  number in every project and every release.

**Ownership.** Every chapter here is syntek-media's own, template-owned and written one sentence
per line for you to read. Every full update of the template puts these chapters back as it wrote
them, a deleted one included, and lists each in its report; what you had stays in Git. Only the
template's update, its recovery and the commands its report prints change a file here. To work
differently from a chapter, record the difference in syntek-author's project settings file,
00-project.md, under Overrides or Workflow aliases, where that file is present, and otherwise in
`.claude/CLAUDE.md` under the heading 'Project-specific rules'
(`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10).

## Cross-references

- `how-to/src/TEMPLATE-GUIDE/CONTEXT.md`: where reading the guide starts, for every template in
  the project.
- `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`, `how-to/src/TEMPLATE-GUIDE/the-data-root.md`
  and `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`: the shared chapters, which explain
  what every template of the family has in common.
- `how-to/docs/syntek-media/`: this template's guides, one practice each.
- `how-to/workflows/syntek-media/`: this template's procedures, with every command.
- `.claude/rules/syntek-media/`: the rules, which decide wherever a chapter only explains.
