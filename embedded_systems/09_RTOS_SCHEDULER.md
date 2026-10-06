# RTOS scheduler: task states và context switch

Phạm vi: **FreeRTOS-Kernel11.1.0 single-core ARM_CM4F** và **Zephyr3.7.0 single-core** đối chiếu rõ; không apply SMP policy. Config/port thực vẫn phải khóa trước firmware.

## 1. Mục tiêu học

Dự đoán ready/running/blocked transitions, scheduler lựa chọn, context save/restore và primitive hợp data/event/resource. Phân tích deadline ở [real-time](16_REAL_TIME.md), không chỉ thuộc APIs.

## 2. Kiến thức tiên quyết

[CPU/exception](12_CORTEX_M.md), [interrupt](06_INTERRUPTS.md), [buffer concurrency](08_CONCURRENCY_BUFFERS.md).

## 3. Vấn đề mà cơ chế này giải quyết

Nhiều activities cần cùng CPU/time/resource. RTOS giữ suspended contexts và chọn runnable work; không tự đảm bảo mọi job kịp deadline hoặc ownership buffer đúng.

## 4. Khái niệm

Task có stack/register context và TCB kernel metadata. Ready eligible nhưng chưa selected; running selected; blocked waiting event/time/resource, khác busy spin; suspended không tự wake cùng blocked rules. Scheduler policy priority/preempt/time-slice/cooperative quyết progress.

## 5. Thành phần bên trong

TCB có saved stack pointer/priority/state/list links tùy kernel; ready lists theo priority, delayed/event wait lists giữ blocked tasks. Tick advances timeouts, event removes waiter→ready. Context switch saves regs/stack state, selects ready task, restores. M4 ports thường PendSV/PSP+MSP/exception context, software saves extra callee regs/FPU theo port.

FreeRTOS higher numeric priority usually higher task priority; Zephyr lower numeric higher priority, negative cooperative/nonnegative preemptive range theo config. Không map hardware NVIC numeric convention sang task numbers.

## 6. Data representation

Queue bounded copies message bytes; pointer fields vẫn borrow/transfer riêng. Semaphore count/event/resource permits, không owned lock semantics; mutex owner task+inheritance support. FreeRTOS notifications per-task value/bits/count theo action; event group represents multiple conditions with clear/wait rules; coalescing may lose multiplicity if assumed counting.

### Một wait phải thay đổi cả dữ liệu lẫn scheduler state

Giả sử queue rỗng. Consumer cần kiểm tra queue và đăng ký waiter như một thao tác được kernel đồng bộ với producer. Nếu tự làm “kiểm tra rỗng → unlock → sleep”, producer có thể enqueue và signal giữa unlock và sleep; consumer ngủ dù dữ liệu đã có. Queue receive của kernel nối predicate, wait-list và wake-up theo giao thức của kernel. Đây là lý do không thay blocking receive bằng một biến flag tự chế.

| Primitive | State được giữ | Wake-up có nghĩa gì? | Điều không tự bảo đảm |
|---|---|---|---|
| Queue | Messages và waiters | Có cơ hội nhận/gửi theo API | Lifetime của pointee |
| Counting semaphore | Count và waiters | Một permit có thể được lấy | Ownership lock |
| Mutex | Owner và waiters | Lock có thể được acquire | Không deadlock; deadline |
| Notification/event bits | Value/bits và waiters | Điều kiện signal phù hợp | Mỗi event được giữ riêng |
| Timer | Expiry và callback state | Callback/waiter được kích hoạt | Callback bắt đầu đúng deadline |

Timeout và signal có thể xảy ra sát nhau. Caller phải dùng kết quả API thực, không suy từ log “producer vừa gửi”; tài nguyên có thể đã được consumer khác lấy. Timeout không mặc nhiên hủy operation đang chạy ở actor khác.

### Context switch có hai lớp context

Trong port ARM_CM4F được tham chiếu, exception hardware lưu basic frame; PendSV code lưu thêm trạng thái mà task phải giữ và ghi saved SP vào TCB. Scheduler chọn TCB kế tiếp rồi port khôi phục SP/registers. Optional FPU làm đường save/restore khác theo port. Scheduler chọn **ai**, port thực hiện **cách giữ execution state**; đọc tasks.c riêng không đủ để xác nhận frame layout.

## 7. Control flow

```text
READY → RUNNING → BLOCKED(event/timeout)
RUNNING → READY khi preempt/yield theo policy
BLOCKED → READY khi event/timeout, không chạy ngay guarantee
READY selected → context switch → resume sau wait
```

Preemptive scheduler có thể chuyển khi higher-priority task ready; cooperative contexts need block/yield theo kernel rules. Equal-priority time slicing/config quyết distribution. Busy highest-priority consumer can starve producer thấp nó đang đợi.

## 8. Lifetime / ownership / state

Task stack live tới termination cleanup theo kernel; borrowed stack pointers không tồn tại sau task deletion. Queue/mutex objects owned system lifecycle, shutdown quiesce waiters trước destroy. FreeRTOS software-timer callbacks chạy trong timer service task; không block callback vì sẽ trì hoãn timer khác. Zephyr3.7 `k_timer` expiry callback chạy trong system clock interrupt handler; đưa work dài sang workqueue. Stop callback chạy trong context caller gọi stop và phải phù hợp ISR nếu caller là ISR. ISR uses allowed nonblocking APIs/urgency threshold và reschedule request contract.

## 9. Invariants

Every wait có producer/release reachable; all protected accesses use same lock; lock order no circular wait; full/timeout/drop outcomes handled. Critical sections bounded; correct ISR API/context/priority threshold. Ready≠deadline guarantee; stack depth units FreeRTOS StackType_t vs bytes API khác, watermarks observed only.

## 10. Ví dụ tối thiểu

**Schedule model**: Producer P priority1, Consumer C priority2. C polls empty queue forever→P not scheduled. Blocking C receive makes C blocked→P enqueue→C ready/preempt according config. Task delay period10 makes eligible later, interference can delay run; periodic release dùng kernel absolute-delay API phù hợp version, không sleep relative accumulating drift.

### Theo dấu lịch thay vì chỉ nhìn tên task

**Mô hình dự đoán**, một core, preemptive, C ưu tiên hơn P:

| Thời điểm logic | P | C | Nguyên nhân |
|---|---|---|---|
| 0 | Ready | Running | C được chọn |
| 1 | Running | Blocked | C gọi receive trên queue rỗng |
| 2 | Ready | Running | P enqueue, C được đánh thức và preempt P |
| 3 | Running | Blocked | C xử lý xong, receive tiếp |

Nếu C thay receive bằng polling, trạng thái hàng 1 không tồn tại. Tăng ưu tiên P có thể đổi symptom nhưng không sửa giao thức chờ. Nếu C giữ mutex rồi chờ message mà P cần cùng mutex để gửi, blocking receive cũng không cứu được: wait-for graph đã có chu trình. Trước khi sửa priority, vẽ cả resource dependencies và task states.

## 11. Failure modes

Starvation, priority inversion, deadlock/livelock, queue overflow, notifications coalescing misunderstood, timer callback blocks, stack overflow, API from invalid ISR, tick wrap naive compare. Fix waits/owner/order/budgets, không tăng mọi priorities.

## 12. Debug / observability

RTOS trace states/reasons/ready→run delay/lock owner/IRQ durations, stack watermarks+call paths, queue/drop progress counters. Force empty/full/late release; graph waiter→owner→dependency. Inheritance mutex experiment tách inversion từ deadlock; high CPU có thể busy spin hoặc useful work, cần progress evidence.

## 13. Liên hệ với bug/lab hiện có

[EMB-16](../labs/embedded_rtos/EMB-16.md) tới [EMB-30](../labs/embedded_rtos/EMB-30.md), đặc biệt [EMB-21](../labs/embedded_rtos/EMB-21.md) mutex/semaphore, [EMB-23](../labs/embedded_rtos/EMB-23.md) events, [EMB-27](../labs/embedded_rtos/EMB-27.md) busy wait.

## 14. Sai lầm thường gặp

Mutex≠semaphore; queue≠shared-memory deep copy; delay≠deadline. Inheritance doesn't break lock cycle or unbounded owner I/O. Watchdog timer alive doesn't prove business progress. RTOS label doesn't alone real-time proof.

## 15. Câu hỏi tự kiểm tra

1. Blocked task consumes spin CPU? Đáp án:no.
2. Wake runs immediately? Đáp án:ready, policy/interference determines.
3. FreeRTOS/Zephyr same priority number meaning? Đáp án:no.
4. Timer callback ISR? Đáp án: FreeRTOS timer task; Zephyr3.7 k_timer expiry ở clock ISR. Không dùng cùng một quy tắc cho hai kernel.
5. Queue pointers deep copied? Đáp án:no.
6. Stack depth100 always100bytes? Đáp án:API/port units.

## 16. Nguồn

[FreeRTOS11.1 tasks.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/tasks.c), [task.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/include/task.h), [queue.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/queue.c), [semphr.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/include/semphr.h), [M4F port](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/portable/GCC/ARM_CM4F/port.c), [timers.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/timers.c), [Zephyr3.7 scheduling](https://docs.zephyrproject.org/3.7.0/kernel/services/scheduling/index.html), [mutex](https://docs.zephyrproject.org/3.7.0/kernel/services/synchronization/mutexes.html), [timers](https://docs.zephyrproject.org/3.7.0/kernel/services/timing/timers.html).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
