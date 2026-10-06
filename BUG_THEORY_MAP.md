# Theory → invariant → existing bug lab

Giữ nguyên 121 ID và nội dung lab; không thêm scenario. Bảng đi từ bài canonical và invariant tới lab đã có. Cột invariant lấy từ mục Invariant của lab gốc, không viết lại mục tiêu để phù hợp implementation. Đọc cơ chế, data/flow/owner ở bài nền trước khi mở Bug/Fix. Các links nền cũ bên trong lab vẫn hợp lệ; bảng này dẫn tới bài sâu được tách trong phase theory-first.

Mỗi lab xuất hiện đúng một dòng; có thể có hai bài nền khi invariant qua nhiều boundary. [Scientific debugging](debug/01_EVIDENCE_METHOD.md) dùng chung mọi dòng.

| Theory / invariants nền | Invariant cụ thể của lab | Existing lab |
|---|---|---|
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Protected operation chỉ xảy ra sau kiểm quyền hợp lệ. | [BE-01](labs/backend/BE-01.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | User chỉ access object/tenant nằm trong scope quyền của principal. | [BE-02](labs/backend/BE-02.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Client chỉ được sửa field trong write contract được phép. | [BE-03](labs/backend/BE-03.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Server giữ domain invariant dù client bỏ mọi validation. | [BE-04](labs/backend/BE-04.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Credential chỉ được accept khi đủ trust/target/lifetime validation. | [BE-05](labs/backend/BE-05.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Refresh/reuse/revocation theo token-family policy atomic. | [BE-06](labs/backend/BE-06.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Concurrent refresh giữ generation và policy session nhất quán. | [BE-07](labs/backend/BE-07.md) |
| [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md#9-invariants) | Dependency không bị dùng ngoài scope/lifetime của nó. | [BE-08](labs/backend/BE-08.md) |
| [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md#9-invariants) | Request state không lẫn giữa user/request đồng thời. | [BE-09](labs/backend/BE-09.md) |
| [web/14_DOTNET_ASYNC_RUNTIME.md](web/14_DOTNET_ASYNC_RUNTIME.md#9-invariants) | Caller quan sát được completion/failure của operation cần chờ. | [BE-10](labs/backend/BE-10.md) |
| [web/14_DOTNET_ASYNC_RUNTIME.md](web/14_DOTNET_ASYNC_RUNTIME.md#9-invariants) | I/O chờ không giữ worker đồng bộ không cần thiết trong async path. | [BE-11](labs/backend/BE-11.md) |
| [web/14_DOTNET_ASYNC_RUNTIME.md](web/14_DOTNET_ASYNC_RUNTIME.md#9-invariants) | Cancellation được propagate tới operation hỗ trợ và không nói sai commit outcome. | [BE-12](labs/backend/BE-12.md) |
| [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) + [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md#9-invariants) | Retry cùng intent không tạo hiệu ứng nghiệp vụ lặp ngoài contract. | [BE-13](labs/backend/BE-13.md) |
| [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) + [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md#9-invariants) | Idempotency key gắn intent/scope/payload, không gắn từng attempt mới. | [BE-14](labs/backend/BE-14.md) |
| [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) | Successful purchases không vượt stock và điều kiện gắn atomic write. | [BE-15](labs/backend/BE-15.md) |
| [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) | Write không âm thầm ghi đè version đã thay đổi sau lần đọc. | [BE-16](labs/backend/BE-16.md) |
| [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md#9-invariants) | Pagination có order/continuation semantics ổn định được quy định. | [BE-17](labs/backend/BE-17.md) |
| [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md#9-invariants) | Access path/work bounded phù hợp workload và latency budget đã đo. | [BE-18](labs/backend/BE-18.md) |
| [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md#9-invariants) | Compound index hỗ trợ predicates/sort mục tiêu theo query plan. | [BE-19](labs/backend/BE-19.md) |
| [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md#9-invariants) | Result/work/memory có giới hạn được enforce server-side. | [BE-20](labs/backend/BE-20.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Cache không trộn data khác tenant/quyền/variant. | [BE-21](labs/backend/BE-21.md) |
| [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md#9-invariants) | Dependency failure không bị trình bày như dữ liệu success rỗng. | [BE-22](labs/backend/BE-22.md) |
| [debug/02_WEB_OBSERVABILITY.md](debug/02_WEB_OBSERVABILITY.md#9-invariants) + [web/07_ASPNET_LIFECYCLE.md](web/07_ASPNET_LIFECYCLE.md#9-invariants) | Trace/log đủ liên kết outcome với request mà không lộ dữ liệu nhạy cảm. | [BE-23](labs/backend/BE-23.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Credentials không đi vào persistent log/traces/error output. | [BE-24](labs/backend/BE-24.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Private secrets không được lưu trong tracked source/history. | [BE-25](labs/backend/BE-25.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Timestamp/instant giữ offset/ngữ nghĩa qua roundtrip. | [BE-26](labs/backend/BE-26.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Wire DTO ổn định và không lộ internal graph/field. | [BE-27](labs/backend/BE-27.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | HTTPstatus và error contract thể hiện outcome nhất quán. | [BE-28](labs/backend/BE-28.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Browser credentials chỉ được cho phép theo origin policy cụ thể; auth độc lập. | [BE-29](labs/backend/BE-29.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Request cost/arrival có quota/bounds để giữ service progress. | [BE-30](labs/backend/BE-30.md) |
| [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | ISR service time/latency nằm budget để không mất event ngoài policy. | [EMB-01](labs/embedded_rtos/EMB-01.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | Main đọc multi-field data từ một snapshot/generation coherent. | [EMB-02](labs/embedded_rtos/EMB-02.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | Mọi increment được bảo vệ atomicity của RMW invariant. | [EMB-03](labs/embedded_rtos/EMB-03.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | Clear/consume không xóa event mới ngoài coalescing policy. | [EMB-04](labs/embedded_rtos/EMB-04.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | Multi-word value không bị quan sát thành torn generation. | [EMB-05](labs/embedded_rtos/EMB-05.md) |
| [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | IRQ gọi kernel API đúng context/urgency threshold theo port. | [EMB-06](labs/embedded_rtos/EMB-06.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | Event multiplicity hoặc intentional coalescing được giữ và đo rõ. | [EMB-07](labs/embedded_rtos/EMB-07.md) |
| [embedded_systems/13_MMIO_MCU.md](embedded_systems/13_MMIO_MCU.md#9-invariants) | Register write chỉ acknowledge/change các bits được chủ ý theo manual. | [EMB-08](labs/embedded_rtos/EMB-08.md) |
| [embedded_systems/06_INTERRUPTS.md](embedded_systems/06_INTERRUPTS.md#9-invariants) | ISR không block chờ actor không thể tiến trong context đó. | [EMB-09](labs/embedded_rtos/EMB-09.md) |
| [embedded_systems/12_CORTEX_M.md](embedded_systems/12_CORTEX_M.md#9-invariants) + [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) | Stack đủ mọi call/nesting paths theo core/port. | [EMB-10](labs/embedded_rtos/EMB-10.md) |
| [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md#9-invariants) + [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) | DMA buffer còn sống/access hợp lệ tới khi engine ngừng dùng. | [EMB-11](labs/embedded_rtos/EMB-11.md) |
| [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md#9-invariants) | CPU/DMA quan sát đúng bytes theo cache/region contract của target. | [EMB-12](labs/embedded_rtos/EMB-12.md) |
| [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md#9-invariants) | CPU không sửa/read vùng đang thuộc DMA ngoài access policy. | [EMB-13](labs/embedded_rtos/EMB-13.md) |
| [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md#9-invariants) | DMA source/destination/length thỏa alignment/region constraints. | [EMB-14](labs/embedded_rtos/EMB-14.md) |
| [embedded_systems/07_DMA_OWNERSHIP.md](embedded_systems/07_DMA_OWNERSHIP.md#9-invariants) | Buffer không được quay vòng reuse trước consumer release. | [EMB-15](labs/embedded_rtos/EMB-15.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) | Shared task state có synchronization cho toàn invariant. | [EMB-16](labs/embedded_rtos/EMB-16.md) |
| [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Lock protocol không tạo circular wait. | [EMB-17](labs/embedded_rtos/EMB-17.md) |
| [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Retry/collision protocol tạo bounded progress theo design. | [EMB-18](labs/embedded_rtos/EMB-18.md) |
| [embedded_systems/16_REAL_TIME.md](embedded_systems/16_REAL_TIME.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Task cần tiến có cơ hội phục vụ theo scheduling/workload policy. | [EMB-19](labs/embedded_rtos/EMB-19.md) |
| [embedded_systems/16_REAL_TIME.md](embedded_systems/16_REAL_TIME.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Blocking ưu tiên cao được bound theo lock/priority protocol đã chọn. | [EMB-20](labs/embedded_rtos/EMB-20.md) |
| [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Owned lock và event signal dùng primitive đúng semantics. | [EMB-21](labs/embedded_rtos/EMB-21.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Queue full không silent loss; producer xử lý outcome theo policy. | [EMB-22](labs/embedded_rtos/EMB-22.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Notification/count/bits giữ đúng yêu cầu multiplicity/wakeup. | [EMB-23](labs/embedded_rtos/EMB-23.md) |
| [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Task stack budget/units đúng và có worst-case margin kiểm được. | [EMB-24](labs/embedded_rtos/EMB-24.md) |
| [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Allocation failures/fragmentation không phá invariant và được xử lý. | [EMB-25](labs/embedded_rtos/EMB-25.md) |
| [embedded_systems/16_REAL_TIME.md](embedded_systems/16_REAL_TIME.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Priority/ready work không gây deadline violation ngoài budget thiết kế. | [EMB-26](labs/embedded_rtos/EMB-26.md) |
| [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Task chờ không ngăn actor producer được schedule. | [EMB-27](labs/embedded_rtos/EMB-27.md) |
| [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Critical section không block dependency đang bị mask/prevent. | [EMB-28](labs/embedded_rtos/EMB-28.md) |
| [embedded_systems/16_REAL_TIME.md](embedded_systems/16_REAL_TIME.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Timeout đúng qua modulo wrap trong interval bounds cho phép. | [EMB-29](labs/embedded_rtos/EMB-29.md) |
| [embedded_systems/08_CONCURRENCY_BUFFERS.md](embedded_systems/08_CONCURRENCY_BUFFERS.md#9-invariants) + [embedded_systems/09_RTOS_SCHEDULER.md](embedded_systems/09_RTOS_SCHEDULER.md#9-invariants) | Queued buffer lifetime/owner chỉ chuyển/release theo completion protocol. | [EMB-30](labs/embedded_rtos/EMB-30.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Mỗi tick tăng đúng từ state hiện hành, không từ binding render đã hết hạn. | [FE-01](labs/frontend/FE-01.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Subscription đang active phải thuộc room hiện hành. | [FE-02](labs/frontend/FE-02.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Effect không tự thay dependency khiến chính nó kích hoạt mãi. | [FE-03](labs/frontend/FE-03.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Mỗi resource setup được thu hồi khi owner kết thúc. | [FE-04](labs/frontend/FE-04.md) |
| [web/02_JS_RUNTIME.md](web/02_JS_RUNTIME.md#9-invariants) | Chỉ request còn sở hữu query UI được apply kết quả. | [FE-05](labs/frontend/FE-05.md) |
| [web/02_JS_RUNTIME.md](web/02_JS_RUNTIME.md#9-invariants) | Loading/error chỉ được completion của owner hiện hành thay đổi. | [FE-06](labs/frontend/FE-06.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Một intent submit tạo tối đa một hiệu ứng theo contract, kể cả request lặp. | [FE-07](labs/frontend/FE-07.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Input giữ một mô hình ownership controlled hoặc uncontrolled suốt lifetime. | [FE-08](labs/frontend/FE-08.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Local state/focus thuộc đúng identity entity khi list thay đổi. | [FE-09](labs/frontend/FE-09.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Snapshot trước không bị mutation và state update có identity phù hợp. | [FE-10](labs/frontend/FE-10.md) |
| [web/04_REACT_MENTAL_MODEL.md](web/04_REACT_MENTAL_MODEL.md#9-invariants) | Derived total luôn phản ánh inputs hiện hành mà không có nguồn sự thật thứ hai. | [FE-11](labs/frontend/FE-11.md) |
| [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md#9-invariants) | HTML server và first-client render tương thích cho hydration. | [FE-12](labs/frontend/FE-12.md) |
| [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md#9-invariants) | Code chạy server không truy cập browser-only global. | [FE-13](labs/frontend/FE-13.md) |
| [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md#9-invariants) | Interactive hooks nằm trong client boundary; private data ở server. | [FE-14](labs/frontend/FE-14.md) |
| [web/01_HTTP_BROWSER.md](web/01_HTTP_BROWSER.md#9-invariants) | Success/empty/error/loading được phân biệt theo response và request owner. | [FE-15](labs/frontend/FE-15.md) |
| [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md#9-invariants) | Cache phản ánh policy freshness/invalidation sau mutation theo key và version. | [FE-16](labs/frontend/FE-16.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Session recovery có giới hạn và không dùng credential cũ như current. | [FE-17](labs/frontend/FE-17.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Server kiểm quyền ngay cả khi caller không chịu browser CORS policy. | [FE-18](labs/frontend/FE-18.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Text chưa tin cậy không trở thành executable HTML ngoài policy đã kiểm. | [FE-19](labs/frontend/FE-19.md) |
| [web/05_NEXT_EXECUTION.md](web/05_NEXT_EXECUTION.md#9-invariants) | Private credential không xuất hiện trong bundle/payload client. | [FE-20](labs/frontend/FE-20.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Ngày lịch giữ đúng nghĩa date-only qua timezone. | [FE-21](labs/frontend/FE-21.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Tính tiền giữ units/rounding/currency và miền precision đã chọn. | [FE-22](labs/frontend/FE-22.md) |
| [web/13_BROWSER_INTERNALS.md](web/13_BROWSER_INTERNALS.md#9-invariants) | Nội dung vẫn truy cập được ở viewport/zoom mục tiêu, không bị layout che. | [FE-23](labs/frontend/FE-23.md) |
| [web/13_BROWSER_INTERNALS.md](web/13_BROWSER_INTERNALS.md#9-invariants) | Control có accessible name/error và dùng được bằng keyboard. | [FE-24](labs/frontend/FE-24.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | State nhận dữ liệu có shape/domain hợp lệ từ runtime boundary. | [FE-25](labs/frontend/FE-25.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Field meaning giữ nguyên qua serialize/bind/read/write. | [INT-01](labs/integration/INT-01.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Casing/accessor client khớp wire contract. | [INT-02](labs/integration/INT-02.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Nullable/absent/empty có nghĩa thống nhất và được xử lý rõ. | [INT-03](labs/integration/INT-03.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Wire numeric type/range tương thích phép toán client. | [INT-04](labs/integration/INT-04.md) |
| [web/03_TYPESCRIPT_BOUNDARIES.md](web/03_TYPESCRIPT_BOUNDARIES.md#9-invariants) | Enum representation và unknown-value policy thống nhất. | [INT-05](labs/integration/INT-05.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Date-only/instant giữ nghĩa và timezone đúng qua flow. | [INT-06](labs/integration/INT-06.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Page base và bounds thống nhất hai phía. | [INT-07](labs/integration/INT-07.md) |
| [web/09_DATABASE_CONCURRENCY.md](web/09_DATABASE_CONCURRENCY.md#9-invariants) | Sort direction/key/tie-break giữ đúng contract. | [INT-08](labs/integration/INT-08.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Client parse được error contract kể cả field/global failures. | [INT-09](labs/integration/INT-09.md) |
| [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md#9-invariants) + [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) | Client nhận đúng success/failure statuses và body presence của endpoint. | [INT-10](labs/integration/INT-10.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Credential được truyền bằng cơ chế browser/API đã thiết kế. | [INT-11](labs/integration/INT-11.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Cookie attributes phù hợp transport/site và defense policy. | [INT-12](labs/integration/INT-12.md) |
| [web/01_HTTP_BROWSER.md](web/01_HTTP_BROWSER.md#9-invariants) | Preflight được xử lý đúng nhưng protected operation vẫn kiểm auth. | [INT-13](labs/integration/INT-13.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Refresh waiters có một owner/generation và failure completion rõ. | [INT-14](labs/integration/INT-14.md) |
| [web/10_IDENTITY_SECURITY.md](web/10_IDENTITY_SECURITY.md#9-invariants) | Response401 cũ không xóa session mới hơn. | [INT-15](labs/integration/INT-15.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Rollback chỉ tác động state còn thuộc mutation đó. | [INT-16](labs/integration/INT-16.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | FE cache invalidation/update giữ consistency policy sau mutation. | [INT-17](labs/integration/INT-17.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | BE cache không vượt stale window/scope và tránh refill race. | [INT-18](labs/integration/INT-18.md) |
| [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) + [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md#9-invariants) | Cùng business intent POST không tạo hai hiệu ứng qua retry. | [INT-19](labs/integration/INT-19.md) |
| [web/12_HTTP_SEMANTICS.md](web/12_HTTP_SEMANTICS.md#9-invariants) + [web/15_DATABASE_TRANSACTIONS.md](web/15_DATABASE_TRANSACTIONS.md#9-invariants) | Timeout không được giả định operation chưa commit; outcome được reconcile. | [INT-20](labs/integration/INT-20.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Upload limits/type/error hợp đồng được giữ xuyên proxy/API/client. | [INT-21](labs/integration/INT-21.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Reconnect khôi phục snapshot/history gap theo protocol. | [INT-22](labs/integration/INT-22.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Stale event không làm state/version quay ngược. | [INT-23](labs/integration/INT-23.md) |
| [web/11_INTEGRATION_FLOW.md](web/11_INTEGRATION_FLOW.md#9-invariants) | Duplicate delivery không biến thành business operation mới. | [INT-24](labs/integration/INT-24.md) |
| [web/08_API_CONTRACTS.md](web/08_API_CONTRACTS.md#9-invariants) | Old/new clients/server tương thích trong rollout window đã định. | [INT-25](labs/integration/INT-25.md) |
| [os/04_CONCURRENCY.md](os/04_CONCURRENCY.md#9-invariants) | Lock acquisition/release không tạo cycle chờ. | [OS-01](labs/os/OS-01.md) |
| [os/04_CONCURRENCY.md](os/04_CONCURRENCY.md#9-invariants) | Conflicting accesses có synchronization/happens-before hợp lệ. | [OS-02](labs/os/OS-02.md) |
| [os/03_IO_IPC_LIFETIME.md](os/03_IO_IPC_LIFETIME.md#9-invariants) | FD/resource được close đúng owner trên success/error paths. | [OS-03](labs/os/OS-03.md) |
| [os/03_IO_IPC_LIFETIME.md](os/03_IO_IPC_LIFETIME.md#9-invariants) | Parent reap child exit state/status theo lifecycle. | [OS-04](labs/os/OS-04.md) |
| [os/02_VIRTUAL_MEMORY.md](os/02_VIRTUAL_MEMORY.md#9-invariants) + [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) | Retention bounded theo business lifecycle, không giữ payload vô ích mãi. | [OS-05](labs/os/OS-05.md) |
| [os/02_VIRTUAL_MEMORY.md](os/02_VIRTUAL_MEMORY.md#9-invariants) + [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) | Access chỉ xảy ra khi object/storage lifetime còn hợp lệ. | [OS-06](labs/os/OS-06.md) |
| [os/02_VIRTUAL_MEMORY.md](os/02_VIRTUAL_MEMORY.md#9-invariants) + [embedded_systems/02_MEMORY_BUILD.md](embedded_systems/02_MEMORY_BUILD.md#9-invariants) | Call depth/work có bounds để không vượt stack budget. | [OS-07](labs/os/OS-07.md) |
| [web/02_JS_RUNTIME.md](web/02_JS_RUNTIME.md#9-invariants) + [os/01_KERNEL_PROCESS.md](os/01_KERNEL_PROCESS.md#9-invariants) | Agent không bị CPU callback chặn vượt responsiveness budget. | [OS-08](labs/os/OS-08.md) |
| [web/14_DOTNET_ASYNC_RUNTIME.md](web/14_DOTNET_ASYNC_RUNTIME.md#9-invariants) + [os/04_CONCURRENCY.md](os/04_CONCURRENCY.md#9-invariants) | Workers không đồng bộ chờ work cần chính pool đã bị giữ hết. | [OS-09](labs/os/OS-09.md) |
| [os/04_CONCURRENCY.md](os/04_CONCURRENCY.md#9-invariants) | Lock owner được progress theo priority protocol phù hợp target. | [OS-10](labs/os/OS-10.md) |
| [os/03_IO_IPC_LIFETIME.md](os/03_IO_IPC_LIFETIME.md#9-invariants) | Use access đúng trusted object, không dựa path check có thể đổi trước open. | [OS-11](labs/os/OS-11.md) |

[Index](00_INDEX.md) · [Coverage](THEORY_COVERAGE_MATRIX.md) · [Validation](VALIDATION.md).
