# CONTEXT.md — brand/workflows/02-sync-with-claude-design/

The procedure for bringing a component across between the brand kit in
`brand/src/design-system/` and the brand's design-system project in Claude Design, in either
direction. The author starts it, with `/design-sync` and a hint naming the kit as a
hand-authored HTML kit, or, where that converter will not take the kit, with `/design import`
and `/design export` through a scratch folder. Either way the sync is incremental: one component
at a time, each seen and approved, never a wholesale replace. It changes no piece already made.

## Directory Tree

```text
brand/workflows/02-sync-with-claude-design/
├── CHECKLIST.md        ← model-tagged checklist; tick it as you go
├── CLAUDE.md           ← operating rules for this procedure
├── CONTEXT.md          ← this file: when to use it, what it produces
└── STEPS.md            ← the ordered steps, each naming its skill and guide
```

## When to use this

- The author has changed a token or a layout in Claude Design and wants it in the repository.
- The author has changed the kit here and wants Claude Design to show it.
- The kit is to be connected to its Claude Design project for the first time.

Reach for a **different** procedure when the values themselves are still to be decided
(`brand/workflows/01-set-up-the-brand-kit/`), or when a design's exported file is to be filed
(`brand/workflows/03-record-a-design-export/`).

## What it produces, and where

- **Changed files in `brand/src/design-system/`**, one component per round, each approved and
  checked, committed with a message naming the components.
- **The project's row** in `brand/src/design-register.md`, the first time, holding its link.
- **A dated record** in `.claude/MEMORY.md` of what was synced, by which route, and what the
  first `/design-sync` actually did with the kit.

## The failure this procedure exists to prevent

A wholesale sync that replaces the kit with what a converter guessed. The toolkit reads the
tokens by name and the cards by their first line, so one renamed token or one moved comment
breaks every render; and a layout changed in the design project and synced unseen reaches every
later piece. One component at a time, each shown to the author and checked before the next,
keeps the kit readable and every change attributable.

## Cross-references

- `brand/docs/reference/claude-design.md` — the two routes, and what a sync must never do.
- `brand/src/design-system/` — the kit, and the layout contract in its previews pair.
- `brand/src/design-register.md` — where the project's link is kept.
