# Outline — Cortex-M4: reset, exceptions và protection

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Wrong vector/default handler, SP out RAM, data init sai, IRQ before driver ready, reserved/invalid instruction, unaligned/permission fault tùy access/core settings, invalid exception return. Fault PC có thể downstream of memory corruption.

Đặt câu hỏi: cơ chế trong [Cortex-M4: reset, exceptions và protection](../../embedded_systems/12_CORTEX_M.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
hardware event → pending/enable/mask/priority arbitration
→ stack interrupted basic/extended context → vector handler
→ compiler prologue/ISR → epilogue
→ exception return token → restore context hoặc tail-chain
```

Reset special entry không ordinary IRQ return. PendSV thường context-switch mechanism port, SVC service entry; policies của RTOS separate core mechanism.

## 3. Demo chạy thật

Claim có phạm vi: Vector đúng image/handler, initial MSP aligned in SRAM budget, Thumb/code addresses hợp target, startup initializes objects trước use. Priority encoding theo implemented bits; fault decode core đúng và stacked context valid. Guard invalid stack before dereference fault dump.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/12_CORTEX_M.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Wrong vector/default handler, SP out RAM, data init sai, IRQ before driver ready, reserved/invalid instruction, unaligned/permission fault tùy access/core settings, invalid exception return. Fault PC có thể downstream of memory corruption.

SWD/GDB regs/vector/startup breaks và core fault bits đúng M4; CFSR subfields+address-valid bits quyết BFAR/MMFAR meaningful. Reset reason vendor register là MCU-specific chưa assumed. Exact ELF và check frame before decode; last trace owner/address helps first violation.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[CMSIS6.0 NVIC](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__NVIC__gr.html), [registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [startup](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html), [CMSIS core_cm4.h](https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.0.0/CMSIS/Core/Include/core_cm4.h). Arm DUI0553 page body chưa fetch được; ghi giới hạn, không declare manual đã đọc.

1. Handler dùng stack nào? Đáp án: MSP; stacked interrupted frame có thể PSP.
2. Vector first word? Đáp án: initial MSP.
3. Disabled source pending tự mất? Đáp án: không.
4. M0 đọc M4 CFSR recipe đúng? Đáp án: không capabilities khác.
5. FPU frame decode cần gì? Đáp án: EXC_RETURN/config/lazy state.

[Index](../../00_INDEX.md) · [Content](../README.md).
