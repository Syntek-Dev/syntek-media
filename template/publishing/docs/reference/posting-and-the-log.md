---
type: guide
skills: [prepare-post]
model: opus
---

# Posting and the log — the package, the schedule, the author's post, the record

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A deliverable goes out in four moves, and Claude makes only the first two:
`prepare-post` writes the post package (everything the author pastes, sets and uploads) and a
schedule row for each deliverable; the author posts; and the publish log records what the author
reports, from the date and the URL to the disclosure that was set. Nothing in the repository
posts, uploads or calls a platform's API, and a log row exists only for an upload the author has
reported.

## The post package

`publishing/src/posts/<piece>.md` carries frontmatter `piece` and `approved`, then one H2 per
deliverable, `## <platform>.<format>` (with ` — cNN` for a cut), each with these bold-led bullets:

| Bullet | Holds |
|---|---|
| **Title** | the title as it will be pasted |
| **Description** | a fenced block, one sentence per line like every `src/` file, its words exactly as they will be posted, the disclosure line included; `prepare-post` joins the lines into paste-ready text in chat when the author posts |
| **Hashtags** | the set, inside the platform's keys; above `platform.instagram.hashtags_max` warns |
| **Disclosure** | the label and its setting with its rule, the description line, any spoken or on-screen line |
| **Captions** | the caption file, and whether it is burned in or uploaded |
| **Thumbnail** | the thumbnail's render name, or `n/a` with the reason |
| **Render** | the deliverable's render name |
| **Calendar** | the content calendar entry, where syntek-author's is present |
| **Scheduled** | DD/MM/YYYY HH:MM, <%TIMEZONE%> |
| **Limits** | each count against its `toolkit/data/platforms.toml` key |

**A placement** is the one file a page of a profile site or an issue of a list plays or shows
first, under its own H2 qualified `— <platform>:<slug>`; its other images are bullets of it, and
it holds only the words outside its written piece. Its bullets are in the website, blog and
newsletter guides, and a feed episode's in the podcast-feed guide, where the project has them.

## The schedule

`publishing/src/schedule.md` holds one row per deliverable to go out, under the columns
`Date · Time · Platform · Deliverable · Piece · Package · Status · Notes`. Status is `planned`
when the package is written, `ready` once the piece passes M7 (captioned → scheduled), `moved`
when the author changes the date (the row takes the new date; Notes keep the old one), `posted`
once the author reports it, or `dropped`, with the reason. Rows are never deleted. A placement's
Platform is `<platform>:<slug>` and its Deliverable the key of its one file; inside a written piece
it takes its Date and Time from that piece, cited in Notes, and is `moved` when that piece moves.

Where syntek-author's social-media documents are present, whichever sets a value (the plan, the
calendar or an operating procedure) owns it: text-only posts and bios are theirs, and the schedule
lists only media deliverables, each row's Notes citing its calendar entry. Standalone, or in a book
project, the schedule holds the whole plan for media. A piece is `published` once every row for
it is `posted` or `dropped`, each posted row with its log row (the ladder guide's last row).

## The publish log

`publishing/src/publish-log.md` has one row per upload or placement the author reports, under the
columns `Date · Platform · Deliverable · Piece · URL · Disclosure set · Captions · Notes`, never
pruned. The URL is the author's, never guessed or built from a handle. Disclosure set is what the
author set: a difference from the package is reported, and a mistake gets a dated note under the
log's `## Corrections`.

## How we apply it here

- A log row is written only from the author's report, never from the package or the schedule.
- A package is approved whole, by the author, before its first schedule row becomes `ready`.
- Times are 24-hour, in <%TIMEZONE%>; dates DD/MM/YYYY; one sentence per line in Notes.

## Who implements it

- **Workflows:** `publishing/workflows/05-prepare-a-post/` writes the package and the schedule
  rows; `publishing/workflows/06-record-a-publication/` logs the author's post and closes the piece.
- **Skill:** `prepare-post` does both, and never posts.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 1 owns who decides (every publish is
the author's) and Section 3 owns the ladder, M7 and the definition of published. The rules own the
requirement; this guide owns the package, the schedule and the log.
