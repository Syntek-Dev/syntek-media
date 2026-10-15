"""Voice remix into a voice trial (DESIGN D82), through media.py voice remix plan/run.

Not run directly, and no self-test of its own: media.py voice remix calls it and media.py's
self-test exercises it (DESIGN D20). The one ElevenLabs call the toolkit makes itself, because
the ElevenLabs MCP server has no remix tool; saving a chosen preview and every other ElevenLabs
call stay on MCP (create_voice_from_preview takes a preview's generated_voice_id).

Plan is offline: it checks the trial name (speak plan --trial's rule), the source voice and the
lengths, and prints the request, one call and its characters, never a credit rate (D36); it
writes nothing. Run needs --approve-call before the key is read or anything is sent, and refuses
before any call a trial whose record or previews exist, a trial path that is not a folder, a
credits log without its table and a key that is not printable ASCII. It then sends that one
request: standard library only, no redirect, a 30-second timeout, no retry. The key comes only
from a user-scope ELEVENLABS_API_KEY in the shell, sent as the xi-api-key header and never
written or printed. Every preview is decoded and checked before anything is written; all of
them and <name>.remix.json are written into a hidden staging folder under voice-trials/ and
moved into production/src/voiceover/generated/voice-trials/<name>/ only once all are written
(as <name>.pNN.mp3), so a failure leaves no partial trial; then the trial's credits-log row is
appended (piece '—', tool 'voice remix'). Any failure after the call says the call was made and
gives the row to add by hand. A trial is never a take: it enters no register. The self-test
uses runtime fixtures and a stubbed transport, never the service. Exit 0: done; 2: cannot run.
"""
from __future__ import annotations

import base64
import binascii
import errno
import http.client
import json
import math
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import media_common as C
from media_score import NoRedirect

ENDPOINT = 'https://api.elevenlabs.io/v1/text-to-voice/{voice_id}/remix'
# The request's bounds, from the ElevenLabs API reference (VERIFY: checked 15/10/2026).
DESCRIBE_RANGE = (5, 1000)    # voice_description, characters
TEXT_RANGE = (100, 1000)      # text, characters, when the author gives the preview text
# The response carries every preview as base64 audio; a house cap, not a documented limit
# (VERIFY: checked 15/10/2026 against a remix's usual three short previews).
READ_CAP = 32 * 1024 * 1024
TIMEOUT = 30
VOICE_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}')
MP3_TYPES = ('audio/mpeg', 'audio/mp3')
TOOL = 'voice remix'
LOG_HEAD = ('Date', 'Piece', 'Tool')
NAME_RULE = ('voice remix needs one trial folder name, the rule of speak plan --trial: up to 64 letters, '
             'digits, ., _ and -, opening with a letter or digit; never a path, . or ..')
MAYBE_CHARGED = ('; the call may have been charged: check the account and add the credits-log row by hand; '
                 'no automatic retry')
# What a remix bills is not documented beside the endpoint: the log counts the description and the
# preview text, given or generated (VERIFY on first use against the account's usage).
BASIS = 'billing basis VERIFY'


def bounded(value, label, low, high):
    if not isinstance(value, str) or not value.strip():
        raise C.Fatal(f'{label} must be text and non-empty')
    if not low <= len(value) <= high:
        raise C.Fatal(f'{label} is {len(value)} characters; ElevenLabs takes {low} to {high} (VERIFY)')
    return value


def prepare(args):
    """(trial folder, source voice, request body, characters): every check made before a call."""
    folder = C.trial_folder(args.name, NAME_RULE)
    voice = args.source
    if not isinstance(voice, str) or not VOICE_RE.fullmatch(voice):
        raise C.Fatal('--from needs a voice ID the account owns (letters, digits, - and _ only)')
    describe = bounded(args.describe, '--describe', *DESCRIBE_RANGE)
    body = {'voice_description': describe}
    if args.text is not None:
        body['text'] = bounded(args.text, '--text', *TEXT_RANGE)
    # Without text, ask ElevenLabs to write the preview text; previews come back in the response,
    # not streamed (VERIFY: the API reference's defaults, checked 15/10/2026).
    body['auto_generate_text'] = args.text is None
    body['stream_previews'] = False
    chars = len(describe) + len(args.text or '')
    return folder, voice, body, chars


def existing(folder: Path, name: str) -> list:
    """The trial's remix outputs already present: its record or any preview. A trial path, or the
    voice-trials folder, that exists and is not a real folder is refused here, before any call."""
    for p, link_refused in ((folder.parent, False), (folder, True)):
        if (link_refused and p.is_symlink()) or (p.exists() and not p.is_dir()):
            raise C.Fatal(f'{C.shown(p)} is a link or not a folder; a voice trial is a real folder: choose '
                          'a new trial name or move it aside; nothing was sent')
    if not folder.is_dir():
        return []
    record = folder / f'{name}.remix.json'
    found = [record] if record.exists() or record.is_symlink() else []
    return found + sorted(f for f in folder.iterdir() if re.fullmatch(re.escape(name) + r'\.p\d+\.mp3', f.name))


def log_problem(log: Path):
    """Why the credits-log row could not be appended, or None: checked before any call."""
    try:
        lines = C.read_text(log).split('\n')
    except C.Fatal as err:
        return str(err)
    except OSError as err:
        return f'{C.shown(log)} cannot be read ({err.strerror or type(err).__name__})'
    if C.find_table(lines, LOG_HEAD)[0] is None:
        return f"{C.shown(log)} has no table headed '| {' | '.join(LOG_HEAD)} |'"
    return None


def api_key() -> str:
    """The user-scope key, refused before any call when absent or not printable ASCII; the refusal
    never includes it."""
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key:
        raise C.Fatal('set ELEVENLABS_API_KEY at user scope in the shell; never store it in project files')
    if any(not 33 <= ord(ch) <= 126 for ch in key):
        raise C.Fatal('ELEVENLABS_API_KEY holds a character outside printable ASCII (a space, a line break or '
                      'a non-ASCII character): set it again at user scope; nothing was sent')
    return key


def send(voice, body, key):
    """One call, no retry or redirect; errors never include response bodies or credentials."""
    url = ENDPOINT.format(voice_id=urllib.parse.quote(voice, safe=''))
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json',
                                          'Accept': 'application/json'}, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=TIMEOUT) as response:
            data = response.read(READ_CAP + 1)
    except urllib.error.HTTPError as err:
        raise C.Fatal(f'ElevenLabs HTTP {err.code}; no automatic retry') from None
    except (urllib.error.URLError, TimeoutError):
        raise C.Fatal('ElevenLabs connection failed or timed out' + MAYBE_CHARGED) from None
    except (http.client.HTTPException, OSError):
        raise C.Fatal('ElevenLabs connection failed after sending' + MAYBE_CHARGED) from None
    if len(data) > READ_CAP:
        raise C.Fatal('ElevenLabs response exceeds the house byte cap; the call was made: add its credits-log '
                      'row by hand if the account was charged; no automatic retry')
    try:
        return json.loads(data)
    except (ValueError, RecursionError):
        raise C.Fatal('ElevenLabs returned invalid JSON; the call was made: add its credits-log row by hand '
                      'if the account was charged') from None


def is_mp3(data: bytes) -> bool:
    return data[:3] == b'ID3' or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0)


def decode(response):
    """[(audio bytes, preview record)] and the preview text, or a Fatal before anything is written."""
    spent = '; the call was made: add its credits-log row by hand if the account was charged'
    if not isinstance(response, dict) or not isinstance(response.get('previews'), list) \
            or not 1 <= len(response['previews']) <= 99:
        raise C.Fatal('ElevenLabs returned no previews' + spent)
    previews = []
    for n, row in enumerate(response['previews'], start=1):
        if not isinstance(row, dict):
            raise C.Fatal(f'preview {n} is not an object' + spent)
        gid, media = row.get('generated_voice_id'), row.get('media_type')
        if not isinstance(gid, str) or not VOICE_RE.fullmatch(gid):
            raise C.Fatal(f'preview {n} has no usable generated_voice_id' + spent)
        if media not in MP3_TYPES:
            raise C.Fatal(f'preview {n} is {media!r}, not MP3' + spent)
        try:
            audio = base64.b64decode(row.get('audio_base_64') or '', validate=True)
        except (binascii.Error, TypeError, ValueError):
            raise C.Fatal(f'preview {n} is not valid base64' + spent) from None
        if not audio or not is_mp3(audio):
            raise C.Fatal(f'preview {n} does not decode to MP3 audio' + spent)
        duration = row.get('duration_secs')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration):
            duration = None
        previews.append((audio, {'generated_voice_id': gid, 'media_type': media, 'duration_secs': duration}))
    text = response.get('text')
    return previews, text if isinstance(text, str) else None


def publish(dest: Path, data: bytes) -> None:
    """Write a complete file exclusively: neither a partial file nor an overwrite."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.voice-remix-', suffix='.tmp', dir=dest.parent,
                                         delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, dest)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def clear(staging, written) -> str:
    """Remove what this run staged, and the staging folder only if it then holds nothing else."""
    if staging is None:
        return 'no staging folder was made'
    for p in written:
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
    try:
        staging.rmdir()
    except FileNotFoundError:
        return 'the staging folder is gone'
    except OSError:
        return f'{C.shown(staging)} holds other files and was left in place'
    return 'the staging folder was removed'


def place(folder: Path, files: list, existed: bool) -> None:
    """Write every file into a hidden staging folder beside the trial, then move them into place
    only when all are written: the staging folder is renamed to the trial, or, where the trial
    folder was already there and empty of remix outputs, each file is linked in exclusively, and
    any linked before a failure is removed. A failure raises OSError with nothing left under the
    trial's name that this run wrote."""
    trials = folder.parent
    staging, written = None, []
    try:
        trials.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f'.{folder.name}.remix-', dir=trials))
        for fname, data in files:
            publish(staging / fname, data)
            written.append(staging / fname)
        if not existed:
            if folder.exists() or folder.is_symlink():
                raise FileExistsError(errno.EEXIST, f'{C.shown(folder)} appeared during the call')
            os.rename(staging, folder)
            staging = None
            return
        linked = []
        try:
            for fname, _ in files:
                os.link(staging / fname, folder / fname)
                linked.append(folder / fname)
        except OSError:
            for p in linked:
                p.unlink(missing_ok=True)
            raise
        clear(staging, written)
    except OSError as err:
        err.voice_remix_left = clear(staging, written)
        raise


def cmd_remix(args) -> int:
    folder, voice, body, chars = prepare(args)
    name = args.name
    found = existing(folder, name)
    if found:
        raise C.Fatal(f'{C.shown(found[0])} exists: this trial is already remixed; choose a new trial name; '
                      'nothing was sent')
    log = C.path(C.CREDITS_LOG)
    generated = 'text' not in body
    if args.action == 'plan':
        print(f'voice remix plan {name}: POST {ENDPOINT.format(voice_id=voice)}')
        print(json.dumps(body, indent=2, ensure_ascii=False))
        what = ('the description; the generated preview text\'s characters are added after the call'
                if generated else 'the description and the text')
        print(f'  1 call, {chars} characters ({what}; {BASIS}; no credit rate: check the account)')
        print(f'  previews to {C.shown(folder)}/{name}.pNN.mp3, record {name}.remix.json; nothing written now')
        problem = log_problem(log)
        if problem:
            print(f'  note: {problem}; run would refuse before the call')
        print('  next: the author approves this one call, then voice remix run … --approve-call')
        return 0
    if not args.approve_call:
        raise C.Fatal('show voice remix plan and obtain the author\'s approval of this paid call before '
                      '--approve-call')
    problem = log_problem(log)
    if problem:
        raise C.Fatal(f'{problem}: the trial\'s credits-log row could not be written; nothing was sent')
    existed = folder.is_dir()
    key = api_key()
    response = send(voice, body, key)
    previews, text = decode(response)
    if generated:
        chars += len(text or '')
        said = f'preview text generated by ElevenLabs, its {len(text or "")} characters counted'
    else:
        said = 'preview text given by the author'
    model = response.get('model_id') if isinstance(response.get('model_id'), str) else '—'
    output = (Path(C.VOICE_TRIALS) / name).relative_to('production/src').as_posix() + '/'
    cells = [C.today(), '—', TOOL, 1, f'{chars} characters', voice, model, output,
             f'{len(previews)} remix previews of {voice}; a trial, never a take; {said}; {BASIS}']
    row = '| ' + ' | '.join(C.cell(c) for c in cells) + ' |'
    by_hand = f'; add this row to {C.shown(log)} by hand: {row}'
    rows, files = [], []
    for n, (audio, meta) in enumerate(previews, start=1):
        files.append((f'{name}.p{n:02d}.mp3', audio))
        rows.append(dict(file=files[-1][0], **meta))
    record = {'date': C.today(), 'source_voice': voice, 'description': body['voice_description'],
              'text': body.get('text', text), 'text_generated': generated, 'previews': rows}
    files.append((f'{name}.remix.json',
                  (json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')))
    try:
        place(folder, files, existed)
    except OSError as err:
        reason = str(err.args[1]) if isinstance(err, FileExistsError) and len(err.args) > 1 \
            else (err.strerror or type(err).__name__)
        left = getattr(err, 'voice_remix_left', 'no staging folder was made')
        raise C.Fatal(f'the call was made but writing the trial failed ({reason}); no preview was placed in '
                      f'{C.shown(folder)}/ and {left}' + by_hand) from None
    try:
        C.append_table_row(log, LOG_HEAD, cells)
    except (C.Fatal, OSError) as err:
        detail = str(err) if isinstance(err, C.Fatal) else (err.strerror or type(err).__name__)
        raise C.Fatal(f'the call was made and the previews were written to {C.shown(folder)}/, but the '
                      f'credits-log row could not be appended ({detail})' + by_hand) from None
    for row_ in rows:
        print(f'wrote {C.shown(folder / row_["file"])}  generated_voice_id {row_["generated_voice_id"]}')
    print(f'wrote {C.shown(folder / files[-1][0])}')
    print(f'appended the credits-log row to {C.shown(log)} ({chars} characters; {BASIS})')
    print('next: the author listens to every preview; save only the chosen one, through MCP '
          'create_voice_from_preview with its generated_voice_id, after the author\'s yes')
    return 0

def self_test(verdict):
    """Offline fixtures and a stubbed transport exercise every boundary before and after the call."""
    import contextlib
    import io
    from types import SimpleNamespace
    from unittest.mock import patch

    def run(args):
        """(code or the refusal's type, everything printed)."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                return cmd_remix(args), out.getvalue()
            except (C.Fatal, C.Finding) as err:
                return type(err).__name__, out.getvalue() + str(err)

    def every_file(root):
        return {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}

    saved = C.ROOT
    with tempfile.TemporaryDirectory(prefix='voice-remix-self-test-') as tmp:
        C.ROOT = Path(tmp)
        try:
            log = C.path(C.CREDITS_LOG)
            log.parent.mkdir(parents=True)
            log.write_text('# credits-log.md (fixture)\n\n| Date | Piece | Tool | Calls | Characters or minutes '
                           '| Voice | Model | Output | Notes |\n|---|---|---|---|---|---|---|---|---|\n',
                           encoding='utf-8')
            describe = 'An older, gravelly sea captain, slow and warm.'
            audio = [b'ID3' + bytes([n]) * 64 for n in (1, 2)]
            response = {'previews': [{'audio_base_64': base64.b64encode(a).decode(), 'media_type': 'audio/mpeg',
                                      'generated_voice_id': f'fixture-preview-{n}', 'duration_secs': 4.5,
                                      'language': 'en'} for n, a in enumerate(audio, start=1)],
                        'text': 'Fixture preview text written by the service.'}

            def args(name='captain', action='plan', **kw):
                base = dict(name=name, source='fixture-voice', describe=describe, text=None, action=action,
                            approve_call=False)
                base.update(kw)
                return SimpleNamespace(**base)

            trials = C.path(C.VOICE_TRIALS)
            with patch(__name__ + '.send', return_value=response) as transport:
                code, out = run(args())
                verdict('voice remix plan prints one call and its characters, writes nothing, calls nothing',
                        code == 0 and '1 call,' in out and f'{len(describe)} characters' in out
                        and 'added after the call' in out and 'VERIFY' in out
                        and not trials.exists() and not transport.called, out)
                code, out = run(args(action='run'))
                verdict('voice remix run without --approve-call calls nothing',
                        code == 'Fatal' and not transport.called and not trials.exists(), out)
                with patch.dict(os.environ, {'ELEVENLABS_API_KEY': ''}):
                    code, out = run(args(action='run', approve_call=True))
                verdict('voice remix run without ELEVENLABS_API_KEY never reaches transport',
                        code == 'Fatal' and 'user scope' in out and not transport.called, out)
                results = []
                for length, ok in ((4, False), (5, True), (1000, True), (1001, False)):
                    results.append((run(args(describe='d' * length))[0] == 0) == ok)
                for length, ok in ((99, False), (100, True), (1000, True), (1001, False)):
                    results.append((run(args(text='t' * length))[0] == 0) == ok)
                verdict('voice remix holds the description to 5-1000 characters and the text to 100-1000',
                        all(results) and not transport.called, results)
                names = ('../escape', '..', '.', '', 'a/b', 'a\\b', 'a\nb', 'a|b', '-x', 'x' * 65)
                refused = [run(args(name=bad))[0] for bad in names]
                refused.append(run(args(source='bad/voice'))[0])
                verdict('voice remix refuses a trial path, a line break, a |, a leading - or a malformed '
                        'voice ID, creating nothing',
                        refused == ['Fatal'] * (len(names) + 1) and not trials.exists() and not transport.called,
                        refused)
                for bad_key in ('fixture secret', 'fixture-s\u00e9cret', 'fixture-\nsecret'):
                    with patch.dict(os.environ, {'ELEVENLABS_API_KEY': bad_key}):
                        code, out = run(args(action='run', approve_call=True))
                    verdict('voice remix refuses a key outside printable ASCII before any call, never showing '
                            'it: ' + repr(bad_key[7:]), code == 'Fatal' and 'nothing was sent' in out
                            and 'secret' not in out and 's\u00e9cret' not in out and not transport.called
                            and not trials.exists(), out)
                held = log.read_text(encoding='utf-8')
                log.write_text('# credits-log.md (fixture, no table)\n', encoding='utf-8')
                with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}):
                    code, out = run(args(action='run', approve_call=True))
                plan_code, plan_out = run(args())
                log.write_text(held, encoding='utf-8')
                verdict('voice remix refuses a credits log without its table before the key or the call',
                        code == 'Fatal' and 'nothing was sent' in out and 'no table' in out
                        and plan_code == 0 and 'run would refuse' in plan_out
                        and not transport.called and not trials.exists(), out)
                trials.mkdir(parents=True)
                (trials / 'a-file').write_bytes(b'not a folder')
                with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}):
                    code, out = run(args(name='a-file', action='run', approve_call=True))
                verdict('voice remix refuses a trial path that is a file, before any call',
                        code == 'Fatal' and 'nothing was sent' in out and not transport.called, out)
                (trials / 'a-file').unlink()
                trials.rmdir()
            with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}), \
                    patch(__name__ + '.send', return_value=response) as transport:
                code, out = run(args(action='run', approve_call=True))
                folder = trials / 'captain'
                record = json.loads((folder / 'captain.remix.json').read_text(encoding='utf-8')) \
                    if (folder / 'captain.remix.json').is_file() else {}
                files = every_file(C.ROOT)
                logged = log.read_text(encoding='utf-8')
                verdict('approved voice remix writes each preview, the record and one credits-log row, '
                        'printing every generated_voice_id and no secret',
                        code == 0 and transport.call_count == 1
                        and (folder / 'captain.p01.mp3').read_bytes() == audio[0]
                        and (folder / 'captain.p02.mp3').read_bytes() == audio[1]
                        and record.get('source_voice') == 'fixture-voice' and record.get('description') == describe
                        and record.get('text') == response['text'] and record.get('text_generated') is True
                        and [p['generated_voice_id'] for p in record.get('previews', [])]
                        == ['fixture-preview-1', 'fixture-preview-2']
                        and logged.count('| voice remix |') == 1 and '| — | voice remix | 1 |' in logged
                        and f'| {len(describe) + len(response["text"])} characters |' in logged
                        and 'generated by ElevenLabs' in logged and 'billing basis VERIFY' in logged
                        and 'voiceover/generated/voice-trials/captain/' in logged
                        and 'fixture-preview-2' in out and 'create_voice_from_preview' in out
                        and 'fixture-secret' not in out
                        and not any(b'fixture-secret' in data for data in files.values())
                        and not list(folder.glob('.voice-remix-*')) and not list(trials.glob('.*')), out)
                pre = trials / 'pre-made'
                pre.mkdir()
                code, out = run(args(name='pre-made', action='run', approve_call=True, text='t' * 100))
                verdict('voice remix fills a trial folder speak plan --trial made, counting the given text, '
                        'and leaves no staging folder',
                        code == 0 and sorted(p.name for p in pre.iterdir())
                        == ['pre-made.p01.mp3', 'pre-made.p02.mp3', 'pre-made.remix.json']
                        and f'| {len(describe) + 100} characters |' in log.read_text(encoding='utf-8')
                        and not list(trials.glob('.*')), out)
                logged = log.read_text(encoding='utf-8')
                code, out = run(args(action='run', approve_call=True))
                stray = trials / 'stray'
                stray.mkdir()
                (stray / 'stray.p01.mp3').write_bytes(audio[0])
                code2, out2 = run(args(name='stray', action='run', approve_call=True))
                verdict('a trial whose record or previews exist is refused before a second call',
                        code == 'Fatal' and code2 == 'Fatal' and transport.call_count == 2
                        and log.read_text(encoding='utf-8') == logged, out + out2)
            for label, change in (('invalid base64', lambda r: r.update(audio_base_64='not base64!')),
                                  ('a non-MP3 media type', lambda r: r.update(media_type='audio/wav')),
                                  ('audio that is not MP3', lambda r: r.update(
                                      audio_base_64=base64.b64encode(b'RIFF' + bytes(32)).decode()))):
                bad = json.loads(json.dumps(response))
                change(bad['previews'][1])
                before = log.read_text(encoding='utf-8')
                with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}), \
                        patch(__name__ + '.send', return_value=bad):
                    code, out = run(args(name='refused', action='run', approve_call=True))
                folder = trials / 'refused'
                verdict('voice remix refuses ' + label + ' with nothing written',
                        code == 'Fatal' and not (folder.exists() and any(folder.iterdir()))
                        and log.read_text(encoding='utf-8') == before and 'fixture-secret' not in out, out)
            real_link, links = os.link, []

            def second_link_fails(src, dst, *rest, **kw):
                links.append(dst)
                if len(links) == 2:
                    raise OSError(errno.ENOSPC, 'fixture write failure')
                return real_link(src, dst, *rest, **kw)

            before = log.read_text(encoding='utf-8')
            with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}), \
                    patch(__name__ + '.send', return_value=response), patch('os.link', second_link_fails):
                code, out = run(args(name='full-disk', action='run', approve_call=True))
            verdict('a preview write failing on the second file leaves no partial trial or staging folder, '
                    'says the call was made and gives the credits-log row to add by hand',
                    code == 'Fatal' and 'the call was made' in out and 'by hand: | ' in out
                    and '| — | voice remix | 1 |' in out and len(links) == 2
                    and not (trials / 'full-disk').exists() and not list(trials.glob('.*'))
                    and log.read_text(encoding='utf-8') == before, out)
            with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'fixture-secret'}), \
                    patch(__name__ + '.send', return_value=response), \
                    patch('media_common.append_table_row', side_effect=OSError(errno.EACCES, 'fixture')):
                code, out = run(args(name='log-fails', action='run', approve_call=True))
            verdict('a credits-log append failing after the write says the call was made, the previews were '
                    'written, and gives the row to add by hand',
                    code == 'Fatal' and 'the call was made and the previews were written' in out
                    and 'by hand: | ' in out and '| voice remix |' in out
                    and (trials / 'log-fails' / 'log-fails.remix.json').is_file(), out)

            # Prove the real HTTP request without opening a socket.
            class Reply:
                def __enter__(self):
                    return self

                def __exit__(self, *unused):
                    pass

                def read(self, limit):
                    return json.dumps(response).encode()

            body = prepare(args(text='t' * 100))[2]
            with patch('urllib.request.build_opener') as opener:
                opener.return_value.open.return_value = Reply()
                received = send('fixture-voice', body, 'fixture-secret')
                call = opener.return_value.open.call_args
                req = call.args[0]
                verdict('the remix request is one POST to /remix with the quoted voice ID, xi-api-key, the JSON '
                        'body, no redirect and a 30-second timeout',
                        req.full_url == ENDPOINT.format(voice_id=urllib.parse.quote('fixture-voice', safe=''))
                        and req.full_url.endswith('/fixture-voice/remix') and req.method == 'POST'
                        and req.get_header('Xi-api-key') == 'fixture-secret'
                        and json.loads(req.data) == {'voice_description': describe, 'text': 't' * 100,
                                                     'auto_generate_text': False, 'stream_previews': False}
                        and isinstance(opener.call_args.args[0], NoRedirect)
                        and received == response and call.kwargs['timeout'] == 30, (req.full_url, req.data))
            auto = prepare(args())[2]
            verdict('without --text the request asks for generated preview text and unstreamed previews',
                    auto == {'voice_description': describe, 'auto_generate_text': True, 'stream_previews': False},
                    auto)
            class Broken(Reply):
                def read(self, limit):
                    raise http.client.IncompleteRead(b'fixture-secret partial')

            with patch('urllib.request.build_opener') as opener:
                opener.return_value.open.return_value = Broken()
                try:
                    send('fixture-voice', body, 'fixture-secret')
                except C.Fatal as err:
                    verdict('a remix reply cut short (IncompleteRead) is one call, says it may have been charged '
                            'and gives no secret', opener.return_value.open.call_count == 1
                            and 'may have been charged' in str(err) and 'fixture-secret' not in str(err), str(err))
                else:
                    verdict('a remix reply cut short (IncompleteRead) is reported', False)
            for error in (urllib.error.HTTPError(ENDPOINT, 429, 'fixture-secret', {}, None),
                          urllib.error.URLError('fixture-secret'), TimeoutError('fixture-secret')):
                with patch('urllib.request.build_opener') as opener:
                    opener.return_value.open.side_effect = error
                    try:
                        send('fixture-voice', body, 'fixture-secret')
                    except C.Fatal as err:
                        verdict('a remix transport failure is one call, never retried, with no secret: '
                                + type(error).__name__, opener.return_value.open.call_count == 1
                                and 'fixture-secret' not in str(err)
                                and (isinstance(error, urllib.error.HTTPError)
                                     or 'may have been charged' in str(err)), str(err))
                    else:
                        verdict('a remix transport failure is reported: ' + type(error).__name__, False)
        finally:
            C.ROOT = saved
