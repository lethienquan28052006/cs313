# `report/` – Report 4 trang (LaTeX)

**Phụ trách:** #7 (viết chính, gom nội dung). Các thành viên khác cung cấp nội dung cho section liên quan.

## Yêu cầu

- 4 trang, tiếng Anh.
- Có đủ: Introduction, Problem Setup, Method, Experiments, Conclusion, **Tasks assigned to each member**.
- Dùng template ACM 2 cột (`acmart`, định dạng của KDD), cho thống nhất với paper gốc.

## Dự kiến tổ chức

| Thành phần | Nội dung |
|---|---|
| File chính | Khai báo template, tiêu đề, tác giả, ghép các section |
| `sections/` | **Mỗi section một file riêng**, để nhiều người sửa song song mà không bị conflict |
| `figures/` | Bản cuối của các hình (PDF), copy từ `experiments/` và `demos/` |
| File tài liệu tham khảo | BibTeX, trong đó có paper D-Tracker |

Có thể nối thư mục này với Overleaf (Overleaf hỗ trợ đồng bộ với GitHub) để viết trực tuyến.

## Section và nguồn nội dung

| Section | Người viết nháp | Nguồn | Độ dài gợi ý |
|---|---|---|---|
| Introduction | #7 | `docs/paper_notes.md` mục 1 | ~0.5 trang |
| Problem Setup | #7 (nhờ #1 duyệt) | `docs/paper_notes.md` mục 1–2 | ~0.5 trang |
| Method | #3 nháp → #7 biên tập | `docs/paper_notes.md` mục 3–5 | ~1 trang |
| Experiments | #4 (tái hiện), #5 + #6 (demo) nháp → #7 biên tập | `experiments/results/`, `demos/*/` | ~1.5 trang |
| Conclusion | #7 | Key findings thống nhất với #2 | ~0.25 trang |
| Tasks of each member | #7 | Bảng thành viên trong `README.md` gốc | ~0.25 trang |

## Việc cần làm

- [ ] Dựng file chính và các section rỗng với template ACM; build thử ra PDF
- [ ] Viết Introduction và Problem Setup
- [ ] Nhận nháp Method, Experiments; biên tập cho thống nhất giọng văn và ký hiệu (ký hiệu theo `docs/paper_notes.md` mục 2)
- [ ] Kiểm tra giới hạn 4 trang; nếu thừa thì cắt chữ, không thu nhỏ font hay lề
- [ ] Viết bảng phân công thành viên
