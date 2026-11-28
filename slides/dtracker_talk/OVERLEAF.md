# D-Tracker talk — Overleaf

## Cách dùng

1. Upload `dtracker_talk_overleaf.zip` lên Overleaf (New Project → Upload Project).
2. **Menu → Compiler** chọn **XeLaTeX**.
3. Main document: `main.tex`.
4. Bấm **Recompile**.

Kết quả mong đợi: **40 trang**, 16:9.

## Cấu trúc ZIP

```text
main.tex      # Beamer 16:9, entry point
theme.tex     # màu, font, hộp, footer
parts/        # nội dung từng phần
figures/      # hình lấy từ paper + nền vân lục giác + logo UIT
fonts/        # Be Vietnam Pro (.ttf), được nạp bằng đường dẫn tương đối
latexmkrc     # chọn XeLaTeX khi chạy latexmk
OVERLEAF.md   # hướng dẫn này
```

## Chỉnh nội dung

- Slide 1 (cover) và S0 (Nội dung) ở `00_cover`; 2–5 ở `01_problem`; 6–13 ở `02_model`; 14–17 ở `03_estimation`; 18–23 ở `04_experiments`; 24–25 ở `05_demo_qa`; A1–A9 ở `99_appendix`.
- Slide 24 (Demo) là slide chia chương “05 Demo”, cố ý không có nội dung.
- Font Be Vietnam Pro nằm trong `fonts/`, nên không cần cài thêm font trên Overleaf; chỉ cần compiler là XeLaTeX.
- Dòng “Nguồn: …” ở chân slide do macro `\papersource{}` vẽ ở vị trí cố định, nên không chiếm chỗ của nội dung. Nếu nội dung quá dài, nó sẽ đè lên dòng nguồn; khi đó hãy cắt bớt chữ, đừng dùng `shrink`.
- Nếu Overleaf báo thiếu font: kiểm tra lại compiler đã là XeLaTeX chưa.
