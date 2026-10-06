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
| M1 | idea → briefed | Every frontmatter field set (a recorded piece briefed before its recording is logged has `source_media: []`, which counts as set); deliverables are keys of selected platforms, or `audiobook.<store>` keys for an audiobook; purpose, shape, metaphor, call to action, disclosure plan and rights needs written (shape and metaphor may read `n/a`, never blank); no flag in the brief; the author's word. | — |
| M2 | briefed → scripted | **Scripted:** the author approved `script.md` (`approved:` dated); zero flags in it; `script time` within 10% of `target_seconds`, its `{pause S}` holds included (how a trailer of stills and cards meets its length, never by padded words), and inside every deliverable's `max_seconds`; companion reports run where present and every finding decided; every factual claim verified or cut. **Recorded:** the author approved `transcript.md`; every beat anchored on the recording; zero flags in it; fact-check run where present and every finding decided. **Audiobook** (it has no script): the author approved its chapter register (`approved:` dated), with a row for every chapter and the credit rows `ch00` and `ch99`, the credits' words written; every chapter's source `final`, or a text the author provided; zero flags in the register. | — |
| M3 | scripted → storyboarded | Every spoken line sits in a storyboard row; every row has a shot with a source; framing noted for every vertical deliverable; a `needed` rights row for every licensed or identifiable item. | `picture: false`; `origin: recorded` |
| M4 | storyboarded → produced | Every master exists and probes clean (one per aspect for a scene piece); `footage verify` passes for every source it uses; every take it uses was heard, approved and archived (for an audiobook, every mastered chapter, the credits included, approved and archived; its chunk takes need not be); loudness within the house targets; the author has watched or heard it through. A scene piece dates the four `M4.*` sub-checks first, in order below; every other piece records them `n/a` with a reason. | — |
| M5 | produced → cut | Every deliverable of the brief and the cut-down plan is rendered and passes its verification; audiobook: `audiobook check` passes on every file; the author has seen or heard each. A feed episode's `podcast.feed_audio` is encoded here like any audio deliverable, untagged: its tags and chapters are written at M7. A GIF preview is made with the thumbnails, towards M7, never here. | — |
| M6 | cut → captioned | Every deliverable with speech and picture has captions that pass `captions check --script` (against the script, or a recorded piece's transcript), burned where the platform takes no sidecar or the brief asks, sidecar otherwise. Captions burned in the cutting pass let M5 and M6 pass together; both dates are recorded. **On a site of the website or blog profile, whoever owns it:** every self-hosted video with speech has its WebVTT sidecar, never burned, and every piece or cut with speech placed there has its published transcript of exactly what the page plays (`captions transcript`, with `--lines` for a cut), described where the picture carries what the words do not, and approved by the author. **A feed episode** (`podcast.feed_audio`) has its published transcript and its master-timed WebVTT. | audiobook; a podcast with no `podcast.feed_audio` deliverable and no placement on such a site, unless the brief asks for a transcript; deliverables without speech (a silent loop, an image, a GIF) |
| M7 | captioned → scheduled | Every rights row the piece uses is `cleared`; the disclosure is set per deliverable; thumbnails and the piece's other images approved where the platform takes one; the post package approved and inside every limit; zero flags in the piece's files (`flags --piece <piece> --strict`); a schedule row for every deliverable and every placement, a placement being the one file a page or issue plays or shows first, its other images bullets of it, never rows. **A placement** on a site or list the brand does not own has its profile row's dated agreement, and names under Links to the placement it depends on; a written piece it sits in is read, and one not `final` is a warning. **A feed episode:** its show's details approved; its register row `ready`, with its words, chapters and `pub_date`; its file tagged with `feed tag`; and `feed check` exiting 0 against the show's tracked feed. | — |
| — | scheduled → published | Not a gate: every schedule row for the piece is `posted` or `dropped`, and each posted row has its publish-log row. | — |

Commands are `python3 toolkit/media.py` commands. The brief's skeleton is in
`scripts/src/pieces/CLAUDE.md`, loudness in `production/docs/reference/sound-and-loudness.md`,
caption limits in `publishing/docs/reference/captions.md`.

## Scripted, recorded and audio-only pieces

A **scripted** piece is written first, then voiced or filmed. A **recorded** piece already exists as a recording,
its footage IDs in `source_media`: its approved, anchored transcript is M2 and stands in for a script.
A gate that is `n/a` moves the piece past that status. The procedure passing M2 dates M3 `n/a` for no picture,
a recording or an audiobook; `storyboard` refuses such a piece, and its master needs no storyboard.

## Scene progress toward M4

A shot typed `scene` makes a scene piece. Date these in order under `storyboarded`; an inapplicable sub-check is `n/a` with its reason.

- **M4.takes:** every used take heard, approved and archived, and `media.py voice join` has joined them with their pauses.
- **M4.words:** `transcribe` timed every word; words/check accepted through `-o`; the author agreed the voice says the script, a skipped cross-check named.
- **M4.cues:** `cues` matched every board, accepted through `-o`; Time and shot Seconds re-timed; the author agreed the board before animation, in `production/workflows/09-time-the-voice/`.
- **M4.stills:** `lipsync` mouth JSON accepted through `-o`; every board's stills at every master size opened and reported; findings fixed or accepted, then the author watched the preview master and has no timing note left, in production/workflows/10-animate-a-scene/.

Every other piece records all four `n/a` with a reason: alongside M3 for footage, or before M4 where M3 is `n/a`.
The master procedure writes any missing entries before proceeding, including for boards made before these sub-checks existed.

## Recording a gate

`verified:` holds a gate or sub-check's date, `'n/a — reason'`, or `'waived DD/MM/YYYY — reason'` on the author's word.
A brief that passed M1 before Shape and Metaphor existed keeps its date until it is next re-briefed; new/re-briefed fields are never blank.
A material change clears its gate or sub-check and every later one, and `status` steps back to the earliest cleared gate's starting rung.
A corrected typing slip clears nothing. A re-time raises board `version`, keeps `approved:` and M3, but clears `M4.cues`, `M4.stills`, M4 and later gates;
a note replacing a shot or changing words also clears M3. A new/re-rolled take clears all four sub-checks and M4: join, transcribe and lipsync again.
Re-timing alone needs no new mouth file, because mouths depend on the voice. Apply timing notes through `production/workflows/09-time-the-voice/`.

## How we apply it here

Read the status from the brief, never memory or a renders folder. Never set an unearned status: the author's word is part of every gate.
Every checklist's See line cites its gate and move without restating it; a procedure that moves no piece says no gate applies.

## Who implements it

`run-media-workflow` reads `status` and `verified`, and routes on the first undated `M4.*` under `storyboarded`.
The procedures each checklist names write dates: `scripts/workflows/01-brief-a-piece/` (M1), `scripts/workflows/02-write-a-script/` or
`production/workflows/08-bring-in-a-recording/` (M2), `scripts/workflows/03-storyboard-a-piece/` (M3), then the master procedure (M4).
`publishing/workflows/02-cut-for-a-platform/` (M5), `publishing/workflows/03-caption-a-piece/` (M6), and the rights, thumbnail and package procedures (M7)
finish the piece. `publishing/workflows/06-record-a-publication/` records published; podcast and audiobook procedures serve their own masters.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 requires these gates, Section 1 says who decides.
A project guide may add a check, never remove or weaken one. The rules own the requirement; this guide owns the checks and their record.
