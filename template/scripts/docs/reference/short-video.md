---
type: guide
skills: [write-script, repurpose]
model: opus
---

# Short video — a vertical short: the hook, one idea, and the sound off

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** A short is a vertical video watched on a phone, often with the sound off, by
someone who will scroll past in the first seconds unless something stops them. It carries one
idea, states it early, and ends before the viewer's attention does. A short is either a piece of
its own, scripted for the format, or a cut-down of a longer piece; the two are planned in
different places and must not be confused.

## Its own piece, or a cut-down

- **Its own piece** (`kind: short-video`): briefed, scripted and boarded like any other, with
  short deliverables such as `youtube.short`, `tiktok.video` or `instagram.reel` in its brief.
  A short re-scripted from a longer piece is its own piece too, with `parent` naming that piece.
- **A cut-down**: a stretch of an existing master, lifted without a new script. It is not a
  piece and has no brief; it lives in its parent's cut-down plan in `publishing/src/cut-downs/`,
  planned with the `repurpose` skill.

## The hook

The first line is the reason to stay: a question, a surprise, a promise, a picture that needs
explaining. No greeting, no logo sting and no name before it. The brief's `## Hook` holds it in
one sentence, and the script's first beat delivers it in the first line spoken and the first
`TEXT:` cue shown, so it lands with the sound off as well as on.

## Sound off, and one idea

- Every spoken line is captioned, and the words that matter most also appear as `TEXT:` cues.
- One idea per short: a second point is a second short, not a faster first one.
- The call to action is one line, said and shown, and it asks for one thing.
- The length is set by the brief's `target_seconds`, inside every deliverable's `max_seconds` in
  `toolkit/data/platforms.toml`; never by a number remembered from a platform's help page.

## Vertical first

Board the short for 9:16 from the start: faces and text inside each deliverable's safe zone, no
detail that only reads on a large screen, and `TEXT:` cues short enough for the narrow caption
width. A short cut from a landscape master is reframed in its cut-down plan (`centre`, a crop,
or `pad`), and a short made for its own sake is better shot vertical than cropped.

## How we apply it here

- Write the hook last if it will not come first; test it by reading only the first line aloud.
- Time the script with `python3 toolkit/media.py script time` before anyone hears it.
- A batch of near-identical shorts is never planned: each cut-down has its own hook and its own
  reason to stand alone.
- AI disclosure follows the brief's plan for every short, own piece or cut-down alike.

## Who implements it

- **Workflows:** `scripts/workflows/02-write-a-script/` writes and times a short's script;
  `publishing/workflows/01-plan-the-cut-downs/` plans shorts cut from a longer master.
- **Skills:** `write-script` writes the script; `repurpose` plans the cut-downs.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 3 makes M2 (briefed → scripted)
binding, including a script that fits every deliverable's limit, and Section 5 owns AI
disclosure. The rules own the requirements; this guide owns how a short is written to be watched.
