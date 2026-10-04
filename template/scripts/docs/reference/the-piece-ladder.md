---
type: guide
skills: [run-media-workflow]
model: opus
---

# The piece ladder — nine statuses, seven gates, and the author's word at each

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A piece's brief says how far it is from published, in its `status:` key, on one
ladder: `idea · briefed · scripted · storyboarded · produced · cut · captioned · scheduled ·
published`. It moves up a rung only when the gate for that move passes, and the gate's date goes
in the brief's `verified:` map. The gates, M1 to M7, are defined here for every piece; the `M`
keeps them apart from syntek-author's gates, which govern its units and never a piece.

## The gates

| Gate | Moves | Passes when | n/a for |
|---|---|---|---|
| M1 | idea → briefed | Every frontmatter field set (a recorded piece briefed before its recording is logged has `source_media: []`, which counts as set); deliverables are keys of selected platforms, or `audiobook.<store>` keys for an audiobook; purpose, call to action, disclosure plan and rights needs written; no flag in the brief; the author's word. | — |
| M2 | briefed → scripted | **Scripted:** the author approved `script.md` (`approved:` dated); zero flags in it; `script time` within 10% of `target_seconds`, its `{pause S}` holds included (how a trailer of stills and cards meets its length, never by padded words), and inside every deliverable's `max_seconds`; companion reports run where present and every finding decided; every factual claim verified or cut. **Recorded:** the author approved `transcript.md`; every beat anchored on the recording; zero flags in it; fact-check run where present and every finding decided. **Audiobook** (it has no script): the author approved its chapter register (`approved:` dated), with a row for every chapter and the credit rows `ch00` and `ch99`, the credits' words written; every chapter's source `final`, or a text the author provided; zero flags in the register. | — |
| M3 | scripted → storyboarded | Every spoken line sits in a storyboard row; every row has a shot with a source; framing noted for every vertical deliverable; a `needed` rights row for every licensed or identifiable item. | `picture: false`; `origin: recorded` |
| M4 | storyboarded → produced | The master exists and probes clean; `footage verify` passes for every source it uses; every take it uses was heard, approved and archived (for an audiobook, every mastered chapter, the credits included, approved and archived; its chunk takes need not be); loudness within the house targets; the author has watched or heard it through. | — |
| M5 | produced → cut | Every deliverable of the brief and the cut-down plan is rendered and passes its verification; audiobook: `audiobook check` passes on every file; the author has seen or heard each. A feed episode's `podcast.feed_audio` is encoded here like any audio deliverable, untagged: its tags and chapters are written at M7. A GIF preview is made with the thumbnails, towards M7, never here. | — |
| M6 | cut → captioned | Every deliverable with speech and picture has captions that pass `captions check --script` (against the script, or a recorded piece's transcript), burned where the platform takes no sidecar or the brief asks, sidecar otherwise. Captions burned in the cutting pass let M5 and M6 pass together; both dates are recorded. **On a site of the website or blog profile, whoever owns it:** every self-hosted video with speech has its WebVTT sidecar, never burned, and every piece or cut with speech placed there has its published transcript of exactly what the page plays (`captions transcript`, with `--lines` for a cut), described where the picture carries what the words do not, and approved by the author. **A feed episode** (`podcast.feed_audio`) has its published transcript and its master-timed WebVTT. | audiobook; a podcast with no `podcast.feed_audio` deliverable and no placement on such a site, unless the brief asks for a transcript; deliverables without speech (a silent loop, an image, a GIF) |
| M7 | captioned → scheduled | Every rights row the piece uses is `cleared`; the disclosure is set per deliverable; thumbnails and the piece's other images approved where the platform takes one; the post package approved and inside every limit; zero flags in the piece's files (`flags --piece <piece> --strict`); a schedule row for every deliverable and every placement, a placement being the one file a page or issue plays or shows first, its other images bullets of it, never rows. **A placement** on a site or list the brand does not own has its profile row's dated agreement, and names under Links to the placement it depends on; a written piece it sits in is read, and one not `final` is a warning. **A feed episode:** its show's details approved; its register row `ready`, with its words, chapters and `pub_date`; its file tagged with `feed tag`; and `feed check` exiting 0 against the show's tracked feed. | — |
| — | scheduled → published | Not a gate: every schedule row for the piece is `posted` or `dropped`, and each posted row has its publish-log row. | — |

Commands are `python3 toolkit/media.py` commands. The brief's skeleton is in
`scripts/src/pieces/CLAUDE.md`, loudness in `production/docs/reference/sound-and-loudness.md`,
caption limits in `publishing/docs/reference/captions.md`.

## Scripted, recorded and audio-only pieces

- A **scripted** piece (`origin: scripted`) is written first, then voiced or filmed. A
  **recorded** piece (`origin: recorded`) is a talk, interview or conversation that already
  exists as a recording, its footage IDs in `source_media`: its approved transcript is its M2,
  its M3 is `n/a — recorded`, and the transcript stands in for the script wherever one is read.
- A gate that is `n/a` moves the piece straight past that status: a piece with `picture: false`
  (no deliverable carries a picture: an episode, a standalone voiceover, an audiobook) goes
  `scripted` → `produced`, and so does a recorded talk. The procedure that passes M2 records the
  M3 `n/a` beside it; `storyboard` refuses such a piece, and its master is assembled without one.

## Recording a gate

`verified:` holds one entry per gate, keyed by its number: a date when it passed,
`'n/a — <reason>'` when it does not apply, or `'waived DD/MM/YYYY — <reason>'` on the author's
explicit word — `{M1: 03/10/2026, M2: 08/10/2026, M3: 'n/a — recorded'}`. A gate that does not
apply is recorded `n/a` with its reason, never skipped in silence. A material change after a gate
passed (a beat rewritten, a claim added, a shot replaced, a deliverable re-cut) clears that gate's
date and every later one, and `status:` steps back to the rung the earliest cleared gate leads
from; a corrected typing slip clears nothing.

## How we apply it here

- Read a piece's status from its brief, never from memory or from what sits in a renders folder.
- Never set a status a gate has not earned. The author's word is part of every gate.
- Every `CHECKLIST.md` cites the gate it passes as `M2 (briefed → scripted)` and never restates
  it; a procedure that moves no piece says that no gate here applies to it.

## Who implements it

- **Workflows:** every procedure, through its checklist's See line:
  `scripts/workflows/01-brief-a-piece/` (M1); `scripts/workflows/02-write-a-script/` or
  `production/workflows/08-bring-in-a-recording/` (M2); `scripts/workflows/03-storyboard-a-piece/`
  (M3); `production/workflows/03-assemble-the-master/` (M4);
  `publishing/workflows/02-cut-for-a-platform/` (M5); `publishing/workflows/03-caption-a-piece/`
  (M6); `production/workflows/07-clear-the-rights/`, `publishing/workflows/04-brief-a-thumbnail/`
  and `publishing/workflows/05-prepare-a-post/` (M7, with the podcast-feed procedure for a feed
  episode); `publishing/workflows/06-record-a-publication/` (published). The podcast-episode and
  audiobook procedures, where the project has them, take an episode to M4 and a book M2 to M5.
- **Skills:** `run-media-workflow` reads `status` and `verified` to resolve 'next' and checks
  each gate before a step moves a piece; the skill each procedure names writes the date.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 owns the requirement: these gates
bind every piece, and a project guide of this name may add a check to a gate but never remove or
weaken one. Section 1 owns who decides what. The rules own the requirement; this guide owns what
each gate checks and how the record is kept.
