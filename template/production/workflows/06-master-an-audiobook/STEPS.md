---
workflow: 06-master-an-audiobook
phase: produce
skills: [narrate-audiobook]
model: opus
---

# STEPS.md — master an audiobook

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for mastering, checking and packaging an audiobook's chapters. Each step
names the skill and guide it uses. **Run in order** (no chapter is packaged before it passes its
check and the author has heard it) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). The
> `narrate-audiobook` skill runs every step.

## 1. Confirm the chapters are ready

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Read the register and the brief. M2 is dated (the register approved) and M3 is recorded as
`n/a — no picture`; if M3 is not, record it now. Every chapter to master, the credits `ch00` and
`ch99` included, is on the `human` or `ai` route, and every part of it is approved (AI) or its
recording logged (human). A chapter not ready goes back to
`production/workflows/05-narrate-an-audiobook/`. _Substantive._

## 2. Master each chapter

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

For each chapter and each credit, run `python3 toolkit/media.py audiobook master` on its approved
takes in part order (or its recording), with `--piece` and `--chapter`, and `--head` and `--tail`
where the author wants room tone other than the default. It joins them, putting between two parts
exactly the pause the chapter's `<piece>.chNN.chunks.toml` records (a scene break's silence),
adds room tone, masters to the ACX profile and encodes to
`production/src/audiobook/renders/<piece>.chNN.mp3`. Record the Master and Duration and set the
row to `mastered`. _Mechanical._

## 3. Check each file

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Run `python3 toolkit/media.py audiobook check` on every mastered file. Report each failure with
its measurement; fix it at the source (master again, or regenerate or re-record a part on the
author's word), never by loosening the check. Set each passing row's Check and Status to
`checked`. _Mechanical._

## 4. Listen through and approve

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

The author hears every chapter whole: names, numbers and dropped or doubled lines are what the
check cannot hear. A fault goes back to step 2 or to the procedure that voiced the part. The
mastered chapter is what the author approves; its chunk takes need no approval of their own.
_Substantive._

## 5. Archive the masters and record M4

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/source-media.md`

Archive each approved master with
`python3 toolkit/media.py footage add FILE --kind generated --location LABEL` for an AI chapter,
or `--kind audio` for a human one, note the chapter in the manifest row's `notes`, and record the
footage ID in the register. Its chunk takes are archived too only where the author wants them
kept. When every master is approved and archived, record M4 in the brief's `verified` with
today's date and set `status` to `produced`. _Mechanical._

## 6. Package per channel

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

For each channel on the `human` or `ai` route: the opening and closing credits as files of their
own (`ch00`, `ch99`), the chapters in order, and the channel's own targets from the
`[audiobook.<store>]` table its `channels` name gives, flagging any key it lists in `verify`.
Where the channel takes a retail sample, cut it from a mastered chapter with
`python3 toolkit/media.py cut <piece>.chNN.mp3 --deliverable audiobook.acx --in TC --out TC`, a
range no longer than the table's `sample_max_seconds`; `cut` trims and encodes an audio
deliverable and verifies it. On a synthetic narration channel, note the disclosure it
asks for (Spotify's digital voice narration box, for one) for the post package. Set each
packaged row to `packaged`. _Substantive._

## 7. Record M5

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

When every file passes `audiobook check` and the author has heard each, record M5 in `verified`
with today's date, record `M6: 'n/a — audiobook'` (an audiobook carries no captions), and set
`status` to `cut`. _Mechanical._

## 8. Hand back

> **Skill:** `narrate-audiobook` · **Guide:** `production/docs/reference/audiobook-narration.md`

Report each chapter's duration and check, the masters archived, each channel's package and its
disclosure, and anything still flagged `VERIFY`. Point to
`publishing/workflows/05-prepare-a-post/`. _Substantive._
