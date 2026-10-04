---
type: guide
skills: [cut-for-platform]
model: opus
---

# Source media — logged once, kept outside Git, proved by checksum

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** Every recorded or licensed file a piece is cut from (camera footage, a recorded
talk, a music bed, stock, an image, an archived take) is logged once in
`production/src/footage/manifest.toml`, with its checksum and where its master copy lives. The
files themselves stay outside Git. The manifest is what makes an edit reproducible: an edit
decision list names a footage ID, and the checksum proves the file behind it is the one the edit
was made with.

## Why footage lives outside Git

Footage is large and rarely diffed. Committed, it would bloat every clone for good; in Git LFS it
would exhaust storage and bandwidth quotas within a few projects. So the master copy of every
source file lives in external storage the author chooses (a drive, a NAS, a cloud folder), named
in the manifest by a **location label**, never by a link that carries a secret. Git LFS is used
only for large design exports in `brand/src/exports/large/`.

## The manifest

| Field | Holds |
|---|---|
| `id` | `F0001` onwards: permanent, never reused, cited by edit decision lists and shot lists |
| `path` | the file in the mirror, relative to `production/src/footage/` |
| `kind` | `video · audio · music · stock · image · generated` |
| `sha256`, `bytes`, `duration` | what `footage add` measured; `duration` in decimal seconds, `0.0` for an image |
| `location` | the label of the master copy's home |
| `recorded` | DD/MM/YYYY |
| `rights` | the rights-register ID when the file is licensed or shows people |
| `notes` | for a generated file, the take or chapter it archives |

`python3 toolkit/media.py footage add FILE --kind KIND --location LABEL` copies the file into the
mirror when it lies outside it (it never moves the original), measures it and appends the next
ID; `--rights RRNNNN` links its rights row. It refuses a file whose hash is already listed.

## The local mirror

`production/src/footage/raw/` is the git-ignored copy of the files this machine needs.
`python3 toolkit/media.py footage verify` checks it against the manifest: a changed byte or an
unlisted file fails, and an entry not mirrored here is listed so it can be fetched from its
location. The toolkit opens a mirrored file only by the path the manifest names, and prints
names and hashes, never contents.

## Music beds, stock and archived takes

- A music bed or a stock clip is source media like any other: a manifest row (`kind = "music"`
  or `"stock"`) and a rights row before an edit names it, in an `[[audio]]` or `[[clip]]` table.
- An approved ElevenLabs take, or a mastered audiobook chapter, cannot be made again:
  regenerating spends credits and gives a different take. The skill that made it offers to
  archive it with `footage add --kind generated`, and its `notes` name the take or chapter.

## How we apply it here

- Log a file before an edit names it; an edit decision list cites footage by ID, never by path.
- A file that shows people, private places or someone else's work carries its rights ID.
- Never edit, trim or re-encode a mirrored file; a derived file is a render, made by the toolkit.
- One file, one row: a re-recorded take is a new file with a new ID.
- Back up each location as the author would any master; the repository holds only its record.

## Who implements it

- **Workflows:** `production/workflows/01-log-source-media/`, and
  `production/workflows/08-bring-in-a-recording/` for a recording that becomes a piece.
- **Skill:** `cut-for-platform` reads the manifest and refuses a source that does not verify.

## Governing standard

`.claude/rules/syntek-media/06-global-rules.md` Section 4 owns never overwriting source media,
and `.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 3 owns what the toolkit may read
and write. This guide owns how a source file is logged, kept and proved.
