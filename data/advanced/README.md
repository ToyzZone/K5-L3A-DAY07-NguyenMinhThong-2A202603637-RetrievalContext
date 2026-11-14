# Dữ liệu thử thách nâng cao

**Tài liệu:** WHO, *Global status report on physical activity 2022*. Geneva: World Health Organization; 2022. ISBN 978-92-4-005915-3 (electronic). 132 trang PDF (A4), Adobe InDesign 18, tạo ngày 2022-11-24.

- Trang gốc: <https://iris.who.int/handle/10665/363607>
- File PDF (tải ngày 2026-11-14): <https://iris.who.int/server/api/core/bitstreams/8804f1b0-dbae-4e58-a251-36fd14dc7e02/content>
- SHA-256: `dfc7b117bdcf4328706c5437711c2382ef575d159183ae9e99d3d8c8ef15fc1c`
- Giấy phép: CC BY-NC-SA 3.0 IGO (ghi trong tài liệu). Dùng cho mục đích học tập phi thương mại, có ghi nguồn. PDF và ảnh trang không đưa vào git; tải lại bằng link trên.
- Số trang: trang in = trang vật lý − 16 trong phần thân. Benchmark ghi cả hai.

## Tái tạo

```bash
mkdir -p data/advanced/pdf data/advanced/pages
curl -sSL -o data/advanced/pdf/who-gsr-pa-2022.pdf "https://iris.who.int/server/api/core/bitstreams/8804f1b0-dbae-4e58-a251-36fd14dc7e02/content"
shasum -a 256 data/advanced/pdf/who-gsr-pa-2022.pdf          # phải khớp SHA-256 ở trên
pdftoppm -r 110 -png data/advanced/pdf/who-gsr-pa-2022.pdf data/advanced/pages/p   # poppler
"$PY" src/advanced.py extract   # dùng cache data/advanced/extracted/ nếu có, không gọi lại API
"$PY" src/advanced.py index
"$PY" src/advanced.py verify
```

## Pipeline và kiểm chứng trích xuất

- **Text:** text layer của PDF (`pdftotext`), chuẩn hóa và chia đoạn như index B của Day 6 (≤ 800 ký tự).
- **Bảng, biểu đồ, infographic, sơ đồ, box:** `gpt-5.4` đọc ảnh trang (110 dpi) cùng hai dải lề trái/phải xoay 90° để đọc nhãn "FIGURE N" in dọc. Mỗi phần tử thành chunk riêng (bảng dài tách theo hàng, ≤ 1500 ký tự, lặp lại tiêu đề). Ảnh chụp trang trí không được index.
- **Index:** `GSRT` = chỉ text layer (457 chunk, đối chứng); `GSR` = text + phần tử trực quan (596 chunk); `GSRC` = GSR, thêm nhãn cho phần tử không có nhãn (600 chunk, bản dùng). Trong GSRC, bảng hoặc hình nối từ trang trước kế thừa nhãn của nó ("TABLE 2 (continued …)"), phần tử khác lấy chữ đầu trang làm tiêu đề. Cùng embedding `bge-small-en-v1.5` và bảng pgvector của Day 6.
- **Trang không có chunk:** 2, 55, 113, 130, 131, đều là trang trắng hoặc chỉ có header. Không có trang nội dung nào bị bỏ.

Các lần thử và lỗi đã tìm thấy khi đối chiếu với ảnh gốc:

1. **v1** (`gpt-5.4-mini`, gửi kèm text layer): model **bịa biểu đồ** từ câu "see Fig. 5" trên trang chỉ có chữ (p26 sinh ra "Fig. 5"/"Fig. 6" kèm số liệu), và lặp hình ở trang dẫn chiếu (p60, p73, p94).
2. **v2** (mini, chỉ ảnh): hết bịa nhưng **đọc sai nhãn in dọc** (p47 "FIGURE 14" → "Figure 1", p49 → "Figure 5") và sót một số phần tử.
3. **v3** (bản dùng: `gpt-5.4`, ảnh + dải lề xoay): đủ Figure 1–36, mỗi số đúng một trang (p18 … p95), Table 1 (p12), Table 2 (p34–36), Table 1 chương 9 (p108, bản gốc in "TABLE 1"). Trang chỉ có chữ (p26) không còn phần tử bịa. Một sửa tay: p30 có nhãn "FIGURE 14" không in trên trang (đã xem dải lề) → đặt `label: null`, ghi trong `manual_correction` của `extracted/p-030.json`.
4. Đối chiếu giá trị: Fig. 5/6 (p27) khớp ảnh; Fig. 6 không in nhãn số nên giá trị ghi `~` (ước lượng từ trục, ví dụ tăng huyết áp ~44% số ca, trong khi đoạn văn p26 ghi 47%: chênh lệch có sẵn trong bản gốc).

Chi phí trích xuất v3: $1.23 (giá gpt-5.4 $2.50/$15 cho 1M token vào/ra). v1, v2 tốn thêm $0.43 + $0.38 và không được dùng.

| Thư mục / file | Nội dung |
|---|---|
| `extracted/p-NNN.json` | Kết quả model vision cho từng trang: mỗi bảng, biểu đồ, bản đồ, infographic, sơ đồ, box có `type`, `label`, `title`, `location`, `content` (bảng Markdown, điểm dữ liệu biểu đồ; `~` = ước lượng từ trục). Có commit để không phải trả phí chạy lại. |
| `questions.json` | Benchmark dev/test, chia trước mọi thí nghiệm. Mỗi câu: nhóm chính, đáp án, evidence theo trang vật lý + trang in + phần tử (Fig./Table/Box) + vị trí + giá trị; câu thiếu evidence có regex kiểm tra trên cả 132 trang. |
| `pdf/`, `pages/` | PDF gốc và ảnh trang 110 dpi (không commit). |
