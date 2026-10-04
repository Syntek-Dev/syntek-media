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

## 2. Look for the written side's documents

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Where syntek-author's social-media family is present (check the companion's
`.claude/skills/<skill>/SKILL.md` for social-media-documents, and ask the author where its
documents are kept), read its social media plan, content calendar and any operating procedure for
this platform, document by document. A document covers the platform when it names it with a
cadence; whatever any of them sets (cadence, tone, call to action, hashtags, bios) it owns, and
the profile's section cites it in prose. The profile holds the account (or the sites or lists)
and the deliverables used, and only what no document sets. Where none is present, say so: the
profile holds all of it. _Substantive._

## 3. Record the account

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Write the handle and URL exactly as the author gives them, and remove the section's flag; never
guess one. For a podcast, one row per show: its register's slug, its name, where its feed is
served and its listings. For the website and blog profiles, one row per site under `## Sites`, and
for the newsletter profile one row per list under `## Lists`: a kebab slug the author agrees
(frozen once a schedule row uses it), the domain or sender as given, the owner, and for a site or
list the brand does not own, the dated record of its agreement in Agreement, recorded once (a blog
row reads 'see website' where the website profile lists the site). No subscriber, count, password
or account ID goes in a row. _Mechanical._

## 4. Choose the deliverables used

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Run `python3 toolkit/media.py presets` and show the author this platform's deliverables, each
with its `verify` keys and any override already applied. Record the keys the brand will use
under `## Deliverables used`; a key named in `verify` is still flagged by every checklist that
relies on it. _Substantive._

## 5. Set the cadence, the tone and the call to action

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Only where no written-side document sets them: offer options with a recommendation for how often and
when the brand posts here (times in the project's time zone, <%TIMEZONE%>), how its voice shifts
here, and what a viewer or listener is asked to do. Keep the tone consistent with
`brand/src/voice/voice.md` and the written voice. Write what the author decides, and remove each
flag. _Substantive._

## 6. Write the hashtag sets

> **Skill:** none · **Guide:** `brand/docs/reference/platform-profiles.md`

Only where no written-side document sets them, and only on a platform that takes hashtags (the
brand's own sites, blogs and newsletters take none): agree named sets with the author, each for a kind of
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

Report what the profile now holds, what it cites from the written side's documents, each site's
or list's agreement still to come, any override added
and its source, any `verify` key a deliverable relies on, and anything still flagged.
_Substantive._
