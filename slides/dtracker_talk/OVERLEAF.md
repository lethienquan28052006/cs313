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
parts/            # bảy file nội dung được main.tex ghép qua \input
figures/          # hai hình/crop paper dùng ở phần experiments
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
- Sửa nội dung trong `parts/`: slide 1 ở `00_cover`; 2–6 ở `01_problem`; 7–18 ở `02_methodology`; 19–24 ở `03_experiments`; 25–27 ở `04_reproduction`; 28–29 ở `05_demo_conclusion`; A1–A4 ở `99_backup`.
- Nếu đổi số slide, cập nhật cả `outline.md` và các marker `% SLIDE` trong file part tương ứng, rồi chạy `make check` trên bản local.
- Hình/crop paper có credit KDD 2025/CC BY 4.0 ngay trên slide.
