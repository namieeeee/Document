# Outline — Bit, số và byte: từ ý nghĩa tới representation

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Nhầm endian tạo số hợp lệ nhưng sai; signed/unsigned interpretation làm −1 thành 255; shift vượt width gây UB theo C17; mask sai offset đụng field cạnh; raw struct chứa padding tạo bytes khác giữa builds. Sửa bằng format explicit và kiểm miền trước operation; cast sau khi UB đã xảy ra không sửa được.

Đặt câu hỏi: cơ chế trong [Bit, số và byte: từ ý nghĩa tới representation](../../foundations/01_DIGITAL_REPRESENTATION.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Mask chọn một tập vị trí bit. `x & mask` giữ bit được chọn; `x | mask` set; `x & ~mask` clear; `x ^ mask` toggle. Với `x=0xA5`, `x&0x0F=0x05`, `(x>>4)&0x0F=0x0A`. Để thay field bốn bit ở vị trí 4, mô hình toán là `(old & ~0xF0) | ((value & 0x0F)<<4)`.

Trong C phải xét promotion/type của `~` và shift trước khi dùng biểu thức này. Với register W1C, phép RMW ấy có thể sai do side effect phần cứng; xem [MMIO](../../foundations/../embedded_systems/13_MMIO_MCU.md).

## 3. Demo chạy thật

Claim có phạm vi: Độ rộng field, byte order, signedness và đơn vị phải được thống nhất ở hai đầu. Giá trị đầu vào nằm trong miền representable; byte offset+width không vượt capacity. Bits reserved được xử lý theo format; không tự xem mọi unknown bit là lỗi hoặc cho phép chúng thay field khác. Phép toán ngôn ngữ phải hợp lệ độc lập với representation của CPU.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../foundations/01_DIGITAL_REPRESENTATION.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Nhầm endian tạo số hợp lệ nhưng sai; signed/unsigned interpretation làm −1 thành 255; shift vượt width gây UB theo C17; mask sai offset đụng field cạnh; raw struct chứa padding tạo bytes khác giữa builds. Sửa bằng format explicit và kiểm miền trước operation; cast sau khi UB đã xảy ra không sửa được.

Dùng dump byte ở cả input/output và bảng decode bằng tay để tìm boundary đầu sai. Đọc compiler type/warnings khi kết quả arithmetic lạ. Logic analyzer cho bit order trên dây, debugger cho byte order memory; hai phép đo trả lời câu hỏi khác nhau. Lưu frame cố định `00 01 7F 80 FF` để phân biệt signedness, endian và length.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[WG14 N1570](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), phần representation/integer conversions: C11 public draft dùng cho nền giữ nguyên trong phạm vi C17 này; không gọi draft là ISO C17 đã licensed. [CERT shift](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int34-c/) cho constraints phép dịch. [Inventory nguồn nội bộ](../../foundations/../SOURCE_INVENTORY.md).

1. Vì sao `0xFF` vừa có thể là −1 vừa có thể là 255? Đáp án: interpretation chọn miền/representation.
2. `01 00` LE16 và BE16 khác thế nào? Đáp án: 1 và 256.
3. Clear low nibble của `0xA5` ra gì? Đáp án: `0xA0`, theo width được chọn.
4. Vì sao UART 8N1 115200 baud không có 115200 byte/s? Đáp án: mỗi payload byte dùng mười bit trên dây.
5. Số đúng endian nhưng frame sai có thể do đâu? Đáp án: torn read/lifetime/offset/đơn vị, cần evidence boundary.

[Index](../../00_INDEX.md) · [Content](../README.md).
