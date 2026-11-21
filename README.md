# CS313 – Final Project: D-Tracker (KDD 2025)

Nhóm 7 người tái hiện (reimplement) paper:

> **D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams**
> Shingo Higashiguchi, Yasuko Matsubara, Koki Kawabata, Taichi Murayama, Yasushi Sakurai — KDD '25, Toronto.
> Paper: https://arxiv.org/abs/2505.00242 · DOI: 10.1145/3690624.3709192 · Code gốc: https://github.com/Higashiguchi-Shingo/D-Tracker

## Sản phẩm cần nộp

| Sản phẩm | Yêu cầu | Nằm ở đâu |
|---|---|---|
| Implement lại phương pháp | Tự cài đặt, so sánh với code gốc | `dtracker/`, `experiments/` |
| Demo | Trường Giang (VN, theo tỉnh) và GTA VI (quốc tế, theo quốc gia) | `demos/` |
| Thuyết trình | 30–35 phút: problem, method, experiments, key findings | Slides làm ngoài repo; dàn ý, script, hình ở `slides/` |
| Report | 4 trang, tiếng Anh, LaTeX: intro, problem setup, method, experiments, conclusion, tasks của từng thành viên | `report/` |

## Cấu trúc repo và người phụ trách

```
cs313/
├── README.md            # file này
├── CONTRIBUTING.md      # quy trình git, đặt tên branch, PR
├── .github/             # CODEOWNERS, template PR và issue
├── docs/                # tài liệu chung: ghi chú paper, hợp đồng dữ liệu/API, biên bản họp
├── third_party/         # hướng dẫn lấy code gốc của tác giả (không copy vào repo)
├── dtracker/            # #3 + #4 – bản tự cài đặt D-Tracker
├── experiments/         # #4 – tái hiện thí nghiệm của paper, so sánh với code gốc
├── data/                # #5 + #6 – quy ước dữ liệu, nguồn, cách tải
├── demos/               # #5 Trường Giang, #6 GTA VI, phần dùng chung
├── report/              # #7 – report LaTeX 4 trang
├── slides/              # #1 + #2 – dàn ý, script, hình cho slides
└── tests/               # #3 + #4 – kiểm tra tự động
```

Mỗi thư mục có `README.md` riêng mô tả mục tiêu, người phụ trách, việc cần làm và đầu ra.

## Thành viên

| # | Vai trò | Thành viên | GitHub | Thư mục |
|---|---|---|---|---|
| 1 | Thuyết trình A – Problem + Method | _TBD_ | _TBD_ | `slides/` |
| 2 | Thuyết trình B – Experiments + Demo + Findings | _TBD_ | _TBD_ | `slides/` |
| 3 | Reproduce 1 – Mô hình lõi | _TBD_ | _TBD_ | `dtracker/` |
| 4 | Reproduce 2 – Streaming + thí nghiệm | _TBD_ | _TBD_ | `dtracker/`, `experiments/` |
| 5 | Demo Trường Giang | _TBD_ | _TBD_ | `demos/truong-giang/`, `demos/common/` |
| 6 | Demo GTA VI | _TBD_ | _TBD_ | `demos/gta6/`, `demos/common/` |
| 7 | Report | _TBD_ | _TBD_ | `report/` |

Khi có username, điền vào bảng trên và vào `.github/CODEOWNERS`.

## Thứ tự phụ thuộc

```
docs/interfaces.md (chốt ngày đầu)
        │
        ├──> dtracker/ (#3, #4) ──> experiments/ (#4) ──┐
        │                                              ├──> slides/ (#1, #2), report/ (#7)
        └──> data/ + demos/common/ (#5, #6) ──> demos/ ┘
```

Demo không phải chờ bản tự cài đặt xong: trong lúc chờ, demo chạy bằng code gốc (xem `third_party/`), vì cả hai dùng chung một định dạng dữ liệu.

## Bắt đầu

1. Đọc `CONTRIBUTING.md`.
2. Đọc `docs/paper_notes.md` và `docs/interfaces.md`.
3. Nhận issue của mình trên GitHub Project board, tạo branch, làm trong thư mục của mình.
