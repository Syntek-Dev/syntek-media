#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["whisperx==3.8.6"]
# ///
"""Align known English words, offline (DESIGN D67). Started by media.py transcribe.

fetch is the author's one deliberate network step. status and --self-test use only the
standard library. Heavy imports are lazy, with torch first; this worker also runs on 3.10.
The launcher owns project paths and D66's output guard; no interpreter path enters a file.
"""
from __future__ import annotations

import argparse
import contextlib
import difflib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

VERSION = '3.8.6'
WEIGHTS = 'wav2vec2_fairseq_base_ls960_asr_ls960.pth'
MODEL = 'large-v3-turbo'
REPO = 'models--mobiuslabsgmbh--faster-whisper-large-v3-turbo'
LOW_SCORE = 0.5   # maintainer's threshold; a warning, not an untimed-word finding
PART_RE = re.compile(r"[a-z]+(?:'[a-z]+)*", re.I)


class CannotRun(Exception):
    pass


class BadText(Exception):
    pass


def cache_paths() -> dict:
    home = Path.home()
    cache = Path(os.environ.get('XDG_CACHE_HOME') or home / '.cache')
    torch_home = Path(os.environ.get('TORCH_HOME') or cache / 'torch')
    hf_home = Path(os.environ.get('HF_HOME') or cache / 'huggingface')
    hf = Path(os.environ.get('HF_HUB_CACHE') or os.environ.get('HUGGINGFACE_HUB_CACHE') or hf_home / 'hub')
    nltk = [Path(p).expanduser() for p in os.environ.get('NLTK_DATA', '').split(os.pathsep) if p]
    nltk.append(home / 'nltk_data')
    punkt_files = ('collocations.tab', 'sent_starters.txt', 'abbrev_types.txt', 'ortho_context.tab')
    punkt = next((p for p in nltk if all((p / 'tokenizers/punkt_tab/english' / f).is_file()
                                       for f in punkt_files)), nltk[0])
    repo = hf / REPO
    ref = repo / 'refs/main'
    revision = ref.read_text().strip() if ref.is_file() else ''
    snapshot = repo / 'snapshots' / revision if re.fullmatch(r'[a-f0-9]+', revision) else None
    return {'weights': torch_home / 'hub/checkpoints' / WEIGHTS, 'nltk': punkt,
            'punkt_files': [punkt / 'tokenizers/punkt_tab/english' / f for f in punkt_files],
            'snapshot': snapshot}


def missing_cache(paths: dict, cross_check=True) -> list:
    missing = []
    if not paths['weights'].is_file():
        missing.append('English wav2vec2 weights')
    if not all(f.is_file() for f in paths['punkt_files']):
        missing.append("nltk's English punkt_tab")
    snapshot = paths['snapshot']
    required = ('model.bin', 'config.json', 'tokenizer.json')
    if cross_check and (snapshot is None or not all((snapshot / f).is_file() for f in required)
                        or not list(snapshot.glob('vocabulary.*'))):
        missing.append('faster-whisper large-v3-turbo in the default Hugging Face cache')
    return missing


def environment(paths: dict, fetch=False) -> None:
    os.environ['PYANNOTE_METRICS_ENABLED'] = '0'
    os.environ['NLTK_DATA'] = str(paths['nltk'])
    os.environ['HF_HUB_OFFLINE'] = '0' if fetch else '1'


def installed_version() -> str:
    try:
        return importlib.metadata.version('whisperx')
    except importlib.metadata.PackageNotFoundError:
        return ''


def require_version() -> None:
    if not (3, 10) <= sys.version_info[:2] < (3, 14):
        raise CannotRun('transcribe needs Python >=3.10,<3.14; use a supported interpreter at user scope')
    version = installed_version()
    if version != VERSION:
        raise CannotRun(f'WhisperX {VERSION} is required; found {version or "none"}. '
                        'Use MEDIA_TRANSCRIBE_PYTHON naming that environment, or transcribe fetch')


def parts(text: str) -> list:
    """The English model's letters and apostrophe, with punctuation left out of alignment.

    Digits, symbols and foreign letters must never become plausible wildcard timings.
    Hyphens split a word into parts; its original spelling is kept separately for captions.
    """
    text = text.replace('’', "'").replace('‘', "'")
    for char in text:
        kind = unicodedata.category(char)
        if char.isdigit() or kind[0] in ('N', 'S') or (char.isalpha() and not char.isascii()) \
                or kind[0] == 'C' and not char.isspace():
            raise BadText(f'aligner text contains unsupported {char!r}; spell numbers and symbols as spoken')
    if re.search(r'[\[\]{}<>_/\\%&@#*]', text):
        raise BadText('aligner text contains a symbol, IPA or audio tag; use plain spoken respellings')
    return PART_RE.findall(text.replace('-', ' '))


def prepare(segments: list, pronunciations: dict) -> list:
    sounds = {word.casefold(): form for word, form in pronunciations.items()}
    prepared, ids = [], set()
    for segment in segments:
        sid = str(segment.get('id', '')).strip()
        if not sid or sid in ids:
            raise CannotRun('every segment needs a unique id')
        ids.add(sid)
        text = str(segment.get('text', '')).strip()
        groups, align_words = [], []
        for word in text.split():
            # Check the original too: a pronunciation entry must not hide a digit or symbol.
            source = parts(word)
            if not source:
                if groups:
                    groups[-1]['word'] += ' ' + word
                continue
            key = word.strip(".,!?;:\"'‘’“”()—–").casefold()
            spoken = parts(str(sounds.get(key, word)))
            if not spoken:
                raise BadText(f'{sid}: {word!r} has no letters to align')
            groups.append({'word': word, 'parts': spoken})
            align_words.extend(spoken)
        if not groups:
            raise BadText(f'{sid}: no spoken words to align')
        start, end = segment.get('start'), segment.get('end')
        if not finite(start) or not finite(end) or start < 0 or end <= start:
            raise CannotRun(f'{sid}: invalid segment start/end')
        prepared.append({**segment, 'groups': groups, 'align_words': align_words,
                         'align_text': ' '.join(align_words)})
    if not prepared:
        raise CannotRun('no approved segment to align')
    return prepared


def finite(value) -> bool:
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def sequence(text: str) -> list:
    return [word.casefold() for word in PART_RE.findall(text.replace('’', "'").replace('‘', "'"))]


def collect(segment: dict, alignment: dict) -> tuple:
    """Map parts back to one script word; unknown/missing words never inherit another's time."""
    returned = alignment.get('segments', [])
    issues, warnings, rows = [], [], []
    if not returned or any(not item.get('words') for item in returned):
        issues.append(f"{segment['id']}: an aligned segment returned no words")
    aligned = [word for item in returned for word in item.get('words', [])]
    heard = [str(word.get('word', '')).casefold() for word in aligned]
    expected = [word.casefold() for word in segment['align_words']]
    mismatch = heard != expected
    if mismatch:
        issues.append(f"{segment['id']}: aligned word sequence differs: expected {' '.join(expected)!r}; "
                      f"returned {' '.join(heard)!r}")
    cursor = 0
    for group in segment['groups']:
        timed = aligned[cursor:cursor + len(group['parts'])] if not mismatch else []
        cursor += len(group['parts'])
        good = len(timed) == len(group['parts']) and all(
            finite(w.get('start')) and finite(w.get('end')) and finite(w.get('score'))
            and segment['start'] <= w['start'] < w['end'] <= segment['end'] + 0.001
            and 0 <= w['score'] <= 1 for w in timed)
        if good and any(a['end'] > b['start'] + 0.001 for a, b in zip(timed, timed[1:])):
            good = False
        row = {'word': group['word'], 'start': timed[0]['start'] if good else None,
               'end': timed[-1]['end'] if good else None,
               'score': min(w['score'] for w in timed) if good else None, 'segment': segment['id']}
        rows.append(row)
        if not good:
            issues.append(f"{segment['id']}: untimed word {group['word']!r}")
        elif row['score'] < LOW_SCORE:
            warnings.append(f"{segment['id']}: low score {row['score']:.3f} for {group['word']!r}")
    return rows, issues, warnings


def result(piece: str, segments: list, alignments: list, heard: str | None) -> dict:
    rows, issues, warnings, differences = [], [], [], []
    if len(alignments) != len(segments):
        raise CannotRun('alignment result count differs from the input segments')
    for segment, alignment in zip(segments, alignments):
        word_rows, bad, low = collect(segment, alignment)
        rows.extend(word_rows); issues.extend(bad); warnings.extend(low)
        if str(segment.get('request', '')).strip() != str(segment['text']).strip():
            differences.append(f"- {segment['id']}: text: {segment['text']}\n"
                               f"  request: {segment.get('request', '') or '(not recorded)'}")
    if heard is not None:
        script = sequence(' '.join(s['text'] for s in segments))
        actual = sequence(heard)
        if actual != script:
            delta = ' '.join(difflib.ndiff(script, actual))
            issues.append('Heard words disagree with the script: ' + delta)
    sections = [f'# {piece} — words check', '',
                'Alignment times are estimates: check them in a burned preview.', '',
                'Cross-check: ' + ('disabled with --no-cross-check.' if heard is None else
                                    'faster-whisper large-v3-turbo, compared with the script.'), '',
                '## Findings', '', *(['- ' + i for i in issues] or ['None.']), '',
                '## Low scores', '', *(['- ' + w for w in warnings] or ['None below 0.5.']), '',
                '## Request and text differences', '', *(differences or ['None.']), '']
    return {'words': rows, 'check': '\n'.join(sections), 'exit': 1 if issues else 0}


def align_job(job: dict) -> dict:
    segments = prepare(job['segments'], job.get('pronunciations', {}))
    paths = cache_paths()
    environment(paths)
    missing = missing_cache(paths, job.get('cross_check', True))
    if missing:
        raise CannotRun('Missing ' + ', '.join(missing) + '; run python3 toolkit/media.py transcribe fetch once')
    require_version()
    import torch   # first GPU-library import: its wheels supply cuBLAS and cuDNN
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    precision = 'float16' if device == 'cuda' else 'int8'
    print(f'transcribe: {device}; cross-check precision {precision}', file=sys.stderr, flush=True)
    # Libraries may print progress to stdout: reserve our stdout for the JSON reply.
    with contextlib.redirect_stdout(sys.stderr):
        import whisperx
        model, metadata = whisperx.load_align_model('en', device, model_dir=str(paths['weights'].parent))
        audio = whisperx.load_audio(job['audio'])
        aligned = [whisperx.align([{'text': s['align_text'], 'start': s['start'], 'end': s['end']}],
                                 model, metadata, audio, device) for s in segments]
        del model
        if device == 'cuda':
            torch.cuda.empty_cache()
        heard = None
        if job.get('cross_check', True):
            from faster_whisper import WhisperModel
            cross = WhisperModel(str(paths['snapshot']), device=device, compute_type=precision,
                                 local_files_only=True)
            # load_audio already supplies mono 16 kHz samples. Reuse them rather than
            # decode the same file through a second decoder with its own codec versions.
            speech, _info = cross.transcribe(audio, language='en')
            heard = ' '.join(segment.text for segment in speech)
    return result(job['piece'], segments, aligned, heard)


def fetch() -> int:
    paths = cache_paths()
    environment(paths, fetch=True)
    require_version()
    import torch   # before faster-whisper or WhisperX
    import whisperx
    import nltk
    from faster_whisper.utils import download_model
    paths['weights'].parent.mkdir(parents=True, exist_ok=True)
    whisperx.load_align_model('en', 'cpu', model_dir=str(paths['weights'].parent))
    if not nltk.download('punkt_tab', download_dir=str(paths['nltk']), quiet=False):
        raise CannotRun('nltk punkt_tab fetch failed; read the NLTK error above. '
                        'If it refuses a proxy, retry fetch with all proxy variables unset '
                        '(including NO_PROXY and no_proxy); '
                        'only use NLTK_ALLOW_PROXIED_URLOPEN=1 if you trust that proxy')
    download_model(MODEL)   # leave download_root unset: reuse the default HF cache
    missing = missing_cache(cache_paths())
    if missing:
        raise CannotRun('Fetch incomplete: ' + ', '.join(missing))
    print('transcribe fetch: English alignment, punkt_tab and cross-check model ready')
    print('INTERPRETER: ' + sys.executable)
    return 0


def self_test() -> int:
    from types import SimpleNamespace
    from unittest.mock import patch
    failures = []
    def check(label, good):
        print(('ok' if good else 'FAIL') + ' — ' + label)
        if not good:
            failures.append(label)
    segment = {'id': 's01', 'text': 'A ferry crosses.', 'request': '[quiet] A feh-ree crosses.',
               'start': 0.0, 'end': 3.0}
    prepared = prepare([segment], {'ferry': 'feh-ree'})
    check('hyphens split respelling parts, plain words stay mapped',
          prepared[0]['align_text'] == 'A feh ree crosses' and len(prepared[0]['groups']) == 3)
    alignment = {'segments': [{'words': [
        {'word': 'A', 'start': 0.1, 'end': 0.2, 'score': 0.8},
        {'word': 'feh', 'start': 0.3, 'end': 0.6, 'score': 0.7},
        {'word': 'ree', 'start': 0.7, 'end': 1.0, 'score': 0.4},
        {'word': 'crosses', 'start': 1.1, 'end': 2.5, 'score': 0.9}]}]}
    out = result('001-fixture', prepared, [alignment], 'A ferry crosses.')
    check('one respelled word spans all parts and takes their minimum score',
          out['words'][1] == {'word': 'ferry', 'start': 0.3, 'end': 1.0, 'score': 0.4, 'segment': 's01'})
    check('low scores warn; request/text differences are reported, no finding',
          out['exit'] == 0 and 'low score 0.400' in out['check'] and '[quiet]' in out['check'])
    check('cross-check disagreement is a finding',
          result('001-fixture', prepared, [alignment], 'A boat crosses.')['exit'] == 1)
    check('disabling cross-check is explicit',
          'disabled with --no-cross-check' in result('001-fixture', prepared, [alignment], None)['check'])
    for value in ('two 2 boats', 'cost £ thirteen', '[quiet] hello', '/IPA/', 'café',
                  'ten %', 'A & ferry', '@ferry', '#ferry', '*ferry'):
        try:
            parts(value)
            rejected = False
        except BadText:
            rejected = True
        check('reject unsafe aligner text ' + repr(value), rejected)
    for label, mutated in (
        ('no words', {'segments': [{'words': []}]}),
        ('different sequence', {'segments': [{'words': [{**w, 'word': 'Else'} if i == 0 else w
                                                      for i, w in enumerate(alignment['segments'][0]['words'])]}]}),
        ('missing score', {'segments': [{'words': [{**w, 'score': None} for w in alignment['segments'][0]['words']]}]}),
        ('nonfinite times', {'segments': [{'words': [{**w, 'start': float('nan')} for w in alignment['segments'][0]['words']]}]})):
        bad = result('001-fixture', prepared, [mutated], None)
        check(label + ' is a finding with JSON-safe untimed words', bad['exit'] == 1
              and any(w['start'] is None for w in bad['words']))
        if label == 'no words':
            check('empty segments are explicitly named in the check', 'returned no words' in bad['check'])
        json.dumps(bad, allow_nan=False)
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder)
        paths = {'weights': p / 'missing.pth', 'punkt_files': [p / 'missing.tab'], 'snapshot': None}
        check('missing caches checked without dependencies', len(missing_cache(paths)) == 3)
        check('no cross-check does not need its model', len(missing_cache(paths, False)) == 2)
        with patch.dict(os.environ), patch.object(sys.modules[__name__], 'cache_paths',
                                                  return_value={**paths, 'nltk': p}):
            try:
                align_job({'piece':'001-fixture', 'segments':[segment], 'audio':'missing.wav'})
                rejected = False
            except CannotRun as error:
                rejected = 'transcribe fetch' in str(error)
            check('missing fetched files exit before heavy imports, naming transcribe fetch', rejected)
        decoded = object()
        class CrossCheck:
            def __init__(self, *_args, **_kwargs):
                pass
            def transcribe(self, samples, language):
                if samples is not decoded or language != 'en':
                    raise TypeError('cross-check needs the decoded mono samples')
                return [SimpleNamespace(text='A ferry crosses.')], None
        fake_torch = SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False))
        fake_whisperx = SimpleNamespace(load_align_model=lambda *_args, **_kwargs: (object(), {}),
                                       load_audio=lambda _path: decoded,
                                       align=lambda *_args, **_kwargs: alignment)
        with patch.dict(os.environ), patch.dict(sys.modules, {'torch': fake_torch,
                        'whisperx': fake_whisperx,
                        'faster_whisper': SimpleNamespace(WhisperModel=CrossCheck)}), \
                patch.object(sys.modules[__name__], 'cache_paths', return_value={**paths, 'nltk': p}), \
                patch.object(sys.modules[__name__], 'missing_cache', return_value=[]), \
                patch.object(sys.modules[__name__], 'require_version'):
            try:
                reply = align_job({'piece': '001-fixture', 'segments': [segment],
                                   'pronunciations': {'ferry': 'feh-ree'}, 'audio': 'voice.wav'})
                reused = reply['exit'] == 0 and 'disabled with' not in reply['check']
            except TypeError:
                reused = False
            check('default cross-check reuses the decoded mono samples', reused)
    check('self-test imports no heavy dependency', not any(name in sys.modules for name in
                                                        ('torch', 'whisperx', 'faster_whisper', 'nltk')))
    print(f'transcribe self-test: {len(failures)} failure(s)')
    return 1 if failures else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('fetch')
    sub.add_parser('status')
    align = sub.add_parser('align')
    align.add_argument('job', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return self_test()
        if args.command == 'status':
            print(json.dumps({'version': installed_version(), 'missing': missing_cache(cache_paths()),
                              'supported_python': (3, 10) <= sys.version_info[:2] < (3, 14)}))
            return 0
        if args.command == 'fetch':
            return fetch()
        if args.command == 'align':
            reply = align_job(json.loads(args.job.read_text(encoding='utf-8')))
            print(json.dumps(reply, ensure_ascii=False, allow_nan=False))
            return reply['exit']
        parser.error('choose fetch, status or align, or --self-test')
    except BadText as error:
        print(f'transcribe: {error}', file=sys.stderr)
        return 1
    except (CannotRun, OSError, ValueError, KeyError, TypeError, ImportError, RuntimeError) as error:
        print(f'transcribe could not run: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
