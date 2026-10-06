# API: resource, command, validation và version

Phạm vi: HTTP APIs, examples ASP.NET8; contract lựa chọn application được phân biệt với RFC semantics.

## 1. Mục tiêu học

Thiết kế operation từ invariant tới request/response/error, phân biệt bốn lớp validation và vẽ compatibility khi clients/server deploy khác lúc.

## 2. Kiến thức tiên quyết

[HTTP semantics](12_HTTP_SEMANTICS.md), [ASP.NET lifecycle](07_ASPNET_LIFECYCLE.md). Học bài này để hiểu resource/command/contract trước database. Sau [DB foundation](09_DATABASE_CONCURRENCY.md), học tiếp [DB transactions](15_DATABASE_TRANSACTIONS.md) để triển khai invariant concurrent; hai bài DB là phần nối tiếp, không tiên quyết cho lượt đọc API đầu.

## 3. Vấn đề mà cơ chế này giải quyết

API tồn tại qua nhiều clients/releases; bind class và serialize JSON chưa đủ tạo hợp đồng. Phải định nghĩa meaning, quyền, outcomes, concurrency và work bounds để consumer không đoán từ class fields.

## 4. Khái niệm

Resource có identity/state, command diễn tả intent đổi state như approve/cancel. DTO là shape trao đổi; entity là object lưu/identity; domain model giữ rules. Request model chỉ fields client được phép đề nghị; response model chỉ fields caller được phép thấy. Dùng chung entity/DTO có thể đơn giản lúc đầu nhưng làm persistence fields thành public contract.

## 5. Thành phần bên trong

| Lớp kiểm | Câu hỏi | Ví dụ |
|---|---|---|
| Syntax | Bytes parse được không? | JSON malformed |
| Semantic | Value có nghĩa theo schema/units không? | Enum/date/range/type |
| Business | Transition/invariant hợp lệ không? | Không approve order đã canceled |
| Authorization | Caller được operation/field này không? | User A không edit task B |

Authentication xây actor identity, không trả lời business validity. Validation UI cải UX, server/domain/database vẫn giữ authoritative invariants.

## 6. Data representation

ID opaque string; money có currency/unit/rounding và bounds, date-only khác instant có timezone. Nullable, absent, empty và default có meanings khác. PATCH omission thường unchanged theo chosen format, null clear hoặc invalid phải explicit. Error envelope gồm stable code, message phù hợp, traceID và field errors khi cần; không dùng localized message làm code.

Pagination quy định pagebase/cursor/cap/total semantics; sort/filter allowlist, tie-breaker ID và query bounds. Versioning qua URL/header/media type là lựa chọn; compatibility của meaning quan trọng hơn đánh số.

## 7. Control flow

```text
Request bytes → syntax parse → DTO semantic checks
→ principal/resource authorization → business transition
→ atomic storage condition → response DTO/error → client parser
```

Resource policy có thể load object trước authorize nhưng mutation sau authorize. PUT replacement và PATCH operation khác; ordinary partial object không tự định nghĩa PATCH semantics. 201/202/204/error bodies theo contract; no-content phải có parser path riêng.

## 8. Lifetime / ownership / state

DTO input owned request sau parse; domain/storage authoritative owner giữ versions. Client snapshot version v chỉ valid làm expectedVersion, không tự latest. Idempotency intent key lifetime theo retention và user/tenant scope. API version migration giữ old/new readers/writers trong compatibility window; client cached bundle có thể cũ sau server rollout.

## 9. Invariants

Client không set owner/role/tenant internal fields. Business transition và expected version được kiểm cùng write. Queries bounded và stable order. Error status/body nhất quán; effect accepted/completed phân biệt. Same intent+same payload replay đúng outcome; same key+khác payload conflict theo design.

## 10. Ví dụ tối thiểu

[ASP.NET Core/MongoDB fixture](../examples/MongoApi/README.md) đã kiểm thử replay cùng key/payload và conflict khác payload trong 20 lượt với 8 requests song song ([record](../evidence/mongo-api/summary.json)). Chỉ claim idempotency trong fixture đó đã chạy; PATCH authorization/version contract dưới đây vẫn là pseudocode.

Contract minh họa **pseudocode**, không OpenAPI ứng dụng thật:

```text
PATCH /tasks/42
{ title: "B", expectedVersion: 7 }
principal = authenticated actor
condition = id42 AND allowedTenant AND version7
write = titleB, version8
if affected=0: classify inaccessible/notfound/conflict theo policy
success = response DTO version8
```

Không unconditional save sau precheck. Migration title→displayTitle: server đọc compatibility input có precedence rõ, response hỗ trợ clients cũ trong cửa sổ; rename đồng thời FE/BE không atomic.

## 11. Failure modes

Mass assignment khi bind entity; null clear không chủ ý; offset page drifting khi data đổi; status200 error che monitoring; incompatible rollout; client timeout retry mới key; version conflict bị retry stale body mãi. Fix contracts/whitelist/preconditions/migration, không string coercion để che mismatched shape.

## 12. Debug / observability

Capture raw request/response/status/headers và builds trước mapper. Contract fixtures success/no-content/validation/forbidden/conflict dùng cả old/new consumers. For authorization negative case kiểm data và side effect, không chỉ status. Concurrent version barrier và affected count cho evidence state mutation.

## 13. Liên hệ với bug/lab hiện có

[BE-04](../labs/backend/BE-04.md), [BE-27](../labs/backend/BE-27.md), [BE-28](../labs/backend/BE-28.md), [INT-01](../labs/integration/INT-01.md), [INT-03](../labs/integration/INT-03.md), [INT-25](../labs/integration/INT-25.md). Mapping full theory→invariant→lab ở [map](../BUG_THEORY_MAP.md).

## 14. Sai lầm thường gặp

Shape validation không authorization; authorization không giữ stock đủ. DTO không phải tên khác của whole entity. Stable sort không snapshot pages trên mutable dataset. Hidden field/button không access control. API version mới không tự migration persisted data.

## 15. Câu hỏi tự kiểm tra

1. Null và absent có cùng meaning PATCH không? Đáp án: phụ thuộc format, phải explicit.
2. Valid DTO có thể business invalid không? Đáp án: có.
3. User role valid có đủ edit mọi ID? Đáp án: object/field quyền riêng.
4. 202 có chứng minh durable job completed? Đáp án: không.
5. Version7 client edit khi current8 nên làm gì? Đáp án: conflict/reconcile theo contract, không unconditional overwrite.

## 16. Nguồn

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html), [Microsoft Web API design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design), [OWASP API2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). Examples là curriculum, source/OpenAPI thực phải override docs cũ.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
