# Code gốc của tác giả

Repo gốc: https://github.com/Higashiguchi-Shingo/D-Tracker

Repo gốc **không có file license**, nên nhóm **không copy code gốc vào repo này**. Mỗi người tự clone về máy vào đúng thư mục này. Thư mục `third_party/D-Tracker/` đã nằm trong `.gitignore` nên sẽ không bị commit nhầm.

## Khu vực này dùng để làm gì

- Chạy code gốc để có **kết quả đối chứng** cho phần tự cài đặt (#4 dùng trong `experiments/`).
- Cho nhóm demo (#5, #6) chạy thử trên dữ liệu mới **trong lúc bản tự cài đặt chưa xong**.

## Những gì đã kiểm tra trong repo gốc (21/11/2026)

**Cấu trúc:**
- `src/`: `dtracker.py` (mô hình chính), `main.py` (chạy), `accuracy.py` (tính sai số dự báo), `MDL.py` (chi phí MDL), `rank.py` (cập nhật số chiều ẩn), `tucker.py`, `decompose.py`, `utils.py` (đọc dữ liệu thành tensor).
- `bin/run.sh`: chạy mô hình rồi tính sai số. Cách dùng: `cd bin && sh run.sh <dataset>`.
- `data/`: 6 dataset: `chatapp`, `device`, `programming`, `pythonlib`, `vod` (Google Trends) và `covid`.

**Dữ liệu:**
- Các dataset Google Trends có định dạng CSV dạng long với các cột `date, volume, query, geo`, theo tuần, khoảng 7–9 từ khóa × 48 quốc gia, kéo dài khoảng 2006–2023.
- `covid` có các cột `date, location_key, key, value`.

**Vấn đề cần lưu ý khi cài đặt môi trường:**
- README gốc hướng dẫn `pip install -r requirements.txt`, nhưng file thật tên là `requirement.txt` (thiếu chữ "s").
- `requirement.txt` thiếu một số thư viện mà code có import: `lmfit` (trong `dtracker.py`), `psutil` (trong `main.py`, `rank.py`, `decompose.py`) và `torch` (trong `utils.py`).
- Repo có kèm file `__pycache__` của Python 3.10 và 3.11, nên dùng một trong hai phiên bản này.

**Chưa kiểm tra:** chưa chạy thử `run.sh` trên dataset nào. Người phụ trách #4 chạy thử đầu tiên và ghi lại ở đây: phiên bản Python, thời gian chạy, lỗi gặp phải.
