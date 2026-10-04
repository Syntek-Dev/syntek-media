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
| `cut` | `SRC --deliverable KEY --in TC --out TC [--cut cNN] [--frame crop\|pad] [--x PX] [--captions SRT] [-o OUT]` | trims, reframes and encodes one deliverable in one pass, burning captions when given; verifies size, codecs, duration and moov first; an audio deliverable (no width or height, such as an audiobook's retail sample) is trimmed and encoded as audio only | 0 · 1 · 2 |
| `encode` | `SRC --deliverable KEY [--frame crop\|pad] [-o OUT]` | a whole file to a video or audio deliverable, loudness to its target | 0 · 1 · 2 |
| `frame` | `SRC --at TC [-o OUT]` | one PNG still, for a thumbnail background | 0 · 2 |
| `still-video` | `IMAGE AUDIO --deliverable KEY [-o OUT]` | a still under audio as video | 0 · 1 · 2 |
| `extract-audio` | `SRC [--in TC --out TC] [--rate HZ] [-o OUT]` | mono 16-bit WAV of a file or a range, for speech-to-text or alignment; by default `production/src/renders/<stem>[.<in>-<out>].wav` | 0 · 2 |
| `captions check` | `SRT [--deliverable KEY] [--script SCRIPT]` | the caption limits, overlaps and gaps; with `--script`, the words against a script or transcript | 0 · 1 · 2 |
| `captions from-segments` | `REGISTER --deliverable KEY [--offset TC] [-o SRT]` | cues from approved voiceover segments, each segment's duration shared by character count; joins exact | 0 · 1 · 2 |
| `captions align` | `TEXT AUDIO [--lines B.L-B.L] [--anchors] [--noise DB] [--min-silence S] [-o SRT]` | cues spread over the speech that `silencedetect` finds, beat by beat with `--anchors`, one cut's lines with `--lines`; to standard output without `-o` | 0 · 1 · 2 |
| `captions retime` | `SRT (--in TC --out TC \| --edl EDL --source FID) [-o SRT]` | master timing to a cut's, or recording timing to the master's through the edit decision list; to standard output without `-o` | 0 · 2 |
| `captions rewrap` | `SRT --deliverable KEY [-o SRT]` | re-chunks to the deliverable's line width; to standard output without `-o` | 0 · 1 · 2 |
| `captions vtt` | `SRT [-o VTT]` | SRT to WebVTT; to standard output without `-o` | 0 · 2 |
| `captions burn` | `SRC SRT --deliverable KEY [-o OUT]` | an ASS file sized to the output, styled from the caption tokens, burned in; fails when the caption font fell back | 0 · 1 · 2 |
| `loudness measure` | `FILE` | integrated LUFS, true peak and range | 0 · 2 |
| `loudness normalise` | `FILE --target social\|podcast\|acx [-o OUT]` | two-pass `loudnorm` with `-ar`, then re-measured | 0 · 1 · 2 |
| `audiobook text` | `SOURCE --piece PIECE --chapter chNN [--footnotes drop\|inline] [--limit CHARS]` | chapter text with syntek-author's markup stripped and pronunciations applied, every unspoken word listed, chunked into the audiobook's generated folder; a chunk ends at every pause, recorded in the chapter's `<piece>.chNN.chunks.toml` | 0 · 1 · 2 |
| `audiobook master` | `CHUNKS… --piece PIECE --chapter chNN [--head S] [--tail S] [-o OUT]` | joins takes with the pauses the chunk sidecar records, adds room tone, masters to the ACX profile | 0 · 1 · 2 |
| `audiobook check` | `FILE…` | the ACX checks: RMS, peak, noise floor, sample rate, constant bitrate, channels, length, room tone | 0 · 1 · 2 |
| `take add` | `FILE --piece PIECE (--segment sNN \| --chapter chNN --part pNN)` | renames a fresh ElevenLabs file to its name (`.pcm` for a `pcm_*` format), writes the register's `take` and `file`, appends the credits-log row | 0 · 2 |
| `footage add` | `FILE --kind KIND --location LABEL [--rights RRNNNN]` | copies a file into the mirror (never moves it), hashes and probes it, appends the next `F` ID; refuses a duplicate | 0 · 2 |
| `footage verify` | `[--manifest PATH]` | the local mirror against the manifest | 0 · 1 · 2 |
| `tokens` | `[--tokens PATH]` | every required custom property present and parseable | 0 · 1 · 2 |
| `flags` | `[PATH…] [--piece PIECE] [--strict]` | both flags, in every form, over the files Git tracks or would track; `--piece` gathers one piece's files across the scripts, production and publishing layers | 0 · 1 · 2 |
| `check` | `[--strict] [--setup]` | the large-file and Git LFS guard and the nested ignore rules; `--setup` adds the readiness report | 0 · 1 · 2 |
| `--self-test` | — | fixtures written at run time; exercises every module; probes that need ffmpeg skip by name | 0 · 1 · 2 |

**`toolkit/card.py`** (`uv run toolkit/card.py …`):
`render HTML (--deliverable KEY | --size WxH) [--transparent] [-o OUT]` renders a layout to PNG
in Chromium, offline, with the safe-zone variables set; `check HTML` proves the tokens resolve
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
  unless `-o` names the path, and nothing outside those folders is overwritten. The caption
  commands that make tracked files (`align`, `retime`, `rewrap`, `vtt`) write to standard output
  unless `-o` names the file, so always pass `-o` for a caption file.
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
| `pandoc` (optional) | cleaner chapter text in `audiobook text`, which works without it |
| `espeak-ng` (optional) | a scratch voice track for timing, labelled approximate |

`python3 toolkit/media.py check --setup` reports every one of them, the allow, ask and deny
entries of `.claude/settings.json`, and whether the ElevenLabs server's base path contains the
project (`brand/workflows/06-check-the-setup/`). If a tool is missing, say which one and which
command it blocks. Never report a command as passed when it could not run.
