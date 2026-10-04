@./CONTEXT.md

# CLAUDE.md — production/src/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → `production/CONTEXT.md` →
`production/CLAUDE.md` → this folder's `CONTEXT.md` (imported above) → this file → the target
subfolder's pair.

## Purpose (one line)

Keep, once each, the records a master is rebuilt from: what each source is and where it lives,
what each piece may use, what each take cost, and how each master is cut.

## How to work here

- **Routing:** each file or folder has one writer and one procedure.

| File or folder | Written by | Procedure |
|---|---|---|
| `footage/manifest.toml` | `python3 toolkit/media.py footage add`, with the author | `production/workflows/01-log-source-media/` |
| `voiceover/` | `voiceover`, with `media.py take add` | `production/workflows/02-make-a-voiceover/` |
| `edits/`, `cards/`, `renders/` | `cut-for-platform`, with `media.py assemble` | `production/workflows/03-assemble-the-master/` |
<: if 'podcast' in MEDIA_KINDS :>| an episode's audio edit and master | `cut-for-platform` | `production/workflows/04-master-a-podcast-episode/` |
<: endif :><: if 'audiobook' in MEDIA_KINDS :>| `audiobook/` | `narrate-audiobook`, with `media.py audiobook` | `production/workflows/05-narrate-an-audiobook/`, `production/workflows/06-master-an-audiobook/` |
<: endif :>| `rights-register.md` | `storyboard` opens rows; the author clears them | `production/workflows/07-clear-the-rights/` |
| `credits-log.md` | `media.py take add`; `captions` for speech-to-text | the procedure that spent the credit |
| a recording's footage row and its captions | `captions` | `production/workflows/08-bring-in-a-recording/` |

- **Model:** **Opus** for every judgement (which take, which cut, whether a permission covers a
  use); the mechanical tier for adding a row the author has already decided and for running the
  toolkit (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps:**
  1. Read the target subfolder's pair, and the guide that governs it, before writing.
  2. Write the entry with the author, in the format the pair gives.
  3. Probe or verify what the toolkit made, and hand back the open questions as
     `AUTHOR TO CONFIRM` flags.
- **Definition of done:** the entry exists in exactly one place, every ID it cites resolves (a
  footage ID in the manifest, a rights ID in the register), and nothing generated was committed.

## Guardrails

- **One sentence per line** in every Markdown artefact here, applied when a paragraph is edited,
  never by mass reflow (`.claude/rules/syntek-media/06-global-rules.md` Section 5).
- **IDs are permanent.** A footage ID, a rights ID, a segment, a cut or a chapter keeps its ID
  for life; a retired entry is marked, never deleted or renumbered.
- **No invented entries.** A row records something the author agreed or the toolkit measured.
  Never fill a seed with plausible examples.
- **Nothing reads what Git ignores.** Open an ignored file only by the path a manifest, register
  or argument names, and print names and hashes, never contents
  (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Never commit a render or generated audio**, and never force one past
  `production/src/.gitignore`.
- **Never overwrite** a register, a manifest row, an edit decision list or a source file without
  confirming with the author.

## Output & naming

- **Seeded:** `rights-register.md`, `credits-log.md` and `footage/manifest.toml`: each ships
  once and is never replaced by `copier update`; if deleted, the next update restores it empty.
- **Written by skills and the toolkit:** `voiceover/<piece>.toml`, `edits/<piece>.toml`,
  `cards/<piece>.<card>.html`<: if 'audiobook' in MEDIA_KINDS :>, `audiobook/<piece>.md` and its two credits files<: endif :>,
  each named for the piece's folder.
- **Template-owned:** `.gitignore`, and the `README.md` of each git-ignored folder;
  `copier update` keeps them current, so never edit them here.
- **Generated (never hand-edit):** everything in `renders/` and in each folder named `generated`;
  `production/src/.gitignore` ignores them.
