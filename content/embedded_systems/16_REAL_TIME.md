# Outline — Real-time: deadline, response time và interference

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

WCET estimate từ average, hidden malloc/I/O/unbounded loops, ISR bursts/long masks, inversion/lock holds, timer drift, high-rate tasks starvation, DMA contention/cache worst path. Removing logging can improve measured timing but no bound proof automatically.

Đặt câu hỏi: cơ chế trong [Real-time: deadline, response time và interference](../../embedded_systems/16_REAL_TIME.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
physical event → release (jitter) → ready queue → dispatch delay
→ execute / preempt / block → resume → finish
R = finish − release; deadline test R≤D
```

Relative delay after work làm release drift theo execution+delay. Absolute periodic release avoids that drift but late job still requires missed-period policy, không catch-up unbounded burst.

## 3. Demo chạy thật

Claim có phạm vi: Modulo elapsed model giữ timeout qua rollover với bound không mất nguyên chu kỳ; không phải native C tick.

```text
python examples/systems_models.py
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/systems.log):

```text
PASS tick rollover model with explicit bounded interval
```

## 4. Cách nó hỏng và cách phát hiện

WCET estimate từ average, hidden malloc/I/O/unbounded loops, ISR bursts/long masks, inversion/lock holds, timer drift, high-rate tasks starvation, DMA contention/cache worst path. Removing logging can improve measured timing but no bound proof automatically.

Measure release/ready/start/finish/preemption/block transitions same clock; GPIO/trace overhead bounded; worst input/path/cache/bus/nesting workload, compile flags/target/voltage-clock config record. WCET measurement maximum observed is lower evidence than rigorous upper bound; stress pass doesn't prove all deadlines. Latency distribution and deadline misses track separate throughput.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[Singh — Cutting-plane algorithms for preemptive uniprocessor real-time scheduling problems, v5 (2023)](https://arxiv.org/pdf/2210.11185), [Zephyr3.7 scheduling](https://docs.zephyrproject.org/3.7.0/kernel/services/scheduling/index.html). Bài nghiên cứu hỗ trợ mô hình fixed-point cho scheduling uniprocessor; ví dụ số là phép tính tự xây theo assumptions ở mục 10. Không suy ra chứng nhận timing trên board. DOI Liu/Layland, lecture PDF và thesis Emberson thử truy cập thất bại; không dùng chúng như nội dung đã đọc.

1. R gồm gì ngoài C? Đáp án:blocking/interference/jitter phù hợp scope.
2. Example L bound no blocking? Đáp án:3.
3. Add blocking3 misses? Đáp án:R7>D5.
4. Average measured max chứng minh WCET upper? Đáp án:not all paths proof.
5. Throughput adequate but deadline miss? Đáp án:possible bursts/priority waiting.

[Index](../../00_INDEX.md) · [Content](../README.md).
