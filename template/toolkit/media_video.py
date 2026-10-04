#!/usr/bin/env python3
"""media_video.py: the master, the deliverables and stills for media.py.

Not run directly: python3 toolkit/media.py assemble, cut, encode, frame and still-video call it,
and media.py's self-test exercises it.

assemble builds a master from an edit decision list, production/src/edits/<piece>.toml (DESIGN
Section 6.4), with ffmpeg's own filters only: a [[clip]] is a video or audio source cut
frame-accurately by its in and out (decoded and re-encoded, never stream-copied), a still or a
card held for its seconds (an image looped, then trimmed), or a solid colour; a clip may enter
with transition = "fade" (xfade, and acrossfade for its sound), and a still or card may carry
motion = "push-in" (a slow zoompan). A GIF or WebP holding one frame is a still; one holding
more (a screen recording saved as a GIF) is moving media, cut by its in and out like a video,
and a moving WebP is refused, named, where ffmpeg cannot decode it (6.1 cannot). frame says how
a source fills the master's size: fit (letterboxed), crop (to fill; x is the left edge in source
pixels) or pad (over a blurred copy of itself). A card under production/src/cards/ is rendered
to production/src/renders/ with 'uv run toolkit/card.py' whenever its PNG is missing or older
than its HTML or tokens.css. [[overlay]] lays a card (rendered with alpha) or a still image over
the picture between two timecodes. [[audio]] places sound on the timeline: vo:<piece> joins the
segments of production/src/voiceover/<piece>.toml with their pause_after, and refuses the master
while any segment is not approved (its line would be skipped); a footage ID or an asset path may
take an in and out range, gain, fades, and duck = true to sit under the voice (sidechaincompress;
a ducked track is music). With size = "" the master is audio only (.wav) and takes sound from
every clip. A clip's out may not pass the end of its source. The picture's frame rate is the
first video clip's; an animated GIF's only where no other clip has one, rounded to a whole
number (GIF frame delays are centiseconds); 30 where there is none; a rate that is not standard
(a variable-rate recording) is snapped to the nearest of 23.976, 24, 25, 29.97, 30, 50, 59.94 and
60. A clip with no sound (a screen recording) is silence under the [[audio]] tracks. Loudness
goes to the edit's target by two-pass loudnorm, and the master is probed before it is reported.

cut and encode make one deliverable of toolkit/data/platforms.toml (brand overrides applied)
from moving media (a video, a screen recording, an animated GIF; a still image is refused): size
by crop (centred, or from --x) or a blurred pad (encode asks for --frame whenever the source's
shape differs from the deliverable's, and never crops unasked), H.264 with faststart and closed
GOPs, AAC; no -r unless the source exceeds the table's fps_max (or runs at a rate the table's
fps_allowed does not list, when it is snapped to the nearest one it does). cut seeks before the
input and re-encodes, so it is frame-accurate; with --captions it burns them in the same pass
with -copyts, the SRT timed to SRC, or to the cut when its name carries --cNN (captions with no
cue, an empty cue or overlapping cues are refused before anything renders; any other breach of
the house limits is a warning); with --overlay it lays a transparent PNG of exactly the
deliverable's size over every frame, under the captions. A deliverable with no picture (kind =
"audio": a podcast clip, an audiobook retail sample, a podcast feed's audio) is trimmed and
encoded as sound only, from a picture master too (a talk published as a podcast episode takes
its sound); a cut of an audiobook.<store> key is its retail sample, held to the store's
sample_max_seconds rather than the whole book's limits. A table that sets id3_version
(podcast.feed_audio) is written untagged: the source's tags and chapters are dropped, and the
feed's own are 'feed tag's, at M7 (DESIGN D59). A table with audio_tracks = 0
(website.hero_loop) gets no sound track at all, and its verification fails a file that has one
(DESIGN D57). cut of a kind = "image" table whose only format is gif (newsletter.preview_gif)
is the GIF pass of media_image.py; any other image table is refused (card.py renders it, and
media.py image encodes it).

In an edit decision list, x = 0 (the skeleton's default) means a centred crop; a crop from a
chosen left edge gives that edge in source pixels, 1 or more.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import media_common as C
import media_audio as A

IMAGE_EXT = C.IMAGE_EXT
FRAMES = ("fit", "crop", "pad")
ROLES = ("voice", "music", "effect")
# The standard picture rates a master and a deliverable run at: a source with any other rate (a
# variable-frame-rate phone clip, an OBS or browser capture) is snapped to the nearest of these.
STANDARD_FPS = ("24000/1001", "24", "25", "30000/1001", "30", "50", "60000/1001", "60")


def warn(text: str) -> None:
    """A note for the author on stderr, so a command whose product goes to stdout keeps it clean."""
    print(text, file=sys.stderr)


def is_standard(rate: float) -> bool:
    """Within 0.03% of a standard rate: close enough for a rounded rational, never 29.97 for 30."""
    return any(abs(rate - C.rate(s)) <= C.rate(s) * 0.0003 for s in STANDARD_FPS)


def standard_rate(*candidates) -> str:
    """The first candidate rate that is standard, as its rational; else the standard rate nearest
    the first usable candidate (avg_frame_rate before r_frame_rate); 30 when none is usable."""
    for text in candidates:
        r = C.rate(text)
        for s in STANDARD_FPS:
            if r > 0 and abs(r - C.rate(s)) <= C.rate(s) * 0.0003:
                return s
    r = next((C.rate(t) for t in candidates if 0 < C.rate(t) <= 240), 30.0)
    return min(STANDARD_FPS, key=lambda s: abs(C.rate(s) - r))


# ── The edit decision list ──────────────────────────────────────────────────────────────

def parse_size(text):
    text = str(text or "").strip()
    if not text:
        return None
    m = re.fullmatch(r"(\d+)\s*[xX×]\s*(\d+)", text)
    if not m or int(m.group(1)) % 2 or int(m.group(2)) % 2:
        raise C.Fatal(f"size {text!r} is not WIDTHxHEIGHT with even numbers")
    return int(m.group(1)), int(m.group(2))


def load_edl(p: Path) -> dict:
    data = C.load_toml(p)
    edit = data.get("edit")
    if not isinstance(edit, dict) or not edit.get("piece"):
        raise C.Fatal(f"{C.shown(p)} has no [edit] table with a piece")
    if str(edit.get("loudness", "social")) not in ("social", "podcast", "none"):
        raise C.Fatal(f"{C.shown(p)}: loudness must be social, podcast or none")
    clips = []
    for n, c in enumerate(data.get("clip", []), start=1):
        c = dict(c)
        c.setdefault("id", f"c{n:02d}")
        frame = str(c.get("frame", "fit") or "fit")
        motion = str(c.get("motion", "none") or "none")
        transition = str(c.get("transition", "cut") or "cut")
        if frame not in FRAMES or motion not in ("none", "push-in") or transition not in ("cut", "fade"):
            raise C.Fatal(f"{C.shown(p)} clip {c['id']}: frame is fit|crop|pad, motion none|push-in, "
                          "transition cut|fade")
        c.update(frame=frame, motion=motion, transition=transition)
        clips.append(c)
    return {"edit": edit, "clip": clips, "overlay": data.get("overlay", []),
            "audio": data.get("audio", []), "path": p}


def manifest_entries() -> dict:
    p = C.path(C.MANIFEST)
    if not p.is_file():
        return {}
    return {str(e.get("id")): e for e in C.load_toml(p).get("file", [])}


def source_kind(p: Path, logged_kind: str = "", logged_duration: float = 0.0) -> str:
    """still or media. An image is a still when it holds one frame; a GIF or WebP with more
    frames (a screen recording saved as a GIF) is moving media, cut by in and out like a video.
    The file is probed where it is present; where it is not, the manifest's kind and duration
    decide (an image kind, or an image file logged with no duration, is a still)."""
    ext = p.suffix.lower()
    if ext not in IMAGE_EXT:
        return "media"
    if p.is_file():
        return "still" if C.is_still(p) else "media"
    if logged_kind == "image" or ext not in C.ANIMATED_EXT or not logged_duration:
        return "still"
    return "media"


def resolve_source(source: str, entries: dict) -> dict:
    """{kind: media|still|card, path, label, duration} for a clip or audio source."""
    source = str(source).strip()
    if re.fullmatch(r"F\d{4,}", source):
        e = entries.get(source)
        if e is None:
            return {"kind": "missing", "label": f"{source} (not in production/src/footage/manifest.toml)"}
        p = C.path(C.FOOTAGE) / str(e.get("path", ""))
        logged = float(e.get("duration") or 0)
        kind = source_kind(p, str(e.get("kind", "")), logged)
        if kind == "media" and e.get("kind") == "image" and p.suffix.lower() not in C.ANIMATED_EXT:
            kind = "still"
        return {"kind": kind, "path": p, "label": source, "duration": logged if kind == "media" else 0.0}
    p = C.path(source) if not Path(source).is_absolute() else Path(source)
    if p.suffix.lower() == ".html":
        return {"kind": "card", "path": p, "label": source, "duration": 0.0}
    return {"kind": source_kind(p), "path": p, "label": source, "duration": 0.0}


def timeline(edl: dict, check_files: bool = False) -> list:
    """Every clip with its kind, source path, in, duration and start on the master."""
    entries = manifest_entries()
    out, missing, acc = [], [], 0.0
    for c in edl["clip"]:
        cid = c["id"]
        colour = str(c.get("colour", "") or "").strip()
        source = str(c.get("source", "") or "").strip()
        item = {"id": cid, "clip": c, "source": source, "in": 0.0}
        if colour and not source:
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", colour):
                raise C.Fatal(f"clip {cid}: colour {colour!r} is not #RRGGBB")
            item.update(kind="colour", colour=colour)
            dur = float(c.get("seconds", 0) or 0)
            if dur <= 0:
                raise C.Fatal(f"clip {cid} lasts {dur:g} s: give a colour clip its seconds")
        elif not source:
            raise C.Fatal(f"clip {cid} names neither a source nor a colour")
        else:
            r = resolve_source(source, entries)
            exists = r["kind"] != "missing" and r["path"].is_file()
            lost = r["kind"] == "missing" or (check_files and not exists)
            if lost:
                missing.append(r["label"] if r["kind"] == "missing" else f"{source} ({C.shown(r['path'])})")
            kind = "media" if r["kind"] == "missing" else r["kind"]
            item.update(kind=kind, path=r.get("path"))
            if kind == "media":
                a = C.parse_tc(c.get("in") or 0, f"clip {cid} in")
                length = None
                if exists:
                    item["info"] = C.probe(r["path"])
                    length = C.duration(item["info"])
                if c.get("out"):
                    b = C.parse_tc(c["out"], f"clip {cid} out")
                elif length:
                    b = length
                elif r.get("duration"):
                    b = r["duration"]
                else:
                    b = a
                if length and (b > length + 0.05 or a >= length):
                    edge = "in" if a >= length else "out"
                    raise C.Fatal(f"clip {cid}: {edge} {C.fmt_tc(a if edge == 'in' else b)} is past the end "
                                  f"of {source} ({C.shown(r['path'])} lasts {C.fmt_tc(length)}); ffmpeg "
                                  "would hold its last frame for the difference")
                item["in"] = a
                dur = b - a
            else:
                dur = float(c.get("seconds", 0) or 0)
            if dur <= 0 and lost:
                dur = 0.0
            elif dur <= 0:
                raise C.Fatal(f"clip {cid} lasts {dur:g} s: give a media clip its in and out, and a "
                              "still, card or colour clip its seconds")
        fade = float(c.get("transition_seconds", 0) or 0) if c["transition"] == "fade" else 0.0
        start = acc
        if out and fade > 0:
            asked = fade
            fade = min(fade, out[-1]["dur"] * 0.99, dur * 0.99, acc)
            if fade < asked - 1e-6:
                warn(f"  note: clip {cid}: transition_seconds {asked:g} is longer than this clip or the one "
                     f"before it; the fade lasts {fade:.3f} s")
            start = acc - fade
        item.update(dur=dur, start=start, fade=fade)
        acc = start + dur
        out.append(item)
    if check_files and missing:
        raise C.Fatal("the edit decision list names source media this project does not have: "
                      + "; ".join(dict.fromkeys(missing)) + ". Log each with 'media.py footage add', or mirror it into "
                      "production/src/footage/raw/ and run 'media.py footage verify'")
    return out


# ── Encoding, verification and reporting ────────────────────────────────────────────────

def even(n: float) -> int:
    n = int(round(n))
    return n - (n % 2)


def reframe(inp: str, out: str, sw: int, sh: int, w: int, h: int, mode: str, x, uid: str) -> list:
    """Filter statements taking [inp] at sw x sh to [out] at w x h."""
    if abs(sw / sh - w / h) < 0.005:
        return [f"[{inp}]scale={w}:{h},setsar=1[{out}]"]
    if mode == "fit":
        return [f"[{inp}]scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1[{out}]"]
    if mode == "pad":
        return [f"[{inp}]split=2[bg{uid}][fg{uid}]",
                f"[bg{uid}]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
                f"gblur=sigma=40,eq=brightness=-0.08[bb{uid}]",
                f"[fg{uid}]scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2[fs{uid}]",
                f"[bb{uid}][fs{uid}]overlay=(W-w)/2:(H-h)/2,setsar=1[{out}]"]
    aspect = w / h
    if sw / sh > aspect:
        cw, ch = min(sw, even(sh * aspect)), sh
        cx = (sw - cw) // 2 if x is None else max(0, min(int(x), sw - cw))
        cy = 0
    else:
        cw, ch = sw, min(sh, even(sw / aspect))
        cx, cy = 0, (sh - ch) // 2
    return [f"[{inp}]crop={cw}:{ch}:{cx}:{cy},scale={w}:{h},setsar=1[{out}]"]


def video_codec_args(table: dict, fps: float) -> list:
    args = ["-c:v", "libx264", "-preset", C.X264_PRESET, "-crf", "20", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-bf", "2", "-flags", "+cgop"]
    if fps > 0:
        args += ["-g", str(max(1, round(fps * 2)))]
    cap = table.get("video_bitrate_max") or table.get("video_bitrate")
    if cap:
        args += ["-maxrate", str(cap), "-bufsize", f"{int(A.kbps(cap) * 2)}k"]
    return args


def audio_codec(table: dict) -> str:
    """A deliverable's audio codec: audio_codec, else the first of audio_formats, else mp3 for an
    audiobook store and aac for anything else."""
    formats = table.get("audio_formats") or []
    return str(table.get("audio_codec") or (formats[0] if formats else "")
               or ("mp3" if table["key"].startswith("audiobook.") else "aac"))


def sample_table(table: dict) -> dict:
    """A cut of an audiobook key is a retail sample: limited by sample_max_seconds, never by the
    whole book's min_seconds and max_seconds."""
    if not table["key"].startswith("audiobook."):
        return table
    sample = dict(table)
    sample.pop("min_seconds", None)
    sample.pop("max_seconds", None)
    if table.get("sample_max_seconds"):
        sample["max_seconds"] = table["sample_max_seconds"]
        print(f"  note: a cut of {table['key']} is its retail sample: at most sample_max_seconds "
              f"{table['sample_max_seconds']:g}")
    else:
        print(f"  note: {table['key']} gives no sample_max_seconds: the sample's length is not checked")
    return sample


def audio_codec_args(table: dict) -> list:
    """Codec, bit rate, rate and channels for a deliverable's sound."""
    codec = audio_codec(table)
    rate = str(table.get("audio_sample_rate") or (48000 if table.get("kind") == "video" else 44100))
    channels = ["-ac", "1" if table["key"].startswith("audiobook.") else "2"]   # audiobooks: mono, the house choice
    if codec == "mp3":
        out = ["-c:a", "libmp3lame", "-b:a", str(table.get("audio_bitrate", "192k"))]
    elif codec == "flac":
        out = ["-c:a", "flac"]
    elif codec in ("wav", "pcm"):
        out = ["-c:a", "pcm_s16le"]
    else:
        out = ["-c:a", "aac", "-b:a", str(table.get("audio_bitrate", "192k"))]
    return out + ["-ar", rate] + channels


def faststart(ext: str) -> list:
    return ["-movflags", "+faststart"] if ext in (".mp4", ".m4a", ".mov") else []


def untagged(table: dict) -> list:
    """A table that sets id3_version (podcast.feed_audio) is written untagged, in that ID3 version:
    the source's tags and chapters dropped, because the feed's own are 'feed tag's (DESIGN D59)."""
    if not table.get("id3_version"):
        return []
    return ["-map_metadata", "-1", "-map_chapters", "-1", "-id3v2_version", str(int(table["id3_version"])),
            "-write_id3v1", "0"]


def audio_ext(table: dict) -> str:
    return {"mp3": ".mp3", "flac": ".flac", "wav": ".wav", "pcm": ".wav"}.get(audio_codec(table), ".m4a")


def render(cmd: list, out: Path, cwd=None, what="ffmpeg"):
    return A.render(cmd, out, cwd=cwd, what=what)


def verify(out: Path, table: dict, expect: float | None = None) -> list:
    """Findings for a rendered deliverable against its table."""
    info = C.probe(out)
    found = []
    v, a = C.streams(info, "video"), C.streams(info, "audio")
    dur = C.duration(info)
    kind = table.get("kind")
    if kind == "video":
        if not v:
            return ["it has no picture"]
        size = C.size_of(table)
        got = (int(v[0].get("width", 0)), int(v[0].get("height", 0)))
        if size and got != size:
            found.append(f"picture is {got[0]}x{got[1]}; {table['key']} wants {size[0]}x{size[1]}")
        if table.get("video_codec") and v[0].get("codec_name") != table["video_codec"]:
            found.append(f"video codec {v[0].get('codec_name')}; {table['key']} wants {table['video_codec']}")
        if v[0].get("pix_fmt") != "yuv420p":
            found.append(f"pixel format {v[0].get('pix_fmt')}; wants yuv420p")
        fps = C.rate(v[0].get("avg_frame_rate") or v[0].get("r_frame_rate"))
        if table.get("fps_max") and fps > table["fps_max"] + 0.01:
            found.append(f"{fps:.2f} fps is above fps_max {table['fps_max']}")
        allowed = table.get("fps_allowed") or []
        if allowed and fps > 0 and not rate_allowed(fps, allowed):
            found.append(f"{fps:.3f} fps is not one of {table['key']} fps_allowed "
                         f"({', '.join(f'{a:g}' for a in allowed)})")
        if table.get("container") == "mp4" and C.moov_first(out) is not True:
            found.append("the moov box is not at the front (no faststart)")
    if a and table.get("audio_codec") and a[0].get("codec_name") != table["audio_codec"]:
        found.append(f"audio codec {a[0].get('codec_name')}; {table['key']} wants {table['audio_codec']}")
    if kind == "audio" and not a:
        found.append("it has no sound")
    if C.silent(table) and a:
        found.append(f"it has a sound track; {table['key']} sets audio_tracks = 0 (no sound track at all)")
    if a and table.get("cbr") and a[0].get("codec_name") == "mp3" and A.cbr(out) is False:
        found.append(f"its bit rate is not constant; {table['key']} sets cbr = true")
    if table.get("max_seconds") and dur > table["max_seconds"] + 0.05:
        found.append(f"lasts {dur:.3f} s; {table['key']} max_seconds is {table['max_seconds']:g}")
    if table.get("min_seconds") and dur < table["min_seconds"] - 0.05:
        found.append(f"lasts {dur:.3f} s; {table['key']} min_seconds is {table['min_seconds']:g}")
    if expect is not None and abs(dur - expect) > max(0.1, expect * 0.002):
        found.append(f"lasts {dur:.3f} s where {expect:.3f} s was expected")
    limit = C.max_bytes(table.get("max_size"))
    if limit and out.stat().st_size > limit:
        found.append(f"{out.stat().st_size / 1e6:.1f} MB is over max_size {table['max_size']}")
    for key in table.get("verify", []) or []:
        if key in ("width", "height", "max_seconds", "safe_zone", "caption_formats", "audio_codec"):
            print(f"  note: {table['key']} {key} is unconfirmed (verify): re-check it before publishing")
    return found


def rate_allowed(fps: float, allowed: list) -> bool:
    """True when fps is one of the allowed rates, an NTSC rate (29.97 for 30) counting as its own."""
    return any(abs(fps - a) <= a * 0.002 or abs(fps - a / 1.001) <= a * 0.002 for a in map(float, allowed))


def describe(p: Path, pcm_format=None) -> str:
    info = C.probe(p, pcm_format)
    parts = []
    for s in C.streams(info, "video"):
        parts.append(f"{s.get('width')}x{s.get('height')} {s.get('codec_name')} {s.get('pix_fmt')} "
                     f"{C.rate(s.get('avg_frame_rate') or s.get('r_frame_rate')):.3g} fps")
    for s in C.streams(info, "audio"):
        br = s.get("bit_rate")
        parts.append(f"{s.get('codec_name')} {s.get('sample_rate')} Hz {s.get('channels')} ch"
                     + (f" {int(br) // 1000} kb/s" if br and str(br).isdigit() else ""))
    size = p.stat().st_size
    parts.append(C.fmt_tc(C.duration(info)))
    parts.append(f"{size / 1e6:.1f} MB" if size >= 1e5 else f"{size / 1e3:.0f} kB")
    if p.suffix.lower() in (".mp4", ".mov", ".m4v", ".m4a"):
        parts.append("moov first" if C.moov_first(p) else "moov last")
    return " · ".join(parts)


def print_summary(p: Path) -> None:
    print(f"  probe: {describe(p)}")


def finish(out: Path, found: list, label: str) -> int:
    print_summary(out)
    for f in found:
        print(f"  FAIL {f}")
    print(f"{label} {C.shown(out)}: {'verified' if not found else f'{len(found)} finding(s)'}")
    return 1 if found else 0


def deliverable_name(src: Path, key: str, cut: str | None, burned: bool, ext: str) -> str:
    piece = C.piece_of(src)
    return f"{piece}{'--' + cut if cut else ''}.{C.file_form(key)}{'.burned' if burned else ''}{ext}"


def length_finding(seconds: float, table: dict, what: str, slack: float = 1e-6) -> str:
    """The finding when a length is outside the deliverable's min_seconds or max_seconds, else ''."""
    if table.get("max_seconds") and seconds > table["max_seconds"] + slack:
        return f"{what} lasts {seconds:.3f} s; {table['key']} max_seconds is {table['max_seconds']:g}"
    if table.get("min_seconds") and seconds < table["min_seconds"] - slack:
        return f"{what} lasts {seconds:.3f} s; {table['key']} min_seconds is {table['min_seconds']:g}"
    return ""


def check_cut_id(cut):
    if cut and not re.fullmatch(r"c\d{2,}", cut):
        raise C.Fatal(f"--cut {cut!r} is not cNN")
    return cut


# ── cut, encode, frame, still-video ─────────────────────────────────────────────────────

def picture_filters(info: dict, table: dict, frame: str, x) -> tuple:
    """(statements, fps) taking [0:v] to [v] at the deliverable's size."""
    v = C.streams(info, "video")
    if not v:
        raise C.Fatal("the source has no picture")
    sw, sh = int(v[0]["width"]), int(v[0]["height"])
    size = C.size_of(table)
    if not size:
        raise C.Fatal(f"{table['key']} has no width and height to encode to")
    fps = C.rate(v[0].get("avg_frame_rate") or v[0].get("r_frame_rate"))
    graph = reframe("0:v", "rf", sw, sh, size[0], size[1], frame, x, "0")
    tail = "[rf]"
    allowed = table.get("fps_allowed") or []
    if table.get("fps_max") and fps > table["fps_max"] + 0.01:
        tail += f"fps={table['fps_max']},"
        fps = float(table["fps_max"])
    elif allowed and fps > 0 and not rate_allowed(fps, allowed):
        # A variable or odd rate (a phone clip, a screen capture) the platform does not list:
        # the nearest standard rate it does, so the source's own rate is kept wherever it can be.
        fit = [s for s in STANDARD_FPS if rate_allowed(C.rate(s), allowed)] or STANDARD_FPS
        snap = min(fit, key=lambda s: abs(C.rate(s) - fps))
        print(f"  note: the source runs at {fps:.3f} fps, which {table['key']} does not list; "
              f"the deliverable runs at {C.rate(snap):.3f} fps")
        tail += f"fps={snap},"
        fps = C.rate(snap)
    else:
        tail += "null,"
    return graph, tail, fps


def still_source(src: Path, info: dict) -> None:
    """cut and encode take moving media, an animated GIF among it; a still is refused, named."""
    if C.is_still(src, info):
        raise C.Fatal(f"{C.shown(src)} is a still image: hold it for its seconds in an edit decision "
                      "list ([[clip]] with seconds), or put it under sound with still-video")


def caption_pass(args, table: dict, a: float, b: float, tmp: Path) -> tuple:
    """(seek, filters, family, audio filter) that burn --captions in the cutting pass, the SRT timed
    to the source, or to the cut when its name carries --cNN; refused before anything renders when
    no cue falls inside the range, or the cues cannot be burned."""
    import media_captions as K
    cues = K.read_srt(args.captions)
    shift = a if K.CUT_NAME_RE.search(Path(args.captions).name) else 0.0
    inside = [c for c in cues if c.end + shift > a and c.start + shift < b]
    if cues and not inside:
        raise C.Finding(f"no cue of {C.shown(args.captions)} falls between --in {C.fmt_tc(a)} and --out "
                        f"{C.fmt_tc(b)}: are these the captions of this source? Nothing rendered")
    K.burn_check(inside, K.width_for(table), C.shown(args.captions))
    size = C.size_of(table)
    ass, family = K.caption_ass(cues, size[0], size[1], table, shift)
    filters = K.subtitles_filter(tmp, ass) + ",setpts=PTS-STARTPTS,"
    return (["-ss", C.fmt_tc(a), "-to", C.fmt_tc(b), "-copyts"], filters, family,
            ["-af", "asetpts=PTS-STARTPTS"])


def cmd_cut(args) -> int:
    src = Path(args.src)
    table = C.preset(args.deliverable)
    check_cut_id(args.cut)
    a, b = C.parse_tc(args.cut_in, "--in"), C.parse_tc(args.cut_out, "--out")
    if b <= a:
        raise C.Fatal("--out must come after --in")
    info = C.probe(src)
    still_source(src, info)
    total = C.duration(info)
    if b > total + 0.05:
        raise C.Fatal(f"--out {C.fmt_tc(b)} is past the end of {C.shown(src)} ({C.fmt_tc(total)})")
    burned = bool(args.captions)
    overlay = getattr(args, "overlay", None)
    if C.is_gif(table):
        if not C.streams(info, "video"):
            raise C.Fatal(f"{C.shown(src)} has no picture to cut a GIF from")
        import media_image as I
        return I.cut_gif(args, table, src, info, a, b)
    if table.get("kind") != "video":
        if burned:
            raise C.Fatal(f"{table['key']} is not a video deliverable: no captions to burn")
        if overlay:
            raise C.Fatal(f"{table['key']} is not a video deliverable: no picture to lay --overlay on")
        if table.get("kind") != "audio":
            raise C.Fatal(f"{table['key']} is an image deliverable: render it with card.py, and encode it "
                          "with media.py image")
        if not C.streams(info, "audio"):
            raise C.Fatal(f"{C.shown(src)} has no sound to cut")
        table = sample_table(table)
    short = length_finding(b - a, table, "the cut")
    if short:
        print(f"  FAIL {short} (nothing rendered)")
        return 1
    if table.get("kind") != "video":
        ext = audio_ext(table)
        out = C.output_path(C.path(C.PUB_RENDERS) / deliverable_name(src, table["key"], args.cut, False, ext),
                            args.o, inputs=[src])
        render(["-y", "-ss", C.fmt_tc(a), "-to", C.fmt_tc(b)] + C.input_args(src)
               + ["-map", "0:a:0", "-vn"] + audio_codec_args(table) + untagged(table) + faststart(ext)
               + [str(out)], out, what="cut")
        return finish(out, verify(out, table, expect=b - a), "cut")
    size = C.size_of(table)
    if overlay:
        import media_image as I
        overlay = I.overlay_size(overlay, size)
    out = C.output_path(C.path(C.PUB_RENDERS) / deliverable_name(src, table["key"], args.cut, burned, ".mp4"),
                        args.o, inputs=[src] + ([overlay] if overlay else []))
    graph, tail, fps = picture_filters(info, table, args.frame, args.x)
    with tempfile.TemporaryDirectory(prefix="media-cut-") as tmp:
        tmp = Path(tmp)
        seek = ["-ss", C.fmt_tc(a), "-to", C.fmt_tc(b)]
        audio_filter, family = [], None
        if burned:
            seek, filters, family, audio_filter = caption_pass(args, table, a, b, tmp)
            tail += filters
        inputs = seek + ["-i", str(src.resolve())]
        if overlay:   # under the captions, which the tail burns after it
            inputs += ["-i", str(Path(overlay).resolve())]
            graph.append("[rf][1:v]overlay=0:0:format=auto[rfo]")
            tail = "[rfo]" + tail[len("[rf]"):]
        graph = graph + [tail + "format=yuv420p[v]"]
        has_audio = bool(C.streams(info, "audio")) and not C.silent(table)
        cmd = ["-y", "-loglevel", "info"] + inputs + ["-filter_complex", ";".join(graph), "-map", "[v]"]
        if has_audio:
            cmd += ["-map", "0:a:0"] + audio_filter + audio_codec_args(table)
        else:
            cmd += ["-an"]
        cmd += video_codec_args(table, fps) + ["-movflags", "+faststart", str(out.resolve())]
        proc = render(cmd, out, cwd=tmp, what="cut")
    if C.silent(table) and C.streams(info, "audio"):
        print(f"  note: {table['key']} sets audio_tracks = 0: the source's sound is left out")
    found = verify(out, table, expect=b - a)
    if burned:
        import media_captions as K
        fell, chosen = K.font_fell_back(proc.stderr, family)
        if fell:
            found.append(f"the caption font '{family}' was not found; libass fell back to {chosen}")
    return finish(out, found, "cut")


def cmd_encode(args) -> int:
    src = Path(args.src)
    table = C.preset(args.deliverable)
    if table.get("kind") not in ("video", "audio"):
        raise C.Fatal(f"{table['key']} is an image deliverable: render it with card.py, and encode it with "
                      "media.py image (an animated GIF is media.py cut's)")
    info = C.probe(src)
    still_source(src, info)
    if not C.streams(info, "audio") and table.get("kind") == "audio":
        raise C.Fatal(f"{C.shown(src)} has no sound to encode")
    if table.get("kind") == "audio" and C.streams(info, "video"):
        print(f"  note: {C.shown(src)} has a picture; {table['key']} takes its sound only")
    total = C.duration(info)
    wrong = length_finding(total, table, C.shown(src), 0.05)
    if wrong:
        print(f"  FAIL {wrong}: {'cut it instead' if 'max_seconds' in wrong else 'it is too short'} "
              "(nothing rendered)")
        return 1
    v, size = C.streams(info, "video"), C.size_of(table)
    if table.get("kind") == "video" and v and size and not args.frame:
        sw, sh = int(v[0]["width"]), int(v[0]["height"])
        if abs((sw / sh) / (size[0] / size[1]) - 1) > 0.005:
            raise C.Fatal(f"{C.shown(src)} is {sw}x{sh} and {table['key']} is {size[0]}x{size[1]}: their "
                          "shapes differ, so say how the picture fills the frame: --frame crop (fills it, "
                          "losing the edges) or --frame pad (keeps it all, over a blurred copy)")
    name = C.target_for(table)
    target = C.loudness_target(name)
    has_audio = bool(C.streams(info, "audio")) and not C.silent(table)
    if C.silent(table) and C.streams(info, "audio"):
        print(f"  note: {table['key']} sets audio_tracks = 0: the source's sound is left out")
    layout = "mono" if table["key"].startswith("audiobook.") else "stereo"
    pre = f"aformat=channel_layouts={layout},"   # the deliverable's channels, before loudnorm measures
    afilter = ["-af", pre + A.loudnorm_filter(A.loudnorm_measure(src, target, pre=pre), target)] \
        if has_audio else []
    if table.get("kind") != "video":
        out = C.output_path(C.path(C.PUB_RENDERS) / deliverable_name(src, table["key"], None, False,
                                                                     audio_ext(table)), args.o, inputs=[src])
        render(["-y"] + C.input_args(src) + ["-map", "0:a:0", "-vn"] + afilter + audio_codec_args(table)
               + untagged(table) + faststart(out.suffix) + [str(out)], out, what="encode")
    else:
        out = C.output_path(C.path(C.PUB_RENDERS) / deliverable_name(src, table["key"], None, False, ".mp4"),
                            args.o, inputs=[src])
        graph, tail, fps = picture_filters(info, table, args.frame or "crop", None)
        graph = graph + [tail + "format=yuv420p[v]"]
        cmd = ["-y"] + C.input_args(src) + ["-filter_complex", ";".join(graph), "-map", "[v]"]
        if has_audio:
            cmd += ["-map", "0:a:0"] + afilter + audio_codec_args(table)
        else:
            cmd += ["-an"]
        render(cmd + video_codec_args(table, fps) + ["-movflags", "+faststart", str(out)], out, what="encode")
    found = verify(out, table, expect=total)
    if has_audio:
        summary, lf = A.loudness_findings(out, target, name)
        print(f"  loudness: {summary} ({name} target {target[0]:g} LUFS, {target[1]:g} dBTP)")
        found += lf
    return finish(out, found, "encode")


def cmd_frame(args) -> int:
    src = Path(args.src)
    at = C.parse_tc(args.at, "--at")
    info = C.probe(src)
    if not C.streams(info, "video"):
        raise C.Fatal(f"{C.shown(src)} has no picture")
    if at > C.duration(info):
        raise C.Fatal(f"--at {C.fmt_tc(at)} is past the end of {C.shown(src)}")
    stem = src.name.rsplit(".", 1)[0]
    out = C.output_path(C.path(C.PUB_RENDERS) / f"{stem}.{C.tc_name(at)}.png", args.o, inputs=[src])
    render(["-y", "-ss", C.fmt_tc(at), "-i", str(src), "-frames:v", "1", "-update", "1", str(out)], out,
           what="frame")
    v = C.streams(C.probe(out), "video")[0]
    print(f"wrote {C.shown(out)}: {v.get('width')}x{v.get('height')} at {C.fmt_tc(at)}")
    return 0


def cmd_still_video(args) -> int:
    image, audio = Path(args.image), Path(args.audio)
    table = C.preset(args.deliverable)
    if table.get("kind") != "video":
        raise C.Fatal(f"{table['key']} is not a video deliverable")
    size = C.size_of(table)
    if not size:
        raise C.Fatal(f"{table['key']} has no width and height")
    ainfo = C.probe(audio)
    if not C.streams(ainfo, "audio"):
        raise C.Fatal(f"{C.shown(audio)} has no sound")
    iinfo = C.probe(image)
    iv = C.streams(iinfo, "video")
    if not iv:
        raise C.Fatal(f"{C.shown(image)} is not an image ffmpeg can read")
    if not C.is_still(image, iinfo):
        print(f"  note: {C.shown(image)} moves; still-video holds its first frame")
    total = C.duration(ainfo)
    if table.get("max_seconds") and total > table["max_seconds"] + 0.05:
        print(f"  FAIL the audio lasts {total:.3f} s; {table['key']} max_seconds is {table['max_seconds']:g}")
        return 1
    target = C.loudness_target("social")
    # The image is read at one frame a second and sized once a second; fps=30 after the scale
    # repeats the sized frame, so a 3000x3000 cover is never scaled thirty times a second.
    graph = reframe("0:v", "rf", int(iv[0]["width"]), int(iv[0]["height"]), size[0], size[1], "fit", None, "0")
    graph.append("[rf]fps=30,format=yuv420p[v]")
    out = C.output_path(C.path(C.PUB_RENDERS) / deliverable_name(audio, table["key"], None, False, ".mp4"),
                        args.o, inputs=[image, audio])
    pre = "aformat=channel_layouts=stereo,"
    m = A.loudnorm_measure(audio, target, pre=pre)
    render(["-y"] + C.still_input(image, "1") + C.input_args(audio)
           + ["-filter_complex", ";".join(graph), "-map", "[v]", "-map", "1:a:0", "-af",
              pre + A.loudnorm_filter(m, target)] + audio_codec_args(table)
           + video_codec_args(table, 30) + ["-tune", "stillimage", "-t", f"{total:.3f}",
                                            "-movflags", "+faststart", str(out)], out, what="still-video")
    found = verify(out, table, expect=total)
    summary, lf = A.loudness_findings(out, target, "social")
    print(f"  loudness: {summary}")
    return finish(out, found + lf, "still-video")


# ── assemble ────────────────────────────────────────────────────────────────────────────

def card_png(html: Path, w: int, h: int, transparent: bool) -> Path:
    """The card's PNG at w x h, rendered with card.py when missing or older than its sources."""
    if not html.is_file():
        raise C.Fatal(f"card not found: {C.shown(html)}")
    png = C.path(C.PROD_RENDERS) / f"{html.stem}.{w}x{h}.png"
    tokens = C.path(C.TOKENS)
    newest = max(html.stat().st_mtime, tokens.stat().st_mtime if tokens.is_file() else 0)
    if png.is_file() and png.stat().st_mtime >= newest:
        return png
    uv = shutil.which("uv")
    if not uv:
        raise C.Fatal(f"uv is not installed, and {C.shown(html)} needs rendering: {C.INSTALL['uv']}")
    png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [uv, "run", "--quiet", str(C.TOOLKIT / "card.py"), "render", str(html), "--size", f"{w}x{h}",
           "-o", str(png)] + (["--transparent"] if transparent else [])
    print(f"  rendering {C.shown(html)} → {C.shown(png)}")
    proc = subprocess.run(cmd, cwd=C.ROOT, capture_output=True, text=True)
    if proc.returncode == 1:
        raise C.Finding(f"card.py found problems in {C.shown(html)}:\n{proc.stdout.strip()}\n{proc.stderr.strip()}")
    if proc.returncode != 0:
        raise C.Fatal(f"card.py could not render {C.shown(html)} (exit {proc.returncode}):\n"
                      f"{(proc.stderr or proc.stdout).strip()[-800:]}")
    return png


def voice_segments(piece: str) -> list:
    """(path, duration, pause_after, segment) for each segment, in register order.

    Every segment must be approved: one that is generated (a retake not yet heard) or rejected
    would leave its line out and pull every later line early, so the master is refused, naming
    each such segment and its script lines."""
    import media_captions as K
    import media_repo as R
    reg = C.path(C.VOICEOVER) / f"{piece}.toml"
    if not reg.is_file():
        raise C.Fatal(f"vo:{piece} needs the segment register {C.shown(reg)}")
    pending = [s for s in C.load_toml(reg).get("segment", []) if str(s.get("status", "")).strip() != "approved"]
    if pending:
        raise C.Finding(
            f"vo:{piece}: the voice track would skip " + "; ".join(
                f"segment {s.get('id', '?')} ({str(s.get('status', '') or '').strip() or 'no status'}: "
                f"line {s.get('script_lines') or '?'})" for s in pending)
            + f" of {C.shown(reg)}. Every segment the master voices must be approved: have the author "
            "hear the take (or take it again, on the author's word), or take a segment the script no "
            "longer has out of the register. Nothing rendered")
    _, segs = K.approved_segments(reg)
    archive = {str(e.get("sha256", "")).lower(): str(e.get("id", "")) for e in manifest_entries().values()}
    out = []
    for s in segs:
        f = C.path(C.VOICEOVER) / s["file"]
        if not str(s.get("archived", "") or "").strip():
            fid = archive.get(R.sha256(f)) if archive else None
            if fid:
                print(f"  note: segment {s.get('id')}'s take is archived as {fid}, and its register's archived "
                      f"is empty: record archived = \"{fid}\" in {C.shown(reg)}")
            else:
                print(f"  note: segment {s.get('id')} is approved but not archived (M4 needs every take "
                      "a master uses archived: media.py footage add --kind generated)")
        out.append((f, K.segment_duration(f), float(s.get("pause_after", 0) or 0), s))
    return out


def cmd_assemble(args) -> int:
    edl = load_edl(Path(args.edl))
    e = edl["edit"]
    piece = str(e["piece"])
    size = parse_size(e.get("size", ""))
    ar = int(e.get("audio_rate", 48000) or 48000)
    loud = str(e.get("loudness", "social"))
    clips = timeline(edl, check_files=True)
    if not clips:
        raise C.Fatal(f"{C.shown(edl['path'])} has no [[clip]]")
    for c in clips:
        if c["kind"] == "media":
            c["info"] = c.get("info") or C.probe(c["path"])
            c["has_v"] = bool(C.streams(c["info"], "video"))
            c["has_a"] = bool(C.streams(c["info"], "audio"))
    fps_text = "30"
    if size:
        w, h = size
        for c in clips:
            if c["kind"] == "media" and not c["has_v"]:
                raise C.Fatal(f"clip {c['id']} ({c['source']}) has no picture: in a picture master a "
                              "sound-only source goes in [[audio]]")
        movers = [c for c in clips if c["kind"] == "media"]
        first = next((c for c in movers if c["path"].suffix.lower() not in C.ANIMATED_EXT), None) \
            or next(iter(movers), None)
        if first:
            v = C.streams(first["info"], "video")[0]
            avg, real = v.get("avg_frame_rate"), v.get("r_frame_rate")
            if first["path"].suffix.lower() in C.ANIMATED_EXT:   # GIF delays are centiseconds: 9.98 is 10
                avg = str(max(1, round(C.rate(avg if C.rate(avg) > 0 else real))))
            fps_text = standard_rate(avg, real)
            own = C.rate(avg) if C.rate(avg) > 0 else C.rate(real)
            if not is_standard(own):
                print(f"  note: clip {first['id']} ({first['source']}) runs at {own:.3f} fps, not a standard "
                      f"rate (a variable-rate recording?): the master runs at {C.rate(fps_text):.3f} fps")
        for c in clips:
            if c["kind"] == "card":
                c["path"] = card_png(c["path"], w, h, transparent=False)
                c["kind"] = "still"
            if c["kind"] == "still":
                c["info"] = C.probe(c["path"])
    fps = C.rate(fps_text)
    inputs, graph = [], []

    def add(args_):
        inputs.append(args_)
        return len(inputs) - 1

    total = clips[-1]["start"] + clips[-1]["dur"]
    for i, c in enumerate(clips):
        d = c["dur"]
        mute = bool(c["clip"].get("mute", False))
        # picture
        if size:
            if c["kind"] == "colour":
                graph.append(f"color=c=0x{c['colour'][1:]}:s={w}x{h}:r={fps_text}:d={d:.6f},format=yuv420p,"
                             f"setsar=1,settb=AVTB[v{i}]")
            elif c["kind"] == "media":
                k = c["k"] = add(["-ss", f"{c['in']:.6f}", "-t", f"{d + 0.5:.6f}"] + C.input_args(c["path"]))
                v = C.streams(c["info"], "video")[0]
                graph.append(f"[{k}:v]setpts=PTS-STARTPTS,fps={fps_text}[s{i}]")
                graph += reframe(f"s{i}", f"r{i}", int(v["width"]), int(v["height"]), w, h,
                                 c["clip"]["frame"], c["clip"].get("x") or None, str(i))
                graph.append(f"[r{i}]tpad=stop_mode=clone:stop_duration={d:.6f},trim=duration={d:.6f},"
                             f"setpts=PTS-STARTPTS,format=yuv420p,settb=AVTB[v{i}]")
            else:
                k = add(C.still_input(c["path"], fps_text, d + 1))
                v = C.streams(c["info"], "video")[0]
                graph += reframe(f"{k}:v", f"r{i}", int(v["width"]), int(v["height"]), w, h,
                                 c["clip"]["frame"], c["clip"].get("x") or None, str(i))
                chain = f"[r{i}]"
                if c["clip"]["motion"] == "push-in":
                    frames = max(1, int(round(d * fps)))
                    chain += (f"scale={2 * w}:{2 * h},zoompan=z='1+0.08*on/{frames}':"
                              f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={fps_text},")
                graph.append(chain + f"fps={fps_text},trim=duration={d:.6f},setpts=PTS-STARTPTS,"
                             f"format=yuv420p,setsar=1,settb=AVTB[v{i}]")
        # sound
        if c["kind"] == "media" and c["has_a"] and not mute:
            if size:
                k = c["k"]
            else:
                k = add(["-ss", f"{c['in']:.6f}", "-t", f"{d + 0.5:.6f}"] + C.input_args(c["path"]))
            graph.append(f"[{k}:a]asetpts=PTS-STARTPTS,aresample={ar},aformat=sample_fmts=fltp:"
                         f"channel_layouts=stereo,apad=whole_dur={d:.6f},atrim=duration={d:.6f}[a{i}]")
        else:
            if c["kind"] == "media" and not c["has_a"] and not size:
                print(f"  note: clip {c['id']} has no sound; it is silence in this audio master")
            graph.append(f"anullsrc=r={ar}:cl=stereo,atrim=duration={d:.6f},"
                         f"aformat=sample_fmts=fltp:channel_layouts=stereo[a{i}]")
    # join
    acc_v, acc_a = "v0", "a0"
    first = clips[0]
    if first["clip"]["transition"] == "fade" and float(first["clip"].get("transition_seconds", 0) or 0) > 0:
        t = min(float(first["clip"]["transition_seconds"]), first["dur"] * 0.99)
        if size:
            graph.append(f"[v0]fade=t=in:st=0:d={t:.6f}[vf0]")
            acc_v = "vf0"
        graph.append(f"[a0]afade=t=in:st=0:d={t:.6f}[af0]")
        acc_a = "af0"
    for i, c in enumerate(clips[1:], start=1):
        if c["fade"] > 0:
            if size:
                graph.append(f"[{acc_v}][v{i}]xfade=transition=fade:duration={c['fade']:.6f}:"
                             f"offset={c['start']:.6f}[vj{i}]")
            graph.append(f"[{acc_a}][a{i}]acrossfade=d={c['fade']:.6f}[aj{i}]")
        else:
            if size:
                graph.append(f"[{acc_v}][{acc_a}][v{i}][a{i}]concat=n=2:v=1:a=1[vj{i}][aj{i}]")
            else:
                graph.append(f"[{acc_a}][a{i}]concat=n=2:v=0:a=1[aj{i}]")
        acc_v, acc_a = f"vj{i}", f"aj{i}"
    # overlays
    if size:
        for j, o in enumerate(edl["overlay"]):
            src = str(o.get("source", "")).strip()
            at = C.parse_tc(o.get("at") or 0, f"overlay {j + 1} at")
            until = C.parse_tc(o.get("until") or total, f"overlay {j + 1} until")
            if until <= at:
                raise C.Fatal(f"overlay {j + 1}: until must come after at")
            r = resolve_source(src, manifest_entries())
            if r["kind"] == "card":
                png = card_png(r["path"], w, h, transparent=True)
            elif r["kind"] == "still" and r.get("path") and r["path"].is_file():
                png = r["path"]
            elif r["kind"] == "media" and r.get("path") and r["path"].is_file():
                raise C.Fatal(f"overlay {j + 1}: {src!r} moves; an overlay is a card or a still image "
                              "(put a moving source in a [[clip]])")
            else:
                raise C.Fatal(f"overlay {j + 1}: {src!r} is neither a card nor an image this project has")
            k = add(C.still_input(png, fps_text, until))
            graph.append(f"[{k}:v]scale={w}:{h},format=rgba[ol{j}]")
            graph.append(f"[{acc_v}][ol{j}]overlay=0:0:enable='between(t,{at:.3f},{until:.3f})':"
                         f"eof_action=pass[vo{j}]")
            acc_v = f"vo{j}"
        graph.append(f"[{acc_v}]format=yuv420p[vout]")
    # [[audio]] tracks
    tracks, voices, ducked = [], [], []
    for n, t in enumerate(edl["audio"]):
        src = str(t.get("source", "")).strip()
        given = str(t.get("role", "") or "").strip()
        role = given or ("music" if t.get("duck") else "voice")
        if role not in ROLES:
            raise C.Fatal(f"audio {n + 1}: role {role!r} is not voice, music or effect")
        if t.get("duck") and role != "music":
            raise C.Fatal(f"audio {n + 1}: duck = true ducks a music bed under the voice, and this track's "
                          f"role is {role!r}: set role = \"music\", or drop duck")
        if t.get("duck") and not given:
            print(f"  note: audio {n + 1} sets duck = true and no role: it is mixed as music, ducked "
                  "under the voice")
        at = C.parse_tc(t.get("at") or 0, f"audio {n + 1} at")
        label = f"t{n}"
        if src.startswith("vo:"):
            segs = voice_segments(src[3:].strip() or piece)
            parts = []
            for m, (f, dur, pause, _) in enumerate(segs):
                k = add(C.input_args(f))
                graph.append(f"[{k}:a]asetpts=PTS-STARTPTS,aresample={ar},aformat=sample_fmts=fltp:"
                             f"channel_layouts=stereo,apad=whole_dur={dur + pause:.6f},"
                             f"atrim=duration={dur + pause:.6f}[s{n}_{m}]")
                parts.append(f"[s{n}_{m}]")
            graph.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[raw{n}]")
            length = sum(dur + pause for _, dur, pause, _ in segs)
        else:
            r = resolve_source(src, manifest_entries())
            if r["kind"] == "missing" or not r["path"].is_file():
                raise C.Fatal(f"audio {n + 1}: {r.get('label', src)} is not in this project")
            a = C.parse_tc(t.get("in") or 0, f"audio {n + 1} in")
            seek = ["-ss", f"{a:.6f}"]
            if t.get("out"):
                b = C.parse_tc(t["out"], f"audio {n + 1} out")
                if b <= a:
                    raise C.Fatal(f"audio {n + 1}: out must come after in")
                seek += ["-t", f"{b - a:.6f}"]
                length = b - a
            else:
                length = (r.get("duration") or C.duration(C.probe(r["path"]))) - a
            k = add(seek + C.input_args(r["path"]))
            graph.append(f"[{k}:a]asetpts=PTS-STARTPTS,aresample={ar},aformat=sample_fmts=fltp:"
                         f"channel_layouts=stereo[raw{n}]")
        chain = f"[raw{n}]volume={float(t.get('gain_db', 0) or 0):.2f}dB"
        fi, fo = float(t.get("fade_in", 0) or 0), float(t.get("fade_out", 0) or 0)
        if fi > 0:
            chain += f",afade=t=in:st=0:d={fi:.6f}"
        if fo > 0:
            chain += f",afade=t=out:st={max(0.0, length - fo):.6f}:d={fo:.6f}"
        chain += f",adelay={int(round(at * 1000))}:all=1[{label}]"
        graph.append(chain)
        if role == "voice":
            voices.append(label)
        elif t.get("duck") and role == "music":
            ducked.append(label)
        else:
            tracks.append(label)
    mix = [acc_a]
    if voices:
        if len(voices) > 1:
            graph.append("".join(f"[{v}]" for v in voices) + f"amix=inputs={len(voices)}:duration=longest:"
                         "normalize=0[vox]")
            key = "vox"
        else:
            key = voices[0]
    else:
        key = None
    if ducked:
        if key is None:
            graph.append(f"[{acc_a}]asplit=2[base][keysrc]")
            mix = ["base"]
            key = "keysrc"
        graph.append(f"[{key}]asplit={len(ducked) + 1}[voxmix]" + "".join(f"[sc{d}]" for d in range(len(ducked))))
        if voices:
            mix.append("voxmix")
        else:
            graph.append("[voxmix]anullsink")
        for d, label in enumerate(ducked):
            graph.append(f"[sc{d}]apad[scp{d}]")
            graph.append(f"[{label}][scp{d}]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[dk{d}]")
            mix.append(f"dk{d}")
    elif key:
        mix.append(key)
    mix += tracks
    if len(mix) > 1:
        graph.append("".join(f"[{m}]" for m in mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,"
                     f"atrim=duration={total:.6f}[aout]")
    else:
        graph.append(f"[{mix[0]}]atrim=duration={total:.6f}[aout]")
    ext = ".mp4" if size else ".wav"
    out = C.output_path(C.path(C.PROD_RENDERS) / f"{piece}.master{ext}", args.o)
    print(f"assemble {C.shown(edl['path'])}: {len(clips)} clip(s), {len(edl['overlay'])} overlay(s), "
          f"{len(edl['audio'])} audio track(s), {total:.3f} s" + (f" at {w}x{h}, {fps_text} fps" if size else
                                                                   ", audio only"))
    with tempfile.TemporaryDirectory(prefix="media-assemble-") as tmp:
        stage = Path(tmp) / ("stage.mkv" if size else "stage.wav")
        cmd = ["-y"]
        for a in inputs:
            cmd += a
        cmd += ["-filter_complex", ";".join(graph)]
        if size:
            cmd += ["-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", C.X264_PRESET,
                    "-crf", "18", "-pix_fmt", "yuv420p", "-r", fps_text, "-c:a", "pcm_s16le", "-ar", str(ar)]
        else:
            cmd += ["-map", "[aout]", "-c:a", "pcm_s16le", "-ar", str(ar)]
        A.render(cmd + ["-t", f"{total:.6f}", str(stage)], stage, what="assemble")
        tail = ["-c:a", "aac", "-b:a", "192k", "-ar", str(ar)] if size else ["-c:a", "pcm_s16le", "-ar", str(ar)]
        lead = ["-y", "-i", str(stage), "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy"] if size else \
            ["-y", "-i", str(stage), "-map", "0:a:0"]
        if loud != "none":
            target = C.loudness_target(loud)
            m = A.loudnorm_measure(stage, target)
            lead += ["-af", A.loudnorm_filter(m, target)]
        render(lead + tail + (["-movflags", "+faststart"] if size else []) + [str(out)], out, what="assemble")
    info = C.probe(out)
    found = []
    got = C.duration(info)
    if abs(got - total) > max(0.1, 2 / (fps or 30)):
        found.append(f"lasts {got:.3f} s where the edit adds up to {total:.3f} s")
    if size:
        v = C.streams(info, "video")
        if not v or (int(v[0]["width"]), int(v[0]["height"])) != size:
            found.append("the picture is not the edit's size")
    elif C.streams(info, "video"):
        found.append("an audio master carries a picture")
    if loud != "none":
        summary, lf = A.loudness_findings(out, C.loudness_target(loud), loud)
        print(f"  loudness: {summary} ({loud} target)")
        found += lf
    return finish(out, found, "assemble")
