---
type: guide
skills: [storyboard]
model: opus
---

# Storyboards and shot lists — a picture for every spoken line, a source for every shot

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The storyboard says what the viewer sees while each line of the approved script is
spoken; the shot list names each source and whether it is cleared. Together they are what the edit decision list is written from, so a gap here becomes a
hole in the master. A piece with no picture, or a recorded one, has neither, and its M3 is `n/a`.

## The storyboard

`scripts/src/pieces/<piece>/storyboard.md`: frontmatter `piece`, `version`, `approved`, the H1
`# <Title> — storyboard`, then one table, one row per board. The shot list has no frontmatter.

| Column | Holds |
|---|---|
| `#` | The board's ID, `B01`, `B02` …, permanent once used. |
| `Beat` | The script's beat number. |
| `Time` | Where the board sits in the piece, `MM:SS–MM:SS`. |
| `Picture` | What the viewer sees, in one sentence. |
| `Spoken` | The script lines it covers, as `beat.line` (`2.1–2.3`). |
| `On screen` | The words of the `TEXT:` cues shown over it. |
| `Sound` | The `SFX:` and `MUSIC:` cues under it. |
| `Vertical framing` | For every vertical deliverable: `centre`, `crop x=<px>`, `pad` or `native` for a scene. |
| `Timing notes` | Timing changes from stills and previews; `—` when absent. |

## The shot list

`shot-list.md`, beside it: `| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |`.
Shots are `S01`, `S02` …, each naming its board. Type is
`camera · screen · stock · still · card · colour · generated · scene`. Source is a footage ID (`F0007`),
an image or text capture under `production/src/assets/` (`.txt`, `.ansi`, `.html`), a card under `production/src/cards/`, a colour
`#RRGGBB`, `production/src/scenes/<piece>.scene.py` for a scene, or `to shoot`. Status moves `needed · captured · logged · cleared`; Rights is a
rights-register ID, or `—` where nothing needs clearing.

## Vertical framing

A landscape master is reframed for each vertical deliverable, so the board decides where the
picture sits: `centre`, a crop from a stated `x` offset in source pixels, or `pad` where nothing
may be lost. A scene uses `native`: render its vertical aspect directly, keeping its pixel grid.
Text and faces stay inside its safe zone in `toolkit/data/platforms.toml`, read with `python3 toolkit/media.py presets <key>`; a value listed in a
table's `verify` is unconfirmed and is checked by eye.

## Rights from the first sketch

Every licensed or identifiable thing a board shows or plays — music, stock, footage of people or
private places, a likeness, a quotation on screen, a font, generated art — opens a `needed` row
in `production/src/rights-register.md` as soon as it is boarded, and the shot carries its ID. A
voice or likeness needs recorded consent. Production clears rights; boarding records the need.

## How we apply it here

- Board from the approved script only; every spoken line sits in exactly one board's range.
- Stills, cards and colour clips are shots; note a push-in or fade in Picture for the edit list.
- A generated picture is typed `generated` and must agree with the brief's `ai_visuals`; if it
  does not, the brief's disclosure plan changes first, with the author.
- Every board of a scene piece is Type `scene`; its other sources are images or text captures,
  never recorded video inside a scene; index them with `media.py real <piece>` and accept through `-o`. The brief records `ai_visuals: assisted`.
- After voice timing, `media.py cues <piece>` prints the table; accept the cue index with `-o`
  in `production/src/scenes/`, through `production/workflows/09-time-the-voice/`.
- Re-time Time and shot Seconds or timing-only notes: raise `version`, keep approval and M3,
  clear `M4.cues`, `M4.stills`, M4 and later gates. A word or shot change clears approval and M3.
- Eight-column older boards remain readable; a hyphen or an en dash separates Spoken references.
- Printed Time encloses the words (start rounded down, end up); JSON keeps exact seconds.

## Who implements it

- **Workflow:** `scripts/workflows/03-storyboard-a-piece/`.
- **Skills:** `storyboard` writes both files and opens the rights rows; `cut-for-platform`
  writes the edit decision list from them, through `production/workflows/03-assemble-the-master/`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns rights and consent, and
Section 3 makes M3 (scripted → storyboarded) binding. The rules own the requirements; this guide
owns how the pictures and their sources are written down.
