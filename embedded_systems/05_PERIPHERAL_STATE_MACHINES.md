# GPIO, timer và PWM: hardware state machines

Phạm vi: mô hình ngoại vi độc lập vendor; registers symbolic. [Serial buses](14_SERIAL_BUSES.md), [ADC/CAN](15_ADC_CAN.md) tách riêng để học timing/state đầy đủ.

## 1. Mục tiêu học

Từ tín hiệu pin/clock mô tả register/state transitions và software servicing; tính period/duty đúng assumptions, phân biệt config value với waveform thực.

## 2. Kiến thức tiên quyết

[MMIO/MCU](13_MMIO_MCU.md), [digital](../foundations/01_DIGITAL_REPRESENTATION.md); [interrupt](06_INTERRUPTS.md) học khi chọn async servicing.

## 3. Vấn đề mà cơ chế này giải quyết

GPIO nối logic software với điện áp, timer đo/đếm thời gian, PWM biểu diễn control bằng duty. Các engines chạy theo clock/physical input chứ không theo tốc độ loop CPU; software phải cấu hình và phục vụ events đúng thời hạn.

## 4. Khái niệm

GPIO input sampling/output driver/alternate-function mux là paths khác. Pull-up/down tạo default electrical state, open-drain chỉ actively kéo thấp và cần pull-up, push-pull drives cả mức theo ratings. Timer counter advances clock edges/events; compare/overflow/capture tạo transitions. PWM là mode timer so counter/compare để tạo output pulse.

## 5. Thành phần bên trong

GPIO registers mode/pull/output/input/mux/interrupt detect; external switch bounce có nhiều edges cho một press nên debounce là time/state policy. Output latch value đúng chưa prove pin level nếu mux/open-drain/load sai.

Timer source clock→prescaler→counter→compare/overflow→IRQ/DMA/output. Auto-reload/compare có thể shadow/preload, update event latch giá trị ở boundary để tránh glitch. Capture latches counter lúc edge; overflow sequence phải tính đúng để reconstruct time. Clock bus/timer CPU khác domains.

## 6. Data representation

GPIO bitmask tương ứng pins nhưng board mux/electrical actual manual. Timer counter width/ARR/CCR/status/output mode; compare-ready khác output edge timing. Software maintains debounce states/capture sequence; hardware keeps counter/FIFO/latches. PWM duty integer quantized by counts, không arbitrary real number.

## 7. Control flow

```text
RESET → CLOCKED → CONFIGURED → RUNNING
RUNNING + tick → counter advance
compare/overflow → pin/event/status → service/ack → continue
config pending → update boundary → new latched values
```

GPIO edge→sample/debounce state→accept press sau stability interval theo design. Masking IRQ không ngăn physical bounce; filter/debounce decisions phải explicit.

## 8. Lifetime / ownership / state

Driver/config owner giữ pin/timer allocation tới stop/release; hai modules cùng reconfigure timer frequency ảnh hưởng cả channels shared counter. Update frequency/duty khi running cần synchronized/preload sequence. Capture buffers live tới consumption; reading overflow/timer values coherent cần protocol.

## 9. Invariants

Pin ratings/mux/pulls hợp physical circuit; timer clock/rate tính đúng; output waveform period/duty đáp yêu cầu; config update không glitch vượt permitted policy; acknowledge đúng events và capacity/service latency bounded.

## 10. Ví dụ tối thiểu

**Worked model**, edge-aligned upcounter0..ARR, output high CNT<CCR, timer input1MHz, prescaler divide1, ARR999→period1000 ticks=1ms, CCR250→25% duty. CPU clock80MHz không thay fTimer giả định1MHz.

Center-aligned counts up/down và endpoints/mode thay formula; inverted output high sense thay duty. GPIO debounce model: candidate edge→wait stable10ms→accept; con số10ms là fixture, phải theo switch/user latency specs actual.

## 11. Failure modes

Wrong AF/pull/voltage, bounce multiplicity, timer clock divider assumption, off-by-one ARR, capture wrap missed, PWM update mid-period glitch, shared timer conflict. Fix physical/config/state/timebase; tăng ISR frequency không chữa mux/clock sai.

## 12. Debug / observability

Registers safe-read + pin waveform bằng logic analyzer/scope, capture period/duty/stability và software GPIO trace service. Oscilloscope đo voltage/rise/load; logic analyzer decode edges không proof analog margin. Compare expected counts với actual timebase để phân biệt clock sai/parser sai.

## 13. Liên hệ với bug/lab hiện có

[EMB-07](../labs/embedded_rtos/EMB-07.md) event multiplicity, [EMB-08](../labs/embedded_rtos/EMB-08.md) register ack, [EMB-01](../labs/embedded_rtos/EMB-01.md) servicing timing. Không thêm peripheral labs.

## 14. Sai lầm thường gặp

Register latch≠pin electrical state; timerHz≠CPUHz; PWM configured≠glitch-free. Debounce không one interrupt=one press. Duty formula không universal modes; HAL return≠waveform measured.

## 15. Câu hỏi tự kiểm tra

1. ARR999 at1MHz upcount period? Đáp án:1ms theo model.
2. CCR250 duty? Đáp án:25% theo stated mode.
3. Input bounce cần state gì? Đáp án: candidate/stability/accepted transition.
4. Hai PWM channels share frequency? Đáp án: có thể common timer counter, manual/config.
5. Scope khác analyzer? Đáp án: analog levels vs digital edge decoding.

## 16. Nguồn

[STM32 timers application note AN4776](https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf) là ví dụ vendor, phải verify body trước register claim. [CMSIS6](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html) chỉ core, không peripheral proof. Vendor-specific manual/errata/board schematic còn prerequisite implementation.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
