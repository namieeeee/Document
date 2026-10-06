# C# language: value, reference và resource lifetime

Phạm vi: C#12 / .NET8. Async/IL/JIT/GC thực thi chi tiết ở [runtime](14_DOTNET_ASYNC_RUNTIME.md), học trước ASP.NET.

## 1. Mục tiêu học

Giải thích assignment/copy/boxing, class/struct/interface/generic, nullable/exception và acquire-use-dispose. Không suy placement stack/heap chỉ từ tên type.

## 2. Kiến thức tiên quyết

Biến, hàm và [representation](../foundations/01_DIGITAL_REPRESENTATION.md) ở mức đọc; C# không yêu cầu học toàn C trước. Object identity dùng chung ý tưởng với JS nhưng type/rules khác.

## 3. Vấn đề mà cơ chế này giải quyết

C# cung cấp typed abstractions để diễn tả dữ liệu và behavior; .NET quản lý managed memory. File/socket/lock vẫn cần release theo nghiệp vụ. Copy một struct chứa reference hoặc boxing mutable struct dễ làm developer hiểu sai state thay đổi ở đâu.

## 4. Khái niệm

Value type variable chứa value theo semantics; reference variable chứa reference tới object hoặc null. `class` là reference type, `struct` là value type; `object` có thể giữ reference hoặc boxed value. Interface định nghĩa contract capabilities, implementation được chọn theo instance; không tự cấp instance/thread.

Generic giữ quan hệ type, constraints như `where T:IDisposable` cho operations hợp lệ; .NET generics có runtime representation, không type-erased như TS annotation. Nullable value `int?` là Nullable<int>; nullable reference `string?` là annotations/compiler flow analysis, không runtime wrapper/check tự động.

## 5. Thành phần bên trong

Class gồm fields/state và methods/constructor; struct copy fields theo value semantics. Struct có List field copy reference List, không deep copy. Property là accessors có thể chạy logic, không luôn một memory slot. Exception ném chuyển flow tới catch phù hợp, finally giải cleanup. `throw;` rethrow giữ stack trace tốt hơn ném lại exception variable theo cách tạo throw site mới.

## 6. Data representation

```text
p1: reference ──┐
               ├─ object Person { Name, Tags reference → List }
p2: reference ──┘
s1 struct { N=1, Tags → List }
s2 struct { N=1, Tags → cùng List } sau copy
```

Boxing value type tạo boxed copy trên managed heap; thay box không thay original value. Unboxing đòi đúng type và tạo value theo semantics. Object trong array/class fields có thể chứa struct inline; local ref/value có thể ở register/stack/compiler optimized, nên class=heap/struct=stack là mô hình sai.

## 7. Control flow

Source→compiler typecheck/IL→runtime execution. Constructor thiết lập valid state trước publish; methods kiểm transitions; exception paths phải release resources. `using` được compiler triển khai cleanup qua finally thích hợp; `await using` dùng async-dispose cho resource có IAsyncDisposable. Disposing không bảo đảm operation khác đang dùng object đã hoàn tất.

## 8. Lifetime / ownership / state

GC giữ object reachable từ roots; hết lexical scope không quyết định thời điểm collection. `IDisposable` là contract deterministic release, GC không tự gọi Dispose của mọi object. Finalizer là fallback có limitations/later timing, không deadline close. Owner tạo/acquire resource chịu dispose; borrowed dependency không tự được dispose nếu owner/container giữ nó. Event publisher dài lifetime có thể giữ subscriber qua delegate.

## 9. Invariants

Không dùng disposed resource; mỗi owned acquisition có release trên success/error/cancel. Copy semantics không phá domain invariant; public mutable reference không để caller tùy ý sửa protected state. Nullable warnings không thay input validation; unchecked integer overflow policy phải explicit cho dữ liệu quantity/money.

## 10. Ví dụ tối thiểu

Ví dụ console C#12/.NET8, không cần package ngoài. Kết quả chạy với assertions bổ sung được ghi ở [VALIDATION](../VALIDATION.md):

```csharp
using System.Collections.Generic;
using System.IO;

var a = new Sample(1, new List<int> { 7 });
var b = a;
b.Tags.Add(8); // a.Tags cũng có 8: reference field được copy
object boxed = a.N; // boxed copy int 1
using var stream = new MemoryStream();
stream.WriteByte(42);

record struct Sample(int N, List<int> Tags);
```

Dự đoán a.N vẫn 1 và a.Tags có hai elements. Stream dispose khi scope kết thúc kể cả exception; caller không được lưu stream để dùng sau đó.

## 11. Failure modes

Null dereference do external invalid input; boxing allocation churn; mutable struct copies làm update không tới original; shared reference field ngoài expectation; disposed dependency trong background work; retained subscribers; catch return empty che failure. Fix ownership/copy contracts và failure propagation, không force GC như cách close socket.

## 12. Debug / observability

Debugger inspect reference IDs/fields và stack khi throw; allocation profiler phân biệt boxing/churn/retention; heap roots cho delegates/static fields. Instrument dispose/instance scope và late use bằng synthetic workload. Compiler nullable/type diagnostics là layer đầu, runtime input/regression là layer khác.

## 13. Liên hệ với bug/lab hiện có

[BE-08](../labs/backend/BE-08.md) dependency lifetime; [BE-22](../labs/backend/BE-22.md) exception outcome; [OS-05](../labs/os/OS-05.md) retention model. [Runtime](14_DOTNET_ASYNC_RUNTIME.md) nối tới BE10–12.

## 14. Sai lầm thường gặp

Value copy không đồng nghĩa deep copy. Object reachability không đồng nghĩa resource còn usable. `using` không làm borrowed ownership đúng nếu dispose resource người khác giữ. `string?` không validate JSON. Interface abstraction không quyết định DI lifetime.

## 15. Câu hỏi tự kiểm tra

1. Struct trong class field nằm đâu? Đáp án: có thể inline trong heap object.
2. Copy struct có List có tạo List mới? Đáp án: không.
3. GC tự gọi IDisposable cho mọi object không? Đáp án: không.
4. Nullable annotation có ném lỗi ngay khi external null tới? Đáp án: không.
5. Boxing có giữ original mutable value cùng identity? Đáp án: boxed copy.
6. Exception path nào cần cleanup? Đáp án: mọi path sau acquire theo owner contract.

## 16. Nguồn

[C# specification types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/types), [value types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [boxing](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing), [dispose pattern](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose), [nullable references](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references). Language docs rolling, bài giới hạn C#12 features.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
