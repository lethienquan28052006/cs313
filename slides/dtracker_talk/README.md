# D-Tracker overview talk

Bộ Beamer 16:9 tiếng Việt, khoảng 35 phút, dành cho người chưa có kiến thức nền.
Trọng tâm là ứng dụng và trực giác; các ý toán vẫn được dạy theo thứ tự:

> trực quan → nói bằng lời → công thức → kiểm tra bằng ví dụ số.

## Sản phẩm

- `outline.md`: outline từng slide, timing, mục tiêu, visual, phần toán và lời dẫn.
- `main.tex`: nội dung Beamer.
- `theme.tex`: màu sắc, font, frametitle, footline, box.
- `dtracker_talk.pdf`: bản PDF sau khi build, 21 slide (17 slide chính + 4 backup), 16:9.

## Build

```bash
cd slides/dtracker_talk
make all
```

Makefile ưu tiên Tectonic trên `PATH`, sau đó binary đã có ở
`../paper_explore/.tools/tectonic`. Nếu cả hai không có, `make` tải Tectonic 0.15.0
vào `.tools/` cục bộ.

```bash
make check   # unit test checker + kiểm tra outline/deck/hình
make clean   # xóa build/ và PDF đã copy
```

## Cấu trúc trình bày

- Mở đầu bằng câu hỏi thực tế.
- Dữ liệu tensor, vì sao khó, pipeline.
- Ba lớp trend + seasonal + outlier.
- Trực giác “kênh ẩn”, Tucker, reaction–diffusion.
- Phép chiếu từ kênh ẩn ra dữ liệu, bộ tham số, ALS.
- MDL + regime switching, streaming.
- Ba ứng dụng, bằng chứng, giới hạn, takeaway.
- Bốn slide backup cho Q&A.

## Ghi chú nội dung

- Các công thức chính là Eq. (1)–(4), Eq. (10) và một bước Euler minh họa.
- Không chứng minh ALS/MDL; mục tiêu là đọc và diễn giải được.
- Số liệu “6 bộ dữ liệu”, MAE, 8.0×, 57% lấy từ paper; 57% được giữ đúng mức
  “paper báo cáo”, không gán mẫu số.
- Hình paper dùng lại từ `slides/paper_explore/figures/` với credit CC BY 4.0.
- Slide chỉ dùng tiếng Việt; nếu cần bản Anh, có thể tách theme và dịch nội dung.
