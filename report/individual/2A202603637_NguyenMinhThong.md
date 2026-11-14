# Báo cáo Day 7 — Agentic RAG

Nguyễn Minh Thông · 2A202603637 · Code: [src/](../../src/README.md) · Benchmark: [data/questions.json](../../data/questions.json)

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:** dùng lại corpus Day 6 ([repo Day 6](https://github.com/ToyzZone/K5-L3A-DAY06-NguyenMinhThong-2A202603637-DataIngestion), `starter/data/sources.json`): FM 7-22 Holistic Health and Fitness (US Army, 2020, "approved for public release"), Physical Activity Guidelines for Americans 2nd ed. (HHS, 2018, tác phẩm liên bang Mỹ), WHO guidelines on physical activity and sedentary behaviour (2020, CC BY-NC-SA 3.0 IGO). 466 trang PDF, 342 trang nội dung được index. Index `B` của Day 6 (chunk theo đoạn, ≤ 800 ký tự): **1805 chunk**. Mọi phương pháp Day 7 đọc cùng bảng `chunks` (strategy `B`), nên dense và lexical dùng đúng một phiên bản corpus.
- **Vector store, embedding model, phiên bản và số chiều:** PostgreSQL 16.16 + pgvector 0.8.7 (Docker local, cosine, quét tuần tự, không ANN). Embedding `BAAI/bge-small-en-v1.5` revision `5c38ec7c…`, **384 chiều**, vector chuẩn hóa, query có prefix theo model card. Kết nối: [src/retrieval.py](../../src/retrieval.py) import thẳng `src.embeddings` và `src.store` của Day 6 qua `DAY6_DIR`, chạy bằng venv Day 6 (sentence-transformers 5.7.0, torch 2.15.0, psycopg 3.3.8). Kiểm chứng: dense Day 7 cho đúng Hit@1 16/22, Hit@3 21/22 như cấu hình C của Day 6. Reranker (I2): `BAAI/bge-reranker-base` revision `2cfc18c9…`, chạy local.
- **Agent model, cách chạy và phân chia dev/test:** `gpt-5.4-mini` (snapshot `gpt-5.4-mini-2026-03-17`) qua OpenAI Chat Completions, tool calling. Lệnh chạy: [src/README.md](../../src/README.md). Benchmark 36 câu: **dev 22 có đáp án + 3 thiếu evidence; test 8 có đáp án + 3 thiếu evidence**. 30 câu có đáp án lấy từ benchmark Day 6 (gộp `gold` + `alt_gold`), giữ nguyên split. Test Day 6 chỉ chạy một lần sau khi chốt Day 6 và không dùng để chỉnh Day 6 hay Day 7. 6 câu thiếu evidence được viết mới trước mọi thí nghiệm Day 7 ([data/unanswerable.json](../../data/unanswerable.json)).
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:**
  - Câu có đáp án: hit khi chunk thuộc đúng (nguồn, trang) của gold và chứa trọn câu evidence (phân biệt hoa thường, sau khi gộp khoảng trắng), cùng định nghĩa với Day 6 ([src/bench.py](../../src/bench.py)). `python src/bench.py verify` kiểm tra evidence của mọi câu nằm trọn trong một chunk đã index.
  - Câu thiếu evidence: chọn gần chủ đề (COVID-19, đái tháo đường type 1, thang điểm ACFT, trẻ 2 tuổi, omega-3, creatine). Mỗi câu có regex `absence_check` chạy trên **toàn bộ 466 trang** (kể cả trang không index), chỉ được khớp các trang đã ghi trong `allowed_pages` kèm lý do (ví dụ HHS p83 nói type 1 "was not addressed"). Không kết luận thiếu evidence dựa trên top-k.
  - Gold không bao giờ đi vào agent hay retriever. Filter (7 câu) là phạm vi người hỏi nêu trong câu hỏi (chương hoặc tổ chức), áp cho mọi phương pháp như nhau.

### Tiêu chí chọn cấu hình (chốt 2026-11-14, sau baseline dev, trước mọi cấu hình cải thiện và trước khi chạy test)

Chọn trên **dev**, theo thứ tự ưu tiên:

1. Context Evidence Rate cao hơn.
2. Grounded answer trung bình (nhãn tay 0/1/2) cao hơn.
3. Abstention: phải từ chối đủ 3/3 câu thiếu evidence; ít câu có đáp án bị từ chối nhầm hơn.
4. Nếu vẫn bằng: chi phí và thời gian thấp hơn.

Baseline là `dense` (tương đương cấu hình C của Day 6: index B, filter theo phạm vi nêu trong câu hỏi). Test chỉ chạy một lần cho baseline và cấu hình đã chọn.

**Quyết định (chốt trước khi chạy test):** chọn `hybrid-bm25`. Trên dev, `hybrid-bm25` và `rerank-dense` hòa ở tiêu chí 1–3 (Context Evidence Rate 22/22, grounded 2.0, abstention 3/3, từ chối nhầm 0/22); tiêu chí 4 chọn `hybrid-bm25` ($0.0433 / 61.6 s so với $0.0450 / 94.1 s cho 25 câu).

## Retrieval và thử nghiệm

Chung cho mọi cấu hình agent: top-k 3 mỗi lần search, tối đa 3 lần search, context budget **3000 ký tự** (đếm cả header `[id | nguồn | trang]`; chunk ≤ 800 ký tự nên khoảng 3 chunk), filter theo câu hỏi. Hit@1 / Evidence Hit@3 tính trên **câu hỏi gốc**, không qua LLM ([results/dev/retrieval.json](../../results/dev/retrieval.json)). Context Evidence Rate tính trên context cuối agent gửi model, sau khi model tự viết lại query. Thời gian retrieval là trung vị mỗi query; thời gian agent là tổng cho cả split; chi phí theo giá gpt-5.4-mini ($0.75 / $4.50 cho mỗi 1M token input / output, không trừ cached input nên là cận trên). Retrieval không tốn phí (model local).

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| **Baseline** `dense` | Dense pgvector Day 6, k=3, filter, budget 3000 | Day 6 C | dev | 16/22 (72.7%) | 21/22 (95.5%) | 21/22 (95.5%) | 46 ms · agent 60.3 s, $0.0439 |
| Phương pháp 2 `tfidf` | TF-IDF (starter `TfidfIndex`), k=3, filter | Lexical | dev | 11/22 (50.0%) | 14/22 (63.6%) | 15/22 (68.2%) | 5 ms · agent 63.7 s, $0.0489 |
| Phương pháp 3 `hybrid` | RRF (k=60) dense top-20 + TF-IDF top-20, k=3 | Kết hợp ngữ nghĩa và từ khóa | dev | 13/22 (59.1%) | 20/22 (90.9%) | 20/22 (90.9%) | 40 ms · agent 58.7 s, $0.0457 |
| `bm25` (chỉ retrieval) | Okapi BM25 (k1 1.5, b 0.75), k=3 | Bước kiểm tra cho I3 | dev | 15/22 (68.2%) | 19/22 (86.4%) | không chạy agent | 5 ms |
| Cải thiện 1 `dense-orig` | Dense; lần search đầu = nguyên câu hỏi, sau đó model mới viết lại | Sửa q02 (rewrite làm mất gold) | dev | = dense | = dense | 21/22 (95.5%) | agent 45.1 s, $0.0298 |
| Cải thiện 1b `dense-orig-b6000` | Như I1, budget 6000 | Cho chunk của lần search sau còn chỗ | dev | = dense | = dense | 21/22 (95.5%) | agent 33.7 s, $0.0305 |
| **Cải thiện 2** `hybrid-bm25` (phương pháp mới) | RRF dense top-20 + BM25 top-20, k=3 | TF-IDF kéo hybrid xuống; BM25 bão hòa tf và chuẩn hóa độ dài | dev | 14/22 (63.6%) | **22/22 (100%)** | **22/22 (100%)** | 41 ms · agent 61.6 s, $0.0433 |
| Cải thiện 3 `rerank-dense` (phương pháp mới) | Dense top-20 → cross-encoder bge-reranker-base → k=3 | Hit@1 16/22: xếp lại bằng cross-encoder | dev | **20/22 (90.9%)** | **22/22 (100%)** | **22/22 (100%)** | 649 ms · agent 94.1 s, $0.0450 |
| `rerank_hybrid` (chỉ retrieval) | (dense + BM25) top-40 → cross-encoder → k=3 | Rerank trên tập ứng viên rộng hơn | dev | 20/22 (90.9%) | 22/22 (100%) | không chạy agent | 1042 ms |
| **Cấu hình đã chọn** `hybrid-bm25` | như trên | chốt trên dev | test | 6/8 (75.0%) | 7/8 (87.5%) | 7/8 (87.5%) | 39 ms · agent 31.2 s, $0.0248 |
| Baseline `dense` | như trên | | test | 4/8 (50.0%) | 7/8 (87.5%) | 7/8 (87.5%) | 39 ms · agent 32.7 s, $0.0242 |

`hybrid-bm25` và `rerank-dense` vừa là phương pháp retrieval mới vừa là cấu hình cải thiện, mỗi cấu hình có giả thuyết và kết quả riêng. `rerank_hybrid` cho Hit@1/Hit@3 bằng `rerank-dense` nhưng chậm hơn 60% nên không chạy agent.

**Lỗi dev, nguyên nhân, cách thử:**

1. **q02: model viết lại query làm mất evidence.** Với câu hỏi gốc, dense xếp chunk gold (FM p32 "The 10-week H2F program for BCT…") ở rank 2. Agent lại search `"Basic Combat Training H2F program length FM 7-22"`, mất p32 và trả lời từ p23 ("10-week block of basic combat training"): đúng số nhưng nguồn chỉ hỗ trợ một phần. Thử I1 (search câu hỏi gốc trước): q02 được sửa, nhưng **q03 hỏng**. Câu hỏi gốc của q03 trượt top-3, model hài lòng với context sau một lần search và trả lời "The glycolytic pathway … up to 90 seconds" kèm citation p44 hợp lệ. Đây là ví dụ citation ID hợp lệ, chunk đúng nội dung nó nói, nhưng câu trả lời sai câu hỏi (hỏi phosphagen 5–10 s). Context Evidence Rate giữ 21/22; I1 giảm một nửa số lượt gọi LLM ($0.0439 → $0.0298) nhưng không tăng chất lượng nên không chọn. Phần budget 6000 (I1b) không được kiểm chứng thực sự: agent không search lần hai ở câu có đáp án nào.
2. **TF-IDF kéo hybrid xuống dưới dense.** TF-IDF trượt 8 câu (q01, q02, q08, q10, q22, q23, q24, q26), nên RRF trọng số đều cho Hit@1 13 < dense 16. Với context không có evidence, agent từ chối 4/22 câu (hành vi đúng: không bịa). Thử I3 (BM25): BM25 đơn lẻ lên 15/19, hybrid-bm25 đạt Hit@3 22/22 và Context Evidence Rate 22/22. Giả thuyết đúng về recall; Hit@1 vẫn thấp hơn dense trên dev (14 so với 16) nhưng cao hơn trên test (6/8 so với 4/8).
3. **Thứ hạng dense (Hit@1 16/22)** → I2 cross-encoder: Hit@1 20/22, Context Evidence Rate 22/22, đổi lại khoảng +0.6 s mỗi lần search (tổng 94 s so với 60 s).
4. **Search lặp:** u01 (dense) gọi 3 lần cùng một query y hệt; q29 (test) cũng lặp gần như y hệt. Chưa sửa (xem giới hạn).

**Lý do chọn:** áp đúng tiêu chí đã chốt; dev bão hòa ở tiêu chí 1–3 nên quyết định nằm ở chi phí và thời gian.

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:**
  - **Tool:** 2 tool `search_documents(query)` và `answer(answer, citations)`, `tool_choice=required`, không gọi song song ([src/agent.py](../../src/agent.py)). Mỗi bước là một lần gọi model không trạng thái, đầu vào gồm câu hỏi, các query đã chạy, số lượt còn lại và context tích lũy mới nhất.
  - **Vòng lặp:** dùng `run_agent` của starter. Dừng khi model gọi `answer`, hoặc khi hết 3 lần search (→ từ chối).
  - **Kiểm tra câu trả lời:** chỉ chấp nhận nếu mọi citation có trong context **và** xuất hiện inline dạng `[id]`; nếu không thì chuyển thành từ chối.
  - **Context:** `pack_context` loại chunk trùng ID, giữ thứ tự (chunk của lần search trước được ưu tiên) và bỏ chunk không vừa budget 3000 ký tự. Context chỉ được coi là dữ liệu, không phải chỉ dẫn.
  - **Xử lý lỗi:** lỗi HTTP/provider được ghi `status: error` với nguyên nhân, không thay bằng câu trả lời giả. Số lỗi trong mọi lần chạy: 0.
  - **Số lượt gọi:** phân bố số lần search trên test là {1: 7, 3: 4} cho cả hai cấu hình (câu thiếu evidence luôn dùng hết 3 lượt).

Nhãn tay chỉ cần cho các cấu hình hòa ở tiêu chí 1 (dev) và cho test; các cấu hình dev khác chỉ có số liệu tự động.

| Cấu hình / split | Tool use | Số lượt gọi LLM | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| hybrid-bm25 / dev | 25/25 | 54 | 0 / 0 / 22 · 2.00 | 27/27 | 22/22 | 3/3 | 0/22 |
| rerank-dense / dev | 25/25 | 56 | 0 / 0 / 22 · 2.00 | 23/23 | 22/22 | 3/3 | 0/22 |
| dense (baseline) / test | 11/11 | 30 | 1 / 0 / 7 · 1.75 | 7/8 | 8/8 | 3/3 | 0/8 (*) |
| hybrid-bm25 (chọn) / test | 11/11 | 30 | 1 / 0 / 7 · 1.75 | 9/10 | 8/8 | 3/3 | 0/8 (*) |

(*) q29 về thực chất là từ chối ("the document does not state…") nhưng kèm citation nên `run_agent` ghi `answered`; chấm grounded 0.

**Chấm context trên test** (8 câu có đáp án, cả hai cấu hình; 0 = không có evidence, 1 = có nhưng thiếu điều kiện/nguồn, 2 = đủ): 0: 1 câu (q29), 1: 0 câu, 2: 7 câu.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| q16 (test, hybrid-bm25) | Có đáp án | 1 search `"training period longest how long can it last FM 7-22 phased training period weeks"` → p57 (gold), p53, p54 | "The base period is the longest, lasting up to twelve weeks [fm7-22-2020:p057:para:01]." | Grounded 2, citation đúng, context 2: p57 nêu nguyên văn. |
| u05 (test, hybrid-bm25) | Thiếu evidence | 3 search về "omega-3 … milligrams per day" → các chunk dinh dưỡng FM p74–p90, không có omega-3 | Model gọi `answer("Not enough evidence in the documents.", [])` → từ chối | Từ chối đúng, không bịa liều; regex `omega` = 0 trang. |
| q29 (test, cả hai) | Có đáp án (lỗi) | 3 search gần như trùng nhau → p136, p139, p140:para:00, p143; chunk gold (p140 "Entry into Category 1 is directed by the healthcare provider during the Soldier's initial visit") không xuất hiện ở lần nào | "A physical therapist … may oversee … Category 1 [p139]. The document does not state who directs a Soldier's entry … [p139]" | Grounded 0, citation sai (chỉ hỗ trợ câu lạc đề), context 0. Lỗi retrieval + query rewrite không đa dạng. |
| q03 (dev, dense-orig) | Có đáp án (lỗi) | 1 search = câu hỏi gốc → không có chunk phosphagen | "The glycolytic pathway … up to 90 seconds [p044]" | Citation ID hợp lệ nhưng câu trả lời sai câu hỏi (cần phosphagen, 5–10 s). |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:**
  - Trace: `results/<split>/agent-<config>/traces.json` (mỗi tool call, query, kết quả kèm score, context từng bước, context cuối, câu trả lời, citation, token, thời gian, lỗi).
  - Tổng hợp tự động: `summary.json`. Nhãn tay: `reviews.json` (dev: hybrid-bm25, rerank-dense; test: dense, hybrid-bm25). Tổng hợp nhãn: `agent_metrics.json`. Bảng chấm: `review_sheet.md`.
  - Retrieval: `results/<split>/retrieval.json`. Lệnh chạy: [src/README.md](../../src/README.md).
  - Tổng chi phí agent cho 9 lần chạy đã lưu: **$0.336**, cộng vài lần chạy thử 2 câu không lưu (ước dưới $0.01). Mỗi câu khoảng 2–3 lượt gọi, khoảng 730–1000 token prompt mỗi lượt (I1 bỏ lượt gọi đầu nên trung bình mỗi lượt cao hơn).
- **Kết quả trước/sau, đánh đổi và giới hạn:**
  - **Trước/sau trên test:** hybrid-bm25 cải thiện thứ hạng (Hit@1 4/8 → 6/8) nhưng Context Evidence Rate, grounded answer và abstention bằng baseline. Lợi ích chủ yếu ở bước retrieval; agent bù được thứ hạng kém nhờ đọc cả top-3. Rerank cho Hit@1 tốt nhất trên dev nhưng tốn thêm khoảng 0.6 s mỗi lần search; với top-3 trong context thì phần lợi này không đổi thành chất lượng câu trả lời trên dev.
  - **Dev bão hòa:** hai cấu hình tốt nhất đạt 22/22 và 2.0, nên việc chọn thực chất dựa trên chi phí. Test chỉ có 8 câu có đáp án: chênh 1 câu là 12.5 điểm phần trăm, không đủ để kết luận có ý nghĩa thống kê.
  - **Query rewrite mang kiến thức sẵn có của model vào retrieval** (q03: model tự thêm "phosphagen ATP-PCr"). Không phải rò rỉ gold, nhưng phần thành công không hoàn toàn đến từ corpus.
  - **`run_agent` chỉ xét citation ID:** câu kiểu "tài liệu không nêu …" kèm citation (q29) được tính là `answered`, nên chỉ số từ chối nhầm theo status đánh giá thấp vấn đề. Cần chấm tay.
  - **Search lặp và budget:** query lặp y hệt (u01, q29) và `pack_context` ưu tiên chunk cũ, nên chunk mới của lần search thứ 2–3 thường không vào context (q29: các chunk mới bị bỏ vì hết budget). Hướng sửa: báo model query đã chạy và chặn query trùng, hoặc chọn context theo score thay vì theo thứ tự.
  - **Định nghĩa hit chặt:** phải chứa trọn câu evidence trên đúng trang. Một số câu trả lời đúng từ trang khác chỉ được ghi nhận qua `alt_gold` đã liệt kê sẵn (ví dụ q02 dùng p23 chỉ hỗ trợ một phần).
  - **Nhãn tay:** do Claude Code soạn nháp, người học đọc đối chiếu từng câu và duyệt. Nhãn không độc lập hoàn toàn với AI.
  - Chi phí là cận trên (không trừ cached input). Thời gian đo trên máy cá nhân (macOS, model local) và phụ thuộc mạng tới OpenAI.

## Thử thách nâng cao (nếu thực hiện)

**Kết quả: test 29/30 (96,7%) ≥ 90%.** Nhãn pass/fail từng câu đối chiếu với ảnh trang gốc, nằm trong `results/advanced/test/agent-mm-ctx-img-v2-g54-k6/reviews.json` và `score.json`.

### Tài liệu và trích xuất

- WHO, *Global status report on physical activity 2022*: 132 trang PDF, CC BY-NC-SA 3.0 IGO. Nguồn, SHA-256 và lệnh tải lại ghi trong `data/advanced/README.md`; PDF và ảnh trang không commit.
- Nội dung trực quan được index: 33 biểu đồ, 8 bảng (Table 1, Table 2, các bảng phụ lục), 45 infographic, 25 box, 4 sơ đồ. 4 ảnh chụp trang trí bị bỏ.
- **Text:** text layer (`pdftotext`), chia đoạn như index B của Day 6.
- **Visual:** `gpt-5.4` đọc ảnh từng trang (110 dpi) kèm hai dải lề xoay 90°, để đọc được nhãn "FIGURE N" in dọc. Mỗi phần tử thành một chunk; bảng dài tách theo hàng và lặp lại tiêu đề. Chi phí $1,23.
- **Kiểm chứng trích xuất** (so với ảnh gốc), qua 3 phiên bản:
  - v1 (mini, gửi kèm text): bịa biểu đồ từ câu "see Fig. 5".
  - v2 (mini, chỉ ảnh): đọc sai nhãn in dọc.
  - v3 (bản dùng): đủ Fig. 1–36, mỗi hình đúng một trang. Sửa tay một nhãn bịa ở p30.

### Benchmark (`data/advanced/questions.json`, chia dev/test trước mọi thí nghiệm)

| Split | table | image | chart | multihop | text | unanswerable | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|
| test | 6 | 5 | 5 | 4 | 4 | 6 | 30 |
| dev | 3 | 3 | 3 | 3 | 3 | 3 | 18 |

- **Câu có đáp án:** evidence gồm trang vật lý, trang in, phần tử (Fig./Table/Box), vị trí và giá trị. Câu multihop có ≥ 2 evidence.
- **Câu không có đáp án:** có regex kiểm tra trên cả 132 trang. `advanced.py verify` xác nhận regex chỉ khớp ở những trang đã giải thích lý do.

### Thử nghiệm trên dev và lựa chọn

Mọi cấu hình dùng hybrid RRF dense+BM25 (phương pháp đã chọn ở Day 7) và tối đa 4 lần search.

Tiêu chí, chốt trước khi chạy test:
1. Số câu dev đạt. Đạt = đúng mọi ý của đáp án và không có ý sai; từ chối ở câu không có đáp án cũng tính là đạt.
2. Nếu hòa: context evidence, tức mọi trang evidence đều có trong context cuối.
3. Nếu vẫn hòa: chi phí thấp hơn.

Nhãn dev do Claude chấm theo `expected_answer`, chỉ dùng để chọn cấu hình (`results/advanced/dev/selection.json`).

| Cấu hình | Thay đổi so với dòng trên | Dev đạt | Context evidence | Chi phí | Median |
|---|---|---:|---:|---:|---:|
| text-only | index GSRT: chỉ text layer, mini | 10/18 | 12/15 | $0,067 | 3,3 s |
| mm | + chunk visual (GSR) | 14/18 | 11/15 | $0,052 | 2,1 s |
| mm-img | + gửi ảnh trang của chunk visual | 14/18 | 11/15 | $0,080 | 2,4 s |
| mm-ctx | GSR + nhãn nối trang (GSRC), không ảnh | 15/18 | 14/15 | $0,055 | 3,1 s |
| mm-ctx-img | GSRC + ảnh | 16/18 | 13/15 | $0,097 | 2,7 s |
| mm-ctx-img-v2 | + quy tắc search trong prompt | 15/18 | 15/15 | $0,098 | 3,2 s |
| mm-ctx-img-v2-g54 | + model `gpt-5.4` | 16/18 | 14/15 | $0,357 | 4,7 s |
| **mm-ctx-img-v2-g54-k6** | + top_k 6, budget 12000 | **18/18** | **15/15** | $0,404 | 4,3 s |

Mỗi bước sửa một nhóm lỗi tìm thấy khi đọc trace dev:

- **Visual chunk (mm):** chart, bảng và sơ đồ không có trong text layer nên text-only sai cả 3 câu chart.
- **GSRC (`add_context`):** Table 2 kéo dài p34–36 và Fig. 8 kéo dài p32–33, nhưng nhãn chỉ in ở trang đầu. Vì vậy phần nối trang được kế thừa nhãn ("TABLE 2 (continued …)"). Bảng không có nhãn (Annex 2, p128) được thêm chữ đầu trang làm tiêu đề.
- **v2:** model gửi lại đúng một query 4 lần (a-d10), hoặc kết luận "không có" sau khi chỉ thấy một phần bảng (a-d02). Prompt thêm hai quy tắc: không lặp query, và tìm đủ các phần của bảng trước khi kết luận.
- **g54:** mini đếm sai ("10 … 4.5, and 4.5") và tự sửa giữa câu trả lời, trong khi bằng chứng đã nằm trong context.
- **k6:** Table 2 có 6 chunk, nên câu hỏi về cả bảng cần top_k 6.

Chọn **mm-ctx-img-v2-g54-k6**. Lưu ý: dev đã dùng cho 5 vòng phân tích lỗi và đạt 18/18, tức đã bão hòa. Cùng một cấu hình chạy lại cũng lệch 1–2 câu, nên chỉ test là ước lượng không thiên lệch.

### Kết quả test (chạy 1 lần, cấu hình đã khóa)

| Nhóm | table | image | chart | multihop | text | unanswerable | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|
| Đạt | 6/6 | 4/5 | 5/5 | 4/4 | 4/4 | 6/6 | **29/30** |
| Context evidence | 5/6 | 5/5 | 5/5 | 4/4 | 4/4 | – | 23/24 |

- **Chi phí và tốc độ:** $0,71 cho 30 câu (77 lần gọi `gpt-5.4`, 93 ảnh trang), median 4,2 s/câu. 22/30 câu chỉ cần 1 lần search.
- **Câu trượt, a-t09:** model trả lời "OLDER ADULTS", nhưng ảnh trang 19 ghi "EVERYONE WHO CAN" dưới panel "More is better". Gốc lỗi là bản trích xuất p19 xếp nhãn nhóm lệch một cột. Ảnh trang có được gửi kèm, nhưng model vẫn theo bản trích xuất. Lỗi này chỉ lộ ra ở test; mình không sửa rồi chạy lại để giữ test sạch.
- **Câu đạt nhưng ghi chú, a-t06:** Table 1 không có trong context. Số liệu (46%, 30%, chênh 16, cả hai tăng) đều đúng theo Table 1, nhưng ý "all age groups tăng" chỉ dựa trên một câu chung ở p47.
- **Câu đạt nhưng ghi chú, a-t28:** câu không có đáp án. Model từ chối đúng và dẫn trang 112 ("unable to present any data on … budget allocations"). Starter vẫn tính là `answered` vì câu trả lời có citation, cùng hiện tượng với q29 ở phần cơ bản.

### Giới hạn

- **Lỗi trích xuất còn sót:** chỉ kiểm tra được những trang có câu hỏi. Lỗi ở p19 cho thấy các trang chưa được hỏi có thể còn lỗi tương tự.
- **Giá trị đọc từ trục biểu đồ** mang dấu `~`, nên câu hỏi chỉ hỏi cao nhất, thấp nhất hoặc so sánh, không hỏi giá trị chính xác.
- **Nhãn:** Claude soạn nháp, người học duyệt từng câu dựa trên ảnh trang. Như phần cơ bản, nhãn không độc lập hoàn toàn với AI.
- **Mẫu nhỏ:** test chỉ có 30 câu, nên 1 câu tương đương 3,3 điểm %. Chi phí trả lời bằng `gpt-5.4` gấp khoảng 4 lần mini.
