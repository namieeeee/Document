# Systems10 — Kernel, process, memory và I/O

> Overview tương thích cho các link cũ, không là bài canonical độc lập. Học theory theo [kernel/process](../os/01_KERNEL_PROCESS.md) → [virtual memory](../os/02_VIRTUAL_MEMORY.md) → [I/O và lifetime](../os/03_IO_IPC_LIFETIME.md) → [concurrency](../os/04_CONCURRENCY.md). Nội dung dưới giữ làm bản tóm tắt; sources/version của bài canonical quyết định phạm vi hiện tại.

Tiền đề memory/concurrency và scheduler; mục tiêu theo syscall/data/resource lifetime đủ để debug, không đi vào P2 kernel implementation. Bài Linux/POSIX có nguồn vendor-specific; không giả nó là Windows API.

## Hardware, privilege và syscall

CPU có execution/protection modes theo kiến trúc. Kernel quản lý privileged operations, scheduling, memory mappings và device access; user space gọi API để yêu cầu dịch vụ. Library function có thể xử lý thuần user space hoặc gọi syscall; syscall chuyển qua entry kiểm soát vào kernel để xử lý, rồi trả result/error. Syscall không tự “tạo process” hoặc luôn gây context switch sang process khác: mode transition khác scheduler switch. [intro(2)](https://man7.org/linux/man-pages/man2/intro.2.html).

Process giữ address-space/resource context; threads chia sẻ nhiều tài nguyên trong process nhưng có execution registers/stack/thread state riêng. Scheduler chọn runnable threads theo policy; blocked I/O thread chờ event để trở lại runnable. Context switch lưu/phục hồi context và có costs cache/TLB/timing tùy system; không có số cycle universal. Process isolation không cấm shared memory có chủ đích, và thread stacks “riêng” không ngăn thread khác dùng pointer được chia sẻ nếu lifetime hợp lệ.

## Virtual memory, page và page fault

Virtual address thuộc process mapping; MMU/page tables dịch sang physical storage với permissions theo system. Page là đơn vị quản lý mapping/protection, size phụ thuộc architecture/config. Allocation virtual range khác actual resident physical pages; lần touch có thể fault để map/init/fetch page. Page fault có thể được xử lý bình thường hoặc là protection/invalid access gây signal; “page fault” không luôn crash. [Linux memory concepts](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html).

Heap allocator cấp blocks trên vùng backing memory; allocator free không hứa RSS giảm ngay. Stack mappings/lifetime khác heap object nhưng đều ở virtual address space. Mmap tạo mapping file/device/anonymous với permissions và shared/private semantics; private copy-on-write không tự ghi thay đổi về file. Mapping còn có lifetime munmap độc lập với descriptor theo API. [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html).

Leak, fragmentation và retention/churn khác nhau. Leak giữ resource không còn hữu ích; fragmentation làm free blocks không đáp ứng request; allocation churn tăng overhead nhưng không nhất thiết memory tăng dài hạn. RSS/virtual size/Python traced heap không cùng metric. UAF dùng pointer sau lifetime hết; GC-managed object vẫn có thể giữ native resource sai lifecycle.

## Filesystem, FD, streams và IPC

Filesystem ánh xạ names tới objects theo semantics; descriptor là handle process dùng để access kernel-managed resource. Rename/path tồn tại không bảo đảm object bạn mở sau check giống object đã kiểm: TOCTOU. Handle-based/atomic operations giảm split check/use theo threat model, không sửa bằng sleep. FD close cần cả error paths; file/socket wrapper GC không thay deterministic close.

Pipe là byte stream với read/write endpoints và EOF khi writers phù hợp đóng; socket có stream/datagram semantics theo type. Stream read có thể partial, không message boundary; length-prefix/delimiter parser cần buffers/bounds/state. Close đúng endpoint ảnh hưởng EOF; forgotten writer có thể khiến reader chờ dù child đã xong. [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html).

IPC shared memory cần synchronization/ownership; queue/socket có buffering và backpressure, không infinite capacity. Signal là notification với delivery/mask/handler semantics, không một task RTOS; handler chỉ dùng operations async-signal-safe theo API, standard signals có thể coalesce. Parent cần wait-family để reap child exit status; zombie đã exit không chạy CPU bình thường. [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html), [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html).

## RTOS so general-purpose OS

RTOS MCU thường RAM hữu hạn, direct memory/peripheral map, scheduler hướng timing; có thể có MPU/protection. OS tổng quát thường MMU/VM/process isolation, filesystem/large I/O ecosystem, scheduling tối ưu nhiều workload; realtime variants/config vẫn tồn tại. Không định nghĩa “RTOS không có kernel/VM” hoặc “Linux luôn không realtime”. Chọn guarantees theo target, không theo nhãn. Lock/data race/deadlock/priority inversion có cơ chế chung nhưng APIs/context/resource policies khác.

Invariant: handles/mappings released đúng owner; pointer access trong lifetime/permissions; wait dependencies có progress; stream framing không vượt buffer; check/use cùng trusted object theo design. Durability còn khác visibility: temp+rename không đủ power-loss guarantee nếu thiếu flush/fsync file/directory và filesystem/storage constraints. [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html).

## Debug section — service treo hoặc memory tăng

- **SYMPTOM:** request không xong, process RSS/FD count tăng hoặc children Z.
- **EVIDENCE:** thread stacks/wait graph, process maps/RSS/heap snapshots, FD list, child state/parent PID và stream endpoint owners.
- **POSSIBLE CAUSES:** deadlock/pool starvation, FD leak, forgotten pipe writer, retention, native leak hoặc chưa reap child.
- **DISTINGUISHING TEST:** bounded batches success/error; compare FD baseline/after; waitpid fixture; heap reachable paths vs RSS; không gộp tăng memory thành leak.
- **ROOT CAUSE:** actor/resource lifetime hoặc wait dependency đầu không đúng, theo metric đúng scope.
- **FIX:** scoped close/reap/munmap, correct lock order/framing/ownership và bounded retention; scheduler policy đúng target nếu cần realtime.
- **WRONG FIX:** kill/restart làm permanent fix, forceGC để chữa FD, tăng threads mà vẫn nested wait, check path rồi sleep mở.
- **REGRESSION TEST:** repeated failure paths, partial I/O/EOF, competing threads, path replacement trong temp directory và lifecycle return-to-baseline.

[11 OS labs](../labs/os/README.md); đọc [OSTEP index của tác giả](https://pages.cs.wisc.edu/~remzi/OSTEP/) cho lộ trình sâu hơn, không tuyên bố đã đọc toàn sách. Questions: syscall có luôn switch process không? Fault có luôn fatal không? RSS tăng chứng minh heap leak không? Ai giữ pipe writer làm EOF không tới? Descriptor close có luôn unmap không?

[Debug method](../debug/01_EVIDENCE_METHOD.md) · [Index](../00_INDEX.md).
