"""Day 7 benchmark: Day 6 answerable questions + new unanswerable ones, hit definition, integrity check.

Build:  python src/bench.py build    (writes data/questions.json from Day 6 + data/unanswerable.json)
Verify: python src/bench.py verify   (counts, gold evidence inside one indexed chunk, absence regexes)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / 'data' / 'questions.json'


def squash(text: str) -> str:
    """Same hit rule as Day 6: case-sensitive containment after collapsing whitespace."""
    return ' '.join(text.split())


def hit(chunk: dict, gold: list[dict]) -> bool:
    return any(chunk['source_id'] == g['source_id'] and chunk['page'] == g['page']
               and squash(g['evidence']) in squash(chunk['text']) for g in gold)


def load(split: str | None = None) -> list[dict]:
    qs = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    return [q for q in qs if split in (None, q['split'])]


def build(day6_questions: Path) -> None:
    out = []
    for q in json.loads(day6_questions.read_text(encoding='utf-8')):
        gold = [{'source_id': q['gold_source_id'], 'page': q['gold_page'], 'evidence': q['evidence_quote']}]
        gold += [{'source_id': g['source_id'], 'page': g['page'], 'evidence': g['evidence_quote']} for g in q.get('alt_gold', [])]
        out.append({'id': q['id'], 'split': q['split'], 'type': q['type'], 'answerable': True, 'question': q['question'],
                    'expected_answer': q['expected_answer'], 'gold': gold,
                    **{k: q[k] for k in ('filter', 'note') if k in q}})
    out += json.loads((ROOT / 'data' / 'unanswerable.json').read_text(encoding='utf-8'))
    QUESTIONS.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'wrote {len(out)} questions -> {QUESTIONS}')


def verify() -> None:
    from retrieval import DAY6, Day6
    sys.path.insert(0, str(DAY6))
    from src.ingestion import DATA_DIR, load_pdf, normalize_text

    qs = load()
    ids = [q['id'] for q in qs]
    assert len(set(ids)) == len(ids), 'duplicate question IDs'
    for split, need in (('dev', (15, 2)), ('test', (5, 2))):
        got = (sum(q['answerable'] for q in qs if q['split'] == split), sum(not q['answerable'] for q in qs if q['split'] == split))
        assert got[0] >= need[0] and got[1] >= need[1], f'{split}: {got} answerable/unanswerable, need {need}'
        print(f'{split}: {got[0]} answerable + {got[1]} unanswerable')

    chunks = Day6().all_chunks()
    for q in qs:
        if q['answerable']:
            assert any(hit(c, q['gold']) for c in chunks), f"{q['id']}: no indexed chunk holds its gold evidence"
    print('every answerable question has its evidence inside one indexed chunk')

    # Absence is checked on every page of every PDF (indexed or not), not on what top-k happened to return.
    sources = json.loads((DATA_DIR / 'sources.json').read_text(encoding='utf-8'))
    pages = [(s['source_id'], p.page, squash(normalize_text(p.text))) for s in sources
             for p in load_pdf(DATA_DIR / 'pdf' / s['file'], s['source_id'], s['file'])]
    for q in qs:
        if not q['answerable']:
            found = {(sid, page) for sid, page, text in pages if re.search(q['absence_check'], text, re.I)}
            extra = found - {tuple(p) for p in q['allowed_pages']}
            assert not extra, f"{q['id']}: absence regex matched undocumented pages {sorted(extra)}"
    print(f'absence regexes match only documented pages ({len(pages)} PDF pages scanned)')


if __name__ == '__main__':
    if sys.argv[1:] == ['build']:
        build(Path(__file__).resolve().parents[3] / 'lab 6' / 'benchmark' / 'questions.json')
    elif sys.argv[1:] == ['verify']:
        verify()
    else:
        sys.exit(__doc__)
