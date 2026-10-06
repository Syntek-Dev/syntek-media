---
type: guide
skills: []
model: opus
---

# Design exports — small files in Git, large files in Git LFS, every one registered

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** An export is a file made from a design and kept in the repository so a piece can
use it: a logo, a cover, a background plate, a lower-third, a print file. Small exports are
committed as ordinary files in `brand/src/exports/`; large ones go in `brand/src/exports/large/`,
which Git LFS stores. Every export has one row in `brand/src/design-register.md`. An export is
not a render, which is regenerable and git-ignored, and not footage, which is listed in
`production/src/footage/manifest.toml` and kept in external storage.

## Small or large

| Size | Folder | Storage column |
|---|---|---|
| 10 MB or less | `brand/src/exports/` | `git` |
| over 10 MB | `brand/src/exports/large/` | `lfs` |

`python3 toolkit/media.py check` reports any file over 10 MB that sits outside an ignored folder
or the LFS folder, so a large export committed in the wrong place is caught before it spreads to
every clone.

## Git LFS, and the tripwire

- `brand/src/exports/large/.gitattributes` marks every file in that folder for LFS, except itself
  and the folder's pair, which stay ordinary text. It is the only LFS rule in the project.
- **Never run `git lfs track`.** It writes a root `.gitattributes`, a shared file that no template
  seeds.
- Without git-lfs set up, Git commits a large file whole and says nothing. So when the project
  was generated, and only where no LFS filter was configured, a setting in the repository's own
  `.git/config` (`filter.lfs.required`) was turned on: `git add` of a file in the large folder
  then fails loudly, with `clean filter 'lfs' failed`, instead of committing it.
- That failure is the tripwire working. The fix is to install git-lfs and run `git lfs install`
  once on the machine; never unset the setting, and never move the file out of the folder.
- `media.py check` is the second guard: it reports a file marked for LFS that is stored as a
  plain blob, and one present while no LFS filter is configured.
- The Git host's LFS storage and bandwidth are limited by plan (`VERIFY` the host's current
  terms); keep only what pieces use, and never re-export a large file under the same name.

## The register

| Column | Holds |
|---|---|
| Design | the design's name, as the author calls it |
| Claude Design link | its link, exactly as Claude Design gives it; kept here and nowhere else |
| Export path | the file's path from the repository root |
| Storage | `git` or `lfs` |
| Exported | the date it was exported, DD/MM/YYYY |
| Notes | the rights-register ID of any font, image or music in it; 'superseded' with the date |

## How we apply it here

- Never overwrite an export: a revision is a new file under a new name, with a new row, and the
  old row is marked superseded.
- Sprite frames use `<sprite>-<pose>-mouth-<shape>` (a–h/x), or pose plus `<sprite>-mouth-<shape>`;
  `<sprite>-<pose>-blink` is optional. Keep the native mouth origin and whole-number scale recorded.
- An export that carries a licensed font, image or piece of music has its rows in
  `production/src/rights-register.md` before a piece using it is scheduled.
- A still or logo an edit uses directly may be copied into `production/src/assets/`; the export
  and its row stay the record.
- A podcast show's cover, and an image a partner site wants in its own branding, are exports,
  encoded with `media.py image` (`podcast.cover` and `podcast.id3_cover`; the site's own key).

## Who implements it

- **Workflow:** `brand/workflows/03-record-a-design-export/`.
- **Skills:** none; the author files the export, and Claude checks it and writes its row.

## Governing standard

`.claude/rules/syntek-media/04-toolkit-pipeline.md` Section 2 owns the `check` command and
Section 4 what the toolkit needs, git-lfs for large exports among it;
`.claude/rules/syntek-media/06-global-rules.md` Section 4 owns never overwriting an exported
design asset. The rules own the requirements; this guide owns where an export goes and how it
is recorded.
