# Nguồn, phiên bản và phạm vi kiểm chứng

## Phase theory-first — 2026-10-06

Nguồn của 39 bài canonical được truy cập và đối chiếu theo [THEORY_SOURCE_VERIFICATION](THEORY_SOURCE_VERIFICATION.md). Ledger ghi body available, version, path substitutions và failures; không coi URL hoặc trang index là đã đọc toàn manual. React19/Next15/.NET8/Mongo8/PG16/CMSIS6/FreeRTOS11.1/Zephyr3.7 là phạm vi cụ thể. Những blocks dưới thuộc các phase trước, giữ ngày/giới hạn lịch sử; status timeout N1570 cũ không phải kết quả mới (PDF hiện truy cập được).

Ngày truy cập: **2026-10-05**. Các link dưới đã đọc được nội dung bằng web tool, trừ mục được ghi thất bại. Nguồn là nền cơ chế, không chứng minh lab tự xây đã chạy. Không sao chép code sách/tài liệu vào lab. Tài liệu latest/main có thể đổi; triển khai cần pin release và đọc manual đúng target.

## Web và .NET

| Nguồn chính thức | Dùng cho | Phạm vi |
|---|---|---|
| [React snapshot](https://react.dev/learn/state-as-a-snapshot) | State/closure | Tài liệu hiện hành; không pin React của fixture |
| [React effects](https://react.dev/learn/synchronizing-with-effects) | Lifecycle/cleanup/dependencies | Không thay test race của ứng dụng |
| [Next.js boundaries](https://nextjs.org/docs/app/getting-started/server-and-client-components) | Server/client App Router | Đọc phiên bản hiện hành, đối chiếu lockfile |
| [Next.js caching](https://nextjs.org/docs/app/getting-started/caching) | Cache Components | Không trộn mặc định các phiên bản |
| [Next.js previous cache model](https://nextjs.org/docs/app/guides/caching-without-cache-components) | Cấu hình không Cache Components | Có nhãn previous model |
| [TS narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) | Runtime guard | Assertion không thay validation |
| [MDN execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model) | Agent/job/event loop | MDN là tài liệu nền tảng, không benchmark |
| [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) | Browser cross-origin | CORS không authorization |
| [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html) | HTTP semantics | Không quy định mọi business error envelope |
| [RFC7519](https://www.rfc-editor.org/rfc/rfc7519.html) | JWT claims | Không đủ để tự thiết kế identity provider |
| [.NET middleware](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-8.0) | Pipe line | View .NET8 |
| [.NET DI](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0) | Lifetime/scope | View .NET8 |
| [Resource authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resourcebased?view=aspnetcore-5.0) | Quyền theo đối tượng | Link đọc được là view5, chỉ dùng nguyên tắc; không copy API làm mẫu8 |
| [JWT bearer](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication) | Validation/provider | Trang hiện hành view10 khi đọc; snippet8 chưa được chứng minh bằng trang này |
| [Thread-pool diagnostic](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-threadpool-starvation) | Queue/wait evidence | Tutorial .NET9+, không chạy nguyên tutorial trênSDK8 |
| [OWASP API risks2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) | Auth/object/property/resource risks | Taxonomy, không compliance audit |

## Database

| Nguồn | Dùng cho | Phạm vi |
|---|---|---|
| [MongoDB atomicity](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/) | Conditional update, nhiều document | Single-document atomicity không bảo đảm whole work flow |
| [MongoDB sort/index](https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/) | Compound index/order | Explain cần data set/workload thực |
| [MongoDB unique index](https://www.mongodb.com/docs/manual/core/index-unique/) | Uniqueness | Deployment/sharding constraints phải đọc theo cấu hình |

## C/C++, MCU và RTOS

| Nguồn | Dùng cho | Phạm vi |
|---|---|---|
| [CERT INT32](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/) | Signed overflow | Có ngoại lệ compiler/atomic types; không nói tất cả integer overflow đềuUB |
| [CERT INT34](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/) | Shift count và operands | Đối chiếu compiler/standard version |
| [C++ lifetime draft](https://eel.is/c++draft/basic.life) | Object lifetime | Draft hiện hành, không tiêu chuẩn đã pin |
| [C++ delete-expression draft](https://eel.is/c++draft/expr.delete) | Delete qua base/destructor | Có nuance destroying delete của chuẩn mới |
| [C++ races draft](https://eel.is/c++draft/intro.races) | Happens-before/data race | Không tự áp dụng C++ thread semantics cho mọi ISR port |
| [Vector capacity draft](https://eel.is/c++draft/vector.capacity) | reserve/reallocation | Không là WCET guarantee |
| [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html) | Qualifier/compiler ordering | Implementation GCC, không CPU cache maintenance manual |
| [CMSIS Core6](https://arm-software.github.io/CMSIS_6/latest/Core/index.html) | Core services/startup/NVIC | Overview; không substitute MCU register reference |
| [CMSIS NVIC](https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html) | Priority/vector/exception API | API/core có ngoại lệ khác nhau |
| [CMSIS D-cache M7](https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html) | Cache maintenance theo vùng | Không mọi Cortex-M có D-cache |
| [Free RTOS docs](https://docs.freertos.org/) | Nền RTOS | Overview đọc được |
| [Free RTOS semphr.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h) | Semaphore/mutex API contract | Main development branch, cần pin release trước triển khai |
| [Free RTOS task.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h) | Task/stack depth contracts | Main development branch; port-specific |
| [Zephyr scheduling](https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html) | Cooperative/preemptive scheduling | Latest, cấu hình ảnh hưởng hành vi |
| [Zephyr mutex](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html) | Ownership/inheritance | Không dùng mutex trong ISR |
| [Zephyr message queues](https://docs.zephyrproject.org/latest/kernel/services/data_passing/message_queues.html) | Copy message/bounded queue | Pointer trong message vẫn cần ownership |
| [Zephyr threads](https://docs.zephyrproject.org/latest/kernel/services/threads/index.html) | Lifecycle/stack | Latest; cấu hình và arch-specific |

## OS/debug

| Nguồn | Dùng cho | Phạm vi |
|---|---|---|
| [Linux memory concepts](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html) | VM/pages | Không thay allocator-specific profiling |
| [Linux mutex design](https://docs.kernel.org/locking/mutex-design.html) | Kernel locks | Kernel context khác user mutex |
| [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html) | Reap child | Linux/POSIX, không Windows API |
| [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) | Durability/directory sync | Filesystem/storage có giới hạn riêng |
| [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) | Debug entrypoint | Đọc index; lệnh cụ thể phải kiểm target hỗ trợ |
| [Python3.11 tracemalloc](https://docs.python.org/3.11/library/tracemalloc.html) | Python allocations | Không toàn native/kernel memory |
| [OSTEP tác giả](https://pages.cs.wisc.edu/~remzi/OSTEP/) | Lộ trình học OS | Đã đọc index, không tuyên bố đã đọc toàn sách |

## Truy cập thất bại và phần cần đối chiếu tiếp

- WG14 N1570 PDF tại open-std.org: web tool timeout hai lượt. Không dùng số clause từ PDF chưa đọc; dùng CERT cho signed overflow, ghi phần chuẩn cần đọc khi kiểm compliance.
- Một số Free RTOS Documentation feature URL: fetch thất bại/không có body. Thay bằng header chính thức đọc được, không cite URL thất bại để chứng minh claim.
- Microsoft view8 JWT/resource-authorization/SignalR và performance-best-practices: một số lần fetch thất bại. Dùng nguồn khái niệm đọc được và ghi version khác; chưa cung cấp client SignalR executable.
- Chưa chọn board cụ thể nên chưa xác minh reference manual MCU, cache/DMA errata, pinout, clock tree. Các mục chip-specific là điều kiện cần bổ sung trước firmware thật.
- Chưa đối chiếu toàn bộ MISRA/AUTOSAR/ISO26262 bản licensed. Giáo trình không tuyên bố compliant hoặc dựng rule number.

[Inventory nội bộ](SOURCE_INVENTORY.md) · [Corrections](CORRECTIONS.md) · [Validation](VALIDATION.md).

## Nguồn bổ sung đã đọc —2026-10-06

Các link sau có body truy cập được bằng web tool trong lượt mở rộng; giữ phần diễn giải độc lập, không sao chép dài. Official/primary theo publisher. Older retained links giữ ngày đọc2026-10-05, không giả mọi nguồn được re-fetch hôm nay.

- [arm-software.github.io — group__Core__Register__gr.html](https://arm-software.github.io/CMSIS_6/latest/Core/group__Core__Register__gr.html)
- [arm-software.github.io — startup_c_pg.html](https://arm-software.github.io/CMSIS_6/latest/Core/startup_c_pg.html)
- [cheatsheetseries.owasp.org — Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [cheatsheetseries.owasp.org — Cross_Site_Scripting_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [cheatsheetseries.owasp.org — Password_Storage_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [cheatsheetseries.owasp.org — Session_Management_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [developer.mozilla.org — What_is_a_URL](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL)
- [developer.mozilla.org — Microtask_guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)
- [developer.mozilla.org — box-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing)
- [developer.mozilla.org — label](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/label)
- [developer.mozilla.org — Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [developer.mozilla.org — Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)
- [developer.mozilla.org — Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number)
- [gcc.gnu.org — Optimize-Options.html](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
- [learn.microsoft.com — model-binding?view=aspnetcore-8.0](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0)
- [learn.microsoft.com — asynchronous-programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [learn.microsoft.com — value-types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)
- [learn.microsoft.com — fundamentals](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals)
- [learn.microsoft.com — the-managed-thread-pool](https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool)
- [man7.org — intro.2.html](https://man7.org/linux/man-pages/man2/intro.2.html)
- [man7.org — mmap.2.html](https://man7.org/linux/man-pages/man2/mmap.2.html)
- [man7.org — pipe.7.html](https://man7.org/linux/man-pages/man7/pipe.7.html)
- [man7.org — signal.7.html](https://man7.org/linux/man-pages/man7/signal.7.html)
- [nextjs.org — linking-and-navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating)
- [react.dev — preserving-and-resetting-state](https://react.dev/learn/preserving-and-resetting-state)
- [react.dev — render-and-commit](https://react.dev/learn/render-and-commit)
- [sourceware.org — SECTIONS.html](https://sourceware.org/binutils/docs/ld/SECTIONS.html)
- [www.postgresql.org — transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)
- [www.rfc-editor.org — rfc5789.html](https://www.rfc-editor.org/rfc/rfc5789.html)
- [www.rfc-editor.org — rfc9111.html](https://www.rfc-editor.org/rfc/rfc9111.html)
- [www.rfc-editor.org — rfc9114.html](https://www.rfc-editor.org/rfc/rfc9114.html)
- [www.typescriptlang.org — generics.html](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [www.typescriptlang.org — type-compatibility.html](https://www.typescriptlang.org/docs/handbook/type-compatibility.html)

Giới hạn bổ sung: trang tổng quan OWASP cheat-sheets fetch thất bại, đã dùng các cheat sheet cụ thể đọc được. STM32 RM0090 PDF bị web tool từ chối do kích thước 10842112 bytes; chưa dùng nó chứng minh register/timing chip-specific. Không dựng board address hoặc nói đã đọc manual ấy. Latest docs/drafts không thay release/compiler/port đã pin của dự án.
