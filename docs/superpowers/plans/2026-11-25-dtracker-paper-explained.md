# D-Tracker Paper Explainer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo hai tài liệu PDF LaTeX tiếng Việt và tiếng Anh, mỗi bản khoảng 25–35 trang, giải thích D-Tracker từ kiến thức nền cho người mới.

**Architecture:** Mỗi ngôn ngữ có một file điều phối và các chương `.tex` riêng, dùng chung style, tài nguyên hình và tài liệu tham khảo. Một bản ghi nguồn trung gian khóa mọi công thức/số liệu với vị trí trong paper; script kiểm tra cấu trúc giúp hai ngôn ngữ đồng bộ và quy trình build cục bộ tạo PDF mà không cài package toàn cục.

**Tech Stack:** LaTeX `article`, LuaLaTeX/XeLaTeX hoặc Tectonic, TikZ, `tcolorbox`, `booktabs`, `hyperref`, Python 3 standard library cho kiểm tra, công cụ render PDF trong môi trường cô lập khi cần.

**Spec:** `docs/superpowers/specs/2026-11-25-dtracker-paper-explained-design.md`

## Global Constraints

- Tài liệu là bài giải thích độc lập, **không phải slide**, không dịch nguyên văn và không reimplement thuật toán.
- Hai bản tiếng Việt/tiếng Anh tương đương về chương, công thức, hình, số liệu và câu hỏi tự kiểm tra.
- Công thức quan trọng phải có giải thích bằng lời, ký hiệu và ví dụ đơn giản; số liệu phải đối chiếu arXiv:2505.00242v1.
- Chỉ tạo/sửa file trong phạm vi thiết kế; không cài package toàn cục, không chạy git mutation nếu chưa được yêu cầu riêng.
- Không mô tả kết quả reproduce chưa tồn tại; phân biệt rõ kết quả paper, diễn giải của tài liệu và hạn chế suy luận.

## Review Focus

- **Sai công thức/số liệu:** độc giả có thể truy ngược từng mục về paper; Task 1 tạo source map và Tasks 3–7 đối chiếu source map khi kiểm tra.
- **Chữ đúng nhưng người mới không hiểu:** mỗi phần nền/mô hình phải có trực giác, ví dụ cụ thể và cảnh báo nhầm lẫn; Tasks 3–6 kiểm tra theo checklist nội dung.
- **Hai bản lệch nội dung:** các file chương có cùng tên và cùng label; Task 7 chạy `python3 scripts/check_documents.py` và đối chiếu thủ công bản tóm tắt.
- **PDF lỗi tiếng Việt/hình/tràn dòng:** Task 2 smoke-build và Task 7 clean-build; log không có lỗi, trang PDF được render và đọc trực quan.
- **Nguồn hình không rõ:** Task 1 ghi URL, caption, license và SHA-256; Task 7 kiểm tra mọi hình được tham chiếu và có credit.

---

### Task 1: Khóa nguồn paper và tài nguyên hình

**Files:**
- Create: `slides/paper_explore/sources/paper.html`
- Create: `slides/paper_explore/sources/paper.pdf`
- Create: `slides/paper_explore/sources/source_map.md`
- Create: `slides/paper_explore/sources/figure_manifest.tsv`
- Create: `slides/paper_explore/figures/*`

**Interfaces:**
- Produces: đường dẫn hình ổn định `figures/<paper-file-name>` và bảng `source_map.md` theo mục paper, dùng bởi mọi chương.

- [ ] **Step 1: Tải nguồn paper và liệt kê toàn bộ hình**

Dùng `curl -fL` tải đúng URL arXiv HTML/PDF phiên v1. Trích URL ảnh từ HTML, tải các hình có giá trị giải thích; ghi tên file, URL tuyệt đối, số hình, caption ngắn và SHA-256 vào `figure_manifest.tsv`.

- [ ] **Step 2: Kiểm tra tài nguyên tải về**

Chạy `file sources/paper.pdf figures/*`; xác nhận PDF hợp lệ và mọi hình có định dạng ảnh, kích thước lớn hơn 0. Đọc trực quan các hình chính trước khi dùng.

- [ ] **Step 3: Viết bản đồ nguồn**

Ghi metadata tác giả/DOI/license; tóm tắt và trích vị trí cho Problem 1, Eq. (1)–(12), Algorithms 1–3, Tables 1–4, Figures 1–5, độ phức tạp, thiết lập thí nghiệm, sáu dataset, baseline, metric và các claim `57%`, `8.0x`. Nêu rõ typo/điểm mơ hồ của paper thay vì âm thầm sửa.

- [ ] **Step 4: Đối chiếu tính đầy đủ của nguồn**

So sánh mục lục HTML với `source_map.md`: không bỏ Section 1–6, Appendix A–B; mọi số liệu dự kiến dùng đã có vị trí trích dẫn.

### Task 2: Khung LaTeX song ngữ và quy trình build cục bộ

**Files:**
- Create: `slides/paper_explore/dtracker_style.tex`
- Create: `slides/paper_explore/dtracker_explained_vi.tex`
- Create: `slides/paper_explore/dtracker_explained_en.tex`
- Create: `slides/paper_explore/Makefile`
- Create: `slides/paper_explore/scripts/install_tectonic.sh`
- Create: `slides/paper_explore/scripts/check_documents.py`
- Create: `slides/paper_explore/.gitignore`

**Interfaces:**
- Produces: môi trường `keypoint`, `plainwords`, `commonmistake`, `selfcheck`, `\sourcefig[options]{file}{caption}{label}` và các lệnh build `make vi`, `make en`, `make all`, `make check`.
- Consumes: hình trong Task 1.

- [ ] **Step 1: Viết smoke test cấu trúc trước nội dung**

`check_documents.py` phải fail khi thiếu file chính, input chương không tồn tại, label trùng trong cùng ngôn ngữ, placeholder `TODO|TBD`, hoặc danh sách chapter/self-check khác nhau giữa hai ngôn ngữ. Ban đầu chạy và xác nhận FAIL do chưa có skeleton.

- [ ] **Step 2: Tạo preamble và hai tài liệu tối thiểu**

Dùng engine Unicode, A4, font có dấu Việt, `microtype`, toán AMS, bảng đẹp, đồ họa/TikZ, hộp màu và hyperlink. Main VI/EN chứa title, ngày phiên bản, tuyên bố “tài liệu giải thích, không phải paper gốc”, TOC và input các chương theo cùng danh sách.

- [ ] **Step 3: Tạo build cục bộ và quy tắc ignore**

Installer chỉ đặt Tectonic vào `slides/paper_explore/.tools/` khi máy chưa có engine; script kiểm tra kiến trúc và SHA-256 nếu nguồn phát hành cung cấp. Build ra `build/`, copy hai PDF cuối về thư mục gốc; ignore công cụ/cache/log nhưng giữ nguồn, hình và PDF cuối.

- [ ] **Step 4: Chạy smoke test và build**

Chạy `python3 scripts/check_documents.py`, `make vi`, `make en`. Mong đợi PASS và hai PDF mở được, tiêu đề/dấu tiếng Việt đúng; sửa mọi LaTeX error trước khi qua task sau.

### Task 3: Bối cảnh, bài toán và kiến thức nền

**Files:**
- Create: `slides/paper_explore/sections_vi/01_orientation.tex`
- Create: `slides/paper_explore/sections_vi/02_data_and_problem.tex`
- Create: `slides/paper_explore/sections_vi/03_tensor_primer.tex`
- Create: `slides/paper_explore/sections_en/01_orientation.tex`
- Create: `slides/paper_explore/sections_en/02_data_and_problem.tex`
- Create: `slides/paper_explore/sections_en/03_tensor_primer.tex`

**Interfaces:**
- Consumes: style/build Task 2, `source_map.md` Task 1.
- Produces: các label `sec:orientation`, `sec:problem`, `sec:tensor-primer` giống nhau ở hai ngôn ngữ.

- [ ] **Step 1: Viết VI từ trực giác đến định nghĩa**

Giải thích động lực, ví dụ keyword × location × time, stream/window/horizon, ba thách thức và ba tính chất Interpretable/Automatic/Scalable. Đưa Problem 1 về câu hỏi đầu vào–đầu ra; dùng Figure 1 và 2 kèm credit.

- [ ] **Step 2: Thêm primer không giả định kiến thức nền**

Dùng bảng số nhỏ để giải thích scalar/vector/matrix/tensor, chỉ số và shape; minh họa trend/seasonal/outlier bằng một chuỗi tự tạo được đánh dấu “ví dụ minh họa”. Giải thích Tucker/mode product bằng phép trộn có trọng số và ví dụ `2×2×3`, không chỉ phát biểu công thức.

- [ ] **Step 3: Viết EN tương đương**

Giữ cùng thứ tự ý, công thức, nhãn hình và self-check; dùng thuật ngữ tiếng Anh chuẩn, không dịch máy từng chữ. Mỗi chương có keypoint, plain-language explanation, common mistake và câu hỏi tự kiểm tra.

- [ ] **Step 4: Kiểm tra chương nền**

Chạy `make check all`; xác nhận không lỗi, không placeholder, hai ngôn ngữ cùng danh sách chương và mọi claim paper truy được về source map.

### Task 4: Mô hình D-Tracker và reaction–diffusion

**Files:**
- Create: `slides/paper_explore/sections_vi/04_reaction_diffusion.tex`
- Create: `slides/paper_explore/sections_vi/05_model.tex`
- Create: `slides/paper_explore/sections_en/04_reaction_diffusion.tex`
- Create: `slides/paper_explore/sections_en/05_model.tex`

**Interfaces:**
- Consumes: ký hiệu và primer Task 3.
- Produces: `sec:reaction-diffusion`, `sec:model`; giải thích Eq. (1)–(4), bộ tham số `\theta`, `\theta_d`, `\theta_s`, `\Theta`, `\mathcal F`.

- [ ] **Step 1: Xây trực giác reaction–diffusion**

Từ hai khu vực và mức quan tâm khác nhau, giải thích dấu của `(w_j'-w_j)`, growth rate `a_ij`, diffusion strength `d_ijj'`; có ví dụ số một bước và sơ đồ mũi tên. Phân biệt “mô hình học được tương quan phù hợp giả định diffusion” với bằng chứng nhân quả.

- [ ] **Step 2: Lắp ráp toàn bộ mô hình**

Giải thích Eq. (1) trend + seasonal + outlier; Eq. (2) core/factors và kích thước; Eq. (3) là ODE rời rạc vị trí nhưng liên tục thời gian; Eq. (4) seasonal factors; outlier thưa; hierarchy một model và nhiều regime. Thêm ví dụ truy vết từ một dynamics đến keyword/location và giải thích Figure 1(b).

- [ ] **Step 3: Đồng bộ EN/VI và công thức paper**

Kiểm tra từng ký hiệu/chỉ số/shape với Eq. (1)–(4) trong source map; chỗ paper viết nghi ngờ typo phải chú thích, không tái sản xuất mù quáng.

- [ ] **Step 4: Build và đọc kiểm tra**

Chạy `make check all`; render đúng các trang có công thức dài/sơ đồ và kiểm tra không tràn lề, hình đọc được.

### Task 5: Ước lượng, MDL và streaming

**Files:**
- Create: `slides/paper_explore/sections_vi/06_estimation.tex`
- Create: `slides/paper_explore/sections_vi/07_mdl_streaming.tex`
- Create: `slides/paper_explore/sections_en/06_estimation.tex`
- Create: `slides/paper_explore/sections_en/07_mdl_streaming.tex`

**Interfaces:**
- Consumes: bộ tham số Task 4.
- Produces: `sec:estimation`, `sec:mdl-streaming`; sơ đồ Algorithm 1–3 và giải thích Eq. (5)–(12), độ phức tạp.

- [ ] **Step 1: Giải thích ModelEstimation/ALS**

Dùng một vòng “giữ phần khác cố định → cập nhật một phần”; trình bày mục tiêu LM cho reaction–diffusion, multiplicative update cho W, ALS/pseudoinverse cho S và residual sparsification cho O. Diễn giải ký hiệu trước khi đưa công thức; không yêu cầu chứng minh tối ưu ngoài paper.

- [ ] **Step 2: Giải thích MDL bằng trực giác mã hóa**

Tách model cost + data cost, cừu đối đầu fit và complexity, cách MDL chọn `d_k,d_l,d_s`, outlier và regime; nêu “parameter-free” theo nghĩa paper vẫn có cấu hình/tham số được học.

- [ ] **Step 3: Trình bày Initialize, ModelUpdate và Forecast**

Vẽ pipeline dữ liệu mới đi qua Estimation/Update/Forecast; giải thích add/keep/switch model và tại sao chi phí không tăng theo tổng chiều dài stream. Ghi chính xác phát biểu độ phức tạp và giả định cửa sổ cố định; không phóng đại thành hằng số tuyệt đối.

- [ ] **Step 4: Kiểm tra song ngữ và thuật toán**

Đối chiếu thứ tự bước Algorithms 1–3, Eq. (5)–(12) với source map; chạy `make check all` và render trang bảng/sơ đồ dài.

### Task 6: Thí nghiệm, liên hệ công trình và đánh giá phản biện

**Files:**
- Create: `slides/paper_explore/sections_vi/08_experiments.tex`
- Create: `slides/paper_explore/sections_vi/09_discussion.tex`
- Create: `slides/paper_explore/sections_en/08_experiments.tex`
- Create: `slides/paper_explore/sections_en/09_discussion.tex`

**Interfaces:**
- Consumes: source map Task 1 và toàn bộ mô hình/thuật toán.
- Produces: `sec:experiments`, `sec:discussion` với kết quả paper, không có kết quả reproduce mới.

- [ ] **Step 1: Hướng dẫn đọc thí nghiệm**

Lập bảng sáu dataset, baseline, horizon, RMSE/MAE (theo paper), thiết lập streaming; giải thích metric bằng ví dụ nhỏ và chiều “nhỏ hơn tốt hơn”. Dùng Figure 3–5/Table 3–4 có chọn lọc và chú thích nguồn.

- [ ] **Step 2: Tóm tắt kết quả không phóng đại**

Đối chiếu từng giá trị được nhắc, đặc biệt average ranking, cải thiện tối đa 57%, nhanh tối đa 8.0x và scalability. Tách kết luận được số liệu hỗ trợ khỏi diễn giải case study.

- [ ] **Step 3: Đặt D-Tracker trong bối cảnh và phản biện**

Giải thích Table 1 về tensor/time-series/social activity methods; nêu giả định, interpretability không đồng nghĩa causality, dependence on data quality/window/model adequacy, và phạm vi generalization sang COVID-19. Không bịa ablation/limitation mà paper không nói như một kết quả đã kiểm chứng.

- [ ] **Step 4: Kiểm tra chính xác và build**

Đối chiếu bảng/claim với paper, chạy `make check all`, đọc trực quan mọi bảng kết quả ở cả hai bản.

### Task 7: Phụ lục tự học, QA toàn diện và bàn giao

**Files:**
- Create: `slides/paper_explore/sections_vi/10_learning_aids.tex`
- Create: `slides/paper_explore/sections_en/10_learning_aids.tex`
- Create: `slides/paper_explore/references.tex`
- Create: `slides/paper_explore/README.md`
- Modify: `slides/paper_explore/scripts/check_documents.py`
- Build: `slides/paper_explore/dtracker_explained_vi.pdf`
- Build: `slides/paper_explore/dtracker_explained_en.pdf`

**Interfaces:**
- Produces: sản phẩm cuối cùng; `make check` kiểm tra nguồn, `make all` tạo cả hai PDF.

- [ ] **Step 1: Hoàn thiện công cụ tự học**

Thêm tóm tắt một trang, roadmap đọc lại paper, bảng thuật ngữ VI–EN, bảng ký hiệu có shape/ý nghĩa, câu hỏi tự kiểm tra phân tầng và gợi ý trả lời. References trích paper gốc và các công trình nền thực sự được nhắc.

- [ ] **Step 2: Hoàn thiện kiểm tra tự động và README**

Script xác nhận parity file chương/self-check, input/figure tồn tại, không placeholder/duplicate label. README ghi yêu cầu, cài engine cục bộ, `make all`, `make check`, vị trí PDF, cấu trúc source, nguồn/license hình và cách cập nhật hai ngôn ngữ.

- [ ] **Step 3: Clean build và kiểm tra log**

Xóa riêng `build/`, chạy `make check all`; xác nhận cả hai PDF tồn tại, có khoảng 25–35 trang (hoặc ghi lý do nếu cần vượt nhẹ để đủ nội dung), không LaTeX error, missing glyph, reference hỏng, `??`, overfull box nghiêm trọng.

- [ ] **Step 4: Kiểm tra PDF trực quan và nội dung**

Render mọi trang thành thumbnail bằng công cụ trong `.venv/` hoặc công cụ sẵn có; kiểm tra contact sheet và phóng to trang title/TOC/công thức/sơ đồ/hình/bảng/phụ lục. Đọc lại PDF bằng công cụ file để xác nhận không chỉ nguồn TeX mới đúng. Nếu một bản sửa, kiểm tra bản còn lại tương ứng.

- [ ] **Step 5: Rà soát cuối theo spec**

Lập checklist từng mục của design doc, đối chiếu hai bản và source map; chạy `git diff --check` và `git status --short` chỉ đọc để liệt kê file. Không commit/push, không tuyên bố hoàn thành trước khi build và visual QA thật sự pass.
