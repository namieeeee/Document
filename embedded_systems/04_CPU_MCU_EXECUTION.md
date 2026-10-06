# CPU execution: instructions, calls và ABI

Phạm vi: conceptual load/store CPU; worked calling model Arm AAPCS32/Cortex-M4, không universal instruction/stack layout.

## 1. Mục tiêu học

Vẽ fetch/execute/load/store/control flow, diễn giải PC/SP/flags và function call frame; nối C operation tới instructions thực.

## 2. Kiến thức tiên quyết

[Digital](../foundations/01_DIGITAL_REPRESENTATION.md), [C](01_C_REPRESENTATION.md), [build/memory](11_BUILD_LINK_STARTUP.md).

## 3. Vấn đề mà cơ chế này giải quyết

CPU không chạy C paragraphs, nó execute machine instructions; compiler/ABI quyết representation/control flow. Hiểu atomicity/fault/stack cần biết instruction và bus boundary.

## 4. Khái niệm

CPU có register file, ALU/control unit, PC, SP/status và memory interface. PC theo vị trí execution theo architecture rules; SP track stack; flags điều kiện branch; load/store CPU thao tác registers rồi memory transfers. Core là phần processor, MCU là core+memory/peripheral/clock/reset integration.

## 5. Thành phần bên trong

Fetch instruction→decode operands→execute ALU/branch/memory→update architectural state. Pipelining/cache/stalls/bus contention có thể overlap steps, conceptual flow không cycle simulation. Register values khác SRAM data; compiler giữ variable register hoặc loại bỏ, nên watch memory variable không always capture every logical update.

## 6. Data representation

Register width và instruction encoding target-specific. Arm32 ABI thường arguments/results đầu qua r0-r3, callee-saved subset theo AAPCS; SP alignment public interface rules cần giữ. Return address thường LR với spills khi calls nested. Frame có locals/spills/saved registers nhưng optimizer có thể inline/no frame pointer; không mỗi function push fixed frame.

### ABI nối hai đoạn code không nhìn thấy source của nhau

Trong AAPCS32, r0–r3 được dùng cho các arguments phù hợp quy tắc ABI và kết quả phù hợp kiểu; arguments khác có thể nằm trên stack. Không suy mọi struct/float đều đi qua r0: variant hard-float, type và alignment có quy tắc riêng. Caller phải coi caller-saved registers có thể đổi; callee giữ các registers mà ABI yêu cầu preserve. SP phải đáp ứng alignment ở interface, với public interface yêu cầu 8-byte alignment.

| Trạng thái | Ai chịu trách nhiệm? | Lỗi nếu vi phạm |
|---|---|---|
| Arguments/result representation | Caller và callee cùng ABI | Đọc sai arguments |
| Callee-saved registers | Callee khôi phục trước return | Caller mất state |
| Return address | Call instruction/LR và callee khi gọi lồng | Return sai PC |
| Stack bounds/alignment | Build, caller/callee, runtime/port | Corruption hoặc access lỗi |

Compiler có thể giữ locals trong registers, spill khi cần, inline callee hoặc bỏ biến không ảnh hưởng observable behavior. “Biến local nằm ở stack” chỉ là mô hình phổ biến, không phải quy tắc ngôn ngữ.

## 7. Control flow

```text
caller chuẩn bị arguments → branch-with-link/ABI call
→ callee preserves required registers/allocates frame
→ body load/ALU/store/calls → restore → return continuation
```

Exception entry khác ordinary C function call; hardware frame + compiler prologue + port context layers riêng. Cortex-M reset/exception chi tiết ở [core](12_CORTEX_M.md).

## 8. Lifetime / ownership / state

Register chứa active execution state; context switch cần save state để task resume đúng. Frame storage validity ends theo source lifetime; SP restore không xóa mọi bytes nhưng pointers local invalid. Interrupt nest consumes stack theo MSP/PSP/port; calling conventions phải cùng ABI libraries/assembly.

## 9. Invariants

Instruction fetch executable region, SP alignment/bounds, preserved registers/calling contract, valid load/store addresses. Atomic aligned scalar access target guarantee không whole RMW/multi-field snapshot. C arithmetic defined độc lập CPU bits.

## 10. Ví dụ tối thiểu

Instruction model **pseudocode không assembly target**:

```text
r0 = LOAD counter
r0 = ADD r0,1
STORE counter,r0
```

ISR increment sau LOAD trước STORE có thể mất update; aligned STORE atomic chưa đủ. Actual optimized build phải xem disassembly; compiler có thể chọn khác instructions và source signed overflow vẫn UB.

### Theo dấu một call lồng

**Mô hình AAPCS32, không assembly đã chạy**: A gọi B, call đặt địa chỉ quay về A vào LR. B gọi C thì LR sẽ trở thành địa chỉ quay về B; nếu B còn cần địa chỉ quay về A, B phải bảo toàn nó bằng cách phù hợp. C return về B, B khôi phục return state rồi return về A. Vì vậy stack frame không chỉ chứa locals; nó có thể giữ saved registers, spills và return state.

Với counter ban đầu 5: main LOAD 5; ISR LOAD 5, ADD 1, STORE 6; main ADD trên bản register cũ, STORE 6. Hai increment nhưng kết quả 6. Mỗi load/store có thể hợp lệ và indivisible; invariant “mỗi increment được tính” vẫn sai. Fix phải bảo vệ toàn bộ read-modify-write bằng primitive phù hợp actor/target, không chỉ thêm volatile vào một store.

## 11. Failure modes

Wrong signature/ABI corrupt args, stack misalignment/overflow, invalid PC/LR return, multi-instruction lost update, stale image symbols, peripheral access before clock. Fix calling/state/address invariant, không source line crash suy bug compiler.

## 12. Debug / observability

Exact ELF disassembly/register dump/stack frames/map; single step instruction để đọc call/return, timing capture thay breakpoint khi real time. Optimized out/frame omitted expected theo flags; compare source/ABI/target và symbolize exact PC. C line không instructions count proof.

## 13. Liên hệ với bug/lab hiện có

[EMB-03](../labs/embedded_rtos/EMB-03.md) RMW, [EMB-10](../labs/embedded_rtos/EMB-10.md) stack nesting, [EMB-05](../labs/embedded_rtos/EMB-05.md) multiword atomicity.

## 14. Sai lầm thường gặp

CPU wrap không C signed semantics; function call không scheduler switch; syscall mode transition cũng không luôn task switch. PC current register presentation debugger có architecture nuance. Không dùng instruction timing số của core khác.

## 15. Câu hỏi tự kiểm tra

1. C counter++ là atomic instruction? Đáp án: inspect build, không assume.
2. Vì sao callee preserve registers? Đáp án: caller relies ABI.
3. SP restore giữ local lifetime? Đáp án: không.
4. CPU core khác MCU? Đáp án: integration ngoài core.
5. Exception frame bằng function frame? Đáp án: không.

## 16. Nguồn

[Arm AAPCS32](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst), [CMSIS6 registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [GNU objdump](https://sourceware.org/binutils/docs/binutils/objdump.html). AAPCS32 repo rolling; conceptual contracts, actual compiler/ABI cần pin build.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
