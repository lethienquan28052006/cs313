# D-Tracker Overview Slides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo outline từng slide và bộ Beamer 16:9 tiếng Việt, 35 phút, giải thích D-Tracker trực quan trước khi đưa công thức.

**Architecture:** `outline.md` khóa narrative và timing; `main.tex` triển khai đúng thứ tự slide với theme riêng, TikZ diagram và các hộp intuition/formula/check. Checker kiểm tra cấu trúc; Tectonic tạo PDF; QA render và đọc log xác nhận bố cục.

**Tech Stack:** LaTeX Beamer, XeTeX/Tectonic, TikZ, tcolorbox, fontspec/unicode-math, Python 3 checker.

**Spec:** `docs/superpowers/specs/2026-11-26-dtracker-overview-slides-design.md`

## Global Constraints

- Tiếng Việt, 16:9, 35 phút + Q&A, người mới, ứng dụng được nhấn mạnh.
- Mỗi khái niệm toán theo thứ tự trực quan → lời → công thức → kiểm tra.
- Không bịa kết quả; số liệu paper phải giữ caveat.
- Không sửa explainer hiện có; tạo thư mục độc lập `slides/dtracker_talk/`.

## Review Focus

- Công thức xuất hiện trước trực giác hoặc quá nhiều công thức trên một slide: checker đếm marker `MATH` và QA đọc từng slide.
- Bố cục tràn/collision hoặc chữ quá nhỏ: compile log + render PDF.
- Số liệu/claim bị phóng đại: đối chiếu `../paper_explore/sources/source_map.md`.
- Outline và deck lệch nhau: checker so số slide được đánh dấu.
- PDF thiếu font tiếng Việt/hình: log missing glyph + image existence check.

---

### Task 1: Outline và kiểm tra cấu trúc

**Files:**
- Create: `slides/dtracker_talk/outline.md`
- Create: `slides/dtracker_talk/scripts/check_deck.py`
- Create: `slides/dtracker_talk/scripts/test_check_deck.py`

- [ ] Viết `outline.md` với 15 slide nội dung, 3 section divider, 4 backup; mỗi slide có thời lượng, mục tiêu, visual, math, speaker cue.
- [ ] Viết test checker cho thiếu outline, lệch số slide, placeholder, hình thiếu; chạy và thấy fail.
- [ ] Cài checker; chạy pass trên outline.
- [ ] Compile skeleton Beamer.

### Task 2: Theme và slide nền

**Files:**
- Create: `slides/dtracker_talk/main.tex`
- Create: `slides/dtracker_talk/theme.tex`
- Create: `slides/dtracker_talk/Makefile`
- Create: `slides/dtracker_talk/README.md`
- Create: `slides/dtracker_talk/figures/` (copy hình paper cần dùng)

- [ ] Viết theme 16:9, màu, font, frametitle, footline, title page.
- [ ] Tạo khung slide và kiểm tra compile.
- [ ] Cấu hình Tectonic local/fallback và README.

### Task 3: Nội dung trực quan và toán

**Files:**
- Modify: `slides/dtracker_talk/main.tex`

- [ ] Viết các slide hook, tensor, thử thách, pipeline, decomposition.
- [ ] Viết slide radio/Tucker kèm công thức và shape.
- [ ] Viết slide bể nước/ODE, ví dụ số; phép chiếu và mô hình đầy đủ.
- [ ] Viết slide ALS, MDL/regime, streaming, ứng dụng, evidence, takeaway.
- [ ] Viết backup kỹ thuật.

### Task 4: Build và QA

- [ ] `make check`, clean build, xác nhận 35 phút narrative và số slide.
- [ ] Render toàn bộ PDF, kiểm tra text ngoài lề/blank/missing glyph/overfull.
- [ ] Đối chiếu outline–deck–source map; cập nhật README.
- [ ] Không commit/push nếu người dùng chưa yêu cầu.
