# `demos/` – Demo trên dữ liệu thời sự

**Phụ trách:** #5 (Trường Giang), #6 (GTA VI), cùng làm `common/`

Khu vực này áp dụng D-Tracker lên **dữ liệu mới do nhóm tự thu thập**, để minh họa phương pháp trên chủ đề đang được quan tâm.

| Thư mục | Người | Nội dung |
|---|---|---|
| `common/` | #5 + #6 | Phần dùng chung cho cả hai demo: tải dữ liệu, dựng tensor, vẽ hình |
| `truong-giang/` | #5 | Demo trong nước: mức quan tâm theo tỉnh/thành Việt Nam |
| `gta6/` | #6 | Demo quốc tế: mức quan tâm theo quốc gia |

Hai demo khác nhau ở **cấu hình** (từ khóa, địa điểm, thời gian), còn quy trình xử lý giống nhau. Nhờ vậy #2 so sánh được hai kết quả khi thuyết trình.

Trong lúc bản tự cài đặt chưa xong, demo chạy bằng code gốc (xem `third_party/README.md`), vì cả hai dùng chung định dạng dữ liệu.
