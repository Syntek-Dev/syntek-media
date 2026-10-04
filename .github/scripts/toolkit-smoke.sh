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
#                    Fourteen checks, per render:
#                      1. Every toolkit/*.py that offers `--self-test` passes it (media.py, which
#                         exercises the media_*.py modules, and card.py). A self-test reads only
#                         the toolkit, so one result serves every render whose toolkit/ is
#                         byte-identical (it says so).
#                      2. `cut` on a synthetic clip, for every video and audio deliverable of the
#                         platforms in the answers (and audiobook.acx, the retail sample, where
#                         the project makes audiobooks), writes what the preset says: size, codecs,
#                         yuv420p, sample rate, sound only for audio, and the length cut.
#                      3. `captions burn` onto a cut succeeds at the preset size with an ASS whose
#                         PlayResX/PlayResY is that size; with the caption font made one that is
#                         not installed, the burn fails and says the font fell back.
#                      4. `card.py render` writes a PNG at each image deliverable's preset size,
#                         and `--transparent` keeps alpha (SKIP by name without uv or Chromium,
#                         or with --skip-thumbnails).
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
#                         and fails for each folder's README.md; `git check-attr filter` reports
#                         `lfs` under brand/src/exports/large/ and not for its pair; `media.py
#                         check` is clean on the fresh copy, then flags a plain-blob LFS file, and
#                         flags an LFS-marked file when a fake git-lfs on PATH prints a version but
#                         no filter.lfs.* is configured; with the tripwire of copier.yml applied
#                         (DESIGN.md D19), `git add` of that file fails.
#                      9. A synthetic edit decision list end to end: a lavfi clip, a still with
#                         push-in, a colour clip, a card clip and a card overlay (cards SKIP by
#                         name without Chromium), a fade, a voiceover register of two tone
#                         segments each carrying several cues, and a ducked music bed trimmed and
#                         faded — `assemble` (length and social loudness), `cut` for every video
#                         deliverable in the answers, `captions from-segments` (cue times exact at
#                         the offset, at the segment join and at the last segment's end) and
#                         `retime` to a cut, then `burn` onto that cut.
#                     10. An audio master (`size = ""`) cut from clips of an audio-only source,
#                         under a faded bed, probes as sound only at the expected length.
#                     11. `script time` on a fixture script reports its total; `footage add`
#                         copies (never moves) and refuses a duplicate hash; `footage verify`
#                         passes, then fails on a changed byte; `take add` renames a fake .mp3
#                         take and a fake pcm_* take (to .pcm) and writes their register and
#                         credits-log rows.
#                     12. `audiobook text` on a chapter in syntek-author's markup strips section
#                         markers, comments, citation keys, divs and spans, ends a chunk at the
#                         scene break with 2 s recorded in the sidecar and never in the text
#                         (ruling T3), and lists the unpronounced constructed word (exit 1).
#                         Where the project makes no audiobooks there is no audiobook folder: n/a.
#                     13. `captions align --lines` places every cue of a synthetic cut, and
#                         `--anchors` keeps every cue of a beat inside that beat.
#                     14. `check --setup`, with HOME pointed at a scratch folder holding a fixture
#                         ~/.claude.json, reports a missing ask rule and a base path outside the
#                         repository, and prints no other value from that file.
#
#                    Numbers are stable identifiers. Append, never renumber.
#
#                    A check whose tool is absent is SKIPPED and named (SKIP — …), never passed:
#                    no ffmpeg (checks 2, 3, 5–7, 9, 10, 13), no uv or Chromium (check 4, card.py's
#                    self-test, the cards of check 9). --require-ffmpeg (CI) turns a missing ffmpeg
#                    into exit 2; --skip-thumbnails skips the Chromium steps by name. A step that
#                    does not apply to a render (no audiobook folder, no deliverable short enough
#                    to over-run) is listed as n/a, not as a SKIP.
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
P_SCRIPT="907-smoke-script"; P_BOOK="908-smoke-book"; P_ALIGN="909-smoke-align"
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

tkc() { # $1 = log name, then card.py arguments
  local name="$1" st=0; shift
  (cd "$T" && PYTHONDONTWRITEBYTECODE=1 uv run --quiet toolkit/card.py "$@") >"$OUT/$name.log" 2>&1 || st=$?
  return "$st"
}

said() { # $1 = log name, $2 = an extended regex → yes | no
  if grep -qiE -- "$2" "$OUT/$1.log" 2>/dev/null; then echo yes; else echo no; fi
}

tail_of() { grep -v '^[[:space:]]*$' "$OUT/$1.log" 2>/dev/null | tail -1 | cut -c1-110 || true; }

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

# Every deliverable table, the brand's overrides applied: key kind w h vcodec acodec rate min max aspect.
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
g = lambda v, f: str(v.get(f)) if v.get(f) not in (None, "") else "-"
for k, v in rows.items():
    print("\t".join([k, g(v, "kind"), g(v, "width"), g(v, "height"), g(v, "video_codec"), g(v, "audio_codec"),
                     g(v, "audio_sample_rate"), g(v, "min_seconds"), g(v, "max_seconds"), g(v, "aspect")]))
PY
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
    while IFS='=' read -r k st; do
      if [[ -n "$k" ]]; then rec "selftest.$k" "$st"; rec "selftest.$k.tail" "${SELFTEST_TAIL[$hash/$k]:-}"; fi
    done < <(printf '%s\n' "${SELFTEST_CACHE[$hash]}" | tr ';' '\n')
    rec selftest.reused "$hash"
  else
    local cache=""
    for f in "$T"/toolkit/*.py; do
      grep -q -- '--self-test' "$f" && grep -q '__main__' "$f" || continue
      k="${f##*/}"; st=0
      if [[ "$k" == card.py ]]; then
        if ! $HAVE_UV; then skip_step 1 "card.py --self-test" "uv is not installed"; continue; fi
        tkc "selftest.$k" --self-test || st=$?
        if [[ "$st" -eq 2 ]] && grep -qiE 'playwright install|chromium' "$OUT/selftest.$k.log"; then
          skip_step 1 "card.py --self-test" "Playwright's Chromium is not installed"; continue
        fi
      else
        tk "selftest.$k" --self-test || st=$?
      fi
      rec "selftest.$k" "$st"; rec "selftest.$k.tail" "$(tail_of "selftest.$k")"
      cache+="$k=$st;"; SELFTEST_TAIL["$hash/$k"]="$(tail_of "selftest.$k")"
    done
    SELFTEST_CACHE[$hash]="$cache"
  fi

  # The deliverables this render's answers ask for.
  while IFS=$'\t' read -r k kind w h vc ac rate min max asp; do
    [[ -z "$k" ]] && continue
    if [[ "$k" == audiobook.* ]]; then
      [[ "$k" == audiobook.acx && " $A_KINDS " == *" audiobook "* ]] || continue
    else
      [[ " $A_PLATFORMS " == *" ${k%%.*} "* ]] || continue
    fi
    answered+=("$k"$'\t'"$kind"$'\t'"$w"$'\t'"$h"$'\t'"$vc"$'\t'"$ac"$'\t'"$rate"$'\t'"$min"$'\t'"$max"$'\t'"$asp")
    if [[ "$kind" == video ]]; then
      videos+=("$k"); [[ -z "$first_v" ]] && first_v="$k"
      [[ -z "$first_land" && "$asp" == 16:9 ]] && first_land="$k"
      if [[ "$max" != - ]] && awk -v a="$max" -v b="$short_max" 'BEGIN { exit !(a < b) }'; then short_k="$k"; short_max="$max"; fi
    fi
    [[ "$kind" == image && "$w" != - ]] && images+=("$k $w $h")
  done < <(tables)
  rec deliverables "${#answered[@]}"
  rec first_video "${first_v:--}"

  if ! $HAVE_FFMPEG; then
    for k in 2 3 5 6 7 9 10 13; do skip_step "$k" "every ffmpeg step" "ffmpeg or ffprobe is not installed"; done
  else
    gen_av "$OUT/src.mp4" 5 640x360

    # ── 2. cut, per deliverable ──
    local row
    for row in "${answered[@]}"; do
      IFS=$'\t' read -r k kind w h vc ac rate min max asp <<< "$row"
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
  rec git.notignored "${missing% }"; rec git.readme.ignored "${leaked% }"
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

  # ── 11. script time, footage, takes ──
  smoke_repo "$first_v"

  # ── 12. audiobook text ──
  if [[ -d "$T/production/src/audiobook" ]]; then smoke_text
  else na_step 12 "no audiobook folder (MEDIA_KINDS without audiobook)"; fi

  # ── 13. align ──
  if $HAVE_FFMPEG; then smoke_align; fi

  # ── 14. check --setup ──
  smoke_setup
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
  local st k gen="$T/production/src/voiceover/generated" cards=true expect d1 d2 join last cues first m
  mkdir -p "$gen" "$T/production/src/assets" "$T/production/src/cards" "$T/production/src/edits"
  gen_av "$OUT/clip.mp4" 4 640x360
  gen_tone "$OUT/bed.wav" 8 48000 2 0.3
  gen_tone "$OUT/talk.wav" 4 48000 1 0.2
  tk fvideo footage add "$OUT/clip.mp4" --kind video --location "Smoke drive A" || true
  tk fmusic footage add "$OUT/bed.wav" --kind music --location "Smoke library B" || true
  tk faudio footage add "$OUT/talk.wav" --kind audio --location "Smoke recorder C" || true
  gen_still "$T/production/src/assets/smoke-harbour.png" 800x600
  gen_tone "$gen/$P_EDIT.s01.t1.mp3" 8 44100 1 0.2 -c:a libmp3lame -b:a 128k
  gen_tone "$gen/$P_EDIT.s02.t1.pcm" 8 22050 1 0.2 -f s16le
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
file = "generated/$P_EDIT.s02.t1.pcm"
characters = 116
pause_after = 0.3
status = "approved"
archived = ""
EOF
  if $SKIP_THUMBS; then cards=false; skip_step 9 "the edit's card clip and overlay" "--skip-thumbnails"
  elif ! $HAVE_UV || [[ "$HAVE_CHROMIUM" == false ]]; then cards=false; skip_step 9 "the edit's card clip and overlay" "no uv or no Chromium"; fi
  if $cards; then
    sed 's#href="../../brand/#href="../../../brand/#' "$T/toolkit/templates/card.html" > "$T/production/src/cards/$P_EDIT.title.html"
    sed 's#href="../../brand/#href="../../../brand/#' "$T/toolkit/templates/card.html" > "$T/production/src/cards/$P_EDIT.end.html"
  fi
  {
    printf '[edit]\npiece = "%s"\nversion = 1\nsize = "640x360"\naudio_rate = 48000\nloudness = "social"\n\n' "$P_EDIT"
    printf '[[clip]]\nid = "c01"\nsource = "%s"\nin = "00:00:00.500"\nout = "00:00:02.500"\nframe = "crop"\n\n' "$(manifest_id video)"
    printf '[[clip]]\nid = "c02"\nsource = "production/src/assets/smoke-harbour.png"\nseconds = 2.0\nmotion = "push-in"\ntransition = "fade"\ntransition_seconds = 0.5\n\n'
    printf '[[clip]]\nid = "c03"\ncolour = "#101418"\nseconds = 1.0\n\n'
    if $cards; then
      printf '[[clip]]\nid = "c04"\nsource = "production/src/cards/%s.title.html"\nseconds = 1.5\ntransition = "fade"\ntransition_seconds = 0.4\n\n' "$P_EDIT"
      printf '[[overlay]]\nsource = "production/src/cards/%s.end.html"\nat = "00:00:01.000"\nuntil = "00:00:02.000"\n\n' "$P_EDIT"
    fi
    printf '[[audio]]\nsource = "vo:%s"\nat = "00:00:00.200"\nrole = "voice"\n\n' "$P_EDIT"
    printf '[[audio]]\nsource = "%s"\nat = "00:00:00.000"\nin = "00:00:01.000"\nout = "00:00:07.000"\ngain_db = -6.0\nfade_in = 0.5\nfade_out = 1.0\nrole = "music"\nduck = true\n' "$(manifest_id music)"
  } > "$T/production/src/edits/$P_EDIT.toml"
  expect="4.5"; $cards && expect="5.6"
  st=0; tk assemble assemble "production/src/edits/$P_EDIT.toml" -o "$OUT/c9.master.mp4" || st=$?
  rec edl.status "$st"; rec edl.tail "$(tail_of assemble)"; rec edl.expect "$expect"
  m="$OUT/c9.master.mp4"
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
  d2="$(awk -v b="$(stat -c %s "$gen/$P_EDIT.s02.t1.pcm")" 'BEGIN { printf "%.3f", b / (22050 * 2) }')"
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

  mkdir -p "$T/production/src/voiceover/generated"
  before="$(grep -c . "$T/production/src/credits-log.md" 2>/dev/null || echo 0)"
  for p in "$P_TAKE:mp3_44100_128" "$P_PCM:pcm_22050"; do
    fmt="${p#*:}"; p="${p%%:*}"; ext=".mp3"; [[ "$fmt" == pcm* ]] && ext=".pcm"
    printf '[voiceover]\npiece = "%s"\nvoice_use = "voiceover"\nmodel_id = "eleven_v4"\noutput_format = "%s"\nper_cue = false\n\n[[segment]]\nid = "s01"\nscript_lines = "1.1"\ntext = "The ferry is late again."\nrequest = "The ferry is late again."\ntake = 0\nfile = ""\ncharacters = 24\npause_after = 0.3\nstatus = ""\narchived = ""\n' \
      "$p" "$fmt" > "$T/production/src/voiceover/$p.toml"
    printf 'a fake take, never an ElevenLabs call\n' > "$T/production/src/voiceover/generated/tts_smoke_20270101_101010.mp3"
    st=0; tk "take.$ext" take add production/src/voiceover/generated/tts_smoke_20270101_101010.mp3 --piece "$p" --segment s01 || st=$?
    rec "take${ext}.status" "$st"
    rec "take${ext}.named" "$([[ -f "$T/production/src/voiceover/generated/$p.s01.t1$ext" && ! -e "$T/production/src/voiceover/generated/tts_smoke_20270101_101010.mp3" ]] && echo yes || echo no)"
    rec "take${ext}.register" "$(grep -qF "file = \"generated/$p.s01.t1$ext\"" "$T/production/src/voiceover/$p.toml" && echo yes || echo no)"
    rec "take${ext}.credits" "$(grep -c "| $p |" "$T/production/src/credits-log.md" 2>/dev/null || echo 0)"
  done
  rec take.credits.before "$before"
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
    [[ "$ac" == - || "$fa" == "$ac" ]] || bad+=" audio $fa, wants $ac;"
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
      finding "check 11 — $L take add of a fake ${k#.} take did not rename it and write one register and one credits-log row (exit ${RES[take$k.status]:-?}; named ${RES[take$k.named]:-?}; register ${RES[take$k.register]:-?}; credits rows ${RES[take$k.credits]:-0})"
    fi
  done

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
edl.status	0
edl.expect	5.6
edl.facts	640 360 h264 yuv420p aac 48000 2 5.600
edl.lufs	-14.1
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
  mut edl.facts "640 360 h264 yuv420p aac 48000 2 6.900"; probe "check 9 fires on a master of the wrong length" "check 9 — [fixture] the assembled master lasts 6.900"
  mut edl.lufs -20.0;                     probe "check 9 fires on a master off the social target" "check 9 — [fixture] the assembled master measures -20.0 LUFS"
  mut ecut.youtube.long.dur 3.2;          probe "check 9 fires on a cut of the master of the wrong length" "check 9 — [fixture] cut of the master for youtube.long lasts 3.2"
  mut segs.hasjoin no;                    probe "check 9 fires when no cue starts on the segment join" "check 9 — [fixture] from-segments cues are not exact"
  mut segs.lastend 16.700;                probe "check 9 fires when the last cue overruns its segment" "check 9 — [fixture] from-segments cues are not exact"
  mut retime.inside no;                   probe "check 9 fires when retime leaves a cue outside the cut" "check 9 — [fixture] captions retime"
  mut eburn.status 1;                     probe "check 9 fires when the retimed burn fails" "check 9 — [fixture] the burn of the retimed captions"
  mut amaster.facts "640 360 h264 yuv420p aac 48000 2 1.700"; probe "check 10 fires when the audio master has a picture" "check 10 — [fixture] the audio master is not sound only"
  mut script.total no;                    probe "check 11 fires when script time reports no total" "check 11 — [fixture] script time"
  mut footage.kept no;                    probe "check 11 fires when footage add moves the file" "check 11 — [fixture] footage add did not copy"
  mut footage.dup 0;                      probe "check 11 fires when a duplicate hash is accepted" "check 11 — [fixture] footage add accepted a duplicate hash"
  mut footage.changed 0;                  probe "check 11 fires when a changed byte passes verify" "check 11 — [fixture] footage verify passed a mirror with a changed byte"
  mut take.pcm.named no;                  probe "check 11 fires when a pcm take is not renamed .pcm" "check 11 — [fixture] take add of a fake pcm take"
  mut take.mp3.credits 0;                 probe "check 11 fires when a take writes no credits-log row" "check 11 — [fixture] take add of a fake mp3 take"
  mut abtext.listed no;                   probe "check 12 fires when the constructed word is not listed" "check 12 — [fixture] audiobook text did not list"
  mut abtext.clean no;                    probe "check 12 fires when markup reaches a chunk" "check 12 — [fixture] audiobook text left markup"
  mut abtext.pause no;                    probe "check 12 fires when the scene break is not a 2 s sidecar pause" "check 12 — [fixture] audiobook text did not end a chunk"
  mut align.inside no;                    probe "check 13 fires when an anchored cue leaves its beat" "check 13 — [fixture] captions align --anchors"
  mut align.placed 1;                     probe "check 13 fires when --lines places too few cues" "check 13 — [fixture] captions align --lines placed 1 of 2"
  mut setup.base no;                      probe "check 14 fires when the outside base path is not reported" "check 14 — [fixture] check --setup did not report"
  mut setup.leak yes;                     probe "check 14 fires when check --setup prints a secret" "check 14 — [fixture] check --setup printed a value"
  write_clean_results "$f"; printf 'na.12\tno audiobook folder\nskip.4\tcard renders (no Chromium)\n' >> "$f"
  sed -i '/^abtext\./d; /^card\./d' "$f"; load_results "$f"
  probe_clean "a render with no audiobook folder and no Chromium is clean, its steps listed n/a and skipped"
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
