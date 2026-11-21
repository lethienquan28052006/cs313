# `data/` – Dữ liệu

**Phụ trách:** #5, #6 (dữ liệu demo). Dữ liệu của paper lấy từ repo gốc (xem `third_party/README.md`).

## Cấu trúc

| Thư mục | Nội dung | Commit? |
|---|---|---|
| `raw/` | Dữ liệu tải về chưa xử lý (CSV từ Google Trends theo từng lần tải) | **Không** (đã nằm trong `.gitignore`) |
| `processed/` | Dữ liệu đã ghép thang đo, đúng định dạng ở `docs/interfaces.md` mục 1, kèm file `.meta.md` | Có, nếu dưới khoảng 5 MB |

Hai thư mục con này sẽ được tạo khi có dữ liệu đầu tiên.

## Các dataset dự kiến

| Dataset | Người | Từ khóa | Địa điểm | Thời gian |
|---|---|---|---|---|
| `truong_giang` | #5 | Trường Giang, Nhà ba tôi một phòng, 2 ngày 1 đêm, Trấn Thành (neo) | Các tỉnh/thành Việt Nam có đủ dữ liệu (~15–20) hoặc gộp theo vùng | ~5 năm gần nhất, theo tuần |
| `gta6` | #6 | GTA 6, GTA 5 (neo), Rockstar Games, PS5, Xbox, Nintendo Switch 2, Steam | ~30–40 quốc gia trên các châu lục | 12/2021 → nay, theo tuần |
| `ai_chatbot` (dự phòng) | #6 | ChatGPT, Gemini, Claude, DeepSeek, Copilot | như `gta6` | như `gta6` |

## Lưu ý khi tải Google Trends

- Mỗi lần truy vấn tối đa **5 từ khóa**. Nhiều hơn thì chia thành nhiều lần, mọi lần đều có **từ khóa neo** để ghép về cùng thang đo.
- Dữ liệu chỉ theo tuần khi khoảng thời gian không quá khoảng **5 năm**.
- Thư viện không chính thức (như `pytrends`) dễ bị chặn khi gọi nhiều: tải sớm, lưu lại file thô, nếu bị chặn thì tải tay từ trends.google.com.
- Kiểm tra Google Trends hiện chia Việt Nam theo đơn vị hành chính cũ hay mới.
- Ghi ngày tải vào file `.meta.md`, vì Google Trends có thể trả số liệu hơi khác nhau giữa các lần tải.
