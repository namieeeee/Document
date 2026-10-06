# Outline — Memory: storage, layout và lifetime

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Dangling/realloc, stack overwrite, unaligned cast/effective-type UB, missing init/overlap, fragmentation/leak, unchecked allocation. Compiler optimization expose UB; const/volatile/tăng RAM không fix source invariant.

Đặt câu hỏi: cơ chế trong [Memory: storage, layout và lifetime](../../embedded_systems/02_MEMORY_BUILD.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Reset → copy initialized RAM → zero runtime regions → constructors/runtime → main
Function enter → frame/live locals → calls/use → return/lifetime ends
Allocate → check failure → init → borrow/transfer → release exactly once
```

Thứ tự system/runtime init actual startup quyết; không hardcode SystemInit trước/sau cùng cho mọi build.

## 3. Demo chạy thật

Claim có phạm vi: Live+bounds+alignment+allowed type access; regions không overlap, linker/startup match, worst stack/nesting nằm budget; allocation fail/full có outcome. Owner release không double-free, views không dangling.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/02_MEMORY_BUILD.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Dangling/realloc, stack overwrite, unaligned cast/effective-type UB, missing init/overlap, fragmentation/leak, unchecked allocation. Compiler optimization expose UB; const/volatile/tăng RAM không fix source invariant.

- **SYMPTOM:** initialized counter sai tại đầu main hoặc firmware crash sau tăng buffer.
- **EVIDENCE:** exact ELF build ID, map, linker script, load/runtime addresses, startup copy/zero loops, SP bounds/canary.
- **POSSIBLE CAUSES:** image/stale ELF, .data copy sai, .bss zero initialization missing, RAM overlap hoặc stack overflow.
- **DISTINGUISHING TEST:** breakpoint trước/sau init và main, compare flash initializer/RAM; inspect region overlap; không dùng ELF khác build.
- **ROOT CAUSE:** invariant placement/init/budget bị phá theo address evidence.
- **FIX:** matching linker startup/image, proper regions và bounded stack/heap/ownership.
- **WRONG FIX:** thêm const để ép ROM, tăng stack tới overlap region khác, bỏ optimization để giấu UB.
- **REGRESSION TEST:** coldreset/warmreset theo design, region budget checks, worstinput/nesting, allocation failure cleanup.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [ld sections](https://sourceware.org/binutils/docs/ld/SECTIONS.html), [GCC optimization](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html), [CERT MEM30](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/memory-management-mem/mem30-c/).

1. Bss zeros runtime ở đâu? Đáp án: startup/loader.
2. LMA/VMA khác? Đáp án: stored init/runtime.
3. Pointer sau free nhìn bytes còn? Đáp án: không usable.
4. Largest block metric dùng làm gì? Đáp án: phân biệt fragmentation với total free.
5. Watermark có bound mọi nesting? Đáp án: chỉ observed paths.

[Index](../../00_INDEX.md) · [Content](../README.md).
