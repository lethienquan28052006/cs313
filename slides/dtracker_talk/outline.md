# D-Tracker — outline trình bày 35 phút

**Khán giả:** người chưa có kiến thức nền về tensor, chuỗi thời gian hay paper.
**Phong cách:** academic-clean, lấy cảm hứng từ seminar deck đại học: header breadcrumb, logo nhỏ góc phải, footer ba phần, nền sáng, Latin Modern Sans, mật độ chữ vừa phải.
**Trọng tâm:** ứng dụng và trực giác; vẫn có toán, nhưng mỗi công thức đi sau một mô hình trực quan.
**Sản phẩm:** `dtracker_talk.pdf` (Beamer 16:9), khoảng 35 phút + Q&A.

## Nguyên tắc dẫn dắt

Mỗi khái niệm toán đi qua bốn lớp:

1. **Hình dung:** một hình, ẩn dụ hoặc câu hỏi.
2. **Nói bằng lời:** một câu không có ký hiệu.
3. **Công thức:** một công thức mới, chú thích từng ký hiệu.
4. **Kiểm tra:** thay số, hỏi ngược hoặc nối lại với quyết định thực tế.

Câu chuyện xuyên suốt: một đội marketing có dữ liệu tìm kiếm theo tuần của vài sản phẩm tại nhiều quốc gia, muốn biết **nơi nào quan tâm, lan từ đâu tới đâu, và tương lai ra sao**.

---

## Mở đầu — 1,5 phút

### Slide 1 — Tiêu đề
- **Thời lượng:** 0,5 phút.
- **Mục tiêu:** đặt kỳ vọng: bài giải thích trực quan, không phải đọc paper.
- **Nội dung:** “D-Tracker: hiểu dữ liệu quan tâm đang lan đi đâu”; paper KDD 2025.
- **Visual:** nền sáng, title navy, thanh vàng dọc, monogram góc phải.
- **Math:** không.
- **Lời dẫn:** “Hôm nay ta đi từ một câu hỏi thực tế đến một mô hình toán, nhưng công thức chỉ xuất hiện sau khi đã nhìn thấy nó.”

### Slide 2 — Nội dung
- **Thời lượng:** 1 phút.
- **Mục tiêu:** tạo bản đồ 4 phần.
- **Visual:** bảng 4 dòng, số 01–04 màu vàng, mô tả ngắn.
- **Math:** không.
- **Lời dẫn:** “Bốn phần: dữ liệu, cơ chế, ứng dụng, kết luận.”

## Phần 1 — Dữ liệu và bài toán

### Slide 3 — Phần 01 overview
- **Thời lượng:** 0,2 phút.
- **Mục tiêu:** chuyển phần, nhắc ba ý sẽ học.
- **Visual:** số 01 lớn, danh sách ngắn.
- **Math:** không.

### Slide 4 — Một sản phẩm, 50 quốc gia
- **Thời lượng:** 1,5 phút.
- **Mục tiêu:** tạo nhu cầu trước khi giới thiệu phương pháp.
- **Nội dung:** Ở đâu? Lan từ đâu sang đâu? Sắp tới thế nào?
- **Visual:** bản đồ tín hiệu với các nhóm US/EU/CN/SEA; mũi tên lan truyền.
- **Math:** không.
- **Lời dẫn:** “Một bảng Excel không cho thấy dòng chảy giữa các địa điểm.”

### Slide 5 — Dữ liệu là một chồng bản đồ tuần
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** hiểu tensor bằng hình ảnh trước khi đọc ký hiệu.
- **Visual:** chồng ba heatmap tuần, trục thời gian.
- **Nói bằng lời:** “Mỗi tuần là một bản đồ nhiệt; xếp lại thành tensor.”
- **Math:** \(X_t\in\mathbb R^{k\times l}\), \(\mathcal X^c\in\mathbb R^{k\times l\times L_c}\), \(\widehat X_{t_c+L_f}\).
- **Kiểm tra:** 8 × 50 × 104 = 41.600 ô.

### Slide 6 — Vì sao khó, và D-Tracker làm gì
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** nêu ba thách thức và pipeline tổng.
- **Visual:** ba thẻ thách thức + pipeline bốn khối.
- **Math:** chưa có.
- **Lời dẫn:** “Không phải thiếu dữ liệu; dữ liệu đang kể nhiều câu chuyện chồng lên nhau.”

## Phần 2 — Cơ chế hoạt động

### Slide 7 — Phần 02 overview
- **Thời lượng:** 0,2 phút.
- **Visual:** số 02 lớn + ba ý: tách tín hiệu, nén/lan truyền, ước lượng streaming.

### Slide 8 — Tách ba lớp tín hiệu
- **Thời lượng:** 2,5 phút.
- **Visual:** một chuỗi quan sát bóc thành trend, seasonal, outlier.
- **Math:** \(\mathcal X^c\approx\widehat{\mathcal X}_d+\widehat{\mathcal X}_s+\widehat{\mathcal X}_o\).
- **Kiểm tra:** một cú tăng do khuyến mãi nên nằm ở lớp nào.

### Slide 9 — Nén thành vài “kênh” ẩn
- **Thời lượng:** 1,5 phút.
- **Visual:** ba đài radio + núm volume theo quốc gia/từ khóa.
- **Nói bằng lời:** “Thay vì 400 chuỗi riêng, mô hình tìm vài kiểu diễn biến chung rồi trộn chúng.”
- **Math:** chưa có, chỉ khái niệm kênh ẩn và trọng số.

### Slide 10 — Tucker: từ kênh ẩn ra tensor
- **Thời lượng:** 2,5 phút.
- **Visual:** lõi nhỏ × bảng từ khóa × bảng địa điểm.
- **Math:** \(\widehat{\mathcal X}_d=\mathcal W^{core}\times_{key}W^{key}\times_{loc}W^{loc}\).
- **Kiểm tra:** shapes; 748 tham số so với 41.600 ô.

### Slide 11 — Quan tâm lan như nước
- **Thời lượng:** 1,5 phút.
- **Visual:** hai bể nước thông nhau, mũi tên cao → thấp.
- **Nói bằng lời:** “Nơi cao đẩy sang nơi thấp; mô hình học ống nối nào mạnh.”
- **Cảnh báo:** lan truyền ≠ nhân quả.

### Slide 12 — Một phương trình, một bước số
- **Thời lượng:** 2,5 phút.
- **Math:** \(dw_{ij}/dt=a_{ij}w_{ij}+\sum d_{ijj'}(w_{ij'}-w_{ij})\).
- **Ví dụ:** \(w=1,w'=4,a=.1,d=.5\) → 1.6; bước Euler 2.6.
- **Kiểm tra:** đổi \(w'=0\) để thấy dấu đổi chiều.

### Slide 13 — Từ kênh ẩn đến chuỗi thật
- **Thời lượng:** 1,5 phút.
- **Visual:** kênh → trọng số từ khóa/địa điểm → chuỗi quan sát.
- **Math:** \(\widehat x_{uv}(t)=\sum w^{core}_{ij}(t)W^{key}_{iu}W^{loc}_{jv}\).
- **Nói bằng lời:** “Giá trị thật là tổng vài kênh, nhân mức liên hệ.”

### Slide 14 — Ghép thành mô hình hoàn chỉnh
- **Thời lượng:** 2 phút.
- **Visual:** ba thành phần + cây tham số.
- **Math:** Eq. (1), Eq. (4), outlier thưa; \(\Theta\), \(\mathcal F\).

### Slide 15 — ALS: sửa từng mảnh ghép
- **Thời lượng:** 2 phút.
- **Visual:** vòng tròn bốn mảnh ghép: diffusion, trend, seasonal, outlier.
- **Math:** mục tiêu bình phương sai số; 4 bước cập nhật.
- **Cảnh báo:** không đảm bảo cực trị toàn cục.

### Slide 16 — MDL và chuyển regime
- **Thời lượng:** 2 phút.
- **Visual:** hai cột chi phí mô hình/dữ liệu; timeline ba regime.
- **Math:** \(\langle\mathcal X;\mathcal F\rangle=\langle\mathcal F\rangle+\langle\mathcal X\mid\mathcal F\rangle\).
- **Kiểm tra:** tăng số kênh làm cột nào tăng/giảm.

### Slide 17 — Streaming
- **Thời lượng:** 1,5 phút.
- **Visual:** băng chuyền cửa sổ → ước lượng → so chi phí → dự báo; đồ thị runtime minh họa.
- **Math:** \(\mathcal X^c=\{X_{t_c-L_c+1},\dots,X_{t_c}\}\).
- **Cảnh báo:** không phải mọi phép tính là O(1).

## Phần 3 — Ứng dụng

### Slide 18 — Phần 03 overview
- **Thời lượng:** 0,2 phút.
- **Visual:** số 03 + Marketing/Y tế/Sản phẩm.

### Slide 19 — Ba ứng dụng
- **Thời lượng:** 2,5 phút.
- **Visual:** ba thẻ: Marketing, Y tế công cộng, Sản phẩm/công nghệ.
- **Nội dung:** mỗi thẻ Câu hỏi → Nhận gì → Quyết định gì.
- **Math:** không.
- **Cảnh báo:** luôn ghép chuyên gia miền; không suy luận nhân quả.

## Phần 4 — Kết luận

### Slide 20 — Phần 04 overview
- **Thời lượng:** 0,2 phút.
- **Visual:** số 04 + bằng chứng/giới hạn/takeaway.

### Slide 21 — Bằng chứng và giới hạn
- **Thời lượng:** 1,5 phút.
- **Visual:** ba số lớn + ba điều không được suy ra.
- **Nội dung:** 6 bộ dữ liệu; MAE tốt nhất theo paper; gần phẳng theo stream; 8.0×/57% là claim paper.
- **Cảnh báo:** nhân quả, bất định, phụ thuộc dữ liệu.

### Slide 22 — Ba điều mang về / Q&A
- **Thời lượng:** 1 phút.
- **Visual:** 01–03 lớn trên nền sáng; “Hỏi & đáp”.
- **Lời kết:** “D-Tracker biến bức tường số thành vài câu chuyện, một bản đồ lan truyền và một dự báo.”

## Backup kỹ thuật — Q&A

### Slide A1 — Tensor và Tucker đầy đủ
- Shapes, công thức elementwise, mode product, typo \(d_l\ll k\).

### Slide A2 — Bốn phương trình mô hình
- Eq. (1)–(4), định nghĩa \(\theta,\theta_d,\theta_s,\Theta,\mathcal F\).

### Slide A3 — ALS, MDL và streaming
- Quy trình ModelEstimation, chi phí MDL, rank update, cửa sổ \(L_c\).

### Slide A4 — Đọc kết quả paper
- Hình paper có credit, Table 3, 57%/8.0×, giả định và giới hạn.
