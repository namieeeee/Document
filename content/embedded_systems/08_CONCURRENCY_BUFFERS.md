# Outline — Embedded concurrency: CPU, ISR, DMA và tasks

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Multi-producer mislabeled SPSC, publish index before data, buffer reused/dangling, head/count RMW races, full ignored, DMA cache stale, reset while actors active. More capacity only postpones sustained arrival>service.

Đặt câu hỏi: cơ chế trong [Embedded concurrency: CPU, ISR, DMA và tasks](../../embedded_systems/08_CONCURRENCY_BUFFERS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Producer reserve own slot→write all payload→release-publish→consumer acquire-observe publication→read/copy→release slot. C++ atomics acquire/release có happens-before giữa threads khi sees release; IRQ compiler/port và DMA bus/cache khác layers. Không dùng volatile chỉ vì aligned32.

## 3. Demo chạy thật

Claim có phạm vi: Queue bounded chứa hai item và ghi nhận item thứ ba bị drop theo policy trong model.

```text
python examples/systems_models.py
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/systems.log):

```text
PASS bounded queue with visible drop policy
```

## 4. Cách nó hỏng và cách phát hiện

Multi-producer mislabeled SPSC, publish index before data, buffer reused/dangling, head/count RMW races, full ignored, DMA cache stale, reset while actors active. More capacity only postpones sustained arrival>service.

Trace token/slot/generation/addresses, reserve/publish/read/release/drop; force delayed consumer/wrap/full/fail send. If immutable copy fixes data with same counts, ownership alias issue. Inspect disassembly/order/port guarantees before atomic claims; sanitizer thread model not ISR target proof.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[C++17 N4659 memory model](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [Zephyr3.7 message queues](https://docs.zephyrproject.org/3.7.0/kernel/services/data_passing/message_queues.html), [FreeRTOS11.1 queue source](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/queue.c).

1. Spare-one ringN capacity? Đáp án:N−1.
2. Main+ISR producer SPSC? Đáp án:no.
3. Struct pointer copied pointee? Đáp án:no.
4. Atomics avoid all races? Đáp án:need protocol/lifetime too.
5. Full can overwrite oldest always? Đáp án:only explicit design preserving ownership.

[Index](../../00_INDEX.md) · [Content](../README.md).
