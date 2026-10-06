#!/usr/bin/env bash
#
# toolkit-smoke.sh — Run the toolkit's commands in every render, on synthetic media, and require them to work.
#
#                    Every production skill routes to one command: `python3 toolkit/media.py …`
#                    for masters, cuts, captions, loudness, the audiobook and the repository guard,
#                    and `uv run toolkit/card.py …` for thumbnails and cards (DESIGN.md Section
#                    4.2). Nothing in the template's own repository ever runs them against a
#                    rendered project: a preset that no longer matches what ffmpeg writes, a burn
#                    that loses the caption font, a nested ignore rule that lets renders into Git,
#                    an LFS rule that stores footage as a plain blob — each ships silently and
#                    fails on the author's first deliverable. So each render is copied to a
#                    scratch folder, made a Git repository, and its toolkit is run for real on
#                    clips, tones and stills generated at run time (ffmpeg -f lavfi). Never an
#                    ElevenLabs call: a "take" is a tone or a few fake bytes, and the toolkit's
#                    handling of the files around a call is what is proved (credits).
#
#                    Twenty-six checks, per render: 1–26. Numbers 27–28 are
#                    DESIGN.md Section 7's for commands the toolkit does not have yet, and are
#                    taken when they arrive (24 then gains `real` beside `where` and `cues`).
#                      1. Every toolkit/*.py that offers `--self-test` passes it (media.py, which
#                         exercises the media_*.py modules, card.py and transcribe.py). A self-test reads only
#                         the toolkit, so one result serves every render whose toolkit/ is
#                         byte-identical (it says so). card.py's exit 2 with its own SKIP lines
#                         (no Playwright, Chromium or fc-match) is a named SKIP in its words, and
#                         is carried to every such render as a SKIP, never as a pass.
#                      2. `cut` on a synthetic clip, for every video and audio deliverable of the
#                         platforms in the answers (and audiobook.acx, the retail sample, where
#                         the project makes audiobooks), writes what the preset says: size, codecs,
#                         yuv420p, sample rate, sound only for audio, no sound track where the
#                         table sets audio_tracks = 0, and the length cut. The website.* and
#                         blog.* video keys and podcast.feed_audio are among them.
#                      3. `captions burn` onto a cut succeeds at the preset size with an ASS whose
#                         PlayResX/PlayResY is that size; with the caption font made one that is
#                         not installed, the burn fails and says the font fell back.
#                      4. `card.py render` writes a PNG at each image deliverable's preset size,
#                         and `--transparent` keeps alpha (SKIP by name without uv or Chromium,
#                         or with --skip-thumbnails). A GIF table is check 16's.
#                      5. `loudness normalise` lands within ±1 LU of the social target ([house])
#                         and the podcast target ([platform.podcast.apple_rss_audio]), measured
#                         independently with ffmpeg's ebur128.
#                      6. `audiobook master` then `audiobook check` passes on a synthetic
#                         chapter, and a hot-peak copy of the master fails the check.
#                      7. The toolkit's own validators fail their mutations: a wrong aspect (a
#                         burn onto an uncut 640x360 clip), an over-long cut (fails before it
#                         renders), a 43-character caption line and 20 characters a second —
#                         while a clean SRT passes, so the failures mean something.
#                      8. In the Git copy: `git check-ignore` succeeds for a sample output in
#                         every generated/, renders/ and raw/ folder and in toolkit/__pycache__/,
#                         and in a piece's own folders (D64: a take in generated/<piece>/takes/,
#                         a master, a card render and a timing working copy in renders/<piece>/,
#                         a deliverable in publishing/src/renders/<piece>/), and fails for each
#                         folder's README.md and for a piece's tracked files in production/src/
#                         timing/ and production/src/scenes/; `git check-attr filter` reports
#                         `lfs` under brand/src/exports/large/ and not for its pair; `media.py
#                         check` is clean on the fresh copy, then flags a plain-blob LFS file, and
#                         flags an LFS-marked file when a fake git-lfs on PATH prints a version but
#                         no filter.lfs.* is configured; with the tripwire of copier.yml applied
#                         (DESIGN.md D19), `git add` of that file fails.
#                      9. A synthetic edit decision list end to end: a lavfi clip, a still with
#                         push-in, a colour clip, one card as a clip and as an overlay at one size
#                         (cards SKIP by name without Chromium), a fade, a voiceover register of
#                         two tone segments each carrying several cues, one take flat in
#                         generated/ where an earlier release left it and one in the piece's
#                         takes/ (D65), and a ducked music bed trimmed and faded — `assemble`
#                         (the master in production/src/renders/<piece>/ by default, both card
#                         renders kept in its cards/, the overlay's named .transparent, D47, D64;
#                         length and social loudness), `cut` for every video
#                         deliverable in the answers, `captions from-segments` (cue times exact at
#                         the offset, at the segment join and at the last segment's end) and
#                         `retime` to a cut, then `burn` onto that cut.
#                     10. An audio master (`size = ""`) cut from clips of an audio-only source,
#                         under a faded bed, probes as sound only at the expected length.
#                     11. `script time` on a fixture script reports its total; `footage add`
#                         copies (never moves) and refuses a duplicate hash; `footage verify`
#                         passes, then fails on a changed byte; `take add` renames a fake .mp3
#                         take and a fake pcm_* take (to .pcm) in the piece's own takes/ folder,
#                         writes their register rows naming that path and their credits-log rows,
#                         and numbers the .mp3 take t2 after a flat t1 an earlier release left in
#                         generated/, which it leaves where it was (D64, D65).
#                     12. `audiobook text` on a chapter in syntek-author's markup strips section
#                         markers, comments, citation keys, divs and spans, ends a chunk at the
#                         scene break with 2 s recorded in the sidecar and never in the text
#                         (ruling T3), and lists the unpronounced constructed word (exit 1).
#                         Where the project makes no audiobooks there is no audiobook folder: n/a.
#                     13. `captions align --lines` places every cue of a synthetic cut, and
#                         `--anchors` keeps every cue of a beat inside that beat.
#                     14. `check --setup`, with HOME pointed at a scratch folder holding a fixture
#                         ~/.claude.json, reports a missing ask rule and a base path outside the
#                         repository, prints no other value from that file, and names the optional
#                         encoders `image` needs (libwebp; an AV1 encoder and the avif muxer).
#                     15. `image` encodes a PNG into each format of every image deliverable in the
#                         answers, at its size (jpg, png, webp, avif; an encoder this ffmpeg lacks
#                         is a SKIP by name), flattening alpha where the table says alpha = false;
#                         refuses a source of another shape without --frame; takes a poster from a
#                         video at --at; and fails its verification when max_size is overridden to
#                         1 KB (DESIGN.md D57).
#                     16. `cut` to newsletter.preview_gif with an --overlay PNG writes a GIF at the
#                         preset size, within fps_max and max_size, the overlay on its first frame,
#                         playing floor(max_seconds / clip) times — read from its own loop
#                         extension (plays = count + 1, or once with none) and frame delays — so
#                         it stops within max_seconds; a 3-second range plays once; over max_size
#                         it is remade with fewer frames and its play time unchanged; an overlay
#                         of another size is exit 2; a range longer than max_seconds renders
#                         nothing (exit 1). Where the answers have no GIF table: n/a.
#                     17. A table with audio_tracks = 0 (website.hero_loop) is cut with no sound
#                         track, and with an ffmpeg that maps the source's sound in place of -an
#                         the toolkit's own verification fails the file; website.video is encoded with its index
#                         (moov) at the front. Where the answers have neither: n/a.
#                     18. The podcast feed end to end on a fixture show, offline (D58, D59): the
#                         skeleton fenced in publishing/src/podcast/CLAUDE.md equals
#                         media_feed.SKELETON, flags and computed values aside; `feed new`
#                         refuses a project without that folder (exit 2, naming the update),
#                         reproduces the Podcasting 2.0 specification's published podcast:guid
#                         example and flags owner_email; `feed add` writes the episode guid as
#                         the UUIDv5 of the piece; `encode --deliverable podcast.feed_audio`
#                         from a picture master in its piece's renders folder, with no -o, is
#                         sound only, untagged, at the podcast target, and lands in
#                         publishing/src/renders/<piece>/, the one path feed tag reads (D64);
#                         `feed tag` refuses an empty title changing nothing, then writes
#                         ID3v2.3 title, author, album, three chapters and the cover, leaving the
#                         audio stream as it was and the row's render, bytes and seconds true;
#                         `feed write` needs --as-of (exit 2), gives the same bytes twice and a
#                         feed with every required tag; `--rekey` recomputes every GUID before
#                         publication and is exit 2 after; `feed write -o` writes and then
#                         replaces the tracked feed; `feed chapters` writes version 1.2 JSON;
#                         `feed check` passes, then exits 1 on each mutation (a repeated GUID, a
#                         GUID of the previous feed with no row, a changed enclosure length under
#                         the same URL, a < in a title, bytes that differ from the render, a
#                         flag left), and `feed write -o` then refuses to replace a tracked feed
#                         holding a GUID with no row. Where the render has no podcast folder only
#                         the refusal runs, and the rest is n/a.
#                     19. `captions transcript` on a fixture script keeps the spoken words, gives
#                         on-screen text as [On screen: …], drops a lone speaker's tags, NOTE:
#                         cues, braced directions and every raw cue line, takes only the given
#                         lines with --lines, and writes a file only with -o (D60).
#                     20. Offline speak plans create only takes or trial folders and print characters
#                         and calls, never credits; a re-roll numbers across both layouts and clears
#                         approval and archive. The voice join is mono 16-bit in register order with
#                         pauses, refuses unapproved segments, and levels are finite working JSON only.
#                     21. Rhubarb gets plain dialogue and all nine native shapes; resources resolve
#                         beside the linked executable, fatal errors exit 2, soundFile is relative,
#                         and tracked mouth files refuse edits made before or during recognition.
#                         The real recogniser runs on an espeak-ng voice, or SKIPs by name.
#                     22. Stdlib word-alignment fixtures reject unsafe text, compare word sequences,
#                         map respelling parts, report empty segments and heard-word disagreements,
#                         and make captions at word boundaries. A prepared user interpreter aligns
#                         an espeak-ng fixture; otherwise that live part SKIPs by name. Never fetches
#                         weights, installs WhisperX or invokes uv on transcribe.py.
#                     23. The D66 writer replaces a committed clean named timing copy atomically;
#                         dirty, staged, untracked and outside-Git copies, and unrelated files,
#                         are refused without changing their bytes.
#                     26. Missing WhisperX is an optional setup note naming transcribe fetch;
#                         absent Rhubarb is a note naming lipsync, but an executable whose version
#                         succeeds without its dictionary is broken and reports a finding.
#                     24. `where` on a fixture piece prints its files Git tracks or would track
#                         across scripts/, production/ and publishing/, its timing file among
#                         them, names its three ignored per-piece folders, each existing or
#                         absent, and never names anything inside them (D50, D64); a name with
#                         no piece folder is exit 2.
#                         `cues` retains separate word/line/beat/board lists, exact seconds and
#                         enclosing MM:SS, delivery anchors and SFX/music audio links; unmatched
#                         rows and links are findings, invalid data and author edits are refused.
#                     25. 25 flat stills of 0.16 s at 30 fps (DESIGN.md Section 6.4): the master
#                         is 120 frames, the frame nearest the edit's 4.000 s (still by still,
#                         125), each still starting on the frame nearest its running total, read
#                         from every frame's colour; an overlay with alpha from the fourth still's
#                         start until a later boundary is on that still's first frame and off the
#                         frame `until` falls on; `encode` of that master, its tone running past
#                         the picture, to the first video deliverable with sound that 4 s fits,
#                         passes its own checks and ends its sound with its picture (within half
#                         a frame). With no such deliverable the encode is n/a.
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    A check whose tool is absent is SKIPPED and named (SKIP — …), never passed:
#                    no ffmpeg (checks 2, 3, 5–7, 9, 10, 13, 15–18, 25), no uv or Chromium (check 4, card.py's
#                    self-test, the cards of check 9), no fc-match (card.py's brand-font probe).
#                    --require-ffmpeg (CI) turns a missing ffmpeg into exit 2; --skip-thumbnails
#                    skips the Chromium steps by name. A step that does not apply to a render (no
#                    audiobook folder, no deliverable short enough to over-run, no podcast folder,
#                    no own-channel deliverable) is listed as n/a, not as a SKIP.
#
#                    What it CANNOT check: that a render LOOKS right — only that it is made to
#                    the preset; a person watches the master. Nor ElevenLabs itself, which is
#                    never called. The self-test proves the judging of every check; the driver
#                    that runs the commands is proved by the real run, which names every step it
#                    could not run.
#
# SELF-TEST. --self-test writes a results file at run time — what a clean smoke of a fixture
#            render records — proves it clean, then changes one recorded fact per probe and
#            asserts exactly one finding each. It needs no ffmpeg, uv or Chromium.
#
# Requirements: bash 4.3+, git, python3 ≥ 3.11; ffmpeg and ffprobe (libass, libx264, libmp3lame)
#               for most checks; uv and Playwright's Chromium for card.py. No network, unless uv
#               must fetch card.py's pinned Playwright on its first run.
#
# Usage: toolkit-smoke.sh [--require-ffmpeg] [--skip-thumbnails] [--quiet] [--self-test] [--help] <tree>...
#
# Exit codes:  0 = every step that could run, ran and was made to its preset
#              1 = finding(s), or the self-test no longer separates
#              2 = script error (bad arguments, no python3 or git, --require-ffmpeg without it)

set -euo pipefail
SCRIPT_NAME="toolkit-smoke.sh"
# shellcheck source=_common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

SELF_TEST=false
REQUIRE_FFMPEG=false
SKIP_THUMBS=false
TARGETS=()

usage() {
  cat <<'EOF'
toolkit-smoke.sh — Run the toolkit's commands in every render, on synthetic media

Usage: toolkit-smoke.sh [--require-ffmpeg] [--skip-thumbnails] [--quiet] [--self-test] [--help] <tree>...

  --require-ffmpeg   Treat a missing ffmpeg or ffprobe as an error (CI)
  --skip-thumbnails  Skip every Chromium step (card.py) by name
  --quiet            Print findings only (SKIP lines are always printed)
  --self-test        Prove the checks still fire against a results file written at runtime
  --help             Show this message

Renders are copied before anything runs; the trees given are never written to.
Exit codes: 0 = clean  1 = finding(s), or the self-test no longer separates
            2 = script error
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-ffmpeg)  REQUIRE_FFMPEG=true; shift ;;
    --skip-thumbnails) SKIP_THUMBS=true; shift ;;
    --quiet|-q)        QUIET=true; shift ;;
    --self-test)       SELF_TEST=true; shift ;;
    --help|-h)         usage; exit 0 ;;
    -*)                die "unknown argument: $1" ;;
    *)                 TARGETS+=("$1"); shift ;;
  esac
done

HAVE_FFMPEG=false; command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1 && HAVE_FFMPEG=true
HAVE_UV=false; command -v uv >/dev/null 2>&1 && HAVE_UV=true
HAVE_CHROMIUM=unknown

# The names the smoke's fixtures use: invented, numbered past any real piece.
P_EDIT="903-smoke-edit"; P_AUDIO="904-smoke-audio"; P_TAKE="905-smoke-take"; P_PCM="906-smoke-take-pcm"
P_SCRIPT="907-smoke-script"; P_BOOK="908-smoke-book"; P_ALIGN="909-smoke-align"; P_TRANSCRIPT="913-smoke-transcript"
P_WHERE="914-smoke-where"; P_FRAMES="915-smoke-frames"
CONSTRUCTED="velunar"
SECRET="smoke-secret-value-never-printed"
SECRET_MAIL="robin@example.com"
GONE_ASK="mcp__elevenlabs__voice_clone"

NAME=""; W=""; T=""; OUT=""; GHOME=""; RESULTS=""; TRIPWIRE=""
declare -A RES=()
declare -A SELFTEST_CACHE=() SELFTEST_TAIL=()

# ── Recording ─────────────────────────────────────────────────────────────────

rec() { printf '%s\t%s\n' "$1" "$2" >> "$RESULTS"; }

load_results() { # $1 = results file → RES
  local k v
  RES=()
  while IFS=$'\t' read -r k v; do
    if [[ -n "$k" ]]; then RES["$k"]="$v"; fi
  done < "$1"
  return 0
}

tgit() { # git in the scratch copy, with a scratch HOME and no system config: no filter leaks in
  HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 git -C "$T" -c user.name='syntek-media audit' \
    -c user.email='audit@example.com' -c commit.gpgsign=false "$@"
}

tk() { # $1 = log name, then media.py arguments — returns its exit status, never stops the smoke
  local name="$1" st=0; shift
  (cd "$T" && PYTHONDONTWRITEBYTECODE=1 python3 toolkit/media.py "$@") >"$OUT/$name.log" 2>&1 || st=$?
  return "$st"
}

tko() { # $1 = name, then media.py arguments — standard output to OUT/name.out, messages to OUT/name.log
  local name="$1" st=0; shift
  (cd "$T" && PYTHONDONTWRITEBYTECODE=1 python3 toolkit/media.py "$@") >"$OUT/$name.out" 2>"$OUT/$name.log" || st=$?
  return "$st"
}

tkc() { # $1 = log name, then card.py arguments
  local name="$1" st=0; shift
  (cd "$T" && PYTHONDONTWRITEBYTECODE=1 uv run --quiet toolkit/card.py "$@") >"$OUT/$name.log" 2>&1 || st=$?
  return "$st"
}

said() { # $1 = log name, $2 = an extended regex → yes | no
  if grep -qiE -- "$2" "$OUT/$1.log" 2>/dev/null; then echo yes; else echo no; fi
}

tail_of() { grep -v '^[[:space:]]*$' "$OUT/$1.log" 2>/dev/null | tail -1 | cut -c1-110 || true; }
# A self-test's failing cases (its FAIL lines, up to three) before its last line, so a failure that
# happens only on a CI runner, whose scratch folder is gone when the job ends, can be read in the log.
selftest_tail() {
  local f; f="$(grep -E '(^|[[:space:]])FAIL[[:space:]]' "$OUT/$1.log" 2>/dev/null | head -3 | sed 's/^[[:space:]]*//' | tr '\n' ' ' | cut -c1-400 || true)"
  printf '%s%s' "${f:+$f— }" "$(tail_of "$1")"
}

printed() { # $1 = name (tko), $2 = an extended regex, case-sensitive, on standard output only → yes | no
  if grep -qE -- "$2" "$OUT/$1.out" 2>/dev/null; then echo yes; else echo no; fi
}

# ── Media, generated at run time ─────────────────────────────────────────────

ff() { ffmpeg -v error -y "$@"; }
gen_av() { # $1 = out, $2 = seconds, $3 = WxH: a picture with a tone under it
  ff -f lavfi -i "testsrc2=size=$3:rate=30:duration=$2" -f lavfi -i "sine=frequency=440:sample_rate=48000:duration=$2" \
    -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -ac 2 -shortest "$1"
}
gen_tone() { # $1 = out, $2 = seconds, $3 = rate, $4 = channels, $5 = volume, then codec arguments
  local out="$1" s="$2" r="$3" c="$4" v="$5"; shift 5
  ff -f lavfi -i "sine=frequency=330:sample_rate=$r:duration=$s,volume=$v" -ac "$c" "$@" "$out"
}
gen_still() { ff -f lavfi -i "testsrc2=size=$2:rate=1:duration=1" -frames:v 1 "$1"; }

# "w h vcodec pix acodec rate channels duration" — "-" for an absent field.
probe_facts() {
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,pix_fmt,sample_rate,channels:format=duration \
    -of json "$1" 2>/dev/null | python3 -c '
import json, sys
try: d = json.load(sys.stdin)
except Exception: print("- - - - - - - 0"); sys.exit()
v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), {})
f = lambda x: str(x) if x not in (None, "") else "-"
print(f(v.get("width")), f(v.get("height")), f(v.get("codec_name")), f(v.get("pix_fmt")), f(a.get("codec_name")),
      f(a.get("sample_rate")), f(a.get("channels")), "%.3f" % float(d.get("format", {}).get("duration") or 0))'
}

lufs() { # integrated loudness, measured by ffmpeg's ebur128 — never by the toolkit under test
  ffmpeg -hide_banner -nostats -i "$1" -af ebur128 -f null - 2>&1 | awk '/^[[:space:]]+I:/ { v = $2 } END { print (v == "" ? "nan" : v) }'
}

png_facts() { # "w h colortype alphamin" of a PNG
  local wh ct amin=255
  read -r wh ct < <(python3 -c '
import struct, sys
b = open(sys.argv[1], "rb").read(32)
if b[:8] != b"\x89PNG\r\n\x1a\n": print("0x0 0"); sys.exit()
w, h, _, c = struct.unpack(">IIBB", b[16:26]); print(f"{w}x{h} {c}")' "$1" 2>/dev/null || echo "0x0 0")
  if [[ "$ct" == 6 || "$ct" == 4 ]] && $HAVE_FFMPEG; then
    amin="$(ffmpeg -hide_banner -nostats -i "$1" -vf alphaextract,signalstats,metadata=print:key=lavfi.signalstats.YMIN \
      -f null - 2>&1 | grep -o 'YMIN=[0-9]*' | head -1 | cut -d= -f2)"
  fi
  printf '%s %s %s\n' "$wh" "$ct" "${amin:-255}"
}

srt_times() { # "start end" per cue, in seconds
  python3 -c '
import re, sys
t = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else ""
for a, b in re.findall(r"(\d+:\d\d:\d\d[,.]\d{3}) --> (\d+:\d\d:\d\d[,.]\d{3})", t):
    s = lambda x: sum(float(p) * m for p, m in zip(x.replace(",", ".").split(":"), (3600, 60, 1)))
    print("%.3f %.3f" % (s(a), s(b)))' "$1" 2>/dev/null || true
}

# Every deliverable table, the brand's overrides applied: key kind w h vcodec acodec rate min max
# aspect formats audio_tracks ("-" for an absent field; formats comma-joined).
tables() {
  python3 - "$T/toolkit/data/platforms.toml" "$T/brand/src/platforms/overrides.toml" <<'PY'
import sys, tomllib
try: data = tomllib.load(open(sys.argv[1], "rb"))
except Exception: sys.exit(0)
rows = {}
def walk(prefix, t):
    for k, v in t.items():
        if isinstance(v, dict) and "kind" in v: rows[prefix + k] = dict(v)
        elif isinstance(v, dict): walk(prefix + k + ".", v)
walk("", data.get("platform", {})); walk("audiobook.", data.get("audiobook", {}))
try:
    for o in tomllib.load(open(sys.argv[2], "rb")).get("override", []):
        key, field = str(o.get("key", "")).rsplit(".", 1)
        if key in rows: rows[key][field] = o.get("value")
except Exception: pass
g = lambda v, f: (",".join(map(str, v[f])) if isinstance(v.get(f), list) else str(v.get(f))) if v.get(f) not in (None, "", []) else "-"
for k, v in rows.items():
    print("\t".join([k, g(v, "kind"), g(v, "width"), g(v, "height"), g(v, "video_codec"), g(v, "audio_codec"),
                     g(v, "audio_sample_rate"), g(v, "min_seconds"), g(v, "max_seconds"), g(v, "aspect"),
                     g(v, "formats"), g(v, "audio_tracks")]))
PY
}

# One field of one deliverable table, the brand's overrides applied ("-" when absent; a list
# comma-joined; a boolean as true or false).
tfield() { # $1 = key, $2 = field
  python3 - "$T/toolkit/data/platforms.toml" "$T/brand/src/platforms/overrides.toml" "$1" "$2" <<'PY'
import sys, tomllib
try: data = tomllib.load(open(sys.argv[1], "rb"))
except Exception: print("-"); sys.exit(0)
key, field = sys.argv[3], sys.argv[4]
t = data.get("audiobook", {}) if key.startswith("audiobook.") else data.get("platform", {})
for p in (key.split(".", 1)[1] if key.startswith("audiobook.") else key).split("."):
    t = t.get(p, {}) if isinstance(t, dict) else {}
v = t.get(field) if isinstance(t, dict) else None
try:
    for o in tomllib.load(open(sys.argv[2], "rb")).get("override", []):
        if o.get("key") == f"{key}.{field}": v = o.get("value")
except Exception: pass
if v is None or v == "": print("-")
elif isinstance(v, bool): print("true" if v else "false")
elif isinstance(v, list): print(",".join(map(str, v)))
else: print(v)
PY
}

# A brand override of one field, appended to the scratch copy's overrides.toml (the caller
# restores the file): how a mutation changes a limit without touching platforms.toml.
override() { # $1 = key.field, $2 = a TOML value
  printf '\n[[override]]\nkey = "%s"\nvalue = %s\nwhy = "toolkit-smoke mutation"\nsource = "toolkit-smoke"\nchecked = "01/01/2027"\n' \
    "$1" "$2" >> "$T/brand/src/platforms/overrides.toml"
}

toml_value() { # $1 = TOML file, $2 = dotted table, $3 = key
  python3 - "$1" "$2" "$3" <<'PY'
import sys, tomllib
try:
    d = tomllib.load(open(sys.argv[1], "rb"))
    for p in sys.argv[2].split("."): d = d[p]
    print(d[sys.argv[3]])
except Exception: print("nan")
PY
}

# ── The driver: runs every step in a scratch copy and records what happened ───

skip_step() { # $1 = key, $2 = what, $3 = why — a named SKIP: the tool to look was absent
  rec "skip.$1" "$2 ($3)"
  skip_named "toolkit-smoke check $1 [$NAME] — $2" "$3"
}
na_step() { rec "na.$1" "$2"; }   # does not apply to this render: listed, never a SKIP

# card.py --self-test exits 2, its last line 'self-test incomplete', when a part of it could not
# run (Playwright, its Chromium or fc-match absent), each part named on a SKIP line with why. That
# is a named SKIP here, in card.py's own words: never a pass, never a finding. Any other exit, a
# FAIL beside a SKIP (exit 1) among them, is judged as it stands.
card_skips() { # $1 = exit status, $2 = log → card.py's reasons on one line, or nothing
  [[ "$1" == 2 ]] && grep -q '^self-test incomplete' "$2" 2>/dev/null || return 0
  grep -E '^[[:space:]]+SKIP[[:space:]]' "$2" | sed -E 's/^[[:space:]]+SKIP[[:space:]]+//' | head -3 \
    | paste -sd '|' - | sed 's/|/; /g' | cut -c1-300 || true
}

smoke() { # $1 = tree — fills $RESULTS
  local src="$1" k kind w h vc ac rate min max asp st f out hash first_v="" first_land="" short_k="" short_max=999999
  local -a answered=() videos=() images=()
  W="$(sm_mktemp)"; T="$W/tree"; OUT="$W/out"; GHOME="$W/home"; RESULTS="$W/results.tsv"
  mkdir -p "$OUT" "$GHOME" "$W/shim" "$W/fakebin"; : > "$RESULTS"
  cp -a "$src" "$T"
  [[ -d "$T/.git" ]] || tgit init -q
  tgit add -A >/dev/null 2>&1 || true
  tgit commit -q -m 'toolkit-smoke: the render' >/dev/null 2>&1 || true

  if ! load_answers "$T/$SM_ANSWERS_FILE"; then rec answers missing; return 0; fi
  rec answers ok
  [[ -f "$T/toolkit/media.py" ]] || { rec selftest.media.py missing; return 0; }

  # ── 1. Self-tests (cached by the toolkit's bytes) ──
  hash="$( (cd "$T/toolkit" && find . -type f ! -path '*/__pycache__/*' -print0 | LC_ALL=C sort -z | xargs -0 sha1sum) | sha1sum | cut -c1-12)"
  if [[ -n "${SELFTEST_CACHE[$hash]:-}" ]]; then
    # A skip is carried like a result, so every render with this toolkit names it.
    while IFS='=' read -r k st; do
      [[ -n "$k" ]] || continue
      if [[ "$st" == skip ]]; then skip_step 1 "$k --self-test" "${SELFTEST_TAIL[$hash/$k]:-}"
      else rec "selftest.$k" "$st"; rec "selftest.$k.tail" "${SELFTEST_TAIL[$hash/$k]:-}"; fi
    done < <(printf '%s\n' "${SELFTEST_CACHE[$hash]}" | tr ';' '\n')
    rec selftest.reused "$hash"
  else
    local cache="" why
    for f in "$T"/toolkit/*.py; do
      grep -q -- '--self-test' "$f" && grep -q '__main__' "$f" || continue
      k="${f##*/}"; st=0; why=""
      if [[ "$k" == card.py ]]; then
        if ! $HAVE_UV; then why="uv is not installed"
        else
          tkc "selftest.$k" --self-test || st=$?
          why="$(card_skips "$st" "$OUT/selftest.$k.log")"
        fi
      else
        (cd "$T" && PYTHONDONTWRITEBYTECODE=1 python3 "toolkit/$k" --self-test) \
          >"$OUT/selftest.$k.log" 2>&1 || st=$?
      fi
      if [[ -n "$why" ]]; then
        skip_step 1 "$k --self-test" "$why"; cache+="$k=skip;"; SELFTEST_TAIL["$hash/$k"]="$why"; continue
      fi
      rec "selftest.$k" "$st"; rec "selftest.$k.tail" "$(selftest_tail "selftest.$k")"
      cache+="$k=$st;"; SELFTEST_TAIL["$hash/$k"]="$(selftest_tail "selftest.$k")"
    done
    SELFTEST_CACHE[$hash]="$cache"
  fi

  # The deliverables this render's answers ask for.
  local fmts atr
  while IFS=$'\t' read -r k kind w h vc ac rate min max asp fmts atr; do
    [[ -z "$k" ]] && continue
    if [[ "$k" == audiobook.* ]]; then
      [[ "$k" == audiobook.acx && " $A_KINDS " == *" audiobook "* ]] || continue
    else
      [[ " $A_PLATFORMS " == *" ${k%%.*} "* ]] || continue
    fi
    # A table with audio_tracks = 0 (website.hero_loop) is cut with no sound track (D57).
    [[ "$atr" == 0 ]] && { ac=none; rate=-; }
    answered+=("$k"$'\t'"$kind"$'\t'"$w"$'\t'"$h"$'\t'"$vc"$'\t'"$ac"$'\t'"$rate"$'\t'"$min"$'\t'"$max"$'\t'"$asp"$'\t'"$fmts"$'\t'"$atr")
    if [[ "$kind" == video ]]; then
      videos+=("$k"); [[ -z "$first_v" ]] && first_v="$k"
      [[ -z "$first_land" && "$asp" == 16:9 ]] && first_land="$k"
      if [[ "$max" != - ]] && awk -v a="$max" -v b="$short_max" 'BEGIN { exit !(a < b) }'; then short_k="$k"; short_max="$max"; fi
    fi
    # A GIF table (formats = ["gif"]) is check 16's: cut makes it, never card.py alone.
    [[ "$kind" == image && "$w" != - && "$fmts" != gif ]] && images+=("$k $w $h")
  done < <(tables)
  rec deliverables "${#answered[@]}"
  rec first_video "${first_v:--}"

  if ! $HAVE_FFMPEG; then
    for k in 2 3 5 6 7 9 10 13 15 16 17 18; do skip_step "$k" "every ffmpeg step" "ffmpeg or ffprobe is not installed"; done
  else
    gen_av "$OUT/src.mp4" 5 640x360

    # ── 2. cut, per deliverable ──
    local row
    for row in "${answered[@]}"; do
      IFS=$'\t' read -r k kind w h vc ac rate min max asp fmts atr <<< "$row"
      [[ "$kind" == video || "$kind" == audio ]] || continue
      if [[ "$kind" == video ]]; then out="$OUT/c2.$k.mp4"
      else case "$ac" in mp3) out="$OUT/c2.$k.mp3" ;; flac) out="$OUT/c2.$k.flac" ;; wav|pcm*) out="$OUT/c2.$k.wav" ;; *) out="$OUT/c2.$k.m4a" ;; esac; fi
      st=0; tk "cut.$k" cut "$OUT/src.mp4" --deliverable "$k" --in 00:00:00.000 --out 00:00:04.000 -o "$out" || st=$?
      rec "cut.$k.status" "$st"; rec "cut.$k.tail" "$(tail_of "cut.$k")"
      rec "cut.$k.want" "$kind $w $h $vc $ac $rate 4.000"
      [[ -f "$out" ]] && rec "cut.$k.facts" "$(probe_facts "$out")"
    done

    # ── 3. burn onto a cut; a missing caption font ──
    if [[ -n "$first_v" && -f "$OUT/c2.$first_v.mp4" ]]; then
      printf '1\n00:00:00,200 --> 00:00:01,600\nThe ferry is late again.\n\n2\n00:00:01,800 --> 00:00:03,400\nIt waits for the tide.\n' > "$OUT/burn.srt"
      cat > "$W/shim/ffmpeg" <<SHIM
#!/bin/sh
[ -f captions.ass ] && cp captions.ass "$OUT/burn.ass" 2>/dev/null
exec $(command -v ffmpeg) "\$@"
SHIM
      chmod 755 "$W/shim/ffmpeg"
      st=0; PATH="$W/shim:$PATH" tk burn captions burn "$OUT/c2.$first_v.mp4" "$OUT/burn.srt" --deliverable "$first_v" -o "$OUT/c3.burned.mp4" || st=$?
      rec burn.key "$first_v"; rec burn.status "$st"; rec burn.tail "$(tail_of burn)"
      read -r w h _ <<< "$(probe_facts "$OUT/c3.burned.mp4")"; rec burn.size "${w}x${h}"
      rec burn.want "$(awk -F'\t' -v k="$first_v" '$1 == k { print $3 "x" $4 }' < <(printf '%s\n' "${answered[@]}"))"
      rec burn.playres "$(awk -F': *' '/^PlayResX/ { x = $2 } /^PlayResY/ { y = $2 } END { print (x == "" ? "none" : x "x" y) }' "$OUT/burn.ass" 2>/dev/null || echo none)"
      cp "$T/brand/src/design-system/tokens.css" "$W/tokens.held"
      sed -i -E 's/(--caption-font:)[^;]*;/\1 "Smoke Missing Face";/' "$T/brand/src/design-system/tokens.css"
      st=0; tk font captions burn "$OUT/c2.$first_v.mp4" "$OUT/burn.srt" --deliverable "$first_v" -o "$OUT/c3.nofont.mp4" || st=$?
      cp "$W/tokens.held" "$T/brand/src/design-system/tokens.css"
      rec font.status "$st"; rec font.said "$(said font 'fell back|not found')"
    else
      na_step 3 "no video deliverable in the answers"
    fi

    # ── 5. loudness ──
    gen_tone "$OUT/tone.wav" 6 48000 2 0.1
    rec loud.social.target "$(toml_value "$T/toolkit/data/platforms.toml" house social_loudness_lufs)"
    rec loud.podcast.target "$(toml_value "$T/toolkit/data/platforms.toml" platform.podcast.apple_rss_audio loudness_lufs)"
    for k in social podcast; do
      st=0; tk "loud.$k" loudness normalise "$OUT/tone.wav" --target "$k" -o "$OUT/c5.$k.wav" || st=$?
      rec "loud.$k.status" "$st"; [[ -f "$OUT/c5.$k.wav" ]] && rec "loud.$k.lufs" "$(lufs "$OUT/c5.$k.wav")"
    done

    # ── 6. audiobook master, check, hot peak ──
    # A chapter as a room records it: speech-level tone in phrases over a quiet room (about
    # -78 dB of pink noise), and that room on its own for --room-tone. A pure tone with no room
    # fails ACX by design: master refuses digital silence as room tone (DESIGN D23).
    ff -f lavfi -i "anoisesrc=color=pink:amplitude=0.0006:sample_rate=44100:duration=3" -ac 1 "$OUT/room.wav"
    ff -f lavfi -i "sine=frequency=330:sample_rate=44100:duration=8,volume='0.5*gt(sin(2*PI*0.7*t)+0.2,0)':eval=frame" \
      -f lavfi -i "anoisesrc=color=pink:amplitude=0.0006:sample_rate=44100:duration=8" \
      -filter_complex "[0][1]amix=inputs=2:normalize=0" -ac 1 "$OUT/chapter.wav"
    st=0; tk abmaster audiobook master "$OUT/chapter.wav" --piece "$P_BOOK" --chapter ch01 --room-tone "$OUT/room.wav" \
      -o "$OUT/c6.ch01.mp3" || st=$?
    rec abmaster.status "$st"; rec abmaster.tail "$(tail_of abmaster)"
    if [[ -f "$OUT/c6.ch01.mp3" ]]; then
      st=0; tk abcheck audiobook check "$OUT/c6.ch01.mp3" || st=$?; rec abcheck.status "$st"
      ff -i "$OUT/c6.ch01.mp3" -af volume=14dB -ac 1 -ar 44100 -c:a libmp3lame -b:a 192k "$OUT/c6.hot.mp3"
      st=0; tk abhot audiobook check "$OUT/c6.hot.mp3" || st=$?; rec abhot.status "$st"
    fi

    # ── 7. the toolkit's validators, mutated ──
    printf '1\n00:00:00,500 --> 00:00:02,300\nThe ferry is late again.\n' > "$OUT/clean.srt"
    printf '1\n00:00:00,500 --> 00:00:04,500\nEvery crossing waits on the tide, not time.\n' > "$OUT/line43.srt"
    printf '1\n00:00:00,500 --> 00:00:02,000\nThe ferry is late, the tide ran.\n' > "$OUT/cps20.srt"
    st=0; tk vclean captions check "$OUT/clean.srt" --deliverable "${first_land:-youtube.long}" || st=$?; rec val.clean "$st"
    st=0; tk vline captions check "$OUT/line43.srt" --deliverable "${first_land:-youtube.long}" || st=$?; rec val.line "$st"
    st=0; tk vcps captions check "$OUT/cps20.srt" --deliverable "${first_land:-youtube.long}" || st=$?; rec val.cps "$st"
    if [[ -n "$first_v" ]]; then
      st=0; tk vaspect captions burn "$OUT/src.mp4" "$OUT/clean.srt" --deliverable "$first_v" -o "$OUT/c7.aspect.mp4" || st=$?
      rec val.aspect "$st"; rec val.aspect.said "$(said vaspect 'wants|640x360')"
    else
      na_step 7a "no video deliverable in the answers"
    fi
    if [[ -n "$short_k" ]] && awk -v m="$short_max" 'BEGIN { exit !(m <= 900) }'; then
      local secs; secs="$(awk -v m="$short_max" 'BEGIN { printf "%d", m + 2 }')"
      ff -f lavfi -i "testsrc2=size=160x90:rate=10:duration=$secs" -f lavfi -i "sine=sample_rate=48000:duration=$secs" \
        -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -shortest "$OUT/long.mp4"
      st=0; tk vlong cut "$OUT/long.mp4" --deliverable "$short_k" --in 0 --out "$(awk -v m="$short_max" 'BEGIN { printf "%d", m + 1 }')" -o "$OUT/c7.long.mp4" || st=$?
      rec val.long "$st"; rec val.long.key "$short_k"; rec val.long.rendered "$([[ -f "$OUT/c7.long.mp4" ]] && echo yes || echo no)"
    else
      na_step 7b "no deliverable in the answers with a max_seconds of 15 minutes or less"
    fi
  fi

  # ── 4. card.py ──
  if $SKIP_THUMBS; then skip_step 4 "card renders" "--skip-thumbnails"
  elif ! $HAVE_UV; then skip_step 4 "card renders" "uv is not installed"
  else
    st=0; tkc cardprobe render toolkit/templates/card.html --size 64x64 -o "$OUT/probe.png" || st=$?
    if [[ "$st" -eq 2 ]] && grep -qiE 'playwright install|chromium' "$OUT/cardprobe.log"; then
      HAVE_CHROMIUM=false; skip_step 4 "card renders" "Playwright's Chromium is not installed"
    else
      HAVE_CHROMIUM=true
      for row in "${images[@]}"; do
        read -r k w h <<< "$row"
        st=0; tkc "card.$k" render toolkit/templates/thumbnail.html --deliverable "$k" -o "$OUT/c4.$k.png" || st=$?
        rec "card.$k.status" "$st"; rec "card.$k.want" "${w}x${h}"
        [[ -f "$OUT/c4.$k.png" ]] && rec "card.$k.size" "$(png_facts "$OUT/c4.$k.png" | cut -d' ' -f1)"
      done
      st=0; tkc cardalpha render toolkit/templates/card.html --size 1920x1080 --transparent -o "$OUT/c4.alpha.png" || st=$?
      rec card.alpha.status "$st"
      [[ -f "$OUT/c4.alpha.png" ]] && rec card.alpha.facts "$(png_facts "$OUT/c4.alpha.png")"
    fi
  fi

  # ── 8. Git: ignore rules, LFS attributes, the repository guard, the tripwire ──
  local d missing="" leaked="" hero="brand/src/exports/large/smoke-hero.bin"
  while IFS= read -r d; do
    d="${d#./}"
    tgit check-ignore -q -- "$d/smoke-sample.mp4" || missing+="$d/smoke-sample.mp4 "
    [[ -f "$T/$d/README.md" ]] && tgit check-ignore -q -- "$d/README.md" && leaked+="$d/README.md "
  done < <(cd "$T" && find . -name .git -prune -o -type d \( -name generated -o -name renders -o -name raw \) -print | LC_ALL=C sort)
  tgit check-ignore -q -- toolkit/__pycache__/smoke.cpython.pyc || missing+="toolkit/__pycache__/smoke.cpython.pyc "
  # A piece's output sits in a folder named for it inside its output folder (D64), which the same
  # rules ignore whole; its tracked timing and scene files sit flat beside renders/, never ignored.
  local tracked=""
  for d in "production/src/voiceover/generated/$P_WHERE/takes/$P_WHERE.s01.t1.mp3" \
           "production/src/renders/$P_WHERE/$P_WHERE.master.mp4" \
           "production/src/renders/$P_WHERE/cards/$P_WHERE.title.1920x1080.transparent.png" \
           "production/src/renders/$P_WHERE/timing/$P_WHERE.words.json" \
           "publishing/src/renders/$P_WHERE/$P_WHERE.youtube-long.mp4"; do
    tgit check-ignore -q -- "$d" || missing+="$d "
  done
  for d in "production/src/timing/$P_WHERE.words.json" "production/src/timing/$P_WHERE.mouth.json" \
           "production/src/scenes/$P_WHERE.cues.json" "production/src/scenes/$P_WHERE.scene.py"; do
    tgit check-ignore -q -- "$d" && tracked+="$d "
  done
  rec git.notignored "${missing% }"; rec git.readme.ignored "${leaked% }"; rec git.tracked.ignored "${tracked% }"
  rec git.attr.large "$(tgit check-attr filter -- brand/src/exports/large/smoke.png 2>/dev/null | sed 's/^.*: //')"
  rec git.attr.pair "$(for f in CONTEXT.md CLAUDE.md; do tgit check-attr filter -- "brand/src/exports/large/$f" | sed 's/^.*: //'; done | sort -u | paste -sd' ' -)"
  st=0; HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 tk gitfresh check || st=$?; rec git.fresh "$st"
  tgit config --local --unset-all filter.lfs.required >/dev/null 2>&1 || true
  mkdir -p "$T/brand/src/exports/large"; printf 'not an lfs pointer\n%.0s' 1 2 3 4 > "$T/$hero"
  tgit add -A >/dev/null 2>&1 || true; tgit commit -q -m 'toolkit-smoke: a plain blob' >/dev/null 2>&1 || true
  st=0; HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 tk gitblob check || st=$?
  rec git.blob "$st"; rec git.blob.said "$(said gitblob 'smoke-hero')"
  tgit rm -q --cached -- "$hero" >/dev/null 2>&1 || true; tgit commit -q -m 'toolkit-smoke: untracked again' >/dev/null 2>&1 || true
  printf '#!/bin/sh\necho "git-lfs/3.4.1 (toolkit-smoke fake)"\n' > "$W/fakebin/git-lfs"; chmod 755 "$W/fakebin/git-lfs"
  st=0; HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 PATH="$W/fakebin:$PATH" tk gitfake check || st=$?
  rec git.fake "$st"; rec git.fake.said "$(said gitfake 'smoke-hero')"
  # The tripwire, exactly as copier.yml's copy-time task runs it (DESIGN.md D19).
  if [[ -n "$TRIPWIRE" ]]; then
    (cd "$T" && HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 sh -c "$TRIPWIRE") >"$OUT/tripwire.log" 2>&1 || true
    st=0; tgit add -- "$hero" >"$OUT/tripadd.log" 2>&1 || st=$?; rec git.tripwire.add "$st"
  else
    rec git.tripwire.add none
  fi
  rm -f "$T/$hero"

  # ── 9 and 10. The edit decision list, end to end; an audio master ──
  if $HAVE_FFMPEG; then smoke_edit "${videos[@]}"; fi

  # ── 25. A run of stills on the frame grid; an overlay on a clip boundary; the held sound ──
  if $HAVE_FFMPEG; then smoke_frames "${answered[@]}"; fi

  # ── 11. script time, footage, takes ──
  smoke_repo "$first_v"

  # ── 12. audiobook text ──
  if [[ -d "$T/production/src/audiobook" ]]; then smoke_text
  else na_step 12 "no audiobook folder (MEDIA_KINDS without audiobook)"; fi

  # ── 13. align ──
  if $HAVE_FFMPEG; then smoke_align; fi

  # ── 14. check --setup ──
  smoke_setup

  # ── 15–19. Images, the GIF preview, web video, the podcast feed, transcripts (0.2.0) ──
  if $HAVE_FFMPEG; then
    smoke_image "${answered[@]}"
    smoke_gif "${answered[@]}"
    smoke_web "${answered[@]}"
    smoke_feed
  fi
  smoke_transcript

  # ── 24. where ──
  smoke_where
  smoke_cues
  smoke_timing
  smoke_lipsync
  if $HAVE_FFMPEG; then smoke_voice
  else
    rec skip.20 'the voice tools on tone takes (no ffmpeg or ffprobe)'
    rec skip.23 'the timing guard with voice fixtures (no ffmpeg or ffprobe)'
  fi
}

manifest_id() { # $1 = kind → the first footage ID of that kind
  python3 - "$T/production/src/footage/manifest.toml" "$1" <<'PY'
import sys, tomllib
try: rows = tomllib.load(open(sys.argv[1], "rb")).get("file", [])
except Exception: rows = []
print(next((r["id"] for r in rows if r.get("kind") == sys.argv[2]), "F9999"))
PY
}

smoke_edit() { # $@ = the answered video deliverables
  local st k gen="$T/production/src/voiceover/generated" cards=true expect d1 d2 join last cues first m c miss
  # s01's take sits flat in generated/, where an earlier release left takes, and s02's in the
  # piece's takes/ folder (D64): every reader opens a take by its register row's file (D65).
  mkdir -p "$gen/$P_EDIT/takes" "$T/production/src/assets" "$T/production/src/cards" "$T/production/src/edits"
  gen_av "$OUT/clip.mp4" 4 640x360
  gen_tone "$OUT/bed.wav" 8 48000 2 0.3
  gen_tone "$OUT/talk.wav" 4 48000 1 0.2
  tk fvideo footage add "$OUT/clip.mp4" --kind video --location "Smoke drive A" || true
  tk fmusic footage add "$OUT/bed.wav" --kind music --location "Smoke library B" || true
  tk faudio footage add "$OUT/talk.wav" --kind audio --location "Smoke recorder C" || true
  gen_still "$T/production/src/assets/smoke-harbour.png" 800x600
  gen_tone "$gen/$P_EDIT.s01.t1.mp3" 8 44100 1 0.2 -c:a libmp3lame -b:a 128k
  gen_tone "$gen/$P_EDIT/takes/$P_EDIT.s02.t1.pcm" 8 22050 1 0.2 -f s16le
  cat > "$T/production/src/voiceover/$P_EDIT.toml" <<EOF
[voiceover]
piece = "$P_EDIT"
voice_use = "voiceover"
model_id = "eleven_v4"
output_format = "pcm_22050"
per_cue = false

[[segment]]
id = "s01"
script_lines = "1.1-1.3"
text = "The ferry is late again. Every crossing waits for the tide, not the timetable, and the harbour knows it by heart."
request = "The ferry is late again. Every crossing waits for the tide, not the timetable, and the harbour knows it by heart."
take = 1
file = "generated/$P_EDIT.s01.t1.mp3"
characters = 113
pause_after = 0.4
status = "approved"
archived = ""

[[segment]]
id = "s02"
script_lines = "2.1-2.3"
text = "So the timetable is a promise the sea never signed. Nobody asked the water, and the water never answered the letter."
request = "So the timetable is a promise the sea never signed. Nobody asked the water, and the water never answered the letter."
take = 1
file = "generated/$P_EDIT/takes/$P_EDIT.s02.t1.pcm"
characters = 116
pause_after = 0.3
status = "approved"
archived = ""
EOF
  if $SKIP_THUMBS; then cards=false; skip_step 9 "the edit's card clip and overlay" "--skip-thumbnails"
  elif ! $HAVE_UV || [[ "$HAVE_CHROMIUM" == false ]]; then cards=false; skip_step 9 "the edit's card clip and overlay" "no uv or no Chromium"; fi
  if $cards; then
    sed 's#href="../../brand/#href="../../../brand/#' "$T/toolkit/templates/card.html" > "$T/production/src/cards/$P_EDIT.title.html"
  fi
  {
    printf '[edit]\npiece = "%s"\nversion = 1\nsize = "640x360"\naudio_rate = 48000\nloudness = "social"\n\n' "$P_EDIT"
    printf '[[clip]]\nid = "c01"\nsource = "%s"\nin = "00:00:00.500"\nout = "00:00:02.500"\nframe = "crop"\n\n' "$(manifest_id video)"
    printf '[[clip]]\nid = "c02"\nsource = "production/src/assets/smoke-harbour.png"\nseconds = 2.0\nmotion = "push-in"\ntransition = "fade"\ntransition_seconds = 0.5\n\n'
    printf '[[clip]]\nid = "c03"\ncolour = "#101418"\nseconds = 1.0\n\n'
    if $cards; then
      printf '[[clip]]\nid = "c04"\nsource = "production/src/cards/%s.title.html"\nseconds = 1.5\ntransition = "fade"\ntransition_seconds = 0.4\n\n' "$P_EDIT"
      printf '[[overlay]]\nsource = "production/src/cards/%s.title.html"\nat = "00:00:01.000"\nuntil = "00:00:02.000"\n\n' "$P_EDIT"
    fi
    printf '[[audio]]\nsource = "vo:%s"\nat = "00:00:00.200"\nrole = "voice"\n\n' "$P_EDIT"
    printf '[[audio]]\nsource = "%s"\nat = "00:00:00.000"\nin = "00:00:01.000"\nout = "00:00:07.000"\ngain_db = -6.0\nfade_in = 0.5\nfade_out = 1.0\nrole = "music"\nduck = true\n' "$(manifest_id music)"
  } > "$T/production/src/edits/$P_EDIT.toml"
  expect="4.5"; $cards && expect="5.6"
  # The master and the card renders land in the piece's own folder by default (D47, D64): one
  # card as a clip and as an overlay at one size keeps both renders, the overlay's .transparent.
  st=0; tk assemble assemble "production/src/edits/$P_EDIT.toml" || st=$?
  m="$T/production/src/renders/$P_EDIT/$P_EDIT.master.mp4"
  rec edl.status "$st"; rec edl.tail "$(tail_of assemble)"; rec edl.expect "$expect"
  rec edl.where "$([[ -f "$m" ]] && echo yes || echo no)"
  if $cards && [[ "$st" == 0 ]]; then
    miss=""
    for c in "$P_EDIT.title.640x360.png" "$P_EDIT.title.640x360.transparent.png"; do
      [[ -f "$T/production/src/renders/$P_EDIT/cards/$c" ]] || miss+="$c "
    done
    if [[ -z "$miss" ]]; then rec edl.cards ok; else rec edl.cards "missing from production/src/renders/$P_EDIT/cards/: ${miss% }"; fi
  fi
  if [[ -f "$m" ]]; then
    rec edl.facts "$(probe_facts "$m")"; rec edl.lufs "$(lufs "$m")"
    for k in "$@"; do
      st=0; tk "ecut.$k" cut "$m" --deliverable "$k" --in 00:00:00.000 --out 00:00:04.000 -o "$OUT/c9.$k.mp4" || st=$?
      rec "ecut.$k.status" "$st"; rec "ecut.$k.tail" "$(tail_of "ecut.$k")"
      [[ -f "$OUT/c9.$k.mp4" ]] && rec "ecut.$k.dur" "$(probe_facts "$OUT/c9.$k.mp4" | awk '{ print $8 }')"
    done
  fi
  k="${1:-youtube.long}"
  st=0; tk segs captions from-segments "production/src/voiceover/$P_EDIT.toml" --deliverable "$k" --offset 00:00:00.200 -o "$OUT/c9.segments.srt" || st=$?
  rec segs.status "$st"; rec segs.tail "$(tail_of segs)"
  d1="$(probe_facts "$gen/$P_EDIT.s01.t1.mp3" | awk '{ print $8 }')"
  d2="$(awk -v b="$(stat -c %s "$gen/$P_EDIT/takes/$P_EDIT.s02.t1.pcm")" 'BEGIN { printf "%.3f", b / (22050 * 2) }')"
  join="$(awk -v a="$d1" 'BEGIN { printf "%.3f", 0.2 + a + 0.4 }')"
  last="$(awk -v j="$join" -v b="$d2" 'BEGIN { printf "%.3f", j + b }')"
  rec segs.join "$join"; rec segs.lastwant "$last"
  if [[ -f "$OUT/c9.segments.srt" ]]; then
    cues="$(srt_times "$OUT/c9.segments.srt")"
    rec segs.cues "$(printf '%s\n' "$cues" | grep -c . || true)"
    rec segs.first "$(printf '%s\n' "$cues" | head -1 | cut -d' ' -f1)"
    rec segs.hasjoin "$(printf '%s\n' "$cues" | awk -v j="$join" '$1 + 0 == j + 0 { f = 1 } END { print (f ? "yes" : "no") }')"
    rec segs.lastend "$(printf '%s\n' "$cues" | tail -1 | cut -d' ' -f2)"
    st=0; tk retime captions retime "$OUT/c9.segments.srt" --in 00:00:01.000 --out 00:00:04.000 -o "$OUT/c9.retimed.srt" || st=$?
    rec retime.status "$st"
    first="$(printf '%s\n' "$cues" | awk '$2 > 1.0 { s = $1 - 1.0; if (s < 0) s = 0; printf "%.3f", s; exit }')"
    rec retime.want "$first"
    if [[ -f "$OUT/c9.retimed.srt" ]]; then
      rec retime.first "$(srt_times "$OUT/c9.retimed.srt" | head -1 | cut -d' ' -f1)"
      rec retime.inside "$(srt_times "$OUT/c9.retimed.srt" | awk '$1 < -0.0005 || $2 > 3.0005 { bad = 1 } END { print (NR > 0 && !bad ? "yes" : "no") }')"
    fi
    if [[ -f "$m" && -f "$OUT/c9.retimed.srt" ]]; then
      st=0; tk bcut cut "$m" --deliverable "$k" --in 00:00:01.000 --out 00:00:04.000 -o "$OUT/c9.cut.mp4" || st=$?
      st=0; tk eburn captions burn "$OUT/c9.cut.mp4" "$OUT/c9.retimed.srt" --deliverable "$k" -o "$OUT/c9.burned.mp4" || st=$?
      rec eburn.status "$st"; rec eburn.tail "$(tail_of eburn)"
      [[ -f "$OUT/c9.burned.mp4" ]] && rec eburn.dur "$(probe_facts "$OUT/c9.burned.mp4" | awk '{ print $8 }')"
    fi
  fi

  # ── 10. An audio master ──
  cat > "$T/production/src/edits/$P_AUDIO.toml" <<EOF
[edit]
piece = "$P_AUDIO"
size = ""
audio_rate = 48000
loudness = "podcast"

[[clip]]
id = "c01"
source = "$(manifest_id audio)"
in = "00:00:00.500"
out = "00:00:01.500"

[[clip]]
id = "c02"
source = "$(manifest_id audio)"
in = "00:00:02.000"
out = "00:00:03.000"
transition = "fade"
transition_seconds = 0.3

[[audio]]
source = "$(manifest_id music)"
at = "00:00:00.000"
gain_db = -12.0
fade_in = 0.5
fade_out = 0.5
role = "music"
EOF
  st=0; tk amaster assemble "production/src/edits/$P_AUDIO.toml" -o "$OUT/c10.master.wav" || st=$?
  rec amaster.status "$st"; rec amaster.tail "$(tail_of amaster)"; rec amaster.expect 1.700
  [[ -f "$OUT/c10.master.wav" ]] && rec amaster.facts "$(probe_facts "$OUT/c10.master.wav")"
  return 0
}

smoke_repo() { # $1 = the first answered video deliverable
  local st piece="$T/scripts/src/pieces/$P_SCRIPT" raw="$T/production/src/footage/raw" fmt p ext before
  mkdir -p "$piece"
  cat > "$piece/brief.md" <<EOF
---
piece: $P_SCRIPT
title: "Smoke"
kind: short-video
origin: scripted
picture: true
status: scripted
deliverables: [${1:-youtube.short}]
target_seconds: 10
words_per_minute: 150
verified: {}
---

# Smoke — brief
EOF
  cat > "$piece/script.md" <<'EOF'
---
piece: 907-smoke-script
version: 1
approved: ""
words: 0
estimated_seconds: 0
---

# Smoke — script

## 1. Hook (target 00:03)

VO: {brisk} The harbour bell is ringing.
TEXT: Ringing again?

## 2. The water decides (target 00:07)

ON: Each boat leaves when the water says so, not the clock.
SFX: rope on wood
ON: {pause 0.6} So the clock keeps a promise nobody made it.
EOF
  st=0; tk script script time "scripts/src/pieces/$P_SCRIPT/script.md" || st=$?
  rec script.status "$st"; rec script.total "$(said script 'total')"

  printf 'toolkit-smoke footage bytes\n' > "$OUT/smoke-cam.bin"
  st=0; tk fadd footage add "$OUT/smoke-cam.bin" --kind stock --location "Smoke archive" || st=$?
  rec footage.add "$st"
  rec footage.kept "$([[ -f "$OUT/smoke-cam.bin" ]] && echo yes || echo no)"
  rec footage.copied "$([[ -f "$raw/smoke-cam.bin" ]] && cmp -s "$OUT/smoke-cam.bin" "$raw/smoke-cam.bin" && echo yes || echo no)"
  st=0; tk fdup footage add "$OUT/smoke-cam.bin" --kind stock --location "Smoke archive" || st=$?; rec footage.dup "$st"
  st=0; tk fverify footage verify || st=$?; rec footage.verify "$st"
  if [[ -f "$raw/smoke-cam.bin" ]]; then
    printf 'toolkit-smoke footage bytez\n' > "$raw/smoke-cam.bin"
    st=0; tk fverify2 footage verify || st=$?; rec footage.changed "$st"
    printf 'toolkit-smoke footage bytes\n' > "$raw/smoke-cam.bin"
  fi

  # A call's take lands in its piece's generated/<piece>/takes/ (D21, D64), the folder the
  # toolkit makes before the first call, made here by hand. The mp3 piece also keeps a flat t1 an
  # earlier release left in generated/ and its register never recorded: the new take is t2 (D65).
  local gen="$T/production/src/voiceover/generated" n flat="$P_TAKE.s01.t1.mp3"
  mkdir -p "$gen"
  printf 'a take an earlier release left flat\n' > "$gen/$flat"
  before="$(grep -c . "$T/production/src/credits-log.md" 2>/dev/null || echo 0)"
  for p in "$P_TAKE:mp3_44100_128" "$P_PCM:pcm_22050"; do
    fmt="${p#*:}"; p="${p%%:*}"; ext=".mp3"; n=2; [[ "$fmt" == pcm* ]] && { ext=".pcm"; n=1; }
    printf '[voiceover]\npiece = "%s"\nvoice_use = "voiceover"\nmodel_id = "eleven_v4"\noutput_format = "%s"\nper_cue = false\n\n[[segment]]\nid = "s01"\nscript_lines = "1.1"\ntext = "The ferry is late again."\nrequest = "The ferry is late again."\ntake = 0\nfile = ""\ncharacters = 24\npause_after = 0.3\nstatus = ""\narchived = ""\n' \
      "$p" "$fmt" > "$T/production/src/voiceover/$p.toml"
    mkdir -p "$gen/$p/takes"
    printf 'a fake take, never an ElevenLabs call\n' > "$gen/$p/takes/tts_smoke_20270101_101010.mp3"
    st=0; tk "take.$ext" take add "production/src/voiceover/generated/$p/takes/tts_smoke_20270101_101010.mp3" --piece "$p" --segment s01 || st=$?
    rec "take${ext}.status" "$st"
    rec "take${ext}.named" "$([[ -f "$gen/$p/takes/$p.s01.t$n$ext" && ! -e "$gen/$p/takes/tts_smoke_20270101_101010.mp3" ]] && echo yes || echo no)"
    rec "take${ext}.register" "$(grep -qF "file = \"generated/$p/takes/$p.s01.t$n$ext\"" "$T/production/src/voiceover/$p.toml" && echo yes || echo no)"
    rec "take${ext}.credits" "$(grep -c "| $p |" "$T/production/src/credits-log.md" 2>/dev/null || echo 0)"
  done
  rec take.credits.before "$before"
  rec take.flat "$([[ -f "$gen/$flat" && -f "$gen/$P_TAKE/takes/$P_TAKE.s01.t2.mp3" && ! -e "$gen/$P_TAKE/takes/$flat" ]] && echo yes || echo no)"
}

smoke_text() {
  local st gen="$T/production/src/audiobook/generated" side
  cat > "$OUT/chapter.md" <<EOF
<!-- SMOKE CHAPTER, written at run time. -->

# The Crossing

<!-- section: arrival -->

::: epigraph
'Wait for the water, and the water waits for you.'
:::

The harbour lights went out one by one [@quill2021, p. 12].
The pilot spoke a word of the old tongue, [$CONSTRUCTED]{.conlang lang=example-tongue}, and the rope came free.

* * *

The boat moved out across the bar.
EOF
  st=0; tk abtext audiobook text "$OUT/chapter.md" --piece "$P_BOOK" --chapter ch01 || st=$?
  rec abtext.status "$st"; rec abtext.listed "$(said abtext "constructed.*$CONSTRUCTED|$CONSTRUCTED")"
  if ls "$gen/$P_BOOK".ch01.p*.txt >/dev/null 2>&1; then
    rec abtext.clean "$(cat "$gen/$P_BOOK".ch01.p*.txt | grep -qE '<!--|@quill|:::|\{\.conlang|\{pause|\* \* \*' && echo no || echo yes)"
    side="$gen/$P_BOOK.ch01.chunks.toml"
    rec abtext.pause "$(python3 - "$side" <<'PY'
import sys, tomllib
try: c = tomllib.load(open(sys.argv[1], "rb")).get("chunk", [])
except Exception: c = []
print("yes" if len(c) >= 2 and float(c[0].get("pause_after", 0)) == 2.0 else "no")
PY
)"
  else
    rec abtext.clean no; rec abtext.pause no
  fi
}

smoke_align() {
  local st piece="$T/scripts/src/pieces/$P_ALIGN"
  mkdir -p "$piece"
  cat > "$piece/transcript.md" <<EOF
---
piece: $P_ALIGN
source: F0001
made: by hand
approved: ""
---

# Smoke — transcript

## 1. Opening (at 00:00:00.500)

HOST: The harbour opens at first light.
HOST: The boats go out on the tide.

## 2. Close (at 00:00:04.500)

HOST: We wait for the water to turn.
HOST: Then we leave together.
EOF
  ff -f lavfi -i "sine=frequency=300:sample_rate=48000:duration=8.5" \
    -af "volume='between(t,1,2)+between(t,2.5,3.5)+between(t,5,6)+between(t,6.5,7.5)':eval=frame" "$OUT/speech.wav"
  st=0; tk anchors captions align "scripts/src/pieces/$P_ALIGN/transcript.md" "$OUT/speech.wav" --anchors -o "$OUT/c13.anchors.srt" || st=$?
  rec align.anchors "$st"
  rec align.inside "$(srt_times "$OUT/c13.anchors.srt" | awk 'NR <= 2 && ($1 < 0.5 || $2 > 4.5) { bad = 1 } NR > 2 && ($1 < 4.5 || $2 > 8.5) { bad = 1 } END { print (NR == 4 && !bad ? "yes" : "no") }')"
  ff -ss 4.5 -to 8.5 -i "$OUT/speech.wav" "$OUT/speech-cut.wav"
  st=0; tk lines captions align "scripts/src/pieces/$P_ALIGN/transcript.md" "$OUT/speech-cut.wav" --lines 2.1-2.2 -o "$OUT/c13.lines.srt" || st=$?
  rec align.lines "$st"; rec align.placed "$(srt_times "$OUT/c13.lines.srt" | grep -c . || true)"
}

smoke_setup() {
  local st s="$T/.claude/settings.json"
  mkdir -p "$GHOME"
  python3 - "$GHOME/.claude.json" "$SECRET" "$SECRET_MAIL" "$GHOME/Desktop" <<'PY'
import json, sys
path, secret, mail, base = sys.argv[1:5]
json.dump({"mcpServers": {"elevenlabs": {"type": "stdio", "command": "uvx", "args": ["elevenlabs-mcp"],
           "env": {"ELEVENLABS_API_KEY": secret, "ELEVENLABS_MCP_BASE_PATH": base}}},
           "oauthAccount": {"emailAddress": mail}}, open(path, "w"))
PY
  if [[ -f "$s" ]]; then
    python3 - "$s" "$GONE_ASK" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    ask = d.get("permissions", {}).get("ask", [])
    if sys.argv[2] in ask: ask.remove(sys.argv[2])
    json.dump(d, open(sys.argv[1], "w"), indent=2)
except Exception: pass
PY
  fi
  st=0; HOME="$GHOME" tk setup check --setup || st=$?
  rec setup.status "$st"
  rec setup.ask "$(said setup "$GONE_ASK")"
  rec setup.base "$(said setup 'base path.*(does not contain|outside)|(does not contain|outside).*repositor')"
  rec setup.leak "$(grep -qF -e "$SECRET" -e "$SECRET_MAIL" "$OUT/setup.log" && echo yes || echo no)"
  rec setup.encoders "$([[ "$(said setup 'webp')" == yes && "$(said setup 'avif|av1')" == yes ]] && echo yes || echo no)"
}

# ── 0.2.0: images, the GIF preview, web video, the podcast feed, published transcripts ──
#
# Checks 15–19 (DESIGN.md Section 7; D57–D60). Each records facts; run_checks judges them.

# "WxH codec pix_fmt bytes video-streams" of a still (ffprobe; the first video stream).
img_facts() {
  local b; b="$(stat -c %s "$1" 2>/dev/null || echo 0)"
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,pix_fmt -of json "$1" 2>/dev/null | python3 -c '
import json, sys
try: s = [x for x in json.load(sys.stdin).get("streams", []) if x.get("codec_type") == "video"]
except Exception: s = []
v = s[0] if s else {}
print("%sx%s %s %s %s %d" % (v.get("width", 0), v.get("height", 0), v.get("codec_name", "-"), v.get("pix_fmt", "-"), sys.argv[1], len(s)))' "$b"
}

# "w h frames one-play-seconds loop-count bytes" of a GIF, read from its own blocks: the logical
# screen, every image descriptor, every graphic control extension's delay (centiseconds) and the
# NETSCAPE2.0 loop count (-1 when the file has none: it plays once).
gif_facts() {
  python3 - "$1" <<'PY'
import os, sys
try: d = open(sys.argv[1], "rb").read()
except Exception: print("0 0 0 0 -1 0"); sys.exit()
if d[:6] not in (b"GIF87a", b"GIF89a"): print("0 0 0 0 -1 %d" % len(d)); sys.exit()
w, h = d[6] | d[7] << 8, d[8] | d[9] << 8
i = 13 + (3 * 2 ** ((d[10] & 7) + 1) if d[10] & 0x80 else 0)
frames, delay, loop = 0, 0, -1
def skip_blocks(i):
    while i < len(d) and d[i]: i += d[i] + 1
    return i + 1
while i < len(d):
    b = d[i]
    if b == 0x3B: break
    if b == 0x21:
        label = d[i + 1]
        if label == 0xF9: delay += d[i + 4] | d[i + 5] << 8
        if label == 0xFF and d[i + 3:i + 14] == b"NETSCAPE2.0" and d[i + 14] == 3 and d[i + 15] == 1:
            loop = d[i + 16] | d[i + 17] << 8
        i = skip_blocks(i + 2)
    elif b == 0x2C:
        frames += 1
        p = d[i + 9]; i += 10
        if p & 0x80: i += 3 * 2 ** ((p & 7) + 1)
        i = skip_blocks(i + 1)
    else: break
print("%d %d %d %.3f %d %d" % (w, h, frames, delay / 100.0, loop, len(d)))
PY
}

# The mean "r g b" of a square of a file's first frame.
region_rgb() { # $1 = file, $2 = size, $3 = x, $4 = y
  ffmpeg -v error -i "$1" -frames:v 1 -vf "crop=$2:$2:$3:$4,format=rgb24" -f rawvideo - 2>/dev/null | python3 -c '
import sys
b = sys.stdin.buffer.read()
n = len(b) // 3 or 1
print(" ".join(str(sum(b[c::3]) // n) for c in range(3)))'
}

# yes when an MP4's moov atom comes before its mdat (the index at the front: a page can start
# playing before the whole file arrives).
moov_first() {
  python3 - "$1" <<'PY'
import struct, sys
try: f = open(sys.argv[1], "rb")
except Exception: print("no"); sys.exit()
order, pos, size = [], 0, f.seek(0, 2)
while pos + 8 <= size:
    f.seek(pos); n, t = struct.unpack(">I4s", f.read(8)); hdr = 8
    if n == 1: n = struct.unpack(">Q", f.read(8))[0]; hdr = 16
    if n == 0: n = size - pos
    order.append(t.decode("latin-1"))
    if n < hdr: break
    pos += n
print("yes" if "moov" in order and "mdat" in order and order.index("moov") < order.index("mdat") else "no")
PY
}

max_bytes() { # "1 MB" → 1000000 (the toolkit's own reading of max_size)
  python3 -c '
import re, sys
m = re.fullmatch(r"\s*([\d.]+)\s*(KB|MB|GB|TB)\s*", sys.argv[1], re.I)
print(int(float(m.group(1)) * {"KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12}[m.group(2).upper()]) if m else 0)' "$1"
}

gif_plays() { # a GIF's loop count → how many times it plays (-1: no loop extension, once; 0: for ever)
  case "$1" in -1) echo 1 ;; 0) echo inf ;; *) echo $(( $1 + 1 )) ;; esac
}

ext_for() { case "$1" in jpg|jpeg) echo jpg ;; *) echo "$1" ;; esac; }
codec_for() { case "$1" in jpg|jpeg) echo mjpeg ;; png) echo png ;; webp) echo webp ;; avif) echo av1 ;; gif) echo gif ;; *) echo "$1" ;; esac; }

# Whether this ffmpeg can write a format at all: an encoder it lacks is a named SKIP, never a
# finding against the toolkit (DESIGN.md D57: libwebp, and an AV1 encoder with the avif muxer).
FF_ENCODERS=""; FF_MUXERS=""
can_encode() { # read once into variables: grep -q on a pipe would SIGPIPE ffmpeg under pipefail
  [[ -n "$FF_ENCODERS" ]] || FF_ENCODERS="$(ffmpeg -hide_banner -encoders 2>/dev/null || true)"
  [[ -n "$FF_MUXERS" ]] || FF_MUXERS="$(ffmpeg -hide_banner -muxers 2>/dev/null || true)"
  case "$1" in
    webp) grep -q ' libwebp ' <<< "$FF_ENCODERS" ;;
    avif) grep -qE ' (libaom-av1|libsvtav1) ' <<< "$FF_ENCODERS" && grep -qE ' avif ' <<< "$FF_MUXERS" ;;
    *) return 0 ;;
  esac
}

# ── 15. image ──
smoke_image() { # $@ = the answered rows
  local row k kind w h vc ac rate min max asp fmts atr f st sw sh out first="" poster="" maxk="" wrong f1
  local -A srcof=()
  for row in "$@"; do
    IFS=$'\t' read -r k kind w h vc ac rate min max asp fmts atr <<< "$row"
    [[ "$kind" == image && "$w" != - && "$h" != - && "$fmts" != - && "$fmts" != gif ]] || continue
    if (( w % 2 == 0 && h % 2 == 0 )); then sw=$((w / 2)); sh=$((h / 2)); else sw=$((w * 2)); sh=$((h * 2)); fi
    srcof[$k]="$OUT/c15src-${sw}x${sh}.png"
    # Half-transparent, so a table with alpha = false proves the flattening.
    [[ -f "${srcof[$k]}" ]] || ff -f lavfi -i "testsrc2=size=${sw}x${sh}:rate=1:duration=1,format=rgba,colorchannelmixer=aa=0.6" -frames:v 1 "${srcof[$k]}"
    [[ -z "$first" ]] && first="$k"
    [[ -z "$poster" && "$k" == *poster* ]] && poster="$k"
    [[ -z "$maxk" && "$(tfield "$k" max_size)" != - ]] && maxk="$k"
    rec "img.$k.want" "${w}x${h} $(tfield "$k" alpha)"
    for f in ${fmts//,/ }; do
      if ! can_encode "$f"; then skip_step 15 "image --format $f for $k" "this ffmpeg has no $f encoder or muxer"; continue; fi
      out="$OUT/c15.$k.$(ext_for "$f")"
      st=0; tk "img.$k.$f" image "${srcof[$k]}" --deliverable "$k" --format "$f" -o "$out" || st=$?
      rec "img.$k.$f.status" "$st"; rec "img.$k.$f.tail" "$(tail_of "img.$k.$f")"
      [[ -f "$out" ]] && rec "img.$k.$f.facts" "$(img_facts "$out")"
    done
  done
  if [[ -z "$first" ]]; then na_step 15 "no image deliverable in the answers"; return 0; fi
  # A source of another shape, without --frame: refused, nothing written.
  IFS=x read -r w h <<< "$(awk -F'\t' -v k="$first" '$1 == k { print $3 "x" $4 }' < <(printf '%s\n' "$@"))"
  wrong="$OUT/c15src-wrong.png"
  if [[ "$w" == "$h" ]]; then ff -f lavfi -i "testsrc2=size=320x180:rate=1:duration=1" -frames:v 1 "$wrong"
  else ff -f lavfi -i "testsrc2=size=320x320:rate=1:duration=1" -frames:v 1 "$wrong"; fi
  f1="$(tfield "$first" formats)"; f1="${f1%%,*}"
  st=0; tk img.shape image "$wrong" --deliverable "$first" -o "$OUT/c15.shape.$(ext_for "$f1")" || st=$?
  rec img.shape.key "$first"; rec img.shape.status "$st"
  rec img.shape.written "$([[ -f "$OUT/c15.shape.$(ext_for "$f1")" ]] && echo yes || echo no)"
  # A poster: a frame of a video at --at, at the table's size.
  if [[ -n "$poster" ]]; then
    f1="$(tfield "$poster" formats)"; f1="${f1%%,*}"
    st=0; tk img.poster image "$OUT/src.mp4" --deliverable "$poster" --at 00:00:01.000 -o "$OUT/c15.poster.$(ext_for "$f1")" || st=$?
    rec img.poster.key "$poster"; rec img.poster.status "$st"; rec img.poster.tail "$(tail_of img.poster)"
    rec img.poster.want "$(awk -F'\t' -v k="$poster" '$1 == k { print $3 "x" $4 }' < <(printf '%s\n' "$@"))"
    [[ -f "$OUT/c15.poster.$(ext_for "$f1")" ]] && rec img.poster.size "$(img_facts "$OUT/c15.poster.$(ext_for "$f1")" | cut -d' ' -f1)"
  else
    na_step 15p "no poster deliverable in the answers (website.poster, blog.poster)"
  fi
  # max_size, made impossible by a brand override: the encode must fail its verification.
  if [[ -n "$maxk" ]]; then
    f1="$(tfield "$maxk" formats)"; f1="${f1%%,*}"
    cp "$T/brand/src/platforms/overrides.toml" "$W/overrides.held"
    override "$maxk.max_size" '"1 KB"'
    st=0; tk img.maxsize image "${srcof[$maxk]}" --deliverable "$maxk" --format "$f1" -o "$OUT/c15.maxsize.$(ext_for "$f1")" || st=$?
    cp "$W/overrides.held" "$T/brand/src/platforms/overrides.toml"
    rec img.maxsize.key "$maxk"; rec img.maxsize.status "$st"
  fi
}

# ── 16. the GIF preview ──
smoke_gif() { # $@ = the answered rows
  local row k="" kind w h vc ac rate min max asp fmts atr st a fpsmax maxsize limit ov="$OUT/c16.overlay.png"
  for row in "$@"; do
    IFS=$'\t' read -r k kind w h vc ac rate min max asp fmts atr <<< "$row"
    [[ "$fmts" == gif ]] && break
    k=""
  done
  if [[ -z "$k" ]]; then na_step 16 "no GIF deliverable in the answers (newsletter.preview_gif)"; return 0; fi
  fpsmax="$(tfield "$k" fps_max)"; maxsize="$(tfield "$k" max_size)"
  rec gif.key "$k"; rec gif.want "$w $h $max $fpsmax $(max_bytes "$maxsize")"
  # A grey moving source, so any magenta in the GIF is the overlay's; a 7-second range covers
  # every case below.
  ff -f lavfi -i "testsrc2=size=640x360:rate=30:duration=7,hue=s=0" -f lavfi -i "sine=frequency=440:sample_rate=48000:duration=7" \
    -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -shortest "$OUT/gifsrc.mp4"
  ff -f lavfi -i "color=c=black@0.0:s=${w}x${h},format=rgba" -f lavfi -i "color=c=0xff00ff:s=80x80,format=rgba" \
    -filter_complex "[0][1]overlay=20:20,format=rgba" -frames:v 1 "$ov"
  ff -f lavfi -i "color=c=black@0.0:s=300x169,format=rgba" -frames:v 1 "$OUT/c16.overlay-small.png"
  st=0; tk gif.a cut "$OUT/gifsrc.mp4" --deliverable "$k" --in 00:00:00.000 --out 00:00:02.000 --overlay "$ov" -o "$OUT/c16.a.gif" || st=$?
  rec gif.a.status "$st"; rec gif.a.tail "$(tail_of gif.a)"
  if [[ -f "$OUT/c16.a.gif" ]]; then
    a="$(gif_facts "$OUT/c16.a.gif")"; rec gif.a.facts "$a"
    rec gif.a.overlay "$(region_rgb "$OUT/c16.a.gif" 10 55 55 | awk '{ print ($1 > 180 && $2 < 90 && $3 > 180) ? "yes" : "no" }')"
  fi
  st=0; tk gif.b cut "$OUT/gifsrc.mp4" --deliverable "$k" --in 00:00:01.000 --out 00:00:04.000 --overlay "$ov" -o "$OUT/c16.b.gif" || st=$?
  rec gif.b.status "$st"; [[ -f "$OUT/c16.b.gif" ]] && rec gif.b.facts "$(gif_facts "$OUT/c16.b.gif")"
  # Over max_size: remade at half the frame rate (then a quarter), its play time unchanged.
  if [[ -f "$OUT/c16.a.gif" ]]; then
    limit="$(awk -v b="$(cut -d' ' -f6 <<< "$a")" 'BEGIN { printf "%.1f", b * 0.85 / 1000 }')"
    cp "$T/brand/src/platforms/overrides.toml" "$W/overrides.held"
    override "$k.max_size" "\"$limit KB\""
    st=0; tk gif.c cut "$OUT/gifsrc.mp4" --deliverable "$k" --in 00:00:00.000 --out 00:00:02.000 --overlay "$ov" -o "$OUT/c16.c.gif" || st=$?
    cp "$W/overrides.held" "$T/brand/src/platforms/overrides.toml"
    rec gif.c.status "$st"; rec gif.c.tail "$(tail_of gif.c)"; rec gif.c.limit "$(max_bytes "$limit KB")"
    [[ -f "$OUT/c16.c.gif" ]] && rec gif.c.facts "$(gif_facts "$OUT/c16.c.gif")"
  fi
  st=0; tk gif.d cut "$OUT/gifsrc.mp4" --deliverable "$k" --in 00:00:00.000 --out 00:00:02.000 --overlay "$OUT/c16.overlay-small.png" -o "$OUT/c16.d.gif" || st=$?
  rec gif.d.status "$st"
  if [[ "$max" != - ]]; then
    st=0; tk gif.e cut "$OUT/gifsrc.mp4" --deliverable "$k" --in 00:00:00.000 --out "$(awk -v m="$max" 'BEGIN { printf "%.3f", m + 1 }')" -o "$OUT/c16.e.gif" || st=$?
    rec gif.e.status "$st"; rec gif.e.written "$([[ -f "$OUT/c16.e.gif" ]] && echo yes || echo no)"
  fi
}

# ── 17. a silent loop and web video ──
smoke_web() { # $@ = the answered rows
  local row k kind w h vc ac rate min max asp fmts atr st loop="" web="" real
  for row in "$@"; do
    IFS=$'\t' read -r k kind w h vc ac rate min max asp fmts atr <<< "$row"
    [[ "$kind" == video && "$atr" == 0 && -z "$loop" ]] && loop="$k"
    [[ "$k" == website.video ]] && web="$k"
  done
  if [[ -z "$loop" && -z "$web" ]]; then na_step 17 "no silent loop or website.video in the answers"; return 0; fi
  if [[ -n "$loop" ]]; then
    st=0; tk loop cut "$OUT/src.mp4" --deliverable "$loop" --in 00:00:00.000 --out 00:00:04.000 -o "$OUT/c17.loop.mp4" || st=$?
    rec loop.key "$loop"; rec loop.status "$st"; rec loop.tail "$(tail_of loop)"
    [[ -f "$OUT/c17.loop.mp4" ]] && rec loop.audio "$(probe_facts "$OUT/c17.loop.mp4" | awk '{ print $5 }')"
    # The mutation: an ffmpeg that maps the source's sound where it was told -an keeps the
    # sound; the toolkit's own verification must then fail the file (exit 1).
    real="$(command -v ffmpeg)"; mkdir -p "$W/anshim"; rm -f "$OUT/c17.saw-an"
    cat > "$W/anshim/ffmpeg" <<SHIM
#!/bin/sh
for a do
  shift
  if [ "\$a" = "-an" ]; then echo yes > "$OUT/c17.saw-an"; set -- "\$@" -map '0:a:0?' -c:a aac; continue; fi
  set -- "\$@" "\$a"
done
exec $real "\$@"
SHIM
    chmod 755 "$W/anshim/ffmpeg"
    st=0; PATH="$W/anshim:$PATH" tk loopmut cut "$OUT/src.mp4" --deliverable "$loop" --in 00:00:00.000 --out 00:00:04.000 -o "$OUT/c17.loopmut.mp4" || st=$?
    rec loopmut.status "$st"; rec loopmut.saw "$([[ -f "$OUT/c17.saw-an" ]] && echo yes || echo no)"
    [[ -f "$OUT/c17.loopmut.mp4" ]] && rec loopmut.audio "$(probe_facts "$OUT/c17.loopmut.mp4" | awk '{ print $5 }')"
  fi
  if [[ -n "$web" ]]; then
    st=0; tk web encode "$OUT/src.mp4" --deliverable "$web" -o "$OUT/c17.web.mp4" || st=$?
    rec web.status "$st"; rec web.tail "$(tail_of web)"
    [[ -f "$OUT/c17.web.mp4" ]] && rec web.moov "$(moov_first "$OUT/c17.web.mp4")"
  fi
}

# ── 18. the podcast feed, end to end, offline ──
#
# A fixture show on a fixture episode: the register written by `feed new` and `feed add`, edited
# here line by line as the author would, the feed audio encoded from a picture master, tagged,
# written, chaptered and checked, then mutated. Never a network call: the URLs are example.com's
# and Podcasting 2.0's published example, which nothing fetches.
FEED_SHOW="smoke-talks"; FEED_PIECE="910-smoke-feed"; FEED_SPEC_URL="https://podnews.net/rss/"
FEED_SPEC_GUID="9b024349-ccf0-5f69-a609-6b82873eab3c"   # the Podcasting 2.0 namespace's published example
FEED_AS_OF="01/01/2027 09:00"

# Line-level register edits, as an author makes them: `show KEY=TOML …`, `episode:PIECE KEY=TOML …`,
# or `append TEXT`. A multi-line string is replaced by a one-line one.
reg_edit() { # $1 = register, $2 = scope, then KEY=VALUE pairs (or the text to append)
  python3 - "$@" <<'PY'
import re, sys
path, scope, pairs = sys.argv[1], sys.argv[2], sys.argv[3:]
lines = open(path, encoding="utf-8").read().split("\n")
if scope == "append":
    lines += pairs[0].split("\n"); open(path, "w", encoding="utf-8").write("\n".join(lines)); sys.exit()
def is_header(l): return re.match(r"\s*\[", l) is not None
if scope == "show":
    s = next(i for i, l in enumerate(lines) if l.strip().startswith("[show]"))
else:
    piece, s = scope.split(":", 1)[1], None
    for i, l in enumerate(lines):
        if l.strip().startswith("[[episode]]"):
            j = i + 1
            while j < len(lines) and not is_header(lines[j]):
                if re.match(r'\s*piece\s*=\s*"%s"' % re.escape(piece), lines[j]): s = i
                j += 1
    if s is None: sys.exit("no row for " + piece)
for pair in pairs:
    key, value = pair.split("=", 1)
    e, i, hit = s + 1, s + 1, None
    while e < len(lines) and not is_header(lines[e]): e += 1
    for i in range(s + 1, e):
        if re.match(r"\s*%s\s*=" % re.escape(key), lines[i]): hit = i; break
    if hit is None: lines.insert(s + 1, f"{key} = {value}"); continue
    end = hit
    if lines[hit].count('"""') == 1:
        end = hit + 1
        while end < len(lines) and '"""' not in lines[end]: end += 1
    lines[hit:end + 1] = [f"{key} = {value}"]
open(path, "w", encoding="utf-8").write("\n".join(lines))
PY
}

reg_get() { # $1 = register, $2 = show KEY | episode:PIECE KEY → the value, or "-"
  python3 - "$1" "$2" "$3" <<'PY'
import sys, tomllib
try: d = tomllib.load(open(sys.argv[1], "rb"))
except Exception: print("-"); sys.exit()
scope, key = sys.argv[2], sys.argv[3]
if scope == "show": t = d.get("show", {})
else: t = next((e for e in d.get("episode", []) if e.get("piece") == scope.split(":", 1)[1]), {})
v = t.get(key); print("-" if v is None or v == "" else v)
PY
}

uuid5_of() { # $1 = namespace UUID, $2 = name → UUIDv5
  python3 -c 'import sys, uuid; print(uuid.uuid5(uuid.UUID(sys.argv[1]), sys.argv[2]))' "$1" "$2"
}
feed_guid_for() { # $1 = feed URL → the Podcasting 2.0 podcast:guid
  uuid5_of ead4c236-bf58-58c6-a2c6-a6b28d128cb6 "$(sed -E 's#^[a-zA-Z][a-zA-Z0-9+.-]*://##; s#/+$##' <<< "$1")"
}

# The fenced register skeleton of the podcast folder's CLAUDE.md against media_feed.SKELETON,
# flags and computed values aside (DESIGN.md D59): "same", or what differs.
skeleton_compare() {
  python3 - "$T/publishing/src/podcast/CLAUDE.md" "$T/toolkit" <<'PY'
import re, sys
sys.path.insert(0, sys.argv[2])
try:
    import media_feed
    mod = media_feed.SKELETON
except Exception as exc:
    print(f"media_feed.SKELETON unreadable ({exc.__class__.__name__})"); sys.exit()
try: text = open(sys.argv[1], encoding="utf-8").read()
except Exception: print("no publishing/src/podcast/CLAUDE.md"); sys.exit()
blocks = re.findall(r"```toml\n(.*?)```", text, re.S)
fenced = next((b for b in blocks if "[show]" in b), None)
if fenced is None: print("no fenced [show] skeleton in publishing/src/podcast/CLAUDE.md"); sys.exit()
COMPUTED = ("show", "feed_url", "podcast_guid", "guid", "site")
def norm(t):
    out = []
    for l in str(t).split("\n"):
        if "AUTHOR TO CONFIRM" in l:
            l = re.sub(r"\s*#\s*AUTHOR TO CONFIRM.*$", "", l)
            if not l.strip(): continue
        m = re.match(r"(\s*)([a-z_]+)(\s*=\s*)(\"[^\"]*\"|[^#\s]+)(.*)$", l)
        if m and m.group(2) in COMPUTED: l = m.group(1) + m.group(2) + " = <computed>" + m.group(5)
        l = re.sub(r"\s+", " ", l).strip()
        if l: out.append(l)
    return out
a, b = norm(fenced), norm(mod)
if a == b: print("same"); sys.exit()
for i, (x, y) in enumerate(zip(a, b)):
    if x != y: print(f"line {i + 1}: the folder's '{x[:50]}' against the module's '{y[:50]}'"); sys.exit()
print(f"the folder's copy has {len(a)} lines, the module's {len(b)}")
PY
}

# A written feed against DESIGN.md Section 6.17's required tags: "ok", or what is missing.
feed_xml_check() { # $1 = feed, $2 = podcast:guid, $3 = episode guid, $4 = bytes
  python3 - "$@" <<'PY'
import sys
import xml.etree.ElementTree as ET
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd", "podcast": "https://podcastindex.org/namespace/1.0",
      "atom": "http://www.w3.org/2005/Atom"}
try: root = ET.parse(sys.argv[1]).getroot()
except Exception as exc: print(f"not well-formed XML ({str(exc)[:60]})"); sys.exit()
miss = []
if root.tag != "rss" or root.get("version") != "2.0": miss.append("rss version 2.0")
ch = root.find("channel")
if ch is None: print("no channel"); sys.exit()
for tag in ("title", "link", "description", "language", "itunes:author", "itunes:image", "itunes:category",
            "itunes:explicit", "itunes:owner/itunes:email", "podcast:guid", "podcast:locked", "atom:link"):
    if ch.find(tag, NS) is None: miss.append(tag)
g = ch.find("podcast:guid", NS)
if g is not None and (g.text or "").strip() != sys.argv[2]: miss.append(f"podcast:guid {sys.argv[2]}")
items = ch.findall("item")
if len(items) != 1: miss.append(f"exactly one item (found {len(items)})")
for it in items[:1]:
    for tag in ("title", "description", "pubDate", "itunes:duration", "podcast:transcript"):
        if it.find(tag, NS) is None: miss.append("item " + tag)
    gu = it.find("guid")
    if gu is None or (gu.text or "").strip() != sys.argv[3] or gu.get("isPermaLink") != "false":
        miss.append(f"item guid {sys.argv[3]} isPermaLink=false")
    en = it.find("enclosure")
    if en is None or en.get("length") != sys.argv[4] or en.get("type") != "audio/mpeg": miss.append(f"enclosure length {sys.argv[4]} type audio/mpeg")
    if it.find("podcast:chapters", NS) is None and not any(c.tag.endswith("}chapters") for c in it): miss.append("item chapters")
print("ok" if not miss else "missing: " + ", ".join(miss))
PY
}

smoke_feed() {
  local st reg="$T/publishing/src/podcast/$FEED_SHOW.toml" tracked="$T/publishing/src/podcast/$FEED_SHOW.feed.xml"
  local render="$T/publishing/src/renders/$FEED_PIECE/$FEED_PIECE.podcast-feed-audio.mp3" pg eg sum sumr bytes secs dur held="$W/feed.held"
  local url="https://example.com/podcast/$FEED_SHOW.xml"
  # feed new refuses a project without the folder, naming the update that adds it.
  if [[ -d "$T/publishing/src/podcast" ]]; then mv "$T/publishing/src/podcast" "$W/podcast.away"; fi
  st=0; tk feed.nofolder feed new "$FEED_SHOW" --feed-url "$url" || st=$?
  rec feed.nofolder.status "$st"; rec feed.nofolder.said "$(said feed.nofolder 'copier update.*-a \.copier-answers\.syntek-media\.yml|-a \.copier-answers\.syntek-media\.yml')"
  rec feed.nofolder.made "$([[ -d "$T/publishing/src/podcast" ]] && echo yes || echo no)"
  if [[ ! -d "$W/podcast.away" ]]; then
    na_step 18 "no podcast folder (PLATFORMS without podcast): only feed new's refusal was run"; return 0
  fi
  rm -rf "$T/publishing/src/podcast"; mv "$W/podcast.away" "$T/publishing/src/podcast"
  rec feed.skeleton "$(skeleton_compare)"

  # Identity: the spec's own example, then the fixture show and its episode.
  st=0; tk feed.spec feed new smoke-spec --feed-url "$FEED_SPEC_URL" || st=$?
  rec feed.spec.status "$st"; rec feed.spec.guid "$(reg_get "$T/publishing/src/podcast/smoke-spec.toml" show podcast_guid)"
  st=0; tk feed.new feed new "$FEED_SHOW" --feed-url "$url" || st=$?
  rec feed.new.status "$st"; rec feed.new.tail "$(tail_of feed.new)"
  [[ -f "$reg" ]] || { rec feed.register missing; return 0; }
  rec feed.new.flag "$(grep -q 'AUTHOR TO CONFIRM' "$reg" && echo yes || echo no)"
  pg="$(reg_get "$reg" show podcast_guid)"
  rec feed.new.guid "$([[ "$pg" == "$(feed_guid_for "$url")" ]] && echo ok || echo "$pg")"
  mkdir -p "$T/scripts/src/pieces/$FEED_PIECE"   # feed add writes a GUID once, so the piece must exist
  printf -- '---\npiece: %s\nkind: podcast\nstatus: captioned\ndeliverables: [podcast.feed_audio]\n---\n\n# Smoke feed — brief\n' "$FEED_PIECE" \
    > "$T/scripts/src/pieces/$FEED_PIECE/brief.md"
  st=0; tk feed.add feed add "$FEED_SHOW" --piece "$FEED_PIECE" || st=$?
  rec feed.add.status "$st"; rec feed.add.tail "$(tail_of feed.add)"
  eg="$(reg_get "$reg" "episode:$FEED_PIECE" guid)"
  rec feed.add.guid "$([[ "$pg" != - && "$eg" == "$(uuid5_of "$pg" "$FEED_PIECE")" ]] && echo ok || echo "$eg")"

  # M5: the feed audio from a picture master — sound only, untagged, at the podcast target. Six
  # minutes, so three chapters two minutes apart fit Apple's chapter rules. The master sits in its
  # piece's folder, where assemble writes it, and encode's default is the piece's publishing
  # folder, the one path feed tag reads (D64, D65): no -o.
  mkdir -p "$T/production/src/renders/$FEED_PIECE" "$T/publishing/src/renders" "$T/publishing/src/captions"
  ff -f lavfi -i "testsrc2=size=160x90:rate=5:duration=360" -f lavfi -i "sine=frequency=330:sample_rate=48000:duration=360,volume=0.2" \
    -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -ac 2 -shortest "$T/production/src/renders/$FEED_PIECE/$FEED_PIECE.master.mp4"
  st=0; tk feed.encode encode "production/src/renders/$FEED_PIECE/$FEED_PIECE.master.mp4" --deliverable podcast.feed_audio || st=$?
  rec feed.encode.status "$st"; rec feed.encode.tail "$(tail_of feed.encode)"
  [[ -f "$render" ]] || return 0
  rec feed.encode.facts "$(probe_facts "$render")"; rec feed.encode.lufs "$(lufs "$render")"
  rec feed.encode.tags "$(ffprobe -v error -show_entries format_tags=title,artist,album -of csv=p=0 "$render" 2>/dev/null | tr -d ',\n' | grep -c . || true)"

  # feed tag on a row with no title: refused, nothing changed.
  sum="$(sha1sum < "$render")"; sumr="$(sha1sum < "$reg")"
  st=0; tk feed.tag0 feed tag "$FEED_SHOW" --piece "$FEED_PIECE" || st=$?
  rec feed.tag0.status "$st"
  rec feed.tag0.unchanged "$([[ "$(sha1sum < "$render")" == "$sum" && "$(sha1sum < "$reg")" == "$sumr" ]] && echo yes || echo no)"

  # The author fills the show and the row; the cover and its ID3 copy are design exports encoded
  # with image; the transcript is the master-timed VTT.
  ff -f lavfi -i "testsrc2=size=1500x1500:rate=1:duration=1" -frames:v 1 "$OUT/c18.cover.png"
  st=0; tk feed.cover image "$OUT/c18.cover.png" --deliverable podcast.cover --format jpg -o "publishing/src/renders/$FEED_SHOW.podcast-cover.jpg" || st=$?
  rec feed.cover.status "$st"
  st=0; tk feed.id3cover image "$OUT/c18.cover.png" --deliverable podcast.id3_cover -o "publishing/src/renders/$FEED_SHOW.podcast-id3-cover.jpg" || st=$?
  rec feed.id3cover.status "$st"
  printf 'WEBVTT\n\n00:00:00.500 --> 00:00:02.500\nThe tide decides.\n' > "$T/publishing/src/captions/$FEED_PIECE.en-GB.vtt"
  sed -i -E '/^[[:space:]]*#.*AUTHOR TO CONFIRM/d; s/[[:space:]]*#[[:space:]]*AUTHOR TO CONFIRM.*$//' "$reg"
  reg_edit "$reg" show 'title="Smoke Talks"' 'author="Probe Studio"' 'owner_name="Probe Studio"' \
    'owner_email="podcast@example.com"' 'link="https://example.com/podcast/"' 'media_base="https://example.com/media/"' \
    'copyright="2027 Probe Studio"' 'category="Education"' 'description="A show the audit makes.\nIt exists for a minute."' \
    "cover=\"$FEED_SHOW.podcast-cover.jpg\"" "id3_cover=\"$FEED_SHOW.podcast-id3-cover.jpg\"" 'approved="01/01/2027"'
  reg_edit "$reg" "episode:$FEED_PIECE" 'title="The tide decides"' 'description="Why the ferry waits.\nA voice made with a speech tool reads part of it."' \
    "pub_date=\"$FEED_AS_OF\"" "page=\"https://example.com/podcast/$FEED_PIECE/\"" "transcript=\"$FEED_PIECE.en-GB.vtt\""
  reg_edit "$reg" append "$(printf '\n[[episode.chapter]]\nstart = "00:00:00.000"\ntitle = "The Bell"\n\n[[episode.chapter]]\nstart = "00:02:00.000"\ntitle = "The Crossing"\n\n[[episode.chapter]]\nstart = "00:04:00.000"\ntitle = "The Harbour"\n')"

  # M7: tag in place, the audio stream untouched.
  read -r _ _ _ _ _ _ _ dur <<< "$(probe_facts "$render")"
  st=0; tk feed.tag feed tag "$FEED_SHOW" --piece "$FEED_PIECE" || st=$?
  rec feed.tag.status "$st"; rec feed.tag.tail "$(tail_of feed.tag)"
  rec feed.tag.before "$dur"; rec feed.tag.after "$(probe_facts "$render")"
  rec feed.tag.tags "$(ffprobe -v error -show_entries format_tags=title,artist,album -of default=nw=1 "$render" 2>/dev/null | sed 's/^TAG://I' | LC_ALL=C sort | paste -sd'|' -)"
  rec feed.tag.id3 "$(python3 -c 'import sys; b = open(sys.argv[1], "rb").read(4); print(b[3] if b[:3] == b"ID3" else 0)' "$render" 2>/dev/null || echo 0)"
  rec feed.tag.chapters "$(ffprobe -v error -show_chapters -of csv=p=0 "$render" 2>/dev/null | grep -c . || true)"
  rec feed.tag.apic "$(ffprobe -v error -show_entries stream_disposition=attached_pic -of csv=p=0 "$render" 2>/dev/null | grep -c '^1' || true)"
  bytes="$(stat -c %s "$render")"; secs="$(reg_get "$reg" "episode:$FEED_PIECE" seconds)"
  rec feed.tag.row "$(reg_get "$reg" "episode:$FEED_PIECE" render) $(reg_get "$reg" "episode:$FEED_PIECE" bytes) $secs"
  rec feed.tag.rowwant "$FEED_PIECE.podcast-feed-audio.mp3 $bytes $(probe_facts "$render" | awk '{ print $8 }')"

  # feed write: --as-of is required; one register and one --as-of give one set of bytes.
  st=0; tk feed.write0 feed write "$FEED_SHOW" || st=$?; rec feed.write0.status "$st"
  reg_edit "$reg" "episode:$FEED_PIECE" 'status="ready"'
  st=0; tko feed.write1 feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" || st=$?
  rec feed.write.status "$st"; rec feed.write.tail "$(tail_of feed.write1)"
  tko feed.write2 feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" || true
  rec feed.write.same "$([[ -s "$OUT/feed.write1.out" ]] && cmp -s "$OUT/feed.write1.out" "$OUT/feed.write2.out" && echo yes || echo no)"
  rec feed.write.xml "$(feed_xml_check "$OUT/feed.write1.out" "$pg" "$eg" "$bytes")"

  # --rekey before anything is published: a new URL, every GUID recomputed from it.
  st=0; tk feed.rekey feed new "$FEED_SHOW" --rekey --feed-url "https://example.com/podcast/$FEED_SHOW-v2.xml" || st=$?
  pg="$(reg_get "$reg" show podcast_guid)"; eg="$(reg_get "$reg" "episode:$FEED_PIECE" guid)"
  rec feed.rekey.status "$st"
  rec feed.rekey.ok "$([[ "$pg" == "$(feed_guid_for "https://example.com/podcast/$FEED_SHOW-v2.xml")" && "$eg" == "$(uuid5_of "$pg" "$FEED_PIECE")" ]] && echo yes || echo no)"

  # The tracked feed: written with -o, then replaced after a register change.
  st=0; tk feed.tracked feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" -o "publishing/src/podcast/$FEED_SHOW.feed.xml" || st=$?
  tko feed.tracked.stdout feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" || true
  rec feed.tracked.status "$st"
  rec feed.tracked.same "$([[ -s "$tracked" ]] && cmp -s "$tracked" "$OUT/feed.tracked.stdout.out" && echo yes || echo no)"
  reg_edit "$reg" "episode:$FEED_PIECE" 'description="Why the ferry waits for the water.\nA voice made with a speech tool reads part of it."'
  st=0; tk feed.tracked2 feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" -o "publishing/src/podcast/$FEED_SHOW.feed.xml" || st=$?
  rec feed.tracked2.status "$st"; rec feed.tracked2.replaced "$(grep -q 'waits for the water' "$tracked" 2>/dev/null && echo yes || echo no)"

  st=0; tk feed.chapters feed chapters "$FEED_SHOW" --piece "$FEED_PIECE" -o "$OUT/c18.chapters.json" || st=$?
  rec feed.chapters.status "$st"
  rec feed.chapters.json "$(python3 -c '
import json, sys
try: d = json.load(open(sys.argv[1]))
except Exception: print("invalid"); sys.exit()
s = [c.get("startTime") for c in d.get("chapters", [])]
print("ok" if d.get("version") == "1.2" and s == [0, 120, 240] and all(isinstance(x, float) for x in s) else "version %s starts %s" % (d.get("version"), s))' "$OUT/c18.chapters.json" 2>/dev/null || echo invalid)"

  st=0; tk feed.check feed check "$FEED_SHOW" || st=$?
  rec feed.check.status "$st"; rec feed.check.tail "$(tail_of feed.check)"

  # Mutations: each must exit 1. The register and the tracked feed are restored after each.
  cp "$reg" "$held.toml"; cp "$tracked" "$held.xml" 2>/dev/null || true
  reg_edit "$reg" append "$(printf '\n[[episode]]\npiece = "911-smoke-duplicate"\nguid = "%s"\ntitle = "A copy"\nstatus = "planned"\n' "$eg")"
  st=0; tk feed.m.dup feed check "$FEED_SHOW" || st=$?; rec feed.m.dup "$st"; cp "$held.toml" "$reg"
  python3 - "$held.xml" "$OUT/c18.prev-gone.xml" "$OUT/c18.prev-length.xml" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
gone = '<item><title>Gone</title><guid isPermaLink="false">00000000-0000-5000-8000-0000000000aa</guid><enclosure url="https://example.com/media/gone.mp3" length="1" type="audio/mpeg"/></item>'
open(sys.argv[2], "w", encoding="utf-8").write(t.replace("</channel>", gone + "</channel>", 1))
open(sys.argv[3], "w", encoding="utf-8").write(re.sub(r'(<enclosure[^>]*length=")(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 1), t, count=1))
PY
  st=0; tk feed.m.gone feed check "$FEED_SHOW" --previous "$OUT/c18.prev-gone.xml" || st=$?; rec feed.m.gone "$st"
  cp "$OUT/c18.prev-gone.xml" "$tracked"
  st=0; tk feed.m.gonewrite feed write "$FEED_SHOW" --as-of "$FEED_AS_OF" -o "publishing/src/podcast/$FEED_SHOW.feed.xml" || st=$?
  rec feed.m.gonewrite "$st"; rec feed.m.gonewrite.kept "$(cmp -s "$tracked" "$OUT/c18.prev-gone.xml" && echo yes || echo no)"
  cp "$held.xml" "$tracked"
  st=0; tk feed.m.length feed check "$FEED_SHOW" --previous "$OUT/c18.prev-length.xml" || st=$?; rec feed.m.length "$st"
  reg_edit "$reg" "episode:$FEED_PIECE" 'title="The tide <b>decides</b>"'
  st=0; tk feed.m.angle feed check "$FEED_SHOW" || st=$?; rec feed.m.angle "$st"; cp "$held.toml" "$reg"
  reg_edit "$reg" "episode:$FEED_PIECE" "bytes=$((bytes + 1))"; mv "$tracked" "$held.away"
  st=0; tk feed.m.bytes feed check "$FEED_SHOW" || st=$?; rec feed.m.bytes "$st"; cp "$held.toml" "$reg"; mv "$held.away" "$tracked"
  printf '\n# AUTHOR TO CONFIRM: the owner address\n' >> "$reg"
  st=0; tk feed.m.flag feed check "$FEED_SHOW" || st=$?; rec feed.m.flag "$st"; cp "$held.toml" "$reg"

  # Once an episode is published, the identity is fixed: --rekey is refused.
  reg_edit "$reg" "episode:$FEED_PIECE" 'status="published"'
  sumr="$(sha1sum < "$reg")"
  st=0; tk feed.rekey2 feed new "$FEED_SHOW" --rekey --feed-url "https://example.com/podcast/$FEED_SHOW-v3.xml" || st=$?
  rec feed.rekey2.status "$st"; rec feed.rekey2.unchanged "$([[ "$(sha1sum < "$reg")" == "$sumr" ]] && echo yes || echo no)"
}

# ── 19. the published transcript ──
smoke_transcript() {
  local st piece="$T/scripts/src/pieces/$P_TRANSCRIPT" before after o="publishing/src/captions/$P_TRANSCRIPT.transcript.en-GB.md"
  mkdir -p "$piece" "$T/publishing/src/captions"
  cat > "$piece/script.md" <<EOF
---
piece: $P_TRANSCRIPT
version: 1
approved: ""
words: 0
estimated_seconds: 0
---

# Smoke — script

## 1. Hook (target 00:03)

VO: {brisk} The harbour bell is ringing.
TEXT: Ringing again?
NOTE: hold on the bell
SFX: rope on wood

## 2. The water decides (target 00:07)

VO: Each boat leaves when the water says so.
VO: {pause 0.6} So the clock keeps a promise nobody made it.
VO: The harbour waits for the tide.
EOF
  before="$(find "$T/publishing/src/captions" -type f | LC_ALL=C sort | sha1sum)"
  st=0; tko tr captions transcript "scripts/src/pieces/$P_TRANSCRIPT/script.md" || st=$?
  after="$(find "$T/publishing/src/captions" -type f | LC_ALL=C sort | sha1sum)"
  rec tr.status "$st"; rec tr.tail "$(tail_of tr)"
  rec tr.spoken "$(printed tr 'The harbour bell is ringing\.')"
  rec tr.onscreen "$(printed tr '\[On screen: Ringing again\?\]')"
  rec tr.tags "$(printed tr '(^|[^A-Za-z])VO:')"
  rec tr.note "$(printed tr 'NOTE|hold on the bell')"
  rec tr.braces "$(printed tr '[{}]')"
  rec tr.cues "$(printed tr '^[[:space:]]*(SFX|MUSIC|TEXT):')"
  rec tr.wrote "$([[ "$before" == "$after" ]] && echo no || echo yes)"
  st=0; tko trlines captions transcript "scripts/src/pieces/$P_TRANSCRIPT/script.md" --lines 2.1-2.2 || st=$?
  rec tr.lines.status "$st"
  rec tr.lines.has "$([[ "$(printed trlines 'Each boat leaves')" == yes && "$(printed trlines 'So the clock keeps')" == yes ]] && echo yes || echo no)"
  rec tr.lines.extra "$(printed trlines 'harbour waits|harbour bell')"
  st=0; tk tro captions transcript "scripts/src/pieces/$P_TRANSCRIPT/script.md" -o "$o" || st=$?
  rec tr.o.status "$st"; rec tr.o.written "$([[ -s "$T/$o" ]] && echo yes || echo no)"
}

# ── 0.3.0: where; the frame grid ─────────────────────────────────────────────

# ── 24. where ──
# A fixture piece with tracked files in three folders, its timing file among them, and ignored
# output in two of its three per-piece folders: where lists the first and only names the second.
smoke_where() {
  local st p="$P_WHERE" f want="" got="" hidden=""
  local -a tracked=("scripts/src/pieces/$p/brief.md" "production/src/edits/$p.toml" "production/src/timing/$p.words.json")
  local -a ignored=("production/src/renders/$p/$p.master.mp4" "production/src/renders/$p/cards/$p.title.64x64.png"
                    "production/src/voiceover/generated/$p/takes/$p.s01.t1.mp3")
  for f in "${tracked[@]}" "${ignored[@]}"; do mkdir -p "$(dirname "$T/$f")"; printf 'smoke %s\n' "${f##*/}" > "$T/$f"; done
  st=0; tko where where "$p" || st=$?
  rec where.status "$st"; rec where.tail "$(tail_of where)"
  for f in "${tracked[@]}"; do grep -qxF "  $f" "$OUT/where.out" 2>/dev/null || want+="$f "; done
  rec where.listed "$([[ -z "$want" ]] && echo yes || echo "no: ${want% }")"
  for f in "${ignored[@]}"; do grep -qF -e "${f##*/}" -e "$p/takes" -e "$p/cards" "$OUT/where.out" 2>/dev/null && hidden+="$f "; done
  rec where.hidden "${hidden% }"
  got="$(awk '/^ignored per-piece folders/ { on = 1; next } on { print $1 "=" $2 }' "$OUT/where.out" 2>/dev/null | paste -sd' ' -)"
  want="production/src/renders/$p/=exists production/src/voiceover/generated/$p/=exists publishing/src/renders/$p/=absent"
  rec where.folders "$([[ "$got" == "$want" ]] && echo yes || echo "${got:-none}")"
  st=0; tk where.bad where 914-smoke-no-such-piece || st=$?; rec where.bad "$st"
}

# ── 25. a run of stills on the frame grid, an overlay on a clip boundary, the held sound ──
# 25 flat stills of 0.16 s at 30 fps (4.8 frames each): each starts on the frame nearest its
# running total (0, 5, 10, 14, 19 ...) and the master ends on the one nearest 4.000 s, 120 frames,
# where rounding still by still would give 125. An overlay with alpha over the top half, from
# 0.480 s (the fourth still's start, frame 14) until 0.800 s (frame 24), and a tone running past
# the picture (DESIGN.md Section 6.4). Then the master is encoded to a video deliverable with
# sound: its sound ends no later than its picture, and encode's own check passes.
smoke_timing() {
  local st=0 live why
  PYTHONDONTWRITEBYTECODE=1 python3 - "$T" "$OUT" "$RESULTS" "$HAVE_FFMPEG" \
    >"$OUT/timing-fixture.log" 2>&1 <<'PY' || st=$?
import json, os, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
root, out, receipt = map(Path, sys.argv[1:4])
sys.path.insert(0, str(root / 'toolkit'))
import media_common as C
import media_audio as A
import media_captions as K
import media_repo as R
import transcribe as T
C.ROOT = root
def record(key, good):
    with receipt.open('a') as f: f.write(key + '\t' + ('yes' if good else 'no') + '\n')
segment = {'id':'s01', 'text':'A ferry crosses.', 'request':'A feh-ree crosses.', 'start':0.0, 'end':3.0}
prepared = T.prepare([segment], {'ferry':'feh-ree'})
alignment = {'segments':[{'words':[
    {'word':'A','start':0.1,'end':0.3,'score':0.8},
    {'word':'feh','start':0.4,'end':0.7,'score':0.6},
    {'word':'ree','start':0.8,'end':1.1,'score':0.4},
    {'word':'crosses','start':1.2,'end':2.5,'score':0.9}]}]}
reply = T.result('917-smoke-words', prepared, [alignment], 'A ferry crosses.')
record('timing.parts', prepared[0]['align_text'] == 'A feh ree crosses'
       and reply['words'][1] == {'word':'ferry','start':0.4,'end':1.1,'score':0.4,'segment':'s01'})
rejected = 0
for text in ('A 2 ferry', 'A £ ferry', '[quiet] A ferry'):
    try: T.prepare([{**segment,'text':text}], {})
    except T.BadText: rejected += 1
record('timing.text', rejected == 3)
different = {'segments':[{'words':[{**w,'word':'Else'} if i == 0 else w
                                 for i,w in enumerate(alignment['segments'][0]['words'])]}]}
record('timing.sequence', T.result('917-smoke-words',prepared,[different],None)['exit'] == 1)
empty = T.result('917-smoke-words',prepared,[{'segments':[{'words':[]}]}],None)
record('timing.empty', empty['exit'] == 1 and 'returned no words' in empty['check'])
record('timing.heard', T.result('917-smoke-words',prepared,[alignment],'A boat crosses.')['exit'] == 1
       and reply['exit'] == 0)
record('timing.report', 'low score 0.400' in reply['check'] and 'request: A feh-ree crosses.' in reply['check']
       and 'disabled with --no-cross-check' in T.result('917-smoke-words',prepared,[alignment],None)['check'])
with tempfile.TemporaryDirectory() as folder:
    p = Path(folder)
    absent = {'weights':p/'missing', 'punkt_files':[p/'absent'], 'snapshot':None}
    record('timing.cache', len(T.missing_cache(absent)) == 3 and len(T.missing_cache(absent,False)) == 2)
words = root / C.TIMING / '917-smoke-words.words.json'
words.parent.mkdir(parents=True,exist_ok=True)
words.write_text(json.dumps(reply['words']))
caption = out / 'words.srt'
proc = subprocess.run([sys.executable,str(root/'toolkit/media.py'),'captions','from-words',str(words),
                       '--deliverable','youtube.short','-o',str(caption)],cwd=root,capture_output=True,text=True)
cues = K.read_srt(caption) if caption.is_file() else []
record('timing.captions', proc.returncode == 0 and len(cues) == 1 and cues[0].start == 0.1
       and cues[0].end == 2.5 and cues[0].text == 'A ferry crosses.')
with patch.dict(os.environ, {'MEDIA_TRANSCRIBE_PYTHON':''}), patch.object(A,'transcribe_python',return_value=''):
    rows, findings = R.setup_report(root)
record('setup.transcribe', any('WhisperX interpreter absent' in row and 'transcribe fetch' in row for row in rows)
       and not any('WhisperX interpreter absent' in row for row in findings))
python = os.environ.get('MEDIA_TRANSCRIBE_PYTHON','').strip()
reason = ''
if not python: reason = 'MEDIA_TRANSCRIBE_PYTHON is not set; no audit builds WhisperX'
elif T.missing_cache(T.cache_paths(),False): reason = 'alignment cache absent; the author must run transcribe fetch'
elif sys.argv[4] != 'true': reason = 'ffmpeg is absent'
elif not __import__('shutil').which('espeak-ng'): reason = 'espeak-ng fixture voice is absent'
if reason:
    with receipt.open('a') as f: f.write('timing.live\tskip\ntiming.live.reason\t' + reason + '\n')
else:
    piece = '918-smoke-live'
    takes = root / C.VO_GENERATED / piece / 'takes'
    takes.mkdir(parents=True,exist_ok=True)
    take = takes / (piece + '.s01.t1.wav')
    subprocess.run(['espeak-ng','-s','130','-w',str(take),'A ferry crosses.'],check=True,capture_output=True)
    register = root / C.VOICEOVER / (piece + '.toml')
    register.write_text('[voiceover]\npiece = "918-smoke-live"\noutput_format = "pcm_22050"\n'
                        '[[segment]]\nid = "s01"\nstatus = "approved"\ntext = "A ferry crosses."\n'
                        'request = "A ferry crosses."\nfile = "generated/' + piece + '/takes/' + take.name + '"\n')
    def cli(*args):
        return subprocess.run([sys.executable,str(root/'toolkit/media.py'),*args],cwd=root,
                              capture_output=True,text=True)
    joined = cli('voice','join',piece)
    aligned = cli('transcribe',piece,'--no-cross-check') if joined.returncode == 0 else joined
    print(aligned.stdout); print(aligned.stderr)
    working = root / C.PROD_RENDERS / piece / 'timing' / (piece + '.words.json')
    timed = json.loads(working.read_text()) if working.is_file() else []
    record('timing.live', aligned.returncode == 0 and [w['word'] for w in timed] == ['A','ferry','crosses.']
           and all(w['start'] is not None and w['end'] is not None for w in timed))
PY
  rec timing.status "$st"
  live="$(awk -F '\t' '$1 == "timing.live" {print $2}' "$RESULTS")"
  if [[ "$live" == skip ]]; then
    why="$(awk -F '\t' '$1 == "timing.live.reason" {print $2}' "$RESULTS")"
    skip_step 22 "WhisperX live alignment" "$why"
  fi
}

# ── 21 and 26. native mouth cues and optional/broken Rhubarb setup ──
smoke_lipsync() {
  local st=0 why
  PYTHONDONTWRITEBYTECODE=1 python3 - "$T" "$OUT" "$RESULTS" "$HAVE_FFMPEG" \
    >"$OUT/lipsync-fixture.log" 2>&1 <<'PY' || st=$?
import os, shutil, sys, tempfile
from pathlib import Path
from unittest.mock import patch
root, out, receipt = map(Path, sys.argv[1:4])
sys.path.insert(0, str(root / 'toolkit'))
import media as M
import media_common as C
import media_repo as R
C.ROOT = root
def record(key, value):
    with receipt.open('a') as f: f.write(key + '\t' + value + '\n')
original = shutil.which
with patch.object(shutil, 'which', lambda name, *a, **k: None if name == 'rhubarb' else original(name,*a,**k)):
    rows, findings = R.setup_report(root)
record('setup.rhubarb.absent', 'yes' if any('rhubarb absent: lipsync' in r for r in rows)
       and not any('rhubarb absent' in r for r in findings) else 'no')
with tempfile.TemporaryDirectory() as folder:
    exe = Path(folder) / 'release/rhubarb'
    exe.parent.mkdir()
    exe.write_text('#!/bin/sh\nprintf "Rhubarb Lip Sync version 1.14.0\\n"\n')
    exe.chmod(0o755)
    link = Path(folder) / 'rhubarb'
    link.symlink_to(exe)
    with patch.object(shutil, 'which', lambda name,*a,**k: str(link) if name == 'rhubarb' else original(name,*a,**k)):
        rows, findings = R.setup_report(root)
    record('setup.rhubarb.broken', 'yes' if any('rhubarb for lipsync' in r and 'cmudict-en-us.dict' in r
           for r in findings) else 'no')
if sys.argv[4] != 'true':
    record('mouth.live','skip')
    record('mouth.live.reason','ffmpeg or ffprobe is absent')
else:
    # Use the same generated dialogue, fatal-exit and Git-edit fixtures as the toolkit's
    # self-test. Run them afresh in this render; the live recogniser is never mocked.
    results = {}
    labels = {
        'lipsync passes pocketSphinx and all extended shapes with plain text, never respellings':'dialogue',
        'lipsync keeps native cues and makes soundFile repository-relative':'native',
        'Rhubarb resources are beside the executable through its link':'resources',
        'Rhubarb fatal exit 1 becomes exit 2 with its message and no changed output':'fatal',
        'lipsync refuses non-finite native JSON without changing output':'finite',
        'live Rhubarb recognises the joined espeak voice and stores a relative soundFile':'live',
    }
    def verdict(label, good, detail=''):
        print(('ok ' if good else 'FAIL ') + label, flush=True)
        if not good: print(detail, flush=True)
        key = labels.get(label,'guards')
        results[key] = results.get(key,True) and good
    def skip(label, reason):
        record('mouth.live','skip'); record('mouth.live.reason',reason)
    def cli(*args):
        code, stdout, stderr = M.cli_split(*args)
        return code, stdout + stderr
    with M.hermetic_git(out / 'mouth-gitconfig'):
        M.test_lipsync(verdict,skip,cli,root,True)
    for key, good in results.items(): record('mouth.' + key,'yes' if good else 'no')
PY
  rec mouth.status "$st"
  if [[ "$(awk -F '\t' '$1 == "mouth.live" {print $2}' "$RESULTS")" == skip ]]; then
    why="$(awk -F '\t' '$1 == "mouth.live.reason" {print $2}' "$RESULTS")"
    skip_step 21 "Rhubarb live lip sync" "$why"
  fi
}

# ── 24. separate cue lists, events and author-owned audio links ──
smoke_cues() {
  local st=0
  PYTHONDONTWRITEBYTECODE=1 python3 - "$T" "$OUT" "$RESULTS" \
    >"$OUT/cues-fixture.log" 2>&1 <<'PYCODE' || st=$?
import sys
from pathlib import Path
root, out, receipt = map(Path, sys.argv[1:4])
sys.path.insert(0, str(root / 'toolkit'))
import media as M
import media_common as C
C.ROOT = root
results = {}
labels = {
    'cues keep exact JSON times and print enclosing MM:SS with escaped cells': 'times',
    'cues preserve separate beat, board, line and original word lists': 'lists',
    'cues retain delivery instructions at actual word anchors without inventing sound duration': 'delivery',
    'cues resolve sound and music IDs from tracked audio rows including offset fades and ducking': 'audio',
    'cues report an unmatched board with null times and exit one': 'unmatched',
    'cues report untimed words and leave their board times null': 'untimed',
    'cues refuse non-finite word data without replacing an output': 'finite',
}
def verdict(label, good, detail=''):
    print(('ok ' if good else 'FAIL ') + label, flush=True)
    if not good: print(detail, flush=True)
    key = labels.get(label, 'links' if 'audio links' in label else
                     'boards' if '-column boards' in label else 'guards')
    results[key] = results.get(key, True) and good
def cli(*args):
    code, stdout, stderr = M.cli_split(*args)
    return code, stdout + stderr
with M.hermetic_git(out / 'cues-gitconfig'):
    M.test_cues(verdict, cli, root, True)
with receipt.open('a') as f:
    for key, good in results.items(): f.write('cues.' + key + '\t' + ('yes' if good else 'no') + '\n')
PYCODE
  rec cues.status "$st"
}

smoke_voice() {
  local p="916-smoke-voice" gen="$T/production/src/voiceover/generated"
  mkdir -p "$gen/$p/takes"
  ff -f lavfi -i 'sine=frequency=440:sample_rate=8000:duration=0.2' -c:a pcm_s16le -f s16le "$gen/$p.s01.t1.pcm"
  ff -f lavfi -i 'sine=frequency=880:sample_rate=8000:duration=0.17' -c:a pcm_s16le -f s16le "$gen/$p/takes/fresh.mp3"
  HOME="$GHOME" GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1 python3 - "$T" "$p" > "$OUT/voice.results" <<'PY'
import json, math, os, subprocess, sys, wave
from pathlib import Path
root, piece = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(root / 'toolkit'))
import media_common as C
C.ROOT = root
def record(key, passed): print(key + '\t' + ('yes' if passed else 'no'))
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
def cli(*args):
    result = subprocess.run([sys.executable, 'toolkit/media.py', *map(str, args)], cwd=root, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr
reg = root / C.VOICEOVER / (piece + '.toml')
script = root / C.PIECES / piece / 'script.md'
write(script, '## 1. Opening\n\nVO: {whispers} The ferry is late.\nVO: It leaves at dawn.\n')
header = '[voiceover]\npiece = "' + piece + '"\nmodel_id = "eleven_v4"\noutput_format = "pcm_8000"\n'
def segment(sid, line, text, take, file, pause, status):
    return ('\n[[segment]]\nid = "' + sid + '"\nscript_lines = "' + line + '"\ntext = "' + text
            + '"\nrequest = "' + text + '"\ntake = ' + str(take) + '\nfile = "' + file
            + '"\ncharacters = 0\npause_after = ' + str(pause) + '\nstatus = "' + status + '"\narchived = "F0001"\n')
write(reg, header + segment('s01','1.1','The ferry is late.',1,'generated/' + piece + '.s01.t1.pcm',0.16,'approved')
      + segment('s02','1.2','It leaves at dawn.',0,'',0.03,''))
before = reg.read_bytes()
known_files = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
code, text = cli('speak','plan',piece)
record('voice.plan', code == 0 and '1 calls' in text and '[whispers]' not in text and 's01:' not in text
       and 'credits' not in text.lower() and 'characters' in text and reg.read_bytes() == before
       and (root / C.VO_GENERATED / piece / 'takes').is_dir()
       and known_files == {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()})
code, text = cli('speak','plan',piece,'--segment','s01')
record('voice.tags', code == 0 and '[whispers] The ferry is late.' in text and '1 calls' in text)
code, text = cli('speak','plan','--trial','candidate')
trial = root / C.VO_GENERATED / 'voice-trials' / 'candidate'
record('voice.trial', code == 0 and trial.is_dir() and not list(trial.iterdir()) and reg.read_bytes() == before)
# A re-roll starts with a flat t1, named by its row; take add must pick t2 in takes/.
fresh = root / C.VO_GENERATED / piece / 'takes' / 'fresh.mp3'
code, text = cli('take','add',fresh,'--piece',piece,'--segment','s01')
data = C.load_toml(reg)
s = data['segment'][0]
record('voice.take', code == 0 and s['take'] == 2 and s['status'] == 'generated' and not s['archived']
       and s['file'] == 'generated/' + piece + '/takes/' + piece + '.s01.t2.pcm'
       and (root / C.VO_GENERATED / (piece + '.s01.t1.pcm')).is_file())
# Restore the first tone and use the re-roll's tone for s02: the row's file controls each join.
write(reg, header + segment('s01','1.1','The ferry is late.',1,'generated/' + piece + '.s01.t1.pcm',0.16,'approved')
      + segment('s02','1.2','It leaves at dawn.',2,s['file'],0.03,'approved'))
code, text = cli('voice','join',piece)
voice = root / C.PROD_RENDERS / piece / (piece + '.voice.wav')
joined = False
if voice.is_file():
    with wave.open(str(voice)) as wav:
        joined = wav.getnchannels() == 1 and wav.getsampwidth() == 2 and wav.getframerate() == 8000
        joined = joined and wav.readframes(wav.getnframes()) == (root / C.VO_GENERATED / (piece + '.s01.t1.pcm')).read_bytes() + bytes(2560) + (root / C.VOICEOVER / s['file']).read_bytes() + bytes(480)
record('voice.join', code == 0 and joined)
held = reg.read_text()
write(reg, held.replace('status = "approved"','status = "generated"',1))
other = voice.with_name('pending.wav')
code, text = cli('voice','join',piece,'-o',other)
record('voice.pending', code == 1 and not other.exists() and 's01' in text)
write(reg, held)
code, text = cli('levels',piece)
out = voice.parent / 'timing' / (piece + '.levels.json')
try:
    values = json.loads(out.read_text())['windows']
    finite = len(values) == 6 and values[2]['rms_dbfs'] == -120 and abs(values[-1]['end'] - 0.56) < 1e-9
    finite = finite and all(math.isfinite(row['rms_dbfs']) for row in values)
except Exception: finite = False
record('voice.levels', code == 0 and finite and not (root / C.TIMING / out.name).exists())
# The output helper is the writer that later timing commands own. Test each refusal independently.
tracked = root / C.TIMING / (piece + '.mouth.json')
def writer():
    try:
        target = C.output_path(out, tracked, tracked_timing=(piece, 'mouth.json'))
        C.replace_file(target, b'{"mouthCues": []}\n')
        return 0
    except C.Fatal: return 2
def git(*args):
    subprocess.run(['git','-c','user.name=Fixture Author','-c','user.email=fixture@example.invalid',*args],cwd=C.ROOT,check=True,capture_output=True)
write(tracked, 'first\n')
git('add', str(tracked.relative_to(root)))
git('commit','-qm','timing fixture')
record('guard.clean', writer() == 0 and tracked.read_bytes() == b'{"mouthCues": []}\n'
       and not tracked.with_name('.' + tracked.name + '.partial').exists())
held = tracked.read_bytes()
record('guard.dirty', writer() == 2 and tracked.read_bytes() == held)
git('add', str(tracked.relative_to(root)))
record('guard.staged', writer() == 2 and tracked.read_bytes() == held)
git('reset','--',str(tracked.relative_to(root)))
git('rm','--cached','-f',str(tracked.relative_to(root)))
record('guard.untracked', writer() == 2 and tracked.read_bytes() == held)
elsewhere = root.parent / 'outside-git'
C.ROOT = elsewhere
tracked = elsewhere / C.TIMING / (piece + '.mouth.json')
write(tracked, 'outside\n')
record('guard.outside', writer() == 2 and tracked.read_text() == 'outside\n')
C.ROOT = root
other = root / C.TIMING / (piece + '.levels.json')
write(other,'keep\n')
git('add',str(other.relative_to(root)))
git('commit','-qm','other output')
tracked = other
record('guard.other', writer() == 2 and other.read_text() == 'keep\n')
PY
  local key value
  while IFS=$'\t' read -r key value; do rec "$key" "$value"; done < "$OUT/voice.results"
}

smoke_frames() { # $@ = the answered rows
  local st a="$T/production/src/assets/smoke-frames" k e="" m="$T/production/src/renders/$P_FRAMES/$P_FRAMES.master.mp4" kind min max atr
  mkdir -p "$a" "$T/production/src/edits"
  ff -f lavfi -i "color=c=black:s=320x180:r=1,format=rgb24,geq=r='10+9*N':g='245-9*N':b='60+120*mod(N,2)'" -frames:v 25 "$a/s%02d.png"
  ff -f lavfi -i "color=c=black@0.0:s=320x180,format=rgba,drawbox=x=0:y=0:w=320:h=90:color=0xf0f0f0@1.0:t=fill:replace=1" -frames:v 1 "$a/mark.png"
  ff -f lavfi -i "sine=frequency=330:sample_rate=48000:duration=6" -ac 2 "$a/tone.wav"
  {
    printf '[edit]\npiece = "%s"\nsize = "320x180"\n' "$P_FRAMES"
    for k in $(seq -w 1 25); do printf '\n[[clip]]\nsource = "production/src/assets/smoke-frames/s%s.png"\nseconds = 0.16\n' "$k"; done
    printf '\n[[overlay]]\nsource = "production/src/assets/smoke-frames/mark.png"\nat = "00:00:00.480"\nuntil = "00:00:00.800"\n'
    printf '\n[[audio]]\nsource = "production/src/assets/smoke-frames/tone.wav"\nrole = "music"\n'
  } > "$T/production/src/edits/$P_FRAMES.toml"
  st=0; tk frames assemble "production/src/edits/$P_FRAMES.toml" || st=$?
  rec frames.status "$st"; rec frames.tail "$(tail_of frames)"
  [[ -f "$m" ]] || return 0
  { read -r k; rec frames.count "$k"; read -r k; rec frames.order "$k"; read -r k; rec frames.overlay "$k"; } < <(frame_grid "$m")
  # The first video deliverable with sound that a 4-second master fits (min_seconds and max_seconds).
  while IFS=$'\t' read -r k kind _ _ _ _ _ min max _ _ atr; do
    [[ "$kind" == video && "$atr" != 0 ]] || continue
    awk -v a="$min" -v b="$max" 'BEGIN { exit !((a == "-" || a <= 4) && (b == "-" || b >= 4)) }' && { e="$k"; break; }
  done < <(printf '%s\n' "$@")
  if [[ -z "$e" ]]; then na_step 25b "no video deliverable with sound that a 4-second master fits: the stills master is not encoded"; return 0; fi
  st=0; tk frames.enc encode "$m" --deliverable "$e" --frame crop -o "$OUT/c25.encoded.mp4" || st=$?
  rec frames.enc.key "$e"; rec frames.enc.status "$st"; rec frames.enc.tail "$(tail_of frames.enc)"
  [[ -f "$OUT/c25.encoded.mp4" ]] && rec frames.enc.ends "$(stream_ends "$OUT/c25.encoded.mp4")"
  return 0
}

# Three lines about a master of 25 stills of 0.16 s at 30 fps with an overlay from 0.480 s to
# 0.800 s: its frame count; 'ok' or the first frame whose lower half shows another still than the
# one its running total puts there; 'ok' or the frames whose upper half shows the overlay.
frame_grid() { # $1 = master
  python3 - "$1" <<'PY'
import subprocess, sys
m, n, secs, fps, at, until = sys.argv[1], 25, 0.16, 30, 0.48, 0.80
def patches(crop):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", m, "-vf", f"crop={crop},format=rgb24,scale=1:1:flags=area",
                        "-fps_mode", "passthrough", "-f", "rawvideo", "-"], capture_output=True)
    return [tuple(p.stdout[k:k + 3]) for k in range(0, len(p.stdout) - 2, 3)]
near = lambda t: int(t * fps + 0.5 + 1e-9)
colours = [(10 + 9 * k, 245 - 9 * k, 60 + 120 * (k % 2)) for k in range(n)]
bounds = [near(secs * k) for k in range(n + 1)]
due = [k for k in range(n) for _ in range(bounds[k + 1] - bounds[k])]
low, top = patches("16:16:152:127"), patches("16:16:152:37")
print(len(low))
got = [min(range(n), key=lambda k: sum((a - b) ** 2 for a, b in zip(c, colours[k]))) for c in low]
bad = next((f for f in range(min(len(got), len(due))) if got[f] != due[f]), None)
print("ok" if bad is None and len(got) == len(due) else
      f"frame {bad} shows still {got[bad] + 1} where still {due[bad] + 1} is due" if bad is not None
      else f"{len(got)} frames for the {len(due)} the stills' running totals make")
on = [f for f, c in enumerate(top) if max(abs(x - 240) for x in c) <= 24]
a, b = near(at), near(until)
print("ok" if on == list(range(a, b)) else
      f"on frames {on[0]}-{on[-1]} ({len(on)} frames), wants {a}-{b - 1}" if on else f"on no frame, wants {a}-{b - 1}")
PY
}

stream_ends() { # $1 = a render → "video_end audio_end", each from its stream's own start and duration
  ffprobe -v error -show_entries stream=codec_type,start_time,duration -of csv=p=0 "$1" 2>/dev/null \
    | awk -F, '$1 == "video" { v = $2 + $3 } $1 == "audio" { s = $2 + $3 } END { printf "%.3f %.3f", v, s }'
}

# ── The judging: reads RES, fills FINDINGS and NOTES ─────────────────────────

NOTES=()
num_eq() { awk -v a="$1" -v b="$2" -v t="${3:-0.0005}" 'BEGIN { d = a - b; if (d < 0) d = -d; exit !(a == a + 0 && d <= t) }'; }

run_checks() {
  FINDINGS=(); NOTES=()
  local k v L="[$NAME]" kind w h vc ac rate dur fw fh fv fpix fa frate fdur want st n ct amin
  if [[ "${RES[answers]:-}" == missing ]]; then finding "check 2 — $L the render has no $SM_ANSWERS_FILE, so no deliverable could be chosen"; return 0; fi
  for k in "${!RES[@]}"; do
    case "$k" in skip.*) NOTES+=("skipped: ${RES[$k]}") ;; na.*) NOTES+=("n/a: ${RES[$k]}") ;; esac
  done

  # 1
  [[ "${RES[selftest.media.py]:-}" == missing ]] && finding "check 1 — $L toolkit/media.py is missing"
  for k in "${!RES[@]}"; do
    [[ "$k" =~ ^selftest\.([a-z_]+\.py)$ ]] || continue
    v="${RES[$k]}"; [[ "$v" == 0 || "$v" == missing ]] && continue
    finding "check 1 — $L python3 toolkit/${BASH_REMATCH[1]} --self-test failed (exit $v): ${RES[$k.tail]:-}"
  done

  # 2
  n=0
  for k in "${!RES[@]}"; do
    [[ "$k" =~ ^cut\.(.+)\.status$ ]] || continue
    local key="${BASH_REMATCH[1]}" bad=""
    n=$((n + 1))
    st="${RES[$k]}"
    if [[ "$st" != 0 ]]; then finding "check 2 — $L cut --deliverable $key failed (exit $st): ${RES[cut.$key.tail]:-}"; continue; fi
    read -r kind w h vc ac rate want <<< "${RES[cut.$key.want]:-}"
    read -r fw fh fv fpix fa frate _ fdur <<< "${RES[cut.$key.facts]:-- - - - - - - 0}"
    if [[ "$kind" == video ]]; then
      [[ "$fw" == "$w" && "$fh" == "$h" ]] || bad+=" picture ${fw}x${fh}, wants ${w}x${h};"
      [[ "$vc" == - || "$fv" == "$vc" ]] || bad+=" video $fv, wants $vc;"
      [[ "$fpix" == yuv420p ]] || bad+=" pixel format $fpix;"
    else
      [[ "$fv" == - ]] || bad+=" a picture stream in an audio deliverable;"
    fi
    if [[ "$ac" == none ]]; then
      [[ "$fa" == - ]] || bad+=" a sound track ($fa) in a deliverable with audio_tracks = 0;"
    else
      [[ "$ac" == - || "$fa" == "$ac" ]] || bad+=" audio $fa, wants $ac;"
    fi
    [[ "$rate" == - || "$frate" == "$rate" ]] || bad+=" ${frate} Hz, wants $rate;"
    num_eq "$fdur" "$want" 0.1 || bad+=" lasts $fdur s, cut to $want;"
    [[ -z "$bad" ]] || finding "check 2 — $L cut --deliverable $key does not match its preset:${bad%;}"
  done
  [[ "${RES[deliverables]:-0}" -gt 0 ]] || finding "check 2 — $L the answers name no deliverable in toolkit/data/platforms.toml"
  if [[ -z "${RES[skip.2]:-}" && "$n" -eq 0 && "${RES[deliverables]:-0}" -gt 0 ]]; then
    finding "check 2 — $L no video or audio deliverable of the answers was cut"
  fi

  # 3
  if [[ -n "${RES[burn.status]:-}" ]]; then
    if [[ "${RES[burn.status]}" != 0 ]]; then finding "check 3 — $L captions burn for ${RES[burn.key]} failed (exit ${RES[burn.status]}): ${RES[burn.tail]:-}"
    elif [[ "${RES[burn.size]:-}" != "${RES[burn.want]:-}" || "${RES[burn.playres]:-}" != "${RES[burn.want]:-}" ]]; then
      finding "check 3 — $L the burn for ${RES[burn.key]} is ${RES[burn.size]:-?} with PlayRes ${RES[burn.playres]:-none}; both must be ${RES[burn.want]:-?}"
    fi
    if [[ "${RES[font.status]:-}" != 1 || "${RES[font.said]:-}" != yes ]]; then
      finding "check 3 — $L a burn whose caption font is not installed did not fail saying the font fell back (exit ${RES[font.status]:-?})"
    fi
  fi

  # 4
  for k in "${!RES[@]}"; do
    [[ "$k" =~ ^card\.(.+)\.status$ && "${BASH_REMATCH[1]}" != alpha ]] || continue
    local key="${BASH_REMATCH[1]}"
    if [[ "${RES[$k]}" != 0 ]]; then finding "check 4 — $L card.py render --deliverable $key failed (exit ${RES[$k]})"
    elif [[ "${RES[card.$key.size]:-}" != "${RES[card.$key.want]:-}" ]]; then
      finding "check 4 — $L card.py render --deliverable $key wrote ${RES[card.$key.size]:-nothing}, not ${RES[card.$key.want]:-?}"
    fi
  done
  if [[ -n "${RES[card.alpha.status]:-}" ]]; then
    read -r _ ct amin <<< "${RES[card.alpha.facts]:-0x0 0 255}"
    if [[ "${RES[card.alpha.status]}" != 0 ]]; then finding "check 4 — $L card.py render --transparent failed (exit ${RES[card.alpha.status]})"
    elif [[ "$ct" != 6 || "${amin:-255}" -ge 255 ]]; then finding "check 4 — $L card.py render --transparent wrote no transparent pixel (PNG colour type $ct, minimum alpha ${amin:-255})"; fi
  fi

  # 5
  for k in social podcast; do
    [[ -n "${RES[loud.$k.status]:-}" ]] || continue
    if [[ "${RES[loud.$k.status]}" != 0 ]]; then finding "check 5 — $L loudness normalise --target $k failed (exit ${RES[loud.$k.status]})"
    elif ! num_eq "${RES[loud.$k.lufs]:-nan}" "${RES[loud.$k.target]:-nan}" 1.0; then
      finding "check 5 — $L loudness normalise --target $k measures ${RES[loud.$k.lufs]:-nan} LUFS, not within 1 LU of ${RES[loud.$k.target]:-?}"
    fi
  done

  # 6
  if [[ -n "${RES[abmaster.status]:-}" ]]; then
    if [[ "${RES[abmaster.status]}" != 0 ]]; then finding "check 6 — $L audiobook master failed on a synthetic chapter (exit ${RES[abmaster.status]}): ${RES[abmaster.tail]:-}"
    else
      [[ "${RES[abcheck.status]:-}" == 0 ]] || finding "check 6 — $L audiobook check fails the chapter audiobook master just made (exit ${RES[abcheck.status]:-?})"
      [[ "${RES[abhot.status]:-}" == 1 ]] || finding "check 6 — $L audiobook check passed a hot-peak copy of the master (exit ${RES[abhot.status]:-?})"
    fi
  fi

  # 7
  if [[ -n "${RES[val.clean]:-}" ]]; then
    if [[ "${RES[val.clean]}" != 0 ]]; then finding "check 7 — $L captions check fails a clean SRT (exit ${RES[val.clean]}), so its mutations prove nothing"
    else
      [[ "${RES[val.line]:-}" == 1 ]] || finding "check 7 — $L captions check passed a 43-character line (exit ${RES[val.line]:-?})"
      [[ "${RES[val.cps]:-}" == 1 ]] || finding "check 7 — $L captions check passed 20 characters a second (exit ${RES[val.cps]:-?})"
    fi
  fi
  if [[ -n "${RES[val.aspect]:-}" && ( "${RES[val.aspect]}" != 1 || "${RES[val.aspect.said]:-}" != yes ) ]]; then
    finding "check 7 — $L a burn onto a 640x360 clip for ${RES[first_video]:-?} did not fail the deliverable's verification (exit ${RES[val.aspect]})"
  fi
  if [[ -n "${RES[val.long]:-}" && ( "${RES[val.long]}" != 1 || "${RES[val.long.rendered]:-}" == yes ) ]]; then
    finding "check 7 — $L an over-long cut for ${RES[val.long.key]:-?} did not fail before it rendered (exit ${RES[val.long]}, rendered ${RES[val.long.rendered]:-?})"
  fi

  # 8
  [[ -z "${RES[git.notignored]:-}" ]] || finding "check 8 — $L Git would track generated output: ${RES[git.notignored]}"
  [[ -z "${RES[git.readme.ignored]:-}" ]] || finding "check 8 — $L Git ignores a folder's README.md: ${RES[git.readme.ignored]}"
  [[ -z "${RES[git.tracked.ignored]:-}" ]] || finding "check 8 — $L Git ignores a piece's tracked timing or scene file, which stays flat beside renders/ and is committed (D64): ${RES[git.tracked.ignored]}"
  [[ "${RES[git.attr.large]:-}" == lfs ]] || finding "check 8 — $L git check-attr reports filter '${RES[git.attr.large]:-?}' under brand/src/exports/large/, not lfs"
  [[ "${RES[git.attr.pair]:-}" != *lfs* ]] || finding "check 8 — $L the pair of brand/src/exports/large/ is marked for LFS"
  if [[ "${RES[git.fresh]:-}" != 0 ]]; then finding "check 8 — $L media.py check is not clean on the fresh project (exit ${RES[git.fresh]:-?}), so its LFS findings prove nothing"
  else
    [[ "${RES[git.blob]:-}" == 1 && "${RES[git.blob.said]:-}" == yes ]] || finding "check 8 — $L media.py check did not flag an LFS-marked file committed as a plain blob (exit ${RES[git.blob]:-?})"
    [[ "${RES[git.fake]:-}" == 1 && "${RES[git.fake.said]:-}" == yes ]] || finding "check 8 — $L media.py check did not flag an LFS-marked file while git-lfs answers but no filter is configured (exit ${RES[git.fake]:-?})"
  fi
  if [[ "${RES[git.tripwire.add]:-}" == none ]]; then finding "check 8 — $L copier.yml carries no LFS tripwire task (a command testing filter.lfs.process), so nothing makes git add of an LFS-marked file fail"
  elif [[ "${RES[git.tripwire.add]:-0}" == 0 ]]; then finding "check 8 — $L with the copier.yml tripwire applied, git add of an LFS-marked file still succeeded"; fi

  # 9
  if [[ -n "${RES[edl.status]:-}" ]]; then
    if [[ "${RES[edl.status]}" != 0 ]]; then finding "check 9 — $L assemble failed on the synthetic edit (exit ${RES[edl.status]}): ${RES[edl.tail]:-}"
    else
      [[ "${RES[edl.where]:-yes}" == yes ]] || finding "check 9 — $L assemble did not write the master to production/src/renders/$P_EDIT/$P_EDIT.master.mp4, its piece's own folder (D64)"
      [[ -z "${RES[edl.cards]:-}" || "${RES[edl.cards]}" == ok ]] \
        || finding "check 9 — $L one card used as a clip and as an overlay at one size did not keep both renders, the overlay's .transparent, in its piece's cards/ folder (D47, D64): ${RES[edl.cards]}"
      read -r _ _ _ _ _ _ _ dur <<< "${RES[edl.facts]:-- - - - - - - 0}"
      num_eq "$dur" "${RES[edl.expect]}" 0.1 || finding "check 9 — $L the assembled master lasts $dur s, not ${RES[edl.expect]}"
      num_eq "${RES[edl.lufs]:-nan}" "${RES[loud.social.target]:--14}" 1.0 || finding "check 9 — $L the assembled master measures ${RES[edl.lufs]:-nan} LUFS, not within 1 LU of the social target"
      for k in "${!RES[@]}"; do
        [[ "$k" =~ ^ecut\.(.+)\.status$ ]] || continue
        local key="${BASH_REMATCH[1]}"
        if [[ "${RES[$k]}" != 0 ]]; then finding "check 9 — $L cut of the master for $key failed (exit ${RES[$k]}): ${RES[ecut.$key.tail]:-}"
        elif ! num_eq "${RES[ecut.$key.dur]:-0}" 4.0 0.1; then finding "check 9 — $L cut of the master for $key lasts ${RES[ecut.$key.dur]:-?} s, not 4.000"; fi
      done
    fi
    if [[ "${RES[segs.status]:-}" != 0 ]]; then finding "check 9 — $L captions from-segments failed (exit ${RES[segs.status]:-?}): ${RES[segs.tail]:-}"
    else
      if ! num_eq "${RES[segs.first]:-nan}" 0.2 0.0005 || [[ "${RES[segs.hasjoin]:-}" != yes ]] || ! num_eq "${RES[segs.lastend]:-nan}" "${RES[segs.lastwant]:-nan}" 0.002 || [[ "${RES[segs.cues]:-0}" -lt 4 ]]; then
        finding "check 9 — $L from-segments cues are not exact at the joins (first ${RES[segs.first]:-?} for 0.200, a cue at ${RES[segs.join]:-?}: ${RES[segs.hasjoin]:-?}, last end ${RES[segs.lastend]:-?} for ${RES[segs.lastwant]:-?}, ${RES[segs.cues]:-0} cue(s) for two segments of several)"
      fi
      if [[ "${RES[retime.status]:-}" != 0 || "${RES[retime.inside]:-}" != yes ]] || ! num_eq "${RES[retime.first]:-nan}" "${RES[retime.want]:-nan}" 0.002; then
        finding "check 9 — $L captions retime to a cut 00:00:01–00:00:04 did not shift, clip and drop (exit ${RES[retime.status]:-?}; first cue ${RES[retime.first]:-?} for ${RES[retime.want]:-?}; inside: ${RES[retime.inside]:-?})"
      fi
      if [[ -n "${RES[eburn.status]:-}" ]]; then
        if [[ "${RES[eburn.status]}" != 0 ]]; then finding "check 9 — $L the burn of the retimed captions onto the cut failed (exit ${RES[eburn.status]}): ${RES[eburn.tail]:-}"
        elif ! num_eq "${RES[eburn.dur]:-0}" 3.0 0.1; then finding "check 9 — $L the burned cut lasts ${RES[eburn.dur]:-?} s, not 3.000"; fi
      fi
    fi
  fi

  # 10
  if [[ -n "${RES[amaster.status]:-}" ]]; then
    read -r _ _ fv _ fa _ _ fdur <<< "${RES[amaster.facts]:-- - - - - - - 0}"
    if [[ "${RES[amaster.status]}" != 0 ]]; then finding "check 10 — $L assemble failed on an audio master (exit ${RES[amaster.status]}): ${RES[amaster.tail]:-}"
    elif [[ "$fv" != - || "$fa" == - ]] || ! num_eq "$fdur" "${RES[amaster.expect]}" 0.05; then
      finding "check 10 — $L the audio master is not sound only at ${RES[amaster.expect]} s (picture $fv, sound $fa, $fdur s)"
    fi
  fi

  # 11
  [[ "${RES[script.status]:-}" == 0 && "${RES[script.total]:-}" == yes ]] || finding "check 11 — $L script time on a fixture script did not report its total (exit ${RES[script.status]:-?})"
  [[ "${RES[footage.add]:-}" == 0 && "${RES[footage.kept]:-}" == yes && "${RES[footage.copied]:-}" == yes ]] \
    || finding "check 11 — $L footage add did not copy the file into raw/ and leave the original (exit ${RES[footage.add]:-?}, original kept: ${RES[footage.kept]:-?}, copied: ${RES[footage.copied]:-?})"
  [[ "${RES[footage.dup]:-0}" != 0 ]] || finding "check 11 — $L footage add accepted a duplicate hash"
  [[ "${RES[footage.verify]:-}" == 0 ]] || finding "check 11 — $L footage verify fails a true mirror (exit ${RES[footage.verify]:-?})"
  [[ "${RES[footage.changed]:-}" == 1 ]] || finding "check 11 — $L footage verify passed a mirror with a changed byte (exit ${RES[footage.changed]:-?})"
  for k in .mp3 .pcm; do
    if [[ "${RES[take$k.status]:-}" != 0 || "${RES[take$k.named]:-}" != yes || "${RES[take$k.register]:-}" != yes || "${RES[take$k.credits]:-0}" != 1 ]]; then
      finding "check 11 — $L take add of a fake ${k#.} take did not rename it in its piece's takes/ folder and write one register row naming it there and one credits-log row (exit ${RES[take$k.status]:-?}; named ${RES[take$k.named]:-?}; register ${RES[take$k.register]:-?}; credits rows ${RES[take$k.credits]:-0})"
    fi
  done
  [[ "${RES[take.flat]:-}" == yes ]] \
    || finding "check 11 — $L take add did not number the take in $P_TAKE/takes/ t2, after the flat t1 an earlier release left in generated/, leaving that one where it was (D65)"

  # 12
  if [[ -n "${RES[abtext.status]:-}" ]]; then
    if [[ "${RES[abtext.status]}" != 1 || "${RES[abtext.listed]:-}" != yes ]]; then
      finding "check 12 — $L audiobook text did not list the unpronounced word '$CONSTRUCTED' with exit 1 (exit ${RES[abtext.status]})"
    elif [[ "${RES[abtext.clean]:-}" != yes ]]; then finding "check 12 — $L audiobook text left markup in a chunk (a marker, comment, citation key, div, span or pause mark)"
    elif [[ "${RES[abtext.pause]:-}" != yes ]]; then finding "check 12 — $L audiobook text did not end a chunk at the scene break with 2 s recorded in the sidecar (ruling T3)"; fi
  fi

  # 13
  if [[ -n "${RES[align.anchors]:-}" ]]; then
    [[ "${RES[align.anchors]}" == 0 && "${RES[align.inside]:-}" == yes ]] || finding "check 13 — $L captions align --anchors did not keep every cue of a beat inside its beat (exit ${RES[align.anchors]})"
    [[ "${RES[align.lines]:-}" == 0 && "${RES[align.placed]:-0}" == 2 ]] || finding "check 13 — $L captions align --lines placed ${RES[align.placed]:-0} of 2 cues of the cut (exit ${RES[align.lines]:-?})"
  fi

  # 14
  [[ "${RES[setup.ask]:-}" == yes && "${RES[setup.base]:-}" == yes ]] \
    || finding "check 14 — $L check --setup did not report the missing ask $GONE_ASK and the base path outside the repository (ask: ${RES[setup.ask]:-?}; base path: ${RES[setup.base]:-?})"
  [[ "${RES[setup.leak]:-}" != yes ]] || finding "check 14 — $L check --setup printed a value from ~/.claude.json it must never print (the API key or the account)"
  [[ "${RES[setup.encoders]:-no}" == yes ]] \
    || finding "check 14 — $L check --setup does not name the optional encoders image needs (libwebp for WebP; an AV1 encoder and the avif muxer for AVIF)"

  # 15
  local key fmt bad pix nst plays one total loop frames bytes gw gh want_plays mx fpsmax maxb a_frames a_one rrender rbytes rsecs
  for k in "${!RES[@]}"; do
    [[ "$k" =~ ^img\.(.+)\.(jpg|png|webp|avif)\.status$ ]] || continue
    key="${BASH_REMATCH[1]}"; fmt="${BASH_REMATCH[2]}"; bad=""
    if [[ "${RES[$k]}" != 0 ]]; then finding "check 15 — $L image --deliverable $key --format $fmt failed (exit ${RES[$k]}): ${RES[img.$key.$fmt.tail]:-}"; continue; fi
    read -r w _ <<< "${RES[img.$key.want]:-? -}"
    read -r gw fv pix bytes nst <<< "${RES[img.$key.$fmt.facts]:-0x0 - - 0 0}"
    [[ "$gw" == "$w" ]] || bad+=" ${gw}, wants $w;"
    [[ "$fv" == "$(codec_for "$fmt")" ]] || bad+=" codec $fv, wants $(codec_for "$fmt");"
    if [[ "$(cut -d' ' -f2 <<< "${RES[img.$key.want]:-}")" == false ]] \
       && { [[ "$pix" =~ ^(rgba|bgra|argb|abgr|ya|yuva|gbrap|pal8a) ]] || [[ "$fv" == av1 && "${nst:-1}" -gt 1 ]]; }; then
      bad+=" kept its alpha channel ($pix), though the table says alpha = false;"
    fi
    [[ -z "$bad" ]] || finding "check 15 — $L image --deliverable $key --format $fmt does not match its preset:${bad%;}"
  done
  if [[ -n "${RES[img.shape.status]:-}" && ( "${RES[img.shape.status]}" == 0 || "${RES[img.shape.written]:-}" == yes ) ]]; then
    finding "check 15 — $L image --deliverable ${RES[img.shape.key]:-?} accepted a source of another shape without --frame (exit ${RES[img.shape.status]}, written ${RES[img.shape.written]:-?})"
  fi
  if [[ -n "${RES[img.poster.status]:-}" ]]; then
    if [[ "${RES[img.poster.status]}" != 0 ]]; then finding "check 15 — $L image --deliverable ${RES[img.poster.key]:-?} --at a video's frame failed (exit ${RES[img.poster.status]}): ${RES[img.poster.tail]:-}"
    elif [[ "${RES[img.poster.size]:-}" != "${RES[img.poster.want]:-}" ]]; then finding "check 15 — $L the poster for ${RES[img.poster.key]:-?} is ${RES[img.poster.size]:-nothing}, not ${RES[img.poster.want]:-?}"; fi
  fi
  if [[ -n "${RES[img.maxsize.status]:-}" && "${RES[img.maxsize.status]}" != 1 ]]; then
    finding "check 15 — $L image --deliverable ${RES[img.maxsize.key]:-?} with max_size overridden to 1 KB did not fail its verification (exit ${RES[img.maxsize.status]})"
  fi

  # 16
  if [[ -n "${RES[gif.key]:-}" ]]; then
    read -r w h mx fpsmax maxb <<< "${RES[gif.want]:-0 0 - - 0}"
    if [[ "${RES[gif.a.status]:-}" != 0 ]]; then finding "check 16 — $L cut --deliverable ${RES[gif.key]} --overlay of a 2-second range failed (exit ${RES[gif.a.status]:-?}): ${RES[gif.a.tail]:-}"
    else
      bad=""; read -r gw gh frames one loop bytes <<< "${RES[gif.a.facts]:-0 0 0 0 -1 0}"
      plays="$(gif_plays "$loop")"
      [[ "$gw" == "$w" && "$gh" == "$h" ]] || bad+=" ${gw}x${gh}, wants ${w}x${h};"
      num_eq "$one" 2.0 0.15 || bad+=" one play lasts $one s, cut to 2.000;"
      if [[ "$plays" == inf ]]; then bad+=" it loops for ever;"
      else
        if [[ "$mx" != - ]]; then
          want_plays="$(awk -v m="$mx" 'BEGIN { printf "%d", m / 2.0 + 1e-9 }')"
          [[ "$plays" == "$want_plays" ]] || bad+=" plays $plays times, wants floor($mx / 2) = $want_plays;"
          total="$(awk -v p="$plays" -v o="$one" 'BEGIN { printf "%.3f", p * o }')"
          awk -v t="$total" -v m="$mx" 'BEGIN { exit !(t <= m + 0.05) }' || bad+=" plays for $total s, over max_seconds $mx;"
        fi
      fi
      [[ "$fpsmax" == - ]] || awk -v f="$frames" -v o="$one" -v m="$fpsmax" 'BEGIN { exit !(o > 0 && f / o <= m + 0.5) }' || bad+=" $frames frames in $one s, over fps_max $fpsmax;"
      [[ "${maxb:-0}" -le 0 || "$bytes" -le "$maxb" ]] || bad+=" $bytes bytes, over max_size;"
      [[ "${RES[gif.a.overlay]:-}" == yes ]] || bad+=" the overlay is not on its first frame;"
      [[ -z "$bad" ]] || finding "check 16 — $L the GIF preview of a 2-second range does not match its preset:${bad%;}"
    fi
    if [[ -n "${RES[gif.b.facts]:-}" && "$mx" != - ]]; then
      read -r _ _ _ one loop _ <<< "${RES[gif.b.facts]}"
      plays="$(gif_plays "$loop")"; want_plays="$(awk -v m="$mx" 'BEGIN { printf "%d", m / 3.0 + 1e-9 }')"
      [[ "$plays" == "$want_plays" ]] || finding "check 16 — $L the GIF preview of a 3-second range plays $plays times (loop count $loop), wants floor($mx / 3) = $want_plays"
    elif [[ -n "${RES[gif.b.status]:-}" && "${RES[gif.b.status]}" != 0 ]]; then
      finding "check 16 — $L cut --deliverable ${RES[gif.key]} of a 3-second range failed (exit ${RES[gif.b.status]})"
    fi
    if [[ -n "${RES[gif.c.status]:-}" ]]; then
      if [[ "${RES[gif.c.status]}" != 0 ]]; then finding "check 16 — $L a GIF over max_size was not remade at a lower frame rate (exit ${RES[gif.c.status]}): ${RES[gif.c.tail]:-}"
      else
        read -r _ _ frames one _ bytes <<< "${RES[gif.c.facts]:-0 0 0 0 -1 0}"
        read -r _ _ a_frames a_one _ _ <<< "${RES[gif.a.facts]:-0 0 0 0 -1 0}"
        if ! awk -v a="$frames" -v b="$a_frames" 'BEGIN { exit !(a < b) }' || ! num_eq "$one" "$a_one" 0.15 || [[ "$bytes" -gt "${RES[gif.c.limit]:-0}" ]]; then
          finding "check 16 — $L the GIF remade under max_size is not the same play at a lower frame rate ($frames frames for $a_frames, $one s for $a_one, $bytes bytes for a ${RES[gif.c.limit]:-?}-byte limit)"
        fi
      fi
    fi
    [[ -z "${RES[gif.d.status]:-}" || "${RES[gif.d.status]}" == 2 ]] || finding "check 16 — $L an overlay of another size than the deliverable's was not refused with exit 2 (exit ${RES[gif.d.status]})"
    if [[ -n "${RES[gif.e.status]:-}" && ( "${RES[gif.e.status]}" != 1 || "${RES[gif.e.written]:-}" == yes ) ]]; then
      finding "check 16 — $L a GIF range longer than max_seconds did not fail before it rendered (exit ${RES[gif.e.status]}, written ${RES[gif.e.written]:-?})"
    fi
  fi

  # 17
  if [[ -n "${RES[loop.status]:-}" ]]; then
    if [[ "${RES[loop.status]}" != 0 ]]; then finding "check 17 — $L cut --deliverable ${RES[loop.key]:-?} (audio_tracks = 0) failed (exit ${RES[loop.status]}): ${RES[loop.tail]:-}"
    elif [[ "${RES[loop.audio]:-}" != - ]]; then finding "check 17 — $L the silent loop ${RES[loop.key]:-?} carries a sound track (${RES[loop.audio]:-?})"; fi
    case "${RES[loopmut.status]:-}" in
      1|"") ;;
      0) if [[ "${RES[loopmut.audio]:--}" != - ]]; then
           finding "check 17 — $L the verification passed a ${RES[loop.key]:-?} cut that kept its sound (an ffmpeg that ignores -an)"
         else NOTES+=("n/a: check 17's mutation kept no sound (the toolkit drops it without -an)"); fi ;;
      *) finding "check 17 — $L the mutated loop cut did not run to its verification (exit ${RES[loopmut.status]})" ;;
    esac
  fi
  if [[ -n "${RES[web.status]:-}" ]]; then
    if [[ "${RES[web.status]}" != 0 ]]; then finding "check 17 — $L encode --deliverable website.video failed (exit ${RES[web.status]}): ${RES[web.tail]:-}"
    elif [[ "${RES[web.moov]:-}" != yes ]]; then finding "check 17 — $L website.video was written with its index (moov) after the media data: a page cannot start playing it early"; fi
  fi

  # 18
  if [[ -n "${RES[feed.nofolder.status]:-}" ]]; then
    [[ "${RES[feed.nofolder.status]}" == 2 && "${RES[feed.nofolder.said]:-}" == yes ]] \
      || finding "check 18 — $L feed new without publishing/src/podcast/ did not exit 2 naming 'copier update -a .copier-answers.syntek-media.yml' (exit ${RES[feed.nofolder.status]})"
    [[ "${RES[feed.nofolder.made]:-no}" == no ]] || finding "check 18 — $L feed new created publishing/src/podcast/, a folder only copier update may add"
  fi
  if [[ -n "${RES[feed.skeleton]:-}" ]]; then
    [[ "${RES[feed.skeleton]}" == same ]] || finding "check 18 — $L the register skeleton fenced in publishing/src/podcast/CLAUDE.md is not media_feed.SKELETON's: ${RES[feed.skeleton]}"
    [[ "${RES[feed.spec.status]:-}" == 0 && "${RES[feed.spec.guid]:-}" == "$FEED_SPEC_GUID" ]] \
      || finding "check 18 — $L feed new --feed-url $FEED_SPEC_URL wrote podcast_guid ${RES[feed.spec.guid]:-none}, not the Podcasting 2.0 example's $FEED_SPEC_GUID (exit ${RES[feed.spec.status]:-?})"
  fi
  if [[ "${RES[feed.register]:-}" == missing ]]; then
    finding "check 18 — $L feed new wrote no publishing/src/podcast/$FEED_SHOW.toml (exit ${RES[feed.new.status]:-?}): ${RES[feed.new.tail]:-}"
  elif [[ -n "${RES[feed.new.status]:-}" ]]; then
    [[ "${RES[feed.new.status]}" == 0 ]] || finding "check 18 — $L feed new failed (exit ${RES[feed.new.status]}): ${RES[feed.new.tail]:-}"
    [[ "${RES[feed.new.flag]:-}" == yes ]] || finding "check 18 — $L feed new wrote no AUTHOR TO CONFIRM flag (owner_email is the author's to confirm)"
    [[ "${RES[feed.new.guid]:-}" == ok ]] || finding "check 18 — $L feed new's podcast_guid ${RES[feed.new.guid]:-?} is not the UUIDv5 of its feed URL"
    [[ "${RES[feed.add.status]:-}" == 0 && "${RES[feed.add.guid]:-}" == ok ]] \
      || finding "check 18 — $L feed add did not write the episode's guid as the UUIDv5 of the piece under the show's (exit ${RES[feed.add.status]:-?}; guid ${RES[feed.add.guid]:-?}): ${RES[feed.add.tail]:-}"
    if [[ "${RES[feed.encode.status]:-}" != 0 ]]; then finding "check 18 — $L encode --deliverable podcast.feed_audio from a picture master failed (exit ${RES[feed.encode.status]:-?}): ${RES[feed.encode.tail]:-}"
    else
      read -r _ _ fv _ fa _ _ _ <<< "${RES[feed.encode.facts]:-- - - - - - - 0}"
      bad=""
      [[ "$fv" == - ]] || bad+=" a picture stream ($fv);"
      [[ "$fa" == mp3 ]] || bad+=" audio $fa, wants mp3;"
      [[ "${RES[feed.encode.tags]:-0}" == 0 ]] || bad+=" tagged at M5 (title, artist or album set);"
      num_eq "${RES[feed.encode.lufs]:-nan}" "${RES[loud.podcast.target]:-nan}" 1.0 || bad+=" ${RES[feed.encode.lufs]:-nan} LUFS, not within 1 LU of ${RES[loud.podcast.target]:-?};"
      [[ -z "$bad" ]] || finding "check 18 — $L the feed audio encoded at M5 is not sound only, untagged, at the podcast target:${bad%;}"
    fi
    [[ "${RES[feed.tag0.status]:-}" == 1 && "${RES[feed.tag0.unchanged]:-}" == yes ]] \
      || finding "check 18 — $L feed tag on a row with no title did not exit 1 changing nothing (exit ${RES[feed.tag0.status]:-?}; unchanged ${RES[feed.tag0.unchanged]:-?})"
    [[ "${RES[feed.cover.status]:-0}" == 0 && "${RES[feed.id3cover.status]:-0}" == 0 ]] \
      || finding "check 18 — $L image could not encode the show's cover to podcast.cover and podcast.id3_cover (exit ${RES[feed.cover.status]:-?} and ${RES[feed.id3cover.status]:-?})"
    if [[ "${RES[feed.tag.status]:-}" != 0 ]]; then finding "check 18 — $L feed tag failed on a filled row (exit ${RES[feed.tag.status]:-?}): ${RES[feed.tag.tail]:-}"
    else
      bad=""
      [[ "${RES[feed.tag.tags]:-}" == "album=Smoke Talks|artist=Probe Studio|title=The tide decides" ]] || bad+=" tags '${RES[feed.tag.tags]:-}';"
      [[ "${RES[feed.tag.id3]:-0}" == 3 ]] || bad+=" ID3v2.${RES[feed.tag.id3]:-?}, wants v2.3;"
      [[ "${RES[feed.tag.chapters]:-0}" == 3 ]] || bad+=" ${RES[feed.tag.chapters]:-0} chapters, wants 3;"
      [[ "${RES[feed.tag.apic]:-0}" -ge 1 ]] || bad+=" no cover (APIC) though id3_cover is set;"
      read -r _ _ _ _ fa _ _ dur <<< "${RES[feed.tag.after]:-- - - - - - - 0}"
      [[ "$fa" == mp3 ]] && num_eq "$dur" "${RES[feed.tag.before]:-0}" 0.05 || bad+=" the audio stream changed (${fa}, ${dur} s for ${RES[feed.tag.before]:-?} s);"
      read -r want bytes one <<< "${RES[feed.tag.rowwant]:-- 0 0}"
      read -r rrender rbytes rsecs <<< "${RES[feed.tag.row]:-- 0 0}"
      [[ "$rrender" == "$want" && "$rbytes" == "$bytes" ]] && num_eq "$rsecs" "$one" 0.1 || bad+=" the row reads '${RES[feed.tag.row]:-}', wants '${RES[feed.tag.rowwant]:-}';"
      [[ -z "$bad" ]] || finding "check 18 — $L feed tag did not tag the file as its row says:${bad%;}"
    fi
    [[ "${RES[feed.write0.status]:-}" == 2 ]] || finding "check 18 — $L feed write without --as-of did not exit 2 (exit ${RES[feed.write0.status]:-?}): no clock may be read"
    if [[ "${RES[feed.write.status]:-}" != 0 ]]; then finding "check 18 — $L feed write --as-of failed (exit ${RES[feed.write.status]:-?}): ${RES[feed.write.tail]:-}"
    else
      [[ "${RES[feed.write.same]:-}" == yes ]] || finding "check 18 — $L feed write gave different bytes for the same register and --as-of"
      [[ "${RES[feed.write.xml]:-}" == ok ]] || finding "check 18 — $L the written feed is not the feed DESIGN.md Section 6.17 requires: ${RES[feed.write.xml]:-?}"
    fi
    [[ "${RES[feed.rekey.status]:-}" == 0 && "${RES[feed.rekey.ok]:-}" == yes ]] \
      || finding "check 18 — $L feed new --rekey before anything was published did not recompute the feed URL's GUIDs (exit ${RES[feed.rekey.status]:-?})"
    [[ "${RES[feed.tracked.status]:-}" == 0 && "${RES[feed.tracked.same]:-}" == yes ]] \
      || finding "check 18 — $L feed write -o the tracked feed did not write the bytes feed write prints (exit ${RES[feed.tracked.status]:-?})"
    [[ "${RES[feed.tracked2.status]:-}" == 0 && "${RES[feed.tracked2.replaced]:-}" == yes ]] \
      || finding "check 18 — $L feed write -o did not replace the tracked feed after a register change (exit ${RES[feed.tracked2.status]:-?})"
    [[ "${RES[feed.chapters.status]:-}" == 0 && "${RES[feed.chapters.json]:-}" == ok ]] \
      || finding "check 18 — $L feed chapters did not write version 1.2 JSON chapters at 0, 120 and 240 s (exit ${RES[feed.chapters.status]:-?}: ${RES[feed.chapters.json]:-?})"
    if [[ "${RES[feed.check.status]:-}" != 0 ]]; then
      finding "check 18 — $L feed check fails the fixture show (exit ${RES[feed.check.status]:-?}), so its mutations prove nothing: ${RES[feed.check.tail]:-}"
    else
      for k in "dup:a repeated GUID" "gone:a GUID of the previous feed with no row" "length:an enclosure length changed under the same URL" \
               "angle:a < in a title" "bytes:bytes that differ from the render" "flag:an AUTHOR TO CONFIRM flag left in the register"; do
        [[ "${RES[feed.m.${k%%:*}]:-}" == 1 ]] || finding "check 18 — $L feed check passed ${k#*:} (exit ${RES[feed.m.${k%%:*}]:-?})"
      done
      [[ "${RES[feed.m.gonewrite]:-}" == 1 && "${RES[feed.m.gonewrite.kept]:-}" == yes ]] \
        || finding "check 18 — $L feed write -o replaced a tracked feed holding a GUID with no row (exit ${RES[feed.m.gonewrite]:-?}; kept ${RES[feed.m.gonewrite.kept]:-?})"
    fi
    [[ "${RES[feed.rekey2.status]:-}" == 2 && "${RES[feed.rekey2.unchanged]:-}" == yes ]] \
      || finding "check 18 — $L feed new --rekey after an episode was published was not refused with exit 2, changing nothing (exit ${RES[feed.rekey2.status]:-?})"
  fi

  # 19
  if [[ -n "${RES[tr.status]:-}" ]]; then
    if [[ "${RES[tr.status]}" != 0 ]]; then finding "check 19 — $L captions transcript failed on a fixture script (exit ${RES[tr.status]}): ${RES[tr.tail]:-}"
    else
      bad=""
      [[ "${RES[tr.spoken]:-}" == yes ]] || bad+=" the spoken words are missing;"
      [[ "${RES[tr.onscreen]:-}" == yes ]] || bad+=" no [On screen: …] for the TEXT: cue;"
      [[ "${RES[tr.tags]:-}" == no ]] || bad+=" a lone speaker's VO: tag kept;"
      [[ "${RES[tr.note]:-}" == no ]] || bad+=" a NOTE: cue kept;"
      [[ "${RES[tr.braces]:-}" == no ]] || bad+=" a braced direction kept;"
      [[ "${RES[tr.cues]:-}" == no ]] || bad+=" a raw cue line (SFX:, MUSIC: or TEXT:) kept;"
      [[ "${RES[tr.wrote]:-}" == no ]] || bad+=" a file written without -o;"
      [[ -z "$bad" ]] || finding "check 19 — $L captions transcript is not the published transcript:${bad%;}"
    fi
    [[ "${RES[tr.lines.status]:-}" == 0 && "${RES[tr.lines.has]:-}" == yes && "${RES[tr.lines.extra]:-}" == no ]] \
      || finding "check 19 — $L captions transcript --lines 2.1-2.2 did not take exactly those lines (exit ${RES[tr.lines.status]:-?}; has ${RES[tr.lines.has]:-?}; others ${RES[tr.lines.extra]:-?})"
    [[ "${RES[tr.o.status]:-}" == 0 && "${RES[tr.o.written]:-}" == yes ]] \
      || finding "check 19 — $L captions transcript -o wrote no file (exit ${RES[tr.o.status]:-?})"
  fi

  # 20 and 23
  local feature
  for feature in plan tags trial take join pending levels; do
    if [[ -n "${RES[voice.$feature]:-}" && "${RES[voice.$feature]}" != yes ]]; then
      finding "check 20 — $L voice tools failed $feature (${RES[voice.$feature]})"
    fi
  done
  for feature in clean dirty staged untracked outside other; do
    if [[ -n "${RES[guard.$feature]:-}" && "${RES[guard.$feature]}" != yes ]]; then
      finding "check 23 — $L tracked timing guard failed $feature (${RES[guard.$feature]})"
    fi
  done

  # 21 and the Rhubarb half of 26.
  if [[ -n "${RES[mouth.status]:-}" && "${RES[mouth.status]}" != 0 ]]; then
    finding "check 21 — $L mouth fixture could not run (exit ${RES[mouth.status]})"
  fi
  for feature in dialogue native resources fatal finite guards live; do
    if [[ -n "${RES[mouth.$feature]:-}" && "${RES[mouth.$feature]}" != yes && "${RES[mouth.$feature]}" != skip ]]; then
      finding "check 21 — $L lip sync failed $feature (${RES[mouth.$feature]})"
    fi
  done
  for feature in absent broken; do
    if [[ -n "${RES[setup.rhubarb.$feature]:-}" && "${RES[setup.rhubarb.$feature]}" != yes ]]; then
      finding "check 26 — $L Rhubarb setup failed $feature (${RES[setup.rhubarb.$feature]})"
    fi
  done

  # 22 and the WhisperX half of 26.
  if [[ -n "${RES[timing.status]:-}" && "${RES[timing.status]}" != 0 ]]; then
    finding "check 22 — $L timing fixture could not run (exit ${RES[timing.status]})"
  fi
  for feature in parts text sequence empty heard report cache captions live; do
    if [[ -n "${RES[timing.$feature]:-}" && "${RES[timing.$feature]}" != yes && "${RES[timing.$feature]}" != skip ]]; then
      finding "check 22 — $L word timing failed $feature (${RES[timing.$feature]})"
    fi
  done
  if [[ -n "${RES[setup.transcribe]:-}" && "${RES[setup.transcribe]}" != yes ]]; then
    finding "check 26 — $L missing WhisperX was not an optional note naming transcribe fetch"
  fi

  # 24
  if [[ -n "${RES[cues.status]:-}" ]]; then
    [[ "${RES[cues.status]}" == 0 ]] || finding "check 24 — $L cue fixture could not run (exit ${RES[cues.status]})"
    for feature in times lists delivery audio unmatched untimed finite links boards guards; do
      [[ "${RES[cues.$feature]:-}" == yes ]] || finding "check 24 — $L cue index failed $feature (${RES[cues.$feature]:-missing})"
    done
  fi
  if [[ -n "${RES[where.status]:-}" ]]; then
    if [[ "${RES[where.status]}" != 0 ]]; then finding "check 24 — $L where $P_WHERE failed (exit ${RES[where.status]}): ${RES[where.tail]:-}"
    else
      [[ "${RES[where.listed]:-}" == yes ]] || finding "check 24 — $L where $P_WHERE did not list every file of the piece Git tracks or would track (${RES[where.listed]:-?})"
      [[ -z "${RES[where.hidden]:-}" ]] || finding "check 24 — $L where $P_WHERE named what is inside an ignored per-piece folder, which it names and never lists (D50, D64): ${RES[where.hidden]}"
      [[ "${RES[where.folders]:-}" == yes ]] || finding "check 24 — $L where $P_WHERE did not name its three ignored per-piece folders, each existing or absent (read: ${RES[where.folders]:-?})"
    fi
    [[ "${RES[where.bad]:-}" == 2 ]] || finding "check 24 — $L where with a name that has no piece folder did not exit 2 (exit ${RES[where.bad]:-?})"
  fi

  # 25
  local ve ae
  if [[ -n "${RES[frames.status]:-}" ]]; then
    if [[ "${RES[frames.status]}" != 0 ]]; then finding "check 25 — $L assemble failed on a run of 25 stills of 0.16 s (exit ${RES[frames.status]}): ${RES[frames.tail]:-}"
    else
      [[ "${RES[frames.count]:-}" == 120 ]] \
        || finding "check 25 — $L 25 stills of 0.16 s at 30 fps assembled to ${RES[frames.count]:-?} frames, not 120, the frame nearest the edit's 4.000 s (rounding still by still gives 125)"
      [[ "${RES[frames.order]:-}" == ok ]] || finding "check 25 — $L a still does not start on the frame nearest its running total (Section 6.4): ${RES[frames.order]:-?}"
      [[ "${RES[frames.overlay]:-}" == ok ]] \
        || finding "check 25 — $L an overlay from the fourth still's start (00:00:00.480) until 00:00:00.800 is not on that still's first frame (14) and off frame 24: ${RES[frames.overlay]:-?}"
      if [[ -n "${RES[frames.enc.status]:-}" ]]; then
        if [[ "${RES[frames.enc.status]}" != 0 ]]; then
          finding "check 25 — $L encode of the stills master to ${RES[frames.enc.key]:-?} failed (exit ${RES[frames.enc.status]}): ${RES[frames.enc.tail]:-}"
        else
          read -r ve ae <<< "${RES[frames.enc.ends]:-0 999}"
          awk -v v="$ve" -v a="$ae" 'BEGIN { exit !(a <= v + 1 / 60) }' \
            || finding "check 25 — $L encode of the stills master to ${RES[frames.enc.key]:-?} gives sound to $ae s under $ve s of picture: its sound must end with its picture"
        fi
      fi
    fi
  fi
  return 0
}

# ── Self-test ────────────────────────────────────────────────────────────────

# What a clean smoke of a fixture render records: two video deliverables, an audio one and an
# image one, every step run and made to its preset.
write_clean_results() { # $1 = file
  cat > "$1" <<'EOF'
answers	ok
selftest.media.py	0
selftest.card.py	0
selftest.transcribe.py	0
deliverables	4
first_video	youtube.long
cut.youtube.long.status	0
cut.youtube.long.want	video 1920 1080 h264 aac 48000 4.000
cut.youtube.long.facts	1920 1080 h264 yuv420p aac 48000 2 4.000
cut.youtube.short.status	0
cut.youtube.short.want	video 1080 1920 h264 aac 48000 4.000
cut.youtube.short.facts	1080 1920 h264 yuv420p aac 48000 2 4.000
cut.podcast.apple_rss_audio.status	0
cut.podcast.apple_rss_audio.want	audio - - - aac 44100 4.000
cut.podcast.apple_rss_audio.facts	- - - - aac 44100 2 4.000
burn.key	youtube.long
burn.status	0
burn.size	1920x1080
burn.want	1920x1080
burn.playres	1920x1080
font.status	1
font.said	yes
card.youtube.thumbnail.status	0
card.youtube.thumbnail.want	3840x2160
card.youtube.thumbnail.size	3840x2160
card.alpha.status	0
card.alpha.facts	1920x1080 6 0
loud.social.target	-14.0
loud.podcast.target	-16.0
loud.social.status	0
loud.social.lufs	-13.9
loud.podcast.status	0
loud.podcast.lufs	-15.9
abmaster.status	0
abcheck.status	0
abhot.status	1
val.clean	0
val.line	1
val.cps	1
val.aspect	1
val.aspect.said	yes
val.long	1
val.long.key	youtube.short
val.long.rendered	no
git.notignored
git.readme.ignored
git.attr.large	lfs
git.attr.pair	unspecified
git.fresh	0
git.blob	1
git.blob.said	yes
git.fake	1
git.fake.said	yes
git.tripwire.add	128
git.tracked.ignored
edl.status	0
edl.expect	5.6
edl.facts	640 360 h264 yuv420p aac 48000 2 5.600
edl.lufs	-14.1
edl.where	yes
edl.cards	ok
ecut.youtube.long.status	0
ecut.youtube.long.dur	4.000
segs.status	0
segs.join	8.656
segs.lastwant	16.656
segs.cues	6
segs.first	0.200
segs.hasjoin	yes
segs.lastend	16.656
retime.status	0
retime.want	0.000
retime.first	0.000
retime.inside	yes
eburn.status	0
eburn.dur	3.000
amaster.status	0
amaster.expect	1.700
amaster.facts	- - - - pcm_s16le 48000 2 1.700
script.status	0
script.total	yes
footage.add	0
footage.kept	yes
footage.copied	yes
footage.dup	2
footage.verify	0
footage.changed	1
take.mp3.status	0
take.mp3.named	yes
take.mp3.register	yes
take.mp3.credits	1
take.pcm.status	0
take.pcm.named	yes
take.pcm.register	yes
take.pcm.credits	1
take.flat	yes
abtext.status	1
abtext.listed	yes
abtext.clean	yes
abtext.pause	yes
align.anchors	0
align.inside	yes
align.lines	0
align.placed	2
setup.status	1
setup.ask	yes
setup.base	yes
setup.leak	no
setup.encoders	yes
img.website.og_image.want	1200x630 -
img.website.og_image.jpg.status	0
img.website.og_image.jpg.facts	1200x630 mjpeg yuvj420p 120000 1
img.podcast.cover.want	3000x3000 false
img.podcast.cover.png.status	0
img.podcast.cover.png.facts	3000x3000 png rgb24 900000 1
img.shape.key	website.og_image
img.shape.status	2
img.shape.written	no
img.poster.key	website.poster
img.poster.status	0
img.poster.want	1920x1080
img.poster.size	1920x1080
img.maxsize.key	website.og_image
img.maxsize.status	1
gif.key	newsletter.preview_gif
gif.want	600 338 5 15 1000000
gif.a.status	0
gif.a.facts	600 338 30 2.000 1 400000
gif.a.overlay	yes
gif.b.status	0
gif.b.facts	600 338 45 3.000 -1 600000
gif.c.status	0
gif.c.limit	340000
gif.c.facts	600 338 15 2.000 1 250000
gif.d.status	2
gif.e.status	1
gif.e.written	no
loop.key	website.hero_loop
loop.status	0
loop.audio	-
loopmut.status	1
loopmut.saw	yes
loopmut.audio	aac
web.status	0
web.moov	yes
feed.nofolder.status	2
feed.nofolder.said	yes
feed.nofolder.made	no
feed.skeleton	same
feed.spec.status	0
feed.spec.guid	9b024349-ccf0-5f69-a609-6b82873eab3c
feed.new.status	0
feed.new.flag	yes
feed.new.guid	ok
feed.add.status	0
feed.add.guid	ok
feed.encode.status	0
feed.encode.facts	- - - - mp3 44100 2 360.000
feed.encode.lufs	-16.1
feed.encode.tags	0
feed.tag0.status	1
feed.tag0.unchanged	yes
feed.cover.status	0
feed.id3cover.status	0
feed.tag.status	0
feed.tag.tags	album=Smoke Talks|artist=Probe Studio|title=The tide decides
feed.tag.id3	3
feed.tag.chapters	3
feed.tag.apic	1
feed.tag.before	360.000
feed.tag.after	1400 1400 mjpeg yuvj420p mp3 44100 2 360.000
feed.tag.row	910-smoke-feed.podcast-feed-audio.mp3 576000 360.0
feed.tag.rowwant	910-smoke-feed.podcast-feed-audio.mp3 576000 360.000
feed.write0.status	2
feed.write.status	0
feed.write.same	yes
feed.write.xml	ok
feed.rekey.status	0
feed.rekey.ok	yes
feed.tracked.status	0
feed.tracked.same	yes
feed.tracked2.status	0
feed.tracked2.replaced	yes
feed.chapters.status	0
feed.chapters.json	ok
feed.check.status	0
feed.m.dup	1
feed.m.gone	1
feed.m.gonewrite	1
feed.m.gonewrite.kept	yes
feed.m.length	1
feed.m.angle	1
feed.m.bytes	1
feed.m.flag	1
feed.rekey2.status	2
feed.rekey2.unchanged	yes
tr.status	0
tr.spoken	yes
tr.onscreen	yes
tr.tags	no
tr.note	no
tr.braces	no
tr.cues	no
tr.wrote	no
tr.lines.status	0
tr.lines.has	yes
tr.lines.extra	no
tr.o.status	0
tr.o.written	yes
cues.status	0
cues.times	yes
cues.lists	yes
cues.delivery	yes
cues.audio	yes
cues.unmatched	yes
cues.untimed	yes
cues.finite	yes
cues.links	yes
cues.boards	yes
cues.guards	yes
where.status	0
where.listed	yes
voice.plan	yes
voice.tags	yes
voice.trial	yes
voice.take	yes
voice.join	yes
voice.pending	yes
voice.levels	yes
timing.status	0
timing.parts	yes
timing.text	yes
timing.sequence	yes
timing.empty	yes
timing.heard	yes
timing.report	yes
timing.cache	yes
timing.captions	yes
timing.live	yes
setup.transcribe	yes
mouth.status	0
mouth.dialogue	yes
mouth.native	yes
mouth.resources	yes
mouth.fatal	yes
mouth.finite	yes
mouth.guards	yes
mouth.live	yes
setup.rhubarb.absent	yes
setup.rhubarb.broken	yes
guard.clean	yes
guard.dirty	yes
guard.staged	yes
guard.untracked	yes
guard.outside	yes
guard.other	yes
where.hidden
where.folders	yes
where.bad	2
frames.status	0
frames.count	120
frames.order	ok
frames.overlay	ok
frames.enc.key	youtube.long
frames.enc.status	0
frames.enc.ends	4.000 4.000
EOF
}

self_test() {
  local tmp f
  bold "▸ $SCRIPT_NAME --self-test"; log ""
  tmp="$(sm_mktemp)"
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN
  f="$tmp/results.tsv"; NAME="fixture"
  write_clean_results "$f"
  mut() { # $1 = key, $2 = new value — rewrite one recorded fact, reload
    write_clean_results "$f"
    awk -F'\t' -v OFS='\t' -v k="$1" -v v="$2" '$1 == k { $2 = v; seen = 1 } { print } END { if (!seen) print k, v }' "$f" > "$f.new" && mv "$f.new" "$f"
    load_results "$f"
  }
  load_results "$f"
  st_baseline "a results file a clean smoke of a fixture render writes"

  mut selftest.media.py 1;                probe "check 1 fires when media.py --self-test fails" "check 1 — [fixture] python3 toolkit/media.py --self-test failed"
  mut selftest.media.py missing;          probe "check 1 fires when media.py is missing" "check 1 — [fixture] toolkit/media.py is missing"
  mut selftest.card.py 2;                 probe "check 1 fires when card.py --self-test exits 2 and names no skip" "toolkit/card.py --self-test failed (exit 2)"
  mut selftest.transcribe.py 1;           probe "check 1 fires when the stdlib transcription self-test fails" "toolkit/transcribe.py --self-test failed"
  mut cut.youtube.short.status 2;         probe "check 2 fires when a cut fails" "check 2 — [fixture] cut --deliverable youtube.short failed"
  mut cut.youtube.short.facts "1080 1080 h264 yuv420p aac 48000 2 4.000"
  probe "check 2 fires on a cut at the wrong size" "check 2 — [fixture] cut --deliverable youtube.short does not match its preset: picture 1080x1080"
  mut cut.podcast.apple_rss_audio.facts "640 360 h264 yuv420p aac 44100 2 4.000"
  probe "check 2 fires on a picture in an audio deliverable" "check 2 — [fixture] cut --deliverable podcast.apple_rss_audio does not match its preset: a picture stream"
  mut cut.youtube.long.facts "1920 1080 h264 yuv420p aac 44100 2 4.000"
  probe "check 2 fires on the wrong sample rate" "44100 Hz, wants 48000"
  mut burn.playres "640x360";             probe "check 3 fires when the ASS is not at the output size" "check 3 — [fixture] the burn for youtube.long"
  mut font.status 0;                      probe "check 3 fires when a missing caption font passes" "check 3 — [fixture] a burn whose caption font"
  mut card.youtube.thumbnail.size 1280x720; probe "check 4 fires on a card at the wrong size" "check 4 — [fixture] card.py render --deliverable youtube.thumbnail wrote 1280x720"
  mut card.alpha.facts "1920x1080 2 255"; probe "check 4 fires when --transparent keeps no alpha" "check 4 — [fixture] card.py render --transparent wrote no transparent pixel"
  mut loud.podcast.lufs -19.2;            probe "check 5 fires when the podcast target is missed" "check 5 — [fixture] loudness normalise --target podcast"
  mut abcheck.status 1;                   probe "check 6 fires when the fresh master fails its check" "check 6 — [fixture] audiobook check fails"
  mut abhot.status 0;                     probe "check 6 fires when a hot peak passes" "check 6 — [fixture] audiobook check passed a hot-peak"
  mut val.line 0;                         probe "check 7 fires when a 43-character line passes" "check 7 — [fixture] captions check passed a 43-character line"
  mut val.cps 0;                          probe "check 7 fires when 20 characters a second passes" "check 7 — [fixture] captions check passed 20 characters"
  mut val.clean 1;                        probe "check 7 fires when a clean SRT fails, never with the mutations" "check 7 — [fixture] captions check fails a clean SRT"
  mut val.aspect 0;                       probe "check 7 fires when a wrong aspect passes" "check 7 — [fixture] a burn onto a 640x360 clip"
  mut val.long.rendered yes;              probe "check 7 fires when an over-long cut renders" "check 7 — [fixture] an over-long cut for youtube.short"
  mut git.notignored "production/src/renders/smoke-sample.mp4"; probe "check 8 fires on generated output Git would track" "check 8 — [fixture] Git would track generated output"
  mut git.readme.ignored "publishing/src/renders/README.md";   probe "check 8 fires on an ignored README" "check 8 — [fixture] Git ignores a folder's README.md"
  mut git.attr.large unspecified;         probe "check 8 fires when the large exports are not LFS" "check 8 — [fixture] git check-attr reports filter 'unspecified'"
  mut git.blob 0;                         probe "check 8 fires when a plain blob is not flagged" "check 8 — [fixture] media.py check did not flag an LFS-marked file committed"
  mut git.fake 0;                         probe "check 8 fires when a configured-nothing git-lfs is not flagged" "while git-lfs answers but no filter"
  mut git.fresh 1;                        probe "check 8 fires when check is not clean on a fresh project" "check 8 — [fixture] media.py check is not clean"
  mut git.tripwire.add 0;                 probe "check 8 fires when the tripwire lets git add through" "check 8 — [fixture] with the copier.yml tripwire applied"
  mut git.tripwire.add none;              probe "check 8 fires when copier.yml has no tripwire task" "check 8 — [fixture] copier.yml carries no LFS tripwire"
  mut git.notignored "production/src/voiceover/generated/914-smoke-where/takes/914-smoke-where.s01.t1.mp3"; probe "check 8 fires when a take in a piece's takes/ folder is not ignored" "check 8 — [fixture] Git would track generated output: production/src/voiceover/generated/914-smoke-where/takes/"
  mut git.tracked.ignored "production/src/timing/914-smoke-where.words.json"; probe "check 8 fires when a tracked timing file is ignored" "check 8 — [fixture] Git ignores a piece's tracked timing or scene file"
  mut edl.facts "640 360 h264 yuv420p aac 48000 2 6.900"; probe "check 9 fires on a master of the wrong length" "check 9 — [fixture] the assembled master lasts 6.900"
  mut edl.lufs -20.0;                     probe "check 9 fires on a master off the social target" "check 9 — [fixture] the assembled master measures -20.0 LUFS"
  mut ecut.youtube.long.dur 3.2;          probe "check 9 fires on a cut of the master of the wrong length" "check 9 — [fixture] cut of the master for youtube.long lasts 3.2"
  mut segs.hasjoin no;                    probe "check 9 fires when no cue starts on the segment join" "check 9 — [fixture] from-segments cues are not exact"
  mut segs.lastend 16.700;                probe "check 9 fires when the last cue overruns its segment" "check 9 — [fixture] from-segments cues are not exact"
  mut retime.inside no;                   probe "check 9 fires when retime leaves a cue outside the cut" "check 9 — [fixture] captions retime"
  mut eburn.status 1;                     probe "check 9 fires when the retimed burn fails" "check 9 — [fixture] the burn of the retimed captions"
  mut edl.where no;                       probe "check 9 fires when the master is not in its piece's folder" "check 9 — [fixture] assemble did not write the master to production/src/renders/903-smoke-edit/"
  mut edl.cards "missing from production/src/renders/903-smoke-edit/cards/: 903-smoke-edit.title.640x360.transparent.png"; probe "check 9 fires when the overlay's render replaces the clip's" "check 9 — [fixture] one card used as a clip and as an overlay"
  mut amaster.facts "640 360 h264 yuv420p aac 48000 2 1.700"; probe "check 10 fires when the audio master has a picture" "check 10 — [fixture] the audio master is not sound only"
  mut script.total no;                    probe "check 11 fires when script time reports no total" "check 11 — [fixture] script time"
  mut footage.kept no;                    probe "check 11 fires when footage add moves the file" "check 11 — [fixture] footage add did not copy"
  mut footage.dup 0;                      probe "check 11 fires when a duplicate hash is accepted" "check 11 — [fixture] footage add accepted a duplicate hash"
  mut footage.changed 0;                  probe "check 11 fires when a changed byte passes verify" "check 11 — [fixture] footage verify passed a mirror with a changed byte"
  mut take.pcm.named no;                  probe "check 11 fires when a pcm take is not renamed .pcm" "check 11 — [fixture] take add of a fake pcm take"
  mut take.mp3.credits 0;                 probe "check 11 fires when a take writes no credits-log row" "check 11 — [fixture] take add of a fake mp3 take"
  mut take.mp3.register no;               probe "check 11 fires when the register does not name the take in its takes/ folder" "check 11 — [fixture] take add of a fake mp3 take did not rename it in its piece's takes/ folder"
  mut take.flat no;                       probe "check 11 fires when a take repeats the number of a flat take an earlier release left" "check 11 — [fixture] take add did not number the take in 905-smoke-take/takes/ t2"
  mut abtext.listed no;                   probe "check 12 fires when the constructed word is not listed" "check 12 — [fixture] audiobook text did not list"
  mut abtext.clean no;                    probe "check 12 fires when markup reaches a chunk" "check 12 — [fixture] audiobook text left markup"
  mut abtext.pause no;                    probe "check 12 fires when the scene break is not a 2 s sidecar pause" "check 12 — [fixture] audiobook text did not end a chunk"
  mut align.inside no;                    probe "check 13 fires when an anchored cue leaves its beat" "check 13 — [fixture] captions align --anchors"
  mut align.placed 1;                     probe "check 13 fires when --lines places too few cues" "check 13 — [fixture] captions align --lines placed 1 of 2"
  mut setup.base no;                      probe "check 14 fires when the outside base path is not reported" "check 14 — [fixture] check --setup did not report"
  mut setup.leak yes;                     probe "check 14 fires when check --setup prints a secret" "check 14 — [fixture] check --setup printed a value"
  mut setup.encoders no;                  probe "check 14 fires when check --setup names no optional image encoder" "check 14 — [fixture] check --setup does not name the optional encoders"
  mut img.website.og_image.jpg.facts "1200x628 mjpeg yuvj420p 120000 1"; probe "check 15 fires on an image at the wrong size" "check 15 — [fixture] image --deliverable website.og_image --format jpg does not match its preset: 1200x628"
  mut img.podcast.cover.png.facts "3000x3000 png rgba 900000 1"; probe "check 15 fires when alpha = false keeps its alpha" "kept its alpha channel (rgba)"
  mut img.website.og_image.jpg.status 1;  probe "check 15 fires when an image encode fails" "check 15 — [fixture] image --deliverable website.og_image --format jpg failed"
  mut img.shape.status 0;                 probe "check 15 fires when a source of another shape is accepted" "check 15 — [fixture] image --deliverable website.og_image accepted a source of another shape"
  mut img.poster.size 1280x720;           probe "check 15 fires on a poster at the wrong size" "check 15 — [fixture] the poster for website.poster is 1280x720"
  mut img.maxsize.status 0;               probe "check 15 fires when an image over max_size passes" "check 15 — [fixture] image --deliverable website.og_image with max_size overridden"
  mut gif.a.facts "600 338 30 2.000 0 400000"; probe "check 16 fires on a GIF that loops for ever" "it loops for ever"
  mut gif.a.facts "600 338 30 2.000 2 400000"; probe "check 16 fires on a GIF that plays too often" "plays 3 times, wants floor(5 / 2) = 2"
  mut gif.a.facts "600 338 60 2.000 1 400000"; probe "check 16 fires on a GIF over fps_max" "60 frames in 2.000 s, over fps_max 15"
  mut gif.a.overlay no;                   probe "check 16 fires when the overlay is not on the first frame" "the overlay is not on its first frame"
  mut gif.b.facts "600 338 45 3.000 1 600000"; probe "check 16 fires when a single play carries a loop extension" "check 16 — [fixture] the GIF preview of a 3-second range plays 2 times"
  mut gif.c.facts "600 338 30 2.000 1 330000"; probe "check 16 fires when the remake keeps every frame" "check 16 — [fixture] the GIF remade under max_size"
  mut gif.c.facts "600 338 15 1.000 1 250000"; probe "check 16 fires when the remake shortens the play" "check 16 — [fixture] the GIF remade under max_size"
  mut gif.d.status 1;                     probe "check 16 fires when an overlay of another size is not exit 2" "check 16 — [fixture] an overlay of another size"
  mut gif.e.written yes;                  probe "check 16 fires when an over-long GIF range renders" "check 16 — [fixture] a GIF range longer than max_seconds"
  mut loop.audio aac;                     probe "check 17 fires on a silent loop with a sound track" "check 17 — [fixture] the silent loop website.hero_loop carries a sound track"
  mut loopmut.status 0;                   probe "check 17 fires when the verification passes a loop that kept its sound" "check 17 — [fixture] the verification passed"
  mut web.moov no;                        probe "check 17 fires when website.video has its index at the end" "check 17 — [fixture] website.video was written with its index"
  mut feed.nofolder.said no;              probe "check 18 fires when feed new without the folder does not name the update" "check 18 — [fixture] feed new without publishing/src/podcast/"
  mut feed.nofolder.made yes;             probe "check 18 fires when feed new creates the folder" "check 18 — [fixture] feed new created publishing/src/podcast/"
  mut feed.skeleton "line 3: the folder's 'x' against the module's 'y'"; probe "check 18 fires when the fenced skeleton drifts" "check 18 — [fixture] the register skeleton fenced"
  mut feed.spec.guid 917393e3-1b1e-5cef-ace4-edaa54e1f810; probe "check 18 fires when podcast:guid is not the spec's" "check 18 — [fixture] feed new --feed-url"
  mut feed.new.flag no;                   probe "check 18 fires when feed new flags nothing" "check 18 — [fixture] feed new wrote no AUTHOR TO CONFIRM flag"
  mut feed.add.guid 00000000-0000-5000-8000-000000000001; probe "check 18 fires on an episode guid that is not the UUIDv5" "check 18 — [fixture] feed add did not write"
  mut feed.encode.tags 1;                 probe "check 18 fires when the M5 encode tags the file" "tagged at M5"
  mut feed.encode.facts "640 360 h264 yuv420p mp3 44100 2 360.000"; probe "check 18 fires when the feed audio keeps the picture" "a picture stream (h264)"
  mut feed.tag0.unchanged no;             probe "check 18 fires when feed tag on an empty title changes something" "check 18 — [fixture] feed tag on a row with no title"
  mut feed.tag.chapters 2;                probe "check 18 fires on missing chapter frames" "2 chapters, wants 3"
  mut feed.tag.after "1400 1400 mjpeg yuvj420p mp3 44100 2 359.000"; probe "check 18 fires when tagging changes the audio" "the audio stream changed"
  mut feed.tag.row "910-smoke-feed.podcast-feed-audio.mp3 575999 360.0"; probe "check 18 fires when the row's bytes are not the file's" "the row reads"
  mut feed.write0.status 0;               probe "check 18 fires when feed write reads a clock" "check 18 — [fixture] feed write without --as-of"
  mut feed.write.same no;                 probe "check 18 fires when feed write is not reproducible" "check 18 — [fixture] feed write gave different bytes"
  mut feed.write.xml "missing: podcast:guid"; probe "check 18 fires on a feed missing a required tag" "check 18 — [fixture] the written feed is not the feed"
  mut feed.rekey.ok no;                   probe "check 18 fires when --rekey keeps the old GUIDs" "check 18 — [fixture] feed new --rekey before anything was published"
  mut feed.tracked.same no;               probe "check 18 fires when the tracked feed differs from feed write's bytes" "check 18 — [fixture] feed write -o the tracked feed"
  mut feed.tracked2.replaced no;          probe "check 18 fires when the tracked feed is not replaced" "check 18 — [fixture] feed write -o did not replace"
  mut feed.chapters.json invalid;         probe "check 18 fires on invalid JSON chapters" "check 18 — [fixture] feed chapters"
  mut feed.check.status 1;                probe "check 18 fires when feed check fails the fixture, never with the mutations" "so its mutations prove nothing"
  mut feed.m.gone 0;                      probe "check 18 fires when a vanished GUID passes" "feed check passed a GUID of the previous feed with no row"
  mut feed.m.length 0;                    probe "check 18 fires when a changed length under one URL passes" "feed check passed an enclosure length changed"
  mut feed.m.flag 0;                      probe "check 18 fires when a flag left in the register passes" "feed check passed an AUTHOR TO CONFIRM flag"
  mut feed.m.gonewrite.kept no;           probe "check 18 fires when feed write replaces a feed holding a vanished GUID" "check 18 — [fixture] feed write -o replaced a tracked feed"
  mut feed.rekey2.status 0;               probe "check 18 fires when --rekey is accepted after publication" "check 18 — [fixture] feed new --rekey after an episode was published"
  mut tr.tags yes;                        probe "check 19 fires when a lone speaker's tag is kept" "a lone speaker's VO: tag kept"
  mut tr.onscreen no;                     probe "check 19 fires when on-screen text is lost" "no [On screen: …]"
  mut tr.wrote yes;                       probe "check 19 fires when the transcript is written without -o" "a file written without -o"
  mut tr.lines.extra yes;                 probe "check 19 fires when --lines takes other lines" "check 19 — [fixture] captions transcript --lines 2.1-2.2"
  mut tr.o.written no;                    probe "check 19 fires when -o writes nothing" "check 19 — [fixture] captions transcript -o wrote no file"
  mut where.listed "no: production/src/timing/914-smoke-where.words.json"; probe "check 24 fires when where misses a tracked timing file" "check 24 — [fixture] where 914-smoke-where did not list every file"
  for feature in plan tags trial take join pending levels; do
    mut "voice.$feature" no; probe "check 20 fires when voice $feature fails" "check 20 — [fixture] voice tools failed $feature"
  done
  for feature in clean dirty staged untracked outside other; do
    mut "guard.$feature" no; probe "check 23 fires when timing guard $feature fails" "check 23 — [fixture] tracked timing guard failed $feature"
  done
  for feature in parts text sequence empty heard report cache captions live; do
    mut "timing.$feature" no; probe "check 22 fires when word timing $feature fails" "check 22 — [fixture] word timing failed $feature"
  done
  for feature in dialogue native resources fatal finite guards live; do
    mut "mouth.$feature" no; probe "check 21 fires when lip sync $feature fails" "check 21 — [fixture] lip sync failed $feature"
  done
  mut mouth.status 2;                    probe "check 21 fires when its fixture could not run" "check 21 — [fixture] mouth fixture could not run"
  for feature in absent broken; do
    mut "setup.rhubarb.$feature" no; probe "check 26 fires when Rhubarb setup $feature fails" "check 26 — [fixture] Rhubarb setup failed $feature"
  done
  mut timing.status 2;                   probe "check 22 fires when its fixture could not run" "check 22 — [fixture] timing fixture could not run"
  mut setup.transcribe no;               probe "check 26 fires when absent WhisperX is not an optional setup note" "check 26 — [fixture] missing WhisperX"
  mut where.hidden "production/src/renders/914-smoke-where/914-smoke-where.master.mp4"; probe "check 24 fires when where lists inside an ignored folder" "check 24 — [fixture] where 914-smoke-where named what is inside an ignored per-piece folder"
  mut where.folders "production/src/renders/914-smoke-where/=exists"; probe "check 24 fires when where does not name all three folders" "check 24 — [fixture] where 914-smoke-where did not name its three ignored per-piece folders"
  for feature in times lists delivery audio unmatched untimed finite links boards guards; do
    mut "cues.$feature" no; probe "check 24 fires when cue $feature fails" "check 24 — [fixture] cue index failed $feature"
  done
  mut cues.status 2; probe "check 24 fires when cue fixtures cannot run" "check 24 — [fixture] cue fixture could not run"
  mut where.bad 0;                        probe "check 24 fires when where accepts a name with no piece folder" "check 24 — [fixture] where with a name that has no piece folder"
  mut frames.count 125;                   probe "check 25 fires when stills are rounded one by one" "check 25 — [fixture] 25 stills of 0.16 s at 30 fps assembled to 125 frames"
  mut frames.order "frame 14 shows still 3 where still 4 is due"; probe "check 25 fires when a still starts off its running total" "check 25 — [fixture] a still does not start on the frame nearest its running total"
  mut frames.overlay "on frames 15-23 (9 frames), wants 14-23"; probe "check 25 fires when an overlay misses its clip's first frame" "check 25 — [fixture] an overlay from the fourth still's start"
  mut frames.enc.ends "4.000 4.100";      probe "check 25 fires when an encode's sound runs past its picture" "check 25 — [fixture] encode of the stills master to youtube.long gives sound to 4.100 s under 4.000 s"
  mut frames.enc.status 1;                probe "check 25 fires when an encode of the stills master fails its own check" "check 25 — [fixture] encode of the stills master to youtube.long failed"
  write_clean_results "$f"; printf 'na.12\tno audiobook folder\nskip.4\tcard renders (no Chromium)\nskip.1\tcard.py --self-test (no Chromium)\n' >> "$f"
  sed -i '/^abtext\./d; /^card\./d; /^selftest\.card\.py/d' "$f"; load_results "$f"
  probe_clean "a render with no audiobook folder and no Chromium is clean, its steps listed n/a and skipped"

  # The driver's reading of card.py's own verdict (check 1), on logs in card.py's shape.
  local card_log="$tmp/card.log" why
  local chromium="every browser case (render, transparency, the network guard, check): Chromium for Playwright 1.62.0 is not installed: uv run --with playwright==1.62.0 playwright install chromium"
  local font="the brand-font probe (a @font-face that loads, then one that does not): fc-match is not installed to find a font file"
  local ended="self-test incomplete: 5 case(s) passed, 1 part(s) skipped (SKIP above): a skip is never a pass"
  read_card() { # $1 = label, $2 = exit status, $3 = the log's lines, $4 = the reasons wanted ('' = judged, never skipped)
    ST_PROBES=$((ST_PROBES + 1))
    printf 'card.py --self-test\n  ok   the safe zone scales to the render size\n%s\n' "$3" > "$card_log"
    why="$(card_skips "$2" "$card_log")"
    if [[ "$why" == "$4" ]]; then log "  ✓ $1"
    else
      ST_FAILS=$((ST_FAILS + 1))
      printf '\033[31m  ✗ %s: read %s, wants %s\033[0m\n' "$1" "${why:-(nothing)}" "${4:-(nothing)}"
    fi
  }
  read_card "card.py's exit 2 without Chromium is a named SKIP, in card.py's words" 2 "  SKIP $chromium"$'\n'"$ended" "$chromium"
  read_card "a brand-font SKIP is named for fc-match, never for the Chromium a passing case mentions" 2 \
    "  SKIP $font"$'\n'"  ok   without Playwright's Chromium, the SKIP names the command that installs it"$'\n'"$ended" "$font"
  read_card "a FAIL beside a SKIP (card.py's exit 1) is judged, never skipped" 1 \
    "  FAIL render writes a PNG of exactly the size asked"$'\n'"  SKIP $font"$'\n'"self-test FAILED: 1 case(s), and 1 part(s) skipped (SKIP above)" ""
  read_card "an exit 2 that does not end 'self-test incomplete' is judged, never skipped" 2 \
    "error: Chromium would not start: playwright install chromium" ""
  write_clean_results "$f"
  printf 'na.15\tno image deliverable\nna.16\tno GIF deliverable\nna.17\tno silent loop\nna.18\tno podcast folder\n' >> "$f"
  sed -i '/^img\./d; /^gif\./d; /^loop/d; /^web\./d; /^feed\.[a-mo-z]/d; /^feed\.new/d' "$f"; load_results "$f"
  probe_clean "a render without the own channels or a podcast folder is clean, feed new's refusal still judged"
  write_clean_results "$f"; printf 'na.25b\tno video deliverable with sound\n' >> "$f"
  sed -i '/^frames\.enc\./d' "$f"; load_results "$f"
  probe_clean "a render with no video deliverable a 4-second master fits is clean, its encode n/a"
  write_clean_results "$f"; printf 'skip.9\tthe card clip and overlay (no uv or no Chromium)\n' >> "$f"
  sed -i '/^edl\.cards/d' "$f"; load_results "$f"
  probe_clean "a render with no Chromium is clean, the card renders' folder unread"
  st_finish "a toolkit made to its presets from one that is not"
}

command -v python3 >/dev/null 2>&1 || die "python3 is not installed"
if $SELF_TEST; then
  self_test
  exit $?
fi
command -v git >/dev/null 2>&1 || die "git is not installed"
python3 -c 'import tomllib' 2>/dev/null || die "python3 is older than 3.11 (no tomllib), which the toolkit needs"
$REQUIRE_FFMPEG && ! $HAVE_FFMPEG && die "ffmpeg or ffprobe is not installed and --require-ffmpeg was given"
[[ ${#TARGETS[@]} -gt 0 ]] || die "no rendered tree given (see generate-all.sh)"
TRIPWIRE="$(lfs_tripwire_command)"

bold "▸ $SCRIPT_NAME (ffmpeg: $HAVE_FFMPEG · uv: $HAVE_UV$($SKIP_THUMBS && echo ' · thumbnails skipped'))"
STATUS=0
for target in "${TARGETS[@]}"; do
  [[ -d "$target" ]] || die "not a directory: $target"
  NAME="$(basename "$target")"
  smoke "$target"
  load_results "$RESULTS"
  run_checks
  reused=""; [[ -n "${RES[selftest.reused]:-}" ]] && reused=" (toolkit self-tests: same toolkit/ as an earlier render, result carried)"
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    log "  ✓ $NAME${reused}${NOTES[*]:+ — $(printf '%s; ' "${NOTES[@]}" | sed 's/; $//')}"
    rm -rf "$W"
  else
    bold "✗ $NAME — ${#FINDINGS[@]} finding(s) (logs kept in $W/out/*.log; results in $W/results.tsv):"
    print_findings
    [[ ${#NOTES[@]} -gt 0 ]] && log "    $(printf '%s; ' "${NOTES[@]}" | sed 's/; $//')"
    STATUS=1
  fi
done
log ""
[[ "$STATUS" -eq 0 ]] && { bold "✓ Every toolkit step that could run in every render ran and was made to its preset."; exit 0; }
log "  The toolkit is template-owned (DESIGN.md Section 4.2): fix toolkit/ or its data, never the"
log "  expectation; a preset that no longer matches what a platform takes is a platforms.toml change."
exit 1
