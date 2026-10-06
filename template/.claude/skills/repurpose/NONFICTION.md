# NONFICTION.md — repurpose, non-fiction mode

The domain for cutting down a non-fiction author's long pieces: talks, podcast episodes and long
explainers, cut into clips that each carry one idea with its reasons and its sources.

## Paths and unit

- **Unit:** one piece: a recorded talk, a podcast episode or a long explainer, in
  `scripts/src/pieces/NNN-kebab-title/`. **Cut:** one idea, one question answered, or one story
  told whole.
- **Procedure:** `publishing/workflows/01-plan-the-cut-downs/`.
- **Master:** `production/src/renders/<piece>/<piece>.master.mp4`, or `.wav` for an audio-only
  episode. **Plan:** `publishing/src/cut-downs/<piece>.md`.
- **Sources:** the book's argument and its sources, in syntek-author's content and research
  layers, where present; read, never edited.
- **Guides:** `publishing/docs/reference/cut-downs.md`; the podcast-episode, long-video and
  short-video guides in `scripts/docs/reference/`, where the project makes those kinds;
  `production/docs/reference/rights-and-consent.md` for quotations and scripture.

## Additions to the steps

- **Step 2 — also** read every claim a candidate moment makes against its source. A recorded
  claim that was corrected or accepted at M2 carries its correction into the cut, in a caption or
  on screen.
- **Step 4 — also** an idea is cut with its reason, never its conclusion alone; an audience
  question is cut with the question, or with a title card that asks it. A view the talk argues
  against is cut only with its fair statement, or not at all.
- **Step 6 — also** an audio-only episode's cut goes onto video platforms under a still (the
  episode art or a brand card): name it in the cut's note.
- **Step 7 — also** list any moment that quotes another writer or reads scripture aloud: it needs
  its row (Kind `quotation` or `scripture`) covering audio and video use before it is agreed.

## Domain rules

- A scene piece uses its native master for each aspect, Frame `native`, with the master list
  default first; missing aspects return to `production/workflows/10-animate-a-scene/`.

- **Context travels with the claim.** A cut never makes the author say more, or less, than the
  whole piece says; a qualifier, a caveat or a 'some scholars hold' stays with its claim.
- **Sources stay on screen.** A quotation or a scripture reading shows its source, and for
  scripture its reference and translation, as on-screen text for as long as the words are heard.
- **A translation's permission covers only what it says.** Some permissions cover print and not
  audio or video; the rights row says which, and a cut that reads a translation aloud waits for
  that row to be `cleared`.
- **Guests consent to their cut.** A guest or an audience member heard or shown in a cut has a
  `likeness` or `voice-consent` row that covers clips, not only the full episode.

## Examples

An invented plan for Robin Example's recorded talk, *The Long Table*:

```markdown
| Cut | Deliverables | Lines | In | Out | Frame | Hook | Status |
|---|---|---|---|---|---|---|---|
| c01 | youtube.short, instagram.reel | 2.4–2.8 | 00:06:41.300 | 00:07:24.050 | crop x=700 | Hospitality was never about the food. | approved |
| c02 | facebook.reel | 5.1–5.6 | 00:21:10.900 | 00:21:58.400 | crop x=700 | Why would you set a place for a stranger? | approved |

## c02 — Why would you set a place for a stranger?

Opening words: the question, asked on a title card, because the audience member has no consent row.
On-screen text: 'Hebrews 13:2' and the translation, for as long as the verse is read.
Stands alone: the question, the answer and its one source.
```

An invented question kept out of the plan:

```text
Line 4.3 reads a long passage from a living author's book. Is there a quotation row
that covers video use, or should the cut paraphrase and cite it instead?
```
