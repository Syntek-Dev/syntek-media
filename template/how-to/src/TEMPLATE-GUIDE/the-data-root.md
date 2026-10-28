# The data root — where binary files live, and why

Git, the tool that records every version of your project, keeps text well and large binary files badly, because every version of a binary stays in it for good.
So a project can keep its binary files, such as scans, signed copies, images and audio, in one folder outside the repository: the data root.
The repository, the project folder Git looks after, keeps the text and a list of every file filed there.

## Two ways to keep binary files

Each template asks, in the answer `DATA_STORE`, where the binary files of its filing folders are kept.

- `external` keeps them outside the repository, under the data root.
- `repo` keeps them in the repository, committed beside the work, as projects did before the data root existed.

A template with no filing folder keeps nothing under the data root, whatever the answer, and its own rules say where its binary files go.
Every template applied to a project records the same answer.
Changing it later goes through your template's update, never an edit by hand.
Under `repo`, the data commands, which file, check and fetch these copies, file nothing, and the rest of this chapter applies once you move the files out.
Text work never needs a data root: drafting, proofs and checks all run without one.
A command that files a copy stops, with the reason, when there is no valid root, and never falls back to writing into the repository.

## The data root on each machine

The data root is one folder on each machine you work on, which you choose, set up and back up yourself.
It lies outside every repository, on a local disk or a mounted network share.
The environment variable `SYNTEK_DATA_ROOT` names it: a setting your terminal, and every program it starts, can read.
No file in the project names it, so each machine can keep its root in a different place.
This example uses a folder called data-root in your home folder; put the folder you choose in its place:

```bash
export SYNTEK_DATA_ROOT="$HOME/data-root"
```

To keep it for every new terminal, also add that line to your shell profile, the file your terminal reads when it starts (`~/.zshrc` or `~/.bashrc`).
On Windows, set it in the system's environment settings instead, so that every program sees it.
Then create the folder, with the empty marker file `.syntek-data-root` at its top:

```bash
mkdir -p "$SYNTEK_DATA_ROOT" && touch "$SYNTEK_DATA_ROOT/.syntek-data-root"
```

Run both commands yourself, in your own terminal: a session never writes under the root.
Neither prints anything when it works.
The marker proves the root is there.
A network disk that is not mounted shows an empty folder, and the missing marker gives it away.
The tool never creates the marker.
Never put the data root inside a repository, and never put a repository inside the data root.
Never keep a repository in a folder that a sync service copies either, because a sync service copies file by file and can corrupt Git.
The data commands refuse a root and a repository that contain one another.

## Where each file goes

Below the root, every file keeps the path it has in the repository, so every reference to it still works.
The layout is `<root>/<area>/<kind>/<slug>/<path in the repository>`.
The area, `DATA_AREA`, groups your projects, such as all your business work.
The slug, `DATA_SLUG`, names this project: give every project its own, or two projects share a folder.
The kind is a folder for documents, images, audio or video, named by the answers `DATA_KIND_DOCS`, `DATA_KIND_PHOTOS`, `DATA_KIND_AUDIO` and `DATA_KIND_VIDEOS`.
A file's extension chooses its kind, unless its filing folder fixes one.
Only the filing folders, where a template keeps such files, take part, and each template's map, `.claude/syntek-*-dataroot.json`, names its own.
Each filing folder that holds a filed copy has a manifest, `external.toml`, which lists every copy with its checksum, the date and its state.
A checksum is a fingerprint of a file's exact bytes, so a copy that changes or goes missing is found.
Commit the manifest with the work it lists, and never edit, reorder or delete a row by hand.
Rows are only ever added, and the one change to a row is its state, from current to superseded or withdrawn.
Each row also has a role, which says what the copy is, such as issued, signed or received.
A signed, received, ingested or evidence copy is evidence: it is never replaced, and a changed file is a failure, never an update.
In the project's text, a filed file is named `ext:<path in the repository>`.

## The tool

Each template ships the data-root tool under its own name, as `.claude/syntek-*-dataroot.py`, and the copies are the same bytes.
It needs Python 3.14 or later: on an older Python, every command says in a framed message that it did NOT run, and changes nothing.
You choose its job with one word after its name.

- `root` checks this machine's root and marker, and prints the store, where each kind of file goes and your provider's checklist.
- `store` prints the store each template's answers record.
- `path` prints where one file is kept, so it is opened at that path.
- `add` files a copy of one file under the root and lists it in the manifest.
- `status` reports what is at risk, such as binaries no manifest lists and copies kept online only.
- `verify` checks every listed copy against its checksum.
- `pull` copies listed files back into your work tree, where Git ignores them.
- `plan` lists the binaries Git still holds in the filing folders and where each would go.
- `check-names` checks that names are safe on Windows, which refuses some characters and names.

This command runs `root` and changes nothing; the `for` loop runs the first copy of the tool it finds, whichever template wrote it:

```bash
for f in .claude/syntek-*-dataroot.py; do python3 "$f" root; break; done
```

Run it first on a new machine, and again whenever a data command refuses.
When the tool refuses for any other reason, it says why in one line: fix the cause, and never work round it by copying, moving or editing a file yourself.
Your template may give shorter commands for the same steps, in its procedures under `how-to/workflows/` or in its own chapters.
Moving binary files that Git already holds out of the repository is a copy, never a move.
`plan` with `--copy` files a copy of each one, and taking the originals out of Git is yours to do, once `verify` passes.
Taking a file out of Git deletes it from every other copy of the repository when that copy next pulls.
So set up and verify the root on every machine first.

## One layout per project

Every template applied to a project records the same store, area, slug and kind folders.
A template's first answers default to the other template's recorded ones, and must equal them.
A later difference is reported after the update, and every data command refuses until the answers agree again, while text work goes on.
A change of case alone, such as `Business` to `business`, is refused, because one disk treats them as one folder and another as two.
Any other change leaves the files already filed under the old folders, where the manifest still finds them, and moving them is yours.
Answering `repo` forgets the layout answers, so note them first if you may return to `external`.
Never put `DATA_STORE` or `DATA_SLUG` in your own Copier defaults, a settings file that answers questions for every project you make.
Put an area or a kind folder there only where it equals every other template's recorded answer.
When you remove a template, remove its answers file too, because one left behind still binds the other template's answers.

## The guard and the session

A session never searches, lists, browses or edits anything under a data root.
The files there are records: a search would print their contents into the session, and an edit would break the checksum that proves them unchanged.
Where `.claude/settings.json` wires it, Claude Code runs a guard, a hook that stops any edit or write under a data root.
A hook is a small script Claude Code runs at a fixed moment, here before each use of a file tool.
The guard also stops Claude Code's own search tools there.
On macOS, Linux and WSL, though, Claude Code searches through the shell, which the guard does not read, so there the rules alone keep searches out.
Other clients run no guard, and follow the rules.
The guard never blocks work outside a data root, and lets the call through when it meets an error of its own.
On a Python older than 3.14 it checks nothing: it lets every call through and warns you and the session each time that it did NOT work, until you upgrade.
A session reaches the root's files only through the data-root tool, and opens a filed file only at the path the tool prints for it.

## Keeping a copy: providers

The data root needs a backup, and you choose and run the service that keeps it, such as a cloud drive, a network disk or a backup tool.
The template never installs, configures or runs a sync service, and never uploads or deletes anything there.
Your answer `DATA_PROVIDER` only tailors the checklist the tool prints and the checks it makes.
Point the service at the data root, never at a repository.
A cloud drive may keep some files online only, and download each one when it is read.
The checks never read such a file unless you ask them to.
A file whose name looks like a provider's conflict copy is reported with a hint: compare it with the original, and never rename or delete it.
Every template in a project defaults to the same provider, and a difference is only reported, because it moves no file.

## Where the rules live

- The project's rules, in `.claude/rules/`, say when each data command is used and what each refusal means; where they differ from this chapter, the rules win.
- Every `.claude/syntek-*-agents.md` says how a client other than Claude Code keeps out of the data root.
- Where your template has filing folders, its procedures, in its folder under `how-to/workflows/`, give the steps that set up a machine and move files out.

## Next

- Changing an answer such as `DATA_STORE`, through an update → `how-to/src/TEMPLATE-GUIDE/updating-and-recovery.md`
- Setting up Claude Code and the other coding agents → `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`
