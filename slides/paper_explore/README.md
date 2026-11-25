# D-Tracker — bài đọc giải thích paper

Thư mục này chứa **hai tài liệu PDF LaTeX song ngữ** giải thích paper
[D-Tracker](https://arxiv.org/abs/2505.00242) cho người mới, không phải bộ slide thuyết trình.

- `dtracker_explained_vi.pdf`: bản tiếng Việt.
- `dtracker_explained_en.pdf`: bản tiếng Anh.

Nội dung đi từ ví dụ trực quan, tensor, phân rã Tucker, reaction–diffusion, toàn bộ mô hình,
ALS, MDL, streaming, thí nghiệm, phản biện, đến phụ lục tự học và bảng ký hiệu. Hai bản giữ cùng
chương, công thức, hình, nhãn và số câu tự kiểm tra.

> Đây là tài liệu học tập độc lập. Khi có khác biệt, paper gốc `arXiv:2505.00242v1` là nguồn quyết
> định. Tài liệu không chứa kết quả reproduce mới.

## Build

Yêu cầu tối thiểu: `make`, `python3`, `curl`, `tar`. Không cần cài TeX toàn cục.

```bash
cd slides/paper_explore
make all       # tạo cả hai PDF
make vi        # chỉ bản tiếng Việt
make en        # chỉ bản tiếng Anh
make check     # unit test checker + kiểm tra cấu trúc hai bản
make clean     # xóa build/ và hai PDF đã copy
```

Lần build đầu, `make` tải **Tectonic 0.15.0** vào `.tools/` (đã gitignore) và dùng nó để biên dịch.
Nếu máy đã có `tectonic` trên `PATH`, Makefile dùng bản đó. Tectonic tự tải các package/font cần
thiết trong lần chạy đầu; các lần sau dùng cache.

Build đi qua `build/`; PDF cuối được copy về thư mục này. Log LaTeX nằm trong `build/`.
Tectonic cảnh báo không tìm thấy hyphenation pattern tiếng Việt trong format mặc định; lỗi này không
làm hỏng chữ có dấu và không tạo missing glyph. Có thể bỏ qua hoặc cấu hình pattern riêng nếu muốn
ngắt dòng tiếng Việt tốt hơn.

## Kiểm tra tự động

`make check` chạy:

```bash
python3 scripts/test_check_documents.py
python3 scripts/check_documents.py
```

Checker bắt các lỗi cấu trúc có thể làm hai bản lệch nhau:

- thiếu file main hoặc file chương được `\input`;
- danh sách chương khác nhau giữa VI và EN;
- nhãn `\label` trùng trong một bản hoặc khác tập nhãn giữa hai bản;
- placeholder `TODO`, `TBD`, `chưa điền`;
- hình được tham chiếu nhưng không tồn tại;
- số self-check khác nhau giữa hai ngôn ngữ.

Unit test của checker dùng cây tài liệu tạm và kiểm tra cả trường hợp hợp lệ lẫn từng lỗi.

## Cấu trúc

```text
slides/paper_explore/
├── dtracker_explained_vi.tex     # main VI: metadata, TOC, thứ tự chương
├── dtracker_explained_en.tex     # main EN
├── dtracker_style.tex            # preamble, font, màu, box, macro hình
├── references.tex                # bibliography chung
├── sections_vi/                  # 01 … 10, cùng tên với sections_en/
├── sections_en/
├── figures/                      # hình paper, giữ nguyên tên gốc
├── sources/
│   ├── paper.html                # snapshot arXiv HTML v1
│   ├── paper.pdf                 # snapshot arXiv PDF v1
│   ├── source_map.md             # bản đồ claim/công thức/số liệu → vị trí paper
│   └── figure_manifest.tsv       # URL, caption, license, SHA-256 từng hình
├── scripts/
│   ├── check_documents.py
│   ├── test_check_documents.py
│   └── install_tectonic.sh
├── Makefile
└── .gitignore
```

## Thêm hoặc sửa nội dung

1. Sửa đồng thời file cùng tên trong `sections_vi/` và `sections_en/`.
2. Nếu thêm chương, thêm `\input{...}` vào **cả hai** main theo cùng thứ tự.
3. Giữ cùng `\label`, cùng số hình và cùng số self-check ở hai bản.
4. Mọi số liệu/công thức mới phải thêm vị trí nguồn vào `sources/source_map.md`.
5. Chạy `make check all` và kiểm tra log `build/dtracker_explained_*.log`.

Style dùng font TeX Gyre Pagella/Heros/Cursor đi kèm Tectonic, `unicode-math`, `tcolorbox`,
TikZ và hyperref. Các box có nghĩa cố định: `keypoint`, `plainwords`, `commonmistake`,
`selfcheck`; macro `\sourcefig[width]{file}{caption}{label}` tự thêm credit vào caption.

## Nguồn và giấy phép hình

- Paper: Higashiguchi, Matsubara, Kawabata, Murayama, Sakurai. *D-Tracker: Modeling Interest
  Diffusion in Social Activity Tensor Data Streams*. KDD '25.
  DOI `10.1145/3690624.3709192`, arXiv `2505.00242v1`.
- Snapshot nguồn nằm trong `sources/`, tải ngày 25/11/2026.
- Hình paper được dùng với credit trong caption; arXiv HTML hiển thị CC BY 4.0.
- `figure_manifest.tsv` ghi URL gốc, caption, license và SHA-256 để kiểm tra tính toàn vẹn.
- Văn bản giải thích là tài liệu học tập của dự án CS313; không thay thế hoặc cấp lại giấy phép cho
  paper gốc.

## Những điểm paper chưa rõ (đã nêu trong tài liệu)

- `d_l \ll k` ở §3.3 nhiều khả năng là typo; tài liệu dùng `d_l \ll l`.
- Algorithm 4 trong Appendix A.4 lặp candidate `(d_k,d_l+1,d_s)` và thiếu `(d_k+1,d_l,d_s)`.
- Ký hiệu `n` trong chi phí MDL của outlier không được định nghĩa lại ngay tại công thức.
- Forecast được gọi trong Algorithm 1 nhưng công thức chi tiết không có trong main text.
- Phần văn xuôi nói 48 quốc gia, Table 4 dùng 50 địa điểm.
- Bài toán “1/2/3 tuần” cho horizon 7/14/21 bước của dữ liệu Covid-19 hàng ngày là cách diễn giải
  trong paper, không phải phép đổi đơn vị hoàn toàn nhất quán.

Không sửa âm thầm các điểm trên. Nếu cần khẳng định mạnh hơn, đọc code gốc hoặc liên hệ tác giả.
