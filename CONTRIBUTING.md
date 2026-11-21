# Quy trình làm việc chung

## Nguyên tắc

1. **Mỗi người làm trong thư mục của mình.** Cần sửa thư mục của người khác thì nhắn người đó trước, hoặc mở issue.
2. **Không push thẳng lên `main`.** Mọi thay đổi đi qua Pull Request và cần ít nhất 1 người duyệt (CODEOWNERS tự gán reviewer).
3. **Muốn đổi `docs/interfaces.md`** (định dạng dữ liệu, API mô hình) thì phải mở PR riêng, và cả nhóm reproduce lẫn nhóm demo phải đồng ý. File này là "hợp đồng" để mọi người làm song song.

## Branch

Đặt tên theo dạng `<khu-vực>/<việc-ngắn>`:

| Khu vực | Ví dụ |
|---|---|
| `dtracker/` | `dtracker/trend-als`, `dtracker/streaming` |
| `exp/` | `exp/googletrends-device`, `exp/compare-official` |
| `demo/` | `demo/common-fetch`, `demo/gta6-plots`, `demo/truong-giang-data` |
| `report/` | `report/method`, `report/experiments` |
| `slides/` | `slides/outline`, `slides/figures` |
| `docs/` | `docs/paper-notes` |

Quy trình cho mỗi task:

```bash
git checkout main && git pull
git checkout -b demo/gta6-fetch
# ... làm việc, commit nhỏ và thường xuyên ...
git push -u origin demo/gta6-fetch
# mở Pull Request vào main trên GitHub, gắn issue: "Closes #12"
```

Trước khi mở PR, cập nhật branch với `main` mới nhất (`git pull --rebase origin main`).

## Commit message

Ngắn gọn, viết bằng tiếng Anh hoặc tiếng Việt đều được, nhưng mở đầu bằng khu vực:

```
dtracker: add ALS update for keyword factor
demo/gta6: fetch weekly data for 35 countries
report: draft method section
```

## Issue và Project board

- Mỗi task là một issue (dùng template "Task"), có người nhận, hạn chót và nhãn khu vực.
- Board có 4 cột: **Todo → Doing → Review → Done**.
- Đang bị kẹt thì ghi vào issue và tag người liên quan, đừng chờ đến buổi họp.

## Notebook, dữ liệu và hình

- **Notebook:** xóa output trước khi commit (Kernel → Restart & Clear Output) để tránh conflict. Hình cần giữ thì xuất ra file PNG/PDF.
- **Dữ liệu thô** để trong `data/raw/` và không commit (đã nằm trong `.gitignore`). Dữ liệu đã xử lý dưới khoảng 5 MB thì được commit vào `data/processed/`.
- **Hình** cho slides và report đặt trong `figures/` của khu vực tạo ra hình đó. `slides/` và `report/` chỉ tham chiếu hoặc copy bản cuối.

## Code gốc của tác giả

Repo gốc không có license. **Không copy code gốc vào repo này.** Clone riêng theo hướng dẫn trong `third_party/README.md`.
