# FICTION.md — voiceover, fiction mode

The domain for voicing a novelist's pieces: book trailers, teasers and short readings, where the
narrator sets the book's mood and a constructed name must sound the same in every trailer, every
reading and the audiobook.

## Paths and unit

- **Unit:** one piece. **Segment:** one spoken sentence, or one short beat read as one breath.
- **Procedure:** `production/workflows/02-make-a-voiceover/`.
- **Voiced lines:** the script's `VO:` and `NARRATOR:` lines, and each character's lines under that
  character's upper-case name.
- **Register:** `production/src/voiceover/<piece>.toml`; takes in
  `production/src/voiceover/generated/<piece>/takes/` (git-ignored).
- **Joined voice:** `production/src/renders/<piece>/<piece>.voice.wav`, from `voice join`;
  a scene piece dates `M4.takes` after its used takes are approved and archived.
- **Narrators:** the `voiceover` row of `brand/src/voice/voice.md`, and one `character:<name>` row
  for each character the author has chosen to voice separately.
- **Constructed names:** the language's lexicon or the names register in syntek-author's world
  layer, where present, is the source of each IPA; `voice.md` `## Pronunciations` carries it, with
  that source named.
- **Guides:** `production/docs/reference/voiceover.md`,
  `brand/docs/reference/the-spoken-voice.md`, and the trailer guide in `scripts/docs/reference/`,
  where the project makes trailers.

## Additions to the steps

- **Step 2 — also name each character line's speaker.** A character with no `character:<name>`
  row is read by the narrator, or waits for the author to choose a voice at step 3.
- **Step 3 — also keep one voice per character across every piece.** A character who sounds
  different in the second trailer is a different character to the listener.
- **Step 5 — also take every constructed name's IPA from `voice.md`, never from memory.** Where a
  name has no row, copy its IPA from syntek-author's lexicon or names register, where present, with
  the author's agreement, and name the source. An audio tag suits a trailer (`[whispers]`) where the
  script's braces ask for it and the recorded model supports tags, never as decoration.
- **Step 7 — also stop after the first take that carries a constructed name** and play it to the
  author before the rest are made.

## Domain rules

- **A character's voice is a designed or a stock voice, never an imitation of a real actor or
  reader** (`.claude/rules/syntek-media/03-production-ethics.md` Section 6).
- **The lexicon is the record of how a name is said**, where syntek-author's world layer is
  present: the pronounce skill (syntek-author) is never run from here, and a voice that cannot say
  the IPA is noted as a fault of the voice, never fixed by changing the IPA.
- **Voice only the lines the approved script holds**, even when the book has better ones: what a
  trailer gives away is the brief's decision.
- **A trailer voiced by AI is disclosed** as `publishing/docs/reference/ai-disclosure.md` says,
  whatever a platform's own toggle rule.

## Examples

An invented trailer line for Morgan Example's novel, and the request it becomes:

```text
script.md   NARRATOR: {whispers} Nobody crosses the Vessaran marsh twice.
voice.md    | Vessaran | /ˈvɛsərən/ | VESS-uh-run | names register | stress on the first syllable |
text        Nobody crosses the Vessaran marsh twice.
request     [whispers] Nobody crosses the /ˈvɛsərən/ marsh twice.
```

The `text` is what the captions show; the tag and the IPA reach the server only.
