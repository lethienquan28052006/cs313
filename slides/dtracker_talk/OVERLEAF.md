# D-Tracker final-project talk — Overleaf

## Cách dùng

1. Upload `dtracker_talk_overleaf.zip` lên Overleaf.
2. Mở **Menu → Compiler** và chọn **XeLaTeX**.
3. Chọn Main document: `main.tex`.
4. Bấm **Recompile**.

Kết quả mong đợi: **33 trang** (29 slide chính + 4 backup), 16:9. Không cần shell-escape hay package ngoài TeX Live thông dụng.

## Vì sao cần XeLaTeX?

Deck dùng `fontspec` + `unicode-math`, font Latin Modern Sans/Mono và Latin Modern Math cho tiếng Việt và công thức. TikZ dùng cho các diagram minh họa cơ chế. pdfLaTeX không compile được vì `fontspec`.

## Cấu trúc ZIP

```text
main.tex          # Beamer 16:9, 33 trang
theme.tex         # màu sắc, font, template, panel
figures/          # bốn hình paper dùng ở phần experiments
latexmkrc         # chọn XeLaTeX khi chạy latexmk
OVERLEAF.md       # hướng dẫn này
```

`outline.md`, source map và paper PDF không nằm trong ZIP vì không cần để compile. Chúng vẫn được lưu trong repository.

## Nếu Overleaf báo thiếu font

Chắc chắn compiler là **XeLaTeX**. Nếu project dùng bản TeX Live quá cũ, thay các khối `\setmainfont`, `\setsansfont`, `\setmonofont` và `\setmathfont` trong `theme.tex` bằng tên font Latin Modern có sẵn trên Overleaf.

## Lưu ý khi chỉnh nội dung

- Deck là bài tiếng Việt khoảng 33 phút; outline có timing từng slide.
- Slide 25–27 chỉ là khung reproduction: `---` = “Nhóm sẽ bổ sung sau khi chạy thực nghiệm”.
- Slide 28 Demo cố ý trống phần nội dung.
- Không đổi paper-reported values thành team results.
- Nếu đổi số slide, cập nhật cả `outline.md` và các marker `% SLIDE` trong `main.tex`, rồi chạy `make check` trên bản local.
- Hình paper có credit KDD 2025/CC BY 4.0 ngay trên slide.
