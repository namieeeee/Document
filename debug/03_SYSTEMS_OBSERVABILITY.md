# Debug C/C++/Embedded: source, CPU, wire và scheduler

Phạm vi: GCC/Clang/GDB conceptual tools, Cortex-M4/FreeRTOS11.1/Zephyr3.7. Commands/examples không đã run board; M7 cache comparison separate.

## 1. Mục tiêu học

Chọn warnings/sanitizers/map/disassembly/GDB/SWD/JTAG/fault/register/stack/watchpoints/logic analyzer/scope/GPIO/RTOS trace theo layer, tránh observer effects.

## 2. Kiến thức tiên quyết

[Scientific debug](01_EVIDENCE_METHOD.md), [build](../embedded_systems/11_BUILD_LINK_STARTUP.md), [core](../embedded_systems/12_CORTEX_M.md), peripheral/RTOS mechanism liên quan.

## 3. Vấn đề mà cơ chế này giải quyết

Source crash line có thể hậu quả memory corruption/stack/IRQ/DMA. Host sanitizer không thấy electrical/timing/cache device; debugger stop changes hardware state. Need combine exact artifacts và minimally intrusive target observations.

## 4. Khái niệm

Warnings static clues, sanitizers instrument executed paths, map/symbol/disassembly actual build layout/code, debugger register/memory/control stop, probe transport SWD/JTAG, waveform tools physical signals, RTOS trace scheduling history. Tool không universal correctness oracle.

## 5. Thành phần bên trong

Compiler warnings catch conversions/format/unused/danger patterns; ASan bounds/UAF, UBSan subset UB, TSan thread races khi host supported, not arbitrary ISR/DMA proof. Map budgets/layout, disassembly load/add/store/calls, GDB break stops execution/watch data access supported. Hardware comparators limited width/count/actors; CPU watchpoint may not trigger DMA bus writes.

## 6. Data representation

Evidence exact ELF/image hash/compiler flags/target/core, registers/stacked context/owner generations, raw buffers before/after hardware, clock timestamp correlation. Fault frame M4 basic/extended/FPU selection, status address-valid bits. Trace ring capacity/loss counter must be visible to avoid fake full history.

## 7. Control flow

```text
warning/source contract → exact ELF/map/instruction path
→ target register/frame/memory snapshot
→ peripheral waveform + event/service timing
→ ISR/DMA/task owner transitions → first broken invariant
```

Not every case needs all tools. Suspected parser UB start host fixture; suspected baud capture wire; suspected priority inversion RTOS wait graph; fault symbolize exact PC but investigate producer write earlier.

## 8. Lifetime / ownership / state

Probe/debug session owner controls run/reset/flash scope; actual task here docs only no device actions. Breakpoint may freeze CPU while DMA/peripherals continue or debugger freeze config; inspect semantics. GPIO trace/log/printf consume time/bus, measure overhead. Fault capture bounded safe storage not allocate/recursive log.

## 9. Invariants

Symbols match image/core, frame validated before decode, measurement layer matches claim, instrumentation overhead/loss documented, synthetic scope. Sanitizer pass only paths executed; stack watermark observed not maximum proof; waveform correct doesn't prove buffer ownership.

## 10. Ví dụ tối thiểu

GDB commands **minh họa**, require target/probe/ELF, chưa chạy:

```text
info registers
bt
x/16wx $sp
disassemble /m function_name
```

`$sp` current handler vs interrupted thread stack differs; use EXC_RETURN to select valid frame on M4. GDB memory reads MMIO can clear/pop state, check safe registers. Breakpoint at handler measures stepped state not real ISR latency.

## 11. Failure modes

Stale ELF, wrong core fault registers, optimized source variable assumptions, CPU watchpoint missed DMA, printf extends ISR, stack invalid makes fault decoder fault again, sanitizer changes race timing, analyzer wrong protocol mode. Fix evidence reliability plus root invariant, not claim 'debugger shows no bug'.

## 12. Debug / observability

Freeze artifact IDs→capture reset/fault context safely→check stack bounds/frame variant→symbolize PC→disassemble previous operations/caller→trace owner/source pointer→wire/scheduler measurement if hardware interaction. Force host bounds/error fixtures, then target burden needed explicitly; no mock output mislabeled measured.

## 13. Liên hệ với bug/lab hiện có

[EMB-03](../labs/embedded_rtos/EMB-03.md), [EMB-08](../labs/embedded_rtos/EMB-08.md), [EMB-10](../labs/embedded_rtos/EMB-10.md), [EMB-12](../labs/embedded_rtos/EMB-12.md), [EMB-20](../labs/embedded_rtos/EMB-20.md), [OS-06](../labs/os/OS-06.md).

## 14. Sai lầm thường gặp

SWD/JTAG transport≠debugging hypothesis; sanitizer≠MCU proof; map≠WCET; scope analog vs analyzer digital; no watch hit≠no writes; breakpoint hide issue≠fixed.

## 15. Câu hỏi tự kiểm tra

1. Map proves stack max? Đáp án:no reserved region not dynamic peak.
2. ASan host proves DMA cache? Đáp án:no.
3. CPU watchpoint DMA write? Đáp án:depends debug system, no guarantee.
4. Fault PC different build ELF? Đáp án:invalid symbolization.
5. GPIO pulse handler duration equals event latency? Đáp án:no need event timestamp.
6. Scope vs analyzer? Đáp án:levels/rise/noise vs decoded edges.

## 16. Nguồn

[GDB breakpoints/watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Breakpoints.html), [GCC warnings](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [ASan](https://clang.llvm.org/docs/AddressSanitizer.html), [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [TSan](https://clang.llvm.org/docs/ThreadSanitizer.html), [CMSIS6 core](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html). Tool/target versions phải record khi thực hành.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
