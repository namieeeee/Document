# Outline — Integration: wire meaning, intent và state owners

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Wrong wire types/casing; stale session401 xóa newer login; retry mới key; stale cache backend/client; rollback old snapshot; lost realtime events; duplicate event counter; upload JSON parser che413. Fix layer đầu phá invariant và recovery policy, không refresh mọi thứ hoặc setTimeout reorder.

Đặt câu hỏi: cơ chế trong [Integration: wire meaning, intent và state owners](../../web/11_INTEGRATION_FLOW.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
snapshot task42/version7 → edit intentK/generation2
→ serialize allowed fields/expectedVersion7 → request attemptR
→ authorize/filter → conditional write v7→v8
→ responseDTO v8/status → parse → apply nếu owner hợp lệ
→ render/commit
```

Timeout mở state 'unknown', reconcile theo key/status/query. Optimistic value chỉ prediction, không authoritative commit. A error tới sau B success không được rollback snapshot của A đè B. Refetch cũng request async phải guard generation.

## 3. Demo chạy thật

Claim có phạm vi: Rollback chỉ thuộc version đang sở hữu optimistic state trong host fixture.

```text
node examples/web_models.mjs
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/web.log):

```text
PASS rollback ownership
```

## 4. Cách nó hỏng và cách phát hiện

Wrong wire types/casing; stale session401 xóa newer login; retry mới key; stale cache backend/client; rollback old snapshot; lost realtime events; duplicate event counter; upload JSON parser che413. Fix layer đầu phá invariant và recovery policy, không refresh mọi thứ hoặc setTimeout reorder.

Capture sanitized raw input/output và state version/generation sau mapper/apply; traceID nối API/DB. Hold backend fixture correct rồi force client completion orders để tách frontend race. Drop response sau commit; force reconnect missing range; test old/new builds; align upload limits/statuss giữa hops.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html), [Mongo8 atomicity](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/), [MDN Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date). Cơ chế từng boundary truy nguồn ở prerequisite chapters; timelines là reasoning của giáo trình.

1. RequestID có thay key intent không? Đáp án: không, attempt khác intent.
2. Optimistic rollback A được làm gì sau B commit? Đáp án: không đè B, reconcile theo owner.
3. V3 trước v2 nên ignore luôn? Đáp án: tùy snapshot/delta semantics và gap policy.
4. Status413 HTML parse JSON có ý nghĩa gì? Đáp án: parser assumption sai, giữ original outcome.
5. FE/BE cùng DTO name có guarantee wire? Đáp án: raw fixtures mới kiểm representation.

[Index](../../00_INDEX.md) · [Content](../README.md).
