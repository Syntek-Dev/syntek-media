---
workflow: 04-update-the-template
phase: review
skills: []
model: opus
---

# STEPS.md — update the template

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for taking syntek-media's latest changes into this project, from a clean
tree to a commit. Each step names the guide it uses. **Run in order**, from the top folder of the
project, and tick `CHECKLIST.md` as you go. Every command runs exactly as written, in bash, zsh
or another POSIX shell.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure, and `run-media-workflow` never routes it. Every step that changes the project
> waits for the author's word.

## 1. A clean, committed tree in its own repository, on a branch

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command prints the top folder of the repository the project is in:

```bash
git rev-parse --show-toplevel
```

It should print this project's own folder. A folder above it means the project sits inside
another repository: stop, and tell the author, because the update needs a repository of its own.
This command lists every change not yet committed:

```bash
git status
```

It should end `nothing to commit, working tree clean`. Where it lists anything, commit it with
the author, or move it out of the project, files Git does not track included: an update may
write over an untracked file at one of the template's paths. Where it lists nothing but the
author has told Git to hide untracked files, this command shows them too, and should also end
`nothing to commit`:

```bash
git status --untracked-files=all
```

Then start a branch for the update:

```bash
git switch -c update-syntek-media
```

It should print `Switched to a new branch 'update-syntek-media'`. Where it says that branch
already exists, an earlier update was never merged or deleted: settle it with the author first.
_Mechanical._

## 2. Update syntek-author first, where it is present

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command shows whether syntek-author has been applied to the project, and, where it has,
the release it was last updated to:

```bash
ls .copier-answers.syntek-author.yml && sed -n "s/^_commit: *['\"]\{0,1\}\([^'\"]*\).*/\1/p" .copier-answers.syntek-author.yml
```

Where it says `No such file or directory`, the project is standalone: go on at step 3.
Otherwise the two templates share files, answers and the user guide, so syntek-author is updated
first, every time, to v0.6.0 or later: an older one ships no user guide of its own, which a
combined project must not keep. Run syntek-author's own update procedure, in its folder under
how-to/workflows/, to its own commit, then come back here; `git status` should again end
`nothing to commit, working tree clean`. _Mechanical._

## 3. Check the three hazards

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command shows what stands at the three names an update must handle with care:

```bash
ls -ld .agents .agents.syntek-held how-to
```

It prints one line for each that exists, and `No such file or directory` for each that does
not; both are expected. Then, by what it shows:

- **`.agents.syntek-held` exists:** an earlier update stopped with an .agents link held aside.
  Put it back first, with step 2 of
  `how-to/workflows/syntek-media/05-recover-a-stopped-update/`, then start this procedure
  again.
- **.agents is a link to a folder outside the project** (its line shows `->` and a path that
  leads out of the project): nothing to do. The update holds it aside as `.agents.syntek-held`
  and puts it back.
- **`how-to` is a file or a link** (its line does not start with `d`, or shows `->`): stop. An
  update stops on a file there or on a link that leads outside the project, and writes the user
  guide through any other link. Agree a new name with the author, rename it (`git mv how-to`
  and the new name, such as `my-how-to`, for one Git tracks), commit, and start this procedure
  again.

Where `how-to` does not exist yet, the update creates it. _Mechanical._

## 4. Settle any changed answer with the author

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

Ask the author whether this update should change any answer, such as a platform or a media kind
added or removed, or a coding agent recorded. An answer changes only through the update, never
by editing `.copier-answers.syntek-media.yml`; where changing one is the point of the update,
follow `how-to/workflows/syntek-media/02-change-the-answers/` instead, which runs these steps.
A list answer, such as `PLATFORMS`, `MEDIA_KINDS` or `AGENT_CLIENTS`, is given whole: every
value the project keeps, the new one included, because the list given replaces the recorded
one. `BRAND_KIND` never changes: the update refuses it and touches nothing, because a different
brand kind is a new project.

Removing a platform or a media kind deletes every file it generated, the platform's profile and
other filled-in seeds included. Before it asks its first question, the update prints what each
removal deletes, workflows by full folder name: where a value is going, read that list with the
author before they answer, and have them copy out and commit anything they still need. Every
file it deletes is in the last commit before the update. The report lists under `DELETED` only the ones
the author had changed, each with a `restore:` line that brings it back; one they never changed
has no entry, and comes back from that commit.
`how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md` explains every answer, and what it
costs to change. _Substantive._

## 5. Run the update

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

The author runs the update in their own terminal, because Copier asks every question again
there, each with the recorded answer as its default: pressing Enter keeps it. The five settings
in front of the command turn Git's background housekeeping off for this one run, which can
otherwise stop an update with `OSError: [Errno 39] Directory not empty`, and
`--python '>=3.14'` runs Copier on Python 3.14 or later, which the update report needs: left to
itself, `uvx` may run Copier on an older Python it already has. Keep the quotes, or the shell
reads `>` as a redirection:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml
```

Without `-a`, Copier finds no answers file and changes nothing. A session never runs the command
above: it has no terminal, so Copier stops with `Interactive session required`, and an .agents
link outside the project is left held aside as `.agents.syntek-held` (step 2 of
`how-to/workflows/syntek-media/05-recover-a-stopped-update/` puts it back). Where the author asks
a session to run the update, it runs this form instead, once step 4 has settled every answer:
`--defaults` keeps every recorded answer, and gives a question new in this version its default.

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust --defaults -a .copier-answers.syntek-media.yml
```

Where the project was rendered from a local clone of the template at `HEAD`, add
`--vcs-ref=HEAD` at the end of either form, until a newer release tag exists. It ends with the
update report, whose first line starts `▸ syntek-media update report`. If it stops instead with
`OSError: [Errno 39] Directory not empty`, or with `FileExistsError: [Errno 17]` or
`NotADirectoryError` naming `how-to`, or with `ForbiddenPathError` naming a path in `how-to` or,
after a framed `agents-outside-link did NOT run`, in .agents, or with any other error after
which `git status` shows changes, commit nothing and run
`how-to/workflows/syntek-media/05-recover-a-stopped-update/`. Where it printed, in place of the
report, a message framed in lines of `=` that says `family-update did NOT run`, Copier ran on a
Python older than 3.14 and nothing was reported, refreshed or put back in `how-to/`: tell the
author at once, look for conflict markers and `.rej` files with them, commit the update, then
run it again as above, with `--python '>=3.14'`. _Mechanical._

## 6. Read the migration output and the update report with the author

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

A release that moves something prints its own report, a migration, above the update report.
The update that crosses 0.6.0 prints one, once, about the user guide and any file of the
author's at its paths; an update that crosses 0.4.2 prints one about .agents. Read each line of
every migration's output with the author, and make the hand edits it names.

Then go through every section the update report prints with the author. In every compare
command, the lines starting `-` are the template's and those starting `+` the author's.

- **`CONFLICT`:** both versions are in the file, between `<<<<<<<` and `>>>>>>>`. Resolve each
  with the author, keeping what they want of each, then run `git add` on the file. A conflict
  under `how-to/` is never edited: the update has already put the template's text back, and the
  file is listed under `RESTORED` instead, with a `then:` line giving the `git add` to run.
- **`REJECTED HUNKS`:** the file holds the template's version, and the author's lines are in a
  `.rej` file beside it. Outside `how-to/`, carry over what the author wants from it by hand,
  then delete the `.rej` file. Under `how-to/`, run only the `rm` line the entry prints; where
  Claude Code refuses it, the author runs it in their own terminal.
- **`DELETED`:** the template retired the file, or an answer no longer ships it. The author's
  version is in Git; the entry's `restore:` command brings it back if they want it.
- **`RESTORED`:** a file of the user guide was put back to the template's text, because
  `how-to/` is read-only. What the author had is in Git, and the entry's `yours:` command prints
  it. Where they want to keep working their way, record it in syntek-author's project settings
  file, 00-project.md, under Overrides or Workflow aliases, where that file is present, and
  otherwise in `.claude/CLAUDE.md` under the heading 'Project-specific rules'
  (`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10), never in `how-to/`.
- **`LEFT AS IT IS`:** a file of the user guide kept its text; act on its `why:` line with the
  author. A copy Git does not hold: commit it or move it out, and the next update puts the
  template's text back. A link, or a path beyond one: make `how-to` a real folder, as step 3
  says. Not a regular file (a folder or other entry where a guide file belongs): move it out
  with the author, and the next update puts the file back. Another template's version of a shared file, or a clone with no
  record of another template: leave it for that template's own update.
- **`NOT UPDATED`:** the update left the file as the author had it, for the reason its heading
  gives. Compare it, and run the entry's `take:` command only where the author wants the
  template's version.
- **`NOT RESTORED`**, **`NOT ADDED`** and **`NOT COMPARED`:** read each entry to the author, and
  act only on their word.

Note, too, the lines starting `▸ syntek-media: added` that name the settings entries and MCP
servers it added, and the other `▸ syntek-media:` lines naming what to add or run by hand. A line saying a client file exists
but the recorded answers do not name its client sends the author on to
`how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`, to record it. Where no report
appeared, look for conflict markers and `.rej` files by hand, with `git status`. _Substantive._

## 7. Read the changes, and make the hand edits

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command lists every file the update changed or added:

```bash
git status
```

It should show no file as `both modified`. Then read the changes themselves with the author:

```bash
git diff
```

Where a platform or a media kind changed, edit by hand, with the author, the files that describe
the project's options, because an update never rewrites them: in a standalone project
`README.md`, `CONTEXT.md` and Section 1 of `.claude/CLAUDE.md` (over syntek-author they are
syntek-author's), and any rows for a removed platform in `brand/src/platforms/overrides.toml`.
The brand section of the rules, `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1,
follows the answers on its own. Copier may have printed a `MissingFileWarning` about
`.copier-answers.syntek-media.yml`, or, where syntek-author has not been applied, about its
answers file: both are expected and harmless. _Substantive._

## 8. Carry new rules to the other clients

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

Where the update added deny or ask rules to `.claude/settings.json`, the other coding agents do
not see them until the permissions script copies them into their own files. This command shows
the plan and any rule a client file lacks, and changes nothing:

```bash
python3 .claude/syntek-media-permissions.py --check
```

It ends `Every expressible rule is in place.` where nothing is missing, or names each rule a
client file lacks. On the author's word, this command adds the missing rules to the client
files that exist, and never creates one:

```bash
python3 .claude/syntek-media-permissions.py --write
```

_Mechanical._

## 9. Commit, with the answers file

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

Once every conflict is resolved and the author has agreed every change, this command commits the
whole update, `.copier-answers.syntek-media.yml` included, which every later update works from:

```bash
git add -A && git commit -m 'Update from syntek-media'
```

Afterwards `git status` should end `nothing to commit, working tree clean`. Merge the branch
into the project's main line with the author, the way they usually do. _Mechanical._

## 10. Update another template separately afterwards

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command lists every template's answers file in the project:

```bash
ls .copier-answers.*.yml
```

Where it lists another besides `.copier-answers.syntek-media.yml` and syntek-author's, which
step 2 updated first, that template is updated separately, after this commit, with its own
procedure in its own folder under `how-to/workflows/`, never with this one. _Mechanical._
