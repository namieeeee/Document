# Outline — C# language: value, reference và resource lifetime

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Null dereference do external invalid input; boxing allocation churn; mutable struct copies làm update không tới original; shared reference field ngoài expectation; disposed dependency trong background work; retained subscribers; catch return empty che failure. Fix ownership/copy contracts và failure propagation, không force GC như cách close socket.

Đặt câu hỏi: cơ chế trong [C# language: value, reference và resource lifetime](../../web/06_CSHARP_RUNTIME.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Source→compiler typecheck/IL→runtime execution. Constructor thiết lập valid state trước publish; methods kiểm transitions; exception paths phải release resources. `using` được compiler triển khai cleanup qua finally thích hợp; `await using` dùng async-dispose cho resource có IAsyncDisposable. Disposing không bảo đảm operation khác đang dùng object đã hoàn tất.

## 3. Demo chạy thật

Claim có phạm vi: Checked arithmetic tại int boundary ném exception trong C# fixture, không chứng minh C UB.

```text
dotnet run --project examples/CoreModels/CoreModels.csproj -c Release
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/core.log):

```text
PASS checked arithmetic boundary (C# not C UB)
```

## 4. Cách nó hỏng và cách phát hiện

Null dereference do external invalid input; boxing allocation churn; mutable struct copies làm update không tới original; shared reference field ngoài expectation; disposed dependency trong background work; retained subscribers; catch return empty che failure. Fix ownership/copy contracts và failure propagation, không force GC như cách close socket.

Debugger inspect reference IDs/fields và stack khi throw; allocation profiler phân biệt boxing/churn/retention; heap roots cho delegates/static fields. Instrument dispose/instance scope và late use bằng synthetic workload. Compiler nullable/type diagnostics là layer đầu, runtime input/regression là layer khác.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[C# specification types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/types), [value types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types), [boxing](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing), [dispose pattern](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose), [nullable references](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references). Language docs rolling, bài giới hạn C#12 features.

1. Struct trong class field nằm đâu? Đáp án: có thể inline trong heap object.
2. Copy struct có List có tạo List mới? Đáp án: không.
3. GC tự gọi IDisposable cho mọi object không? Đáp án: không.
4. Nullable annotation có ném lỗi ngay khi external null tới? Đáp án: không.
5. Boxing có giữ original mutable value cùng identity? Đáp án: boxed copy.
6. Exception path nào cần cleanup? Đáp án: mọi path sau acquire theo owner contract.

[Index](../../00_INDEX.md) · [Content](../README.md).
