# Build/link: source tới ELF và flash

Phạm vi: GCC/binutils/ELF conceptual cross-toolchain; commands minh họa chưa chạy.

## 1. Mục tiêu học

Phân loại preprocess/compile/link/runtime failure; đọc symbols/relocations/map/disassembly cùng exact image.

## 2. Kiến thức tiên quyết

[C](01_C_REPRESENTATION.md), [memory](02_MEMORY_BUILD.md). Chưa cần CPU để hiểu translation units, symbols và placement. Sau bài [CPU](04_CPU_MCU_EXECUTION.md), quay lại phần disassembly để giải thích instructions; đây là lượt đọc mở rộng, không phải dependency ngược.

## 3. Vấn đề mà cơ chế này giải quyết

Translation units compile riêng, references nối lúc link; firmware cần regions/startup. Header declaration không definition.

## 4. Khái niệm

Preprocess include/macros→compile semantics/code→assemble object→link references/layout→ELF→BIN/HEX→program flash→reset.

## 5. Thành phần bên trong

Object sections/symbol table/relocations; defined symbol location, undefined cần object/lib, weak/local/global binding. Library archive selection/link order ảnh hưởng resolution. MEMORY/SECTIONS script gán regions/boundaries; startup dùng cùng symbols copy/zero/constructors.

## 6. Data representation

ELF structured sections/segments/debug/symbols; BIN flat bytes không đủ start addresses; HEX address records/checksum không debug. Map placement/selection/budget; symbols names/addresses/binding; disassembly actual instructions.

## 7. Control flow

```text
.c/header → preprocess → compile → assembly/object
→ link objects/libraries/script → ELF+map → BIN/HEX nếu cần → flash
Reset/startup → copy initialized RAM + zero runtime regions → runtime/main
```

Object chứa symbol/relocation cho linker resolve references; header prototype không tự cung cấp implementation. Undefined symbol lúc link khác compile type error. ELF giữ segments/sections/symbol/debug metadata tùy build; BIN là image bytes theo conversion, không giữ mọi addresses/symbols. Map cho region budget, placement và symbol size. Load address nơi initializer stored khác runtime address của .data RAM; nếu startup copy từ saiaddr, global init sai trước main.

Linker và startup phải cùng hiểu boundary symbols. Kiểm .data/.bss sizing, vector placement, stacktop và reserved regions. C++ runtime còn constructors/initialization contract. [CMSIS startup template](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html) là template, order thực phải đọc startup dùng trong build.

## 8. Lifetime / ownership / state

Build owner giữ compiler/flags/target/hash; debug ELF match flash. Weak default handler che typo; definition chưa đủ nếu vector wrong. Generated headers/dependencies có version/lifecycle; stale build không source mới.

## 9. Invariants

Symbols resolved compatible ABI/signatures; vector/startup/linker target match; regions không overlap, exact image/symbolization; build success không hardware proof.

## 10. Ví dụ tối thiểu

Commands **chưa chạy**:

```text
arm-none-eabi-nm -n firmware.elf
arm-none-eabi-objdump -d -S firmware.elf
arm-none-eabi-size firmware.elf
```

nm binding/address; objdump instructions/source; size sections, map thêm reserved RAM/stack.

## 11. Failure modes

Missing/duplicate symbol, ABI flags mismatch, discarded vector/init, weak handler typo, wrong LMA/VMA, stale BIN/programmer base. Fix dependency/placement, không jump main bypass init.

## 12. Debug / observability

Record versions/flags/inputs/hash/map, compare vectors flash/ELF; step reset/copy/zero/main. Optimized C line không fixed instruction; trace undefined reference về missing object/library.

## 13. Liên hệ với bug/lab hiện có

[EMB-08](../labs/embedded_rtos/EMB-08.md), [EMB-10](../labs/embedded_rtos/EMB-10.md), [EMB-24](../labs/embedded_rtos/EMB-24.md); documents memory/build topic context.

## 14. Sai lầm thường gặp

Header≠implementation; BIN size≠RAM budget; map≠worst stack; stale ELF dù source đúng vẫn fault decode sai.

## 15. Câu hỏi tự kiểm tra

1. Relocation? Đáp án: patch references sau layout.
2. ELF/BIN? Đáp án: metadata/structure khác flat image.
3. ISR defined không chạy? Đáp án: vector/enable/binding.
4. Global initial sai? Đáp án: LMA/VMA/copy/image.
5. Undefined link thêm extern? Đáp án: cần definition.

## 16. Nguồn

[GCC stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html), [GNU ld](https://sourceware.org/binutils/docs/ld/), [nm](https://sourceware.org/binutils/docs/binutils/nm.html), [objdump](https://sourceware.org/binutils/docs/binutils/objdump.html), [CMSIS6 startup](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
