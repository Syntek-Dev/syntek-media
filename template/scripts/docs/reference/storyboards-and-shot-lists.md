---
type: guide
skills: [storyboard]
model: opus
---

# Storyboards and shot lists — a picture for every spoken line, a source for every shot

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

**What it is.** The storyboard says what the viewer sees while each line of the approved script is
spoken; the shot list says where every one of those pictures comes from and whether it is
cleared. Together they are what the edit decision list is written from, so a gap here becomes a
hole in the master. A piece with no picture, or a recorded one, has neither, and its M3 is `n/a`.

## The storyboard

`scripts/src/pieces/<piece>/storyboard.md`: frontmatter `piece`, `version`, `approved`, the H1
`# <Title> — storyboard`, then one table, one row per board (`shot-list.md` has no frontmatter:
the H1 `# <Title> — shot list`, then its table).

| Column | Holds |
|---|---|
| `#` | The board's ID, `B01`, `B02` …, permanent once used. |
| `Beat` | The script's beat number. |
| `Time` | Where the board sits in the piece, `MM:SS–MM:SS`. |
| `Picture` | What the viewer sees, in one sentence. |
| `Spoken` | The script lines it covers, as `beat.line` (`2.1–2.3`). |
| `On screen` | The words of the `TEXT:` cues shown over it. |
| `Sound` | The `SFX:` and `MUSIC:` cues under it. |
| `Vertical framing` | For every vertical deliverable: `centre`, `crop x=<px>` or `pad`. |

## The shot list

`shot-list.md`, beside it: `| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |`.
Shots are `S01`, `S02` …, each naming the board it serves. Type is one of
`camera · screen · stock · still · card · colour · generated`. Source is a footage ID (`F0007`),
an asset under `production/src/assets/`, a card under `production/src/cards/`, a colour
`#RRGGBB`, or `to shoot`. Status moves `needed · captured · logged · cleared`; Rights is a
rights-register ID, or `—` where nothing needs clearing.

## Vertical framing

A landscape master is reframed for each vertical deliverable, so the board decides where the
picture sits: `centre`, a crop from a stated `x` offset in source pixels, or `pad` where nothing
may be lost. Text and faces stay inside the deliverable's safe zone, read from
`toolkit/data/platforms.toml` with `python3 toolkit/media.py presets <key>`; a value listed in a
table's `verify` is unconfirmed and is checked by eye.

## Rights from the first sketch

Every licensed or identifiable thing a board shows or plays — music, stock, footage of people or
private places, a likeness, a quotation on screen, a font, generated art — opens a `needed` row
in `production/src/rights-register.md` as soon as it is boarded, and the shot carries its ID. A
voice or a likeness is used only with the person's recorded consent. Clearing happens in
production; boarding is where the need is first written down.

## How we apply it here

- Board from the approved script only; every spoken line sits in exactly one board's range.
- Stills, cards and colour clips are shots like any other; note a slow push-in or a fade in the
  Picture column, for the edit decision list to carry.
- A generated picture is typed `generated` and must agree with the brief's `ai_visuals`; if it
  does not, the brief's disclosure plan changes first, with the author.
- One sentence per line in every cell and note.

## Who implements it

- **Workflow:** `scripts/workflows/03-storyboard-a-piece/`.
- **Skills:** `storyboard` writes both files and opens the rights rows; `cut-for-platform`
  writes the edit decision list from them, through `production/workflows/03-assemble-the-master/`.

## Governing standard

`.claude/rules/syntek-media/03-production-ethics.md` Section 6 owns rights and consent, and
Section 3 makes M3 (scripted → storyboarded) binding. The rules own the requirements; this guide
owns how the pictures and their sources are written down.
