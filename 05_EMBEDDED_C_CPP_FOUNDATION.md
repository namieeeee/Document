# 05 — C/C++: từ giá trị đến binary

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Systems01 — C: representation, pointer và hợp đồng](embedded_systems/01_C_REPRESENTATION.md)
- [Systems02 — Memory, lifetime và build tới ELF](embedded_systems/02_MEMORY_BUILD.md)
- [Systems03 — C++ embedded: lifetime và chi phí](embedded_systems/03_CPP_OWNERSHIP.md)

Mục tiêu: đọc code nền từ ZIP, phân biệt lỗi ngôn ngữ và giả định phần cứng, hiểu ownership trước ISR/RTOS. Tiền đề: viết được hàm/vòng lặp C. [Corrections](CORRECTIONS.md) chỉ ra những chỗ nguồn nội bộ cần nuance; không chạy EXE có sẵn trong ZIP.

## kiểu, promotion và lifetime

Kiểu cho biết miền giá trị và phép toán; địa chỉ không nói object còn sống. `uint8_t` có thể được promote thành int trước phép toán; cast cuối không sửa overflow đã xảy ra trước đó. So sánh signed/unsigned cần xem conversion, không suy đoán theo dấu trong source. Signed overflow có thể là undefined behavior; không lấy kết quả một lần chạy làm luật. [CERT INT32](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/).

Array là vùng phần tử liên tiếp; pointer là giá trị trỏ. `sizeof` parameter khai báo như array cho kích thước pointer sau điều chỉnh, không số phần tử caller. Truyền buffer cùng length/capacity và kiểm bounds. Pointer đến local hết lifetime sau return; static local sống lâu nhưng tạo state chung và không tự thread-safe. Function pointer/callback cần contract về lifetime của context và nơi callback được gọi.

```c
// Hàm hoàn chỉnh; caller vẫn phải bảo đảm p có ít nhất n phần tử.
#include <stddef.h>
#include <stdbool.h>
bool minimum(const int *p, size_t n, int *out) {
    if (!p || !out || n == 0) return false;
    int v = p[0];
    for (size_t i = 1; i < n; ++i) if (p[i] < v) v = p[i];
    *out = v;
    return true;
}
```

## qualifier và representation

`const` hạn chế sửa qua access path đó, không bảo đảm ROM. `volatile` yêu cầu semantics truy cập theo compiler, không biến read-modify-write thành atomic và không thay mutex/barrier. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html). `restrict` là cam kết aliasing của caller trong phạm vi quy định, không bật tùy ý để tối ưu. `static` ở file scope liên quan linkage; ở local liên quan storage duration. Scope, linkage, duration là ba câu hỏi khác nhau.

Bitwise dùng unsigned đủ rộng; kiểm shift count nhỏ hơn độ rộng và xem promotion. Macro lặp evaluation (`SQUARE(i++)`) có thể gây lỗi; function/inline thường rõ hơn nhưng không hứa compiler luôn inline. Struct có padding/alignment; không serialize bằng memcpy toàn struct rồi coi wire format portable. Định nghĩa byte order, widths, version, length, integrity và bounds. CRC cần đủ tham số/coverage/test vector; CRC phát hiện lỗi ngẫu nhiên theo mô hình, không xác thực người gửi.

### Bài tính bằng tay: promotion không phải cast cuối

Giả định implementation có int32 và cung cấp uint8_t. `uint8_t a=250,b=10; uint8_t c=a+b;` promote operands sang int, cộng ra260 rồi chuyển về uint8_t được4 theo modulo. Đây không phải signed overflow. Nhưng `int x=INT_MAX; x+1` không hợp lệ theo semantics signed thông thường; cast kết quả sang unsigned sau phép cộng không sửa UB đã xảy ra. Để tính an toàn, chọn miền rộng đủ trước operation và kiểm input/output range theo contract.

Giả định unsigned int có cùng rank/width với int: `int s=-1; unsigned int u=1; s<u` chuyển s sang unsigned và không cho kết quả theo trực giác “-1 nhỏ hơn1”. Test cả negative input trước conversion. [CERT shift guidance](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/) bổ sung bounds/operand constraints; không áp dụng `1 << n` cho n tùy ý.

Undefined behavior = chuẩn không ràng buộc outcome trong trường hợp đó; implementation-defined = implementation phải chọn và tài liệu hóa hành vi thuộc loại ấy; unspecified = có các lựa chọn được phép nhưng không cần công bố lựa chọn mỗi lần. “Chạy ra đúng” không biến UB thành implementation-defined. Đối chiếu chuẩn phiên bản/compiler của dự án trước khi phân loại một expression cụ thể.

## build và map

Source → preprocessing → compilation → assembly → object → link ELF → image BIN/HEX → flash. Header khai báo không tự cấp một implementation; link lỗi undefined symbol khác compiler lỗi unknown type. Map file chỉ ra symbol/section và placement theo linker script. `.data` có giá trị khởi tạo, `.bss` được zero theo startup, `.text`/`.rodata` thường nằm flash nhưng MCU/script quyết định. BIN không giữ mọi metadata của ELF.

Kiểm relocation, startup và linker script như một bộ. Khi tăng buffer, theo dõi RAM/stack/heap, không chỉ flash. Thiếu stack thường chỉ lộ khi nested call/interrupt. Heap allocation thành công ở host không chứng minh bounded latency hay fragmentation chấp nhận được trên MCU.

## C++ không đồng nghĩa cấp phát tự do

RAII gắn cleanup với lifetime; ownership có một chủ hoặc shared theo thiết kế. Copy/move quyết định tài nguyên được nhân bản hay chuyển; con trỏ raw không tự cho biết owner. Polymorphic base cần virtual destructor khi delete derived qua base theo mô hình conventional delete, không phải mọi class đều phải virtual. [Delete-expression draft](https://eel.is/c++draft/expr.delete) có điều kiện chi tiết, gồm ngoại lệ destroying delete của phiên bản mới; không đưa ngoại lệ đó vào bài C++17 như API đã có. Vtable/RTTI/exceptions có trade-off tool chain/ABI; đo binary và timing, không cấm/bật theo khẩu hiệu.

`std::vector::push_back` amortized, lần realloc có thể tốn nhiều hơn và invalidate reference. `reserve` giảm realloc đến capacity đó, không cấm vượt capacity. Bounded buffer cần chính sách full rõ. Template definition thường ở header để instantiate; explicit instantiation là ngoại lệ cần hiểu. [C++ lifetime draft](https://eel.is/c++draft/basic.life), [vector capacity draft](https://eel.is/c++draft/vector.capacity). Draft không thay tiêu chuẩn phiên bản dự án.

## Thực hành

Lấy `pointer.c` làm bài bounds/division, `vector.cpp` làm bài capacity, không sao chép toàn code chưa kiểm. Khi có GCC/Clang, biên dịch host với warnings và sanitizer phù hợp; chúng phát hiện một số lỗi, không chứng minh ISR/DMA đúng. Máy hiện tại chưa có compiler C/C++ nên phần này chưa được chạy.

1. Vì sao volatile không bảo vệ counter++?
2. `const` và ROM khác nhau thế nào?
3. Padding phá serialization ở đâu?
4. Vì sao reserve không đủ để bảo đảm thời gian realtime?
5. Linker script và startup phải thống nhất dữ liệu nào?

Hoàn thành khi giải thích được lifetime, bounds, placement và ownership của từng buffer. Tiếp [06](06_MCU_FIRMWARE_RTOS.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [EMB-11](labs/embedded_rtos/EMB-11.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** DMA còn tham chiếu buffer sau khi storage/lifetime của buffer không còn hợp lệ. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: DMA buffer còn sống/access hợp lệ tới khi engine ngừng dùng.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Sleep trước return local buffer hoặc volatile local để DMA safe.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](embedded_systems/07_DMA_OWNERSHIP.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
