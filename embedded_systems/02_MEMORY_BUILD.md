# Memory: storage, layout và lifetime

Phạm vi: C17 source model, bare-metal ELF conventions; linker/startup quyết actual placement.

## 1. Mục tiêu học

Nối objects tới sections/RAM/flash, phát hiện bounds/alignment/alias/lifetime errors và stack/heap budget.

## 2. Kiến thức tiên quyết

[C](01_C_REPRESENTATION.md), [digital](../foundations/01_DIGITAL_REPRESENTATION.md); [build](11_BUILD_LINK_STARTUP.md) và [CPU](04_CPU_MCU_EXECUTION.md) nối tiếp.

## 3. Vấn đề mà cơ chế này giải quyết

Source không nói mọi object đặt đâu; compiler/linker/startup/owners phối hợp storage đúng trước access. Corruption có thể crash xa operation đầu sai.

## 4. Khái niệm

Scope quyết định tên truy cập được; storage duration quyết định storage tồn tại; lifetime quyết định object được dùng hợp lệ. Automatic local thường dùng stack/register theo ABI/compiler nhưng compiler có thể optimize bỏ. Static-duration không đồng nghĩa mọi bytes nằm flash; initialized mutable thường cần RAM runtime và initializer flash. Con trỏ tới local hết lifetime sau return dù address vẫn có bytes cũ.

Sections là tổ chức binary/tool chain: text thường instructions, rodata readonly data, data initialized mutable, bss zero initialized; heap/stack là vùng quản lý runtime/linker script thường không đơn giản mỗi cái là section file có bytes tương ứng. Bss thường không chứa payload zero đầy đủ trong image; startup/loader tạo zero trước dùng. Placement thực do script/loader, không C bắt tên section ấy. [Linker SECTIONS](https://sourceware.org/binutils/docs/ld/SECTIONS.html).

## 5. Thành phần bên trong

Automatic frame có locals/spills/saved registers theo ABI; object có thể optimized/register. Heap allocator chia blocks/free lists hoặc pools theo implementation. Stack/task/ISR regions port chọn; heap/stack không nhất thiết payload sections trong ELF.

.data initializer LMA flash và VMA RAM phải được copy; .bss NOBITS không chứa đủ zeros trong image, startup zero. Placement table/region symbols mới proof actual image.

## 6. Data representation

Alignment là địa chỉ phù hợp object/access type; padding giúp members/elements thỏa layout. Cast bytes+1 thành uint32_t* không bảo đảm alignment/type access hợp lệ. Dùng explicit bytes/memcpy phù hợp thay dereference kiểu ép tùy tiện, vẫn cần bounds và endian. Aliasing rules cho compiler quyền tối ưu khi types/access không được phép; restrict là cam kết có điều kiện của caller, không thêm vô cớ. UB cho optimizer giả định điều kiện invalid không xảy ra; debug/O0 thấy giá trịđẹp không chứng minh chương trình có semantics đúng. [GCC optimize options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html), [C++ lifetime draft](https://eel.is/c++draft/basic.life) cho trackC++ liên quan.

### Source object, storage bytes và wire representation

Một struct có members và có thể có padding. Giả sử ABI minh họa: char ở offset0, int32 cần alignment4, nên compiler có thể đặt ba padding bytes rồi int32 ở offset4; sizeof có thể là8. Đây không phải layout portable cho mọi target. Ghi raw struct qua UART vừa đưa padding lên dây vừa phụ thuộc endianness/ABI; parser bên kia không biết những lựa chọn ấy.

Đọc object representation qua character bytes là một cơ chế riêng được ngôn ngữ cho phép; nó không cho phép mọi cast pointer rồi dereference như một object type khác. Memcpy bytes vào scalar phù hợp có thể tránh unaligned access ở source level, nhưng vẫn cần chứng minh representation hợp lệ và endian meaning. Với wire protocol, decode explicit từng field là cách giữ format độc lập layout compiler.

| Vùng minh họa | Bytes ở image | Bytes khi chạy | Ai tạo trạng thái đầu? |
|---|---|---|---|
| text/rodata | Thường trong load image | Flash hoặc vùng đã load | Programmer/loader |
| data | Initializers | Mutable RAM | Startup/loader copy |
| bss | Thường NOBITS | Zero RAM | Startup/loader zero |
| Stack/heap | Không phải toàn bộ payload sẵn | State tạo động | Call/allocator/runtime |

Một map file chứng minh placement tĩnh của image, không chứng minh stack sẽ không vượt bound. Budget phải cộng call depth, large locals, library paths, ISR nesting và port context theo stacks thực.

## 7. Control flow

```text
Reset → copy initialized RAM → zero runtime regions → constructors/runtime → main
Function enter → frame/live locals → calls/use → return/lifetime ends
Allocate → check failure → init → borrow/transfer → release exactly once
```

Thứ tự system/runtime init actual startup quyết; không hardcode SystemInit trước/sau cùng cho mọi build.

## 8. Lifetime / ownership / state

Stack chứa state gọi hàm theo ABI và các spills/locals cần storage; ISR nest/task context dùng stack theo port. Stack overflow có thể overwrite trước khi fault, nên crashsite không rootcause. Heap cấp phát/release variable blocks; fragmentation khác leak: tổng free đủ nhưng largest free block không đáp ứng. Pool/fixed capacity giúp bound allocation behavior nhưng vẫn cần WCET/work path; stdarray/reserve không tự proof deadline.



Borrowed view phải kết thúc trước owner release/reallocation; DMA dùng pointer sau return cần storage lifetime đủ và access owner. Static lifetime dài không chữa buffer reuse.

## 9. Invariants

Live+bounds+alignment+allowed type access; regions không overlap, linker/startup match, worst stack/nesting nằm budget; allocation fail/full có outcome. Owner release không double-free, views không dangling.

## 10. Ví dụ tối thiểu

Timeline **mô phỏng**: .data counter initializer7 ở FLASH_B, runtime RAM_A; copy đúng mới main7. Local F→startDMA(F)→return→DMA still reads F phá lifetime. Addresses symbolic.

Fragmentation: free8+8+8 request20 contiguous fail dù total24; leak là blocks không release; churn là allocation rate cao có thể free lại.

### Borrow và reallocation có thể phá lifetime mà địa chỉ vẫn đẹp

Owner cấp block → consumer giữ pointer/view → owner realloc hoặc release → consumer đọc pointer cũ. Không cần hardware fault để chương trình sai; allocator có thể chưa tái dùng bytes, khiến run đơn giản “đúng”. Mọi access vẫn phải dựa trên object live và owner protocol.

Nếu sửa bằng static buffer, storage duration dài hơn nhưng producer vẫn có thể ghi đè khi consumer/DMA còn đọc. Lifetime và access ownership là hai điều kiện riêng. Pool giải allocation predictability khi capacity/return protocol bounded; nếu token không trả sau send fail, pool vẫn cạn dù không dùng malloc.

Host sanitizer có thể giúp tìm UAF/OOB trong paths đã chạy. Trên MCU không có sanitizer tương ứng, dùng canaries/watchpoints/trace generation và giảm reproducer; absence fault không là absence UB.

## 11. Failure modes

Dangling/realloc, stack overwrite, unaligned cast/effective-type UB, missing init/overlap, fragmentation/leak, unchecked allocation. Compiler optimization expose UB; const/volatile/tăng RAM không fix source invariant.

## 12. Debug / observability

- **SYMPTOM:** initialized counter sai tại đầu main hoặc firmware crash sau tăng buffer.
- **EVIDENCE:** exact ELF build ID, map, linker script, load/runtime addresses, startup copy/zero loops, SP bounds/canary.
- **POSSIBLE CAUSES:** image/stale ELF, .data copy sai, .bss zero initialization missing, RAM overlap hoặc stack overflow.
- **DISTINGUISHING TEST:** breakpoint trước/sau init và main, compare flash initializer/RAM; inspect region overlap; không dùng ELF khác build.
- **ROOT CAUSE:** invariant placement/init/budget bị phá theo address evidence.
- **FIX:** matching linker startup/image, proper regions và bounded stack/heap/ownership.
- **WRONG FIX:** thêm const để ép ROM, tăng stack tới overlap region khác, bỏ optimization để giấu UB.
- **REGRESSION TEST:** coldreset/warmreset theo design, region budget checks, worstinput/nesting, allocation failure cleanup.

## 13. Liên hệ với bug/lab hiện có

[EMB-10](../labs/embedded_rtos/EMB-10.md), [EMB-11](../labs/embedded_rtos/EMB-11.md), [EMB-24](../labs/embedded_rtos/EMB-24.md), [EMB-25](../labs/embedded_rtos/EMB-25.md), [OS-06](../labs/os/OS-06.md).

## 14. Sai lầm thường gặp

Scope/storage/lifetime/placement khác; total free khác largest; alignment không đủ live/type; map không dynamic stack proof; O0 pass không absence UB.

## 15. Câu hỏi tự kiểm tra

1. Bss zeros runtime ở đâu? Đáp án: startup/loader.
2. LMA/VMA khác? Đáp án: stored init/runtime.
3. Pointer sau free nhìn bytes còn? Đáp án: không usable.
4. Largest block metric dùng làm gì? Đáp án: phân biệt fragmentation với total free.
5. Watermark có bound mọi nesting? Đáp án: chỉ observed paths.

## 16. Nguồn

[N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [ld sections](https://sourceware.org/binutils/docs/ld/SECTIONS.html), [GCC optimization](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html), [CERT MEM30](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/memory-management-mem/mem30-c/).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
