# FICTION.md — narrate-audiobook, fiction mode

The domain for narrating a novel: chapters read in one voice, scene breaks heard as silence, and
every constructed name said as its language records it.

## Paths and unit

- **Unit:** one audiobook piece. **Chapter:** one chapter of the novel, one file.
- **Procedures:** `production/workflows/05-narrate-an-audiobook/` and
  `production/workflows/06-master-an-audiobook/`.
- **Source:** the chapter's file in syntek-author's manuscript layer, where present, whose status
  is `final`; otherwise the text the author provided.
- **Register:** `production/src/audiobook/<piece>.md`; chunks and takes in the generated folder
  beside it, masters in the renders folder (both git-ignored).
- **Narrator:** the `narration` row of `brand/src/voice/voice.md`; `character:<name>` rows only
  where the author has chosen a voiced cast.
- **Constructed names:** the IPA in the language's lexicon or the names register of syntek-author's
  world layer, where present, copied into `voice.md` `## Pronunciations` with its source named.
- **Footnotes:** `--footnotes drop`; a novel rarely has any, and a listener cannot use one.

## Additions to the steps

- **Step 3 — also check the credits.** The opening credits give the title, the author and the
  narrator; an AI narrator is named as such. The closing credits follow the guide.
- **Step 5 — also settle every constructed word from its recorded IPA.** The command lists each
  word in a `.conlang` span; copy its IPA from syntek-author's lexicon or names register, where
  present, with the author's agreement. A word with no IPA anywhere goes back to the author: never
  guess one from the spelling.
- **Step 5 — also keep dialogue, dialect and invented spelling exactly as written.** A chunk that
  reads oddly is reported, never regularised.
- **Step 6 — also account for every scene break.** Each ends a chunk, and the chapter's sidecar
  holds its silence: tell the author how many each chapter has, to hear each one at step 10.
- **Step 10 — also hear each constructed name the first time it is voiced**, before the rest of
  the book is approved.

## Domain rules

- **The lexicon is the record of how a name is said**, where syntek-author's world layer is
  present: the pronounce skill (syntek-author) is never run from here, and a voice that cannot say
  the IPA is noted as a fault of the voice, never fixed by changing the IPA.
- **A voiced cast is the author's decision**: each character keeps one voice for the whole book,
  and none imitates a real actor or reader (`.claude/rules/syntek-media/03-production-ethics.md`
  Section 6).
- **The words are the author's**: no line is cut, softened or explained for the ear.
- **AI narration is disclosed** on every channel that carries it, as
  `publishing/docs/reference/ai-disclosure.md` sets out.

## Examples

An invented line from Morgan Example's novel, carried from the source to the chunk:

```text
source    She said the old word, [hevrith]{.conlang lang=example-tongue}, and the lamps went out.
listed    hevrith: no spoken form
voice.md  | hevrith | /ˈhɛvrɪθ/ | HEV-rith | names register | the oath-word |
chunk     She said the old word, /ˈhɛvrɪθ/, and the lamps went out.
```

The source keeps its span and its spelling; only the chunk, which is never tracked, carries the IPA.
