---
name: media-tone
description: >-
  A tone pass on the words a piece says or shows (script lines, on-screen text, cards, thumbnail
  words and the post words media owns), read together for the creator's spoken voice, the
  audience, the type of content and where it is posted. Freezes every figure, date, claim,
  quotation, disclosure, credit and limit, and every recorded word, and proves them unchanged
  after. Reports by location, applies only what the author accepts, and hands a tone the author
  settles to the brand's procedures, never writing the spoken voice or a profile. Use when the
  author says 'does this sound like us?', 'is the hook too salesy for this platform?', 'make the
  short less formal' or 'check the tone of the trailer'. Not for
  writing or revising the script (`write-script`). Not for a written document's voice (the tone
  skill (syntek-author), where present), nor for channel voice or bios (the social-media-documents
  skill (syntek-author), where present).
---

# Skill: Media Tone (<%BRAND_NAME%>)

Locale: en_GB · <%TIMEZONE%> · dates DD/MM/YYYY.

A viewer or listener forms a view of the brand from how its pieces sound before they meet anyone.
This skill reads the words a piece says or shows for **four things at once**: the creator (how
<%BRAND_NAME%> sounds aloud), the audience (who is listening), the type of content (a Short is not
a long video, a trailer is not a podcast episode) and where it is posted (each platform's tone).
It reports each line that misses, and proposes a change with its reason. It works only on **how**
a line says things, never **what** it says: every figure, date, claim, quotation, disclosure,
credit and limit leaves a tone pass exactly as it entered, and the skill proves it before it hands
back.

It runs beside the tone skill (syntek-author), where present, and never stands aside for it: that
skill owns a written document's voice, in business projects, and this one owns the words a piece says or shows. It is
**not a gate**, and no procedure runs it: it runs when the author names it or asks for a tone pass.

## Governing procedures (route here — do not restate at length)

- No layer's procedure runs this skill. If a layer's `workflows/local/` holds a procedure of the
  author's that names it, follow that procedure instead: the author's local procedure governs
  (`run-media-workflow`, step 2).
- `brand/src/voice/voice.md` — `## Spoken style` (the Register line and its sub-bullets by type
  of content), `## Written voice` and `## Narrators`; the creator's voice this pass reads against,
  never edits.
- `brand/docs/reference/the-spoken-voice.md` — how the spoken voice is written down, and the
  register by type of content.
- `brand/docs/reference/platform-profiles.md` — what a profile's `## Tone on this platform`,
  `## Call to action` and `## The social plan` sections hold, and when a written-side document
  owns them.
- `.claude/rules/syntek-media/01-layout-and-routing.md` Section 1 — the audience test every
  script is written for.
- `scripts/docs/reference/writing-for-the-ear.md` — the spoken line, which a tone change must
  still keep; `scripts/docs/reference/the-piece-ladder.md` — M2, and why a change to an approved
  script is a revision.
- `.claude/rules/syntek-media/03-production-ethics.md` Sections 1, 5 and 7 — who decides what,
  disclosure, and never fabricate.
- `brand/workflows/05-write-the-spoken-voice/` and `brand/workflows/04-set-up-a-platform/` — where
  a tone the author settles is recorded; this skill hands it to them.

The mode file adds this project's types of content, its tone marks and its domain rules.

## Steps

> **Mode.** Before step 1, read the brand-kind mode file beside this one — exactly one of `BUSINESS.md`, `FICTION.md`, `NONFICTION.md` ships in this folder. The mode owns the domain (paths, unit, extra reads, domain rules, examples); this file owns the procedure. Where they disagree, the procedure wins and the disagreement is reported to the author.

1. **Fix the piece and the words in scope.** Agree with <%OWNER_FIRST_NAME%> which piece (its
   folder in `scripts/src/pieces/`) and which words: the script's spoken lines and `TEXT:` cues,
   the storyboard's on-screen text, the thumbnail brief's words, and the post package's words that
   media owns (title, description, hashtags, an embed's title and alt text). Words another skill
   owns stay out: a blog post's or a newsletter's own words, a bio and a text-only post. Where the
   script is approved (`approved:` dated, M2 in `verified`), say before anything else that an
   accepted change to it is a revision that clears M2 and every later gate, and ask whether to go
   on. *Complete when:* the piece, every file in scope and the author's word on an approved script
   are settled.

2. **List what the pass must not touch.** Before reading for tone, list with its exact wording and
   location every figure, date, price, claim, quotation, disclosure line, credit, rights line,
   call-to-action target (the thing the viewer is asked to do, and where) and every value taken
   from the platform data. In a recorded piece's transcript, and in its captions, **every word is
   frozen**: they are what was said. *Complete when:* the frozen list exists, with a count of each
   kind.

3. **Read the four inputs.** **The creator:** `voice.md` `## Spoken style`, its Register line and
   the sub-bullet for this type of content where one stands, and the narrator's Use under
   `## Narrators`. **The audience:** the audience test and the brief's `## Audience`. **The type
   of content:** the brief's `kind`, `origin` and `picture`, each deliverable, and the guide for
   the piece's kind where this project ships it. **Where it is posted:** each platform profile's
   `## Tone on this platform` and `## Call to action`; where its `## The social plan` line names a
   written-side document that sets the tone, that document owns it and is read, never restated.
   Note every flag still open in those sections: a finding resting on an unsettled one says so.
   *Complete when:* each input is read, or named as unset, and the open flags are listed.

4. **Read for tone.** Read every line in scope against the four inputs together: the register
   for this type of content, the audience's ear, and each platform's tone where the line goes to
   more than one. Note where a line sounds like another brand, a different kind of piece, or the
   wrong platform; where a hook oversells what the piece delivers; where on-screen text and the
   spoken line pull in different directions; and where a post's words promise what the piece does
   not. Apply the mode file's tone marks. *Complete when:* every line in scope has been read and
   each miss is recorded with its location and the input it misses.

5. **Report.** Give numbered proposals by location (`beat.line` in a script, the board row, the
   thumbnail or post section), each with the line, the input it misses, the proposed change and a
   one-line reason, grouped where one decision fixes many. Then the lines the pass deliberately
   leaves alone, and, **raised, not proposed**, any line where the tone problem sits inside a
   frozen item, put to the author as a question. Where the right tone is itself unsettled (no
   register for this type of content, no tone for this platform), say so and offer the brand's
   procedure. *Complete when:* the author has the report and has accepted or declined each
   proposal.

6. **Apply only what is accepted, then prove the frozen list.** Apply each accepted change in its
   own file, one spoken sentence per line, and show the changed lines. In an approved script the
   change is a revision, as `write-script` makes one: raise `version`, clear `approved:`, run
   `python3 toolkit/media.py script time` again, and tell the author M2 must pass again. Then
   compare the frozen list from step 2 with the files: every item must be byte-identical.
   *Complete when:* the accepted changes are in, the frozen list is unchanged, and any difference has been
   reverted and reported.

7. **Hand a settled tone to its procedure, and hand back.** Where the author settles a tone that
   should hold beyond this piece, never write it here: a register for a type of content goes to
   `brand/workflows/05-write-the-spoken-voice/`, as a sub-bullet of the Register line, and a
   platform's tone, where no written-side document sets it, to
   `brand/workflows/04-set-up-a-platform/`. Report what changed, what was declined, the frozen-list
   result, any gate the changes cleared, and each tone handed on. *Complete when:* the author has
   the report, and every settled tone is named with the procedure that will record it.

## Anti-patterns

- **Changing a figure, date, claim, quotation, disclosure, credit or limit.** A friendlier
  promise is a changed promise; raise it instead.
- **Editing a recorded transcript's words** for tone. They are what was said.
- **Writing `voice.md` or a profile.** A settled tone goes to its brand procedure.
- **Restating a social-media document's tone** in a profile or a post, where that document sets
  it.
- **Rewriting the whole piece.** Propose by line; the author's voice survives only if every change
  is visible and refusable.
- **Applying a change to an approved script quietly.** It clears M2 and every later gate; say so
  first.
- **Toning for the eye.** A line that reads well but cannot be said in one breath is worse aloud.
- **Inventing a voice** where `voice.md` is unset: say so, and offer the brand's procedure.

## Cross-references

- `write-script` — drafts and revises the script; a tone change to it follows its revision rule.
- `storyboard`, `thumbnail-brief`, `prepare-post` — own the on-screen text, the thumbnail words and
  the post package this pass reads.
- `media-research` — reads a platform's own rules; this skill never sets them.
- `brand/workflows/05-write-the-spoken-voice/` · `brand/workflows/04-set-up-a-platform/` — where a
  settled tone is recorded.
- The tone skill (syntek-author), where present — a written document's voice; the
  social-media-documents skill (syntek-author), where present — channel voice, bios and text-only
  posts.
