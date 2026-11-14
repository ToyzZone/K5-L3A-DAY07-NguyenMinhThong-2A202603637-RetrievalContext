"""Embed the Day 7 result files into report/lab_walkthrough.html (the <script id="data"> block is replaced in place).

Run from the repo root after any new run or label change:  python report/build_walkthrough.py
The page shows only numbers read from these files; nothing is typed in by hand.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'
PAGE = ROOT / 'report' / 'lab_walkthrough.html'
SUMMARY_KEYS = ('config', 'method', 'index', 'top_k', 'budget', 'max_searches', 'original_first', 'images', 'split', 'model',
                'questions', 'errors', 'status', 'tool_use', 'searches_distribution', 'context_evidence_rate', 'by_group',
                'abstained_unanswerable', 'abstained_answerable', 'llm_calls', 'images_sent', 'prompt_tokens',
                'completion_tokens', 'cost_usd', 'median_seconds', 'total_seconds')


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def runs_in(base: Path, chunks: dict) -> dict:
    runs = {}
    for d in sorted(base.glob('*/agent-*')):
        split, name = d.parent.name, d.name.removeprefix('agent-')
        if split not in ('dev', 'test') or not (d / 'traces.json').exists():
            continue
        summary = load(d / 'summary.json')
        traces = {}
        for t in load(d / 'traces.json'):
            events = []
            for e in t['events']:
                if e['event'] != 'search':
                    events.append({'event': e['event']})
                    continue
                for c in e['results']:
                    chunks.setdefault(c['id'], {'text': c['text'], 'source_id': c['source_id'], 'page': c['page'],
                                                'kind': c['id'].split(':')[2]})
                events.append({'event': 'search', 'query': e['query'], 'context_ids': e['context_ids'],
                               'context_chars': len(e['context']), 'results': [[c['id'], round(c['score'], 4)] for c in e['results']]})
            traces[t['query_id']] = {
                'status': t['status'], 'answer': t.get('answer'), 'citations': t.get('citations', []), 'error': t.get('error'),
                'seconds': t['seconds'], 'events': events, 'final_context_ids': t['final_context_ids'],
                'context_evidence': t['context_evidence'],
                'calls': [{'tool': (c['tool_calls'] or [{}])[0].get('name'), 'args': (c['tool_calls'] or [{}])[0].get('arguments'),
                           'in': c['usage'].get('prompt_tokens'), 'out': c['usage'].get('completion_tokens'),
                           'seconds': c['seconds'], 'images': c.get('images', 0)} for c in t['llm_calls']]}
        run = {'summary': {k: summary[k] for k in SUMMARY_KEYS if k in summary}, 'traces': traces}
        for extra in ('reviews', 'agent_metrics', 'score'):
            if (d / f'{extra}.json').exists():
                data = load(d / f'{extra}.json')
                run[extra] = {r['query_id']: r for r in data} if extra == 'reviews' else data
        runs[f'{split}/{name}'] = run
    return runs


def main() -> None:
    chunks: dict = {}
    data = {
        'questions': load(ROOT / 'data' / 'questions.json'),
        'retrieval': {s: {m: {**{k: v[k] for k in ('n', 'hit1', 'hit3', 'median_ms', 'misses_at_3')},
                              'per': {t['query_id']: t['top3'] for t in v['traces']}}
                          for m, v in load(RES / s / 'retrieval.json').items()} for s in ('dev', 'test')},
        'runs': runs_in(RES, chunks),
        'advanced': None,
    }
    adv_q = ROOT / 'data' / 'advanced' / 'questions.json'
    if adv_q.exists():
        sel = RES / 'advanced' / 'dev' / 'selection.json'
        data['advanced'] = {'questions': load(adv_q), 'runs': runs_in(RES / 'advanced', chunks),
                            'selection': load(sel) if sel.exists() else None}
    data['chunks'] = chunks
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = PAGE.read_text(encoding='utf-8')
    html, n = re.subn(r'(<script id="data" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + blob + m.group(2), html, count=1, flags=re.S)
    assert n == 1, 'data block not found in lab_walkthrough.html'
    PAGE.write_text(html, encoding='utf-8')
    print(f'{PAGE.relative_to(ROOT)}: {len(html) / 1024:.0f} KB, {len(data["runs"])} runs, {len(chunks)} chunks, '
          f'advanced={"yes" if data["advanced"] else "no"}')


if __name__ == '__main__':
    main()
