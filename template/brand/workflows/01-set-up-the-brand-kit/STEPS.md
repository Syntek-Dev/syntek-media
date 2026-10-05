---
workflow: 01-set-up-the-brand-kit
phase: author
skills: []
model: opus
---

# STEPS.md — set up the brand kit

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The ordered procedure for settling the brand kit with the author. Each step names the skill and
guide it uses. **Run in order** (the written brand before any token, the tokens before the
layouts, the checks before the proofs) and tick `CHECKLIST.md` as you go.

> Read the read-order files first (this folder's `CONTEXT.md` and `CLAUDE.md`). No media skill
> runs this procedure: the grill-with-docs skill (syntek-author), where present, settles each
> decision with the author, and the toolkit checks the result.

## 1. Grill the kit with the author

> **Skill:** grill-with-docs (syntek-author), where present · **Guide:** `brand/docs/reference/the-brand-kit.md`

Check that the companion's `.claude/skills/<skill>/SKILL.md` exists for grill-with-docs; where it
does not, say so, and ask the same questions in rounds yourself, each with a recommended answer
(`.claude/rules/syntek-media/06-global-rules.md` Section 8). Settle what the kit must do before
any value is chosen: where the brand is seen and at what sizes, what must read at a glance, what
a thumbnail and a title card carry, how captions should sit over the brand's pictures, and what
the author already has (a palette, a logo, fonts and their licences). Look facts up rather than
asking for them. _Substantive._

## 2. Reconcile with the written brand

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Where syntek-author is applied, read its brand guide, standards/brand/brand-guide.md (or the
Brand folder its 00-project.md Paths name), and its voice notes, where present: the palette, the
faces and the logo rules. List the values the kit will share with them and any the
author wants different on screen, report each difference with both values, and record the
author's decision. Where none is present, say so: the kit starts from the author's answers.
_Substantive._

## 3. Set the colours

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Offer values for the six colour tokens, as `#RRGGBB`, with a recommendation. Check text on
background, text on surface and on-accent on accent against 4.5:1, and say which pairs fail
before the author chooses. Write the chosen values into `brand/src/design-system/tokens.css` and
remove the colour group's flag. _Substantive._

## 4. Set the type, and add the fonts

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Agree the display and body faces and their weights. For each font file the author supplies, read
its licence and record what it allows (video, thumbnails, embedding) in a `font` row of
`production/src/rights-register.md`, through `production/workflows/07-clear-the-rights/` where it
is not yet cleared. Then place the file in `brand/src/design-system/fonts/` as
`<family>-<weight>.<ext>`, add its font-face rule to `tokens.css` with a relative source, and name
the family in its token. A generic family stands in until a font is cleared. _Substantive._

## 5. Set the space unit and the radius

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Agree the unit every layout multiplies and the corner radius, in relative units so a layout
holds at every deliverable's size, and remove the space group's flag. _Substantive._

## 6. Set the caption style

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Agree the caption face, weight and size, the text and outline colours (`#RRGGBB`) and the
outline width; sizes are in `vh`, a share of the frame's height. The face must be in the fonts
folder or installed, because `captions burn` fails rather than burn a fallback face. The longest
line a vertical deliverable allows (`publishing/docs/reference/captions.md`) must fit inside its
safe zone at that size. Remove the caption group's flag. _Substantive._

## 7. Check the tokens

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Run `python3 toolkit/media.py tokens`. Exit 0: every required token is present and parses. Exit
1: fix each token it names with the author, and run it again. Exit 2: it could not run; say which
tool is missing (`brand/workflows/06-check-the-setup/` reports it) and never report the check as
passed. _Mechanical._

## 8. Adapt the two layouts

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

With the author, adapt `brand/src/design-system/previews/thumbnail.html` and
`brand/src/design-system/previews/card.html`: where the picture, the title, the kicker and the
name sit, how large the title is, what a title card and an end card carry. Keep the layout
contract in `brand/src/design-system/previews/CLAUDE.md`: line 1 unchanged, tokens only, one file
for every aspect ratio, text inside the safe-zone variables, nothing over the network, and the
card's background transparent. Placeholder words stay placeholders. Remove a layout's flag only
when the author calls it the brand's own. _Substantive._

## 9. Check every card, and render proofs

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Run `uv run toolkit/card.py check` on each of the seven cards. Render each layout at a landscape
and a vertical size with `uv run toolkit/card.py render <card> --size 1920x1080` and
`--size 1080x1920`, and the card once more with `--transparent`; render the captions card at the
vertical size. Every render takes `-o` naming a file in today's proofs folder,
`production/src/renders/proofs/brand-kit-DD-MM-YYYY/` (`thumbnail.1920x1080.png`, for example),
which no piece owns and the command makes. Show every proof to the author. A missing browser is
exit 2 with its install command: give it, and stop.
_Mechanical (rendering); judging each proof with the author is substantive._

## 10. Record

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Record each decision in `.claude/MEMORY.md` under Decisions, dated (under the heading
syntek-author's 00-project.md Memory headings map it to, where present). Run
`python3 toolkit/media.py flags brand/src/design-system/` and confirm no `AUTHOR TO CONFIRM` is
left in `tokens.css` or the two layouts. With the author's agreement, commit the kit before any
sync with Claude Design. _Mechanical._

## 11. Hand back

> **Skill:** none · **Guide:** `brand/docs/reference/the-brand-kit.md`

Report the values decided, the fonts added with their rights rows, the proofs and where they are,
each difference from the written brand and how the author settled it, and anything still
flagged. Where the brand keeps a Claude Design project, the next procedure is
`brand/workflows/02-sync-with-claude-design/`. _Substantive._
