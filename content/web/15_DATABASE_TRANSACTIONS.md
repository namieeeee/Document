# Outline — Concurrency và consistency: invariant nằm ở đâu?

Mức của claim minh họa: **VERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Lost updates, write skew, deadlock, unknown commit, duplicate on retry, stale replica read, dedup claim/result gap, lease old owner writes after takeover. Fix gắn đúng invariant boundary; generic retry có thể amplify bug. Transaction abort là expected conflict/failure path, không mọi error là business invalid.

Đặt câu hỏi: cơ chế trong [Concurrency và consistency: invariant nằm ở đâu?](../../web/15_DATABASE_TRANSACTIONS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
A read stock1    B read stock1
A decides yes   B decides yes
A writes0       B writes0  → hai successes, chỉ một decrement observed
```

Sửa một document: filter stock>=qty và atomic decrement; matched count là quyết định success. Version edit: filter id+expectedVersion, set fields và increment version; zero affected là conflict/notfound/access outcome phải classify theo policy.

Multi-document stock+order: begin supported transaction→conditional decrement→insert order→commit; fail abort. Không external payment API nằm trong DB atomicity. Outbox ghi event cùng transaction rồi publisher retry; consumer idempotency xử lý repeated delivery.

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

Lost updates, write skew, deadlock, unknown commit, duplicate on retry, stale replica read, dedup claim/result gap, lease old owner writes after takeover. Fix gắn đúng invariant boundary; generic retry có thể amplify bug. Transaction abort là expected conflict/failure path, không mọi error là business invalid.

### Crash windows cho dedup và outbox

Một intent cần durable key, scope và payload fingerprint. “Ghi key → gọi side effect → ghi result” có crash window giữa gọi side effect và ghi result; retry không biết side effect đã xảy ra. Nếu effect và dedup result nằm trong cùng DB transaction, có thể commit cùng boundary. Nếu effect là dịch vụ ngoài, cần provider idempotency/reconciliation hoặc protocol nhiều bước, không claim exactly-once toàn hệ thống.

Outbox lưu domain mutation và pending message cùng transaction. Relay có thể gửi message rồi crash trước mark delivered; message được gửi lại. Consumer phải dedup hoặc áp version/invariant an toàn. Outbox giải atomicity giữa state và ý định publish, không biến delivery thành chỉ-một-lần.

Để debug, đặt crash injection trước/ sau commit, sau publish và trước acknowledgement trong synthetic model. Quan sát durable rows/messages và business totals; số HTTP200 không phải bằng chứng invariant.

Force both reads before writes bằng barrier; record versions/affected count/commit outcome và business totals. Vẽ wait graph cho locks, distinguish lock wait vs query scan. Test response loss trước/sau commit, concurrent same key/khác payload, crash giữa claim/effect/result và two replicas. Review conditions atomic thay chỉ assert HTTP200. Explain performance không proof consistency.

## 5. Giới hạn trung thực

Standalone MongoDB, một API instance và 20 rounds; không chứng minh multi-document transaction, replica set, failover hoặc majority write concern. Docker Compose chưa chạy local.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[MongoDB8 atomicity](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/), [transactions](https://www.mongodb.com/docs/v8.0/core/transactions/), [snapshot read concern](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/), [PostgreSQL16 isolation](https://www.postgresql.org/docs/16/transaction-iso.html), [explicit locking](https://www.postgresql.org/docs/16/explicit-locking.html), [retryable writes Mongo8](https://www.mongodb.com/docs/v8.0/core/retryable-writes/). Chưa dùng failed fetch làm verification; retry source trong REFERENCES.

1. Vì sao stock cuối0 vẫn oversold? Đáp án: hai successes sau cùng read1.
2. Condition cần đặt ở đâu? Đáp án: cùng authoritative write.
3. Write-skew có cần cùng row không? Đáp án: không.
4. Transaction bao external payment không? Đáp án: DB không tự atomic với service ngoài.
5. Commit timeout có safe retry mới intent? Đáp án: không, reconcile/dedup.
6. Unique key giữ same key/khác payload thế nào? Đáp án: key scope/hash conflict contract.

[Index](../../00_INDEX.md) · [Content](../README.md).
