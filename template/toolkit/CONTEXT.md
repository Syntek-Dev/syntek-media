# CONTEXT.md — toolkit/

The supporting layer that holds the machinery: the one command that turns tracked sources into
masters, deliverables and images (and, where the project self-hosts a podcast, its feed), the one
script that turns a layout into a PNG, the word aligner, the platform data and fallback layouts.
It is minimal: standard-library Python driving ffmpeg and ffprobe, with heavy dependencies in
pinned PEP 723 scripts; no server or web interface. Only the author's `transcribe fetch` reaches
the network deliberately, uv's first package install aside. Run it from the repository root;
you do not keep work here. The rules it serves live in
`.claude/rules/syntek-media/04-toolkit-pipeline.md`; if the two ever disagree, `--help` is right
and the rules file is reported as stale.

## Directory Tree

```text
toolkit/
├── CONTEXT.md          ← this file
├── CLAUDE.md           ← operating rules
├── .gitignore          ← keeps Python's __pycache__/ out of Git
├── media.py            ← the one command: python3 toolkit/media.py <command>; --help lists them all
├── media_common.py     ← shared: TOML, timecodes, presets and the brand's overrides, paths, the ffmpeg runner (thread-capped)
├── media_video.py      ← assemble, cut, encode, frame, still-video
├── media_audio.py      ← extract-audio, loudness, audiobook, take add, voice plans, join, timing
├── media_captions.py   ← captions (check, from-segments, align, retime, rewrap, vtt, transcript, burn) and script time
├── media_repo.py       ← footage, tokens, flags, check, where
├── media_image.py      ← image, and the GIF pass of cut (a newsletter's preview GIF)
├── media_feed.py       ← feed: a self-hosted podcast's register, RSS feed, chapters and file tags
├── card.py             ← HTML and CSS to PNG in headless Chromium (uv run; Playwright 1.62.0, pinned)
├── transcribe.py       ← offline known-word alignment; WhisperX 3.8.6, Python >=3.10,<3.14
├── data/               ← platforms.toml: every deliverable's delivery specs, dated and sourced
└── templates/          ← thumbnail.html and card.html: fallbacks for the brand's two layouts
```

## What's here

- `media.py` — **the only entry point.** Every render, check and register write goes through
  `python3 toolkit/media.py <command>`: probe, presets, script time, assemble, cut, encode, frame,
  image, still-video, extract-audio, captions, loudness, audiobook, take add, speak plan, voice join,
  levels, transcribe, lipsync, feed, footage,
  tokens, flags, where and check. Its `--self-test` writes lavfi clips, a still, screen recordings in the
  shapes Playwright and VHS write (WebM, MP4, animated GIF, none with sound), SRT, TOML, a show
  register and a git repository at run time and exercises every module; a probe that needs
  ffmpeg, or an encoder this ffmpeg lacks, is skipped by name, never passed.
- `media_common.py`, `media_video.py`, `media_audio.py`, `media_captions.py`, `media_repo.py`,
  `media_image.py`, `media_feed.py` — the helper modules `media.py` imports. **They have no
  command of their own**; each opens with a docstring saying what it owns.
- **The brand's own channels** (sites, blogs and newsletters): web video is `cut` or `encode` to a
  `website.*` or `blog.*` key; a silent loop is a cut whose table sets `audio_tracks = 0`, and gets
  no sound track; every still (a poster, a share, featured or preview image, a show's cover) is
  `image`, from a `card.py` render, a design export or a video's frame at `--at`, into the
  table's format (JPEG, PNG, WebP or AVIF); a newsletter's preview GIF is `cut` to its GIF table
  with a `--overlay` rendered by `card.py render --transparent`, and plays only as many times as
  fit its `max_seconds`.
- **A self-hosted podcast** (`feed`, where the project self-hosts one): `feed new` opens a show's
  register in the show registers' folder, with its `podcast:guid` written once; `feed add` gives
  each episode its row and GUID; `feed tag` writes the episode's tags, chapters and cover into
  its feed audio (encoded untagged at M5 with `encode`); `feed chapters` writes its JSON chapters;
  `feed check` proves the register offline; `feed write --as-of` writes the RSS feed the author
  uploads. Nothing is fetched or posted.
- `card.py` — renders a thumbnail or card layout at a deliverable's exact size with the
  safe-zone variables set on `:root`, aborting every outside request, and checks a layout against
  the contract: tokens linked and resolving, brand fonts loading, `@dsCard` on line 1 of a
  preview. **A script with a dependency**, declared inline (PEP 723) and pinned, so
  `uv run toolkit/card.py` fetches Playwright for itself and installs nothing globally.
- `transcribe.py` — WhisperX 3.8.6 aligns approved segment words on the joined voice; the heard-word
  cross-check runs by default. `media.py transcribe` uses `MEDIA_TRANSCRIBE_PYTHON` where set,
  otherwise offline uv. Only the author runs `transcribe fetch` once; the worker's self-test
  needs no dependency. Working words/check files land in the piece's ignored timing folder;
  accepted tracked copies are written together through `-o`, both Git-clean for replacement.
- **Lip sync:** `media.py lipsync <piece>` runs CPU Rhubarb on the joined voice with plain
  segment text. It preserves native mouth cues and writes repository-relative `soundFile`,
  first to working timing JSON, then to an accepted tracked mouth file through `-o`. Keep the
  dictionary beside the executable's real path; a version check alone cannot prove readiness.
  Review its centisecond estimates at `M4.stills`.
- **Cue index:** `media.py cues <piece>` connects tracked words to beats, boards, lines and
  delivery/SFX/music events. Effect/music events take their source and mix from audio rows
  linked by `cue`; it prints enclosing MM:SS boards and exact seconds, then accepts JSON through `-o`.
- `data/platforms.toml` — the template's platform data, refreshed by `copier update`; the
  brand's confirmed corrections are `[[override]]` tables in `brand/src/platforms/overrides.toml`,
  which every command applies and prints.
- `templates/` — the layouts a piece copies only where the brand has no
  `brand/src/design-system/previews/thumbnail.html` or
  `brand/src/design-system/previews/card.html` of its own.
- **Exit codes, everywhere:** 0 done and verified, or clean; 1 a finding, or an output that failed
  its verification; 2 could not run (bad arguments, a missing input, a missing tool named with its
  install hint, or the tool itself failed).
- **Outputs go to a renders or generated folder** (`production/src/renders/`,
  `publishing/src/renders/`, `production/src/voiceover/generated/` and the audiobook folder's,
  where the project makes audiobooks), a piece's into a folder named for it there
  (`production/src/renders/<piece>/`, `publishing/src/renders/<piece>/` and
  `production/src/voiceover/generated/<piece>/takes/`), picked from the leading piece key of the
  file's name; a name with no piece key stays at the folder's top, and the audiobook folder's
  stay flat. Nothing is written elsewhere unless `-o` names a path, and nothing outside those
  folders is ever overwritten but the tracked files named below. `captions align`, `retime`,
  `rewrap`, `vtt` and `transcript` write to the path `-o` names, or else to stdout, because
  their home, `publishing/src/captions/`, is tracked; so does `feed write`, whose tracked home is
  the show registers' folder. A piece's timing and scene data is written first as a working copy
  in its `production/src/renders/<piece>/timing/`, and in `production/src/timing/` or
  `production/src/scenes/` only where `-o` names the file.
- **The tracked files the toolkit replaces, and only these:** a show's tracked feed,
  `<show>.feed.xml` beside its register, written only by `feed write -o` once the author reports
  the feed live, after its GUID comparison passes, through a temporary file renamed over it; and
  a piece's tracked timing and scene files, which only the command that makes each replaces,
  with `-o` naming it, only while Git reports no uncommitted change to it (an uncommitted change,
  an untracked copy or a project outside a Git work tree is refused, exit 2, changing nothing),
  through a temporary file renamed over it. The registers it writes (`take add`, `footage add`,
  and `feed new`, `feed add` and `feed tag` for a show's register) are edited line by line, and a
  value the author set is never rewritten, except that `take add` resets a re-rolled segment's
  `status` and `archived`.
- **Nothing here reads a file Git ignores.** `flags` and the large-file scan of `check` list only
  what Git tracks or would track; `footage verify`, `take add` and `audiobook` open an ignored
  media file only by the path a manifest, register or argument names, and print its name and hash,
  never its content. `where <piece>` lists a piece's tracked files and names its ignored
  per-piece folders, saying whether each exists, never listing what is inside. Outside a git
  work tree every file is read.
- **Nothing here spends.** No command calls ElevenLabs; only the author's model fetch uses the network. `take add`
  names and logs a file a skill has already generated with the author's yes.

## Cross-references

- `.claude/rules/syntek-media/04-toolkit-pipeline.md` — the pipeline, every command's arguments
  and exits, and what the toolkit needs.
- `.claude/rules/syntek-media/08-naming-and-memory.md` — the names every output takes.
- `brand/workflows/06-check-the-setup/` — `media.py check --setup` before the first spend.
- `production/docs/reference/edit-decision-lists.md` — the edit decision list `assemble` reads.
- `production/docs/reference/sound-and-loudness.md` — the loudness targets `loudness` and
  `assemble` meet.
- `publishing/docs/reference/captions.md` — the caption limits, the four timing routes and the
  published transcript.
- `publishing/docs/reference/platform-specs.md` — how `data/platforms.toml` is read.
- `publishing/docs/reference/thumbnails.md` — the images `card.py` lays out and `image` encodes,
  and the preview GIF.
- The website, blog and newsletter guides, and the podcast-feed guide, where the project publishes
  to those channels or self-hosts a podcast — each in `publishing/docs/reference/`.
