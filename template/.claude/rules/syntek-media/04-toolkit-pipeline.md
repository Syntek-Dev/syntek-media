# 04-toolkit-pipeline.md — how sources become masters and deliverables, and the toolkit commands

**Last Updated**: <%DATE%> **Version**: 0.1.0 **Maintained By**: <%OWNER_NAME%>
**Language**: British English (en_GB)

> **Template-owned.** Shipped by syntek-media and replaced by every `copier update`: never edit it here. Where syntek-author's project settings file (00-project.md) is present, it outranks this file and says where project rules go; otherwise they go in `.claude/CLAUDE.md`, under the heading 'Project-specific rules'.

Every render runs through `toolkit/`: one standard-library command line,
`python3 toolkit/media.py <command>`, and one PEP 723 script, `uv run toolkit/card.py`. Its
`--help` lists every command; **where this file and `--help` disagree, `--help` is right**, and
this file is reported as stale. Media has no root Makefile; one that exists is syntek-author's.

---

## 1. The pipeline

```text
brand/src/design-system/tokens.css ──► HTML layouts (the brand's previews, else toolkit/templates/)
        └──► uv run toolkit/card.py render ──► card and thumbnail PNGs
footage (manifest + local mirror), cards, the voice track
        └──► media.py assemble production/src/edits/<piece>.toml ──► master (production/src/renders/)
                └──► media.py cut / encode / still-video ──► deliverables (publishing/src/renders/)
                        └──► media.py captions burn (or a sidecar .srt and .vtt)
card PNGs, renders and design exports ──► media.py image ──► JPEG, WebP, AVIF; posters (--at)
the overlay PNG (card.py --transparent) + the master ──► media.py cut --overlay ──► a GIF preview
a show register (publishing/src/podcast/) ──► media.py feed tag, chapters, check, write ──► the feed
ElevenLabs (MCP) ──► generated/ (absolute output_directory) ──► media.py take add
        └──► the segment or chapter register, and a credits-log row
```

`assemble` renders any card PNG that is missing or older than its HTML or `tokens.css` first, so a
master always rebuilds from tracked files.

---

## 2. The commands

Exit codes everywhere: **0** done and verified (or clean); **1** a finding, or an output that failed
its verification; **2** could not run (bad arguments, missing input, a missing tool named with its
install hint, or the tool itself failed). `--deliverable KEY` takes a `<platform>.<format>` key of
`toolkit/data/platforms.toml`. Timecodes are `HH:MM:SS.mmm`.

| Command (`python3 toolkit/media.py …`) | Arguments | What it does | Exit |
|---|---|---|---|
| `probe` | `FILE [--json]` | duration, size and every stream (a `.pcm` take read with its `--output-format`) | 0 · 2 |
| `presets` | `[KEY] [--stale-after DAYS --today DD/MM/YYYY]` | deliverable tables with their `verify` keys and brand overrides applied; lists stale `checked` dates | 0 · 1 · 2 |
| `script time` | `PATH [--wpm N] [--write]` | spoken words and pauses per beat (each against its own `(target MM:SS)`) and in total, at the brief's `words_per_minute` unless `--wpm` overrides, against `target_seconds` (±10%) and each `max_seconds` | 0 · 1 · 2 |
| `assemble` | `EDL [-o OUT]` | the master from an edit decision list: frame-accurate clips, stills, cards, colour, fades, push-in, the voice track, `[[audio]]` ranges, ducking, loudness; ffprobe-verified | 0 · 1 · 2 |
| `cut` | `SRC --deliverable KEY --in TC --out TC [--cut cNN] [--frame crop\|pad] [--x PX] [--captions SRT] [--overlay PNG] [-o OUT]` | trims, reframes and encodes one deliverable in one pass, burning captions when given and laying a transparent overlay of the deliverable's size when given; verifies size, codecs, duration and moov first; an audio deliverable (no width or height, such as an audiobook's retail sample) is trimmed and encoded as audio only; a table with `audio_tracks = 0` gets no sound track; a GIF table (`newsletter.preview_gif`) is cut to a GIF within its `max_seconds`, `fps_max`, `colours_max` and `max_size` | 0 · 1 · 2 |
| `encode` | `SRC --deliverable KEY [--frame crop\|pad] [-o OUT]` | a whole file to a video or audio deliverable, loudness to its target; an audio deliverable from a picture master takes its sound only; `podcast.feed_audio` untagged, its tags `feed tag`'s | 0 · 1 · 2 |
| `frame` | `SRC --at TC [-o OUT]` | one PNG still, for a thumbnail background | 0 · 2 |
| `image` | `SRC --deliverable KEY [--at TC] [--format jpg\|png\|webp\|avif] [--frame crop\|pad] [-o OUT]` | an image deliverable from a PNG or still, or from a video at `--at` (a poster): scaled to the table's size, in its first `formats` entry or `--format`, flattened where `alpha = false`, verified for size, format and `max_size`; never a GIF (that is `cut`'s) | 0 · 1 · 2 |
| `still-video` | `IMAGE AUDIO --deliverable KEY [-o OUT]` | a still under audio as video | 0 · 1 · 2 |
| `extract-audio` | `SRC [--in TC --out TC] [--rate HZ] [-o OUT]` | mono 16-bit WAV of a file or a range, for speech-to-text or alignment; by default `production/src/renders/<stem>[.<in>-<out>].wav` | 0 · 2 |
| `captions check` | `SRT [--deliverable KEY] [--script SCRIPT]` | the caption limits, overlaps and gaps; with `--script`, the words against a script or transcript | 0 · 1 · 2 |
| `captions from-segments` | `REGISTER --deliverable KEY [--offset TC] [-o SRT]` | cues from approved voiceover segments, each segment's duration shared by character count; joins exact | 0 · 1 · 2 |
| `captions align` | `TEXT AUDIO [--lines B.L-B.L] [--anchors] [--noise DB] [--min-silence S] [-o SRT]` | cues spread over the speech that `silencedetect` finds, beat by beat with `--anchors`, one cut's lines with `--lines`; to standard output without `-o` | 0 · 1 · 2 |
| `captions retime` | `SRT (--in TC --out TC \| --edl EDL --source FID) [-o SRT]` | master timing to a cut's, or recording timing to the master's through the edit decision list; to standard output without `-o` | 0 · 2 |
| `captions rewrap` | `SRT --deliverable KEY [-o SRT]` | re-chunks to the deliverable's line width; to standard output without `-o` | 0 · 1 · 2 |
| `captions vtt` | `SRT [-o VTT]` | SRT to WebVTT; to standard output without `-o` | 0 · 2 |
| `captions transcript` | `TEXT [--lines B.L-B.L] [--date DD/MM/YYYY] [-o MD]` | the published transcript of a script or transcript, whole or one cut's lines: one sentence per line, a paragraph per beat, on-screen text kept, directions dropped; to standard output without `-o` | 0 · 2 |
| `captions burn` | `SRC SRT --deliverable KEY [-o OUT]` | an ASS file sized to the output, styled from the caption tokens, burned in; fails when the caption font fell back | 0 · 1 · 2 |
| `loudness measure` | `FILE` | integrated LUFS, true peak and range | 0 · 2 |
| `loudness normalise` | `FILE --target social\|podcast\|acx [-o OUT]` | two-pass `loudnorm` with `-ar`, then re-measured | 0 · 1 · 2 |
| `audiobook text` | `SOURCE --piece PIECE --chapter chNN [--footnotes drop\|inline] [--limit CHARS]` | chapter text with syntek-author's markup stripped and pronunciations applied, every unspoken word listed, chunked into the audiobook's generated folder; a chunk ends at every pause, recorded in the chapter's `<piece>.chNN.chunks.toml` | 0 · 1 · 2 |
| `audiobook master` | `CHUNKS… --piece PIECE --chapter chNN [--head S] [--tail S] [-o OUT]` | joins takes with the pauses the chunk sidecar records, adds room tone, masters to the ACX profile | 0 · 1 · 2 |
| `audiobook check` | `FILE…` | the ACX checks: RMS, peak, noise floor, sample rate, constant bitrate, channels, length, room tone | 0 · 1 · 2 |
| `take add` | `FILE --piece PIECE (--segment sNN \| --chapter chNN --part pNN)` | renames a fresh ElevenLabs file to its name (`.pcm` for a `pcm_*` format), writes the register's `take` and `file`, appends the credits-log row | 0 · 2 |
| `feed new` | `SHOW --feed-url URL [--site SLUG] [--rekey]` | writes a show register from its skeleton with the show's identity, once; `--rekey` corrects the feed URL and every GUID only while nothing is published; refuses a project without the show-register folder | 0 · 2 |
| `feed add` | `SHOW --piece PIECE` | appends an episode's row, `planned`, its GUID written once | 0 · 2 |
| `feed tag` | `SHOW --piece PIECE` | re-muxes the episode's M5 render without re-encoding, with the row's ID3 tags, chapters and the show's cover; writes `render`, `bytes` and `seconds` into the row; refuses an empty title or description and bad chapters | 0 · 1 · 2 |
| `feed write` | `SHOW --as-of 'DD/MM/YYYY HH:MM' [-o FILE]` | the show's RSS feed of every `ready` or `published` episode due by `--as-of`, the same bytes for the same input; compares with the tracked feed first and writes nothing when a GUID vanished or a length changed under an old URL; to standard output without `-o` | 0 · 1 · 2 |
| `feed chapters` | `SHOW --piece PIECE [-o OUT]` | the episode's JSON chapters, by default into `publishing/src/renders/` | 0 · 1 · 2 |
| `feed check` | `SHOW [--feed FILE] [--previous FILE]` | offline: required values, no flag left, unique GUIDs and enclosures, the tracked-feed comparison, the render's size and length, the cover and art, the chapter keys | 0 · 1 · 2 |
| `footage add` | `FILE --kind KIND --location LABEL [--rights RRNNNN]` | copies a file into the mirror (never moves it), hashes and probes it, appends the next `F` ID; refuses a duplicate | 0 · 2 |
| `footage verify` | `[--manifest PATH]` | the local mirror against the manifest | 0 · 1 · 2 |
| `tokens` | `[--tokens PATH]` | every required custom property present and parseable | 0 · 1 · 2 |
| `flags` | `[PATH…] [--piece PIECE] [--strict]` | both flags, in every form, over the files Git tracks or would track; `--piece` gathers one piece's files across the scripts, production and publishing layers | 0 · 1 · 2 |
| `check` | `[--strict] [--setup]` | the large-file and Git LFS guard and the nested ignore rules; `--setup` adds the readiness report, the optional image encoders among it | 0 · 1 · 2 |
| `--self-test` | — | fixtures written at run time; exercises every module; probes that need ffmpeg skip by name | 0 · 1 · 2 |

**`toolkit/card.py`** (`uv run toolkit/card.py …`):
`render HTML (--deliverable KEY | --size WxH) [--transparent] [-o OUT]` renders a layout to PNG
in Chromium, offline, with the safe-zone variables set and, for a deliverable, `data-deliverable`
and `data-platform` on `:root` (so a newsletter image shows its play button); `check HTML` proves the tokens resolve
and the brand fonts load; `--self-test`. A missing browser is exit 2, naming
`uv run --with playwright==1.62.0 playwright install chromium`.

---

## 3. Rules

- **Renders are generated.** Never hand-edit a master, deliverable, PNG or take; change the source
  and render again. Deliverables come from `media.py`, never a hand-typed ffmpeg command, so each
  carries its verification; ffmpeg and ffprobe may still inspect a file.
- **Read the render before reporting it.** The skill reports the command's own probe, and the
  author watches or listens: a render that succeeded is not a deliverable that was checked.
- **Never `-c copy` for a frame-accurate cut**: a stream copy cuts on the nearest keyframe and
  drifts every caption after it.
- **Outputs go to a renders or generated folder**, named as
  `.claude/rules/syntek-media/08-naming-and-memory.md` Section 1 says; nothing is written elsewhere
  unless `-o` names the path, and nothing outside those folders is overwritten. The commands that
  make tracked files (`captions align`, `retime`, `rewrap`, `vtt` and `transcript`, and
  `feed write`) write to standard output unless `-o` names the file, so always pass `-o`.
- **The exceptions are named.** The registers and the manifest are written only by `take add`,
  `footage add` and, for a show register, `feed new`, `feed add` and `feed tag`, none of which
  rewrites a value the author set. A show's tracked feed, `<show>.feed.xml` beside its register,
  is the one tracked file the toolkit overwrites: only `feed write -o`, after its GUID comparison,
  through a temporary file, once the author reports the feed live.
- **Platform numbers live in `toolkit/data/platforms.toml`**, which an update refreshes. A
  confirmed difference is an `[[override]]` in `brand/src/platforms/overrides.toml`, never an edit
  of the data file (`publishing/workflows/07-refresh-the-platform-specs/`).
- **Big binaries never sit in plain Git.** Renders and generated audio are ignored by
  `production/src/.gitignore` and `publishing/src/.gitignore`; footage and archived takes live in
  external storage, listed in `production/src/footage/manifest.toml`; Git LFS is only for
  `brand/src/exports/large/`. Never add a root `.gitattributes` or run `git lfs track`.
- **Nothing reads what Git ignores**: `flags` and `check` filter through `git check-ignore`, and an
  ignored media file is opened only by the path a manifest, register or argument names, its name
  and hash printed, never its content (`.claude/rules/syntek-media/06-global-rules.md` Section 12).
- **Keep the toolkit minimal**: the Python standard library only (3.11 or later) and TOML data,
  with one exception, `toolkit/card.py`, which declares Playwright inline and runs through `uv run`.

---

## 4. What the toolkit needs

| Tool | For |
|---|---|
| `ffmpeg` and `ffprobe`, built with libass, x264 and mp3lame | every render, probe, loudness pass and caption burn |
| `python3` (3.11 or later) and `git` | every `media.py` command; the repository root and what Git ignores |
| `uv`, with Playwright's Chromium | `toolkit/card.py`, and the card PNGs `assemble` renders |
| `git-lfs` | large design exports in `brand/src/exports/large/` |
| ffmpeg's libwebp, an AV1 encoder (libaom-av1 or libsvtav1) and the `avif` muxer (optional) | `media.py image` to WebP and AVIF; JPEG and PNG need none |
| `pandoc` (optional) | cleaner chapter text in `audiobook text`, which works without it |
| `espeak-ng` (optional) | a scratch voice track for timing, labelled approximate |

`python3 toolkit/media.py check --setup` reports every one of them, the allow, ask and deny
entries of `.claude/settings.json`, and whether the ElevenLabs server's base path contains the
project (`brand/workflows/06-check-the-setup/`). If a tool is missing, say which one and which
command it blocks. Never report a command as passed when it could not run.
