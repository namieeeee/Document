# Interrupts: event, preemption và coherent state

Phạm vi: Armv7E-M Cortex-M4/CMSIS6.0; FreeRTOS11.1 IRQ thresholds theo port, không universal priority recipe.

## 1. Mục tiêu học

Vẽ event→NVIC→entry→ISR→ack→return; phân tích priority/nesting/latency/jitter/reentrancy và critical snapshots.

## 2. Kiến thức tiên quyết

[Cortex-M4](12_CORTEX_M.md), [peripheral/MMIO](13_MMIO_MCU.md), [C/memory](01_C_REPRESENTATION.md).

## 3. Vấn đề mà cơ chế này giải quyết

Polling mọi event lãng phí và khó đáp ứng latency; interrupts chuyển control flow tới service, nhưng preemption tạo interleavings/shared-state/stack constraints.

## 4. Khái niệm

Peripheral event/status khác IRQ line, NVIC pending khác active, mask/enable khác acknowledge source. ISR là handler execution; synchronous fault/exception có causes khác device IRQ. Priority arbitration quyết urgency, không business importance label.

## 5. Thành phần bên trong

Peripheral tạo event/status và interrupt request khi enabled theo config. NVIC ghi pending, xét enable/mask/priority và core state để quyết định lấy exception. Cortex-M lưu state cần thiết theo exception model, chuyển PC tới handler qua vector và dùng context phù hợp; ISR/compiler còn prologue/epilogue riêng. Return phục hồi execution hoặc chuyển exception theo hardware/port. Không giả định mọi frame giống nhau khi có FPU/security extension hoặc mọi register tự được lưu theo một C ABI bất kỳ. [NVIC](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__NVIC__gr.html), [Core registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html).

```text
Peripheral event → pending IRQ → arbitration/masks
→ context save + vector → acknowledge/acquire minimal data
→ enqueue/notify task → exception return → interrupted flow hoặc scheduler
```

Pending không đồng nghĩa đang chạy; disable/mask không tự xóa peripheral event. Acknowledge ở peripheral khác clear NVIC pending; chọn sequence theo register semantics để không mất event tới giữa các bước. Nếu level nguồn còn asserted, return có thể kích lại. “Handler gọi rồi” chưa chứng minh nguồn đã serviced.

## 6. Data representation

NVIC enable/pending/active/priorities, peripheral event latches/FIFOs, core stacked context, driver ring/sequence giữ states ở different actors. Boolean ready encode có/không chứ không multiplicity; counter/queue capacity/full policy needed. Same two fields read separately không cùng generation guarantee.

### Pending, active và peripheral status là ba state khác nhau

Pending ghi nhận một exception đang chờ được xét; active ghi handler đã được nhận và chưa hoàn tất. Peripheral status mô tả event của thiết bị. Một pending bit thường không đếm được mọi event: nếu hai edges tới khi bit đã set, multiplicity có thể không được giữ. Muốn đếm samples phải dùng hardware counter/FIFO/DMA hoặc protocol có capacity và overflow policy.

Acknowledge là thao tác theo peripheral manual: read-to-clear, write-one-to-clear, đọc data register hay sequence khác. Clear NVIC pending không thay việc phục vụ nguồn IRQ. Với level source còn asserted, interrupt có thể pending lại. Ngược lại, read-modify-write trên W1C register có thể clear những flags mà ISR chưa xử lý.

### Urgency, priority grouping và kernel threshold

Trên M4, số priority nhỏ biểu thị urgency cao; số bits implemented do MCU quyết định. CMSIS NVIC_SetPriority nhận logical value rồi xử lý vị trí bits theo định nghĩa device; không đưa một byte đã shift như thể chưa shift. Grouping tách preemption/subpriority; subpriority không tự cho phép preempt.

Critical section dựa BASEPRI không chặn mọi interrupt. FreeRTOS port đặt threshold để bảo vệ kernel structures; IRQ urgency cao hơn threshold vẫn có thể chạy nhưng không được gọi kernel APIs bị cấm ở mức đó. Vì vậy “đã vào critical” chưa chứng minh buffer main/ISR riêng được bảo vệ. Phải đối chiếu cả source actor và mask đang dùng.

## 7. Control flow

Hardware event→IRQ pending→mask/priority decision→save context/vector→compiler prologue→bounded acquire/ack→publish queue/notify→restore/return. Level source still asserted retrigger; acknowledge sequence follow manual to avoid new event cleared. RTOS wake may request context switch after ISR theo port.

## 8. Lifetime / ownership / state

Latency từ event đến service gồm hardware propagation, mask interval, đang phục vụ interrupt khác, context costs và bus/memory stalls. Duration ISR là time bên trong handler, không toàn latency. Priority số nhỏ thường urgency cao trên Cortex-M; implemented bits/grouping và preemption/subpriority tùy core/config. Free RTOS API IRQ threshold phải theo port/release; không so số priority kernel trực tiếp với unshifted hardware encoding.

Nesting tạo thêm contexts/stack demand; tail-chaining tối ưu một số transitions, không chứng minh deadline. Tắt interrupt lâu để giữ data coherent có thể làm UART overrun. Phải bound critical section, save/restore mask trước đó, không enable vô điều kiện nếu caller vốn đang masked.

ISR may reenter shared driver via higher interrupt/task interactions; nonreentrant static scratch needs exclusion or per-context storage. Callback borrowed buffer lifetime tied handoff, not IRQ function name.

## 9. Invariants

Atomic access chỉ nói thao tác không bị quan sát như phần bị xé theo guarantee target; read-modify-write hoặc pair snapshot là invariant khác. Volatile counter++ thường load/add/store: ISR cập nhật giữa load và store có thể mất increment. Hai aligned scalar reads vẫn có thể lấy x mới/y cũ. Critical snapshot, atomic protocol hoặc versioned scheme đúng memory semantics mới bảo vệ; không chọn lock-free bằng niềm tin “MCU 32 bit”. [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html).

Ví dụ main thấy ready=true, process buffer, rồi ready=false; event mới tới trong process bị clear cuối. Clear trước process cũng chưa bảo vệ buffer bị ISR ghi tiếp. Cần event counting/coalescing policy và buffer owner; ISR signal không tự chuyển lifetime của memory. Queue pointer khác queue copied-value; xem [buffers](08_CONCURRENCY_BUFFERS.md).

Invariant: acknowledge không mất event ngoài policy; ISR bounded/nonblocking; kernel API context/urgency hợp lệ; shared data coherent; stack đủ cho nesting. ISR có thể dùng notify/queue ISR-safe và check full result; mutex chờ owner task không hợp ISR contract phổ biến.

Nonblocking bounded ISR, acknowledge correct source, coherent snapshot, full policy and save/restore mask state. Critical section CPU doesn't stop DMA.

## 10. Ví dụ tối thiểu

**Instruction schedule model**: main LOAD count0→ISR count1→main ADD old0+1→STORE1, two increments only1. Volatile doesn't merge instructions. Pair x/y: main read xGen1→ISR writes x/yGen2→main read yGen2 creates mixed snapshot. Protect small copy via target critical protocol, process outside masked region.

### Tách latency thành các khoảng có thể đo

**Timeline minh họa**, không số đo core: event ở t0; peripheral/NVIC giữ pending; mask mở ở t1; core nhận exception ở t2; instruction ISR đầu ở t3; data xử lý xong ở t4. Event-to-handler latency là t3−t0, handler execution là t4−t3. Một ISR rất ngắn vẫn có latency lớn do mask hoặc higher-urgency handler.

GPIO set tại entry chỉ đo được từ entry trở đi nếu không có timestamp event ngoài CPU. Muốn chứng minh latency event→ISR, dùng đồng thời signal event và GPIO entry trên logic analyzer, ghi clock/config/nesting load. Đặt breakpoint có thể cho thiết bị tiếp tục chạy, làm FIFO đầy; đó là observer effect, không bằng chứng rằng tốc độ bình thường cũng overflow.

## 11. Failure modes

Lost increment/event clear race, torn/mixed snapshot, invalid priority calling kernel, long mask/ISR overrun, blocking ISR waits interrupted owner, reentrant scratch corruption/nesting stack. Fix exact invariant/protocol not just ISR shortness.

## 12. Debug / observability

- **SYMPTOM:** producer2 events nhưng counter chỉ tăng1, hoặc pair sample không coherent.
- **EVIDENCE:** disassembly RMW, event/read/write timeline, mask state, alignment/width và sequence numbers.
- **POSSIBLE CAUSES:** lost update, event coalescing có chủ đích, torn access hoặc register clear sai.
- **DISTINGUISHING TEST:** buộc ISR giữa load/store trong model; trên board trace bounded/GPIO và kiểm event counts; tách pair reads để tìm mixed generation.
- **ROOT CAUSE:** invariant nhiều bước không nằm trong synchronization protocol, không phải compiler “quên volatile”.
- **FIX:** atomic/critical snapshot theo port hoặc queue/owner protocol; giữ mask restoration đúng.
- **WRONG FIX:** thêm volatile rồi coi atomic, tắt mọi IRQ trong toàn processing, dùng blocking mutex trong ISR.
- **REGRESSION TEST:** event trước/trong/sau clear, bursts/full policy, max nesting/stack và API threshold trên target.



Measure event→entry latency separately handler duration; GPIO/trace timestamps with overhead. Stop CPU changes peripheral progress, bounded trace preferable timing evidence.

## 13. Liên hệ với bug/lab hiện có

[EMB-01](../labs/embedded_rtos/EMB-01.md), [EMB-02](../labs/embedded_rtos/EMB-02.md), [EMB-03](../labs/embedded_rtos/EMB-03.md), [EMB-04](../labs/embedded_rtos/EMB-04.md), [EMB-06](../labs/embedded_rtos/EMB-06.md), [EMB-09](../labs/embedded_rtos/EMB-09.md), [EMB-10](../labs/embedded_rtos/EMB-10.md).

## 14. Sai lầm thường gặp

Atomic scalar doesn't atomic RMW/pair; mask doesn't erase event; clear NVIC not peripheral ack; tiny ISR doesn't guarantee low latency if masked. priority number encoding library/implemented bits differs unshifted CMSIS vs register value.

## 15. Câu hỏi tự kiểm tra

1. Pending active? Đáp án: pending waiting, active servicing.
2. Volatile++ atomic? Đáp án: no.
3. Restore IRQ unconditionally enable safe? Đáp án: no, preserve prior mask.
4. Mask CPU excludes DMA? Đáp án: no.
5. Latency equals handler duration? Đáp án: no.
6. Inheritance mutex usable blocking ISR? Đáp án: not that context contract.

## 16. Nguồn

[CMSIS6 NVIC](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__NVIC__gr.html), [core registers](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/group__Core__Register__gr.html), [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [FreeRTOS11.1 M4F port](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/V11.1.0/portable/GCC/ARM_CM4F/port.c). Actual MCU implemented priority bits/vendor ack still verify.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
