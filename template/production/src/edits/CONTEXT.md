# CONTEXT.md — production/src/edits/

One edit decision list per piece, from which `python3 toolkit/media.py assemble` builds the
master. The list is the record of every cut; the master in `production/src/renders/` is generated
from it and from the logged footage, the cards and the approved voiceover, so a change is made
here and assembled again, never by editing a render.

## Directory Tree

```text
production/src/edits/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules and the list skeleton
└── <piece>.toml        ← one piece's edit decision list, named for its piece folder
```

## What's here

- **The shape is fixed by `production/docs/reference/edit-decision-lists.md`**: an `[edit]`
  table (piece, version, the master's frame or `""` for an audio master, sample rate, loudness
  target), then one `[[clip]]` table per clip in timeline order, `[[overlay]]` tables for cards
  over the picture, and `[[audio]]` tables for the voice, music beds and effects.
- A clip's `source` is a footage ID, an asset under `production/src/assets/` or a card under
  `production/src/cards/`; a sound's `source` may also be `vo:<piece>`, the piece's approved
  voiceover segments joined in order.
- A generated project may hold the worked example's list, where it was kept. It names footage no
  project has, so `assemble` on it exits 2 by design; delete it with the rest of the worked
  example once you no longer need it, and it will not come back.

## Cross-references

- `production/workflows/03-assemble-the-master/` — the procedure that writes and assembles a list.
- `production/docs/reference/sound-and-loudness.md` — where each sound sits, and how loud.
- `production/src/footage/manifest.toml` — the footage IDs a list cites.
- `scripts/src/pieces/` — the storyboard, shot list or transcript a list is written from.
