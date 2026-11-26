# D-Tracker — outline trình bày 35 phút

**Khán giả:** người chưa có kiến thức nền về tensor, chuỗi thời gian hay paper.
**Trọng tâm:** ứng dụng và trực giác; vẫn có toán, nhưng mỗi công thức đi sau một mô hình trực quan.
**Sản phẩm:** `dtracker_talk.pdf` (Beamer 16:9), trình bày khoảng 35 phút + Q&A.

## Nguyên tắc dẫn dắt

Mỗi khái niệm toán đi qua bốn lớp:

1. **Hình dung:** một hình, ẩn dụ hoặc câu hỏi.
2. **Nói bằng lời:** một câu không có ký hiệu.
3. **Công thức:** chỉ một công thức mới mỗi slide, chú thích từng ký hiệu.
4. **Kiểm tra:** thay số, hỏi ngược hoặc nối lại với quyết định thực tế.

Câu chuyện xuyên suốt: một đội marketing có dữ liệu tìm kiếm theo tuần của vài sản phẩm tại nhiều quốc gia, muốn biết **nơi nào quan tâm, lan từ đâu tới đâu, và tương lai ra sao**.

---

## Phần mở đầu — 2 phút

### Slide 1 — Tiêu đề
- **Thời lượng:** 0,5 phút.
- **Mục tiêu:** đặt đúng kỳ vọng: đây là bài giải thích, không phải phần đọc paper.
- **Nội dung:** “D-Tracker: hiểu dữ liệu quan tâm đang lan đi đâu”; tên paper, KDD 2025.
- **Visual:** nền navy, đường cong teal, một bản đồ chấm sáng.
- **Math:** không.
- **Lời dẫn:** “Hôm nay chúng ta sẽ đi từ một câu hỏi rất thực tế đến một mô hình toán, nhưng mỗi công thức sẽ chỉ xuất hiện sau khi ta đã nhìn thấy nó.”

### Slide 2 — Một sản phẩm, nhiều quốc gia
- **Thời lượng:** 1,5 phút.
- **Mục tiêu:** tạo nhu cầu trước khi giới thiệu phương pháp.
- **Nội dung:** ba câu hỏi: Ở đâu? Lan từ đâu sang đâu? Sắp tới thế nào?
- **Visual:** bản đồ thế giới với các điểm sáng; ba callout tương ứng ba câu hỏi.
- **Math:** không.
- **Lời dẫn:** “Nếu chỉ có một bảng Excel 50 cột, bạn sẽ không thấy được dòng chảy giữa các nơi.”
- **Chuyển ý:** “Trước khi trả lời, hãy xem dữ liệu thực sự có hình dạng gì.”

## Phần 1 — Dữ liệu và bài toán

### Slide 3 — Dữ liệu là một chồng bản đồ tuần
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** hiểu tensor bằng hình ảnh trước khi đọc ký hiệu.
- **Visual:** chồng 3–4 bảng nhỏ, mỗi bảng là heatmap từ khóa × quốc gia; trục thời gian bên cạnh.
- **Nói bằng lời:** “Mỗi tuần là một bản đồ nhiệt; xếp các bản đồ lại ta có một tensor.”
- **Math:** \(X_t\in\mathbb{R}^{k\times l}\), \(\mathcal X^c\in\mathbb R^{k\times l\times L_c}\), đầu ra \(\widehat X_{t_c+L_f}\).
- **Kiểm tra:** “8 từ khóa × 50 quốc gia × 104 tuần là bao nhiêu ô?” (41.600).
- **Lời dẫn:** “Tensor chỉ là cách nói ‘nhiều bảng xếp theo thời gian’.”

### Slide 4 — Vì sao khó, và D-Tracker làm gì
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** nêu ba thách thức và pipeline tổng.
- **Visual:** bốn biểu tượng thách thức; bên dưới là pipeline “tách tín hiệu → nén → mô phỏng lan truyền → dự báo”.
- **Nói bằng lời:** “Không phải thiếu dữ liệu; dữ liệu đang kể nhiều câu chuyện chồng lên nhau và thay đổi theo thời gian.”
- **Math:** chưa có; chỉ tên các khối.
- **Lời dẫn:** “Bây giờ đi vào từng khối, bắt đầu bằng việc tách tín hiệu.”

## Phần 2 — Cơ chế hoạt động

### Slide 5 — Ba lớp tín hiệu
- **Thời lượng:** 3 phút.
- **Mục tiêu:** hiểu vì sao phải tách trend, seasonal, outlier.
- **Visual:** một chuỗi quan sát được “bóc” thành ba dải màu: trend xanh, seasonal vàng, outlier đỏ.
- **Nói bằng lời:** “Xu hướng dài hạn, nhịp lặp theo mùa và cú sốc bất thường phải được nhìn riêng.”
- **Math:** \(\mathcal X^c\approx\widehat{\mathcal X}_d+\widehat{\mathcal X}_s+\widehat{\mathcal X}_o\).
- **Kiểm tra:** hỏi khán giả một cú tăng do khuyến mãi nên nằm ở lớp nào.
- **Lời dẫn:** “Tách xong, phần trend vẫn quá lớn để đọc; ta phải nén nó.”

### Slide 6 — Nén thành vài “kênh” ẩn
- **Thời lượng:** 2 phút.
- **Mục tiêu:** tạo trực giác Tucker mà không cần ký hiệu.
- **Visual:** ba “đài radio” phát ba kiểu tín hiệu; mỗi quốc gia/từ khóa có núm volume.
- **Nói bằng lời:** “Thay vì 400 chuỗi riêng, mô hình tìm vài kiểu diễn biến chung rồi trộn chúng.”
- **Math:** chưa có, chỉ khái niệm “kênh ẩn” và “trọng số”.
- **Lời dẫn:** “Cách trộn đó chính là một phép phân rã tensor.”

### Slide 7 — Tucker: từ kênh ẩn ra tensor
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** đọc được công thức Tucker và kích thước.
- **Visual:** sơ đồ lõi nhỏ × bảng từ khóa × bảng địa điểm; mũi tên “trải” theo hai chiều.
- **Nói bằng lời:** “Lõi nhỏ giữ các kênh; hai bảng hệ số nói kênh nào thuộc về ai.”
- **Math:** \(\widehat{\mathcal X}_d=\mathcal W^{core}\times_{key}W^{key}\times_{loc}W^{loc}\); một dòng elementwise.
- **Kiểm tra:** nêu shapes: \((d_k,d_l,L_c)\), \((d_k,k)\), \((d_l,l)\); so sánh 748 tham số với 41.600 ô.
- **Lời dẫn:** “Các kênh không đứng yên; chúng tăng giảm và lan sang nhau.”

### Slide 8 — Quan tâm lan như nước
- **Thời lượng:** 2 phút.
- **Mục tiêu:** hiểu diffusion bằng trực giác trước khi thấy ODE.
- **Visual:** hai bể nước thông nhau, mũi tên từ mức cao sang mức thấp; bản đồ nhóm địa điểm.
- **Nói bằng lời:** “Nơi đang cao sẽ đẩy sang nơi thấp; mô hình học ống nối nào mạnh.”
- **Math:** chưa có; chỉ ký hiệu \(w,w'\).
- **Cảnh báo:** “Đây là giả thuyết có cấu trúc, không tự động là nhân quả.”
- **Lời dẫn:** “Hãy viết điều vừa nhìn bằng một phương trình.”

### Slide 9 — Một phương trình, một bước số
- **Thời lượng:** 3 phút.
- **Mục tiêu:** đọc được hệ reaction–diffusion và kiểm tra bằng số.
- **Visual:** bên trái hai bể; bên phải công thức và một “dải tính”.
- **Math:** \(dw_{ij}/dt=a_{ij}w_{ij}+\sum_{j'} d_{ijj'}(w_{ij'}-w_{ij})\).
- **Nói bằng lời:** “Tự tăng/giảm cộng với lực kéo từ các nhóm khác.”
- **Ví dụ:** \(w=1,w'=4,a=0.1,d=0.5\) → \(1.6\); bước Euler thành \(2.6\).
- **Kiểm tra:** đổi \(w'=0\) để thấy dấu đổi chiều.

### Slide 10 — Một kênh ảnh hưởng đến chuỗi thật thế nào?
- **Thời lượng:** 1,5 phút.
- **Mục tiêu:** nối lõi ẩn với dữ liệu quan sát.
- **Visual:** một kênh → hai “núm” trọng số → một chuỗi từ khóa–quốc gia.
- **Math:** \(\widehat x_{uv}(t)=\sum_{i,j} w^{core}_{ij}(t)W^{key}_{iu}W^{loc}_{jv}\).
- **Nói bằng lời:** “Giá trị thật là tổng vài kênh, nhân với mức liên hệ của từng từ khóa và địa điểm.”
- **Lời dẫn:** “Còn mùa vụ và outlier được ghép vào đâu?”

### Slide 11 — Ghép thành mô hình hoàn chỉnh
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** thấy đủ ba thành phần và hệ tham số.
- **Visual:** sơ đồ ba tầng: dữ liệu = trend + seasonal + outlier; hộp tham số bên cạnh.
- **Math:** Eq. (4) seasonal; outlier thưa; \(\Theta=\{\theta_d,\theta_s,\widehat{\mathcal X}_o\}\), \(\mathcal F=\{\Theta_1,\dots,\Theta_N\}\).
- **Nói bằng lời:** “Một mô hình là một bộ quy tắc; nhiều mô hình là nhiều chương của cùng một bộ phim.”
- **Lời dẫn:** “Vậy làm sao tìm ra các tham số đó?”

### Slide 12 — ALS: sửa từng mảnh ghép
- **Thời lượng:** 2 phút.
- **Mục tiêu:** hiểu tinh thần tối ưu, không đi vào đạo hàm.
- **Visual:** vòng tròn bốn mảnh ghép: diffusion, hệ số trend, mùa vụ, outlier.
- **Math:** mục tiêu bình phương sai số; một công thức cập nhật đại diện.
- **Nói bằng lời:** “Giữ ba phần cố định, sửa phần còn lại; lặp đến khi ổn định.”
- **Cảnh báo:** “Không đảm bảo cực trị toàn cục.”
- **Lời dẫn:** “Còn một câu hỏi: bao nhiêu kênh và khi nào đổi mô hình?”

### Slide 13 — MDL và chuyển regime
- **Thời lượng:** 3 phút.
- **Mục tiêu:** hiểu tự động chọn độ phức tạp và thời điểm đổi mô hình.
- **Visual:** hai cột “chi phí mô hình” + “chi phí dữ liệu”; timeline ba regime.
- **Math:** \(\langle\mathcal X;\mathcal F\rangle=\langle\mathcal F\rangle+\langle\mathcal X\mid\mathcal F\rangle\).
- **Nói bằng lời:** “Mô hình nào mô tả cả mô hình lẫn dữ liệu bằng ít bit nhất.”
- **Kiểm tra:** tăng số kênh làm cột nào tăng, cột nào giảm.
- **Lời dẫn:** “Khi dữ liệu mới đến mỗi tuần, ta không muốn chạy lại từ đầu.”

### Slide 14 — Streaming: chỉ giữ cửa sổ gần nhất
- **Thời lượng:** 1,5 phút.
- **Mục tiêu:** hiểu vì sao chi phí không tăng theo chiều dài stream.
- **Visual:** băng chuyền: cửa sổ \(L_c\) → ước lượng → so chi phí → dự báo.
- **Math:** \(\mathcal X^c=\{X_{t_c-L_c+1},\dots,X_{t_c}\}\); Algorithm 1 dạng pseudo.
- **Nói bằng lời:** “Mỗi bước chỉ nhìn một cửa sổ cố định, không quét lại lịch sử.”
- **Cảnh báo:** “Không có nghĩa mọi phép tính là O(1).”

## Phần 3 — Ứng dụng và kết luận

### Slide 15 — Ba ứng dụng
- **Thời lượng:** 2,5 phút.
- **Mục tiêu:** nối mô hình với quyết định.
- **Visual:** ba thẻ: Marketing, Y tế công cộng, Sản phẩm/công nghệ.
- **Nội dung:** mỗi thẻ một câu hỏi → đầu ra D-Tracker → quyết định.
- **Ví dụ:** dồn ngân sách theo thị trường dẫn đầu; chuẩn bị nguồn lực theo vùng lan; phát hiện công nghệ đang lên.
- **Math:** không; chỉ ánh xạ output sang quyết định.

### Slide 16 — Bằng chứng và giới hạn
- **Thời lượng:** 1,5 phút.
- **Mục tiêu:** cân bằng giữa kết quả và cảnh báo.
- **Visual:** ba số lớn: 6 bộ dữ liệu, MAE tốt nhất, gần như không tăng thời gian; cạnh đó là biển “không phải nhân quả”.
- **Math:** không.
- **Nội dung:** 57% và 8× chỉ nói như paper báo cáo; dự báo điểm; phụ thuộc dữ liệu/cửa sổ.

### Slide 17 — Ba điều mang về
- **Thời lượng:** 1 phút.
- **Mục tiêu:** khép mạch.
- **Nội dung:** tách tín hiệu; nén thành vài kênh hiểu được; dự báo và thích nghi.
- **Visual:** ba dòng lớn, kết thúc bằng một câu hỏi mở.
- **Lời kết:** “D-Tracker biến bức tường số thành vài câu chuyện, một bản đồ lan truyền và một dự báo.”

## Backup kỹ thuật — dùng cho Q&A

### Slide A1 — Shapes và Tucker đầy đủ
- Công thức elementwise, kích thước từng tensor, giải thích mode product.

### Slide A2 — Eq. (1)–(4) và hệ tham số
- Bốn công thức mô hình, định nghĩa \(\theta,\theta_d,\theta_s,\Theta,\mathcal F\).

### Slide A3 — ALS và MDL chi tiết
- Eq. (5)–(9) ở mức đọc hiểu; chi phí MDL; điều kiện chọn model.

### Slide A4 — Kết quả paper và cách đọc
- Sáu dataset, MAE/RMSE, ablation, các điểm mơ hồ/typo, cách đọc bài giải thích dài.
