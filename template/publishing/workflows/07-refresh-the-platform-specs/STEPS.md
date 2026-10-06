---
workflow: 07-refresh-the-platform-specs
phase: review
skills: []
model: opus
---

# STEPS.md — refresh the platform specs

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for re-reading stale platform data at its source and recording what has
changed. Each step names the guide it uses, and any toolkit command. **Run in order** — the
ordering is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/platform-specs.md`. No media skill runs this procedure; the research
> skill (syntek-author), where present, helps with the reading.

## 1. List the stale tables

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Run `python3 toolkit/media.py presets --stale-after 183 --today DD/MM/YYYY`, with today's date.
Exit 1 lists every table checked more than about six months ago; exit 0 means none is stale. Add
every `verify` key a render or package is about to rely on, whatever its date. _Mechanical._

## 2. Narrow the list to what the project uses

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Keep the tables of the platforms this project posts to (the brand section of
`.claude/rules/syntek-media/01-layout-and-routing.md`) and the deliverables its briefs and
platform profiles name. A table the project never uses is noted and left for another time.
_Mechanical._

## 3. Re-read each source

> **Skill:** research (syntek-author), where present · **Guide:** `publishing/docs/reference/platform-specs.md`

For each table on the list, open its `source` and `extra_sources` on the platform's own help,
developer or ads pages, and note what each value says today, and the date it was read. A value the
platform's own page does not state stays in `verify`; a press report or a third party may point to
a change, never confirm one. _Substantive._

## 4. Propose the overrides

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

For each confirmed difference, draft an `[[override]]` row: `key` as
`<platform>.<format>.<field>`, `value` in the field's own type, `why` (what the platform now says),
`source` (the page it says it on) and `checked` (today, DD/MM/YYYY). Put every row to the author
with the page it rests on. _Substantive._

## 5. Record what the author confirms

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Append each confirmed row to `brand/src/platforms/overrides.toml`. **Never edit
`toolkit/data/platforms.toml`**: `copier update` replaces it, and an edit there becomes a
conflict. _Mechanical._

## 6. Check each override applies

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Run `python3 toolkit/media.py presets KEY` for each deliverable an override touches, and confirm
the toolkit prints the override and uses its value. A row it does not apply is fixed before
anything relies on it. _Mechanical._

## 7. Retire overrides the data file has caught up with

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Where a `copier update` has brought `toolkit/data/platforms.toml` into line with an override, the
override is now redundant. Propose its removal to the author, and remove it only on the author's
word. _Substantive._

## 8. Re-read the disclosure rules

> **Skill:** none · **Guide:** `publishing/docs/reference/ai-disclosure.md`

Re-read the source of each row of the disclosure guide for a platform this project posts to. A
rule that has changed is reported to the author; on the author's word it is recorded in a
same-named guide in `publishing/docs/project/`, which overrides the reference guide. The
reference guide itself is never edited.

Re-read the platform/surface advice used by the Jev scorecard too, following
`publishing/docs/reference/scoring-options.md`. Separate official published advice from labelled
hypotheses; report announced changes and stale or unresolved sources. On the author's word,
update project guides and the project rubric, increment their versions, and use the revised
context in new option JSON. Never change a checked date without reading its source, invent
algorithm weights, edit the toolkit rubric in a generated project or rewrite past score results. _Substantive._

## 9. Hand back

> **Skill:** none · **Guide:** `publishing/docs/reference/platform-specs.md`

Report every table re-read and the date, every override added or retired, every value still in
`verify`, every disclosure rule that changed, and any deliverable already rendered or packaged
that a corrected value affects (for `publishing/workflows/02-cut-for-a-platform/` or
`publishing/workflows/05-prepare-a-post/`). Record the refresh date in `.claude/MEMORY.md` under
Status, or the heading syntek-author's project settings file maps it to, where present, and name
the next refresh, about six months on. _Substantive._
