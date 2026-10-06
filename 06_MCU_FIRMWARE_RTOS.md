# 06 — MCU, ISR, DMA và RTOS

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Systems04 — CPU chạy C như thế nào?](embedded_systems/04_CPU_MCU_EXECUTION.md)
- [Systems05 — Peripheral là state machine phần cứng](embedded_systems/05_PERIPHERAL_STATE_MACHINES.md)
- [Systems06 — Interrupt: chuyển control flow, giữ invariant](embedded_systems/06_INTERRUPTS.md)
- [Systems07 — DMA: actor phần cứng và buffer ownership](embedded_systems/07_DMA_OWNERSHIP.md)
- [Systems08 — Main, ISR, DMA và task cùng một buffer](embedded_systems/08_CONCURRENCY_BUFFERS.md)
- [Systems09 — RTOS: scheduler trước API](embedded_systems/09_RTOS_SCHEDULER.md)

Mục tiêu: chuyển mô hình memory/ownership thành firmware có deadline và bằng chứng. Tiền đề chương 05. Cortex-M là core tham chiếu; chỉ dùng địa chỉ register/IRQ từ manual đúng MCU. STM32 là lựa chọn thực hành, không coi mọi dòng có cùng cache/DMA/peripheral.

## reset và core

Vector table chứa entry startup/handler theo kiến trúc; startup cụ thể khởi tạo stack, copy `.data`, zero `.bss`, gọi phần system/runtime rồi main. Thứ tự `SystemInit`, runtime C++ constructors và relocation phụ thuộc startup thực; đọc file dùng trong build thay vì học thuộc một pseudo-order. PC chỉ lệnh, xPSR giữ trạng thái; privileged/unprivileged và MSP/PSP là cơ chế core, RTOS chọn cách dùng. [CMSIS Core](https://arm-software.github.io/CMSIS_6/latest/Core/index.html).

NVIC quản lý interrupt; số priority bits do implementation. Trên Cortex-M priority số nhỏ thường có urgency cao hơn, nhưng grouping/subpriority và ngưỡng RTOS phải theo port. Không mọi core đều có cùng API grouping; xem [CMSIS NVIC](https://arm-software.github.io/CMSIS_6/latest/Core/group__NVIC__gr.html). Nesting/tail-chaining giảm một số overhead, không làm ISR vô hạn an toàn. SysTick có thể làm time base; RTOS có thể dùng timer khác hoặc tickless. Không suy ra thời gian wall clock chỉ từ tick count.

## peripheral theo protocol

GPIO: kiểm mode, pull, electrical level và bounce. Timer/PWM: clock tree → prescaler → period/duty, tránh nhầm clock bus với timer clock. UART cần baud/framing/overrun và ring buffer; SPI cần mode/chip select, I2 C cần pull-up/address/timeout/bus recovery. CAN cần bitrate, arbitration/filter/error state; bus vật lý và termination quyết định nhiều lỗi. ADC cần reference, sample time/impedance, calibration và đơn vị; raw count không tự là nhiệt độ.

Watchdog phải được feed sau bằng chứng progress của các tác vụ quan trọng. Feed trong timer độc lập có thể che main đã treo. Khi reset, lưu reset reason và tối thiểu evidence an toàn, không ghi flash vô hạn trong ISR.

## ISR ngắn và có ownership

ISR acknowledge đúng nguồn, lấy dữ liệu cần giữ rồi signal task bằng API ISR-safe. Đừng printf/block/malloc trong ISR nếu không có contract rõ. Shared flag có thể mất nhiều event; counter/queue cần giới hạn và overflow policy. Critical section phải ngắn và theo port; tắt mọi interrupt lâu có thể phá deadline peripheral khác. Atomic CPU store không mặc nhiên áp dụng cho packed/misaligned hoặc multiword data.

DMA chạy độc lập với CPU. Buffer phải sống tới completion; một local buffer bị dùng sau return có lỗi lifetime. CPU không được đọc/ghi vùng DMA đang sở hữu. Với chip có data cache, clean/invalidate đúng hướng, alignment và cache-line sharing; chip không cache không có lỗi coherency ấy nhưng vẫn có race ownership. Memory barrier, compiler barrier và cache maintenance giải quyết ba vấn đề khác nhau. [CMSIS D-cache Cortex-M7](https://arm-software.github.io/CMSIS_6/latest/Core/group__Dcache__functions__m7.html) có contract alignment cho thao tác theo vùng; vẫn cần manual MCU/engine trước khi chọn buffer placement.

```text
FREE → CPU_FILL → DMA_OWNED → COMPLETE → CPU_CONSUME → FREE
```

Double buffer không tự giải quyết ownership: nếu CPU chưa xử lý xong mà DMA quay lại buffer đó, dữ liệu vẫn bị ghi đè. Đo worst-case service time và có drop/backpressure policy.

## RTOS là scheduling cộng đồng bộ

Task ready chưa chắc chạy; task blocked không tiêu CPU như busy wait. Deadline cần WCET, blocking, interference và jitter. Priority inversion: H chờ lock L giữ, M chạy trước L; inheritance giúp L được chạy để nhả lock, không sửa deadlock hoặc task tự giữ lock vô hạn. Mutex có owner; semaphore truyền event/resource count; queue còn truyền dữ liệu. [Free RTOS semphr.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/semphr.h), [Zephyr mutex](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html).

Zephyr phân biệt cooperative/preemptive theo cấu hình và priority range; không mang số priority Free RTOS sang Zephyr mà không map semantics. [Zephyr scheduling](https://docs.zephyrproject.org/latest/kernel/services/scheduling/index.html). Stack size đơn vị phụ thuộc API: Free RTOS stack depth dùng đơn vị Stack Type_t theo port, không mặc nhiên byte; xem [task.h](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h). Kiểm header/port release và high-water mark, kể cả nested ISR và C++ call depth. Với Zephyr message queue, phân biệt dữ liệu được copy vào queue và một field pointer bên trong payload: queue không tự copy vùng pointer trỏ tới. [Message queues](https://docs.zephyrproject.org/latest/kernel/services/data_passing/message_queues.html).

## Lab và checkpoint

[30 lab embedded/RTOS](labs/embedded_rtos/README.md): 10 ISR, 5 DMA, 15 RTOS. Simulation timeline chỉ kiểm invariant; phải đo trên board bằng trace/GPIO/logic analyzer trước khi khẳng định realtime. Không dùng register giả như địa chỉ thật.

1. ISR vừa clear flag vừa xảy ra event mới có thể mất dữ liệu ra sao?
2. Cache clean khác invalidate khi DMA transmit/receive thế nào?
3. Priority inheritance không giải quyết điều gì?
4. Task stack và ISR stack có dùng cùng vùng trên port của bạn không?
5. Watchdog cần bằng chứng progress nào?

Hoàn thành khi vẽ được ownership và lịch task/ISR, có overflow policy, và xác định manual/port cần tra cứu. Tiếp [07](07_OPERATING_SYSTEMS_ADVANCED.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [EMB-03](labs/embedded_rtos/EMB-03.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Increment gồm load/modify/store, volatile không làm chuỗi này atomic. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Mọi increment được bảo vệ atomicity của RMW invariant.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Thêm volatile count rồi coi counter++ atomic.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](embedded_systems/06_INTERRUPTS.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
