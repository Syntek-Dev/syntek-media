#!/usr/bin/env python3
"""media_feed.py: a self-hosted podcast's show register, feed, chapters and file tags, for media.py.

Not run directly: python3 toolkit/media.py feed new, add, tag, write, chapters and check call it,
and media.py's self-test exercises it (DESIGN D58, D59, Section 6.17).

A self-hosted show is published from one RSS 2.0 feed, written here from the show's register,
publishing/src/podcast/<show>.toml, where the project self-hosts a podcast: the single source of
every value the feed carries. Apple Podcasts and Spotify ingest that feed; the author uploads
it, after every file it names, at the episode's publication time, because a static feed has no
clock. Nothing here fetches, posts or opens the network.

The register's skeleton is SKELETON, below: the one copy (the folder's CLAUDE.md shows the same
text with no live flag). 'feed new' writes it, filled with the show's slug, its feed URL, its
site and its podcast:guid, and flags owner_email for the author. Identity is written once: the
show's podcast:guid is the UUIDv5 of its feed URL without the scheme and trailing slashes, in
the Podcasting 2.0 namespace ead4c236-bf58-58c6-a2c6-a6b28d128cb6, and each episode's guid
(written by 'feed add') is the UUIDv5 of its piece in the show's GUID; neither is ever
recomputed, except by 'feed new --rekey', which rewrites the feed URL and every GUID, and only
while no row is published and no tracked feed exists.

'feed tag' re-muxes an episode's M5 render,
publishing/src/renders/<piece>/<piece>.podcast-feed-audio.mp3, without re-encoding (-c:a copy),
its old tags and chapters dropped: ID3v2.3 title, the show's author and title, the track number,
the chapters (CTOC and CHAP, each ending at the next start, the last at the end) and the show's
id3_cover; it changes nothing, exit 1, while the row's words, its chapters or the show's title or
author are not ready, and writes render, bytes and seconds back into the row. It reads the
render in the piece's own folder only (DESIGN D64, D65): one an earlier release left flat at the
top of publishing/src/renders/ is never tagged, and feed tag exits 2 naming the encode that makes
it, and the flat file where there is one. A render's name alone goes into the row; every reader
finds it in its piece's folder, and a name with no piece key (a show's cover encodes, a feed's
upload copy) at the top of publishing/src/renders/.

'feed write' writes the feed of every ready or published episode whose pub_date is not after
--as-of, newest first, in the project's timezone; the same register and --as-of always give the
same bytes. Before it writes anything it compares the new feed with the show's tracked copy,
publishing/src/podcast/<show>.feed.xml, where one exists, and refuses (exit 1) a changed
podcast:guid, a GUID that vanished while its row is not withdrawn, or an enclosure whose length
changed under the same URL; -o that tracked copy replaces it through a temporary file (the one
tracked file the toolkit ever overwrites), and without -o the feed goes to stdout.
'feed chapters' writes Podcasting 2.0 JSON chapters, to publishing/src/renders/<piece>/ unless -o
names a path; 'feed check' proves the register (or, with --feed, any saved feed) offline against
Section 6.17 and the [platform.podcast] keys of toolkit/data/platforms.toml, never numbers of its
own. Where an episode's render, or its art, is missing from its piece's folder, feed check reads a
flat one an earlier release left at the top of publishing/src/renders/ and names it in a warning,
so a published episode is never silently left unchecked (DESIGN D65).

The register is edited line by line (as 'take add' edits its register): the author's comments
and values survive every write, and a value the author set is never rewritten.

Standard library only; Python 3.11+.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import media_common as C

PODCAST_NAMESPACE = uuid.UUID("ead4c236-bf58-58c6-a2c6-a6b28d128cb6")   # Podcasting 2.0 podcast:guid
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
      "content": "http://purl.org/rss/1.0/modules/content/",
      "podcast": "https://podcastindex.org/namespace/1.0",
      "psc": "http://podlove.org/simple-chapters",
      "atom": "http://www.w3.org/2005/Atom"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PIECE_RE = re.compile(r"^\d{3}-[a-z0-9][a-z0-9-]*$")
GUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
STATUSES = ("planned", "ready", "published", "withdrawn")
ROUTES = ("upload", "rss", "none")
FEED_AUDIO = "podcast.feed_audio"
FLAG = "# AUTHOR TO CONFIRM: owner_email: a role address the brand reads (it is public: the directories send their ownership codes to it)"
PERSONAL_DOMAINS = ("gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "hotmail.co.uk", "live.com",
                    "live.co.uk", "yahoo.com", "yahoo.co.uk", "icloud.com", "me.com", "mac.com", "aol.com",
                    "proton.me", "protonmail.com", "gmx.com", "btinternet.com", "sky.com")

SKELETON = '''\
[show]
show = "<show>"              # kebab slug, frozen: names this file and its feed
title = ""                    # no episode numbers; within platform.podcast.tag_max_chars
site = ""                     # the website profile's slug of the site serving the feed, where that platform is chosen; else "" and the podcast profile names the server
feed_url = ""                 # written by feed new from --feed-url: the feed's permanent https URL, for life (D58); feed new --rekey alone changes it, before anything is published
new_feed_url = ""             # only while moving the feed: a redirect too, for platform.podcast.feed_move_min_days
link = ""                     # the show's page
media_base = ""               # the URL folder the audio, art, captions and chapters are published under
language = "en-gb"
author = ""
owner_name = ""
owner_email = ""              # public: the directories send their ownership codes here; a role address (feed new flags it)
copyright = ""
category = ""                 # Apple's category, exactly as Apple spells it
subcategory = ""
explicit = false
type = "episodic"             # episodic | serial (serial: every episode numbered)
cover = ""                    # the published name of the podcast.cover render; a new cover gets a new name
id3_cover = ""                # the podcast.id3_cover render encode embeds in every episode; "" = none
podcast_guid = ""             # written once by feed new; never recomputed (feed new --rekey only while nothing is published)
locked = true                 # no other host may import the feed
complete = false
block = false
youtube_route = "upload"      # upload | rss | none (D58: never upload and rss for one show)
description = """
"""                           # plain text, one sentence per line; within platform.podcast.show_description_max_bytes; the disclosure sentence where any episode uses a synthetic voice (D25)
approved = ""                 # DD/MM/YYYY: the author approved the show's details
last_updated = ""

[[episode]]                   # one row per episode, in any order; never deleted
piece = ""                    # the piece (D17)
guid = ""                     # written once by feed add; NEVER changes, even when the title or the URL does
title = ""                    # no episode or season number, no show name
number = 0                    # 0 = left out (serial needs it)
season = 0
type = "full"                 # full | trailer | bonus
explicit = false
pub_date = ""                 # DD/MM/YYYY HH:MM, the project's timezone: <pubDate>; the schedule row's time
render = ""                   # written by feed tag: the podcast.feed_audio render's name
audio_url = ""                # "" = media_base + the render's name; a corrected file gets a NEW url, the guid stays
bytes = 0                     # written by feed tag; equals the served Content-Length
seconds = 0.0                 # written by feed tag: the render's probed duration
art = ""                      # the published name of a podcast.episode_art render; "" = the show's cover
page = ""                     # the episode page on the feed's site (pages on other sites are placements, D61)
transcript = ""               # the published name of the master-timed VTT; "" = none
description = """
"""                           # plain text (no < or >), one sentence per line; within platform.podcast.episode_description_max_chars; the disclosure sentence (D25)
status = "planned"            # planned (feed add) · ready (M7, the feed workflow) · published (the author's report, publishing/workflows/06-record-a-publication/) · withdrawn (kept here, left out of the feed)
notes = ""

[[episode.chapter]]           # optional; at least platform.podcast.chapters_min, the first at 00:00:00.000
start = "00:00:00.000"        # on the master (D29)
title = ""                    # within platform.podcast.chapter_title_max_chars; title case
'''


# ── The register: reading, and writing it line by line ───────────────────────────────────

def register_path(show: str) -> Path:
    return C.path(C.PODCAST) / f"{show}.toml"


def tracked_feed(show: str) -> Path:
    return C.path(C.PODCAST) / f"{show}.feed.xml"


def check_show(show: str) -> str:
    if not SLUG_RE.fullmatch(show or ""):
        raise C.Fatal(f"SHOW {show!r} is not a kebab slug (lower-case letters, digits and hyphens): it names "
                      "the register and the feed for life")
    return show


def need_folder() -> Path:
    folder = C.path(C.PODCAST)
    if not folder.is_dir():
        raise C.Fatal(f"this project has no {C.PODCAST}/: the podcast platform is not chosen. Add podcast to "
                      "PLATFORMS with 'uvx copier update --trust -a .copier-answers.syntek-media.yml', which "
                      "adds the folder; the toolkit never makes it")
    return folder


def load(show: str) -> tuple:
    """(path, text, data) of a show's register."""
    check_show(show)
    need_folder()
    p = register_path(show)
    if not p.is_file():
        raise C.Fatal(f"{C.shown(p)} does not exist: open the show with 'media.py feed new {show} --feed-url URL'")
    data = C.load_toml(p)
    if not isinstance(data.get("show"), dict):
        raise C.Fatal(f"{C.shown(p)} has no [show] table")
    return p, C.read_text(p), data


def episodes(data: dict) -> list:
    return [e for e in data.get("episode", []) if isinstance(e, dict)]


def row_of(data: dict, piece: str, show: str) -> dict:
    row = next((e for e in episodes(data) if str(e.get("piece", "")) == piece), None)
    if row is None:
        raise C.Fatal(f"{piece} has no [[episode]] row in {C.shown(register_path(show))}: run "
                      f"'media.py feed add {show} --piece {piece}' first")
    return row


def toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.3f}"
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + "".join(ch if ch >= " " or ch == "\t" else f"\\u{ord(ch):04x}" for ch in text) + '"'


HEADER_RE = re.compile(r"^\s*\[\[?\s*([A-Za-z0-9_.-]+)\s*\]\]?\s*(?:#.*)?$")
KEY_RE = r'^(\s*)({key})(\s*=\s*)("(?:[^"\\]|\\.)*"|[^\s#]+)([ \t]*)(#.*)?$'


def inside_strings(lines: list) -> set:
    """The indices of lines that continue a multi-line string (never a key or a header)."""
    inside, in_string = set(), False
    for i, line in enumerate(lines):
        if in_string:
            inside.add(i)
        if line.count('"""') % 2 == 1:
            in_string = not in_string
    return inside


def blocks(lines: list) -> list:
    """(table, start, end) for each table of a TOML text, its header line at start; lines inside a
    multi-line string are never read as headers."""
    found, skip = [], inside_strings(lines)
    for i, line in enumerate(lines):
        m = HEADER_RE.match(line) if i not in skip else None
        if m:
            if found:
                found[-1][2] = i
            found.append([m.group(1), i, len(lines)])
    return [tuple(b) for b in found]


def set_line(line: str, key: str, value) -> str:
    m = re.match(KEY_RE.format(key=re.escape(key)), line)
    if m.group(4).startswith('"""'):
        raise C.Fatal(f"{key} is a multi-line string: the toolkit never writes one")
    head = f"{m.group(1)}{m.group(2)}{m.group(3)}{toml_value(value)}"
    if m.group(6):
        col = m.start(6)
        head = head.ljust(col) if len(head) < col else head + " "
        return head + m.group(6)
    return head


def edit(text: str, table: str, updates: dict, piece: str | None = None) -> str:
    """Rewrite single-line fields of [show] (piece None) or of the [[episode]] row of piece."""
    lines = text.split("\n")
    skip = inside_strings(lines)
    for name, start, end in blocks(lines):
        if name != table:
            continue
        keys = [i for i in range(start + 1, end) if i not in skip]
        if piece is not None:
            own = next((re.match(KEY_RE.format(key="piece"), lines[i]) for i in keys
                        if re.match(KEY_RE.format(key="piece"), lines[i])), None)
            if not own or own.group(4).strip('"') != piece:
                continue
        for key, value in updates.items():
            for i in keys:
                if re.match(KEY_RE.format(key=re.escape(key)), lines[i]):
                    lines[i] = set_line(lines[i], key, value)
                    break
            else:
                at = end
                while at > start + 1 and not lines[at - 1].strip():
                    at -= 1
                lines.insert(at, f"{key} = {toml_value(value)}")
                end += 1
        return "\n".join(lines)
    raise C.Fatal(f"no [{table}]" + (f" row for {piece}" if piece else "") + " to write into")


def skeleton_parts() -> tuple:
    """(the [show] table, the [[episode]] table, the [[episode.chapter]] table) of SKELETON."""
    lines = SKELETON.rstrip("\n").split("\n")
    parts = {name: "\n".join(lines[s:e]).rstrip("\n") for name, s, e in blocks(lines)}
    return parts["show"], parts["episode"], parts["episode.chapter"]


def write_register(p: Path, text: str) -> None:
    data = text if text.endswith("\n") else text + "\n"
    try:
        import tomllib
        tomllib.loads(data)
    except Exception as err:   # never leave a register the toolkit cannot read
        raise C.Fatal(f"the register would not parse after this write ({err}); nothing written") from None
    C.replace_file(p, data.encode("utf-8"))


# ── Identity ────────────────────────────────────────────────────────────────────────────

def bare_url(url: str) -> str:
    """A feed URL without its scheme and trailing slashes, as podcast:guid is seeded."""
    return re.sub(r"^[A-Za-z][A-Za-z0-9+.-]*://", "", url.strip()).rstrip("/")


def podcast_guid(feed_url: str) -> str:
    return str(uuid.uuid5(PODCAST_NAMESPACE, bare_url(feed_url)))


def episode_guid(show_guid: str, piece: str) -> str:
    try:
        return str(uuid.uuid5(uuid.UUID(show_guid), piece))
    except ValueError:
        raise C.Fatal(f"the show's podcast_guid {show_guid!r} is not a UUID: feed new writes it") from None


def check_feed_url(url: str, what: str = "--feed-url") -> str:
    url = (url or "").strip()
    if not re.match(r"^https://[^\s/]+\.[^\s/]+/\S*$", url) or not url.isascii():
        raise C.Fatal(f"{what} {url!r} is not an https URL of ASCII characters (the feed's permanent address)")
    return url


# ── Values the feed carries ─────────────────────────────────────────────────────────────

def plain(text) -> str:
    """One sentence per line, paragraphs parted by a blank line → plain-text paragraphs."""
    paras = re.split(r"\n\s*\n", str(text or "").strip())
    return "\n\n".join(" ".join(ln.strip() for ln in p.splitlines() if ln.strip()) for p in paras if p.strip())


def url_of(base: str, name: str) -> str:
    name = str(name or "").strip()
    if not name or re.match(r"^https?://", name):
        return name
    base = str(base or "").strip()
    return (base.rstrip("/") + "/" + name.lstrip("/")) if base else ""


def platform_podcast(data=None) -> dict:
    data = data or C.load_presets(quiet=True)[0]
    return data.get("platform", {}).get("podcast", {})


def when(row: dict):
    try:
        return C.parse_datetime(str(row.get("pub_date", "")), "pub_date")
    except C.Fatal:
        return None


def chapters_of(row: dict) -> list:
    return [c for c in row.get("chapter", []) if isinstance(c, dict)]


def item_model(show: dict, row: dict) -> dict:
    base = show.get("media_base", "")
    url = str(row.get("audio_url", "") or "").strip() or url_of(base, row.get("render", ""))
    transcript = str(row.get("transcript", "") or "").strip()
    return {"piece": str(row.get("piece", "")), "guid": str(row.get("guid", "")), "url": url,
            "length": int(row.get("bytes", 0) or 0), "title": str(row.get("title", "")),
            "description": plain(row.get("description", "")), "when": when(row), "row": row,
            "transcript": url_of(base, transcript),
            "transcript_type": "application/srt" if transcript.lower().endswith(".srt") else "text/vtt",
            "art": url_of(base, row.get("art", "")), "page": str(row.get("page", "") or "").strip()}


def included(data: dict, as_of=None, tagged_planned: bool = False) -> list:
    """The episodes a feed carries: ready or published (and, for feed check, planned rows already
    tagged), withdrawn left out; with as_of, only those whose pub_date is not after it; newest first."""
    show, rows = data["show"], []
    for e in episodes(data):
        status = str(e.get("status", "planned"))
        if status == "withdrawn":
            continue
        if status in ("ready", "published") or (tagged_planned and str(e.get("render", "") or "").strip()):
            item = item_model(show, e)
            if as_of is not None and (item["when"] is None or item["when"] > as_of):
                continue
            rows.append(item)
    rows.sort(key=lambda i: (i["when"].timestamp() if i["when"] else -math.inf, i["piece"]), reverse=True)
    return rows


# ── The feed itself ─────────────────────────────────────────────────────────────────────

def text_el(tag: str, value, **attrs) -> str:
    a = "".join(f" {k}={quoteattr(str(v))}" for k, v in attrs.items())
    return f"<{tag}{a}>{escape(str(value))}</{tag}>"


def empty_el(tag: str, **attrs) -> str:
    return f"<{tag}" + "".join(f" {k}={quoteattr(str(v))}" for k, v in attrs.items()) + "/>"


def build_xml(data: dict, items: list, as_of, enclosure_type: str) -> str:
    """The show's RSS 2.0 feed: deterministic, no clock read (DESIGN Section 6.17)."""
    s = data["show"]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" ' + " ".join(f'xmlns:{k}="{v}"' for k, v in NS.items()) + ">",
           "  <channel>"]
    ch = ["    " + text_el("title", s.get("title", "")),
          "    " + text_el("link", s.get("link", "")),
          "    " + text_el("language", s.get("language", "")),
          "    " + text_el("description", plain(s.get("description", ""))),
          "    " + empty_el("atom:link", href=s.get("feed_url", ""), rel="self", type="application/rss+xml")]
    if str(s.get("copyright", "")).strip():
        ch.append("    " + text_el("copyright", s["copyright"]))
    ch += ["    " + text_el("lastBuildDate", format_datetime(as_of)),
           "    " + text_el("itunes:author", s.get("author", "")),
           "    <itunes:owner>" + text_el("itunes:name", s.get("owner_name", ""))
           + text_el("itunes:email", s.get("owner_email", "")) + "</itunes:owner>",
           "    " + empty_el("itunes:image", href=url_of(s.get("media_base", ""), s.get("cover", "")))]
    cat, sub = str(s.get("category", "")).strip(), str(s.get("subcategory", "")).strip()
    if cat:
        ch.append(f"    <itunes:category text={quoteattr(cat)}>"
                  + (empty_el("itunes:category", text=sub) if sub else "") + "</itunes:category>")
    ch += ["    " + text_el("itunes:explicit", "true" if s.get("explicit") else "false"),
           "    " + text_el("itunes:type", s.get("type", "episodic")),
           "    " + text_el("podcast:guid", s.get("podcast_guid", "")),
           "    " + text_el("podcast:locked", "yes" if s.get("locked", True) else "no",
                            owner=s.get("owner_email", ""))]
    if str(s.get("new_feed_url", "")).strip():
        ch.append("    " + text_el("itunes:new-feed-url", s["new_feed_url"]))
    if s.get("complete"):
        ch.append("    " + text_el("itunes:complete", "Yes"))
    if s.get("block"):
        ch.append("    " + text_el("itunes:block", "Yes"))
    out += ch
    for i in items:
        e = i["row"]
        it = ["    <item>",
              "      " + text_el("title", i["title"]),
              "      " + text_el("guid", i["guid"], isPermaLink="false"),
              "      " + text_el("pubDate", format_datetime(i["when"]) if i["when"] else "")]
        if i["page"]:
            it.append("      " + text_el("link", i["page"]))
        it += ["      " + text_el("description", i["description"]),
               "      " + empty_el("enclosure", url=i["url"], length=i["length"], type=enclosure_type),
               "      " + text_el("itunes:duration", int(round(float(e.get("seconds", 0) or 0)))),
               "      " + text_el("itunes:episodeType", e.get("type", "full")),
               "      " + text_el("itunes:explicit", "true" if e.get("explicit") else "false")]
        if int(e.get("number", 0) or 0):
            it.append("      " + text_el("itunes:episode", int(e["number"])))
        if int(e.get("season", 0) or 0):
            it.append("      " + text_el("itunes:season", int(e["season"])))
        if i["art"]:
            it.append("      " + empty_el("itunes:image", href=i["art"]))
        if i["transcript"]:
            it.append("      " + empty_el("podcast:transcript", url=i["transcript"], type=i["transcript_type"],
                                          language="en-GB", rel="captions"))
        chapters = chapters_of(e)
        if chapters:
            it.append("      " + empty_el("podcast:chapters", url=url_of(s.get("media_base", ""),
                                                                         f"{i['piece']}.chapters.json"),
                                          type="application/json+chapters"))
            it.append('      <psc:chapters version="1.1">')
            for c in chapters:
                it.append("        " + empty_el("psc:chapter", start=C.fmt_tc(C.parse_tc(c.get("start", 0))),
                                               title=c.get("title", "")))
            it.append("      </psc:chapters>")
        it.append("    </item>")
        out += it
    out += ["  </channel>", "</rss>"]
    xml = "\n".join(out) + "\n"
    return xml.replace("©", "&#xA9;")


def parse_feed(p) -> dict:
    """The parts of a saved feed the comparison and the checks read."""
    try:
        root = ET.parse(str(p)).getroot()
    except (ET.ParseError, OSError) as err:
        raise C.Finding(f"{C.shown(p)} is not a well-formed feed: {err}") from None
    channel = root.find("channel")
    if root.tag != "rss" or channel is None:
        raise C.Finding(f"{C.shown(p)} is not an RSS 2.0 feed (no <rss><channel>)")

    def t(el, path):
        x = el.find(path, NS)
        return (x.text or "").strip() if x is not None else None
    image = channel.find("itunes:image", NS)
    owner = channel.find("itunes:owner/itunes:email", NS)
    feed = {"guid": t(channel, "podcast:guid") or "", "title": t(channel, "title"), "link": t(channel, "link"),
            "description": t(channel, "description"), "language": t(channel, "language"),
            "author": t(channel, "itunes:author"), "image": image.get("href") if image is not None else None,
            "category": channel.find("itunes:category", NS) is not None,
            "explicit": t(channel, "itunes:explicit"), "owner_email": (owner.text or "").strip() if owner is not None else None,
            "self": next((a.get("href") for a in channel.findall("atom:link", NS) if a.get("rel") == "self"), None),
            "items": []}
    for it in channel.findall("item"):
        enc = it.find("enclosure")
        feed["items"].append({
            "guid": t(it, "guid") or "", "title": t(it, "title"), "description": t(it, "description"),
            "pubDate": t(it, "pubDate"), "url": enc.get("url", "") if enc is not None else "",
            "length": int(enc.get("length", "0") or 0) if enc is not None and (enc.get("length") or "0").isdigit() else -1,
            "type": enc.get("type") if enc is not None else None,
            "chapters": [(c.get("start", ""), c.get("title", "")) for c in it.findall("psc:chapters/psc:chapter", NS)]})
    return feed


def compare(new: dict, old: dict, data, label: str) -> list:
    """Findings when a feed would change what the directories already hold (DESIGN D59): the
    show's podcast:guid, a GUID that vanished while its row is not withdrawn (or that no row
    holds: retyped), an enclosure whose length changed under the same URL."""
    found = []
    if old["guid"] and new["guid"] != old["guid"]:
        found.append(f"the show's podcast:guid is {new['guid'] or 'empty'}; {label} carries {old['guid']}: the "
                     "directories would take it for another show")
    rows = {str(e.get("guid", "")): e for e in episodes(data)} if data else {}
    now = {i["guid"] for i in new["items"]}
    for i in old["items"]:
        if i["guid"] in now:
            continue
        row = rows.get(i["guid"])
        if not data:
            found.append(f"the GUID {i['guid']} of {label} ('{i['title']}') is missing from this feed: a "
                         "directory would drop the episode, or list it twice under a new GUID")
        elif row is None:
            found.append(f"the GUID {i['guid']} of {label} ('{i['title']}') is in no row of the register: a GUID "
                         "retyped or a row deleted lists the episode twice; put the row's guid back")
        elif str(row.get("status", "")) != "withdrawn":
            found.append(f"{row.get('piece')} (GUID {i['guid']}) is in {label} and missing from this feed, and its "
                         "row is not withdrawn: write the feed --as-of its pub_date or later, or withdraw it")
    lengths = {i["url"]: i["length"] for i in new["items"]}
    for i in old["items"]:
        if i["url"] in lengths and lengths[i["url"]] != i["length"]:
            found.append(f"the enclosure {i['url']} was {i['length']} bytes in {label} and is {lengths[i['url']]} "
                         "now: publish a corrected file under a new URL (audio_url, a -v2 before its extension), "
                         "keeping its GUID (DESIGN D58)")
    return found


def model_of(data: dict, items: list) -> dict:
    return {"guid": str(data["show"].get("podcast_guid", "")), "items": items}


# ── Checks ──────────────────────────────────────────────────────────────────────────────

def chapter_findings(chapters: list, seconds: float, pt: dict, label: str) -> tuple:
    """(findings, warnings) for an episode's chapters against [platform.podcast]."""
    if not chapters:
        return [], []
    found, warns, starts = [], [], []
    for n, c in enumerate(chapters, start=1):
        try:
            starts.append(C.parse_tc(c.get("start", ""), f"{label} chapter {n} start"))
        except C.Fatal as err:
            found.append(str(err))
            return found, warns
    least = int(pt.get("chapters_min") or 0)
    if least and len(chapters) < least:
        found.append(f"{label} has {len(chapters)} chapter(s); platform.podcast.chapters_min is {least}")
    if starts[0] > 0.0005:
        found.append(f"{label}'s first chapter starts at {C.fmt_tc(starts[0])}; it must start at 00:00:00.000")
    for n in range(1, len(starts)):
        if starts[n] <= starts[n - 1]:
            found.append(f"{label} chapter {n + 1} starts at {C.fmt_tc(starts[n])}, not after chapter {n}")
    if seconds and any(s >= seconds for s in starts):
        found.append(f"{label} has a chapter starting at or after the end ({C.fmt_tc(seconds)})")
    if seconds and pt.get("chapters_per_hour_max"):
        allowed = int(pt["chapters_per_hour_max"]) * max(1, math.ceil(seconds / 3600))
        if len(chapters) > allowed:
            found.append(f"{label} has {len(chapters)} chapters; platform.podcast.chapters_per_hour_max allows "
                         f"{allowed} for its length")
    longest = int(pt.get("chapter_title_max_chars") or 0)
    words = int(pt.get("chapter_title_max_words") or 0)
    for n, c in enumerate(chapters, start=1):
        title = str(c.get("title", "")).strip()
        if not title:
            found.append(f"{label} chapter {n} has no title")
        if longest and len(title) > longest:
            found.append(f"{label} chapter {n}'s title is {len(title)} characters; platform.podcast."
                         f"chapter_title_max_chars is {longest}")
        if "<" in title or ">" in title:
            found.append(f"{label} chapter {n}'s title holds '<' or '>'")
        if words and len(title.split()) > words:
            warns.append(f"{label} chapter {n}'s title is {len(title.split())} words; platform.podcast."
                         f"chapter_title_max_words is {words} (unconfirmed: verify)")
    gap = float(pt.get("chapter_min_seconds") or 0)
    ends = starts[1:] + ([seconds] if seconds else [])
    for n, (s, e) in enumerate(zip(starts, ends), start=1):
        if gap and e - s < gap:
            warns.append(f"{label} chapter {n} lasts {e - s:.1f} s; platform.podcast.chapter_min_seconds is "
                         f"{gap:g} (Apple's best practice)")
    return found, warns


def personal(address: str) -> bool:
    local, _, domain = str(address).partition("@")
    return domain.lower() in PERSONAL_DOMAINS or bool(re.fullmatch(r"[a-z]+[._][a-z]+", local.lower()))


def value_findings(data: dict, text: str, items: list, pt: dict, show_name: str) -> tuple:
    """(findings, warnings) from the register's own values: what feed write and feed check share."""
    s = data["show"]
    found, warns = [], []
    if re.search(r"#\s*AUTHOR TO CONFIRM:", text):
        found.append("the register still carries an AUTHOR TO CONFIRM flag: confirm the value with the author "
                     "and delete the flag's line")
    if str(s.get("show", "")) != show_name:
        found.append(f"[show] show is {s.get('show')!r}; the register's name says {show_name!r}")
    for key in ("title", "link", "feed_url", "media_base", "language", "author", "owner_name", "owner_email",
                "category", "cover", "podcast_guid", "description", "approved"):
        if not str(s.get(key, "") or "").strip():
            found.append(f"[show] {key} is empty")
    if str(s.get("podcast_guid", "")).strip() and not GUID_RE.fullmatch(str(s["podcast_guid"])):
        found.append(f"[show] podcast_guid {s['podcast_guid']!r} is not a UUID")
    if str(s.get("approved", "")).strip():
        try:
            C.parse_date(str(s["approved"]))
        except C.Fatal as err:
            found.append(f"[show] approved: {err}")
    if s.get("type", "episodic") not in (pt.get("show_types") or ["episodic", "serial"]):
        found.append(f"[show] type {s.get('type')!r} is not one of platform.podcast.show_types")
    if s.get("youtube_route", "upload") not in ROUTES:
        found.append(f"[show] youtube_route {s.get('youtube_route')!r} is not upload, rss or none")
    for key in ("explicit", "locked", "complete", "block"):
        if key in s and not isinstance(s[key], bool):
            found.append(f"[show] {key} is not true or false")
    tag_max = int(pt.get("tag_max_chars") or 0)
    if tag_max and len(str(s.get("title", ""))) > tag_max:
        found.append(f"[show] title is {len(str(s['title']))} characters; platform.podcast.tag_max_chars is {tag_max}")
    desc = plain(s.get("description", ""))
    most = int(pt.get("show_description_max_bytes") or 0)
    if most and len(desc.encode("utf-8")) > most:
        found.append(f"[show] description is {len(desc.encode('utf-8'))} bytes; platform.podcast."
                     f"show_description_max_bytes is {most}")
    for key in ("title", "description"):
        if "<" in str(s.get(key, "")) or ">" in str(s.get(key, "")):
            found.append(f"[show] {key} holds '<' or '>' (plain text only: YouTube's RSS ingestion refuses them)")
    urls = [("feed_url", s.get("feed_url")), ("link", s.get("link")), ("media_base", s.get("media_base")),
            ("new_feed_url", s.get("new_feed_url")), ("cover", url_of(s.get("media_base", ""), s.get("cover", "")))]
    email = str(s.get("owner_email", "") or "").strip()
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        found.append(f"[show] owner_email {email!r} is not an email address")
    elif email and personal(email):
        warns.append(f"[show] owner_email {email} looks like a person's own address: it is public, so use a role "
                     "address the brand reads (DESIGN D36)")
    if not str(s.get("site", "") or "").strip() and C.path("brand/src/platforms/website.md").is_file():
        warns.append("[show] site is empty while the project has a website profile: name the site that serves the feed")
    serial = s.get("type") == "serial"
    seen_urls = {}
    all_guids = {}
    for e in episodes(data):
        g = str(e.get("guid", ""))
        if g:
            if g in all_guids:
                found.append(f"{e.get('piece')} and {all_guids[g]} share the GUID {g}")
            all_guids[g] = e.get("piece")
        if str(e.get("status", "planned")) not in STATUSES:
            found.append(f"{e.get('piece')}: status {e.get('status')!r} is not planned, ready, published or withdrawn")
    for i in items:
        e, label = i["row"], i["piece"] or "an episode"
        if not GUID_RE.fullmatch(i["guid"]):
            found.append(f"{label}: guid {i['guid']!r} is not a UUID (feed add writes it)")
        for key in ("title", "description"):
            if not str(e.get(key, "") or "").strip():
                found.append(f"{label}: {key} is empty")
            if "<" in str(e.get(key, "")) or ">" in str(e.get(key, "")):
                found.append(f"{label}: {key} holds '<' or '>' (plain text only)")
        if tag_max and len(i["title"]) > tag_max:
            found.append(f"{label}: title is {len(i['title'])} characters; platform.podcast.tag_max_chars is {tag_max}")
        cap = int(pt.get("episode_description_max_chars") or 0)
        if cap and len(i["description"]) > cap:
            found.append(f"{label}: description is {len(i['description'])} characters; platform.podcast."
                         f"episode_description_max_chars is {cap}")
        if i["when"] is None:
            found.append(f"{label}: pub_date {e.get('pub_date')!r} is not DD/MM/YYYY HH:MM")
        if e.get("type", "full") not in (pt.get("episode_types") or ["full", "trailer", "bonus"]):
            found.append(f"{label}: type {e.get('type')!r} is not one of platform.podcast.episode_types")
        if serial and not int(e.get("number", 0) or 0):
            found.append(f"{label}: a serial show numbers every episode, and its number is 0")
        if not i["url"]:
            found.append(f"{label}: no enclosure URL (feed tag writes render; media_base and render give the URL)")
        elif i["url"] in seen_urls:
            found.append(f"{label} and {seen_urls[i['url']]} enclose the same URL {i['url']}")
        seen_urls[i["url"]] = label
        if i["length"] <= 0 or float(e.get("seconds", 0) or 0) <= 0:
            found.append(f"{label}: bytes and seconds are not written: run feed tag")
        urls += [(f"{label} audio", i["url"]), (f"{label} page", i["page"]), (f"{label} art", i["art"]),
                 (f"{label} transcript", i["transcript"])]
        cf, cw = chapter_findings(chapters_of(e), float(e.get("seconds", 0) or 0), pt, label)
        found += cf
        warns += cw
        if not i["page"]:
            warns.append(f"{label}: page is empty (the episode page on the feed's site)")
        if not i["transcript"]:
            warns.append(f"{label}: transcript is empty (the master-timed VTT the feed names for Apple)")
    for what, url in urls:
        url = str(url or "").strip()
        if url and (not url.isascii() or " " in url):
            found.append(f"{what} URL {url!r} is not plain ASCII with no spaces (Apple)")
        elif url and not url.startswith("https://"):
            warns.append(f"{what} URL {url} is not https")
    return found, warns


def image_findings(p: Path, table: dict, label: str) -> list:
    """A local cover or episode art against its table: size, shape, minimum and alpha."""
    info = C.probe(p)
    v = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
    if not v:
        return [f"{label} {C.shown(p)} holds no picture"]
    w, h = int(v[0].get("width") or 0), int(v[0].get("height") or 0)
    found = []
    if table.get("aspect") == "1:1" and w != h:
        found.append(f"{label} is {w}x{h}; {table['key']} is square ({table['aspect']})")
    if table.get("min_width") and w < int(table["min_width"]):
        found.append(f"{label} is {w} px wide; {table['key']} min_width is {table['min_width']}")
    if table.get("width") and w > int(table["width"]):
        found.append(f"{label} is {w} px wide; {table['key']} width is {table['width']} at most")
    if table.get("alpha") is False and C.has_alpha(v[0].get("pix_fmt")):
        found.append(f"{label} keeps an alpha channel; {table['key']} sets alpha = false")
    return found


def render_path(name: str) -> Path:
    """Where a render named name lives: its piece's publishing/src/renders/<piece>/, or the folder's
    top for a name with no piece key, such as a show's cover encodes (DESIGN D64, Section 6.16)."""
    name = Path(name).name
    return C.piece_folder(C.PUB_RENDERS, name) / name


def local_render(name: str, warns: list):
    """The render named name as feed check reads it (DESIGN D65): in its piece's folder, or, where
    that has none, flat at the top of publishing/src/renders/ where an earlier release left it,
    named in a warning, so a published episode is never silently left unchecked. None where
    neither exists."""
    p = render_path(name)
    if p.is_file():
        return p
    flat = C.path(C.PUB_RENDERS) / Path(name).name
    if flat != p and flat.is_file():
        warns.append(f"{flat.name} is not in {C.shown(p.parent)}/: the flat {C.shown(flat)} an earlier release "
                     f"left is checked in its place; move it into {C.shown(p.parent)}/ or make it again there, "
                     "where the toolkit reads it from this release on")
        return flat
    return None


def file_findings(data: dict, items: list, presets: dict) -> tuple:
    """(findings, warnings, notes): the renders, cover and art against the register, where they are
    local: each in its piece's folder, or a flat one an earlier release left, with a warning."""
    found, warns, notes = [], [], []
    s = data["show"]
    for key, name, label in (("podcast.cover", s.get("cover", ""), "the cover"),
                             ("podcast.id3_cover", s.get("id3_cover", ""), "the ID3 cover")):
        name = str(name or "").strip()
        if not name or re.match(r"^https?://", name):
            continue
        p = local_render(name, warns)
        if p:
            found += image_findings(p, C.preset(key, presets), label)
        else:
            notes.append(f"{label} {name} is not in {C.shown(render_path(name).parent)}/: its size and alpha are "
                         "not checked here")
    for i in items:
        e = i["row"]
        render = str(e.get("render", "") or "").strip()
        if render:
            p = local_render(render, warns)
            if p:
                if p.stat().st_size != i["length"]:
                    found.append(f"{i['piece']}: bytes is {i['length']}; {render} is {p.stat().st_size} bytes "
                                 "(tagged or encoded again since: run feed tag)")
                try:
                    got = C.duration(C.probe(p))
                    if abs(got - float(e.get("seconds", 0) or 0)) > 0.05:
                        found.append(f"{i['piece']}: seconds is {e.get('seconds')}; {render} lasts {got:.3f} s")
                except C.Fatal as err:
                    notes.append(f"{i['piece']}: {err}")
            else:
                notes.append(f"{i['piece']}: {render} is not in {C.shown(render_path(render).parent)}/ (renders are "
                             "not kept): bytes and seconds are not checked against it")
        art = str(e.get("art", "") or "").strip()
        if art and not re.match(r"^https?://", art):
            p = local_render(art, warns)
            if p:
                found += image_findings(p, C.preset("podcast.episode_art", presets), f"{i['piece']}'s art")
    return found, warns, notes


# ── Commands ────────────────────────────────────────────────────────────────────────────

REGISTER_HEAD = """\
# {show}.toml: the show register of {show} (DESIGN Section 6.17), the one source of its feed.
# Written by python3 toolkit/media.py feed new; feed add appends each [[episode]] row, and feed tag
# writes render, bytes and seconds. Write the words by hand; never edit feed_url, podcast_guid or a
# guid: they are the show's and each episode's identity for life (feed new --rekey alone changes
# them, and only before anything is published).
"""
EPISODES_NOTE = "\n# Episodes: 'python3 toolkit/media.py feed add {show} --piece <piece>' appends one row each.\n"


def fill_line(lines: list, key: str, value) -> None:
    for n, line in enumerate(lines):
        if re.match(KEY_RE.format(key=re.escape(key)), line):
            lines[n] = set_line(line, key, value)
            return
    raise C.Fatal(f"the skeleton has no {key}")


def cmd_new(args) -> int:
    show = check_show(args.show)
    need_folder()
    url = check_feed_url(args.feed_url)
    site = (args.site or "").strip()
    if site and not SLUG_RE.fullmatch(site):
        raise C.Fatal(f"--site {site!r} is not a kebab slug (the website profile's slug of the site)")
    p = register_path(show)
    guid = podcast_guid(url)
    if args.rekey:
        if site:
            raise C.Fatal("--rekey changes only the feed URL and the GUIDs: write site in the register by hand")
        _, text, data = load(show)
        live = [e.get("piece") for e in episodes(data) if str(e.get("status", "")) == "published"]
        if live:
            raise C.Fatal(f"--rekey is refused: {', '.join(map(str, live))} is published, so the show's GUIDs are "
                          "public for life (a feed that moves keeps them: new_feed_url and a redirect)")
        if tracked_feed(show).exists():
            raise C.Fatal(f"--rekey is refused: {C.shown(tracked_feed(show))} exists, so the feed has been public")
        text = edit(text, "show", {"feed_url": url, "podcast_guid": guid})
        for e in episodes(data):
            piece = str(e.get("piece", ""))
            if piece:
                text = edit(text, "episode", {"guid": episode_guid(guid, piece)}, piece=piece)
        write_register(p, text)
        print(f"feed new --rekey {show}: feed_url {url}, podcast_guid {guid}, {len(episodes(data))} episode "
              f"guid(s) written again in {C.shown(p)}")
        return 0
    if p.exists():
        raise C.Fatal(f"{C.shown(p)} exists: a show is opened once (its feed URL and GUID are for life; "
                      "--rekey corrects them only before anything is published)")
    show_part, _, _ = skeleton_parts()
    lines = show_part.split("\n")
    fill_line(lines, "show", show)
    fill_line(lines, "feed_url", url)
    fill_line(lines, "podcast_guid", guid)
    if site:
        fill_line(lines, "site", site)
    at = next(n for n, ln in enumerate(lines) if re.match(KEY_RE.format(key="owner_email"), ln))
    lines.insert(at, FLAG)
    write_register(p, REGISTER_HEAD.format(show=show) + "\n" + "\n".join(lines) + "\n"
                   + EPISODES_NOTE.format(show=show))
    print(f"feed new {show}: wrote {C.shown(p)} (podcast:guid {guid}, from {bare_url(url)})")
    print("  next: write the show's details with the author (title, author, owner, category, description, "
          "cover, id3_cover), confirm owner_email and delete its flag, then date approved")
    if not site:
        print("  note: no --site: where the website platform is chosen, name the site that serves the feed in "
              "site; otherwise the podcast profile names the server")
    return 0


def cmd_add(args) -> int:
    show = check_show(args.show)
    piece = args.piece.strip()
    if not PIECE_RE.fullmatch(piece):
        raise C.Fatal(f"--piece {piece!r} is not NNN-kebab-title")
    p, text, data = load(show)
    if not (C.path(C.PIECES) / piece).is_dir():
        raise C.Fatal(f"{C.PIECES}/{piece}/ does not exist: an episode's GUID is written once, so the piece "
                      "must be the right one; open the piece first")
    if any(str(e.get("piece", "")) == piece for e in episodes(data)):
        raise C.Fatal(f"{piece} already has a row in {C.shown(p)}: a row is added once, and never deleted")
    show_guid = str(data["show"].get("podcast_guid", "")).strip()
    if not GUID_RE.fullmatch(show_guid):
        raise C.Fatal(f"[show] podcast_guid in {C.shown(p)} is not a UUID: feed new writes it")
    guid = episode_guid(show_guid, piece)
    _, episode, chapter = skeleton_parts()
    lines = episode.split("\n")
    fill_line(lines, "piece", piece)
    fill_line(lines, "guid", guid)
    block = "\n".join(lines) + "\n\n" + "\n".join("# " + ln for ln in chapter.split("\n"))
    write_register(p, text.rstrip("\n") + "\n\n" + block + "\n")
    print(f"feed add {show}: {piece}, guid {guid}, status planned, in {C.shown(p)}")
    print("  next: its words, pub_date and chapters with the author (a chapter: uncomment the "
          "[[episode.chapter]] table, one per chapter); then feed tag")
    return 0


def ffmeta_value(text) -> str:
    return re.sub(r"([=;#\\\n])", r"\\\1", str(text))


def cmd_tag(args) -> int:
    show = check_show(args.show)
    piece = args.piece.strip()
    p, text, data = load(show)
    row = row_of(data, piece, show)
    if str(row.get("status", "")) == "withdrawn":
        raise C.Fatal(f"{piece} is withdrawn: it leaves the feed, and its file is never tagged again")
    table = C.preset(FEED_AUDIO)
    render = render_path(f"{piece}.{C.file_form(FEED_AUDIO)}.mp3")
    if not render.is_file():
        # Only the piece's folder is read (DESIGN D65): a flat render an earlier release left is named,
        # never tagged, because the register's render is found in the piece's folder from now on.
        flat = C.path(C.PUB_RENDERS) / render.name
        raise C.Fatal(f"{C.shown(render)} does not exist: encode it at M5 (publishing/workflows/02-cut-for-a-platform/: "
                      f"media.py encode <master> --deliverable {FEED_AUDIO})"
                      + (f"; the flat {C.shown(flat)} an earlier release left is not read: move it into "
                         f"{C.shown(render.parent)}/ or encode it again" if flat.is_file() else ""))
    s, pt = data["show"], platform_podcast()
    info = C.probe(render)
    a = C.streams(info, "audio")
    if not a:
        raise C.Fatal(f"{C.shown(render)} has no sound")
    seconds = C.duration(info)
    found = []
    for key in ("title", "description"):
        if not str(row.get(key, "") or "").strip():
            found.append(f"{piece}: {key} is empty: write and approve the episode's words first")
    for key in ("title", "author"):
        if not str(s.get(key, "") or "").strip():
            found.append(f"[show] {key} is empty")
    chapters = chapters_of(row)
    cf, cw = chapter_findings(chapters, seconds, pt, piece)
    found += cf
    cover = None
    if str(s.get("id3_cover", "") or "").strip():
        name = str(s["id3_cover"]).strip()
        cover = C.path(name) if "/" in name else render_path(name)
        if not cover.is_file():
            raise C.Fatal(f"[show] id3_cover names {name}, and {C.shown(cover)} does not exist: encode it with "
                          "media.py image <the cover's design export> --deliverable podcast.id3_cover")
        found += image_findings(cover, C.preset("podcast.id3_cover"), "the ID3 cover")
        size = C.size_of(C.preset("podcast.id3_cover"))
        v = C.streams(C.probe(cover), "video") or [x for x in C.probe(cover).get("streams", [])
                                                    if x.get("codec_type") == "video"]
        if size and v and (int(v[0]["width"]), int(v[0]["height"])) != size:
            found.append(f"the ID3 cover is {v[0]['width']}x{v[0]['height']}; podcast.id3_cover is {size[0]}x{size[1]}")
    for w in cw:
        print(f"  warning: {w}")
    if found:
        for f in found:
            print(f"  FAIL {f}")
        print(f"feed tag {piece}: {len(found)} finding(s); nothing changed")
        return 1
    version = int(table.get("id3_version") or 3)
    meta = [";FFMETADATA1", f"title={ffmeta_value(row['title'])}", f"artist={ffmeta_value(s['author'])}",
            f"album={ffmeta_value(s['title'])}"]
    if int(row.get("number", 0) or 0):
        meta.append(f"track={int(row['number'])}")
    starts = [C.parse_tc(c["start"]) for c in chapters]
    for n, c in enumerate(chapters):
        end = starts[n + 1] if n + 1 < len(chapters) else seconds
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(round(starts[n] * 1000))}",
                 f"END={int(round(end * 1000))}", f"title={ffmeta_value(c.get('title', ''))}"]
    tmp_out = render.with_name(f".{render.stem}.tagging.mp3")
    with tempfile.TemporaryDirectory(prefix="media-feed-") as tmp:
        ffmeta = Path(tmp) / "tags.ffmeta"
        ffmeta.write_text("\n".join(meta) + "\n", encoding="utf-8")
        cmd = ["-y", "-i", str(render)]
        meta_index = 1
        if cover:
            cmd += ["-i", str(cover)]
            meta_index = 2
        cmd += ["-i", str(ffmeta), "-map", "0:a:0"]
        if cover:
            cmd += ["-map", "1:v:0"]
        cmd += ["-map_metadata", str(meta_index), "-map_chapters", str(meta_index if chapters else -1),
                "-c:a", "copy"]
        if cover:
            cmd += ["-c:v", "copy", "-disposition:v:0", "attached_pic", "-metadata:s:v", "title=Album cover",
                    "-metadata:s:v", "comment=Cover (front)"]
        cmd += ["-id3v2_version", str(version), "-write_id3v1", "0", "-f", "mp3", str(tmp_out)]
        try:
            C.ffmpeg(cmd, what="feed tag")
            problems = tag_findings(tmp_out, info, row, s, len(chapters), bool(cover), version)
            if problems:
                for f in problems:
                    print(f"  FAIL {f}")
                print(f"feed tag {piece}: the tagged file failed its verification; nothing changed")
                return 1
            os.replace(tmp_out, render)
        finally:
            if tmp_out.exists():
                tmp_out.unlink()
    n = render.stat().st_size
    got = C.duration(C.probe(render))
    write_register(p, edit(text, "episode", {"render": render.name, "bytes": n, "seconds": round(got, 3)}, piece=piece))
    print(f"feed tag {piece}: {C.shown(render)} tagged (ID3v2.{version}: title, author, show, "
          f"{'track, ' if int(row.get('number', 0) or 0) else ''}{len(chapters)} chapter(s)"
          f"{', cover' if cover else ''}); the audio stream unchanged")
    print(f"  wrote render = \"{render.name}\", bytes = {n}, seconds = {got:.3f} into {C.shown(p)}")
    if str(row.get("status", "")) == "published":
        print("  note: this episode is published, and its file now differs from the published one: publish it under "
              "a new name and set audio_url to the new URL (a -v2 before the extension); its guid stays (DESIGN D58)")
    return 0


def id3_version_of(p: Path):
    head = Path(p).read_bytes()[:4]
    return head[3] if head[:3] == b"ID3" else None


def tag_findings(p: Path, before: dict, row: dict, s: dict, chapters: int, cover: bool, version: int) -> list:
    proc = C.run([C.need("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
                  "-show_chapters", str(p)], what="ffprobe on the tagged file")
    info = json.loads(proc.stdout)
    found = []
    a0, a1 = C.streams(before, "audio")[0], (C.streams(info, "audio") or [{}])[0]
    for key in ("codec_name", "sample_rate", "channels"):
        if a0.get(key) != a1.get(key):
            found.append(f"the audio stream's {key} changed ({a0.get(key)} → {a1.get(key)})")
    if abs(C.duration(before) - C.duration(info)) > 0.05:
        found.append(f"the duration changed ({C.duration(before):.3f} → {C.duration(info):.3f} s)")
    tags = {k.lower(): v for k, v in info.get("format", {}).get("tags", {}).items()}
    for key, want in (("title", row.get("title")), ("artist", s.get("author")), ("album", s.get("title"))):
        if tags.get(key) != str(want):
            found.append(f"the {key} tag reads {tags.get(key)!r}, not {want!r}")
    if len(info.get("chapters", [])) != chapters:
        found.append(f"{len(info.get('chapters', []))} chapter(s) in the file; the row has {chapters}")
    if cover and not any(st.get("disposition", {}).get("attached_pic") for st in info.get("streams", [])):
        found.append("no cover (APIC) in the file")
    if id3_version_of(p) != version:
        found.append(f"the file's ID3 tag is version 2.{id3_version_of(p)}, not 2.{version}")
    return found


def cmd_write(args) -> int:
    show = check_show(args.show)
    p, text, data = load(show)
    as_of = C.parse_datetime(args.as_of, "--as-of")
    presets = C.load_presets(quiet=True)[0]
    items = included(data, as_of)
    if not items:
        raise C.Finding(f"no episode of {show} is ready or published by {args.as_of}: a feed carries at least "
                        "one (set the row ready at M7, with its pub_date)")
    found, warns = value_findings(data, text, items, presets.get("platform", {}).get("podcast", {}), show)
    tracked = tracked_feed(show)
    if tracked.is_file():
        try:
            found += compare(model_of(data, items), parse_feed(tracked), data, f"the tracked {tracked.name}")
        except C.Finding as err:
            found.append(str(err))
    report = sys.stderr if not args.o else sys.stdout
    for w in warns:
        print(f"  warning: {w}", file=report)
    if found:
        for f in found:
            print(f"  FAIL {f}", file=report)
        print(f"feed write {show}: {len(found)} finding(s); nothing written", file=report)
        return 1
    table = C.preset(FEED_AUDIO, presets)
    xml = build_xml(data, items, as_of, str(table.get("enclosure_type") or "audio/mpeg"))
    ET.fromstring(xml.encode("utf-8"))   # well-formed, or this is a bug: it raises
    if not args.o:
        sys.stdout.write(xml)
        sys.stdout.flush()
        print(f"feed write {show}: {len(items)} episode(s) as of {args.as_of} (to stdout)", file=sys.stderr)
        return 0
    out = C.output_path(Path(args.o), None, inputs=[p], tracked_feed=tracked)
    C.replace_file(out, xml.encode("utf-8"))
    what = "the tracked feed, replaced" if out.resolve() == tracked.resolve() else "the upload copy" \
        if C.in_output_folder(out) else "a copy"
    print(f"feed write {show}: wrote {C.shown(out)} ({what}): {len(items)} episode(s) as of {args.as_of}, "
          f"newest {items[0]['piece']}")
    return 0


def cmd_chapters(args) -> int:
    show = check_show(args.show)
    piece = args.piece.strip()
    _, _, data = load(show)
    row = row_of(data, piece, show)
    chapters = chapters_of(row)
    if not chapters:
        print(f"  FAIL {piece} has no [[episode.chapter]] rows")
        return 1
    found, warns = chapter_findings(chapters, float(row.get("seconds", 0) or 0), platform_podcast(), piece)
    for w in warns:
        print(f"  warning: {w}")
    if found:
        for f in found:
            print(f"  FAIL {f}")
        print(f"feed chapters {piece}: {len(found)} finding(s); nothing written")
        return 1
    doc = {"version": "1.2", "title": str(row.get("title", "")), "podcastName": str(data["show"].get("title", ""))}
    if str(row.get("render", "") or "").strip():
        doc["fileName"] = str(row["render"])
    doc["chapters"] = [{"startTime": round(C.parse_tc(c["start"]), 3), "title": str(c.get("title", ""))}
                       for c in chapters]
    out = C.output_path(render_path(f"{piece}.chapters.json"), args.o)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"feed chapters {piece}: wrote {C.shown(out)} ({len(chapters)} chapter(s), JSON chapters version 1.2)")
    return 0


def feed_file_findings(feed: dict, pt: dict) -> tuple:
    """(findings, warnings) for a saved feed read with --feed: the tags a directory needs."""
    found, warns = [], []
    for key, label in (("title", "<title>"), ("link", "<link>"), ("description", "<description>"),
                       ("language", "<language>"), ("author", "<itunes:author>"), ("image", "<itunes:image href>"),
                       ("explicit", "<itunes:explicit>"), ("owner_email", "<itunes:owner><itunes:email>")):
        if not feed.get(key):
            found.append(f"the channel has no {label}")
    if not feed.get("category"):
        found.append("the channel has no <itunes:category>")
    if not feed["guid"]:
        warns.append("the channel has no <podcast:guid>")
    if not feed["items"]:
        found.append("the feed carries no episode")
    guids, urls = {}, {}
    for n, i in enumerate(feed["items"], start=1):
        label = f"item {n} ('{i['title'] or ''}')"
        for key in ("title", "guid", "pubDate", "description"):
            if not i.get(key):
                found.append(f"{label} has no <{key}>")
        if i["pubDate"]:
            try:
                parsedate_to_datetime(i["pubDate"])
            except (TypeError, ValueError):
                found.append(f"{label}: pubDate {i['pubDate']!r} is not an RFC 2822 date")
        if not i["url"] or i["length"] < 0 or not i["type"]:
            found.append(f"{label} has no complete <enclosure url length type>")
        for key in ("title", "description"):
            if i.get(key) and ("<" in i[key] or ">" in i[key]):
                found.append(f"{label}: its {key} holds '<' or '>' (plain text only)")
        if i["guid"] in guids:
            found.append(f"{label} repeats the GUID of item {guids[i['guid']]}")
        guids.setdefault(i["guid"], n)
        if i["url"] in urls:
            found.append(f"{label} encloses the same URL as item {urls[i['url']]}")
        urls.setdefault(i["url"], n)
        if i["url"] and not i["url"].isascii():
            found.append(f"{label}: its enclosure URL is not ASCII")
        if i["chapters"]:
            rows = [{"start": s, "title": t} for s, t in i["chapters"]]
            cf, cw = chapter_findings(rows, 0.0, pt, label)
            found += cf
            warns += cw
    return found, warns


def cmd_check(args) -> int:
    show = check_show(args.show)
    need_folder()
    presets = C.load_presets(quiet=True)[0]
    pt = presets.get("platform", {}).get("podcast", {})
    reg = register_path(show)
    data = C.load_toml(reg) if reg.is_file() else None
    found, warns, notes = [], [], []
    if args.feed:
        feed = parse_feed(Path(args.feed))
        label = C.shown(args.feed)
        f, w = feed_file_findings(feed, pt)
        found += f
        warns += w
        new = feed
    else:
        if data is None:
            raise C.Fatal(f"{C.shown(reg)} does not exist: open the show with 'media.py feed new {show} --feed-url URL'")
        if not isinstance(data.get("show"), dict):
            raise C.Fatal(f"{C.shown(reg)} has no [show] table")
        label = C.shown(reg)
        items = included(data, None, tagged_planned=True)
        f, w = value_findings(data, C.read_text(reg), items, pt, show)
        found += f
        warns += w
        f, w, n = file_findings(data, items, presets)
        found += f
        warns += w
        notes += n
        new = model_of(data, items)
        untagged = [str(e.get("piece")) for e in episodes(data) if str(e.get("status", "planned")) == "planned"
                    and not str(e.get("render", "") or "").strip()]
        if untagged:
            notes.append(f"not yet tagged, so left out of this check: {', '.join(untagged)}")
    previous = Path(args.previous) if args.previous else tracked_feed(show)
    if previous.is_file() and (not args.feed or Path(args.feed).resolve() != previous.resolve()):
        try:
            found += compare(new, parse_feed(previous), data, f"the {'previous' if args.previous else 'tracked'} "
                             f"{previous.name}")
        except C.Finding as err:
            found.append(str(err))
    elif args.previous:
        raise C.Fatal(f"--previous {C.shown(previous)} does not exist")
    else:
        notes.append(f"no tracked {previous.name} yet: nothing published to compare with")
    print(f"feed check {label} (offline; nothing is fetched)")
    for n in notes:
        print(f"  note: {n}")
    for w in warns:
        print(f"  warning: {w}")
    for f in found:
        print(f"  FAIL {f}")
    print(f"feed check {show}: {'clean' if not found else f'{len(found)} finding(s)'}"
          + (f", {len(warns)} warning(s)" if warns else ""))
    return 1 if found else 0


def uuid5_by_hand(namespace: str, name: str) -> str:
    """RFC 4122 version 5, written out (SHA-1 of the namespace's bytes and the name): the self-test
    proves podcast_guid against it, without the uuid module's help."""
    digest = bytearray(hashlib.sha1(uuid.UUID(namespace).bytes + name.encode("utf-8")).digest()[:16])
    digest[6] = (digest[6] & 0x0F) | 0x50
    digest[8] = (digest[8] & 0x3F) | 0x80
    h = digest.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


if __name__ == "__main__":
    sys.exit("media_feed.py has no command of its own: run python3 toolkit/media.py feed --help")
