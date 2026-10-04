# CONTEXT.md — scripts/docs/reference/

The template's guides for planning, writing and boarding a piece, one per question. Each explains
how one part of the work is done in this project, names the skill and workflow that carry it out,
and points at the media rules file that owns the requirement. These files are template-owned:
`copier update` keeps them current, and a same-named guide in `scripts/docs/project/` overrides
any of them, except that the ladder guide's gates can only be added to.

## Directory Tree

```text
scripts/docs/reference/
├── CONTEXT.md                     ← this file
├── CLAUDE.md                      ← operating rules
├── the-piece-ladder.md            ← nine statuses, and the gates M1–M7 between them
├── writing-for-the-ear.md         ← a script heard once: tags, directions, timing, transcripts
<: if 'short-video' in MEDIA_KINDS :>├── short-video.md                 ← a vertical short: the hook, one idea, sound off
<: endif :><: if 'long-video' in MEDIA_KINDS :>├── long-video.md                  ← an explainer or a talk that holds attention to the end
<: endif :><: if 'podcast' in MEDIA_KINDS :>├── podcast-episodes.md            ← an episode: its shape, its voices and its disclosure
<: endif :><: if 'trailer' in MEDIA_KINDS :>├── trailers.md                    ← a trailer built from stills, cards, voice and music
<: endif :><: if 'voiceover' in MEDIA_KINDS :>├── standalone-voiceovers.md       ← a piece that is a voiceover and nothing else
<: endif :>└── storyboards-and-shot-lists.md  ← a picture for every spoken line, a source for every shot
```

## What's here

- `the-piece-ladder.md` — **read before moving any piece.** The nine statuses, the gates M1 to
  M7 for scripted, recorded and audio-only pieces, `n/a` and waivers, and what published means.
- `writing-for-the-ear.md` — **read before writing or approving a script.** The script file,
  speaker tags, cues and braced directions, timing with `media.py script time`, and a recorded
  piece's transcript.
- `storyboards-and-shot-lists.md` — the storyboard's rows and the shot list's sources, vertical
  framing, and the rights row every licensed or identifiable item opens.
<: if 'short-video' in MEDIA_KINDS :>- `short-video.md` — the hook in the first seconds, one idea per short, vertical framing,
  and when a short is its own piece rather than a cut-down.
<: endif :><: if 'long-video' in MEDIA_KINDS :>- `long-video.md` — the shape of an explainer or a talk, keeping the picture moving, and
  lines that will stand alone as cut-downs.
<: endif :><: if 'podcast' in MEDIA_KINDS :>- `podcast-episodes.md` — an episode's shape, host and guest lines, disclosure in the audio,
  and the audio master.
<: endif :><: if 'trailer' in MEDIA_KINDS :>- `trailers.md` — what a trailer promises, building it from stills, cards, fades and
  push-ins, and the rights a trailer needs.
<: endif :><: if 'voiceover' in MEDIA_KINDS :>- `standalone-voiceovers.md` — when a voiceover is the whole piece, writing the read, the
  cost before the take, and delivering it.
<: endif :>
## Cross-references

- `scripts/docs/project/` — your overrides and additions; checked before this folder.
- `scripts/workflows/CLAUDE.md` — the procedures these guides are applied in.
- `.claude/rules/syntek-media/03-production-ethics.md` — the rules every guide here defers to.
