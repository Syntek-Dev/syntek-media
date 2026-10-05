---
workflow: 03-caption-a-piece
phase: publish
skills: [captions]
model: opus
---

# STEPS.md — caption a piece's deliverables

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for captioning every deliverable of a piece that has speech and picture.
Each step names the skill and guide it uses, and the toolkit command it runs. **Run in order** —
the ordering is load-bearing — and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`), then
> `publishing/docs/reference/captions.md`. The `captions` skill runs every caption command; read
> it before step 1.

## 1. List what needs captions

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

From the brief and the cut-down plan, list every deliverable with its key. Each one with speech
and picture needs captions. A feed episode (`podcast.feed_audio`) needs its master-timed `.vtt`
and its published transcript. Every piece or cut with speech placed on a site of the website or
blog profile, whoever owns it, needs its published transcript, and every self-hosted video there
its `.vtt` sidecar, never burned: read the package or the brief for where each goes. What M6's
`n/a` list in the ladder guide names (an audiobook, a podcast with neither, a deliverable without
speech, such as a silent loop, an image or a GIF) is `n/a`: note the reason now. Note which
deliverables are burned (their table's `caption_formats` is empty, or the brief asks) and which
take a sidecar. _Substantive._

## 2. Choose the timing route

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

Generated voiceover takes route four where accepted aligned words exist, otherwise route one
from its segment register. Speech on camera, and a recorded
piece, take route two, alignment over the speech the toolkit finds. Route three, by hand, is for
what neither fits. The words always come from `script.md`, or from a recorded piece's approved
`transcript.md`; **a piece with neither goes back to
`production/workflows/08-bring-in-a-recording/`**, and no speech-to-text is run here.
_Substantive._

## 3. Make the master's captions

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

Write the result to `publishing/src/captions/<piece>.en-GB.srt` with `-o`: without it
`captions align`, `retime`, `rewrap` and `vtt` write to the terminal. Route one, from the segment
register; route two, a scripted piece, aligned on the master's own audio (`extract-audio` writes
`<stem>.wav` into the piece's `production/src/renders/<piece>/` and prints the path):

```bash
python3 toolkit/media.py captions from-segments production/src/voiceover/<piece>.toml --deliverable KEY -o <srt>
python3 toolkit/media.py extract-audio <master>
python3 toolkit/media.py captions align scripts/src/pieces/<piece>/script.md <audio> -o <srt>
```

Route four: run `voice join <piece>` then `transcribe <piece>` and read its printed check.
If models are absent, give the author `python3 toolkit/media.py transcribe fetch`; never run it.
Resolve its findings, then on acceptance run `transcribe <piece> -o
production/src/timing/<piece>.words.json`, with the words check beside it. Existing tracked
copies must be committed and unchanged. Use `captions from-words
production/src/timing/<piece>.words.json --deliverable KEY --offset TC -o <srt>`, the offset
from the edit's voice row. Word boundaries stay intact; short gaps are findings for review.
Route two, a recorded piece: retime its recording-timed file to the master with
`captions retime … --edl` (`production/docs/reference/recorded-pieces.md`), unless that has
already been done. _Mechanical._

## 4. Make each cut's captions

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

For each cut in the plan, carry the master's timing to it, written with `-o` to
`publishing/src/captions/<piece>--cNN.en-GB.srt`; where the cut shows drift, align it on its own
audio and lines instead:

```bash
python3 toolkit/media.py captions retime publishing/src/captions/<piece>.en-GB.srt --in <In> --out <Out> -o <cut srt>
python3 toolkit/media.py extract-audio <master> --in <In> --out <Out>
python3 toolkit/media.py captions align <script or transcript> <audio> --lines <beat.line-beat.line> -o <cut srt>
```

_Mechanical._

## 5. Rewrap where a deliverable needs its own width

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

A vertical deliverable takes a narrower line than a landscape one. Where one file serves
deliverables of different widths, run
`python3 toolkit/media.py captions rewrap <srt> --deliverable KEY -o <rewrapped srt>`, the result
named with the `.<platform>-<format>` qualifier before `.en-GB`. _Mechanical._

## 6. Check every file against its source

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

Run `captions check <srt> --deliverable KEY --script <script or transcript>` with
`python3 toolkit/media.py` on every file. Each finding is decided, not waved through: a timing
fault is re-made; a word that differs follows the script, or, for a recorded piece, the transcript
is corrected first, with the author, and the caption made again. Break lines at clauses, never
inside a name. _Substantive._

## 7. Burn in, or attach

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

A burned deliverable is burned with
`python3 toolkit/media.py captions burn <render> <srt> --deliverable KEY`, or re-cut with its
captions through `publishing/workflows/02-cut-for-a-platform/`. A sidecar deliverable keeps its
SRT, with `python3 toolkit/media.py captions vtt <srt> -o <vtt>` where its platform takes WebVTT:
every self-hosted video on a profile site, and a feed episode, whose `.vtt` is the master's. A
burn that fails on the caption font is fixed at the font, never accepted. _Mechanical._

## 8. Make the published transcripts

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

For the whole piece, and for each distinct cut placed on a profile site, write the transcript of
exactly what that page plays from the script or the recorded transcript, with `-o`:

```bash
python3 toolkit/media.py captions transcript <script or transcript> -o publishing/src/captions/<piece>.transcript.en-GB.md
python3 toolkit/media.py captions transcript <script or transcript> --lines <beat.line-beat.line> -o publishing/src/captions/<piece>--cNN.transcript.en-GB.md
```

Then, with the author, describe in words what the picture carries and the words do not (on-screen
text is kept by the command), and fix only a mis-transcription. The author approves each one.
_Substantive._

## 9. Watch a burned preview

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

With the author, watch every burned deliverable, and one burned preview of each sidecar file:
in time with the speech, inside the safe zone, readable at the size it will be seen. Alignment is
a heuristic; this is where its misses are caught. _Substantive._

## 10. Record the gate

> **Skill:** `captions` · **Guide:** `scripts/docs/reference/the-piece-ladder.md`

When every deliverable that needs captions has a checked file, burned where it must be, every
published transcript step 1 listed is approved, and the author has seen them, set the brief's
`status` to `captioned` and date M6 in `verified`; where nothing needed captions, record M6 as
`n/a` with the reason from step 1. _Mechanical._

## 11. Hand back

> **Skill:** `captions` · **Guide:** `publishing/docs/reference/captions.md`

Report each caption file and what it is timed to, which deliverables are burned and which carry a
sidecar, each published transcript and the page it serves, every finding and how it was decided,
and any `verify` key relied on. Point at
`publishing/workflows/04-brief-a-thumbnail/` and `publishing/workflows/05-prepare-a-post/`.
_Substantive._
