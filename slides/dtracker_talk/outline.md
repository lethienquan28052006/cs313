# D-Tracker — outline đồ án Data Mining

**Đối tượng:** sinh viên, chưa cần biết tensor, PDE hay time-series forecasting.
**Thời lượng:** 32 phút 45 giây cho 29 slide chính; còn khoảng 2 phút dự phòng trong giới hạn 35 phút. Bốn slide backup không tính giờ.
**Phạm vi:** paper gốc + outline + slide. Không phát biểu rằng nhóm đã cài đặt hay reproduce. Slide 28 Demo cố ý để trống phần nội dung.
**Phong cách:** academic-clean; hình/bảng cho dữ kiện, TikZ cho cấu trúc và cơ chế, chữ cho lập luận.

## Ví dụ xuyên suốt và quy ước đọc

Ví dụ giảng dạy giả định: theo dõi lượt tìm kiếm **iPhone** và **Galaxy** tại **Bắc Mỹ, châu Âu, Đông Nam Á** theo tuần. Các giá trị nhỏ 2, 4, 8… là **dữ liệu minh họa do nhóm tự tạo để kiểm tra phép tính**, không phải dữ liệu hay kết quả paper.

Mỗi khái niệm toán đi theo bốn lớp:

1. **Nhìn:** hình, bảng hoặc tình huống cụ thể.
2. **Nói:** một câu không dùng ký hiệu.
3. **Viết:** công thức tối thiểu, chú thích ký hiệu.
4. **Thử:** thay số hoặc nối về bài toán ban đầu.

Nguồn paper được kiểm chứng tại `sources/source_map.md`: arXiv:2505.00242v1, KDD 2025, 12 trang.

---

## A. Problem và big picture — 7 phút 15 giây

### Slide 1
- **Tên:** D-Tracker — Theo dõi sự lan tỏa của mối quan tâm.
- **Thời lượng:** 0:30.
- **Mục đích:** nêu paper và mục tiêu buổi trình bày.
- **Visual/message:** cover sáng; KDD 2025; phụ đề đồ án Data Mining.
- **Formula/check:** không.
- **Source:** PDF p. 1, bibliographic block.
- **Lời dẫn:** “Ta bắt đầu từ một bài toán marketing rất cụ thể, đi qua mô hình, rồi kết thúc bằng bằng chứng thực nghiệm.”

### Slide 2
- **Tên:** Problem — một bảng dữ liệu, ba câu hỏi.
- **Thời lượng:** 1:15.
- **Mục đích:** tạo motivation trước thuật ngữ.
- **Visual:** hai từ khóa iPhone/Galaxy và ba vùng; câu hỏi “đang tăng hay giảm?”, “có lan giữa vùng?”, “tuần tới ra sao?”.
- **Message:** mô hình cần vừa nén, vừa diễn giải, vừa cập nhật liên tục.
- **Formula/check:** không.
- **Source:** §1 p. 1, ví dụ marketing; câu chuyện cụ thể là minh họa.
- **Lời dẫn:** “Nếu chỉ có Excel, ta vẫn khó trả lời đồng thời ba câu hỏi này.”

### Slide 3
- **Tên:** Dữ liệu thực chất là một chồng bảng theo tuần.
- **Thời lượng:** 1:15.
- **Mục đích:** giải thích tensor bằng hình trước ký hiệu.
- **Visual:** hai lát bảng 2×3 ở tuần `t` và `t+1`; mũi tên thời gian.
- **Message:** mỗi tuần là một ma trận từ khóa × địa điểm; xếp theo thời gian thành tensor bậc ba.
- **Formula:** `X_t∈N^(k×l)`, `𝒳∈N^(k×l×t_c)`; ở ví dụ `k=2`, `l=3`.
- **Check:** một tuần có 6 ô; 104 tuần có 624 ô minh họa.
- **Source:** §3.1 p. 4; số ví dụ là minh họa.
- **Lời dẫn:** “Tensor ở đây không phải phép toán mới; đó là cách gọi chồng bảng có thứ tự thời gian.”

### Slide 4
- **Tên:** Problem 1 — stream forecasting.
- **Thời lượng:** 1:00.
- **Mục đích:** chốt input/output và lý do chỉ giữ cửa sổ gần nhất.
- **Visual:** băng chuyền tuần; cửa sổ `L_c`; mũi tên dự báo `L_f`.
- **Message:** tại mỗi thời điểm, dùng dữ liệu gần nhất để học quy luật đang thay đổi và dự báo tiếp.
- **Formula:** `𝒳^c={X_t}_(t=t_c−L_c+1)^(t_c)` → learn dynamics → `X̂_(t_c+L_f)`.
- **Check:** cận dưới `t_c−L_c+1` làm cửa sổ có đúng `L_c` phần tử; paper in cận dưới `t_c−L_c`, nên deck ghi rõ indexing convention thay vì copy công thức có thể đếm thành `L_c+1`. Cửa sổ 104 tuần, dự báo 13 tuần tương ứng cấu hình GoogleTrends của paper.
- **Source:** Problem 1 §3.1 p. 4; §5 Q1 p. 7.
- **Lời dẫn:** “Không cần giữ toàn bộ lịch sử trong bộ nhớ, nhưng vẫn phải thích nghi với hiện tại.”

### Slide 5
- **Tên:** Vì sao khó? Ba phức tạp chồng lên nhau.
- **Thời lượng:** 1:15.
- **Mục đích:** tách ba thách thức paper nêu.
- **Visual:** ba panel Complex patterns / Dynamic changes / High-dimensional stream.
- **Message:** trend, seasonality, diffusion, outlier cùng thay đổi trên nhiều chuỗi và thời gian không giới hạn.
- **Formula/check:** không.
- **Source:** §1 pp. 1–2.
- **Lời dẫn:** “Vấn đề không chỉ là nhiều dữ liệu; nhiều quy luật còn thay đổi và che lấp nhau.”

### Slide 6
- **Tên:** Lộ trình buổi trình bày.
- **Thời lượng:** 0:30.
- **Mục đích:** định hướng bốn phần tiếp theo.
- **Visual:** Method → Paper experiments → Reproduction → Demo.
- **Message:** đã có problem; tiếp theo là ý tưởng/cơ chế rồi bằng chứng.
- **Formula/check:** không.
- **Source:** cấu trúc do nhóm thiết kế.
- **Lời dẫn:** “Khi nghe phần method, chỉ cần nhớ mô hình đang trả lời lại ba câu hỏi ở slide đầu.”

### Slide 7
- **Tên:** Ý tưởng D-Tracker — nén, tách, thích nghi.
- **Thời lượng:** 1:30.
- **Mục đích:** nhìn toàn pipeline trước từng phương trình.
- **Visual:** input window → tách trend/seasonal/outlier → latent reaction–diffusion + factors → model update → forecast.
- **Message:** dùng tensor decomposition để nén và diễn giải; reaction–diffusion cho động học; MDL cho cập nhật tự động.
- **Formula:** sơ đồ khái niệm, chưa tính.
- **Check:** chỉ ra vị trí trả lời tăng/giảm, lan và dự báo trên pipeline.
- **Source:** §1 p. 2; Figure 2 p. 4; Algorithm 1 p. 5.
- **Lời dẫn:** “Ba động từ cần nhớ là nén, tách và thích nghi.”

## B. Methodology qua ví dụ — 12 phút 45 giây

### Slide 8
- **Tên:** Bóc một chuỗi quan sát thành ba lớp.
- **Thời lượng:** 1:15.
- **Mục đích:** hiểu decomposition trước Eq. (1).
- **Visual:** một chuỗi iPhone minh họa bóc thành trend tăng, seasonal lặp, outlier một cú sốc.
- **Message:** trend/diffusion, seasonality và outlier là ba loại tín hiệu khác nhau; mô hình không trộn chúng lại.
- **Formula:** chưa viết.
- **Check:** ra máy mới lặp hằng năm thuộc seasonal; sự kiện bất thường một lần thuộc outlier.
- **Source:** §1 p. 1 và §3.3 p. 4; ví dụ minh họa.
- **Lời dẫn:** “Muốn học xu hướng thật, trước hết đừng để mùa vụ và cú sốc che mắt.”

### Slide 9
- **Tên:** Eq. (1) — cộng ba lớp để khôi phục dữ liệu.
- **Thời lượng:** 1:00.
- **Mục đích:** đọc và kiểm tra công thức decomposition.
- **Visual:** ba thẻ giá trị minh họa 17 = 10 + 5 + 2.
- **Message:** tensor hiện tại được xấp xỉ bằng trend + seasonal + outlier.
- **Formula:** `𝒳^c≈𝒳̂_d+𝒳̂_s+𝒳̂_o`.
- **Check:** với một ô minh họa, d=10, s=5, o=2, tổng 17; outlier được giả định thưa.
- **Source:** Eq. (1) §3.3 p. 4; p. 5 sparse-outlier assumption.
- **Lời dẫn:** “Ba ký hiệu chỉ là nhãn của ba lớp ta vừa bóc ở slide trước.”

### Slide 10
- **Tên:** Nén — vài “giai điệu” chung thay hàng trăm chuỗi.
- **Thời lượng:** 1:00.
- **Mục đích:** giới thiệu latent dynamics và factors.
- **Visual:** hai giai điệu tăng/giảm + bảng trọng số trộn cho iPhone/Galaxy và ba vùng.
- **Message:** các chuỗi có thể dùng chung vài kiểu biến động, khác nhau ở mức liên hệ.
- **Formula:** chưa viết mode-product.
- **Check:** trọng số lớn nghĩa là chuỗi đó liên hệ mạnh hơn với latent pattern; factor không âm giúp giữ hướng diễn giải.
- **Source:** §3.3 Eq. (2) setup p. 4; interpretability p. 5.
- **Lời dẫn:** “Giống phối nhạc: ít track nền, mỗi chuỗi chỉ chỉnh âm lượng khác nhau.”

### Slide 11
- **Tên:** Tucker — trộn latent patterns để dựng lại tensor.
- **Thời lượng:** 1:15.
- **Mục đích:** giải thích Eq. (2) và shapes.
- **Visual:** `W(core)` × keyword-factor × location-factor → `X̂_d`; một phép trộn nhỏ.
- **Message:** lõi chứa động học nén; hai ma trận quyết định mỗi từ khóa/địa điểm nhận bao nhiêu từ mỗi kênh.
- **Formula:** `𝒳̂_d=𝒲^(core)×_key W^(key)×_loc W^(loc)`; shapes `(d_k×d_l×L_c)`, `(d_k×k)`, `(d_l×l)`.
- **Check:** một kênh latent mức 8, trọng số từ khóa 0.5 vị trí 0.25 đóng góp 1 vào chuỗi thật (minh họa một term).
- **Source:** Eq. (2) §3.3 p. 4; shapes.
- **Lời dẫn:** “Mode-product có thể hiểu là nhân trọng số rồi cộng các kênh, không cần học cú pháp tensor trước.”

### Slide 12
- **Tên:** Reaction + diffusion — tự đổi và ảnh hưởng lẫn nhau.
- **Thời lượng:** 1:30.
- **Mục đích:** trực giác hai thành phần động học trong một slide.
- **Visual:** hai bể nước A/B; vòi reaction làm mực nước tự tăng; ống diffusion từ cao sang thấp.
- **Message:** reaction mô tả tăng/giảm nội tại; diffusion mô tả liên hệ từ latent dynamics lân cận.
- **Formula:** sơ đồ `tự tăng/giảm + tổng(khác − hiện tại)`.
- **Check:** A=8, B=2 thì A kéo B lên và B kéo A xuống nếu hai hệ số dương.
- **Source:** §3.2 p. 4; §3.3 p. 5; ví dụ minh họa.
- **Cảnh báo:** diffusion trong mô hình không chứng minh quan hệ nhân quả.
- **Lời dẫn:** “Có hai lực: một lực tại chỗ, một lực do chênh lệch với hàng xóm.”

### Slide 13
- **Tên:** Eq. (3) — thay một bộ số để đọc reaction–diffusion.
- **Thời lượng:** 1:15.
- **Mục đích:** biến PDE thành phép tính dễ kiểm tra.
- **Visual:** hai thành phần reaction/diffusion được tô màu, rồi một bước Euler.
- **Message:** tốc độ thay đổi bằng tăng trưởng tại chỗ cộng ảnh hưởng chênh lệch.
- **Formula:** `dw_ij/dt=a_ij w_ij+Σ_j' d_ijj'(w_ij'−w_ij)`; chỉ dùng hai latent nodes trong ví dụ.
- **Check:** `w=2`, `w'=8`, `a=0.1`, `d=0.5`: reaction=0.2, diffusion=3, derivative=3.2; Euler bước 1 → 5.2 (minh họa).
- **Source:** Eq. (3) §3.3 p. 4; ý nghĩa hệ số p. 5.
- **Lời dẫn:** “Không cần giải PDE tay; trước hết hãy kiểm tra dấu và từng đại lượng.”

### Slide 14
- **Tên:** Ghép đủ model — trend, seasonal, outlier và nhiều regime.
- **Thời lượng:** 1:00.
- **Mục đích:** nối Eq. (2)–(4) và parameter hierarchy.
- **Visual:** cây `Θ={θ_d,θ_s,X̂_o}` → `ℱ={Θ_1,…,Θ_N}`.
- **Message:** seasonal cũng được nén bằng các factors; mỗi regime có một bộ tham số, stream có thể cần nhiều bộ.
- **Formula:** `𝒳̂_s=S(time)×_keyS(key)×_locS(loc)`; `θ_d`, `θ_s`, `Θ`, `ℱ` ở mức định nghĩa.
- **Check:** ra máy mới có chu kỳ lặp cùng từ khóa nhưng cường độ khác nhau theo vị trí.
- **Source:** Eq. (4) p. 5; Definitions 3–5 pp. 5–6.
- **Lời dẫn:** “Một bộ tham số mô tả một giai đoạn, không nhất thiết toàn bộ 12 năm.”

### Slide 15
- **Tên:** ModelEstimation — ALS sửa từng nhóm tham số.
- **Thời lượng:** 1:00.
- **Mục đích:** giải thích cách fit mà không chứng minh optimization.
- **Visual:** vòng bốn bước reaction–diffusion → trend factors → seasonal factors → outlier residual.
- **Message:** khi sửa một nhóm, tạm giữ các nhóm khác cố định, lặp đến hội tụ.
- **Formula:** mục tiêu tổng quát “giảm reconstruction error”; LM cho nonlinear reaction–diffusion, residual sparsification bằng MDL.
- **Check:** nếu đang cập nhật seasonal thì trend/outlier được tạm giữ vai trò residual đã biết.
- **Source:** §4.1 p. 6; Algorithm 2 Appendix A.2 p. 10.
- **Lời dẫn:** “Giống chỉnh một bản phối theo lượt: nhịp, giai điệu, âm lượng rồi loại nhiễu.”

### Slide 16
- **Tên:** MDL — chọn model đủ tốt nhưng không rườm rà.
- **Thời lượng:** 1:15.
- **Mục đích:** trực giác automatic structure selection.
- **Visual:** hai cột chi phí mô tả model + chi phí mã hóa dữ liệu; model quá ít/quá nhiều kênh.
- **Message:** thêm kênh thường giảm data-error cost nhưng tăng model cost; chọn tổng nhỏ hơn.
- **Formula:** `⟨𝒳;ℱ⟩=⟨ℱ⟩+⟨𝒳|ℱ⟩`.
- **Check:** model A cost 20+70=90; B cost 35+45=80; chọn B theo tổng cost (minh họa).
- **Source:** Eq. (10) §4.2 p. 6.
- **Lời dẫn:** “MDL giống nguyên tắc viết ghi chú: đủ chi tiết để hiểu nhưng không chép lại mọi thứ.”

### Slide 17
- **Tên:** Model switching + RankUpdate — thích nghi khi quy luật đổi.
- **Thời lượng:** 1:00.
- **Mục đích:** giải thích khi nào thêm regime và khi nào đổi số latent patterns.
- **Visual:** timeline hai regime; nhánh accept/reject candidate theo tổng cost; rank ±1 neighborhood.
- **Message:** chỉ thêm candidate nếu MDL giảm; sau đó thử rank lân cận để cập nhật cấu trúc.
- **Formula:** accept nếu `⟨𝒳^c;ℱ∪Θ'⟩<⟨𝒳^c;ℱ⟩`.
- **Check:** một đợt ra máy mới có thể làm quy luật mới xuất hiện, nhưng không khẳng định mọi product launch gây switch.
- **Source:** §4.3 p. 7; Algorithms 3–4 p. 11.
- **Lời dẫn:** “D-Tracker không đổi model vì cảm tính; nó so tổng chi phí trước và sau.”

### Slide 18
- **Tên:** Streaming — mỗi tuần mới đi qua ba bước.
- **Thời lượng:** 1:15.
- **Mục đích:** khép method thành thuật toán trực tuyến.
- **Visual:** window mới → ModelEstimation → ModelUpdate → Forecast → tuần tiếp theo.
- **Message:** tính toán trên cửa sổ gần nhất; candidate được fit lại, model/rank được cập nhật theo MDL, sau đó dự báo.
- **Formula:** `X^c → Θ' → {ℱ,ranks} → X̂_(t_c+L_f)`.
- **Check:** RankUpdate chạy nhiều lần ModelEstimation nên có spikes thời gian; “independent of stream length” không có nghĩa mọi bước O(1).
- **Source:** Algorithm 1 p. 5; Lemma 1 p. 6; §5 Q2 p. 8.
- **Lời dẫn:** “Đây là vòng lặp vận hành chứ không phải một lần train rồi đóng gói.”

## C. Experiments của paper — 7 phút 15 giây

### Slide 19
- **Tên:** Paper kiểm tra ba câu hỏi gì?
- **Thời lượng:** 1:15.
- **Mục đích:** nêu Q1–Q3 và protocol chính.
- **Visual:** Accuracy / Scalability / Effectiveness; thanh cấu hình MAE-RMSE, windows/horizons.
- **Message:** không chỉ forecast; paper còn kiểm tra thời gian và khả năng diễn giải.
- **Formula:** MAE/RMSE lower better; Table 3 scale `×10^-2`.
- **Check:** GoogleTrends `L_c=104`, horizons 13/26/39 tuần; Covid `L_c=56`, horizons 7/14/21 ngày.
- **Source:** §5 Q1–Q3 p. 7.
- **Lời dẫn:** “Đọc kết quả theo ba câu hỏi này, tránh chỉ nhìn một con số đẹp nhất.”

### Slide 20
- **Tên:** Sáu thực nghiệm trên GoogleTrends và Covid-19.
- **Thời lượng:** 1:15.
- **Mục đích:** mô tả datasets, baselines và chuẩn hóa.
- **Visual:** bảng 6 dòng tên dataset, shape, nhóm từ khóa; hàng badges 7 baselines.
- **Message:** năm chủ đề GoogleTrends + Covid-19; shapes Table 4 là `(time,keyword,location)`.
- **Formula:** normalization min=0,max=1.
- **Check:** Device `(676,8,50)`; Covid `(990,2,50)`; không thống nhất con số 48 vs 50 locations giữa prose/Table 4.
- **Source:** §5 Datasets p. 7; Table 4 p. 11.
- **Lời dẫn:** “Các shape đọc theo Table 4; đây là detail quan trọng khi reproduce.”

### Slide 21
- **Tên:** Q1 Accuracy — D-Tracker dẫn đầu MAE trong thiết lập paper.
- **Thời lượng:** 1:30.
- **Mục đích:** cho thấy kết quả định lượng mà không dồn cả bảng khổng lồ.
- **Visual:** native table một horizon mỗi loại dữ liệu, D-Tracker vs best baseline MAE, kèm tên baseline.
- **Message:** ở các cặp được chọn D-Tracker có MAE thấp hơn; paper cũng báo cáo best MAE trên tất cả datasets/horizons.
- **Formula/check:** Table 3 entries `×10^-2`; không gọi đây là kết quả reproduce.
- **Source:** Table 3 p. 8 và narrative §5 Q1 p. 7; full values trong `sources/source_map.md`.
- **Lời dẫn:** “Ta lấy một lát cắt để đọc số; backup có toàn bộ MAE/RMSE của D-Tracker qua 18 dòng.”

### Slide 22
- **Tên:** Ablation — mỗi thành phần giúp ở những dữ liệu khác nhau.
- **Thời lượng:** 1:00.
- **Mục đích:** hiểu đóng góp và tính phụ thuộc dataset.
- **Visual:** Figure 3 `drop_rate.png` có credit; ba takeaways bên cạnh.
- **Message:** seasonal hữu ích khi seasonality mạnh; diffusion nổi bật ở VoD/Chatapp; Language không hưởng lợi từ diffusion.
- **Formula/check:** ablation ở horizon 26 tuần/14 ngày; không đọc số trên bar nếu không cần.
- **Source:** Figure 3 + discussion §5 Q1 pp. 7–8.
- **Lời dẫn:** “Không có thành phần nào nên được tuyên truyền là luôn giúp mọi dữ liệu.”

### Slide 23
- **Tên:** Q2 Scalability — nhanh hơn, nhưng vẫn có RankUpdate spikes.
- **Thời lượng:** 1:00.
- **Mục đích:** trình bày wall-clock và average time với điều kiện đúng.
- **Visual:** callout lớn `up to 8.0×` cho claim paper và sơ đồ fixed-window → ModelEstimation → RankUpdate spikes; không nhúng hai dense plot không đọc được khi chiếu.
- **Message:** thời gian xử lý cửa sổ không tăng theo tổng độ dài stream trong thí nghiệm; RankUpdate tạo spikes vì fit nhiều candidates.
- **Formula/check:** paper nói fastest average time và “up to 8.0× faster”; gắn nhãn paper-reported.
- **Source:** Figure 4 §5 Q2 p. 8; claim §1 p. 3.
- **Lời dẫn:** “Đường gần phẳng không có nghĩa mỗi phép toán là hằng số; hãy nhìn cả các spikes.”

### Slide 24
- **Tên:** Q3 Effectiveness — factors giúp kể câu chuyện trong dữ liệu.
- **Thời lượng:** 1:15.
- **Mục đích:** nối output mô hình với diễn giải có kiểm chứng.
- **Visual:** crop vùng diffusion 2010–2011 từ paper Figure 1(b) có credit; ba bước `latent dynamics → keyword/location factor → diffusion`.
- **Message:** Device preview diễn giải Galaxy/iPad 2010–2011 qua latent groups và diffusion Group 1 → Group 2; đây là mô hình structural interpretation.
- **Formula/check:** factor cao = liên hệ mạnh hơn; không suy ra causal intervention.
- **Source:** §1.1 p. 2, Figure 1 caption/text; §5 Q3 p. 8 cho ý nghĩa effectiveness.
- **Lời dẫn:** “Giá trị của mô hình không chỉ là dự báo đúng, mà còn cho ngườidùng một cách đọc các nhóm và luồng diffusion.”

## D. Reproduction của nhóm — 2 phút 45 giây, chờ kết quả thật

### Slide 25
- **Tên:** Reproduction setup — khung cần ghi lại.
- **Thời lượng:** 1:00 khi có nội dung.
- **Mục đích:** chuẩn bị cấu trúc báo cáo reproducibility.
- **Visual:** hai cột paper target và team environment/config.
- **Message:** giữ đúng normalization, input window, horizons và init search; ghi code/data versions và hardware.
- **Formula/check:** paper-side values có source; team-side `—` được chú thích “Nhóm sẽ bổ sung sau khi chạy thực nghiệm”. Reproduction phải ghi rõ indexing `t_c-L_c+1…t_c` để giữ đúng `L_c` quan sát và đối chiếu với reference code.
- **Source:** §5 p. 7; Appendix B.1 p. 11.
- **Lời dẫn:** “Đây là protocol dự kiến, chưa phải tuyên bố rằng nhóm đã chạy.”

### Slide 26
- **Tên:** Reproduction results — Paper vs. nhóm.
- **Thời lượng:** 1:00 khi có nội dung.
- **Mục đích:** có bảng trống đúng chỗ để điền MAE/RMSE và so sánh cùng điều kiện.
- **Visual:** table paper reference và team result; cột team `—`.
- **Message:** không copy số paper thành số team; chỉ so cùng dataset/horizon/preprocessing.
- **Formula/check:** `— = Nhóm sẽ bổ sung sau khi chạy thực nghiệm`; paper column dùng Table 3 khi minh họa định dạng.
- **Source:** Table 3 p. 8 cho cột paper; cột nhóm chưa có dữ liệu.
- **Lời dẫn:** “Khi có kết quả, cần giữ rõ hai cột này độc lập.”

### Slide 27
- **Tên:** Reproduction analysis — điều gì giống và khác paper?
- **Thời lượng:** 0:45 khi có nội dung.
- **Mục đích:** sẵn khung cho runtime và lessons.
- **Visual:** ba panel Accuracy / Runtime-resources / Issues-adjustments.
- **Message:** báo cáo cả sai khác, môi trường và thay đổi cần thiết, không chỉ cherry-pick kết quả tốt.
- **Formula/check:** không đặt thời gian giả định; mỗi panel mang nhãn chờ kết quả nhóm.
- **Source:** khung phân tích do nhóm thiết kế, chưa phát sinh claim thực nghiệm.
- **Lời dẫn:** “Reproduce thành công hay chưa đều cần giải thích bằng cấu hình và log.”

## E. Demo và kết luận — 2 phút 45 giây

### Slide 28
- **Tên:** Demo.
- **Thời lượng dự kiến sau khi nhóm thêm nội dung:** 2:00.
- **Mục đích:** giữ chỗ cho sản phẩm nhóm.
- **Visual/message/formula/check:** cố ý trống phần nội dung; chỉ title/navigation/footer.
- **Source:** yêu cầu người dùng; không có implementation claim.
- **Lờidẫn:** nhóm tự bổ sung.

### Slide 29
- **Tên:** Ba điều mang về — Q&A.
- **Thời lượng:** 0:45 + thời gian hỏi đáp ngoài kịch bản.
- **Mục đích:** khép câu chuyện.
- **Visual:** 01 nén/tách; 02 reaction–diffusion diễn giải; 03 MDL streaming thích nghi.
- **Message:** D-Tracker biến tensor stream thành latent dynamics + factors + dự báo có thể cập nhật.
- **Formula/check:** nhắc lại ranh giới “interpretable diffusion ≠ causal proof”.
- **Source:** §6 p. 9.
- **Lời kết:** “Một câu: nén cho gọn, mô hình hóa cho hiểu, cập nhật cho hợp hiện tại.”

## Backup kỹ thuật — không tính giờ

### Slide A1
- **Tên:** Tensor/Tucker dimensions và lỗi in `d_l<<k`.
- Shape conventions, mode-product, nonnegative factors và lý do phải là `d_l<<l` theo kích thước. Source: Eq. (2) §3.3 p. 4.

### Slide A2
- **Tên:** Eq. (1)–(4), parameter hierarchy và initialization.
- Đầy đủ `θ,θ_d,θ_s,Θ,ℱ`; STL → PARAFAC seasonal; NTD trend factors. Source: §3 pp. 4–5; Appendix A.1 p. 10.

### Slide A3
- **Tên:** Algorithms, MDL và complexity.
- ModelEstimation bốn updates, ModelUpdate, RankUpdate ±1, c_F=32 bits, duplication trong printed Algorithm 4, giới hạn Lemma 1. Source: §4 pp. 5–7; Appendix A pp. 10–11.

### Slide A4
- **Tên:** Full D-Tracker Table 3 và protocol phụ.
- 18 dòng MAE/RMSE `×10^-2`, training/tuning periods và hardware. Source: Table 3 p. 8; Appendix B.1 p. 11.
