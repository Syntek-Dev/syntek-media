#!/usr/bin/env python3
"""media_scene.py: deterministic scene state for the media toolkit (D70, D71).

Standard-library helpers, exercised by media.py's self-test. Frame positions are
whole design pixels at device scale one; all timing is calculated outside the page.
The scene runner supplies the author-selected layout and deliverable tables.
"""
from __future__ import annotations

import math
from bisect import bisect_right

import media_common as C


def number(value, label: str) -> float:
    """A finite real value, with a named toolkit error instead of an encoder failure."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise C.Fatal(f'{label} must be a finite number')
    return float(value)


def whole(value, label: str, minimum: int = 0) -> int:
    result = number(value, label)
    if not result.is_integer() or result < minimum:
        raise C.Fatal(f'{label} must be a whole number at least {minimum}')
    return int(result)


def frame_time(frame: int, fps: float = 30, offset: float = 0) -> float:
    """The middle of a frame relative to the joined voice, including its EDL offset."""
    frame = whole(frame, 'frame')
    fps = number(fps, 'fps')
    if fps <= 0:
        raise C.Fatal('fps must be greater than zero')
    return (frame + 0.5) / fps - number(offset, 'voice offset')


class MouthTimeline:
    """Validated native Rhubarb intervals; gaps and times outside speech use rest X."""
    def __init__(self, cues: list):
        if not isinstance(cues, list):
            raise C.Fatal('mouthCues must be a list; run lipsync again')
        self.cues = []
        last_end = 0.0
        for cue in cues:
            if not isinstance(cue, dict) or cue.get('value') not in tuple('ABCDEFGHX'):
                raise C.Fatal('invalid mouth shape; run lipsync again')
            start = number(cue.get('start'), 'mouth cue start')
            end = number(cue.get('end'), 'mouth cue end')
            if start < last_end or end <= start:
                raise C.Fatal('mouth cues must be ordered, non-overlapping intervals; run lipsync again')
            self.cues.append((start, end, cue['value']))
            last_end = end
        self.starts = [cue[0] for cue in self.cues]

    def shape(self, frame: int, fps: float = 30, offset: float = 0) -> str:
        t = frame_time(frame, fps, offset)
        at = bisect_right(self.starts, t) - 1
        if at >= 0 and t < self.cues[at][1]:
            return self.cues[at][2]
        return 'X'


def safe_zone(width: int, height: int, tables: list[dict]) -> dict[str, int]:
    """Largest scaled margin on each edge among deliverables of this exact aspect.

    Use card.py's rounding convention, so frame and safe variables agree between
    still cards and scenes. The caller gathers the brief and cut-down deliverables.
    """
    width, height = whole(width, 'frame width', 1), whole(height, 'frame height', 1)
    zone = dict.fromkeys(('top', 'bottom', 'left', 'right'), 0)
    for table in tables:
        tw, th = table.get('width'), table.get('height')
        if tw is None or th is None:
            continue  # An audio deliverable has no picture and contributes no margin.
        tw, th = whole(tw, 'deliverable width', 1), whole(th, 'deliverable height', 1)
        if tw * height != th * width:
            continue
        margins = table.get('safe_zone') or {}
        if not isinstance(margins, dict):
            raise C.Fatal('deliverable safe_zone must be a table')
        for edge, total, size in (('top', height, th), ('bottom', height, th),
                                  ('left', width, tw), ('right', width, tw)):
            value = number(margins.get(edge, 0), f'safe {edge}')
            if value < 0:
                raise C.Fatal(f'safe {edge} must not be negative')
            zone[edge] = max(zone[edge], round(value * total / size))
    return zone


def frame_vars(width: int, height: int, tables: list[dict]) -> dict[str, str]:
    width, height = whole(width, 'frame width', 1), whole(height, 'frame height', 1)
    zone = safe_zone(width, height, tables)
    return {'--frame-width': f'{width}px', '--frame-height': f'{height}px',
            **{f'--safe-{edge}': f'{value}px' for edge, value in zone.items()}}


def typed_text(text: str, frame: int, start: int, frames_per_character: int) -> str:
    """Reveal one more character per author-set frame hold, starting at start."""
    frame, start = whole(frame, 'frame'), whole(start, 'typed line start')
    hold = whole(frames_per_character, 'frames per character', 1)
    count = 0 if frame < start else 1 + (frame - start) // hold
    return text[:count]


def brand_tokens() -> dict:
    """Read the brand's declared custom properties through the existing token reader."""
    return C.read_tokens()


# The scene's author sets layouts and holds; the kit supplies timing and neutral painting.
import json
import os
import re
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from urllib.parse import quote


@dataclass
class Keyframe:
    at: int | str
    x: int | None = None
    y: int | None = None
    anchor: str | None = None
    pose: str | None = None
    facing: str | None = None
    response: dict = field(default_factory=dict)


@dataclass
class Sprite:
    folder: str = ''                  # explicit brand export folder; never a directory scan
    name: str = 'character'
    extension: str = '.png'
    scale: int = 1
    layered: bool = False
    mouth: tuple[int, int] = (0, 0)   # mouth-layer origin in unscaled sprite pixels
    walk: tuple[str, ...] = ()
    walk_hold: int = 3
    breathe_hold: int = 30
    blink_every: int = 120
    blink_frames: int = 3
    css_frames: dict = field(default_factory=dict)  # author-supplied geometry, used by runtime fixtures


@dataclass
class Element:
    name: str
    kind: str = 'text'               # text, graphic, source, sprite
    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1
    layer: int = 0
    text: str = ''
    source: str = ''                 # a source key of the accepted real index
    style: dict = field(default_factory=dict)  # brand custom-property values only
    start: int | str = 0
    end: int | str | None = None
    type_hold: int = 1
    typed: bool = False
    pose: str = 'idle'
    facing: str = 'right'
    hold: int = 1                    # movement holds for this many whole frames
    anchors: dict = field(default_factory=dict)  # local points, e.g. {'left': (0, 0)}
    keyframes: list[Keyframe] = field(default_factory=list)
    responses: list[dict] = field(default_factory=list)
    sprite: Sprite | None = None


def local_path(root: Path, value: str, parent: str | None = None) -> Path:
    # Keep explicit local-mirror symlinks usable; confine the declared path, not its storage.
    p = Path(os.path.abspath(root / value))
    base = Path(os.path.abspath(root / parent)) if parent else root.resolve()
    if not p.is_relative_to(base):
        raise C.Fatal(f'scene path {value!r} must stay inside {parent or "the repository"}')
    return p


def timing_file(root: Path, name: str, command: str):
    p = root / name
    if not p.is_file():
        raise C.Fatal(f'{name} is missing: run {command}')
    try:
        return json.loads(p.read_text(encoding='utf-8'), parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
    except (OSError, ValueError) as err:
        raise C.Fatal(f'{name} is unreadable: {err}; run {command}') from None


class Scene:
    """A tracked scene returns Scene(root, piece, frames, layout, fps=30).

    layout(width, height, safe) returns Elements for that native frame size. Timing
    references are beat:ID, board:ID, line:ID and word:INDEX (their starts on the voice).
    A reference may end in :end. Integer at values are already master frame numbers.
    """
    def __init__(self, root: Path, piece: str, frames: int, layout, fps: float = 30,
                 stylesheets: tuple[str, ...] = ()):
        self.root, self.piece = Path(root).resolve(), piece
        if not re.fullmatch(r'\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*', piece):
            raise C.Fatal('a scene needs its NNN-kebab-title piece key')
        self.frames, self.fps = whole(frames, 'scene frames', 1), number(fps, 'scene fps')
        if self.fps <= 0 or not callable(layout):
            raise C.Fatal('a scene needs positive fps and a callable layout(width, height, safe)')
        self.layout, self.stylesheets = layout, stylesheets
        self.cues = timing_file(self.root, f'{C.SCENES}/{piece}.cues.json', f'media.py cues {piece} -o {C.SCENES}/{piece}.cues.json')
        self.words = timing_file(self.root, f'{C.TIMING}/{piece}.words.json', f'media.py transcribe {piece} -o {C.TIMING}/{piece}.words.json')
        mouth = timing_file(self.root, f'{C.TIMING}/{piece}.mouth.json', f'media.py lipsync {piece} -o {C.TIMING}/{piece}.mouth.json')
        self.real = timing_file(self.root, f'{C.SCENES}/{piece}.real.json', f'media.py real {piece} -o {C.SCENES}/{piece}.real.json')
        if not isinstance(self.cues, dict) or self.cues.get('piece') != piece or not isinstance(self.words, list):
            raise C.Fatal('scene cues or words do not match the piece; run cues and transcribe again')
        if not isinstance(mouth, dict):
            raise C.Fatal('mouth JSON must be the native lipsync object')
        self.mouth = MouthTimeline(mouth.get('mouthCues'))
        if not isinstance(self.real, dict) or self.real.get('piece') != piece or not isinstance(self.real.get('sources'), list):
            raise C.Fatal('real JSON must name this piece and its sources; run real again')
        self.sources = {}
        for row in self.real['sources']:
            if not isinstance(row, dict) or row.get('kind') not in ('image', 'text') or not row.get('source') \
                    or row['source'] in self.sources or not isinstance(row.get('path'), str) \
                    or Path(row['path']).is_absolute() or not re.fullmatch(r'[a-f0-9]{64}', str(row.get('sha256', ''))):
                raise C.Fatal('invalid real source; run real again')
            self.sources[row['source']] = row
        self.edl = C.load_toml(self.root / C.EDITS / f'{piece}.toml')
        edit = self.edl.get('edit', {})
        if edit.get('piece') != piece or self.edl.get('clip') or self.edl.get('overlay'):
            raise C.Fatal('scene edit must name its piece and contain no clip or overlay rows')
        voices = [r for r in self.edl.get('audio', []) if r.get('source') == f'vo:{piece}']
        if len(voices) != 1:
            raise C.Fatal(f'scene edit needs exactly one audio source vo:{piece}')
        if voices[0].get('in') or voices[0].get('out'):
            raise C.Fatal('the scene joined voice cannot be trimmed: timing uses its full WAV')
        self.offset = C.parse_tc(voices[0].get('at') or 0, 'voice at')
        self.tables = self.deliverables()
        self.tokens = C.read_tokens(self.root / C.TOKENS)

    def deliverables(self) -> list[dict]:
        brief = self.root / C.PIECES / self.piece / 'brief.md'
        if not brief.is_file():
            raise C.Fatal(f'{brief.relative_to(self.root)} is missing: brief the piece first')
        text = brief.read_text(encoding='utf-8')
        header = text.split('---', 2)[1] if text.startswith('---') and text.count('---') >= 2 else ''
        block = re.search(r'^deliverables:\s*([^\n]*)(?:\n((?:[ \t]+[^\n]*\n?)*))', header, re.M)
        keys = set(re.findall(r'\b[a-z_]+\.[a-z_]+\b', ''.join(block.groups('')))) if block else set()
        plan = self.root / 'publishing/src/cut-downs' / f'{self.piece}.md'
        if plan.is_file():
            # Only the Deliverables column of the cut table contributes safe margins.
            for line in plan.read_text(encoding='utf-8').splitlines():
                if re.match(r'^\s*\|\s*c\d+\s*\|', line):
                    columns = line.split('|')
                    keys.update(re.findall(r'\b[a-z_]+\.[a-z_]+\b', columns[2]))
        data = C.load_presets()[0]
        return [C.preset(key, data=data) for key in sorted(keys)]

    def frame(self, reference: int | str) -> int:
        if not isinstance(reference, str):
            return whole(reference, 'keyframe at')
        bits = reference.split(':')
        end = len(bits) == 3 and bits[-1] == 'end'
        if len(bits) not in (2, 3) or len(bits) == 3 and not end:
            raise C.Fatal(f'invalid timing reference {reference!r}')
        group, name = bits[:2]
        if group == 'word':
            try: row = self.words[int(name)] if int(name) >= 0 else None
            except (ValueError, IndexError): row = None
        else:
            rows = self.cues.get({'beat': 'beats', 'board': 'boards', 'line': 'lines'}.get(group, ''), [])
            row = next((r for r in rows if str(r.get('id')) == name), None)
        if not row or row.get('end' if end else 'start') is None:
            raise C.Fatal(f'{reference!r} has no accepted time: run transcribe and cues again')
        seconds = number(row['end' if end else 'start'], reference) + self.offset
        # Boundaries begin at the first frame whose midpoint reaches them.
        return max(0, math.ceil(seconds * self.fps - 0.5))

    def elements(self, width: int, height: int) -> list[Element]:
        safe = safe_zone(width, height, self.tables)
        result = list(self.layout(width, height, safe))
        if any(not isinstance(e, Element) for e in result) or len({e.name for e in result}) != len(result):
            raise C.Fatal('scene layout must return Elements with unique names')
        for e in result:
            if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]*', e.name) or e.kind not in ('text', 'graphic', 'source', 'sprite'):
                raise C.Fatal(f'invalid scene element {e.name!r}')
            whole(e.width, f'{e.name} width', 1); whole(e.height, f'{e.name} height', 1)
            whole(e.hold, f'{e.name} movement hold', 1)
            self.frame(e.start)
            if e.end is not None: self.frame(e.end)
            if e.facing not in ('left', 'right'):
                raise C.Fatal(f'{e.name} facing must be left or right')
            if e.kind == 'sprite' and e.sprite is None:
                raise C.Fatal(f'{e.name} needs a Sprite slot')
            if e.sprite:
                sprite = e.sprite
                whole(sprite.scale, 'sprite scale', 1)
                for value in sprite.mouth: whole(value, 'native mouth origin')
                for parts in sprite.css_frames.values():
                    for part in parts:
                        for key in ('x', 'y'): whole(part[key], 'sprite part ' + key)
                        for key in ('width', 'height'): whole(part[key], 'sprite part ' + key, 1)
                        for key, value in part.get('style', {}).items():
                            if not re.fullmatch(r'[a-z-]+', key) or not re.fullmatch(r'var\(--[a-zA-Z0-9_-]+\)', str(value)):
                                raise C.Fatal('sprite geometry uses brand custom properties only')
            for key, value in e.style.items():
                if not re.fullmatch(r'[a-z-]+', key) or not re.fullmatch(r'var\(--[a-zA-Z0-9_-]+\)', str(value)):
                    raise C.Fatal(f'{e.name} style uses brand custom properties only')
        return sorted(result, key=lambda e: e.layer)

    def position(self, e: Element, frame: int, elements: dict, seen: tuple = ()) -> tuple:
        if e.name in seen:
            raise C.Fatal('cyclic scene anchors: ' + ' → '.join((*seen, e.name)))
        seen = (*seen, e.name)
        def point(key):
            x, y = e.x if key.x is None else key.x, e.y if key.y is None else key.y
            if key.anchor:
                name, sep, anchor = key.anchor.partition('.')
                target = elements.get(name)
                if not target:
                    raise C.Fatal(f'{e.name} names missing anchor element {name}')
                anchors = {'centre': (target.width // 2, target.height // 2), **target.anchors}
                if (anchor or 'centre') not in anchors:
                    raise C.Fatal(f'{name} has no anchor {anchor!r}')
                tx, ty, _ = self.position(target, self.frame(key.at), elements, seen)
                ax, ay = anchors[anchor or 'centre']
                x, y = tx + ax + (key.x or 0), ty + ay + (key.y or 0)
            return number(x, f'{e.name} x'), number(y, f'{e.name} y')
        keys = [Keyframe(0, e.x, e.y), *e.keyframes]
        keys.sort(key=lambda k: self.frame(k.at))
        before = [k for k in keys if self.frame(k.at) <= frame]
        current = before[-1]
        later = next((k for k in keys if self.frame(k.at) > frame), None)
        x, y = point(current)
        moving = False
        if later:
            end_x, end_y = point(later)
            start, end = self.frame(current.at), self.frame(later.at)
            elapsed = (frame - start) // e.hold * e.hold
            progress = elapsed / (end - start)
            moving = (x, y) != (end_x, end_y)
            # Author positions remain measurable in stills; interpolated moves are snapped.
            if moving:
                x, y = round(x + (end_x - x) * progress), round(y + (end_y - y) * progress)
        return x, y, moving

    def art(self, sprite: Sprite, stem: str, optional: bool = False) -> Path | None:
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', stem) or sprite.extension.lower() not in ('.png', '.svg', '.webp', '.jpg'):
            raise C.Fatal('sprite art needs a safe filename stem and a still-image extension')
        p = local_path(self.root, str(Path(sprite.folder) / (stem + sprite.extension)), 'brand')
        if optional and not p.is_file(): return None
        if not p.is_file(): raise C.Fatal(f'missing sprite frame: {p.relative_to(self.root)}')
        return p

    def state(self, frame: int, elements: list[Element], page: Path) -> list[dict]:
        frame = whole(frame, 'frame')
        if frame >= self.frames: raise C.Fatal('frame is outside the scene')
        names = {e.name: e for e in elements}
        def link(p): return quote(os.path.relpath(p, page.parent).replace(os.sep, '/'), safe='/')
        responses = {e.name: list(e.responses) for e in elements}
        for e in elements:
            for key in e.keyframes:
                if key.anchor and key.response:
                    target = key.anchor.partition('.')[0]
                    if target not in responses: raise C.Fatal(f'missing anchor element {target}')
                    responses[target].append({'at': key.at, **key.response})
        output = []
        for e in elements:
            start, end = self.frame(e.start), self.frame(e.end) if e.end is not None else self.frames
            if not start <= frame < end: continue
            x, y, moving = self.position(e, frame, names)
            text, style = e.text, dict(e.style)
            visible = True
            for response in responses[e.name]:
                if frame >= self.frame(response['at']):
                    if 'highlight' in response:
                        value = str(response['highlight'])
                        if not re.fullmatch(r'var\(--[a-zA-Z0-9_-]+\)', value):
                            raise C.Fatal('anchor highlights use a brand custom property')
                        style['background-color'] = value
                    dx, dy = response.get('nudge', (0, 0))
                    x += whole(abs(dx), 'nudge x') * (-1 if dx < 0 else 1)
                    y += whole(abs(dy), 'nudge y') * (-1 if dy < 0 else 1)
                    visible = bool(response.get('reveal', visible))
            state = {'name': e.name, 'kind': e.kind, 'x': x, 'y': y, 'width': e.width,
                     'height': e.height, 'text': text, 'style': style, 'visible': visible, 'images': []}
            if e.typed: state['text'] = typed_text(text, frame, start, e.type_hold)
            if e.kind == 'source':
                row = self.sources.get(e.source)
                if row is None: raise C.Fatal(f'{e.source!r} is not indexed: run real again')
                p = local_path(self.root, row['path'])
                if not p.is_file(): raise C.Fatal(f'missing real source: {row["path"]}; run real again')
                if row['kind'] == 'text':
                    state['kind'], state['text'] = 'text', p.read_text(encoding='utf-8')
                else: state['images'] = [{'src': link(p), 'x': 0, 'y': 0, 'width': e.width, 'height': e.height}]
            if e.sprite:
                s = e.sprite
                scale = whole(s.scale, 'sprite scale', 1)
                pose, facing = e.pose, e.facing
                for key in sorted(e.keyframes, key=lambda k: self.frame(k.at)):
                    if self.frame(key.at) > frame: break
                    pose, facing = key.pose or pose, key.facing or facing
                    if key.anchor and not key.facing:
                        target = names[key.anchor.partition('.')[0]]
                        tx, _, _ = self.position(target, frame, names)
                        facing = 'right' if tx >= x else 'left'
                if moving and s.walk:
                    pose = s.walk[(frame // whole(s.walk_hold, 'walk hold', 1)) % len(s.walk)]
                if facing not in ('left', 'right'): raise C.Fatal('sprite facing must be left or right')
                mouth = self.mouth.shape(frame, self.fps, self.offset)
                blink = bool(s.blink_every and frame % whole(s.blink_every, 'blink interval', 1)
                             < whole(s.blink_frames, 'blink frames', 1))
                bob = 0 if moving or not s.breathe_hold else (frame // whole(s.breathe_hold, 'breathing hold', 1) % 2) * scale
                state.update(pose=pose, facing=facing, mouth=mouth, blink=False, y=y + bob, scale=scale)
                if s.css_frames:
                    parts = s.css_frames.get(f'{pose}-mouth-{mouth}')
                    if parts is None: raise C.Fatal(f'missing sprite frame: {s.name}-{pose}-mouth-{mouth}')
                    state['parts'] = parts
                    state['blink'] = blink and 'blink' in s.css_frames
                    if state['blink']: state['parts'] = [*parts, *s.css_frames['blink']]
                elif s.layered:
                    base = self.art(s, f'{s.name}-{pose}')
                    mouth_path = self.art(s, f'{s.name}-mouth-{mouth.lower()}')
                    state['images'] = [{'src': link(base), 'x': 0, 'y': 0},
                                       {'src': link(mouth_path), 'x': s.mouth[0] * scale, 'y': s.mouth[1] * scale}]
                else:
                    state['images'] = [{'src': link(self.art(s, f'{s.name}-{pose}-mouth-{mouth.lower()}')), 'x': 0, 'y': 0}]
                if not s.css_frames and blink:
                    layer = self.art(s, f'{s.name}-{pose}-blink', optional=True)
                    if layer:
                        state['images'].append({'src': link(layer), 'x': 0, 'y': 0})
                        state['blink'] = True
            output.append(state)
        return output

    def write_page(self, width: int, height: int) -> tuple[Path, list[Element]]:
        elements = self.elements(width, height)
        page = self.root / C.PROD_RENDERS / self.piece / 'scene/index.html'
        page.parent.mkdir(parents=True, exist_ok=True)
        tokens = local_path(self.root, C.TOKENS, 'brand')
        links = [tokens, *[local_path(self.root, p, 'brand') for p in self.stylesheets]]
        if any(not p.is_file() or p.suffix != '.css' for p in links):
            raise C.Fatal('scene brand stylesheets must be existing local CSS files')
        link_html = ''.join('<link rel="stylesheet" href="' + escape(quote(os.path.relpath(p, page.parent), safe='/')) + '">' for p in links)
        # Each state is computed in Python. Javascript applies it without a clock or randomness.
        states = [self.state(n, elements, page) for n in range(self.frames)]
        encoded = json.dumps(states, ensure_ascii=False, allow_nan=False, separators=(',', ':')).replace('<', '\\u003c')
        page.write_text('<!doctype html><html><head><meta charset="utf-8">' + link_html +
                        '<style>' + PAINT_CSS + '</style></head><body><main id="scene"></main><script>const states=' +
                        encoded + ';' + PAINTER + '</script></body></html>', encoding='utf-8')
        return page, elements


PAINT_CSS = '''
*{box-sizing:border-box;animation:none!important;transition:none!important}
html,body{margin:0;width:var(--frame-width);height:var(--frame-height);overflow:hidden;
background:var(--color-bg);color:var(--color-text);font-family:var(--font-body)}
#scene{position:relative;width:var(--frame-width);height:var(--frame-height)}
.element{position:absolute;white-space:pre-wrap;overflow:hidden}
.element img{position:absolute;image-rendering:pixelated;max-width:none}
.sprite-content{position:absolute;inset:0;transform-origin:center}
.part{position:absolute}
'''
PAINTER = '''
window.draw = function(frame){
 if(!Number.isInteger(frame)||frame<0||frame>=states.length)throw Error('invalid frame');
 const root=document.getElementById('scene');root.replaceChildren();
 for(const state of states[frame]){
  const node=document.createElement('div');node.className='element';
  node.dataset.name=state.name;node.dataset.kind=state.kind;
  for(const key of ['pose','mouth','facing','blink'])if(key in state)node.dataset[key]=String(state[key]);
  Object.assign(node.style,{left:state.x+'px',top:state.y+'px',width:state.width+'px',height:state.height+'px',...state.style});
  if(!state.visible)node.style.visibility='hidden';
  node.textContent=state.text;
  const content=document.createElement('div');content.className='sprite-content';
  if(state.facing==='left')content.style.transform='scaleX(-1)';
  for(const image of state.images){
   const img=document.createElement('img');img.src=image.src;
   img.style.left=image.x+'px';img.style.top=image.y+'px';
   if(image.width){img.style.width=image.width+'px';img.style.height=image.height+'px'}
   else if(state.scale){img.style.transform='scale('+state.scale+')';img.style.transformOrigin='top left'}
   content.append(img);
  }
  for(const part of state.parts||[]){
   const div=document.createElement('div');div.className='part';
   Object.assign(div.style,{left:part.x*state.scale+'px',top:part.y*state.scale+'px',
     width:part.width*state.scale+'px',height:part.height*state.scale+'px',...part.style});content.append(div);
  }
  node.append(content);root.append(node);
 }
};
window.draw(0);
'''
