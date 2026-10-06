# Outline — GPIO, timer và PWM: hardware state machines

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Wrong AF/pull/voltage, bounce multiplicity, timer clock divider assumption, off-by-one ARR, capture wrap missed, PWM update mid-period glitch, shared timer conflict. Fix physical/config/state/timebase; tăng ISR frequency không chữa mux/clock sai.

Đặt câu hỏi: cơ chế trong [GPIO, timer và PWM: hardware state machines](../../embedded_systems/05_PERIPHERAL_STATE_MACHINES.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
RESET → CLOCKED → CONFIGURED → RUNNING
RUNNING + tick → counter advance
compare/overflow → pin/event/status → service/ack → continue
config pending → update boundary → new latched values
```

GPIO edge→sample/debounce state→accept press sau stability interval theo design. Masking IRQ không ngăn physical bounce; filter/debounce decisions phải explicit.

## 3. Demo chạy thật

Claim có phạm vi: Pin ratings/mux/pulls hợp physical circuit; timer clock/rate tính đúng; output waveform period/duty đáp yêu cầu; config update không glitch vượt permitted policy; acknowledge đúng events và capacity/service latency bounded.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/05_PERIPHERAL_STATE_MACHINES.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Wrong AF/pull/voltage, bounce multiplicity, timer clock divider assumption, off-by-one ARR, capture wrap missed, PWM update mid-period glitch, shared timer conflict. Fix physical/config/state/timebase; tăng ISR frequency không chữa mux/clock sai.

Registers safe-read + pin waveform bằng logic analyzer/scope, capture period/duty/stability và software GPIO trace service. Oscilloscope đo voltage/rise/load; logic analyzer decode edges không proof analog margin. Compare expected counts với actual timebase để phân biệt clock sai/parser sai.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[STM32 timers application note AN4776](https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf) là ví dụ vendor, phải verify body trước register claim. [CMSIS6](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html) chỉ core, không peripheral proof. Vendor-specific manual/errata/board schematic còn prerequisite implementation.

1. ARR999 at1MHz upcount period? Đáp án:1ms theo model.
2. CCR250 duty? Đáp án:25% theo stated mode.
3. Input bounce cần state gì? Đáp án: candidate/stability/accepted transition.
4. Hai PWM channels share frequency? Đáp án: có thể common timer counter, manual/config.
5. Scope khác analyzer? Đáp án: analog levels vs digital edge decoding.

[Index](../../00_INDEX.md) · [Content](../README.md).
