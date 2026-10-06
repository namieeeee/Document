# Lab embedded_rtos

Các ví dụ đều là mô phỏng. Snippet ngữ cảnh/pseudocode cần fixture ghi trong lab; chưa phải ứng dụng/firmware độc lập. Xem [validation](../../VALIDATION.md) trước khi coi một kết quả là đã chạy.

| ID | Lỗi |
|---|---|
| EMB-01 | [ISR quá dài](EMB-01.md) |
| EMB-02 | [Shared data không đồng bộ](EMB-02.md) |
| EMB-03 | [Volatile không atomic](EMB-03.md) |
| EMB-04 | [ISR/main clear race](EMB-04.md) |
| EMB-05 | [Torn access](EMB-05.md) |
| EMB-06 | [IRQ priority sai RTOS](EMB-06.md) |
| EMB-07 | [Mất nhiều event](EMB-07.md) |
| EMB-08 | [Register read-modify-write](EMB-08.md) |
| EMB-09 | [Block trong ISR](EMB-09.md) |
| EMB-10 | [Nested ISR stack](EMB-10.md) |
| EMB-11 | [DMA buffer lifetime](EMB-11.md) |
| EMB-12 | [DMA cache coherence](EMB-12.md) |
| EMB-13 | [DMA CPU ownership](EMB-13.md) |
| EMB-14 | [DMA alignment](EMB-14.md) |
| EMB-15 | [DMA double buffer reuse](EMB-15.md) |
| EMB-16 | [RTOS race](EMB-16.md) |
| EMB-17 | [RTOS deadlock](EMB-17.md) |
| EMB-18 | [RTOS livelock](EMB-18.md) |
| EMB-19 | [RTOS starvation](EMB-19.md) |
| EMB-20 | [Priority inversion](EMB-20.md) |
| EMB-21 | [Mutex dùng như semaphore](EMB-21.md) |
| EMB-22 | [Queue overflow](EMB-22.md) |
| EMB-23 | [Lost notification event](EMB-23.md) |
| EMB-24 | [Task stack overflow](EMB-24.md) |
| EMB-25 | [Heap fragmentation](EMB-25.md) |
| EMB-26 | [Priority assignment sai](EMB-26.md) |
| EMB-27 | [Busy wait RTOS](EMB-27.md) |
| EMB-28 | [Block trong critical](EMB-28.md) |
| EMB-29 | [Tick wraparound](EMB-29.md) |
| EMB-30 | [Buffer ownership queue](EMB-30.md) |
