# Outline — ADC và CAN: sampling, arbitration và error states

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

ADC source impedance/sample time sai, overrun, old DMA cache bytes, wrong Vref/units/channel/skew, aliasing. CAN bitrate/sample point/termination/noACK/error storms/bus-off/starvation, stale mailbox/payload endian. Fix physics/timing/owner trước scale factor random.

Đặt câu hỏi: cơ chế trong [ADC và CAN: sampling, arbitration và error states](../../embedded_systems/15_ADC_CAN.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
timer trigger → ADC acquire → convert → DMA/result complete
→ buffer ownership handoff → calibrated engineering units
CAN transmit pending → arbitration win/loss → bits/error/ACK
→ complete or retry/recovery → application confirmation protocol nếu cần
```

CAN ACK cho valid frame reception bởi một node, không intended consumer application processed; controller auto-retry có completion/timeout policy.

## 3. Demo chạy thật

Claim có phạm vi: Analog input within permitted range, acquisition settling/channel/timebase correct, raw generation complete trước consume, unit conversion/calibration defined. CAN bit timing/transceiver/termination configured, queues/errors bounded, lost arbitration treated normal, bus-off observable with safe recovery.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/15_ADC_CAN.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

ADC source impedance/sample time sai, overrun, old DMA cache bytes, wrong Vref/units/channel/skew, aliasing. CAN bitrate/sample point/termination/noACK/error storms/bus-off/starvation, stale mailbox/payload endian. Fix physics/timing/owner trước scale factor random.

Scope input/reference and bus physical levels, analyzer CAN bit/frame/errors, register counters/overrun/status, trigger GPIO/timebase và DMA generations. Known ADC voltage fixture plus calibration before sensor comparison. CAN loopback proves controller path only, không physical bus/transceiver/peer ACK.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[ST ADC accuracy AN2834](https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf), [TI SLOA101B — CAN introduction](https://www.ti.com/lit/an/sloa101b/sloa101b.pdf). Bosch CAN2.0 URL thử fetch thất bại, không ghi đã đọc protocol ấy. Per-MCU register/errata/electrical setup chưa validated.

1. ADC2048 nghĩa temperature? Đáp án: cần Vref/resolution/calibration/sensor transfer.
2. Short sample time lỗi dù conversion complete? Đáp án: chưa settle acquisition.
3. CAN arbitration loss lỗi bus? Đáp án: normal contention.
4. ACK nghĩa consumer applied? Đáp án: no.
5. Average CAN utilization low proof deadline? Đáp án: priority interference/bursts còn.

[Index](../../00_INDEX.md) · [Content](../README.md).
