# Báo cáo mở rộng giáo trình — 2026-10-06

## Phase theory-first — 2026-10-06

Đây là report lịch sử của lần expansion trước. Report hiện tại ở [THEORY_COMPLETION_REPORT](THEORY_COMPLETION_REPORT.md), coverage ở [matrix](THEORY_COVERAGE_MATRIX.md). Không dùng số file/URL/test trong báo cáo cũ như số hiện tại.

## Audit

Baseline: 146 file (142 Markdown và bốn file code/project), 121 lab. Đã đọc toàn bộ nội dung; kiểm lại inventory ZIP (247 entries, 141 nội dung text unique trong bản trích), hash và ví dụ nguồn. Không tạo lại giáo trình hoặc tăng số bug. Khoảng trống chính là thiếu nền trước framework, flow/ownership/lifetime quá cô đọng, debug chưa xuyên suốt và thiếu liên kết từ lab tới cơ chế.

[Bảng GAP theo topic, coverage, mechanism, bug/debug và priority](AUDIT_GAPS.md).

## Files modified

Giữ phần giải thích, ví dụ và reasoning tốt; thêm liên kết học tuần tự và debug cho chương cũ. 121 lab được chuẩn hóa theo cấu trúc yêu cầu, bổ sung invariant/wrong fixes riêng. Danh sách thực sự khác baseline:

- [00_INDEX.md](00_INDEX.md)
- [01_FE_BE_ARCHITECTURE.md](01_FE_BE_ARCHITECTURE.md)
- [02_FRONTEND_DEEP_DIVE_AND_BUGS.md](02_FRONTEND_DEEP_DIVE_AND_BUGS.md)
- [03_BACKEND_DEEP_DIVE_AND_BUGS.md](03_BACKEND_DEEP_DIVE_AND_BUGS.md)
- [04_FE_BE_INTEGRATION_AND_REAL_BUGS.md](04_FE_BE_INTEGRATION_AND_REAL_BUGS.md)
- [05_EMBEDDED_C_CPP_FOUNDATION.md](05_EMBEDDED_C_CPP_FOUNDATION.md)
- [06_MCU_FIRMWARE_RTOS.md](06_MCU_FIRMWARE_RTOS.md)
- [07_OPERATING_SYSTEMS_ADVANCED.md](07_OPERATING_SYSTEMS_ADVANCED.md)
- [08_DEBUGGING_PLAYBOOK.md](08_DEBUGGING_PLAYBOOK.md)
- [09_REAL_BUG_CASEBOOK.md](09_REAL_BUG_CASEBOOK.md)
- [10_AI_ASSISTED_CODING_AND_DEBUG.md](10_AI_ASSISTED_CODING_AND_DEBUG.md)
- [CORRECTIONS.md](CORRECTIONS.md)
- [REFERENCES.md](REFERENCES.md)
- [SOURCE_INVENTORY.md](SOURCE_INVENTORY.md)
- [VALIDATION.md](VALIDATION.md)
- [examples/README.md](examples/README.md)
- [labs/backend/BE-01.md](labs/backend/BE-01.md)
- [labs/backend/BE-02.md](labs/backend/BE-02.md)
- [labs/backend/BE-03.md](labs/backend/BE-03.md)
- [labs/backend/BE-04.md](labs/backend/BE-04.md)
- [labs/backend/BE-05.md](labs/backend/BE-05.md)
- [labs/backend/BE-06.md](labs/backend/BE-06.md)
- [labs/backend/BE-07.md](labs/backend/BE-07.md)
- [labs/backend/BE-08.md](labs/backend/BE-08.md)
- [labs/backend/BE-09.md](labs/backend/BE-09.md)
- [labs/backend/BE-10.md](labs/backend/BE-10.md)
- [labs/backend/BE-11.md](labs/backend/BE-11.md)
- [labs/backend/BE-12.md](labs/backend/BE-12.md)
- [labs/backend/BE-13.md](labs/backend/BE-13.md)
- [labs/backend/BE-14.md](labs/backend/BE-14.md)
- [labs/backend/BE-15.md](labs/backend/BE-15.md)
- [labs/backend/BE-16.md](labs/backend/BE-16.md)
- [labs/backend/BE-17.md](labs/backend/BE-17.md)
- [labs/backend/BE-18.md](labs/backend/BE-18.md)
- [labs/backend/BE-19.md](labs/backend/BE-19.md)
- [labs/backend/BE-20.md](labs/backend/BE-20.md)
- [labs/backend/BE-21.md](labs/backend/BE-21.md)
- [labs/backend/BE-22.md](labs/backend/BE-22.md)
- [labs/backend/BE-23.md](labs/backend/BE-23.md)
- [labs/backend/BE-24.md](labs/backend/BE-24.md)
- [labs/backend/BE-25.md](labs/backend/BE-25.md)
- [labs/backend/BE-26.md](labs/backend/BE-26.md)
- [labs/backend/BE-27.md](labs/backend/BE-27.md)
- [labs/backend/BE-28.md](labs/backend/BE-28.md)
- [labs/backend/BE-29.md](labs/backend/BE-29.md)
- [labs/backend/BE-30.md](labs/backend/BE-30.md)
- [labs/embedded_rtos/EMB-01.md](labs/embedded_rtos/EMB-01.md)
- [labs/embedded_rtos/EMB-02.md](labs/embedded_rtos/EMB-02.md)
- [labs/embedded_rtos/EMB-03.md](labs/embedded_rtos/EMB-03.md)
- [labs/embedded_rtos/EMB-04.md](labs/embedded_rtos/EMB-04.md)
- [labs/embedded_rtos/EMB-05.md](labs/embedded_rtos/EMB-05.md)
- [labs/embedded_rtos/EMB-06.md](labs/embedded_rtos/EMB-06.md)
- [labs/embedded_rtos/EMB-07.md](labs/embedded_rtos/EMB-07.md)
- [labs/embedded_rtos/EMB-08.md](labs/embedded_rtos/EMB-08.md)
- [labs/embedded_rtos/EMB-09.md](labs/embedded_rtos/EMB-09.md)
- [labs/embedded_rtos/EMB-10.md](labs/embedded_rtos/EMB-10.md)
- [labs/embedded_rtos/EMB-11.md](labs/embedded_rtos/EMB-11.md)
- [labs/embedded_rtos/EMB-12.md](labs/embedded_rtos/EMB-12.md)
- [labs/embedded_rtos/EMB-13.md](labs/embedded_rtos/EMB-13.md)
- [labs/embedded_rtos/EMB-14.md](labs/embedded_rtos/EMB-14.md)
- [labs/embedded_rtos/EMB-15.md](labs/embedded_rtos/EMB-15.md)
- [labs/embedded_rtos/EMB-16.md](labs/embedded_rtos/EMB-16.md)
- [labs/embedded_rtos/EMB-17.md](labs/embedded_rtos/EMB-17.md)
- [labs/embedded_rtos/EMB-18.md](labs/embedded_rtos/EMB-18.md)
- [labs/embedded_rtos/EMB-19.md](labs/embedded_rtos/EMB-19.md)
- [labs/embedded_rtos/EMB-20.md](labs/embedded_rtos/EMB-20.md)
- [labs/embedded_rtos/EMB-21.md](labs/embedded_rtos/EMB-21.md)
- [labs/embedded_rtos/EMB-22.md](labs/embedded_rtos/EMB-22.md)
- [labs/embedded_rtos/EMB-23.md](labs/embedded_rtos/EMB-23.md)
- [labs/embedded_rtos/EMB-24.md](labs/embedded_rtos/EMB-24.md)
- [labs/embedded_rtos/EMB-25.md](labs/embedded_rtos/EMB-25.md)
- [labs/embedded_rtos/EMB-26.md](labs/embedded_rtos/EMB-26.md)
- [labs/embedded_rtos/EMB-27.md](labs/embedded_rtos/EMB-27.md)
- [labs/embedded_rtos/EMB-28.md](labs/embedded_rtos/EMB-28.md)
- [labs/embedded_rtos/EMB-29.md](labs/embedded_rtos/EMB-29.md)
- [labs/embedded_rtos/EMB-30.md](labs/embedded_rtos/EMB-30.md)
- [labs/frontend/FE-01.md](labs/frontend/FE-01.md)
- [labs/frontend/FE-02.md](labs/frontend/FE-02.md)
- [labs/frontend/FE-03.md](labs/frontend/FE-03.md)
- [labs/frontend/FE-04.md](labs/frontend/FE-04.md)
- [labs/frontend/FE-05.md](labs/frontend/FE-05.md)
- [labs/frontend/FE-06.md](labs/frontend/FE-06.md)
- [labs/frontend/FE-07.md](labs/frontend/FE-07.md)
- [labs/frontend/FE-08.md](labs/frontend/FE-08.md)
- [labs/frontend/FE-09.md](labs/frontend/FE-09.md)
- [labs/frontend/FE-10.md](labs/frontend/FE-10.md)
- [labs/frontend/FE-11.md](labs/frontend/FE-11.md)
- [labs/frontend/FE-12.md](labs/frontend/FE-12.md)
- [labs/frontend/FE-13.md](labs/frontend/FE-13.md)
- [labs/frontend/FE-14.md](labs/frontend/FE-14.md)
- [labs/frontend/FE-15.md](labs/frontend/FE-15.md)
- [labs/frontend/FE-16.md](labs/frontend/FE-16.md)
- [labs/frontend/FE-17.md](labs/frontend/FE-17.md)
- [labs/frontend/FE-18.md](labs/frontend/FE-18.md)
- [labs/frontend/FE-19.md](labs/frontend/FE-19.md)
- [labs/frontend/FE-20.md](labs/frontend/FE-20.md)
- [labs/frontend/FE-21.md](labs/frontend/FE-21.md)
- [labs/frontend/FE-22.md](labs/frontend/FE-22.md)
- [labs/frontend/FE-23.md](labs/frontend/FE-23.md)
- [labs/frontend/FE-24.md](labs/frontend/FE-24.md)
- [labs/frontend/FE-25.md](labs/frontend/FE-25.md)
- [labs/integration/INT-01.md](labs/integration/INT-01.md)
- [labs/integration/INT-02.md](labs/integration/INT-02.md)
- [labs/integration/INT-03.md](labs/integration/INT-03.md)
- [labs/integration/INT-04.md](labs/integration/INT-04.md)
- [labs/integration/INT-05.md](labs/integration/INT-05.md)
- [labs/integration/INT-06.md](labs/integration/INT-06.md)
- [labs/integration/INT-07.md](labs/integration/INT-07.md)
- [labs/integration/INT-08.md](labs/integration/INT-08.md)
- [labs/integration/INT-09.md](labs/integration/INT-09.md)
- [labs/integration/INT-10.md](labs/integration/INT-10.md)
- [labs/integration/INT-11.md](labs/integration/INT-11.md)
- [labs/integration/INT-12.md](labs/integration/INT-12.md)
- [labs/integration/INT-13.md](labs/integration/INT-13.md)
- [labs/integration/INT-14.md](labs/integration/INT-14.md)
- [labs/integration/INT-15.md](labs/integration/INT-15.md)
- [labs/integration/INT-16.md](labs/integration/INT-16.md)
- [labs/integration/INT-17.md](labs/integration/INT-17.md)
- [labs/integration/INT-18.md](labs/integration/INT-18.md)
- [labs/integration/INT-19.md](labs/integration/INT-19.md)
- [labs/integration/INT-20.md](labs/integration/INT-20.md)
- [labs/integration/INT-21.md](labs/integration/INT-21.md)
- [labs/integration/INT-22.md](labs/integration/INT-22.md)
- [labs/integration/INT-23.md](labs/integration/INT-23.md)
- [labs/integration/INT-24.md](labs/integration/INT-24.md)
- [labs/integration/INT-25.md](labs/integration/INT-25.md)
- [labs/integration/README.md](labs/integration/README.md)
- [labs/os/OS-01.md](labs/os/OS-01.md)
- [labs/os/OS-02.md](labs/os/OS-02.md)
- [labs/os/OS-03.md](labs/os/OS-03.md)
- [labs/os/OS-04.md](labs/os/OS-04.md)
- [labs/os/OS-05.md](labs/os/OS-05.md)
- [labs/os/OS-06.md](labs/os/OS-06.md)
- [labs/os/OS-07.md](labs/os/OS-07.md)
- [labs/os/OS-08.md](labs/os/OS-08.md)
- [labs/os/OS-09.md](labs/os/OS-09.md)
- [labs/os/OS-10.md](labs/os/OS-10.md)
- [labs/os/OS-11.md](labs/os/OS-11.md)

## Files added

22 module lý thuyết (11 Web, 10 Embedded/Systems, một bài debug dùng chung), GAP, map và báo cáo này. Debug là phương pháp xuyên suốt hai track, không phải track thứ ba.

- [AUDIT_GAPS.md](AUDIT_GAPS.md)
- [BUG_THEORY_MAP.md](BUG_THEORY_MAP.md)
- [EXPANSION_REPORT.md](EXPANSION_REPORT.md)
- [debug/01_EVIDENCE_METHOD.md](debug/01_EVIDENCE_METHOD.md)
- [embedded_systems/01_C_REPRESENTATION.md](embedded_systems/01_C_REPRESENTATION.md)
- [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md)
- [embedded_systems/03_CPP_OWNERSHIP.md](embedded_systems/03_CPP_OWNERSHIP.md)
- [embedded_systems/04_CPU_MCU_EXECUTION.md](embedded_systems/04_CPU_MCU_EXECUTION.md)
- [embedded_systems/05_PERIPHERAL_STATE_MACHINES.md](embedded_systems/05_PERIPHERAL_STATE_MACHINES.md)
- [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md)
- [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md)
- [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md)
- [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md)
- [embedded_systems/10_OS_KERNEL_USERSPACE.md](embedded_systems/10_OS_KERNEL_USERSPACE.md)
- [web/01_HTTP_BROWSER.md](web/01_HTTP_BROWSER.md)
- [web/02_JS_RUNTIME.md](web/02_JS_RUNTIME.md)
- [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md)
- [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md)
- [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md)
- [web/06_CSHARP_RUNTIME.md](web/06_CSHARP_RUNTIME.md)
- [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md)
- [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md)
- [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md)
- [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md)
- [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md)

## Major additions

- Web: request/connection/cache/CORS; JS stack/closure/task/microtask; TS static/runtime; React render/commit/identity; Next server/client/hydration; C# Task/thread/GC; ASP.NET pipeline/DI; API contracts; MongoDB concurrency/index; identity/security; integration ownership/retry/realtime.
- Embedded/Systems: C representation và UB; memory/build/ELF; C++ lifetime/RAII/cost; CPU/reset/startup; peripheral state machines; interrupt/context/latency; DMA ownership/cache; ring buffer/producer-consumer; RTOS scheduler/resources; kernel/userspace/process/VM/I/O.
- Debug: chọn metric đúng, phân biệt giả thuyết, thiết kế distinguishing test, giữ build/source evidence và kiểm invariant bản sửa. Có câu hỏi tự kiểm tra thay vì cam kết cấp độ sau số tuần cố định.

## Bugs linked

121/121 lab: FE 25, BE 30, integration 25, embedded/RTOS 30, OS 11. Giữ IDs/mục tiêu, không thêm lab để tăng số lượng. [Map lab ↔ theory](BUG_THEORY_MAP.md) cho từng bài. Các case reasoning sâu và 25 integration traces cũ được giữ.

## Sources

Giữ Base_C.zip, Base_CPP.zip, documents.zip và các correction kỹ thuật cũ. [Inventory và mapping nội bộ](SOURCE_INVENTORY.md); [corrections](CORRECTIONS.md). 33 nguồn official/primary mới đọc từ MDN/RFC, React/TS/Next, Microsoft, OWASP, PostgreSQL, GCC/binutils, CMSIS, Linux man-pages; [danh mục và giới hạn](REFERENCES.md). MongoDB vẫn là stack database chính; PostgreSQL chỉ minh họa isolation relational, không thay semantics MongoDB.

## Validation

| Kiểm tra | Kết quả |
|---|---|
| UTF-8 / Markdown / fences | PASS — 167 Markdown |
| Relative links / broken references | PASS — 1799 links/anchors tồn tại |
| Reachability | PASS — 167 Markdown reachable từ index |
| Duplicate accidental content | PASS — không file trùng hoặc đoạn dài lặp nhầm trong file |
| Bug labels / IDs / theory map | PASS — 121 lab giữ ID và có nguồn lý thuyết |
| Source validity | REVIEWED — nguồn mới có body đọc được; nguồn cũ giữ ngày đọc; lỗi truy cập ghi riêng |
| Original ZIPs / code files | PASS — hash giữ nguyên |
| Second-pass review | Hoàn tất; không thay cho kiểm định độc lập hoặc chạy target |

So baseline: **138 file sửa, 25 file thêm, không file xóa**. `labs/frontend/README.md` có chỉnh sửa đồng thời của người dùng và được giữ nguyên bytes, không nằm trong danh sách áp dụng.

[Chi tiết lệnh, kết quả và phạm vi chứng minh](VALIDATION.md). 17 nhóm host checks cũ và hai snippet mới PASS. Các trường hợp mô phỏng không được ghi thành kết quả production hoặc target đã chạy.

## Remaining gaps

Chưa biên dịch snippet C/TS, chưa chạy browser/API/MongoDB/Linux/MCU fixtures đầy đủ; chưa chọn board/RTOS port hoặc đọc được reference manual cần thiết. Chưa đo timing/cache/durability hay đánh giá năng lực học viên. Cần thực hành theo project/version/target để biến các scenario thành integration tests; chưa xem 121 lab là 121 chương trình chạy độc lập.

[Bắt đầu học](00_INDEX.md).
