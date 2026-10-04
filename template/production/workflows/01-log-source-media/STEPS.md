---
workflow: 01-log-source-media
phase: produce
skills: []
model: opus
---

# STEPS.md — log source media

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for logging source files before an edit names them. Each step names the
guide it uses. **Run in order** (a file's rights and location are settled before it is logged)
and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure; every value in it comes from the author or from the toolkit.

## 1. Confirm what is coming in

> **Skill:** none · **Guide:** `production/docs/reference/source-media.md`

Ask the author which files are being logged, what kind each is (`video`, `audio`, `music`,
`stock`, `image` or `generated`), when it was recorded, and which piece it is for, if one is
known yet. A recording that is itself to become a piece goes to
`production/workflows/08-bring-in-a-recording/` instead. _Substantive._

## 2. Check the rights

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

A file that is licensed, or shows a recognisable person, a private place or someone else's work,
needs a row in `production/src/rights-register.md`. Find it, or open a `needed` row with the
author; never log such a file without its rights ID. _Substantive._

## 3. Agree the location

> **Skill:** none · **Guide:** `production/docs/reference/source-media.md`

Agree with the author where the master copy of each file lives (a named drive, a NAS, a cloud
folder) and the label that names it. A label, never a link that carries a token. _Substantive._

## 4. Add each file

> **Skill:** none · **Guide:** `production/docs/reference/source-media.md`

For each file, run `python3 toolkit/media.py footage add FILE --kind KIND --location LABEL`,
adding `--rights RRNNNN` where it has a row. The toolkit copies the file into
`production/src/footage/raw/` when it lies outside it, hashes and measures it, and appends the
next footage ID. If it refuses a duplicate, report the existing ID and log nothing. Then fill the
new row's `recorded` (DD/MM/YYYY) and any `notes` with the author. _Mechanical._

## 5. Verify the mirror

> **Skill:** none · **Guide:** `production/docs/reference/source-media.md`

Run `python3 toolkit/media.py footage verify`. A changed byte or an unlisted file fails: report
it, and never change the manifest to match. Entries listed as not mirrored can be fetched from
their location when a piece needs them. _Mechanical._

## 6. Hand back

> **Skill:** none · **Guide:** `production/docs/reference/source-media.md`

Report each footage ID with its kind, duration and location, the rights rows opened, and the
result of `footage verify`. Remind the author that the master copies are safe only once they are
backed up at their location. _Substantive._
