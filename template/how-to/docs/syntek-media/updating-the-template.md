---
type: guide
skills: []
model: opus
---

# Updating the template — taking syntek-media's improvements safely, and getting back from an update that stopped

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** An update brings syntek-media's later improvements into this project. Copier
renders the template's newer version with the answers recorded in
`.copier-answers.syntek-media.yml` and merges it into your files. The update script that ends
every update then refreshes the shared files, adds new settings entries, puts the user guide
back and prints a report, headed '▸ syntek-media update report', of every file it did not
simply deliver. An update starts from a committed tree, on a branch, one template at a time.

## What an update changes

- **Template-owned files** (the media rules, skills, guides, workflows and toolkit) are merged
  with any edits; where you and the template changed the same lines, both stay between
  conflict markers.
- **Seeds** are never overwritten; one you delete comes back empty.
- **Copy-only files** are never rendered again, but the family-shared ones are refreshed where
  you never changed them, and new settings entries and the two MCP servers are added once.
- **The user guide in `how-to/`** is put back wherever it differs, your edits and deletions
  included, and each file is listed under `RESTORED`; one it cannot safely put back is listed
  under `LEFT AS IT IS`, with the reason. What you had stays in Git.

## When an update stops

An update can stop after Copier has written the new version and moved the answers file forward,
before the report has run: with `OSError: [Errno 39] Directory not empty`, when Git's background
housekeeping collides with Copier; with `FileExistsError` or `NotADirectoryError` naming
`how-to`, when `how-to` is a file; or with `ForbiddenPathError`, when `how-to` is a link that
leads outside the project, or the .agents folder is one and the migration output says
`agents-outside-link did NOT run`. Never commit what it left: an update run over
it takes the new version as already reached and skips the steps that version needed. It is
discarded, after a dry run lists what the discard would delete, and the update is run again.

## How we apply it here

- One template at a time: where syntek-author is present, it is updated and committed first.
- A committed tree, untracked files included, on a branch; `how-to` a real folder.
- Every update command runs `uvx --python '>=3.14' copier` with
  `-a .copier-answers.syntek-media.yml` and the five `GIT_CONFIG_*` variables, which turn Git's
  housekeeping off for that one run (bash, zsh or another POSIX shell).
- The report is read with the author, every section of it, before anything is committed.
- A conflict or a `.rej` file under `how-to/` is settled only with the commands the report
  prints, never by editing the file. A departure from the guide is recorded in syntek-author's
  project settings file, 00-project.md, under Overrides or Workflow aliases, where that file is
  present, and otherwise in `.claude/CLAUDE.md` under the heading 'Project-specific rules'.
- New deny and ask rules are carried to the other clients with
  `python3 .claude/syntek-media-permissions.py`, `--check` first and `--write` on the author's
  word.

## Who implements it

- `how-to/workflows/syntek-media/04-update-the-template/`: an update, from a clean tree to a
  commit.
- `how-to/workflows/syntek-media/05-recover-a-stopped-update/`: an update that stopped part way.
- No skill runs either; follow each by hand, step by step with its checklist open.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 11 owns how an answer changes, and
Section 3 why the guide is never edited by hand; `.claude/rules/syntek-media/01-layout-and-routing.md`
Section 8 owns which files are the template's and which are yours. The rules own the
requirement; this guide owns the everyday way through an update.
