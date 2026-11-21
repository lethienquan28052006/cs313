# `demos/gta6/` – Demo quốc tế

**Phụ trách:** #6

## Mục tiêu

Mô hình hóa mức quan tâm tìm kiếm về GTA VI và nhóm game/console **theo quốc gia**, cùng cấu trúc với dataset `device` trong paper (vài từ khóa × nhiều quốc gia, theo tuần). Nhờ vậy có thể so sánh trực tiếp với kết quả của paper.

## Thiết kế

- **Từ khóa:** GTA 6, GTA 5 (từ khóa neo), Rockstar Games, PS5, Xbox, Nintendo Switch 2, Steam.
- **Quốc gia:** khoảng 30–40 nước trên các châu lục, có Việt Nam; bỏ nước có dữ liệu toàn 0.
- **Thời gian:** 12/2021 → nay, theo tuần.
- Chi tiết ở `data/README.md`.

## Các mốc sự kiện để đối chiếu

| Thời điểm | Sự kiện |
|---|---|
| 02/2022 | Rockstar công bố đang phát triển GTA VI |
| 12/2023 | Trailer 1 |
| 05/2025 | Trailer 2; lùi ngày phát hành sang 26/05/2026 |
| 06/11/2025 | Lùi ngày phát hành sang 19/11/2026 |
| 15/10/2026 | Launch trailer |
| 19/11/2026 | Ngày phát hành dự kiến |

Trước khi đưa vào slides, kiểm tra lại các mốc trailer và xác nhận game đã thực sự phát hành.

## Câu hỏi demo cần trả lời

1. **Nhóm từ khóa:** mô hình có tự tách thành nhóm "GTA" và nhóm "console/nền tảng" không?
2. **Lan truyền:** mức quan tâm GTA 6 lan từ Mỹ / Anh sang các nước khác (giống "iPhone" trong paper), hay tăng đồng loạt vì trailer ra cùng lúc toàn cầu? Kết quả nào cũng là một finding.
3. **Outlier hay regime:** các đỉnh trailer và lùi lịch được xếp vào outlier hay regime mới?
4. **Streaming:** cho dữ liệu vào từng tuần, so dự báo với thực tế ở tuần phát hành. Tải lại dữ liệu sát ngày thuyết trình để có đủ các tuần sau phát hành.

## Phương án dự phòng

Nếu dữ liệu GTA 6 tăng quá đồng loạt và không thấy lan truyền, chạy thêm dataset `ai_chatbot` (xem `data/README.md`) theo cùng quy trình.

## Đầu ra

- Dataset `gta6` (và có thể `ai_chatbot`) trong `data/processed/` kèm `.meta.md`
- Notebook chạy demo (đã xóa output)
- `figures/`: bản đồ lan truyền, phân rã, dự báo so với thực tế, timeline regime
- 3–5 gạch đầu dòng kết luận cho #2
