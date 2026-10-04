# credits-log.md — every credit <%BRAND_NAME%> spends

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **This file is a seeded stub, and it is deliberately unfinished.**
> It ships with the project so that the skills which route here point at something real from day one.
> Until `python3 toolkit/media.py take add` logs the first take, the table below has no rows.

One row per credit-spending call, so that what was spent is visible across every skill and every piece.
`take add` writes the row for a voiceover or narration take, the `captions` skill writes it for speech-to-text, and any later generation writes its own.
A row is written when the call is made, whether or not its result is kept.

## How to add a row

- Rows are appended in the order the calls were made, and never edited or deleted; a correction is a new row whose Notes name the row it corrects.
- The Date column is DD/MM/YYYY; the Piece column is the piece's folder name, or `—` for a call no piece owns, such as a voice trial.
- The Tool column is the MCP tool's name without its prefix, such as `text_to_speech` or `speech_to_text`.
- The Calls column is the number of calls the row covers, normally one.
- The Characters or minutes column holds the request's characters for text-to-speech, or the audio's minutes for speech-to-text.
- The Voice column is the voice's name as `brand/src/voice/voice.md` records it; the Model column is the model ID.
- The Output column is the file the call produced, relative to `production/src/`, or `—`.

## Log

| Date | Piece | Tool | Calls | Characters or minutes | Voice | Model | Output | Notes |
|---|---|---|---|---|---|---|---|---|
