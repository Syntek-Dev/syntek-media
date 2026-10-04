---
workflow: 02-sync-with-claude-design
phase: author
skills: []
model: opus
---

# STEPS.md — sync with Claude Design

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for bringing components across between the brand kit and its Claude Design
project. Each step names the skill and guide it uses. **Run in order** (nothing moves before the
kit is committed and checked, and nothing moves that the author has not named) and tick
`CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure: the sync is the author's command, and Claude reads, checks and records
> alongside it.

## 1. Confirm what moves, and which way

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

Ask the author which components move (a token group, a card, a layout) and in which direction:
from the design project into the repository, or from the repository into the design project. If
nothing was asked, stop. _Substantive._

## 2. Make the kit clean

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

Confirm with `git status` that `brand/src/design-system/` has no uncommitted change, or commit it
first with the author's agreement, so that the sync's changes show as their own diff. Run
`python3 toolkit/media.py tokens` and `uv run toolkit/card.py check` on every card; fix a failure
through `brand/workflows/01-set-up-the-brand-kit/` before anything moves. _Mechanical._

## 3. Choose the route

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

Read `.claude/MEMORY.md` for an earlier sync. `/design-sync` is the route the brand asked for;
its converter is built for React component packages and Storybook, so its first run on this
plain HTML kit is unproven (`VERIFY`). Where an earlier run is recorded as refusing or rewriting
the kit, use route two at step 5. Tell the author which route and why. _Substantive._

## 4. The author starts `/design-sync`

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

The author types the command; Claude never starts it. Where access is not yet authorised, the
author runs `/design-login` first. Give the author this hint to pass with it:

```text
/design-sync brand/src/design-system/ is a hand-authored HTML kit, not a React package:
tokens.css holds the CSS custom properties, fonts/ the font files, and previews/*.html one card
each, with an @dsCard comment on line 1. Sync only the components named, one at a time; never
convert, rename, delete or replace the kit wholesale.
```

Watch what it proposes. If it proposes to convert, rewrite, rename or delete anything beyond the
named components, the author cancels it, and the sync continues by route two. Record what the
first run did, dated, in `.claude/MEMORY.md`. _Substantive._

## 5. Or: `/design export` and `/design import`, through a scratch folder

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

For the repository into the design project, the author runs `/design export` on a scratch copy of
the components to send. For the design project into the repository, the author runs
`/design import` with the project, into a scratch folder outside `brand/`, never into the kit.
Check where each verb writes before its first use (`VERIFY`), and keep the scratch folder out of
Git. _Mechanical (moving files); deciding what comes across is substantive._

## 6. Bring each component across, one at a time

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

For one component, show the author the change against the kit as it stands; on a yes, apply it
under the component's existing name; then the next. Never delete a card, rename a required
token, move a card's line 1 or take a value typed in place of a token. A design that arrives with
an exported file is filed through `brand/workflows/03-record-a-design-export/`. _Substantive._

## 7. Check after each component

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Run `python3 toolkit/media.py tokens` and `uv run toolkit/card.py check` on the card that
changed. For `thumbnail.html` or `card.html`, render a landscape and a vertical proof into
`production/src/renders/` and tell the author that the change reaches every piece copied from
now on, and no thumbnail or card already copied. _Mechanical._

## 8. Record

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

The first time, add the design project's row to `brand/src/design-register.md` with the link the
author gives, and dashes for its export columns. Record in `.claude/MEMORY.md`, dated, what was
synced, in which direction and by which route. With the author's agreement, commit with a
message naming the components. _Mechanical._

## 9. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/claude-design.md`

Report each component synced and its direction, the route used, the checks and proofs, and
anything changed on one side and not yet synced, which a handoff must carry
(`.claude/rules/syntek-media/07-session-boundaries.md` Section 3). _Substantive._
