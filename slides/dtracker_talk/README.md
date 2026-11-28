# D-Tracker — slide seminar

Bộ Beamer 16:9 tiếng Việt (giữ thuật ngữ tiếng Anh) cho đồ án CS313. Thời lượng: **20 phút trình bày paper + 15 phút demo**.
Người nghe không cần theo được chứng minh. Mỗi khái niệm đi theo thứ tự: câu hỏi → trực giác/ví dụ → công thức tối thiểu → nói lại công thức bằng lời. Phần tối ưu nặng toán chỉ giữ ý tưởng ở main deck, công thức đầy đủ nằm ở Appendix.

## Sản phẩm

- `dtracker_talk.pdf`: 34 trang = 25 slide chính (gồm slide Demo để trống và slide Q&A) + 9 slide Appendix A1–A9.
- `outline.md`: mạch kể chuyện, bảng thời gian, nội dung và lời dẫn từng slide, cùng các điểm đã chỉnh so với outline ban đầu.
- `main.tex`: entry point; `theme.tex`: màu, font, hộp; `parts/`: nội dung.
- `dtracker_talk_overleaf.zip`: gói upload Overleaf (xem `OVERLEAF.md`).
- `sources/source_map.md`: đối chiếu slide → section / equation / figure / table của paper.
- `sources/figure_manifest.tsv`: nguồn, license, SHA-256 của các hình lấy từ paper.

## Cấu trúc

```text
parts/00_cover.tex        # slide 1
parts/01_problem.tex      # slide 2–5    Vấn đề
parts/02_model.tex        # slide 6–13   Mô hình
parts/03_estimation.tex   # slide 14–17  Tìm tham số (ý tưởng)
parts/04_experiments.tex  # slide 18–23  Thực nghiệm + takeaways
parts/05_demo_qa.tex      # slide 24–25  Demo (trống), Q&A
parts/99_appendix.tex     # slide A1–A9  Toán chi tiết, Table 3 đầy đủ
```

Mỗi frame có marker `% SLIDE n` khớp với heading `### Slide n` trong `outline.md`. Nếu thêm hoặc bớt slide, sửa cả hai chỗ rồi chạy `make check`.

## Build

```bash
cd slides/dtracker_talk
make all      # check + PDF + Overleaf ZIP
make check    # unit test checker + đồng bộ outline/deck/hình
make clean
```

Makefile ưu tiên `latexmk` + XeLaTeX nếu máy đã cài TeX Live. Nếu không có, Makefile dùng Tectonic (cần mạng để tải bundle lần đầu).
Deck dùng `fontspec` và `unicode-math`, nên phải compile bằng **XeLaTeX**, không dùng pdfLaTeX.

## Quy ước nội dung

- Mọi số liệu đều lấy từ paper (paper-reported), không phải kết quả nhóm chạy lại. Table 3 ở slide 19 và A9 đã được đối chiếu tự động với text paper.
- Ví dụ COVID, Black Friday, Tết và các chuỗi đồ chơi là minh họa của nhóm; trên slide đều có ghi chú.
- Hình lấy từ paper (CC BY 4.0) có ghi nguồn ở chân mỗi slide.
