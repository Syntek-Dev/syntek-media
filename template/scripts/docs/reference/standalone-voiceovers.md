---
type: guide
skills: [write-script, voiceover]
model: opus
---

# Standalone voiceovers — a piece that is a voiceover and nothing else

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Most voiceovers are one part of a piece with pictures, made through its segment
register while the piece is produced. A standalone voiceover is different: the read is the whole
deliverable — an audio introduction, a narrated announcement, a short spoken piece posted as a
still under audio. It is a piece of its own, `kind: voiceover`, usually with `picture: false`,
so its M3 is `n/a — no picture`.

## When a voiceover is the whole piece

| The work is… | It is… |
|---|---|
| The narration of a piece with pictures | That piece's voiceover, not a piece of its own. |
| A read that is published or delivered on its own | A standalone voiceover: brief it as a piece. |
| A read later laid under a still for a video platform | A standalone voiceover whose deliverable is a video key, made with `python3 toolkit/media.py still-video`; captions then apply. |

Its deliverables are keys of `toolkit/data/platforms.toml` for the platforms it reaches, like any
piece's.

## Writing the read

The script is written for one voice, every spoken line under `VO:` or `NARRATOR:`, in beats that
become the voiceover's segments: one segment per spoken sentence or beat, never one per caption
line. Directions in braces say how a line is read; a direction becomes an audio tag only where
the recorded model supports tags. Any word the voice may say wrongly — a name, a place, a term
of art — goes into the pronunciations of `brand/src/voice/voice.md` before the first take, never
into the script as IPA.

## The cost before the take

Every take spends credits and cannot be repeated exactly, so the read is approved as a script
before anything is generated. The voiceover skill states the characters, the number of calls and
the estimated credits, and waits for a yes; the setup, the calls and the cost discipline are in
`production/docs/reference/elevenlabs.md`, not here. When the author records the read, the
recording is source media and the piece is still scripted.

## Delivering it

The approved takes are joined into a master, levelled to the deliverable's loudness target and
encoded to its format. An approved take is archived as source media as soon as it is approved,
because a lost take can only be replaced by a new one, at a new cost.

## How we apply it here

- Keep a standalone read short enough to approve in one listening; split a long one into pieces.
- A synthetic voice, the brand owner's own cloned voice included, is disclosed wherever the
  piece is published.
- No voice is cloned for a read without the person's recorded consent.

## Who implements it

- **Workflows:** `scripts/workflows/02-write-a-script/` writes and approves the read;
  `production/workflows/02-make-a-voiceover/` voices it, take by take.
- **Skills:** `write-script` writes the read; `voiceover` makes and logs every take.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 4 owns credits, Section 5 owns AI
disclosure and Section 6 owns consent before a voice. The rules own the requirements; this guide
owns what a standalone voiceover is and how its read is written.
