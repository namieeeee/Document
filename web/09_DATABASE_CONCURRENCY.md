# Database foundation: storage, relations và access paths

Phạm vi: nền database chung; MongoDB8.0 và PostgreSQL16 dùng như hai implementations riêng. Transaction semantics ở [bài tiếp](15_DATABASE_TRANSACTIONS.md).

## 1. Mục tiêu học

Vẽ data→record/document→storage→access path→query→transaction, giải thích keys/constraints/joins và đọc query plan thay đoán từ query string.

## 2. Kiến thức tiên quyết

[API models](08_API_CONTRACTS.md), representation values; chưa cần database production. Mọi ví dụ synthetic/pseudocode.

## 3. Vấn đề mà cơ chế này giải quyết

Persistent storage phải tìm dữ liệu, bảo vệ constraints và duy trì state qua operations. Duyệt mọi records đơn giản nhưng tốn work; index đổi read cost thành storage/write overhead. Model dữ liệu quyết định atomic boundary và query patterns.

## 4. Khái niệm

Record là đơn vị dữ liệu logic; storage engine tổ chức pages/blocks và versions/buffers theo implementation. Query mô tả selection/projection/order, planner chọn access path, executor thực hiện. Transaction nhóm operations theo guarantees của engine/config. Data schema vẫn tồn tại ở application kể cả document store linh hoạt.

## 5. Thành phần bên trong

Relational table có rows với columns/domain; primary key định danh, unique constraint giữ uniqueness, foreign key giữ referential relation. Join ghép rows theo relation/predicate, không tự tenant authorization. Normalize giảm duplication nhưng joins có cost; denormalize đổi sang consistency của duplicated state.

Mongo collection chứa BSON documents; BSON có typed values/embedded documents/arrays, không chỉ JSON text. ObjectId/string/date/decimal có representation riêng; wire serialization phải thống nhất. Embed có thể đưa invariant về một document atomic; references phù hợp independent lifetime nhưng multi-document work cần coordination.

## 6. Data representation

Index giữ ordered/search structure keys→record locations/version references theo engine. Compound keys có lexicographic order; equality prefix rồi range/sort affects usefulness, không rule index luôn nhanh. Unique key scope cần tenant nếu uniqueness per tenant. Sparse/partial/null/missing/sharding rules tùy Mongo config; không suy unique field universal constraint mọi missing docs.

Storage/cache buffer khác application cache; planner caches plan, dữ liệu changes ảnh hưởng estimates. Explain shape có thể thay qua version/engine; đọc semantic metric examined/returned thay assert một stage name universal.

## 7. Control flow

```text
Query/filter/projection/order/limit
→ parse/plan candidate paths → choose path
→ index traversal hoặc scan → fetch/filter rows/docs
→ sort/aggregate nếu cần → return results
```

Index `(tenantId,createdAt,_id)` có thể hỗ trợ tenant equality và ordered pagination; scan descending/ascending/compound combinations theo engine. Limit5 vẫn có thể scan/sort rất nhiều nếu predicate/access path kém. Projection giảm payload, covered query có thể tránh fetch khi conditions đủ.

## 8. Lifetime / ownership / state

Connection pool owns connections, per-operation cursor/transaction owns server resources tới close/exhaust/commit/abort. Long cursor/transaction có thể giữ snapshots/locks/versions, tăng resource costs. Index updated cùng writes theo engine, nên thêm index làm writes chậm và dùng RAM/disk. Schema changes/migrations có lifecycle riêng; curriculum không chạy migrations.

## 9. Invariants

Keys/constraints phản ánh invariant đúng scope; query result stable order với total tie-breaker; work/result size capped phù hợp SLA. Không dùng field ID như quyền. Data access và serialization không đổi units/null semantics. Atomic document update chỉ giữ invariant nằm trong boundary đó.

## 10. Ví dụ tối thiểu

Pseudocode Mongo8, **chưa chạy DB**:

```javascript
// Fixture: tasks với tenantId, createdAt, _id
find({ tenantId: 'T' })
  .sort({ createdAt: -1, _id: -1 })
  .limit(5)
  .project({ title: 1, createdAt: 1 });
// Candidate index: { tenantId:1, createdAt:-1, _id:-1 }
```

Relational model: Tasks(owner_id FK Users.id, id PK, title, version). Join Users/Tasks có thể lấy display name, nhưng query vẫn phải constrain allowed owner/tenant. Không copy syntax pseudocode này như native driver API executable.

## 11. Failure modes

Full scan/sort cho small limit; wrong compound prefix; too many indexes increase write cost; duplicate data drift; null/decimal serialization mismatch; missing unique constraint cho check-then-insert; offset drift sau concurrent insert. Sửa access path/model/constraint dựa workload, không index mọi fields.

## 12. Debug / observability

Explain trên synthetic representative cardinality/skew: compare returned, docs/rows examined, keys examined, sort spill, chosen index, latency và write overhead. Planner estimate khác actual execution stats; cold/warm caches khác. Khi query nhanh nhưng API chậm, đo pool queue/serialization/network thay tiếp thêm index.

## 13. Liên hệ với bug/lab hiện có

[BE-17](../labs/backend/BE-17.md) stable pagination; [BE-18](../labs/backend/BE-18.md) access path; [BE-19](../labs/backend/BE-19.md) index order; [BE-20](../labs/backend/BE-20.md) bounded work. [DB transactions](15_DATABASE_TRANSACTIONS.md) giữ BE15/16 invariants.

## 14. Sai lầm thường gặp

Document database không nghĩa không schema/transactions; relational constraint không authorization. Index used không nghĩa efficient; low examined/returned ratio không full performance proof nếu I/O/pool bottleneck khác. SQL isolation level names không áp nguyên Mongo concerns. Limit không bounded scan guarantee.

## 15. Câu hỏi tự kiểm tra

1. Vì sao index thêm có write cost? Đáp án: mỗi mutation duy trì index/storage.
2. FK giữ user quyền không? Đáp án: chỉ referential constraint.
3. Limit5 query vẫn chậm do đâu? Đáp án: nhiều scan/sort trước limit.
4. Embed giúp atomicity thế nào? Đáp án: đưa fields cùng document boundary.
5. Cursor order có tự snapshot dataset? Đáp án: không, need consistency policy.

## 16. Nguồn

[MongoDB8 compound indexes](https://www.mongodb.com/docs/v8.0/core/indexes/index-types/index-compound/), [BSON types](https://www.mongodb.com/docs/v8.0/reference/bson-types/), [explain](https://www.mongodb.com/docs/v8.0/reference/explain-results/), [unique indexes](https://www.mongodb.com/docs/v8.0/core/index-unique/), [PostgreSQL16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html), [joins](https://www.postgresql.org/docs/16/tutorial-join.html).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
