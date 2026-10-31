---
type: guide
skills: []
model: opus
---

# Reporting a template problem — telling a fault in the template from an edit in the project, and reporting it safely

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Some faults are the template's: a copy that collides with a file it should have
left alone, a rule that contradicts another, a toolkit command that fails on a clean project, a
chapter that says something the rules do not. Others come from an edit in the project, a
settings entry left out, or a tool missing on this machine. Reporting a template problem means
telling the two apart, collecting what the maintainers need, leaving out everything private,
and sending it to the template's source.

## A template fault or a project edit

A fault is the template's when it happens in a file the template owns, as the template wrote
it, on a machine that `python3 toolkit/media.py check --setup` reports clean. So reproduce it
first, and rule out the project's own changes: `git status` and `git log` show what the project
has changed, and a template-owned file you edited is put right by the next update, not by a
report. A collision on a copy ('Interactive session required', ending 'Consider using
`--overwrite`') is always a template fault.

## What to collect

- The `_commit` and `_src_path` lines of `.copier-answers.syntek-media.yml`: the version you
  run, and the source the report goes to.
- The exact command you ran and Copier's or the tool's full output.
- The Python and Copier versions, with Copier asked as `uvx --python '>=3.14' copier --version`.
- What `python3 toolkit/media.py check --setup` reports.

## What never goes in a report

A report is public. Never include an API key, an ElevenLabs voice ID, a platform account ID, a
real person's name, a channel handle, a path inside your home folder, or a release form's
details. Replace each with a plain placeholder, and say that you did.

## A security problem

A problem that could expose a key, spend someone's credits or let a session edit what it must
not is reported privately, through the private vulnerability reporting at the source
`_src_path` names, and never in a public issue.

## How we apply it here

- A session drafts the report; the author reads it and files it. A session never files an issue
  and never writes an address: it names the source by `_src_path`.
- The draft is redacted before the author sees it, by the confidentiality rule.
- Work goes on under the rules as written until the maintainers answer.

## Who implements it

- `how-to/workflows/syntek-media/03-report-a-template-problem/`: every step, from reproducing
  the fault to the draft.
- No skill runs it; follow it by hand, step by step with its checklist open.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 10 owns what is confidential and never
written into a committed file or a report. The rules own the requirement; this guide owns the
everyday way to a safe report.
