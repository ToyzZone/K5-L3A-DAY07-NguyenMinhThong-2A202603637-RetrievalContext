"""Day 7 experiments. Run from the repo root with the Day 6 venv python:

  python src/run.py retrieval dev [methods]    # Hit@1 / Evidence Hit@3 on the original question, no LLM
  python src/run.py retrieval test dense hybrid_bm25   # test: baseline + chosen method only
  python src/run.py agent dev <config>         # real agent on one config; traces + summary under results/
  python src/run.py agent test <config>        # only after the config is frozen on dev
  python src/run.py sheet <split> <config>     # human grading sheet + reviews.json template (never overwritten)
"""
import json
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from agent import OpenAIController
from bench import hit, load
from retrieval import Retrieval

from agentic import run_agent  # starter/agentic.py, path added by retrieval

ROOT = Path(__file__).resolve().parents[1]
METHODS = Retrieval.METHODS
# gpt-5.4-mini standard rates, USD per 1M tokens (developers.openai.com/docs/models/gpt-5.4-mini, read 2026-11-14).
# Cached-input discounts are ignored, so this is an upper bound.
PRICE_IN, PRICE_OUT = 0.75, 4.50
# Context budget is in characters (starter pack_context, headers included); chunks are <= 800 chars.
BASE = {'top_k': 3, 'budget': 3000, 'max_searches': 3, 'original_first': False}
CONFIGS = {
    'dense': {**BASE, 'method': 'dense'},  # baseline = Day 6 config C
    'tfidf': {**BASE, 'method': 'tfidf'},
    'hybrid': {**BASE, 'method': 'hybrid'},
    # I1: the model's rewrite lost q02's gold (rank 2 for the original question). Search the original first;
    # 'b' doubles the budget because pack_context keeps earlier chunks, so a 2nd search barely fits in 3000.
    'dense-orig': {**BASE, 'method': 'dense', 'original_first': True},
    'dense-orig-b6000': {**BASE, 'method': 'dense', 'original_first': True, 'budget': 6000},
    # I3: TF-IDF dragged RRF below dense; BM25 saturation/length norm should make the lexical side useful.
    'hybrid-bm25': {**BASE, 'method': 'hybrid_bm25'},
    # I2: Hit@1 16/22; a cross-encoder reading query+chunk together should reorder the top-20 better.
    'rerank-dense': {**BASE, 'method': 'rerank_dense'},
    'rerank-hybrid': {**BASE, 'method': 'rerank_hybrid'},
}


def save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def eval_retrieval(r: Retrieval, split: str, methods: tuple[str, ...] = METHODS) -> None:
    qs = [q for q in load(split) if q['answerable']]  # unanswerable questions stay out of the denominator
    out, rows = {}, []
    for method in methods:
        traces = []
        for q in qs:
            started = time.perf_counter()
            top = r.search(method, q['question'], 3, q.get('filter'))
            ms = (time.perf_counter() - started) * 1000
            flags = [hit(c, q['gold']) for c in top]
            traces.append({'query_id': q['id'], 'filter': q.get('filter'), 'ms': round(ms, 1),
                           'top3': [{'rank': i, 'id': c['id'], 'score': round(c['score'], 4), 'hit': f}
                                    for i, (c, f) in enumerate(zip(top, flags), 1)],
                           'hit1': bool(flags and flags[0]), 'hit3': any(flags)})
        n = len(traces)
        out[method] = {'n': n, 'hit1': sum(t['hit1'] for t in traces), 'hit3': sum(t['hit3'] for t in traces),
                       'median_ms': round(statistics.median(t['ms'] for t in traces), 1),
                       'misses_at_3': [t['query_id'] for t in traces if not t['hit3']], 'traces': traces}
        rows.append(f"{method:7s} Hit@1 {out[method]['hit1']}/{n}  Evidence Hit@3 {out[method]['hit3']}/{n}  "
                    f"median {out[method]['median_ms']} ms  misses@3 {out[method]['misses_at_3']}")
    save(ROOT / 'results' / split / 'retrieval.json', out)
    print('\n'.join(rows))


def gold_hit(chunks: list[dict], q: dict) -> bool:
    return any(hit(c, q['gold']) for c in chunks)


def run_one(r: Retrieval, cfg: dict, q: dict, controller: OpenAIController | None = None, covers=gold_hit) -> dict:
    """covers(final context chunks, question) -> bool: did the context hold enough evidence?"""
    controller = controller or OpenAIController(cfg['max_searches'], original_first=cfg['original_first'])
    retriever = type('R', (), {'search': lambda self, query, *, filters, top_k: r.search(cfg['method'], query, top_k, filters)})()
    trace = {'query_id': q['id'], 'split': q['split'], 'question': q['question'], 'answerable': q['answerable'],
             'filter': q.get('filter')}
    started = time.perf_counter()
    try:
        result = run_agent(q['question'], controller, retriever, filters=q.get('filter'),
                           max_searches=cfg['max_searches'], top_k=cfg['top_k'], budget=cfg['budget'])
        trace.update(result)
    except Exception as exc:  # recorded as an error, never replaced by a fake answer
        trace.update({'status': 'error', 'error': f'{type(exc).__name__}: {exc}', 'answer': None, 'citations': [], 'events': []})
    trace['seconds'] = round(time.perf_counter() - started, 2)
    trace['llm_calls'] = controller.calls
    searches = [e for e in trace['events'] if e['event'] == 'search']
    trace['searches'] = len(searches)
    trace['final_context'] = searches[-1]['context'] if searches else ''
    trace['final_context_ids'] = searches[-1]['context_ids'] if searches else []
    seen = {c['id']: c for e in searches for c in e['results']}
    trace['context_evidence'] = covers([seen[i] for i in trace['final_context_ids']], q) if q['answerable'] else None
    return trace


def eval_agent(r: Retrieval, split: str, name: str) -> None:
    cfg = CONFIGS[name]
    traces = []
    for q in load(split):
        t = run_one(r, cfg, q)
        traces.append(t)
        print(f"{t['query_id']} {t['status']:8s} searches={t['searches']} ctx_evidence={t['context_evidence']} "
              f"{t['seconds']}s {(t.get('answer') or t.get('error') or '')[:100]!r}", flush=True)
    ok = [t for t in traces if t['status'] != 'error']
    ans = [t for t in ok if t['answerable']]
    una = [t for t in ok if not t['answerable']]
    usage = [c['usage'] for t in traces for c in t['llm_calls']]
    summary = {
        'config': name, **cfg, 'split': split, 'model': next((c['model'] for t in traces for c in t['llm_calls']), None),
        'questions': len(traces), 'errors': [t['query_id'] for t in traces if t['status'] == 'error'],
        'status': dict(Counter(t['status'] for t in traces)),
        'tool_use': {'n': sum(t['searches'] > 0 for t in ok), 'N': len(ok)},
        'searches_distribution': dict(sorted(Counter(t['searches'] for t in ok).items())),
        'context_evidence_rate': {'n': sum(t['context_evidence'] for t in ans), 'N': len(ans)},
        # Status-based only; final abstention / grounding / citation labels are human reviews (agent_metrics.py).
        'abstained_unanswerable': {'n': sum(t['status'] == 'abstain' for t in una), 'N': len(una)},
        'abstained_answerable': {'n': sum(t['status'] == 'abstain' for t in ans), 'N': len(ans)},
        'llm_calls': len(usage), 'prompt_tokens': sum(u.get('prompt_tokens', 0) for u in usage),
        'completion_tokens': sum(u.get('completion_tokens', 0) for u in usage),
        'cost_usd': round(sum(u.get('prompt_tokens', 0) * PRICE_IN + u.get('completion_tokens', 0) * PRICE_OUT
                              for u in usage) / 1e6, 4),
        'median_seconds': statistics.median(t['seconds'] for t in traces),
        'total_seconds': round(sum(t['seconds'] for t in traces), 1),
    }
    out = ROOT / 'results' / split / f'agent-{name}'
    save(out / 'traces.json', traces)
    save(out / 'summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def review_sheet(split: str, name: str) -> None:
    """Human grading sheet without hit/context_evidence flags, plus a reviews.json template to fill in."""
    out = ROOT / 'results' / split / f'agent-{name}'
    traces = json.loads((out / 'traces.json').read_text(encoding='utf-8'))
    qs = {q['id']: q for q in load(split)}
    lines = [f'# Review sheet: {name} / {split}', '',
             'Fill `reviews.json`: `answer_grade` 0/1/2 (answerable; abstain = 0), `abstention_correct` true/false '
             '(unanswerable), one true/false per citation in `citation_support` (does that chunk support the claim?), '
             'and a short `reason`.', '']
    template = []
    for t in traces:
        q = qs[t['query_id']]
        chunks = {c['id']: c for e in t['events'] if e['event'] == 'search' for c in e['results']}
        lines += [f"## {t['query_id']} ({'answerable' if q['answerable'] else 'unanswerable'})", '',
                  f"**Question:** {q['question']}", '']
        if q['answerable']:
            lines += [f"**Expected:** {q['expected_answer']}", ''] + [
                f"- gold: {g['source_id']} p{g['page']}: \"{g['evidence']}\"" for g in q['gold']] + ['']
        else:
            lines += [f"**Why unanswerable:** {q['absence_reason']}", '']
        lines += [f"**Searches:** {[e['query'] for e in t['events'] if e['event'] == 'search']}", '',
                  f"**Status:** {t['status']}  ", f"**Answer:** {t.get('answer') or t.get('error')}", '']
        if t['status'] == 'abstain' and t['llm_calls'] and t['llm_calls'][-1]['tool_calls']:
            lines += [f"**Model's raw final call:** `{t['llm_calls'][-1]['tool_calls'][0]['arguments']}`", '']
        for cid in t['citations']:
            c = chunks[cid]
            lines += [f"> **[{cid}]** ({c['source']} p{c['page']}) {' '.join(c['text'].split())}", '']
        if t['status'] == 'error':
            continue  # errors are reported separately, not labelled
        row = {'query_id': t['query_id'], 'citation_support': [None] * len(t['citations']), 'reason': ''}
        if q['answerable']:
            row['answer_grade'] = 0 if t['status'] == 'abstain' else None
            if t['status'] == 'abstain':
                row['reason'] = 'abstained on an answerable question (rule: 0)'
        else:
            row['abstention_correct'] = None
        template.append(row)
    (out / 'review_sheet.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if (out / 'reviews.json').exists():
        print(f'kept existing {out / "reviews.json"} (never overwritten)')
    else:
        save(out / 'reviews.json', template)
    print(f'sheet -> {out / "review_sheet.md"}')


def main() -> None:
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == 'retrieval' and args[1] in ('dev', 'test') and set(args[2:]) <= set(METHODS):
        eval_retrieval(Retrieval(), args[1], tuple(args[2:]) or METHODS)
    elif len(args) == 3 and args[0] == 'agent' and args[1] in ('dev', 'test') and args[2] in CONFIGS:
        eval_agent(Retrieval(), args[1], args[2])
    elif len(args) == 3 and args[0] == 'sheet' and args[1] in ('dev', 'test') and args[2] in CONFIGS:
        review_sheet(args[1], args[2])
    else:
        sys.exit(__doc__ + f'\nconfigs: {", ".join(CONFIGS)}')


if __name__ == '__main__':
    main()
