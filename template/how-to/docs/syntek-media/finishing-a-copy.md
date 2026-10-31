---
type: guide
skills: []
model: opus
---

# Finishing a copy — what a copy of syntek-media leaves to the author, and finishing it before the first spend

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A copy of syntek-media writes every file the project lacks and leaves every
shared file that already stands exactly as it was, so a project that already had a
`.claude/settings.json` keeps its own. The copy then prints, at its end, the few things it
cannot do for you. Finishing the copy means doing those by hand, checking the set-up, and
committing, before any session spends a credit.

## What the copy has already done

On Python 3.14 or later, the copy's last step, the `baseline` task, records the version just
copied for the first update's report and offers the settings entries and MCP servers the
template lists to the files the copy kept, once each: the compaction settings, the asks for every
ElevenLabs tool that spends credits, for `voice remix run` and for the Scrapling and
code-review-graph tools, the denies (the generated and renders folders and `how-to/` among them),
and the handoff and guide-guard hooks. It never removes or
changes an entry of yours. A copy that made `.claude/settings.json` itself already holds all of
them.

## What stays by hand

- **The allows no lane offers.** Where the copy kept an existing settings file, its `"allow"`
  list needs the toolkit, ffmpeg and ffprobe entries and `WebSearch` and `WebFetch`, as the
  message after the copy lists them; without them every toolkit call asks for permission.
- **The data-root guard,** the seed's other `PreToolUse` hook, in a settings file that lacks it:
  no copy or update in either template adds it.
- **Everything the `baseline` task offers,** where it did not run: the copy printed, framed in
  lines of `=`, that family-update did NOT run (a Python older than 3.14), or ran with
  `--skip-tasks`.
- **The other clients' settings.** `python3 .claude/syntek-media-permissions.py --write` carries
  the asks and denies to each other coding agent's settings file the project has, after
  `--check` has shown what it would change. It never creates a file.
- **The ElevenLabs server,** added once at user scope with a base path that contains the
  project, the key exported in your shell and never typed or committed.
- **Git LFS,** with `git lfs install` once, where large design exports will be kept.
- **The setup check,** `python3 toolkit/media.py check --setup`, cleared before the first call
  that spends credits.

## How we apply it here

- Read what the copy printed first: 'conflict' then 'skip', or 'identical', is expected for a
  shared file; a collision ('Interactive session required', ending 'Consider using
  `--overwrite`') stops the work and is reported.
- Every change to a settings file is made on the author's word, and never removes or weakens an
  entry the author already has.
- The index lines in `README.md`, `CONTEXT.md` and `.claude/CLAUDE.md` are optional: the media
  rules load at launch whatever those files say.
- The copy is committed with `.copier-answers.syntek-media.yml`, which every update merges
  against.

## Who implements it

- `how-to/workflows/syntek-media/01-finish-a-copy/`: every step, with its commands.
- `brand/workflows/06-check-the-setup/`: the setup check, finding by finding.
- No skill runs it; follow it by hand, step by step with its checklist open.

## Governing standard

`.claude/rules/syntek-media/01-layout-and-routing.md` Section 10 owns where the project's own
settings and departures are recorded; `.claude/rules/syntek-media/03-production-ethics.md`
Section 4 owns why no credit is spent before the setup check is clean. The rules own the
requirement; this guide owns the everyday way through the end of a copy.
