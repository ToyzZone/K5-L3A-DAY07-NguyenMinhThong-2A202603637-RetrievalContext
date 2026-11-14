# Code Day 7

Agentic RAG trên index Day 6 ([repo Day 6](https://github.com/ToyzZone/K5-L3A-DAY06-NguyenMinhThong-2A202603637-DataIngestion)).

| File | Nội dung |
|---|---|
| `retrieval.py` | Kết nối embedder + pgvector Day 6 (index `B`); các phương pháp `dense`, `tfidf`, `bm25`, `hybrid` (RRF dense+TF-IDF), `hybrid_bm25` (RRF dense+BM25), `rerank_dense`, `rerank_hybrid` (cross-encoder `BAAI/bge-reranker-base`, pin revision) |
| `agent.py` | Controller gọi OpenAI Chat Completions với 2 tool `search_documents` / `answer`; vòng lặp dùng `starter/agentic.py` (`run_agent`) |
| `run.py` | Cấu hình thí nghiệm, chạy retrieval/agent, lưu trace + summary, xuất bảng chấm tay |
| `bench.py` | Tạo `data/questions.json` từ benchmark Day 6 + `data/unanswerable.json`; định nghĩa hit; kiểm chứng benchmark |

## Chuẩn bị

1. Clone repo Day 6 cạnh repo này (mặc định `../../lab 6/starter`, hoặc đặt `DAY6_DIR=<đường-dẫn>/starter`), làm theo README Day 6: tạo `.venv`, `pip install -r requirements.txt`, `docker compose -p day6_student_starter up -d --wait`, `python -m src.run dev` để nạp index `A`/`B`.
2. Chạy mọi lệnh Day 7 bằng **Python của venv Day 6** (cùng model embedding, cùng version thư viện):
   `PY="<day6>/starter/.venv/bin/python"`
3. `cp .env.example .env` rồi điền `OPENAI_API_KEY` (model mặc định `gpt-5.4-mini`).

## Lệnh

Chạy từ thư mục gốc repo:

```bash
"$PY" -m unittest discover -s tests -v          # test offline (mock), không đo chất lượng
"$PY" src/bench.py verify                        # kiểm chứng benchmark
"$PY" src/run.py retrieval dev                   # Hit@1 / Evidence Hit@3 mọi phương pháp, không gọi LLM
"$PY" src/run.py agent dev <config>              # agent thật; configs trong run.py: CONFIGS
"$PY" src/run.py sheet dev <config>              # bảng chấm tay + reviews.json mẫu (không ghi đè)
"$PY" starter/agent_metrics.py --cases data/questions.json --traces results/dev/agent-<config>/traces.json \
  --reviews results/dev/agent-<config>/reviews.json --split dev --output results/dev/agent-<config>/agent_metrics.json
```

Test chỉ chạy một lần sau khi chốt cấu hình: `retrieval test dense hybrid_bm25`, `agent test dense`, `agent test hybrid-bm25`.

Kết quả nằm trong `results/<split>/`: `retrieval.json`, `agent-<config>/{traces,summary,reviews,agent_metrics}.json`, `review_sheet.md`.
