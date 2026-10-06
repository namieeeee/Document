# Scientific debugging: chứng minh cơ chế phá invariant

Phạm vi: phương pháp chung Web/Embedded/OS. Reproduction/model measurement không được đổi thành production incident hoặc target proof.

## 1. Mục tiêu học

Từ symptom xây competing hypotheses/predictions, chọn discriminating experiment, tìm first broken invariant và tạo regression bảo vệ mechanism.

## 2. Kiến thức tiên quyết

Đã đọc ít nhất một cơ chế trong [Web](../web/01_HTTP_BROWSER.md) hoặc [Systems](../foundations/01_DIGITAL_REPRESENTATION.md). Chưa cần mọi tools; chọn cơ chế đang investigate.

## 3. Vấn đề mà cơ chế này giải quyết

Một symptom có nhiều causes, stack frame cuối thường chỉ hậu quả. Sửa theo correlation hoặc tăng timeout có thể che bug không giữ correctness. Debug cần inference từ evidence và phép thử bác bỏ alternative explanations.

## 4. Khái niệm

Observation là facts đo/nhìn, evidence là observation có context/source, hypothesis là explanation candidate, prediction là outcome expected nếu hypothesis đúng. Root cause là causal mechanism đầu phá invariant trong scope, không chỉ exception name. Fix thay guarantee; workaround đổi điều kiện để ít lộ.

## 5. Thành phần bên trong

```text
Observation → evidence → hypotheses → predictions
→ discriminating experiment → causal boundary/root cause
→ fix invariant → regression + scope/limitations
```

Mỗi vòng chọn một câu hỏi có thể answer. Reproduction giữ trigger/schedule nhưng không automatically explanation. Correlation A/B không chứng minh A causes B; controlled intervention với alternatives giúp phân biệt.

## 6. Data representation

Evidence record: exact build/version/config/tool/target/input, expected invariant vs actual, sequence/time/actor/entity/owner IDs, raw state before/after boundary, workload/frequency. Tách observed/predicted/inferred/unmeasured labels. Logs synthetic/redacted, no secrets; clock bases/precision khác phải reconcile.

## 7. Control flow

Ví dụ UI queryB hiệnA: cache hypothesis predicts raw responseB stale; mapper hypothesis predicts rawB correct mappedB wrong; race predicts both raw correct but applyA late. Thu Network raw+mapping/apply owner rồi force Bcomplete→Acomplete. Correct raw+lateapply supports race; evidence cache wrong bác bỏ race-only explanation.

DMA old bytes: immutable buffer test tách reuse; cache/RAM evidence tách coherence; waveform tách framing. Có thể multiple causes; một intervention fix symptom không đủ nếu đổi cả buffer và clock cùng lúc.

## 8. Lifetime / ownership / state

Measurement owner giữ fixture/artifacts/build relation; baseline trước change, trace buffers bounded, logs retention policy. Observer effect: breakpoint stops CPU while peripheral may continue/freeze by config, printf changes ISR time, sanitizer changes layout. Evidence late/corrupted trace phải verify before causal conclusion.

## 9. Invariants

Original trigger fail bản lỗi, same fixture pass fix với expected property độc lập implementation. One experiment isolates variable hoặc ghi confounds; negative/boundary/error/cancel/reversed order giữ invariant. Không claim tests/source/target run nếu tool không thật executed.

### Thiết kế phép thử có thể bác bỏ chính giả thuyết mình thích

Với symptom “query B nhưng UI hiện A”, đừng ghi hypothesis là “async bị lỗi”: câu đó không tạo prediction kiểm tra được. Tách ba mô hình:

| Giả thuyết | Prediction trước khi sửa | Phép thử phân biệt |
|---|---|---|
| Cache trả sai representation | Response cho B đã chứa dữ liệu A | Xem raw response và cache key |
| Mapper dùng field cũ | Raw B đúng, mapped state sai trước apply | Ghi input/output mapper cùng intent ID |
| Response A apply trễ | Raw A/B đều đúng; apply A sau B | Ép B hoàn tất trước A, ghi apply sequence |

Không phải mọi phép thử cần chạy thật trên production. Fixture có thể giữ payload, ép schedule bằng barrier và thay dependency delay. Sau mỗi thử, ghi observed outcome rồi cập nhật hypotheses; không sửa prediction sau khi thấy kết quả để luôn “đúng”.

Nếu tắt cache làm symptom biến mất, chưa loại được race: thao tác đó cũng đổi timing. Giữ schedule cố định và quan sát raw data để tách hai thay đổi. Khi nhiều causes cùng tồn tại, sửa từng invariant và thêm regression cho từng trigger, thay vì chọn một label root cause cho mọi lần thất bại.

## 10. Ví dụ tối thiểu

**Investigation model** stock1 two purchases succeed: H1 inventory request qty wrong predicts payload mismatch; H2 check-then-act predicts bothread1 then unconditionalwrite0. Force barrier both reads, record affected versions and successes. Conditional decrement eliminates second success while same payload/schedule; regression asserts totals/stock not function implementation string.

## 11. Failure modes

Confirmation bias only testing expected cause; fixing stack crash consumer while producer overflow persists; stale symbols/build; random stress no reproduction; instrument masks race; tests mirror code; swallowed failures improve metric; simultaneous config changes confound. Fix validation mechanism và evidence quality trước broad patch.

## 12. Debug / observability

Choose evidence layer via [Web tools](02_WEB_OBSERVABILITY.md) hoặc [systems](03_SYSTEMS_OBSERVABILITY.md). Measure first stage where expected/actual diverge, keep higher/lower raw data. If no tool, write predicted trace and missing evidence, don't fabricate outputs. Performance experiments same workload/build/hardware, CPU/wall/tail latency/allocations separate.

### Regression phải làm bản lỗi thất bại vì đúng lý do

Một regression cho stale response cần hai requests và reversed completion order; chỉ test một response không kích hoạt interleaving. Assertion là “state thuộc intent đang active”, không là “code có AbortController”. Cancellation có thể tới sau response, nên guard owner/version vẫn cần theo contract.

Một regression cho idempotency cần cùng key/cùng payload, cùng key/khác payload, retry sau unknown outcome và concurrency. Nếu test chỉ mock dependency để trả cùng object, nó có thể xanh dù durable dedup chưa tồn tại.

Đánh giá evidence theo phạm vi: deterministic host model chứng minh một schedule có thể phá invariant; sanitizer thấy một access sai trong run; trace board ghi một timing đã quan sát. Không chuyển bất kỳ bằng chứng hữu hạn nào thành bảo đảm mọi schedules hoặc mọi paths.

## 13. Liên hệ với bug/lab hiện có

[INT-20](../labs/integration/INT-20.md), [FE-05](../labs/frontend/FE-05.md), [BE-15](../labs/backend/BE-15.md), [EMB-13](../labs/embedded_rtos/EMB-13.md), [OS-09](../labs/os/OS-09.md). [Map](../BUG_THEORY_MAP.md) nối all121 invariants; no extra bug count.

## 14. Sai lầm thường gặp

Symptom≠root cause; correlation≠cause; reproduction≠explanation; symptom fix≠invariant fix. Hundred pass runs not mathematical race proof. Model proof scope doesn't include hardware/cache/electrical realities absent model. Diagnostic workaround may useful experiment, not permanent fix guarantee.

## 15. Câu hỏi tự kiểm tra

1. Raw responseB correct but finalA suggests what next evidence? Đáp án:apply IDs/order/state mapping.
2. Bug gone under breakpoint proof fixed? Đáp án:no observer effect.
3. Baseline bad doesn't fail regression? Đáp án:test lacks trigger/property.
4. Same addresses proof ownership? Đáp án:no generation/lifetime/access protocol.
5. Faster mean but more deadline misses fixed? Đáp án:metric/invariant wrong target.
6. Compiler pass proves DMA coherence? Đáp án:no.

## 16. Nguồn

Nguồn cơ chế theo chapters, phương pháp này là reasoning framework của giáo trình. [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) cho observation commands; [Clang sanitizer docs](https://clang.llvm.org/docs/AddressSanitizer.html) cho scope/limits; [Chrome Performance](https://developer.chrome.com/docs/devtools/performance) cho measurement. Không gán một postmortem/standard chưa đọc.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
