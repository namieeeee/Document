# Embedded concurrency: CPU, ISR, DMA và tasks

Phạm vi: generic ownership/publication model; C17/C++17 threads semantics khác implementation ISR/DMA contract. Không claim portable lock-free ISR algorithm.

## 1. Mục tiêu học

Tách visibility/atomicity/order/ownership/lifetime và thiết kế SPSC/pool/queue với bounded capacity/full/release.

## 2. Kiến thức tiên quyết

[Interrupt](06_INTERRUPTS.md), [DMA](07_DMA_OWNERSHIP.md), [C memory](02_MEMORY_BUILD.md); RTOS scheduler học sau.

## 3. Vấn đề mà cơ chế này giải quyết

Actors interleave hoặc cùng bus memory, nên scalar type đúng chưa coherent message. Queue pointer copy không copy contents; ownership phải quyết ai publish/use/reuse.

## 4. Khái niệm

Atomicity: operation/snapshot có bị chia cho actor khác quan sát không? Visibility/order: producer writes đã thấy đúng khi consumer đọc chưa? Ownership/lifetime: ai được access và object còn sống không? Volatile không giải cả ba; atomic scalar không giữ multi-step invariant; critical section CPU không chặn DMA bằng cách tự nhiên. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [C++ race draft](https://eel.is/c++draft/intro.races). Thread semantics không được mang nguyên xi sang hardware ISR mà bỏ compiler/port contract.

Main chạy, IRQ preempt tại instruction boundary; DMA transfer chạy qua bus; scheduler cho task khác chạy khi yield/block/preempt. Một scope local trên stack task không được gửi pointer tới consumer rồi producer return. GC languages cũng có ownership race dù object còn live: lifetime an toàn chưa giữ message contents.

## 5. Thành phần bên trong

Ring có N slots, head chỉ next write, tail chỉ next read theo design. Có design chừa1 slot để full khi nexthead==tail; có design dùng count/generation cho đủ N slots. Chốt capacity semantics trước code. Producer ghi payload rồi publish availability theo memory protocol; consumer chỉ đọc published slots rồi release. Single producer/single consumer là giả định về actors thực, không số function names: main+ISR cùng produce thành multi-producer.

```text
Slot FREE → producer owns/write → PUBLISHED
→ consumer owns/read/copy → FREE
```

SPSC thường mỗi actor sở hữu một index, nhưng cần atomic width/alignment/order và port guarantees. Count++/-- do cả hai actors sửa trở thành RMWrace. Multi-producer cần reservation/protocol khác. Không xuất “lock-free portable C ISR ring” khi không có target/compiler contract. Critical section giữ snapshot ngắn theo port là lựa chọn bảo thủ; data processing bên ngoài vùng masked.

## 6. Data representation

Slot states FREE/WRITING/PUBLISHED/READING; indexes head/tail with defined capacity rule, sequence/generation/pool tokens. Copied struct pointer field still aliases pointee. Shared count++/-- two actors RMW adds contention that per-owner indices avoid, nhưng width/order contract vẫn needed.

## 7. Control flow

Producer reserve own slot→write all payload→release-publish→consumer acquire-observe publication→read/copy→release slot. C++ atomics acquire/release có happens-before giữa threads khi sees release; IRQ compiler/port và DMA bus/cache khác layers. Không dùng volatile chỉ vì aligned32.

## 8. Lifetime / ownership / state

Queue copied message giữ bytes message riêng; nếu field message là pointer, pointee vẫn không tự được copy. Pool token chuyển quyền buffer và consumer trả token sauuse; send fail phải trả owner đúng. Semaphore/event chỉ signal không tự trao memory owner. Notification bits có thể coalesce event; nếu cần mỗi sample dùng count/queue và overflow policy. [Zephyr message queue](https://docs.zephyrproject.org/3.7.0/kernel/services/data_passing/message_queues.html).

Bounded buffer full phải reject/drop/backpressure/counter theo usecase; tăng N chưa sửa average arrival rate vượt service rate. Reset queue khi runtime active cần quiesce actors hoặc transactional state; zerohead/tail tùy ý có thể consumer read slot đangDMA-owned.

Queue reset/shutdown cần quiesce all actors; return token exactly once, send fail trả producer ownership. Lost token leak capacity, double return two writers.

## 9. Invariants

One writer per slot, published complete before consume, immutable while borrowed, storage live, capacity/full policy observable. SPSC thực đúng one producer/one consumer, main+ISR producers thành MPSC.

## 10. Ví dụ tối thiểu

**Model** ring4 slots spare-one policy capacity3: head0/tail0 empty; publish3 messages leaves head3/tail0 full nexthead0. Consumer release tail1 opens one slot. Count-based full-capacity design khác; không mix tests expecting capacity4.

Queue pointer p to stack struct, producer overwrite p after send before consumer→consumer sees next message: pointer queued but ownership missing.

## 11. Failure modes

Multi-producer mislabeled SPSC, publish index before data, buffer reused/dangling, head/count RMW races, full ignored, DMA cache stale, reset while actors active. More capacity only postpones sustained arrival>service.

## 12. Debug / observability

Trace token/slot/generation/addresses, reserve/publish/read/release/drop; force delayed consumer/wrap/full/fail send. If immutable copy fixes data with same counts, ownership alias issue. Inspect disassembly/order/port guarantees before atomic claims; sanitizer thread model not ISR target proof.

## 13. Liên hệ với bug/lab hiện có

[EMB-16](../labs/embedded_rtos/EMB-16.md), [EMB-22](../labs/embedded_rtos/EMB-22.md), [EMB-23](../labs/embedded_rtos/EMB-23.md), [EMB-30](../labs/embedded_rtos/EMB-30.md).

## 14. Sai lầm thường gặp

Atomic head not full protocol; queue copied bytes not deep ownership; semaphore signal not buffer release; critical CPU not DMA exclude. Notification coalescing can be desired latest-state but not every-sample count.

## 15. Câu hỏi tự kiểm tra

1. Spare-one ringN capacity? Đáp án:N−1.
2. Main+ISR producer SPSC? Đáp án:no.
3. Struct pointer copied pointee? Đáp án:no.
4. Atomics avoid all races? Đáp án:need protocol/lifetime too.
5. Full can overwrite oldest always? Đáp án:only explicit design preserving ownership.

## 16. Nguồn

[C++17 N4659 memory model](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [Zephyr3.7 message queues](https://docs.zephyrproject.org/3.7.0/kernel/services/data_passing/message_queues.html), [FreeRTOS11.1 queue source](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/queue.c).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
