# 08 — Debug: biến triệu chứng thành phép thử

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Debug dùng chung hai track — bằng chứng trước kết luận](debug/01_EVIDENCE_METHOD.md)

Mục tiêu: sửa lỗi dựa trên evidence, giảm thử ngẫu nhiên. Dùng sau một nhánh chương 02–07. Không cần chạy mọi tool; chọn tool trả lời câu hỏi hiện tại.

## biên bản tối thiểu

Ghi phiên bản/build, input, expected/actual, bước tái hiện, tần suất và boundary. “Đôi khi lỗi” cần timeline: event nào trước/sau, request/version nào sở hữu dữ liệu. Giữ fixture nhỏ; chụp trước khi sửa. Tách quan sát (“response401”) khỏi inference (“token hết hạn”) vì signature sai cũng có thể401.

## vòng lặp bằng chứng

1. Thu nhỏ tái hiện mà giữ failure; không cắt phần concurrency gây lỗi.
2. Nêu 2–3 giả thuyết và dự đoán khác nhau của chúng.
3. Chọn phép đo phân biệt ít tác động nhất.
4. Chỉ sửa sau khi evidence ủng hộ cơ chế; ghi điều gì bác bỏ giả thuyết.
5. Regression trên trigger gốc, case biên và failure path.

Ví dụ UI hiển thị query A dù input B: giả thuyết cache sai hoặc response đảo thứ tự. Network cho A300 ms/B20 ms; thêm request Id ở apply log. Nếu A apply sau B, race có bằng chứng; nếu response đúng nhưng reducer chọn state cũ, điều tra state mapping. Disable cache là phép thử phụ, không phải fix mặc định.

## công cụ theo tầng

| Câu hỏi | Bằng chứng | Giới hạn |
|---|---|---|
| Request có đến BE? | Network + trace Id API | Browser error không luôn là server error |
| DB chậm hay queue chậm? | Dependency timing + explain + queue delay | Query plan cần dữ liệu đại diện |
| Ai ghi buffer? | Watchpoint + ownership trace | DMA có thể không kích CPU watchpoint theo debug system |
| ISR quá lâu? | GPIO pulse/trace với timestamp | Instrumentation thay đổi timing |
| Thread bị giữ ở đâu? | Stack sample + wait graph | Snapshot đơn lẻ không thể hiện toàn lịch |
| Memory tăng vì gì? | Allocation snapshots + FD count | Một tool không bao hết native/kernel |

GDB dùng debug symbols để map PC về source, stack để xem call chain, breakpoint/watchpoint để dừng tại event. Optimization có thể inline hoặc loại biến; không coi `<optimized out>` là missing source. Có thể rebuild debug để hiểu, rồi xác nhận bug còn tái hiện build thật. [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) là mục lục chính thức để chọn lệnh đúng target.

Firmware fault: giữ stacked PC/LR/xPSR và fault status theo core, map PC vào ELF đúng build; xem stack bounds, invalid pointer, alignment trước khi đổi clock. Ghi reset reason và build ID. Không đọc register fault của core khác hoặc decode địa chỉ với ELF khác.

## timing và heisenbug

printf, breakpoint và sanitizer có thể đổi lịch hoặc layout. Nếu lỗi biến mất khi debug, dùng bounded ring trace hoặc trigger GPIO ít tác động; vẫn đo overhead. Race không được bác bỏ bằng100 lần không lỗi. Thiết kế barrier/delay để buộc interleaving và kiểm invariant. Không tự đặt “confidence95%” nếu chưa có mô hình thống kê phù hợp.

## Performance khác correctness

Trước tối ưu, kiểm kết quả đúng và workload đại diện. Đo warmup, p50/p95/p99, CPU/wall, allocations và throughput cùng limits. Chỉ thay một yếu tố trong thí nghiệm; báo hardware/config. Không mang claim tốc độ10–20 x trong tài liệu nội bộ thành cam kết. Queue đầy có thể là burst, consumer chậm hoặc capacity sai; tăng capacity chỉ trì hoãn lỗi nếu arrival rate bền vượt service rate.

## Nối mô hình giữa các tầng

| Mẫu chung | Web/OS | Embedded/RTOS | Không được đồng nhất |
|---|---|---|---|
| Công việc chờ được phục vụ | Event loop job, continuation async, thread-pool queue | Task ready, ISR signal, ring buffer | await không tự là task RTOS hoặc interrupt |
| Ownership thay đổi theo thời gian | Request generation, optimistic mutation version | DMA buffer state, queue pool ownership | GC giữ object sống không bảo đảm frame coherent |
| Atomicity của invariant | DB conditional update, mutex user-space | Critical section/atomic theo core và port | Lock process-local không khóa nhiều API replica |
| Budget và recovery | Deadline, cancel, retry/backoff | Deadline, timeout, watchdog reset | Cancel/timeout không chứng minh side effect chưa xảy ra |
| Memory bị giữ | Closure/cache, managed heap, virtual pages | Static RAM, task stack, bounded pool | RSS, heap used và static RAM không cùng metric |

Khi chuyển kinh nghiệm từ web sang firmware, giữ câu hỏi về ownership/progress nhưng thay bằng chứng và guarantee theo target. Queue bounded cần biết arrival/service rate ở cả hai; tăng capacity không thay throughput dài hạn.

## Thực hành

Chọn một lab [casebook](09_REAL_BUG_CASEBOOK.md), viết biên bản trước khi mở Fix. Chạy [mô phỏng độc lập](examples/README.md) để quan sát timeline race, không coi nó thay browser/MCU.

1. Một phép thử nào bác bỏ giả thuyết cache?
2. Watchpoint có bắt được mọi DMA write không?
3. Vì sao test tuần tự không kiểm lost update?
4. Test xanh chứng minh điều gì trong phạm vi fixture?
5. Vì sao cần ELF đúng build?

Hoàn thành khi có reproducer, evidence, root cause và regression giải thích được. Tiếp [10](10_AI_ASSISTED_CODING_AND_DEBUG.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [OS-09](labs/os/OS-09.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Tất cả worker chờ công việc chỉ chính pool đó mới chạy được. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Workers không đồng bộ chờ work cần chính pool đã bị giữ hết.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Tăng workers một ít nhưng nested blocking protocol không đổi.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](web/06_CSHARP_RUNTIME.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
