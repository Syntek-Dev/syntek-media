---
type: guide
skills: []
model: opus
---

# Changing the answers — an answer changes only through an update, and a removal deletes what it made

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The answers given when the project was made are recorded in
`.copier-answers.syntek-media.yml`, and every update renders the template from them. An answer
changes only by passing the new one to an update with `--data`; the file is never edited by
hand, because a hand edit and the files rendered from the old answer would then disagree
silently. The brand section of the media rules follows the new answer on its own.

## Lists are replaced whole

`PLATFORMS`, `MEDIA_KINDS` and `AGENT_CLIENTS` are lists, and a list answer replaces the whole
list. `--data 'PLATFORMS=[youtube, podcast]'` keeps those two platforms and removes every other
one the project had, so the new answer names every value you keep as well as the one you add.

## A removal deletes what it generated

Removing a platform or a media kind deletes every file it generated, the seeds you have filled
in included, such as the platform's profile with everything you wrote in it. Git keeps the last
committed copy, and files you created yourself are never deleted. Every update prints, before it
asks its questions, what each removal deletes, workflows by full folder name: read that list,
copy out what you still need, and commit before you run the update.

## What never changes, and what follows a change

- **`BRAND_KIND` is frozen.** An update that answers it differently stops before it touches a
  file, because the mode files, the worked example and the brand seeds were written for one
  kind of brand. A different brand kind is a new project.
- **A newly ticked coding agent** brings only its row of the model table in
  `.claude/rules/syntek-media/05-model-allocation.md`. The update script offers the two MCP
  servers once to that client's files where they already stand, and writes none of them;
  `how-to/docs/syntek-media/enabling-a-coding-agent-client.md` explains how they come.
- **Hand edits follow a change of platforms or media kinds:** the shared files that describe the
  options (`README.md`, `CONTEXT.md` and `.claude/CLAUDE.md`, where media wrote them) and any
  rows for a removed platform in `brand/src/platforms/overrides.toml`.
- **A new platform** has a profile seed to fill in, in the platforms folder of the brand layer.

## How we apply it here

- The answer and its new value are named first, with the author, and a list is written out whole.
- A `BRAND_KIND` change is refused before any command runs.
- What a removal deletes is listed for the author, copied out and committed before the update.
- The update runs as every update does, on a branch from a committed tree, as
  `uvx --python '>=3.14' copier` with `-a .copier-answers.syntek-media.yml` and the five
  `GIT_CONFIG_*` variables, and its report is read before anything is committed.
- The hand edits are made after the update, and the change is committed with the answers file.

## Who implements it

- `how-to/workflows/syntek-media/02-change-the-answers/`: every step, with the update command.
- `brand/workflows/04-set-up-a-platform/`: a new platform's profile, once the update has run.
- No skill runs it; follow it by hand, step by step with its checklist open.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 11 owns how an answer changes, what a
removal deletes and what is edited by hand afterwards. The rules own the requirement; this guide
owns the everyday way through a changed answer.
