# Hợp đồng dữ liệu và API (chốt ngày đầu)

File này để nhóm reproduce (#3, #4) và nhóm demo (#5, #6) làm song song mà không phải chờ nhau. **Muốn đổi bất kỳ mục nào thì mở PR riêng và cần cả hai nhóm đồng ý** (xem `CONTRIBUTING.md`).

## 1. Định dạng dữ liệu

Dùng **đúng định dạng của code gốc**, để dữ liệu demo chạy được cả bằng code gốc lẫn bản tự cài đặt.

### File CSV dạng "long"

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `date` | `YYYY-MM-DD` | ngày đầu tuần (dữ liệu theo tuần) |
| `volume` | số thực | mức quan tâm Google Trends (0–100 sau khi ghép thang đo) |
| `query` | chuỗi | từ khóa |
| `geo` | chuỗi | mã địa điểm: mã quốc gia ISO alpha-2 (`US`, `VN`…) hoặc mã tỉnh (`VN-SG`…) |

Ví dụ:

```
date,volume,query,geo
2022-01-02,12.0,GTA 6,US
2022-01-02,3.5,GTA 6,VN
```

Quy ước:
- Mọi tổ hợp (date, query, geo) đều phải có một dòng; thiếu dữ liệu thì ghi `0`.
- File nén `.csv.gz`, đặt tên `<dataset>.csv.gz` (ví dụ `gta6.csv.gz`, `truong_giang.csv.gz`).
- Mỗi dataset có thêm một file mô tả `<dataset>.meta.md`: danh sách từ khóa, địa điểm, khoảng thời gian, từ khóa neo, ngày tải.

### Tensor

- Từ CSV dựng tensor shape **(T, K, L)**: số tuần × số từ khóa × số địa điểm.
- Thứ tự từ khóa và địa điểm: **sắp xếp theo bảng chữ cái** (giống code gốc).
- Chuẩn hóa: **min-max trên toàn bộ tensor** về [0, 1] (giống code gốc, chế độ `scale="full"`).

## 2. Độ dài dữ liệu và các tham số cửa sổ

Code gốc chạy với các giá trị sau (trong `bin/run.sh`):

| Tham số | Giá trị gốc | Ý nghĩa |
|---|---|---|
| `lc` | 104 | độ dài cửa sổ hiện tại (2 năm) |
| `lf` | 39 | số tuần dự báo |
| đánh giá | 13 / 26 / 39 tuần | các tầm dự báo được tính sai số |
| `seasonal_period` | 52 | chu kỳ mùa vụ theo năm |

Dữ liệu của paper dài khoảng 17 năm (~880 tuần). Google Trends chỉ trả dữ liệu theo tuần khi khoảng thời gian không quá khoảng 5 năm (~260 tuần), nên dữ liệu demo sẽ ngắn hơn nhiều. Nhóm demo cần thử và ghi lại giá trị `lc` / `lf` đã dùng.

## 3. API mô hình

Bản tự cài đặt (`dtracker/`) và phần gọi code gốc đều phải cung cấp **cùng các chức năng** dưới đây. Nhờ vậy demo và thí nghiệm đổi qua lại giữa hai bản mà không phải sửa gì.

| Chức năng | Đầu vào | Đầu ra |
|---|---|---|
| Khởi tạo mô hình | tensor đoạn đầu (lc × K × L) | mô hình đã fit |
| Cập nhật streaming | dữ liệu tuần mới (K × L) | mô hình đã cập nhật |
| Dự báo | số tuần h | tensor (h × K × L) |
| Lấy các thành phần | — | trend, seasonal, outlier, cùng shape với dữ liệu |
| Lấy ma trận lan truyền | — | cường độ diffusion giữa các nhóm địa điểm, kèm nhóm của từng địa điểm |
| Lấy các regime | — | danh sách thời điểm chuyển regime |

Tên hàm và tham số cụ thể do #3 và #4 đề xuất trong PR đầu tiên vào `dtracker/`, rồi ghi bổ sung vào mục này.

## 4. Đầu ra kết quả

- Bảng số liệu: CSV, cột gồm `dataset, method, horizon, metric, value`.
- Hình: PNG (cho slides) và PDF (cho report), đặt trong `figures/` của khu vực tạo ra hình.
- Tên hình: `<dataset>_<loại-hình>.png`, ví dụ `gta6_diffusion_map.png`, `device_forecast_h13.png`.
