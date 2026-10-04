# BUSINESS.md — storyboard, business mode

The domain for boarding a business's pieces: the team, the premises and the work on camera, screen
recordings of the product or service, and the brand's own cards, with the consent of every client,
customer and member of staff who can be recognised.

## Paths and unit

- **Unit:** one piece. **Board row:** one picture, carrying one spoken line or a run of lines.
- **Procedure:** `scripts/workflows/03-storyboard-a-piece/`.
- **Script:** `scripts/src/pieces/<piece>/script.md`. **Board and shot list:**
  `scripts/src/pieces/<piece>/storyboard.md` and `scripts/src/pieces/<piece>/shot-list.md`.
- **The brand's look:** `brand/src/design-system/tokens.css` and the card layout in
  `brand/src/design-system/previews/`; syntek-author's brand guide,
  standards/brand/brand-guide.md, where present (or the brand folder its project settings name),
  for how the logo may be used.
- **The brand's own pictures:** `production/src/assets/` (logos, product stills, screenshots) and
  `production/src/footage/manifest.toml`.
- **Rights:** `production/src/rights-register.md`.
- **Guides:** `scripts/docs/reference/storyboards-and-shot-lists.md` and
  `production/docs/reference/rights-and-consent.md`.

## Additions to the steps

- **Step 2 — also read the brand's visual rules.** Read the tokens, the card layout, the logo files
  in `production/src/assets/` and syntek-author's brand guide, where present, so every card and
  name caption uses the brand's colours, type and logo as the guide allows.
- **Step 4 — also put the call to action on an end card.** The last beat's `TEXT:` call to action
  becomes an end card row with its own Time, and the logo sits on that card, never over footage of
  a person.
- **Step 6 — also prefer the brand's own pictures.** The team, the premises, the work and a screen
  recording of the product or service come before stock; stock is used only where the brand has
  no picture of its own. A screen recording shows demonstration data only.
- **Step 7 — also clear every person and every client.** Staff, customers and clients who can be
  recognised need a `footage-release` or `likeness` row; filming on a client's premises needs a
  `location` row; a client's logo or work on screen is an `artwork` row, with that client's
  permission.
- **Step 9 — also group the shoot by place.** The shoot list groups every `to shoot` shot by
  location and names who must be on camera, so that one visit covers each place.

## Domain rules

- **Consent before a likeness** (`.claude/rules/syntek-media/03-production-ethics.md` Section 6):
  nobody who can be recognised appears without a release on the register.
- **No client data on screen** (`.claude/rules/syntek-media/06-global-rules.md` Section 10): no
  real names, email addresses, account numbers or dashboards in a screen recording; demonstration
  data, or the shot is reframed or filmed again.
- **The brand's tokens are the only colours and type on a card**, and the logo is used only as
  the brand's guide allows.
- **A picture never promises more than the script says**: no award, client logo or result on
  screen that the brief cannot evidence (Section 7).

## Examples

Invented board rows for Harbour Lane Studio's explainer:

```markdown
| # | Beat | Time | Picture | Spoken | On screen | Sound | Vertical framing |
|---|---|---|---|---|---|---|---|
| B01 | 1 | 00:00–00:04 | The owner at the studio desk, mid-shot | 1.1 | Visitors, but no bookings? | voice; room tone | crop x=656 |
| B02 | 2 | 00:04–00:14 | Screen recording: a long booking form, demonstration data | 2.1 | Ask for the date first | voice; music low | pad |
| B03 | 3 | 00:14–00:22 | End card: the call to action and the logo | 3.1–3.2 | Book a free review: link below | voice; music out | centre |
```

The shot list behind them:

```markdown
| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |
|---|---|---|---|---|---|---|---|
| S01 | B01 | camera | to shoot | crop x=656 | — | needed | RR0002 |
| S02 | B02 | screen | to shoot | pad | — | needed | — |
| S03 | B03 | card | production/src/cards/004-booking-forms.end.html | centre | 8.0 | needed | — |
```
