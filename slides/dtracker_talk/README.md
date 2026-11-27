# D-Tracker final-project talk

Bộ Beamer 16:9 tiếng Việt cho đồ án Data Mining, thời lượng **32 phút 45 giây**, dành cho sinh viên chưa có nhiều nền tảng toán. Deck giữ phong cách academic-clean: nền sáng, Latin Modern Sans, header breadcrumb, logo nhỏ và footer ba phần.

Mỗi khái niệm được giải thích theo thứ tự:

> ví dụ/hình → nói bằng lời → công thức tối thiểu → kiểm tra bằng ví dụ số.

## Phạm vi hiện tại

Chỉ gồm **paper gốc + outline + slide**. Chưa cài đặt D-Tracker, chưa chạy reproduction và chưa soạn report 4 trang.

- Slide 1–7: Problem và big picture.
- Slide 8–18: Methodology qua ví dụ từ khóa × địa điểm × tuần.
- Slide 19–24: Experiments của paper.
- Slide 25–27: khung reproduction; `---` nghĩa là “Nhóm sẽ bổ sung sau khi chạy thực nghiệm”.
- Slide 28: Demo, cố ý trống phần nội dung.
- Slide 29: Takeaways/Q&A.
- Slide A1–A4: backup kỹ thuật, không tính vào thời lượng chính.

## Sản phẩm

- `dtracker_talk.pdf`: 33 trang = 29 slide chính + 4 backup, 16:9.
- `outline.md`: mục tiêu, timing, visual, công thức, nguồn và lời dẫn từng slide.
- `main.tex`: nội dung Beamer.
- `theme.tex`: màu sắc, font, frametitle, footline và panel.
- `dtracker_talk_overleaf.zip`: gói upload Overleaf.
- `sources/source_map.md`: claim ledger với page/section/equation/figure/table anchors.
- `sources/figure_manifest.tsv`: nguồn, caption, license và SHA-256 của bốn hình paper được dùng.

Paper gốc đã được đối chiếu byte-identical với arXiv và nằm tại:

```text
slides/paper_explore/sources/paper.pdf
```

ArXiv:2505.00242v1, KDD 2025, 12 trang; SHA-256 `8f3d301da12cbd17ec19cfcd6cb666654ded0fef06f57054826abf887ef9f715`.

## Build và kiểm tra

```bash
cd slides/dtracker_talk
make all          # PDF + Overleaf ZIP
make check        # unit test checker + outline/deck/hình
make overleaf-zip # chỉ tạo lại ZIP
make clean        # xóa build/, PDF và ZIP đã tạo
```

Makefile ưu tiên Tectonic trên `PATH`, sau đó binary tại `../paper_explore/.tools/tectonic`. Nếu cả hai không có, `make` tải Tectonic 0.15.0 vào `.tools/` cục bộ.

File ZIP chỉ chứa các thành phần cần trên Overleaf: `main.tex`, `theme.tex`, `latexmkrc`, `OVERLEAF.md` và `figures/`. Source map, paper gốc và các artifact kiểm chứng không được đưa vào ZIP.

## Ghi chú nội dung

- Các công thức chính là Eq. (1)–(4), Eq. (10), algorithm flow và một bước Euler minh họa.
- Không chứng minh ALS/MDL; mục tiêu là đọc và diễn giải được mô hình.
- Các số trong câu chuyện iPhone/Galaxy được gắn nhãn minh họa; không phải dữ liệu paper.
- Kết quả experiments đều gắn nhãn **paper-reported**. Phần trăm trên slide 21 được tính lại từ Table 3; không phải kết quả reproduce.
- Slide reproduction không dùng số paper để lấp kết quả nhóm. Demo chưa có implementation claim.
- Bốn hình paper có credit KDD 2025/CC BY 4.0 và được kiểm tra hash với manifest nguồn.
- Native executor chỉ kiểm tra log, cấu trúc và text bounds; visual review được ủy quyền cho DeepSeek với tối đa 4 ảnh/lượt.
