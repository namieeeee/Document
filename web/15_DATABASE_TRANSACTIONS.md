# Concurrency và consistency: invariant nằm ở đâu?

Phạm vi: MongoDB8.0 và PostgreSQL16, semantics vendor riêng. Examples là schedules/pseudocode, không concurrent database run.

## 1. Mục tiêu học

Vẽ lost-update/check-then-act/write-skew schedules; chọn conditional mutation, locks hoặc transaction theo invariant; giải thích idempotency và crash window. Không dùng từ 'transaction' như blanket guarantee.

## 2. Kiến thức tiên quyết

[DB foundation](09_DATABASE_CONCURRENCY.md), [HTTP retry](12_HTTP_SEMANTICS.md), [API versions](08_API_CONTRACTS.md). Atomic CPU scalar khác database transaction boundary.

## 3. Vấn đề mà cơ chế này giải quyết

Concurrent clients cùng đọc một state rồi quyết định độc lập. Nếu condition và effect tách ra, từng request đúng riêng nhưng kết quả chung phá invariant. Replicas, retries và crash làm process-local lock không đủ; storage boundary phải là nơi quyết định authoritative mutation.

## 4. Khái niệm

Race condition là outcome phụ thuộc interleaving. Lost update: A/B đọc v7, A ghi B1, B ghi B2 vô điều kiện xóa A. Check-then-act: hai caller thấy stock1 và cùng bán. Atomicity là all-or-nothing cho boundary operation/transaction; isolation là observations/interleavings được cho phép; consistency có thể chỉ domain invariants hoặc replica/read guarantees, cần nói nghĩa cụ thể; durability là commit survive failures theo config.

## 5. Thành phần bên trong

Optimistic concurrency kiểm expected version cùng write, conflict khi state đổi. Pessimistic locking giữ lock trước read/decision/write theo transaction engine; lock thời gian dài tăng blocking/deadlock. Unique constraint atomically chặn duplicate keys, không tự giữ every business invariant.

MVCC cho reader nhìn snapshots/versions; snapshot isolation không tự serializable. Write-skew: hai on-call doctors đều thấy hai người trực, mỗi transaction bỏ một row khác nhau; mỗi write riêng không conflict nhưng cuối không ai trực. Cần transaction isolation/protected common decision boundary phù hợp.

## 6. Data representation

State gồm durable records/versions, uncommitted writes/snapshots, locks/wait graph và dedup records. Mongo readConcern/writeConcern và transaction concerns ảnh hưởng reads/durability; không equate majority write với mọi latest read. PostgreSQL16 Read Committed statement snapshots; Repeatable Read stable transaction snapshot nhưng serialization anomalies có thể còn; Serializable có thể abort để giữ serial-equivalent committed outcomes.

Idempotency record `(tenant,user,key,payloadHash,state,outcome)` có claim/executing/completed/failed/recovery states. Payload canonicalization/version là contract, không tự hash JSON string tùy order.

## 7. Control flow

```text
A read stock1    B read stock1
A decides yes   B decides yes
A writes0       B writes0  → hai successes, chỉ một decrement observed
```

Sửa một document: filter stock>=qty và atomic decrement; matched count là quyết định success. Version edit: filter id+expectedVersion, set fields và increment version; zero affected là conflict/notfound/access outcome phải classify theo policy.

Multi-document stock+order: begin supported transaction→conditional decrement→insert order→commit; fail abort. Không external payment API nằm trong DB atomicity. Outbox ghi event cùng transaction rồi publisher retry; consumer idempotency xử lý repeated delivery.

## 8. Lifetime / ownership / state

Locks/snapshots giữ tới transaction end; giữ lock qua network call làm uncontrolled lifetime. Error/cancel path phải abort/release; commit reply lost có thể unknown dù server commit. Retry whole transaction khi known transient abort theo driver/vendor rules, không lặp external side effect tùy ý.

Dedup retention phải dài hơn retry window/business semantics; expiry khiến cùng key có thể lại được coi mới. Crash after external effect before saving outcome cần provider idempotency/reconciliation; memory dictionary hoặc pending lease không đóng gap. Expired lease cũng cần fencing nếu old owner còn chạy.

## 9. Invariants

Invariant như stock>=0 và successes<=initial stock phải bao condition+write. Stale expected version không overwrite mới. Same intent effect at most once trong scoped dedup guarantees; completed reply replay không bypass current resource authorization policy. Cross-document constraints có transaction/model boundary thực, không annotations.

### Từ schedule tới isolation cần chọn

**Mô hình hai bác sĩ A/B**, invariant: ít nhất một người trực. Hai transactions cùng đọc A=true,B=true; T1 tắt A, T2 tắt B. Chúng ghi hai records khác nhau nên kiểm version riêng từng record chưa phát hiện việc read set chung đã lỗi thời. Nếu isolation cho phép schedule này, cả hai commit và invariant sai: đây là write skew.

| Cách giữ invariant | Cơ chế | Điều cần cân nhắc |
|---|---|---|
| Serialize qua guard record/lock | Hai operations cạnh tranh cùng boundary | Lock order và contention |
| Serializable transaction | Database ngăn/chấm dứt schedule không serializable | Retry aborted transaction |
| Remodel thành một aggregate | Invariant trong atomic boundary phù hợp | Aggregate size và contention |
| Conditional record writes riêng | Phát hiện lost update cùng record | Chưa đủ cho cross-record invariant |

Transaction không giữ locks trên HTTP payment service hoặc biến memory ở server khác. Trước khi chọn “bọc transaction”, vẽ toàn bộ read/write set, invariant và external side effects. PostgreSQL16 isolation và MongoDB8 read/write concerns có semantics riêng; không dùng tên “snapshot” như bảo đảm serializable chung.

## 10. Ví dụ tối thiểu

Pseudocode, **kết quả dự đoán**:

```text
purchase(qty=1):
  affected = updateOne(id=P AND stock>=1, stock-=1)
  if affected==1: success else soldOut
```

Hai contenders stock1: chỉ một match thành công theo atomic update guarantee. SQL16 analogue `UPDATE stock SET n=n-1 WHERE id=:p AND n>=1`, kiểm rows affected; bind parameters. Nếu order record cần cùng atomic effect, include transaction hoặc model khác.

Idempotency schedule: A/B cùng key claim bằng unique constraint; winner effect, loser observe/wait/replay. Không claim bằng `if not exists then insert` mà không atomic uniqueness.

## 11. Failure modes

Lost updates, write skew, deadlock, unknown commit, duplicate on retry, stale replica read, dedup claim/result gap, lease old owner writes after takeover. Fix gắn đúng invariant boundary; generic retry có thể amplify bug. Transaction abort là expected conflict/failure path, không mọi error là business invalid.

### Crash windows cho dedup và outbox

Một intent cần durable key, scope và payload fingerprint. “Ghi key → gọi side effect → ghi result” có crash window giữa gọi side effect và ghi result; retry không biết side effect đã xảy ra. Nếu effect và dedup result nằm trong cùng DB transaction, có thể commit cùng boundary. Nếu effect là dịch vụ ngoài, cần provider idempotency/reconciliation hoặc protocol nhiều bước, không claim exactly-once toàn hệ thống.

Outbox lưu domain mutation và pending message cùng transaction. Relay có thể gửi message rồi crash trước mark delivered; message được gửi lại. Consumer phải dedup hoặc áp version/invariant an toàn. Outbox giải atomicity giữa state và ý định publish, không biến delivery thành chỉ-một-lần.

Để debug, đặt crash injection trước/ sau commit, sau publish và trước acknowledgement trong synthetic model. Quan sát durable rows/messages và business totals; số HTTP200 không phải bằng chứng invariant.

## 12. Debug / observability

Force both reads before writes bằng barrier; record versions/affected count/commit outcome và business totals. Vẽ wait graph cho locks, distinguish lock wait vs query scan. Test response loss trước/sau commit, concurrent same key/khác payload, crash giữa claim/effect/result và two replicas. Review conditions atomic thay chỉ assert HTTP200. Explain performance không proof consistency.

## 13. Liên hệ với bug/lab hiện có

[BE-15](../labs/backend/BE-15.md), [BE-16](../labs/backend/BE-16.md), [BE-13](../labs/backend/BE-13.md), [BE-14](../labs/backend/BE-14.md), [INT-20](../labs/integration/INT-20.md). Existing CoreModels barrier/dedup checks là algorithm models, không Mongo deployment guarantees.

## 14. Sai lầm thường gặp

Read rồi write trong cùng service method không atomic. Mutex process-local không đồng bộ API replicas. Snapshot không serializable blanket; serializable không never abort. HTTP idempotent PUT không giữ concurrent edits khác intents. Atomicity và durability/visibility là lớp khác nhau.

## 15. Câu hỏi tự kiểm tra

1. Vì sao stock cuối0 vẫn oversold? Đáp án: hai successes sau cùng read1.
2. Condition cần đặt ở đâu? Đáp án: cùng authoritative write.
3. Write-skew có cần cùng row không? Đáp án: không.
4. Transaction bao external payment không? Đáp án: DB không tự atomic với service ngoài.
5. Commit timeout có safe retry mới intent? Đáp án: không, reconcile/dedup.
6. Unique key giữ same key/khác payload thế nào? Đáp án: key scope/hash conflict contract.

## 16. Nguồn

[MongoDB8 atomicity](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/), [transactions](https://www.mongodb.com/docs/v8.0/core/transactions/), [snapshot read concern](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/), [PostgreSQL16 isolation](https://www.postgresql.org/docs/16/transaction-iso.html), [explicit locking](https://www.postgresql.org/docs/16/explicit-locking.html), [retryable writes Mongo8](https://www.mongodb.com/docs/v8.0/core/retryable-writes/). Chưa dùng failed fetch làm verification; retry source trong REFERENCES.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
