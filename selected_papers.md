# CS313 – Final Project: Danh sách paper được chọn

Yêu cầu: chọn 1 paper KDD (2022–2026), đọc hiểu, implement lại phương pháp, thuyết trình 30–35 phút và viết report 4 trang.

Tiêu chí lọc của nhóm:
- KDD 2025 trở về sau
- Không dùng LLM, mang tính data mining thuần
- Có ứng dụng thực tế rõ ràng, dễ demo trực quan
- Có code chính thức, chạy được trên GPU < 10GB hoặc CPU

> Lưu ý: chưa paper nào được clone và chạy thử. Cần kiểm tra code và dataset trước khi chốt.

## Tổng quan

| # | Paper | Hội nghị | Mảng | Paper | Code |
|---|---|---|---|---|---|
| 1 | NILMFormer | KDD 2025 (Applied Data Science Track) | Time series, năng lượng | [arXiv 2506.05880](https://arxiv.org/abs/2506.05880) | [GitHub](https://github.com/adrienpetralia/NILMFormer) |
| 2 | PatchSTG | KDD 2025 | Spatio-temporal, giao thông | [arXiv 2412.09972](https://arxiv.org/abs/2412.09972) | [GitHub](https://github.com/LMissher/PatchSTG) |
| 3 | D-Tracker | KDD 2025 | Tensor stream mining, hành vi xã hội | [arXiv 2505.00242](https://arxiv.org/abs/2505.00242) | [GitHub](https://github.com/Higashiguchi-Shingo/D-Tracker) |
| 4 | ModePlait | KDD 2025 | Causal discovery trên data stream | [arXiv 2502.08963](https://arxiv.org/abs/2502.08963) | [GitHub](https://github.com/C-Naoki/ModePlait) |

---

## 1. NILMFormer: Non-Intrusive Load Monitoring that Accounts for Non-Stationarity

- **Tác giả:** Adrien Petralia, Philippe Charpentier, Youssef Kadhi, Themis Palpanas (EDF R&D, Université Paris Cité)
- **Hội nghị:** KDD 2025, Applied Data Science Track
- **Paper:** https://arxiv.org/abs/2506.05880
- **Code:** https://github.com/adrienpetralia/NILMFormer
- **Slides của tác giả:** https://helios2.mi.parisdescartes.fr/~themisp/publications/kdd25-nilmformer-slides.pdf

### Dùng để làm gì
Bài toán **Non-Intrusive Load Monitoring (NILM)**, hay "tách điện năng": chỉ từ **một chuỗi điện tiêu thụ tổng** của cả nhà (đo bằng đồng hồ điện thông minh), ước lượng **từng thiết bị** (máy giặt, tủ lạnh, ấm đun nước, máy rửa bát…) đã tiêu thụ bao nhiêu điện và vào lúc nào, mà không cần lắp cảm biến riêng cho từng thiết bị.

### Phương pháp
- Mô hình **sequence-to-sequence dựa trên Transformer**: nhận vào chuỗi điện tổng, trả ra chuỗi điện của một thiết bị.
- Xử lý **tính không dừng (non-stationarity)** của dữ liệu điện. Mỗi đoạn con đầu vào được chuẩn hóa bằng cách trừ mean và chia std. Thông tin mean/std không bị bỏ đi mà được mã hóa thành token đưa vào mô hình, rồi dùng để "khôi phục thang đo" (de-stationarization) cho đầu ra.
- **TimeRPE:** positional encoding chỉ dựa trên timestamp (giờ, ngày, tháng), giúp mô hình biết thói quen dùng điện theo thời gian.
- Dataset công khai: UK-DALE, REFIT (cùng 2 dataset khác trong paper).

### Ứng dụng
- Đang được **triển khai thật tại EDF** (tập đoàn điện lực Pháp) trong dịch vụ theo dõi tiêu thụ, cung cấp thông tin chi tiết cho **hàng triệu khách hàng**.
- Hóa đơn điện chi tiết theo từng thiết bị, giúp người dùng biết thiết bị nào tốn điện nhất.
- Phát hiện thiết bị hỏng hoặc hoạt động bất thường (tủ lạnh chạy liên tục, bình nóng lạnh rò rỉ…).
- Hỗ trợ điện lực dự báo phụ tải và thiết kế chương trình tiết kiệm năng lượng.

### Ý tưởng demo
Dashboard (Streamlit): chọn một ngày, hiện biểu đồ điện tổng và các đường điện từng thiết bị do mô hình tách ra, kèm ước tính chi phí theo thiết bị.

---

## 2. PatchSTG: Efficient Large-Scale Traffic Forecasting with Transformers: A Spatial Data Management Perspective

- **Tác giả:** Yuchen Fang và cộng sự
- **Hội nghị:** KDD 2025
- **Paper:** https://arxiv.org/abs/2412.09972
- **Code:** https://github.com/LMissher/PatchSTG

### Dùng để làm gì
**Dự báo lưu lượng giao thông quy mô lớn**: dự báo lưu lượng xe trong tương lai cho **hàng nghìn cảm biến** trên mạng lưới đường cao tốc (ví dụ toàn bang California), một cách vừa chính xác vừa nhanh.

### Phương pháp
- Vấn đề: các mô hình spatio-temporal (GNN/Transformer) thông thường tính attention giữa mọi cặp cảm biến, chi phí bùng nổ khi số cảm biến lên đến hàng nghìn.
- Ý tưởng chính lấy từ **quản lý dữ liệu không gian**: dùng **cây KD-tree** để chia các cảm biến theo tọa độ địa lý thành các **"patch" không đều** (*irregular spatial patching*), sao cho các cảm biến gần nhau rơi vào cùng một patch.
- Mô hình Transformer xử lý theo hai tầng:
  - **depth attention:** attention bên trong mỗi patch, để học quan hệ cục bộ;
  - **breadth attention:** attention giữa các patch, để học quan hệ toàn cục.
- Kết quả: giảm mạnh số điểm phải tính toán động. Tác giả báo cáo training **nhanh hơn tới 10 lần** và **tiết kiệm bộ nhớ tới 4 lần**, vẫn đạt độ chính xác state-of-the-art.
- Dataset: LargeST (SD, GBA, GLA, CA). Bộ SD nhỏ, phù hợp GPU < 10GB.

### Ứng dụng
- Hệ thống giao thông thông minh: cảnh báo kẹt xe trước 1 giờ, điều chỉnh đèn tín hiệu.
- Ứng dụng bản đồ và gọi xe: ước tính thời gian di chuyển, gợi ý tuyến đường tránh kẹt.
- Quy hoạch đô thị: xác định các nút giao thông thường xuyên quá tải.
- Kỹ thuật chia patch không gian áp dụng được cho các mạng cảm biến lớn khác (chất lượng không khí, mạng điện, mạng nước).

### Ý tưởng demo
Bản đồ California có các điểm cảm biến đổi màu theo dự báo kẹt xe (animation theo giờ). Có thể vẽ các patch do KD-tree chia để minh họa ý tưởng chính của paper.

---

## 3. D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams

- **Tác giả:** Shingo Higashiguchi, Yasuko Matsubara, Koki Kawabata, Taichi Murayama, Yasushi Sakurai (Đại học Osaka)
- **Hội nghị:** KDD 2025
- **Paper:** https://arxiv.org/abs/2505.00242
- **Code:** https://github.com/Higashiguchi-Shingo/D-Tracker

### Dùng để làm gì
Mô hình hóa và dự báo **dữ liệu hoạt động xã hội** dạng tensor **(từ khóa × khu vực × thời gian)**, ví dụ lượng tìm kiếm Google Trends cho nhiều từ khóa ở nhiều bang hoặc quốc gia. Paper tự động **tìm ra các pattern ẩn** trong dữ liệu:
- **Xu hướng (trend):** mức độ quan tâm tăng hoặc giảm dài hạn;
- **Mùa vụ (seasonality):** chu kỳ lặp lại (theo tuần, theo năm);
- **Lan truyền quan tâm (interest diffusion):** một chủ đề nổi lên ở một khu vực rồi lan dần sang các khu vực lân cận;
- **Bất thường (outlier):** các đột biến bất ngờ (tin nóng, sự kiện đặc biệt).

Đồng thời dự báo xu hướng quan tâm trong tương lai.

### Phương pháp
- Kết hợp **phân rã tensor** với **phương trình phản ứng–khuếch tán (reaction-diffusion equation)**, loại phương trình vật lý mô tả cách một đại lượng lan truyền trong không gian.
- Tensor quan sát được tách thành các thành phần: trend, seasonal, diffusion giữa các vùng, và outlier.
- Thiết kế để hoạt động trên **luồng dữ liệu (stream)**: cập nhật mô hình liên tục khi có dữ liệu mới.
- Ưu điểm tác giả nêu:
  - **Diễn giải được:** các tham số có ý nghĩa rõ ràng (vùng nào lan sang vùng nào, mạnh bao nhiêu);
  - **Không cần chỉnh hyperparameter;**
  - **Mở rộng tốt:** thời gian chạy không tăng theo độ dài chuỗi.
- Không dùng deep learning, chạy được trên CPU.
- Dữ liệu thí nghiệm: Google Trends và dữ liệu ca nhiễm COVID-19.

### Ứng dụng
- **Marketing và quảng cáo:** biết trước khu vực nào sắp quan tâm đến sản phẩm hoặc trào lưu để chạy chiến dịch đúng nơi, đúng lúc.
- **Y tế công cộng:** theo dõi và dự báo dịch bệnh lan giữa các vùng (thí nghiệm COVID-19 trong paper).
- **Bán lẻ và chuỗi cung ứng:** chuẩn bị hàng theo mùa và theo vùng (ví dụ điều hòa vào mùa hè, quà tặng dịp lễ).
- **Truyền thông và mạng xã hội:** phân tích cách một chủ đề "viral" lan rộng, phát hiện sự kiện bất thường.

### Ý tưởng demo
- Tự tải dữ liệu Google Trends với các từ khóa vui (ví dụ "World Cup", "iPhone", "Pokémon"), có thể thử cả theo tỉnh/thành ở Việt Nam.
- Bản đồ animation thể hiện mức quan tâm lan dần giữa các vùng.
- Biểu đồ tách một chuỗi thành trend, mùa vụ và bất thường; dự báo vài tuần tiếp theo.

---

## 4. ModePlait: Modeling Time-evolving Causality over Data Streams

- **Tác giả:** Naoki Chihara, Yasuko Matsubara, Ren Fujiwara, Yasushi Sakurai (Đại học Osaka)
- **Hội nghị:** KDD 2025
- **Paper:** https://arxiv.org/abs/2502.08963
- **Code:** https://github.com/C-Naoki/ModePlait
- **Slides của tác giả:** https://c-naoki.vercel.app/assets/KDD2025/slides.pdf

### Dùng để làm gì
Cho nhiều chuỗi thời gian chạy song song (multivariate co-evolving data streams), ModePlait:
1. **Phát hiện quan hệ nhân quả** giữa các biến (biến nào ảnh hưởng đến biến nào);
2. Nhận ra khi **quan hệ nhân quả đó thay đổi theo thời gian** (*time-evolving causality*);
3. **Dự báo** giá trị tương lai dựa trên cấu trúc nhân quả đã học.

### Phương pháp
- Dữ liệu thực tế thường đi qua nhiều **"chế độ" (mode/regime)** khác nhau, mỗi chế độ có một cấu trúc nhân quả và động học riêng. Ví dụ: máy vận hành bình thường, máy bắt đầu xuống cấp, máy hỏng.
- ModePlait mô hình hóa mỗi chế độ bằng một hệ động học có cấu trúc nhân quả, và **tự động phát hiện thời điểm chuyển** giữa các chế độ (một dạng phân đoạn hoặc tìm pattern trên luồng dữ liệu).
- Hoạt động **trực tuyến (streaming)**: xử lý dữ liệu khi nó đến, thời gian chạy **không tăng theo độ dài luồng dữ liệu**.
- Tác giả báo cáo vượt các phương pháp state-of-the-art cả về phát hiện nhân quả biến đổi theo thời gian lẫn dự báo.
- Không dùng deep learning nặng, chạy được trên CPU.

### Ứng dụng
- **Công nghiệp và bảo trì dự đoán:** khi máy bình thường, nhiệt độ ảnh hưởng áp suất theo một cách; khi máy sắp hỏng, quan hệ đó thay đổi. Phát hiện sự thay đổi là tín hiệu để bảo trì sớm.
- **Kinh tế và tài chính:** quan hệ giữa các chỉ số (giá xăng, lạm phát, giá thực phẩm) thay đổi theo từng giai đoạn kinh tế.
- **Y tế:** các chỉ số sinh tồn của bệnh nhân ảnh hưởng lẫn nhau khác đi khi bệnh chuyển biến.
- **Hệ thống IT:** phát hiện khi quan hệ giữa các metric máy chủ (CPU, bộ nhớ, độ trễ) thay đổi bất thường.

### Ý tưởng demo
- Timeline dữ liệu được tô màu theo từng chế độ mà mô hình phát hiện.
- Đồ thị nhân quả (mũi tên giữa các biến) thay đổi khi chuyển sang chế độ mới.
- So sánh đường dự báo với giá trị thật.

---

## Bước tiếp theo
- [ ] Clone và chạy thử code của 4 paper, ghi lại kết quả và mức tài nguyên cần dùng
- [ ] Đọc kỹ paper, so sánh độ khó implement và độ dễ demo
- [ ] Nhóm chốt 1 paper
- [ ] Lập kế hoạch: implement, demo, slides (30–35 phút), report 4 trang, chia task cho các thành viên
