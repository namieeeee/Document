# Outline — RTOS scheduler: task states và context switch

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Starvation, priority inversion, deadlock/livelock, queue overflow, notifications coalescing misunderstood, timer callback blocks, stack overflow, API from invalid ISR, tick wrap naive compare. Fix waits/owner/order/budgets, không tăng mọi priorities.

Đặt câu hỏi: cơ chế trong [RTOS scheduler: task states và context switch](../../embedded_systems/09_RTOS_SCHEDULER.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
READY → RUNNING → BLOCKED(event/timeout)
RUNNING → READY khi preempt/yield theo policy
BLOCKED → READY khi event/timeout, không chạy ngay guarantee
READY selected → context switch → resume sau wait
```

Preemptive scheduler có thể chuyển khi higher-priority task ready; cooperative contexts need block/yield theo kernel rules. Equal-priority time slicing/config quyết distribution. Busy highest-priority consumer can starve producer thấp nó đang đợi.

## 3. Demo chạy thật

Claim có phạm vi: Every wait có producer/release reachable; all protected accesses use same lock; lock order no circular wait; full/timeout/drop outcomes handled. Critical sections bounded; correct ISR API/context/priority threshold. Ready≠deadline guarantee; stack depth units FreeRTOS StackType_t vs bytes API khác, watermarks observed only.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/09_RTOS_SCHEDULER.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Starvation, priority inversion, deadlock/livelock, queue overflow, notifications coalescing misunderstood, timer callback blocks, stack overflow, API from invalid ISR, tick wrap naive compare. Fix waits/owner/order/budgets, không tăng mọi priorities.

RTOS trace states/reasons/ready→run delay/lock owner/IRQ durations, stack watermarks+call paths, queue/drop progress counters. Force empty/full/late release; graph waiter→owner→dependency. Inheritance mutex experiment tách inversion từ deadlock; high CPU có thể busy spin hoặc useful work, cần progress evidence.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[FreeRTOS11.1 tasks.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/tasks.c), [task.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/include/task.h), [queue.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/queue.c), [semphr.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/include/semphr.h), [M4F port](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/portable/GCC/ARM_CM4F/port.c), [timers.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/timers.c), [Zephyr3.7 scheduling](https://docs.zephyrproject.org/3.7.0/kernel/services/scheduling/index.html), [mutex](https://docs.zephyrproject.org/3.7.0/kernel/services/synchronization/mutexes.html), [timers](https://docs.zephyrproject.org/3.7.0/kernel/services/timing/timers.html).

1. Blocked task consumes spin CPU? Đáp án:no.
2. Wake runs immediately? Đáp án:ready, policy/interference determines.
3. FreeRTOS/Zephyr same priority number meaning? Đáp án:no.
4. Timer callback ISR? Đáp án: FreeRTOS timer task; Zephyr3.7 k_timer expiry ở clock ISR. Không dùng cùng một quy tắc cho hai kernel.
5. Queue pointers deep copied? Đáp án:no.
6. Stack depth100 always100bytes? Đáp án:API/port units.

[Index](../../00_INDEX.md) · [Content](../README.md).
