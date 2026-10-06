---
workflow: 09-time-the-voice
phase: produce
skills: [voiceover, storyboard]
model: opus
---

# STEPS.md — time the voice

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

The procedure for timing a scene piece's approved joined voice and re-timing its boards.
Run in order with `CHECKLIST.md` open. It works towards M4 (storyboarded → produced), through
`M4.words` and `M4.cues`; mouths are first reviewed at `M4.stills`, in production/workflows/10-animate-a-scene/.

## 1. Read the piece and its progress

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Read the brief, approved script, storyboard, shot list and segment register. Confirm the scene
route (a shot typed `scene`), `storyboarded`, and `M4.takes` dated or explicitly `n/a` with its
reason. Follow the first undated sub-check; keep the dates already earned unless the voice or
boards changed. A new/re-rolled take clears all four sub-checks, M4 and later gates. _Substantive._

## 2. Check the offline tools

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Run `python3 toolkit/media.py check --setup`. Read its WhisperX interpreter, cached models and
Rhubarb dictionary lines. If anything this procedure needs is missing or broken, give its fix
and stop. The author alone runs `transcribe fetch`; never fetch a model from this procedure.
Every command here is offline and spends no credits. _Mechanical._

## 3. Join the approved takes

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

Run `python3 toolkit/media.py voice join <piece>`: approved takes in register order, with their
pauses, as mono 16-bit WAV in the piece's production renders folder. Stop at an unapproved take;
return to `production/workflows/02-make-a-voiceover/`, never substitute a scratch track.
_Mechanical._

## 4. Align and agree the words

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

When only the boards are being re-timed and `M4.words` still stands, keep the accepted words
and check; continue to step 5. Otherwise run `python3 toolkit/media.py transcribe <piece>`
and read the printed check with the author.
Resolve findings before going on; discuss low-score warnings and every request/text difference.
The cross-check is on by default; omit it only on the author's word with `--no-cross-check`,
which the check records. Once accepted, repeat with `-o production/src/timing/<piece>.words.json`:
words and check are written together. The author reads the tracked check and agrees the words;
record `M4.words` in `verified`, after the preceding sub-check, and update `last_updated`.
_Substantive._

## 5. Make the mouth timings

> **Skill:** `voiceover` · **Guide:** `production/docs/reference/voiceover.md`

A board-only re-time with unchanged voice keeps its accepted mouth file; continue to step 6.
Otherwise run `python3 toolkit/media.py lipsync <piece>` on the same joined voice. Its dialogue is the
segments' plain `text`, never request tags or pronunciation respellings. Read its printed result;
accept its data through `-o production/src/timing/<piece>.mouth.json`. Its US-English recogniser
and truncated centisecond timings need review at `M4.stills`, in production/workflows/10-animate-a-scene/;
never approve the mouths from this JSON alone. Do not run `levels`: it is an optional diagnostic.
_Mechanical._

## 6. Match and re-time the boards

> **Skill:** `storyboard` · **Guide:** `scripts/docs/reference/storyboards-and-shot-lists.md`

Run `python3 toolkit/media.py cues <piece>`; read the table, event IDs and every finding.
Link each SFX/MUSIC event to one logged effect/music `[[audio]]` row with `cue = 'e02'` in
the edit; that row owns its exact placement, range, gain, fades and ducking. Re-run cues.
Resolve findings, then propose the storyboard's Time column and the shot list's Seconds from
the actual words, with the author's Timing notes. On agreement, repeat through
`-o production/src/scenes/<piece>.cues.json`, and apply the board/shot edits. A re-time raises
board `version`, keeps `approved:` and M3, and clears `M4.cues`, `M4.stills`, M4 and later gates.
A note replacing a shot or changing words also clears M3: return to
`scripts/workflows/03-storyboard-a-piece/` instead. Once the author has agreed the current
re-timed board, date `M4.cues` after `M4.words` and update `last_updated`. _Substantive._

## 7. Hand back

> **Skill:** none · **Guide:** `production/docs/reference/voiceover.md`

Report the accepted tracked timing files, decisions on the words check and the board's new
version, which sub-checks are dated, and what remains. Commit accepted data; any existing
tracked output must be committed and unchanged before `-o` can replace it. Never open an
ignored working copy: commands print the evidence. Next is production/workflows/10-animate-a-scene/,
where the author checks stills and the preview master. _Mechanical._
