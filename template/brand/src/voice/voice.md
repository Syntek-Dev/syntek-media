# voice.md — how <%BRAND_NAME%> sounds aloud

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `brand/workflows/05-write-the-spoken-voice/` has settled the voice with the author, each section below holds its writing rules and an `AUTHOR TO CONFIRM` flag, and the tables have no rows.

The spoken voice of <%BRAND_NAME%>: how it sounds when it is heard, who says it for each use, and how its hard words are said.
The `voiceover` skill reads this file before every call and uses exactly what it records.
Voice IDs are kept here and nowhere else in the repository.

## Spoken style

<!-- AUTHOR TO CONFIRM: the pace in words a minute, the register, how the brand's name is said aloud, and the words the brand never says aloud. -->

- **Pace (words a minute):** —
- **Register:** —
- **The brand's name, said aloud:** —
- **Never said aloud:** —

The scripts layer times every script at this pace unless a piece's brief sets its own `words_per_minute`.
Write the name as a respelling, stressed syllable in capitals, and add it to Pronunciations below.

## Written voice

The written voice is syntek-author's, where present (its voice notes, standards/style/voice-notes.md, and in a business its brand voice, brand-voice.md in the Brand folder its 00-project.md Paths name), and is not restated here.

## Narrators

<!-- AUTHOR TO CONFIRM: one narrator for each use the brand needs, chosen with the author by listening, and recorded here with the date it was chosen. -->

- One row per use: the Use column takes one of `voiceover · narration · podcast-host · character:<name>`, and a segment or chapter register names its narrator by that Use.
- The Service column reads `ElevenLabs` for a voice used through the user-scope MCP server `elevenlabs`.
- The Voice column holds the voice's name and the Voice ID column its ID, exactly as ElevenLabs gives them.
- The Model ID column holds the model found with `mcp__elevenlabs__list_models` when the narrator was chosen; it is never assumed.
- The Stability, Similarity, Style and Speed columns hold the settings sent on every call, unchanged between calls.
- The Output format column holds the ElevenLabs output format chosen for the deliverable; `mp3_44100_192` needs the Creator tier or above, and `pcm_44100` the Pro tier or above.
- The Consent column holds the rights-register ID of the person's recorded consent for any cloned voice, the owner's own included, or a dash for a stock or designed voice.
- The Chosen column holds the date the author chose the narrator, DD/MM/YYYY.
- Changing a narrator is the author's decision: record it in `.claude/MEMORY.md` with its date, then change the row.

| Use | Service | Voice | Voice ID | Model ID | Stability | Similarity | Style | Speed | Output format | Consent | Chosen |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Pronunciations

<!-- AUTHOR TO CONFIRM: every word a narrator might say wrongly, the brand's own name first, each with its IPA, a respelling and where the pronunciation comes from. -->

- One row per word, in alphabetical order.
- The IPA column is broad IPA without slashes; the request text puts it between slashes only where the recorded model reads inline IPA.
- The Respelling column is how an English-speaking listener would say the word, in plain hyphenated syllables with the stressed syllable in capitals (VAH-ree).
- The Source column says where the pronunciation comes from: the person named, an authoritative reference, or syntek-author's names register (world/src/names-register.md), where present, for an invented name.
- A script never holds IPA: `voiceover` substitutes it into the request text, and never writes it back.
- Never delete a row: a corrected pronunciation keeps its row, with 'corrected DD/MM/YYYY' and the old form in Notes.

| Word | IPA | Respelling | Source | Notes |
|---|---|---|---|---|
