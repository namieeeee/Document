# Cortex-M4: reset, exceptions và protection

Phạm vi: **Armv7E-M Cortex-M4**, optional FPU phân biệt; CMSIS-Core6.0.0. M0/M0+/M7/M33 không tự cùng capabilities. Chưa có MCU/board firmware run.

## 1. Mục tiêu học

Vẽ reset→startup→main và exception entry/return; biết MSP/PSP/mode/priority/fault ở core tham chiếu.

## 2. Kiến thức tiên quyết

[CPU/ABI](04_CPU_MCU_EXECUTION.md), [memory/build](11_BUILD_LINK_STARTUP.md), [MCU/MMIO](13_MMIO_MCU.md).

## 3. Vấn đề mà cơ chế này giải quyết

CPU phải bắt đầu với stack/code hợp lệ và chuyển sang handler không mất interrupted state. Core protection/priority quyết ai có thể preempt và fault capture cần frame đúng.

## 4. Khái niệm

Thread mode chạy application, Handler mode chạy exceptions; privilege rules chọn allowed operations. Thread dùng MSP hoặc PSP theo CONTROL/config, Handler dùng MSP. NVIC quản enable/pending/active/priority; SysTick là core timer có thể làm timebase, không nghĩa mọi RTOS uses SysTick.

## 5. Thành phần bên trong

Vector table chứa initial MSP và reset handler address rồi exception/device handlers. Boot mapping/VTOR alignment/location actual MCU/system quyết; reset lấy initial context rồi startup init RAM/runtime/clocks theo actual build. M4 configurable fault classes MemManage/BusFault/UsageFault có status registers; disabled/escalated faults có thể vào HardFault. M0 capabilities fault/BASEPRI khác, M7 caches/M33 security không áp M4.

## 6. Data representation

Basic exception stacking: r0-r3,r12,LR,PC,xPSR, plus alignment adjustment khi applicable. Optional FPU/extended/lazy stacking đổi frame/state; EXC_RETURN token ở LR hướng return stack/frame/mode. Interrupted context có thể PSP, handler current MSP; decode stacked pointer phải đọc EXC_RETURN, không lấy MSP blindly.

## 7. Control flow

```text
hardware event → pending/enable/mask/priority arbitration
→ stack interrupted basic/extended context → vector handler
→ compiler prologue/ISR → epilogue
→ exception return token → restore context hoặc tail-chain
```

Reset special entry không ordinary IRQ return. PendSV thường context-switch mechanism port, SVC service entry; policies của RTOS separate core mechanism.

## 8. Lifetime / ownership / state

Stacked frame live khi handler/exception active; nested handler thêm MSP load. FPU lazy preservation cần correct flags/port context. NVIC pending != active; disable không xóa peripheral source. Thread unprivileged policy cần MPU/config nếu muốn memory access protection, CONTROL alone không full per-region isolation.

## 9. Invariants

Vector đúng image/handler, initial MSP aligned in SRAM budget, Thumb/code addresses hợp target, startup initializes objects trước use. Priority encoding theo implemented bits; fault decode core đúng và stacked context valid. Guard invalid stack before dereference fault dump.

## 10. Ví dụ tối thiểu

Fault workflow **pseudocode**, không handler compile-ready:

```text
read EXC_RETURN → select interrupted stack (MSP/PSP)
check SP range/alignment/frame variant
capture stacked PC/LR/xPSR + M4 CFSR/HFSR
symbolize PC with exact ELF
```

Không print/allocate trong fault handler không bounded; corrupted frame không valid chỉ vì fault occurred.

## 11. Failure modes

Wrong vector/default handler, SP out RAM, data init sai, IRQ before driver ready, reserved/invalid instruction, unaligned/permission fault tùy access/core settings, invalid exception return. Fault PC có thể downstream of memory corruption.

## 12. Debug / observability

SWD/GDB regs/vector/startup breaks và core fault bits đúng M4; CFSR subfields+address-valid bits quyết BFAR/MMFAR meaningful. Reset reason vendor register là MCU-specific chưa assumed. Exact ELF và check frame before decode; last trace owner/address helps first violation.

## 13. Liên hệ với bug/lab hiện có

[EMB-06](../labs/embedded_rtos/EMB-06.md) kernel IRQ threshold, [EMB-10](../labs/embedded_rtos/EMB-10.md) nesting stack, [EMB-05](../labs/embedded_rtos/EMB-05.md) atomic width.

## 14. Sai lầm thường gặp

Không hardcode eight words mọi FPU frame; handler stack khác interrupted thread stack; priority nhỏ urgency cao hardware nhưng RTOS priorities convention khác. HardFault không always hardware hỏng.

## 15. Câu hỏi tự kiểm tra

1. Handler dùng stack nào? Đáp án: MSP; stacked interrupted frame có thể PSP.
2. Vector first word? Đáp án: initial MSP.
3. Disabled source pending tự mất? Đáp án: không.
4. M0 đọc M4 CFSR recipe đúng? Đáp án: không capabilities khác.
5. FPU frame decode cần gì? Đáp án: EXC_RETURN/config/lazy state.

## 16. Nguồn

[CMSIS6.0 NVIC](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__NVIC__gr.html), [registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [startup](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html), [CMSIS core_cm4.h](https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.0.0/CMSIS/Core/Include/core_cm4.h). Arm DUI0553 page body chưa fetch được; ghi giới hạn, không declare manual đã đọc.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
