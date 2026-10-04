---
workflow: 04-set-up-a-platform
phase: author
skills: []
model: opus
---

# STEPS.md — set up a platform

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for filling one platform profile with the author. Each step names the skill
and guide it uses. **Run in order** (the social media plan is read before any choice is written,
because where it is present it owns most of them) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No media skill
> runs this procedure; `prepare-post` reads the profile it fills.

## 1. Confirm the platform

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Confirm the platform is one this project posts to: its profile exists as
`brand/src/platforms/<platform>.md`. If it does not, the platform is added by re-answering the
project's questions through Copier (`.claude/rules/syntek-media/06-global-rules.md` Section 11),
which brings its profile and its publishing guide; never make a profile by hand. Read the profile
as it stands. _Substantive._

## 2. Look for the social media plan

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Where syntek-author's social-media family is present (check the companion's
`.claude/skills/<skill>/SKILL.md` for social-media-documents, and ask the author where the plan
is kept), read its social media plan and content calendar for this platform. Where the plan
covers cadence, tone, call to action, hashtags and bios, the profile records only the account and
the deliverables used, and its other sections say the plan owns them. Where no plan is present,
say so: the profile holds all of it. _Substantive._

## 3. Record the account

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Write the handle and URL (for a podcast, the show's name, its feed and its listings) exactly as
the author gives them, and remove the section's flag. Never guess one. _Mechanical._

## 4. Choose the deliverables used

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Run `python3 toolkit/media.py presets` and show the author this platform's deliverables, each
with its `verify` keys and any override already applied. Record the keys the brand will use
under `## Deliverables used`; a key named in `verify` is still flagged by every checklist that
relies on it. _Substantive._

## 5. Set the cadence, the tone and the call to action

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Only where no social media plan owns them: offer options with a recommendation for how often and
when the brand posts here (times in the project's time zone, <%TIMEZONE%>), how its voice shifts
here, and what a viewer or listener is asked to do. Keep the tone consistent with
`brand/src/voice/voice.md` and the written voice. Write what the author decides, and remove each
flag. _Substantive._

## 6. Write the hashtag sets

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Only where no social media plan owns them: agree named sets with the author, each for a kind of
piece. Count each set against the platform's hashtag keys in `toolkit/data/platforms.toml`, cited
by key, never by number; `prepare-post` warns above them. _Substantive._

## 7. Record a confirmed correction as an override

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Only when the author has the platform's own current words and where they are published: add one
`[[override]]` table to `brand/src/platforms/overrides.toml` with the key, the value in the
field's own type, the platform's words, the source and the date checked, then run
`python3 toolkit/media.py presets` to see it applied. A difference not yet confirmed goes to
`publishing/workflows/07-refresh-the-platform-specs/` instead. Never edit
`toolkit/data/platforms.toml`. _Substantive._

## 8. Clear the flags, and record

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Run `python3 toolkit/media.py flags brand/src/platforms/` and confirm no flag is left in a section
`prepare-post` reads. Record the decisions in `.claude/MEMORY.md`, dated, under the heading
syntek-author's 00-project.md Memory headings map it to, where present. _Mechanical._

## 9. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Report what the profile now holds, what it cites from the social media plan, any override added
and its source, any `verify` key a deliverable relies on, and anything still flagged.
_Substantive._
