# CONTEXT.md — brand/docs/reference/

The template's brand guides, one per question. Each explains how one part of the brand is kept
in this project, names the skill and workflow that carry it out, and points at the rules file
that owns the requirement. These files are template-owned: `copier update` keeps them current,
and a same-named guide in `brand/docs/project/` overrides any of them.

## Directory Tree

```text
brand/docs/reference/
├── CONTEXT.md                ← this file
├── CLAUDE.md                 ← operating rules
├── the-brand-kit.md          ← one set of tokens behind every layout
├── claude-design.md          ← keeping the brand and its design project in step
├── design-exports.md         ← small files in Git, large files in Git LFS, every one registered
├── the-spoken-voice.md       ← how the brand sounds aloud, and who says it
└── platform-profiles.md      ← the brand's own choices for each platform, and its corrections
```

## What's here

- `the-brand-kit.md` — **read before changing a token, a font or a layout.** The required
  tokens, fonts and their licences, the preview cards and the two layout components, and how the
  kit agrees with syntek-author's brand guide, where present.
- `claude-design.md` — the brand's design-system project in Claude Design, the two sync routes,
  and why a sync moves one component at a time.
- `design-exports.md` — where an exported asset goes by size, Git LFS and its tripwire, and the
  design register's columns.
- `the-spoken-voice.md` — the spoken voice against the written one, a narrator for each use,
  pronunciations, and consent before a voice is cloned.
- `platform-profiles.md` — what a profile holds, where the platform's own facts live instead,
  overrides, and what a social media plan takes over where one is present.

## Cross-references

- `brand/docs/project/` — your overrides and additions; checked before this folder.
- `brand/workflows/CLAUDE.md` — the procedures these guides are applied in.
- `.claude/rules/syntek-media/03-production-ethics.md` — who decides, credits, consent and the
  flags every guide here defers to.
