@./CONTEXT.md

# CLAUDE.md — toolkit/

Read order: `.claude/CLAUDE.md` → `.claude/MEMORY.md` → this folder's `CONTEXT.md` (imported
above) → this file → `python3 toolkit/media.py <command> --help` for the command you will run.

## Purpose (one line)

Keep the production machinery small, dependable and run through one command, so a master or a
deliverable is one line and a failed render says exactly what failed.

## How to work here

- **Routing:** `cut-for-platform` runs `assemble`, `cut`, `encode`, `still-video` and `loudness`,
  web video and silent loops among them, and `feed tag` (it changes a render); `captions` runs
  `extract-audio` and every `captions` action, `captions transcript` included;
  `voiceover` runs `take add` and `footage add --kind generated`; `thumbnail-brief` runs
  `uv run toolkit/card.py render`, then `media.py image` for every still in its deliverable's
  format and `media.py cut … --overlay` for a newsletter's preview GIF; `write-script` runs
  `script time`; `prepare-post` reads `presets`, runs `flags --piece`, and for a self-hosted
  podcast `feed new`, `feed add`, `feed chapters`, `feed check` and `feed write`. The audiobook
  skill, where the project makes audiobooks, runs `audiobook text`, `audiobook master` and
  `audiobook check`. `brand/workflows/03-record-a-design-export/` runs `image` for a show's cover.
  `brand/workflows/01-set-up-the-brand-kit/` runs `tokens` and `card.py check`;
  `brand/workflows/06-check-the-setup/` runs `check --setup`;
  `production/workflows/01-log-source-media/` runs `footage add` and `footage verify`;
  `publishing/workflows/07-refresh-the-platform-specs/` runs `presets --stale-after 183`. Any
  skill may run `where <piece>` to find a piece's files.
- **Model:** the mechanical tier for running a command and reporting what it printed; **Opus** for
  any change to a script, the data or a layout
  (`.claude/rules/syntek-media/05-model-allocation.md`).
- **Concrete steps (running a command):**
  1. Run it from the repository root as `python3 toolkit/media.py …` (or `uv run toolkit/card.py
     …`); never type the ffmpeg command it wraps, because the command carries the preset, the
     overrides, the naming and the verification.
  2. Read what it printed: the probe line, every `FAIL` and every note on an unconfirmed
     (`verify`) value.
  3. Report the exit code with the probe; the author watches or listens before a render counts.
- **Concrete steps (a platform value has changed):** confirm the platform's own words with the
  author, then add an `[[override]]` to `brand/src/platforms/overrides.toml` with its source and
  the date checked, and run `media.py presets <key>` to see it applied; never edit
  `data/platforms.toml` in a project.
- **Concrete steps (changing the machinery):** describe the change and why to the author first;
  keep helper modules standard-library only; dependencies live in pinned PEP 723 scripts,
  `card.py` and `transcribe.py`. Run `python3 toolkit/media.py --self-test`,
  `uv run toolkit/card.py --self-test` and `python3 toolkit/transcribe.py --self-test` before and after.
- **Concrete steps (a self-hosted podcast's feed):** `feed write` takes `--as-of` always (the
  episode's `pub_date`, the time it is uploaded): at M7 its upload copy goes to the top of
  `publishing/src/renders/`, which no piece owns; once the author reports the feed live,
  `publishing/workflows/06-record-a-publication/` writes the tracked copy with the same
  `--as-of`. A refusal (a changed `podcast:guid`, a GUID gone while its row is not withdrawn, a
  length changed under the same URL) is read, never worked around: the register is corrected.
- **Definition of done:** the command exited 0, its probe was read, and nothing in a renders or
  generated folder was edited by hand.

## Guardrails

- **Minimalism is a feature.** No new dependency, server or framework without the author's
  decision; a module that needs a package is a module that breaks on the next machine.
- **Never edit a render.** Masters, deliverables, card and thumbnail PNGs and takes are generated;
  change the source and render again.
- **Never stream-copy a cut.** `-c copy` cuts on the nearest keyframe; `cut` and `assemble` seek
  before the input and re-encode, so every caption stays on its frame.
- **Never overwrite outside the output folders.** A path `-o` names may be new; an existing
  script, register, caption file, master copy or design export is never written over. The
  exceptions are a show's tracked feed, which only `feed write -o` replaces, after its
  comparison, and a piece's tracked timing and scene files, which only the command that makes
  each replaces through `-o`, while Git holds the old version committed and unchanged.
- **Identity is for life.** A show's `podcast:guid` and each episode's `guid` are written once by
  `feed new` and `feed add`; never type one by hand, and `feed new --rekey` only while nothing is
  published.
- **Voice planning is offline.** `speak plan` prints requests, characters and calls and creates
  only the takes or trial folder. `voice join` reads approved takes by their recorded paths;
  `levels` writes only working JSON, never a tracked copy or a credit rate.
- **Never read what Git ignores.** Each scan lists only what Git tracks or would track; an ignored
  media file is opened only by the path a manifest, register or argument names.
- **A piece's output folders are the toolkit's.** It makes a piece's folder in
  `production/src/renders/`, `production/src/voiceover/generated/` and
  `publishing/src/renders/` when it first writes there; never make one by hand, and never put a
  tracked file in one, where it would never be committed.
- **Fail loudly.** A command that cannot do its job exits 2 naming the missing tool and its install
  hint, or the missing file; it never leaves a partial output behind.
- **Never spend from here.** No command calls ElevenLabs; a take is generated by a skill, after the
  author's yes, and only named and logged here.
- **Argument lists, never shell strings.** Every ffmpeg call is a `subprocess.run([...])` list, run
  with its working folder set where filtergraph quoting would bite, so a path with spaces or quotes
  is safe in any shell.
- **Never take the whole machine.** Every ffmpeg call runs under a thread cap: `MEDIA_THREADS`
  when it is set, else every CPU but two; run one render at a time.

## Output & naming

- **Template-owned:** every file here; `copier update` replaces them. The modules carry a usage
  docstring and exit codes (0 done or clean, 1 a finding, 2 could not run).
- **Generated (never hand-edit):** masters (`<piece>.master.mp4` or `.wav`) and extracts in
  `production/src/renders/<piece>/`, and card PNGs (`<piece>.<card>.<W>x<H>[.transparent].png`)
  in its cards folder; deliverables
  (`<piece>[--cNN].<platform>-<format>[.burned].<ext>`), thumbnail PNGs, encoded images
  (`<stem>.<platform>-<format>.<ext>`), preview GIFs, captions, stills, a feed episode's audio
  (`<piece>.podcast-feed-audio.mp3`, tagged in place by `feed tag`) and JSON chapters
  (`<piece>.chapters.json`) in `publishing/src/renders/<piece>/`, and a feed's upload copy
  (`<show>.feed.xml`) at that folder's top; takes (`<piece>.sNN.tN.mp3` or `.pcm`) in
  `production/src/voiceover/generated/<piece>/takes/`, as
  `.claude/rules/syntek-media/08-naming-and-memory.md` Section 1 names them. A name with no
  piece key, such as a footage file's extract or a show cover's encode, stays at its folder's
  top. Where the project makes audiobooks, its folder's generated/ holds the
  chapter chunks (`<piece>.chNN.pNN.txt`), their sidecar (`<piece>.chNN.chunks.toml`, the pause
  after each chunk) and the takes; its renders/ holds the mastered chapters (`<piece>.chNN.mp3`),
  the credits being `ch00` (opening) and `ch99` (closing).
- **Captions go where `-o` says:** `captions align`, `retime`, `rewrap`, `vtt` and `transcript`
  write to the path `-o` names, normally in `publishing/src/captions/`, or else to stdout; an
  existing caption or transcript file there is never overwritten, so the author moves the old
  one aside first.
- **Also writes, on request:** a script's `words` and `estimated_seconds` (`script time --write`),
  a segment or chapter register's take and the credits-log row (`take add`), a manifest row
  (`footage add`), and, where the project self-hosts a podcast, a show's register (`feed new`,
  `feed add`, `feed tag`) and its tracked feed (`feed write -o`).
- **New modules:** `media_<area>.py`, standard library only, imported by `media.py` and covered by
  its `--self-test`; never a second command line.
- **Lip sync:** `media.py lipsync <piece>` uses the approved joined voice and plain segment
  `text`, never respellings or request tags. Preserve Rhubarb's native cues and centisecond
  timings, with `soundFile` repository-relative even for linked audio. Rhubarb's fatal exit 1
  becomes exit 2; its dictionary belongs beside its real executable through any link. Missing
  Rhubarb is an optional setup note naming `lipsync`, a broken installed copy a finding.
- **Known-word alignment:** `media.py transcribe <piece>` reads approved segments on the joined
  WAV, prints the words check and writes ignored working timing; `-o` accepts words/check into
  `production/src/timing/`, both committed and unchanged before replacement. Cross-check is on
  by default; `--no-cross-check` records its omission. Only the author runs `transcribe fetch`.
- **Captions from words:** `captions from-words WORDS --deliverable KEY [--offset TC] [-o SRT]`
  preserves first/last word boundaries, reports short gaps and checks the existing house limits.
