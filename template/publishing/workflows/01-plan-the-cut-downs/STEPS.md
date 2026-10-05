---
workflow: 01-plan-the-cut-downs
phase: convert
skills: [repurpose]
model: opus
---

# STEPS.md — plan the cut-downs of a master

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for turning one finished master into an agreed plan of short cuts. Each step
names the skill and guide it uses. **Run in order** — the ordering is load-bearing — and tick
`CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/cut-downs.md`. The `repurpose` skill is this procedure in skill form;
> read it, and its mode file, before step 1.

## 1. Confirm the piece and its master

> **Skill:** `repurpose` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

Read the piece's brief, `scripts/src/pieces/<piece>/brief.md`. Its `verified` must date M4: the
master exists, probes clean and the author has watched it through. Find the master in the
piece's own folder, `production/src/renders/<piece>/`; a missing render is remade by
`production/workflows/03-assemble-the-master/`, never stood in for. **Without a master there is
nothing to time a cut against: stop.** _Mechanical._

## 2. Read what the piece must carry

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

Read the brief's purpose, audience and call to action; the script, or a recorded piece's
transcript, with its `beat.line` numbering; and, where syntek-author's content calendar is
present, the entries it plans for this piece. A calendar entry asks for a cut; it never chooses
the moment. _Substantive._

## 3. Read each platform's limits

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/platform-specs.md`

For each platform a cut may go to, read its guide in `publishing/docs/reference/` and run
`python3 toolkit/media.py presets KEY` for each candidate deliverable. Note `max_seconds`,
`safe_zone`, `caption_formats`, every key in `verify`, and each override the toolkit prints.
_Mechanical._

## 4. Get the master's timing

> **Skill:** `repurpose` · **Guide:** `production/docs/reference/recorded-pieces.md`

Read In and Out from the master-timed captions (`publishing/src/captions/<piece>.en-GB.srt`) where
they exist, or from the edit decision list (`production/src/edits/<piece>.toml`). For a recorded
piece whose master-timed captions do not exist yet, carry its recording-timed captions to the
master first:

```bash
python3 toolkit/media.py captions retime publishing/src/captions/<piece>.<FID>.en-GB.srt \
  --edl production/src/edits/<piece>.toml --source <FID> -o publishing/src/captions/<piece>.en-GB.srt
```

Every cut is then timed on the master, never on the recording. _Mechanical._

## 5. Find the moments

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

Read the script or transcript for moments that stand alone: a viewer who has never seen the master
understands the cut from its first line. For each candidate, name the lines it carries, its hook
and why it stands alone. The mode file says what a moment is for this brand. _Substantive._

## 6. Frame each cut for its deliverables

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

For each vertical deliverable choose `crop x=<px>`, with the speaker in frame, or `pad`; start
from the storyboard's Vertical framing column (`scripts/src/pieces/<piece>/storyboard.md`), where
the piece has a storyboard. Keep faces, titles and captions inside `safe_zone`, and set the
caption width the cut needs. _Substantive._

## 7. Check lengths, and refuse near-identical cuts

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

Every cut's Out minus its In sits inside the `max_seconds` of each of its deliverables; a cut that
does not is re-chosen, never stretched. No two cuts carry the same moment in a different crop or
caption: drop or merge them, and say why. _Substantive._

## 8. Propose, and let the author decide

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

Put the plan to the author as its table, with a line of reasoning per cut and the recommendation
first. A cut the author approves is `approved`; one deferred stays `planned`; one declined is not
written. Never approve a cut on the author's behalf to keep the work moving. _Substantive._

## 9. Write the plan

> **Skill:** `repurpose` · **Guide:** `publishing/src/cut-downs/CLAUDE.md`

Write `publishing/src/cut-downs/<piece>.md` in its skeleton: frontmatter, the table, and a
`## cNN — <hook>` section per cut, one sentence per line. Date `approved` once the author has
agreed the whole plan. An existing plan is revised, never overwritten without confirming.
_Mechanical._

## 10. Hand back

> **Skill:** `repurpose` · **Guide:** `publishing/docs/reference/cut-downs.md`

Report each cut, its deliverables and its hook; every `verify` key the plan relies on; which cuts
need their own thumbnail; and the next procedures: captions first, where they can be made before
the cut (`publishing/workflows/03-caption-a-piece/`), then
`publishing/workflows/02-cut-for-a-platform/`. _Substantive._
