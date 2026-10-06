# Outline — I/O, IPC và resource acquire-use-release

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

FD leak, double-close reused number, pipe reader stuck inherited writer, zombie child, partial framing OOB, signal handler unsafe deadlock, path TOCTOU, assumed durability. Fix owners/bounded parser/handle validation/reap, no forceGC or sleep.

Đặt câu hỏi: cơ chế trong [I/O, IPC và resource acquire-use-release](../../os/03_IO_IPC_LIFETIME.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Acquire→validate→use with loop handling partial/EINTR/nonblocking readiness per API→release success/error/cancel. Parent start child→close unused IPC ends→read/write→wait/reap; thread join/detach theo contract. Poll readiness not promise next operation succeeds forever, races/other consumers remain.

## 3. Demo chạy thật

Claim có phạm vi: Python context manager đóng file trong success/exception path; không đo Linux FD hoặc kernel lifetime.

```text
python examples/systems_models.py
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/systems.log):

```text
PASS file lifecycle success and exception path (host, not Linux FD count)
```

## 4. Cách nó hỏng và cách phát hiện

FD leak, double-close reused number, pipe reader stuck inherited writer, zombie child, partial framing OOB, signal handler unsafe deadlock, path TOCTOU, assumed durability. Fix owners/bounded parser/handle validation/reap, no forceGC or sleep.

FD inventory before/after bounded success/error batches, endpoint owner graph, thread stacks/syscall wait, child state/parentPID, mapped regions and read counts. Synthetic path replacement fixture in temp only. Strace/per-process inspection Linux required; not claim run Windows.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[open(2)](https://man7.org/linux/man-pages/man2/open.2.html), [close(2)](https://man7.org/linux/man-pages/man2/close.2.html), [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html), [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html), [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html), [signal-safety(7)](https://man7.org/linux/man-pages/man7/signal-safety.7.html), [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html).

1. Why no EOF child exited? Đáp án:other write refs.
2. Read2 of requested4? Đáp án:partial normal, accumulate.
3. Close fd then mmap live? Đáp án:yes mapping separate.
4. Double close dangerous? Đáp án:number reused resource.
5. Signal printf always safe? Đáp án:not async-signal-safe contract.
6. Rename guarantee full durability? Đáp án:no fsync/storage scope.

[Index](../../00_INDEX.md) · [Content](../README.md).
