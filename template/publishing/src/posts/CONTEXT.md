# CONTEXT.md — publishing/src/posts/

One post package per piece: for every deliverable the piece goes out as, everything the author
pastes, sets and uploads when posting it, from the title and the description to the AI label and
the caption file. A package is written before the post and approved by the author; nothing here is
posted from the repository. The schedule says when each deliverable goes out; the publish log
records what happened. Text-only posts, bios and the content calendar are not here: where
syntek-author's social-media documents are present, they own them.

## Directory Tree

```text
publishing/src/posts/
├── CONTEXT.md        ← this file
├── CLAUDE.md         ← operating rules, and the package's skeleton
└── <piece>.md        ← one post package per piece, one section per deliverable
```

## What's here

- `<piece>.md` — a package, written by `prepare-post` with the author. **The shape is fixed by
  `publishing/docs/reference/posting-and-the-log.md`**: frontmatter `piece` and `approved`; one
  `## <platform>.<format>` section per deliverable (with ` — cNN` for a cut), each with the
  bullets **Title**, **Description**, **Hashtags**, **Disclosure**, **Captions**, **Thumbnail**,
  **Render**, **Calendar**, **Scheduled** and **Limits**. The skeleton is fenced in this folder's
  `CLAUDE.md`.
- A generated project may hold one worked example package, where it was kept; delete it, with the
  other example files, once you no longer need it, and none of them will come back.

## Cross-references

- `publishing/docs/reference/posting-and-the-log.md` — the package, the schedule and the log.
- `publishing/docs/reference/ai-disclosure.md` — what goes in each **Disclosure** bullet.
- `publishing/workflows/05-prepare-a-post/` — the procedure that writes a package.
- `publishing/src/schedule.md` — the row each section becomes.
