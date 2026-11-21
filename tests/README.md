# `tests/` – Kiểm tra tự động

**Phụ trách:** #3 + #4 (người viết phần nào thì viết test cho phần đó). #5, #6 thêm test cho `demos/common/` nếu cần.

## Khu vực này làm gì

Kiểm tra nhanh, chạy được trong vài giây, để biết một thay đổi có làm hỏng phần khác hay không trước khi merge PR.

## Nên kiểm tra

| Nội dung | Người |
|---|---|
| Dựng tensor từ CSV cho ra đúng shape (T, K, L) và đúng thứ tự từ khóa/địa điểm | #5, #6 |
| Mô hình fit và dự báo được trên một tensor nhỏ, kết quả đúng shape | #3 |
| Trên dữ liệu giả sinh từ hệ phản ứng–khuếch tán với tham số biết trước, mô hình tìm lại được tham số gần đúng | #3 |
| Streaming: cập nhật từng tuần không lỗi; dữ liệu giả có đổi regime giữa chừng thì mô hình phát hiện được | #4 |
