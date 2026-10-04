# CONTEXT.md — brand/src/exports/large/

Exported design assets over 10 MB: a layered source file, a high-resolution plate, a motion
still sequence. Git LFS stores them, so a clone carries a small pointer per file and fetches the
content only when it is needed. The folder's own `.gitattributes` marks every file in it for
LFS except itself and this pair; it is the only place in the project that uses LFS, and no
root `.gitattributes` exists or is ever written for it.

## Directory Tree

```text
brand/src/exports/large/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── .gitattributes      ← template-owned: every file here through Git LFS, except itself and the pair
└── <design>.<ext>      ← one large exported file, named for its design in kebab-case
```

## What's here

- Large exported files, each with a row in `brand/src/design-register.md` whose Storage is
  `lfs`. **Until the first large export is recorded, this folder holds only its pair and
  `.gitattributes`.**
- `.gitattributes` — template-owned; `copier update` keeps it current. It applies
  `filter=lfs diff=lfs merge=lfs -text` to every file here and exempts `.gitattributes`,
  `CONTEXT.md` and `CLAUDE.md`, which stay ordinary text.
- Git LFS must be installed and set up (`git lfs install`, once per machine) before a file is
  added here. Where it was not when the project was generated, a setting in the repository's own
  `.git/config` makes `git add` of a file here fail loudly rather than commit it whole.

## Cross-references

- `brand/docs/reference/design-exports.md` — LFS, the tripwire, and what the failure means.
- `brand/workflows/03-record-a-design-export/` — the procedure that files a large export.
- `brand/workflows/06-check-the-setup/` — the check that reports git-lfs and its filter.
