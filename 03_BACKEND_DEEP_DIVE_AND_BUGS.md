# 03 — Backend .NET 8: quyền, async và dữ liệu

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Web06 — C# và runtime trước ASP.NET](web/06_CSHARP_RUNTIME.md)
- [Web07 — ASP.NET Core: lifecycle một request](web/07_ASPNET_LIFECYCLE.md)
- [Web08 — API: invariant trước endpoint shape](web/08_API_CONTRACTS.md)
- [Web09 — Database: access path, atomicity và invariant](web/09_DATABASE_CONCURRENCY.md)
- [Web10 — Identity, credentials và quyền](web/10_IDENTITY_SECURITY.md)

Mục tiêu: thiết kế endpoint giữ invariant ngay khi client sai hoặc request đồng thời. Tiền đề: C# class/Task, chương 01. Stack bài: ASP.NET Core 8 Web API, MongoDB; bài SQL dùng để đối chiếu transaction/index, không yêu cầu chạy hai DB một lúc.

## pipeline và lifetime

Request đi qua middleware theo thứ tự đăng ký, rồi quay ngược trên đường response. Middleware ghi lỗi cần bao quanh phần có thể ném lỗi; auth phải trước đoạn dựa trên principal. Không coi thứ tự trong một project khác là template universal. [Middleware .NET 8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-8.0).

Transient tạo khi được resolve; scoped gắn scope, thường mỗi request; singleton dùng chung toàn ứng dụng. Singleton giữ “current user” gây lẫn request. Singleton không được capture scoped dependency rồi sống lâu hơn scope. Scope của background job phải được tạo/giải phóng đúng vòng đời. [DI .NET 8](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0).

## async có ownership

`Task` đại diện completion/failure. `async void` ngoài event handler làm caller khó chờ/bắt lỗi. Fire-and-forget dùng request-scoped service có thể chạy sau dispose. Với công việc phải bền vững, dùng hàng đợi và worker có lifecycle/retry/dead-letter; response “đã nhận” khác “đã hoàn tất”.

`await` I/O cho thread phục vụ việc khác. `.Result`/`.Wait()` có thể làm nghẽn thread pool; ASP.NET Core không có cùng SynchronizationContext của UI cũ nên không khẳng định mọi `.Result` đều deadlock. CPU-bound không tự nhanh hơn vì thêm async. CancellationToken cần truyền xuống operation có hỗ trợ; operation đã commit không được “undo” bằng token.

```csharp
// Fragment controller/service; repository được inject qua constructor.
public async Task<TaskDto?> ReadAsync(string id, CancellationToken ct)
{
    return await repository.ReadAsync(id, ct);
}
```

## security và consistency

Authentication trả lời ai; authorization trả lời được làm gì trên đối tượng cụ thể. Có token hợp lệ không đồng nghĩa được xem mọi ID. Backend phải kiểm tra ownership/tenant theo principal, không tin owner Id client gửi. DTO ghi chỉ chứa field được phép; bind thẳng entity có thể cho user sửa role hoặc tenant. [OWASP API risks](https://api-security.owasp.org/editions/2023/en/0x11-t10/).

Token validation cần kiểm signature, issuer, audience, lifetime theo provider và cấu hình đúng. Refresh rotation cần thiết kế xử lý reuse và concurrent refresh; không tự phát hành token bằng thuật toán tự chế. Hướng dẫn JWT đã đọc thuộc phiên bản tài liệu hiện hành, không phải bằng chứng snippet này tương thích mọi API .NET 8: [Microsoft JWT](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication).

Đọc quantity=1 rồi update=0 là check-then-act: hai request cùng đọc có thể cùng bán một món. Với MongoDB, một update document có filter `quantity >= 1` và `$inc:-1` giữ invariant đơn document; kiểm matched/modified count. Khi invariant trải nhiều document, xét transaction hoặc đổi mô hình, không áp dụng single-document guarantee cho toàn work flow. [Atomic writes](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/).

SQL đối chiếu: constraint bảo vệ uniqueness; transaction cần isolation đúng; optimistic concurrency dùng version trong WHERE và kiểm số hàng ảnh hưởng. Không chọn transaction dài chỉ để “an toàn” nếu có thể atomic update ngắn. Pagination phải có sort ổn định, ví dụ createdAt + ID. Index chọn theo workload và explain, không mọi field; compound index thứ tự ảnh hưởng khả năng hỗ trợ sort. [MongoDB sort/index](https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/).

## quan sát không làm rò dữ liệu

Log trace Id, outcome, latency và dependency; redaction trước khi lưu. Rate limit giảm abuse nhưng không thay auth; size limit/timeout và bounded query ngăn request nhỏ gây công việc vô hạn. Cache key phải có tenant và biến thể quyền liên quan. HTTP error có status đúng và contract thống nhất; không trả200 cùng body `success:false` cho mọi lỗi.

## Thực hành và tự kiểm tra

[30 lab BE](labs/backend/README.md). Với concurrency, dùng barrier để hai request đọc cùng version; đừng chạy tuần tự rồi kết luận không có race. Thread-pool diagnostic tài liệu mới hướng .NET9+, counters cụ thể phải đối chiếu tool .NET8: [Microsoft diagnostic](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-threadpool-starvation).

1. Vì sao mutex trong một process không bảo vệ nhiều API replica?
2. Scope nào cần cho worker?
3. Cancellation khác rollback thế nào?
4. Khi nào unique index thay thế được check tồn tại?
5. Vì sao log đầy đủ token là nguy hiểm?

Hoàn thành khi endpoint chịu được input sai, truy cập chéo user và request cạnh tranh mà giữ invariant. Tiếp [04](04_FE_BE_INTEGRATION_AND_REAL_BUGS.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [BE-09](labs/backend/BE-09.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** State request được lưu trong singleton dùng chung, request sau thay dữ liệu request trước. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Request state không lẫn giữa user/request đồng thời.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Serialize toàn server requests bằng một lock lớn.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](web/07_ASPNET_LIFECYCLE.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
