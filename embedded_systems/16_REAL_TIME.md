# Real-time: deadline, response time và interference

Phạm vi: single CPU fixed-priority preemptive task model với assumptions nêu rõ. Timing là worked simulation, không WCET đã đo trên board; scheduler API bài [RTOS](09_RTOS_SCHEDULER.md).

## 1. Mục tiêu học

Tính release/response/deadline/utilization, phân tích worst-case interference/blocking, và biết đo gì trước claim real-time.

## 2. Kiến thức tiên quyết

[RTOS state](09_RTOS_SCHEDULER.md), [interrupt timing](06_INTERRUPTS.md), [memory/cache actors](07_DMA_OWNERSHIP.md).

## 3. Vấn đề mà cơ chế này giải quyết

Kết quả đúng nhưng quá trễ có thể vô dụng. Average throughput và CPU load không chứng minh every deadline; contention/jitter/path variations cần bounded model.

## 4. Khái niệm

Period T khoảng releases, deadline D là time result must finish từ release; WCET C upper bound execution under specified target/config/input. Response R includes execution+blocking+interference+release/dispatch delays relevant scope. Latency từ event tới chosen endpoint; jitter là variation của interval/latency/release. Hard deadline misses violate requirement, soft misses degrade utility; classification by product consequence.

## 5. Thành phần bên trong

Scheduler ưu tiên work ready; ISR/masks/nonpreemptive sections/locks và bus/cache stalls affect service. Priority inversion H chờ lock L giữ, M trì hoãn L; inheritance raises owner to permit release but not eliminates lock hold cost/deadlock. Starvation task continually eligible no service; bounded higher-priority jobs needed for guarantees.

## 6. Data representation

Task model tuple `(C,T,D,J,B,priority)` cùng interference sets, critical sections, arrival bounds. Utilization U=sum C/T riêng tasks, ISR/overheads add; U<1 necessary under ideal workload but not sufficient arbitrary priorities/blocking/deadlines. Deterministic là bounded/predictable behavior theo requirements, không merely identical results.

## 7. Control flow

```text
physical event → release (jitter) → ready queue → dispatch delay
→ execute / preempt / block → resume → finish
R = finish − release; deadline test R≤D
```

Relative delay after work làm release drift theo execution+delay. Absolute periodic release avoids that drift but late job still requires missed-period policy, không catch-up unbounded burst.

## 8. Lifetime / ownership / state

Job owns output/buffers từ release tới completion/handoff; outstanding jobs may overlap nếu R>T, resources/capacity must bound. Lock owner lifetime quyết blocking bound; external I/O no bounded response cannot simply insert into hard-deadline C. Watchdog progress criteria theo critical job completions/deadlines, không periodic timer-only feed.

## 9. Invariants

R worst upper bound≤D under explicit assumptions; execution/arrival/blocking bounded; overload/drop/degraded safe behavior explicit; WCET metric environment matches deployment. Deadline guarantee không từ scheduler name/API delay.

## 10. Ví dụ tối thiểu

**Worked model** two independent periodic tasks, single CPU fixed priority, D=T, no jitter/blocking/overheads: H C1/T4, L C2/T5, H higher. U=1/4+2/5=0.65. L recurrence R0=2, R1=2+ceil(2/4)×1=3, R2=2+ceil(3/4)×1=3≤5. H R1≤4. Add L blocking3: R0=5, R1=5+ceil(5/4)=7, R2=5+ceil(7/4)=7>5: misses dù original U thấp.

General recurrence `R_i=C_i+B_i+Σ ceil((R_i+J_j)/T_j)C_j` under suitable sporadic fixed-priority assumptions; includes higher-priority task jitter convention, ISR/overhead phải model thêm. Trong bài R và D đo từ lúc job eligible/release; nếu product deadline đo từ external event/arrival thì phải kiểm thêm own release jitter, ví dụ J_i+R_i≤D_event. Không bỏ J_i khỏi event-to-result bound. Không áp arbitrary SMP/self-suspending/cooperative models.

### Diễn giải fixed-point và priority inversion

Recurrence đếm số lần higher-priority jobs có thể chen vào cửa sổ dài R. Với H period4, cửa sổ R=3 chứa một H job; nếu blocking đẩy R tới5 thì cửa sổ chứa hai H jobs. Đó là lý do interference tăng theo các bước ceil, không chỉ tăng tuyến tính theo CPU utilization. Lặp tới fixed point; nếu bound vượt deadline thì model không chứng minh schedulable. Chỉ xét U=0.65 bỏ mất vị trí releases và blocking.

**Mô hình inversion**: L giữ mutex; H ready và block trên mutex; M ready, priority giữa H/L. Không inheritance, M có thể trì hoãn L nên H gián tiếp chờ M dù priority cao hơn. Có inheritance theo mutex protocol, L được nâng effective priority phù hợp để chạy tới release; H vẫn chịu thời gian critical section còn lại. Nếu L chờ I/O không bounded, nâng priority không tạo bound.

**Mô hình jitter**: sensor event tới ở e, task eligible ở e+J, chạy xong sau thêm R. Requirement event-to-result≤D cần J+R≤D. Đo chỉ start→finish bỏ ready wait, đo release→finish bỏ event→release. Chọn cùng endpoint/timebase trước so hai trace.

Một deadline test là lập luận có assumptions: task arrivals bounded, execution budget đáng tin, resource protocol có blocking bound và overhead accounted. Khi input gây allocation path mới hoặc IRQ burst ngoài arrival bound, phải cập nhật model; pass schedules cũ không chuyển thành proof model mới.

## 11. Failure modes

WCET estimate từ average, hidden malloc/I/O/unbounded loops, ISR bursts/long masks, inversion/lock holds, timer drift, high-rate tasks starvation, DMA contention/cache worst path. Removing logging can improve measured timing but no bound proof automatically.

## 12. Debug / observability

Measure release/ready/start/finish/preemption/block transitions same clock; GPIO/trace overhead bounded; worst input/path/cache/bus/nesting workload, compile flags/target/voltage-clock config record. WCET measurement maximum observed is lower evidence than rigorous upper bound; stress pass doesn't prove all deadlines. Latency distribution and deadline misses track separate throughput.

## 13. Liên hệ với bug/lab hiện có

[EMB-01](../labs/embedded_rtos/EMB-01.md), [EMB-19](../labs/embedded_rtos/EMB-19.md), [EMB-20](../labs/embedded_rtos/EMB-20.md), [EMB-26](../labs/embedded_rtos/EMB-26.md), [EMB-28](../labs/embedded_rtos/EMB-28.md), [EMB-29](../labs/embedded_rtos/EMB-29.md).

## 14. Sai lầm thường gặp

Scheduler presence≠real time; U low≠schedulable; deterministic container≠WCET full path; measured ISR duration≠event latency. Inheritance≠no inversion delay/deadlock. Faster mean≠deadline margin.

## 15. Câu hỏi tự kiểm tra

1. R gồm gì ngoài C? Đáp án:blocking/interference/jitter phù hợp scope.
2. Example L bound no blocking? Đáp án:3.
3. Add blocking3 misses? Đáp án:R7>D5.
4. Average measured max chứng minh WCET upper? Đáp án:not all paths proof.
5. Throughput adequate but deadline miss? Đáp án:possible bursts/priority waiting.

## 16. Nguồn

[Singh — Cutting-plane algorithms for preemptive uniprocessor real-time scheduling problems, v5 (2023)](https://arxiv.org/pdf/2210.11185), [Zephyr3.7 scheduling](https://docs.zephyrproject.org/3.7.0/kernel/services/scheduling/index.html). Bài nghiên cứu hỗ trợ mô hình fixed-point cho scheduling uniprocessor; ví dụ số là phép tính tự xây theo assumptions ở mục 10. Không suy ra chứng nhận timing trên board. DOI Liu/Layland, lecture PDF và thesis Emberson thử truy cập thất bại; không dùng chúng như nội dung đã đọc.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
