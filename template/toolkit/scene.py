#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright==1.62.0"]
# ///
"""scene.py: local, deterministic stills and native scene masters (D70–D72).

Usage:
    uv run toolkit/scene.py stills PIECE [--size WxH --size WxH]
    uv run toolkit/scene.py render PIECE [--size WxH] [--memory-max SIZE]
    uv run toolkit/scene.py --self-test

The tracked scene defines build_scene(root, piece), returning media_scene.Scene.
Every run executes it by path and writes its ignored page afresh. Exit codes:
0 verified, 1 findings, 2 could not run. No generation API or model fetch.
"""
from __future__ import annotations

import argparse
import json
import os
import runpy
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import card
import media_audio as A
import media_common as C
import media_scene as S
import media_video as V


BOXES = '''() => Array.from(document.querySelectorAll('.element')).filter(node =>
 ['text','sprite'].includes(node.dataset.kind) && getComputedStyle(node).visibility!=='hidden').map(node=>{
 const box=node.getBoundingClientRect();
 return {name:node.dataset.name,kind:node.dataset.kind,x:box.x,y:box.y,width:box.width,height:box.height,
 overflow:{width:Math.max(0,node.scrollWidth-node.clientWidth),height:Math.max(0,node.scrollHeight-node.clientHeight)}};
})'''


def box_findings(boxes: list, width: int, height: int, safe: dict) -> list[str]:
    found = []
    for box in boxes:
        name = box['name']
        if any(abs(box[key] - round(box[key])) > 0.001 for key in ('x', 'y', 'width', 'height')):
            found.append(f'{name}: box is off the design-pixel grid')
        if box['x'] < safe['left'] or box['y'] < safe['top'] \
                or box['x'] + box['width'] > width - safe['right'] \
                or box['y'] + box['height'] > height - safe['bottom']:
            found.append(f'{name}: box is outside the safe zone')
        if box['kind'] == 'text' and any(v > 0 for v in box['overflow'].values()):
            found.append(f'{name}: text overflows its box')
    texts = [b for b in boxes if b['kind'] == 'text']
    for n, a in enumerate(texts):
        for b in texts[n + 1:]:
            if max(a['x'], b['x']) < min(a['x'] + a['width'], b['x'] + b['width']) \
                    and max(a['y'], b['y']) < min(a['y'] + a['height'], b['y'] + b['height']):
                found.append(f'{a["name"]} and {b["name"]}: text boxes overlap')
    return found


def load_scene(piece: str) -> S.Scene:
    if not isinstance(piece, str) or not S.re.fullmatch(r'\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*', piece):
        raise C.Fatal('scene piece must be NNN-kebab-title')
    source = C.path(C.SCENES) / f'{piece}.scene.py'
    if not source.is_file():
        raise C.Fatal(f'{C.shown(source)} is missing: write the scene in production/workflows/10-animate-a-scene/')
    try:
        namespace = runpy.run_path(str(source))
        build = namespace.get('build_scene')
        if not callable(build): raise C.Fatal(f'{C.shown(source)} must define build_scene(root, piece)')
        scene = build(C.ROOT, piece)
    except (C.Fatal, C.Finding): raise
    except Exception as err:
        raise C.Fatal(f'{C.shown(source)} could not build its scene: {err}') from None
    if not isinstance(scene, S.Scene) or scene.piece != piece or scene.root != C.ROOT.resolve():
        raise C.Fatal('build_scene must return a Scene for this repository and piece')
    return scene


def frame_page(browser, scene: S.Scene, size: tuple):
    width, height = size
    html, elements = scene.write_page(width, height)
    page, blocked, failed = browser.page(html, width, height, S.frame_vars(width, height, scene.tables))
    return page, blocked, failed


def draw(page, frame: int):
    page.evaluate('(frame) => window.draw(frame)', frame)
    page.evaluate('async () => {await document.fonts.ready; await Promise.all(Array.from(document.images, img => img.decode().catch(() => {})))}')


def page_findings(page, blocked, failed) -> list:
    found = card.image_findings(page, failed)
    found += [f'requested {url} over the network (aborted)' for url in dict.fromkeys(blocked)]
    found += [f'the font {family!r} did not load' for family, status in page.evaluate(card.LOAD_FONTS) if status != 'loaded']
    return found


def requested_sizes(args, scene):
    default = V.parse_size(scene.edl['edit'].get('size'))
    if not default: raise C.Fatal('a scene edit needs its default picture size')
    given = args.size or []
    if isinstance(given, str): given = [given]
    return list(dict.fromkeys(card.parse_size(s) for s in given)) if given else [default]


def cmd_stills(args) -> int:
    scene = load_scene(args.piece)
    folder = C.piece_folder(C.PROD_RENDERS, args.piece, 'stills')
    folder.mkdir(parents=True, exist_ok=True)
    report = {'piece': args.piece, 'fps': scene.fps, 'stills': []}
    boards = scene.cues.get('boards')
    if not isinstance(boards, list) or not boards:
        raise C.Fatal('scene cues have no boards: run media.py cues again')
    with card.Browser() as browser:
        for size in requested_sizes(args, scene):
            width, height = size
            page, blocked, failed = frame_page(browser, scene, size)
            try:
                for board in boards:
                    name = str(board.get('id', ''))
                    if not S.re.fullmatch(r'b\d+', name): raise C.Fatal('cue board IDs must be bNN: run cues again')
                    start = S.number(board.get('start'), f'{name} start') + scene.offset
                    end = S.number(board.get('end'), f'{name} end') + scene.offset
                    if end <= start: raise C.Fatal(f'{name} has no interval: run cues again')
                    frames = (scene.frame(f'board:{name}'), max(0, S.math.ceil((start + end) / 2 * scene.fps - 0.5)))
                    for suffix, frame in zip(('', '.mid'), frames):
                        if frame >= scene.frames: raise C.Fatal(f'{name} is outside the scene length')
                        draw(page, frame)
                        boxes = page.evaluate(BOXES)
                        found = box_findings(boxes, width, height, S.safe_zone(width, height, scene.tables))
                        found += page_findings(page, blocked, failed)
                        out = folder / f'{scene.piece}.{name}{suffix}.{width}x{height}.png'
                        browser.capture(page, path=str(out), full_page=False)
                        report['stills'].append({'board': name, 'size': f'{width}x{height}', 'frame': frame,
                                                'path': out.relative_to(C.ROOT).as_posix(), 'boxes': boxes, 'findings': found})
                        print(f'wrote {C.shown(out)}; frame {frame}')
                        for finding in found: print(f'  FAIL {name}{suffix}: {finding}')
            finally: page.close()
    out = folder / f'{scene.piece}.stills.json'
    C.replace_file(out, (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode())
    print(f'wrote {C.shown(out)}')
    return int(any(still['findings'] for still in report['stills']))


def cmd_render(args) -> int:
    command = [sys.executable, str(Path(__file__).resolve()), 'render', args.piece]
    if args.size: command += ['--size', args.size]
    if args.memory_max: command += ['--memory-max', args.memory_max]
    code = C.memory_scope(args.memory_max, command, cwd=C.ROOT)
    if code is not None: return code
    scene = load_scene(args.piece)
    width, height = requested_sizes(args, scene)[0]
    default = V.parse_size(scene.edl['edit']['size'])
    if width % 2 or height % 2: raise C.Fatal('a scene master needs an even width and height')
    edit = scene.edl['edit']
    rate = S.whole(edit.get('audio_rate', 48000), 'edit audio_rate', 1)
    loudness = str(edit.get('loudness', 'social'))
    if loudness not in ('none', 'social', 'podcast'): raise C.Fatal('edit loudness must be none, social or podcast')
    duration = scene.frames / scene.fps
    samples = V.tick(Fraction(scene.frames) / Fraction(str(scene.fps)), Fraction(rate))
    stem = f'{scene.piece}.master' + ('' if (width, height) == default else f'.{width}x{height}')
    out = C.output_path(C.piece_folder(C.PROD_RENDERS, scene.piece) / (stem + '.mp4'), None)
    findings = []
    with tempfile.TemporaryDirectory(prefix='media-scene-') as tmp:
        stage = Path(tmp) / 'stage.mkv'
        inputs = [['-f', 'image2pipe', '-vcodec', 'png', '-framerate', str(scene.fps), '-i', 'pipe:0']]
        def add(args_):
            inputs.append(args_)
            return len(inputs) - 1
        graph = [f'anullsrc=r={rate}:cl=stereo,atrim=end_sample={samples}[base]']
        V.mix_audio(scene.edl.get('audio', []), scene.piece, rate, samples, add, graph, 'base', joined=True)
        threads = str(C.threads())
        command = [C.need('ffmpeg'), '-hide_banner', '-nostats', '-y', '-filter_threads', threads,
                   '-filter_complex_threads', threads]
        for inp in inputs: command += [str(v) for v in inp]
        command += ['-filter_complex', ';'.join(graph), '-map', '0:v', '-map', '[aout]',
                    '-c:v', 'libx264', '-preset', C.X264_PRESET, '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-threads', threads, '-c:a', 'pcm_s16le', '-ar', str(rate), '-t', f'{duration:.9f}', str(stage)]
        with card.Browser() as browser:
            page, blocked, failed = frame_page(browser, scene, (width, height))
            try:
                def frames():
                    for frame in range(scene.frames):
                        draw(page, frame)
                        current = page_findings(page, blocked, failed)
                        if current:
                            for finding in current:
                                if finding not in findings: findings.append(finding)
                        yield browser.capture(page, type='png', full_page=False)
                C.stream_run(command, frames(), cwd=C.ROOT, what='scene frame encoder')
            finally: page.close()
        filters = []
        if loudness != 'none':
            target = C.loudness_target(loudness)
            filters.append(A.loudnorm_filter(A.loudnorm_measure(stage, target), target))
        filters.append(V.held_sound(samples, rate))
        V.render(['-y', '-i', str(stage), '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'copy', '-af', ','.join(filters),
                  '-c:a', 'aac', '-b:a', '192k', '-ar', str(rate), '-movflags', '+faststart', str(out)], out, what='scene master')
    info = json.loads(C.run([C.need('ffprobe'), '-v', 'error', '-count_frames', '-show_streams', '-of', 'json', str(out)]).stdout)
    picture, audio = C.streams(info, 'video'), C.streams(info, 'audio')
    if not picture or int(picture[0].get('nb_read_frames') or 0) != scene.frames:
        findings.append(f'master frame count differs from scene length {scene.frames}')
    if not audio or not picture:
        findings.append('master needs picture and sound')
    else:
        video_end = float(picture[0].get('start_time') or 0) + float(picture[0].get('duration') or 0)
        audio_end = float(audio[0].get('start_time') or 0) + float(audio[0].get('duration') or 0)
        if abs(audio_end - video_end) > 2 / rate:
            findings.append(f'sound ends at {audio_end:.6f}s, picture at {video_end:.6f}s')
    if loudness != 'none':
        target = C.loudness_target(loudness)
        measured = A.loudnorm_measure(out, target)
        if abs(float(measured['input_i']) - target[0]) > 1:
            findings.append(f'master loudness {measured["input_i"]} LUFS is outside the selected {target[0]:g} LUFS target')
    print(f'wrote {C.shown(out)}; {scene.frames} frames at {scene.fps:g} fps')
    for finding in findings: print('  FAIL ' + finding)
    return int(bool(findings))


def write_fixture(root: Path, piece: str = '922-scene-fixture') -> None:
    """Neutral runtime fixture: CSS placeholder, two boards, indexed text and a voice."""
    import math
    import struct
    import wave
    def text(name, content):
        p = root / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding='utf-8')
    def data(name, body): text(name, json.dumps(body, allow_nan=False))
    text(C.TOKENS, ':root{--color-bg:#181818;--color-text:#eeeeee;--color-accent:#888888;'
                   '--color-surface:#444444;--font-body:monospace;}')
    text(f'{C.PIECES}/{piece}/brief.md', '---\npiece: ' + piece + '\ndeliverables: []\n---\n')
    text(f'{C.EDITS}/{piece}.toml', '[edit]\npiece="' + piece + '\"\nsize="160x90"\n'
         'audio_rate=48000\nloudness="social"\n[[audio]]\nsource="vo:' + piece + '\"\nat=0\nrole="voice"\ngain_db=-12\n'
         '[[audio]]\nsource="production/src/footage/raw/scene-bed.wav"\nrole="music"\nduck=true\nfade_in=0.1\nfade_out=0.1\n')
    take = root / C.VO_GENERATED / piece / 'takes' / (piece + '.s01.t1.wav')
    take.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which('espeak-ng'):
        C.run(['espeak-ng', '-w', str(take), 'One. Two.'], what='scene fixture voice')
    else:
        with wave.open(str(take), 'wb') as f:
            f.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
            f.writeframes(b''.join(struct.pack('<h', round(5000 * math.sin(2 * math.pi * 220 * n / 48000))) for n in range(48000)))
    bed = root / C.RAW / 'scene-bed.wav'; bed.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(bed), 'wb') as f:
        f.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
        f.writeframes(b''.join(struct.pack('<h', round(8000 * math.sin(2 * math.pi * 110 * n / 48000))) for n in range(96000)))
    voice = root / C.PROD_RENDERS / piece / (piece + '.voice.wav')
    voice.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(take, voice)
    text(f'{C.VOICEOVER}/{piece}.toml', '[voiceover]\npiece="' + piece + '\"\n'
         '[[segment]]\nid="s01"\ntext="One. Two."\nscript_lines="1.1-2.1"\nstatus="approved"\n'
         'file="generated/' + piece + '/takes/' + take.name + '\"\npause_after=0\narchived="F0001"\n')
    data(f'{C.TIMING}/{piece}.words.json', [{'word': 'One.', 'start': 0, 'end': 0.5, 'score': 1, 'segment': 's01'},
                                          {'word': 'Two.', 'start': 1, 'end': 1.5, 'score': 1, 'segment': 's01'}])
    data(f'{C.TIMING}/{piece}.mouth.json', {'metadata': {'soundFile': voice.relative_to(root).as_posix()},
                                         'mouthCues': [{'start': 0, 'end': 0.5, 'value': 'A'},
                                                       {'start': 1, 'end': 1.5, 'value': 'H'}]})
    data(f'{C.SCENES}/{piece}.cues.json', {'piece': piece,
         'beats': [{'id': 1, 'start': 0, 'end': 1}, {'id': 2, 'start': 1, 'end': 2}],
         'lines': [{'id': '1.1', 'start': 0, 'end': 0.5}, {'id': '2.1', 'start': 1, 'end': 1.5}],
         'boards': [{'id': 'b01', 'start': 0, 'end': 1}, {'id': 'b02', 'start': 1, 'end': 2}],
         'words': [], 'events': []})
    asset = root / C.ASSETS / (piece + '.txt'); text(asset.relative_to(root), 'Local capture')
    import hashlib
    data(f'{C.SCENES}/{piece}.real.json', {'piece': piece, 'sources': [{'source': asset.relative_to(root).as_posix(),
         'kind': 'text', 'path': asset.relative_to(root).as_posix(), 'sha256': hashlib.sha256(asset.read_bytes()).hexdigest()}]})
    text(f'{C.SCENES}/{piece}.scene.py', FIXTURE_SCENE)


FIXTURE_SCENE = """from media_scene import Scene, Element, Sprite, Keyframe

def build_scene(root, piece):
    def layout(width, height, safe):
        parts = {}
        for pose in ('idle', 'walk1', 'walk2', 'point'):
            for shape in 'ABCDEFGHX':
                parts[pose + '-mouth-' + shape] = [
                    dict(x=0,y=0,width=12,height=16,style={'background-color':'var(--color-accent)'}),
                    dict(x=2,y=8,width=1+'ABCDEFGHX'.index(shape),height=2,style={'background-color':'var(--color-bg)'})]
        parts['blink'] = [dict(x=2,y=3,width=8,height=1,style={'background-color':'var(--color-bg)'})]
        label = Element('label',text='One',x=safe['left']+5,y=safe['top']+5,
                        width=width-safe['left']-safe['right']-10,height=20,typed=True,type_hold=3,
                        anchors={'left':(0,25)})
        character = Element('character',kind='sprite',x=safe['left']+5,y=safe['top']+30,width=12,height=16,
                  sprite=Sprite(css_frames=parts,walk=('walk1','walk2'),breathe_hold=15,blink_every=15),
                  keyframes=[Keyframe('line:2.1',anchor='label.left',x=width//3,pose='point',facing='left',
                              response={'highlight':'var(--color-surface)'})])
        return [label, character]
    return Scene(root,piece,60,layout)
"""


def self_test() -> int:
    failures, skips = [], []
    def check(name, ok, detail=''):
        print(('  ok   ' if ok else '  FAIL ') + name)
        if not ok: failures.append(name); print(str(detail)[-1000:])
    def attempt(name, fn):
        try: fn()
        except Exception as err: check(name, False, err)
    print('scene.py --self-test')
    saved = C.ROOT
    from media import held_env
    with tempfile.TemporaryDirectory(prefix='scene-self-test-') as tmp, \
            held_env(drop=('MEDIA_MEMORY_MAX', '_MEDIA_MEMORY_CAPPED', '_MEDIA_MEMORY_RECEIPT')):
        root = Path(tmp) / 'project'; root.mkdir(); C.ROOT = root
        try:
            write_fixture(root)
            # The user's platform data is read from the toolkit, shared by every fixture.
            data = root / 'toolkit/data'; data.mkdir(parents=True)
            shutil.copyfile(Path(__file__).parent / 'data/platforms.toml', data / 'platforms.toml')
            scene = load_scene('922-scene-fixture')
            def state_checks():
                page, elements = scene.write_page(160, 90)
                states = [scene.state(n, elements, page) for n in (0, 14, 29, 30, 44, 59)]
                mouths = [next(e for e in state if e['name'] == 'character')['mouth'] for state in states]
                check('Python samples shapes and rest at the middle of each native frame', mouths == ['A','A','X','H','H','X'])
                at = next(e for e in states[3] if e['name'] == 'character')
                label = next(e for e in states[3] if e['name'] == 'label')
                check('arrival points, mirrors and answers on the line’s frame', at['pose'] == 'point'
                      and at['facing'] == 'left' and label['style'].get('background-color') == 'var(--color-surface)')
                check('frame state is repeatable without a browser clock', states[3] == scene.state(30, elements, page))
                check('the scene page links local brand files and contains only the painter clock',
                      'requestAnimationFrame' not in page.read_text() and 'setTimeout' not in page.read_text()
                      and 'tokens.css' in page.read_text() and 'window.draw' in page.read_text())
                check('runpy leaves no cache in the tracked scene folder', not (root / C.SCENES / '__pycache__').exists())
                original = scene.layout
                scene.layout = lambda w,h,safe: [S.Element('source',kind='source',source=f'{C.ASSETS}/922-scene-fixture.txt',width=100,height=20)]
                page, elements = scene.write_page(160,90)
                check('indexed captures become literal on-screen text', scene.state(0,elements,page)[0]['text'] == 'Local capture')
                scene.layout = original
            attempt('standard-library scene state', state_checks)
            have_browser = True
            try:
                with card.Browser(): pass
            except C.Fatal as err:
                have_browser = False; skips.append(str(err)); print('  SKIP ' + str(err))
            if have_browser:
                def browser_checks():
                    args = argparse.Namespace(piece=scene.piece,size=['160x90','90x160'])
                    code = cmd_stills(args)
                    report = json.loads((root / C.PROD_RENDERS / scene.piece / 'stills' / (scene.piece+'.stills.json')).read_text())
                    check('two boards have first/middle stills at both native sizes', code == 0 and len(report['stills']) == 8, report)
                    check('stills report names every measured text/sprite box and frame',
                          all(len(row['boxes']) == 2 and row['frame'] in (0,15,30,45) for row in report['stills']))
                    with card.Browser() as browser:
                        page,blocked,failed = frame_page(browser, scene, (160,90))
                        draw(page,30); a=page.screenshot(); draw(page,30); b=page.screenshot()
                        check('capturing the same frame twice gives identical pixels', a == b)
                        check('frame and safe variables precede the first draw', page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--frame-width').trim()") == '160px')
                        page.close()
                    original = scene.layout
                    for name, elements, phrase in (
                        ('overlap',[S.Element('a',width=30,height=20,text='One'),S.Element('b',width=30,height=20,text='Two')],'overlap'),
                        ('safe',[S.Element('a',x=-1,width=30,height=20,text='One')],'safe zone'),
                        ('overflow',[S.Element('a',width=1,height=1,text='Long text')],'overflows'),
                        ('grid',[S.Element('a',x=0.5,width=30,height=20,text='One')],'pixel grid')):
                        scene.layout = lambda w,h,safe, elements=elements: elements
                        with card.Browser() as browser:
                            page,blocked,failed = frame_page(browser,scene,(160,90)); draw(page,0)
                            found = box_findings(page.evaluate(BOXES),160,90,S.safe_zone(160,90,scene.tables))
                            check('stills flag ' + name, any(phrase in finding for finding in found), found); page.close()
                    scene.layout = original
                attempt('browser stills', browser_checks)
                if shutil.which('ffmpeg') and shutil.which('ffprobe'):
                    def render_checks():
                        for size in (None,'90x160'):
                            code = cmd_render(argparse.Namespace(piece=scene.piece,size=size,memory_max=None))
                            suffix = '' if size is None else '.'+size
                            master = root / C.PROD_RENDERS / scene.piece / (scene.piece+'.master'+suffix+'.mp4')
                            info=C.probe(master)
                            check('native scene master ' + (size or '160x90') + ' has exact frames and held sound', code==0
                                  and V.parse_size(size or '160x90') == tuple(int(C.streams(info,'video')[0][k]) for k in ('width','height')))
                            target=C.loudness_target('social'); measure=A.loudnorm_measure(master,target)
                            check('master loudness is selected by the edit key', abs(float(measure['input_i'])-float(target[0])) <= 1, measure)
                    attempt('scene masters',render_checks)
                else:
                    skips.append('ffmpeg or ffprobe is missing: scene render'); print('  SKIP '+skips[-1])
            for suffix, command in (('cues.json','cues'),('words.json','transcribe'),('mouth.json','lipsync'),('real.json','real')):
                folder = C.TIMING if suffix in ('words.json','mouth.json') else C.SCENES
                p=root/folder/(scene.piece+'.'+suffix); saved_bytes=p.read_bytes(); p.unlink()
                try: load_scene(scene.piece); check('missing '+suffix+' names '+command,False)
                except C.Fatal as err: check('missing '+suffix+' names '+command,command in str(err))
                finally: p.write_bytes(saved_bytes)
            edl=root/C.EDITS/(scene.piece+'.toml'); original=edl.read_text(); edl.write_text(original+'\n[[clip]]\ncolour="#222222"\nseconds=1\n')
            check('an assemble clip is refused by the scene runner',main(['render',scene.piece])==2)
            edl.write_text(original)
        finally: C.ROOT=saved
    if failures: print(f'self-test FAILED: {len(failures)} case(s)'); return 1
    if skips: print(f'self-test incomplete: {len(skips)} part(s) skipped (SKIP above)'); return 2
    print('self-test passed'); return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true')
    sub = parser.add_subparsers(dest='action')
    stills = sub.add_parser('stills', help='each board’s first and middle frame, at native sizes')
    stills.add_argument('piece'); stills.add_argument('--size', action='append')
    stills.set_defaults(func=cmd_stills)
    render = sub.add_parser('render', help='a native master from deterministic frames and the shared audio mix')
    render.add_argument('piece'); render.add_argument('--size'); render.add_argument('--memory-max')
    render.set_defaults(func=cmd_render)
    args = parser.parse_args(argv)
    try:
        if args.self_test: return self_test()
        if not args.action: parser.print_help(); return 0
        return args.func(args)
    except C.Finding as err:
        print('finding: ' + str(err), file=sys.stderr); return 1
    except C.Fatal as err:
        print('error: ' + str(err), file=sys.stderr); return 2
    except Exception as err:
        print('error: scene could not run: ' + str(err).splitlines()[0], file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
