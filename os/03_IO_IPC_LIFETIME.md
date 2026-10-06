# I/O, IPC và resource acquire-use-release

Phạm vi: Linux/POSIX file/FD/socket/pipe/signal/wait contracts; không Windows equivalent API/durability claims.

## 1. Mục tiêu học

Theo handles/backing objects, partial I/O/EOF/framing, child/signal lifecycle, và thiết kế release đúng owner cho memory/file/socket/thread/process/lock/device/buffer.

## 2. Kiến thức tiên quyết

[Kernel/threads](01_KERNEL_PROCESS.md), [VM/mmap](02_VIRTUAL_MEMORY.md), memory/ownership. Học tiếp [Concurrency](04_CONCURRENCY.md) cho shared handles; không là dependency ngược.

## 3. Vấn đề mà cơ chế này giải quyết

Kernel resources không là object GC thu tùy ý. Paths có thể đổi, streams trả partial bytes, IPC giữ endpoints, và failure paths vẫn acquire resources; cần protocol lifetime/backpressure.

## 4. Khái niệm

Filesystem names→file objects, fd là integer handle trong process tới open-file description/resource theo Linux. Socket có stream/datagram types, pipe unidirectional byte stream. IPC shared memory needs synchronization; signal is asynchronous notification with mask/delivery/handler constraints.

## 5. Thành phần bên trong

Open creates descriptor/ref→read/write operations use object→close drops descriptor ref. Dup/fork may share open file description/offset. Path rename/unlink không always end opened object's lifetime. TOCTOU check path then open gap may resolve different object; handle-based validation/atomic open flags theo threat model.

Pipe EOF when no write-end refs and queued data exhausted; forgotten inherited writer keeps reader waiting. Socket stream network close/half-close has semantics, read0 EOF; datagrams giữ message units nhưng truncation/limits theo API.

## 6. Data representation

FD tables/references, stream offsets/kernel queues, application framing buffer `(expectedLength,received,limit)`, child exit status, signal disposition/mask. Standard signals may coalesce, realtime signals different; handler restricted async-signal-safe calls, không mutex/malloc/printf freely.

## 7. Control flow

Acquire→validate→use with loop handling partial/EINTR/nonblocking readiness per API→release success/error/cancel. Parent start child→close unused IPC ends→read/write→wait/reap; thread join/detach theo contract. Poll readiness not promise next operation succeeds forever, races/other consumers remain.

## 8. Lifetime / ownership / state

Resource table:

| Resource | Owner/use boundary | Release |
|---|---|---|
| memory/buffer | allocate/pool token + borrowers | free/return after readers stop |
| file/socket/device | valid handle, async I/O may pending | close after handoff/quiesce |
| thread | execution + join state | join/detach cleanup contract |
| process | child lifecycle/status | wait after exit |
| lock | owner protected invariant | unlock every acquired path |
| mapping | address region | munmap independently FD |

Handle reused number can refer new resource after close; double-close can close wrong new descriptor.

## 9. Invariants

Owned handles close exactly once; EOF endpoint ownership correct; frame length/work bounded; child status reaped; async handlers use allowed operations; check/use same trusted object. Durability different visibility: flush/fsync file/directory/storage constraints, rename not alone power-loss proof.

## 10. Ví dụ tối thiểu

**Pseudo stream parser**: read up to header4 loop until complete/EOF/error→decode length with cap→read body loop until length complete→publish. One read header4 may return2, not malformed yet; EOF mid-body is truncated frame.

Temp-write+rename model: write file→flush user buffer→fsync file→rename in supported filesystem→fsync directory for durability requirements; error outcomes/cross-filesystem constraints still matter. No executed power-loss claim.

## 11. Failure modes

FD leak, double-close reused number, pipe reader stuck inherited writer, zombie child, partial framing OOB, signal handler unsafe deadlock, path TOCTOU, assumed durability. Fix owners/bounded parser/handle validation/reap, no forceGC or sleep.

## 12. Debug / observability

FD inventory before/after bounded success/error batches, endpoint owner graph, thread stacks/syscall wait, child state/parentPID, mapped regions and read counts. Synthetic path replacement fixture in temp only. Strace/per-process inspection Linux required; not claim run Windows.

## 13. Liên hệ với bug/lab hiện có

[OS-03](../labs/os/OS-03.md), [OS-04](../labs/os/OS-04.md), [OS-06](../labs/os/OS-06.md), [OS-11](../labs/os/OS-11.md).

## 14. Sai lầm thường gặp

Fd integer not object identity forever; close wrapper≠all refs gone; stream read≠one message; standard signal≠counted queue; GC≠deterministic native release; rename visibility≠power-loss durability.

## 15. Câu hỏi tự kiểm tra

1. Why no EOF child exited? Đáp án:other write refs.
2. Read2 of requested4? Đáp án:partial normal, accumulate.
3. Close fd then mmap live? Đáp án:yes mapping separate.
4. Double close dangerous? Đáp án:number reused resource.
5. Signal printf always safe? Đáp án:not async-signal-safe contract.
6. Rename guarantee full durability? Đáp án:no fsync/storage scope.

## 16. Nguồn

[open(2)](https://man7.org/linux/man-pages/man2/open.2.html), [close(2)](https://man7.org/linux/man-pages/man2/close.2.html), [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html), [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html), [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html), [signal-safety(7)](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
