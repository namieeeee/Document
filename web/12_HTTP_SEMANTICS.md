# HTTP: semantics, representation, cache và partial failure

Phạm vi: RFC 9110/9111 (2022), HTTP semantics độc lập transport. Ví dụ application contract được ghi riêng; không suy mọi endpoint có cùng error convention.

## 1. Mục tiêu học

Phân loại một operation theo safe/idempotent/cacheable, vẽ conditional GET và conditional write, rồi giải thích tại sao một retry có thể tạo hai side effects. Đọc headers/status phải suy được actor đang biết gì và chưa biết gì.

## 2. Kiến thức tiên quyết

[Network/browser](01_HTTP_BROWSER.md), bytes và identifier. Học tiếp [Database concurrency](15_DATABASE_TRANSACTIONS.md) sau API/DB foundation để triển khai invariant phía storage; chưa cần bài đó để hiểu HTTP semantics.

## 3. Vấn đề mà cơ chế này giải quyết

HTTP cần một hợp đồng chung giữa clients, caches, proxies và origins. Client không biết implementation server, cache không biết business domain; methods, validators và status giúp các actor phối hợp. Network không có một transaction bao cả DB commit lẫn delivery response nên partial failure là trạng thái tự nhiên.

## 4. Khái niệm

Resource là đối tượng trừu tượng được định danh, representation là dữ liệu mô tả trạng thái ở một lúc. Method cho semantics yêu cầu; status cho outcome ở HTTP boundary. Safe nghĩa client không yêu cầu thay đổi state; ghi log có thể tồn tại. Idempotent nghĩa lặp cùng request có cùng hiệu ứng dự kiến như một lần; response có thể khác. Cacheable nghĩa có thể tái sử dụng response theo các điều kiện, không chỉ vì method GET.

## 5. Thành phần bên trong

| Method | Safe | Idempotent theo semantics | Nội dung contract |
|---|---|---|---|
| GET/HEAD | Có | Có | Đọc representation/metadata |
| PUT | Không | Có | Thay trạng thái resource đích theo representation |
| DELETE | Không | Có | Bỏ liên kết resource; lần sau có thể 404 |
| POST | Không | Không mặc định | Xử lý payload theo resource |
| PATCH | Không | Không mặc định | Áp patch document theo format |

GET/HEAD thường cacheable; POST có thể cache dưới điều kiện explicit, support thực tế tùy cache. Semantics method không cho phép backend biến GET thành tạo đơn rồi coi retry an toàn. PATCH set `done=true` có thể idempotent theo thiết kế; PATCH increment không như vậy.

## 6. Data representation

Request/response gồm control data, fields, content và framing do version đảm nhiệm. `Content-Type` mô tả media type body; `Accept` đề nghị media types response. `Accept-Language` và `Accept-Encoding` chọn ngôn ngữ/content coding; compression gzip/br thay bytes vận chuyển chứ không semantics DTO. `Vary` chỉ fields request tham gia chọn cached representation; quên nó có thể trả sai language/encoding.

ETag là opaque validator cho representation, không tự là version integer DB. Strong validator dùng cho so sánh cần byte-equivalence theo rules; weak validator có tiền tố W/ và chỉ tương đương semantic ở use cases cho phép. `If-Match` dùng strong comparison cho precondition write; `If-None-Match` cho validation GET thường weak comparison. Status 304 không có content để parse như JSON success.

## 7. Control flow

Cache có hai câu hỏi: response được lưu không, và được dùng ngay không. Freshness dựa lifetime và current age theo cache rules; stale không tự được dùng, trừ policy cho phép. Validation gửi ETag/Last-Modified về server; 304 cho phép dùng stored representation và cập nhật metadata; 200 thay representation.

```text
GET → cache lookup theo URI/method/Vary
  → fresh & reusable: cached response
  → stale: GET If-None-Match
      → unchanged: 304 + reuse stored body
      → changed: 200 + store body mới theo policy
```

`no-store` cấm lưu theo directive; `no-cache` có thể lưu nhưng phải validation trước reuse; `private` giới hạn shared-cache use. TTL không phải bảo đảm data mới tức thì sau mutation.

## 8. Lifetime / ownership / state

Cache owns stored bytes và metadata tới eviction/invalidation; consumer không được mutate snapshot dùng chung. Request lifetime kết thúc ở actor quan sát; transaction lifetime riêng phía server. AbortSignal yêu cầu host dừng fetch/đọc theo support, không revoke side effect đã commit. Reused connections tồn tại lâu hơn request, HTTP/2 stream reset không mặc định rollback endpoint.

Status classes: 1xx interim, 2xx success, 3xx redirect/conditional signals, 4xx lỗi request/context, 5xx server failure. 201 thường tạo resource với Location khi phù hợp; 202 là accepted, chưa bảo đảm job hoàn tất; 204 không có body; 401 có challenge theo auth scheme; 403 quyền bị từ chối; 412 precondition thất bại. Application 409 cho version conflict là convention khác conditional HTTP 412.

## 9. Invariants

Cache key/policy giữ đúng representation và principal; protected personalized data không bị shared cache replay cho user khác. Retry phải giữ cùng intent và không thực hiện effect mới khi outcome chưa biết. Precondition được kiểm cùng mutation atomic phía server; kiểm ETag rồi ghi vô điều kiện vẫn race. Deadline/cancel chỉ là observation/control request ở một boundary.

## 10. Ví dụ tối thiểu

Trace minh họa **mô phỏng**, không output thực thi:

```http
GET /tasks/42 HTTP/1.1
If-None-Match: "v7"
```

Nếu chưa đổi, server trả 304 và browser dùng body đã lưu. Với edit:

```http
PUT /tasks/42 HTTP/1.1
If-Match: "v7"
Content-Type: application/json

{"title":"B","done":false}
```

Backend chuyển validator thành condition hợp lệ theo contract, atomically kiểm/write; nếu current v8 thì reject precondition. Không gửi stale body để ghi đè v8.

Timeline retry: A gửi create intent K → server commit order O → response mất → A timeout → A gửi lại. Nếu key mới K2, server thấy intent mới và có thể tạo O2. Giữ K chỉ có hiệu quả khi server dedup atomic và xử lý crash window.

## 11. Failure modes

Retry storm tăng tải khi dependency đã yếu. Timeout trước gửi, trong handler và sau commit có outcomes khác nhau nhưng client đều có thể thấy một lỗi timeout. Compression mismatch tạo decode error; cache sai Vary tạo wrong representation; retry stale PUT ghi đè update mới dù method idempotent. Idempotent không tự giải conflict giữa hai intents khác nhau.

## 12. Debug / observability

Dùng Network so status/headers/body từng attempt với trace ID và intent. Tách DNS/connect/queue/server/response timings; timeout actor nào phải được ghi. Controlled experiment drop response sau commit, so DB outcome với trước handler fail. Retry policy dựa method + application effect + transient class + remaining budget; bounded attempts, exponential backoff/jitter và tôn trọng Retry-After khi phù hợp. Không retry mọi 4xx, không log credentials.

## 13. Liên hệ với bug/lab hiện có

[BE-13](../labs/backend/BE-13.md), [BE-14](../labs/backend/BE-14.md), [INT-19](../labs/integration/INT-19.md), [INT-20](../labs/integration/INT-20.md): cùng intent chỉ một effect. [INT-10](../labs/integration/INT-10.md): parser phân biệt 201/204/error thay chỉ chấp nhận 200.

## 14. Sai lầm thường gặp

Idempotent không phải exactly-once delivery hoặc response giống bytes. `fetch` thường resolve khi nhận HTTP 400/500; caller kiểm `ok/status`, rejection chủ yếu network/abort theo API. Cache bust query tùy ý có thể dùng cô lập thí nghiệm nhưng không thay invalidation design. Cancel không bảo đảm server đã dừng.

## 15. Câu hỏi tự kiểm tra

1. DELETE lần đầu 204, lần sau 404 có phá idempotency không? Đáp án: không, effect đích vẫn xóa.
2. Vì sao 304 không parse JSON? Đáp án: dùng stored representation.
3. `no-cache` có cấm storage không? Đáp án: không.
4. ETag precheck rồi unconditional write có safe không? Đáp án: không, race ở check/write gap.
5. Abort sau commit giải quyết duplicate ra sao? Đáp án: không; cần dedup/reconcile.
6. GET thay đổi stock vi phạm gì? Đáp án: safe semantics, làm các intermediary retry/prefetch sai.

## 16. Nguồn

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html): methods §9, status §15, preconditions §13, negotiation §12. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html): cache storage/freshness/validation. [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html): PATCH. [Fetch standard](https://fetch.spec.whatwg.org/): browser fetch/cancel/CORS. [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) cho ứng dụng headers.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
