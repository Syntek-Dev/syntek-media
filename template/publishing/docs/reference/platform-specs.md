---
type: guide
skills: [cut-for-platform, prepare-post]
model: opus
---

# Platform specs — how the platform data is read, corrected and kept fresh

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Every platform limit this project relies on (a size, a length, a codec, a caption
format, a character count) lives in one dated file, `toolkit/data/platforms.toml`, built from each
platform's own help pages and read by the toolkit's presets, `cut-for-platform`, `thumbnail-brief`
and `prepare-post`. No guide, plan or package writes a limit as a number: each cites its key, so
that when a platform changes its rules there is one place to change. The file is template-owned
and refreshed by `copier update`; the brand's confirmed corrections live beside its profiles.

## Reading a table

- `[platform.<name>]` holds a platform's account-wide limits: title, description, caption and
  post characters, hashtag rules, the grid crop, the AI-label field.
- `[platform.<name>.<format>]` is one deliverable; `<platform>.<format>` is its key
  (`youtube.short`), and `<platform>-<format>` its form in a file name, with the dot and every
  underscore turned into hyphens (`linkedin.video_vertical` becomes `linkedin-video-vertical`),
  in a render, a thumbnail and a caption qualifier alike.
- `[audiobook.<store>]` is a mastering and delivery target, read by the audiobook route.
- `python3 toolkit/media.py presets KEY` prints a table as the toolkit will use it, with its
  `verify` keys and every override applied; with no key it prints them all.

## The verify, chosen and absent keys

| Field | Means | What to do |
|---|---|---|
| `verify` | these keys were not confirmed from an official source on `checked` | rely on them only with a `VERIFY` flag in the plan or package |
| `chosen` | a house choice inside an official range, not a platform rule | change it only on the author's word |
| an absent key | the platform publishes no value | keep the source's value (frame rate, sample rate) or skip the check |
| `max_size` | copied exactly as the platform states it | never convert the units |
| `safe_zone` | pixels at the table's size; `0` means none published for that edge | scale it for another size |
| `caption_formats = []` | no sidecar upload is documented | burn the captions in |
| `notes` | what the source says that no field can hold | read it before trusting the numbers |

## Overrides

A confirmed difference between a platform and this file is never fixed by editing it: the next
`copier update` would undo the edit, or turn it into a conflict. It is an `[[override]]` row in
`brand/src/platforms/overrides.toml`, with `key` (`<platform>.<format>.<field>`), `value` (of the
field's own type), `why` (what the platform now says), `source` and `checked` (DD/MM/YYYY). The
toolkit applies every override and prints it, so a corrected limit is never silent. When an
update brings the data file into line, the override is retired, on the author's word.

## Staleness

Platforms change their limits without notice. Every table carries `checked` and `source`;
`python3 toolkit/media.py presets --stale-after 183 --today DD/MM/YYYY` lists every table checked
more than about six months before today, and a stale table is re-read at its source before a
render or a package relies on it.

## How we apply it here

- A plan or package cites the key, then the value `presets` printed, never the value alone.
- A `verify` key relied on is named in the hand-back, every time.
- A source re-read is dated; a value nobody could confirm stays in `verify`.

## Who implements it

- **Workflow:** `publishing/workflows/07-refresh-the-platform-specs/` finds stale tables, re-reads
  their sources and records each confirmed difference as an override.
- **Skills:** `cut-for-platform` reads each deliverable's preset before rendering; `prepare-post`
  reads the character and hashtag keys before writing a package.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 7 owns never fabricating a platform
rule or limit; `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns data held as
TOML and read by the toolkit. The rules own the requirement; this guide owns reading, correcting
and refreshing the platform data.
