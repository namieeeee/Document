# OS concurrency: happens-before, waits và progress

Phạm vi: C++17 thread memory model và POSIX/Linux user-space synchronization; kernel mutex context khác. Pseudocode không portable ISR/DMA algorithm.

## 1. Mục tiêu học

Phân biệt race/data race, chọn mutex/semaphore/condition variable/atomic/order, vẽ deadlock/starvation/inversion/pool wait graphs.

## 2. Kiến thức tiên quyết

[Threads](01_KERNEL_PROCESS.md), [memory](02_VIRTUAL_MEMORY.md), [resource lifetime](03_IO_IPC_LIFETIME.md).

## 3. Vấn đề mà cơ chế này giải quyết

Shared address space không chỉ chứa values mà có interleavings/visibility. Invariant nhiều steps và waits cần mutual exclusion/publication/progress protocol; atomic scalar chỉ giải một part.

## 4. Khái niệm

Race condition broader outcome depends ordering; C++ data race conflicting memory accesses from threads without happens-before at least one non-atomic write → UB per rules. Mutex protects shared invariant, semaphore permits/events, condition variable wakes waiters about predicate changes, atomic has indivisible operations/order semantics.

## 5. Thành phần bên trong

Mutex acquire/release synchronize participants using same lock. Condition variable wait atomically releases lock and blocks, reacquires before return; spurious wakeups/other consumers require predicate loop. Signal not persistent message counter; change predicate under mutex then notify appropriate waiters.

Atomics relaxed gives atomic variable modification rules not unrelated payload publication; release-store/acquire-load seeing it can publish earlier writes. Seq_cst stronger ordering doesn't solve wrong ownership/lifetime or multi-step check-then-act. No arbitrary fence fixes all data races.

## 6. Data representation

Protected predicate/queue state under mutex; wait sets, lock owner graph; atomic flag/counter with explicit ordering; bounded pool pending jobs/workers. CPU cache coherence not language happens-before replacement. Shared buffer stays live and immutable as long consumer accesses.

## 7. Control flow

```text
producer lock → change predicate/data → unlock → notify
consumer lock → while !predicate: wait(lock)
→ predicate true under lock → consume/change state → unlock
```

Wake doesn't guarantee predicate remains true before lock reacquired. Acquire/release publication flag code needs one-shot/reuse protocol; resetting flag while consumer reads requires generations/exclusion.

## 8. Lifetime / ownership / state

Lock acquire owns release responsibility on exception/cancel; RAII lock guard can enforce scope. No destroy mutex/CV with active users/waiters. Queue item pointer lifetime crosses producer thread stack. Pool shutdown stop acceptance→signal workers→drain/cancel with clear outcome→join/release.

## 9. Invariants

Every protected access same protocol; predicate checked under lock after every wake; no circular wait; producer/release able to run; atomics publication ordered and storage live; queue/cancel/full bounded. Lock process-local not multi-process/database replicas unless designed interprocess primitive.

### Publication phải nối payload với tín hiệu

**Pseudocode one-shot giữa hai C++17 threads**, payload non-atomic, ready atomic, producer ghi một lần và không sửa lại khi consumer còn đọc:

```text
Producer: payload = 42
          ready.store(true, release)

Consumer: if ready.load(acquire) == true:
              use(payload)
```

Acquire đọc giá trị từ release tạo synchronization; writes trước publication được nối happens-before tới consumer access sau acquire. Đổi ready thành volatile không tạo quan hệ đó. Relaxed ready vẫn có atomicity riêng của flag nhưng không đủ publication cho non-atomic payload. Dùng atomic payload riêng có thể tránh data race từng field nhưng chưa bảo đảm hai fields cùng một generation.

Protocol one-shot không tự dùng lại được: producer ghi payload mới khi consumer đang đọc sẽ phá exclusion/lifetime. Reusable queue cần slot states hoặc sequence cùng ownership. Seq_cst không làm buffer trở nên immutable và không chặn owner free.

### Vì sao condition variable phải gắn với predicate?

**Schedule lỗi**: C kiểm queue empty ngoài lock; P enqueue và notify; C mới bắt đầu wait. Notification không được giữ như message nên C có thể ngủ dù queue đã có item.

**Protocol đúng**: C lock, kiểm predicate; wait atomically unlock-and-wait theo API; P đổi predicate dưới cùng lock rồi notify; C được wake, reacquire lock và kiểm lại. Thread khác có thể lấy item trước C, hoặc C có spurious wakeup, nên dùng while thay if. Kết quả wake chỉ nói “hãy kiểm state”, không phải “item này thuộc C”.

Nếu cancellation hoặc shutdown cần đánh thức waiters, nó phải đổi một predicate quan sát được dưới protocol, ví dụ stopping hoặc queue-not-empty, rồi notify. Chỉ notify mà không đổi predicate làm waiter quay lại ngủ.

## 10. Ví dụ tối thiểu

**Pseudocode** two threads A lockX→waitY, B lockY→waitX creates cycle. Fixed order X thenY removes this acquisition cycle if all access paths comply; unknown callbacks under lock can add hidden dependency.

Pool2 workers each parent waits child queued same pool→no free worker; increasing to3 may only delay nested saturation. Make parents async/nonblocking or scheduling design with capacity guarantees.

## 11. Failure modes

Unsynchronized data race, missed predicate notifications/spurious wake, deadlock, livelock retry same phase, starvation high work, inversion lower owner blocked by medium, same-pool wait, lifetime dangling. Thread-safe methods composing check/read/write can still logical race.

## 12. Debug / observability

Thread stacks+owner/wait graph with IDs/timestamps, ThreadSanitizer host if support, forced barriers on original interleaving, queue delay/progress/CPU metrics. Data-race-free not logical race-free; stress passes no absence proof. Kernel locks and user locks require different tools/context.

## 13. Liên hệ với bug/lab hiện có

[OS-01](../labs/os/OS-01.md), [OS-02](../labs/os/OS-02.md), [OS-09](../labs/os/OS-09.md), [OS-10](../labs/os/OS-10.md), [BE-16](../labs/backend/BE-16.md) logical composition analog.

## 14. Sai lầm thường gặp

Volatile≠atomic; atomic counter≠whole invariant; notify≠predicate true; fairness≠deadline; inheritance≠deadlock fix; more workers≠nested wait guarantee. Kernel locking docs not user CV semantics.

## 15. Câu hỏi tự kiểm tra

1. CV wait loop why? Đáp án:spurious/competing consumers.
2. Relaxed flag publishes payload? Đáp án:no guarantee appropriate synchronization.
3. All methods thread-safe composition? Đáp án:may still race across steps.
4. Deadlock needs CPU high? Đáp án:no waiting.
5. Seq_cst keeps freed buffer alive? Đáp án:no.
6. Pool workers all wait children issue? Đáp án:capacity wait cycle.

## 16. Nguồn

[C++17 N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [pthread_cond_wait](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3.html), [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [OSTEP condition variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf), [TSan docs](https://clang.llvm.org/docs/ThreadSanitizer.html).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
