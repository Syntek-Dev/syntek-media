# CONTEXT.md — publishing/src/captions/

Every caption file the project makes: SRT, the master format, and WebVTT generated from it, each
timed to exactly one thing (the master, one cut, or one recording) and named so that the name
says which; and the published transcripts a page or a podcast episode carries beside its player. The words in every file are the script's, or a recorded piece's approved transcript's;
only the timing is made here. Burned versions of a deliverable are renders, in
`publishing/src/renders/`, never here.

## Directory Tree

```text
publishing/src/captions/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules and the naming patterns
├── <piece>….en-GB.srt ← one caption file per timing, with a .vtt beside it where a platform needs one
└── <piece>[--cNN].transcript.en-GB.md ← a published transcript of the whole piece or one cut
```

## What's here

| File | Timed to | Made by |
|---|---|---|
| `<piece>.en-GB.srt` | the master | `captions from-segments`, `captions align` or `captions retime --edl` |
| `<piece>--cNN.en-GB.srt` | one cut | `captions retime --in --out` from the master's, or `captions align --lines` |
| `<piece>.<FID>.en-GB.srt` | a recording (`F0001`) | `captions align --anchors`, from the approved transcript |
| `….<platform>-<format>.en-GB.srt` | as above, rewrapped | `captions rewrap`, for a deliverable that needs its own line width |
| `….en-GB.vtt` | as its `.srt` | `captions vtt`; the sidecar on a profile site, and a feed episode's `podcast:transcript` (master-timed) |
| `<piece>[--cNN].transcript.en-GB.md` | not timed: exactly what one page plays | `captions transcript` (`--lines` for a cut), then described by hand with the author |

- **The shape and the limits are fixed by `publishing/docs/reference/captions.md`.** Every file
  passes `python3 toolkit/media.py captions check` against its script or transcript before M6.
- A generated project may hold one worked example caption file, where it was kept; delete it, with
  the other example files, once you no longer need it, and none of them will come back.

## Cross-references

- `publishing/docs/reference/captions.md` — house limits, the three timing routes, burned or
  sidecar.
- `publishing/workflows/03-caption-a-piece/` — the procedure that writes these files.
- `production/workflows/08-bring-in-a-recording/` — where a recording's own captions are made.
- `production/src/voiceover/` — the segment registers the first timing route reads.
