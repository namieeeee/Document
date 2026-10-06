# Outline — Interrupts: event, preemption và coherent state

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Lost increment/event clear race, torn/mixed snapshot, invalid priority calling kernel, long mask/ISR overrun, blocking ISR waits interrupted owner, reentrant scratch corruption/nesting stack. Fix exact invariant/protocol not just ISR shortness.

Đặt câu hỏi: cơ chế trong [Interrupts: event, preemption và coherent state](../../embedded_systems/06_INTERRUPTS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Hardware event→IRQ pending→mask/priority decision→save context/vector→compiler prologue→bounded acquire/ack→publish queue/notify→restore/return. Level source still asserted retrigger; acknowledge sequence follow manual to avoid new event cleared. RTOS wake may request context switch after ISR theo port.

## 3. Demo chạy thật

Claim có phạm vi: Atomic access chỉ nói thao tác không bị quan sát như phần bị xé theo guarantee target; read-modify-write hoặc pair snapshot là invariant khác. Volatile counter++ thường load/add/store: ISR cập nhật giữa load và store có thể mất increment. Hai aligned scalar reads vẫn có thể lấy x mới/y cũ. Critical snapshot, atomic protocol hoặc versioned scheme đúng memory semantics mới bảo vệ; không chọn lock-free bằng niềm tin “MCU 32 bit”. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html).

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/06_INTERRUPTS.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Lost increment/event clear race, torn/mixed snapshot, invalid priority calling kernel, long mask/ISR overrun, blocking ISR waits interrupted owner, reentrant scratch corruption/nesting stack. Fix exact invariant/protocol not just ISR shortness.

- **SYMPTOM:** producer2 events nhưng counter chỉ tăng1, hoặc pair sample không coherent.
- **EVIDENCE:** disassembly RMW, event/read/write timeline, mask state, alignment/width và sequence numbers.
- **POSSIBLE CAUSES:** lost update, event coalescing có chủ đích, torn access hoặc register clear sai.
- **DISTINGUISHING TEST:** buộc ISR giữa load/store trong model; trên board trace bounded/GPIO và kiểm event counts; tách pair reads để tìm mixed generation.
- **ROOT CAUSE:** invariant nhiều bước không nằm trong synchronization protocol, không phải compiler “quên volatile”.
- **FIX:** atomic/critical snapshot theo port hoặc queue/owner protocol; giữ mask restoration đúng.
- **WRONG FIX:** thêm volatile rồi coi atomic, tắt mọi IRQ trong toàn processing, dùng blocking mutex trong ISR.
- **REGRESSION TEST:** event trước/trong/sau clear, bursts/full policy, max nesting/stack và API threshold trên target.



Measure event→entry latency separately handler duration; GPIO/trace timestamps with overhead. Stop CPU changes peripheral progress, bounded trace preferable timing evidence.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[CMSIS6 NVIC](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__NVIC__gr.html), [core registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [FreeRTOS11.1 M4F port](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/portable/GCC/ARM_CM4F/port.c). Actual MCU implemented priority bits/vendor ack still verify.

1. Pending active? Đáp án: pending waiting, active servicing.
2. Volatile++ atomic? Đáp án: no.
3. Restore IRQ unconditionally enable safe? Đáp án: no, preserve prior mask.
4. Mask CPU excludes DMA? Đáp án: no.
5. Latency equals handler duration? Đáp án: no.
6. Inheritance mutex usable blocking ISR? Đáp án: not that context contract.

[Index](../../00_INDEX.md) · [Content](../README.md).
