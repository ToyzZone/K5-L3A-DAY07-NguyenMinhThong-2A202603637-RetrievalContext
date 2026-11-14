"""Offline checks of Day 7 logic (fake model/retriever). Needs the Day 6 venv; measures no quality."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import agent  # noqa: E402
from bench import hit  # noqa: E402
from retrieval import BM25, rrf  # noqa: E402
from run import CONFIGS, run_one  # noqa: E402


def chunk(cid, text='x', page=1):
    return {'id': cid, 'text': text, 'source_id': 'doc', 'source': 'doc.pdf', 'page': page,
            'metadata': {'section': 's'}, 'score': 1.0}


def tool(name, args):
    import json
    return {'model': 'fake', 'usage': {'prompt_tokens': 10, 'completion_tokens': 2},
            'choices': [{'message': {'tool_calls': [{'function': {'name': name, 'arguments': json.dumps(args)}}]}}]}


class Day7Tests(unittest.TestCase):
    def test_rrf_rewards_agreement_and_keeps_top_k(self):
        a, b, c = chunk('a'), chunk('b'), chunk('c')
        fused = rrf([[a, b], [b, c]], top_k=2)
        self.assertEqual([x['id'] for x in fused], ['b', 'a'])  # b is in both lists
        self.assertTrue(all(x['strategy'] == 'hybrid' for x in fused))

    def test_hit_needs_page_and_whole_quote_across_line_breaks(self):
        gold = [{'source_id': 'doc', 'page': 5, 'evidence': 'less than 2,300 milligrams'}]
        self.assertTrue(hit(chunk('a', 'to less than 2,300\nmilligrams per day', 5), gold))
        self.assertFalse(hit(chunk('a', 'to less than 2,300', 5), gold))
        self.assertFalse(hit(chunk('a', 'less than 2,300 milligrams', 6), gold))

    def test_run_one_traces_search_answer_and_context_evidence(self):
        script = iter([tool('search_documents', {'query': 'sodium'}),
                       tool('answer', {'answer': '2,300 mg [a]', 'citations': ['a']})])
        agent.post = lambda payload: next(script)
        retrieval = type('R', (), {'search': lambda self, m, q, k, f: [chunk('a', 'less than 2,300 milligrams', 5)]})()
        q = {'id': 'q1', 'split': 'dev', 'question': 'sodium?', 'answerable': True,
             'gold': [{'source_id': 'doc', 'page': 5, 'evidence': '2,300 milligrams'}]}
        t = run_one(retrieval, CONFIGS['dense'], q)
        self.assertEqual((t['status'], t['citations'], t['searches'], t['context_evidence']), ('answered', ['a'], 1, True))
        self.assertEqual([c['usage']['prompt_tokens'] for c in t['llm_calls']], [10, 10])

    def test_original_first_searches_the_question_without_a_model_call(self):
        script = iter([tool('answer', {'answer': '2,300 mg [a]', 'citations': ['a']})])
        agent.post = lambda payload: next(script)
        seen = []
        retrieval = type('R', (), {'search': lambda self, m, q, k, f: seen.append(q) or [chunk('a')]})()
        q = {'id': 'q1', 'split': 'dev', 'question': 'Sodium limit?', 'answerable': True,
             'gold': [{'source_id': 'doc', 'page': 9, 'evidence': 'nope'}]}
        t = run_one(retrieval, CONFIGS['dense-orig'], q)
        self.assertEqual((seen, len(t['llm_calls']), t['context_evidence']), (['Sodium limit?'], 1, False))

    def test_advanced_evidence_needs_every_page_and_long_tables_split_with_header(self):
        import advanced
        q = {'evidence': [{'page': 27}, {'page': 104}]}
        self.assertFalse(advanced.evidence_pages_covered([{'page': 27}], q))
        self.assertTrue(advanced.evidence_pages_covered([{'page': 27}, {'page': 104}, {'page': 5}], q))
        rows = '\n'.join(f'| row {i} | {i} |' for i in range(200))
        rec = {'elements': [{'type': 'table', 'label': 'Table 3', 'title': 'T', 'content': rows},
                            {'type': 'photo', 'content': 'decorative'}]}
        parts = advanced.visual_chunks(104, rec)
        self.assertGreater(len(parts), 1)  # split, photo dropped
        self.assertTrue(all(c.text.startswith('[TABLE] Table 3') and len(c.text) <= advanced.MAX_VISUAL_CHARS for c in parts))
        self.assertEqual(' '.join(c.text.split('\n', 1)[1] for c in parts).split(), rows.split())  # no row lost
        self.assertEqual(parts[0].chunk_id, 'who-gsr-2022:p104:table:00-0')

    def test_advanced_context_continues_labels_one_page_only(self):
        import advanced
        p34 = {'elements': [{'type': 'table', 'label': 'TABLE 2', 'title': 'Summary'}]}
        p35 = {'elements': [{'type': 'table', 'label': None, 'title': None}, {'type': 'photo', 'label': None}]}
        _, prev = advanced.add_context(34, p34, 'x', None)
        rec, prev = advanced.add_context(35, p35, 'x', prev)
        rec36, _ = advanced.add_context(36, {'elements': [{'type': 'table', 'label': None}]}, 'x', prev)
        self.assertEqual(rec['elements'][0]['label'], 'TABLE 2 (continued from printed page 18)')
        self.assertEqual(rec36['elements'][0]['label'], 'TABLE 2 (continued from printed page 19)')  # no chained suffix
        self.assertIsNone(rec['elements'][1]['label'])  # photos untouched
        rec, _ = advanced.add_context(128, {'elements': [{'type': 'table', 'label': None, 'title': None}]}, 'Annex 2: Data sources', None)
        self.assertEqual((rec['elements'][0]['label'], rec['elements'][0]['title']), (None, 'page begins: Annex 2: Data sources'))

    def test_bm25_prefers_rare_term_matches_and_skips_non_matches(self):
        docs = [chunk('a', 'sodium sodium limit'), chunk('b', 'limit limit limit limit'), chunk('c', 'water')]
        ranked = BM25(docs).search('sodium limit')
        self.assertEqual([c['id'] for c in ranked], ['a', 'b'])

    def test_abstain_and_errors_are_recorded_not_faked(self):
        script = iter([tool('answer', {'answer': agent.ABSTAIN, 'citations': []})])
        agent.post = lambda payload: next(script)
        retrieval = type('R', (), {'search': lambda self, m, q, k, f: []})()
        q = {'id': 'u1', 'split': 'dev', 'question': 'covid?', 'answerable': False}
        cfg = CONFIGS['dense']
        t = run_one(retrieval, cfg, q)
        self.assertEqual((t['status'], t['searches'], t['context_evidence']), ('abstain', 0, None))
        agent.post = lambda payload: (_ for _ in ()).throw(RuntimeError('OpenAI HTTP 429'))
        t = run_one(retrieval, cfg, q)
        self.assertEqual(t['status'], 'error')
        self.assertIn('429', t['error'])


if __name__ == '__main__':
    unittest.main()
