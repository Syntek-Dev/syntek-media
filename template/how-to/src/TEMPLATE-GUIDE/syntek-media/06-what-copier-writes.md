# What Copier writes — the kinds of file, and what a copy and an update do to each

Every file syntek-media wrote into your project belongs to one kind, and its kind decides what a copy and a later update do to it.
Knowing a file's kind is most of what updating safely needs.
This chapter names the kinds, then says what a copy does, what an update does, and where the update itself is explained.

## Five kinds of file

**Template-owned files** belong to the template, and every update brings its changes to them.

- They are the media rules in `.claude/rules/syntek-media/`, the media skills and their mode files, every `docs/reference/` guide and numbered workflow, and `toolkit/`.
- They also include most folders' `CONTEXT.md` and `CLAUDE.md`, the bridge `.claude/syntek-media-agents.md`, the data-root and permissions scripts beside it, and this guide's files under its `syntek-media/` folders.
- Never edit one: `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md` shows where your own way goes instead.

**Seeds** are written once, empty of entries, for you to fill in, and are yours from then on.

- They include the design tokens and preview cards, the spoken voice, the platform profiles and their overrides, the piece register, the rights register, the credits log, the footage manifest, the schedule and the publish log.
- Every layer's `docs/project/` and `workflows/local/` pair is a seed too.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 8 lists them all.

**The worked example** is one piece carried from its brief to its post package, written only where you answered `SEED_EXAMPLES` on.

**Your folders** are the folders the template only signposts: it ships their pair, and everything you put in them is yours.

- The piece folders under `scripts/src/pieces/`, the edit decision lists, cards, cut-down plans, captions, thumbnails and post packages all live in folders of this kind.

**Copy-only shared files** are the files a project carries once, whichever template writes them first.

- They include `README.md`, `CONTEXT.md`, `.gitignore`, `.mcp.json`, and in `.claude/` the files `CLAUDE.md`, `CONTEXT.md`, `MEMORY.md` and `settings.json` with the pair of `.claude/skills/`.
- They also include each coding agent's entrypoint, settings and folder pair, written only for the clients you chose.
- Some of them are **family-shared**: every template of the family ships them byte for byte, so a project with two templates keeps one copy.
- The family-shared files are the working-practice skills, such as `handoff` and `grill-me`, the hooks in `.claude/hooks/`, the pair of `handoffs/`, the guide's shared files, `.mcp.json` and the coding agents' files.
- The rest, such as `README.md` and `.claude/settings.json`, are syntek-media's own copy-only files.

## What a copy does

A copy is the first run of Copier, which writes the template into the project.

- It writes every template-owned file, seed and folder pair the answers call for.
- It writes the worked example where you asked for it.
- It writes each copy-only shared file only where the project has none, and skips one that stands.
- Copier prints such a file as 'conflict' and then 'skip', or as 'identical', and leaves it exactly as it was.
- Any other file that already stands where the template would write one is a collision, which is a fault in the template.
- A copy run without a terminal stops there, and one run in a terminal asks whether to overwrite, even with `--defaults`, where the answer is no.
- `how-to/workflows/syntek-media/03-report-a-template-problem/` says how to report it.

When the files are written, the copy runs a few small tasks, which is why its command carries `--trust`.
It starts a Git repository where none exists, makes the hooks runnable, and sets a guard that stops a large design export going into Git without Git LFS.
Over a syntek-author project older than v0.6.0, it prints a warning to update syntek-author first.
Its last task records the version just copied inside the repository, so that the first update can report against it.
That task also adds the listed settings entries and MCP servers, once each, to a settings or MCP file the copy kept.
It needs Copier to run on Python 3.14 or later, and on an older Python it prints a message, framed in lines of `=`, that it did NOT run.
The message Copier prints after the copy then says what to add by hand.
A copy never commits, so your first commit is yours, and `how-to/workflows/syntek-media/01-finish-a-copy/` takes you to it.

## What an update does

An update brings a newer version of the template into the project, and treats each kind of file differently.

- **Template-owned files** are merged: the template's changes are joined with any edits of yours.
- Where you and the template changed the same lines, the file holds both versions between conflict markers, for you to resolve.
- **Seeds** are never overwritten, and one you delete comes back as a fresh, empty copy.
- A seed that belongs to a platform or a media kind you remove is deleted with it, filled in or not.
- **The worked example** is never written again, so once you delete it, it stays deleted.
- **Copy-only shared files** are never rendered by Copier on an update, so it never writes over or recreates one.

After Copier, the family's update script runs, and it alone changes some copy-only files.
Its list holds the working-practice skills, the hooks and their pair, the pair of `handoffs/` and the guide's shared files.

- It replaces a listed file only while it still holds a version this template wrote here and the new version differs.
- It writes a listed file the project has never had, such as a shared skill new in this release.
- It keeps a listed file you have edited, or one that holds syntek-author's version, and names it in its report.
- Outside the guide, a listed file you deleted stays deleted.
- It adds the listed settings entries, top-level settings and MCP servers to the files that lack them, once each.
- It never adds back one it has offered before, never removes or reorders one of yours, and never weakens one.
- It never creates a coding agent's files, and only adds the MCP servers to a recorded client's file that already exists.

**The guide in `how-to/`** is put back on every full update.

- The update puts the template's text back on any file of the guide that differs, your edits and deletions included, and lists each one.
- What you had stays in Git, and the report gives the command that shows it.
- A copy restores nothing, and neither does an update whose script does not run to the end, such as one on a Python older than 3.14.
- The next update that runs in full puts the guide back.

## The update report

The update script ends with a report of every file the new version changed that the update did not simply deliver, with commands to compare it or take the template's version.
`how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md` explains the report, section by section, and what to do when no report appears.

## Running an update

Run every update the way `how-to/workflows/syntek-media/04-update-the-template/` says: on a branch, from a clean, committed tree.
This is the command, with the five settings in front that turn Git's background housekeeping off for the run:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml
```

`-a` names the answers file, which Copier finds only when you name it.
`--python '>=3.14'` runs Copier on Python 3.14 or later, which the update script and the migrations around it need.
Copier may print a `MissingFileWarning` about an answers file, and that is expected and harmless.
The template reads your previous answers so it can refuse a changed `BRAND_KIND`, and syntek-author's, where they stand, to keep the data-root answers in step.
The update that first brings this guide, into 0.6.0, prints a report once that names where the guide starts and lists any of your files at its paths.

## What an update never touches

- Your work: pieces, register rows, plans, packages, and every file in a folder the template only signposts.
- A seed that exists, apart from the deletion that comes with removing its platform or media kind.
- A copy-only file the update script does not list, apart from the settings entries and servers added once.
- A file that belongs to no template, your own files under `how-to/` included, though no session may edit them there.
- A file Git ignores, such as a render or a take.

The one change that deletes work of yours is removing a platform or a media kind, which `how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md` explains.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 8: who owns which files, and the full list of seeds.
- `.claude/rules/syntek-media/06-global-rules.md` Section 3: the guide is read-only.
- `.claude/rules/syntek-media/06-global-rules.md` Section 11: answers change through Copier, and what a removal deletes.
- `how-to/docs/syntek-media/updating-the-template.md`: what an update changes, and why it is run as it is.
- `how-to/workflows/syntek-media/04-update-the-template/`: the update, with every command.
- `how-to/workflows/syntek-media/05-recover-a-stopped-update/`: getting back from an update that stopped.

## Next

- Running an update, step by step → `how-to/workflows/syntek-media/04-update-the-template/`
- Reading the report, and an update that stopped → `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`
- Making the project your own without conflicts → `how-to/src/TEMPLATE-GUIDE/syntek-media/10-customising.md`
