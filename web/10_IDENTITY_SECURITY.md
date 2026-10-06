# Security: identity, authority và trust boundaries

Phạm vi: OWASP API2023/cheat sheets, JWT RFC7519/8725; ASP.NET8 là host ví dụ. Không triển khai provider/token issuance hay thay policy ứng dụng trong phase tài liệu.

## 1. Mục tiêu học

Vẽ credential→authentication→principal→session/token→authorization và nhận ra boundary bị phá bởi XSS/CSRF/BOLA/injection. Chọn evidence không chứa credential thật.

## 2. Kiến thức tiên quyết

[HTTP/cookies](12_HTTP_SEMANTICS.md), [browser isolation](13_BROWSER_INTERNALS.md), [ASP.NET](07_ASPNET_LIFECYCLE.md), [atomic mutation](15_DATABASE_TRANSACTIONS.md).

## 3. Vấn đề mà cơ chế này giải quyết

Client và input không được tin mặc định. Hệ thống cần chứng minh actor identity, giới hạn capability và bảo vệ intent/resource/data sinks; một authenticated user vẫn có thể cố truy cập object khác. Credentials và application data có exposure/lifetime khác nhau.

## 4. Khái niệm

Identity định danh actor; credential chứng minh một quyền nhận identity theo scheme. Authentication validate credential; authorization quyết định operation/resource/field/context có được phép. Trust boundary là nơi data/authority vượt vùng bảo đảm khác; server-render UI vẫn phải authorize data/action boundary.

## 5. Thành phần bên trong

Password storage dùng salted adaptive password hash qua library/provider đã hỗ trợ; salt chống precomputed sharing, work factor tăng guessing cost; pepper nếu dùng là secret riêng có lifecycle. Hash không mã hóa có thể decrypt; weak password vẫn bị đoán. Rate/abuse controls cần vì hash không giải toàn threat.

Session server lưu state gắn opaque identifier; cookie là browser transport/storage, có thể mang session ID/token/preferences. JWT signed là claims format, payload thường không encrypted. Validate signature/algorithm allowlist/issuer/audience/lifetime/key trust theo provider; decode không verification. Access token cho resource; refresh credential cho renew endpoint, scope/lifetime khác.

## 6. Data representation

Principal gồm validated identity/claims, không raw ownerId client. Refresh family có generation/used/revoked state; rotation tiêu thụ old credential và tạo mới atomic. Reuse detection phải có concurrency/grace policy provider, client single-flight trong một tab không bảo đảm mọi devices. Local stateless JWT check không tự thấy revocation mới; short expiry/introspection/revocation state là design choices.

Cookie Secure chỉ HTTPS send policy, HttpOnly hạn chế JS read, SameSite theo site chứ không origin; Domain/Path không thay full authorization boundary.

## 7. Control flow

```text
Untrusted request → credential transport → validate provider trust
→ principal → load/filter resource scope → authorize operation/fields
→ business checks → atomic mutation → permitted response
```

BOLA: lookup ID mà bỏ object/tenant scope. Mass assignment: writable fields vượt authority. Injection: input trở thành executable query/command syntax; bind params/allowlist structure thay concatenate. CORS kiểm script cross-origin response access, không server quyền và không ngăn mọi side effect.

## 8. Lifetime / ownership / state

Session/token lifetime bắt đầu issuance và kết thúc expiry/revoke theo validator awareness. Credential chỉ đến actors cần nó; refresh không mọi API, secret server không bundle/HTML/log. Rotation/revoke khi exposure thật cần quy trình riêng; xóa working file không thu credential đã lộ/history.

CSRF lợi dụng browser tự mang ambient cookies ngoài user intent; chống bằng token/origin checks/SameSite theo architecture. XSS chạy untrusted script trong trusted context; HttpOnly không ngăn nó dùng authenticated requests. Output encoding theo sink và HTML sanitization cho allowed markup giữ boundary.

## 9. Invariants

Authenticated không vượt resource/field scope. Side effects chỉ sau authority và intent defenses. Credentials không vào persistent logs/client bundles. Trust được verify tại boundary, không tin client role. Security controls không được disable để hết error; cache key/policy phải giữ principal isolation.

## 10. Ví dụ tối thiểu

Trace threat model **mô phỏng**: A logged in, task42 thuộc B. A đổi URL tới42; server có valid principal A nhưng query phải constrain allowed tenant/owner hoặc resource policy, deny không side effect. ID khó đoán không thay check.

XSS example context chỉ text display: dùng textContent/render escaped text thay innerHTML cho raw user input. Nếu product cho rich HTML, sanitizer allowlist/URL policy cần separate design; một encoder không áp mọi HTML/JS/URL contexts.

## 11. Failure modes

JWT wrong audience vẫn nhận nếu chỉ decode; revoked refresh replay do nonatomic state; BOLA lookup; mass assignment role; SQL/NoSQL injection query structure; CSRF cookie action; XSS HTML sink; public credential bundle; logs masked ở UI nhưng raw sink giữ. Fix đúng trust/authority/sink, không taxonomy-only checklist.

## 12. Debug / observability

DevTools cookie blocked reason/request credential presence, server stage principal scheme/policy outcome đã redaction, resource scope/query và affected count. Synthetic A/B/anonymous fixtures, wrongaud/expired claims qua supported validators, request không Origin vẫn auth. Không log raw token/password; correlation ID đủ nối traces. CORS error khác401/403 cần stage evidence.

## 13. Liên hệ với bug/lab hiện có

[BE-01](../labs/backend/BE-01.md), [BE-02](../labs/backend/BE-02.md), [BE-03](../labs/backend/BE-03.md), [BE-05](../labs/backend/BE-05.md), [BE-06](../labs/backend/BE-06.md), [FE-19](../labs/frontend/FE-19.md), [BE-24](../labs/backend/BE-24.md), [BE-29](../labs/backend/BE-29.md).

## 14. Sai lầm thường gặp

CORS ≠ authorization, cookie ≠ session, JWT ≠ encrypted secret, HttpOnly ≠ no XSS impact. Input valid không trusted actor; CRC/hash data integrity không origin authentication. Frontend hidden button/rate limit không server enforcement.

## 15. Câu hỏi tự kiểm tra

1. Decode token có chứng minh trusted issuer? Đáp án: không.
2. Session state cần ở đâu? Đáp án: theo scheme, thường server store; cookie chỉ ID/transport.
3. Revoke tới local JWT validator tự động không? Đáp án: cần policy/state awareness.
4. Parameter binding có cho client mọi sortable field? Đáp án: cấu trúc/field authority vẫn allowlist.
5. CSRF có bị CORS chặn hết không? Đáp án: không.
6. Scope token valid có đủ object quyền? Đáp án: còn policy trên resource/fields.

## 16. Nguồn

[JWT RFC7519](https://www.rfc-editor.org/rfc/rfc7519.html), [JWT best practices RFC8725](https://www.rfc-editor.org/rfc/rfc8725.html), [OWASP password](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [session](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html), [injection](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), [API2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
