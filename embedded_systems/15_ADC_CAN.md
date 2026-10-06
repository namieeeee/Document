# ADC và CAN: sampling, arbitration và error states

Phạm vi: ADC generic; **Classical CAN** mental model, CAN FD payload/bitrate differences không gộp. No board measurements/register addresses.

## 1. Mục tiêu học

Nối analog signal tới sampled raw data/units, và CAN frame tới bus arbitration/error/recovery; xác định acquisition/completion/consumption boundaries.

## 2. Kiến thức tiên quyết

[Digital](../foundations/01_DIGITAL_REPRESENTATION.md), [GPIO/timer](05_PERIPHERAL_STATE_MACHINES.md), [serial](14_SERIAL_BUSES.md), [MMIO](13_MMIO_MCU.md).

## 3. Vấn đề mà cơ chế này giải quyết

ADC tạo số từ điện áp tại một khoảng sampling có error/bandwidth limits; CAN nhiều nodes tranh bus phải xác định priority/error recovery. Data-ready không tự valid physics và CAN ACK không chứng minh business action completed.

## 4. Khái niệm

ADC sample/hold lấy mức analog rồi conversion quantize theo resolution/reference; sample time/source impedance/calibration tác động accuracy. CAN uses controller+transceiver+physical differential bus, dominant/recessive bits, arbitration/error detection. Frame identifier dùng arbitration/interpretation, không luôn device address.

## 5. Thành phần bên trong

ADC trigger→acquisition capacitor settling→conversion→result register/FIFO→EOC/overrun→IRQ/DMA; sequential channels có skew/crosstalk constraints, reference noise làm scale sai. Nyquist/anti-alias filtering/bandwidth là input-system constraints; higher sample rate không alone correct sensor model.

CAN idle→arbitration→frame data/CRC→ACK→completion, controllers monitor sent/read bits. Nodes losing nondestructive arbitration defer, còn winner continues. Error counters/status drive error-active/error-passive/bus-off; recovery follows configured/protocol rules. Acceptance filter chọn frames software receives, không authorization.

## 6. Data representation

ADC raw integer counts, resolution/reference/channel/timestamp/generation; count chưa voltage/temperature. Typical ideal unipolar mapping x≈V/Vref×(2^N−1) nhưng ADC transfer/calibration/endpoint formula vendor-specific. CAN ID/data length/payload/error/timestamp; Classical CAN payload max8bytes, CANFD riêng max64 và may switch data bitrate. Payload fields encode endian/units/version explicit.

## 7. Control flow

```text
timer trigger → ADC acquire → convert → DMA/result complete
→ buffer ownership handoff → calibrated engineering units
CAN transmit pending → arbitration win/loss → bits/error/ACK
→ complete or retry/recovery → application confirmation protocol nếu cần
```

CAN ACK cho valid frame reception bởi một node, không intended consumer application processed; controller auto-retry có completion/timeout policy.

## 8. Lifetime / ownership / state

ADC DMA buffer live/owned through transfer, circular mode reuse deadline. Calibration/reference/channel config owner cannot change mid measurement without defined boundary. CAN mailbox/queued payload immutable until copied/transmitted per driver; timeout/cancel needs engine quiescence before reclaim.

## 9. Invariants

Analog input within permitted range, acquisition settling/channel/timebase correct, raw generation complete trước consume, unit conversion/calibration defined. CAN bit timing/transceiver/termination configured, queues/errors bounded, lost arbitration treated normal, bus-off observable with safe recovery.

### Một sample cần hai clocks và một owner

ADC peripheral clock quyết acquisition/conversion timing; timer trigger quyết thời điểm bắt đầu sample sequence. Tăng ADC clock không tự tăng tốc độ trigger; tăng trigger quá nhanh có thể gây overrun hoặc không đủ acquisition time. Sample-and-hold capacitor cần thời gian settle theo source impedance và front-end. Code đọc raw đúng sau completion vẫn có thể đo sai analog value nếu acquisition chưa settle.

**Mô hình tự xây**: samples raw [2048,2048] với Vref3.3, cùng resolution/channel/calibration cho cùng approximately1.65V. Nếu Vref thực đổi nhưng converter vẫn dùng3.3, raw không thay cách encode mà physical meaning đã khác. Nếu multi-channel sequence lấy các channels ở thời điểm khác nhau, không gọi chúng snapshot đồng thời khi signal đang thay nhanh. Lưu channel/time/generation cùng buffer để downstream không ghép nhầm.

### Bus state và application state không cùng boundary

CAN controller có thể ACK frame hợp lệ mà application chưa dequeue hoặc apply payload. Acceptance filter chủ yếu chọn receive path, không proof sender identity. Error counters/error-passive/bus-off thuộc controller protocol; application cần policy khi không còn progress, kể cả retry/recovery được bật.

**Mô hình tự xây**: request command K được transmit/ACK; receiver queue đầy và bỏ message. Sender thấy transmission success nhưng command chưa được thực hiện. Nếu yêu cầu business confirmation, payload protocol cần request ID/result/timeout và dedup phù hợp; resend command không idempotent có thể tạo duplicate nếu receiver thực hiện nhưng response mất.

Bit timing phải thống nhất nominal bitrate/sample point và oscillator/bus constraints giữa nodes. CAN FD có data phase riêng khi switch bitrate, không dùng cùng tính toán Classical CAN cho mọi frame. Các register fields và recovery sequence vẫn cần exact controller/manual; không đoán từ tên HAL API.

## 10. Ví dụ tối thiểu

**Model** N12 ideal ADC/Vref3.3V, raw2048→approx1.65V theo illustrative formula; actual transfer/calibration/vendor tolerances quyết accuracy. Voltage≠temperature nếu sensor law chưa known.

CAN contenders same format IDs0x100 và0x200:0x100 generally wins bitwise arbitration; extended/base format arbitration details không simplified numeric rule mọi frames. Higher-priority continuous frames có thể delay others, throughput đủ chưa bound latency.

## 11. Failure modes

ADC source impedance/sample time sai, overrun, old DMA cache bytes, wrong Vref/units/channel/skew, aliasing. CAN bitrate/sample point/termination/noACK/error storms/bus-off/starvation, stale mailbox/payload endian. Fix physics/timing/owner trước scale factor random.

## 12. Debug / observability

Scope input/reference and bus physical levels, analyzer CAN bit/frame/errors, register counters/overrun/status, trigger GPIO/timebase và DMA generations. Known ADC voltage fixture plus calibration before sensor comparison. CAN loopback proves controller path only, không physical bus/transceiver/peer ACK.

## 13. Liên hệ với bug/lab hiện có

[EMB-12](../labs/embedded_rtos/EMB-12.md), [EMB-13](../labs/embedded_rtos/EMB-13.md), [EMB-15](../labs/embedded_rtos/EMB-15.md) sampling buffer/cache/reuse; [EMB-19](../labs/embedded_rtos/EMB-19.md) starvation mechanism. Không thêm lab mới.

## 14. Sai lầm thường gặp

Raw ADC≠physical quantity; CAN filter≠security policy; ACK≠application completion; FD≠Classical same timing/payload. DMA no CPU copy vẫn service/ownership constraints. CRC not sender authentication.

## 15. Câu hỏi tự kiểm tra

1. ADC2048 nghĩa temperature? Đáp án: cần Vref/resolution/calibration/sensor transfer.
2. Short sample time lỗi dù conversion complete? Đáp án: chưa settle acquisition.
3. CAN arbitration loss lỗi bus? Đáp án: normal contention.
4. ACK nghĩa consumer applied? Đáp án: no.
5. Average CAN utilization low proof deadline? Đáp án: priority interference/bursts còn.

## 16. Nguồn

[ST ADC accuracy AN2834](https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf), [TI SLOA101B — CAN introduction](https://www.ti.com/lit/an/sloa101b/sloa101b.pdf). Bosch CAN2.0 URL thử fetch thất bại, không ghi đã đọc protocol ấy. Per-MCU register/errata/electrical setup chưa validated.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
