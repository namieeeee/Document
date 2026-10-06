# Giáo trình kỹ thuật: theory trước lab

Hồ sơ hiện tại: [phase status](audit/PHASE_STATUS.md) · [review checklist](REVIEW_CHECKLIST.md) · [self-review](audit/SELF_REVIEW.md) · [39 outline nội dung](content/README.md) · [archive overview cũ](archive/README.md) · [MongoDB fixture](examples/MongoApi/README.md) · [báo cáo hoàn thiện](audit/COMPLETION_REPORT.md).

[README của repository](README.md).

Bộ tự học tiếng Việt về Web/FE/BE, Embedded/Systems, OS/RTOS và debugging. Bản theory-first ngày 2026-10-06 đi theo dependency: nền → cơ chế → representation/flow → lifetime/state → invariant → failure/evidence → lab. Đọc [coverage before/after](THEORY_COVERAGE_MATRIX.md) để biết phạm vi và giới hạn; không dùng số file làm bằng chứng đã học xong.

## Bắt đầu và chọn nhánh

Người mới chưa hiểu bytes đọc F1; người học web bắt đầu W1 và J1. Không bắt người học C# phải học toàn bộ C hay RTOS. DBG được đọc sau một cơ chế đầu tiên và dùng xuyên suốt, không để cuối khóa mới học debug.

- **Frontend:** W1 → W2 → J1 → W3 → J2 → T1 → R1 → N1. T1 hữu ích cho source typed, không là điều kiện semantics của React.
- **Backend:** F1 → W1 → W2 → C1 → D1 → A1 → A2 → DB1 → DB2. Học J1/W3 cho browser trust model rồi S1 trước triển khai security.
- **Integration:** sau cả frontend/backend và S1, đọc I1 → DW rồi chọn lab ở map.
- **Embedded:** F1 → C2 → M1 → B1 → CPU → MCU → CM4 → PER → SER → ADC → IRQ → DMA → BUF → RTOS → RT → DS. CPP là nhánh sau B1 khi dùng C++; không prerequisite của firmware C.
- **OS:** sau CPU/M1: OS1 → OS2 → OS3 → OS4. Không cần học mọi peripheral hay thuộc APIs RTOS trước OS.

Mũi tên là thứ tự đọc gợi ý; bảng dưới ghi prerequisites bắt buộc cụ thể. Link “học tiếp/mở rộng” trong bài không phải prerequisite ngược. Ví dụ đọc build trước CPU để hiểu symbols/placement, rồi quay lại disassembly sau CPU; API trước DB foundation, transactions triển khai concurrency sau đó. Hai vòng đọc mở rộng này không tạo cycle trong dependency graph.

## Bảng bài và dependency

IDs chỉ dùng điều hướng. Mỗi bài canonical có 16 mục, ví dụ/schedule minh họa, invariant, phép đo phân biệt và self-check có đáp án. Hoàn thành một bài khi tự vẽ được flow, giải thích state/owner, dự đoán failure và chọn evidence; có thể đọc self-check trước để kiểm nền.

| ID | Bài canonical | Tiên quyết | Tại sao học ở đây? |
|---|---|---|---|
| F1 | [foundations/01_DIGITAL_REPRESENTATION.md](foundations/01_DIGITAL_REPRESENTATION.md) | Biến/hàm hoặc toán căn bản | Bits/bytes, signedness, endian; nền đọc memory và wire |
| W1 | [web/01_HTTP_BROWSER.md](web/01_HTTP_BROWSER.md) | Biến/hàm hoặc toán căn bản | URL/origin và request qua DNS/TCP/TLS; chưa dùng framework |
| J1 | [foundations/02_JAVASCRIPT_LANGUAGE.md](foundations/02_JAVASCRIPT_LANGUAGE.md) | Biến/hàm hoặc toán căn bản | Bindings, reference, closure, prototype trước async/React |
| W2 | [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md) | W1 | Representation, cache và preconditions trước retry/API |
| W3 | [web/13_BROWSER_INTERNALS.md](web/13_BROWSER_INTERNALS.md) | W2, J1 | DOM/render pipeline, events/storage trước scheduling UI |
| J2 | [web/02_JS_RUNTIME.md](web/02_JS_RUNTIME.md) | J1, W3 | Jobs, microtasks và continuation trước effect/fetch race |
| T1 | [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md) | J1 | Types là lớp tĩnh; giữ boundary runtime values |
| R1 | [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md) | J2, W3 | Snapshot/identity/commit trước hooks và framework routing |
| N1 | [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md) | R1, W2, W3 | Build/server/browser graphs và serialized boundary |
| C1 | [web/06_CSHARP_RUNTIME.md](web/06_CSHARP_RUNTIME.md) | F1 | Type/copy/boxing/dispose trước managed async |
| D1 | [web/14_DOTNET_ASYNC_RUNTIME.md](web/14_DOTNET_ASYNC_RUNTIME.md) | C1 | IL/JIT/GC/Task trước server lifecycle |
| A1 | [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md) | W2, D1 | Request pipeline/scopes trước endpoint design |
| A2 | [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md) | A1, W2 | Resource/command/validation trước storage implementation |
| DB1 | [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md) | A2 | Records, storage, index/plans trước transaction schedules |
| DB2 | [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md) | DB1, W2 | Atomicity/isolation/dedup giữ invariant concurrent |
| S1 | [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md) | DB2, W3, A1 | Credentials/session/quyền và trust boundaries |
| I1 | [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md) | N1, A2, DB2, S1 | Nối intent/version/owner qua FE, API và data |
| C2 | [embedded_systems/01_C_REPRESENTATION.md](embedded_systems/01_C_REPRESENTATION.md) | F1 | C semantics trước layout/registers |
| M1 | [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md) | C2 | Live objects, placement, aliasing và budgets |
| B1 | [embedded_systems/11_BUILD_LINK_STARTUP.md](embedded_systems/11_BUILD_LINK_STARTUP.md) | M1 | Translation units/symbols/linker/startup trước đọc image |
| CPU | [embedded_systems/04_CPU_MCU_EXECUTION.md](embedded_systems/04_CPU_MCU_EXECUTION.md) | B1, F1 | Instructions/registers/calls/ABI trước Cortex-M |
| CPP | [embedded_systems/03_CPP_OWNERSHIP.md](embedded_systems/03_CPP_OWNERSHIP.md) | C2, M1, B1 | Nhánh C++ RAII/copy/move; không bắt buộc firmware C |
| MCU | [embedded_systems/13_MMIO_MCU.md](embedded_systems/13_MMIO_MCU.md) | CPU, B1 | Core+memory/clock/bus; register side effects trước HAL |
| CM4 | [embedded_systems/12_CORTEX_M.md](embedded_systems/12_CORTEX_M.md) | CPU, MCU, B1 | Reset/vector/stack/exception của M4 trước ISR |
| PER | [embedded_systems/05_PERIPHERAL_STATE_MACHINES.md](embedded_systems/05_PERIPHERAL_STATE_MACHINES.md) | MCU, F1 | GPIO/timer/PWM là hardware state machines |
| SER | [embedded_systems/14_SERIAL_BUSES.md](embedded_systems/14_SERIAL_BUSES.md) | PER, MCU | UART/SPI/I2C: wire timing và service state |
| ADC | [embedded_systems/15_ADC_CAN.md](embedded_systems/15_ADC_CAN.md) | SER, PER | Acquisition/trigger và Classical CAN bus/error state |
| IRQ | [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md) | CM4, MCU, C2 | Pending/entry/ack/return; priority và latency |
| DMA | [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md) | IRQ, PER, M1 | Bus actor độc lập; completion/ownership/cache |
| BUF | [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md) | IRQ, DMA, M1 | Publication và lifetime qua main/ISR/DMA/task |
| RTOS | [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md) | CM4, IRQ, BUF | States/ready/wait/context switch trước APIs |
| RT | [embedded_systems/16_REAL_TIME.md](embedded_systems/16_REAL_TIME.md) | RTOS, IRQ, DMA | Response/deadline/interference trước claim real-time |
| OS1 | [os/01_KERNEL_PROCESS.md](os/01_KERNEL_PROCESS.md) | CPU, M1 | Hardware→kernel→userspace→syscall trước threads |
| OS2 | [os/02_VIRTUAL_MEMORY.md](os/02_VIRTUAL_MEMORY.md) | OS1, M1 | Mappings/MMU/TLB/fault/COW trước heap/RSS diagnosis |
| OS3 | [os/03_IO_IPC_LIFETIME.md](os/03_IO_IPC_LIFETIME.md) | OS1, OS2 | FD/IPC và acquire-use-release trước shared handles |
| OS4 | [os/04_CONCURRENCY.md](os/04_CONCURRENCY.md) | OS1, OS2, OS3 | Locks/predicate/order/wait graph và pool starvation |
| DBG | [debug/01_EVIDENCE_METHOD.md](debug/01_EVIDENCE_METHOD.md) | W1 **hoặc** F1 | Đọc sau W1 hoặc F1; phương pháp dùng xuyên suốt |
| DW | [debug/02_WEB_OBSERVABILITY.md](debug/02_WEB_OBSERVABILITY.md) | DBG | Đã học cơ chế Web ở tầng đang đo; chọn evidence theo boundary |
| DS | [debug/03_SYSTEMS_OBSERVABILITY.md](debug/03_SYSTEMS_OBSERVABILITY.md) | DBG, B1, CM4 | Đã học peripheral/RTOS liên quan; chọn tool theo tầng |

## Chương gốc: overview và casebook

Chương 01–10 giữ nội dung gốc và vai trò overview, thực hành/casebook. Các bài canonical ở bảng trên là nơi học theory sâu; số chương gốc không phải progression thay thế dependency.

| Chương | Học được gì | Kiến thức trước đó |
|---|---|---|
| [01 — Kiến trúc FE/BE](01_FE_BE_ARCHITECTURE.md) | Theo dấu request, phân định trách nhiệm và ranh giới tin cậy | Đọc code đơn giản |
| [02 — Frontend và lỗi](02_FRONTEND_DEEP_DIVE_AND_BUGS.md) | Event loop, React state/effect, Next.js, browser và 25 lab | Chương 01; JavaScript căn bản |
| [03 — Backend và lỗi](03_BACKEND_DEEP_DIVE_AND_BUGS.md) | .NET pipeline/DI/async, API, quyền, MongoDB và 30 lab | Chương 01; C# căn bản |
| [04 — Tích hợp FE↔BE](04_FE_BE_INTEGRATION_AND_REAL_BUGS.md) | Contract, cookie/CORS, retry/realtime và 25 lab | Chương 02–03 |
| [05 — C/C++ cho embedded](05_EMBEDDED_C_CPP_FOUNDATION.md) | Kiểu, lifetime, memory/build, ownership và đọc tài liệu nội bộ | C cơ bản hoặc bài tập nguồn |
| [06 — MCU, firmware, RTOS](06_MCU_FIRMWARE_RTOS.md) | Cortex-M, startup, peripheral, ISR/DMA và scheduling | Chương 05 |
| [07 — OS nâng cao](07_OPERATING_SYSTEMS_ADVANCED.md) | Process/thread, memory, I/O, IPC và concurrency | Chương 05–06 |
| [08 — Debug đa tầng](08_DEBUGGING_PLAYBOOK.md) | Dựng giả thuyết, lấy bằng chứng, GDB/trace/timing | Một nhánh web hoặc embedded |
| [09 — Casebook](09_REAL_BUG_CASEBOOK.md) | Lab có tái hiện, sửa và regression; phân biệt mô phỏng/incident | Dùng song song các chương |
| [10 — Code/debug cùng AI](10_AI_ASSISTED_CODING_AND_DEBUG.md) | Đọc repo, baseline, thay đổi nhỏ, kiểm tra và review diff | Git cơ bản; chương 08 |

[Systems10 cũ](embedded_systems/10_OS_KERNEL_USERSPACE.md) là overview tương thích cho link lab cũ; theory OS hiện nằm ở OS1–OS4. Không tạo một nhánh lý thuyết OS thứ hai.

## Theory → invariant → 121 lab

[BUG_THEORY_MAP](BUG_THEORY_MAP.md) giữ 121 ID: FE25, BE30, INT25, EMB30, OS11; không thêm lab. Đọc theory và invariant trước Bug/Fix. Lab là educational reproduction với fixtures/outputs dự đoán; chưa có nghĩa đã chạy integration/browser/board.

Một lượt học: dự đoán flow/state → nêu invariant → chọn trigger và phép thử phân biệt → thu evidence → giải root cause → kiểm fix/regression. Nếu kết quả thực khác prediction, giữ evidence và xét assumptions; không sửa output để vừa tài liệu.

## Phiên bản và evidence

| Nhóm | Phạm vi của theory |
|---|---|
| JavaScript / TypeScript | ECMAScript2023 semantics nền; TS5.x strict, declarations đối chiếu compiler của project |
| React / Next.js | React19; Next15 App Router, không lấy defaults của major khác |
| C# / .NET / ASP.NET | C#12/.NET8/ASP.NET Core8 |
| Database | MongoDB8.0 và PostgreSQL16; isolation/read-write concerns phân biệt |
| C / C++ | C17 với N1570 public C11 draft cho nền chung; C++17 với N4659 |
| Core / RTOS | Cortex-M4 Armv7E-M, optional FPU; CMSIS6.0; FreeRTOS11.1.0 ARM_CM4F single-core; Zephyr3.7.0 single-core |
| OS / tools | Linux/POSIX conceptual và man-pages/kernel docs rolling; không gán layout/timing cho release chưa khóa |

[VALIDATION](VALIDATION.md) tách kết quả đã chạy khỏi mô hình. [Nguồn/phiên bản](REFERENCES.md) và [ledger truy cập nguồn](THEORY_SOURCE_VERIFICATION.md) ghi body đọc được, URL đổi và giới hạn. Không access secrets/production hoặc chạy binaries từ ZIP.

## Hồ sơ của đợt mở rộng

- [Theory completion report](THEORY_COMPLETION_REPORT.md): before/after, files, P0/P1 và giới hạn.
- [Coverage matrix](THEORY_COVERAGE_MATRIX.md): evidence cho từng lớp.
- [Source inventory](SOURCE_INVENTORY.md) và [corrections](CORRECTIONS.md): ZIP chỉ là context, không authority cuối.
- [Audit lịch sử](AUDIT_GAPS.md), [expansion report lịch sử](EXPANSION_REPORT.md): phân biệt phase cũ với phase theory-first hiện tại.
