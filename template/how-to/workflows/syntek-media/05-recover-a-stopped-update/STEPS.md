---
workflow: 05-recover-a-stopped-update
phase: review
skills: []
model: opus
---

# STEPS.md — recover a stopped update

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for undoing a syntek-media update that stopped part way, and running it
again. Each step names the guide it uses. **Run in order**: the held link comes back before the
discard, and the dry run is read before anything is deleted. Work from the top folder of the
project, in a POSIX shell (Terminal on macOS and Linux, Git Bash on Windows, never PowerShell),
and tick `CHECKLIST.md` as you go. Every command runs exactly as written.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure, and `run-media-workflow` never routes it. Steps 3, 4 and 5 wait for the
> author's word.

## 1. Confirm the stop; commit nothing

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

An update has stopped part way when it ended with one of these errors instead of its report:
`OSError: [Errno 39] Directory not empty`, on a temporary folder Copier was deleting;
`FileExistsError: [Errno 17]` or `NotADirectoryError` naming `how-to`, where `how-to` in the
project is a file rather than a folder; `ForbiddenPathError` naming a path in `how-to`, where
`how-to` is a link that leads outside the project; or `ForbiddenPathError` naming a path in
.agents, after a message framed in lines of `=` that says `agents-outside-link did NOT run`,
where .agents is a link that leads outside the project and Copier ran on a Python older than
3.14 (step 6 runs it on a newer one). By then Copier has written the new version's files and
moved `.copier-answers.syntek-media.yml` forward, but nothing that runs after it has run. This
command shows what it left:

```bash
git status
```

It lists files changed and files new. Commit none of it: an update run over it would take the
new version as already reached, report 'Keeping template version' where it should say
'Updating to template version', and skip the steps that version needs. Where it ends
`nothing to commit, working tree clean`, Copier wrote nothing: go on at step 2, then skip to
step 5. _Substantive._

## 2. Put back a held .agents link

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

An update that stops can leave an .agents link to a folder outside the project held aside as
`.agents.syntek-held`, and the discard in step 4 would delete it. This command shows what stands
at both names:

```bash
ls -ld .agents .agents.syntek-held
```

Where it says `No such file or directory` for `.agents.syntek-held`, nothing is held: go on at
step 3. Otherwise, clear the way for the held link. Where .agents is a link (its line shows
`->`), remove that link alone, never with `rm -r` and never with a trailing slash:

```bash
rm .agents
```

Where .agents is a folder or a file instead, first check that `ls -ld .agents.from-update`
says `No such file or directory`, then move it aside:

```bash
mv .agents .agents.from-update
```

`.agents.from-update` now holds what the update wrote; the author checks it at step 3, before
the discard. Where .agents was not there at all, neither command is needed. Then, once
`ls -ld .agents` says `No such file or directory`, put the held link back:

```bash
mv .agents.syntek-held .agents
```

Never run that `mv` while .agents stands: it would put the held link inside it, and inside the
folder outside the project where .agents is a link. Afterwards `ls -ld .agents` shows the link
again, with `->` and the folder outside the project. Where the held link was committed beside
an identical .agents link, the next update moves nothing, says so, and asks for the held link to
be removed with `rm .agents.syntek-held` and the removal committed: do that with the author.
_Mechanical._

## 3. See what the discard would delete

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This dry run deletes nothing. It lists every untracked file and folder the discard in step 4
would delete, not only the ones the update wrote:

```bash
git clean -n -d
```

Each line starts `Would remove`. Go through them with the author, and commit, or move out of the
project, anything of theirs it lists; then run it again, until it lists only what the update
wrote. Where step 2 moved .agents aside, it lists `.agents.from-update` too: check it with the
author, and move it out of the project now if they want anything in it, or the discard removes
it. Files Git ignores are not listed, and the discard leaves them alone. _Substantive._

## 4. Discard the stopped update, with the author's agreement

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command discards every uncommitted change in the repository, the stopped update included,
and deletes every untracked file and folder step 3 listed. Run it only with the author's
agreement, and only in a project that is its own repository:

```bash
git reset --hard && git clean -fd
```

Afterwards `git status` should end `nothing to commit, working tree clean`, and
`.copier-answers.syntek-media.yml` names the version the project had again. _Mechanical._

## 5. Make how-to a real folder, where it was not one

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

This command shows what stands at `how-to`:

```bash
ls -ld how-to
```

A line starting `d` is a folder, and `No such file or directory` means the update will create
one: either way, go on at step 6. Where it is a file, or a link (its line shows `->`), an
update stops on the file or on a link that leads outside the project, and writes the user guide
through any other link. Agree a new name with the author, such as `my-how-to`, and rename it:
for a file or link Git tracks,

```bash
git mv how-to my-how-to
```

or `mv how-to my-how-to` for one it does not, with the agreed name in place of `my-how-to`.
Then commit the rename, with a message the author agrees. The next update writes the guide into
a new `how-to` folder; in a project that already had the guide, it puts each file back and lists
it under `RESTORED`. _Substantive._

## 6. Run the update again

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

The author runs the update again in their own terminal, with the same answers as before; the
five settings in front turn Git's background housekeeping off for this one run, and
`--python '>=3.14'` runs Copier on Python 3.14 or later, which the update report needs: left to
itself, `uvx` may run Copier on an older Python it already has. Keep the quotes, or the shell
reads `>` as a redirection:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml
```

Where the stopped run changed an answer with `--data`, add the same `--data` at the end. A session has
no terminal for Copier's questions, so it never runs the command above; where the author asks a
session to run the update, it runs this form, which keeps every recorded answer:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust --defaults -a .copier-answers.syntek-media.yml
```

_Mechanical._

## 7. Confirm and continue

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/updating-the-template.md`

Copier should print 'Updating to template version' and the new version, never 'Keeping template
version'. The update should end with its report, whose first line starts
`▸ syntek-media update report` and names the version the project had before the arrow, never
the new version on both sides. Continue at step 6 of
`how-to/workflows/syntek-media/04-update-the-template/`, reading the migration output and the
report with the author. Where it stops again with `OSError: [Errno 39]`, which comes and goes,
start this procedure again at step 1; where it stops again on `how-to`, return to step 5. Where
it printed, in place of the report, a message framed in lines of `=` that says
`family-update did NOT run`, Copier ran on a Python older than 3.14 and nothing was reported,
refreshed or put back in `how-to/`: tell the author at once, look for conflict markers and
`.rej` files with them, commit the update, then run it again as step 6 shows, with
`--python '>=3.14'`. _Mechanical._
