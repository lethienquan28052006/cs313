# `dtracker/` – Bản tự cài đặt D-Tracker

**Phụ trách:** #3 Reproduce 1 (mô hình lõi), #4 Reproduce 2 (streaming)

Khu vực này chứa **bản cài đặt lại D-Tracker do nhóm tự viết**, theo mô tả trong paper. Không copy code gốc; được đọc code gốc để đối chiếu.

## Mục tiêu

Cài đặt đủ các thành phần của mô hình, cung cấp đúng các chức năng ghi trong `docs/interfaces.md` mục 3, để `experiments/` và `demos/` dùng được.

## Phân chia bên trong

| Phần | Người | Nội dung |
|---|---|---|
| Trend | #3 | Phân rã tensor với lõi động học sinh ra từ hệ phản ứng–khuếch tán (tốc độ tăng trưởng, cường độ khuếch tán giữa các nhóm địa điểm) |
| Seasonal | #3 | Thành phần mùa vụ theo chu kỳ (mặc định 52 tuần) |
| Outlier | #3 | Thành phần bất thường thưa (sparse) |
| Ước lượng tham số | #3 | Vòng lặp ALS cập nhật lần lượt từng thành phần |
| Streaming | #4 | Cập nhật mô hình khi có dữ liệu tuần mới, chi phí không tăng theo độ dài chuỗi |
| Chọn số chiều và regime | #4 | Chọn số nhóm từ khóa/địa điểm bằng chi phí MDL, phát hiện điểm thay đổi, lưu và chuyển regime |

#3 và #4 chia file sao cho mỗi người sửa file riêng, chỉ dùng chung phần khai báo API.

## Việc cần làm

- [ ] #3 điền mục 2–4 trong `docs/paper_notes.md` (ký hiệu, mô hình, ALS)
- [ ] #4 điền mục 5 trong `docs/paper_notes.md` (streaming, MDL, regime)
- [ ] Đề xuất tên hàm cụ thể cho API, ghi vào `docs/interfaces.md` mục 3 (PR riêng)
- [ ] Cài đặt trend + seasonal + outlier + ALS, fit được trên một dataset của paper
- [ ] Cài đặt streaming và regime switching
- [ ] Kiểm tra trên dữ liệu giả có lời giải biết trước (xem `tests/`)

## Đầu ra

- Mô hình chạy được trên ít nhất một dataset của paper và trên dữ liệu demo.
- Một đoạn mô tả ngắn những chỗ **bản tự cài đặt khác code gốc** (để đưa vào report và slides).
