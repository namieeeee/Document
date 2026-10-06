# ASP.NET Core: lifecycle request và dependency scope

Phạm vi: ASP.NET Core8, Kestrel, MVC controllers có `[ApiController]`. Minimal API8 có binding/validation conventions riêng, không áp automatic MVC model validation tùy ý.

## 1. Mục tiêu học

Theo request từ connection tới serialized response, xác định stage short circuit/failure, service owner và response-start boundary. Chọn lifetime DI/config/options theo data thực, không theo tên layer.

## 2. Kiến thức tiên quyết

[HTTP](12_HTTP_SEMANTICS.md), [C#](06_CSHARP_RUNTIME.md), [.NET async/runtime](14_DOTNET_ASYNC_RUNTIME.md). API/business validation học tiếp [contract](08_API_CONTRACTS.md).

## 3. Vấn đề mà cơ chế này giải quyết

Server phải dịch protocol vào application operation và bảo vệ resource trước side effects. Middleware/endpoint/DI cho composition và construction có lifecycle; nếu thứ tự hoặc scope sai, endpoint logic đúng vẫn có thể unauthorized/lẫn user/disposed service.

## 4. Khái niệm

Kestrel xử lý transport/protocol, tạo request context vào application pipeline. Middleware là delegate có thể gọi next hoặc trả response sớm. Routing chọn endpoint/metadata; authentication xây principal; authorization kiểm policies/resource; binding tạo input values; validation kiểm constraints; endpoint/service/repository thực hiện business work. Logging/configuration là hạ tầng xuyên pipeline, không chỉ controller.

## 5. Thành phần bên trong

Request đi middleware order đăng ký; response unwind ngược các middleware đã gọi next. Error middleware ở ngoài bao downstream exception; static files/cache/auth có thể short-circuit. Endpoint metadata cần được xác định trước policy middleware sử dụng. MVC binding đọc route/query/body qua binder/formatter; `[ApiController]` có automatic invalid ModelState response, nhưng business rules vẫn service/domain.

DI registration tạo graph: transient mới theo resolve, scoped shared trong scope, singleton app lifetime. Singleton thread-safe/stateless hợp lệ; scoped trong một request có thể bị dùng concurrently nên scoped không tự thread-safe.

## 6. Data representation

HttpContext chứa request/response/user/features/items/RequestAborted; không object toàn app để singleton lưu current user. DTO là values mới từ binding, principal do auth handler tạo. Response headers/body có started state; sau headers gửi, middleware không tùy ý thay status thành JSON error.

Configuration tổng hợp providers theo precedence; options bind settings thành typed object. IOptions app-level value, IOptionsSnapshot scoped snapshot theo request, IOptionsMonitor update/current values và change hooks; chọn theo .NET8 contract. Options validation/startup check xác minh config, không external dependency luôn healthy.

## 7. Control flow

```text
Client → Kestrel → outer exception/logging
→ routing → CORS/authentication → authorization
→ MVC binding → model validation → endpoint
→ service business validation → repository/DB
→ DTO serialization → unwind middleware → response bytes
```

Sơ đồ responsibility; actual Program.cs và auto-added hosting middleware quyết định order. Authorization resource-specific có thể cần resource load rồi policy trước mutation, không giả mọi object check xảy ra trước binding. Pass cancellation tới I/O hỗ trợ; client disconnect không làm transaction rollback tự động.

## 8. Lifetime / ownership / state

Request scope giữ scoped/disposable services tới end; container owns constructed disposable dependencies theo DI rules. Fire-and-forget capture service có thể dùng sau scope dispose. BackgroundService tạo scope own cho từng work unit và observe completion; request không giữ job scope vô hạn. Db client thread-safe dài lifetime tùy library không bị đổi scoped chỉ vì dùng DB.

Response success theo operation contract chỉ sau completion cần thiết; accepted-job API phải nói durable acceptance nghĩa gì. Exception/cancel cleanup phải release DB/stream/lock trước owner kết thúc.

## 9. Invariants

Auth/authorization trước protected side effects; binding/validation chưa đủ domain invariant. Dependency dài lifetime không capture ngắn lifetime; user/tenant request state không shared singleton. Error outcome giữ HTTP meaning, không swallow thành empty200; trace không chứa secrets. Không dùng context sau request lifetime.

### Middleware chạy hai chiều

Mô hình A→B→Endpoint: A làm phần trước await next; B làm phần trước; endpoint chạy; B tiếp tục phần sau; A tiếp tục phần sau. Exception unwind ngược về handler đặt phía ngoài. Nếu B short-circuit và không gọi next, endpoint và phần downstream không chạy nhưng phần sau next của A vẫn có thể chạy.

Khi response đã started, headers/status không còn tùy ý đổi; exception middleware phải xử lý theo started state, không viết thêm JSON vào body đang stream rồi gọi đó là error response chuẩn. Ghi request correlation ID, selected endpoint, auth result và phase response-start để biết lỗi xảy ra ở boundary nào.

### DI lifetime là đồ thị dependencies

Singleton giữ reference tới dependency thường giữ nó lâu bằng singleton. Nếu reference đó là scoped service, request scope kết thúc nhưng singleton còn dùng reference: lifetime dependency không phù hợp owner. Container validation có thể phát hiện một số graphs; factory/service locator che lỗi không thay hợp đồng lifetime.

Transient không nghĩa “an toàn đa luồng”; scoped không nghĩa “một thread dùng”; singleton không nghĩa “immutable”. Một request có thể có concurrent operations cùng dùng scoped dependency; service đó vẫn phải đáp ứng concurrency contract của nó. Background worker tạo scope riêng và giữ scope đến work completion, không mượn request scope để chạy sau response.

Options/configuration cần phân biệt snapshot theo scope, monitor thay đổi và validation lúc startup/runtime. Cập nhật config không bảo đảm một multi-field operation đã lấy snapshot nhất quán nếu code đọc nhiều lúc; chọn boundary phù hợp invariant.

## 10. Ví dụ tối thiểu

Middleware fragment ASP.NET8, không full app:

```csharp
app.Use(async (ctx, next) => {
    logger.LogInformation("Enter {TraceId}", ctx.TraceIdentifier);
    await next(ctx);
    logger.LogInformation("Exit {Status}", ctx.Response.StatusCode);
});
```

Downstream throw sẽ bỏ Exit nếu không finally; lifecycle logs cần finally/outcome policy khi thích hợp. Logger là dependency fixture, không log body/token. Short circuit `return` trước next khiến endpoint không chạy dù route match.

## 11. Failure modes

Captive dependency disposed use; singleton current user cross-talk; auth middleware đặt sau protected endpoint; catch ngoài không bao throw; write response rồi exception mapping fail; options provider precedence sai; unobserved request job. Fix tại pipeline/lifetime/error owner, không serialize toàn server hoặc disable auth.

## 12. Debug / observability

Trace middleware enter/exit, endpoint metadata, status/HasStarted, service instance/scope và dependency timing với requestID. Barrier A set→B set→A read chứng minh singleton state lẫn. Scope validation phát hiện một số captive graph, không mọi runtime capture. 403 không controller trace có thể expected short circuit; xem stage cuối observed trước sửa binder.

## 13. Liên hệ với bug/lab hiện có

[BE-08](../labs/backend/BE-08.md), [BE-09](../labs/backend/BE-09.md) scope/current user; [BE-22](../labs/backend/BE-22.md) error meaning; [BE-23](../labs/backend/BE-23.md) correlation; [BE-12](../labs/backend/BE-12.md) cancellation. Negative auth test phải kiểm không side effect, không chỉ status.

## 14. Sai lầm thường gặp

Scoped không là 'mỗi thread'; singleton không mặc nhiên sai; transient disposable không tự caller owner nếu container tạo. Binding success không authorization. Middleware có next nhưng không bắt buộc gọi. Exception handler không sửa được response đã start bằng mọi cách.

## 15. Câu hỏi tự kiểm tra

1. Response unwind qua middleware chưa gọi next không? Đáp án: không theo downstream chain đó.
2. Singleton giữ scoped repo là gì? Đáp án: captive dependency/lifetime mismatch.
3. IOptionsSnapshot dùng singleton có hợp không? Đáp án: snapshot scoped, cần monitor hoặc phù hợp design.
4. HasStarted ảnh hưởng gì? Đáp án: status/header/error response không còn tùy đổi.
5. ApiController validation có giữ stock invariant? Đáp án: không, cần atomic business write.

## 16. Nguồn

[Middleware8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-8.0), [DI8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0), [options8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options?view=aspnetcore-8.0), [binding8](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0), [validation8](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-8.0), [error handling8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling?view=aspnetcore-8.0).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
