# `demos/common/` – Phần dùng chung cho hai demo

**Phụ trách:** #5 + #6 (thống nhất sớm, trước khi làm demo riêng)

## Khu vực này làm gì

| Chức năng | Mô tả |
|---|---|
| Tải dữ liệu | Nhận danh sách từ khóa, địa điểm, khoảng thời gian, từ khóa neo; tải Google Trends theo từng lô tối đa 5 từ khóa; lưu file thô vào `data/raw/` |
| Ghép thang đo | Dùng từ khóa neo để đưa các lô về cùng thang đo; xuất CSV đúng định dạng `docs/interfaces.md` vào `data/processed/` |
| Dựng tensor | CSV → tensor (T, K, L), chuẩn hóa min-max giống code gốc |
| Vẽ hình | Bản đồ lan truyền giữa các nhóm địa điểm; phân rã trend / seasonal / outlier; dự báo so với thực tế; timeline các regime |

## Việc cần làm

- [ ] Thống nhất định dạng file cấu hình cho một demo (từ khóa, địa điểm, thời gian, neo, `lc`, `lf`)
- [ ] Chức năng tải dữ liệu và ghép thang đo
- [ ] Chức năng dựng tensor; kiểm tra bằng cách chạy code gốc trên dữ liệu vừa dựng
- [ ] Chức năng vẽ 4 loại hình ở trên, dùng chung màu sắc và phong cách cho cả hai demo
