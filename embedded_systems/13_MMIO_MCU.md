# MCU và memory-mapped I/O

Phạm vi: generic MCU hardware model, core tham chiếu M4. Không register addresses/HAL recipe của board chưa chọn.

## 1. Mục tiêu học

Phân biệt CPU core/MCU và vẽ instruction→bus→register→hardware state; đọc register access types trước bit operations.

## 2. Kiến thức tiên quyết

[CPU](04_CPU_MCU_EXECUTION.md), [C representation](01_C_REPRESENTATION.md), [build](11_BUILD_LINK_STARTUP.md).

## 3. Vấn đề mà cơ chế này giải quyết

CPU phải điều khiển hardware tự hoạt động, không chỉ RAM. MCU integration clock/reset/bus/map quyết whether access reaches engine.

## 4. Khái niệm

MCU gồm core, flash/SRAM, buses/bridges, peripherals, clock/reset/interrupt integration. Flash giữ executable/persistent data theo erase/program constraints; SRAM volatile runtime. Clock domains/dividers/gates khác CPU clock; reset peripheral có state defaults cần manual.

## 5. Thành phần bên trong

Load/store address decoder chọn SRAM/flash hoặc peripheral bridge; device register read/write phản ứng hardware. Configuration changes mode, data accesses move FIFO/payload, status reports events. Bus/device widths/alignment/ordering và read/write side effects không RAM semantics.

## 6. Data representation

Register access kinds read-only/write-only/read-write/W1C/read-to-clear/set-clear aliases theo manual. W1C bit write1 acknowledge, write0 thường leave; RMW status OR mask có thể write1 back unrelated pending bits. Volatile access giữ compiler semantics nhưng không read atomic multi-register/correct acknowledge.

## 7. Control flow

Clock/reset enable→configure mux/rate/mode khi inactive→clear relevant stale events theo manual→enable engine/IRQ→hardware progresses→status/data→ack/recover. IRQ enable before state ready có thể call default/invalid owner. HAL functions wrap operations, không thay physical/clock/ownership contract.

## 8. Lifetime / ownership / state

Software owns config/driver state; hardware owns status/FIFO/current transfer independent CPU. Reset/quiesce handshake trước reuse/reconfigure; clock off/reset không universal atomic cancel dữ liệu. Shared peripheral access main/ISR/tasks cần arbitration; DMA không bị CPU lock chặn.

## 9. Invariants

Address/width/region accessible target, clock/reset/config valid trước active, write semantics đúng, unrelated pending events không mất, one configuration owner. Reserved bits theo manual không assume always write0.

## 10. Ví dụ tối thiểu

Model **pseudocode không real addresses**:

```text
STATUS bits: A=1, B=1; both W1C
software wants ackA
write STATUS = maskA       → clears A only
read STATUS then OR maskA  → writes A|B, clears B unintended
```

B có thể đến giữa read/write, cần follow vendor sequence/latching semantics.

## 11. Failure modes

Wrong map/bus width, gate clock off, pin alternate function wrong, RMW clear event, reconfigure running engine, snapshot side-effect reads, invalid reserved bits. Fix correct manual sequence và owner, không arbitrary delay/volatile every variable.

## 12. Debug / observability

Manual access-type/clock tree/mux, register snapshot only safe-read fields, logic scope physical signals, bus/fault status/core exact. Compare software expects vs hardware state before/after one access. HAL debug stepping có observer effects.

## 13. Liên hệ với bug/lab hiện có

[EMB-08](../labs/embedded_rtos/EMB-08.md) W1C, [EMB-04](../labs/embedded_rtos/EMB-04.md) event clear race, [EMB-07](../labs/embedded_rtos/EMB-07.md) multiplicity.

## 14. Sai lầm thường gặp

Register≠RAM variable; volatile≠barrier/cache flush; same core≠same MCU map/peripheral. Reading status in debugger có thể alter state, confirm safe access before inspect.

## 15. Câu hỏi tự kiểm tra

1. CPU clock giống timer clock? Đáp án: no, tree/domains.
2. W1C OR RMW safe? Đáp án: có thể ack unrelated bits.
3. CPU mutex stops DMA? Đáp án: không.
4. HAL start success nghĩa wire completed? Đáp án: no.
5. Core manual đủ UART pin/address? Đáp án: vendor manual cần.

## 16. Nguồn

[GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [CMSIS6 core](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html). **Vendor verification còn thiếu:** RM0090 fetch failed, không cite nó như read evidence. Concepts general; electrical/register-specific implementation cần actual RM/errata.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
