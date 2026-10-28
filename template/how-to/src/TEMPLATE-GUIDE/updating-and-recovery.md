# Updating and recovery — what an update does, and how to get back from one that stopped

An update brings a template's improvements into your project.
It works on a clean branch, one template at a time.
When it stops part way, you undo it and run it again.

## Before you update

A template is a source that Copier applies to your project, and Copier is the tool that applies it and brings in the template's later versions.
Each template keeps your answers to its questions in its answers file at the top of the project, `.copier-answers.<template>.yml`, where `<template>` is the template's name.
Commit that file with every update, and never edit it by hand: it is the record every later update works from.
A commit is a snapshot of the project that Git, the tool that records every version of it, keeps for good.
Commit everything before you start, files Git does not yet track included.
Copier refuses to start while Git shows uncommitted changes, but where your Git settings hide untracked files, it may write over one.
This command lists every change not yet committed, and should report nothing to commit:

```bash
git status
```

Where you have told Git to hide untracked files, this command shows them as well, and should also report nothing to commit:

```bash
git status --untracked-files=all
```

The project must be its own repository, the folder Git looks after, never a folder inside another repository.
Work on a branch, a separate line of work that you merge back when it is done or throw away.
Update one template at a time, and commit between them.
Check that `how-to` is a real folder before you update:

```bash
ls -ld how-to
```

Its line should start with `d`, for a folder; where nothing is there yet, the update creates the folder.
If `how-to` is a file or a link instead, rename it before you update.
An update stops on a file or on a link that leads outside the project, and writes through any other link.
Every update command carries five settings in front of it, which turn Git's automatic housekeeping off for that one run.
They are `GIT_CONFIG_COUNT=2`, `GIT_CONFIG_KEY_0=gc.auto`, `GIT_CONFIG_VALUE_0=0`, `GIT_CONFIG_KEY_1=maintenance.auto` and `GIT_CONFIG_VALUE_1=false`.
Copier works in temporary Git repositories, and Git may start tidying one in the background just as Copier deletes it.
That stops the update with `OSError: [Errno 39] Directory not empty`.
The five settings change none of your own Git settings, and need Git 2.31 or later and a POSIX shell, such as bash or zsh.
The command itself is `uvx --python '>=3.14' copier update --trust -a` followed by your template's answers file.
`uvx` runs Copier without installing it, and `--trust` lets the template run its own update steps.
`--python '>=3.14'` makes `uvx` run Copier on Python 3.14 or later, which the update's last step needs: the step that prints the report, refreshes the shared files and puts the guide back.
Without it, `uvx` may run Copier on an older Python it already has.
Keep the quotes: without them, the shell reads `>` as an instruction to write to a file.
`-a` names the answers file, which Copier finds only when you name it.
Your template's own procedure for updating, in its folder under `how-to/workflows/`, gives the exact command.

## What an update does to each kind of file

The template's own files are merged with your edits.
Where you and the template changed the same lines, Copier leaves both versions in the file, between the conflict markers `<<<<<<<` and `>>>>>>>`.
Seeds, the files a template writes once for you to fill in, are never overwritten.
A seed you delete comes back as a fresh copy on the next update of the template that seeds it.
Copy-only files, such as the settings files of the clients other than Claude Code, are written only by a copy, where they are missing, and never by an update.
One file can be a seed in one template and copy-only in another, `.claude/settings.json` among them; each template's rules say which.
An update changes a copy-only file only to add, once, the settings entries and MCP servers described below.
Shared files, which the project's rules call family-shared, are the ones every template of the family ships byte for byte, such as the working-practice skills and hooks and the guide's shared files.
Outside the guide, an update replaces a shared file only while it still holds a version that template wrote here.
It also adds a shared file the project has never had.
A shared file you have edited is kept, and the report names it.
The user guide in `how-to/` is read-only, and the update treats it differently.
After everything else, the update puts the template's text back on any file of the guide that differs, your edits and deletions included, and lists each one.
What you had stays in Git, and the report gives the command that shows it.
It never touches a file there that no template ships, and never writes over another template's version while it stands unchanged.
So read the guide, and never edit it: only an update, its recovery and the commands its report prints change a file there.
To work differently from the guide, record the difference where the project's rules in `.claude/rules/` say a departure from the guide is recorded.
The update also adds to `.claude/settings.json` each hook and permission rule the template lists, and adds the two MCP servers to `.mcp.json` and to the settings file of each client your answers name (OpenCode's and Gemini CLI's once they hold the ask rules the permissions script writes).
It also adds each top-level setting the template lists, such as `"idleCompaction": false`, where your file has no such key, and keeps a value you set yourself, saying so once.
Each is added once, and never added back after you remove it.
Your own work is never a template file, and no update writes over it.

## Reading the report

Every update that runs in full ends with a report.
It lists each file the template changed that the update did not simply deliver, says why, and gives commands to compare it or take the template's version.
It changes none of your files apart from the shared files it refreshes, the settings entries and servers it adds and the guide files it puts back.
It never commits, and needs no network.
Each section is printed only when it has an entry.

- `CONFLICT`: both versions are in the file; resolve it, then run `git add` on it.
- `REJECTED HUNKS`: the file holds the template's version, and your lines are in a `.rej` file beside it.
- `DELETED`: the template retired the file, or an answer no longer ships it, and your version is still in Git.
- `RESTORED`: a file of the guide was put back to the template's text, and what you had is in Git.
- `LEFT AS IT IS`: a file of the guide kept its text, for the reason given.
- `NOT UPDATED`: the update left a file as you had it, for the reason in the section's title.
- `NOT RESTORED`: you had deleted a template file that the template has since changed.
- `NOT ADDED`: a file only a copy writes, which the new version ships here because the template added it or an answer now asks for it (the files of a client you have just recorded, for example).
- `NOT COMPARED`: a file Git ignores, which the update never reads.

The reasons a file is not updated are your edit, another template's version, a file written only once, and a new file where you already had one.

In every compare command, the lines starting `-` are the template's and the lines starting `+` are yours.
In `how-to/`, settle a conflict or a rejected hunk by taking the template's version, never by editing the file.
The update has already put the template's text into a conflicted guide file, and the report's `then:` line gives the `git add` that clears the conflict.
A `.rej` file left under `how-to/` is deleted, with the `rm` command the report prints beside it.
A file listed under `LEFT AS IT IS` kept its text for one of these reasons.

- It holds another template's version, which only that template's own update replaces, once that template ships a newer one.
- Git does not hold your copy, so writing over it would lose it: commit or move it, and the next update puts the template's text back.
- It is a link, or lies beyond one, and an update never writes through a link.
- It is not a plain file.
- This copy of the repository holds no record of another template, so the file may hold its version: updating that template here, to a release that writes update records, settles it, and so does working in a copy that holds its records.

Each update keeps two records inside the project's `.git` folder, which travel with no ordinary push.
`refs/<template>/template` holds the template as made with your answers at each update, with the report.
`refs/<template>/yours` points at your last commit when the update ran, before any of its changes.
The report's commands name them as your template's name followed by `/template` or `/yours`, and keep working offline until the next update.
To print the whole report again, run `git log -1 --format=%B` followed by your template's name and `/template`.

## Another template's files

A project can carry a second template from the same family, and the two share some files.
A shared file holding the other template's version waits for that template's update, and is never put back to an older version while it stands unchanged.
Each template puts back its own guide files and the shared ones, and never touches the other template's folder.
A shared file you deleted comes back when another template is applied to the project later, because a first copy writes every shared file that is missing.
Update the two templates one at a time, each with its own answers file, and commit between them.

## When no report appears

A run with `--pretend` shows what an update would write and runs nothing after that, so it prints no report.
With `SYNTEK_UPDATE_REPORT=off` set, the report lists only conflicts and deletions.
That update also adds or refreshes no shared file, offers no settings entry or server, and puts back no guide file, until an update runs without it.
Where the update cannot rebuild the version you had, the report says so and is short, but the guide is still put back.
If no report line appears at all, Copier skipped every step that runs after it writes, as it does when it cannot read a template version.
Then run `git status`, and look for conflict markers and `.rej` files yourself.
If, in place of the report, a message framed in lines of `=` says `family-update did NOT run`, `uvx` ran Copier on an older Python it already had.
That update printed no report, refreshed no shared file, added no settings entry or server, put back no guide file and kept no record.
Look for conflict markers and `.rej` files yourself, commit the update, then run the same update again, with the five settings from 'Before you update' in front of `uvx --python '>=3.14' copier update`.
That second report says the template did not change, because the first run already moved the answers file to the new version.
Upgrade the Python your terminal runs to 3.14 or later as well, because the project's own tools and hooks need it too; where your template's own chapters say a tool needs an older Python, keep that one beside it.
In a folder inside another repository, one line says that nothing was recorded, refreshed or added.

## When an update stops

An update can stop part way with an error, after Copier has already written the new version's files and moved the answers file forward.
Each of these errors means this.

- `OSError: [Errno 39] Directory not empty`, on a temporary folder Copier was deleting.
- `FileExistsError: [Errno 17]` or `NotADirectoryError` naming `how-to`, where `how-to` is a file rather than a folder.
- `ForbiddenPathError` naming a path in `how-to`, where `how-to` is a link that leads outside the project.
- `ForbiddenPathError` naming a path in `.agents`, after a message framed in lines of `=` that says `agents-outside-link did NOT run`, where `.agents` is a link that leads outside the project and Copier ran on a Python older than 3.14.

Never commit what it left: an update run over it takes the new version as already reached, and skips the steps that version needed.
Undo it and run it again, from the top folder of the project, in this order.
First, put back a held `.agents` link, as `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md` explains, because the discard below would delete it.
Next, see what the discard would delete; this dry run deletes nothing:

```bash
git clean -n -d
```

It lists every untracked file and folder, not only the update's, so commit or move out of the project anything of yours it lists.
Files Git ignores are left alone.
Then, only if you agree, discard every uncommitted change in the repository, the stopped update included:

```bash
git reset --hard && git clean -fd
```

Afterwards `git status` should report nothing to commit.

Where `how-to` was a file or a link, give it another name and commit; `git mv how-to my-how-to` does that for one Git tracks.
Last, run the update again, with the five settings from 'Before you update' in front of `uvx --python '>=3.14' copier update`, and check that the report reads from the version you had.
The second run delivers what an update that never stopped delivers.
Your template's own procedure for recovering from an update that stopped, in its folder under `how-to/workflows/`, gives every command, the update included.

## Updating safely over time

Discarding an update and running it again is safe: the second run delivers what the first did.
Until you commit it, an update counts as not made, so a rerun offers everything again.
A settings entry or server you removed from an uncommitted update comes back on a rerun, so remove it again once the update is committed.
Run updates on one line of history, because the records are kept for each copy of the repository, not for each branch.
So update on a branch cut from your main line and merge it, and bring other long-lived branches up to date by merging.
A formatter or a commit hook that re-indents or re-quotes the answers file changes nothing, as long as the answers themselves stay the same.
The records travel only with `git push --mirror`.
A plain push, which sends your commits to another copy of the repository, leaves them behind, and so does a plain clone.
So in a fresh clone, a copy made with `git clone`, the first update rebuilds the old version once, which takes longer.
There, a shared guide file may also be left as it is until each template has updated once in that clone.
Before you rewrite history to remove a secret, delete both records, or they keep the old commits alive.
The commands are `git update-ref -d refs/<template>/template` and `git update-ref -d refs/<template>/yours`, with your template's name in place of `<template>`.
The next update records them again.

## Where the rules live

- The project's rules, in `.claude/rules/`, decide which files are the template's and which are yours, and what a session may do during an update.
- Every `.claude/syntek-*-agents.md` tells a client other than Claude Code how its template's files are kept up to date.
- Your template's procedures, in its folder under `how-to/workflows/`, give every command for updating and for recovering from an update that stopped.

## Next

- Putting back a held `.agents` link → `how-to/src/TEMPLATE-GUIDE/agent-clients-and-mcp.md`
- Keeping binary files under a data root → `how-to/src/TEMPLATE-GUIDE/the-data-root.md`
- Where each template's chapters start → `how-to/src/TEMPLATE-GUIDE/CONTEXT.md`
