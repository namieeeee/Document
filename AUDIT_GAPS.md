# Audit và kế hoạch bù khoảng trống — 2026-10-06

## Phase theory-first — 2026-10-06

Audit dưới mô tả baseline trước đợt hoàn thiện theory. Coverage hiện tại dùng [matrix before/after](THEORY_COVERAGE_MATRIX.md), không lấy trạng thái historical PARTIAL làm kết luận mới. Đã bổ sung bài language/nền và tách các cơ chế lớn; [report](THEORY_COMPLETION_REPORT.md) ghi P0/P1 và giới hạn còn lại.

Baseline thực tế: `Document_Code/knowledge_base`, 146 file text, 142 Markdown và121 lab. Đã đọc toàn bộ file vào snapshot để bảo toàn nội dung trước sửa. 10 chương tổng quan có khoảng654–1023 từ/chương, nhiều chủ đề lớn cùng nằm trong một chương. Không có Git delivery được yêu cầu cho lần mở rộng này.

| Topic | Current coverage | Missing foundation | Missing mechanism | Missing bugs | Missing debug | Priority |
|---|---|---|---|---|---|---|
| HTTP/browser | Request task và retry | URL/DNS/TLS/header/connection | Request không phải connection, cache layers | Không cần thêm lab | Phân biệt network/CORS/auth | P0 |
| JavaScript | Event loop vài đoạn | Stack/heap/closure/Promise | Task/microtask/render opportunity/retention | Giữ FE01–06 | Time line owner và rejection | P0 |
| TypeScript | Assertion/guard | Structural types/union/generic/unknown | Type erasure vs runtime value | Giữ FE25/INT01–05 | Inspect shape trước mapping | P1 |
| React | State/effect lỗi | Render/commit/identity/ref | Queue update/batching/reconciliation | Giữ FE01–11 | Snapshot vs race; wrong fixes | P0 |
| Next.js | Boundary/cache overview | SSR/RSC/routing | Chỗ chạy/serialization/hydration | Giữ FE12–14/16 | Server log vs browser | P1 |
| C# runtime | Async trong BE | Value/reference/exception/interface | Task≠thread; pool/cancel/lifetime | Giữ BE08–12 | Completion/wait/resource evidence | P0 |
| ASP.NET | Middleware/DI | Server/routing/binding/options | Pipe line order và short circuit | Giữ BE01–12/22–24 | Trace từng stage | P0 |
| API/database | Contract/atomic update | DTO/entity/index/constraint | Isolation/concurrent writes/query plan | Giữ BE13–20/27–28 | Invariant/test barrier/explain | P1 |
| Identity/security | Risk checklist ngắn | Credentials/hash/session/CSRF | Browser credential flow/trust boundary | Giữ BE01–07/24–25/29–30 | 401/403/CORS khác nhau | P1 |
| Integration | Wire lỗi | Intent/version/result | Retry/reconcile/event gap | Giữ25 INT | Trace cụ thể và negative tests | P0 |
| C/memory/build | Một số nuance tốt | Bits/union/enum/sections | Pointer lifetime/alias/build placement | Giữ C bài nguồn/EMB | Map/disassembly/bounds | P0 |
| C++ | RAII vài đoạn | Construction/destruction/reference | Copy/move/virtual/template costs | Không tăng số lab | Ownership và realloc evidence | P1 |
| CPU/MCU | Reset overview | ALU/register/PC/SP/bus/MMIO | Source→instruction→startup | Giữ EMB01–10 | ELF/fault/core-specific | P0 |
| Peripherals | Tên protocol/constraints | State machines | Registers/software interaction | Không cần thêm lab | Wire waveform vs software state | P1 |
| ISR/DMA/concurrency | Ownership tốt nhưng ngắn | Exception/control flow | Atomicity/visibility/ownership khác nhau | Giữ EMB01–15/30 | Timing/word access/cache evidence | P0 |
| RTOS | API/mutex scheduling ngắn | Ready/running/blocked/context | Scheduler/event/timeout/deadline | Giữ EMB16–30 | Wait graph/progress timeline | P0 |
| OS | 667 từ bao nhiều mảng | Kernel/syscall/VM/FD/IPC/signal | Page fault, process resource lifecycle | Giữ11 OS | FD/maps/wait/stack/core | P1 |
| Debug xuyên suốt | Chương08 khá tốt | Evidence và giả thuyết | Distinguishing test/wrongfix | Giữ121 lab | Thêm debug8 mục vào từng chương | P0 |

Kế hoạch: giữ root chapters như overview, thêm11 bài web +10 bài embedded/systems +1 bài debug dùng chung. Mỗi bài có cơ chế, flow, ví dụ, invariant, failure/debug và câu hỏi. Chuyển121 lab sang format yêu cầu, giữ trigger/fix/regression và phần reasoning tốt. Không thêm lab để tăng số lượng.

Phát hiện thêm: bộ sửa spacing trước đây làm hỏng `vào`/`cũng` thành `và o`/`cũ ng`; sửa chính xác các chuỗi sai đã xác định, không dùng regex tách chữ hàng loạt. Pseudocode và kết quả dự đoán cần giữ nhãn trung thực. API-specific hoặc board-specific chưa chạy không chuyển thành PASS bằng review tĩnh.

P2 như kernel internals/distributed optimization chỉ ghi hướng đọc; tập trung bù P0/P1. [Index](00_INDEX.md) · [Validation](VALIDATION.md).
