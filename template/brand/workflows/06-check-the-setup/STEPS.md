---
workflow: 06-check-the-setup
phase: review
skills: []
model: opus
---

# STEPS.md — check the setup

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for checking that this machine and this project are ready for media work.
Each step names the guide it uses. **Run in order** (the report before any fix, and every fix
checked by running the report again) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure: the toolkit's check reports, and the author fixes.

## 1. Run the check

> **Skill:** none · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Run `python3 toolkit/media.py check --setup` from the repository root. It changes nothing. Exit 0
means every line is clean; exit 1 means findings; exit 2 means it could not run, and the tool it
names is the first finding. If `python3` itself is missing or older than 3.11, nothing in the
toolkit runs: say so, and stop. _Mechanical._

## 2. Read each finding with its fix

> **Skill:** none · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Explain each finding to the author: what is missing, what it blocks, and the fix the report gives.

| Finding | Blocks until fixed |
|---|---|
| ffmpeg or ffprobe missing, or built without libass, x264 or mp3lame | every render, caption burn-in and audio master |
| Python older than 3.11 | the whole toolkit |
| uv missing | `card.py`: thumbnails, cards, and any master that holds a card |
| the pinned Playwright's Chromium missing | `card.py render` and `card.py check` |
| git-lfs or its filter missing while `brand/src/exports/large/` holds files | adding a large export |
| an allow entry missing from `.claude/settings.json` | nothing, but every toolkit call asks for permission |
| an ask entry missing from `.claude/settings.json` | every credit-spending ElevenLabs call, which would not prompt |
| a deny entry missing from `.claude/settings.json` | nothing, but a file in a generated or renders folder could be edited by hand |
| the ElevenLabs base path does not contain the repository | speech-to-text and every tool that reads a project file |

_Substantive._

## 3. Fix each finding with the author, one at a time

> **Skill:** none · **Guide:** `production/docs/reference/elevenlabs.md`

Give the exact command for each fix; the author installs software and re-adds the server. For
the base path, the re-add commands and the rule for choosing a folder that contains the project
are in `production/docs/reference/elevenlabs.md`; the key is exported in the author's shell
first and never typed on the command line. A permission entry is added to `.claude/settings.json`
only on the author's explicit word, exactly as the report prints it, changing nothing else in the
file. _Substantive._

## 4. Run the check again

> **Skill:** none · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Run `python3 toolkit/media.py check --setup` again after the fixes. Repeat until it exits 0, or
until every finding left open has been accepted by the author with the commands it blocks. No
credit-spending batch starts while an ElevenLabs line is open. _Mechanical._

## 5. Record

> **Skill:** none · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Add one dated line to `.claude/MEMORY.md` under Status (the heading syntek-author's
00-project.md Memory headings map it to, where present): the setup is clean, or which findings
are open and what each blocks. Supersede an earlier setup line rather than deleting it.
_Mechanical._

## 6. Hand back

> **Skill:** none · **Guide:** `.claude/rules/syntek-media/04-toolkit-pipeline.md`

Report each finding, fixed or open, and for each open one the commands and skills it blocks.
Never report a line as passed when the check could not run it. _Substantive._
