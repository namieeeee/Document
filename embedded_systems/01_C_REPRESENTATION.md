# C17: object, expression, pointer và linkage

Phạm vi: C17; worked examples byte8/int32. N1570 public C11 draft cho rules giữ nguyên ở phần này, không áp C23.

## 1. Mục tiêu học

Dự đoán type/conversion trước arithmetic, và giải thích object/bounds/lifetime/callback contracts. Học semantics trước register/HAL.

## 2. Kiến thức tiên quyết

[Digital representation](../foundations/01_DIGITAL_REPRESENTATION.md), hàm/vòng lặp. [Memory](02_MEMORY_BUILD.md) và [build](11_BUILD_LINK_STARTUP.md) học tiếp.

## 3. Vấn đề mà cơ chế này giải quyết

C cho access storage trực tiếp nhưng đòi caller giữ types/bounds/lifetime. Compile thành công và address nhìn được không chứng minh access hợp lệ; UB có thể lộ khác giữa builds.

## 4. Khái niệm

Variable declaration đặt tên/type cho object; lvalue chỉ định object/function theo rules, expression có value/side effects. Scope là nơi name thấy; linkage nối declarations cùng entity; storage duration automatic/static/thread/allocated; lifetime lúc object usable. Local static block scope/static duration; file static internal linkage; extern declaration không tự cung definition. Uninitialized automatic object không coi zero.

## 5. Thành phần bên trong

Bit là một giá trị nhị phân; byte trong C là đơn vị sizeof(char), không được giả định mọi implementation có8 bits nếu chưa kiểm CHAR_BIT. Bài MCU thông thường giả định byte8 bit và ghi rõ. Hex nhóm4 bit giúp đọc masks/address, không đổi giá trị. `0xA5` biểu diễn10100101; AND mask0 x0 F giữ lower nibble ra5; OR set bit, XOR toggle, complement cần xem type/width trước truncate.

Signed/unsigned mô tả miền giá trị và semantics phép toán, không chỉ bit cao. Ví dụ n-bit unsigned arithmetic modulo2^n theo điều kiện type; signed overflow thông thường UB, không được viện CPU two's-complement wrap để thay luật C. Exact-width typedef có availability constraints; không suy sizeof(int)=4 trên mọi target. [CERT integer overflow](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/).

Trước cộng/shift, integer promotions và usual arithmetic conversions có thể đổi type. Target int32: uint8_t250+10 thành int260 rồi convert về uint8_t4; cast cuối không sửa signed overflow đã xảy ra trước. Signed negative so unsigned cùng rank có thể chuyển thành giá trị unsigned lớn. Shift count phải đúng bounds và operand constraints. [CERT shift](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/).

Usual arithmetic conversions chọn common type sau promotions; &&/|| short-circuit khác &/|. Unsequenced side effects `i++ + i++` có thể UB. Unsigned modulo theo result type; right shift signed negative implementation-defined C17, left shift cần range/count constraints.

## 6. Data representation

Pointer trỏ object/position theo semantics; giá trị địa chỉ nhìn hợp lệ chưa chứng minh object còn sống/bounds/alignment. Array chứa elements liên tiếp; expression thường decay sang pointer nhưng array object không “là pointer”. Function parameter array điều chỉnh về pointer nên sizeof parameter không cho caller capacity. Pointer arithmetic chỉ hợp trong giới hạn object/array liên quan; one-past có thể tạo nhưng không dereference như element.

Struct nhóm members, có alignment/padding; union cho members dùng chung storage với quy tắc access/type riêng, không dùng union như portable serializer tùy ý. Enum tạo named values; representation size không được hard code thành một byte trên wire nếu chưa format explicit. Endianness quyết định thứ tự bytes của multi-byte representation. Bit field order/layout phụ thuộc implementation, không dùng raw struct/uniondump làm CAN/NVM contract.



String C là char sequence terminated null trong available storage; length/capacity/valid string khác nhau. Enum storage width và bit-field layout không wire guarantee; struct assignment không deep-copy pointees. C union representation interpretation và C++ inactive-member rules khác, không portable serializer.

## 7. Control flow

Evaluate operands/types→promotions→operation/sequenced side effects→assignment conversion→store. Function call copy argument values, pointer value vẫn cho mutate pointee. Function pointer call cần compatible signature; cast sai signature không sửa ABI. Callback indirect branch cần execution-context/context-lifetime contract.

Function pointer cho indirect call theo compatible signature; callback còn cần context/ownership/lifetime. Driver gọi callback từ ISR thì caller không được block/giữ buffer sau return nếu contract chỉ borrow. Const cấm sửa qua access path đó, không placement ROM. Volatile dùng cho observable accesses theo compiler/implementation, không lock/atomic/barrier/cacheflush. Static/extern liên quan storage/linkage tùy nơi khai báo; scope là nhìn thấy tên, storage duration là tồn tại storage, lifetime là object hợp lệ. Ba điều không đồng nhất. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html).

## 8. Lifetime / ownership / state

Automatic locals block lifetime; heap allocated tới free; static-duration tới program lifetime. Pointer copy không own object; callback registration giữ context tới unregister/quiescence, callback đang chạy cần completion protocol. Const view không làm immutable owner; sửa truly const object qua cast-away const là UB. restrict là alias promise caller phải giữ.

## 9. Invariants

Live+bounds+alignment+allowed type cùng đúng; arithmetic defined, callback signature/context hợp; string terminator trong capacity, output chỉ đọc khi success; serialization explicit width/endian, concurrency separate protocol.

## 10. Ví dụ tối thiểu

Hàm C17, **chưa compile target**:

```c
#include <stddef.h>
#include <stdbool.h>
bool minimum(const int *p, size_t n, int *out) {
    if (!p || !out || n == 0) return false;
    int v = p[0];
    for (size_t i=1; i<n; ++i) if(p[i]<v) v=p[i];
    *out=v; return true;
}
```

Caller bảo đảm p thật có n ints, out live/writable/aligned; false không đổi out. Division cần b!=0 và INT_MIN/-1 check; status riêng không trả0 che failure.

## 11. Failure modes

OOB/no terminator, conversion/overflow, dangling context, wrong signature, raw padding/endian, unsequenced effects. Optimizer assumes UB absent; O0 đẹp không proof. Fix operation đầu phá semantics.

## 12. Debug / observability

- **SYMPTOM:** decoded value sai, buffer corruption hoặc build optimized thay behavior.
- **EVIDENCE:** raw bytes, length/capacity, expression types, warnings/disassembly, sanitizer host khi có.
- **POSSIBLE CAUSES:** endian/layout, signed conversion, out of bounds, pointer lifetime hoặc compiler assumption about UB.
- **DISTINGUISHING TEST:** fixture bytes0 x34/0 x12 phải0 x1234; length0/1 reject; boundary arithmetic và signed negative; giữ optimization/build info.
- **ROOT CAUSE:** xác định operation đầu phá bounds/range/format, không chỉ location crash cuối.
- **FIX:** explicit parser/checks, status lỗi và type/range trước operation; callback ownership rõ.
- **WRONG FIX:** cast cuối mọi chỗ, volatile mọi variable, rawdump struct hoặc tăng buffer mà vẫn không bounds.
- **REGRESSION TEST:** null/short/boundary/misaligned input contract, endian fixtures và overflow/errorpaths.

## 13. Liên hệ với bug/lab hiện có

[EMB-03](../labs/embedded_rtos/EMB-03.md), [EMB-05](../labs/embedded_rtos/EMB-05.md), [EMB-11](../labs/embedded_rtos/EMB-11.md). Base_C pointer.c luyện division/%s/output contract; [CORRECTIONS](../CORRECTIONS.md) giữ nuances.

## 14. Sai lầm thường gặp

Array≠pointer, const≠ROM, volatile≠mutex, declaration≠implementation. Scope hết không free heap; null check không bounds. Undefined không guarantee, implementation-defined docs choices, unspecified permitted choices.

## 15. Câu hỏi tự kiểm tra

1. Sizeof array parameter? Đáp án: pointer size sau adjustment.
2. Static local? Đáp án: block scope/static duration.
3. Cast cuối sửa overflow? Đáp án: không.
4. Callback stack context sau return? Đáp án: dangling.
5. False minimum cho đọc out? Đáp án: không valid output mới.

## 16. Nguồn

[N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [CERT INT32](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/), [INT34](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html). Draft không full ISO/MISRA certification.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
