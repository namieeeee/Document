# 07 — Từ RTOS đến hệ điều hành tổng quát

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Systems10 — Kernel, process, memory và I/O](embedded_systems/10_OS_KERNEL_USERSPACE.md)
- [Systems08 — Main, ISR, DMA và task cùng một buffer](embedded_systems/08_CONCURRENCY_BUFFERS.md)

Mục tiêu: hiểu process/thread, virtual memory, scheduling và tài nguyên kernel đủ để debug. Tiền đề chương 05–06. Bài thực hành Linux/POSIX không mặc nhiên chạy trên Windows; dùng VM/container Linux đúng cấu hình, không đụng production.

## process không phải thread lớn hơn

Process có không gian địa chỉ và tài nguyên; thread trong process chia sẻ nhiều dữ liệu nhưng có execution state/stack riêng. Thread khác vẫn có thể truy cập object nếu được trao địa chỉ và lifetime còn hợp lệ. Context switch lưu/phục hồi state cần thiết; chi phí gồm scheduling/cache/TLB tùy hệ thống, không có một số cycle universal.

RTOS trên MCU thường dùng RAM hữu hạn và memory map cố định, có thể có MPU; general-purpose OS thường có virtual memory/MMU, process isolation và paging. Không khẳng định mọi RTOS không có protection hoặc mọi OS đều có swap. [Linux memory concepts](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html).

## memory và I/O lifetime

Virtual address không phải physical address. Page fault có thể là demand allocation hoặc lỗi protection; “fault” không luôn crash. RSS, heap used và virtual size đo khác nhau. Leak là tài nguyên không còn hữu ích nhưng vẫn bị giữ; fragmentation là free space không phù hợp request; allocation churn gây overhead mà chưa chắc leak. GC không giải phóng file descriptor/socket đúng thời điểm nghiệp vụ.

File descriptor là handle đến kernel resource. `close` cần đi trên cả success/error paths; ownership hai lớp wrapper có thể double close. Pipe/socket cần xử lý partial read/write, EOF và interrupted call theo API. Child exit để lại trạng thái cần parent reap bằng wait-family; zombie không đang chạy CPU như process bình thường. [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html).

IPC chọn theo semantics: pipe stream, socket stream/datagram, shared memory cần synchronization, queue có capacity. Stream không giữ boundary message: framing bằng length/delimiter cần bounds và partial-data state machine.

## concurrency và persistence

Deadlock cần vòng chờ; tạo lock order nhất quán hoặc tránh giữ lock qua call không kiểm soát. Race condition là kết quả phụ thuộc interleaving; C++ data race cụ thể có thể gây UB. Mutex bảo vệ invariant của dữ liệu dùng cùng lock, không toàn chương trình. Kernel mutex có context constraints riêng, không lấy kernel rule thay cho user mutex. [Linux mutex design](https://docs.kernel.org/locking/mutex-design.html), [C++ data races](https://eel.is/c++draft/intro.races).

Priority inversion cũng xuất hiện trên OS; scheduler fairness không bảo đảm deadline. Thread-pool starvation là thiếu worker khả dụng trong khi nhiều worker chờ/block; CPU có thể chưa đầy. Event loop bị một callback CPU dài chặn dù không có mutex. Đo queue delay và wall/CPU time để phân biệt.

“Ghi temp rồi rename” có thể bảo đảm người đọc thấy một tên file theo filesystem semantics, nhưng chưa tự bảo đảm dữ liệu bền sau power loss. Cần xét flush user space, fsync file và directory, filesystem/mount và lỗi I/O. [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html). Không giả định cùng guarantee trên mọi filesystem/Windows API.

## TOCTOU

Check file tồn tại/quyền rồi mở bằng path là hai operation; path có thể đổi giữa chúng. Giảm khoảng cách chưa loại race. Dùng API atomic/open flags và xác minh qua handle theo threat model; sandbox lab trong thư mục giả. Không tạo exploit trên thư mục hệ thống.

## Thực hành và tự kiểm tra

[11 lab OS](labs/os/README.md). Chạy leak/timing bằng workload có giới hạn. [OSTEP của tác giả](https://pages.cs.wisc.edu/~remzi/OSTEP/) là lộ trình đọc thêm virtualization, concurrency và persistence; index này không chứng minh đã đọc hết sách. Python [tracemalloc](https://docs.python.org/3.11/library/tracemalloc.html) đo Python allocations, không toàn bộ RAM/native allocations.

1. Vì sao một process nhiều virtual memory chưa chắc leak?
2. Mutex có bảo vệ dữ liệu caller không dùng mutex không?
3. Child exit khác parent đã reap thế nào?
4. Stream cần framing vì sao?
5. Vì sao rename chưa đủ để cam kết power-loss durability?

Hoàn thành khi chọn được metric/tool theo giả thuyết và giải thích chỗ mô hình RTOS khác OS. Tiếp [08](08_DEBUGGING_PLAYBOOK.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [OS-03](labs/os/OS-03.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Handle kernel không được close theo lifecycle, dù object user có thể được thu hồi. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: FD/resource được close đúng owner trên success/error paths.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Đợi GC thay close FD deterministic.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](embedded_systems/10_OS_KERNEL_USERSPACE.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
