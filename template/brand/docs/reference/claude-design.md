---
type: guide
skills: []
model: opus
---

# Claude Design — keeping the brand and its design project in step

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The brand has one design-system project in Claude Design, where layouts are
explored and refined visually. The repository's `brand/src/design-system/` is the source of
truth: `tokens.css`, the fonts and the preview cards every render reads. The two are kept in
step by a sync the author starts, incremental and one component at a time, never a wholesale
replace in either direction. This guide covers the two routes, what moves, and what a sync must
never do.

## What the kit is, to Claude Design

- A hand-authored HTML kit: plain CSS and HTML, with no React, no Node and no package.
- Each preview card's first line, `<!-- @dsCard group="…" -->`, is what the Design System pane
  builds its card index from; the groups are `Colors`, `Type`, `Spacing`, `Brand` and
  `Components`.
- The project's link is recorded once, in `brand/src/design-register.md`, and nowhere else.

## Route one: `/design-sync`, started by the author

- The author types `/design-sync` (Claude cannot start it), with a hint that names the kit:
  that it lives at `brand/src/design-system/`, that it is a hand-authored HTML kit of
  `tokens.css`, a fonts folder and `previews/*.html` with `@dsCard` first lines, and that there
  is no React package to convert. `/design-login` authorises access once, with the author's
  claude.ai account.
- Its converter is built for React component packages and Storybook, so what the first sync does
  with a plain HTML kit is unproven: treat it as `VERIFY`, watch what it proposes, and record what
  happened in `.claude/MEMORY.md` with the date.
- If it refuses the kit, or proposes to convert or rewrite it, stop and use route two.

## Route two: `/design import` and `/design export`

- `/design export` creates or updates a design project from a working folder; `/design import`
  pulls a project's files into one. Both move whole folders, so point them at a scratch folder
  outside `brand/` (`VERIFY` where each writes before its first use), never at the kit itself.
- Bring each change across by hand from the scratch copy, one component at a time, as below.

## One component at a time

- **Before:** commit the kit; run `python3 toolkit/media.py tokens`, and
  `uv run toolkit/card.py check` on every card.
- **During:** one component per round: show the author the change, wait for a yes, then the
  next. Never delete a file, rename a required token or replace the kit wholesale.
- **After:** run the checks again, render a proof of any layout that changed, and commit with a
  message naming the components.
- **The two layouts:** a change to `brand/src/design-system/previews/thumbnail.html` or
  `brand/src/design-system/previews/card.html` reaches every piece copied after it, and never
  a thumbnail or card already copied; say so before it syncs.

## How we apply it here

- The author starts every sync; Claude never starts one unasked, and never syncs a component the
  author has not named.
- A sync needs the author's claude.ai sign-in; without it, say so and stop.
- Changes made on one side and not yet synced are named in the handoff.

## Who implements it

- **Workflow:** `brand/workflows/02-sync-with-claude-design/`.
- **Skills:** none; the sync is the author's command, and Claude reads, checks and records
  alongside it.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 4 owns never overwriting a brand file or
an exported design asset without confirmation, and Section 8 the grilling pass design work opens
with; `.claude/rules/syntek-media/07-session-boundaries.md` Section 3 owns naming unsynced
design changes in a handoff. The rules own the requirements; this guide owns how the brand and
its design project are kept in step.
