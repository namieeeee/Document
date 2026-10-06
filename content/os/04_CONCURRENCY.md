# Outline — OS concurrency: happens-before, waits và progress

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Unsynchronized data race, missed predicate notifications/spurious wake, deadlock, livelock retry same phase, starvation high work, inversion lower owner blocked by medium, same-pool wait, lifetime dangling. Thread-safe methods composing check/read/write can still logical race.

Đặt câu hỏi: cơ chế trong [OS concurrency: happens-before, waits và progress](../../os/04_CONCURRENCY.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
producer lock → change predicate/data → unlock → notify
consumer lock → while !predicate: wait(lock)
→ predicate true under lock → consume/change state → unlock
```

Wake doesn't guarantee predicate remains true before lock reacquired. Acquire/release publication flag code needs one-shot/reuse protocol; resetting flag while consumer reads requires generations/exclusion.

## 3. Demo chạy thật

Claim có phạm vi: Every protected access same protocol; predicate checked under lock after every wake; no circular wait; producer/release able to run; atomics publication ordered and storage live; queue/cancel/full bounded. Lock process-local not multi-process/database replicas unless designed interprocess primitive.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../os/04_CONCURRENCY.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Unsynchronized data race, missed predicate notifications/spurious wake, deadlock, livelock retry same phase, starvation high work, inversion lower owner blocked by medium, same-pool wait, lifetime dangling. Thread-safe methods composing check/read/write can still logical race.

Thread stacks+owner/wait graph with IDs/timestamps, ThreadSanitizer host if support, forced barriers on original interleaving, queue delay/progress/CPU metrics. Data-race-free not logical race-free; stress passes no absence proof. Kernel locks and user locks require different tools/context.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[C++17 N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [pthread_cond_wait](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3.html), [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [OSTEP condition variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf), [TSan docs](https://clang.llvm.org/docs/ThreadSanitizer.html).

1. CV wait loop why? Đáp án:spurious/competing consumers.
2. Relaxed flag publishes payload? Đáp án:no guarantee appropriate synchronization.
3. All methods thread-safe composition? Đáp án:may still race across steps.
4. Deadlock needs CPU high? Đáp án:no waiting.
5. Seq_cst keeps freed buffer alive? Đáp án:no.
6. Pool workers all wait children issue? Đáp án:capacity wait cycle.

[Index](../../00_INDEX.md) · [Content](../README.md).
