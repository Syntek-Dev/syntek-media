---
workflow: 07-clear-the-rights
phase: review
skills: []
model: opus
---

# STEPS.md — clear the rights

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for clearing every licence, release and consent a piece uses. Each step
names the guide it uses. **Run in order** (an item is matched to its row before its evidence is
judged) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No skill runs
> this procedure; every permission in it comes from the author.

## 1. List what the piece uses

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

Gather every item from the piece's records: the brief's `rights`, the shot list's Rights column,
the `rights` of every footage ID its edit decision list names, each music bed and effect, the
narrator's row in `brand/src/voice/voice.md` for a cloned voice, every quotation or scripture
reading in the script or transcript, the brand's fonts, and any artwork or generated material.
_Substantive._

## 2. Match each item to its row

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

Find each item's row in `production/src/rights-register.md` and add the piece to its Pieces. An
item with no row gets one, opened as `needed` with the author, the next ID in sequence.
_Mechanical._

## 3. Check the evidence

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

For each `cleared` row, check that its Evidence names where the permission is filed, and that the
permission covers this use: the platforms in the brief and the post package, the territory, how
long the piece stays up, and the medium (audio, picture or print). A row that does not cover the
use goes back to `needed`, with the reason in Notes. A row whose Expires falls before the
scheduled date is not cleared for this piece. _Substantive._

## 4. Request what is missing

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

For each `needed` row, the author requests the permission. Draft the request if the author asks,
but never send it. Set the row to `requested`, with the date in Notes. _Substantive._

## 5. Record each answer

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

When the author reports an answer, record it: `cleared` with its Evidence and Expires, `refused`
with the date and the reason, or `expired`. Never record a permission as cleared without the
permission in hand. _Mechanical._

## 6. Resolve what cannot be cleared

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

For each `refused`, `expired` or unanswered row the piece cannot wait for, agree with the author
what happens: the item is cut, replaced or re-shot, through the procedure that owns that file
(`production/workflows/03-assemble-the-master/` for the master). Never publish around a refusal.
_Substantive._

## 7. Hand back

> **Skill:** none · **Guide:** `production/docs/reference/rights-and-consent.md`

Report every row the piece uses with its status, what was requested and when, and what was cut or
replaced. Say plainly whether the rights part of M7 is met: every row the piece uses `cleared`.
_Substantive._
