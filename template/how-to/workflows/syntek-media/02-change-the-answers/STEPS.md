---
workflow: 02-change-the-answers
phase: plan
skills: []
model: opus
---

# STEPS.md — change the answers

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for changing an answer through an update, from naming it to a commit.
Each step names the guide it uses. **Run in order**, from the top folder of the project, and
tick `CHECKLIST.md` as you go. Every command runs exactly as written, in bash, zsh or another
POSIX shell.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure. Every step that changes the project waits for the author's word.

## 1. Name the answer and its new value

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

This command prints every answer the project recorded, under its question's name:

```bash
cat .copier-answers.syntek-media.yml
```

Agree with the author which question changes, by that name, and its new value, word for word.
`how-to/src/TEMPLATE-GUIDE/syntek-media/05-the-answers.md` explains each question and what it
costs to change. Where the project also holds `.copier-answers.syntek-author.yml`, a coding
agent or a data-root answer is best changed in both templates alike: the message after the
update names any data-root answer the two records disagree on. _Substantive._

## 2. Refuse a change of brand kind

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

Where the answer is `BRAND_KIND`, stop here and tell the author: the update refuses a different
brand kind and touches nothing, because a different brand kind is a new project. Where they
still want one, the way forward is a new project, made by a fresh copy into another folder.
_Substantive._

## 3. Give a list answer whole

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

`PLATFORMS`, `MEDIA_KINDS` and `AGENT_CLIENTS` are lists, and a new list replaces the old one
entirely: every value it leaves out is removed. Write out with the author the whole list the
project keeps, each value as step 1's command printed it, the new one added or the departing one
left out, such as `[youtube, podcast]`. Every other answer is a single value. _Substantive._

## 4. List what a removal deletes, and commit what the author needs

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

Where a platform or a media kind leaves its list, the update deletes every file it generated,
seeds the author has filled in included, such as the platform's profile. The update prints that
list before its first question, and
`how-to/src/TEMPLATE-GUIDE/syntek-media/11-platforms-and-media-kinds.md` describes what each
kind of value takes with it: read it with the author, for each departing value, before the
update runs. The author copies out what they still need, and every file in the list is
committed. This command should then end `nothing to commit, working tree clean`:

```bash
git status
```

Files the author created themselves are never deleted. Where nothing is removed, skip this step.
_Substantive._

## 5. Prepare the tree for the update

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

Run steps 1 to 3 of `how-to/workflows/syntek-media/04-update-the-template/`, with their
commands: a clean, committed tree in its own repository on the branch `update-syntek-media`;
syntek-author updated and committed first, where the project holds its answers file; and the
three names an update handles with care checked with `ls -ld .agents .agents.syntek-held how-to`.
Come back here once they pass. _Mechanical._

## 6. Run the update with the new value

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

The update takes the new answer from `--data`, followed by the question's name, `=` and the
value, in single quotes; Copier then does not ask that question. The command below changes the
platforms to the list `[youtube, podcast]`: put the question and the value settled at steps 1
and 3 in their place, and add one more `--data` for each further answer that changes. The five
settings in front turn Git's background housekeeping off for this one run, and
`--python '>=3.14'` runs Copier on Python 3.14 or later, which the update report needs. The
author runs it in their own terminal, where Copier asks every other question again, each with
the recorded answer as its default:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust -a .copier-answers.syntek-media.yml --data 'PLATFORMS=[youtube, podcast]'
```

A session never runs that form: it has no terminal, so Copier stops with
`Interactive session required`. Where the author asks a session to run the update, it runs this
form instead, in which `--defaults` keeps every other recorded answer:

```bash
GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=gc.auto GIT_CONFIG_VALUE_0=0 GIT_CONFIG_KEY_1=maintenance.auto GIT_CONFIG_VALUE_1=false \
  uvx --python '>=3.14' copier update --trust --defaults -a .copier-answers.syntek-media.yml --data 'PLATFORMS=[youtube, podcast]'
```

A refused `BRAND_KIND` stops the update before it writes anything. _Mechanical._

## 7. Read the report and the changes

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

Follow the end of step 5 and steps 6 and 7 of
`how-to/workflows/syntek-media/04-update-the-template/` with the author:
the run should end with the update report, whose first line starts
`▸ syntek-media update report`; a stop with an error goes to
`how-to/workflows/syntek-media/05-recover-a-stopped-update/`, with nothing committed; then the
migration output, every section of the report, `git status` and `git diff`. A removal shows
under `DELETED` only the files the author had changed, each with the `restore` command that
brings it back; the rest of the list read at step 4 is gone without an entry, and is in the
last commit before the update. A `MissingFileWarning` about an answers file is expected and harmless. _Substantive._

## 8. Make the hand edits

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

The brand section of the media rules updates itself, but no update rewrites a seed or a shared
file. After a change of platforms or media kinds, edit by hand, with the author, the files that
describe the project's options: `README.md`, `CONTEXT.md` and Section 1 of `.claude/CLAUDE.md`
in a project made by syntek-media alone (over syntek-author they are syntek-author's, and are
edited only where the author wants), and, for a removed platform, its rows in
`brand/src/platforms/overrides.toml`. After any other change, edit the seeds that quote the old
answer, where the author wants them to match. _Substantive._

## 9. Carry on with what the new answer brings

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

The update writes a new platform's profile empty and a new coding agent's row of the model
table, and nothing more:

- **A new platform:** fill in its profile with `brand/workflows/04-set-up-a-platform/`, after the
  commit at step 10.
- **A new coding agent:** add its files with
  `how-to/workflows/syntek-media/06-enable-a-coding-agent-client/`, after the commit at step 10;
  the client is already recorded, so that procedure starts at its step 2.

Where neither applies, skip this step. _Substantive._

## 10. Commit, with the answers file

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/changing-the-answers.md`

Once every conflict is resolved and the author has agreed every change, this command commits the
whole update, `.copier-answers.syntek-media.yml` included, which every later update works from:

```bash
git add -A && git commit -m 'Update from syntek-media'
```

Afterwards `git status` should end `nothing to commit, working tree clean`. Merge the branch
into the project's main line with the author, the way they usually do. _Mechanical._
