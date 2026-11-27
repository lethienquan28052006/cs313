# D-Tracker overview talk — Overleaf

## Cách dùng

1. Upload file `dtracker_talk_overleaf.zip` lên Overleaf.
2. Mở **Menu → Compiler** và chọn **XeLaTeX**.
3. Main document: `main.tex`.
4. Bấm **Recompile**.

Không cần shell-escape, không cần cài package ngoài TeX Live có sẵn trên Overleaf.

## Vì sao cần XeLaTeX?

Bộ slide dùng:

- `fontspec` + `unicode-math` để hỗ trợ tiếng Việt và công thức Unicode;
- font TeX Gyre Pagella/Heros/Cursor đi kèm TeX Live;
- TikZ cho toàn bộ diagram.

pdfLaTeX sẽ không compile được vì `fontspec`.

## Cấu trúc

```text
main.tex          # Beamer 16:9, 21 slide
theme.tex         # màu sắc, font, template
figures/          # hình paper dùng ở backup slide
latexmkrc         # gợi ý dùng XeLaTeX nếu Overleaf chạy latexmk
OVERLEAF.md       # file hướng dẫn này
```

## Nếu Overleaf báo thiếu font

Trong **Menu → Compiler**, chắc chắn compiler là XeLaTeX. Nếu project dùng bản TeX Live
quá cũ, thay ba khối `\setmainfont`, `\setsansfont`, `\setmonofont` trong `theme.tex` bằng
font có sẵn trên Overleaf (ví dụ `Latin Modern Roman`, `Latin Modern Sans`, `Latin Modern Mono`).

## Lưu ý nội dung

Đây là bộ slide tiếng Việt 35 phút, có toán nhưng đi theo trình tự trực quan → lời → công thức →
ví dụ số. Hình paper ở slide backup có credit CC BY 4.0.
