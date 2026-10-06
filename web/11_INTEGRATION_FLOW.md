# Integration: wire meaning, intent và state owners

Phạm vi: browser ↔ ASP.NET8 ↔ MongoDB8 mental model; realtime protocol là contract abstract, không claim SignalR version API đã chạy.

## 1. Mục tiêu học

Theo intent xuyên UI/network/API/DB/response, phân biệt authoritative version và optimistic state; xử lý retry/rollback/realtime gaps không phá newer work.

## 2. Kiến thức tiên quyết

Toàn Web foundation tới [security](10_IDENTITY_SECURITY.md), đặc biệt [JS ownership](02_JS_RUNTIME.md), [API](08_API_CONTRACTS.md), [DB concurrency](15_DATABASE_TRANSACTIONS.md).

## 3. Vấn đề mà cơ chế này giải quyết

Mỗi layer giữ representation và deadline khác nhau. JSON parse success không đủ wire meaning; server data đúng chưa đủ UI apply đúng. Deployment partial và network partial failure làm owners phải nói rõ permission publish/recovery.

## 4. Khái niệm

Intent là operation người dùng muốn, attempt là một lần gửi, requestID là correlation cho attempt, idempotency key là identity intent theo scope. Entity version là authoritative ordering state, client generation là permission apply local, eventID là delivery dedup. Không dùng một ID cho mọi mục đích.

## 5. Thành phần bên trong

UI form/query cache giữ local/remote snapshots; serializer tạo bytes; proxy có body cap/cache/deadline; API parse/auth/business; DB giữ durable conditional state; parser response giữ shape; reducer/cache apply theo owner. Mỗi arrow có nghĩa/capacity/error contract; trace chỉ có ích khi IDs nối đúng entities/attempts.

## 6. Data representation

Wire DTO chốt casing/required/null/enum/precision/units/date/timezone. Date-only YYYY-MM-DD khác instant UTC/offset; JS Number safe range giới hạn integer money, currency không luôn hai decimals. Pagination pagebase/sort tuple/query encoding phải thống nhất. HTTP error body có thể HTML từ proxy, không JSON API envelope.

## 7. Control flow

```text
snapshot task42/version7 → edit intentK/generation2
→ serialize allowed fields/expectedVersion7 → request attemptR
→ authorize/filter → conditional write v7→v8
→ responseDTO v8/status → parse → apply nếu owner hợp lệ
→ render/commit
```

Timeout mở state 'unknown', reconcile theo key/status/query. Optimistic value chỉ prediction, không authoritative commit. A error tới sau B success không được rollback snapshot của A đè B. Refetch cũng request async phải guard generation.

## 8. Lifetime / ownership / state

Query cache owner giữ keys theo tenant/filter/sort; backend cache owner khác HTTP/router/client caches. Invalidate một layer không guarantee layer khác fresh. Refill race sau invalidation có thể publish old response; versioned cache protocol cần theo design.

Realtime subscription lifetime qua reconnect; events có order scope/version, duplicate window và recovery gap. Snapshot→subscribe gap cần replay cursor/watermark/subscription protocol atomic phù hợp server, không sleep. Logout/change user invalidate old responses và cached authority.

## 9. Invariants

Wire meaning giữ qua mọi boundary. Same intent retry không effect lặp. Stale completion/rollback không overwrite newer owner. Realtime duplicate không tính lại business event, older versions không regress state; gap phải observable/recovered. Upload content/limits/path được enforce nơi authoritative.

## 10. Ví dụ tối thiểu

Timeline **mô phỏng**: initial titleX/v7, A optimisticA, B optimisticB, Bsuccess v9, Aerror. Unconditional restoreX sai; rollback chỉ nếu state còn generationA, nếu không giữ B/refetch authorized latest. Status unknown sau timeout khác known business error.

Upload trace: browser gửi file giả→proxy413 HTML→client đọc status/type trước JSON. Realtime v3 trước v2: nếu payload snapshots có đủ state có thể ignore v2, nếu deltas phụ thuộc v2 phải detect gap/replay; không áp arrival order mù.

## 11. Failure modes

Wrong wire types/casing; stale session401 xóa newer login; retry mới key; stale cache backend/client; rollback old snapshot; lost realtime events; duplicate event counter; upload JSON parser che413. Fix layer đầu phá invariant và recovery policy, không refresh mọi thứ hoặc setTimeout reorder.

## 12. Debug / observability

Capture sanitized raw input/output và state version/generation sau mapper/apply; traceID nối API/DB. Hold backend fixture correct rồi force client completion orders để tách frontend race. Drop response sau commit; force reconnect missing range; test old/new builds; align upload limits/statuss giữa hops.

## 13. Liên hệ với bug/lab hiện có

[25 lab integration](../labs/integration/README.md), đặc biệt [INT-16](../labs/integration/INT-16.md), [INT-20](../labs/integration/INT-20.md), [INT-22](../labs/integration/INT-22.md), [INT-23](../labs/integration/INT-23.md), [INT-24](../labs/integration/INT-24.md), [INT-25](../labs/integration/INT-25.md).

## 14. Sai lầm thường gặp

DB đúng không UI đúng; reconnect không replay; refetch không race-free; UI disabled không server idempotency. Cursor/order event không global total order nếu contract chỉ per entity. Client cache invalidation không invalidate server automatically.

## 15. Câu hỏi tự kiểm tra

1. RequestID có thay key intent không? Đáp án: không, attempt khác intent.
2. Optimistic rollback A được làm gì sau B commit? Đáp án: không đè B, reconcile theo owner.
3. V3 trước v2 nên ignore luôn? Đáp án: tùy snapshot/delta semantics và gap policy.
4. Status413 HTML parse JSON có ý nghĩa gì? Đáp án: parser assumption sai, giữ original outcome.
5. FE/BE cùng DTO name có guarantee wire? Đáp án: raw fixtures mới kiểm representation.

## 16. Nguồn

[RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html), [Mongo8 atomicity](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/), [MDN Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date). Cơ chế từng boundary truy nguồn ở prerequisite chapters; timelines là reasoning của giáo trình.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
