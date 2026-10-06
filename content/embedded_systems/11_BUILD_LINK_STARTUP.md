# Outline — Build/link: source tới ELF và flash

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Missing/duplicate symbol, ABI flags mismatch, discarded vector/init, weak handler typo, wrong LMA/VMA, stale BIN/programmer base. Fix dependency/placement, không jump main bypass init.

Đặt câu hỏi: cơ chế trong [Build/link: source tới ELF và flash](../../embedded_systems/11_BUILD_LINK_STARTUP.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
.c/header → preprocess → compile → assembly/object
→ link objects/libraries/script → ELF+map → BIN/HEX nếu cần → flash
Reset/startup → copy initialized RAM + zero runtime regions → runtime/main
```

Object chứa symbol/relocation cho linker resolve references; header prototype không tự cung cấp implementation. Undefined symbol lúc link khác compile type error. ELF giữ segments/sections/symbol/debug metadata tùy build; BIN là image bytes theo conversion, không giữ mọi addresses/symbols. Map cho region budget, placement và symbol size. Load address nơi initializer stored khác runtime address của .data RAM; nếu startup copy từ saiaddr, global init sai trước main.

Linker và startup phải cùng hiểu boundary symbols. Kiểm .data/.bss sizing, vector placement, stacktop và reserved regions. C++ runtime còn constructors/initialization contract. [CMSIS startup template](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html) là template, order thực phải đọc startup dùng trong build.

## 3. Demo chạy thật

Claim có phạm vi: Symbols resolved compatible ABI/signatures; vector/startup/linker target match; regions không overlap, exact image/symbolization; build success không hardware proof.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/11_BUILD_LINK_STARTUP.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Missing/duplicate symbol, ABI flags mismatch, discarded vector/init, weak handler typo, wrong LMA/VMA, stale BIN/programmer base. Fix dependency/placement, không jump main bypass init.

Record versions/flags/inputs/hash/map, compare vectors flash/ELF; step reset/copy/zero/main. Optimized C line không fixed instruction; trace undefined reference về missing object/library.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[GCC stages](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html), [GNU ld](https://sourceware.org/binutils/docs/ld/), [nm](https://sourceware.org/binutils/docs/binutils/nm.html), [objdump](https://sourceware.org/binutils/docs/binutils/objdump.html), [CMSIS6 startup](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/startup_c_pg.html).

1. Relocation? Đáp án: patch references sau layout.
2. ELF/BIN? Đáp án: metadata/structure khác flat image.
3. ISR defined không chạy? Đáp án: vector/enable/binding.
4. Global initial sai? Đáp án: LMA/VMA/copy/image.
5. Undefined link thêm extern? Đáp án: cần definition.

[Index](../../00_INDEX.md) · [Content](../README.md).
