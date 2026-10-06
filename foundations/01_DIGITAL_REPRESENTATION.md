# Bit, số và byte: từ ý nghĩa tới representation

Phạm vi: toán nhị phân; ví dụ byte 8 bit. C17 không bắt mọi byte có 8 bit; kiểm `CHAR_BIT`. Quy tắc phép toán C học tiếp ở [C semantics](../embedded_systems/01_C_REPRESENTATION.md).

## 1. Mục tiêu học

Đọc một dump hex thành bytes, giải thích cùng bits có thể mang ý nghĩa signed/unsigned khác nhau, và tự encode/decode số nhiều byte. Sau bài, phải dự đoán được mask, shift, wrap và thứ tự bytes trước khi dùng parser/register.

## 2. Kiến thức tiên quyết

Biết cộng/trừ và lũy thừa. Chưa cần pointer hoặc MCU. Đây là nền cho [C](../embedded_systems/01_C_REPRESENTATION.md), [CPU](../embedded_systems/04_CPU_MCU_EXECUTION.md) và wire protocol.

## 3. Vấn đề mà cơ chế này giải quyết

Máy lưu các trạng thái hữu hạn; một mẫu bit chưa mang sẵn đơn vị, dấu hay cấu trúc. Software phải chọn cách diễn giải để biến điện áp/storage thành số, ký tự hoặc lệnh. Nếu hai actor đọc cùng bytes theo format khác nhau, cả hai phép đọc có thể chạy thành công nhưng kết quả nghiệp vụ sai.

## 4. Khái niệm

Bit có hai giá trị 0/1. Một số nhị phân có trọng số vị trí: `1010₂ = 1×8+0×4+1×2+0 = 10`. Hex dùng 16 chữ số `0..9,A..F`; mỗi chữ số biểu diễn bốn bit, nên `0xA5` là `1010 0101`, bằng 165. Cách viết không đổi giá trị; `10` thập phân và `0x0A` có thể biểu diễn cùng số.

Byte là đơn vị bộ nhớ nhỏ nhất có địa chỉ trong mô hình C; `sizeof(char)==1`, còn số bit là `CHAR_BIT`. KiB=1024 bytes, khác kB=1000 bytes. Bitrate 115200 bit/s khác 115200 byte/s; framing UART còn thêm bits không phải payload.

## 5. Thành phần bên trong

Unsigned n bit có `2^n` mẫu, biểu diễn `0..2^n−1`. Trong two's complement, trọng số bit cao là `−2^(n−1)` còn các bit thấp giữ trọng số dương: `1111 1111` diễn giải signed 8 bit là −1, unsigned là 255. Miền signed là `−2^(n−1)..2^(n−1)−1`, bất đối xứng nên trị tuyệt đối của min có thể không nằm trong cùng signed type.

Để encode −5 trong 8 bit two's complement: +5 là `00000101`, đảo bit thành `11111010`, cộng 1 thành `11111011`. Đây là mô hình representation, chưa cho phép mọi phép cộng signed trong C wrap.

## 6. Data representation

| Bytes/bits | Interpretation | Value |
|---|---|---|
| `0x80` | unsigned 8 bit | 128 |
| `0x80` | signed 8 bit two's complement | −128 |
| `34 12` | little-endian 16 bit | `0x1234` |
| `34 12` | big-endian 16 bit | `0x3412` |

Endianness là thứ tự byte của giá trị nhiều byte; không đảo thứ tự bit trong từng byte. Bit order trên dây SPI là một lựa chọn protocol khác. Dump memory phải ghi địa chỉ tăng dần, độ rộng và format để người khác giải thích được.

## 7. Control flow

Mask chọn một tập vị trí bit. `x & mask` giữ bit được chọn; `x | mask` set; `x & ~mask` clear; `x ^ mask` toggle. Với `x=0xA5`, `x&0x0F=0x05`, `(x>>4)&0x0F=0x0A`. Để thay field bốn bit ở vị trí 4, mô hình toán là `(old & ~0xF0) | ((value & 0x0F)<<4)`.

Trong C phải xét promotion/type của `~` và shift trước khi dùng biểu thức này. Với register W1C, phép RMW ấy có thể sai do side effect phần cứng; xem [MMIO](../embedded_systems/13_MMIO_MCU.md).

## 8. Lifetime / ownership / state

Representation của buffer sống trong storage do owner quản lý. Decode tạo một giá trị mới; nó không tự làm source bytes bất biến. Wire buffer cần được giữ ổn định từ lúc kiểm length đến lúc đọc field. Khi write, mọi byte của một field phải được tạo xong trước publication; hai actor nhìn prefix mới/suffix cũ sẽ có một số sai dù endian đúng.

## 9. Invariants

Độ rộng field, byte order, signedness và đơn vị phải được thống nhất ở hai đầu. Giá trị đầu vào nằm trong miền representable; byte offset+width không vượt capacity. Bits reserved được xử lý theo format; không tự xem mọi unknown bit là lỗi hoặc cho phép chúng thay field khác. Phép toán ngôn ngữ phải hợp lệ độc lập với representation của CPU.

## 10. Ví dụ tối thiểu

Ví dụ tính bằng tay, kết quả **dự đoán**: unsigned 8 bit `250+10 mod 256 = 4`. Trong C target int32, hai `uint8_t` thường promote thành int, phép cộng tạo 260 rồi assignment về uint8_t tạo 4; đây là conversion, không phải int overflow.

Fragment C17, cần `uint8_t`, `uint16_t` và `uint32_t`, buffer ít nhất hai byte:

```c
#include <stdint.h>
uint16_t decode_le16(const uint8_t p[2]) {
    return (uint16_t)((uint32_t)p[0] | ((uint32_t)p[1] << 8));
}
```

Caller bảo đảm lifetime/bounds; parameter `[2]` không tự kiểm capacity. Fixture `34 12` dự đoán trả `0x1234`. Ví dụ còn cần `uint32_t`; cast trước shift tránh promotion sang signed int16 không biểu diễn được kết quả khi high byte lớn.

## 11. Failure modes

Nhầm endian tạo số hợp lệ nhưng sai; signed/unsigned interpretation làm −1 thành 255; shift vượt width gây UB theo C17; mask sai offset đụng field cạnh; raw struct chứa padding tạo bytes khác giữa builds. Sửa bằng format explicit và kiểm miền trước operation; cast sau khi UB đã xảy ra không sửa được.

## 12. Debug / observability

Dùng dump byte ở cả input/output và bảng decode bằng tay để tìm boundary đầu sai. Đọc compiler type/warnings khi kết quả arithmetic lạ. Logic analyzer cho bit order trên dây, debugger cho byte order memory; hai phép đo trả lời câu hỏi khác nhau. Lưu frame cố định `00 01 7F 80 FF` để phân biệt signedness, endian và length.

## 13. Liên hệ với bug/lab hiện có

[EMB-05](../labs/embedded_rtos/EMB-05.md): giá trị nhiều word có thể torn; invariant snapshot cùng generation. [EMB-08](../labs/embedded_rtos/EMB-08.md): mask đúng toán học vẫn có thể acknowledge nhầm register. Bài bitwise trong Base_C là context luyện tính, giữ correction ở [CORRECTIONS](../CORRECTIONS.md).

## 14. Sai lầm thường gặp

Không suy int luôn 32 bit, byte luôn octet, hay two's complement CPU cho phép signed overflow C. Hex không đồng nghĩa địa chỉ; một số có thể là dữ liệu. CRC là phép kiểm integrity theo tham số, không authentication. Không đọc packet bằng cast struct nếu chưa chứng minh layout/bounds/alignment.

## 15. Câu hỏi tự kiểm tra

1. Vì sao `0xFF` vừa có thể là −1 vừa có thể là 255? Đáp án: interpretation chọn miền/representation.
2. `01 00` LE16 và BE16 khác thế nào? Đáp án: 1 và 256.
3. Clear low nibble của `0xA5` ra gì? Đáp án: `0xA0`, theo width được chọn.
4. Vì sao UART 8N1 115200 baud không có 115200 byte/s? Đáp án: mỗi payload byte dùng mười bit trên dây.
5. Số đúng endian nhưng frame sai có thể do đâu? Đáp án: torn read/lifetime/offset/đơn vị, cần evidence boundary.

## 16. Nguồn

[WG14 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), phần representation/integer conversions: C11 public draft dùng cho nền giữ nguyên trong phạm vi C17 này; không gọi draft là ISO C17 đã licensed. [CERT shift](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/) cho constraints phép dịch. [Inventory nguồn nội bộ](../SOURCE_INVENTORY.md).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
