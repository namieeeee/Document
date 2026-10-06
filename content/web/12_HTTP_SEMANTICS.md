# Outline — HTTP: semantics, representation, cache và partial failure

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Retry storm tăng tải khi dependency đã yếu. Timeout trước gửi, trong handler và sau commit có outcomes khác nhau nhưng client đều có thể thấy một lỗi timeout. Compression mismatch tạo decode error; cache sai Vary tạo wrong representation; retry stale PUT ghi đè update mới dù method idempotent. Idempotent không tự giải conflict giữa hai intents khác nhau.

Đặt câu hỏi: cơ chế trong [HTTP: semantics, representation, cache và partial failure](../../web/12_HTTP_SEMANTICS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Cache có hai câu hỏi: response được lưu không, và được dùng ngay không. Freshness dựa lifetime và current age theo cache rules; stale không tự được dùng, trừ policy cho phép. Validation gửi ETag/Last-Modified về server; 304 cho phép dùng stored representation và cập nhật metadata; 200 thay representation.

```text
GET → cache lookup theo URI/method/Vary
  → fresh & reusable: cached response
  → stale: GET If-None-Match
      → unchanged: 304 + reuse stored body
      → changed: 200 + store body mới theo policy
```

`no-store` cấm lưu theo directive; `no-cache` có thể lưu nhưng phải validation trước reuse; `private` giới hạn shared-cache use. TTL không phải bảo đảm data mới tức thì sau mutation.

## 3. Demo chạy thật

Claim có phạm vi: Cache key/policy giữ đúng representation và principal; protected personalized data không bị shared cache replay cho user khác. Retry phải giữ cùng intent và không thực hiện effect mới khi outcome chưa biết. Precondition được kiểm cùng mutation atomic phía server; kiểm ETag rồi ghi vô điều kiện vẫn race. Deadline/cancel chỉ là observation/control request ở một boundary.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../web/12_HTTP_SEMANTICS.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Retry storm tăng tải khi dependency đã yếu. Timeout trước gửi, trong handler và sau commit có outcomes khác nhau nhưng client đều có thể thấy một lỗi timeout. Compression mismatch tạo decode error; cache sai Vary tạo wrong representation; retry stale PUT ghi đè update mới dù method idempotent. Idempotent không tự giải conflict giữa hai intents khác nhau.

Dùng Network so status/headers/body từng attempt với trace ID và intent. Tách DNS/connect/queue/server/response timings; timeout actor nào phải được ghi. Controlled experiment drop response sau commit, so DB outcome với trước handler fail. Retry policy dựa method + application effect + transient class + remaining budget; bounded attempts, exponential backoff/jitter và tôn trọng Retry-After khi phù hợp. Không retry mọi 4xx, không log credentials.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html): methods §9, status §15, preconditions §13, negotiation §12. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html): cache storage/freshness/validation. [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html): PATCH. [Fetch standard](https://fetch.spec.whatwg.org/): browser fetch/cancel/CORS. [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) cho ứng dụng headers.

1. DELETE lần đầu 204, lần sau 404 có phá idempotency không? Đáp án: không, effect đích vẫn xóa.
2. Vì sao 304 không parse JSON? Đáp án: dùng stored representation.
3. `no-cache` có cấm storage không? Đáp án: không.
4. ETag precheck rồi unconditional write có safe không? Đáp án: không, race ở check/write gap.
5. Abort sau commit giải quyết duplicate ra sao? Đáp án: không; cần dedup/reconcile.
6. GET thay đổi stock vi phạm gì? Đáp án: safe semantics, làm các intermediary retry/prefetch sai.

[Index](../../00_INDEX.md) · [Content](../README.md).
