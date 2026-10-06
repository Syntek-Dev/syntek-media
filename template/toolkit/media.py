#!/usr/bin/env python3
"""media.py: the media toolkit's one command: masters, deliverables, captions, audio and checks.

Usage:
    python3 toolkit/media.py probe FILE [--json] [--output-format pcm_RATE]
    python3 toolkit/media.py presets [KEY] [--stale-after DAYS --today DD/MM/YYYY]
    python3 toolkit/media.py script time PATH [--wpm N] [--write]
    python3 toolkit/media.py assemble EDL [--memory-max SIZE] [-o OUT]
    python3 toolkit/media.py cut SRC --deliverable KEY --in TC --out TC [--cut cNN] [--frame crop|pad]
                                 [--x PX] [--captions SRT] [--overlay PNG] [-o OUT]
    python3 toolkit/media.py encode SRC --deliverable KEY [--frame crop|pad] [-o OUT]
    python3 toolkit/media.py frame SRC --at TC [-o OUT]
    python3 toolkit/media.py image SRC --deliverable KEY [--at TC] [--format jpg|png|webp|avif]
                                   [--frame crop|pad] [-o OUT]
    python3 toolkit/media.py still-video IMAGE AUDIO --deliverable KEY [-o OUT]
    python3 toolkit/media.py extract-audio SRC [--in TC --out TC] [--rate HZ] [-o OUT]
    python3 toolkit/media.py captions check SRT [--deliverable KEY] [--script SCRIPT]
    python3 toolkit/media.py captions from-segments REGISTER --deliverable KEY [--offset TC] [-o SRT]
    python3 toolkit/media.py captions from-words WORDS --deliverable KEY [--offset TC] [-o SRT]
    python3 toolkit/media.py captions align TEXT AUDIO [--lines B.L-B.L] [--anchors] [--noise DB]
                                            [--min-silence S] [-o SRT]
    python3 toolkit/media.py captions retime SRT (--in TC --out TC | --edl EDL --source FID) [-o SRT]
    python3 toolkit/media.py captions rewrap SRT --deliverable KEY [-o SRT]
    python3 toolkit/media.py captions vtt SRT [-o VTT]
    python3 toolkit/media.py captions transcript TEXT [--lines B.L-B.L] [--date DD/MM/YYYY] [-o MD]
    python3 toolkit/media.py captions burn SRC SRT --deliverable KEY [-o OUT]
    python3 toolkit/media.py loudness measure FILE
    python3 toolkit/media.py loudness normalise FILE --target social|podcast|acx [-o OUT]
    python3 toolkit/media.py audiobook text SOURCE --piece PIECE --chapter chNN
                                            [--footnotes drop|inline] [--limit CHARS]
    python3 toolkit/media.py audiobook master CHUNKS... --piece PIECE --chapter chNN [--head S]
                                              [--tail S] [--room-tone FILE] [-o OUT]
    python3 toolkit/media.py audiobook check FILE...
    python3 toolkit/media.py take add FILE --piece PIECE (--segment sNN | --chapter chNN --part pNN)
    python3 toolkit/media.py speak plan [PIECE [--segment sNN...]] [--trial NAME]
    python3 toolkit/media.py voice join PIECE [-o OUT]
    python3 toolkit/media.py levels PIECE [--window S]
    python3 toolkit/media.py transcribe PIECE [--no-cross-check] [-o WORDS]
    python3 toolkit/media.py transcribe fetch
    python3 toolkit/media.py lipsync PIECE [-o FILE]
    python3 toolkit/media.py cues PIECE [-o FILE]
    python3 toolkit/media.py real PIECE [-o FILE]
    python3 toolkit/media.py feed new SHOW --feed-url URL [--site SLUG] [--rekey]
    python3 toolkit/media.py feed add SHOW --piece PIECE
    python3 toolkit/media.py feed tag SHOW --piece PIECE
    python3 toolkit/media.py feed write SHOW --as-of 'DD/MM/YYYY HH:MM' [-o FILE]
    python3 toolkit/media.py feed chapters SHOW --piece PIECE [-o FILE]
    python3 toolkit/media.py feed check SHOW [--feed FILE] [--previous FILE]
    python3 toolkit/media.py footage add FILE --kind KIND --location LABEL [--rights RRNNNN]
    python3 toolkit/media.py footage verify [--manifest PATH]
    python3 toolkit/media.py tokens [--tokens PATH]
    python3 toolkit/media.py flags [PATH...] [--piece PIECE] [--strict]
    python3 toolkit/media.py where PIECE
    python3 toolkit/media.py check [--strict] [--setup]
    python3 toolkit/media.py score plan INPUT [--rubric TOML] [--model NAME] [-o JSON]
    python3 toolkit/media.py score run INPUT --approve-call [--rubric TOML] [--model NAME] [-o JSON]
    python3 toolkit/media.py --self-test

KEY is a deliverable of toolkit/data/platforms.toml, written <platform>.<format> (youtube.short,
podcast.apple_rss_audio) or audiobook.<store> (audiobook.acx); the brand's confirmed corrections
in brand/src/platforms/overrides.toml are applied and printed. TC is a timecode, HH:MM:SS.mmm.
Every path is relative to the working folder; defaults are relative to the repository root.

Outputs go to a renders/ or generated/ folder by default, a piece's into its own folder there,
named for the leading piece key of the output's name (production/src/renders/<piece>/ for
masters, cards and extracts; publishing/src/renders/<piece>/ for deliverables, images, GIFs,
burned captions, timed captions from segments, stills, a feed episode's audio and JSON
chapters); a name with no piece key stays at the top of its folder, and the audiobook folder's
generated/ and renders/ stay flat. Each is named as the house names it (DESIGN D64,
Section 6.16); nothing is written elsewhere unless -o names a path, and nothing outside those
folders is ever overwritten. captions align, retime, rewrap, vtt and transcript, and feed
write, write to -o or, without it, to stdout (report lines go to stderr): their files belong in
tracked folders, where the toolkit never chooses a path. The exceptions, each written only by
the commands named for it: the registers and the manifest (take add, footage add, and a
podcast show's register: feed new, feed add and feed tag, none of which rewrites a value the
author set), and a show's tracked feed, publishing/src/podcast/<show>.feed.xml, which only
feed write -o replaces, after its GUID comparison passes, through a temporary file renamed over
it; and D66's named timing and scene files, replaced only by their owning command through -o
while committed and unchanged in Git, through the same temporary-file rule. Timing working
copies, levels included, sit in production/src/renders/<piece>/timing/. Every render is probed.

The modules beside this file do the work and have no command of their own: media_common.py
(TOML, timecodes, presets and overrides, paths, the ffmpeg runner), media_video.py (assemble,
cut, encode, frame, still-video), media_audio.py (extract-audio, loudness, audiobook, take),
media_captions.py (captions, script time), media_repo.py (footage, tokens, flags, where, check),
media_image.py (image, and the GIF pass of cut) and media_feed.py (a self-hosted podcast's
register, feed, chapters and file tags), and media_score.py (Jev option scoring). card.py renders HTML and CSS to PNG and runs through
uv: uv run toolkit/card.py --help.

Standard library only; Python 3.11+; ffmpeg and ffprobe for every command that touches media,
run from argument lists, never a shell string. No command calls ElevenLabs. Network access is
limited to the author-run transcribe fetch, uv package setup and explicitly approved Jev scoring.
Score plan is offline; score run writes JSON to stdout or a new explicit -o, never over an existing file. Exit codes: 0 = done and verified, or clean; 1 = a finding (a check failed, or an
output failed its verification); 2 = could not run (bad arguments, a missing input, a missing
tool, named with its install hint, or the tool itself failed).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_common as C  # noqa: E402
import media_audio as A  # noqa: E402
import media_captions as K  # noqa: E402
import media_feed as F  # noqa: E402
import media_image as I  # noqa: E402
import media_repo as R  # noqa: E402
import media_video as V  # noqa: E402
import media_score as J  # noqa: E402


# ── probe and presets ───────────────────────────────────────────────────────────────────

def cmd_probe(args) -> int:
    p = Path(args.file)
    info = C.probe(p, args.output_format)
    fmt = info.get("format", {})
    image = None   # for an image file: (frames, what an edit decision list does with it)
    if p.suffix.lower() in C.IMAGE_EXT:
        frames = C.image_frames(p, info)
        image = (frames, "a still: a [[clip]] holds it for seconds" if frames <= 1 else
                 "moving: a [[clip]] cuts it by in and out, and cut and encode take it like a video")
    if args.json:
        keep = ("index", "codec_type", "codec_name", "width", "height", "r_frame_rate", "sample_rate",
                "channels", "pix_fmt", "bit_rate", "duration")
        record = {"file": C.shown(p), "duration": C.duration(info), "size": int(fmt.get("size") or
                  p.stat().st_size), "bit_rate": fmt.get("bit_rate"),
                  "streams": [{k: s.get(k) for k in keep if k in s} for s in info.get("streams", [])]}
        if image:
            record.update(frames=image[0], still=image[0] <= 1)
        print(json.dumps(record, indent=2))
        return 0
    print(f"{C.shown(p)}: {V.describe(p, args.output_format)}")
    if image:
        print(f"  image: {image[0]} frame{'s' if image[0] != 1 else ''}, {image[1]}")
    for s in info.get("streams", []):
        if s.get("codec_type") == "video":
            print(f"  stream {s.get('index')}: video {s.get('codec_name')} {s.get('width')}x{s.get('height')} "
                  f"{s.get('pix_fmt')} {s.get('r_frame_rate')}")
        elif s.get("codec_type") == "audio":
            print(f"  stream {s.get('index')}: audio {s.get('codec_name')} {s.get('sample_rate')} Hz "
                  f"{s.get('channels')} ch")
        else:
            print(f"  stream {s.get('index')}: {s.get('codec_type')} {s.get('codec_name')}")
    return 0


HIDDEN = ("checked", "source", "extra_sources", "verify", "chosen", "notes")


def print_table(label: str, table: dict, marks: dict) -> None:
    scalars = {k: v for k, v in table.items() if not (isinstance(v, dict) and "kind" in v)}
    print(f"[{label}]  checked {scalars.get('checked', '?')}")
    verify = set(scalars.get("verify", []) or [])
    chosen = set(scalars.get("chosen", []) or [])
    for key, value in scalars.items():
        if key in HIDDEN:
            continue
        note = []
        if key in verify:
            note.append("verify: unconfirmed")
        if key in chosen:
            note.append("chosen: a house choice")
        if (label, key) in marks:
            note.append(marks[(label, key)])
        print(f"  {key} = {value!r}" + (f"   ({'; '.join(note)})" if note else ""))
    print(f"  source: {scalars.get('source', '?')}")
    if scalars.get("notes"):
        print(f"  notes: {scalars['notes']}")


def cmd_presets(args) -> int:
    data, applied, problems = C.load_presets(quiet=True)
    for p in problems:
        print(f"warning: {p}; ignored", file=sys.stderr)
    marks = {}
    for a in applied:
        field = a["key"].split(".")[-1] if a["table"] != "house" else a["key"].split(".")[1]
        marks[(a["table"], field)] = f"brand override; platforms.toml says {a['was']!r}"
    tables = []
    key = args.key
    if not key or key == "house":
        tables.append(("house", data.get("house", {})))
    for name, ptable in data.get("platform", {}).items():
        if key and key not in (name, ) and not key.startswith(name + "."):
            continue
        tables.append((f"platform.{name}", ptable))
        for fmt, t in ptable.items():
            if isinstance(t, dict) and "kind" in t and (not key or key in (name, f"{name}.{fmt}")):
                tables.append((f"{name}.{fmt}", t))
    for store, t in data.get("audiobook", {}).items():
        if not key or key in ("audiobook", f"audiobook.{store}"):
            tables.append((f"audiobook.{store}", t))
    if key and len(tables) == 0:
        raise C.Fatal(f"{key!r} names no table of toolkit/data/platforms.toml")
    if key and "." in key and not key.startswith("audiobook.") and key != "house":
        tables = [t for t in tables if t[0] == key] or tables
    if args.stale_after is None:
        for label, t in tables:
            print_table(label, t, marks)
        for a in applied:
            print(f"brand override {a['key']} = {a['value']!r} (platforms.toml: {a['was']!r}) — "
                  f"{a['why'] or 'no reason given'}; {a['source'] or 'no source'}; checked {a['checked'] or '?'}")
        return 0
    if args.stale_after < 0:
        raise C.Fatal("--stale-after takes a number of days, 0 or more")
    today = C.parse_date(args.today) if args.today else C.parse_date(C.today())
    stale = []
    for label, t in tables:
        checked = t.get("checked")
        if not checked and all(isinstance(v, dict) for v in t.values()):
            continue
        if not checked:
            stale.append(f"{label}: no checked date")
            continue
        age = (today - C.parse_date(str(checked))).days
        if age > args.stale_after:
            stale.append(f"{label}: checked {checked}, {age} days before {today.strftime('%d/%m/%Y')} "
                         f"(source {t.get('source', '?')})")
    for a in applied:
        if a["checked"]:
            age = (today - C.parse_date(a["checked"])).days
            if age > args.stale_after:
                stale.append(f"override {a['key']}: checked {a['checked']}, {age} days old")
    for s in stale:
        print(f"  STALE {s}")
    dated = sum(1 for _, t in tables if t.get("checked"))
    print(f"presets: {len(stale)} of {dated} dated table(s) older than {args.stale_after} days"
          if stale else f"presets: every table checked within {args.stale_after} days")
    return 1 if stale else 0


# ── The command line ────────────────────────────────────────────────────────────────────

STDOUT_HELP = ("the output path; without -o the captions go to stdout and every report line to "
               "stderr (their home, publishing/src/captions/, is tracked, so the toolkit never "
               "chooses a path there; an existing file there is never overwritten)")
FEED_HELP = ("the output path; without -o the feed goes to stdout and every report line to stderr. "
             "-o publishing/src/renders/<show>.feed.xml is the upload copy (M7); -o "
             "publishing/src/podcast/<show>.feed.xml replaces the tracked feed through a temporary file, "
             "the D59 feed exception, once the author reports the feed live "
             "(publishing/workflows/06-record-a-publication/); any other existing file outside a "
             "renders/ or generated/ folder is never overwritten")

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="media.py", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Run 'media.py <command> --help' for one command's arguments.")
    sub = ap.add_subparsers(dest="cmd", metavar="command")

    def out(p, help_="the output path (default: a renders/ folder, named as the house names it)"):
        p.add_argument("-o", metavar="OUT", help=help_)

    p = sub.add_parser("probe", help="streams, sizes and durations of one file")
    p.add_argument("file")
    p.add_argument("--json", action="store_true")
    p.add_argument("--output-format", help="a raw take's ElevenLabs format, pcm_RATE")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("presets", help="deliverable tables with brand overrides; stale checked dates")
    p.add_argument("key", nargs="?", help="a deliverable key, a platform, audiobook or house")
    p.add_argument("--stale-after", type=int, metavar="DAYS")
    p.add_argument("--today", metavar="DD/MM/YYYY")
    p.set_defaults(func=cmd_presets)

    p = sub.add_parser("script", help="script time")
    ss = p.add_subparsers(dest="sub", metavar="time")
    q = ss.add_parser("time", help="spoken words and seconds per beat against the brief",
                      description="Counts spoken words (tags, braces and cue lines removed) and adds "
                      "every {pause S}, per beat and in total. A beat heading's '(target MM:SS)' is that "
                      "beat's own duration: each beat is compared with its own target, and the targets "
                      "are summed. The total is judged against the brief's target_seconds (within 10%) "
                      "and every deliverable's max_seconds.")
    q.add_argument("path")
    q.add_argument("--wpm", type=float, help="words a minute (default: the brief's words_per_minute, else 150)")
    q.add_argument("--write", action="store_true", help="record words and estimated_seconds")
    q.set_defaults(func=K.cmd_script_time)

    p = sub.add_parser("assemble", help="build a master from an edit decision list")
    p.add_argument("edl")
    p.add_argument('--memory-max', metavar='SIZE', help='systemd memory cap (else MEDIA_MEMORY_MAX)')
    out(p, "the output path (default: production/src/renders/<piece>/<piece>.master.mp4, or .master.wav for an "
           "audio master)")
    p.set_defaults(func=V.cmd_assemble)

    p = sub.add_parser("cut", help="trim, reframe and encode one deliverable")
    p.add_argument("src")
    p.add_argument("--deliverable", required=True, metavar="KEY")
    p.add_argument("--in", dest="cut_in", required=True, metavar="TC")
    p.add_argument("--out", dest="cut_out", required=True, metavar="TC")
    p.add_argument("--cut", metavar="cNN")
    p.add_argument("--frame", choices=("crop", "pad"), default="crop")
    p.add_argument("--x", type=int, metavar="PX", help="crop's left edge in source pixels")
    p.add_argument("--captions", metavar="SRT", help="burn these captions in the same pass")
    p.add_argument("--overlay", metavar="PNG", help="lay this transparent PNG (card.py render --transparent, at "
                   "the deliverable's own size; any other size is refused) over every frame, the first included")
    out(p, "the output path (default: publishing/src/renders/<piece>/<piece>[--cNN].<platform>-<format>[.burned]"
           ".<ext>; a source whose name has no piece key, at the folder's top)")
    p.set_defaults(func=V.cmd_cut)

    p = sub.add_parser("encode", help="encode a whole file to a deliverable, loudness included")
    p.add_argument("src")
    p.add_argument("--deliverable", required=True, metavar="KEY")
    p.add_argument("--frame", choices=("crop", "pad"),
                   help="how a picture of another shape fills the deliverable's frame; required when the "
                        "shapes differ (encode never crops unasked)")
    out(p, "the output path (default: publishing/src/renders/<piece>/<piece>.<platform>-<format>.<ext>; a source "
           "whose name has no piece key, at the folder's top)")
    p.set_defaults(func=V.cmd_encode)

    p = sub.add_parser("frame", help="one PNG still")
    p.add_argument("src")
    p.add_argument("--at", required=True, metavar="TC")
    out(p, "the output path (default: publishing/src/renders/<piece>/<stem>.<HH-MM-SS-mmm>.png; a source whose "
           "name has no piece key, at the folder's top)")
    p.set_defaults(func=V.cmd_frame)

    p = sub.add_parser("image", help="encode one image deliverable from a still or a frame of a video",
                       description="Scales a PNG or other still (a card.py render, a frame, an asset or a design "
                       "export), or a video's frame at --at (a poster: the deliverable's own render), to the table's "
                       "width and height, and writes it in the table's first format, or in --format where that is "
                       "another of the table's formats; transparency is flattened where the table sets alpha = false "
                       "(and always for jpg and avif). Size, codec, alpha, min_width and max_size are verified; over "
                       "max_size_mobile is a warning. A source of another shape needs --frame; a GIF is cut's; a table "
                       "with no width and height renders with card.py --size. A PNG already at the size, asked for as "
                       "png with no -o, is verified where it stands and nothing is written. Default output: "
                       "publishing/src/renders/<piece>/<stem>.<platform>-<format>.<ext>, <stem> the source's name up "
                       "to its first '.' and <piece> its leading piece key (a stem with none, such as a show cover's "
                       "design export, at the folder's top).")
    p.add_argument("src")
    p.add_argument("--deliverable", required=True, metavar="KEY")
    p.add_argument("--at", metavar="TC", help="the frame of a video source (required for a video)")
    p.add_argument("--format", choices=("jpg", "png", "webp", "avif"), metavar="jpg|png|webp|avif",
                   help="one of the table's formats (default: its first)")
    p.add_argument("--frame", choices=("crop", "pad"), metavar="crop|pad",
                   help="how a picture of another shape fills the deliverable's frame; required when the shapes "
                        "differ (image never crops unasked)")
    out(p)
    p.set_defaults(func=I.cmd_image)

    p = sub.add_parser("still-video", help="a still under audio, as video")
    p.add_argument("image")
    p.add_argument("audio")
    p.add_argument("--deliverable", required=True, metavar="KEY")
    out(p, "the output path (default: publishing/src/renders/<piece>/<piece>.<platform>-<format>.mp4, the piece "
           "from AUDIO's name; an AUDIO whose name has no piece key, at the folder's top)")
    p.set_defaults(func=V.cmd_still_video)

    p = sub.add_parser("extract-audio", help="mono 16-bit WAV for speech-to-text or alignment")
    p.add_argument("src")
    p.add_argument("--in", dest="cut_in", metavar="TC")
    p.add_argument("--out", dest="cut_out", metavar="TC")
    p.add_argument("--rate", type=int, default=16000, metavar="HZ")
    out(p, "the output path (default: production/src/renders/<piece>/<stem>[.<in>-<out>].wav, <piece> the "
           "stem's leading piece key, or the folder's top for a stem with none, such as a footage file's)")
    p.set_defaults(func=A.cmd_extract)

    p = sub.add_parser('transcribe', help='align approved known words offline; fetch is the author-run setup')
    p.add_argument('piece', help='PIECE, or fetch for the one deliberate model download')
    p.add_argument('--no-cross-check', action='store_true', help='disable the heard-word cross-check, recorded in the check')
    out(p, 'the words JSON path (default: production/src/renders/<piece>/timing/<piece>.words.json); its check is beside it')
    p.set_defaults(func=A.cmd_transcribe)

    p = sub.add_parser('lipsync', help='Rhubarb mouth shapes from approved plain text and the joined voice')
    p.add_argument('piece')
    out(p, 'the mouth JSON path (default: production/src/renders/<piece>/timing/<piece>.mouth.json)')
    p.set_defaults(func=A.cmd_lipsync)

    p = sub.add_parser('cues', help='exact board, line, word and event timings; print the re-timed storyboard')
    p.add_argument('piece')
    out(p, 'the cues JSON path (default: production/src/renders/<piece>/timing/<piece>.cues.json)')
    p.set_defaults(func=K.cmd_cues)

    p = sub.add_parser('real', help='index shot-list images and text captures; never open the footage mirror')
    p.add_argument('piece')
    out(p, 'the real JSON path (default: production/src/renders/<piece>/timing/<piece>.real.json)')
    p.set_defaults(func=R.cmd_real)

    p = sub.add_parser("captions", help="check, from-segments, from-words, align, retime, rewrap, vtt, transcript, burn")
    cs = p.add_subparsers(dest="sub", metavar="action")
    q = cs.add_parser("check", help="limits, overlaps and gaps; the words against a script")
    q.add_argument("srt")
    q.add_argument("--deliverable", metavar="KEY")
    q.add_argument("--script", metavar="SCRIPT", help="a script.md or a transcript.md")
    q.set_defaults(func=K.cmd_check)
    q = cs.add_parser("from-segments", help="captions timed by the approved voiceover segments")
    q.add_argument("register")
    q.add_argument("--deliverable", required=True, metavar="KEY")
    q.add_argument("--offset", metavar="TC", help="where the voice track starts on the master")
    out(q, "the output path (default: publishing/src/renders/<piece>/<piece>.<platform>-<format>.en-GB.srt)")
    q.set_defaults(func=K.cmd_from_segments)
    q = cs.add_parser('from-words', help='captions at the aligned words’ boundaries')
    q.add_argument('words', help='the accepted words JSON file')
    q.add_argument('--deliverable', required=True, metavar='KEY')
    q.add_argument('--offset', metavar='TC', help='where the voice starts on the master')
    out(q, 'the output path (default: publishing/src/renders/<piece>/<piece>.<platform>-<format>.en-GB.srt)')
    q.set_defaults(func=K.cmd_from_words)
    q = cs.add_parser("align", help="captions spread over the speech silencedetect finds")
    q.add_argument("text", help="a script.md or a transcript.md")
    q.add_argument("audio")
    q.add_argument("--lines", metavar="B.L-B.L", help="only these spoken lines (one cut's)")
    q.add_argument("--anchors", action="store_true", help="hold each beat inside its anchored interval")
    q.add_argument("--noise", type=float, default=-35.0, metavar="DB")
    q.add_argument("--min-silence", type=float, default=0.3, metavar="S")
    out(q, STDOUT_HELP)
    q.set_defaults(func=K.cmd_align)
    q = cs.add_parser("retime", help="master timing to a cut's, or recording timing to the master's")
    q.add_argument("srt")
    q.add_argument("--in", dest="cut_in", metavar="TC")
    q.add_argument("--out", dest="cut_out", metavar="TC")
    q.add_argument("--edl", metavar="EDL")
    q.add_argument("--source", metavar="FID")
    out(q, STDOUT_HELP)
    q.set_defaults(func=K.cmd_retime)
    q = cs.add_parser("rewrap", help="re-chunk to a deliverable's line width")
    q.add_argument("srt")
    q.add_argument("--deliverable", required=True, metavar="KEY")
    out(q, STDOUT_HELP)
    q.set_defaults(func=K.cmd_rewrap)
    q = cs.add_parser("vtt", help="SRT to WebVTT")
    q.add_argument("srt")
    out(q, STDOUT_HELP)
    q.set_defaults(func=K.cmd_vtt)
    q = cs.add_parser("transcript", help="the published transcript of a piece or of one cut's lines",
                      description="The published transcript, <piece>[--cNN].transcript.en-GB.md, from a script.md "
                      "or a transcript.md: the spoken words as the record spells them, one sentence per line, a "
                      "paragraph per beat; speaker names only where two or more people speak; a TEXT cue as "
                      "[On screen: …], an SFX or MUSIC cue as a bracketed sound; NOTE cues and braced directions "
                      "dropped; 'As recorded on DD/MM/YYYY' from --date or, for a transcript.md, its recording's "
                      "recorded date in the manifest. What the picture shows is described by hand.")
    q.add_argument("text", help="a script.md or a transcript.md")
    q.add_argument("--lines", metavar="B.L-B.L", help="only these spoken lines (one cut's, as captions align --lines)")
    q.add_argument("--date", metavar="DD/MM/YYYY", help="the recording's date, for the 'As recorded on' line")
    p_md = ("the output path; without -o the transcript goes to stdout and every report line to stderr (its "
            "home, publishing/src/captions/, is tracked, so the toolkit never chooses a path there; an existing "
            "file there is never overwritten)")
    q.add_argument("-o", metavar="MD", help=p_md)
    q.set_defaults(func=K.cmd_transcript)
    q = cs.add_parser("burn", help="burn captions in (ASS at the output size)")
    q.add_argument("src")
    q.add_argument("srt")
    q.add_argument("--deliverable", required=True, metavar="KEY")
    out(q, "the output path (default: publishing/src/renders/<piece>/<stem>.burned.mp4; a source whose name has "
           "no piece key, at the folder's top)")
    q.set_defaults(func=K.cmd_burn)

    p = sub.add_parser("loudness", help="measure, normalise")
    ls = p.add_subparsers(dest="sub", metavar="action")
    q = ls.add_parser("measure", help="integrated loudness, true peak and loudness range")
    q.add_argument("file")
    q.set_defaults(func=A.cmd_measure)
    q = ls.add_parser("normalise", help="two-pass loudnorm to social, podcast or acx")
    q.add_argument("file")
    q.add_argument("--target", required=True, choices=("social", "podcast", "acx"))
    out(q)
    q.set_defaults(func=A.cmd_normalise)

    p = sub.add_parser("audiobook", help="text, master, check")
    bs = p.add_subparsers(dest="sub", metavar="action")
    q = bs.add_parser("text", help="a chapter's spoken text, in chunks under the model's limit",
                      description="Writes <piece>.chNN.pNN.txt chunks to the audiobook folder's generated/; "
                      "a chunk ends at every {pause N} (a scene break is {pause 2}), and the pause after "
                      "each chunk goes in the sidecar <piece>.chNN.chunks.toml, never in the text. Exit 1 "
                      "lists what has no spoken form: constructed-language spans, Greek and Hebrew, "
                      "scripture references, citation keys, abbreviations with no row in voice.md's "
                      "Pronunciations, and every table and image, which are left out of the text. Exit 2 "
                      "when the chapter register's channels name anything but an [audiobook.<store>] store "
                      "of platforms.toml (acx, google_play, …).")
    q.add_argument("source", help="the chapter's source; for ch00 and ch99 the credits' own file, "
                   "<piece>.ch00.md or <piece>.ch99.md beside the chapter register (an audiobook has no script)")
    q.add_argument("--piece", required=True)
    q.add_argument("--chapter", required=True, metavar="chNN",
                   help="the chapter; ch00 is the opening credits and ch99 the closing credits")
    q.add_argument("--footnotes", choices=("drop", "inline"), default="drop")
    q.add_argument("--limit", type=int, metavar="CHARS")
    q.set_defaults(func=A.cmd_ab_text)
    q = bs.add_parser("master", help="join takes, add room tone, master to ACX, MP3",
                      description="Joins the takes (in the sidecar's chunk order, with exactly its room "
                      "tone after each chunk, when they are named <piece>.chNN.pNN.tN), adds head and tail "
                      "room tone, masters to the ACX profile and checks the result. Room tone is the room's "
                      "own: --room-tone FILE, else the quietest stretch of the takes, looped; never digital "
                      "silence where a room can be heard. The mastered chapter is what M4 needs approved "
                      "and archived. Exit 2 when the chapter register's channels name anything but an "
                      "[audiobook.<store>] store of platforms.toml.")
    q.add_argument("chunks", nargs="+", metavar="CHUNKS", help="the approved take of each chunk, or a recording")
    q.add_argument("--piece", required=True)
    q.add_argument("--chapter", required=True, metavar="chNN")
    q.add_argument("--head", type=float, default=A.ACX_HEAD, metavar="S")
    q.add_argument("--tail", type=float, default=A.ACX_TAIL, metavar="S")
    q.add_argument("--room-tone", metavar="FILE", help="a recording of the room, looped for the head, the "
                   "tail and every pause (default: the quietest stretch of the takes themselves)")
    out(q, "the output path (default: the audiobook folder's renders/<piece>.chNN.mp3)")
    q.set_defaults(func=A.cmd_ab_master)
    q = bs.add_parser("check", help="ACX: RMS, peak, noise floor, rate, CBR, channels, length, room tone")
    q.add_argument("files", nargs="+")
    q.set_defaults(func=A.cmd_ab_check)

    p = sub.add_parser("take", help="take add")
    ts = p.add_subparsers(dest="sub", metavar="add")
    q = ts.add_parser("add", help="name a fresh ElevenLabs take; register and credits-log rows",
                      description="Renames a fresh ElevenLabs file where it lies, to its house name: a voiceover "
                      "take in production/src/voiceover/generated/<piece>/takes/, or flat in generated/ where an "
                      "earlier release kept takes, numbered after the segment's highest take in either; an "
                      "audiobook part's in the audiobook folder's generated/. Writes the register's take and "
                      "file, and for a segment resets status to generated and archived to empty (a re-roll); "
                      "appends the credits-log row. A voice trial (generated/voice-trials/<name>/) is never a "
                      "take, and is refused.")
    q.add_argument("file")
    q.add_argument("--piece", required=True)
    q.add_argument("--segment", metavar="sNN")
    q.add_argument("--chapter", metavar="chNN")
    q.add_argument("--part", metavar="pNN")
    q.set_defaults(func=A.cmd_take_add)

    p = sub.add_parser("speak", help="offline voice request planning")
    ss = p.add_subparsers(dest="sub", metavar="action")
    q = ss.add_parser("plan", help="print request text, characters and calls; create the output folder",
                     description="Offline: applies voice.md pronunciations and supported delivery tags from "
                     "the script; prints character counts and calls, never credits. Skips approved takes "
                     "unless --segment names them. Creates only the takes folder, or --trial's trial folder.")
    q.add_argument("piece", nargs="?", metavar="PIECE")
    q.add_argument("--segment", action="append", metavar="sNN", help="plan this segment, repeat for more")
    q.add_argument("--trial", metavar="NAME", help="create only this voice trial's output directory")
    q.set_defaults(func=A.cmd_speak_plan)

    p = sub.add_parser("voice", help="join approved voice takes")
    vs = p.add_subparsers(dest="sub", metavar="action")
    q = vs.add_parser("join", help="join the approved takes in register order, with pause_after",
                     description="One mono 16-bit WAV at the register's sample rate, using each row's file "
                     "and pause_after; exit 1 while any segment is not approved.")
    q.add_argument("piece", metavar="PIECE")
    out(q, "the WAV path (default: production/src/renders/<piece>/<piece>.voice.wav)")
    q.set_defaults(func=A.cmd_voice_join)

    p = sub.add_parser("levels", help="RMS windows of the joined voice, as finite JSON",
                       description="Reads the joined voice. Writes only a working copy under "
                       "production/src/renders/<piece>/timing/, with silence floored at -120 dBFS; no -o.")
    p.add_argument("piece", metavar="PIECE")
    p.add_argument("--window", type=float, default=0.1, metavar="S", help="window seconds (default: 0.1)")
    p.set_defaults(func=A.cmd_levels)

    p = sub.add_parser("feed", help="a self-hosted podcast: new, add, tag, write, chapters, check",
                       description="A self-hosted show's register, publishing/src/podcast/<show>.toml (where the "
                       "project self-hosts a podcast), and the RSS feed, chapters and file tags made from it. "
                       "Offline: nothing is fetched or posted; the author uploads.")
    fe = p.add_subparsers(dest="sub", metavar="action")
    q = fe.add_parser("new", help="open a show's register, with its podcast:guid",
                      description="Writes publishing/src/podcast/<SHOW>.toml from the register's skeleton, with the "
                      "feed URL, the site and the show's podcast:guid (the UUIDv5 of the feed URL without its scheme "
                      "and trailing slashes, written once), and flags owner_email for the author. Refuses a show that "
                      "exists, and a project without the podcast folder (exit 2: copier update -a "
                      ".copier-answers.syntek-media.yml adds it). --rekey rewrites the feed URL, the podcast:guid and "
                      "every episode's guid of an existing show, only while no row is published and no tracked feed "
                      "exists.")
    q.add_argument("show", metavar="SHOW", help="the show's kebab slug, frozen")
    q.add_argument("--feed-url", required=True, metavar="URL", help="the feed's permanent https URL")
    q.add_argument("--site", metavar="SLUG", help="the website profile's slug of the site serving the feed")
    q.add_argument("--rekey", action="store_true", help="correct a provisional feed URL before anything is published")
    q.set_defaults(func=F.cmd_new)
    q = fe.add_parser("add", help="append an episode's row, with its guid",
                      description="Appends the piece's [[episode]] row, status planned, with its guid (the UUIDv5 of "
                      "the piece under the show's podcast:guid), written once; refuses a piece already in the "
                      "register, and one with no folder under scripts/src/pieces/.")
    q.add_argument("show", metavar="SHOW")
    q.add_argument("--piece", required=True, metavar="PIECE")
    q.set_defaults(func=F.cmd_add)
    q = fe.add_parser("tag", help="write the episode's ID3 tags, chapters and cover into its M5 render",
                      description="Re-muxes publishing/src/renders/<PIECE>/<PIECE>.podcast-feed-audio.mp3 without "
                      "re-encoding (-c:a copy), old tags and chapters dropped: ID3v2.3 title, the show's author and "
                      "title, the number, the chapters (CTOC and CHAP) and the show's id3_cover; verifies the audio "
                      "stream unchanged and the tags present, then writes render, bytes and seconds into the row. Exit "
                      "1, changing nothing, while the row's title or description is empty, its chapters break the "
                      "[platform.podcast] rules, or the show has no title or author; exit 2 for a withdrawn row or "
                      "a render missing from the piece's folder (encode it at M5: "
                      "publishing/workflows/02-cut-for-a-platform/); a flat render an earlier release left at the "
                      "top of publishing/src/renders/ is named, never tagged.")
    q.add_argument("show", metavar="SHOW")
    q.add_argument("--piece", required=True, metavar="PIECE")
    q.set_defaults(func=F.cmd_tag)
    q = fe.add_parser("write", help="the show's RSS feed as of a time",
                      description="The RSS 2.0 feed of every ready or published episode whose pub_date is not after "
                      "--as-of (required: a static feed has no clock, and none is read), newest first, in the "
                      "project's timezone; the same register and --as-of always give the same bytes. Before writing "
                      "anything it compares the feed with the tracked publishing/src/podcast/<SHOW>.feed.xml where "
                      "one exists, and exits 1, writing nothing, when the show's podcast:guid differs, a GUID of the "
                      "tracked copy has vanished while its row is not withdrawn, or an enclosure's length changed "
                      "under the same URL.")
    q.add_argument("show", metavar="SHOW")
    q.add_argument("--as-of", required=True, metavar="'DD/MM/YYYY HH:MM'",
                   help="the moment the feed describes: the episode's pub_date, the time it is uploaded")
    q.add_argument("-o", metavar="FILE", help=FEED_HELP)
    q.set_defaults(func=F.cmd_write)
    q = fe.add_parser("chapters", help="the episode's Podcasting 2.0 JSON chapters",
                      description="JSON chapters (version 1.2, startTime in float seconds) from the row's "
                      "[[episode.chapter]] tables; default publishing/src/renders/<PIECE>/<PIECE>.chapters.json.")
    q.add_argument("show", metavar="SHOW")
    q.add_argument("--piece", required=True, metavar="PIECE")
    q.add_argument("-o", metavar="FILE",
                   help="the output path (default: publishing/src/renders/<piece>/<piece>.chapters.json)")
    q.set_defaults(func=F.cmd_chapters)
    q = fe.add_parser("check", help="the register, or a saved feed, offline",
                      description="Offline, never fetching: the register (or, with --feed, a saved or CMS-made feed) "
                      "against the register's rules and the [platform.podcast] keys: every required value set and no "
                      "AUTHOR TO CONFIRM flag left; GUIDs and enclosure URLs unique; the comparison feed write makes, "
                      "against the tracked feed or --previous; bytes and seconds against the render where it is "
                      "local, in the episode's piece folder or, failing that, flat where an earlier release left it, "
                      "which a warning names; the cover and episode art against podcast.cover and "
                      "podcast.episode_art; the chapter "
                      "rules (a chapter under chapter_min_seconds warns); no '<' or '>' in a title or description; "
                      "ASCII URLs; a warning where site is empty while the website profile exists, and where the "
                      "owner address looks like a person's own.")
    q.add_argument("show", metavar="SHOW")
    q.add_argument("--feed", metavar="FILE", help="check this saved feed instead of the register")
    q.add_argument("--previous", metavar="FILE", help="compare with this feed instead of the tracked copy")
    q.set_defaults(func=F.cmd_check)

    p = sub.add_parser("footage", help="add, verify")
    fs = p.add_subparsers(dest="sub", metavar="action")
    q = fs.add_parser("add", help="copy into the mirror, hash, and log the next F ID")
    q.add_argument("file")
    q.add_argument("--kind", required=True, choices=R.KINDS)
    q.add_argument("--location", required=True, metavar="LABEL")
    q.add_argument("--rights", metavar="RRNNNN")
    q.set_defaults(func=R.cmd_footage_add)
    q = fs.add_parser("verify", help="the local mirror against the manifest")
    q.add_argument("--manifest", metavar="PATH")
    q.set_defaults(func=R.cmd_footage_verify)

    p = sub.add_parser("tokens", help="every required custom property of tokens.css")
    p.add_argument("--tokens", metavar="PATH")
    p.set_defaults(func=R.cmd_tokens)

    p = sub.add_parser("flags", help="AUTHOR TO CONFIRM and VERIFY across the media layers")
    p.add_argument("paths", nargs="*", metavar="PATH")
    p.add_argument("--piece", metavar="PIECE", help="only that piece's files: its folder under "
                   "scripts/src/pieces/ and every file in scripts/, production/ and publishing/ (or "
                   "under the PATHs given) named <piece>.… or <piece>--cNN.…, its timing/ and scenes/ "
                   "files included (M7 needs zero)")
    p.add_argument("--strict", action="store_true", help="exit 1 when any flag is open")
    p.set_defaults(func=R.cmd_flags)

    p = sub.add_parser("where", help="a piece's files across the layers, and its ignored folders by name",
                       description="Prints the piece's files git tracks or would track across scripts/, "
                       "production/ and publishing/, gathered as flags --piece gathers them (its timing and "
                       "scene files included), then names its ignored per-piece folders, "
                       "production/src/renders/<piece>/, production/src/voiceover/generated/<piece>/ and "
                       "publishing/src/renders/<piece>/, each said to exist or not and never listed (DESIGN "
                       "D50, D64).")
    p.add_argument("piece", metavar="PIECE")
    p.set_defaults(func=R.cmd_where)

    p = sub.add_parser("score", help="Jev title/thumbnail option scoring (plan is offline)")
    score = p.add_subparsers(dest="action", required=True)
    for action in ("plan", "run"):
        p = score.add_parser(action, help="offline request preview" if action == "plan" else
                            "one explicitly approved paid TypeSafe request")
        p.add_argument("input", metavar="INPUT", help="candidate/context JSON; see scoring-options.md")
        p.add_argument("--rubric", metavar="TOML", help="author-owned rubric copy, with its own version")
        p.add_argument("--model", default="jev-latest", help="Jev model/alias; resolved version is recorded")
        p.add_argument("--today", metavar="DD/MM/YYYY", help="guidance freshness date; defaults to today")
        p.add_argument("-o", "--output", metavar="JSON", help="new JSON file; otherwise stdout; never overwrite")
        if action == "run":
            p.add_argument("--approve-call", action="store_true", help="author has approved this paid call")
        p.set_defaults(func=J.cmd_score, approve_call=False)

    p = sub.add_parser("check", help="the repository guard; --setup adds the readiness report")
    p.add_argument("--strict", action="store_true", help="warnings count as findings")
    p.add_argument("--setup", action="store_true")
    p.set_defaults(func=R.cmd_check)
    return ap


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = build_parser()
    args = ap.parse_args(argv)
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    try:
        return args.func(args)
    except C.Finding as err:
        print(f"FAIL {err}")
        return 1
    except C.Fatal as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2


# ── Self-test ───────────────────────────────────────────────────────────────────────────

TOKENS_CSS = """:root {
  --color-bg: #101418; --color-surface: #1c232b; --color-text: #f4f1ea;
  --color-text-muted: #b9b4aa; --color-accent: #d4a24c; --color-on-accent: #101418;
  --font-display: "Fixture Display", sans-serif; --font-body: sans-serif;
  --weight-display: 700; --weight-body: 400; --space-unit: 8px; --radius: 6px;
  --caption-font: CAPTION_FONT; --caption-weight: 700; --caption-size: 4.5vh;
  --caption-text: #FFFFFF; --caption-outline: #000000; --caption-outline-width: 0.4vh;
}
"""
OVERRIDES_TOML = """# overrides.toml (self-test fixture)
[[override]]
key = "tiktok.video.max_seconds"
value = 1
why = "fixture"
source = "fixture"
checked = "01/09/2026"

[[override]]
key = "instagram.hashtags_max"
value = 4
why = "fixture"
source = "fixture"
checked = "01/09/2026"

[[override]]
key = "youtube.long.max_seconds"
value = "long"
why = "a wrong type, which is ignored"
source = "fixture"
checked = "01/09/2026"
"""
VOICE_MD = """# voice.md (self-test fixture)

## Narrators

| Use | Service | Voice | Voice ID | Model ID | Stability | Similarity | Style | Speed | Output format | Consent | Chosen |
|---|---|---|---|---|---|---|---|---|---|---|---|
| voiceover | ElevenLabs | Fixture Voice | fixture | eleven_v4 | 0.5 | 0.75 | 0 | 1.0 | mp3_44100_128 | — | 01/01/2026 |
| narration | ElevenLabs | Fixture Narrator | fixture | eleven_v4 | 0.5 | 0.75 | 0 | 1.0 | pcm_44100 | — | 01/01/2026 |

## Pronunciations

| Word | IPA | Respelling | Source | Notes |
|---|---|---|---|---|
| Tharvel | ˈθɑːvəl | THAR-vel | fixture | |
"""
CREDITS_MD = """# credits-log.md (self-test fixture)

| Date | Piece | Tool | Calls | Characters or minutes | Voice | Model | Output | Notes |
|---|---|---|---|---|---|---|---|---|
"""
SCRIPT_MD = """---
piece: 001-fixture
version: 1
approved: ""
words: 0
estimated_seconds: 0
---

# Fixture — script

## 1. Hook (target 00:03)

VO: {brisk} The ferry is late again.
TEXT: Late again?

## 2. The tide decides (target 00:10)

ON: Every crossing waits for the tide, not the timetable.
SFX: gulls, low
ON: {pause 0.6} So the timetable is a promise the sea never signed.
"""
BRIEF_MD = """---
piece: 001-fixture
title: "Fixture"
kind: short-video
origin: scripted
status: scripted
deliverables: [youtube.short, instagram.reel]
target_seconds: 10
words_per_minute: 150
verified: {}
---
"""
TRANSCRIPT_MD = """---
piece: 001-fixture
source: F0003
made: by hand
approved: ""
---

# Fixture — transcript

## 1. Opening (at 00:00:00.500)

HOST: The harbour opens at dawn.
HOST: Boats leave on the tide.

## 2. Close (at 00:00:04.500)

HOST: We wait for the light.
HOST: Then we go out together.
"""
CHAPTER_MD = """<!-- EXAMPLE CHAPTER, a fixture. -->

# The Ford

<!-- section: opening -->

::: epigraph
'Count the stones, and the river lets you pass.'

— a saying of the [hebori]{.conlang lang=example-tongue}
:::

The last window went dark [@doe2020, p. 4].
[Tharvel]{.conlang lang=example-tongue} counted a hundred breaths.[^1] <!-- AUTHOR TO CONFIRM: a fixture flag -->

* * *

The river was louder in the dark, as John 3:16 was louder in the mind.

::: scene-break
:::

She stepped down.

[^1]: A breath is a count of four.
"""
CHAPTER_REG = """---
piece: 002-fixture-book
route: ai
channels: [spotify_authors]
voice_use: narration
model_id: eleven_v4
output_format: pcm_22050
---

| Ch | Title | Source | Route | Takes | Master | Duration | Check | Status |
|---|---|---|---|---|---|---|---|---|
| ch01 | The Ford | provided | ai |  |  |  |  | planned |
"""


CHAPTER_REG_NO_FORMAT = """---
piece: 008-fixture-voice-format
route: ai
channels: [spotify_authors]
voice_use: narration
model_id: eleven_v4
---

| Ch | Title | Source | Route | Takes | Master | Duration | Check | Status |
|---|---|---|---|---|---|---|---|---|
| ch00 | Opening credits | 008-fixture-voice-format.ch00.md | ai |  |  |  |  | planned |
| ch01 | The Ford | provided | ai |  |  |  |  | planned |
"""
CREDITS_CH00_MD = """The Ford, a fixture.
Read by a fixture narrator.
"""
SCRIPT_SHAPED_MD = """# The Ford — script

## Opening credits

NARRATOR: The Ford, a fixture.

## Chapters

1. The Ford — manuscript/src/01-the-ford/01-the-ford.md
"""
BUSINESS_CHAPTER_MD = """# Running the studio

HLS takes bookings by the week.

| Step | What to do |
|------|-----------------|
| 1 | Pick a date |
| 2 | Pay the deposit |

: Booking checklist

![Chart of bookings by month](chart.png)

See [the guide][g] for the rest.

[g]: https://example.org/guide
"""


def self_test() -> int:
    """Prove each module does what its docstring says, on fixtures written at run time."""
    failures = []

    def verdict(label, passed, detail=""):
        print(f"  {'ok  ' if passed else 'FAIL'} {label}")
        if not passed:
            failures.append(label)
            print(f"         {str(detail)[-1500:]}")

    def skip(label, why):
        print(f"  skip {label}: {why}")

    def cli(*argv):
        code, out, err = cli_split(*argv)
        return code, out + err

    print("media.py --self-test")
    given = dict(os.environ)
    saved_root, saved_preset, saved_zone = C.ROOT, C.X264_PRESET, C.TIMEZONE
    rendered_zone = not C.TIMEZONE.startswith("<")
    C.X264_PRESET = "ultrafast"
    C.TIMEZONE = "Europe/London"   # the fixtures' feed dates are written for this zone
    have_ff = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
    have_git = bool(shutil.which("git"))
    with tempfile.TemporaryDirectory(prefix="media-self-test-") as tmp, hermetic_git(Path(tmp) / "gitconfig"), \
            held_env(drop=('MEDIA_MEMORY_MAX', '_MEDIA_MEMORY_CAPPED', '_MEDIA_MEMORY_RECEIPT')):
        root = Path(tmp) / "project"
        C.ROOT = root
        try:
            write_fixture(root)
            groups = [("presets, timecodes and tokens", lambda: test_common(verdict, cli)),
                      ("captions and script time", lambda: test_captions(verdict, cli, root)),
                      ("footage, takes in both layouts, audiobook text, flags, where and check",
                       lambda: test_repo(verdict, skip, cli, root, have_git, have_ff)),
                      ("uv scripts: the interpreter, the timeout, the first-run lock, card renders and the "
                       "setup row", lambda: test_uv(verdict, skip, cli, root)),
                      ("default output paths: each piece's own folder", lambda: test_piece_defaults(verdict))]
            groups.append(('deterministic scene timing and safe zones', lambda: test_scene_timing(verdict)))
            groups.append(('offline Jev scoring and paid-call boundaries', lambda: J.self_test(verdict)))
            groups.append(('scene layouts, movement, interaction and local sources', lambda: test_scene_model(verdict)))
            groups.append(('streamed frame input and opt-in memory scopes', lambda: test_render_helpers(verdict, root)))
            groups.append(('eight- and nine-column storyboard input', lambda: test_storyboards(verdict, root)))
            groups.append(('cue index, script events and audio cue links',
                           lambda: test_cues(verdict, cli, root, have_git)))
            groups.append(('real source hashes, metadata and tracked-output guards',
                           lambda: test_real(verdict, cli, have_git)))
            groups.append(("offline voice plans and tracked timing guards",
                           lambda: test_voice_plan(verdict, skip, cli, root, have_git)))
            groups.append(('word alignment logic and captions from words',
                           lambda: test_words(verdict, cli, root)))
            if have_ff:
                groups.append(("the shared sound of both master routes", lambda: test_shared_mix(verdict)))
                groups.append(("cut, burn-in, loudness, assemble, align and the audiobook master",
                               lambda: test_media(verdict, skip, cli, root)))
                groups.append(("image, the GIF preview, the silent loop and web video",
                               lambda: test_web(verdict, skip, cli, root)))
                groups.append(("the podcast feed: register, tags, feed, chapters and checks",
                               lambda: test_feed(verdict, skip, cli, root, saved_zone if rendered_zone else None)))
                groups.append(('transcribe launcher and paired output guards',
                               lambda: test_transcribe(verdict, cli, root, have_git)))
                groups.append(('Rhubarb dialogue, resources, exits and tracked mouth guards',
                               lambda: test_lipsync(verdict, skip, cli, root, have_git)))
            else:
                skip("every ffmpeg probe (cut, burn-in, loudness, assemble, align, audiobook, image, GIF, "
                     "the podcast feed, transcribe launcher and lipsync)", "ffmpeg or ffprobe is not installed")
            for label, group in groups:
                try:
                    group()
                except Exception as err:  # a broken probe is a failure, never a crash
                    import traceback
                    verdict(f"{label}: ran to the end", False,
                            f"{type(err).__name__}: {err}\n{traceback.format_exc()}")
        finally:
            C.ROOT, C.X264_PRESET, C.TIMEZONE = saved_root, saved_preset, saved_zone
    changed = sorted(k for k in set(given) | set(os.environ) if given.get(k) != os.environ.get(k))
    verdict("the self-test hands back the environment it was given, git's variables included",
            not changed, f"changed: {', '.join(changed)}")
    if failures:
        print(f"self-test FAILED: {len(failures)} case(s)")
        return 1
    print("self-test passed")
    return 0


def test_real(verdict, cli, have_git: bool) -> None:
    """D69: named assets and offline footage metadata, with the approved source schema."""
    saved_root = C.ROOT
    with tempfile.TemporaryDirectory(prefix='media-real-test-') as temp:
        root = Path(temp) / 'project'
        C.ROOT = root
        piece = '923-real-fixture'
        shot = root / C.PIECES / piece / 'shot-list.md'
        default = root / C.PROD_RENDERS / piece / 'timing' / f'{piece}.real.json'
        tracked = root / C.SCENES / f'{piece}.real.json'
        asset = write(root / C.ASSETS / 'real-image.svg', '<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2"/></svg>')
        captures = [write(root / C.ASSETS / ('real-capture' + ext), 'ready\n')
                    for ext in ('.txt', '.ansi', '.html')]
        manifest = write(root / C.MANIFEST, ''.join(
            f'[[file]]\nid="{fid}"\npath="raw/{name}"\nkind="{kind}"\nduration={seconds}\nsha256="' + 'b' * 64 + '"\n'
            for fid, name, kind, seconds in (('F0401', 'offline.png', 'image', 0.0),
                ('F0402', 'video.mp4', 'video', 1.0), ('F0403', 'sound.wav', 'audio', 0.0),
                ('F0404', 'moving.gif', 'image', 1.0))))
        def shots(sources):
            write(shot, '| Shot | Board | Type | Source | Framing | Seconds | Status | Rights |\n'
                  '|------|-------|------|--------|---------|---------|--------|--------|\n' +
                  ''.join(f'| S{i:02d} | b01 | still | {source} | native | 1 | cleared | — |\n'
                          for i, source in enumerate(sources, 1)))
        def indexed(): return json.loads(default.read_text(encoding='utf-8'))
        wanted = [f'{C.SCENES}/{piece}.scene.py', str(asset.relative_to(root)),
                  *(str(p.relative_to(root)) for p in captures), 'F0401', str(asset.relative_to(root))]
        try:
            shots(wanted)
            before = {p: p.read_bytes() for p in (shot, asset, manifest, *captures)}
            code, text = cli('real', piece)
            data = indexed()
            verdict('real hashes assets and all three text capture formats in the approved schema',
                    code == 0 and data['piece'] == piece and len(data['sources']) == 5 and
                    data['sources'][0] == {'source': str(asset.relative_to(root)), 'kind': 'image',
                       'path': str(asset.relative_to(root)), 'sha256': R.sha256(asset)} and
                    all(r['kind'] == 'text' and r['sha256'] == R.sha256(p)
                        for r, p in zip(data['sources'][1:4], captures)), text)
            verdict('real uses the footage manifest hash without opening an absent mirror',
                    data['sources'][4] == {'source': 'F0401', 'kind': 'image',
                      'path': C.RAW + '/offline.png', 'sha256': 'b' * 64} and not (root / C.RAW).exists(), text)
            verdict('real skips the scene file, deduplicates sources and changes no input',
                    all(p.read_bytes() == held for p, held in before.items()) and
                    'ready\n' not in text and 'SHA-256' in text and not tracked.exists(), text)
            absent = root / C.ASSETS / 'real-output-source.txt'
            shots([str(absent.relative_to(root))])
            alias, text = cli('real', piece, '-o', absent)
            shots(['F0401'])
            mirror_alias, _ = cli('real', piece, '-o', root / C.RAW / 'offline.png')
            verdict('real refuses an output that is also a missing asset or footage source',
                    (alias, mirror_alias) == (2, 2) and not absent.exists()
                    and not (root / C.RAW).exists(), text)
            shots(['production/src/assets/absent.txt', 'F9999'])
            code, text = cli('real', piece)
            verdict('real reports missing assets and footage IDs as findings',
                    code == 1 and 'missing' in text and indexed()['sources'] == [], text)
            shots(['F0402', 'F0403', 'F0404'])
            code, text = cli('real', piece)
            verdict('real refuses footage video, sound and moving images as findings',
                    code == 1 and text.count('not video or sound') == 3 and indexed()['sources'] == [], text)
            bad = [write(root / C.ASSETS / ('real-bad' + ext), 'not a capture')
                   for ext in ('.log', '.out', '.mp4')]
            big = root / C.ASSETS / 'real-large.txt'
            with big.open('wb') as stream: stream.seek(R.LARGE); stream.write(b'x')
            shots([*(str(p.relative_to(root)) for p in bad), str(big.relative_to(root)),
                   'production/src/assets/../footage/raw/offline.png', str(asset)])
            code, text = cli('real', piece)
            verdict('real refuses unsupported captures, large assets and paths outside assets',
                    code == 1 and '10 MB' in text and indexed()['sources'] == [], text)
            gif = write(root / C.ASSETS / 'real-moving.gif', 'runtime stand-in')
            webp = root / C.ASSETS / 'real-moving.webp'
            webp.write_bytes(b'RIFF' + b'\0' * 4 + b'WEBPVP8X' + b'\0' * 4 + b'\x02')
            frames = C.image_frames
            try:
                C.image_frames = lambda p, info=None: 2 if Path(p) == gif else frames(p, info)
                shots([str(gif.relative_to(root)), str(webp.relative_to(root))])
                code, text = cli('real', piece)
                verdict('real rejects animated assets using the existing moving-image classification',
                        code == 1 and text.count('moving media') == 2 and indexed()['sources'] == [], text)
            finally: C.image_frames = frames
            shots(wanted)
            if have_git:
                def git(*args):
                    return C.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.com',
                                  *args], cwd=root, what='real fixture git')
                git('init', '-q')
                write(root / '.gitignore', '/production/src/renders/\n')
                first, _ = cli('real', piece, '-o', tracked)
                git('add', '.'); git('commit', '-q', '-m', 'real fixture')
                old = tracked.read_bytes()
                asset.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding='utf-8')
                code, text = cli('real', piece, '-o', tracked)
                verdict('real replaces only its committed unchanged tracked index through -o',
                        first == 0 and code == 0 and tracked.read_bytes() != old and
                        json.loads(tracked.read_text())['sources'][0]['sha256'] == R.sha256(asset), text)
                dirty = tracked.read_bytes()
                refused, text = cli('real', piece, '-o', tracked)
                git('add', str(tracked.relative_to(root)))
                staged, _ = cli('real', piece, '-o', tracked)
                other = write(root / C.SCENES / 'other.json', '{}')
                other_code, _ = cli('real', piece, '-o', other)
                fresh_piece = '924-real-untracked'
                write(root / C.PIECES / fresh_piece / 'shot-list.md', shot.read_text())
                untracked = write(root / C.SCENES / f'{fresh_piece}.real.json', '{}')
                untracked_code, _ = cli('real', fresh_piece, '-o', untracked)
                C.ROOT = Path(temp) / 'outside'
                outside = write(C.ROOT / C.SCENES / f'{piece}.real.json', '{}')
                write(C.ROOT / C.PIECES / piece / 'shot-list.md', shot.read_text())
                outside_code, _ = cli('real', piece, '-o', outside)
                C.ROOT = root
                verdict('real protects dirty, staged, untracked, outside-Git and other existing outputs',
                        (refused, staged, other_code, untracked_code, outside_code) == (2, 2, 2, 2, 2)
                        and tracked.read_bytes() == dirty and other.read_text() == '{}'
                        and untracked.read_text() == '{}' and outside.read_text() == '{}', text)
        finally:
            C.ROOT = saved_root


def cli_split(*argv):
    """(exit code, stdout, stderr) of one media.py command run in this process; argparse's own
    refusal (a missing required argument) is its exit 2, as on the command line."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main([str(a) for a in argv])
        except SystemExit as stop:
            code = stop.code if isinstance(stop.code, int) else 2
    return code, out.getvalue(), err.getvalue()


def write(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


@contextlib.contextmanager
def held_env(drop=(), **values):
    """A context in which os.environ lacks the variables named in drop and carries values, every
    one of them restored after; each subprocess, the toolkit's own git among them, inherits it."""
    keys = set(drop) | set(values)
    saved = {k: os.environ[k] for k in keys if k in os.environ}
    for k in keys:
        os.environ.pop(k, None)
    os.environ.update(values)
    try:
        yield
    finally:
        for k in keys:
            os.environ.pop(k, None)
        os.environ.update(saved)


def hermetic_git(config: Path):
    """A context in which every git the self-test causes reads none of the machine's own files: no
    system configuration or attributes, a scratch global configuration in place of ~/.gitconfig,
    no global attributes or ignore file, and no GIT_ variable of the caller's (a hook's GIT_DIR, a
    'git -c' parent's GIT_CONFIG_PARAMETERS). A machine whose git configures an LFS filter would
    otherwise store the fixtures' LFS file as a pointer and pass the filter checks. HOME and
    XDG_CONFIG_HOME are left alone, because uv, Playwright and fontconfig read them; git 2.32 or
    later reads GIT_CONFIG_GLOBAL in their place. gc and maintenance stay off, so no background
    run writes into a fixture repository while it is removed."""
    write(config, "# media.py --self-test: the only global git configuration its fixtures read\n"
                  f"[core]\n\tattributesFile = {os.devnull}\n\texcludesFile = {os.devnull}\n"
                  "[gc]\n\tauto = 0\n[maintenance]\n\tauto = false\n")
    return held_env(drop=[k for k in os.environ if k.startswith("GIT_")], GIT_CONFIG_NOSYSTEM="1",
                    GIT_ATTR_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(config))


def git_version() -> tuple:
    proc = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return tuple(int(n) for n in re.findall(r"\d+", proc.stdout)[:2])


def caption_family() -> str:
    if shutil.which("fc-match"):
        proc = subprocess.run(["fc-match", "-f", "%{family[0]}", "sans-serif"], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            return f'"{proc.stdout.strip()}"'
    return "sans-serif"


def write_fixture(root: Path) -> None:
    write(root / C.TOKENS, TOKENS_CSS.replace("CAPTION_FONT", caption_family()))
    (root / C.FONTS).mkdir(parents=True)
    write(root / C.OVERRIDES, OVERRIDES_TOML)
    write(root / C.VOICE_MD, VOICE_MD)
    write(root / C.MANIFEST, "# manifest.toml (self-test fixture): one [[file]] per source file\n")
    write(root / C.RAW / "README.md", "# raw\n")
    write(root / C.CREDITS_LOG, CREDITS_MD)
    for d in (C.VO_GENERATED, C.AB_GENERATED, C.AB_RENDERS, C.PROD_RENDERS, C.PUB_RENDERS):
        write(root / d / "README.md", "# generated output\n")
    for rel, rules in R.IGNORE_RULES.items():
        write(root / rel, "# fixture\n" + "\n".join(rules) + "\n")
    for name in ("CONTEXT.md", "CLAUDE.md"):
        write(root / "brand/src/exports/large" / name, "# pair\n")
    piece = root / C.PIECES / "001-fixture"
    write(piece / "script.md", SCRIPT_MD)
    write(piece / "brief.md", BRIEF_MD)
    write(piece / "transcript.md", TRANSCRIPT_MD)
    write(root / C.AUDIOBOOK / "002-fixture-book.md", CHAPTER_REG)
    write(root / C.AUDIOBOOK / "008-fixture-voice-format.md", CHAPTER_REG_NO_FORMAT)
    write(root / C.AUDIOBOOK / "008-fixture-voice-format.ch00.md", CREDITS_CH00_MD)
    write(root / "manuscript/src/01-the-ford/01-the-ford.md", CHAPTER_MD)
    settings = {"permissions": {"allow": list(R.SETTINGS_ALLOW), "ask": list(R.SETTINGS_ASK[:-1]),
                                "deny": ["AskUserQuestion"]}}
    write(root / C.SETTINGS, json.dumps(settings, indent=2))


def test_common(verdict, cli) -> None:
    ok = all(abs(C.parse_tc(C.fmt_tc(t)) - t) < 5e-4 for t in (0, 1.25, 59.999, 3725.5))
    verdict("timecodes round trip through HH:MM:SS.mmm", ok and C.fmt_tc(3725.5) == "01:02:05.500")
    try:
        C.parse_tc("00:61:00.000")
        verdict("a bad timecode is refused", False, "no error")
    except C.Fatal:
        verdict("a bad timecode is refused", True)
    data, applied, problems = C.load_presets(quiet=True)
    keys = C.deliverable_keys(data)
    missing = [k for k in keys if not (C.preset(k, data).get("checked") and C.preset(k, data).get("source"))]
    verdict("every deliverable table keeps checked and source", keys and not missing, missing)
    house = data.get("house", {})
    verdict("[house] holds the social loudness decision (DESIGN D24)",
            house.get("social_loudness_lufs") == -14.0 and house.get("social_true_peak_db") == -1.0
            and house.get("source") == "DESIGN.md D24", house)
    verdict("loudness targets: social, podcast, acx",
            C.loudness_target("social", data) == (-14.0, -1.0) and C.loudness_target("podcast", data) == (-16.0, -1.0)
            and C.loudness_target("acx", data) == (-20.0, -3.5))
    verdict("a brand override is applied, a platform-wide one too",
            C.preset("tiktok.video", data)["max_seconds"] == 1 and data["platform"]["instagram"]["hashtags_max"] == 4,
            applied)
    verdict("an override of the wrong type is reported and ignored",
            any("youtube.long.max_seconds" in p for p in problems)
            and C.preset("youtube.long", data)["max_seconds"] == 43200, problems)
    code, out = cli("presets", "tiktok.video")
    verdict("presets prints the table with its override marked", code == 0 and "brand override" in out, out)
    code, out = cli("presets", "--stale-after", "183", "--today", "03/10/2026")
    verdict("presets --stale-after passes on the checked date", code == 0, out)
    code, out = cli("presets", "--stale-after", "183", "--today", "03/10/2027")
    verdict("presets --stale-after finds every table stale a year on", code == 1 and "STALE" in out, out[-400:])
    code, out = cli("presets", "nosuch.key.at.all")
    verdict("an unknown preset key is exit 2", code == 2, out)
    loop, gif = C.preset("website.hero_loop", data), C.preset("newsletter.preview_gif", data)
    verdict("the own channels' tables: a silent loop (audio_tracks = 0) and a GIF (formats = [\"gif\"]) take no "
            "caption_formats; the feed audio is untagged MP3 at the podcast target",
            C.silent(loop) and "caption_formats" not in loop and C.is_gif(gif) and "caption_formats" not in gif
            and not C.silent(C.preset("website.video", data)) and C.target_for(C.preset("podcast.feed_audio", data))
            == "podcast" and C.preset("podcast.feed_audio", data).get("id3_version") == 3
            and C.preset("podcast.episode_art", data).get("alpha") is False
            and C.target_for(C.preset("website.video", data)) == "social", (loop, gif))
    code, out = cli("presets", "website.hero_loop")
    verdict("presets prints website.hero_loop with audio_tracks a house choice",
            code == 0 and "audio_tracks = 0" in out and "chosen: a house choice" in out, out)
    code, out = cli("tokens")
    verdict("tokens: every required token present and parseable", code == 0, out)
    good = C.read_text(C.path(C.TOKENS))
    write(C.path(C.TOKENS), good.replace("--caption-size: 4.5vh;", "--caption-size: 40px;")
          .replace("--radius: 6px;", ""))
    code, out = cli("tokens")
    verdict("tokens: a missing token and a caption size not in vh fail",
            code == 1 and "--radius is missing" in out and "--caption-size" in out, out)
    write(C.path(C.TOKENS), good)


FAKE_UV = '''#!PYTHON
"""A fake uv for media.py --self-test: answers --version, 'python find' and 'run', logging each."""
import json, os, sys, time
args = sys.argv[1:]


def note(**fields):
    with open(os.environ["FAKE_UV_LOG"], "a", encoding="utf-8") as fh:
        fh.write(json.dumps(fields) + "\\n")


if args[:1] == ["--version"]:
    print("uv 0.0.0 (self-test fixture)")
elif args[:2] == ["python", "find"]:
    note(find=args[2:], downloads=os.environ.get("UV_PYTHON_DOWNLOADS", ""),
         offline=os.environ.get("UV_OFFLINE", ""))
    request = [a for a in args[2:] if not a.startswith("-")]
    found = request[0] if request and os.path.isabs(request[0]) else \\
        os.environ.get("FAKE_UV_SYSTEM" if "--system" in args else "FAKE_UV_PLAIN", "")
    if not found:
        sys.exit("error: no interpreter found")
    print(found)
elif args[:1] == ["run"]:
    start = time.time()
    time.sleep(float(os.environ.get("FAKE_UV_SLEEP") or 0))
    if "-o" in args:
        with open(args[args.index("-o") + 1], "wb") as fh:
            fh.write(b"fixture png")
    note(run=args[1:], start=start, end=time.time())
    sys.exit(int(os.environ.get("FAKE_UV_EXIT") or 0))
else:
    sys.exit(2)
'''
UV_SCRIPT = '# /// script\n# requires-python = ">=3.11,<3.99"\n# dependencies = []\n# ///\nprint("fixture")\n'


def fake_python(p: Path, version: list, base: str, venv: bool) -> Path:
    """An interpreter that answers check --setup's -c probe with a fixed version and base."""
    answer = json.dumps({"version": version, "base": base, "venv": venv})
    write(p, f"#!/bin/sh\necho '{answer}'\n").chmod(0o755)
    return p


def test_uv(verdict, skip, cli, root: Path) -> None:
    """D20's uv helper, card renders in the piece's cards/ folder (D47, D64) and check --setup's
    interpreter row (D49), all against a fake uv on PATH: no environment is built, nothing fetched."""
    import threading
    import time
    renders = C.path(C.PROD_RENDERS)
    verdict("an output's piece folder is keyed on the leading piece key, a name with none stays at the top, "
            "and timing/ and scenes/ are tracked folders of production/src/ (D64)",
            C.piece_folder(C.PROD_RENDERS, "003-why-the-ferry-runs-late--c01.youtube-short.mp4")
            == renders / "003-why-the-ferry-runs-late"
            and C.piece_folder(C.PUB_RENDERS, "003-a.chapters.json", "x") == C.path(C.PUB_RENDERS) / "003-a" / "x"
            and C.piece_folder(renders, "talk-cam-a.wav", "cards") == renders
            and C.piece_key("talk-cam-a.wav") is None and C.piece_of("talk-cam-a.wav") == "talk-cam-a"
            and V.card_name(Path("title.html"), 640, 360, True) == renders / "title.640x360.transparent.png"
            and (C.TIMING, C.SCENES) == ("production/src/timing", "production/src/scenes"))
    if os.name != "posix":
        skip("the uv helper, card renders and the setup row with a fake uv", "the fake uv is a POSIX script")
        return
    work = Path(str(root) + "-uv")
    log = work / "uv.log"
    write(work / "bin" / "uv", FAKE_UV.replace("PYTHON", sys.executable, 1)).chmod(0o755)
    venv = work / "venv"
    env = {"PATH": f"{work / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}", "FAKE_UV_LOG": str(log),
           "FAKE_UV_SYSTEM": "/fixture/system/python3", "FAKE_UV_PLAIN": str(venv / "bin" / "python3"),
           "VIRTUAL_ENV": str(venv), "HOME": str(work / "home")}
    plain = ["UV_PYTHON", "FAKE_UV_SLEEP", "FAKE_UV_EXIT"]

    def calls(kind):
        lines = log.read_text(encoding="utf-8").splitlines() if log.is_file() else []
        return [c for c in (json.loads(x) for x in lines) if kind in c]

    def uv_run(script, timeout=60, **values):
        log.unlink(missing_ok=True)
        with held_env(drop=plain, **dict(env, **values)), contextlib.redirect_stderr(io.StringIO()) as said:
            try:
                return C.uv_script(script, ["--self-test"], timeout=timeout), said.getvalue()
            except C.Fatal as err:
                return err, said.getvalue()

    saved_locks, C.UV_LOCKS = C.UV_LOCKS, work / "locks"
    try:
        script = write(work / "fixture-script.py", UV_SCRIPT)
        proc, _ = uv_run(script)
        run, finds = calls("run"), calls("find")
        verdict("a uv script runs under the interpreter 'uv python find --system' gives for its requires-python, "
                "never the active virtual environment's, and the lookup fetches nothing (D20)",
                getattr(proc, "returncode", None) == 0 and [f["find"] for f in finds] == [["--system", ">=3.11,<3.99"]]
                and all(f["downloads"] == "never" and f["offline"] == "1" for f in finds) and len(run) == 1
                and run[0]["run"] == ["--quiet", "--python", "/fixture/system/python3", str(script.resolve()),
                                      "--self-test"], log.read_text(encoding="utf-8") if log.is_file() else proc)
        proc, _ = uv_run(script, UV_PYTHON="/fixture/named/python3")
        run = calls("run")
        verdict("UV_PYTHON, where it is set, is the interpreter, and nothing is looked up (D20)",
                getattr(proc, "returncode", None) == 0 and not calls("find") and len(run) == 1
                and run[0]["run"][:3] == ["--quiet", "--python", "/fixture/named/python3"], run or proc)
        err, _ = uv_run(script, FAKE_UV_SYSTEM="")
        verdict("no Python outside a virtual environment in the script's range is exit 2, naming the fix",
                isinstance(err, C.Fatal) and ">=3.11,<3.99" in str(err) and "UV_PYTHON" in str(err)
                and not calls("run"), err)
        began = time.monotonic()
        err, _ = uv_run(script, timeout=1, FAKE_UV_SLEEP="6")
        verdict("a uv script that outlives its timeout is stopped, with every process it started (exit 2)",
                isinstance(err, C.Fatal) and "did not finish within 1 s" in str(err)
                and time.monotonic() - began < 5 and not calls("run"), err)

        first = write(work / "fixture-first-run.py", UV_SCRIPT)
        log.unlink(missing_ok=True)

        def together(n=2):
            done = []
            threads = [threading.Thread(target=lambda: done.append(C.uv_script(first, [], timeout=60)))
                       for _ in range(n)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            return done

        def apart(a, b):
            return a["start"] >= b["end"] - 0.05 or b["start"] >= a["end"] - 0.05
        with held_env(drop=plain, **dict(env, FAKE_UV_SLEEP="0.8")), \
                contextlib.redirect_stderr(io.StringIO()) as said:
            done = together()
            spans = calls("run")
            later = together()
            spans_later = calls("run")[2:]
        verdict("two first runs of one script never overlap: the second waits while the first builds its "
                "environment (D20's first-run lock)",
                [p.returncode for p in done] == [0, 0] and len(spans) == 2 and apart(*spans)
                and "waiting for another run of fixture-first-run.py" in said.getvalue(), (spans, said.getvalue()))
        verdict("later runs also hold the lock, so a deleted environment is rebuilt without racing",
                [p.returncode for p in later] == [0, 0] and len(spans_later) == 2 and apart(*spans_later),
                spans_later)
        verdict("the per-script lock sits at user scope, never in the project",
                any(C.UV_LOCKS.glob("fixture-first-run-*.lock"))
                and not any(root.rglob("*.lock")) and not any(root.rglob("*.built")), sorted(C.UV_LOCKS.iterdir()))
        failing = write(work / "fixture-failing.py", UV_SCRIPT)
        proc, _ = uv_run(failing, FAKE_UV_EXIT="1")
        verdict("a run that fails records no environment, so the next first run still takes the lock",
                getattr(proc, "returncode", None) == 1 and not any(C.UV_LOCKS.glob("fixture-failing-*.built")), proc)
        C.UV_LOCKS = write(work / "not-a-folder", "a file, where the lock folder would go\n") / "locks"
        proc, said = uv_run(write(work / "fixture-unlocked.py", UV_SCRIPT))
        verdict("where the lock directory cannot be written, exit 2 without starting uv",
                isinstance(proc, C.Fatal) and "cannot take its first-run lock" in str(proc)
                and not calls("run"), proc)
        C.UV_LOCKS = work / "locks"

        html = write(C.path(C.CARDS) / "019-cards.title.html", "<!doctype html><html lang=\"en-GB\"></html>\n")
        cards = renders / "019-cards" / "cards"
        log.unlink(missing_ok=True)
        with held_env(drop=plain, **env), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            clip = V.card_png(html, 640, 360, transparent=False)
            over = V.card_png(html, 640, 360, transparent=True)
        run = [c["run"] for c in calls("run")]
        verdict("a card renders into its piece's cards/ folder, an overlay's named .transparent, so the clip's and "
                "the overlay's at one size are both kept (D47, D64); card.py starts with D20's interpreter",
                clip == cards / "019-cards.title.640x360.png" and over == cards / "019-cards.title.640x360.transparent.png"
                and clip.is_file() and over.is_file() and len(run) == 2
                and run[0][:4] == ["--quiet", "--python", "/fixture/system/python3", str((C.TOOLKIT / "card.py").resolve())]
                and "--transparent" not in run[0] and run[1][-1] == "--transparent", run)
        now = time.time()
        for p, age in ((C.path(C.TOKENS), 300), (clip, 200), (html, 100), (over, 0)):
            os.utime(p, (now - age, now - age))
        log.unlink(missing_ok=True)
        with held_env(drop=plain, **env), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            V.card_png(html, 640, 360, transparent=False)
            V.card_png(html, 640, 360, transparent=True)
        run = [c["run"] for c in calls("run")]
        verdict("each variant is judged fresh on its own: a clip render older than its HTML is made again, a "
                "newer overlay render is kept", len(run) == 1 and "--transparent" not in run[0], run)

        base_py = fake_python(work / "base" / "python3", [3, 12, 3], "", False)
        own_py = fake_python(work / "base" / "python3.14", [3, 14, 8], "", False)
        fake_python(venv / "bin" / "python3", [3, 14, 8], str(base_py), True)
        log.unlink(missing_ok=True)
        with held_env(drop=plain, **dict(env, FAKE_UV_SYSTEM=str(base_py))):
            rows = R.uv_interpreter_rows(root)
            finds = calls("find")
            code, out = cli("check", "--setup")
        verdict("check --setup fails a plain 'uv run' that would take a virtual environment's Python on another "
                "Python's base, naming UV_PYTHON and the interpreter media.py takes (D49)",
                rows and rows[0][0] is False and "Python 3.14.8 whose base" in rows[0][1] and "Python 3.12.3" in rows[0][1]
                and "UV_PYTHON" in rows[0][2] and str(base_py) in rows[0][2]
                and code == 1 and "FAIL  uv's interpreter for " in out and "fix: set UV_PYTHON at user scope" in out,
                (rows, out))
        verdict("the interpreter row asks only 'uv python find', with downloads and the network off, and builds "
                "no environment", finds and all(f["downloads"] == "never" and f["offline"] == "1" for f in finds)
                and not calls("run"), log.read_text(encoding="utf-8") if log.is_file() else "")
        with held_env(drop=plain, **dict(env, UV_PYTHON=str(base_py))):
            named = R.uv_interpreter_rows(root)
        fake_python(venv / "bin" / "python3", [3, 14, 8], str(own_py), True)
        with held_env(drop=plain, **dict(env, FAKE_UV_SYSTEM=str(base_py))):
            own = R.uv_interpreter_rows(root)
        verdict("check --setup passes UV_PYTHON naming an interpreter outside a virtual environment, and a virtual "
                "environment on a base of its own version",
                named and named[0][0] is True and "UV_PYTHON names" in named[0][1]
                and own and own[0][0] is True and "same version" in own[0][1], (named, own))
    finally:
        C.UV_LOCKS = saved_locks


def test_piece_defaults(verdict) -> None:
    """Where the commands' default outputs land (DESIGN D64, Section 6.16), worked out without a
    render: the piece's own folder inside the right renders/ folder, keyed on the leading piece key
    of the output's name, and the folder's top for a name with none. The commands themselves are
    proved writing there in the ffmpeg groups (cut, encode, frame, still-video, assemble, image,
    the GIF, captions, the feed)."""
    import card as CARD
    prod, pub = C.path(C.PROD_RENDERS), C.path(C.PUB_RENDERS)
    piece = "003-why-the-ferry-runs-late"
    card = C.path(C.CARDS) / f"{piece}.title.html"
    thumb = C.path("publishing/src/thumbnails") / f"{piece}--c02.html"
    proof = C.path("brand/src/design-system/previews") / "thumbnail.html"
    verdict("card.py render's default: a card in its piece's cards/ folder, named as assemble names it, an "
            "overlay's .transparent; a thumbnail in its piece's folder of publishing/src/renders/; a layout whose "
            "name has no piece key at that folder's top (D47, D64)",
            CARD.default_png(card, "640x360") == V.card_name(card, 640, 360, False)
            == prod / piece / "cards" / f"{piece}.title.640x360.png"
            and CARD.default_png(card, "640x360", True) == V.card_name(card, 640, 360, True)
            and CARD.default_png(thumb, "youtube-short") == pub / piece / f"{piece}--c02.youtube-short.png"
            and CARD.default_png(proof, "youtube-thumbnail") == pub / "thumbnail.youtube-thumbnail.png",
            [CARD.default_png(card, "640x360"), CARD.default_png(thumb, "youtube-short"),
             CARD.default_png(proof, "youtube-thumbnail")])
    got = [V.deliverable_path(Path(f"{piece}.master.mp4"), "youtube.short", "c01", True, ".mp4"),
           V.deliverable_path(Path("talk-cam-a.mp4"), "youtube.short", None, False, ".mp4"),
           K.default_srt(f"{piece}.youtube-long.en-GB.srt"), K.default_srt("talk-cam-a.youtube-long.en-GB.srt"),
           F.render_path(f"{piece}.podcast-feed-audio.mp3"), F.render_path("fixture-show.podcast-cover.jpg")]
    verdict("a deliverable, timed captions and a feed episode's render default to the piece's folder of "
            "publishing/src/renders/, and a name with no piece key to its top (D64)",
            got == [pub / piece / f"{piece}--c01.youtube-short.burned.mp4", pub / "talk-cam-a.youtube-short.mp4",
                    pub / piece / f"{piece}.youtube-long.en-GB.srt", pub / "talk-cam-a.youtube-long.en-GB.srt",
                    pub / piece / f"{piece}.podcast-feed-audio.mp3", pub / "fixture-show.podcast-cover.jpg"], got)


def test_scene_model(verdict) -> None:
    import scene as worker
    import media_scene as S
    saved = C.ROOT
    with tempfile.TemporaryDirectory(prefix='media-scene-model-') as tmp:
        root = Path(tmp) / 'project'; root.mkdir(); C.ROOT = root
        try:
            worker.write_fixture(root)
            data = root / 'toolkit/data'; data.mkdir(parents=True)
            shutil.copyfile(C.TOOLKIT / 'data/platforms.toml', data / 'platforms.toml')
            scene = worker.load_scene('922-scene-fixture')
            page, elements = scene.write_page(160, 90)
            original = page.read_bytes(); page.write_text('stale author edit')
            scene.write_page(160, 90)
            verdict('a scene run writes the local page afresh from the tracked Python', page.read_bytes() == original)
            verdict('scene clocks resolve beat, line, board and original word boundaries',
                    [scene.frame(ref) for ref in ('beat:2','line:2.1','board:b02','word:1','word:1:end')]
                    == [30,30,30,30,45])
            def character(n): return next(row for row in scene.state(n,elements,page) if row['name']=='character')
            verdict('movement is stepped on whole pixels with a walk cycle before arrival',
                    [character(n)['pose'] for n in range(6)] == ['walk1'] * 3 + ['walk2'] * 3
                    and character(2)['x'] != character(5)['x']
                    and all(float(character(n)['x']).is_integer() for n in range(30)))
            elements[1].hold = 3
            verdict('a stepped position holds for the author-set number of frames',
                    character(0)['x'] == character(2)['x'] and character(3)['x'] != character(2)['x'])
            elements[1].hold = 1
            verdict('an anchor arrival changes pose, facing and the target highlight together',
                    character(30)['pose']=='point' and character(30)['facing']=='left'
                    and next(row for row in scene.state(30,elements,page) if row['name']=='label')['style']
                    == {'background-color':'var(--color-surface)'})
            verdict('one aspect is laid out independently of another, without crop or pad',
                    scene.elements(90,160)[0].width==80 and scene.elements(160,90)[0].width==150)
            brief=root/C.PIECES/scene.piece/'brief.md'
            brief.write_text('---\ndeliverables:\n  - youtube.long\n---\n')
            plan=root/'publishing/src/cut-downs'/(scene.piece+'.md');plan.parent.mkdir(parents=True)
            plan.write_text('| Cut | Deliverables | Lines |\n| c01 | tiktok.video | 1.1 |\n')
            verdict('safe margins gather both the brief and cut plan deliverable columns',
                    {table['key'] for table in scene.deliverables()} == {'youtube.long','tiktok.video'})

            sprite=S.Sprite(css_frames=elements[1].sprite.css_frames,scale=2,breathe_hold=15,blink_every=15)
            idle=S.Element('idle',kind='sprite',x=10,y=10,width=24,height=32,sprite=sprite)
            a=scene.state(0,[idle],page)[0]; b=scene.state(15,[idle],page)[0]; c=scene.state(4,[idle],page)[0]
            verdict('idle life blinks deterministically and breathes by one scaled sprite pixel',
                    a['blink'] and b['blink'] and not c['blink'] and b['y']-a['y']==2)
            art=root/'brand/src/exports';art.mkdir(parents=True)
            sprite=S.Sprite(folder='brand/src/exports',name='figure',extension='.svg',layered=True,mouth=(2,3),scale=2)
            for stem in ('figure-idle','figure-mouth-a','figure-idle-blink'):
                (art/(stem+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="12" height="16"></svg>')
            idle.sprite=sprite
            state=scene.state(0,[idle],page)[0]
            verdict('layered sprites place a native mouth and optional blink above the pose',
                    len(state['images'])==3 and state['images'][1]['x']==4 and state['images'][1]['y']==6)
            (art/'figure-mouth-a.svg').unlink()
            try: scene.state(0,[idle],page); missing=False
            except C.Fatal as err: missing='figure-mouth-a.svg' in str(err)
            verdict('a missing required sprite frame is a named could-not-run error',missing)
            try:
                scene.state(0,[S.Element('a',keyframes=[S.Keyframe(0,anchor='b')]),
                               S.Element('b',keyframes=[S.Keyframe(0,anchor='a')])],page)
                cycle=False
            except C.Fatal as err: cycle='cyclic' in str(err)
            verdict('cyclic anchor references fail before drawing',cycle)
            try: scene.frame('word:99'); absent=False
            except C.Fatal as err: absent='accepted time' in str(err)
            verdict('an absent timing anchor names the commands that repair it',absent)
        finally: C.ROOT = saved


def test_scene_timing(verdict) -> None:
    import media_scene as S
    mouth = S.MouthTimeline([{'start': 0, 'end': 0.03, 'value': 'A'},
                             {'start': 0.03, 'end': 0.08, 'value': 'B'},
                             {'start': 0.10, 'end': 0.11, 'value': 'C'}])
    verdict('mouth shapes sample frame middles, with rest in gaps and after speech',
            [mouth.shape(n) for n in range(5)] == ['A', 'B', 'X', 'X', 'X'])
    verdict('mouth sampling subtracts the edit voice offset',
            mouth.shape(0, 30, 1) == 'X' and mouth.shape(30, 30, 1) == 'A')
    edge = S.MouthTimeline([{'start': 0.05, 'end': 0.15, 'value': 'H'},
                            {'start': 0.15, 'end': 0.25, 'value': 'G'}])
    verdict('mouth intervals include starts, exclude ends and never borrow a later cue',
            [edge.shape(n, 10) for n in range(3)] == ['H', 'G', 'X'])
    bad = ([{'start': 0, 'end': 0.1, 'value': 'Z'}],
           [{'start': float('nan'), 'end': 0.1, 'value': 'X'}],
           [{'start': 0, 'end': 0.1, 'value': 'A'}, {'start': 0.05, 'end': 0.2, 'value': 'B'}])
    rejected = 0
    for cues in bad:
        try: S.MouthTimeline(cues)
        except C.Fatal: rejected += 1
    verdict('invalid, non-finite and overlapping mouth cues cannot produce frame state', rejected == len(bad))
    tables = [{'width': 1080, 'height': 1920, 'safe_zone': {'top': 288, 'right': 192}},
              {'width': 540, 'height': 960, 'safe_zone': {'bottom': 200, 'left': 30}},
              {'width': 1920, 'height': 1080, 'safe_zone': {'top': 900}}, {'kind': 'audio'}]
    verdict('scene safe zones combine the largest edge of each same-aspect deliverable',
            S.safe_zone(540, 960, tables) == {'top': 144, 'bottom': 200, 'left': 30, 'right': 96})
    verdict('scene frame variables use whole pixels at the requested native size',
            S.frame_vars(540, 960, tables)['--safe-right'] == '96px'
            and S.frame_vars(540, 960, tables)['--frame-width'] == '540px')
    verdict('typed text holds for author-selected whole frames and stops at its full length',
            [S.typed_text('abc', n, 2, 2) for n in range(9)]
            == ['', '', 'a', 'a', 'ab', 'ab', 'abc', 'abc', 'abc'])
    verdict('scene tokens are the brand properties, read by the shared token parser',
            S.brand_tokens() == C.read_tokens() and '--color-bg' in S.brand_tokens())


def test_shared_mix(verdict) -> None:
    import array
    import wave
    saved_root = C.ROOT
    try:
        with tempfile.TemporaryDirectory(prefix='media-shared-mix-') as folder:
            root = Path(folder)
            C.ROOT = root
            write_fixture(root)
            piece = '920-mix-fixture'
            gen = root / C.VO_GENERATED / piece / 'takes'
            gen.mkdir(parents=True)
            src = gen / 'voice.wav'
            C.ffmpeg(['-y', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=8000:duration=0.3',
                      '-ac', '1', '-c:a', 'pcm_s16le', src])
            write(root / C.VOICEOVER / (piece + '.toml'),
                  '[voiceover]\npiece="' + piece + '"\noutput_format="pcm_8000"\n[[segment]]\n'
                  'id="s01"\nfile="generated/' + piece + '/takes/voice.wav"\ntext="A ferry."\n'
                  'status="approved"\npause_after=0.1\n')
            assert A.cmd_voice_join(argparse.Namespace(piece=piece, o=None)) == 0
            asset = root / C.ASSETS / 'bed.wav'
            asset.parent.mkdir(parents=True, exist_ok=True)
            C.ffmpeg(['-y', '-f', 'lavfi', '-i', 'sine=frequency=660:sample_rate=48000:duration=1',
                      '-ac', '2', '-c:a', 'pcm_s16le', asset])
            rows = [dict(source='vo:' + piece, at=0.1, role='voice', gain_db=-3, fade_in=.03, fade_out=.02),
                    dict(source=C.ASSETS + '/bed.wav', at=0, role='music', duck=True, gain_db=-15,
                         fade_in=.05, fade_out=.1, **{'in': .1, 'out': .9}),
                    dict(source=C.ASSETS + '/bed.wav', at=.4, role='effect', gain_db=-25,
                         **{'in': .05, 'out': .15})]
            results = []
            for joined in (False, True):
                inputs, graph = [], ['anullsrc=r=48000:cl=stereo,atrim=end_sample=48000[base]']
                def add(args):
                    index = len(inputs)
                    inputs.append(args)
                    return index
                label = V.mix_audio(rows, piece, 48000, 48000, add, graph, 'base', joined=joined)
                output = root / ('joined.wav' if joined else 'segments.wav')
                C.ffmpeg(['-y'] + [v for args in inputs for v in args]
                         + ['-filter_complex', ';'.join(graph), '-map', '[' + label + ']',
                            '-c:a', 'pcm_s16le', output])
                with wave.open(str(output)) as audio:
                    assert audio.getnframes() == 48000 and audio.getnchannels() == 2
                    results.append(array.array('h', audio.readframes(audio.getnframes())))
            difference = max(abs(a - b) for a, b in zip(*results))
            verdict('both master routes share offsets ranges fades gain and ducking with sample-exact sound',
                    difference <= 2, f'maximum PCM difference: {difference}')
            A.joined_voice(piece).unlink()
            try:
                V.mix_audio(rows, piece, 48000, 48000, lambda args: 0, [], 'base', joined=True)
                refused = False
            except C.Fatal as err:
                refused = 'voice join' in str(err)
            verdict('a scene needs the accepted voice join and never silently rebuilds it from takes', refused)
    finally:
        C.ROOT = saved_root


def test_render_helpers(verdict, root: Path) -> None:
    from unittest.mock import patch
    import time
    with held_env(drop=('MEDIA_MEMORY_MAX', '_MEDIA_MEMORY_CAPPED', '_MEDIA_MEMORY_RECEIPT')):
        code = C.memory_scope(None, ['unused'])
        verdict('no memory setting stays here and announces an uncapped render', code is None)
        with patch.object(C.shutil, 'which', return_value=None):
            with held_env(MEDIA_MEMORY_MAX='512M'):
                code = C.memory_scope(None, ['unused'])
            verdict('a requested cap without systemd remains explicitly uncapped', code is None)
        calls = []
        command = [sys.executable, 'a path with spaces.py', 'assemble', "an author's edit.toml"]
        child_code = 0
        start = True
        def scope(argv, **kwargs):
            if '--property=Version' in argv:
                return subprocess.CompletedProcess(argv, 0)
            calls.append((argv, kwargs))
            if start:
                with held_env(**kwargs['env']):
                    C.memory_scope(kwargs['env']['_MEDIA_MEMORY_CAPPED'], command)
            return subprocess.CompletedProcess(argv, child_code)
        with patch.object(C.shutil, 'which', side_effect=lambda name: '/bin/' + name), \
                patch.object(C.subprocess, 'run', scope), held_env(MEDIA_MEMORY_MAX='256M'):
            for child_code in (0, 1):
                code = C.memory_scope('512M', command)
                verdict(f'memory scope forwards render exit {child_code} without recursive scopes',
                        code == child_code and len(calls) == child_code + 1)
            argv, kw = calls[0]
            verdict('explicit memory cap overrides user setting, disables swap and keeps argument boundaries',
                    'MemoryMax=512M' in argv and 'MemorySwapMax=0' in argv and argv[-len(command):] == command
                    and kw['env']['_MEDIA_MEMORY_CAPPED'] == '512M')
            for child_code, start in ((137, True), (1, False)):
                try:
                    C.memory_scope('512M', command)
                    refused = False
                except C.Fatal as err:
                    refused = '512M' in str(err)
                verdict('memory scope reports a killed render or failed scope setup as exit two: '
                        + str(child_code) + '/' + str(start), refused)
    with patch.object(R.shutil, 'which', return_value=None):
        rows, findings = R.setup_report(root)
    verdict('absent systemd-run is an optional setup note for memory caps, never a requirement',
            any('systemd-run' in row and row.startswith('--') for row in rows)
            and not any('systemd-run' in finding for finding in findings))
    output = root / 'streamed-bytes.bin'
    # Fill stderr before consuming stdin: a PIPE not drained would deadlock before it reads.
    receiver = ('import sys,pathlib; sys.stderr.write("x" * 262144); sys.stderr.flush(); '
                'pathlib.Path(sys.argv[1]).write_bytes(sys.stdin.buffer.read())')
    chunks = [b'first' * 65536, b'last' * 65536]
    code = C.stream_run([sys.executable, '-c', receiver, output], iter(chunks), what='frame fixture')
    verdict('streaming drains large diagnostics without deadlock and preserves every binary chunk',
            code == 0 and output.read_bytes() == b''.join(chunks))
    try:
        C.stream_run([sys.executable, '-c', 'import sys; sys.stderr.write("encoder refused input"); sys.exit(7)'],
                     iter(chunks), what='frame fixture')
        refused = False
    except C.Fatal as err:
        refused = 'encoder refused input' in str(err) and 'exit 7' in str(err)
    verdict('streaming reports a broken encoder pipe with the actual diagnostic', refused)
    pidfile = root / 'stream-child.pid'
    processes = []
    original = C.subprocess.Popen
    def launched(*args, **kwargs):
        child = original(*args, **kwargs)
        processes.append(child)
        return child
    def broken_producer():
        yield b'frame' * 65536
        until = time.monotonic() + 5
        while not pidfile.is_file() and time.monotonic() < until:
            time.sleep(0.01)
        raise C.Fatal('the scene frame failed')
    receiver = ('import sys,pathlib,subprocess,time; sys.stdin.buffer.read(327680); '
                'child=subprocess.Popen([sys.executable,"-c","import time; time.sleep(30)"]); '
                'pathlib.Path(sys.argv[1]).write_text(str(child.pid)); time.sleep(30)')
    with patch.object(C.subprocess, 'Popen', launched):
        try:
            C.stream_run([sys.executable, '-c', receiver, pidfile], broken_producer(), what='frame fixture')
            refused = False
        except C.Fatal as err:
            refused = str(err) == 'the scene frame failed'
    stopped = bool(processes) and all(child.poll() is not None for child in processes)
    if os.name == 'posix' and pidfile.is_file():
        pid = int(pidfile.read_text())
        status = Path('/proc') / str(pid) / 'stat'
        if sys.platform.startswith('linux'):
            until = time.monotonic() + 2
            while status.is_file() and status.read_text().split()[2] != 'Z' and time.monotonic() < until:
                time.sleep(0.01)
            stopped = stopped and (not status.is_file() or status.read_text().split()[2] == 'Z')
        else:
            try:
                os.kill(pid, 0)
                stopped = False
            except ProcessLookupError:
                pass
    verdict('a failed frame producer stops the encoder and its child processes', refused and stopped)


def test_storyboards(verdict, root: Path) -> None:
    script = root / 'board-script.md'
    write(script, '## 1. Opening (target 00:10)\nVO: {quiet} A ferry crosses.\n'
          'TEXT: Not spoken.\nVO: Home again.\n')
    parsed = K.read_script(script)
    for count, dash in ((8, '-'), (9, '–')):
        headings = ['#','Beat','Time','Picture','Spoken','On screen','Sound','Vertical framing']
        cells = ['B01','1',f'00:00{dash}00:10','A ferry \\| its wake',f'1.1{dash}1.2','A ferry','—','native']
        if count == 9:
            headings.append('Timing notes'); cells.append('Hold the last frame.')
        board = root / f'boards-{count}.md'
        text = ('# Storyboard\n\n| ' + ' | '.join(headings) + ' |\n| '
                + ' | '.join(['---'] * count) + ' |\n| ' + ' | '.join(cells) + ' |\n')
        write(board, text)
        header, rows = K.read_storyboard(board)
        chosen = K.select_lines(parsed, rows[0].cells[4])
        verdict(f'boards: {count} cells, {dash} ranges, escaped picture pipe and spoken-only line references',
                len(header) == 9 and len(rows) == 1 and rows[0].id == 'B01' and rows[0].beat == 1
                and rows[0].cells[3] == 'A ferry | its wake'
                and rows[0].cells[8] == ('—' if count == 8 else 'Hold the last frame.')
                and [line.text for line in chosen] == ['A ferry crosses.', 'Home again.']
                and board.read_text() == text)
    rows = [{'word': word} for word in ('A','ferry','crosses.','Home','again.')]
    indices, findings = K.match_script_words(parsed, rows)
    verdict('word-to-line matching ignores punctuation and keeps actual word indices',
            indices == {'1.1': [0,1,2], '1.2': [3,4]} and not findings)
    indices, findings = K.match_script_words(parsed, rows[:2] + rows[3:])
    verdict('a missing script word is reported and later lines retain their real word indices',
            indices['1.2'] == [2,3] and any('1.1' in finding and 'crosses' in finding for finding in findings))
    write(script, '## 1. Opening\nVO: Ferry boat.\nVO: Ferry boat.\nVO: A half-hearted answer.\n')
    repeated = K.read_script(script)
    indices, findings = K.match_script_words(repeated, [{'word': word} for word in
                                                      ('FERRY','boat.','Ferry','boat.','A','half-hearted','answer.')])
    verdict('repeated words keep line order and hyphen parts share the original aligned word index',
            indices == {'1.1': [0,1], '1.2': [2,3], '1.3': [4,5,6]} and not findings)
    original = board.read_text()
    for label, changed in (
            ('duplicate IDs', original + original.splitlines()[-1] + '\n'),
            ('ragged cells', original.replace(' | native |', ' | native | extra |')),
            ('missing header', '# Not a storyboard\n'),
            ('invalid ID', original.replace('B01', 'B00'))):
        board.write_text(changed)
        try:
            K.read_storyboard(board)
            rejected = False
        except C.Fatal:
            rejected = True
        verdict('boards refuse ' + label + ' without rewriting the source', rejected
                and board.read_text() == changed)


def test_cues(verdict, cli, root: Path, have_git: bool) -> None:
    from unittest.mock import patch
    saved_root = C.ROOT
    with tempfile.TemporaryDirectory(prefix='media-cues-') as folder:
        root = Path(folder)
        C.ROOT = root
        try:
            piece = '919-cue-fixture'
            script = write(root / C.PIECES / piece / 'script.md',
                           '## 1. Opening (target 00:02)\nVO: {quiet} A ferry {emphatic} crosses.\n'
                           'SFX: tick\n\n## 2. Home (target 00:02)\nVO: {laughing} Home again.\n'
                           'MUSIC: playful instrumental\n')
            board = root / C.PIECES / piece / 'storyboard.md'
            rows = [dict(word=w, start=a, end=b, score=0.9, segment=s) for w,a,b,s in
                    [('A',0.125,0.375,'s01'),('ferry',0.4,0.8,'s01'),('crosses.',0.85,1.25,'s01'),
                     ('Home',1.6,1.9,'s02'),('again.',1.95,2.4,'s02')]]
            words = write(root / C.TIMING / f'{piece}.words.json', json.dumps(rows))
            edit = write(root / C.EDITS / f'{piece}.toml', '[edit]\npiece = "919-cue-fixture"\n'
                         '[[audio]]\nsource = "vo:919-cue-fixture"\nat = 0.5\nrole = "voice"\n'
                         '[[audio]]\nsource = "F0991"\ncue = "e03"\nrole = "effect"\nat = 1.75\n'
                         '[[audio]]\nsource = "F0992"\ncue = "e05"\nrole = "music"\nat = 2.0\n'
                         'in = 0.1\nout = 0.9\ngain_db = -20\nfade_in = 0.1\nfade_out = 0.2\nduck = true\n')
            write(root / C.MANIFEST, '[[file]]\nid = "F0991"\nkind = "audio"\nduration = 0.2\n'
                  'path = "raw/not-present.wav"\n[[file]]\nid = "F0992"\nkind = "music"\nduration = 5.0\n'
                  'path = "raw/not-present-music.wav"\n')
            working = root / C.PROD_RENDERS / piece / 'timing' / f'{piece}.cues.json'
            headings = ['#','Beat','Time','Picture','Spoken','On screen','Sound','Vertical framing']
            for count, dash in ((8,'-'), (9,'–')):
                head = headings + (['Timing notes'] if count == 9 else [])
                cells = [['B01','1','00:00–00:10','A ferry \\| its wake',f'1.1{dash}1.1','Ferry','tick','native'],
                         ['B02','2','00:10–00:20','Home',f'2.1{dash}2.1','Home','music','native']]
                text = '| ' + ' | '.join(head) + ' |\n|' + '|'.join(['---'] * count) + '|\n'
                text += '\n'.join('| ' + ' | '.join(row + (['Hold.'] if count == 9 else [])) + ' |'
                                  for row in cells) + '\n'
                write(board, text)
                with patch.object(C, 'probe', side_effect=AssertionError('cues must not open the footage mirror')):
                    code, output = cli('cues', piece)
                data = json.loads(working.read_text()) if working.is_file() else {}
                verdict(f'cues match {count}-column boards with {dash} ranges and never rewrite the source',
                        code == 0 and board.read_text() == text and len(data.get('boards', [])) == 2, output)
            verdict('cues keep exact JSON times and print enclosing MM:SS with escaped cells',
                    data['boards'][0]['start'] == 0.125 and data['boards'][0]['end'] == 1.25
                    and '00:00–00:02' in output and '00:01–00:03' in output and 'A ferry \\| its wake' in output
                    and 'exact start=0.125 end=1.25' in output, output)
            verdict('cues preserve separate beat, board, line and original word lists',
                    set(data) == {'piece','beats','boards','lines','words','events'}
                    and data['beats'][1]['title'] == 'Home' and data['lines'][1]['word_indices'] == [3,4]
                    and data['words'] == [dict(row,line='1.1' if i < 3 else '2.1') for i,row in enumerate(rows)]
                    and data['boards'][0]['timing_notes'] == 'Hold.')
            events = data['events']
            verdict('cues retain delivery instructions at actual word anchors without inventing sound duration',
                    [e['instruction'] for e in events if e['kind'] == 'delivery'] == ['quiet','emphatic','laughing']
                    and events[0]['anchor']['word'] == 0 and events[1]['anchor']['time'] == 0.85
                    and events[3]['script_line'] == '2.1' and 'end' not in events[3])
            verdict('cues resolve sound and music IDs from tracked audio rows including offset fades and ducking',
                    events[2]['source'] == 'F0991' and events[2]['start'] == 1.25
                    and events[4]['source'] == 'F0992' and events[4]['start'] == 1.5
                    and abs(events[4]['end'] - 2.3) < 0.000001 and events[4]['mix']['gain_db'] == -20
                    and events[4]['mix']['fade_out'] == 0.2 and events[4]['mix']['duck'] is True)
            old = board.read_text()
            board.write_text(old.replace('2.1–2.1', '2.9–2.9'))
            code, output = cli('cues', piece)
            unmatched = json.loads(working.read_text())
            verdict('cues report an unmatched board with null times and exit one', code == 1
                    and unmatched['boards'][1]['start'] is None and 'B02' in output, output)
            board.write_text(old)
            held = edit.read_text()
            for label, changed in [('missing',held.replace('cue = "e05"','cue = "e99"')),
                                   ('duplicate',held + '\n[[audio]]\nsource="F0992"\ncue="e05"\nrole="music"\n')]:
                edit.write_text(changed)
                code, output = cli('cues', piece)
                incomplete = json.loads(working.read_text())
                verdict(f'cues report {label} audio links rather than guessing a music placement',
                        code == 1 and incomplete['events'][4]['start'] is None and 'e05' in output, output)
            edit.write_text(held)
            invalid = [dict(row) for row in rows]; invalid[1]['start'] = None
            words.write_text(json.dumps(invalid))
            code, output = cli('cues', piece)
            verdict('cues report untimed words and leave their board times null', code == 1
                    and json.loads(working.read_text())['boards'][0]['end'] is None, output)
            before = working.read_bytes()
            invalid[1]['start'] = float('nan'); words.write_text(json.dumps(invalid))
            code, output = cli('cues', piece)
            verdict('cues refuse non-finite word data without replacing an output', code == 2
                    and working.read_bytes() == before, output)
            words.write_text(json.dumps(rows))
            target = root / C.SCENES / f'{piece}.cues.json'
            code, output = cli('cues', piece, '-o', target)
            verdict('cues write accepted data only through explicit tracked output', code == 0 and target.is_file(), output)
            if have_git:
                C.run(['git','init','-q'],cwd=root)
                C.run(['git','config','user.name','Fixture'],cwd=root)
                C.run(['git','config','user.email','fixture@example.com'],cwd=root)
                C.run(['git','add','-A'],cwd=root); C.run(['git','commit','-qm','accepted cues'],cwd=root)
                code, output = cli('cues', piece, '-o', target)
                verdict('cues replace a clean committed cue file atomically', code == 0
                        and not target.with_name('.' + target.name + '.partial').exists(), output)
                target.write_text('author edit\n')
                with patch.object(K, 'build_cues', side_effect=AssertionError('dirty output must fail early')):
                    code, output = cli('cues', piece, '-o', target)
                verdict('cues refuse dirty output before matching', code == 2 and target.read_text() == 'author edit\n', output)
                C.run(['git','restore',str(target.relative_to(root))],cwd=root)
                original = K.script_events
                def concurrent_edit(*args):
                    target.write_text('edited during matching\n')
                    return original(*args)
                with patch.object(K, 'script_events', concurrent_edit):
                    code, output = cli('cues', piece, '-o', target)
                verdict('cues recheck author edits immediately before replacement', code == 2
                        and target.read_text() == 'edited during matching\n', output)
        finally:
            C.ROOT = saved_root


def test_captions(verdict, cli, root: Path) -> None:
    cues = [K.Cue(1.0, 3.0, ["The ferry is late again."]), K.Cue(3.2, 6.0, ["Every crossing waits", "for the tide."])]
    text = K.srt_text(cues)
    back = K.parse_srt(text)
    verdict("SRT round trip", [(c.start, c.end, c.lines) for c in back] == [(c.start, c.end, c.lines) for c in cues],
            text)
    verdict("WebVTT uses dots and a header", K.vtt_text(cues).startswith("WEBVTT") and "00:00:01.000 -->"
            in K.vtt_text(cues))
    srt = write(root / C.CAPTIONS / "001-fixture.en-GB.srt", text)
    code, out = cli("captions", "check", srt, "--deliverable", "youtube.long")
    verdict("a clean SRT passes captions check", code == 0, out)
    long_line = "x" * 43
    code, out = cli("captions", "check", write(root / "t1.srt", K.srt_text([K.Cue(0, 4, [long_line])])))
    verdict("a 43-character landscape line fails", code == 1 and "43 characters" in out, out)
    code, out = cli("captions", "check", write(root / "t2.srt", K.srt_text([K.Cue(0, 2, ["x" * 40])])))
    verdict("20 characters a second fails", code == 1 and "20.0 characters a second" in out, out)
    code, out = cli("captions", "check", write(root / "t3.srt", K.srt_text(
        [K.Cue(0, 2, ["One two three."]), K.Cue(1.9, 4, ["Four five six."])])))
    verdict("an overlap fails", code == 1 and "overlaps" in out, out)
    code, out = cli("captions", "check", write(root / "t4.srt", K.srt_text([K.Cue(0, 3, ["x" * 33])])),
                    "--deliverable", "youtube.short")
    verdict("a 33-character line fails a 9:16 deliverable", code == 1 and "limit 32" in out, out)
    code, out = cli("captions", "check", write(root / "t0.srt", ""))
    verdict("an SRT with no cues fails captions check", code == 1 and "no cues" in out, out)
    code, out = cli("captions", "check", write(root / "t0b.srt", "1\n00:00:00,000 --> 00:00:02,000\n\n"))
    verdict("a cue with no text fails captions check", code == 1 and "has no text" in out, out)
    tangled = write(root / "t3b.srt", K.srt_text([K.Cue(0.5, 2.0, ["One two three."]), K.Cue(1.8, 3.0, ["Four five."]),
                                                  K.Cue(2.172, 2.9, ["Six."])]))
    code, out, err = cli_split("captions", "rewrap", tangled, "--deliverable", "youtube.short")
    rew = K.parse_srt(out) if code != 2 else []
    verdict("rewrap of overlapping cues leaves no cue ending before it starts, and every word",
            rew and all(c.end > c.start for c in rew) and "Six." in out and "Four five." in out, out + err)
    code, out, err = cli_split("captions", "vtt", tangled)
    verdict("captions vtt refuses overlapping cues (exit 1) and writes nothing",
            code == 1 and "overlaps" in err and "WEBVTT" not in out, out + err)
    script = root / C.PIECES / "001-fixture" / "script.md"
    good = K.srt_text([K.Cue(0.0, 2.2, ["The ferry is late again."]),
                       K.Cue(2.4, 5.6, ["Every crossing waits for the tide,", "not the timetable."]),
                       K.Cue(5.8, 9.4, ["So the timetable is a promise", "the sea never signed."])])
    code, out = cli("captions", "check", write(root / "t5.srt", good), "--script", script)
    verdict("captions check --script: the same words pass", code == 0, out)
    code, out = cli("captions", "check", write(root / "t6.srt", good.replace("tide", "tides")), "--script", script)
    verdict("captions check --script: a changed word fails", code == 1 and "tides" in out, out)
    code, out = cli("captions", "check", write(root / "t6b.srt", good.split("\n\n3\n")[0] + "\n"),
                    "--script", script)
    verdict("captions check --script: an uncaptioned ending fails a master", code == 1 and "closing" in out, out)
    code, out = cli("captions", "check", write(root / "001-fixture--c01.en-GB.srt", good.split("\n\n3\n")[0] + "\n"),
                    "--script", script)
    verdict("captions check --script: a cut may stop inside the script", code == 0, out)
    wide = K.srt_text([K.Cue(0.0, 6.0, ["Every crossing waits for the tide, and not", "for the timetable that the office prints."])])
    code, out, err = cli_split("captions", "rewrap", write(root / "t7.srt", wide), "--deliverable", "youtube.short")
    rew = K.parse_srt(out) if code != 2 else []
    out += err
    verdict("rewrap to 9:16 re-chunks within 32 characters, to stdout without -o", code == 0 and len(rew) >= 2
            and all(len(line) <= 32 for c in rew for line in c.lines)
            and not list((root / C.PUB_RENDERS).glob("t7*")), out)
    code, out = cli("captions", "retime", srt, "--in", "00:00:02.000", "--out", "00:00:05.000",
                    "-o", root / C.PUB_RENDERS / "cut.srt")
    cut = K.read_srt(root / C.PUB_RENDERS / "cut.srt")
    verdict("retime --in --out shifts, clips and drops", code == 0 and len(cut) == 2 and cut[0].start == 0.0
            and abs(cut[1].start - 1.2) < 1e-6 and abs(cut[1].end - 3.0) < 1e-6, K.srt_text(cut))
    code, out = cli("captions", "retime", srt, "--in", "0", "--out", "1", "--edl", root / "x.toml", "--source", "F0001")
    verdict("retime refuses --in and --out together with --edl (exit 2)", code == 2 and "not both" in out, out)
    code, out, err = cli_split("captions", "vtt", srt)
    verdict("captions vtt prints WebVTT to stdout without -o, and writes no file",
            code == 0 and out.startswith("WEBVTT") and not err and not list(root.rglob("*.vtt")), out + err)
    vtt = root / C.CAPTIONS / "001-fixture.en-GB.vtt"
    code, out = cli("captions", "vtt", srt, "-o", vtt)
    verdict("captions vtt -o writes the named file", code == 0 and vtt.is_file(), out)
    code, out = cli("captions", "vtt", srt, "-o", vtt)
    verdict("captions vtt never overwrites a file outside renders/ and generated/", code == 2 and "never" in out, out)
    code, out = cli("captions", "vtt", srt, "-o", srt)
    verdict("an output that is its own input is refused", code == 2, out)
    para = ("The harbour master, who had kept the light for forty years, said the tide was never late; "
            "only the people waiting for it were early, and they blamed the boat.")
    chunks = K.chunk_text(para, 32)
    verdict("chunking keeps every cue inside two lines of 32", chunks and
            all(K.break_lines(c, 32) for c in chunks) and " ".join(chunks) == para, chunks)
    code, out = cli("script", "time", script)
    verdict("script time counts spoken words only, with pauses", code == 0 and "  Total" in out and
            " 24 " in out and "0.6" in out and "within" in out, out)
    verdict("script time reads each beat's target as its own duration and sums them",
            "target 00:03.0" in out and "target 00:10.0" in out and "beat targets sum to 00:13.0" in out
            and "from the brief's words_per_minute" in out, out)
    write(root / C.PIECES / "001-fixture" / "brief.md", BRIEF_MD.replace("words_per_minute: 150", "words_per_minute: 75"))
    code, out = cli("script", "time", script)
    verdict("script time takes the brief's words_per_minute (75: the beats run long)",
            code == 1 and "75 words a minute" in out and "long by" in out, out)
    code, out = cli("script", "time", script, "--wpm", "150")
    verdict("--wpm overrides the brief's pace", code == 0 and "from --wpm" in out, out)
    write(root / C.PIECES / "001-fixture" / "brief.md", BRIEF_MD)
    code, out = cli("script", "time", script, "--wpm", "0")
    verdict("--wpm 0 is refused (exit 2)", code == 2, out)
    code, out = cli("script", "time", script, "--wpm", "5")
    verdict("script time: an estimate past the target and max_seconds is a finding",
            code == 1 and "OUTSIDE" in out and "youtube.short max_seconds 180: OVER" in out, out)
    code, out = cli("script", "time", script, "--write")
    meta = C.split_frontmatter(C.read_text(script))[0]
    verdict("script time --write records words and estimated_seconds", meta.get("words") == 24
            and isinstance(meta.get("estimated_seconds"), float), meta)
    test_transcript(verdict, root, script)


def test_transcript(verdict, root: Path, script: Path) -> None:
    code, out, err = cli_split("captions", "transcript", script)
    verdict("captions transcript: spoken words a sentence a line, TEXT as [On screen: …], SFX in lower case, "
            "NOTE cues, braces and one voice's tags dropped, to stdout without -o",
            code == 0 and "The ferry is late again.\n[On screen: Late again?]" in out and "[gulls, low]" in out
            and "{" not in out and "VO:" not in out and "ON:" not in out and "**" not in out
            and "So the timetable is a promise the sea never signed." in out
            and not list(C.path(C.CAPTIONS).glob("*.transcript.*")), out + err)
    verdict("captions transcript: a paragraph per beat", "Late again?]\n\nEvery crossing" in out, out)
    code, out, err = cli_split("captions", "transcript", script, "--lines", "2.1-2.2")
    verdict("captions transcript --lines takes only one cut's lines (the lines captions align --lines takes)",
            code == 0 and "The ferry is late again." not in out and "Every crossing waits" in out
            and "So the timetable" in out and "(lines 2.1-2.2)" in out, out + err)
    two = write(root / C.PIECES / "001-fixture" / "two-voices.md", TRANSCRIPT_MD.replace(
        "HOST: Boats leave on the tide.", "GUEST: Boats leave on the tide.").replace("piece: 001-fixture", "piece: 001-fixture"))
    code, out, err = cli_split("captions", "transcript", two, "--date", "03/10/2026")
    verdict("captions transcript names two speakers in bold, and says when it was recorded",
            code == 0 and "**Host:** The harbour opens at dawn." in out and "**Guest:** Boats leave on the tide." in out
            and "As recorded on 03/10/2026." in out, out + err)
    transcript = root / C.PIECES / "001-fixture" / "transcript.md"
    code, out, err = cli_split("captions", "transcript", transcript)
    verdict("captions transcript of one speaker's transcript names nobody", code == 0 and "**" not in out
            and "HOST" not in out and "The harbour opens at dawn." in out, out + err)
    dest = C.path(C.CAPTIONS) / "001-fixture.transcript.en-GB.md"
    code, out, err = cli_split("captions", "transcript", script, "-o", dest)
    code2, out2, err2 = cli_split("captions", "transcript", script, "-o", dest)
    verdict("captions transcript writes only with -o, and never over the tracked file",
            code == 0 and dest.is_file() and code2 == 2 and "never overwrites" in err2, err + err2)
    dest.unlink()


def test_repo(verdict, skip, cli, root: Path, have_git: bool, have_ff: bool) -> None:
    src = write(Path(str(root) + "-outside") / "talk-cam-a.bin", "fixture footage bytes\n")
    code, out = cli("footage", "add", src, "--kind", "stock", "--location", "Archive drive A")
    rows = R.manifest_rows(C.path(C.MANIFEST))
    verdict("footage add copies (never moves) and logs F0001", code == 0 and src.is_file() and
            (C.path(C.RAW) / "talk-cam-a.bin").is_file() and rows and rows[0]["id"] == "F0001", out)
    code, out = cli("footage", "add", src, "--kind", "stock", "--location", "Archive drive A")
    verdict("footage add refuses a duplicate hash", code == 2 and "already logged as F0001" in out, out)
    code, out = cli("footage", "verify")
    verdict("footage verify passes on a true mirror", code == 0, out)
    (C.path(C.RAW) / "talk-cam-a.bin").write_text("fixture footage bytez\n", encoding="utf-8")
    code, out = cli("footage", "verify")
    verdict("footage verify fails on a changed byte", code == 1 and "differ" in out, out)
    (C.path(C.RAW) / "talk-cam-a.bin").write_text("fixture footage bytes\n", encoding="utf-8")
    write(C.path(C.RAW) / "stray.bin", "x")
    code, out = cli("footage", "verify")
    verdict("footage verify fails on an unlisted file", code == 1 and "not in the manifest" in out, out)
    (C.path(C.RAW) / "stray.bin").unlink()
    for piece, fmt in (("003-fixture-mp3", "mp3_44100_128"), ("004-fixture-pcm", "pcm_22050")):
        write(C.path(C.VOICEOVER) / f"{piece}.toml",
              f'[voiceover]\npiece = "{piece}"\nvoice_use = "voiceover"\nmodel_id = "eleven_v4"\n'
              f'output_format = "{fmt}"\nper_cue = false\n\n[[segment]]\nid = "s01"\nscript_lines = "1.1"\n'
              'text = "The ferry is late again."\nrequest = "The ferry is late again."\ntake = 0\nfile = ""\n'
              'characters = 24\npause_after = 0.3\nstatus = ""\narchived = ""\n')
        fresh = write(C.path(C.VO_GENERATED) / "tts_The_f_20261003_101010.mp3", "fake take")
        code, out = cli("take", "add", fresh, "--piece", piece, "--segment", "s01")
        ext = ".pcm" if fmt.startswith("pcm") else ".mp3"
        reg = C.load_toml(C.path(C.VOICEOVER) / f"{piece}.toml")["segment"][0]
        verdict(f"take add names a {fmt.split('_')[0]} take {ext} and writes the register",
                code == 0 and (C.path(C.VO_GENERATED) / f"{piece}.s01.t1{ext}").is_file() and not fresh.exists()
                and reg["take"] == 1 and reg["file"] == f"generated/{piece}.s01.t1{ext}"
                and reg["status"] == "generated", out)
    log = C.read_text(C.path(C.CREDITS_LOG))
    verdict("take add appends one credits-log row per take", log.count("| text_to_speech |") == 2
            and "Fixture Voice" in log and "24 characters" in log, log)
    fresh = write(C.path(C.AB_GENERATED) / "tts_Chapt_20261003_101010.mp3", "fake chapter take")
    write(C.path(C.AB_GENERATED) / "002-fixture-book.ch01.p01.txt", "x" * 120)
    code, out = cli("take", "add", fresh, "--piece", "002-fixture-book", "--chapter", "ch01", "--part", "p01")
    reg = C.read_text(C.path(C.AUDIOBOOK) / "002-fixture-book.md")
    verdict("take add names a chapter part's take and writes the chapter register",
            code == 0 and (C.path(C.AB_GENERATED) / "002-fixture-book.ch01.p01.t1.pcm").is_file()
            and "| p01.t1 |" in reg and "| generated |" in reg, out + reg)
    code, out = cli("take", "add", write(root / "loose.mp3", "x"), "--piece", "003-fixture-mp3", "--segment", "s01")
    verdict("take add refuses a file outside generated/", code == 2, out)
    fresh = write(C.path(C.AB_GENERATED) / "tts_Credits_20261003_101011.mp3", "fake credits take")
    code, out = cli("take", "add", fresh, "--piece", "008-fixture-voice-format", "--chapter", "ch00", "--part", "p01")
    reg = C.read_text(C.path(C.AUDIOBOOK) / "008-fixture-voice-format.md")
    verdict("take add reads the output format from voice.md when the chapter register has none, "
            "and takes the opening credits as ch00",
            code == 0 and (C.path(C.AB_GENERATED) / "008-fixture-voice-format.ch00.p01.t1.pcm").is_file()
            and "Output format of the narration row" in out
            and "| ch00 | Opening credits | 008-fixture-voice-format.ch00.md | ai | p01.t1 |" in reg,
            out + reg)
    test_takes(verdict, cli)
    chapter = root / "manuscript/src/01-the-ford/01-the-ford.md"
    A.USE_PANDOC = False
    try:
        code, out = cli("audiobook", "text", chapter, "--piece", "002-fixture-book", "--chapter", "ch01")
    finally:
        A.USE_PANDOC = True
    chunk = C.read_text(C.path(C.AB_GENERATED) / "002-fixture-book.ch01.p01.txt")
    verdict("audiobook text strips markers, comments, citation keys, divs and spans",
            "<!--" not in chunk and "@doe" not in chunk and ":::" not in chunk and "{.conlang" not in chunk
            and "hebori" in chunk and "breath is" not in chunk, chunk)
    parts = sorted(C.path(C.AB_GENERATED).glob("002-fixture-book.ch01.p*.txt"))
    side = C.path(C.AB_GENERATED) / "002-fixture-book.ch01.chunks.toml"
    chunks = C.load_toml(side).get("chunk", []) if side.is_file() else []
    verdict("audiobook text ends a chunk at each scene break and records the pause in the sidecar, "
            "never in the text",
            len(parts) == 3 and not any("{pause" in C.read_text(x) for x in parts)
            and [c["pause_after"] for c in chunks] == [2.0, 2.0, 0.0]
            and [c["file"] for c in chunks] == [x.name for x in parts], [C.read_text(x) for x in parts] + chunks)
    verdict("audiobook text applies voice.md's pronunciations", "/ˈθɑːvəl/" in chunk, chunk)
    verdict("audiobook text lists the unpronounced word and the scripture reference (exit 1)",
            code == 1 and "hebori" in out and "John 3:16" in out and "Tharvel" not in out.split("before any call")[-1], out)
    code, out = cli("audiobook", "text", chapter, "--piece", "002-fixture-book", "--chapter", "ch01",
                    "--footnotes", "inline", "--limit", "200")
    parts = sorted(C.path(C.AB_GENERATED).glob("002-fixture-book.ch01.p*.txt"))
    texts = [C.read_text(p).strip() for p in parts]
    verdict("audiobook text inlines footnotes and chunks under --limit at paragraph boundaries",
            len(parts) >= 2 and all(len(t) <= 200 for t in texts) and any("breath is a count" in t for t in texts),
            texts)
    credits = C.path(C.AUDIOBOOK) / "008-fixture-voice-format.ch00.md"
    code, out = cli("audiobook", "text", credits, "--piece", "008-fixture-voice-format", "--chapter", "ch00")
    credit = C.read_text(C.path(C.AB_GENERATED) / "008-fixture-voice-format.ch00.p01.txt") \
        if (C.path(C.AB_GENERATED) / "008-fixture-voice-format.ch00.p01.txt").is_file() else ""
    verdict("audiobook text reads ch00 from the credits' own file beside the chapter register",
            code == 0 and "The Ford, a fixture." in credit and "Read by a fixture narrator." in credit
            and "note:" not in out, out + credit)
    code, out = cli("audiobook", "text", credits, "--piece", "008-fixture-voice-format", "--chapter", "ch01")
    verdict("audiobook text refuses the opening credits' file as another chapter (exit 2)",
            code == 2 and "--chapter ch00" in out, out)
    write(root / C.AUDIOBOOK / "009-fixture-channels.md",
          CHAPTER_REG.replace("002-fixture-book", "009-fixture-channels")
          .replace("[spotify_authors]", "[acx, spotify-authors]"))
    code, out = cli("audiobook", "text", chapter, "--piece", "009-fixture-channels", "--chapter", "ch01")
    verdict("audiobook text refuses a channel that is not the store part of an [audiobook.<store>] key "
            "(exit 2), and accepts one that is",
            code == 2 and "'spotify-authors'" in out and "spotify_authors" in out and "'acx'" not in out
            and not list(C.path(C.AB_GENERATED).glob("009-fixture-channels.*")), out)
    shaped = write(root / "scratch-script.md", SCRIPT_SHAPED_MD)
    code, out = cli("audiobook", "text", shaped, "--piece", "008-fixture-voice-format", "--chapter", "ch99")
    verdict("audiobook text refuses a file shaped like an audiobook script: an audiobook has none (exit 2)",
            code == 2 and "has no script" in out, out)
    business = write(root / "manuscript/src/02-running/02-running.md", BUSINESS_CHAPTER_MD)
    for pandoc in (False, True):
        if pandoc and not shutil.which("pandoc"):
            skip("audiobook text lists a table, an image and an abbreviation (through pandoc)",
                 "pandoc is not installed")
            continue
        A.USE_PANDOC = pandoc
        try:
            code, out = cli("audiobook", "text", business, "--piece", "014-fixture-guide", "--chapter", "ch02")
        finally:
            A.USE_PANDOC = True
        chunk = "".join(C.read_text(x) for x in sorted(C.path(C.AB_GENERATED).glob("014-fixture-guide.ch02.p*.txt")))
        verdict("audiobook text lists a table, an image and an abbreviation, and leaves the table, the "
                f"image and every square bracket out of the text ({'pandoc' if pandoc else 'plain'})",
                code == 1 and "table" in out and "'Booking checklist'" in out and "image" in out
                and "'Chart of bookings by month'" in out and "abbreviation  HLS" in out
                and "Pick a date" not in chunk and "----" not in chunk and "Chart of bookings" not in chunk
                and "[" not in chunk and "]" not in chunk and "the guide for the rest" in chunk
                and "example.org" not in chunk, out + chunk)
    if shutil.which("pandoc"):
        code, out = cli("audiobook", "text", chapter, "--piece", "002-fixture-book", "--chapter", "ch01")
        chunk = C.read_text(C.path(C.AB_GENERATED) / "002-fixture-book.ch01.p01.txt")
        side = C.load_toml(C.path(C.AB_GENERATED) / "002-fixture-book.ch01.chunks.toml").get("chunk", [])
        verdict("audiobook text through pandoc gives the same spoken text and pauses",
                code == 1 and "{pause" not in chunk and "@doe" not in chunk and "/ˈθɑːvəl/" in chunk
                and [c["pause_after"] for c in side] == [2.0, 2.0, 0.0], chunk + str(side))
    else:
        skip("audiobook text through pandoc", "pandoc is not installed")
    alt = Path(str(root) + "-where")   # a project outside any work tree: where's plain list, filtered
    C.ROOT = alt
    try:
        test_where(verdict, cli, alt, False)
    finally:
        C.ROOT = root
    if not have_git:
        skip("flags, check and check --setup in a git repository", "git is not installed")
        return
    git = ["git", "-c", "user.name=media self-test", "-c", "user.email=toolkit@example.com"]
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    write(root / ".gitignore", "/manuscript/\nignored-notes.md\n")
    write(root / "brand/src/notes.md", "<!-- AUTHOR TO CONFIRM: the handle -->\nAn example: `<!-- VERIFY: x -->`\n")
    write(root / "brand/src/sample.css", "a { color: red; } /* VERIFY: the accent */\n")
    write(root / "publishing/src/sample.toml", "# AUTHOR TO CONFIRM: the cadence\n")
    write(root / "brand/src/ignored-notes.md", "<!-- VERIFY: never read -->\n")
    machine = Path(str(root) + "-machine")  # a machine whose own git filters, marks and ignores
    for rel, text in ((".gitconfig", '[filter "lfs"]\n\tclean = false\n\tprocess = false\n'),
                      ("etc/gitconfig", '[filter "lfs"]\n\tclean = false\n\tprocess = false\n'),
                      (".config/git/attributes", "* filter=lfs diff=lfs merge=lfs -text\n"),
                      (".config/git/ignore", "*.md\n")):
        write(machine / rel, text)
    label = ("the fixtures' git reads no LFS filter, attribute or ignore rule from the machine's system or "
             "global files")
    if git_version() < (2, 32):
        skip(label, "git is older than 2.32, the first to read GIT_CONFIG_GLOBAL in place of ~/.gitconfig")
    else:
        with held_env(HOME=str(machine), XDG_CONFIG_HOME=str(machine / ".config"),
                      GIT_CONFIG_SYSTEM=str(machine / "etc/gitconfig")):
            filters = R.git_config("filter.lfs.process", root) + R.git_config("filter.lfs.clean", root)
            marked = R.lfs_marked(["brand/src/notes.md"], root)
            kept = C.not_ignored([root / "brand/src/notes.md"], root)
        verdict(label, not filters and not marked and len(kept) == 1,
                f"filter: {filters!r}; marked: {sorted(marked)}; not ignored: {kept}")
    code, out = cli("flags")
    verdict("flags lists both flags in every form, never a backticked example or an ignored file",
            code == 0 and "AUTHOR TO CONFIRM: 2" in out and "VERIFY: 1" in out and "never read" not in out, out)
    code, out = cli("flags", "--strict")
    verdict("flags --strict is exit 1 while any flag is open", code == 1, out)
    write(root / "publishing/src/posts/001-fixture.md", "<!-- VERIFY: the hashtag limit -->\n")
    write(root / C.CARDS / "001-fixture.title.html", "<!-- AUTHOR TO CONFIRM: the words -->\n")
    write(root / "publishing/src/captions/001-fixture--c01.en-GB.srt", "1\n00:00:00,000 --> 00:00:01,000\nx\n")
    write(root / "publishing/src/posts/002-other.md", "<!-- VERIFY: another piece's flag -->\n")
    code, out = cli("flags", "--piece", "001-fixture", "--strict")
    verdict("flags --piece gathers one piece's files across the layers by their names",
            code == 1 and "AUTHOR TO CONFIRM: 1" in out and "VERIFY: 1" in out and "002-other" not in out
            and "001-fixture.title.html" in out and "of 001-fixture" in out, out)
    code, out = cli("flags", "--piece", "009-no-such-piece")
    verdict("flags --piece names a piece that has no folder (exit 2)", code == 2, out)
    code, out = cli("flags", root / "publishing", "--piece", "001-fixture")
    verdict("flags PATH --piece keeps the piece's files under that path",
            code == 0 and "VERIFY: 1" in out and "AUTHOR TO CONFIRM: 0" in out, out)
    test_where(verdict, cli, root, True)
    code, out = cli("check")
    verdict("check is clean on a fresh repository", code == 0, out)
    verdict("the project root is the toolkit's parent, never git's top level", C._find_root() == C.TOOLKIT.parent)
    mono = Path(str(root) + "-mono")
    (mono / "media-project").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(mono)], check=True)
    _, warns = R.repository_guard(mono / "media-project")
    verdict("check warns when the project sits inside a larger repository", any("top level" in w for w in warns), warns)
    hero = write(root / "brand/src/exports/large/hero.bin", "not an lfs pointer\n" * 4)
    subprocess.run(git + ["add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(git + ["commit", "-qm", "fixture"], cwd=root, check=True, capture_output=True)
    code, out = cli("check")
    verdict("check finds an LFS-marked file stored as a plain blob", code == 1 and "plain blob" in out, out)
    subprocess.run(git + ["rm", "-q", "--cached", str(hero)], cwd=root, check=True, capture_output=True)
    fake = Path(str(root) + "-bin")
    write(fake / "git-lfs", "#!/bin/sh\necho 'git-lfs/3.4.1 (fixture)'\n").chmod(0o755)
    saved = os.environ["PATH"]
    os.environ["PATH"] = f"{fake}{os.pathsep}{saved}"
    try:
        code, out = cli("check")
    finally:
        os.environ["PATH"] = saved
    verdict("check finds an LFS-marked file while git-lfs prints a version but no filter is configured",
            code == 1 and "no LFS filter is configured" in out and "plain blob" not in out, out)
    hero.unlink()
    big = root / "production/src/assets/huge.bin"
    big.parent.mkdir(parents=True, exist_ok=True)
    with open(big, "wb") as fh:
        fh.truncate(R.LARGE + 1)
    with open(root / C.PROD_RENDERS / "huge-render.bin", "wb") as fh:
        fh.truncate(R.LARGE + 1)
    code, out = cli("check")
    verdict("check finds a file over 10 MB outside the ignored folders, and only that one",
            code == 1 and "production/src/assets/huge.bin" in out and "huge-render" not in out, out)
    big.unlink()
    rules = root / "publishing/src/.gitignore"
    write(rules, "/renders/*\n")
    code, out = cli("check")
    verdict("check finds a missing nested ignore rule", code == 1 and "!/renders/README.md" in out, out)
    write(rules, "/renders/*\n!/renders/README.md\n")
    home = Path(str(root) + "-home")
    secret = "fixture-secret-value-never-printed"
    claude = {"mcpServers": {"elevenlabs": {"type": "stdio", "command": "uvx", "args": ["elevenlabs-mcp"],
                                            "env": {"ELEVENLABS_API_KEY": secret,
                                                    "ELEVENLABS_MCP_BASE_PATH": str(home / "Desktop")}}},
              "oauthAccount": {"emailAddress": "fixture@example.com"}}
    write(home / ".claude.json", json.dumps(claude))
    saved_home = os.environ.get("HOME")
    os.environ["HOME"] = str(home)
    try:
        code, out = cli("check", "--setup")
        verdict("check --setup reports a missing ask rule and a base path outside the repository",
                code == 1 and "ask mcp__elevenlabs__create_voice_from_preview is not in" in out
                and "does not contain this repository" in out, out)
        verdict("check --setup prints no other value from ~/.claude.json",
                secret not in out and "fixture@example.com" not in out and "uvx elevenlabs-mcp" in out, out)
        verdict("check --setup names the optional encoders image needs, as notes, never findings",
                ("libwebp (optional" in out and "avif muxer (optional" in out) or not shutil.which("ffmpeg"), out)
        verdict("check --setup names fontconfig's fc-match, without which card.py --self-test is incomplete, as "
                "a note, never a finding", "--    fc-match (optional, fontconfig" in out
                and "FAIL  fc-match" not in out, out)
        verdict("check --setup requires D13's two deny entries, each with its fix, like the allows",
                "FAIL  deny Edit(**/generated/**) is not in" in out and "FAIL  deny Edit(**/renders/**) is not in" in out
                and 'fix: add "Edit(**/renders/**)" to permissions.deny by hand' in out, out)
        claude["mcpServers"]["elevenlabs"]["env"]["ELEVENLABS_MCP_BASE_PATH"] = str(root.parent)
        write(home / ".claude.json", json.dumps(claude))
        settings = json.loads(C.read_text(root / C.SETTINGS))
        settings["permissions"]["deny"] += list(R.SETTINGS_DENY)
        write(root / C.SETTINGS, json.dumps(settings, indent=2))
        code, out = cli("check", "--setup")
        verdict("check --setup accepts a base path that contains the repository",
                "contains this repository" in out and "does not contain" not in out, out)
        verdict("check --setup passes the deny entries once they are present",
                "ok    deny Edit(**/generated/**)" in out and "ok    deny Edit(**/renders/**)" in out
                and "FAIL  deny" not in out, out)
    finally:
        if saved_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = saved_home


def test_words(verdict, cli, root: Path) -> None:
    from unittest.mock import patch
    with patch.dict(os.environ, {'MEDIA_TRANSCRIBE_PYTHON': str(root / 'missing-python')}):
        try:
            A.run_transcribe(['status'])
            correct = False
        except C.Fatal as error:
            correct = 'MEDIA_TRANSCRIBE_PYTHON' in str(error) and 'uv is not installed' not in str(error)
        verdict('missing named transcription interpreter gets its own hint', correct)
    import transcribe as T
    verdict('transcribe worker standard-library self-test', T.self_test() == 0)
    rows = [{'word': 'A', 'start': 0.1, 'end': 0.3, 'score': 0.8, 'segment': 's01'},
            {'word': 'ferry', 'start': 0.4, 'end': 1.1, 'score': 0.7, 'segment': 's01'},
            {'word': 'crosses.', 'start': 1.2, 'end': 2.5, 'score': 0.9, 'segment': 's01'},
            {'word': 'Home.', 'start': 2.8, 'end': 4.0, 'score': 0.8, 'segment': 's02'}]
    source = root / C.TIMING / '033-fixture.words.json'
    write(source, json.dumps(rows))
    code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short')
    destination = K.default_srt('033-fixture.youtube-short.en-GB.srt')
    cues = K.read_srt(destination) if destination.is_file() else []
    verdict('from-words: every cue lands on its first and last word, within limits',
            code == 0 and [(c.start, c.end, c.text) for c in cues] ==
            [(0.1, 2.5, 'A ferry crosses.'), (2.8, 4.0, 'Home.')], out)
    explicit = root / C.CAPTIONS / '033-fixture.offset.en-GB.srt'
    code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short', '--offset', '2',
                    '-o', explicit)
    verdict('from-words: an offset shifts the exact boundaries, explicit -o writes tracked captions',
            code == 0 and K.read_srt(explicit)[0].start == 2.1, out)
    rows[-1]['start'] = 2.52
    write(source, json.dumps(rows))
    code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short')
    verdict('from-words: short gap is a finding, no spoken word is trimmed',
            code == 1 and 'before the next cue' in out and K.read_srt(destination)[0].end == 2.5, out)
    before = destination.read_bytes()
    for value, expected in ((None, 1), (float('nan'), 2), (-0.1, 2)):
        rows[0]['start'] = value
        write(source, json.dumps(rows))
        code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short')
        verdict(f'from-words: invalid time {value!r} refuses output',
                code == expected and destination.read_bytes() == before, out)
    rows[0]['start'] = 0.1
    for score in (None, True, float('nan'), 1.1):
        rows[0]['score'] = score
        write(source, json.dumps(rows))
        code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short')
        verdict(f'from-words: invalid score {score!r} refuses output',
                code == 2 and destination.read_bytes() == before, out)
    rows[0]['score'] = 0.8
    for word in ('{quiet} A', '[quiet] A'):
        rows[0]['word'] = word
        write(source, json.dumps(rows))
        code, out = cli('captions', 'from-words', source, '--deliverable', 'youtube.short')
        verdict('from-words: directions and tags refuse output ' + word,
                code == 1 and destination.read_bytes() == before, out)


def test_lipsync(verdict, skip, cli, root: Path, have_git: bool) -> None:
    import wave
    from unittest.mock import patch
    piece = '036-mouth-fixture'
    takes = root / C.VO_GENERATED / piece / 'takes'
    takes.mkdir(parents=True, exist_ok=True)
    rows = []
    for number, text in enumerate(('A ferry crosses.', 'Home again.'), 1):
        take = takes / f'{piece}.s{number:02d}.t1.wav'
        with wave.open(str(take), 'wb') as audio:
            audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000)
            audio.writeframes(b'\0\0' * 4800)
        rows.append(f'[[segment]]\nid = "s{number:02d}"\nstatus = "approved"\ntext = "{text}"\n'
                    f'request = "[quiet] feh-ree"\npause_after = {number / 10}\n'
                    f'file = "generated/{piece}/takes/{take.name}"\n')
    register = root / C.VOICEOVER / f'{piece}.toml'
    write(register, f'[voiceover]\npiece = "{piece}"\noutput_format = "pcm_8000"\n' + ''.join(rows))
    code, out = cli('voice', 'join', piece)
    verdict('lipsync fixture uses the real approved voice join with pauses', code == 0, out)
    release = root / 'tool-fixture' / 'release' / 'rhubarb'
    write(release, '#!/usr/bin/env python3\nimport sys\n'
                   'if sys.argv[1:] == ["--version"]:\n'
                   '    print("Rhubarb Lip Sync version 1.14.0")\n'
                   'else:\n'
                   '    print("synthetic recogniser failure", file=sys.stderr)\n'
                   '    raise SystemExit(1)\n')
    release.chmod(0o755)
    linked = root / 'tool-fixture' / 'bin' / 'rhubarb'
    linked.parent.mkdir(parents=True, exist_ok=True)
    linked.symlink_to(release)
    dictionary = C.rhubarb_dictionary(linked)
    write(dictionary, 'fixture\n')
    verdict('Rhubarb resources are beside the executable through its link',
            dictionary == release.parent / 'res/sphinx/cmudict-en-us.dict')
    original_which, original_run = shutil.which, C.run
    def which(name, *args, **kwargs):
        return str(linked) if name == 'rhubarb' else original_which(name, *args, **kwargs)
    body = {'metadata': {'soundFile': str(A.joined_voice(piece)), 'duration': 1.5},
            'mouthCues': [{'start': n / 10, 'end': (n + 1) / 10, 'value': shape}
                          for n, shape in enumerate('ABCDEFGHX')]}
    calls = []
    def recogniser(argv, **kwargs):
        if str(argv[0]) != str(linked):
            return original_run(argv, **kwargs)
        calls.append(([str(a) for a in argv], Path(argv[argv.index('-d') + 1]).read_text()))
        return subprocess.CompletedProcess(argv, 0, json.dumps(body), '')
    with patch.object(shutil, 'which', which), patch.object(C, 'run', recogniser), \
            patch.object(A, 'pronunciations', return_value={'ferry': 'feh-ree'}):
        code, out = cli('lipsync', piece)
        working = A.joined_voice(piece).parent / 'timing' / f'{piece}.mouth.json'
        made = json.loads(working.read_text()) if working.is_file() else {}
        verdict('lipsync passes pocketSphinx and all extended shapes with plain text, never respellings',
                code == 0 and calls[-1][0][1:7] == ['-r','pocketSphinx','--extendedShapes','GHX','-f','json']
                and calls[-1][1] == 'A ferry crosses.\nHome again.\n', out)
        verdict('lipsync keeps native cues and makes soundFile repository-relative',
                made.get('mouthCues') == body['mouthCues'] and made.get('metadata', {}).get('soundFile') ==
                f'{C.PROD_RENDERS}/{piece}/{piece}.voice.wav' and '9 mouth cues' in out, out)
        # Keep the repository's logical input name even when the joined WAV is a link
        # to user storage: resolving that link must not put a home path in tracked JSON.
        voice = A.joined_voice(piece)
        with tempfile.TemporaryDirectory(prefix='media-mouth-audio-') as folder:
            external = Path(folder) / 'joined.wav'
            shutil.copyfile(voice, external)
            voice.unlink()
            voice.symlink_to(external)
            try:
                code, out = cli('lipsync', piece)
                linked_body = json.loads(working.read_text())
                verdict('linked joined audio still records its logical repository-relative soundFile',
                        code == 0 and linked_body['metadata']['soundFile'] ==
                        f'{C.PROD_RENDERS}/{piece}/{piece}.voice.wav', out)
            finally:
                voice.unlink()
                shutil.copyfile(external, voice)
        before = working.read_bytes()
        dictionary.unlink()
        code, out = cli('lipsync', piece)
        verdict('lipsync refuses a missing dictionary without changing output', code == 2
                and 'cmudict-en-us.dict' in out and working.read_bytes() == before, out)
        setup_rows, setup_findings = R.setup_report(root)
        verdict('setup marks the dictionary missing even when Rhubarb --version succeeds',
                any('rhubarb for lipsync' in line for line in setup_findings))
        write(dictionary, 'fixture\n')
        setup_rows, setup_findings = R.setup_report(root)
        verdict('setup accepts the dictionary beside the linked executable\'s real path',
                any('rhubarb for lipsync' in line and 'ready' in line for line in setup_rows)
                and not any('rhubarb for lipsync' in line for line in setup_findings))
        with patch.object(C, 'run', original_run):
            code, out = cli('lipsync', piece)
        verdict('Rhubarb fatal exit 1 becomes exit 2 with its message and no changed output',
                code == 2 and 'exit 1' in out and 'synthetic recogniser failure' in out
                and working.read_bytes() == before, out)
        body['metadata']['duration'] = float('nan')
        code, out = cli('lipsync', piece)
        verdict('lipsync refuses non-finite native JSON without changing output',
                code == 2 and working.read_bytes() == before, out)
        body['metadata']['duration'] = 1.5
        for field, invalid in (('value', 'Z'), ('start', -0.1), ('end', None)):
            old = body['mouthCues'][0][field]
            body['mouthCues'][0][field] = invalid
            code, out = cli('lipsync', piece)
            verdict(f'lipsync refuses invalid native cue {field} without changing output',
                    code == 2 and working.read_bytes() == before, out)
            body['mouthCues'][0][field] = old
        held_register = register.read_text()
        register.write_text(held_register.replace('status = "approved"', 'status = "generated"', 1))
        count = len(calls)
        code, out = cli('lipsync', piece)
        verdict('lipsync refuses an unapproved take before recognition', code == 1
                and len(calls) == count and working.read_bytes() == before, out)
        register.write_text(held_register)
        held_voice = voice.read_bytes()
        with wave.open(str(voice), 'wb') as audio:
            audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000)
            audio.writeframes(b'\0\0' * 800)
        code, out = cli('lipsync', piece)
        verdict('lipsync refuses a joined voice whose duration no longer matches the takes',
                code == 2 and len(calls) == count and working.read_bytes() == before, out)
        voice.write_bytes(held_voice)
        voice.rename(voice.with_suffix('.held.wav'))
        code, out = cli('lipsync', piece)
        verdict('lipsync names voice join when joined audio is missing',
                code == 2 and 'voice join' in out and len(calls) == count, out)
        voice.with_suffix('.held.wav').rename(voice)
        target = root / C.TIMING / f'{piece}.mouth.json'
        code, out = cli('lipsync', piece, '-o', target)
        verdict('lipsync first explicit -o accepts the tracked mouth file', code == 0 and target.is_file(), out)
        if have_git:
            with tempfile.TemporaryDirectory(prefix='media-mouth-git-') as folder:
                saved = C.ROOT
                try:
                    C.ROOT = Path(folder)
                    shutil.copytree(root / C.VOICEOVER, C.ROOT / C.VOICEOVER)
                    voice = A.joined_voice(piece)
                    voice.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(root / C.PROD_RENDERS / piece / f'{piece}.voice.wav', voice)
                    target = C.ROOT / C.TIMING / f'{piece}.mouth.json'
                    write(target, 'old mouth\n')
                    C.run(['git','init','-q'], cwd=C.ROOT)
                    C.run(['git','config','user.name','Fixture'], cwd=C.ROOT)
                    C.run(['git','config','user.email','fixture@example.com'], cwd=C.ROOT)
                    C.run(['git','add','-A'], cwd=C.ROOT)
                    C.run(['git','commit','-qm','fixture'], cwd=C.ROOT)
                    code, out = cli('lipsync', piece, '-o', target)
                    verdict('lipsync replaces a committed clean tracked mouth file', code == 0
                            and json.loads(target.read_text())['mouthCues'] == body['mouthCues'], out)
                    C.run(['git','add','-A'], cwd=C.ROOT)
                    C.run(['git','commit','-qm','accepted mouths'], cwd=C.ROOT)
                    target.write_text('author edit\n')
                    count = len(calls)
                    code, out = cli('lipsync', piece, '-o', target)
                    verdict('dirty mouth output refuses before recognition', code == 2
                            and len(calls) == count and target.read_text() == 'author edit\n', out)
                    C.run(['git','restore',str(target.relative_to(C.ROOT))], cwd=C.ROOT)
                    def editing_recogniser(argv, **kwargs):
                        if str(argv[0]) == str(linked):
                            target.write_text('edited during recognition\n')
                        return recogniser(argv, **kwargs)
                    with patch.object(C, 'run', editing_recogniser):
                        code, out = cli('lipsync', piece, '-o', target)
                    verdict('mouth guard rechecks author edits during recognition', code == 2
                            and target.read_text() == 'edited during recognition\n', out)
                finally:
                    C.ROOT = saved
    with patch.object(shutil, 'which', lambda name, *a, **k: None if name == 'rhubarb'
                      else original_which(name, *a, **k)):
        setup_rows, setup_findings = R.setup_report(root)
        verdict('absent Rhubarb is a setup note naming lipsync, never a finding',
                any('rhubarb absent: lipsync' in line for line in setup_rows)
                and not any('rhubarb absent' in line for line in setup_findings))
        code, out = cli('lipsync', piece)
        verdict('missing Rhubarb blocks only lipsync with its install hint',
                code == 2 and 'res/ folder' in out, out)
    if not original_which('rhubarb'):
        skip('Rhubarb live lip sync', 'rhubarb is absent')
    elif not original_which('espeak-ng'):
        skip('Rhubarb live lip sync', 'espeak-ng fixture voice is absent')
    else:
        live = '037-mouth-live'
        take = root / C.VO_GENERATED / live / 'takes' / f'{live}.s01.t1.wav'
        take.parent.mkdir(parents=True, exist_ok=True)
        C.run(['espeak-ng','-v','en-gb','-s','130','-w',take,'A ferry crosses.'])
        write(root / C.VOICEOVER / f'{live}.toml', f'[voiceover]\npiece = "{live}"\n'
              'output_format = "pcm_22050"\n[[segment]]\nid = "s01"\nstatus = "approved"\n'
              f'text = "A ferry crosses."\nfile = "generated/{live}/takes/{take.name}"\n')
        code, out = cli('voice','join',live)
        code, out = cli('lipsync',live) if code == 0 else (code, out)
        file = A.joined_voice(live).parent / 'timing' / f'{live}.mouth.json'
        actual = json.loads(file.read_text()) if file.is_file() else {}
        verdict('live Rhubarb recognises the joined espeak voice and stores a relative soundFile',
                code == 0 and bool(actual.get('mouthCues')) and actual.get('metadata', {}).get('soundFile') ==
                f'{C.PROD_RENDERS}/{live}/{live}.voice.wav', out)


def test_transcribe(verdict, cli, root: Path, have_git: bool) -> None:
    import subprocess
    import wave
    from unittest.mock import patch
    piece = '034-fixture'
    take = root / C.VOICEOVER / 'generated' / piece / 'takes' / f'{piece}.s01.t1.wav'
    take.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(take), 'wb') as audio:
        audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(8000)
        audio.writeframes(b'\0\0' * 24000)
    register = root / C.VOICEOVER / f'{piece}.toml'
    def register_text(text='A ferry crosses.', request='A ferry crosses.'):
        return ('[voiceover]\npiece = "034-fixture"\noutput_format = "pcm_8000"\n'
                '[[segment]]\nid = "s01"\nstatus = "approved"\n'
                f'text = "{text}"\nrequest = "{request}"\n'
                f'file = "generated/{piece}/takes/{take.name}"\npause_after = 0\n')
    write(register, register_text())
    code, out = cli('voice', 'join', piece)
    verdict('transcribe fixture joined with the real voice command', code == 0, out)
    reply = {'words': [{'word': 'A', 'start': 0.1, 'end': 0.3, 'score': 0.8, 'segment': 's01'},
                       {'word': 'ferry', 'start': 0.4, 'end': 1.1, 'score': 0.7, 'segment': 's01'},
                       {'word': 'crosses.', 'start': 1.2, 'end': 2.5, 'score': 0.9, 'segment': 's01'}],
             'check': '# Words check\n\nFixture alignment.\n', 'exit': 0}
    jobs = []
    def worker(argv, fetch=False):
        jobs.append(json.loads(Path(argv[-1]).read_text()))
        return subprocess.CompletedProcess(argv, 0, json.dumps(reply), '')
    with patch.object(A, 'run_transcribe', worker):
        code, out = cli('transcribe', piece, '--no-cross-check')
        working = A.joined_voice(piece).parent / 'timing' / f'{piece}.words.json'
        verdict('transcribe launcher supplies the known segment window and prints its check',
                code == 0 and working.is_file() and jobs[-1]['segments'][0]['start'] == 0
                and jobs[-1]['segments'][0]['end'] == 3 and jobs[-1]['cross_check'] is False
                and 'Fixture alignment.' in out, out)
        for text in ('A 2 ferry crosses.', 'A & ferry crosses.', 'A ten % ferry crosses.'):
            write(register, register_text(text))
            calls = len(jobs)
            with patch.object(C, 'probe', wraps=C.probe) as probe:
                code, out = cli('transcribe', piece)
            verdict('transcribe rejects digits and symbols before a worker or process starts: ' + text,
                    code == 1 and len(jobs) == calls and probe.call_count == 0, out)
        write(register, register_text())
        tracked = root / C.TIMING / f'{piece}.words.json'
        checkfile = tracked.with_name(f'{piece}.words-check.md')
        code, out = cli('transcribe', piece, '-o', tracked)
        verdict('transcribe explicit -o writes its paired tracked files for the first time',
                code == 0 and tracked.is_file() and checkfile.is_file(), out)
        if have_git:
            with tempfile.TemporaryDirectory(prefix='media-timing-git-') as folder:
                saved = C.ROOT
                gitroot = Path(folder)
                try:
                    C.ROOT = gitroot
                    write(gitroot / C.VOICEOVER / register.name, register_text())
                    copied_take = gitroot / take.relative_to(root)
                    copied_take.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(take, copied_take)
                    copied_voice = A.joined_voice(piece)
                    copied_voice.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(root / C.PROD_RENDERS / piece / f'{piece}.voice.wav', copied_voice)
                    C.run(['git', 'init', '-q'], cwd=gitroot)
                    C.run(['git', 'config', 'user.name', 'Fixture'], cwd=gitroot)
                    C.run(['git', 'config', 'user.email', 'fixture@example.com'], cwd=gitroot)
                    target = gitroot / C.TIMING / f'{piece}.words.json'
                    sibling = target.with_name(f'{piece}.words-check.md')
                    write(target, 'old words\n'); write(sibling, 'old check\n')
                    C.run(['git', 'add', '-A'], cwd=gitroot)
                    C.run(['git', 'commit', '-qm', 'fixture'], cwd=gitroot)
                    code, out = cli('transcribe', piece, '-o', target)
                    verdict('transcribe -o replaces both committed clean outputs', code == 0
                            and json.loads(target.read_text()) == reply['words']
                            and sibling.read_text() == reply['check'], out)
                    C.run(['git', 'add', '-A'], cwd=gitroot)
                    C.run(['git', 'commit', '-qm', 'accepted timing'], cwd=gitroot)
                    sibling.write_text('author edit\n')
                    before = target.read_bytes()
                    calls = len(jobs)
                    code, out = cli('transcribe', piece, '-o', target)
                    verdict('paired guards: a dirty words check refuses before either output changes',
                            code == 2 and len(jobs) == calls and target.read_bytes() == before
                            and sibling.read_text() == 'author edit\n', out)
                    C.run(['git', 'restore', str(sibling.relative_to(gitroot))], cwd=gitroot)
                    def editing_worker(argv, fetch=False):
                        sibling.write_text('edited during alignment\n')
                        return worker(argv, fetch)
                    with patch.object(A, 'run_transcribe', editing_worker):
                        code, out = cli('transcribe', piece, '-o', target)
                    verdict('paired guards recheck edits made while the alignment runs',
                            code == 2 and target.read_bytes() == before
                            and sibling.read_text() == 'edited during alignment\n', out)
                finally:
                    C.ROOT = saved


def test_voice_plan(verdict, skip, cli, root: Path, have_git: bool) -> None:
    piece = "031-request-plan"
    register = C.path(C.VOICEOVER) / f"{piece}.toml"
    script = C.path(C.PIECES) / piece / "script.md"
    raw = "## 1. Opening\n\nVO: {whispers} The ferry is late again. {pause 0.2}\n"
    write(script, raw)
    reg = voice_register(piece, [("s01", 1, "generated/old.mp3", "approved", "F0001"),
                                 ("s02", 0, "", "", "")])
    write(register, reg)
    voice_md = C.path(C.VOICE_MD)
    held_voice = C.read_text(voice_md)
    write(voice_md, "## Pronunciations\n\n| Word | IPA | Respelling |\n|---|---|---|\n| ferry | feri | feh ree |\n")
    try:
        before = register.read_bytes()
        code, out = cli("speak", "plan", piece)
        verdict("speak plan skips approved takes, prints IPA and script-derived tags offline, creates only "
                "the takes directory and leaves the register unchanged",
                code == 0 and "[whispers] The /feri/ is late again." in out and "1 calls" in out
                and "s01:" not in out and "pause" not in out and "credits" not in out.lower()
                and (C.path(C.VO_GENERATED) / piece / "takes").is_dir()
                and register.read_bytes() == before, out)
        for model, form, tags in (("eleven_v3", "feh ree", True), ("eleven_v4_turbo", "/feri/", True),
                                  ("eleven_multilingual_v2", "feh ree", False)):
            write(register, reg.replace('model_id = "eleven_v4"', f'model_id = "{model}"'))
            code, out = cli("speak", "plan", piece, "--segment", "s01", "--segment", "s02")
            verdict(f"speak plan {model}: the approved segment can be explicitly planned, pronunciations "
                    "follow IPA support and tags follow the confirmed model set",
                    code == 0 and "2 calls" in out and form in out
                    and ("[whispers]" in out) == tags, out)
        write(register, reg)
        code, out = cli("speak", "plan", piece, "--segment", "s99")
        verdict("speak plan refuses an unknown segment without altering the register", code == 2
                and "unknown segment" in out and register.read_bytes() == before, out)
        words = "a" * (A.MODEL_LIMITS["eleven_v4"] + 1)
        write(script, f"## 1. Opening\n\nVO: {words}\n")
        write(register, reg.replace("The ferry is late again.", words))
        code, out = cli("speak", "plan", piece)
        verdict("speak plan flags a request over the model's limit, reporting characters and calls, no rate",
                code == 1 and "OVER LIMIT" in out and "1 calls" in out and "credits" not in out.lower(), out[-400:])
        code, out = cli("speak", "plan", "--trial", "candidate-a")
        trial = C.path(C.VO_GENERATED) / "voice-trials" / "candidate-a"
        verdict("speak plan --trial creates only the trial directory, with no piece or register",
                code == 0 and trial.is_dir() and not list(trial.iterdir()) and str(trial.resolve()) in out, out)
        code, out = cli("speak", "plan", "--trial", "../escape")
        verdict("speak plan refuses a trial directory traversal", code == 2, out)
    finally:
        write(voice_md, held_voice)
    if not have_git:
        skip("D66 tracked timing guard", "git is not installed")
        return
    saved = C.ROOT
    C.ROOT = root.parent / "timing-guard"
    C.ROOT.mkdir()
    def git(*argv):
        subprocess.run(["git", *argv], cwd=C.ROOT, capture_output=True, check=True)
    try:
        git("init", "-q")
        git("config", "user.name", "Fixture Author")
        git("config", "user.email", "fixture@example.com")
        files = []
        patterns = {"words.json": C.TIMING, "words-check.md": C.TIMING, "mouth.json": C.TIMING,
                    "cues.json": C.SCENES, "real.json": C.SCENES}
        verdict("D66 names exactly the five approved timing and scene exceptions", C.TIMING_OUTPUTS == patterns)
        for suffix, folder in patterns.items():
            p = write(C.path(folder) / f"{piece}.{suffix}", "first\n")
            files.append((suffix, p))
        other = write(C.path(C.TIMING) / f"{piece}.levels.json", "first\n")
        git("add", ".")
        git("commit", "-qm", "fixture")
        explicit_only = False
        try:
            C.output_path(files[0][1], tracked_timing=(piece, files[0][0]))
        except C.Fatal:
            explicit_only = True
        verdict("D66 never replaces the tracked copy without an explicit -o", explicit_only)
        for suffix, p in files:
            made = C.output_path(root / "renders" / p.name, p, tracked_timing=(piece, suffix))
            C.replace_file(made, b"replacement\n")
            refused = False
            try:
                C.output_path(root / "renders" / p.name, p, tracked_timing=(piece, suffix))
            except C.Fatal:
                refused = True
            verdict(f"D66 {suffix}: a committed clean file is replaced atomically, then a dirty rerun is refused",
                    p.read_bytes() == b"replacement\n" and refused and not p.with_name(f".{p.name}.partial").exists())
            git("add", str(p.relative_to(C.ROOT)))
            staged_refused = False
            try:
                C.output_path(p, p, tracked_timing=(piece, suffix))
            except C.Fatal:
                staged_refused = True
            verdict(f"D66 {suffix}: staged changes are protected too", staged_refused)
        untracked = write(C.path(C.TIMING) / "032-untracked.mouth.json", "untracked\n")
        def refuses(p, owner):
            try:
                C.output_path(p, p, tracked_timing=owner)
                return False
            except C.Fatal:
                return True
        verdict("D66 protects an untracked copy and an unrelated tracked output",
                refuses(untracked, ("032-untracked", "mouth.json")) and refuses(other, (piece, "mouth.json")))
        outside = root.parent / "outside-git"
        C.ROOT = outside
        p = write(C.path(C.TIMING) / f"{piece}.mouth.json", "outside\n")
        verdict("D66 refuses an existing timing copy outside a Git work tree", refuses(p, (piece, "mouth.json")))
        p.unlink()
        made = C.output_path(p, p, tracked_timing=(piece, "mouth.json"))
        C.replace_file(made, b"first write\n")
        verdict("D66 allows the first explicit -o as the ordinary output rule does", p.read_bytes() == b"first write\n")
    finally:
        C.ROOT = saved


def voice_register(piece: str, rows: list) -> str:
    """A segment register for the take fixtures: one [[segment]] per (id, take, file, status, archived)."""
    text = (f'[voiceover]\npiece = "{piece}"\nvoice_use = "voiceover"\nmodel_id = "eleven_v4"\n'
            'output_format = "mp3_44100_128"\nper_cue = false\n')
    for sid, take, file, status, archived in rows:
        text += (f'\n[[segment]]\nid = "{sid}"\nscript_lines = "1.1"\ntext = "The ferry is late again."\n'
                 f'request = "The ferry is late again."\ntake = {take}\nfile = "{file}"\ncharacters = 24\n'
                 f'pause_after = 0.3\nstatus = "{status}"\narchived = "{archived}"\n')
    return text


def test_takes(verdict, cli) -> None:
    """take add across both layouts (DESIGN D64, D65, Section 6.6): a take in the piece's takes/
    folder, a re-roll after a flat take an earlier release left and back, a mixed register, and the
    refusals (a voice trial, the piece's own folder beside takes/, another piece's takes/)."""
    gen = C.path(C.VO_GENERATED)
    piece = "003-fixture-mp3"   # its s01 holds a flat t1, named by test_repo's first take add
    reg = C.path(C.VOICEOVER) / f"{piece}.toml"
    write(reg, C.read_text(reg).replace('status = "generated"', 'status = "approved"')
          .replace('archived = ""', 'archived = "F0042"'))   # t1 heard, approved and archived
    takes = gen / piece / "takes"
    fresh = write(takes / "tts_The_f_20261005_090000.mp3", "fake re-roll")
    code, out = cli("take", "add", fresh, "--piece", piece, "--segment", "s01")
    seg = C.load_toml(reg)["segment"][0]
    verdict("take add names a take where it lies in the piece's takes/ folder, a re-roll after a flat take an "
            "earlier release left numbered t2, and resets status to generated and archived to empty (D64, D65, "
            "Section 6.6)",
            code == 0 and (takes / f"{piece}.s01.t2.mp3").is_file() and (gen / f"{piece}.s01.t1.mp3").is_file()
            and not fresh.exists() and seg["take"] == 2
            and seg["file"] == f"generated/{piece}/takes/{piece}.s01.t2.mp3"
            and seg["status"] == "generated" and seg["archived"] == "", out + C.read_text(reg))
    fresh = write(gen / "tts_The_f_20261005_090100.mp3", "fake flat re-roll")
    code, out = cli("take", "add", fresh, "--piece", piece, "--segment", "s01")
    seg = C.load_toml(reg)["segment"][0]
    verdict("take add still names a take flat in generated/ where it lies, numbered after the takes/ folder's "
            "t2, and says where new calls write (D65)",
            code == 0 and (gen / f"{piece}.s01.t3.mp3").is_file() and not (takes / f"{piece}.s01.t3.mp3").exists()
            and seg["take"] == 3 and seg["file"] == f"generated/{piece}.s01.t3.mp3"
            and f"{C.VO_GENERATED}/{piece}/takes/" in out, out)
    homes = (takes, gen)
    verdict("next_take numbers after the highest take in either layout and after the register's own take, "
            "per segment", A.next_take(homes, f"{piece}.s01") == 4 and A.next_take(homes, f"{piece}.s01", 7) == 8
            and A.next_take(homes, f"{piece}.s02") == 1 and A.next_take(takes, f"{piece}.s01") == 3,
            [A.next_take(homes, f"{piece}.s01"), A.next_take(homes, f"{piece}.s01", 7)])
    mixed = "006-fixture-mixed"
    write(gen / f"{mixed}.s01.t1.mp3", "fake flat take")
    # s02's t2 was rejected and archived, and its local copy is gone: only the register remembers it
    mreg = write(C.path(C.VOICEOVER) / f"{mixed}.toml", voice_register(mixed, [
        ("s01", 1, f"generated/{mixed}.s01.t1.mp3", "approved", "F0007"),
        ("s02", 2, f"generated/{mixed}/takes/{mixed}.s02.t2.mp3", "rejected", "F0008")]))
    fresh = write(gen / mixed / "takes" / "tts_Every_20261005_090200.mp3", "fake take")
    code, out = cli("take", "add", fresh, "--piece", mixed, "--segment", "s02")
    rows = C.load_toml(mreg)["segment"]
    verdict("a mixed register: take add writes s02's take in its takes/ folder, numbered after the register's "
            "own take where that take's local copy is gone (t3), and leaves s01's flat file, take, status and "
            "archived as they were (D65)",
            code == 0 and rows[0]["file"] == f"generated/{mixed}.s01.t1.mp3" and rows[0]["take"] == 1
            and rows[0]["status"] == "approved" and rows[0]["archived"] == "F0007" and rows[1]["take"] == 3
            and rows[1]["file"] == f"generated/{mixed}/takes/{mixed}.s02.t3.mp3" and rows[1]["status"] == "generated"
            and rows[1]["archived"] == "", out + C.read_text(mreg))
    # a flat raw-PCM t1 the register no longer records (restored from Git), then an MP3 re-roll in takes/
    lost = "007-fixture-restored"
    write(gen / f"{lost}.s01.t1.pcm", "fake flat pcm take")
    lreg = write(C.path(C.VOICEOVER) / f"{lost}.toml", voice_register(lost, [("s01", 0, "", "", "")]))
    fresh = write(gen / lost / "takes" / "tts_The_f_20261005_090250.mp3", "fake take")
    code, out = cli("take", "add", fresh, "--piece", lost, "--segment", "s01")
    seg = C.load_toml(lreg)["segment"][0]
    verdict("take add numbers a re-roll after every take of its segment in both layouts, by name, whatever the "
            "extension, where the register no longer records the flat one (t2 after a flat t1.pcm; D65)",
            code == 0 and seg["take"] == 2 and seg["file"] == f"generated/{lost}/takes/{lost}.s01.t2.mp3"
            and (gen / f"{lost}.s01.t1.pcm").is_file(), out + C.read_text(lreg))
    before, logged = C.read_text(reg), C.read_text(C.path(C.CREDITS_LOG))
    trial = write(gen / "voice-trials" / "warm-narrator" / "tts_Hello_20261005_090300.mp3", "fake trial")
    code, out = cli("take", "add", trial, "--piece", piece, "--segment", "s01")
    verdict("take add refuses a voice trial, which is never a take (exit 2: nothing renamed, no register or "
            "credits-log row; D21)", code == 2 and "never a take" in out and trial.is_file()
            and C.read_text(reg) == before and C.read_text(C.path(C.CREDITS_LOG)) == logged, out)
    scratch = write(gen / piece / "tts_The_f_20261005_090400.mp3", "fake")
    other = write(gen / "004-fixture-pcm" / "takes" / "tts_The_f_20261005_090500.mp3", "fake")
    code1, out1 = cli("take", "add", scratch, "--piece", piece, "--segment", "s01")
    code2, out2 = cli("take", "add", other, "--piece", piece, "--segment", "s01")
    verdict("take add refuses a file in the piece's own folder beside takes/, where scratch tracks sit, and one "
            "in another piece's takes/ (exit 2, nothing renamed)",
            code1 == 2 and code2 == 2 and scratch.is_file() and other.is_file() and f"{piece}/takes" in out1
            and C.read_text(reg) == before, out1 + out2)


WHERE_PIECE = "010-fixture-where"


def where_fixture(base: Path) -> tuple:
    """A piece's files in every layer and in its ignored per-piece folders, written under base:
    (the tracked or trackable paths where must print, the ignored files it must never name)."""
    p = WHERE_PIECE
    tracked = [f"scripts/src/pieces/{p}/brief.md", f"production/src/edits/{p}.toml",
               f"production/src/voiceover/{p}.toml", f"production/src/timing/{p}.words.json",
               f"production/src/timing/{p}.words-check.md", f"production/src/timing/{p}.mouth.json",
               f"production/src/scenes/{p}.cues.json", f"production/src/scenes/{p}.scene.py",
               f"publishing/src/posts/{p}.md"]
    ignored = [f"production/src/renders/{p}/{p}.master.mp4", f"production/src/renders/{p}/{p}.voice.wav",
               f"production/src/renders/{p}/timing/{p}.levels.json",
               f"production/src/renders/{p}/timing/{p}.words-check.md",
               f"production/src/renders/{p}.flat-extract.wav",
               f"production/src/voiceover/generated/{p}/takes/{p}.s01.t1.mp3",
               f"production/src/voiceover/generated/{p}/{p}.s01.scratch.wav",
               f"production/src/footage/raw/{p}.recording.wav"]
    text = {"words-check.md": "<!-- AUTHOR TO CONFIRM: the word 'Tharvel' -->\n",
            "scene.py": "# VERIFY: the walk's speed\n"}
    for rel in tracked:
        write(base / rel, next((t for end, t in text.items() if rel.endswith(end)), "{}\n"))
    for rel in ignored:
        write(base / rel, "<!-- VERIFY: never read -->\n")
    write(base / "production/src/timing/011-other.words.json", "{}\n")
    return tracked, ignored


def where_lines(out: str) -> tuple:
    """(the file lines, {folder: state}) of where's output."""
    files, folders, section = [], {}, "files"
    for line in out.splitlines():
        if line.startswith("ignored per-piece folders"):
            section = "folders"
        elif line.startswith("  ") and not line.strip().startswith("note:"):
            if section == "files":
                files.append(line.strip())
            else:
                name, state = line.split()[0], line.split()[-1]
                folders[name] = state
    return files, folders


def test_where(verdict, cli, root: Path, in_tree: bool) -> None:
    """where PIECE (DESIGN D50, D64): the piece's files, gathered as flags --piece gathers them, then
    its three ignored per-piece folders by name, each said to exist or not; never a file inside an
    output folder or the footage mirror, inside a Git work tree (in_tree: root is the self-test's
    repository, with its ignore rules) or outside one, where the plain list is filtered."""
    p = WHERE_PIECE
    tracked, ignored = where_fixture(root)
    code, out = cli("where", p)
    files, folders = where_lines(out)
    names = {Path(rel).name for rel in tracked}   # a working copy may share a tracked file's name
    leaked = [rel for rel in ignored if rel in out or (Path(rel).name in out and Path(rel).name not in names)]
    state = "inside a Git work tree" if in_tree else "outside a Git work tree"
    verdict(f"where lists the piece's tracked files across the layers, timing/ and scenes/ among them, and "
            f"names its ignored per-piece folders, existing or not, never listing what is inside them ({state})",
            code == 0 and sorted(files) == sorted(tracked) and not leaked and "011-other" not in out
            and folders == {f"{C.PROD_RENDERS}/{p}/": "exists", f"{C.VO_GENERATED}/{p}/": "exists",
                            f"{C.PUB_RENDERS}/{p}/": "absent"}
            and (in_tree or C.in_work_tree(root) or "not inside a Git work tree" in out),
            out + f"\nleaked: {leaked}")
    if not in_tree:
        return
    notes = write(root / f"scripts/src/pieces/{p}/ignored-notes.md", "<!-- VERIFY: never read -->\n")
    code, out = cli("where", p)
    verdict("where leaves out a file Git ignores in the piece's own folder (D50)",
            code == 0 and "ignored-notes" not in out and notes.is_file(), out)
    code, out = cli("flags", "--piece", p, "--strict")
    verdict("flags --piece gathers the piece's files in production/src/timing/ and production/src/scenes/, and "
            "never the working copies in its ignored timing/ folder (D50, D64)",
            code == 1 and "AUTHOR TO CONFIRM: 1" in out and "VERIFY: 1" in out
            and f"production/src/timing/{p}.words-check.md:1" in out
            and f"production/src/scenes/{p}.scene.py:1" in out and "never read" not in out, out)
    code1, out1 = cli("where", "012-no-such-piece")
    code2, out2 = cli("where", "Fixture")
    verdict("where refuses a piece with no folder and a name that is not a piece's (exit 2)",
            code1 == 2 and "no piece folder" in out1 and code2 == 2 and "not a piece name" in out2, out1 + out2)


def lavfi(*args) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + [str(a) for a in args], check=True)


def test_media(verdict, skip, cli, root: Path) -> None:
    work = Path(str(root) + "-media")
    work.mkdir()
    test_voice_join(verdict, cli)
    src = work / "camera clip.mp4"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=3", "-f", "lavfi", "-i",
          "sine=frequency=440:sample_rate=48000:duration=3", "-c:v", "libx264", "-preset", "ultrafast",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", src)
    code, out = cli("footage", "add", src, "--kind", "video", "--location", "Camera card 1")
    code2, out2 = cli("probe", C.path(C.RAW) / src.name, "--json")
    info = json.loads(out2) if code2 == 0 else {}
    verdict("footage add reads a video's duration; probe --json reports it", code == 0 and code2 == 0
            and abs(info.get("duration", 0) - 3.0) < 0.1, out + out2)
    # A master an earlier release left flat (DESIGN D65): a source like any other, whose outputs
    # still go to the piece's own folders (D64).
    master = C.path(C.PROD_RENDERS) / "001-fixture.master.mp4"
    shutil.copy2(src, master)
    pub = C.path(C.PUB_RENDERS) / "001-fixture"
    code, out = cli("cut", master, "--deliverable", "youtube.short", "--in", "00:00:00.500", "--out",
                    "00:00:02.500", "--cut", "c01")
    made = pub / "001-fixture--c01.youtube-short.mp4"
    verdict("cut makes youtube.short at 1080x1920, H.264, moov first, frame-accurate length, in the piece's "
            "folder of publishing/src/renders/ (D64)",
            code == 0 and made.is_file() and "verified" in out
            and not (C.path(C.PUB_RENDERS) / made.name).exists(), out)
    code, out = cli("cut", master, "--deliverable", "instagram.reel", "--in", "0", "--out", "3",
                    "--frame", "pad", "--cut", "c02")
    verdict("cut --frame pad fills 9:16 over a blurred copy", code == 0, out)
    code, out = cli("cut", master, "--deliverable", "tiktok.video", "--in", "0", "--out", "2")
    verdict("an over-long cut fails before it renders", code == 1 and "nothing rendered" in out, out)
    code, out = cli("cut", master, "--deliverable", "instagram.reel", "--in", "0", "--out", "2", "--cut", "c08")
    verdict("a cut under min_seconds fails before it renders", code == 1 and "min_seconds" in out
            and "nothing rendered" in out and not (pub / "001-fixture--c08.instagram-reel.mp4").exists(), out)
    with contextlib.redirect_stdout(io.StringIO()):
        found = V.verify(master, C.preset("youtube.short", quiet=True))
    verdict("a wrong aspect fails the deliverable's verification", any("640x360" in f for f in found), found)
    srt = write(C.path(C.CAPTIONS) / "001-fixture.en-GB.srt",
                K.srt_text([K.Cue(0.6, 1.9, ["The ferry is late again."]), K.Cue(2.0, 2.4, ["Late."])]))
    code, out = cli("cut", master, "--deliverable", "youtube.short", "--in", "00:00:00.500", "--out",
                    "00:00:02.500", "--cut", "c01", "--captions", srt)
    burned = pub / "001-fixture--c01.youtube-short.burned.mp4"
    verdict("cut --captions burns in the cutting pass (-copyts) with the caption font found",
            code == 0 and burned.is_file(), out)
    burned.unlink(missing_ok=True)
    code, out = cli("captions", "burn", made, srt, "--deliverable", "youtube.short")
    verdict("captions burn writes the ASS at the output size and keeps the font, its render named <stem>.burned "
            "in the piece's folder (D64)", code == 0 and burned.is_file(), out)
    good = C.read_text(C.path(C.TOKENS))
    write(C.path(C.TOKENS), good.replace("--caption-font:", "--caption-font: NoSuchBrandFont, "))
    code, out = cli("captions", "burn", made, srt, "--deliverable", "youtube.short", "-o",
                    C.path(C.PUB_RENDERS) / "burn-missing.mp4")
    write(C.path(C.TOKENS), good)
    verdict("captions burn reports a missing caption font", code == 1 and "fell back" in out, out)
    tangled = write(root / "tangled.srt", K.srt_text([K.Cue(0.2, 1.5, ["One."]), K.Cue(1.0, 1.8, ["Two."])]))
    code, out = cli("captions", "burn", made, tangled, "--deliverable", "youtube.short", "-o",
                    C.path(C.PUB_RENDERS) / "burn-tangled.mp4")
    verdict("captions burn refuses overlapping cues (exit 1, nothing rendered)", code == 1 and "cannot be burned"
            in out and not (C.path(C.PUB_RENDERS) / "burn-tangled.mp4").exists(), out)
    for target, want in (("social", -14.0), ("podcast", -16.0)):
        code, out = cli("loudness", "normalise", master, "--target", target)
        got = A.ebur128(C.path(C.PROD_RENDERS) / f"001-fixture.master.{target}.mp4")["I"]
        verdict(f"loudness normalise lands within 1 LU of {target} ({want:g})", code == 0 and abs(got - want) <= 1.0, out)
    code, out = cli("extract-audio", master, "--in", "00:00:01.000", "--out", "00:00:02.500")
    wav = C.path(C.PROD_RENDERS) / "001-fixture" / "001-fixture.master.00-00-01-000-00-00-02-500.wav"
    info = C.probe(wav) if wav.is_file() else {}
    a = C.streams(info, "audio")
    verdict("extract-audio writes mono 16 kHz WAV of the range, in the piece's folder of production/src/renders/ "
            "(D64)", code == 0 and a and a[0]["channels"] == 1
            and a[0]["sample_rate"] == "16000" and abs(C.duration(info) - 1.5) < 0.05, out)
    footage = C.path(C.RAW) / src.name   # a footage file's stem carries no piece key
    code, out = cli("extract-audio", footage)
    pinned = C.path(C.PROD_RENDERS) / "001-fixture" / "camera clip.wav"
    code2, out2 = cli("extract-audio", footage, "-o", pinned)
    verdict("extract-audio writes a stem with no piece key at the top of production/src/renders/, and -o wins "
            "(production/workflows/08-bring-in-a-recording/ passes the piece's folder; D64, ruling T5)",
            code == 0 and (C.path(C.PROD_RENDERS) / "camera clip.wav").is_file() and code2 == 0
            and pinned.is_file() and not (C.path(C.PROD_RENDERS) / "camera clip").exists(), out + out2)
    keyed = work / "001-fixture.room.wav"   # outside every output folder, its name keyed to a piece
    lavfi("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=3,volume=0.2", keyed)
    code, out = cli("loudness", "normalise", keyed, "--target", "social")
    verdict("loudness normalise writes a source from outside the output folders into its piece's folder of "
            "production/src/renders/ (D64)", code == 0
            and (C.path(C.PROD_RENDERS) / "001-fixture" / "001-fixture.room.social.wav").is_file(), out)
    code, out = cli("frame", master, "--at", "00:00:01.000")
    verdict("frame writes one PNG still, in the piece's folder", code == 0
            and (pub / "001-fixture.master.00-00-01-000.png").is_file(), out)
    still = work / "still.png"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=800x600:rate=1:duration=1", "-frames:v", "1", still)
    tone = work / "episode.wav"
    lavfi("-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=2", tone)
    code, out = cli("still-video", still, tone, "--deliverable", "youtube.long")
    code2, out2 = cli("frame", src, "--at", "00:00:01.000")
    top = C.path(C.PUB_RENDERS)
    verdict("still-video puts a still under audio at the deliverable's size; it, and frame, write a name with no "
            "piece key (episode.wav, camera clip.mp4) at the top of publishing/src/renders/ (D64)",
            code == 0 and (top / "episode.youtube-long.mp4").is_file() and code2 == 0
            and (top / "camera clip.00-00-01-000.png").is_file(), out + out2)
    code, out = cli("encode", master, "--deliverable", "podcast.apple_rss_audio")
    verdict("encode makes an audio deliverable at the podcast loudness, in the piece's folder",
            code == 0 and "podcast target" in out and (pub / "001-fixture.podcast-apple-rss-audio.m4a").is_file(), out)
    code, out = cli("cut", master, "--deliverable", "podcast.apple_rss_audio", "--in", "00:00:00.500",
                    "--out", "00:00:02.000", "--cut", "c03")
    clip = pub / "001-fixture--c03.podcast-apple-rss-audio.m4a"
    info = C.probe(clip) if clip.is_file() else {}
    verdict("cut makes an audio deliverable: trimmed, sound only, AAC",
            code == 0 and not C.streams(info, "video") and abs(C.duration(info) - 1.5) < 0.1, out)
    code, out = cli("cut", master, "--deliverable", "youtube.thumbnail", "--in", "0", "--out", "1")
    verdict("cut refuses an image deliverable (exit 2)", code == 2 and "card.py" in out, out)
    step = work / "step.wav"   # loud for 2 s, then 10 dB quieter for 3.6 s: a short programme ending low
    lavfi("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=2,volume=0.3", "-f", "lavfi", "-i",
          "sine=frequency=440:sample_rate=48000:duration=3.6,volume=0.1", "-filter_complex",
          "[0:a][1:a]concat=n=2:v=0:a=1", "-ac", "2", step)
    code, out = cli("loudness", "normalise", step, "--target", "social", "-o", C.path(C.PROD_RENDERS) / "step.social.wav")
    got = A.ebur128(C.path(C.PROD_RENDERS) / "step.social.wav")["I"] if code != 2 else float("nan")
    verdict("loudness normalise of a short programme that ends quiet lands on the target (ebur128 measures "
            "it, never loudnorm's end-weighted reading)", code == 0 and abs(got - (-14.0)) <= 0.5, f"{got}\n{out}")
    # encode and still-video put a downmix before the meter, and ffmpeg then prints loudnorm's JSON
    # before ebur128's Summary: both must still be read, or the end-weighted reading drives the pass.
    for argv, made, want in (
            (("encode", step, "--deliverable", "podcast.apple_rss_audio"), "step.encode.m4a", -16.0),
            (("still-video", still, step, "--deliverable", "youtube.long"), "step.still.mp4", -14.0)):
        dest = C.path(C.PUB_RENDERS) / made
        code, out = cli(*argv, "-o", dest)
        got = A.ebur128(dest)["I"] if dest.is_file() else float("nan")
        verdict(f"{argv[0]} of a programme that ends quiet lands within 0.5 LU of {want:g} (a downmix before "
                "the meter)", code == 0 and abs(got - want) <= 0.5, f"{got}\n{out}")
    silent = work / "no sound.mp4"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=320x180:rate=25:duration=1", "-c:v", "libx264", "-preset",
          "ultrafast", "-pix_fmt", "yuv420p", silent)
    code, out = cli("loudness", "measure", silent)
    verdict("loudness measure names a file with no sound (exit 2), never ffmpeg's raw log",
            code == 2 and "has no audio stream" in out and "Stream map" not in out, out)
    portrait = work / "portrait.mp4"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=1", "-f", "lavfi", "-i",
          "sine=frequency=440:sample_rate=48000:duration=1", "-c:v", "libx264", "-preset", "ultrafast",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", portrait)
    code, out = cli("encode", portrait, "--deliverable", "youtube.long", "-o", C.path(C.PUB_RENDERS) / "p.mp4")
    verdict("encode refuses a picture of another shape without --frame (exit 2), naming crop and pad",
            code == 2 and "--frame crop" in out and "--frame pad" in out
            and not (C.path(C.PUB_RENDERS) / "p.mp4").exists(), out)
    code, out = cli("encode", portrait, "--deliverable", "youtube.long", "--frame", "pad", "-o",
                    C.path(C.PUB_RENDERS) / "p.mp4")
    verdict("encode --frame pad fills the other shape", code == 0 and "1920x1080" in out, out)
    test_assemble(verdict, skip, cli, root, work)
    test_stills(verdict, cli)
    test_overlays(verdict, cli)
    test_align(verdict, cli, root, work)
    test_audiobook(verdict, cli, root, work)
    test_screen(verdict, skip, cli, work)
    test_held_sound(verdict, cli, work)
    test_source_sound(verdict, cli, work)


def test_voice_join(verdict, cli) -> None:
    import wave
    piece = "033-voice-join"
    files = [C.path(C.VO_GENERATED) / f"{piece}.s01.t1.pcm",
             C.path(C.VO_GENERATED) / piece / "takes" / f"{piece}.s02.t1.pcm"]
    for f, duration, frequency in zip(files, (0.2, 0.17), (440, 880)):
        f.parent.mkdir(parents=True, exist_ok=True)
        lavfi("-f", "lavfi", "-i", f"sine=frequency={frequency}:sample_rate=8000:duration={duration}",
              "-c:a", "pcm_s16le", "-f", "s16le", f)
    register = C.path(C.VOICEOVER) / f"{piece}.toml"
    reg = voice_register(piece, [("s01", 1, f"generated/{files[0].name}", "approved", "F0001"),
                                 ("s02", 1, f"generated/{piece}/takes/{files[1].name}", "approved", "F0002")])
    reg = reg.replace('output_format = "mp3_44100_128"', 'output_format = "pcm_8000"')
    # Different pauses for each segment, the final pause included.
    reg = reg.replace("pause_after = 0.3", "pause_after = 0.16", 1)
    at = reg.rfind("pause_after = 0.3")
    reg = reg[:at] + reg[at:].replace("pause_after = 0.3", "pause_after = 0.03", 1)
    write(register, reg)
    code, out = cli("voice", "join", piece)
    voice = A.joined_voice(piece)
    with wave.open(str(voice), "rb") as wav:
        data = wav.readframes(wav.getnframes())
        facts = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes())
    expected = files[0].read_bytes() + bytes(1280 * 2) + files[1].read_bytes() + bytes(240 * 2)
    verdict("voice join reads flat and per-piece takes by their register paths, in order, with exact "
            "silence after both, as mono 16-bit WAV at the register's rate",
            code == 0 and facts == (1, 2, 8000, 4480) and data == expected, out + str(facts))
    code, out = cli("levels", piece)
    levels = C.piece_folder(C.PROD_RENDERS, piece, "timing") / f"{piece}.levels.json"
    result = json.loads(levels.read_text())
    windows = result["windows"]
    verdict("levels defaults to 0.1 s windows, floors digital silence, writes finite JSON only to the "
            "working timing folder, and ends its final short window at the voice duration",
            code == 0 and result["piece"] == piece and result["sample_rate"] == 8000
            and result["window_seconds"] == 0.1 and len(windows) == 6
            and windows[2]["rms_dbfs"] == -120 and abs(windows[-1]["start"] - 0.5) < 1e-9
            and abs(windows[-1]["end"] - 0.56) < 1e-9
            and all(math.isfinite(w["rms_dbfs"]) for w in windows)
            and not (C.path(C.TIMING) / levels.name).exists(), out + str(result))
    code, out = cli("levels", piece, "--window", "0.2")
    verdict("levels accepts a different window while ACX keeps its 0.5 s default",
            code == 0 and len(json.loads(levels.read_text())["windows"]) == 3 and A.WINDOW == 0.5, out)
    for value in ("0", "-0.1", "nan", "inf"):
        before = levels.read_bytes()
        code, out = cli("levels", piece, "--window", value)
        verdict(f"levels refuses invalid window {value} without changing its output",
                code == 2 and levels.read_bytes() == before, out)
    code, out = cli("levels", piece, "-o", "elsewhere.json")
    verdict("levels has no tracked-output option", code == 2, out)
    code, out = cli("levels", "034-missing-voice")
    verdict("levels names voice join when its named joined voice is missing",
            code == 2 and "voice join 034-missing-voice" in out, out)
    write(register, reg.replace('status = "approved"', 'status = "generated"', 1))
    target = voice.with_name("unapproved.wav")
    code, out = cli("voice", "join", piece, "-o", target)
    verdict("voice join refuses each unapproved segment before writing (exit 1)",
            code == 1 and "s01" in out and not target.exists(), out)
    write(register, reg)
    target = voice.with_name("chosen-output")
    code, out = cli("voice", "join", piece, "-o", target)
    verdict("voice join honours an explicit output path without a filename extension, still as WAV",
            code == 0 and target.is_file() and C.probe(target).get("format", {}).get("format_name") == "wav", out)


def test_assemble(verdict, skip, cli, root: Path, work: Path) -> None:
    music = work / "bed.wav"
    lavfi("-f", "lavfi", "-i", "sine=frequency=660:sample_rate=48000:duration=8", "-af", "volume=0.3", music)
    code, out = cli("footage", "add", music, "--kind", "music", "--location", "Library A", "--rights", "RR0001")
    verdict("a music bed is logged as footage", code == 0 and f"logged {kind_id('music')}" in out, out)
    talk = work / "talk.wav"
    lavfi("-f", "lavfi", "-i", "sine=frequency=200:sample_rate=48000:duration=3", talk)
    cli("footage", "add", talk, "--kind", "audio", "--location", "Recorder B")
    # a mixed register (DESIGN D65): s01's take flat in generated/, as an earlier release left it, and
    # s02's in the piece's generated/<piece>/takes/ (D64); every reader opens the path its row names
    gen = C.path(C.VO_GENERATED)
    takes = gen / "005-assembly" / "takes"
    takes.mkdir(parents=True, exist_ok=True)
    lavfi("-f", "lavfi", "-i", "sine=frequency=250:sample_rate=44100:duration=4", "-c:a", "libmp3lame",
          "-b:a", "128k", gen / "005-assembly.s01.t1.mp3")
    lavfi("-f", "lavfi", "-i", "sine=frequency=300:sample_rate=22050:duration=5", "-f", "s16le", "-ac", "1",
          takes / "005-assembly.s02.t1.pcm")
    write(C.path(C.VOICEOVER) / "005-assembly.toml", """[voiceover]
piece = "005-assembly"
voice_use = "voiceover"
model_id = "eleven_v4"
output_format = "pcm_22050"
per_cue = false

[[segment]]
id = "s01"
script_lines = "1.1-1.2"
text = "The ferry is late again. Every crossing waits for the tide."
request = "The ferry is late again. Every crossing waits for the tide."
take = 1
file = "generated/005-assembly.s01.t1.mp3"
characters = 59
pause_after = 0.4
status = "approved"
archived = "F0009"

[[segment]]
id = "s02"
script_lines = "2.1-2.2"
text = "So the timetable is a promise. The sea never signed it, and nobody asked."
request = "So the timetable is a promise. The sea never signed it, and nobody asked."
take = 1
file = "generated/005-assembly/takes/005-assembly.s02.t1.pcm"
characters = 73
pause_after = 0.3
status = "approved"
archived = ""
""")
    w, h = 640, 360
    html = write(C.path(C.CARDS) / "005-assembly.title.html", "<!doctype html><html lang=\"en-GB\"></html>\n")
    endcard = write(C.path(C.CARDS) / "005-assembly.end.html", "<!doctype html><html lang=\"en-GB\"></html>\n")
    # the card PNGs assemble would render, already fresh in the piece's cards/ folder: the title as a
    # clip, the end card as an overlay, whose render is named .transparent (D47, D64)
    title_png, end_png = V.card_name(html, w, h, False), V.card_name(endcard, w, h, True)
    title_png.parent.mkdir(parents=True, exist_ok=True)
    lavfi("-f", "lavfi", "-i", f"color=c=0x1c232b:s={w}x{h}", "-frames:v", "1", title_png)
    lavfi("-f", "lavfi", "-i", f"color=c=white@0.5:s={w}x{h},format=rgba", "-frames:v", "1", end_png)
    C.path(C.ASSETS).mkdir(parents=True, exist_ok=True)
    shutil.copy2(work / "still.png", C.path(C.ASSETS) / "harbour.png")
    video, bed = kind_id("video"), kind_id("music")
    edl = write(C.path(C.EDITS) / "005-assembly.toml", f"""[edit]
piece = "005-assembly"
version = 1
size = "{w}x{h}"
audio_rate = 48000
loudness = "social"

[[clip]]
id = "c01"
source = "{video}"
in = "00:00:00.500"
out = "00:00:02.500"
frame = "crop"

[[clip]]
id = "c02"
source = "production/src/assets/harbour.png"
seconds = 3.0
motion = "push-in"
transition = "fade"
transition_seconds = 0.5

[[clip]]
id = "c03"
colour = "#101418"
seconds = 1.0

[[clip]]
id = "c04"
source = "production/src/cards/005-assembly.title.html"
seconds = 1.5
transition = "fade"
transition_seconds = 0.4

[[overlay]]
source = "production/src/cards/005-assembly.end.html"
at = "00:00:01.000"
until = "00:00:02.000"

[[audio]]
source = "vo:005-assembly"
at = "00:00:00.200"
role = "voice"

[[audio]]
source = "{bed}"
at = "00:00:00.000"
in = "00:00:01.000"
out = "00:00:07.000"
gain_db = -6.0
fade_in = 0.5
fade_out = 1.0
role = "music"
duck = true
""")
    total = 2.0 + 3.0 - 0.5 + 1.0 + 1.5 - 0.4
    code, out = cli("assemble", edl)
    master = C.path(C.PROD_RENDERS) / "005-assembly" / "005-assembly.master.mp4"
    info = C.probe(master) if master.is_file() else {}
    verdict("assemble: a clip, a push-in still with a fade, a colour clip, a card, an overlay, a mixed voice "
            "register (one take flat, one in its piece's takes/, each read by its row's file, D65) and a "
            "ducked, trimmed, faded bed, the master in its piece's folder (D64)",
            code == 0 and abs(C.duration(info) - total) < 0.1, out)
    if master.is_file():
        got = A.ebur128(master)["I"]
        verdict("assemble lands the master within 1 LU of the social target", abs(got - (-14.0)) <= 1.0, got)
    code, out = cli("captions", "from-segments", C.path(C.VOICEOVER) / "005-assembly.toml", "--deliverable",
                    "youtube.long", "--offset", "00:00:00.200")
    timed = C.path(C.PUB_RENDERS) / "005-assembly" / "005-assembly.youtube-long.en-GB.srt"
    cues = K.read_srt(timed) if timed.is_file() else []
    d1 = K.segment_duration(C.path(C.VO_GENERATED) / "005-assembly.s01.t1.mp3")
    starts = [round(c.start, 3) for c in cues]
    join = round(0.2 + d1 + 0.4, 3)
    verdict("from-segments: several cues per segment, each segment's first cue exactly on its join, written to "
            "the piece's folder in publishing/src/renders/ (D64)",
            code == 0 and len(cues) >= 4 and starts[0] == 0.2 and join in starts
            and abs(cues[-1].end - (join + K.segment_duration(takes / "005-assembly.s02.t1.pcm"))) < 0.002,
            out + str(starts))
    rec = write(C.path(C.CAPTIONS) / "005-assembly.F0001.en-GB.srt",
                K.srt_text([K.Cue(0.6, 1.8, ["On the recording."]), K.Cue(3.0, 3.8, ["Outside the clip."])]))
    code, out = cli("captions", "retime", rec, "--edl", edl, "--source", video,
                    "-o", C.path(C.PUB_RENDERS) / "005-retimed.srt")
    moved = K.read_srt(C.path(C.PUB_RENDERS) / "005-retimed.srt")
    verdict("retime --edl maps recording time through the clip and drops the rest",
            code == 0 and len(moved) == 1 and abs(moved[0].start - 0.1) < 1e-6, K.srt_text(moved))
    register = C.path(C.VOICEOVER) / "005-assembly.toml"
    held = C.read_text(register)
    code, out = cli("footage", "add", takes / "005-assembly.s02.t1.pcm", "--kind", "generated",
                    "--location", "Archive drive A")
    seg = C.load_toml(register)["segment"][1]
    verdict("footage add --kind generated writes the take's F ID into its segment's archived, the take in "
            "its piece's takes/ folder (D64)",
            code == 0 and re.fullmatch(r"F\d{4}", seg.get("archived", "")) is not None
            and f'wrote archived = "{seg.get("archived")}"' in out, out + C.read_text(register))
    write(register, held.replace('status = "approved"\narchived = ""', 'status = "generated"\narchived = ""'))
    code, out = cli("assemble", edl, "-o", C.path(C.PROD_RENDERS) / "005-unapproved.mp4")
    write(register, held)
    verdict("assemble refuses a voice track that would skip a segment not approved (exit 1, nothing rendered)",
            code == 1 and "s02 (generated: line 2.1-2.2)" in out
            and not (C.path(C.PROD_RENDERS) / "005-unapproved.mp4").exists(), out)
    for body, label in (('out = "00:00:02.500"', 'out = "00:00:09.500"'), ('role = "music"\nduck = true', 'role = "effect"\nduck = true')):
        bad = write(C.path(C.EDITS) / "005-bad.toml", C.read_text(edl).replace(body, label))
        code, out = cli("assemble", bad, "-o", C.path(C.PROD_RENDERS) / "005-bad.mp4")
        what = "a clip whose out is past its source's end" if "out" in body else "duck on a track that is not music"
        verdict(f"assemble refuses {what} (exit 2)", code == 2 and ("past the end" in out if "out" in body
                                                                   else "duck = true" in out), out)
    # A recording cut at an edit: a cue across the cut is placed once (or dropped), never doubled,
    # and captions check against the transcript names what the edit left out as a note.
    talk_id = kind_id("video")
    split = write(C.path(C.EDITS) / "012-talk.toml", f"""[edit]
piece = "012-talk"
size = "640x360"
loudness = "none"

[[clip]]
id = "c01"
source = "{talk_id}"
in = "00:00:00.000"
out = "00:00:01.200"

[[clip]]
id = "c02"
source = "{talk_id}"
in = "00:00:02.000"
out = "00:00:03.000"
transition = "fade"
transition_seconds = 0.2
""")
    write(root / C.PIECES / "012-talk" / "transcript.md", f"""---
piece: 012-talk
source: {talk_id}
made: by hand
approved: ""
---

# Talk — transcript

## 1. Opening (at 00:00:00.000)

HOST: The ferry is late.

## 2. A tangent (at 00:00:01.100)

HOST: Rope pier cargo quay.

## 3. Close (at 00:00:02.000)

HOST: We go out.
""")
    rec = write(C.path(C.CAPTIONS) / f"012-talk.{talk_id}.en-GB.srt",
                K.srt_text([K.Cue(0.0, 1.0, ["The ferry is late."]), K.Cue(1.1, 2.3, ["Rope pier cargo quay."]),
                            K.Cue(2.2, 3.0, ["We go out."])]))
    code, out, err = cli_split("captions", "retime", rec, "--edl", split, "--source", talk_id)
    placed = K.parse_srt(out) if code == 0 else []
    verdict("retime --edl places a cue across an edit once at most, never doubled, and reports the counts",
            code == 0 and [c.text for c in placed].count("Rope pier cargo quay.") <= 1
            and "written from 3" in err and "dropped" in err, out + err)
    master = write(C.path(C.CAPTIONS) / "012-talk.en-GB.srt",
                   K.srt_text([K.Cue(0.0, 1.5, ["The ferry is late."]), K.Cue(1.6, 2.7, ["We go out."])]))
    code, out = cli("captions", "check", master, "--script", root / C.PIECES / "012-talk" / "transcript.md")
    verdict("captions check of an edited recorded master notes the words the edit removed, and passes",
            code == 0 and "note: words of the transcript the edit leaves out" in out and "rope pier" in out, out)
    phone = work / "phone.mp4"   # a variable-rate recording: five frames of every seven kept
    lavfi("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=2", "-vf", "select='lt(mod(n\\,7)\\,5)'",
          "-fps_mode", "vfr", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", phone)
    code, out = cli("footage", "add", phone, "--kind", "video", "--location", "Phone")
    vfr = write(C.path(C.EDITS) / "013-vfr.toml", f"""[edit]
piece = "013-vfr"
size = "640x360"
loudness = "none"

[[clip]]
id = "c01"
source = "{logged_id(out)}"
in = "00:00:00.000"
out = "00:00:01.500"

[[clip]]
id = "c02"
source = "{talk_id}"
in = "00:00:00.000"
out = "00:00:01.000"
""")
    code, out = cli("assemble", vfr)
    made = C.path(C.PROD_RENDERS) / "013-vfr" / "013-vfr.master.mp4"
    v = C.streams(C.probe(made), "video") if made.is_file() else []
    verdict("assemble snaps a variable-rate first clip to a standard rate, and says so",
            code == 0 and v and V.is_standard(C.rate(v[0].get("avg_frame_rate"))) and "not a standard rate" in out,
            out + str(v[0].get("avg_frame_rate") if v else ""))
    with contextlib.redirect_stdout(io.StringIO()):
        found = V.verify(phone, C.preset("youtube.long", quiet=True))
    verdict("a rate outside the deliverable's fps_allowed fails its verification",
            any("fps_allowed" in f for f in found), found)
    lost = write(C.path(C.CAPTIONS) / "012-talk.lost.en-GB.srt", K.srt_text([K.Cue(1.1, 2.1, ["We go out."])]))
    code, out = cli("captions", "check", lost, "--script", root / C.PIECES / "012-talk" / "transcript.md")
    verdict("captions check still fails words missing from a stretch the edit keeps",
            code == 1 and "the ferry is late" in out, out)
    if shutil.which("uv") and any(R.playwright_cache().glob(f"chromium*-{R.PLAYWRIGHT_REVISION}")):
        real = write(C.path(C.CARDS) / "005-assembly.title.html", CARD_HTML)
        write(C.path(C.TOKENS), C.read_text(C.path(C.TOKENS)))
        os.utime(real, None)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                png = V.card_png(real, w, h, transparent=False)
            verdict("a stale card is rendered again with card.py, into its piece's cards/ folder", png.is_file()
                    and png.stat().st_mtime >= real.stat().st_mtime
                    and png.parent == C.path(C.PROD_RENDERS) / "005-assembly" / "cards", png)
        except (C.Fatal, C.Finding) as err:
            verdict("a stale card is rendered again with card.py, into its piece's cards/ folder", False, err)
    else:
        skip("a stale card is rendered again with card.py, into its piece's cards/ folder",
             "uv or Playwright's Chromium is not installed")
    audio_edl = write(C.path(C.EDITS) / "006-podcast.toml", f"""[edit]
piece = "006-podcast"
size = ""
audio_rate = 48000
loudness = "podcast"

[[clip]]
id = "c01"
source = "{kind_id('audio')}"
in = "00:00:00.500"
out = "00:00:01.500"

[[clip]]
id = "c02"
source = "{kind_id('audio')}"
in = "00:00:02.000"
out = "00:00:03.000"
transition = "fade"
transition_seconds = 0.3

[[audio]]
source = "{bed}"
at = "00:00:00.000"
gain_db = -12.0
fade_in = 0.5
fade_out = 0.5
role = "music"
""")
    code, out = cli("assemble", audio_edl)
    wav = C.path(C.PROD_RENDERS) / "006-podcast" / "006-podcast.master.wav"
    info = C.probe(wav) if wav.is_file() else {}
    verdict("an audio master (size = \"\") is sound only, cut from clips under a faded bed, in its piece's folder",
            code == 0 and not C.streams(info, "video") and abs(C.duration(info) - (1.0 + 1.0 - 0.3)) < 0.05, out)
    bad = write(C.path(C.EDITS) / "007-missing.toml", '[edit]\npiece = "007-missing"\nsize = "640x360"\n\n'
                '[[clip]]\nid = "c01"\nsource = "F0099"\nin = "0"\nout = "2"\n')
    code, out = cli("assemble", bad)
    verdict("assemble names footage the project does not have (exit 2)", code == 2 and "F0099" in out, out)


def test_stills(verdict, cli) -> None:
    """A long list of stills: one input for a run of plain stills and colours, every boundary on the
    frame its running total rounds to (a still of 0.16 s at 30 fps holds 5, 5, 4, 5, 5 frames), a
    run split only where a push-in, a fade or a video comes between, and never by its sources'
    sizes, decoders, pixel formats or orientations, each image framed once before the render. Each
    still is a flat colour, so every frame of the master says which it shows."""
    stills = C.path(C.ASSETS) / "stills"
    stills.mkdir(parents=True, exist_ok=True)
    lavfi("-f", "lavfi", "-i", "color=c=black:s=320x180:r=1,format=rgb24,geq=r='10+6*N':g='245-6*N':"
          "b='60+120*mod(N,2)'", "-frames:v", "40", stills / "s%03d.png")
    (stills / "s007.png").rename(stills / "harbour's edge 07.png")   # a quote and a space in an ffconcat line
    colours = [(10 + 6 * k, 245 - 6 * k, 60 + 120 * (k % 2)) for k in range(40)]
    names = [f"s{k + 1:03d}.png" if k != 6 else "harbour's edge 07.png" for k in range(40)]
    edl = write(C.path(C.EDITS) / "014-stills.toml", '[edit]\npiece = "014-stills"\nsize = "320x180"\n'
                'loudness = "none"\n' + "".join(f'\n[[clip]]\nsource = "production/src/assets/stills/{n}"\n'
                                                 "seconds = 0.16\n" for n in names))
    code, out, stage = spied_assemble(cli, edl)
    master = C.path(C.PROD_RENDERS) / "014-stills" / "014-stills.master.mp4"
    seen = frame_colours(master) if code == 0 and master.is_file() else []
    bounds = [(48 * k + 5) // 10 for k in range(41)]   # round(0.16 k x 30), half up
    want = [k for k in range(40) for _ in range(bounds[k + 1] - bounds[k])]
    got = [min(range(40), key=lambda k: sum((a - b) ** 2 for a, b in zip(rgb, colours[k]))) for rgb in seen]
    wrong = next((f for f, (a, b) in enumerate(zip(got, want)) if a != b), None)
    verdict("assemble: 40 stills of 0.16 s at 30 fps are exactly 192 frames (6.400 s), each still on the frames "
            "its running total rounds to (5, 5, 4, 5, 5...), the last one whole",
            len(seen) == 192 and got == want and abs(C.duration(C.probe(master)) - 6.4) < 0.0005,
            f"{len(seen)} frames; first wrong frame {wrong}: still {got[wrong] + 1 if wrong is not None else '-'} "
            f"where {want[wrong] + 1 if wrong is not None else '-'} was due\n{out}")
    lists = stage.get("lists", [])
    lines = lists[0].splitlines() if len(lists) == 1 else []
    files = [line for line in lines if line.startswith("file ")]
    held = [round(float(line.split()[1]) * 1e6) for line in lines if line.startswith("duration ")]
    verdict("assemble reads a run of plain stills through one ffconcat input, never one looped input each "
            "(each still framed once, a quote in its name too; frame-exact durations adding up to 6.400 s; the "
            "last image named twice)",
            stage.get("inputs") == 1 and stage.get("loops") == 0 and stage.get("framed") == 40 and len(files) == 41
            and files[-1] == files[-2] and len(held) == 40 and sum(held) == 6_400_000
            and all("/framed-" in f.replace("\\", "/") for f in files), f"{stage}\n{out}")
    flat = {"a": "2050c0", "b": "e0a020", "c": "20c040", "d": "8020e0"}
    for name, hexa in flat.items():
        lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s=320x180", "-frames:v", "1", stills / f"mix-{name}.png")
    for name, hexa in (("j1", "30a0dc"), ("j2", "e0c828")):
        lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s=320x180", "-frames:v", "1", stills / f"mix-{name}.jpg")
    exif_turned(stills / "mix-j2.jpg")
    src = "source = \"production/src/assets/stills/mix-{}\"\n"
    edl = write(C.path(C.EDITS) / "015-mixed.toml", '[edit]\npiece = "015-mixed"\nsize = "320x180"\n'
                'loudness = "none"\n\n[[clip]]\n' + src.format("a.png") + 'seconds = 0.37\n\n[[clip]]\n'
                'colour = "#c03050"\nseconds = 0.25\n\n[[clip]]\n' + src.format("b.png") + 'seconds = 0.52\n'
                'motion = "push-in"\n\n[[clip]]\n' + src.format("c.png") + 'seconds = 0.45\ntransition = "fade"\n'
                'transition_seconds = 0.2\n\n[[clip]]\n' + src.format("d.png") + 'seconds = 0.17\n\n[[clip]]\n'
                f'source = "{kind_id("video")}"\nin = "00:00:00.500"\nout = "00:00:00.900"\n\n[[clip]]\n'
                + src.format("j1.jpg") + 'seconds = 0.2\nframe = "crop"\n\n[[clip]]\n' + src.format("j2.jpg")
                + 'seconds = 0.2\nframe = "crop"\n')
    code, out, stage = spied_assemble(cli, edl)
    master = C.path(C.PROD_RENDERS) / "015-mixed" / "015-mixed.master.mp4"
    seen = frame_colours(master) if code == 0 and master.is_file() else []
    # Ends at 0.37, 0.62, 1.14, 1.39 (from 0.94: a 0.2 s fade), 1.56, 1.96, 2.16, 2.36 s: frames 11, 19, 34, 42
    # (from 28), 47, 59, 65 and 71. Per-clip rounding (0.37 s as 12 frames) puts the colour on frame 12.
    spans = [(0, 11, "2050c0"), (11, 19, "c03050"), (34, 42, "20c040"), (42, 47, "8020e0"), (59, 65, "30a0dc"),
             (65, 71, "e0c828")]
    off = [(f, seen[f]) for a, b, hexa in spans for f in range(a, b) if f < len(seen) and max(
        abs(x - y) for x, y in zip(seen[f], bytes.fromhex(hexa))) > 12]
    counts = [sum(line.startswith("duration ") for line in x.splitlines()) for x in stage.get("lists", [])]
    verdict("assemble: a still, a colour, a push-in, a fade into two stills, a video and two JPEGs (one turned by "
            "EXIF) are 71 frames, each clip on its cumulative boundaries, plain stills and colours split into runs "
            "only where a push-in, a fade or a video comes between them, never by decoder or orientation",
            len(seen) == 71 and not off and counts == [2, 2, 2] and stage.get("loops") == 1,
            f"{len(seen)} frames; off: {off[:6]}; runs {counts}; looped {stage.get('loops')}\n{out}")
    test_still_sources(verdict, cli, stills)


def test_still_sources(verdict, cli, stills: Path) -> None:
    """Stills that ffmpeg decodes unalike, one after another with no push-in or fade between them:
    sizes, decoders (PNG, JPEG, GIF), pixel formats (rgb24, 16-bit, grey), an EXIF orientation,
    every frame mode, and a colour. Each was its own input for the whole render before every image
    was framed first (64 stills of two sizes peaked at 2.4 GB, 213 passed 6 GB); now they are one
    input, each image framed once (the first, named twice, is framed once), and every frame shows
    the clip due on it. Each clip is 0.2 s, six frames at 30 fps; a 16x16 patch at the frame's
    centre is the source's own colour under every frame mode."""
    plan = [("a.png", "320x180", "2050c0", "fit", []), ("b.jpg", "400x180", "e0a020", "crop", ["-q:v", "2"]),
            ("c.png", "320x200", "20c040", "pad", []), ("", "", "8020e0", "", []),
            ("e.jpg", "320x180", "30a0dc", "fit", ["-q:v", "2"]), ("f.gif", "160x90", "c03050", "fit", []),
            ("a.png", "", "2050c0", "fit", []), ("g.png", "320x180", "a0c8e0", "fit", ["-pix_fmt", "rgb48be"]),
            ("h.png", "320x180", "808080", "crop", ["-pix_fmt", "gray"])]
    body = '[edit]\npiece = "018-sources"\nsize = "320x180"\nloudness = "none"\n'
    for name, size, hexa, frame, extra in plan:
        if not name:
            body += f'\n[[clip]]\ncolour = "#{hexa}"\nseconds = 0.2\n'
            continue
        p = stills / f"src-{name}"
        if size and name.endswith(".gif"):   # a palette of its own, so the flat colour stays exact
            lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s={size}:r=1:d=1", "-vf",
                  "split[a][b];[a]palettegen[p];[b][p]paletteuse", "-frames:v", "1", p)
        elif size:
            lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s={size}", "-frames:v", "1", *extra, p)
        if name == "e.jpg" and size:
            exif_turned(p)   # stands 180x320, a portrait, under fit
        body += f'\n[[clip]]\nsource = "production/src/assets/stills/src-{name}"\nseconds = 0.2\nframe = "{frame}"\n'
    edl = write(C.path(C.EDITS) / "018-sources.toml", body)
    code, out, stage = spied_assemble(cli, edl)
    master = C.path(C.PROD_RENDERS) / "018-sources" / "018-sources.master.mp4"
    seen = frame_colours(master, "16:16:152:82") if code == 0 and master.is_file() else []
    off = [(f, seen[f]) for f in range(len(seen)) if f // 6 < len(plan) and max(
        abs(x - y) for x, y in zip(seen[f], bytes.fromhex(plan[f // 6][2]))) > 12]
    lists = stage.get("lists", [])
    verdict("assemble reads stills of other sizes, decoders, pixel formats and orientations, and a colour, "
            "through one ffconcat input when nothing comes between them, never one input each, every image "
            "framed once and every frame showing its clip (54 frames)",
            code == 0 and len(seen) == 54 and not off and stage.get("inputs") == 1 and stage.get("loops") == 0
            and len(lists) == 1 and sum(line.startswith("duration ") for line in lists[0].splitlines()) == 9
            and stage.get("framed") == 8, f"{len(seen)} frames; off: {off[:6]}; {stage}\n{out}")


def test_overlays(verdict, cli) -> None:
    """[[overlay]] on the master's frames: from the frame its at rounds to, up to and not including
    the frame its until rounds to, each rounded as a clip's boundary is (half up, from the running
    total). Flat clips under two opaque boxes, one in each half of the frame, so every frame says
    which clip and which overlay it shows. At 30 fps the clips end on frames 2, 5 (0.05 + 0.1 s is
    4.5 frames, half up), 11 (0.37 s, frame 11 shown at 0.3667 s), 19 and 25; the left box is timed
    to the third clip (00:00:00.150 to .370) and the right box to the fourth (.370 to .620)."""
    folder = C.path(C.ASSETS) / "overlays"
    folder.mkdir(parents=True, exist_ok=True)
    for name, hexa in (("a", "2050c0"), ("b", "e0a020"), ("e", "30a0dc")):
        lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s=64x36", "-frames:v", "1", folder / f"{name}.png")
    for name, x, hexa in (("left", 0, "f0f0f0"), ("right", 32, "101010")):
        lavfi("-f", "lavfi", "-i", f"color=c=black@0.0:s=64x36,format=rgba,drawbox=x={x}:y=0:w=32:h=36:"
              f"color=0x{hexa}@1.0:t=fill:replace=1", "-frames:v", "1", folder / f"box-{name}.png")
    src = 'source = "production/src/assets/overlays/{}"\n'
    text = ('[edit]\npiece = "016-overlays"\nsize = "64x36"\nloudness = "none"\n\n[[clip]]\n' + src.format("a.png")
            + 'seconds = 0.05\n\n[[clip]]\n' + src.format("b.png") + 'seconds = 0.1\n\n[[clip]]\n'
            'colour = "#20c040"\nseconds = 0.22\n\n[[clip]]\ncolour = "#8020e0"\nseconds = 0.25\n\n[[clip]]\n'
            + src.format("e.png") + 'seconds = 0.2\n\n[[overlay]]\n' + src.format("box-left.png")
            + 'at = "00:00:00.150"\nuntil = "00:00:00.370"\n\n[[overlay]]\n' + src.format("box-right.png")
            + 'at = "00:00:00.370"\nuntil = "00:00:00.620"\n')
    edl = write(C.path(C.EDITS) / "016-overlays.toml", text)
    code, out = cli("assemble", edl)
    master = C.path(C.PROD_RENDERS) / "016-overlays" / "016-overlays.master.mp4"
    made = code == 0 and master.is_file()
    halves = {"left": frame_colours(master, "16:16:8:10") if made else [],
              "right": frame_colours(master, "16:16:40:10") if made else []}
    under = ["2050c0"] * 2 + ["e0a020"] * 3 + ["20c040"] * 6 + ["8020e0"] * 8 + ["30a0dc"] * 6
    due = {"left": ["f0f0f0" if 5 <= f < 11 else u for f, u in enumerate(under)],
           "right": ["101010" if 11 <= f < 19 else u for f, u in enumerate(under)]}

    def off(half, frames):
        """The frames, of those named, whose half does not show the colour due there."""
        seen = halves[half]
        return [f for f in frames if f >= len(seen) or max(
            abs(a - b) for a, b in zip(seen[f], bytes.fromhex(due[half][f]))) > 12]
    whole = len(halves["left"]) == len(halves["right"]) == 25
    shown = (f"{len(halves['left'])} frames; off: left {off('left', range(25))[:8]}, right "
             f"{off('right', range(25))[:8]}\n{out}")
    verdict("an [[overlay]] at a clip's start (00:00:00.370) is on that clip's first frame (11), shown at "
            "0.3667 s, and not on the frame before", whole and not off("right", [10, 11]), shown)
    verdict("an [[overlay]] until a clip's end is gone on the next clip's first frame (11, and 19), and on "
            "every frame of the clip it is timed to", whole and not off("left", range(4, 12))
            and not off("right", range(10, 20)), shown)
    verdict("an [[overlay]] at 00:00:00.150 starts on the frame its clip does where the running total "
            "0.05 + 0.1 s puts that clip on a half frame (frame 5, half up), never a frame early",
            whole and not off("left", [4, 5]) and not off("right", [4, 5]), shown)
    verdict("assemble: every frame of a master with two overlays shows the clip and the overlays due on it "
            "(25 frames)", whole and not off("left", range(25)) and not off("right", range(25)), shown)
    for old, new, what, word in (
            ('until = "00:00:00.620"', 'until = "00:00:00.380"', "covers no frame (.370 to .380 at 30 fps)",
             "under one frame"),
            ('at = "00:00:00.370"\nuntil = "00:00:00.620"', 'at = "00:00:01.000"\nuntil = "00:00:02.000"',
             "starts after the master's last frame", "has ended")):
        bad = write(C.path(C.EDITS) / "016-bad.toml", text.replace(old, new))
        code, out = cli("assemble", bad, "-o", C.path(C.PROD_RENDERS) / "016-bad.mp4")
        verdict(f"assemble refuses an [[overlay]] that {what} (exit 2, nothing rendered)",
                code == 2 and "overlay 2" in out and word in out
                and not (C.path(C.PROD_RENDERS) / "016-bad.mp4").exists(), out)


def test_held_sound(verdict, cli, work: Path) -> None:
    """A master's sound, and each deliverable's, ends with its picture, every frame of it on time.
    A steady tone has no loudness range, so loudnorm never runs linear on it, and its dynamic mode
    (ffmpeg 6.1.1) stamps the short block it reads last as a whole 100 ms: the sound ran on to the
    next tenth of a second, one AAC frame stretched over the hole and all after it stamped late.
    A 30 s stills master encoded to youtube.long had 30.100 s of sound under 30.000 s of picture."""
    folder = C.path(C.ASSETS) / "held"
    folder.mkdir(parents=True, exist_ok=True)
    for name, hexa in (("a", "2050c0"), ("b", "e0a020")):
        lavfi("-f", "lavfi", "-i", f"color=c=0x{hexa}:s=64x36", "-frames:v", "1", folder / f"{name}.png")
    lavfi("-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=5", "-ac", "2", folder / "tone.wav")
    src = 'source = "production/src/assets/held/{}"\n'

    def master(piece: str, second: str) -> tuple:
        """(exit code, output, master): two stills, 2 s and second, over the tone."""
        edl = write(C.path(C.EDITS) / f"{piece}.toml", f'[edit]\npiece = "{piece}"\nsize = "64x36"\n\n[[clip]]\n'
                    + src.format("a.png") + "seconds = 2.0\n\n[[clip]]\n" + src.format("b.png")
                    + f"seconds = {second}\n\n[[audio]]\n" + src.format("tone.wav") + 'role = "music"\n')
        code, out = cli("assemble", edl)
        return code, out, C.path(C.PROD_RENDERS) / piece / f"{piece}.master.mp4"

    def ends(p: Path) -> dict:
        """Where each stream of a render ends, from its own probe: {"video": s, "audio": s}."""
        info = C.probe(p) if p.is_file() else {}
        return {s["codec_type"]: float(s.get("start_time") or 0) + float(s.get("duration") or 0)
                for s in info.get("streams", []) if s.get("codec_type") in ("video", "audio")}

    def held(p: Path, length: float, slack: float) -> str:
        """'' when p's sound, and its picture where it has one, end at length within slack and no
        AAC frame between its first and its last lasts longer than the rest; else what is wrong."""
        got = ends(p)
        wrong = [f"its {kind} ends at {end:.4f} s" for kind, end in got.items() if abs(end - length) > slack]
        if "audio" not in got:
            wrong.append("it has no sound")
        proc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                               "packet=pts,duration", "-of", "json", str(p)], capture_output=True, text=True)
        packets = json.loads(proc.stdout or "{}").get("packets", []) if proc.returncode == 0 else []
        frame = int(packets[1].get("duration", 0)) if len(packets) > 2 else 0
        stretched = [k for k in packets[1:-1] if int(k.get("duration", 0)) != frame]
        if stretched:
            wrong.append(f"an AAC frame is stretched over a hole in its timestamps: {stretched[0]}")
        return "; ".join(wrong)

    # 130 frames at 30 fps (4.333 s): the master's own loudness pass ran its sound on to 4.400 s.
    code, out, grid = master("017-held-grid", "2.3333")
    wrong = held(grid, 130 / 30, 1 / 60)
    verdict("assemble holds a stills master's sound to its picture after the loudness pass (130 frames, 4.333 s: "
            "never on to the next tenth, 4.400 s)", code == 0 and "verified" in out and not wrong, f"{wrong}\n{out}")
    # 4.000 s: a master the loudness pass leaves whole, whose deliverables ran on to 4.100 s.
    code, out, whole = master("017-held", "2.0")
    made = C.path(C.PUB_RENDERS) / "017-held.youtube-long.mp4"
    code2, out2 = cli("encode", whole, "--deliverable", "youtube.long", "-o", made)
    wrong = held(made, 4.0, 1 / 60) if code == 0 else out
    verdict("encode of a 4.000 s stills master to youtube.long holds its sound to the picture (never 4.100 s of "
            "sound under 4.000 s of picture, nor an AAC frame stretched over a hole)",
            code2 == 0 and "verified" in out2 and not wrong, f"{wrong}\n{out2}")
    sound = C.path(C.PUB_RENDERS) / "017-held.podcast.m4a"
    code2, out2 = cli("encode", whole, "--deliverable", "podcast.apple_rss_audio", "-o", sound)
    wrong = held(sound, 4.0, 0.002) if code == 0 else out
    verdict("encode of the same master to podcast.apple_rss_audio lasts the master's 4.000 s, its timestamps "
            "unbroken", code2 == 0 and "verified" in out2 and not wrong, f"{wrong}\n{out2}")
    episode = work / "held episode.m4a"
    lavfi("-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=4.37", "-ac", "2", "-c:a", "aac", episode)
    cover = folder / "a.png"
    made = C.path(C.PUB_RENDERS) / "017-held.still.mp4"
    code2, out2 = cli("still-video", cover, episode, "--deliverable", "youtube.long", "-o", made)
    wrong = held(made, C.duration(C.probe(episode)), 1 / 30)
    verdict("still-video keeps the whole of its sound, to its last sample, under its picture (never cut short by "
            "-t at loudnorm's late timestamps)", code2 == 0 and "verified" in out2 and not wrong, f"{wrong}\n{out2}")
    probe = {"format": {"duration": "30.150000"},
             "streams": [{"codec_type": "video", "duration": "30.000000", "avg_frame_rate": "30/1"},
                         {"codec_type": "audio", "duration": "30.150000"}]}
    found = V.length_findings(probe, 30.0)
    near = V.length_findings({"streams": [dict(probe["streams"][0]), dict(probe["streams"][1], duration="30.050000")]},
                             30.0, held=True)
    verdict("a deliverable's length is checked stream by stream, naming the sound where it runs past its picture "
            "and, where the toolkit held it, where it ends more than a frame from the picture",
            found == ["its sound lasts 30.150 s where 30.000 s was expected"] and len(near) == 1
            and "sound lasts 30.050 s and its picture 30.000 s" in near[0], f"{found} {near}")


def test_source_sound(verdict, cli, work: Path) -> None:
    """A source made elsewhere whose sound and picture end apart (a screen recording, a phone clip).
    cut and captions burn keep the source's own sound, so they are judged by the file's length, as
    before the toolkit held any sound: checked stream by stream, a cut of a sound 0.3 s short and a
    burn of a sound 0.2 s long each failed, and nothing the author could pass fixed them. encode
    holds a sound to its picture only within a frame and 0.1 s: it once cut 7 s of a recording's
    sound, said only a note, and reported the deliverable verified."""
    made = {}
    for name, size, picture, sound in (("short", "1080x1920", 2, 1.7), ("long", "1080x1920", 2, 2.2),
                                       ("far", "192x108", 1, 4), ("near", "192x108", 1, 1.1)):
        made[name] = work / f"sound-{name}.mp4"
        lavfi("-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30:duration={picture}", "-f", "lavfi", "-i",
              f"sine=frequency=440:sample_rate=48000:duration={sound}", "-c:v", "libx264", "-preset", "ultrafast",
              "-pix_fmt", "yuv420p", "-c:a", "aac", made[name])
    out_dir = C.path(C.PUB_RENDERS)
    code, out = cli("cut", made["short"], "--deliverable", "youtube.short", "--in", "0", "--out", "00:00:02.000",
                    "-o", out_dir / "sound-short.cut.mp4")
    verdict("cut of a source whose sound stops 0.3 s before its picture is verified by the file's length "
            "(exit 0), never failed for the sound it never had", code == 0 and "verified" in out, out)
    srt = write(work / "sound.srt", K.srt_text([K.Cue(0.3, 1.5, ["The ferry is late."])]))
    for name, what in (("short", "stops 0.3 s before"), ("long", "runs 0.2 s past")):
        code, out = cli("captions", "burn", made[name], srt, "--deliverable", "youtube.short", "-o",
                        out_dir / f"sound-{name}.burned.mp4")
        verdict(f"captions burn of a source whose sound {what} its picture is clean (exit 0): it keeps the "
                "source's sound, and is judged by the file's length", code == 0 and "FAIL" not in out, out)
    far = out_dir / "sound-far.youtube-long.mp4"
    code, out = cli("encode", made["far"], "--deliverable", "youtube.long", "-o", far)
    verdict("encode refuses a source whose sound runs 3 s past its picture, naming it (exit 1, nothing rendered), "
            "never cutting the author's sound with only a note", code == 1 and "runs 3.000 s past its picture" in out
            and "nothing rendered" in out and not far.exists(), out)
    near = out_dir / "sound-near.youtube-long.mp4"
    code, out = cli("encode", made["near"], "--deliverable", "youtube.long", "-o", near)
    info = C.probe(near) if near.is_file() else {}
    ends = [V.span(info, kind) for kind in ("video", "audio")]
    verdict("encode holds a sound 0.1 s past its picture (within a frame and 0.1 s) to the picture, verified",
            code == 0 and "verified" in out and all(ends) and abs(ends[1][1] - ends[0][1]) <= 1 / 30 + 1e-3,
            f"{ends}\n{out}")


def spied_assemble(cli, edl: Path) -> tuple:
    """(exit code, output, stage) of one assemble, stage holding its render's input count, looped
    inputs and each ffconcat list, read while the list exists, and how many images it framed."""
    stage, real = {"framed": 0}, C.ffmpeg

    def spy(args, cwd=None, what="ffmpeg"):
        args = [str(a) for a in args]
        if args and Path(args[-1]).name.startswith("framed-"):   # framed_still's own pass
            stage["framed"] += 1
        elif "-filter_complex" in args:
            stage.update(inputs=args.count("-i"), loops=args.count("-loop"), lists=[
                Path(args[args.index("-i", n) + 1]).read_text(encoding="utf-8")
                for n in range(len(args) - 1) if args[n:n + 2] == ["-f", "concat"]])
        return real(args, cwd=cwd, what=what)
    C.ffmpeg = spy
    try:
        code, out = cli("assemble", edl)
    finally:
        C.ffmpeg = real
    return code, out, stage


def frame_colours(p: Path, crop: str = "") -> list:
    """The mean (r, g, b) of every frame of a video, in order: each frame (or the region crop names,
    as ffmpeg's crop takes it: w:h:x:y) scaled to one pixel."""
    proc = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", (f"crop={crop}," if crop else "")
                           + "format=rgb24,scale=1:1:flags=area", "-fps_mode", "passthrough", "-f", "rawvideo",
                           "-"], capture_output=True, check=True)
    return [tuple(proc.stdout[k:k + 3]) for k in range(0, len(proc.stdout) - 2, 3)]


def exif_turned(jpg: Path) -> Path:
    """The JPEG with an EXIF orientation of 6 (turned a quarter clockwise), as a phone writes one."""
    tiff = (b"MM\x00\x2a\x00\x00\x00\x08\x00\x01" + b"\x01\x12\x00\x03\x00\x00\x00\x01\x00\x06\x00\x00"
            + b"\x00\x00\x00\x00")
    app1 = b"Exif\x00\x00" + tiff
    data = jpg.read_bytes()
    jpg.write_bytes(data[:2] + b"\xff\xe1" + (len(app1) + 2).to_bytes(2, "big") + app1 + data[2:])
    return jpg


def kind_id(kind: str) -> str:
    """The footage ID the fixture logged for a kind."""
    return next((r["id"] for r in R.manifest_rows(C.path(C.MANIFEST)) if r["kind"] == kind), "F9999")


CARD_HTML = """<!doctype html>
<html lang="en-GB">
<head><meta charset="utf-8"><link rel="stylesheet" href="../../../brand/src/design-system/tokens.css">
<style>html, body { margin: 0; width: 100vw; height: 100vh; overflow: hidden; background: var(--color-bg); }</style>
</head><body></body></html>
"""


def test_align(verdict, cli, root: Path, work: Path) -> None:
    speech = work / "recording.wav"
    lavfi("-f", "lavfi", "-i", "sine=frequency=300:sample_rate=48000:duration=8.5", "-af",
          "volume='between(t,1,2)+between(t,2.5,3.5)+between(t,5,6)+between(t,6.5,7.5)':eval=frame", speech)
    transcript = root / C.PIECES / "001-fixture" / "transcript.md"
    code, out = cli("captions", "align", transcript, speech, "--anchors", "-o",
                    C.path(C.CAPTIONS) / "001-fixture.F0003.en-GB.srt")
    cues = K.read_srt(C.path(C.CAPTIONS) / "001-fixture.F0003.en-GB.srt")
    beat1 = [c for c in cues if c.text.startswith(("The harbour", "Boats"))]
    beat2 = [c for c in cues if c.text.startswith(("We wait", "Then"))]
    verdict("captions align --anchors keeps every cue of a beat inside its beat",
            code == 0 and len(beat1) == 2 and len(beat2) == 2 and all(0.5 <= c.start and c.end <= 4.5 for c in beat1)
            and all(4.5 <= c.start and c.end <= 8.5 for c in beat2), out + K.srt_text(cues))
    verdict("captions align snaps line starts to speech", abs(beat1[0].start - 1.0) < 0.15 and
            abs(beat1[1].start - 2.5) < 0.15 if len(beat1) == 2 else False, K.srt_text(cues))
    cut = work / "cut.wav"
    lavfi("-ss", "4.5", "-to", "8.5", "-i", speech, cut)
    code, out, err = cli_split("captions", "align", transcript, cut, "--lines", "2.1-2.2")
    cues = K.parse_srt(out) if code != 2 else []
    verdict("captions align --lines places every cue of one cut (to stdout without -o)", code == 0 and len(cues) == 2
            and abs(cues[0].start - 0.5) < 0.15 and abs(cues[1].start - 2.0) < 0.15 and "cue(s) placed" in err,
            out + err)


def test_audiobook(verdict, cli, root: Path, work: Path) -> None:
    gen = C.path(C.AB_GENERATED)
    takes = []
    for k, dur in ((1, 9), (2, 7)):
        t = gen / f"002-fixture-book.ch01.p{k:02d}.t1.mp3"
        # speech at about -21 dB RMS (sine's own amplitude is 1/8) over a room at about -72 dB: a
        # recording ACX would take, its room tone heard between the phrases
        lavfi("-f", "lavfi", "-i", f"sine=frequency=220:sample_rate=44100:duration={dur}", "-f", "lavfi", "-i",
              f"anoisesrc=color=white:amplitude=0.0005:sample_rate=44100:duration={dur}", "-filter_complex",
              "[0:a]volume='lt(mod(t,4),3.2)':eval=frame[s];[s][1:a]amix=inputs=2:normalize=0",
              "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k", t)
        takes.append(t)
    side = write(gen / "002-fixture-book.ch01.chunks.toml",
                 'piece = "002-fixture-book"\nchapter = "ch01"\nsource = "fixture"\n\n'
                 '[[chunk]]\npart = "p01"\nfile = "002-fixture-book.ch01.p01.txt"\ncharacters = 9\npause_after = 1.5\n\n'
                 '[[chunk]]\npart = "p02"\nfile = "002-fixture-book.ch01.p02.txt"\ncharacters = 7\npause_after = 0.0\n')
    code, out = cli("audiobook", "master", takes[0], "--piece", "002-fixture-book", "--chapter", "ch01")
    verdict("audiobook master refuses a chapter with a chunk the sidecar lists but no take (exit 2)",
            code == 2 and "no take given for p02" in out, out)
    code, out = cli("audiobook", "master", takes[1], takes[0], "--piece", "002-fixture-book", "--chapter", "ch01")
    mp3 = C.path(C.AB_RENDERS) / "002-fixture-book.ch01.mp3"
    got = C.duration(C.probe(mp3)) if mp3.is_file() else 0.0
    verdict("audiobook master joins takes in chunk order with the sidecar's room tone between them, "
            "built from the takes' own quietest stretch, and passes the ACX check",
            code == 0 and abs(got - (A.ACX_HEAD + 9 + 1.5 + 7 + A.ACX_TAIL)) < 0.1 and "chunk order" in out
            and "1.5 s after" in out and "archive this master" in out and "room tone: the quietest" in out,
            f"{got}\n{out}")
    side.unlink()
    code, out = cli("audiobook", "master", *takes, "--piece", "002-fixture-book", "--chapter", "ch01",
                    "-o", C.path(C.AB_RENDERS) / "no-sidecar.mp3")
    got = C.duration(C.probe(C.path(C.AB_RENDERS) / "no-sidecar.mp3")) if code != 2 else 0.0
    verdict("audiobook master without a sidecar joins the takes with no pause", code == 0
            and abs(got - (A.ACX_HEAD + 9 + 7 + A.ACX_TAIL)) < 0.1, f"{got}\n{out}")
    code, out = cli("audiobook", "check", mp3)
    verdict("audiobook check passes the master", code == 0, out)
    hot = C.path(C.AB_RENDERS) / "hot.mp3"
    lavfi("-i", mp3, "-af", "volume=16dB", "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", hot)
    code, out = cli("audiobook", "check", hot)
    verdict("audiobook check fails a hot-peak mutation", code == 1 and "FAIL  peak" in out, out)
    padded = C.path(C.AB_RENDERS) / "padded.mp3"   # the master with digital silence added at both ends
    lavfi("-i", mp3, "-af", "adelay=1500:all=1,apad=pad_dur=2", "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame",
          "-b:a", "192k", padded)
    code, out = cli("audiobook", "check", padded)
    verdict("audiobook check fails a head and a tail of digital silence, and leaves it out of the noise floor",
            code == 1 and "digital silence, not room tone" in out and "of digital silence left out" in out, out)
    noisy = work / "noisy-ch02.wav"   # a recording whose own floor is far above -60 dB
    lavfi("-f", "lavfi", "-i", "sine=frequency=220:sample_rate=44100:duration=8", "-f", "lavfi", "-i",
          "anoisesrc=color=pink:amplitude=0.006:sample_rate=44100:duration=8", "-filter_complex",
          "[0:a]volume=0.2,volume='lt(mod(t,4),3.2)':eval=frame[s];[s][1:a]amix=inputs=2:normalize=0", "-ac", "1",
          noisy)
    code, out = cli("audiobook", "master", noisy, "--piece", "002-fixture-book", "--chapter", "ch02")
    verdict("audiobook master of a noisy recording fails the noise floor: the head, the tail and the pauses are "
            "its own room tone, never digital silence that hides it",
            code == 1 and "FAIL  noise floor" in out and "room tone: the quietest" in out, out)
    tone = work / "tone-ch03.wav"   # a take with no quiet stretch at all
    lavfi("-f", "lavfi", "-i", "sine=frequency=220:sample_rate=44100:duration=6", "-ac", "1", tone)
    room = work / "room.wav"
    lavfi("-f", "lavfi", "-i", "anoisesrc=color=pink:amplitude=0.0005:sample_rate=44100:duration=3", "-ac", "1", room)
    code, out = cli("audiobook", "master", tone, "--piece", "002-fixture-book", "--chapter", "ch03")
    verdict("audiobook master with no room tone to be found says so, and the ACX check fails it",
            code == 1 and "none found" in out and "--room-tone FILE" in out, out)
    code, out = cli("audiobook", "master", tone, "--piece", "002-fixture-book", "--chapter", "ch03", "--room-tone",
                    room, "-o", C.path(C.AB_RENDERS) / "with-room.mp3")
    verdict("audiobook master --room-tone FILE loops a recording of the room for the gaps, and passes",
            code == 0 and "room tone: --room-tone" in out and "passes the ACX check" in out, out)
    code, out = cli("cut", mp3, "--deliverable", "audiobook.acx", "--in", "00:00:01.000", "--out", "00:00:06.000")
    sample = C.path(C.PUB_RENDERS) / "002-fixture-book" / "002-fixture-book.audiobook-acx.mp3"
    a = C.streams(C.probe(sample), "audio") if sample.is_file() else []
    verdict("cut makes an audiobook retail sample: sound only, MP3, 44.1 kHz, mono, held to sample_max_seconds, "
            "in the piece's folder of publishing/src/renders/ (the audiobook folder's renders/ stays flat)",
            code == 0 and a and a[0]["codec_name"] == "mp3" and a[0]["sample_rate"] == "44100"
            and a[0]["channels"] == 1 and "sample_max_seconds 300" in out, out)
    overrides = C.path(C.OVERRIDES)
    saved = C.read_text(overrides)
    write(overrides, saved + '\n[[override]]\nkey = "audiobook.acx.sample_max_seconds"\nvalue = 3\n'
                             'why = "fixture"\nsource = "fixture"\nchecked = "01/09/2026"\n')
    try:
        code, out = cli("cut", mp3, "--deliverable", "audiobook.acx", "--in", "00:00:01.000", "--out",
                        "00:00:06.000", "-o", C.path(C.PUB_RENDERS) / "too-long-sample.mp3")
    finally:
        write(overrides, saved)
    verdict("an audiobook sample over sample_max_seconds fails before it renders",
            code == 1 and "nothing rendered" in out and not (C.path(C.PUB_RENDERS) / "too-long-sample.mp3").exists(), out)


def encoders() -> str:
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return proc.stdout


def logged_id(out: str) -> str:
    m = re.search(r"logged (F\d{4,})", out)
    return m.group(1) if m else "F9999"


def test_screen(verdict, skip, cli, work: Path) -> None:
    """Screen recordings as sources: Playwright's VP8 WebM (1920x1080, 25 fps), VHS's H.264 MP4,
    VP9 WebM and animated GIF (1200x600), none with sound, and a one-frame GIF held as a still."""
    rec = work / "screen"
    rec.mkdir()
    have = encoders()
    shots = [("browser.webm", "1920x1080", 25, "libvpx",
              ["-c:v", "libvpx", "-deadline", "realtime", "-cpu-used", "16", "-b:v", "400k"]),
             ("terminal.mp4", "1200x600", 50, "libx264",
              ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"]),
             ("terminal.webm", "1200x600", 50, "libvpx-vp9",
              ["-c:v", "libvpx-vp9", "-deadline", "realtime", "-cpu-used", "8", "-b:v", "400k"]),
             ("terminal.gif", "1200x600", 25, "gif",
              ["-vf", "split[a][b];[a]palettegen=max_colors=32[p];[b][p]paletteuse"])]
    made = []
    for name, size, fps, encoder, codec in shots:
        if f" {encoder} " not in have:
            skip(f"the {name} screen recording", f"this ffmpeg has no {encoder} encoder")
            continue
        lavfi("-f", "lavfi", "-i", f"testsrc2=size={size}:rate={fps}:duration=1.2", "-an", *codec, rec / name)
        made.append(name)
    slide = rec / "slide.gif"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=1200x600:rate=1:duration=1", "-frames:v", "1", slide)
    gif = rec / "terminal.gif"
    code, out = cli("probe", gif, "--json")
    info = json.loads(out) if code == 0 else {}
    code2, out2 = cli("probe", slide, "--json")
    info2 = json.loads(out2) if code2 == 0 else {}
    verdict("probe counts an animated GIF's frames (moving) and a one-frame GIF's (a still)",
            info.get("frames") == 30 and info.get("still") is False and info2.get("frames") == 1
            and info2.get("still") is True, out + out2)
    ids, lengths = {}, {}
    for name in made + ["slide.gif"]:
        code, out = cli("footage", "add", rec / name, "--kind", "video", "--location", "Screen recordings")
        ids[name] = logged_id(out) if code == 0 else "F9999"
    for row in R.manifest_rows(C.path(C.MANIFEST)):
        lengths[str(row.get("id"))] = float(row.get("duration") or 0)
    verdict("footage add logs each screen recording with its length, and a one-frame GIF with 0.0",
            all(abs(lengths.get(ids[n], 0) - 1.2) < 0.05 for n in made)
            and lengths.get(ids["slide.gif"]) == 0.0, f"{ids} {lengths}")
    raw = C.path(C.RAW)
    code, out = cli("cut", raw / "terminal.gif", "--deliverable", "youtube.short", "--in", "00:00:00.200",
                    "--out", "00:00:01.000", "--frame", "crop", "-o", C.path(C.PUB_RENDERS) / "gif.short.mp4")
    verdict("cut takes an animated GIF as its source", code == 0 and "verified" in out, out)
    code, out = cli("encode", raw / "terminal.gif", "--deliverable", "youtube.long", "--frame", "crop",
                    "-o", C.path(C.PUB_RENDERS) / "gif.long.mp4")
    verdict("encode takes an animated GIF as its source (it has no sound: none is made)",
            code == 0 and "verified" in out, out)
    code, out = cli("cut", raw / "slide.gif", "--deliverable", "youtube.short", "--in", "0", "--out", "1")
    verdict("cut refuses a one-frame GIF, naming it a still (exit 2)", code == 2 and "still image" in out, out)
    if " libwebp_anim " in have:
        anim = rec / "moving.webp"
        lavfi("-f", "lavfi", "-i", "testsrc2=size=320x160:rate=10:duration=0.5", "-c:v", "libwebp_anim", anim)
        code, out = cli("probe", anim, "--json")
        moving = code == 0 and json.loads(out).get("still") is False
        verdict("an animated WebP is moving where ffmpeg decodes it, and refused by name where it cannot",
                moving or (code == 2 and "animated WebP" in out), out)
    else:
        skip("an animated WebP is moving or refused by name", "this ffmpeg has no libwebp_anim encoder")
    # (a) and (b) alone: a GIF cut by in and out, a one-frame GIF held for seconds; the master's
    # rate is the GIF's, a whole number, as no other clip has one.
    only = write(C.path(C.EDITS) / "010-gif.toml", f"""[edit]
piece = "010-gif"
size = "640x360"
loudness = "none"

[[clip]]
id = "c01"
source = "{ids.get('terminal.gif', 'F9999')}"
in = "00:00:00.200"
out = "00:00:01.000"

[[clip]]
id = "c02"
source = "{ids['slide.gif']}"
seconds = 0.5
""")
    code, out = cli("assemble", only)
    master = C.path(C.PROD_RENDERS) / "010-gif" / "010-gif.master.mp4"
    info = C.probe(master) if master.is_file() else {}
    v = C.streams(info, "video")
    verdict("assemble cuts an animated GIF by in and out and holds a one-frame GIF (never -loop on the gif "
            "demuxer), at the GIF's own whole-number rate",
            code == 0 and abs(C.duration(info) - 1.3) < 0.1 and bool(v)
            and C.rate(v[0].get("avg_frame_rate")) == 25, out)
    bed = rec / "screen-bed.wav"
    lavfi("-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=8", "-af", "volume=0.3", bed)
    code, out = cli("footage", "add", bed, "--kind", "music", "--location", "Library C")
    music = logged_id(out)
    clips, total = [], 0.0
    plan = [("browser.webm", 'in = "00:00:00.100"\nout = "00:00:01.100"\nframe = "fit"\n', 1.0, 0.0),
            ("terminal.mp4", 'in = "00:00:00.000"\nout = "00:00:01.000"\nframe = "pad"\n', 1.0, 0.3),
            ("terminal.webm", 'in = "00:00:00.200"\nout = "00:00:01.200"\nframe = "fit"\n', 1.0, 0.0),
            ("terminal.gif", 'in = "00:00:00.100"\nout = "00:00:01.100"\nframe = "crop"\n', 1.0, 0.3),
            ("slide.gif", 'seconds = 1.0\nmotion = "push-in"\n', 1.0, 0.0)]
    for n, (name, body, dur, fade) in enumerate([p for p in plan if p[0] in ids], start=1):
        enter = f'transition = "fade"\ntransition_seconds = {fade}\n' if fade and clips else ""
        clips.append(f'[[clip]]\nid = "c{n:02d}"\nsource = "{ids[name]}"\n{body}{enter}')
        total += dur - (fade if enter else 0.0)
    edl = write(C.path(C.EDITS) / "011-screen.toml", '[edit]\npiece = "011-screen"\nsize = "1280x720"\n'
                'audio_rate = 48000\nloudness = "social"\n\n' + "\n".join(clips) + f"""
[[audio]]
source = "{music}"
at = "00:00:00.000"
in = "00:00:00.500"
out = "00:00:07.500"
gain_db = -6.0
fade_in = 0.3
fade_out = 0.5
role = "music"
""")
    code, out = cli("assemble", edl)
    master = C.path(C.PROD_RENDERS) / "011-screen" / "011-screen.master.mp4"
    info = C.probe(master) if master.is_file() else {}
    verdict("assemble: screen recordings with no sound (WebM VP8 and VP9, MP4, GIF) and a one-frame GIF, "
            "with fades, under a music bed, to the social loudness",
            code == 0 and "verified" in out and abs(C.duration(info) - total) < 0.1
            and bool(C.streams(info, "audio")), f"{total}\n{out}")
    if not master.is_file():
        return
    srt = write(C.path(C.CAPTIONS) / "011-screen.en-GB.srt",
                K.srt_text([K.Cue(0.3, 1.6, ["The browser opens the page."]),
                            K.Cue(2.0, 3.4, ["The terminal runs the check."])]))
    for frame in ("pad", "crop"):
        code, out = cli("cut", master, "--deliverable", "youtube.short", "--in", "00:00:00.000", "--out",
                        "00:00:03.500", "--frame", frame, "--captions", srt,
                        "-o", C.path(C.PUB_RENDERS) / f"011-screen.short-{frame}.mp4")
        verdict(f"cut of the screen-recording master to youtube.short, --frame {frame}, captions burned",
                code == 0 and "verified" in out and "1080x1920" in out, out)
    code, out = cli("encode", master, "--deliverable", "youtube.long", "-o", C.path(C.PUB_RENDERS) / "011-screen.long.mp4")
    verdict("encode of the screen-recording master to youtube.long, at its loudness",
            code == 0 and "verified" in out and "1920x1080" in out, out)



def pixel(p: Path, x: int, y: int) -> tuple:
    """The (r, g, b) of one pixel of an image's first frame."""
    proc = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-frames:v", "1", "-vf",
                           f"format=rgb24,crop=1:1:{x}:{y}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, check=True)
    return tuple(proc.stdout[:3])


def with_override(key: str, value: str):
    """A context in which overrides.toml carries one more override, restored after."""
    @contextlib.contextmanager
    def held():
        p = C.path(C.OVERRIDES)
        saved = C.read_text(p)
        write(p, saved + f'\n[[override]]\nkey = "{key}"\nvalue = {value}\nwhy = "fixture"\nsource = "fixture"\n'
                         'checked = "01/09/2026"\n')
        try:
            yield
        finally:
            write(p, saved)
    return held()


def test_web(verdict, skip, cli, root: Path) -> None:
    """image, the GIF pass of cut, --overlay, the silent loop and web video (DESIGN D57)."""
    work = Path(str(root) + "-web")
    work.mkdir()
    renders = C.path(C.PUB_RENDERS)
    web = renders / "021-web"   # the piece's own folder, where every default of its outputs lands (D64)
    master = C.path(C.PROD_RENDERS) / "021-web" / "021-web.master.mp4"
    for folder in (master.parent, web):
        folder.mkdir(parents=True, exist_ok=True)
    lavfi("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=3", "-f", "lavfi", "-i",
          "sine=frequency=440:sample_rate=48000:duration=3", "-c:v", "libx264", "-preset", "ultrafast",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", master)
    card = web / "021-web.blog-featured-image.png"   # what card.py render writes for the key (default_png)
    lavfi("-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=1:duration=1", "-frames:v", "1", card)
    have = {fmt: C.image_encoder(fmt) for fmt in ("webp", "avif")}
    code, out = cli("image", card, "--deliverable", "blog.featured_image")
    got = C.streams(C.probe(web / "021-web.blog-featured-image.jpg"), "video") if code == 0 else []
    verdict("image encodes a PNG into the table's first format (jpg) at its size, named <stem>.<platform>-<format>, "
            "in the piece's folder (D64)",
            code == 0 and got and got[0]["codec_name"] == "mjpeg" and (got[0]["width"], got[0]["height"]) == (1920, 1080),
            out)
    for fmt, codec in (("webp", "webp"), ("avif", "av1")):
        if not have[fmt]:
            skip(f"image --format {fmt}", f"this ffmpeg lacks {'libwebp' if fmt == 'webp' else 'an AV1 encoder or the avif muxer'}")
            continue
        code, out = cli("image", card, "--deliverable", "blog.featured_image", "--format", fmt)
        made = web / f"021-web.blog-featured-image.{fmt}"
        got = C.streams(C.probe(made), "video") if made.is_file() else []
        verdict(f"image --format {fmt} writes {codec} at the table's size", code == 0 and got
                and got[0]["codec_name"] == codec and int(got[0]["width"]) == 1920, out)
    code, out = cli("image", card, "--deliverable", "website.poster", "--format", "png")
    verdict("image refuses a format the table does not list (exit 2)", code == 2 and "not one of" in out, out)
    share = web / "021-web.website-og-image.png"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=1200x630:rate=1:duration=1", "-frames:v", "1", share)
    held = share.read_bytes()
    code, out = cli("image", share, "--deliverable", "website.og_image", "--format", "png")
    verdict("image of a PNG already at the size, asked for as png, verifies it where it stands and writes nothing",
            code == 0 and "nothing written" in out and share.read_bytes() == held
            and len(list(web.glob("021-web.website-og-image*"))) == 1
            and not list(renders.glob("021-web.website-og-image*")), out)
    clear = work / "cover-export.png"   # a design export with transparency
    lavfi("-f", "lavfi", "-i", "color=c=0x204060@0.5:s=3000x3000,format=rgba", "-frames:v", "1", clear)
    code, out = cli("image", clear, "--deliverable", "podcast.id3_cover", "-o", renders / "fixture-show.podcast-id3-cover.jpg")
    got = C.streams(C.probe(renders / "fixture-show.podcast-id3-cover.jpg"), "video") if code == 0 else []
    verdict("image flattens a transparent export where alpha = false (podcast.id3_cover, 1400x1400 JPEG)",
            code == 0 and "flattened" in out and got and (got[0]["width"], got[0]["height"]) == (1400, 1400), out)
    code, out = cli("image", clear, "--deliverable", "podcast.cover")
    cover = renders / "cover-export.podcast-cover.png"
    got = C.streams(C.probe(cover), "video") if code == 0 and cover.is_file() else []
    verdict("image keeps a PNG cover opaque where alpha = false (no alpha channel), and writes a design export "
            "whose name has no piece key at the top of publishing/src/renders/ (D64)",
            code == 0 and got and not C.has_alpha(got[0].get("pix_fmt")), out)
    code, out = cli("image", card, "--deliverable", "podcast.cover")
    verdict("image refuses a source of another shape without --frame (exit 2), naming crop and pad",
            code == 2 and "--frame crop" in out and "--frame pad" in out, out)
    code, out = cli("image", card, "--deliverable", "podcast.cover", "--frame", "crop", "--format", "jpg")
    verdict("image --frame crop fills another shape", code == 0 and "3000x3000" in out, out)
    code, out = cli("image", master, "--deliverable", "website.poster", "--at", "00:00:01.000")
    poster = web / "021-web.website-poster.jpg"
    got = C.streams(C.probe(poster), "video") if poster.is_file() else []
    verdict("image takes a poster from a video at --at, at the poster's size",
            code == 0 and got and (got[0]["width"], got[0]["height"]) == (1920, 1080), out)
    code, out = cli("image", master, "--deliverable", "website.poster")
    verdict("image of a video without --at is refused (exit 2)", code == 2 and "--at" in out, out)
    code, out = cli("image", card, "--deliverable", "youtube.podcast_thumbnail")
    verdict("image refuses a table with no width and height, naming card.py --size (exit 2)",
            code == 2 and "--size" in out, out)
    with with_override("newsletter.preview_image.max_size", '"1 KB"'):
        code, out = cli("image", card, "--deliverable", "newsletter.preview_image", "--frame", "crop", "-o",
                        renders / "too-heavy.jpg")
    verdict("image fails an output over max_size (a max_size mutation, exit 1)",
            code == 1 and "over newsletter.preview_image max_size" in out, out)
    # The GIF preview: an overlay rendered at the deliverable's size, a red square at its centre.
    overlay = web / "021-web.newsletter-preview-gif.png"
    lavfi("-f", "lavfi", "-i", "color=c=black@0.0:s=600x338,format=rgba", "-vf",
          "drawbox=x=280:y=149:w=40:h=40:color=red@1.0:t=fill:replace=1", "-frames:v", "1", overlay)
    code, out = cli("cut", master, "--deliverable", "newsletter.preview_gif", "--in", "0", "--out", "3",
                    "--overlay", overlay)
    gif = web / "021-web.newsletter-preview-gif.gif"
    facts = I.gif_facts(gif) if gif.is_file() else {}
    red = pixel(gif, 300, 169) if gif.is_file() else (0, 0, 0)
    verdict("cut to newsletter.preview_gif: a GIF at 600x338 within fps_max, the overlay on its first frame, in "
            "the piece's folder",
            code == 0 and facts.get("width") == 600 and facts.get("height") == 338
            and facts["frames"] / facts["seconds"] <= 15.0 and red[0] > 180 and red[1] < 80 and red[2] < 80,
            f"{out}\n{facts}\n{red}")
    verdict("a 3-second GIF plays once (no loop extension), within max_seconds",
            facts.get("loop") is None and facts.get("plays") == 1 and facts.get("play_seconds", 9) <= 5.0, facts)
    code, out = cli("cut", master, "--deliverable", "newsletter.preview_gif", "--in", "0", "--out", "2",
                    "--cut", "c02", "--overlay", overlay)
    two = web / "021-web--c02.newsletter-preview-gif.gif"
    facts2 = I.gif_facts(two) if two.is_file() else {}
    verdict("a 2-second GIF plays twice (loop count 1), its play time read from the loop extension and the "
            "frame delays within max_seconds",
            code == 0 and facts2.get("loop") == 1 and facts2.get("plays") == 2 and facts2.get("play_seconds", 9) <= 5.0,
            f"{out}\n{facts2}")
    long_src = work / "long.mp4"
    lavfi("-f", "lavfi", "-i", "testsrc2=size=320x180:rate=30:duration=6", "-c:v", "libx264", "-preset",
          "ultrafast", "-pix_fmt", "yuv420p", long_src)
    code, out = cli("cut", long_src, "--deliverable", "newsletter.preview_gif", "--in", "0", "--out", "6",
                    "-o", renders / "too-long.gif")
    verdict("a GIF range longer than max_seconds renders nothing (exit 1)",
            code == 1 and "nothing rendered" in out and not (renders / "too-long.gif").exists(), out)
    code, out = cli("cut", master, "--deliverable", "newsletter.preview_gif", "--in", "0", "--out", "2",
                    "--overlay", card, "-o", renders / "wrong-overlay.gif")
    verdict("an overlay of another size is refused (exit 2)", code == 2 and "1920x1080" in out, out)
    if two.is_file():
        budget = max(1, int(two.stat().st_size * 0.75 / 1000))
        with with_override("newsletter.preview_gif.max_size", f'"{budget} KB"'):
            code, out = cli("cut", master, "--deliverable", "newsletter.preview_gif", "--in", "0", "--out", "2",
                            "--overlay", overlay, "-o", renders / "thinned.gif")
        thin = I.gif_facts(renders / "thinned.gif") if (renders / "thinned.gif").is_file() else {}
        verdict("a GIF over max_size is made again at half the frame rate, its duration unchanged",
                code == 0 and "every second frame" in out and thin.get("frames", 0) * 2 <= facts2["frames"] + 1
                and abs(thin.get("seconds", 0) - facts2["seconds"]) <= 0.15, f"{out}\n{thin}\n{facts2}")
    code, out = cli("cut", master, "--deliverable", "youtube.long", "--in", "0", "--out", "1", "--overlay",
                    overlay, "-o", renders / "wrong-video-overlay.mp4")
    verdict("--overlay on a video cut refuses another size too (exit 2)", code == 2 and "600x338" in out, out)
    big = renders / "overlay-1080.png"
    lavfi("-f", "lavfi", "-i", "color=c=black@0.0:s=1920x1080,format=rgba", "-vf",
          "drawbox=x=900:y=480:w=120:h=120:color=red@1.0:t=fill:replace=1", "-frames:v", "1", big)
    code, out = cli("cut", master, "--deliverable", "website.video", "--in", "0", "--out", "2", "--overlay", big,
                    "-o", renders / "overlaid.mp4")
    red = pixel(renders / "overlaid.mp4", 960, 540) if code == 0 else (0, 0, 0)
    verdict("--overlay lays a PNG over a video cut, and website.video keeps its index at the front",
            code == 0 and "verified" in out and red[0] > 160 and red[1] < 90 and "moov first" in out, f"{out}\n{red}")
    code, out = cli("cut", master, "--deliverable", "website.hero_loop", "--in", "0", "--out", "2", "--cut", "c09")
    loop = web / "021-web--c09.website-hero-loop.mp4"
    info = C.probe(loop) if loop.is_file() else {}
    verdict("cut to website.hero_loop (audio_tracks = 0) writes no sound track from a source with sound",
            code == 0 and C.streams(info, "video") and not C.streams(info, "audio"), out)
    code, out = cli("encode", master, "--deliverable", "website.hero_loop", "--frame", "crop",
                    "-o", renders / "loop-encoded.mp4")
    info = C.probe(renders / "loop-encoded.mp4") if code == 0 else {}
    verdict("encode to website.hero_loop writes no sound track either", code == 0 and not C.streams(info, "audio"), out)
    with contextlib.redirect_stdout(io.StringIO()):
        found = V.verify(master, C.preset("website.hero_loop", quiet=True))
    verdict("a silent table's verification fails a file that keeps its sound (a mutation)",
            any("audio_tracks = 0" in f for f in found), found)
    code, out = cli("image", master, "--deliverable", "newsletter.preview_gif", "--at", "1")
    verdict("image refuses a GIF table: the GIF is cut's (exit 2)", code == 2 and "cut" in out, out)
    code, out = cli("encode", master, "--deliverable", "website.poster")
    verdict("encode refuses an image table, naming image and card.py (exit 2)",
            code == 2 and "media.py image" in out and "card.py" in out, out)


FEED_SHOW = {"title": "Harbour Lane Talks", "link": "https://www.example.com/podcast/harbour-lane-talks/",
             "media_base": "https://media.example.com/podcast/harbour-lane-talks/", "author": "Harbour Lane Studio",
             "owner_name": "Harbour Lane Studio", "owner_email": "podcast@example.com",
             "copyright": "© 2026 Harbour Lane Studio", "category": "Business", "subcategory": "Entrepreneurship",
             "cover": "fixture-show.podcast-cover.jpg", "id3_cover": "fixture-show.podcast-id3-cover.jpg",
             "approved": "04/10/2026"}


def set_description(text: str, after: str, words: str) -> str:
    """Fill the empty description of [show] (after = 'show') or of an episode (after = its piece)."""
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines) if (ln.startswith("[show]") if after == "show"
                                                       else ln.startswith(f'piece = "{after}"')))
    at = next(i for i in range(start, len(lines)) if lines[i].startswith('description = """'))
    lines.insert(at + 1, words)
    return "\n".join(lines)


def test_feed(verdict, skip, cli, root: Path, project_zone) -> None:
    """The self-hosted podcast feed end to end, offline (DESIGN D58, D59, Section 6.17)."""
    show = "fixture-show"
    reg = C.path(C.PODCAST) / f"{show}.toml"
    tracked = C.path(C.PODCAST) / f"{show}.feed.xml"
    url = "https://www.example.com/podcast/fixture-show/feed.xml"
    if project_zone:
        saved, C.TIMEZONE = C.TIMEZONE, project_zone
        try:
            verdict(f"the project's timezone ({project_zone}) is known to this machine", C.zone() is not None)
        except C.Fatal as err:
            verdict(f"the project's timezone ({project_zone}) is known to this machine", False, err)
        finally:
            C.TIMEZONE = saved
    code, out = cli("feed", "new", show, "--feed-url", url)
    verdict("feed new refuses a project without the podcast folder (exit 2), naming copier update -a",
            code == 2 and "copier update" in out and "-a .copier-answers.syntek-media.yml" in out
            and not C.path(C.PODCAST).exists(), out)
    for name in ("CONTEXT.md", "CLAUDE.md"):
        write(C.path(C.PODCAST) / name, "# pair\n")
    code, out = cli("feed", "new", show, "--feed-url", url + "/", "--site", "studio")
    data = C.load_toml(reg) if reg.is_file() else {"show": {}}
    by_hand = F.uuid5_by_hand(str(F.PODCAST_NAMESPACE), "www.example.com/podcast/fixture-show/feed.xml")
    verdict("feed new writes the register from the skeleton, with podcast:guid the UUIDv5 of the feed URL "
            "(scheme and trailing slashes stripped, RFC 4122 by hand), and flags owner_email",
            code == 0 and data["show"].get("podcast_guid") == by_hand and data["show"].get("site") == "studio"
            and data["show"].get("show") == show and "# AUTHOR TO CONFIRM: owner_email" in C.read_text(reg), out)
    show_part = F.skeleton_parts()[0].split("\n")
    verdict("the register keeps every line of the skeleton's [show] table, comments included",
            all(ln.split("=")[0] in C.read_text(reg) for ln in show_part), show_part)
    code, out = cli("feed", "new", show, "--feed-url", url)
    verdict("feed new refuses a show that exists (exit 2)", code == 2 and "exists" in out, out)
    for piece in ("031-episode-one", "032-episode-two"):
        (C.path(C.PIECES) / piece).mkdir(parents=True, exist_ok=True)
        cli("feed", "add", show, "--piece", piece)
    data = C.load_toml(reg)
    rows = data.get("episode", [])
    verdict("feed add appends one planned row per piece, each guid the UUIDv5 of the piece in the show's GUID",
            len(rows) == 2 and rows[0]["guid"] == F.uuid5_by_hand(by_hand, "031-episode-one")
            and rows[1]["status"] == "planned", rows)
    code, out = cli("feed", "add", show, "--piece", "031-episode-one")
    verdict("feed add refuses a piece already in the register (exit 2)", code == 2 and "already" in out, out)
    code, out = cli("feed", "add", show, "--piece", "039-no-such-piece")
    verdict("feed add refuses a piece with no folder: a GUID is for life (exit 2)", code == 2, out)
    code, out = cli("feed", "new", show, "--feed-url", "https://www.example.com/podcast/fixture-show/rss.xml",
                    "--rekey")
    data = C.load_toml(reg)
    verdict("feed new --rekey rewrites the feed URL and every GUID while nothing is published",
            code == 0 and data["show"]["feed_url"].endswith("/rss.xml") and data["show"]["podcast_guid"] != by_hand
            and data["episode"][0]["guid"] == F.episode_guid(data["show"]["podcast_guid"], "031-episode-one"), out)
    cli("feed", "new", show, "--feed-url", url, "--rekey")
    # M5: the feed audio, encoded from a picture master (a talk as an episode), untagged.
    renders = C.path(C.PUB_RENDERS)
    for piece, hz in (("031-episode-one", 330), ("032-episode-two", 440)):
        master = C.path(C.PROD_RENDERS) / piece / f"{piece}.master.mp4"
        master.parent.mkdir(parents=True, exist_ok=True)
        lavfi("-f", "lavfi", "-i", "testsrc2=size=320x180:rate=25:duration=3", "-f", "lavfi", "-i",
              f"sine=frequency={hz}:sample_rate=48000:duration=3", "-c:v", "libx264", "-preset", "ultrafast",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-metadata", "title=master title", master)
        code, out = cli("encode", master, "--deliverable", "podcast.feed_audio")
    audio = renders / "031-episode-one" / "031-episode-one.podcast-feed-audio.mp3"
    info = C.probe(audio) if audio.is_file() else {}
    tags = {k.lower(): v for k, v in info.get("format", {}).get("tags", {}).items()}
    verdict("encode to podcast.feed_audio from a picture master: sound only, MP3, untagged, at the podcast target, "
            "in the piece's folder of publishing/src/renders/ (D64)",
            code == 0 and info and not C.streams(info, "video") and C.streams(info, "audio")[0]["codec_name"] == "mp3"
            and "title" not in tags and "podcast target" in out and F.id3_version_of(audio) == 3, out + str(tags))
    # The show's covers: design exports encoded with image (test_web made them, or make them now).
    if not (renders / "fixture-show.podcast-id3-cover.jpg").is_file():
        lavfi("-f", "lavfi", "-i", "color=c=0x204060:s=1400x1400", "-frames:v", "1", renders / "fixture-show.podcast-id3-cover.jpg")
    lavfi("-f", "lavfi", "-i", "color=c=0x204060:s=3000x3000", "-frames:v", "1", renders / "fixture-show.podcast-cover.jpg")
    before, held = audio.read_bytes(), C.read_text(reg)
    code, out = cli("feed", "tag", show, "--piece", "031-episode-one")
    verdict("feed tag of a row with no title or description is exit 1, changing nothing",
            code == 1 and "title is empty" in out and audio.read_bytes() == before and C.read_text(reg) == held, out)
    code, out = cli("feed", "tag", show, "--piece", "039-not-a-row")
    verdict("feed tag of a piece with no row is exit 2, naming feed add", code == 2 and "feed add" in out, out)
    text = C.read_text(reg)
    text = F.edit(text, "show", FEED_SHOW)
    text = set_description(text, "show", "Short talks on running a small business by the water.\n"
                                         "For owners with no time to spare.")
    text = "\n".join(ln for ln in text.split("\n") if "AUTHOR TO CONFIRM" not in ln)
    for n, (piece, title, when) in enumerate((("031-episode-one", "Why the ferry runs late", "05/10/2026 09:00"),
                                              ("032-episode-two", "What the tide owes us", "12/10/2026 09:00")), start=1):
        text = F.edit(text, "episode", {"title": title, "number": n, "pub_date": when,
                                        "page": f"https://www.example.com/podcast/fixture-show/{piece}/",
                                        "transcript": f"{piece}.en-GB.vtt"}, piece=piece)
        text = set_description(text, piece, "Every crossing waits for the tide, not the timetable.\n"
                                             "This episode uses a synthetic voice for the narrator.")
    text = text.replace('notes = ""\n\n# [[episode.chapter]]', 'notes = ""\n\n[[episode.chapter]]\nstart = "00:00:00.000"\n'
                        'title = "The Hook"\n\n[[episode.chapter]]\nstart = "00:00:01.000"\ntitle = "The Tide"\n\n'
                        '[[episode.chapter]]\nstart = "00:00:02.000"\ntitle = "What Next"\n\n# [[episode.chapter]]', 1)
    write(reg, text)
    code, out = cli("feed", "tag", show, "--piece", "031-episode-one")
    proc = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
                           "-show_chapters", str(audio)], capture_output=True, text=True)
    tagged = json.loads(proc.stdout) if proc.returncode == 0 else {}
    tags = {k.lower(): v for k, v in tagged.get("format", {}).get("tags", {}).items()}
    row = C.load_toml(reg)["episode"][0]
    verdict("feed tag writes ID3v2.3 title, author, album, track, three chapters and the cover, the audio stream "
            "unchanged, and writes render, bytes and seconds into the row",
            code == 0 and tags.get("title") == "Why the ferry runs late" and tags.get("artist") == "Harbour Lane Studio"
            and tags.get("album") == "Harbour Lane Talks" and tags.get("track") == "1"
            and len(tagged.get("chapters", [])) == 3 and F.id3_version_of(audio) == 3
            and any(s.get("disposition", {}).get("attached_pic") for s in tagged.get("streams", []))
            and abs(C.duration(tagged) - C.duration(info)) < 0.05 and row["bytes"] == audio.stat().st_size
            and row["render"] == audio.name and abs(row["seconds"] - C.duration(tagged)) < 0.01, out + str(row))
    cli("feed", "tag", show, "--piece", "032-episode-two")
    code, out = cli("feed", "chapters", show, "--piece", "031-episode-one")
    chapters = renders / "031-episode-one" / "031-episode-one.chapters.json"
    doc = json.loads(C.read_text(chapters)) if code == 0 and chapters.is_file() else {}
    verdict("feed chapters writes Podcasting 2.0 JSON chapters (startTime in float seconds), in the piece's folder",
            code == 0 and doc.get("version") == "1.2" and [c["startTime"] for c in doc.get("chapters", [])]
            == [0.0, 1.0, 2.0], out)
    code, out = cli("feed", "check", show)
    verdict("feed check of a complete register is exit 0 (short chapters only warn)",
            code == 0 and "chapter_min_seconds" in out, out)
    code, out = cli("feed", "write", show, "--as-of", "05/10/2026 09:00")
    verdict("feed write leaves out a row that is not ready (exit 1, nothing written)",
            code == 1 and "ready" in out, out)
    write(reg, C.read_text(reg).replace('status = "planned"', 'status = "ready"'))
    code, out = cli("feed", "write", show)
    verdict("feed write without --as-of is exit 2: no clock is read", code == 2, out)
    code, first, err = cli_split("feed", "write", show, "--as-of", "05/10/2026 09:00")
    code2, again, _ = cli_split("feed", "write", show, "--as-of", "05/10/2026 09:00")
    try:
        feed = ET.fromstring(first.encode("utf-8"))
    except ET.ParseError as e:
        feed = None
        err += str(e)
    ns = F.NS
    item = feed.find("channel/item") if feed is not None else None
    ok = feed is not None and item is not None and all(feed.find(p, ns) is not None for p in (
        "channel/title", "channel/link", "channel/description", "channel/language", "channel/itunes:author",
        "channel/itunes:image", "channel/itunes:category", "channel/itunes:explicit", "channel/podcast:guid",
        "channel/itunes:owner/itunes:email", "channel/atom:link"))
    verdict("feed write --as-of: well-formed RSS with every required tag, the same bytes twice, only the episodes "
            "out by then, an RFC 2822 date in the project's zone, plain text and &#xA9;",
            code == 0 and code2 == 0 and first == again and ok and len(feed.findall("channel/item")) == 1
            and item.find("pubDate").text == "Mon, 05 Oct 2026 09:00:00 +0100"
            and item.find("guid").get("isPermaLink") == "false" and "&#xA9;" in first
            and item.find("enclosure").get("length") == str(audio.stat().st_size)
            and item.find("podcast:transcript", ns) is not None and item.find("psc:chapters", ns) is not None,
            first[-1200:] + err)
    upload = renders / f"{show}.feed.xml"
    code, out = cli("feed", "write", show, "--as-of", "12/10/2026 09:00", "-o", upload)
    write(reg, C.read_text(reg).replace('status = "ready"', 'status = "published"'))
    code2, out2 = cli("feed", "write", show, "--as-of", "12/10/2026 09:00", "-o", tracked)
    verdict("feed write -o: the upload copy into renders/, then the tracked copy, byte for byte the same",
            code == 0 and code2 == 0 and tracked.read_bytes() == upload.read_bytes()
            and C.read_text(tracked).count("<item>") == 2, out + out2)
    write(reg, F.edit(C.read_text(reg), "show", {"title": "Harbour Lane Talks Weekly"}))
    code, out = cli("feed", "write", show, "--as-of", "12/10/2026 09:00", "-o", tracked)
    verdict("feed write -o the tracked copy replaces it after a register change (the D59 feed exception)",
            code == 0 and "Talks Weekly" in C.read_text(tracked), out)
    code, out = cli("feed", "write", show, "--as-of", "12/10/2026 09:00", "-o", reg.with_name("CLAUDE.md"))
    verdict("feed write -o never overwrites any other tracked file (exit 2)", code == 2 and "never" in out, out)
    code, out = cli("feed", "check", show)
    verdict("feed check against the tracked feed is exit 0", code == 0, out)
    code, out = cli("feed", "new", show, "--feed-url", url, "--rekey")
    verdict("feed new --rekey is refused once a row is published (exit 2)", code == 2 and "published" in out, out)
    held, sound = C.read_text(reg), audio.read_bytes()

    def mutate(label, change, expect, write_too=False):
        write(reg, change(held))
        try:
            code, out = cli("feed", "check", show)
            ok = code == 1 and expect in out
            if write_too:
                kept = tracked.read_bytes()
                code2, out2 = cli("feed", "write", show, "--as-of", "12/10/2026 09:00", "-o", tracked)
                ok = ok and code2 == 1 and "nothing written" in out2 and tracked.read_bytes() == kept
                out += out2
            verdict(f"feed check fails {label} (exit 1)" + (", and feed write writes nothing" if write_too else ""),
                    ok, out)
        finally:
            write(reg, held)
            audio.write_bytes(sound)
    g1 = C.load_toml(reg)["episode"][0]["guid"]
    g2 = C.load_toml(reg)["episode"][1]["guid"]
    mutate("a repeated GUID", lambda t: t.replace(f'guid = "{g2}"', f'guid = "{g1}"'), "share the GUID")
    mutate("a GUID vanished from the tracked feed while its row is not withdrawn",
           lambda t: t.replace(f'guid = "{g2}"', f'guid = "{F.episode_guid(g1, "a retyped guid")}"'),
           "in no row of the register", write_too=True)
    write(reg, F.edit(held, "episode", {"status": "withdrawn"}, piece="032-episode-two"))
    code, out = cli("feed", "write", show, "--as-of", "12/10/2026 09:00")
    verdict("a withdrawn row leaves the feed, and its GUID's absence is no finding", code == 0
            and g2 not in out and g1 in out, out[-600:])
    write(reg, held)

    def retitled(t):
        t = t.replace('title = "Why the ferry runs late"', 'title = "Why the ferry always runs late"')
        write(reg, t)
        cli("feed", "tag", show, "--piece", "031-episode-one")
        return C.read_text(reg)
    mutate("an enclosure whose length changed under the same URL (a file tagged again)", retitled,
           "publish a corrected file under a new URL", write_too=True)
    mutate("a '<' in a title", lambda t: t.replace('title = "What the tide owes us"', 'title = "What the <tide>"'),
           "'<' or '>'")
    mutate("bytes that differ from the render", lambda t: t.replace(f"bytes = {audio.stat().st_size}",
                                                                   f"bytes = {audio.stat().st_size + 7}"),
           "is " + str(audio.stat().st_size) + " bytes")
    mutate("an AUTHOR TO CONFIRM flag left in the register",
           lambda t: t.replace("[show]\n", "[show]\n# AUTHOR TO CONFIRM: the category\n"), "AUTHOR TO CONFIRM")
    code, out = cli("feed", "check", show, "--feed", tracked)
    verdict("feed check --feed validates a saved feed offline", code == 0 and "nothing is fetched" in out, out)
    # A render an earlier release left flat (DESIGN D65): feed check reads it, naming it in a warning;
    # feed tag never tags it, and exits 2 naming the encode that makes it in the piece's folder.
    flat, kept = renders / audio.name, C.read_text(reg)
    os.replace(audio, flat)
    try:
        code, out = cli("feed", "check", show)
        verdict("feed check reads an episode's render an earlier release left flat, where the piece's folder has "
                "none, and names it in a warning (D65)",
                code == 0 and "warning:" in out and f"the flat {C.shown(flat)}" in out, out)
        size = flat.stat().st_size
        write(reg, kept.replace(f"bytes = {size}", f"bytes = {size + 7}"))
        code, out = cli("feed", "check", show)
        verdict("feed check compares bytes with that flat render, so a published episode is never left unchecked",
                code == 1 and f"is {size} bytes" in out and f"the flat {C.shown(flat)}" in out, out)
        write(reg, kept)
        before = flat.read_bytes()
        code, out = cli("feed", "tag", show, "--piece", "031-episode-one")
        verdict("feed tag refuses a render missing from the piece's folder (exit 2), naming the encode that makes "
                "it and the flat file, which it never tags (D65)",
                code == 2 and "--deliverable podcast.feed_audio" in out and f"the flat {C.shown(flat)}" in out
                and flat.read_bytes() == before and C.read_text(reg) == kept and not audio.exists(), out)
    finally:
        write(reg, kept)
        os.replace(flat, audio)


if __name__ == "__main__":
    sys.exit(main())
