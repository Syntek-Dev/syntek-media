# Applying over syntek-author — adding syntek-media to a syntek-author project

The usual way to start is a project that syntek-author already made, with syntek-media applied on top of it.
This chapter says what to have in place first, gives the copy command, and explains what Copier prints and what to do about each line.

## Before you copy

Start from a clean, committed tree, on a branch of its own, so that every file the copy writes shows in Git and can be undone.

```bash
git switch -c apply-syntek-media
```

The project's syntek-author must be v0.6.0 or later, and updated to it before syntek-media is applied.
An older syntek-author treats every `src/` folder as your own work, so its checks would read this guide's chapters as if you had written them.
It also puts nothing back in `how-to/`, so a change made there would stand until a newer update.
From v0.6.0, syntek-author carries its own guide, in a folder named for it beside this one.
Where syntek-author's answers file stands without that guide, the copy prints a warning that this syntek-author is older than v0.6.0.
Then update syntek-author first, by its own procedure, commit, and only then carry on here.
From then on, update syntek-author before syntek-media, every time.
Choose the brand kind that matches the project: `business` over a business project, `author-fiction` over a novel, and `author-nonfiction` over a theology book.

## The copy

Run the copy from the project's top folder, with the template's source in place of SOURCE:

```bash
uvx --python '>=3.14' copier copy --trust SOURCE .
```

The source is the template's address, which its README gives, and which the `_src_path` line of `.copier-answers.syntek-media.yml` records in every project made from it.
The `.` at the end means the current folder, the project itself.
`--trust` lets the template run its tasks, the small commands that finish a copy, which Copier otherwise refuses.
Copier asks each question in turn, and each has a default you can accept.
You can also answer from a file instead, with `--data-file` and an edited copy of one of the template's example answers.
For a project already in use, add `--data SEED_EXAMPLES=false`, so that no worked example piece is added.
In that file, delete the data-root, client and model lines, so that those questions take syntek-author's recorded answers.
Never pass `--overwrite`: it would let the copy replace syntek-author's files with media's.

## What Copier prints

Copier prints one line for each file it writes or finds.

- 'conflict' then 'skip', for a shared file the project already holds, means the copy left it exactly as it was.
- 'identical' means the project's copy and the template's are the same bytes.
- Both are expected for the shared files, such as `README.md`, `.claude/settings.json` and the working-practice skills, and neither is a collision.
- A `MissingFileWarning` about `.copier-answers.syntek-media.yml` is expected too, because a first copy has no earlier answers to read.

Any other path that already exists is a collision, and a collision is a template bug.
A copy run without a terminal stops with 'Interactive session required' before it writes that file.
A copy run in a terminal instead asks 'Overwrite …?', even with `--defaults`, and yes is its default: answer no.
Either way, `git status` shows anything written before the stop.
Remove what the copy wrote, and report the collision as `how-to/workflows/syntek-media/03-report-a-template-problem/` says.

## The copy's last task

The last task of the copy runs on the Python that runs Copier, Python 3.14 or later.
It records the version just copied inside the repository's Git folder, so that the first update can report from it.
It then adds to the settings and MCP files the copy kept, once each, the entries and servers the template lists that they lack.
It never removes or changes an entry you already have.
On an older Python, it prints a framed message, between two lines of `=`, saying that family-update did NOT run.
That message also says the copy recorded nothing and added no settings entry or MCP server.
A copy run with `--skip-tasks` skips the task without any message.
In either case, add the entries by hand, as item 2 of the copy's closing message lists them.
Then start every update with `uvx --python '>=3.14' copier`, as this guide always shows it.
The first update on Python 3.14 renders this version again, and offers any entry still missing.

## Answers taken from syntek-author's record

Some questions belong to the whole family of templates, and their defaults come from syntek-author's answers file.

- The data root, the folder outside the repository for binary files, must have the same first answers as syntek-author's, because one project keeps one layout.
- The coding agents and their models default to the ones syntek-author recorded.
- The OpenCode address, model and context are taken only from a record with the same provider.

So the first copy writes no client file that syntek-author's answers leave out.
Where syntek-author's record holds no answer on the clients at all, as an older syntek-author's may not, the copy offers all of them, so check the answer before you accept it.
`how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md` explains every answer, and `how-to/src/TEMPLATE-GUIDE/the-data-root.md` explains the data root.

## When .agents is not a plain folder

The .agents folder is where some coding agents look for skills and settings.
Where it is a link rather than a folder, or holds a skills folder of your own, the copy needs a step before and after it.
`how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`, under 'When .agents is not a plain folder', gives each case and its commands.

## Then finish the copy

The copy ends with a closing message that lists the edits only you can make, such as the toolkit's permission entries in `.claude/settings.json`.
Review the whole change with `git diff` before you make them.
`how-to/workflows/syntek-media/01-finish-a-copy/` takes you through each edit, the setup check and the first commit, with `.copier-answers.syntek-media.yml` included.
There are no adoption scripts, and nothing of yours moves: every media folder is new, and loose media already in the project is yours to sort.

## Where the rules live

- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 8: who owns which files, and why a shared file is left as it is.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 10: syntek-author's project settings file, and which rule wins.
- `.claude/rules/syntek-media/06-global-rules.md` Section 11: the answers change only through Copier.
- `how-to/workflows/syntek-media/01-finish-a-copy/`: every step after the copy.

## Next

- Finishing the copy, step by step → `how-to/workflows/syntek-media/01-finish-a-copy/`
- Living with both templates from now on → `how-to/src/TEMPLATE-GUIDE/syntek-media/12-beside-syntek-author.md`
- What the copy wrote, and what an update will do to it → `how-to/src/TEMPLATE-GUIDE/syntek-media/06-what-copier-writes.md`
