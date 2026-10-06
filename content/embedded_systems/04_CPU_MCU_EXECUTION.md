# Outline — CPU execution: instructions, calls và ABI

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Wrong signature/ABI corrupt args, stack misalignment/overflow, invalid PC/LR return, multi-instruction lost update, stale image symbols, peripheral access before clock. Fix calling/state/address invariant, không source line crash suy bug compiler.

Đặt câu hỏi: cơ chế trong [CPU execution: instructions, calls và ABI](../../embedded_systems/04_CPU_MCU_EXECUTION.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
caller chuẩn bị arguments → branch-with-link/ABI call
→ callee preserves required registers/allocates frame
→ body load/ALU/store/calls → restore → return continuation
```

Exception entry khác ordinary C function call; hardware frame + compiler prologue + port context layers riêng. Cortex-M reset/exception chi tiết ở [core](../../embedded_systems/12_CORTEX_M.md).

## 3. Demo chạy thật

Claim có phạm vi: Instruction fetch executable region, SP alignment/bounds, preserved registers/calling contract, valid load/store addresses. Atomic aligned scalar access target guarantee không whole RMW/multi-field snapshot. C arithmetic defined độc lập CPU bits.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/04_CPU_MCU_EXECUTION.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Wrong signature/ABI corrupt args, stack misalignment/overflow, invalid PC/LR return, multi-instruction lost update, stale image symbols, peripheral access before clock. Fix calling/state/address invariant, không source line crash suy bug compiler.

Exact ELF disassembly/register dump/stack frames/map; single step instruction để đọc call/return, timing capture thay breakpoint khi real time. Optimized out/frame omitted expected theo flags; compare source/ABI/target và symbolize exact PC. C line không instructions count proof.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[Arm AAPCS32](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst), [CMSIS6 registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [GNU objdump](https://sourceware.org/binutils/docs/binutils/objdump.html). AAPCS32 repo rolling; conceptual contracts, actual compiler/ABI cần pin build.

1. C counter++ là atomic instruction? Đáp án: inspect build, không assume.
2. Vì sao callee preserve registers? Đáp án: caller relies ABI.
3. SP restore giữ local lifetime? Đáp án: không.
4. CPU core khác MCU? Đáp án: integration ngoài core.
5. Exception frame bằng function frame? Đáp án: không.

[Index](../../00_INDEX.md) · [Content](../README.md).
