# D-Tracker — Overleaf report skeleton

Khung LaTeX tiếng Anh cho report đồ án Data Mining, dựa trên `CS114_Report.zip` do người dùng cung cấp. **Đây chưa phải report hoàn chỉnh** và không chứa implementation/reproduction result do nhóm tự tạo.

## Layout và giới hạn trang

- `IEEEtran` conference, kiểu hai cột của template; không dùng `titlepage`.
- Trang 1: thông tin project một cột và ToC.
- Trang 2 trở đi: Abstract + hai cột Introduction → Task Assignment.
- Hiện bản khung compile thành **3 trang**, trong giới hạn tối đa **4 trang**.
- Khi thay placeholders bằng nội dung thật, phải kiểm tra lại `make check`; không được thu nhỏ font/lề để né giới hạn trang.

## Cấu trúc cần sửa

`main.tex` chứa preamble, metadata và thứ tự các `\input`. Chỉnh nội dung trong từng file:

```text
sections/01_introduction.tex    # Introduction, motivation, project scope
sections/02_problem_setup.tex   # Input window, notation, challenges
sections/03_method.tex          # Decomposition, latent factors, diffusion, estimation
sections/04_experiments.tex    # Setup, original-paper results, team reproduction
sections/05_conclusion.tex     # Summary, limitations, next steps
sections/06_tasks.tex           # Work assigned to each member
references.bib                 # D-Tracker KDD 2025 entry and additional sources
images/Logo_UIT.svg.png         # Optional logo copied unchanged from supplied template
```

`references.bib` có sẵn entry thật cho D-Tracker: DOI `10.1145/3690624.3709192`, arXiv:2505.00242v1.

## Quy ước viết

- Thay `\pending{...}` bằng nội dung thật. Các hướng dẫn trong dấu ngoặc vuông chỉ là gợi ý, không phải dữ kiện được xác nhận.
- Course, instructor, team name, member IDs và Task Assignment là vùng nhóm phải tự điền.
- **Results from the Original Paper** chỉ chứa kết quả có trong paper, kèm trang/table/figure citation.
- **Our Reproduction** chỉ điền kết quả từ experiment log thực tế. Không chép số paper thành kết quả nhóm, không suy diễn runtime hay success.
- File 01–04 có citation `higashiguchi2025dtracker` làm mẫu; thêm citation cụ thể vào đoạn văn sau khi viết.
- Không cần build lại PDF/ZIP bằng tay trên Overleaf; Overleaf tự sinh PDF từ source.

## Build local

```bash
cd report
make all           # PDF + Overleaf ZIP
make check         # 6 unit tests + structure/layout/page-count check
make pdf           # chỉ build dtracker_report.pdf
make overleaf-zip  # chỉ tạo dtracker_report_overleaf.zip
make clean         # xóa build/, PDF và ZIP đã tạo
```

Checker yêu cầu đủ section, ngăn `titlepage`, duy trì hai subsection Original Paper/Our Reproduction và kiểm tra PDF ≤4 trang. `make clean` không xóa source.

Makefile ưu tiên Tectonic tại `report/.tools/tectonic` (bản 0.17.0 đã được cài cục bộ), sau đó binary trên `PATH`, cuối cùng `../slides/paper_explore/.tools/tectonic`. Bản local 0.17.0 tránh BibTeX rerun bug `tectonic#1150`; thư mục `.tools/` và `build/` không được đưa vào Overleaf ZIP hay cố ý commit binary.

## Lưu ý tương thích

- `references.bib` dùng BibTeX + `IEEEtran.bst`; không cần Biber/biblatex.
- Với Tectonic XeTeX, có thể xuất hiện notices `inputenc package ignored` và font-shape substitution `TU/ptm`. Đây là ghi chú riêng của engine khi dùng `inputenc`/T5; không phải missing glyph hay layout error. Overleaf sẽ dùng pdfLaTeX.

Xem `OVERLEAF.md` để upload trực tiếp.
