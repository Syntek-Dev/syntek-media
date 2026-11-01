# BUSINESS.md — media-tone, business mode

The domain for a tone pass on a business's pieces: explainers, product and service shorts, team
and customer stories, and their posts. A business's spoken voice sits beside its written brand
voice, and a viewer hears the difference between a peer who knows the work and a sales pitch.

## Paths and unit

- **Unit:** one piece.
- **The words in scope:** `scripts/src/pieces/<piece>/script.md` (spoken lines and `TEXT:` cues),
  `scripts/src/pieces/<piece>/storyboard.md` (on-screen text), `publishing/src/thumbnails/<piece>.md`
  (its words) and `publishing/src/posts/<piece>.md` (the words media owns).
- **The creator:** `brand/src/voice/voice.md`; syntek-author's brand voice and voice person, where
  present (standards/brand/brand-voice.md, or the brand folder its project settings name), read as
  an input and never edited.
- **Where it is posted:** each profile in `brand/src/platforms/` the piece's deliverables go to,
  and the social-media documents a profile's social-plan line names, where present.
- **Guides:** `brand/docs/reference/the-spoken-voice.md` and
  `brand/docs/reference/platform-profiles.md`.

## Additions to the steps

- **Step 2 — also freeze every claim about the business:** a price, a discount, a result, a
  guarantee, a client's name, a comparison and an offer's end date, word for word.
- **Step 3 — also read the written brand voice,** where syntek-author's is present, for its marks
  and its voice person ('I' or 'we'): a post's written words are read against it as an input, and
  a spoken line that contradicts it is reported, never resolved silently.
- **Step 4 — also read for the pitch.** Superlatives, buzzwords and urgency that the piece does
  not earn; a hook that promises more than the piece shows; 'we' where the brand speaks as one
  person, or 'I' where it speaks as a team.
- **Step 6 — also keep every disclosure where the plan puts it.** A paid partnership's label or
  an AI disclosure line is frozen, and no tone change moves it later in the piece or the post.

## Domain rules

- **Specific over superlative.** A line that says what the business does beats one that says how
  good it is; a tone change never adds a claim the brief does not make.
- **A customer's or a member of staff's words are theirs.** A recorded line is never retoned, and
  a quoted one is changed only with their consent and the author's word.
- **Professional on one platform is not stiff on another.** The register for a Short and for a
  long explainer can differ, as the Register line's sub-bullets set them, while the brand stays
  one voice.

## Examples

An invented proposal for a Harbour Lane Studio short:

```text
3 · 1.2 · VO: Our world-class team delivers seamless results. · Register (short: plain, peer to peer)
    · VO: We book, shoot and edit your video in a week. · Says what is done; the 'week' is the brief's own claim, unchanged.
```

An invented tone handed on: 'On the short, speak as a neighbour who knows the work; on the long
explainer, as the person who will run the shoot' — for `brand/workflows/05-write-the-spoken-voice/`,
as two sub-bullets of the Register line.
