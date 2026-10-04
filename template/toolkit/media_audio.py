#!/usr/bin/env python3
"""media_audio.py: audio extraction, loudness, the audiobook route and take naming for media.py.

Not run directly: python3 toolkit/media.py extract-audio, loudness …, audiobook … and take add
call it, and media.py's self-test exercises it.

Loudness (DESIGN D24): two-pass EBU R128 loudnorm, always with -ar on the output (loudnorm
works at 192 kHz inside). social is the house target of platforms.toml [house]; podcast is
[platform.podcast.apple_rss_audio]; acx masters to about -20 LUFS and -3.5 dBTP, inside the
window of [audiobook.acx], which is then checked as ACX measures it: RMS, sample peak and the
noise floor (the quietest 0.5 s window, windows of digital silence below -90 dB left out, so a
padded file is measured by its own recording; never astats' own trough).

The audiobook route (DESIGN D23): 'audiobook text' turns a chapter in syntek-author's markup
into plain spoken text (section markers, comments, citation keys and Pandoc divs and spans
removed, a scene break turned into {pause 2}, footnotes dropped or inlined, the brand's
pronunciations applied) and writes chunks at paragraph boundaries under the model's character
limit into the audiobook folder's generated/ (git-ignored; chapter text never goes into a
tracked file); it lists every constructed-language span, Greek or Hebrew word, scripture
reference, bare citation key and abbreviation with no spoken form, and every table and image,
which it leaves out (a table read cell by cell is a run of words and dashes; Pandoc reads an
image as '[alt]', and a square bracket is an Eleven v4 audio tag, so no chunk keeps one). A
chunk ends at every {pause N} (a scene break's {pause 2} included), and the mark never reaches
the text: the pause after each chunk is recorded in the sidecar <piece>.chNN.chunks.toml beside
the chunks. The credits are chapters ch00 (opening) and ch99 (closing), read from their own
files, <piece>.ch00.md and <piece>.ch99.md beside the chapter register: an audiobook has no
script (DESIGN D23). 'audiobook text' and 'audiobook master' both refuse a chapter register
whose channels name anything but the store part of an [audiobook.<store>] key of platforms.toml
(acx, google_play, …; DESIGN Section 6.7). 'audiobook master' joins the takes (in the sidecar's
chunk order, with exactly its room tone after each chunk, when the takes are named
<piece>.chNN.pNN.tN), adds head and tail room tone and encodes 192 kbps CBR, 44.1 kHz, mono
MP3. Room tone is the room's own, never digital silence where a room can be heard: --room-tone
FILE, else the quietest stretch of the takes, looped; and 'audiobook check' fails a file whose
head or tail is digital silence; the mastered chapter is what M4 needs approved and archived
(DESIGN D52). 'audiobook check' measures any MP3 against [audiobook.acx].

'take add' (DESIGN D21, D44) renames a fresh ElevenLabs file to its permanent name at once (the
server names files by the second and can overwrite one), writes the register and appends the
credits-log row. A pcm_* take is headerless 16-bit little-endian mono in a file the server names
.mp3: it is renamed .pcm and read with the register's sample rate (VERIFY the raw layout on
first use). An audiobook's output format is the chapter register's output_format, else the
Output format of its voice_use row in brand/src/voice/voice.md.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import tempfile
from pathlib import Path

import media_common as C

ACX_HEAD, ACX_TAIL = 1.5, 2.0
MODEL_LIMITS = {   # characters per request (ElevenLabs documentation, 03/10/2026; VERIFY on change)
    "eleven_v4": 10000, "eleven_v4_turbo": 10000, "eleven_v3": 5000,
    "eleven_multilingual_v2": 10000, "eleven_flash_v2_5": 40000, "eleven_turbo_v2_5": 40000,
}
DEFAULT_LIMIT = 5000
IPA_MODELS = {"eleven_v4", "eleven_v4_turbo"}   # read inline IPA between slashes (VERIFY on change)
SCENE = "QQSCENEBREAKQQ"   # a placeholder no chapter carries
USE_PANDOC = True   # the self-test turns it off to prove the plain fallback
BOOKS = ("Genesis|Gen|Exodus|Exod|Ex|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Joshua|Josh|"
         "Judges|Judg|Ruth|Samuel|Sam|Kings|Kgs|Chronicles|Chron|Chr|Ezra|Nehemiah|Neh|Esther|"  # scrub: allow — the books of Samuel, not a person
         "Esth|Job|Psalms|Psalm|Pss|Ps|Proverbs|Prov|Ecclesiastes|Eccles|Eccl|Song of Songs|"
         "Song of Solomon|Song|Isaiah|Isa|Jeremiah|Jer|Lamentations|Lam|Ezekiel|Ezek|Daniel|Dan|"
         "Hosea|Hos|Joel|Amos|Obadiah|Obad|Jonah|Micah|Mic|Nahum|Nah|Habakkuk|Hab|Zephaniah|"
         "Zeph|Haggai|Hag|Zechariah|Zech|Malachi|Mal|Matthew|Matt|Mt|Mark|Mk|Luke|Lk|John|Jn|"
         "Acts|Romans|Rom|Corinthians|Cor|Galatians|Gal|Ephesians|Eph|Philippians|Phil|"
         "Colossians|Col|Thessalonians|Thess|Timothy|Tim|Titus|Philemon|Phlm|Hebrews|Heb|James|"
         "Jas|Peter|Pet|Jude|Revelation|Rev")
SCRIPTURE_RE = re.compile(rf"\b(?:[1-3]\s?)?(?:{BOOKS})\.?\s\d{{1,3}}:\d{{1,3}}"
                          r"(?:\s?[-–]\s?\d{1,3}(?::\d{1,3})?)?")
GREEK_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff][\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f']*")
HEBREW_RE = re.compile(r"[\u0590-\u05ff\ufb1d-\ufb4f][\u0590-\u05ff\ufb1d-\ufb4f'\"]*")
CITEKEY_RE = re.compile(r"(?<![\w.@])@([A-Za-z0-9_][\w:.#$%&+?<>~/-]*[A-Za-z0-9_])")
# An abbreviation: a run of capitals and digits holding two capitals or more (HLS, BBC, MP3, IV),
# with an optional plural s. A model may spell it, say it as a word or guess.
ABBREV_RE = re.compile(r"(?<![\w'’])(?=[A-Z0-9]*[A-Z][A-Z0-9]*[A-Z])[A-Z0-9]{2,}s?(?![\w'’])")
IMAGE_RE = re.compile(r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\](?:\(([^()\s]*)[^()]*\)|\[[^\]]*\])(?:\{[^{}]*\})?")
HTML_IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
PIPE_RULE_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$|^\s*\|\s*:?-{3,}:?\s*\|\s*$")
GRID_RULE_RE = re.compile(r"^\s*\+(?:[-=:]+\+)+\s*$")
SIMPLE_RULE_RE = re.compile(r"^\s*-{2,}(?:[ \t]+-{2,})+\s*$")
CAPTION_RE = re.compile(r"^\s*(?:Table)?:\s+(.+?)\s*$", re.S)


# ── Loudness ────────────────────────────────────────────────────────────────────────────

def has_audio(p, pcm_format=None) -> bool:
    return bool(C.streams(C.probe(p, pcm_format), "audio"))


LOUDNORM_JSON_RE = re.compile(r'\{\s*"input_i"[^{}]*\}')   # loudnorm's print_format=json block


def r128_summary(stderr: str):
    """{I, thresh, LRA, TP} from the Summary the ebur128 filter prints, or None without one."""
    if "Summary:" not in stderr:
        return None
    tail = stderr[stderr.rfind("Summary:"):]

    def grab(label):
        m = re.search(label + r"\s*(-?inf|-?[\d.]+)", tail)
        return float(m.group(1)) if m else float("nan")
    return {"I": grab(r"\bI:"), "thresh": grab(r"Threshold:"), "LRA": grab(r"LRA:"), "TP": grab(r"Peak:")}


def ebur128(p, pcm_format=None) -> dict:
    """Integrated loudness (LUFS), loudness range (LU) and true peak (dBTP)."""
    if not has_audio(p, pcm_format):
        raise C.Fatal(f"{C.shown(p)} has no audio stream")
    proc = C.ffmpeg(C.input_args(p, pcm_format) + ["-map", "0:a:0", "-af", "ebur128=peak=true",
                                                    "-f", "null", "-"], what="ebur128")
    got = r128_summary(proc.stderr)
    if got is None:
        raise C.Fatal(f"ebur128 gave no summary for {C.shown(p)}")
    return {"I": got["I"], "LRA": got["LRA"], "TP": got["TP"]}


def loudnorm_measure(p, target: tuple, lra: float = 11.0, pcm_format=None, pre: str = "") -> dict:
    """loudnorm's first pass, its programme figures taken from the ebur128 meter that also judges
    the output; pre is any filter the render applies before loudnorm (a downmix).

    loudnorm's own input_i leans towards the last seconds of a short programme (measured with
    ffmpeg 6.1: 2 s of tone then 3.6 s 10 dB quieter reads 1.3 LU below ebur128, and the reverse
    order 1 LU above), so a 6-second master ending on a quiet bed was raised 1.3 LU too far by
    the linear second pass, which applies target minus input_i. ebur128 runs in the same pass,
    before loudnorm (it passes the sound through unchanged), and its integrated loudness,
    threshold, range and true peak replace loudnorm's; loudnorm's target_offset is kept for its
    dynamic mode.

    The two filters print at the end of the run in no fixed order (ffmpeg 6.1 prints loudnorm's
    JSON first whenever a filter such as an aformat downmix stands before ebur128), so the JSON
    is found by its own keys and the meter's Summary is read from the whole log."""
    integrated, peak = target
    proc = C.ffmpeg(C.input_args(p, pcm_format) + [
        "-map", "0:a:0", "-af",
        f"{pre}ebur128=peak=true,loudnorm=I={integrated}:TP={peak}:LRA={lra}:print_format=json",
        "-f", "null", "-"], what="loudnorm measurement")
    text = proc.stderr
    found = LOUDNORM_JSON_RE.findall(text)
    try:
        data = json.loads(found[-1])
    except (IndexError, ValueError, json.JSONDecodeError):
        raise C.Fatal(f"loudnorm gave no measurement for {C.shown(p)}") from None
    meter = r128_summary(text)
    if meter and all(math.isfinite(meter[k]) for k in ("I", "thresh", "LRA", "TP")):
        data.update(input_i=f"{meter['I']:.2f}", input_thresh=f"{meter['thresh']:.2f}",
                    input_lra=f"{meter['LRA']:.2f}", input_tp=f"{meter['TP']:.2f}")
    if data.get("input_i") in ("-inf", None) or float(data["input_i"]) < -69:
        raise C.Fatal(f"{C.shown(p)} has no measurable programme loudness (silence?)")
    return data


def loudnorm_filter(m: dict, target: tuple) -> str:
    integrated, peak = target
    lra = min(50.0, max(11.0, float(m["input_lra"]) + 1.0))
    return (f"loudnorm=I={integrated}:TP={peak}:LRA={lra:.1f}:measured_I={m['input_i']}:"
            f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
            f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:"
            "print_format=summary")


def loudness_findings(p, target: tuple, name: str) -> tuple:
    """(summary, findings) for a rendered file against a loudness target: within 1 LU, under the peak."""
    got = ebur128(p)
    integrated, peak = target
    found = []
    if not abs(got["I"] - integrated) <= 1.0:
        found.append(f"integrated loudness {got['I']:.1f} LUFS is not within 1 LU of the {name} "
                     f"target {integrated:g}")
    if not got["TP"] <= peak + 0.2:
        found.append(f"true peak {got['TP']:.1f} dBTP is above the {name} ceiling {peak:g}")
    return f"{got['I']:.1f} LUFS, {got['TP']:.1f} dBTP, LRA {got['LRA']:.1f} LU", found


AUDIO_CODECS = {".mp3": ["-c:a", "libmp3lame", "-b:a", "192k"], ".m4a": ["-c:a", "aac", "-b:a", "192k"],
                ".aac": ["-c:a", "aac", "-b:a", "192k"], ".wav": ["-c:a", "pcm_s16le"],
                ".flac": ["-c:a", "flac"]}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv"}


def cmd_measure(args) -> int:
    got = ebur128(args.file)
    print(f"loudness {C.shown(args.file)}: integrated {got['I']:.1f} LUFS · true peak "
          f"{got['TP']:.1f} dBTP · loudness range {got['LRA']:.1f} LU")
    return 0


def normalise(src: Path, out: Path, name: str, data=None) -> tuple:
    """Two-pass loudnorm of src into out; (summary, findings)."""
    target = C.loudness_target(name, data)
    info = C.probe(src)
    if not C.streams(info, "audio"):
        raise C.Fatal(f"{C.shown(src)} has no audio to normalise")
    ext = out.suffix.lower()
    if ext in VIDEO_EXT:
        codec = ["-map", "0:v?", "-map", "0:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-movflags", "+faststart"]
    elif ext in AUDIO_CODECS:
        codec = ["-map", "0:a:0", "-vn"] + AUDIO_CODECS[ext]
    else:
        raise C.Fatal(f"cannot write {ext or 'a file with no extension'}: use .mp4, .wav, .mp3, .m4a or .flac")
    sr = C.streams(info, "audio")[0].get("sample_rate")
    ar = 44100 if name in ("acx", "podcast") else int(sr or 48000)
    pre = "aformat=channel_layouts=mono," if name == "acx" else ""
    m = loudnorm_measure(src, target, pre=pre)
    render(["-y"] + C.input_args(src) + ["-af", pre + loudnorm_filter(m, target), "-ar", str(ar)]
           + codec + [str(out)], out, what="loudnorm")
    return loudness_findings(out, target, name)


def render(cmd: list, out: Path, cwd=None, what="ffmpeg"):
    """Run ffmpeg; a failed run leaves no partial output behind."""
    try:
        return C.ffmpeg(cmd, cwd=cwd, what=what)
    except C.Fatal:
        if Path(out).exists() and C.in_output_folder(out):
            Path(out).unlink()
        raise


def default_out_dir(src: Path) -> Path:
    return src.resolve().parent if C.in_output_folder(src) else C.path(C.PROD_RENDERS)


def cmd_normalise(args) -> int:
    src = Path(args.file)
    stem, ext = src.name.rsplit(".", 1) if "." in src.name else (src.name, "wav")
    out = C.output_path(default_out_dir(src) / f"{stem}.{args.target}.{ext}", args.o, inputs=[src])
    summary, found = normalise(src, out, args.target)
    print(f"wrote {C.shown(out)}: {summary}")
    for f in found:
        print(f"  FAIL {f}")
    return 1 if found else 0


def cmd_extract(args) -> int:
    src = Path(args.src)
    if not has_audio(src):
        raise C.Fatal(f"{C.shown(src)} has no audio stream")
    seek, label = [], ""
    if args.cut_in is not None or args.cut_out is not None:
        if args.cut_in is None or args.cut_out is None:
            raise C.Fatal("extract-audio takes --in and --out together")
        a, b = C.parse_tc(args.cut_in), C.parse_tc(args.cut_out)
        if b <= a:
            raise C.Fatal("--out must come after --in")
        seek, label = ["-ss", C.fmt_tc(a), "-to", C.fmt_tc(b)], f".{C.tc_name(a)}-{C.tc_name(b)}"
    if not 8000 <= args.rate <= 192000:
        raise C.Fatal(f"--rate {args.rate} is not a sample rate between 8000 and 192000 Hz")
    stem = src.name.rsplit(".", 1)[0]
    out = C.output_path(C.path(C.PROD_RENDERS) / f"{stem}{label}.wav", args.o, inputs=[src])
    render(["-y"] + seek + C.input_args(src) + ["-map", "0:a:0", "-vn", "-ac", "1", "-ar",
                                                str(args.rate), "-c:a", "pcm_s16le", str(out)], out,
           what="extract-audio")
    info = C.probe(out)
    print(f"wrote {C.shown(out)}: mono 16-bit {args.rate} Hz, {C.fmt_tc(C.duration(info))}")
    return 0


# ── ACX measurement ─────────────────────────────────────────────────────────────────────

def astats_overall(p) -> tuple:
    proc = C.ffmpeg(C.input_args(p) + ["-map", "0:a:0", "-af",
                                       "astats=measure_perchannel=none:measure_overall=RMS_level+Peak_level",
                                       "-f", "null", "-"], what="astats")
    text = proc.stderr[proc.stderr.rfind("Overall"):]

    def grab(label):
        m = re.search(label + r":\s*(-?inf|-?[\d.]+)", text)
        return float(m.group(1)) if m else float("nan")
    return grab("RMS level dB"), grab("Peak level dB")


DIGITAL_SILENCE_DB = -90.0   # quieter than any room: digital silence, or nearly (MP3 makes it -100 to -140)
ROOM_TONE_MAX_DB = -45.0     # a window louder than this holds speech or a breath, not room tone
WINDOW = 0.5                 # ACX measures the noise floor over 0.5 s windows


def window_levels(p) -> list:
    """The RMS level (dB) of every 0.5 s window of a file, in order, at 44.1 kHz mono."""
    proc = C.ffmpeg(C.input_args(p) + [
        "-map", "0:a:0", "-af",
        f"aformat=channel_layouts=mono,aresample=44100,asetnsamples=n={int(44100 * WINDOW)}:p=0,"
        "astats=metadata=1:reset=1:measure_perchannel=RMS_level:measure_overall=none,"
        "ametadata=print:key=lavfi.astats.1.RMS_level:file=-", "-f", "null", "-"], what="window levels")
    return [float("-inf") if "inf" in m.group(1) else float(m.group(1))
            for m in re.finditer(r"lavfi\.astats\.1\.RMS_level=(-?inf|-?[\d.]+)", proc.stdout)]


def noise_floor(p, levels=None) -> tuple:
    """(the quietest 0.5 s window's RMS, the number of windows of digital silence left out).

    A window below DIGITAL_SILENCE_DB is digital silence, not a room: it is left out, so a file
    padded with silence is measured by its own recording, as ACX hears it."""
    levels = window_levels(p) if levels is None else levels
    real = [v for v in levels if v > DIGITAL_SILENCE_DB]
    return (min(real) if real else float("-inf")), len(levels) - len(real)


def edge_silences(p, total: float, noise_db: float = -50.0) -> tuple:
    """Seconds of near-silence at the head and the tail."""
    proc = C.ffmpeg(C.input_args(p) + ["-map", "0:a:0", "-af", f"silencedetect=noise={noise_db}dB:d=0.25",
                                       "-f", "null", "-"], what="silencedetect")
    spans, start = [], None
    for line in proc.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m and start is not None:
            spans.append((start, float(m.group(1))))
            start = None
    if start is not None:
        spans.append((start, total))
    head = next((b - a for a, b in spans if a <= 0.05), 0.0)
    tail = next((b - a for a, b in reversed(spans) if b >= total - 0.1), 0.0)
    return head, tail


def cbr(p) -> bool | None:
    """True when every MP3 frame after the first is one size (give or take a padding byte)."""
    proc = C.run([C.need("ffprobe"), "-v", "error", "-select_streams", "a:0", "-show_entries",
                  "packet=size", "-of", "csv=p=0", str(p)], what="ffprobe packets")
    sizes = [int(x) for x in proc.stdout.split() if x.strip().isdigit()][1:]
    if not sizes:
        return None
    return max(sizes) - min(sizes) <= 1


def kbps(text) -> float:
    m = re.fullmatch(r"\s*([\d.]+)\s*([kKmM]?)\s*", str(text or ""))
    if not m:
        return 0.0
    return float(m.group(1)) * {"": 0.001, "k": 1, "K": 1, "m": 1000, "M": 1000}[m.group(2)]


def acx_findings(p, table: dict) -> tuple:
    """(rows, findings, channels) for one file against [audiobook.acx]."""
    info = C.probe(p)
    audio = C.streams(info, "audio")
    if not audio:
        raise C.Fatal(f"{C.shown(p)} has no audio stream")
    a = audio[0]
    total = C.duration(info)
    rows, found = [], []

    def row(ok, text):
        rows.append(("ok  " if ok else "FAIL") + "  " + text)
        if not ok:
            found.append(text)
    sr = int(a.get("sample_rate") or 0)
    want_sr = int(table.get("audio_sample_rate", 44100))
    want_kbps = kbps(table.get("audio_bitrate", "192k"))
    got_kbps = float(a.get("bit_rate") or info.get("format", {}).get("bit_rate") or 0) / 1000
    is_cbr = cbr(p) if a.get("codec_name") == "mp3" else None
    row(a.get("codec_name") == table.get("audio_codec", "mp3"), f"codec {a.get('codec_name')} "
        f"(wants {table.get('audio_codec', 'mp3')})")
    row(sr == want_sr, f"sample rate {sr} Hz (wants {want_sr})")
    row(got_kbps >= want_kbps - 1, f"bit rate {got_kbps:.0f} kb/s (at least {want_kbps:g})")
    if table.get("cbr"):
        row(bool(is_cbr), "constant bit rate" if is_cbr else "not constant bit rate (CBR required)")
    rms, peak = astats_overall(p)
    lo, hi = table.get("rms_min_db", -23.0), table.get("rms_max_db", -18.0)
    row(lo <= rms <= hi, f"RMS {rms:.1f} dB ({lo:g} to {hi:g})")
    pmax = table.get("peak_max_db", -3.0)
    row(peak <= pmax, f"peak {peak:.1f} dB (at most {pmax:g})")
    levels = window_levels(p)
    floor, digital = noise_floor(p, levels)
    fmax = table.get("noise_floor_max_db", -60.0)
    row(floor <= fmax, f"noise floor {floor:.1f} dB (at most {fmax:g}; the quietest 0.5 s window"
        + (f", {digital} window(s) of digital silence left out)" if digital else ")"))
    head, tail = edge_silences(p, total)
    tmin, tmax = table.get("room_tone_min_seconds", 1.0), table.get("room_tone_max_seconds", 5.0)
    row(tmin <= head <= tmax and tmin <= tail <= tmax,
        f"room tone {head:.2f} s at the head, {tail:.2f} s at the tail ({tmin:g} to {tmax:g})")
    dead = [where for where, v in (("head", levels[0] if levels else 0.0), ("tail", levels[-1] if levels else 0.0))
            if v <= DIGITAL_SILENCE_DB]
    row(not dead, "the room tone is the room's own" if not dead else
        f"the {' and the '.join(dead)} {'is' if len(dead) == 1 else 'are'} digital silence, not room tone: "
        "ACX hears it as a gated or edited file (master it again with the recording's own room tone, or "
        "--room-tone FILE)")
    longest = table.get("file_max_seconds", 7200)
    row(total <= longest, f"length {C.fmt_tc(total)} (at most {longest / 60:g} minutes)")
    return rows, found, int(a.get("channels") or 0)


def cmd_ab_check(args) -> int:
    table = C.preset("audiobook.acx")
    failures, channels = 0, set()
    for f in args.files:
        rows, found, ch = acx_findings(Path(f), table)
        channels.add(ch)
        print(f"audiobook check {C.shown(f)}")
        for r in rows:
            print(f"  {r}")
        failures += bool(found)
    if len(channels) > 1:
        print(f"  FAIL the files do not share one channel layout ({', '.join(map(str, sorted(channels)))}): "
              "ACX needs all mono or all stereo")
        failures += 1
    elif channels and channels != {1}:
        print("  note: the house masters audiobooks in mono; these files are not mono")
    print(f"audiobook check: {'clean' if not failures else f'{failures} file(s) or rule(s) failed'}")
    return 1 if failures else 0


# ── audiobook text ──────────────────────────────────────────────────────────────────────

def pronunciations(ipa: bool = True) -> dict:
    """Word -> spoken form from voice.md: '/IPA/' where the model reads inline IPA, else the respelling."""
    p = C.path(C.VOICE_MD)
    if not p.is_file():
        return {}
    lines = C.read_text(p).split("\n")
    head, last = C.find_table(lines, ("Word", "IPA"))
    out = {}
    if head is None:
        return out
    for line in lines[head + 2:last + 1]:
        cells = C.split_row(line)
        if len(cells) < 3 or not cells[0] or "AUTHOR TO CONFIRM" in line:
            continue
        word, sounds, respelling = cells[0], cells[1].strip("/ "), cells[2]
        if ipa and sounds:
            out[word] = f"/{sounds}/"
        elif respelling:
            out[word] = respelling
    return out


def _footnotes(text: str, mode: str) -> str:
    defs, kept, current = {}, [], None
    for line in text.split("\n"):
        m = re.match(r"^\[\^([^\]]+)\]:\s?(.*)$", line)
        if m:
            current = m.group(1)
            defs[current] = m.group(2).strip()
            continue
        if current and re.match(r"^(?: {4}|\t)\S", line):
            defs[current] += " " + line.strip()
            continue
        current = None
        kept.append(line)
    text = "\n".join(kept)

    def note(body):
        return f" ({body.strip()})" if mode == "inline" else ""
    text = re.sub(r"\^\[((?:[^\[\]]|\[[^\[\]]*\])*)\]", lambda m: note(m.group(1)), text)
    return re.sub(r"\[\^([^\]]+)\]", lambda m: note(defs.get(m.group(1), "")), text)


def is_table(block: list) -> bool:
    """A Pandoc table: pipe, grid, simple or multiline (a line of two or more runs of dashes)."""
    if any(GRID_RULE_RE.match(ln) for ln in block):
        return True
    if any(PIPE_RULE_RE.match(ln) for ln in block) and any("|" in ln for ln in block):
        return True
    return len(block) >= 2 and any(SIMPLE_RULE_RE.match(ln) for ln in block)


def table_label(block: list, heading: str) -> str:
    """What names a table to the author: its first row's cells, after the heading it sits under."""
    row = next((ln for ln in block if ln.strip() and not (GRID_RULE_RE.match(ln) or PIPE_RULE_RE.match(ln)
                                                         or re.match(r"^\s*-{3,}\s*$", ln))), "")
    cells = [c.strip() for c in re.split(r"\||\s{2,}", row) if c.strip()]
    label = " / ".join(cells)[:60] or "a table"
    return f"{label} (under '{heading}')" if heading else label


def drop_tables(text: str, note) -> str:
    """Every table (and its caption) left out of the spoken text and listed: a table has no
    spoken form, and read cell by cell it is a run of words and dashes."""
    blocks, cur = [], []
    for line in text.split("\n"):
        if line.strip():
            cur.append(line)
        else:
            if cur:
                blocks.append(cur)
            blocks.append(None)
            cur = []
    if cur:
        blocks.append(cur)
    real = [k for k, b in enumerate(blocks) if b is not None]
    tables = {k for k in real if is_table(blocks[k])}
    out, heading = [], ""
    for n, k in enumerate(real):
        block = blocks[k]
        h = re.match(r"^\s*#{1,6}\s+(.*?)\s*#*\s*$", block[0])
        if h:
            heading = h.group(1)
        if k in tables:
            before = real[n - 1] if n > 0 else None
            after = real[n + 1] if n + 1 < len(real) else None
            cap = next((CAPTION_RE.match(" ".join(blocks[j])) for j in (after, before)
                        if j is not None and j not in tables and CAPTION_RE.match(" ".join(blocks[j]))), None)
            note("table", f"'{cap.group(1).strip()}'" if cap else table_label(block, heading))
            continue
        neighbour = {real[n - 1] if n > 0 else None, real[n + 1] if n + 1 < len(real) else None}
        if CAPTION_RE.match(" ".join(block)) and neighbour & tables:
            continue   # the table's caption goes with it
        out.append("\n".join(block))
    return "\n\n".join(out)


def drop_images(text: str, note) -> str:
    """Every image left out of the spoken text and listed by its alt text (Pandoc reads an image
    as '[alt]', and square brackets are the audio-tag syntax of Eleven v4)."""
    def image(m):
        note("image", f"'{m.group(1).strip()}'" if m.group(1).strip() else (m.group(2) or "an image"))
        return ""

    def html(m):
        alt = re.search(r'\balt\s*=\s*"([^"]*)"', m.group(0), re.I)
        note("image", f"'{alt.group(1)}'" if alt and alt.group(1) else "an <img> with no alt text")
        return ""
    return HTML_IMG_RE.sub(html, IMAGE_RE.sub(image, text))


def spoken_text(source: str, footnotes: str, sayings: dict) -> tuple:
    """(plain spoken text, unspoken items) from a chapter in syntek-author's markup.

    Listed, never sent as they stand: constructed-language spans, Greek and Hebrew words,
    scripture references, bare citation keys, tables (left out), images and charts (left out),
    abbreviations with no row in voice.md's Pronunciations, and any square bracket left in the
    text, which the text never keeps (Eleven v4 reads [words] as an audio tag)."""
    _, body, _ = C.split_frontmatter(source)
    text = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    text = _footnotes(text, footnotes)
    unspoken = []

    def note(kind, item):
        if item not in sayings and (kind, item) not in unspoken:
            unspoken.append((kind, item))
    text = drop_images(drop_tables(text, note), note)
    out = []
    for line in text.split("\n"):
        div = re.match(r"^\s*:{3,}\s*(.*?)\s*:*\s*$", line)
        if div:
            if "scene-break" in div.group(1):
                out += ["", SCENE, ""]
            continue
        if re.match(r"^\s*(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$", line) and \
                not (out and out[-1].strip() and re.fullmatch(r"\s*-+\s*", line)):
            out += ["", SCENE, ""]   # a rule; a line of dashes under text is a setext heading's
            continue
        out.append(line)
    text = "\n".join(out)

    def span(m):
        words, attrs = m.group(1), m.group(2)
        classes = re.findall(r"\.([\w-]+)", attrs)
        lang = re.search(r"lang=([\w-]+)", attrs)
        if any(c in ("conlang", "conlang-native") for c in classes):
            note("constructed", words)
        elif lang and lang.group(1) in ("grc", "el", "hbo", "he"):
            note("greek" if lang.group(1) in ("grc", "el") else "hebrew", words)
        return words
    text = re.sub(r"\[([^\[\]]+)\]\{([^{}]*)\}", span, text)
    text = re.sub(r"[ \t]*\[(?:[^\[\]]*?;\s*)?-?@[A-Za-z0-9_][^\[\]]*\](?![({])", "", text)
    for m in CITEKEY_RE.finditer(text):
        note("citation key", "@" + m.group(1))
    for m in GREEK_RE.finditer(text):
        note("greek", m.group(0))
    for m in HEBREW_RE.finditer(text):
        note("hebrew", m.group(0))
    for m in SCRIPTURE_RE.finditer(text):
        note("scripture", m.group(0))
    said = re.sub(r"\]\([^)]*\)|<[^<>\s]+>|`[^`]*://[^`]*`", " ", text.replace(SCENE, " "))
    for m in ABBREV_RE.finditer(said):
        note("abbreviation", m.group(0))
    if USE_PANDOC and shutil.which("pandoc"):
        proc = C.run(["pandoc", "-f", "markdown-smart", "-t", "plain", "--wrap=none"], what="pandoc",
                     input_text=text)
        text = proc.stdout
    else:
        text = plain_markdown(text)
    for word in sorted(sayings, key=len, reverse=True):
        text = re.sub(rf"(?<![\w/]){re.escape(word)}(?![\w/])", sayings[word], text)
    paras = []
    for block in re.split(r"\n\s*\n", text):
        para = re.sub(r"\s+", " ", block).strip()
        if para:
            paras.append("{pause 2}" if SCENE in para else para)
    while paras and paras[0] == "{pause 2}":
        paras.pop(0)
    while paras and paras[-1] == "{pause 2}":
        paras.pop()
    collapsed = []
    for para in paras:
        if not (para == "{pause 2}" and collapsed and collapsed[-1] == para):
            collapsed.append(para)
    text = "\n\n".join(collapsed)
    for m in re.finditer(r"\[[^\[\]]*\]|[\[\]]", text):
        note("brackets", m.group(0))
    return re.sub(r"[ \t]{2,}", " ", re.sub(r"[\[\]]", "", text)), unspoken


def plain_markdown(text: str) -> str:
    """What 'pandoc -t plain' does to the Markdown a chapter uses, when pandoc is absent."""
    out = []
    for line in text.split("\n"):
        h = re.match(r"^\s*#{1,6}\s+(.*?)\s*#*\s*$", line)
        if h:
            out += ["", h.group(1), ""]
            continue
        if re.fullmatch(r"\s*(?:=+|-+)\s*", line) and out and out[-1].strip():
            out += [""]   # a setext heading's underline
            continue
        line = re.sub(r"^\s*>\s?", "", line)
        line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"(?m)^ {0,3}\[[^\]]+\]:\s+\S.*$", "", text)   # a reference link's definition
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m.group(1) or m.group(2), text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\\([\\`*_{}\[\]()#+\-.!>~|])", r"\1", text)


def chunk_paragraphs(text: str, limit: int) -> list:
    """Chunks under limit, split at paragraph boundaries (a long paragraph at sentence ones)."""
    units = []
    for para in text.split("\n\n"):
        if len(para) <= limit:
            units.append(para)
            continue
        cur = ""
        for sentence in re.split(r"(?<=[.!?…])\s+", para):
            while len(sentence) > limit:
                cut = sentence.rfind(" ", 0, limit)
                cut = cut if cut > 0 else limit
                if cur:
                    units.append(cur)
                    cur = ""
                units.append(sentence[:cut])
                sentence = sentence[cut:].strip()
            trial = f"{cur} {sentence}".strip()
            if len(trial) <= limit:
                cur = trial
            else:
                units.append(cur)
                cur = sentence
        if cur:
            units.append(cur)
    chunks, cur = [], ""
    for u in units:
        trial = f"{cur}\n\n{u}" if cur else u
        if len(trial) <= limit:
            cur = trial
        else:
            chunks.append(cur)
            cur = u
    if cur:
        chunks.append(cur)
    return chunks


def chapter_id(text: str) -> str:
    m = re.fullmatch(r"ch(\d+)", str(text).strip().lower())
    if not m:
        raise C.Fatal(f"chapter {text!r} is not chNN")
    return f"ch{int(m.group(1)):02d}"


def part_id(text: str) -> str:
    m = re.fullmatch(r"p(\d+)", str(text).strip().lower())
    if not m:
        raise C.Fatal(f"part {text!r} is not pNN")
    return f"p{int(m.group(1)):02d}"


def segment_id(text: str) -> str:
    m = re.fullmatch(r"s(\d+)", str(text).strip().lower())
    if not m:
        raise C.Fatal(f"segment {text!r} is not sNN")
    return f"s{int(m.group(1)):02d}"


def chapter_register(piece: str) -> Path:
    return C.path(C.AUDIOBOOK) / f"{piece}.md"


def chapter_model(piece: str) -> str:
    reg = chapter_register(piece)
    if reg.is_file():
        return str(C.split_frontmatter(C.read_text(reg))[0].get("model_id", "") or "")
    return ""


def model_limit(piece: str) -> tuple:
    model = chapter_model(piece)
    if model in MODEL_LIMITS:
        return MODEL_LIMITS[model], f"the limit of {model}"
    return DEFAULT_LIMIT, ("a cautious default: the chapter register names no model it knows"
                           if not model else f"a cautious default: {model} is not in the toolkit's list")


def chapter_channels(piece: str) -> list:
    """The chapter register's channels, each the store part of an [audiobook.<store>] key of
    platforms.toml (DESIGN Section 6.7); any other name is refused (exit 2)."""
    reg = chapter_register(piece)
    if not reg.is_file():
        return []
    raw = C.split_frontmatter(C.read_text(reg))[0].get("channels", []) or []
    names = [str(c).strip() for c in (raw if isinstance(raw, list) else [raw]) if str(c).strip()]
    stores = list(C.load_toml(C.PLATFORMS_TOML).get("audiobook", {}))
    bad = [n for n in names if n not in stores]
    if bad:
        raise C.Fatal(f"{C.shown(reg)}: channels {', '.join(repr(b) for b in bad)} "
                      f"{'names' if len(bad) == 1 else 'name'} no [audiobook.<store>] table of "
                      "toolkit/data/platforms.toml: write each channel as the store part of its key "
                      f"({', '.join(stores)})")
    return names


CREDITS = {"ch00": "opening credits", "ch99": "closing credits"}   # the chapter IDs of the credit files
PAUSE_MARK_RE = re.compile(r"\{\s*pause\s+(\d*\.?\d+)\s*\}", re.I)


def h2_sections(text: str) -> dict:
    """Each '## Heading' of a Markdown file (lower case) -> the lines under it."""
    out, current = {}, None
    for line in text.split("\n"):
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            current = h.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return out


def chapter_source(src: Path, ch: str, piece: str) -> str:
    """The text audiobook text reads: the chapter's own source, or for ch00 and ch99 the credits'
    own file, <piece>.ch00.md or <piece>.ch99.md beside the chapter register (DESIGN D23, Section
    6.7: an audiobook has no script). A credits file named for one chapter is refused for another,
    and a file shaped like a script's chapter plan is refused outright."""
    raw = C.read_text(src)
    named = re.fullmatch(rf"{re.escape(piece)}\.(ch\d+)\.md", src.name)
    if named and named.group(1) != ch:
        what = CREDITS.get(named.group(1), f"chapter {named.group(1)}")
        raise C.Fatal(f"{C.shown(src)} is the {what} of {piece}: run it as --chapter {named.group(1)}")
    if ch in CREDITS and not named:
        print(f"  note: {ch} is the {CREDITS[ch]}; its source is normally {piece}.{ch}.md beside the "
              f"chapter register in {C.AUDIOBOOK}/, and {C.shown(src)} is read as given")
    sections = h2_sections(raw)
    if "chapters" in sections and any(k in sections for k in CREDITS.values()):
        raise C.Fatal(f"{C.shown(src)} is shaped like an audiobook script (a chapter plan with credits "
                      "sections), and an audiobook has no script: each chapter is read from its own "
                      f"source, and the credits from {piece}.ch00.md and {piece}.ch99.md beside the "
                      "chapter register")
    return raw


def split_at_pauses(text: str) -> list:
    """[(text, pause after it)]: the text cut at every {pause N}, which never reaches ElevenLabs."""
    parts = PAUSE_MARK_RE.split(text)
    segments = []
    for k in range(0, len(parts), 2):
        body = parts[k].strip()
        pause = float(parts[k + 1]) if k + 1 < len(parts) else 0.0
        if body:
            segments.append([body, pause])
        elif segments:
            segments[-1][1] += pause
    if segments:
        segments[-1][1] = 0.0   # the tail's room tone follows the last chunk
    return [(body, pause) for body, pause in segments]


def sidecar_path(piece: str, ch: str) -> Path:
    return C.path(C.AB_GENERATED) / f"{piece}.{ch}.chunks.toml"


def write_sidecar(piece: str, ch: str, src: Path, rows: list) -> Path:
    """The chunk sidecar: every chunk file in reading order with the pause after it."""
    lines = [f"# {piece}.{ch}.chunks.toml: written by 'python3 toolkit/media.py audiobook text', read by",
             "# 'audiobook master'. One [[chunk]] per text chunk, in reading order; pause_after is the room",
             "# tone, in seconds, the master puts after that chunk's take (a scene break, or a pause mark,",
             "# which never reaches ElevenLabs as text). Generated: never hand-edit; make the chunks again.",
             f"piece = {toml_str(piece)}", f"chapter = {toml_str(ch)}", f"source = {toml_str(C.shown(src))}", ""]
    for part, name, chars, pause in rows:
        lines += ["[[chunk]]", f"part = {toml_str(part)}", f"file = {toml_str(name)}",
                  f"characters = {chars}", f"pause_after = {pause:.3f}", ""]
    side = sidecar_path(piece, ch)
    side.write_text("\n".join(lines), encoding="utf-8")
    return side


def cmd_ab_text(args) -> int:
    src = Path(args.source)
    ch = chapter_id(args.chapter)
    limit, why = (args.limit, "--limit") if args.limit else model_limit(args.piece)
    if limit < 200:
        raise C.Fatal("--limit below 200 characters would split sentences everywhere")
    chapter_channels(args.piece)
    model = chapter_model(args.piece)
    source = chapter_source(src, ch, args.piece)
    text, unspoken = spoken_text(source, args.footnotes, pronunciations(ipa=model in IPA_MODELS))
    if not text.strip():
        raise C.Fatal(f"{C.shown(src)} has no spoken text")
    chunks = []
    for body, pause in split_at_pauses(text):
        pieces = chunk_paragraphs(body, limit)
        chunks += [(c, pause if k == len(pieces) - 1 else 0.0) for k, c in enumerate(pieces)]
    gen = C.path(C.AB_GENERATED)
    gen.mkdir(parents=True, exist_ok=True)
    for old in list(gen.glob(f"{args.piece}.{ch}.p*.txt")) + [sidecar_path(args.piece, ch)]:
        if old.exists():
            old.unlink()
    print(f"audiobook text {C.shown(src)} → {args.piece} {ch} (footnotes {args.footnotes}; "
          f"limit {limit:,} characters: {why}; pronunciations as "
          f"{'inline IPA' if model in IPA_MODELS else 'respellings'})")
    rows = []
    for k, (chunk, pause) in enumerate(chunks, start=1):
        out = gen / f"{args.piece}.{ch}.p{k:02d}.txt"
        out.write_text(chunk + "\n", encoding="utf-8")
        rows.append((f"p{k:02d}", out.name, len(chunk), pause))
        print(f"  p{k:02d}  {len(chunk):>7,} characters  {C.shown(out)}"
              + (f"  then {pause:g} s of room tone" if pause else ""))
    side = write_sidecar(args.piece, ch, src, rows)
    print(f"  total {sum(len(c) for c, _ in chunks):,} characters in {len(chunks)} chunk(s); "
          f"the pauses between them are in {C.shown(side)}, never in the text")
    if unspoken:
        print("Words and references with no spoken form (add a row to the Pronunciations table of "
              "brand/src/voice/voice.md, or settle them with the author, before any call):")
        for kind, item in unspoken:
            print(f"  {kind:<13} {item}")
        return 1
    return 0


# ── audiobook master ────────────────────────────────────────────────────────────────────

def chapter_row(piece: str, ch: str):
    reg = chapter_register(piece)
    if not reg.is_file():
        return None, None, None
    lines = C.read_text(reg).split("\n")
    head, last = C.find_table(lines, ("Ch", "Title"))
    if head is None:
        return lines, None, None
    names = [c.lower() for c in C.split_row(lines[head])]
    for i in range(head + 2, last + 1):
        cells = C.split_row(lines[i])
        if cells and re.fullmatch(r"(?:ch)?0*(\d+)", cells[0].lower() or "x") and \
                int(re.sub(r"\D", "", cells[0])) == int(ch[2:]):
            return lines, i, dict(zip(names, cells))
    return lines, None, None


def piece_title(piece: str) -> str:
    brief = C.path(C.PIECES) / piece / "brief.md"
    if brief.is_file():
        return str(C.split_frontmatter(C.read_text(brief))[0].get("title", "") or piece)
    return piece


def cmd_ab_master(args) -> int:
    ch = chapter_id(args.chapter)
    takes = [Path(t) for t in args.chunks]
    for t in takes:
        if not t.is_file():
            raise C.Fatal(f"not found: {C.shown(t)}")
    for label, value in (("--head", args.head), ("--tail", args.tail)):
        if not 0 <= value <= 10:
            raise C.Fatal(f"{label} {value:g} s is outside 0 to 10 seconds")
    chapter_channels(args.piece)
    _, _, row = chapter_row(args.piece, ch)
    title = (row or {}).get("title") or (CREDITS[ch].capitalize() if ch in CREDITS else f"Chapter {int(ch[2:])}")
    takes, pauses = sidecar_pauses(args.piece, ch, takes)
    out = C.output_path(C.path(C.AB_RENDERS) / f"{args.piece}.{ch}.mp3", args.o, inputs=takes)
    with tempfile.TemporaryDirectory(prefix="media-ab-") as tmp:
        joined = Path(tmp) / "joined.wav"
        tone, said = room_tone(takes, args.room_tone, Path(tmp))
        print(f"  room tone: {said}")
        # head, then each take followed by its pause, then the tail: every gap is room tone
        order = [("tone", args.head)]
        for k in range(len(takes)):
            order += [("take", k), ("tone", pauses[k])]
        order[-1] = ("tone", args.tail)
        cmd, chains, labels = ["-y"], [], []
        for k, t in enumerate(takes):
            cmd += C.input_args(t)
            chains.append(f"[{k}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono[c{k}]")
        n = len(takes)
        for j, (what, value) in enumerate(order):
            if what == "take":
                labels.append(f"[c{value}]")
                continue
            if value <= 0:
                continue
            if tone is not None:
                cmd += ["-stream_loop", "-1", "-t", f"{value:.3f}", "-i", str(tone)]
                chains.append(f"[{n}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,"
                              f"atrim=duration={value:.6f},asetpts=PTS-STARTPTS[r{j}]")
                n += 1
            else:
                chains.append(f"anullsrc=r=44100:cl=mono,atrim=duration={value:.6f},"
                              f"aformat=sample_fmts=fltp:channel_layouts=mono[r{j}]")
            labels.append(f"[r{j}]")
        graph = ";".join(chains) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]"
        render(cmd + ["-filter_complex", graph, "-map", "[out]", "-ac", "1", "-ar", "44100",
                      "-c:a", "pcm_s16le", str(joined)], joined, what="joining the takes")
        target = C.loudness_target("acx")
        m = loudnorm_measure(joined, target)
        tags = ["-id3v2_version", "3", "-metadata", f"title={title}", "-metadata",
                f"album={piece_title(args.piece)}"]
        if ch not in CREDITS:
            tags += ["-metadata", f"track={int(ch[2:])}"]
        if not C.BRAND_NAME.startswith("<"):
            tags += ["-metadata", f"artist={C.BRAND_NAME}"]
        render(["-y", "-i", str(joined), "-af", loudnorm_filter(m, target), "-ar", "44100", "-ac", "1",
                "-c:a", "libmp3lame", "-b:a", "192k"] + tags + [str(out)], out, what="ACX master")
    inner = [f"{p:g} s after {Path(t).name}" for t, p in zip(takes, pauses) if p > 0]
    print(f"wrote {C.shown(out)} from {len(takes)} take(s): head {args.head:g} s, tail {args.tail:g} s"
          + (f"; room tone {', '.join(inner)}" if inner else ""))
    rows, found, _ = acx_findings(out, C.preset("audiobook.acx", quiet=True))
    for r in rows:
        print(f"  {r}")
    print(f"audiobook master: {'passes the ACX check' if not found else 'FAILS the ACX check'}")
    print("  next: the author listens to the chapter through; once it is approved, archive this master "
          "(M4 needs the mastered chapter approved and archived, DESIGN D52): python3 toolkit/media.py "
          f"footage add {C.shown(out)} --kind generated --location LABEL (--kind audio for the master "
          "of a human recording). Archiving its chunk takes as well is allowed, never required.")
    return 1 if found else 0


def room_tone(takes: list, given, tmp: Path) -> tuple:
    """(a WAV of room tone, or None; what it is) for the head, the tail and every pause.

    Never digital silence where the room can be heard: --room-tone FILE (a recording of the
    room) when given, else the quietest stretch of the takes themselves (up to 3 s of 0.5 s
    windows within 3 dB of the quietest, between DIGITAL_SILENCE_DB and ROOM_TONE_MAX_DB), which
    the master loops. With neither, the gaps are digital silence and the ACX check says so."""
    out = tmp / "room-tone.wav"
    if given:
        g = Path(given)
        if not g.is_file():
            raise C.Fatal(f"not found: {C.shown(g)} (--room-tone)")
        if not has_audio(g):
            raise C.Fatal(f"{C.shown(g)} has no audio stream (--room-tone)")
        render(["-y"] + C.input_args(g) + ["-map", "0:a:0", "-t", "30", "-ac", "1", "-ar", "44100",
                                           "-c:a", "pcm_s16le", str(out)], out, what="room tone")
        floor, _ = noise_floor(out)
        if floor == float("-inf"):
            raise C.Fatal(f"{C.shown(g)} is digital silence: --room-tone takes a recording of the room")
        return out, f"--room-tone {C.shown(g)} ({floor:.1f} dB), looped for the head, the tail and every pause"
    best = None
    for t in takes:
        levels = window_levels(t)
        for k, v in enumerate(levels):
            if DIGITAL_SILENCE_DB < v <= ROOM_TONE_MAX_DB and (best is None or v < best[0]):
                n = 1
                while k + n < len(levels) and n < 6 and DIGITAL_SILENCE_DB < levels[k + n] <= v + 3:
                    n += 1
                best = (v, t, k * WINDOW, n * WINDOW)
    if best is None:
        return None, ("none found: every quiet stretch of the takes is digital silence, or none is "
                      f"quieter than {ROOM_TONE_MAX_DB:g} dB, so the head, the tail and the pauses are "
                      "digital silence, which the ACX check fails; record 5 to 10 s of the room and pass "
                      "--room-tone FILE")
    level, t, start, length = best
    render(["-y", "-ss", f"{start:.3f}", "-t", f"{length:.3f}"] + C.input_args(t)
           + ["-map", "0:a:0", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(out)], out, what="room tone")
    return out, (f"the quietest {length:g} s of {Path(t).name}, at {C.fmt_tc(start)} ({level:.1f} dB), "
                 "looped for the head, the tail and every pause")


def sidecar_pauses(piece: str, ch: str, takes: list) -> tuple:
    """(takes in chunk order, the room tone after each) from the chunk sidecar of 'audiobook text'.

    Without a sidecar, or for takes not named <piece>.chNN.pNN.tN (a human recording), the takes
    are joined as given with no pause between them. With one, every chunk needs exactly one take.
    """
    side = sidecar_path(piece, ch)
    plain = (takes, [0.0] * len(takes))
    if not side.is_file():
        return plain
    rx = re.compile(rf"^{re.escape(piece)}\.{ch}\.(p\d+)\.t\d+\.\w+$")
    found = [rx.match(Path(t).name) for t in takes]
    if not all(found):
        print(f"  note: {C.shown(side)} lists this chapter's text chunks, but these takes are not all "
              f"named {piece}.{ch}.pNN.tN, so no pause from it is put between them")
        return plain
    order = [(str(c.get("part", "")), float(c.get("pause_after", 0) or 0))
             for c in C.load_toml(side).get("chunk", [])]
    by_part = {}
    for t, m in zip(takes, found):
        part = m.group(1)
        if part in by_part:
            raise C.Fatal(f"two takes for {part}: {Path(by_part[part]).name} and {Path(t).name}; give "
                          "only the approved take of each part")
        by_part[part] = t
    known = [part for part, _ in order]
    stray = [part for part in by_part if part not in known]
    if stray:
        raise C.Fatal(f"{', '.join(stray)} is not a chunk listed in {C.shown(side)}: make the chunks "
                      "again with 'audiobook text', or give this chapter's takes")
    missing = [part for part in known if part not in by_part]
    if missing:
        raise C.Fatal(f"no take given for {', '.join(missing)} of {ch}: {C.shown(side)} lists "
                      f"{len(known)} chunk(s), and every one needs its approved take")
    ordered = [by_part[part] for part in known]
    if [Path(t).name for t in ordered] != [Path(t).name for t in takes]:
        print(f"  note: the takes are joined in chunk order, as {C.shown(side)} lists them")
    return ordered, [pause for _, pause in order]


# ── take add ────────────────────────────────────────────────────────────────────────────

def toml_str(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def set_toml_fields(text: str, table: str, match: tuple, updates: dict) -> str:
    """Rewrite fields of the [[table]] whose match[0] equals match[1]; add missing ones."""
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.strip() == f"[[{table}]]"]
    for k, s in enumerate(starts):
        end = next((i for i in range(s + 1, len(lines)) if lines[i].lstrip().startswith("[")), len(lines))
        block = lines[s + 1:end]
        key_re = re.compile(rf"^\s*{re.escape(match[0])}\s*=\s*(.+?)\s*(?:#.*)?$")
        hit = next((key_re.match(b) for b in block if key_re.match(b)), None)
        if not hit or hit.group(1).strip().strip('"\'') != match[1]:
            continue
        for key, value in updates.items():
            new = f"{key} = {value}"
            for i in range(s + 1, end):
                m = re.match(rf"^(\s*){re.escape(key)}\s*=", lines[i])
                if m:
                    comment = re.search(r"\s+#[^\"]*$", lines[i])
                    lines[i] = m.group(1) + new + (comment.group(0) if comment else "")
                    break
            else:
                insert = end
                while insert > s + 1 and not lines[insert - 1].strip():
                    insert -= 1
                lines.insert(insert, new)
                end += 1
        return "\n".join(lines)
    raise C.Fatal(f"no [[{table}]] with {match[0]} = \"{match[1]}\"")


def next_take(folder: Path, prefix: str) -> int:
    numbers = [int(m.group(1)) for f in folder.glob(f"{prefix}.t*.*")
               if (m := re.match(rf"^{re.escape(prefix)}\.t(\d+)\.", f.name))]
    return max(numbers, default=0) + 1


def voice_name(use: str) -> str:
    return C.voice_row(use).get("voice") or use or ""


def extension_for(fmt: str) -> str:
    fmt = str(fmt or "mp3_44100_128")
    if fmt.startswith("pcm_"):
        return ".pcm"
    if fmt.startswith("mp3_"):
        return ".mp3"
    raise C.Fatal(f"output_format {fmt!r}: the toolkit names and reads mp3_* and pcm_* takes only")


def cmd_take_add(args) -> int:
    src = Path(args.file)
    if not src.is_file():
        raise C.Fatal(f"not found: {C.shown(src)}")
    if not C.in_output_folder(src) or "generated" not in src.resolve().parent.parts:
        raise C.Fatal(f"{C.shown(src)} is not in a generated/ folder: every ElevenLabs call passes "
                      "an absolute output_directory inside one")
    piece = args.piece
    if args.segment:
        if args.chapter or args.part:
            raise C.Fatal("take add takes --segment, or --chapter with --part, not both")
        sid = segment_id(args.segment)
        reg = C.path(C.VOICEOVER) / f"{piece}.toml"
        data = C.load_toml(reg)
        head = data.get("voiceover", {})
        seg = next((s for s in data.get("segment", []) if str(s.get("id")) == sid), None)
        if seg is None:
            raise C.Fatal(f"{C.shown(reg)} has no [[segment]] with id = \"{sid}\"")
        folder = C.path(C.VO_GENERATED)
        prefix = f"{piece}.{sid}"
        fmt = head.get("output_format", "mp3_44100_128")
        chars = int(seg.get("characters") or 0) or len(str(seg.get("request") or seg.get("text") or ""))
        voice, model, note = voice_name(head.get("voice_use", "")), head.get("model_id", ""), f"segment {sid}"
    else:
        if not (args.chapter and args.part):
            raise C.Fatal("take add needs --segment sNN, or --chapter chNN with --part pNN")
        ch, part = chapter_id(args.chapter), part_id(args.part)
        reg = chapter_register(piece)
        if not reg.is_file():
            raise C.Fatal(f"not found: {C.shown(reg)} (the chapter register)")
        meta = C.split_frontmatter(C.read_text(reg))[0]
        folder = C.path(C.AB_GENERATED)
        prefix = f"{piece}.{ch}.{part}"
        fmt, fmt_from = C.chapter_format(piece)
        print(f"  output format {fmt}, from {fmt_from}")
        chunk = folder / f"{prefix}.txt"
        chars = len(C.read_text(chunk).strip()) if chunk.is_file() else 0
        voice, model, note = voice_name(str(meta.get("voice_use", ""))), meta.get("model_id", ""), f"{ch} {part}"
        lines, row_index, _ = chapter_row(piece, ch)
        if row_index is None:
            raise C.Fatal(f"{C.shown(reg)} has no row for {ch}")
    if src.resolve().parent != folder.resolve():
        raise C.Fatal(f"{C.shown(src)} is not in {C.shown(folder)}, where takes for this register live")
    ext = extension_for(fmt)
    n = next_take(folder, prefix)
    dest = folder / f"{prefix}.t{n}{ext}"
    while dest.exists():
        n += 1
        dest = folder / f"{prefix}.t{n}{ext}"
    src.rename(dest)
    print(f"renamed {C.shown(src)} → {C.shown(dest)}")
    if args.segment:
        rel = dest.relative_to(C.path(C.VOICEOVER)).as_posix()
        text = set_toml_fields(C.read_text(reg), "segment", ("id", sid),
                               {"take": n, "file": toml_str(rel), "status": toml_str("generated"),
                                "archived": toml_str("")})
        reg.write_text(text, encoding="utf-8")
        print(f"wrote take = {n}, file = \"{rel}\" and status = \"generated\" for {sid} in {C.shown(reg)}")
    else:
        lines, row_index, _ = chapter_row(piece, ch)
        names = [c.lower() for c in C.split_row(lines[C.find_table(lines, ('Ch', 'Title'))[0]])]
        cells = C.split_row(lines[row_index])
        cells += [""] * (len(names) - len(cells))
        if "takes" in names:
            k = names.index("takes")
            entries = [e.strip() for e in cells[k].split(",") if e.strip() and not e.strip().startswith(part)]
            cells[k] = ", ".join(entries + [f"{part}.t{n}"])
        if "status" in names and cells[names.index("status")] in ("", "planned"):
            cells[names.index("status")] = "generated"
        lines[row_index] = "| " + " | ".join(C.cell(c) for c in cells) + " |"
        reg.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {part}.t{n} into the {ch} row of {C.shown(reg)}")
    log = C.path(C.CREDITS_LOG)
    if not log.is_file():
        raise C.Fatal(f"not found: {C.shown(log)}: the take is renamed and the register written, "
                      "but the credits-log row is not: add it by hand")
    C.append_table_row(log, ("Date", "Piece", "Tool"),
                       [C.today(), piece, "text_to_speech", 1, f"{chars} characters", voice, model,
                        dest.resolve().relative_to(C.path("production/src").resolve()).as_posix(),
                        note + (f"; {fmt}" if ext == ".pcm" else "")])
    print(f"appended the credits-log row to {C.shown(log)} ({chars} characters)")
    return 0
