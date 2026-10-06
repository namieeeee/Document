# Outline — ASP.NET Core: lifecycle request và dependency scope

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Captive dependency disposed use; singleton current user cross-talk; auth middleware đặt sau protected endpoint; catch ngoài không bao throw; write response rồi exception mapping fail; options provider precedence sai; unobserved request job. Fix tại pipeline/lifetime/error owner, không serialize toàn server hoặc disable auth.

Đặt câu hỏi: cơ chế trong [ASP.NET Core: lifecycle request và dependency scope](../../web/07_ASPNET_LIFECYCLE.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Client → Kestrel → outer exception/logging
→ routing → CORS/authentication → authorization
→ MVC binding → model validation → endpoint
→ service business validation → repository/DB
→ DTO serialization → unwind middleware → response bytes
```

Sơ đồ responsibility; actual Program.cs và auto-added hosting middleware quyết định order. Authorization resource-specific có thể cần resource load rồi policy trước mutation, không giả mọi object check xảy ra trước binding. Pass cancellation tới I/O hỗ trợ; client disconnect không làm transaction rollback tự động.

## 3. Demo chạy thật

Claim có phạm vi: Auth/authorization trước protected side effects; binding/validation chưa đủ domain invariant. Dependency dài lifetime không capture ngắn lifetime; user/tenant request state không shared singleton. Error outcome giữ HTTP meaning, không swallow thành empty200; trace không chứa secrets. Không dùng context sau request lifetime.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../web/07_ASPNET_LIFECYCLE.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Captive dependency disposed use; singleton current user cross-talk; auth middleware đặt sau protected endpoint; catch ngoài không bao throw; write response rồi exception mapping fail; options provider precedence sai; unobserved request job. Fix tại pipeline/lifetime/error owner, không serialize toàn server hoặc disable auth.

Trace middleware enter/exit, endpoint metadata, status/HasStarted, service instance/scope và dependency timing với requestID. Barrier A set→B set→A read chứng minh singleton state lẫn. Scope validation phát hiện một số captive graph, không mọi runtime capture. 403 không controller trace có thể expected short circuit; xem stage cuối observed trước sửa binder.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[Middleware8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-8.0), [DI8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0), [options8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options?view=aspnetcore-8.0), [binding8](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0), [validation8](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-8.0), [error handling8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling?view=aspnetcore-8.0).

1. Response unwind qua middleware chưa gọi next không? Đáp án: không theo downstream chain đó.
2. Singleton giữ scoped repo là gì? Đáp án: captive dependency/lifetime mismatch.
3. IOptionsSnapshot dùng singleton có hợp không? Đáp án: snapshot scoped, cần monitor hoặc phù hợp design.
4. HasStarted ảnh hưởng gì? Đáp án: status/header/error response không còn tùy đổi.
5. ApiController validation có giữ stock invariant? Đáp án: không, cần atomic business write.

[Index](../../00_INDEX.md) · [Content](../README.md).
