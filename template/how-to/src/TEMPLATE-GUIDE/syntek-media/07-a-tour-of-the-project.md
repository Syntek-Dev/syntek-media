# A tour of the project — the layers, the piece folder, the output folders and this guide

This chapter walks round the folders syntek-media gave the project, and says what each one is for.
`CONTEXT.md` at the top of the project is the map, and this chapter explains what the map shows.

## The four layers

The top-level folders syntek-media adds are its layers, and each holds one stage of the work.

- `brand/` holds the brand kit: the design tokens and preview cards, the thumbnail and card layouts, design exports, the spoken voice, and one profile for each platform.
- `scripts/` holds the pieces, one folder each, with the piece register that numbers them.
- `production/` holds the source media and its manifest, voiceovers, edit decision lists, cards, timing and scene files, rights and credits.
- `publishing/` holds the cut-down plans, captions, thumbnails, post packages, the schedule and the publish log.

These are production layers: work is made in them through steps you repeat for every piece.
`toolkit/` sits beside them as a supporting folder, which is run rather than worked in.
It holds `toolkit/media.py`, the command every render, encode and check runs through, `toolkit/card.py`, which turns an HTML layout into an image, the platform data in `toolkit/data/` and the fallback layouts in `toolkit/templates/`.
`python3 toolkit/media.py --help` lists every command.

## Inside a layer

Every production layer splits into the same parts, so once you know one you know them all.

- `docs/reference/` holds the guides the template ships, which explain how this kind of work is done; every update replaces them.
- `docs/project/` holds your own guides, and one with the same name as a reference guide is read instead of it.
- `src/` holds the work itself: the plans, the scripts, the registers and the evidence.
- Numbered workflows, such as `scripts/workflows/01-brief-a-piece/`, are the template's procedures, each with its steps and a checklist.
- `workflows/local/` holds your own procedures, and one with the same folder name as a template workflow replaces it.

Workflow numbers never change and are never reused, because other files cite them.
So a workflow is always named by its full folder name, never by its number alone.
Every folder carries a `CONTEXT.md`, which says what is there and why, and a `CLAUDE.md`, which says how to work there.
Together they are the folder pair, and reading them is the quickest way to learn what a folder is for.

## The piece folder

A piece is one deliverable work: a short, an explainer, a talk, a trailer, an episode, an audiobook or a standalone voiceover.
Each piece has its own folder under `scripts/src/pieces/`, named with a three-digit number and a few words, such as a folder that starts `003-`.
The number is frozen and never reused, and every other file about the piece starts with the same name.
The folder holds the brief, the script or the transcript, the storyboard, the shot list and its own folder pair.
The brief, `brief.md`, is the piece's plan: what it is for, who it is for, and where it stands on the ladder.
A piece climbs the ladder only through its gates, M1 to M7, which `scripts/docs/reference/the-piece-ladder.md` explains.
`scripts/src/piece-register.md` lists every piece by number, kind and origin, but never its status, which lives in the brief.

## The output folders

Renders, takes and source footage are large, can be made again or live elsewhere, so Git ignores them.

- `production/src/renders/` holds each piece's masters.
- `production/src/voiceover/generated/` holds each piece's generated voice, with its takes in a folder of their own.
- `publishing/src/renders/` holds each piece's deliverables for the platforms.
- `production/src/footage/raw/` holds this machine's copies of the source footage the manifest lists.
- Where the project makes audiobooks, the audiobook folder in `production/src/` holds a generated folder and a renders folder of the same kind.

Each of these folders carries only a tracked `README.md`, and Git ignores everything else in it.
Inside one, each piece's output has a folder of its own, which carries nothing at all.
A session never lists those folders: `python3 toolkit/media.py where <piece>` names them and lists the piece's tracked files instead.
The piece's tracked timing and scene files stay in `production/src/timing/` and `production/src/scenes/`, under the piece's name.
An approved voiceover take cannot be made again, so archive it when you approve it.

## The .claude folder

`.claude/` is the folder Claude Code reads, and the other coding agents read it too.

- `.claude/CLAUDE.md` is the project brief, and `.claude/MEMORY.md` is the project's memory: decisions, facts and where the work stands.
- `.claude/rules/syntek-media/` holds the media rules, which load at the start of every session.
- `.claude/skills/` holds the skills, which `how-to/src/TEMPLATE-GUIDE/syntek-media/08-skills-and-the-router.md` introduces.
- `.claude/hooks/` holds the session hooks, which warn as a session fills and stop the guide being edited.
- `.claude/syntek-media-agents.md` is the bridge, which tells the other coding agents what to read.
- `.claude/settings.json` holds Claude Code's permissions and the entries that run the hooks.

Handoffs between sessions go in `handoffs/`, a folder every template of the family shares.

## The guide itself

`how-to/` is the user guide, and it is read-only.
Its shared chapters sit in `how-to/src/TEMPLATE-GUIDE/`, and its shared pairs in each folder, the same in every template of the family.
syntek-media's own chapters, guides and procedures sit only in the folders named `syntek-media` under `how-to/src/TEMPLATE-GUIDE/`, `how-to/docs/` and `how-to/workflows/`.
A companion template's files sit in folders named for that template.
Read it, and never edit it: Claude Code's deny in `.claude/settings.json` refuses an edit, the guide guard `.claude/hooks/how-to-read-only.sh` refuses one too, and the next update puts the guide's text back.
To work differently from the guide, record it in syntek-author's project settings file, 00-project.md, under Overrides or Workflow aliases, where that file is present.
Otherwise record it in `.claude/CLAUDE.md` under the heading 'Project-specific rules'.
Keep your own notes and procedures in a layer's `docs/project/` or `workflows/local/`, never in `how-to/`.

## Binary files and the data root

A project can keep binary files outside the repository, under a folder on each machine called the data root.
syntek-media files nothing under a data root, whatever `DATA_STORE` records, because its map, `.claude/syntek-media-dataroot.json`, claims no folder.
Its footage stays where `production/src/footage/manifest.toml` lists it, and its renders stay in the ignored output folders above.
So for media there is no data-root procedure to follow, and the shared chapter's route to this template's own procedure ends here.
`how-to/src/TEMPLATE-GUIDE/the-data-root.md` explains the data root for a template that does file there, such as syntek-author where it is applied.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Sections 2 to 4: the layers, the kinds of layer and the parts of a layer.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 5: the piece, its folder and the ladder.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 6: the folder pair, and the folders without one.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10: where a departure from the guide is recorded.
- `.claude/rules/syntek-media/06-global-rules.md` Section 3: the guide is read-only.
- `.claude/rules/syntek-media/06-global-rules.md` Section 12: what Git ignores stays out of the session, and the data root.

## Next

- The skills, and how a request finds one → `how-to/src/TEMPLATE-GUIDE/syntek-media/08-skills-and-the-router.md`
- Making your first piece → `how-to/src/TEMPLATE-GUIDE/syntek-media/09-your-first-piece.md`
- The data root, for a template that files there → `how-to/src/TEMPLATE-GUIDE/the-data-root.md`
