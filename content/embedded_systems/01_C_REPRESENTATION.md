# Outline — C17: object, expression, pointer và linkage

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

OOB/no terminator, conversion/overflow, dangling context, wrong signature, raw padding/endian, unsequenced effects. Optimizer assumes UB absent; O0 đẹp không proof. Fix operation đầu phá semantics.

Đặt câu hỏi: cơ chế trong [C17: object, expression, pointer và linkage](../../embedded_systems/01_C_REPRESENTATION.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Evaluate operands/types→promotions→operation/sequenced side effects→assignment conversion→store. Function call copy argument values, pointer value vẫn cho mutate pointee. Function pointer call cần compatible signature; cast sai signature không sửa ABI. Callback indirect branch cần execution-context/context-lifetime contract.

Function pointer cho indirect call theo compatible signature; callback còn cần context/ownership/lifetime. Driver gọi callback từ ISR thì caller không được block/giữ buffer sau return nếu contract chỉ borrow. Const cấm sửa qua access path đó, không placement ROM. Volatile dùng cho observable accesses theo compiler/implementation, không lock/atomic/barrier/cacheflush. Static/extern liên quan storage/linkage tùy nơi khai báo; scope là nhìn thấy tên, storage duration là tồn tại storage, lifetime là object hợp lệ. Ba điều không đồng nhất. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html).

## 3. Demo chạy thật

Claim có phạm vi: Live+bounds+alignment+allowed type cùng đúng; arithmetic defined, callback signature/context hợp; string terminator trong capacity, output chỉ đọc khi success; serialization explicit width/endian, concurrency separate protocol.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/01_C_REPRESENTATION.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

OOB/no terminator, conversion/overflow, dangling context, wrong signature, raw padding/endian, unsequenced effects. Optimizer assumes UB absent; O0 đẹp không proof. Fix operation đầu phá semantics.

- **SYMPTOM:** decoded value sai, buffer corruption hoặc build optimized thay behavior.
- **EVIDENCE:** raw bytes, length/capacity, expression types, warnings/disassembly, sanitizer host khi có.
- **POSSIBLE CAUSES:** endian/layout, signed conversion, out of bounds, pointer lifetime hoặc compiler assumption about UB.
- **DISTINGUISHING TEST:** fixture bytes0 x34/0 x12 phải0 x1234; length0/1 reject; boundary arithmetic và signed negative; giữ optimization/build info.
- **ROOT CAUSE:** xác định operation đầu phá bounds/range/format, không chỉ location crash cuối.
- **FIX:** explicit parser/checks, status lỗi và type/range trước operation; callback ownership rõ.
- **WRONG FIX:** cast cuối mọi chỗ, volatile mọi variable, rawdump struct hoặc tăng buffer mà vẫn không bounds.
- **REGRESSION TEST:** null/short/boundary/misaligned input contract, endian fixtures và overflow/errorpaths.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), [CERT INT32](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/), [INT34](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html). Draft không full ISO/MISRA certification.

1. Sizeof array parameter? Đáp án: pointer size sau adjustment.
2. Static local? Đáp án: block scope/static duration.
3. Cast cuối sửa overflow? Đáp án: không.
4. Callback stack context sau return? Đáp án: dangling.
5. False minimum cho đọc out? Đáp án: không valid output mới.

[Index](../../00_INDEX.md) · [Content](../README.md).
