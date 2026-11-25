# Thiết kế: Tài liệu giải thích D-Tracker cho người mới

## Mục đích

Tạo một bản PDF bằng LaTeX giải thích lại paper **D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams** (arXiv:2505.00242v1) theo mạch bài giảng, để một sinh viên chưa có kiến thức nền về paper, tensor hay D-Tracker có thể tự đọc và hiểu ý tưởng, mô hình, thuật toán và thí nghiệm. Có hai phiên bản nội dung tương đương: tiếng Việt và tiếng Anh.

## Phạm vi và tiêu chí thành công

- Tài liệu độc lập, khoảng 25–35 trang mỗi ngôn ngữ, không phải slide thuyết trình.
- Bắt đầu từ trực giác và kiến thức nền; mỗi công thức quan trọng đều có giải thích bằng lời, ký hiệu và ví dụ đơn giản.
- Trình bày đủ bối cảnh, định nghĩa bài toán, kiến thức nền, mô hình, thuật toán tối ưu/streaming, thí nghiệm, kết luận, ưu điểm và hạn chế.
- Có hình từ paper kèm nguồn, sơ đồ giải thích, hộp ý chính/lỗi hiểu sai/câu hỏi tự kiểm tra, bảng thuật ngữ và bảng ký hiệu.
- Kết thúc bằng sơ đồ tổng quan và hướng dẫn đọc lại paper gốc.
- Mọi khẳng định và số liệu về paper phải được đối chiếu với nguồn; không trộn với kết quả reproduce chưa có.
- Cả hai bản phải biên dịch thành công và PDF được kiểm tra trực quan.

## Ngoài phạm vi

- Không dịch nguyên văn từng câu hoặc sao chép toàn bộ paper.
- Không reimplement thuật toán, chạy lại thí nghiệm hoặc tạo kết quả mới.
- Không sửa code mô hình, API, dữ liệu và các tài liệu nhóm ngoài phạm vi cần thiết.
- Không tạo bộ slide Beamer.

## Các phương án đã cân nhắc

1. **Bộ slide Beamer 40–50 trang chiếu mỗi ngôn ngữ:** phù hợp thuyết trình nhưng gãy mạch khi tự đọc; đã bị người dùng loại bỏ.
2. **Bài Explainer LaTeX `article`, hai ngôn ngữ:** mạch liên tục, có đủ chỗ giải thích nền và công thức; là phương án được chọn.
3. **Một bản song ngữ xen kẽ từng đoạn:** thuận tiện đối chiếu nhưng dài, dày chữ và khó đọc liên tục; không chọn.

## Quyết định triển khai

- Vị trí: `slides/paper_explore/`, độc lập với slide chung của nhóm.
- Hai nguồn chính: `dtracker_explained_vi.tex` và `dtracker_explained_en.tex`; mỗi file xuất một PDF cùng tên.
- Dùng LaTeX `article` với bố cục nhất quán; engine ưu tiên LuaLaTeX/XeLaTeX để hỗ trợ tiếng Việt. Chỉ giữ mã nguồn và tài nguyên trong repo, không cài package toàn cục.
- Hình paper đặt trong `slides/paper_explore/figures/`, ghi nguồn paper và số hình trong chú thích.
- Tái sử dụng định nghĩa LaTeX dùng chung nếu giúp hai bản đồng bộ, nhưng tránh phức tạp hóa cấu trúc.
- Có `README.md` và lệnh build đơn giản; không yêu cầu người đọc phải biết quy trình LaTeX trước.
- File thiết kế này được lưu tại `docs/superpowers/specs/2026-11-25-dtracker-paper-explained-design.md`; không tự commit git.

## Cấu trúc nội dung

1. Paper giải quyết vấn đề gì và tại sao quan trọng?
2. Ví dụ Google Trends và bức tranh tổng thể của D-Tracker.
3. Chuỗi thời gian, tensor, tensor stream và bài toán dự báo.
4. Phân rã tensor/Tucker qua ví dụ nhỏ.
5. Trend, seasonality và outlier.
6. Reaction–diffusion từ trực giác đến hệ phương trình.
7. Kết hợp các thành phần trong mô hình D-Tracker.
8. ALS/ModelEstimation và ý nghĩa từng bước cập nhật.
9. MDL, chọn số chiều, xử lý outlier và chuyển regime/ModelUpdate.
10. Thuật toán streaming, dự báo và độ phức tạp.
11. Thí nghiệm: dữ liệu, baseline, metric, kết quả và cách diễn giải hình.
12. Đóng góp, giả định, ưu điểm, hạn chế và các câu hỏi phản biện.
13. Tổng kết, câu hỏi tự kiểm tra có hướng dẫn và hướng dẫn đọc lại paper gốc.
14. Phụ lục thuật ngữ, ký hiệu và nguồn tham khảo.

## Quyền quyết định của người thực hiện

Người thực hiện có thể điều chỉnh số trang, thứ tự tiểu mục và số lượng sơ đồ để nội dung rõ ràng hơn, miễn giữ nguyên phạm vi, độ chính xác và tính tương đương giữa hai ngôn ngữ. Nếu môi trường không có TeX engine, dùng công cụ cục bộ/cách build cô lập và ghi rõ trong README, không cài đặt toàn cục.
