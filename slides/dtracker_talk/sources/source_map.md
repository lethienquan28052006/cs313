# D-Tracker talk — source map

Bảng đối chiếu từng slide với paper. Mọi số liệu trên slide đều lấy từ paper. Ví dụ minh họa do nhóm tự đặt được ghi rõ ngay trên slide.

- Paper: Higashiguchi, Matsubara, Kawabata, Murayama, Sakurai. *D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams*. KDD 2025. arXiv:2505.00242v1. DOI `10.1145/3690624.3709192`.
- Bản PDF trong repo: `slides/paper_explore/sources/paper.pdf` (SHA-256 `8f3d301da12cbd17ec19cfcd6cb666654ded0fef06f57054826abf887ef9f715`).
- Code gốc: `https://github.com/Higashiguchi-Shingo/D-Tracker`.

## Slide → paper

| Slide | Nội dung | Nguồn trong paper | Ghi chú |
|---|---|---|---|
| 2 | Social activity data, 3 câu hỏi của marketer | §1 đoạn 1; Figure 1(a) | |
| 3 | 3 thách thức, 3 thuộc tính | §1 (a)(b)(c); Abstract; Table 1 | “Không khẳng định chạy thuần CPU”: Appendix B.1 ghi máy có cả Xeon CPU và RTX A6000 GPU |
| 4 | Tensor $k\times l\times t_c$, cửa sổ $\mathcal X_c$ | §3.1, Table 2, Table 4 | Device: (676, 8, 50); $L_c=104$ (§5 Q1) |
| 5 | Problem 1 | §3.1 | |
| 6 | $\mathcal X_c\approx\widehat{\mathcal X}_d+\widehat{\mathcal X}_s+\widehat{\mathcal X}_o$ | §3.3, Eq. (1), Figure 2 | Chuỗi đồ chơi là hình minh họa |
| 7 | Gom nhóm, $d_k\ll k$, $d_l\ll l$ | §3.3 trước Eq. (2); Figure 1(b) ($d_k=3$, $d_l=2$) | Paper có typo “$d_l\ll k$” |
| 8 | Tucker, kích thước, không âm | Eq. (2); đoạn “Interpretability of $\theta_d$” | |
| 9 | Phương trình phản ứng–khuếch tán | §3.2 (dạng tổng quát), Eq. (3), các bullet $a_{ij}$, $d_{ijj'}$ | $d_{ijj'}>0$: $w_{ij'}$ lan sang $w_{ij}$ |
| 10 | Ví dụ COVID / iPhone | §3.2 (giả định cao → thấp); §1.1 và Figure 1(b) (iPhone 2019–2021) | Ví dụ COVID là minh họa của nhóm |
| 11 | Def. 1, Def. 2; fit $L_c$ bước, forecast $L_f$ bước | Def. 1–2; Algorithm 1 | Số tham số $A$, $\mathcal D$ tính từ $d_k=3$, $d_l=2$ |
| 12 | Seasonal tensor, Def. 3 | Eq. (4), Def. 3 | Black Friday / Tết là minh họa của nhóm |
| 13 | Outlier thưa, Def. 4–5, đổi mô hình | §3.3, Def. 4–5, Figure 1(a) | |
| 14 | Algorithm 1; grid search khởi tạo | §4, Algorithm 1; Appendix B.1 “Hyperparameter tuning” | |
| 15 | ALS, LM, multiplicative update, CP-ALS, sparsify; Lemma 1 | §4.1.1–4.1.3, Eq. (5)(6)(8), footnote 1, Lemma 1 | |
| 16 | MDL | §4.2, Eq. (9)(10), footnote 2 ($c_F=32$) | |
| 17 | ModelUpdate, RankUpdate; Pythonlib $d_k$: 2 → 3 | §4.3; §5 Q2 (gai thời gian); §5 Q3 | |
| 18 | Dataset, $L_c$, $L_f$, baseline, metric | §5; Table 4; Appendix B.1 | |
| 19 | Table 3 đầy đủ (chuyển từ Phụ lục) | Table 3; Appendix B.1 | Script kiểm tra 18/18 dòng; ô tô đậm = nhỏ nhất theo từng metric |
| 20 | Table 3 rút gọn; “tới 57%” | Table 3; §1 | 57% = Covid-19, $L_f=7$: 1 − 0.47/1.10 |
| 21 | Scalability, “tới 8.0×” | Figure 4; §5 Q2; §1 | |
| 22 | Diễn giải Device 2010–2011 / 2019–2021; pandas | §1.1, Figure 1(b); §5 Q3, Figure 5 | |
| 23 | Ablation | Figure 3; §5 “Ablation study” | Số % đọc từ nhãn trên cột của Figure 3 |
| 24 | Kết quả nhóm reproduce | Cột Paper: Table 3 (D-Tracker, $L_f$ giữa) | Cột Nhóm do nhóm tự điền, không phải số của paper |
| 25 | Takeaways; hạn chế | §6 | Hạn chế là nhận xét của nhóm |
| A1–A8 | Công thức đầy đủ | Eq. (2)–(10); Appendix A.1–A.4 | |

## Đối chiếu tự động Table 3

Bảng ở slide 19, 20 và cột Paper ở slide 24 được so với text trích từ `paper.pdf` (`pdftotext`). Thứ tự cột của paper: D-Tracker, DISMO, FluxCube, PatchTST, Autoformer, DeepAR, LaST, CoST; mỗi phương pháp có MAE ×3 rồi RMSE ×3. Kết quả: 18/18 dòng khớp. Ô tô đậm đúng là giá trị nhỏ nhất theo từng metric, và D-Tracker có MAE nhỏ nhất ở cả 18 dòng.

## Hình

Xem `figure_manifest.tsv`.
