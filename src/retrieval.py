"""Retrieval over the Day 6 index. Run with the Day 6 venv (same model, same pins).

Day 6 repo: https://github.com/ToyzZone/K5-L3A-DAY06-NguyenMinhThong-2A202603637-DataIngestion
Set DAY6_DIR to its starter/ folder if it is not at ../../lab 6/starter.
"""
import math
import os
import sys
from collections import Counter
from pathlib import Path

DAY6 = Path(os.getenv('DAY6_DIR') or Path(__file__).resolve().parents[3] / 'lab 6' / 'starter')
sys.path.insert(0, str(DAY6))  # Day 6's `src` is a regular package, so it wins over this folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'starter'))

from baseline import TfidfIndex, tokenize  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from src.embeddings import MyEmbedder  # noqa: E402
from src.store import METADATA, PgVectorStore  # noqa: E402

INDEX = 'B'  # Day 6 chosen chunking: paragraph blocks <= 800 chars (Day 6 config C = B + question-scope filter)


def to_chunk(row: dict, strategy: str, score: float) -> dict:
    """Day 6 row -> Day 7 chunk contract (data/README.md)."""
    m = row['metadata']
    return {'id': row['chunk_id'], 'text': row['text'], 'source_id': m['document_id'], 'source': m['source'],
            'page': m['page'], 'metadata': m, 'score': score, 'strategy': strategy}


class Day6:
    """The Day 6 embedder + pgvector table. Errors propagate: no fallback."""

    def __init__(self, index: str = INDEX) -> None:
        load_dotenv(DAY6 / '.env')
        self.index = index  # 'B' = Day 6 corpus; 'GSR' = advanced-challenge document (src/advanced.py)
        self.embedder = MyEmbedder()
        self.store = PgVectorStore(os.environ['DATABASE_URL'], self.embedder.dimensions)

    def dense(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        rows = self.store.search(self.index, self.embedder.embed_query(query), top_k, filters)
        return [to_chunk(r, 'dense', r['score']) for r in rows]

    def all_chunks(self) -> list[dict]:
        """Every chunk of the index, so lexical methods search the exact same corpus version."""
        with self.store._connect() as conn:
            rows = conn.execute(f"SELECT chunk_id, text, {', '.join(METADATA)} FROM chunks "
                                "WHERE strategy = %s ORDER BY chunk_id", (self.index,)).fetchall()
        return [to_chunk({'chunk_id': r['chunk_id'], 'text': r['text'], 'metadata': {k: r[k] for k in METADATA}},
                         'corpus', 0.0) for r in rows]


def matches(chunk: dict, filters: dict | None) -> bool:
    return all(chunk['metadata'].get(k) == v for k, v in (filters or {}).items())


def rrf(rankings: list[list[dict]], top_k: int, k: int = 60) -> list[dict]:
    """Reciprocal rank fusion: rank-based, so dense cosine and TF-IDF scores never need a common scale."""
    fused: dict[str, dict] = {}
    for ranked in rankings:
        for rank, c in enumerate(ranked, 1):
            fused.setdefault(c['id'], {**c, 'score': 0.0, 'strategy': 'hybrid'})['score'] += 1 / (k + rank)
    return sorted(fused.values(), key=lambda c: (-c['score'], c['id']))[:top_k]


class BM25:
    """Okapi BM25 (k1=1.5, b=0.75): term-frequency saturation + length normalisation that plain TF-IDF lacks."""

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks, self.k1, self.b = chunks, k1, b
        self.tf = [Counter(tokenize(c['text'])) for c in chunks]
        self.lengths = [sum(t.values()) for t in self.tf]
        self.avg = sum(self.lengths) / len(self.lengths)
        df = Counter(term for t in self.tf for term in t)
        self.idf = {t: math.log(1 + (len(chunks) - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def search(self, query: str) -> list[dict]:
        terms = set(tokenize(query)) & self.idf.keys()  # ponytail: query term repeats ignored
        out = []
        for c, tf, n in zip(self.chunks, self.tf, self.lengths):
            norm = self.k1 * (1 - self.b + self.b * n / self.avg)
            s = sum(self.idf[t] * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in terms if t in tf)
            if s > 0:
                out.append({**c, 'score': s, 'strategy': 'bm25'})
        return sorted(out, key=lambda c: (-c['score'], c['id']))


RERANKER = 'BAAI/bge-reranker-base'
RERANKER_REVISION = '2cfc18c9415c912f9d8155881c133215df768a70'  # HF commit used for every reported run


class Retrieval:
    """Methods over the same index version: dense (Day 6 pgvector), tfidf, bm25, hybrid (RRF), rerank."""

    POOL = 20  # candidates per retriever before fusion / rerank
    METHODS = ('dense', 'tfidf', 'bm25', 'hybrid', 'hybrid_bm25', 'rerank_dense', 'rerank_hybrid')

    def __init__(self, index: str = INDEX) -> None:
        self.day6 = Day6(index)
        self.chunks = self.day6.all_chunks()
        self.tfidf_index = TfidfIndex(self.chunks)  # starter/baseline.py, English \w+ tokens
        self.bm25_index = BM25(self.chunks)
        self._reranker = None

    @property
    def reranker(self):
        if self._reranker is None:  # ~1.1 GB download on first use; only rerank configs pay for it
            from sentence_transformers import CrossEncoder
            self._reranker = CrossEncoder(RERANKER, revision=RERANKER_REVISION)
        return self._reranker

    def dense(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        return self.day6.dense(query, top_k, filters)

    def tfidf(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        # ponytail: scores all 1805 chunks then filters, ~ms; pre-filter the index if the corpus grows
        ranked = self.tfidf_index.search(query, top_k=len(self.chunks))
        return [c for c in ranked if matches(c, filters)][:top_k]

    def bm25(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        return [c for c in self.bm25_index.search(query) if matches(c, filters)][:top_k]

    def hybrid(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        return rrf([self.dense(query, self.POOL, filters), self.tfidf(query, self.POOL, filters)], top_k)

    def hybrid_bm25(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        return rrf([self.dense(query, self.POOL, filters), self.bm25(query, self.POOL, filters)], top_k)

    def rerank(self, query: str, candidates: list[dict], top_k: int, strategy: str) -> list[dict]:
        scores = self.reranker.predict([(query, c['text']) for c in candidates])
        ranked = sorted(zip(candidates, scores), key=lambda p: (-p[1], p[0]['id']))
        return [{**c, 'score': float(s), 'strategy': strategy} for c, s in ranked[:top_k]]

    def rerank_dense(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        return self.rerank(query, self.dense(query, self.POOL, filters), top_k, 'rerank_dense')

    def rerank_hybrid(self, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        # Fusion order is irrelevant here: the cross-encoder re-scores the whole candidate union.
        pool = rrf([self.dense(query, self.POOL, filters), self.bm25(query, self.POOL, filters)], 2 * self.POOL)
        return self.rerank(query, pool, top_k, 'rerank_hybrid')

    def search(self, method: str, query: str, top_k: int, filters: dict | None = None) -> list[dict]:
        if method not in self.METHODS:
            raise ValueError(f'unknown retrieval method {method!r}')
        return getattr(self, method)(query, top_k, filters)


if __name__ == '__main__':
    day6 = Day6()
    chunks = day6.all_chunks()
    top = day6.dense('What daily sodium limit does a healthy eating pattern set for adults?', 3)
    assert len(chunks) == day6.store.count(INDEX) and len(top) == 3 and top[0]['score'] >= top[-1]['score']
    assert all(k in top[0] for k in ('id', 'text', 'source_id', 'source', 'page', 'metadata', 'score'))
    for c in top:
        print(f"{c['score']:.4f} {c['id']} | {c['text'][:90]!r}")
    print(f"Day 6 OK: {len(chunks)} chunks in index {INDEX}, {day6.embedder.model_name} "
          f"{day6.embedder.dimensions} dims, DAY6_DIR={DAY6}")
