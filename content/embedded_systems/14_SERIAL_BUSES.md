# Outline — UART, SPI và I2C: wire/state/service flow

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

UART baud/parity/electrical/overrun vs ring overwrite; SPI mode/bit order/CS too early; I2C pull-ups/address/NACK/stuck/clock stretching timeout; parser losing sync after error. Fix layer đầu mất/sai byte, no checksum removal để che corruption.

Đặt câu hỏi: cơ chế trong [UART, SPI và I2C: wire/state/service flow](../../embedded_systems/14_SERIAL_BUSES.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
UART receive: start detect → sample bits → frame/error → FIFO → IRQ/DMA → ring → parser
SPI: assert CS → clock/shift/read-write → last bit/engine idle → deassert CS
I2C: START → address → ACK → data+ACK cycles → STOP or repeatedSTART
```

IRQ/DMA giảm CPU copy nhưng FIFO/bus/parser deadlines vẫn tồn tại. Disable IRQ không stop peer sending; error clear/restart phải phục hồi application framing.

## 3. Demo chạy thật

Claim có phạm vi: Electrical levels/pulls/clock/framing agreement; no buffer overrun ngoài explicit loss policy; CS/START-STOP transaction boundaries đúng; only completed data publish. Retry I2C write có thể duplicate device command nếu outcome unknown, protocol ack không universal business idempotence.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/14_SERIAL_BUSES.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

UART baud/parity/electrical/overrun vs ring overwrite; SPI mode/bit order/CS too early; I2C pull-ups/address/NACK/stuck/clock stretching timeout; parser losing sync after error. Fix layer đầu mất/sai byte, no checksum removal để che corruption.

Wire analyzer capture with correct baud/mode/address, scope rise/noise, safe register FIFO/error status, IRQ/DMA service timing/head-tail/drop counters. Wire đúng nhưng buffer thiếu→service/ownership; wire sai→physical/config trước parser. Capture burst/full/timeout/recovery, không printf inside ISR làm latency worse.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[NXP I2C specification UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf), [Analog Devices SPI](https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html). UART/SPI vendor register/timing cần manual target; URL body failures được ghi REFERENCES, không dùng guessed details làm authority.

1. UART1152008N1 payload? Đáp án:≈11520B/s ideal.
2. TX-empty release CS safe? Đáp án: cần shift-complete.
3. I2C0x48/0x90? Đáp án: notation/API shift difference.
4. Wire has all bytes but parser thiếu? Đáp án: trace FIFO→buffer→parser.
5. DMA solves framing? Đáp án: không.

[Index](../../00_INDEX.md) · [Content](../README.md).
