# Outline — Scientific debugging: chứng minh cơ chế phá invariant

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Confirmation bias only testing expected cause; fixing stack crash consumer while producer overflow persists; stale symbols/build; random stress no reproduction; instrument masks race; tests mirror code; swallowed failures improve metric; simultaneous config changes confound. Fix validation mechanism và evidence quality trước broad patch.

Đặt câu hỏi: cơ chế trong [Scientific debugging: chứng minh cơ chế phá invariant](../../debug/01_EVIDENCE_METHOD.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Ví dụ UI queryB hiệnA: cache hypothesis predicts raw responseB stale; mapper hypothesis predicts rawB correct mappedB wrong; race predicts both raw correct but applyA late. Thu Network raw+mapping/apply owner rồi force Bcomplete→Acomplete. Correct raw+lateapply supports race; evidence cache wrong bác bỏ race-only explanation.

DMA old bytes: immutable buffer test tách reuse; cache/RAM evidence tách coherence; waveform tách framing. Có thể multiple causes; một intervention fix symptom không đủ nếu đổi cả buffer và clock cùng lúc.

## 3. Demo chạy thật

Claim có phạm vi: Original trigger fail bản lỗi, same fixture pass fix với expected property độc lập implementation. One experiment isolates variable hoặc ghi confounds; negative/boundary/error/cancel/reversed order giữ invariant. Không claim tests/source/target run nếu tool không thật executed.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../debug/01_EVIDENCE_METHOD.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Confirmation bias only testing expected cause; fixing stack crash consumer while producer overflow persists; stale symbols/build; random stress no reproduction; instrument masks race; tests mirror code; swallowed failures improve metric; simultaneous config changes confound. Fix validation mechanism và evidence quality trước broad patch.

Choose evidence layer via [Web tools](../../debug/02_WEB_OBSERVABILITY.md) hoặc [systems](../../debug/03_SYSTEMS_OBSERVABILITY.md). Measure first stage where expected/actual diverge, keep higher/lower raw data. If no tool, write predicted trace and missing evidence, don't fabricate outputs. Performance experiments same workload/build/hardware, CPU/wall/tail latency/allocations separate.

### Regression phải làm bản lỗi thất bại vì đúng lý do

Một regression cho stale response cần hai requests và reversed completion order; chỉ test một response không kích hoạt interleaving. Assertion là “state thuộc intent đang active”, không là “code có AbortController”. Cancellation có thể tới sau response, nên guard owner/version vẫn cần theo contract.

Một regression cho idempotency cần cùng key/cùng payload, cùng key/khác payload, retry sau unknown outcome và concurrency. Nếu test chỉ mock dependency để trả cùng object, nó có thể xanh dù durable dedup chưa tồn tại.

Đánh giá evidence theo phạm vi: deterministic host model chứng minh một schedule có thể phá invariant; sanitizer thấy một access sai trong run; trace board ghi một timing đã quan sát. Không chuyển bất kỳ bằng chứng hữu hạn nào thành bảo đảm mọi schedules hoặc mọi paths.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

Nguồn cơ chế theo chapters, phương pháp này là reasoning framework của giáo trình. [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) cho observation commands; [Clang sanitizer docs](https://clang.llvm.org/docs/AddressSanitizer.html) cho scope/limits; [Chrome Performance](https://developer.chrome.com/docs/devtools/performance) cho measurement. Không gán một postmortem/standard chưa đọc.

1. Raw responseB correct but finalA suggests what next evidence? Đáp án:apply IDs/order/state mapping.
2. Bug gone under breakpoint proof fixed? Đáp án:no observer effect.
3. Baseline bad doesn't fail regression? Đáp án:test lacks trigger/property.
4. Same addresses proof ownership? Đáp án:no generation/lifetime/access protocol.
5. Faster mean but more deadline misses fixed? Đáp án:metric/invariant wrong target.
6. Compiler pass proves DMA coherence? Đáp án:no.

[Index](../../00_INDEX.md) · [Content](../README.md).
