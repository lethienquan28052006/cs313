# D-Tracker — Outline slide (bản dựng lại)

> Paper: Higashiguchi et al., *D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams*, KDD 2025 (arXiv:2505.00242).
> Tổng thời gian: **35 phút** = **20 phút trình bày paper** + **15 phút demo** (slide demo để trống) + Q&A.
> Người nghe: biết ML/data mining cơ bản, **không** cần theo được chứng minh. Mỗi khái niệm đi theo thứ tự:
> **câu hỏi → trực giác/ví dụ → công thức tối thiểu → nói lại công thức bằng lời.**
> Phần tối ưu nặng toán → chỉ giữ ý tưởng ở main deck, công thức đầy đủ để ở **Appendix**.

---

## 0. Mạch kể chuyện (một câu cho mỗi phần)

1. **Vấn đề:** Lượt tìm kiếm theo *từ khóa × địa điểm × thời gian* rất có giá trị, nhưng nó là một luồng dữ liệu lớn, trộn nhiều loại tín hiệu và thay đổi liên tục.
2. **Ý tưởng:** Tách dữ liệu thành *xu hướng + lan truyền*, *mùa vụ*, *bất thường*; nén phần xu hướng vào vài “nhóm ẩn” và để một phương trình phản ứng–khuếch tán sinh ra nó.
3. **Tìm tham số:** Sửa lần lượt từng nhóm tham số (ALS); dùng MDL (“mô hình nào nén dữ liệu tốt nhất”) để tự chọn mọi thứ còn lại, kể cả lúc nào đổi mô hình.
4. **Kết quả:** Dự báo chính xác hơn, nhanh hơn, và *đọc được* câu chuyện lan truyền (ví dụ iPhone, pandas).

---

## 1. Bảng thời gian (phần paper = 20:00)

| # | Slide | Phần | Thời lượng | Cộng dồn |
|---|---|---|---|---|
| 1 | Cover | — | 0:30 | 0:30 |
| 2 | Vì sao quan tâm dữ liệu tìm kiếm? | I. Vấn đề | 1:00 | 1:30 |
| 3 | Vì sao khó? 3 thách thức | I | 1:15 | 2:45 |
| 4 | Dữ liệu là một tensor 3 chiều | I | 1:00 | 3:45 |
| 5 | Bài toán: Stream forecasting | I | 0:45 | 4:30 |
| 6 | Big picture: X_c ≈ X_d + X_s + X_o | II. Mô hình | 1:00 | 5:30 |
| 7 | Trend tensor: vì sao phải gom nhóm? | II | 1:00 | 6:30 |
| 8 | Phân rã Tucker: W(core), W(key), W(loc) | II | 1:15 | 7:45 |
| 9 | Phương trình phản ứng–khuếch tán | II | 1:15 | 9:00 |
| 10 | Trực giác: COVID-19 và iPhone | II | 1:00 | 10:00 |
| 11 | Từ phương trình đến W(core) và dự báo | II | 1:00 | 11:00 |
| 12 | Seasonal tensor | II | 1:00 | 12:00 |
| 13 | Outlier tensor + bộ tham số đầy đủ | II | 0:45 | 12:45 |
| 14 | Tìm tham số: vòng lặp streaming | III. Ước lượng | 0:45 | 13:30 |
| 15 | ModelEstimation = ALS | III | 1:00 | 14:30 |
| 16 | MDL trong một slide | III | 1:00 | 15:30 |
| 17 | ModelUpdate: đổi mô hình & đổi rank | III | 0:45 | 16:15 |
| 18 | Thiết lập thực nghiệm | IV. Thực nghiệm | 0:30 | 16:45 |
| 19 | Độ chính xác (Q1) | IV | 0:50 | 17:35 |
| 20 | Tốc độ (Q2) | IV | 0:35 | 18:10 |
| 21 | Khả năng diễn giải (Q3) | IV | 0:50 | 19:00 |
| 22 | Ablation: thành phần nào có ích? | IV | 0:30 | 19:30 |
| 23 | Takeaways & hạn chế | V | 0:30 | 20:00 |
| 24 | **DEMO** (trống) | — | 15:00 | 35:00 |
| 25 | Cảm ơn / Q&A | — | — | — |
| A1–A9 | Appendix (không tính giờ) | — | — | — |

Chỗ dự phòng nếu bị cháy giờ: slide 10 chỉ nói ví dụ iPhone (bỏ COVID), slide 22 lướt nhanh.

---

## 2. Chi tiết từng slide

Quy ước mỗi slide: **Mục tiêu** · **Trên slide** · **Hình** · **Lời nói** (ý chính) · **Nguồn** trong paper.

---

### Slide 1 — Cover
- **Trên slide:** Tên paper, tác giả, KDD 2025; tên môn, nhóm, GVHD, logo UIT.
- **Lời nói:** “Hôm nay nhóm trình bày một phương pháp dự báo mức độ quan tâm của người dùng tới một từ khóa, ở từng quốc gia, theo thời gian thực.”

---

## PHẦN I — VẤN ĐỀ (≈ 4 phút)

### Slide 2 — Vì sao quan tâm dữ liệu tìm kiếm?
- **Mục tiêu:** Cho người nghe thấy *giá trị ứng dụng* trước khi nói tới toán.
- **Trên slide:**
  - Social activity data: lượt tìm kiếm, lượt xem, bài đăng, số ca nhiễm… phản ánh **sự quan tâm** của con người.
  - 3 câu hỏi của một marketer (paper, §1):
    1. Người dùng ở **đâu** đang quan tâm sản phẩm?
    2. Sự quan tâm **lan** từ vùng nào sang vùng nào?
    3. Sắp tới mức quan tâm sẽ **thay đổi** thế nào?
  - Ứng dụng: dự báo nhu cầu, gợi ý, dịch tễ học, quảng cáo theo vùng.
- **Hình:** Figure 1(a) (đường Google Trends “iPhone” với đỉnh mỗi mùa thu). File: `figures/Figure1_a.png`.
- **Lời nói:** iPhone ra mắt mỗi mùa thu → đỉnh hằng năm; xu hướng khác nhau theo nước.
- **Nguồn:** §1, Figure 1(a).

### Slide 3 — Vì sao khó? (3 thách thức) và D-Tracker hứa gì
- **Trên slide:** hai cột.
  - *Thách thức* (§1):
    - (a) **Nhiều mẫu trộn lẫn:** xu hướng + mùa vụ + **lan truyền giữa các nước** + ngoại lai đột ngột.
    - (b) **Mẫu thay đổi theo thời gian:** lan truyền thường chỉ xảy ra một thời gian ngắn sau khi ra mắt sản phẩm → mô hình học từ quá khứ nhanh lỗi thời.
    - (c) **Nhiều chiều & vô hạn:** hàng chục từ khóa × ~50 nước × chuỗi thời gian không có điểm kết thúc.
  - *D-Tracker hứa* (Abstract):
    - **Interpretable** — đọc được trend & lan truyền.
    - **Automatic** — không có hyperparameter phải tinh chỉnh.
    - **Scalable** — thời gian xử lý mỗi bước **không phụ thuộc** độ dài luồng; chỉ cần cửa sổ dữ liệu gần nhất.
- **Hình (tùy chọn):** Bảng Table 1 rút gọn (D-Tracker vs DISMO, FluxCube, PatchTST, DeepAR… với 6 tiêu chí ✓).
- **Lời nói:** Nối (a)(b)(c) ↔ ba lời hứa. Không cần GPU hay huấn luyện lại cả lịch sử: mỗi bước chỉ làm việc trên cửa sổ gần nhất.
- **Lưu ý trung thực:** paper **không** khẳng định “chạy thuần CPU”; máy thí nghiệm có cả CPU Xeon và GPU A6000 (GPU dành cho baseline deep learning). Nói là: “mô hình nhỏ, tối ưu kiểu cổ điển, không cần deep learning” — không nói “paper chứng minh chạy trên CPU”.
- **Nguồn:** §1, Table 1, Appendix B.1.

### Slide 4 — Dữ liệu là một tensor 3 chiều
- **Mục tiêu:** Ký hiệu nền, đủ để theo phần sau.
- **Trên slide:**
  - Tại mỗi thời điểm t: ma trận X_t kích thước k × l, phần tử x_ij(t) = số lượt tìm từ khóa i tại địa điểm j.
  - Xếp các X_t theo thời gian: 𝓧 = {X_1, …, X_{t_c}} ∈ ℕ^{k×l×t_c} — **tensor bậc 3** (keyword × location × time).
  - t_c = thời điểm hiện tại, tăng dần → luồng “bán vô hạn”.
  - **Cửa sổ hiện tại:** 𝓧_c = X_{t_c−L_c : t_c} — chỉ giữ L_c bước gần nhất (giới hạn thời gian & bộ nhớ).
  - Ví dụ số: Device = 8 từ khóa × 50 nước × 676 tuần; L_c = 104 tuần (2 năm).
- **Hình:** TikZ khối lập phương 3 trục (Keyword / Location / Time), tô đậm “lát” cửa sổ L_c ở cuối trục thời gian; một “sợi” (fiber) được tô màu = 1 chuỗi thời gian (iPhone, Việt Nam).
- **Nguồn:** §3.1, Table 2, Table 4.

### Slide 5 — Bài toán: Stream forecasting
- **Trên slide:** Box “Problem 1”:
  - **Input:** cửa sổ 𝓧_c (L_c bước gần nhất), cập nhật mỗi khi có X_{t_c+1} mới.
  - **Output:** (1) các động thái thay đổi theo thời gian: **trend, mùa vụ, lan truyền quan tâm**; (2) dự báo X_{t_c+L_f} (L_f bước tới).
  - Làm liên tục, mỗi bước thời gian một lần.
- **Lời nói:** Khác bài toán forecasting thường ở hai điểm: phải *giải thích* được (không chỉ ra số) và phải *chạy theo luồng*.
- **Nguồn:** §3.1, Problem 1.

---

## PHẦN II — MÔ HÌNH D-TRACKER (≈ 8 phút)

### Slide 6 — Big picture: tách cửa sổ thành 3 thành phần
- **Mục tiêu:** Bản đồ cho cả phần II. Người nghe phải nhớ được slide này.
- **Trên slide:**
  - Thách thức chính: **trend và lan truyền bị che** bởi mùa vụ và ngoại lai.
  - Giả sử: **𝓧_c ≈ 𝓧̂_d + 𝓧̂_s + 𝓧̂_o** (Eq. 1), cả ba cùng kích thước k × l × L_c.
    - 𝓧̂_d — **Trend tensor:** xu hướng + lan truyền.
    - 𝓧̂_s — **Seasonal tensor:** mẫu lặp theo chu kỳ.
    - 𝓧̂_o — **Outlier tensor:** điểm bất thường, rất thưa.
- **Hình:** Một chuỗi đồ chơi (vẽ bằng pgfplots) = đường trend tăng dần + sóng sin + 2 gai nhọn → “=” ba đường con. Bên cạnh là Figure 2 thu nhỏ (`figures/overview.png`) làm mốc.
- **Lời nói:** “Ba slide tới mỗi slide xử lý một thành phần; trend là phần thú vị nhất.”
- **Nguồn:** §3.3, Eq. (1), Figure 2.

### Slide 7 — Trend tensor: vì sao phải gom nhóm?
- **Mục tiêu:** Trả lời “yếu tố ẩn là gì” bằng trực giác trước khi có công thức.
- **Trên slide:**
  - Nếu mô hình từng cặp (keyword, location) riêng: Device có 8 × 50 = **400 chuỗi** → nhiều tham số, dễ overfit, chậm, khó đọc.
  - Ý tưởng: gom **từ khóa → nhóm chủ đề ẩn**, **địa điểm → nhóm vùng ẩn**.
    - Ví dụ Device (Fig. 1b): d_k = 3 nhóm từ khóa, d_l = 2 nhóm vùng → chỉ **3 × 2 = 6 chuỗi ẩn**.
  - **Yếu tố ẩn (latent factor)** = một “nhóm mềm”: mỗi từ khóa/nước thuộc về các nhóm với một **mức độ** (không phải 0/1).
  - Lợi ích: tín hiệu mạnh hơn (gộp nhiễu), dễ diễn giải, tính nhanh hơn.
- **Hình:** Sơ đồ 400 đường mảnh rối → mũi tên → 6 đường đậm, có nhãn “nhóm Apple”, “nhóm Galaxy/iPad”… “nhóm Mỹ–EU–TQ”, “phần còn lại”.
- **Nguồn:** §3.3, Fig. 1(b).

### Slide 8 — Phân rã Tucker: W(core), W(key), W(loc)
- **Trên slide:**
  - **𝓧̂_d = 𝓦^(core) ×_key W^(key) ×_loc W^(loc)** (Eq. 2)
  - Kích thước:
    - 𝓦^(core) ∈ ℝ^{d_k × d_l × L_c} — **động thái ẩn** (latent dynamics): d_k·d_l chuỗi thời gian ẩn.
    - W^(key) ∈ ℝ₊^{d_k × k} — mỗi từ khóa “thuộc” nhóm từ khóa nào bao nhiêu.
    - W^(loc) ∈ ℝ₊^{d_l × l} — mỗi nước “thuộc” nhóm vùng nào bao nhiêu.
  - **Mode product nói bằng lời:** “×_key” = trộn các nhóm từ khóa thành từ khóa thật; “×_loc” = trộn các nhóm vùng thành nước thật. Cụ thể cho một phần tử:
    > x̂_uv(t) = Σ_i Σ_j W^(key)_{iu} · W^(loc)_{jv} · w_ij(t)
    → chuỗi “iPhone tại Việt Nam” = **tổng có trọng số** của các chuỗi ẩn.
  - Trọng số **không âm** → không “đảo dấu” câu chuyện → diễn giải được.
- **Hình:** TikZ: khối nhỏ W(core) ở giữa, hai ma trận mỏng W(key), W(loc) cắm vào hai trục → khối to 𝓧̂_d. Có thể đặt Figure 1(b) phần giữa (`figures/Wkey.png`, `figures/Wloc.png`) làm ví dụ thật.
- **Lời nói:** “Đây là phân rã Tucker không âm. Phần ‘mode product’ chính xác để ở Appendix A1.”
- **Nguồn:** §3.3, Eq. (2); interpretability đoạn sau Def. 2.

### Slide 9 — Phương trình phản ứng–khuếch tán
- **Mục tiêu:** Show công thức trước, rồi bóc từng thành phần (đúng yêu cầu).
- **Trên slide:**
  - Gốc vật lý/hóa học: ∂u_i/∂t = f(u_i) + Σ_j D·(u_j − u_i) — chất đi từ nơi **nồng độ cao** sang **nồng độ thấp**.
  - D-Tracker áp vào 𝓦^(core) (Eq. 3):
    > **dw_ij/dt = a_ij · w_ij  +  Σ_{j′} d_ijj′ · (w_ij′ − w_ij)**
    >  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*phản ứng* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*khuếch tán*
  - Chú thích (tô màu từng phần):
    - w_ij(t): mức quan tâm của **nhóm từ khóa i** tại **nhóm vùng j**.
    - a_ij: **tốc độ tăng trưởng tự thân**; a_ij > 0 tăng, a_ij < 0 giảm.
    - d_ijj′ ≥ 0: **cường độ lan** của nhóm từ khóa i **từ vùng j′ sang vùng j**. Nếu vùng j′ quan tâm nhiều hơn (w_ij′ > w_ij) thì w_ij được kéo lên.
    - Lan truyền chỉ xảy ra **giữa các nhóm vùng, cùng một nhóm từ khóa**.
  - Có d_k·d_l phương trình; tham số A ∈ ℝ^{d_k×d_l}, 𝓓 ∈ ℝ₊^{d_k×d_l×d_l}.
- **Hình:** Hai “bình” (vùng j′ đầy, vùng j vơi) nối bằng ống có mũi tên d_ijj′; mỗi bình có vòi riêng a_ij.
- **Nguồn:** §3.2, §3.3, Eq. (3).

### Slide 10 — Trực giác: COVID-19 và iPhone
- **Trên slide:** bảng 2 cột × 2 hàng (Phản ứng / Khuếch tán).
  - **COVID-19:**
    - Phản ứng a_ij: tốc độ lây *trong* một thành phố — nhanh hay chậm tùy chính sách giãn cách.
    - Khuếch tán d_ijj′: người dân di chuyển giữa các thành phố → dịch dần dịch chuyển từ vùng nặng sang vùng nhẹ.
  - **iPhone mới ra mắt:**
    - Phản ứng: sức hút tự thân tại một thị trường (quảng cáo, truyền thông).
    - Khuếch tán: sự quan tâm lan qua biên giới, từ Mỹ/EU/TQ sang các nước còn lại.
- **Hình:** Bản đồ lan truyền thật của paper cho iPhone 2019–2021, cắt từ Figure 1(b) (`figures/Figure1b_diffusion_2019.png`) — nối sang slide 21.
- **Lời nói:** Nhấn mạnh **giả định** của paper: quan tâm đi từ nơi cao sang nơi thấp, giống chất hóa học [55, 8].
- **Nguồn:** §3.2 (giả định lan truyền), §1.1 (iPhone). Ví dụ COVID là **minh họa của nhóm**, không phải kết quả paper — ghi chú nhỏ “ví dụ minh họa”.

### Slide 11 — Từ phương trình đến W(core) và dự báo
- **Trên slide:**
  - Cho A, 𝓓 và trạng thái đầu w_0 → **giải số** hệ phương trình theo từng bước:
    - chạy L_c bước → được 𝓦^(core) của cửa sổ hiện tại (**khớp dữ liệu**);
    - **chạy tiếp** L_f bước → động thái tương lai → nhân lại với W^(key), W^(loc) → **dự báo**.
  - **Definition 1:** θ = {A, 𝓓}; f_θ(θ, w_0, L) = sinh chuỗi 𝓦^(core) dài L từ w_0.
  - **Definition 2:** θ_d = {W^(key), W^(loc), θ} — toàn bộ tham số của trend tensor.
  - Đếm tham số (Device, d_k=3, d_l=2): A có 6 số, 𝓓 có 12 số → rất nhỏ so với 400 chuỗi × 104 tuần.
- **Hình:** Timeline: đoạn [t_c−L_c, t_c] liền nét (“fit”), đoạn (t_c, t_c+L_f] nét đứt (“forecast”), cùng một đường cong do ODE sinh ra.
- **Ghi chú:** phần “interpretability” (đạo hàm của từng chuỗi thật = chiếu đa tuyến tính của hệ ẩn) **không** trình bày ở main deck → Appendix A2.
- **Nguồn:** Def. 1, Def. 2.

### Slide 12 — Seasonal tensor
- **Trên slide:**
  - **𝓧̂_s = S^(time) ×_key S^(key) ×_loc S^(loc)** (Eq. 4) — thay vì lưu cả khối k × l × L_c, nén vào **3 ma trận 2 chiều** qua d_s mẫu mùa vụ ẩn:
    - S^(time) ∈ ℝ^{d_s × L_c}: d_s **đường cong chu kỳ chuẩn** (mỗi cột là một bước thời gian). *Ví dụ:* một mẫu “đỉnh mùa thu” (ra mắt sản phẩm), một mẫu “đỉnh cuối năm” (Black Friday/Giáng sinh).
    - S^(key) ∈ ℝ^{d_s × k}: từ khóa nào ăn khớp với mẫu nào. *Ví dụ:* iPhone, Apple Watch nặng ở mẫu “mùa thu”.
    - S^(loc) ∈ ℝ^{d_s × l}: mẫu đó mạnh/yếu ở nước nào. *Ví dụ:* mẫu “Black Friday” mạnh ở Mỹ, yếu ở Việt Nam; mẫu “Tết” chỉ ở các nước châu Á.
  - Mỗi phần tử: x̂ˢ_uv(t) = Σ_r S^(key)_{ru} · S^(loc)_{rv} · S^(time)_{rt}.
  - **Definition 3:** θ_s = {S^(time), S^(key), S^(loc)}.
  - (Ghi chú, nói sau ở Appendix: dạng này là phân rã CP; vì sao nén → ít tham số hơn, MDL ưa thích.)
- **Hình:** 3 thanh ma trận mỏng → “tích ngoài” → khối 3D; nhỏ bên cạnh là 2 đường sin mẫu.
- **Nguồn:** Eq. (4), Def. 3. Các ví dụ Black Friday/Tết là **minh họa của nhóm**.

### Slide 13 — Outlier tensor & bộ tham số đầy đủ
- **Trên slide:**
  - 𝓧̂_o: chỉ chứa giá trị bất thường; giả định **hiếm** → tensor **thưa** (hầu hết bằng 0).
  - **Definition 4:** Θ = {θ_d, θ_s, 𝓧̂_o} — *một mô hình* mô tả trend, lan truyền, mùa vụ, ngoại lai của **một giai đoạn**.
  - **Definition 5:** 𝓕 = {Θ_1, …, Θ_N} — tập các mô hình cho **N giai đoạn (regime)** khác nhau của luồng; khi hành vi đổi, D-Tracker “đổi mô hình”.
- **Hình:** Figure 1(a) với các đường chấm dọc = thời điểm đổi mô hình (`figures/Figure1_a.png`), mỗi đoạn tô một màu Θ_1, Θ_2, …
- **Chỉnh so với outline gốc:** F không phải “mỗi observation một Θ” mà là **mỗi giai đoạn một Θ**.
- **Nguồn:** Def. 4, Def. 5, Fig. 1(a).

---

## PHẦN III — TÌM THAM SỐ (≈ 3 phút 45, chỉ ý tưởng)

### Slide 14 — Vòng lặp streaming (Algorithm 1)
- **Trên slide:** flowchart một vòng lặp, mỗi khi có tuần mới:
  1. Cắt cửa sổ 𝓧_c.
  2. **ModelEstimation:** ước lượng một mô hình ứng viên Θ′ cho cửa sổ.
  3. **ModelUpdate:** giữ mô hình cũ hay thêm Θ′ (đổi giai đoạn)? Có đổi d_k, d_l, d_s không?
  4. **Forecast:** dự báo L_f bước tới.
- Hai câu hỏi chính: “*ước lượng thế nào?*” (slide 15) và “*chọn cấu trúc thế nào?*” (slide 16–17).
- Khởi tạo một lần: grid search (d_k, d_l) ∈ [2,4], d_s ∈ [0,4] theo cost MDL.
- **Nguồn:** §4, Algorithm 1, Appendix B.1.

### Slide 15 — ModelEstimation = Alternating Least Squares
- **Trên slide:** vòng tròn 4 ô, mỗi ô “sửa một nhóm, cố định phần còn lại”:
  1. **θ = {A, 𝓓} và w_0** — khớp ODE với phần dư 𝓧_c − 𝓧̂_s − 𝓧̂_o (bình phương tối thiểu phi tuyến, Levenberg–Marquardt).
  2. **W^(key), W^(loc)** — cập nhật nhân (multiplicative update) kiểu Nonnegative Tucker → luôn không âm.
  3. **S^(time), S^(key), S^(loc)** — CP-ALS trên phần dư 𝓧_c − 𝓧̂_d − 𝓧̂_o.
  4. **𝓧̂_o** — lấy phần dư 𝓧_c − 𝓧̂_d − 𝓧̂_s, **làm thưa**: chỉ giữ điểm nào giúp giảm tổng cost MDL → không cần ngưỡng tay.
  - Lặp đến hội tụ.
- **Câu chốt:** “Mỗi thành phần được khớp trên *phần dữ liệu mà hai thành phần kia chưa giải thích*.”
- Độ phức tạp: O(d_k·d_l² + k·d_k + l·d_l) — **không có L hay t_c** → không phụ thuộc độ dài luồng.
- **Công thức đầy đủ → Appendix A3–A5.**
- **Nguồn:** §4.1, Eq. (5)(6)(8), Lemma 1, Algorithm 2.

### Slide 16 — MDL trong một slide
- **Mục tiêu:** Người nghe hiểu MDL là gì và nó được dùng ở 3 chỗ.
- **Trên slide:**
  - Nguyên lý **Minimum Description Length:** mô hình tốt nhất là mô hình **nén dữ liệu ngắn nhất**.
  - Tổng cost: **⟨𝓧; 𝓕⟩ = ⟨𝓕⟩ + ⟨𝓧 | 𝓕⟩**
    - ⟨𝓕⟩: số bit để **lưu mô hình** (mỗi tham số khác 0 tốn ~32 bit + chỉ số vị trí).
    - ⟨𝓧 | 𝓕⟩: số bit để **lưu phần sai số** (sai số càng nhỏ càng ít bit, mã hóa Gaussian/Huffman).
  - Cân bằng tự nhiên: mô hình to → khớp tốt nhưng tốn bit lưu; mô hình nhỏ → rẻ nhưng sai số tốn bit.
  - **Dùng ở 3 chỗ:** (1) giữ điểm nào làm outlier; (2) chọn d_k, d_l, d_s; (3) có nên đổi mô hình không.
  - ⇒ Đây là lý do D-Tracker **không cần hyperparameter**.
- **Hình:** Cân hai đĩa: “bit mô hình” vs “bit sai số”; hoặc ví dụ: lưu 1 điểm outlier tốn ~32 bit + vị trí — chỉ đáng nếu nó tiết kiệm nhiều hơn thế ở phần sai số.
- **Nguồn:** §4.2, Eq. (7)(9)(10). Công thức chi tiết → Appendix A6.

### Slide 17 — ModelUpdate: khi nào đổi mô hình, đổi rank
- **Trên slide:**
  - So sánh cost: **giữ 𝓕 cũ** vs **thêm Θ′ mới**. Rẻ hơn → thêm Θ′ (đổi giai đoạn).
  - **RankUpdate:** thử tăng/giảm **một** trong d_k, d_l, d_s đúng 1 đơn vị (giả định cấu trúc đổi từ từ); chọn cái có cost thấp nhất.
  - Ví dụ thật: Pythonlib, d_k đổi từ 2 → 3 giữa 2013–2015 và 2020–2022 (Fig. 5).
- **Hình:** Timeline với các đỉnh nhỏ (spike) thời gian chạy khi RankUpdate xảy ra (preview Figure 4 trái).
- **Nguồn:** §4.3, Algorithm 3–4, §5 Q2/Q3.

---

## PHẦN IV — THỰC NGHIỆM (≈ 3 phút 15)

### Slide 18 — Thiết lập
- **Trên slide:** bảng gọn:
  - 6 dataset: 5 Google Trends (Device, Pythonlib, VoD, Chatapp, Language; tuần, 2010–2022, 676 bước, 7–9 từ khóa × 50 nước) + Covid-19 (ngày, 2020–2022, 990 bước, 2 chỉ số × 50 nước). Chuẩn hóa về [0, 1].
  - L_c = 104 tuần (Covid: 56 ngày); L_f ∈ {13, 26, 39} tuần (Covid: {7, 14, 21} ngày).
  - 7 baseline: DISMO, FluxCube (mô hình lan truyền/tensor), PatchTST, Autoformer, DeepAR, LaST, CoST (deep learning).
  - Metric: MAE, RMSE.
  - 3 câu hỏi: Q1 chính xác? Q2 nhanh? Q3 diễn giải được?
- **Nguồn:** §5, Table 4, Appendix B.1.

### Slide 19 — Q1: Độ chính xác
- **Trên slide:** Table 3 rút gọn: mỗi dataset 1 dòng (L_f = 26 hoặc giữa), cột D-Tracker / DISMO / PatchTST / tốt nhất của deep learning; tô đậm best.
  - Chốt: **MAE tốt nhất trên cả 6 dataset**; cải thiện tới **57%**; RMSE cạnh tranh.
  - Vì sao baseline thua: deep learning offline không kịp thích nghi khi trend đổi; DISMO bỏ qua phụ thuộc giữa các vùng và không đổi rank.
- **Lưu ý khi dựng:** lấy số trực tiếp từ Table 3 (đã có text trích), kiểm tra lại từng ô.
- **Nguồn:** Table 3, §5 Q1.

### Slide 20 — Q2: Tốc độ
- **Hình:** Figure 4 (`figures/scalability.png`, `figures/avgtime.png`).
- **Trên slide:** Thời gian mỗi bước **phẳng** theo độ dài luồng (spike nhỏ = RankUpdate); DISMO tăng dần, FluxCube rất chậm; D-Tracker nhanh nhất, **tới 8.0× nhanh hơn**.
- **Nguồn:** Figure 4, §5 Q2, §1.

### Slide 21 — Q3: Khả năng diễn giải
- **Hình:** Figure 1(b) đầy đủ — Device, 2 giai đoạn (`figures/Figure1_b.png`).
- **Trên slide (câu chuyện đọc được):**
  - 2010–2011: Dynamics #2 (gắn với “Galaxy”) tăng mạnh ở Đông Nam Á & Nam Mỹ; Dynamics #3 (Galaxy, iPad) lan từ Group 1 → Group 2.
  - 2019–2021: Dynamics #1 (“iPhone”) lan từ Mỹ, châu Âu, Trung Quốc (Group 1) → phần còn lại (Group 2).
  - (Tùy thời gian) Pythonlib: “pandas” lan từ Bắc Mỹ/Úc → châu Á (Fig. 5).
- **Lời nói:** Đây là thứ mà PatchTST/DeepAR không cho được: *ai lan sang ai*.
- **Nguồn:** §1.1, Fig. 1(b), Fig. 5.

### Slide 22 — Ablation
- **Hình:** Figure 3 (`figures/drop_rate.png`).
- **Trên slide:** bỏ diffusion → VoD, Chatapp tệ đi nhiều; bỏ seasonal → Device, Language, Covid tệ; bỏ outlier/RankUpdate → tệ ở một số dataset. Dataset ít mùa vụ/ít ngoại lai thì thành phần tương ứng không giúp.
- **Nguồn:** Figure 3, §5.

### Slide 23 — Takeaways & hạn chế
- **Takeaways (3 dòng):** Phân rã + ODE phản ứng–khuếch tán → **đọc được lan truyền**; MDL → **tự động**; cửa sổ + cập nhật tăng dần → **nhanh, không phụ thuộc độ dài luồng**.
- **Hạn chế / câu hỏi mở (nhận xét của nhóm):**
  - Lan truyền giữa **nhóm vùng ẩn**, không phải giữa từng nước; muốn nói “từ Mỹ sang Việt Nam” phải đọc qua W^(loc).
  - Phản ứng a·w là tăng/giảm **hàm mũ** → dự báo dài hạn có thể bùng nổ/tắt dần nếu không đổi mô hình.
  - Giả định quan tâm đi từ cao → thấp; sự kiện toàn cầu đồng thời (trailer, ra mắt cùng lúc) chưa chắc là “lan truyền”.
  - Mô hình chỉ có ý nghĩa khi dữ liệu đã chuẩn hóa; Google Trends là chỉ số tương đối.
- Chuyển tiếp: “Bây giờ nhóm demo trên dữ liệu thật…”

---

### Slide 24 — DEMO
- Slide gần như trống: chỉ tiêu đề “Demo” (+ tùy chọn: tên dataset demo). Nhóm tự bật demo, 15 phút.

### Slide 25 — Cảm ơn / Q&A
- Link paper, link code gốc (github.com/Higashiguchi-Shingo/D-Tracker), repo nhóm.

---

## APPENDIX (không tính giờ, dành cho người muốn đọc / thầy hỏi)

### Slide A1 — Mode product & unfolding
Định nghĩa ×_key, unfold, ví dụ kích thước Device. Nguồn: Eq. (2), Kolda & Bader.

### Slide A2 — Interpretability của θ_d
d𝓧_uv/dt = Σ_i Σ_j W^(key)_{iu} W^(loc)_{jv} [a_ij w_ij + Σ_j′ d_ijj′(w_ij′ − w_ij)]. Nguồn: đoạn sau Def. 2.

### Slide A3 — Cập nhật θ, w_0
Eq. (5), Levenberg–Marquardt, O(d_k d_l²). Nguồn: §4.1.1.

### Slide A4 — Cập nhật W^(key), W^(loc)
Eq. (6)(7), multiplicative update, khởi tạo NTD. Nguồn: §4.1.1, App. A.1.

### Slide A5 — Cập nhật S^(·)
Eq. (8), CP-ALS (Khatri–Rao, Hadamard, pseudoinverse). Nguồn: §4.1.2.

### Slide A6 — Cost MDL đầy đủ
Eq. (9)(10), c_F = 32 bit, log*. Nguồn: §4.2.

### Slide A7 — Algorithm 2 (ModelEstimation)
Pseudocode + Lemma 1. Nguồn: App. A.2–A.3.

### Slide A8 — ModelUpdate & RankUpdate
Algorithm 3–4. Nguồn: §4.3, App. A.4.

### Slide A9 — Table 3 đầy đủ
MAE/RMSE mọi dataset, mọi L_f; số đã đối chiếu tự động với text paper. Nguồn: Table 3.

---

## 3. Những điểm nhóm cần chỉnh so với outline gốc (đã kiểm với paper)

1. **Chiều lan truyền:** d_ijj′ > 0 nghĩa là **w_ij′ lan sang w_ij** (từ vùng j′ sang vùng j), không phải j → j′. Và i, j là **nhóm ẩn** (latent keyword group, latent location group), không phải từ khóa/nước thật.
2. **𝓕 = {Θ_1, …, Θ_N}** là các mô hình của **N giai đoạn**, không phải mỗi observation.
3. **Sinh 𝓦^(core):** chạy ODE **L_c bước** (độ dài cửa sổ), không phải t_c bước đầu tiên.
4. **Ai dùng NTD, ai dùng CP-ALS:** W^(key), W^(loc) → cập nhật kiểu Nonnegative Tucker [24] (NTD còn dùng để khởi tạo); S^(·) → CP-ALS [25]; θ → Levenberg–Marquardt. Outlier → làm thưa theo MDL.
5. **“Chạy thuần CPU / không cần nhiều dữ liệu”:** paper nói *không phụ thuộc độ dài luồng*, *chỉ giữ cửa sổ gần nhất*, *nhanh hơn tới 8×*; **không** nói chạy thuần CPU (máy thí nghiệm có GPU). Slide sẽ nói đúng mức paper nói.
6. Paper có typo “d_l ≪ k” (ý là d_l ≪ l) — slide viết đúng.
7. Kích thước W^(key) ∈ ℝ₊^{d_k×k}, W^(loc) ∈ ℝ₊^{d_l×l}, 𝓦^(core) ∈ ℝ^{d_k×d_l×L_c}; 𝓓 ∈ ℝ₊^{d_k×d_l×d_l}.

---

## 4. Cách dựng LaTeX

- Xóa nội dung `parts/*.tex` cũ; giữ khung build (`Makefile`, `latexmkrc`, Overleaf zip workflow); lịch sử cũ vẫn còn trong git.
- Cấu trúc mới:
  ```
  parts/00_cover.tex
  parts/01_problem.tex        # slide 2–5
  parts/02_model.tex          # slide 6–13
  parts/03_estimation.tex     # slide 14–17
  parts/04_experiments.tex    # slide 18–23
  parts/05_demo_qa.tex        # slide 24–25
  parts/99_appendix.tex       # A1–A9 (\appendix, đánh số A1…)
  ```
- Hình khái niệm (tensor, Tucker, hai bình khuếch tán, vòng ALS, cân MDL) vẽ bằng **TikZ**; hình kết quả **cắt từ paper** (đã có trong `slides/paper_explore/figures/`), ghi nguồn dưới hình.
- Cập nhật `outline.md`, `README.md`, `sources/source_map.md`, `sources/figure_manifest.tsv`, `scripts/check_deck.py` cho đúng số slide mới.
- Build bằng tectonic, render từng trang ra PNG để tự kiểm tra tràn chữ/chồng hình trước khi gửi.
