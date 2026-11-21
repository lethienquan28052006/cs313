# `demos/truong-giang/` – Demo trong nước

**Phụ trách:** #5

## Mục tiêu

Mô hình hóa mức quan tâm tìm kiếm về nghệ sĩ Trường Giang **theo tỉnh/thành Việt Nam**, xem D-Tracker tách được xu hướng, mùa vụ, bất thường và lan truyền giữa các vùng hay không.

## Thiết kế

- **Từ khóa:** Trường Giang, Nhà ba tôi một phòng, 2 ngày 1 đêm, Trấn Thành (đối chứng và từ khóa neo). Chi tiết ở `data/README.md`.
- **Địa điểm:** các tỉnh/thành có đủ dữ liệu, hoặc gộp theo vùng nếu tỉnh nhỏ toàn giá trị 0.
- **Thời gian:** khoảng 5 năm gần nhất, theo tuần.

## Câu hỏi demo cần trả lời

1. **Mùa vụ:** phim Tết lặp lại hằng năm. Mô hình có bắt được chu kỳ 52 tuần không?
2. **Regime:** đỉnh Tết 2026 (phim "Nhà ba tôi một phòng") và đỉnh từ tháng 9/2026 (tranh luận trên mạng) có được tách thành các regime khác nhau không?
3. **Lan truyền:** mức quan tâm bắt đầu ở TP.HCM / Hà Nội rồi lan ra các tỉnh, hay tăng đồng loạt?

## Lưu ý nội dung

Sự việc từ tháng 9/2026 liên quan đến đời tư và đang được xử lý pháp lý. **Chỉ dùng từ khóa trung tính, không đưa nội dung tin đồn lên slide hay report.** Chỉ trình bày "mức quan tâm tăng", không bàn về nguyên nhân.

## Đầu ra

- Dataset `truong_giang` trong `data/processed/` kèm `.meta.md`
- Notebook chạy demo (đã xóa output)
- `figures/`: bản đồ lan truyền, phân rã, dự báo, timeline regime
- 3–5 gạch đầu dòng kết luận cho #2 dùng khi thuyết trình
