# CONTEXT.md — scripts/src/pieces/000-example-piece/

A worked example, shipped once when the project was generated, so the shape of a piece is
visible before any real piece exists. It is a 30-second vertical short, <: if BRAND_KIND == 'business' :>a business explainer<: elif BRAND_KIND == 'author-fiction' :>a novel's teaser<: else :>a talk clip<: endif :>,
spoken on camera so that it needs no generated audio, and carried from brief to post package as
plans only. Its edit decision list names footage no project has, so it stops at `storyboarded`,
as its brief says. It is not part of the channel. Delete this folder and the example's seven
files in the production and publishing layers when they have served their purpose (the steps are
in this folder's CLAUDE.md); `copier update` will not bring them back.

## Directory Tree

```text
scripts/src/pieces/000-example-piece/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← how to practise on the example, and how to remove it
├── brief.md          ← status storyboarded, M1 to M3 dated; why the walk-through stops there
├── script.md         ← four beats spoken on camera, one sentence per line; approved
├── storyboard.md     ← one board per beat on the 30-second timeline; approved
└── shot-list.md      ← four camera shots still to shoot, and the title card
```

## What's here

- `brief.md` — **where this piece stands:** `status: storyboarded`, with M1 to M3 dated in
  `verified`, and in its Notes the reason it goes no further. Its rights row and its footage are
  named RR0000 and F0000, IDs no project has.
- `script.md` — the approved words: four beats of `ON:` lines and one `TEXT:` cue, inside 10% of
  the brief's 30 seconds at the brief's own pace.
- `storyboard.md` and `shot-list.md` — a board per beat, framed `centre` because the master is
  shot vertical, and a source for every shot: four camera shots `to shoot`, and the title card.
- Elsewhere under this piece's name, all of them plans for a master that is never made:
  `production/src/edits/000-example-piece.toml` (the edit decision list, cut from F0000);
  `production/src/cards/000-example-piece.title.html` (the title card, a copy of the brand's card
  component); `publishing/src/cut-downs/000-example-piece.md` (a story cut where the project uses
  Instagram or Facebook, and why the other platforms get none);
  `publishing/src/captions/000-example-piece.en-GB.srt` (the master's captions, the script's words
  exactly); `publishing/src/thumbnails/000-example-piece.md` and
  `publishing/src/thumbnails/000-example-piece.html` (the thumbnail brief and its layout); and
  `publishing/src/posts/000-example-piece.md` (the post package, one section per deliverable).

## The one thing this example shows

Every file a piece makes is named for it, and every number agrees from one file to the next. The
script's beats, the storyboard's times, the edit decision list's clips, the captions' cues and the
cut-down plan's In and Out all sit on one 30-second timeline: beat 1 from 00:00 to 00:05, beat 2
to 00:15, beat 3 to 00:24 and beat 4 to 00:30. Change one beat and every later file has to follow,
which is why a material change clears the gates after it.

## Cross-references

- `scripts/docs/reference/the-piece-ladder.md` — the gates the example passes, and the one it
  stops before.
<: if 'short-video' in MEDIA_KINDS :>- `scripts/docs/reference/short-video.md` — a short made as a piece of its own.
<: endif :>- `scripts/docs/reference/writing-for-the-ear.md` — the script's format and its timing.
- `scripts/docs/reference/storyboards-and-shot-lists.md` — the boards and the shots.
- `production/docs/reference/edit-decision-lists.md` — the clips, the overlay and the fields.
- `publishing/docs/reference/cut-downs.md` — why a 30-second piece gets so few cuts.
- `publishing/docs/reference/captions.md` — the limits the example's captions keep.
- `publishing/docs/reference/ai-disclosure.md` — why its post package discloses nothing.
