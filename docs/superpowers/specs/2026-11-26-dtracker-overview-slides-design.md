# Thiết kế: bộ slide overview D-Tracker

## Mục đích

Tạo một bộ Beamer tiếng Việt khoảng 35 phút để giới thiệu D-Tracker cho người chưa có kiến thức nền, tập trung vào ứng dụng và cách mô hình hoạt động. Vẫn dạy các ý tưởng toán cốt lõi, nhưng mỗi công thức phải được mở đường bằng hình ảnh, ẩn dụ và lời giải thích trước khi xuất hiện.

## Cấu trúc trải nghiệm

Mỗi khái niệm toán đi theo bốn lớp:

1. **Quan sát / ẩn dụ:** chồng bảng, ba lớp màu, đài radio, bể nước, vali, băng chuyền.
2. **Nói bằng lời:** một câu không ký hiệu.
3. **Công thức:** chỉ một công thức mới mỗi slide, có chú thích từng ký hiệu.
4. **Kiểm tra:** thay số cụ thể hoặc hỏi ngược để khán giả tự dự đoán.

## Phạm vi

- Khoảng 16 slide chính, 3 slide chuyển phần, 4 slide backup kỹ thuật.
- Thời lượng mục tiêu 35 phút + Q&A.
- Có các ý toán: tensor và bài toán dự báo; phân rã trend/seasonal/outlier; Tucker; reaction–diffusion; phép chiếu từ lõi ẩn; ALS; MDL; streaming.
- Có ứng dụng marketing, y tế công cộng, sản phẩm/công nghệ; có phần giới hạn và đạo đức diễn giải.
- Dùng hình paper có credit khi hữu ích; ưu tiên diagram TikZ để giải thích cơ chế.

## Ngoài phạm vi

- Không chứng minh định lý, không đi hết Eq. (5)–(9), không thay thế bài đọc 35 trang.
- Không trình bày kết quả reproduce chưa có.
- Không làm bản tiếng Anh trong phạm vi này.

## Quyết định triển khai

- Vị trí: `slides/dtracker_talk/`.
- `outline.md` là nguồn cấu trúc từng slide.
- `main.tex`: Beamer 16:9, tiếng Việt, theme tùy biến màu navy/teal/gold, font TeX Gyre, TikZ.
- `outline.md` dùng cùng thứ tự slide với `main.tex`; checker xác nhận số frame chính, placeholder, hình và cấu trúc.
- Build bằng Tectonic, tái sử dụng binary ở `../paper_explore/.tools/tectonic` nếu có, nếu không tải cục bộ.
- QA: compile sạch, không missing glyph/overfull, PDF đúng số trang, render kiểm tra bố cục.

## Nội dung chính

1. Mở đầu bằng câu hỏi ứng dụng.
2. Dữ liệu là chồng bản đồ tuần; tensor và bài toán.
3. Vì sao khó; pipeline tổng.
4. Ba lớp trend + seasonal + outlier và Eq. (1).
5. Trực giác nén thành vài “kênh”.
6. Tucker và phép chiếu, Eq. (2).
7. Trực giác diffusion như bể nước.
8. Eq. (3), một bước Euler bằng số.
9. Từ kênh ẩn ra chuỗi thật; mùa vụ, outlier và bộ tham số.
10. ALS như bốn mảnh ghép.
11. MDL và chuyển regime.
12. Streaming và dự báo.
13. Ba ứng dụng.
14. Bằng chứng và giới hạn.
15. Ba điều mang về.
16. Backup: công thức đầy đủ, ALS, MDL, bảng kết quả.
