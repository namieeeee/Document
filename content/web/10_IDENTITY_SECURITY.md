# Outline — Security: identity, authority và trust boundaries

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

JWT wrong audience vẫn nhận nếu chỉ decode; revoked refresh replay do nonatomic state; BOLA lookup; mass assignment role; SQL/NoSQL injection query structure; CSRF cookie action; XSS HTML sink; public credential bundle; logs masked ở UI nhưng raw sink giữ. Fix đúng trust/authority/sink, không taxonomy-only checklist.

Đặt câu hỏi: cơ chế trong [Security: identity, authority và trust boundaries](../../web/10_IDENTITY_SECURITY.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Untrusted request → credential transport → validate provider trust
→ principal → load/filter resource scope → authorize operation/fields
→ business checks → atomic mutation → permitted response
```

BOLA: lookup ID mà bỏ object/tenant scope. Mass assignment: writable fields vượt authority. Injection: input trở thành executable query/command syntax; bind params/allowlist structure thay concatenate. CORS kiểm script cross-origin response access, không server quyền và không ngăn mọi side effect.

## 3. Demo chạy thật

Claim có phạm vi: Authenticated không vượt resource/field scope. Side effects chỉ sau authority và intent defenses. Credentials không vào persistent logs/client bundles. Trust được verify tại boundary, không tin client role. Security controls không được disable để hết error; cache key/policy phải giữ principal isolation.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../web/10_IDENTITY_SECURITY.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

JWT wrong audience vẫn nhận nếu chỉ decode; revoked refresh replay do nonatomic state; BOLA lookup; mass assignment role; SQL/NoSQL injection query structure; CSRF cookie action; XSS HTML sink; public credential bundle; logs masked ở UI nhưng raw sink giữ. Fix đúng trust/authority/sink, không taxonomy-only checklist.

DevTools cookie blocked reason/request credential presence, server stage principal scheme/policy outcome đã redaction, resource scope/query và affected count. Synthetic A/B/anonymous fixtures, wrongaud/expired claims qua supported validators, request không Origin vẫn auth. Không log raw token/password; correlation ID đủ nối traces. CORS error khác401/403 cần stage evidence.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[JWT RFC7519](https://www.rfc-editor.org/rfc/rfc7519.html), [JWT best practices RFC8725](https://www.rfc-editor.org/rfc/rfc8725.html), [OWASP password](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [session](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html), [injection](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), [API2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).

1. Decode token có chứng minh trusted issuer? Đáp án: không.
2. Session state cần ở đâu? Đáp án: theo scheme, thường server store; cookie chỉ ID/transport.
3. Revoke tới local JWT validator tự động không? Đáp án: cần policy/state awareness.
4. Parameter binding có cho client mọi sortable field? Đáp án: cấu trúc/field authority vẫn allowlist.
5. CSRF có bị CORS chặn hết không? Đáp án: không.
6. Scope token valid có đủ object quyền? Đáp án: còn policy trên resource/fields.

[Index](../../00_INDEX.md) · [Content](../README.md).
