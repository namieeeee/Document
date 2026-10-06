# Outline — Database foundation: storage, relations và access paths

Mức của claim minh họa: **VERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Full scan/sort cho small limit; wrong compound prefix; too many indexes increase write cost; duplicate data drift; null/decimal serialization mismatch; missing unique constraint cho check-then-insert; offset drift sau concurrent insert. Sửa access path/model/constraint dựa workload, không index mọi fields.

Đặt câu hỏi: cơ chế trong [Database foundation: storage, relations và access paths](../../web/09_DATABASE_CONCURRENCY.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Query/filter/projection/order/limit
→ parse/plan candidate paths → choose path
→ index traversal hoặc scan → fetch/filter rows/docs
→ sort/aggregate nếu cần → return results
```

Index `(tenantId,createdAt,_id)` có thể hỗ trợ tenant equality và ordered pagination; scan descending/ascending/compound combinations theo engine. Limit5 vẫn có thể scan/sort rất nhiều nếu predicate/access path kém. Projection giảm payload, covered query có thể tránh fetch khi conditions đủ.

## 3. Demo chạy thật

Claim có phạm vi: Conditional single-document update và unique index giữ invariant dưới concurrent HTTP requests.

```text
python examples/MongoApi/verify.py --mongod <path-to-mongod>
```

Output quan sát trích nguyên từ [evidence](../../evidence/mongo-api/verification.log):

```text
database=document_fixture_753b4351f86942aa9787bbcbe2666fe8
EXPECTED FAIL broken stock invariant: successes=2 for available=1
round 1: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 2: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 3: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 4: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 5: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 6: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 7: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 8: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 9: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 10: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 11: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 12: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 13: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 14: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 15: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 16: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 17: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 18: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 19: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
round 20: conditional-update PASS; unique-index PASS; idempotent-replay PASS (8 concurrent + 1 retry + conflict)
PASS: 20/20 rounds for each of 3 database invariants

```

## 4. Cách nó hỏng và cách phát hiện

Full scan/sort cho small limit; wrong compound prefix; too many indexes increase write cost; duplicate data drift; null/decimal serialization mismatch; missing unique constraint cho check-then-insert; offset drift sau concurrent insert. Sửa access path/model/constraint dựa workload, không index mọi fields.

Explain trên synthetic representative cardinality/skew: compare returned, docs/rows examined, keys examined, sort spill, chosen index, latency và write overhead. Planner estimate khác actual execution stats; cold/warm caches khác. Khi query nhanh nhưng API chậm, đo pool queue/serialization/network thay tiếp thêm index.

## 5. Giới hạn trung thực

Standalone MongoDB, một API instance và 20 rounds; không chứng minh multi-document transaction, replica set, failover hoặc majority write concern. Docker Compose chưa chạy local.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[MongoDB8 compound indexes](https://www.mongodb.com/docs/v8.0/core/indexes/index-types/index-compound/), [BSON types](https://www.mongodb.com/docs/v8.0/reference/bson-types/), [explain](https://www.mongodb.com/docs/v8.0/reference/explain-results/), [unique indexes](https://www.mongodb.com/docs/v8.0/core/index-unique/), [PostgreSQL16 constraints](https://www.postgresql.org/docs/16/ddl-constraints.html), [joins](https://www.postgresql.org/docs/16/tutorial-join.html).

1. Vì sao index thêm có write cost? Đáp án: mỗi mutation duy trì index/storage.
2. FK giữ user quyền không? Đáp án: chỉ referential constraint.
3. Limit5 query vẫn chậm do đâu? Đáp án: nhiều scan/sort trước limit.
4. Embed giúp atomicity thế nào? Đáp án: đưa fields cùng document boundary.
5. Cursor order có tự snapshot dataset? Đáp án: không, need consistency policy.

[Index](../../00_INDEX.md) · [Content](../README.md).
