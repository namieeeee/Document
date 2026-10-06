# Outline — API: resource, command, validation và version

Mức của claim minh họa: **VERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Mass assignment khi bind entity; null clear không chủ ý; offset page drifting khi data đổi; status200 error che monitoring; incompatible rollout; client timeout retry mới key; version conflict bị retry stale body mãi. Fix contracts/whitelist/preconditions/migration, không string coercion để che mismatched shape.

Đặt câu hỏi: cơ chế trong [API: resource, command, validation và version](../../web/08_API_CONTRACTS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Request bytes → syntax parse → DTO semantic checks
→ principal/resource authorization → business transition
→ atomic storage condition → response DTO/error → client parser
```

Resource policy có thể load object trước authorize nhưng mutation sau authorize. PUT replacement và PATCH operation khác; ordinary partial object không tự định nghĩa PATCH semantics. 201/202/204/error bodies theo contract; no-content phải có parser path riêng.

## 3. Demo chạy thật

Claim có phạm vi: Cùng idempotency key/payload trả một orderId; payload khác bị 409 trong HTTP/MongoDB fixture.

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

Mass assignment khi bind entity; null clear không chủ ý; offset page drifting khi data đổi; status200 error che monitoring; incompatible rollout; client timeout retry mới key; version conflict bị retry stale body mãi. Fix contracts/whitelist/preconditions/migration, không string coercion để che mismatched shape.

Capture raw request/response/status/headers và builds trước mapper. Contract fixtures success/no-content/validation/forbidden/conflict dùng cả old/new consumers. For authorization negative case kiểm data và side effect, không chỉ status. Concurrent version barrier và affected count cho evidence state mutation.

## 5. Giới hạn trung thực

Standalone MongoDB, một API instance và 20 rounds; không chứng minh multi-document transaction, replica set, failover hoặc majority write concern. Docker Compose chưa chạy local.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html), [Microsoft Web API design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design), [OWASP API2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). Examples là curriculum, source/OpenAPI thực phải override docs cũ.

1. Null và absent có cùng meaning PATCH không? Đáp án: phụ thuộc format, phải explicit.
2. Valid DTO có thể business invalid không? Đáp án: có.
3. User role valid có đủ edit mọi ID? Đáp án: object/field quyền riêng.
4. 202 có chứng minh durable job completed? Đáp án: không.
5. Version7 client edit khi current8 nên làm gì? Đáp án: conflict/reconcile theo contract, không unconditional overwrite.

[Index](../../00_INDEX.md) · [Content](../README.md).
