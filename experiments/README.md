# `experiments/` – Tái hiện thí nghiệm của paper

**Phụ trách:** #4 Reproduce 2

Khu vực này chạy lại các thí nghiệm trong paper và **so sánh bản tự cài đặt với code gốc**. Đây là nguồn số liệu chính cho phần Experiments của slides và report.

## Mục tiêu

1. Chạy code gốc trên các dataset của paper, ghi lại kết quả (sai số dự báo, thời gian chạy).
2. Chạy bản tự cài đặt (`dtracker/`) trên cùng dữ liệu, cùng tham số.
3. Làm bảng **"ours vs official"** và so với số liệu báo cáo trong paper.

## Dự kiến tổ chức

| Thư mục / file | Nội dung |
|---|---|
| `configs/` | Mỗi dataset một file cấu hình: tên dataset, `lc`, `lf`, các tầm dự báo |
| Phần chạy code gốc | Gọi code trong `third_party/D-Tracker/` |
| Phần chạy bản tự cài đặt | Gọi `dtracker/` |
| Phần so sánh | Gộp kết quả thành bảng và vẽ hình |
| `results/` | Chỉ commit CSV tóm tắt và hình; output thô để ngoài repo |

## Thí nghiệm cần tái hiện

- [ ] Độ chính xác dự báo trên các dataset Google Trends (ít nhất `device` và một dataset khác) và `covid`, với các tầm 13 / 26 / 39 tuần
- [ ] Thời gian chạy theo độ dài luồng dữ liệu (paper khẳng định không tăng theo độ dài)
- [ ] Hình lan truyền quan tâm giữa các nhóm quốc gia (ví dụ "iPhone" trong dataset `device`)
- [ ] (Nếu kịp) ablation: bỏ seasonal, bỏ diffusion
- [ ] (Nếu kịp) một vài baseline đơn giản để so sánh

## Đầu ra

- `results/` có bảng CSV theo định dạng ở `docs/interfaces.md` mục 4.
- Hình đã xuất sẵn cho #2 (slides) và #7 (report).
- Ghi chú ngắn: kết quả nào khớp với paper, kết quả nào lệch và giải thích vì sao.
