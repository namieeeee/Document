# UART, SPI và I2C: wire/state/service flow

Phạm vi: generic protocols, vendor registers/HAL chưa khóa target. Timing numbers worked fixtures, không actual board measurement.

## 1. Mục tiêu học

Mô tả ba engines từ electrical signals/clock tới FIFO/register/error state và buffer software; chỉ ra wire-complete khác data-ready.

## 2. Kiến thức tiên quyết

[MMIO](13_MMIO_MCU.md), [GPIO/timer](05_PERIPHERAL_STATE_MACHINES.md), [digital](../foundations/01_DIGITAL_REPRESENTATION.md).

## 3. Vấn đề mà cơ chế này giải quyết

Serial engine truyền/nhận theo thời gian wire độc lập software. Byte có thể mất nếu service không kịp, và protocol byte stream không luôn application packet; cần state/framing/ownership/error recovery.

## 4. Khái niệm

UART asynchronous framing start/data/parity/stop, receiver biết baud nhưng không shared clock wire. SPI synchronous shift full-duplex thường với SCLK/MOSI/MISO/CS; clock phase/polarity và CS define sampling/framing. I2C open-drain SDA/SCL shared bus với START/address/ACK/data/STOP, pull-up/electrical timing và arbitration.

## 5. Thành phần bên trong

UART TX buffer/FIFO→shift register→wire; RX samples→shift→FIFO/status; errors parity/framing/overrun; RX-ready cần service trước FIFO overflow. UART không tự packet delimiter/length.

SPI master clock shifts both sides, read thường cần dummy writes; CPOL idle level và CPHA sampling edge thống nhất endpoints. TX register empty/FIFO empty chưa shift register idle; CS release cần transfer-complete contract. Slave phải đủ chuẩn bị data/service rate.

I2C controller state START→address+R/W→ACK/NACK→bytes→STOP/repeatedSTART; 7-bit address vs shifted API argument cần explicit. Clock stretching/arbitration/NACK/stuck bus có causes khác, timeout/recovery device/vendor rules.

## 6. Data representation

Hardware shift/FIFO/status and clock divisors giữ transfer state. Software message parser keeps partial bytes/length/checksum state; driver transfer holds source/destination/count/owner. UART baud 8N1 mỗi byte dùng10 bits; SPI raw bits/cycle còn CS gaps; I2C address/ACK overhead và pull-up rise time làm throughput khác frequency label.

### Đọc một giao tiếp từ wire vào software state

| Bus | Tín hiệu vật lý | Clock/timing | State/register model | Error và recovery cần thiết |
|---|---|---|---|---|
| UART | TX/RX và GND; mức điện theo transceiver | Hai đầu cùng baud/format, sampling theo UART | Shift register ↔ FIFO ↔ status/data | Framing/parity/overrun; clear/drain theo manual |
| SPI | SCK, MOSI/MISO, CS | Controller tạo SCK; CPOL/CPHA và CS setup/hold | TX/RX FIFO, shifter, busy/completion | Timeout/overrun, deselect/resync theo device |
| I2C | SDA/SCL open-drain với pull-ups phù hợp | SCL, rise time, stretch theo devices | START/address/ACK/data/STOP | NACK/arbitration/stuck-bus; bounded recovery |

UART8N1 có start1+data8+stop1 bits mỗi payload byte. Receiver clock không cần bằng từng cycle transmitter nhưng baud mismatch/noise có thể làm sample sai. “Receive complete” của một byte không có nghĩa application frame đã đủ: parser phải biết delimiter/length/checksum theo protocol và giữ state qua nhiều reads.

SPI hai chiều shift theo clocks; gửi command bytes có thể đồng thời nhận dummy/status bytes. CPOL định idle level; CPHA chọn quan hệ sampling/shift edges. Phải đọc timing diagram của device, không gọi chung “mode0 nhanh nhất”. Với nhiều devices, bus owner giữ cấu hình và CS cho toàn transaction; task khác đổi mode giữa frame sẽ phá contract dù mỗi write register đúng.

I2C ACK/NACK diễn ra trong transaction; NACK có thể là device absent, not-ready hoặc protocol completion tùy bước. Clock stretching làm service time dài hơn ideal clock calculation; nếu controller/device không hỗ trợ cùng rules, timeout phải phân loại. Không toggle recovery pins tùy ý khi actor khác đang dùng bus.

## 7. Control flow

```text
UART receive: start detect → sample bits → frame/error → FIFO → IRQ/DMA → ring → parser
SPI: assert CS → clock/shift/read-write → last bit/engine idle → deassert CS
I2C: START → address → ACK → data+ACK cycles → STOP or repeatedSTART
```

IRQ/DMA giảm CPU copy nhưng FIFO/bus/parser deadlines vẫn tồn tại. Disable IRQ không stop peer sending; error clear/restart phải phục hồi application framing.

## 8. Lifetime / ownership / state

TX buffers immutable tới DMA/peripheral completion đúng tầng; RX complete buffer owner chuyển parser; borrowed data không retain ngoài callback. Bus transaction owner giữ CS/I2C exclusive operation tới STOP/quiescence; tasks interleave transactions cần serialization không block ISR. Error path giữ actual engine stopped trước reclaim.

## 9. Invariants

Electrical levels/pulls/clock/framing agreement; no buffer overrun ngoài explicit loss policy; CS/START-STOP transaction boundaries đúng; only completed data publish. Retry I2C write có thể duplicate device command nếu outcome unknown, protocol ack không universal business idempotence.

## 10. Ví dụ tối thiểu

**Model predicted** UART115200 baud8N1 payload max≈11520bytes/s không gaps; 64byteFIFO chứa khoảng5.56ms wire input, service worst gap lớn hơn có thể overrun. Margin cần burst/actual FIFO rules.

SPI trace: CS-low, 16 clocks, CS-high; nhả CS khi TX FIFO empty nhưng last bits still shifting cắt frame. I2C device7-bit0x48 có thể API accepts0x48 hoặc shifted0x90; check API, không thử cả ngẫu nhiên.

### Bốn completion boundaries khác nhau

**Mô hình SPI**: CPU copy command vào driver queue → DMA chuyển bytes vào TX FIFO → shifter gửi bit cuối → device hoàn tất nội bộ sau thời gian busy riêng. Bốn mốc này không đồng nghĩa. Driver có thể cho caller reuse source buffer sau copy, hoặc sau DMA done theo contract; CS thường cần wire completion, đọc kết quả sensor cần device-ready protocol.

Một API return success có thể chỉ là queue accepted. Thiết kế operation phải ghi rõ success boundary, timeout boundary và owner được reclaim ở đâu. Khi timeout, cancel/quiesce hardware theo driver contract trước reuse buffer; chỉ đặt flag done trong software không ngừng bus actor.

## 11. Failure modes

UART baud/parity/electrical/overrun vs ring overwrite; SPI mode/bit order/CS too early; I2C pull-ups/address/NACK/stuck/clock stretching timeout; parser losing sync after error. Fix layer đầu mất/sai byte, no checksum removal để che corruption.

## 12. Debug / observability

Wire analyzer capture with correct baud/mode/address, scope rise/noise, safe register FIFO/error status, IRQ/DMA service timing/head-tail/drop counters. Wire đúng nhưng buffer thiếu→service/ownership; wire sai→physical/config trước parser. Capture burst/full/timeout/recovery, không printf inside ISR làm latency worse.

## 13. Liên hệ với bug/lab hiện có

[EMB-01](../labs/embedded_rtos/EMB-01.md), [EMB-07](../labs/embedded_rtos/EMB-07.md), [EMB-08](../labs/embedded_rtos/EMB-08.md), [EMB-13](../labs/embedded_rtos/EMB-13.md), [EMB-22](../labs/embedded_rtos/EMB-22.md).

## 14. Sai lầm thường gặp

UART bytes≠application frames; ready≠wire complete; clock rate≠payload rate; I2C NACK≠always dead bus. Increase ring không sửa sustainable producer>consumer. Device retry không always safe.

## 15. Câu hỏi tự kiểm tra

1. UART1152008N1 payload? Đáp án:≈11520B/s ideal.
2. TX-empty release CS safe? Đáp án: cần shift-complete.
3. I2C0x48/0x90? Đáp án: notation/API shift difference.
4. Wire has all bytes but parser thiếu? Đáp án: trace FIFO→buffer→parser.
5. DMA solves framing? Đáp án: không.

## 16. Nguồn

[NXP I2C specification UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf), [Analog Devices SPI](https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html). UART/SPI vendor register/timing cần manual target; URL body failures được ghi REFERENCES, không dùng guessed details làm authority.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
