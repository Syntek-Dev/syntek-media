---
workflow: 03-report-a-template-problem
phase: review
skills: []
model: opus
---

# STEPS.md — report a template problem

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for reporting a fault in syntek-media, from confirming it is the template's
to a draft the author files. Each step names the guide it uses. **Run in order**, from the top
folder of the project, and tick `CHECKLIST.md` as you go. Every command runs exactly as written,
in bash, zsh or another POSIX shell, and changes nothing in the project.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure. A session drafts the report; only the author files it.

## 1. Confirm the fault is the template's

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/reporting-a-template-problem.md`

Reproduce it first: run the failing command again where that spends nothing and changes nothing,
or read the file again, and note the exact words. A stopped update is never run again here:
follow `how-to/workflows/syntek-media/05-recover-a-stopped-update/`, and report only what still
fails after it. Then rule out the project's own edits. Where a file is at fault, this command
lists every commit that touched it; put its path in place of `FILE`:

```bash
git log --format='%h %ad %s' --date=short -- FILE
```

A commit the author made, rather than a copy or an update of the template, may be the cause. To
compare the file with the template's own text at the recorded version, these commands render a
fresh project into a new temporary folder, outside the project, and print its path:

```bash
SRC=$(sed -n "s/^_src_path: *['\"]\{0,1\}\([^'\"]*\).*/\1/p" .copier-answers.syntek-media.yml)
REF=$(sed -n "s/^_commit: *['\"]\{0,1\}\([^'\"]*\).*/\1/p" .copier-answers.syntek-media.yml)
FRESH=$(mktemp -d)
uvx --python '>=3.14' copier copy --trust --defaults --vcs-ref="$REF" --data-file .copier-answers.syntek-media.yml "$SRC" "$FRESH"
echo "$FRESH"
```

Then `diff "$FRESH/FILE" FILE` shows every line where the project's file differs. The same fault
in the fresh render is the template's; one only in the project is the project's, and this
procedure ends there. Never run a copy over the real project. Once the comparison is done, the
author removes the temporary folder with `rm -rf "$FRESH"`. _Substantive._

## 2. Collect the versions and the output

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/reporting-a-template-problem.md`

These commands print the template's recorded version and its source:

```bash
sed -n 's/^_commit: *//p' .copier-answers.syntek-media.yml
sed -n 's/^_src_path: *//p' .copier-answers.syntek-media.yml
```

Where the project also holds `.copier-answers.syntek-author.yml`, run the first command on that
file too, and note that the project is beside syntek-author. Note the brand kind, from
`sed -n 's/^BRAND_KIND: *//p' .copier-answers.syntek-media.yml`. Copy the exact command that
failed and everything it printed, the error included. Then collect the set-up report and the
versions of the tools:

```bash
python3 toolkit/media.py check --setup
uvx --python '>=3.14' copier --version
python3 --version
git --version
uname -sr
```

Where the toolkit was involved, add the first line of `ffmpeg -version`. _Mechanical._

## 3. Redact

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/reporting-a-template-problem.md`

Read everything collected with the author, line by line, and take out what
`.claude/rules/syntek-media/06-global-rules.md` Section 10 keeps private: API keys and any line
that holds one, voice IDs, Claude Design links, platform account IDs and channel handles, a real
person's name or a release form's details, and private correspondence. Write a home folder as
`~`, and replace any other absolute path that names a person or a machine with a short
description. Where `_src_path` is a folder on this machine, write that the project came from a
local clone, and of which release. Leave every error message, file name inside the project and
version as it is. _Substantive._

## 4. Send a security problem privately

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/reporting-a-template-problem.md`

A security problem is one that would let something run, spend or be read without the author's
say: a permission rule that lets a paid call run without its prompt, a command that reads or
writes outside the project, a migration that touches more than it says. Never put one in a
public issue, discussion or pull request. The author reports it through the source's private
vulnerability reporting, such as the source's Security tab and its 'Report a vulnerability'
where the source is on GitHub, with the draft of step 5 as its text. _Substantive._

## 5. Draft the issue for the author

> **Skill:** none · **Guide:** `how-to/docs/syntek-media/reporting-a-template-problem.md`

Write the draft in the session, never into a file in the project, under these headings:

- **Title:** what failed and where, in one line.
- **What happened**, with the path and line of the file, or the step where it happened.
- **What you expected instead**, and where a file the template wrote says so.
- **Steps to reproduce**, from a clean, committed tree, each command as it was run.
- **Full output**, redacted, in a fenced block.
- **Versions:** syntek-media's `_commit`; syntek-author's, where present; the brand kind;
  standalone or beside syntek-author; Copier, Python, git and the system; the set-up report.

Give the author the draft and the source as `_src_path` names it. The author files the issue
there, using the source's bug report form where it has one; a session never files it, and never
writes the source's web address. _Substantive._
