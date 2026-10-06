# .NET: IL/JIT/GC và async continuations

Phạm vi: .NET8 managed runtime, C#12 Task-based async; không dùng .NET9+ diagnostic counter tutorial như bằng chứng đã chạy trên .NET8.

## 1. Mục tiêu học

Vẽ source→assembly/IL→runtime/JIT→machine code; mô tả GC roots/generations và async state machine. Dự đoán operation nào giữ worker, cancellation có thể dừng ở đâu và Task completion thuộc ai.

## 2. Kiến thức tiên quyết

[C# language/lifetime](06_CSHARP_RUNTIME.md), execution stack, [OS concurrency](../os/04_CONCURRENCY.md) là bài mở rộng. Task không phải thread hay task RTOS.

## 3. Vấn đề mà cơ chế này giải quyết

Compiler cần output portable cho runtime và runtime cần quản lý execution/memory. I/O có thể đợi lâu hơn CPU work; giữ một thread cho mỗi wait làm server tốn workers. Async cho continuation sau completion nhưng không tự bảo vệ shared state hoặc durable job lifecycle.

## 4. Khái niệm

Assembly chứa IL/metadata/type references/resources theo output. Runtime load dependencies, quản lý execution và exceptions; JIT chuyển IL method sang machine code khi cần theo implementation. Tiered compilation/ReadyToRun/AOT là deployment modes khác; không nói mọi method luôn JIT một lần hoặc IL instruction map 1:1 machine instruction.

## 5. Thành phần bên trong

GC tìm roots, trace reachable graph và thu unreachable objects; generations nhóm tuổi để nhiều collections nhỏ hơn. Gen0/Gen1 thường objects trẻ, Gen2 sống lâu; large-object heap có policy riêng. Survivor promotion không chứng minh business còn cần object. Collection có costs và pauses tùy mode, heap fragmentation/retention/allocation rate khác nhau.

Thread pool có queues/workers và policy điều chỉnh; I/O completion có thể schedule continuations khi result sẵn. Task là completion abstraction, có thể completed hoặc pending I/O mà không một worker sleeping riêng. SynchronizationContext/TaskScheduler ảnh hưởng continuation placement; ASP.NET Core không có UI context mặc định.

## 6. Data representation

Compiler async method lưu logical state/resume location, parameters/locals cần qua awaits; Task cho result/exception/cancellation. Awaiter kiểm IsCompleted; nếu chưa complete đăng ký continuation và return control; khi ready GetResult nhận value hoặc throw. Completed task có thể tiến qua await inline trong .NET; không cam kết đổi thread.

Task fault giữ exceptions để caller observe. Task.WhenAll quan sát nhóm operations, không khóa mutation. Async void caller không có Task để await; ngoài event-handler contract phù hợp, error ownership khó giữ. Fire-and-forget mất owner completion/resource nếu chỉ discard Task.

### Async state machine giữ gì qua một await?

Xét method đọc bytes rồi parse: trước await, caller và method đang dùng cùng call chain. Nếu read chưa complete, stack call có thể unwind nhưng logical operation chưa kết thúc. Compiler phải giữ những locals còn cần sau await trong state machine theo implementation; vì vậy reference tới buffer có thể tiếp tục giữ buffer reachable. Lifetime của operation dài hơn lifetime của đoạn stack đang chạy.

Pseudocode khái niệm, không output compiler:

```text
state 0: start read; obtain awaiter
if not completed:
    save resume state = 1
    register continuation
    return to caller with outer Task
state 1: awaiter.GetResult() -> value or exception
parse value -> settle outer Task
```

Awaiter completed có thể đi thẳng sang GetResult. Nếu read fault, exception đi vào outer Task và caller await nhận exception; một catch quanh lúc tạo Task không thay cho await/observe. WhenAll hoàn tất sau các Tasks đầu vào hoàn tất; await thường throw một exception, Task.Exception giữ thông tin aggregate faults theo contract. Nó không tự cancel siblings hoặc rollback side effects của sibling thành công.

### GC roots và native resources có hai cơ chế lifetime

Một static dictionary giữ request objects làm chúng reachable qua roots dù request đã hết; GC không biết business muốn bỏ entry. Một stream object unreachable có thể được GC xử lý, nhưng file handle là resource cần release theo dispose contract, không dựa vào lúc collection xảy ra. Async cleanup có thể cần IAsyncDisposable khi resource API yêu cầu; method scope phải giữ resource đến operation completion.

## 7. Control flow

```text
Call async method → chạy sync đến await
→ awaited task completed? yes: nhận result và tiếp
→ no: lưu state, đăng ký continuation, trả Task cho caller
→ I/O completes → continuation runnable → resume/GetResult
→ return/fault/cancel → settle outer Task
```

Task.Run schedule CPU delegate vào pool; async keyword không tự parallel. Thread.Sleep giữ worker; Task.Delay biểu diễn timer completion. `.Result/.Wait` block caller; dưới tải có thể worker starvation khi continuations/work cần workers đang chờ. Deadlock là dependency cycle cụ thể, không mọi sync wait đều deadlock.

## 8. Lifetime / ownership / state

Operation owner phải await/observe và giữ dependency sống tới completion. Background jobs cần hosted lifecycle, own scope và durable handoff nếu phải sống qua crash; HTTP202 chỉ accepted theo contract. CancellationTokenSource owns registrations/timer và cần dispose khi hết; token là cooperative signal, callee phải observe. Cancellation xảy ra sau DB commit không undo dữ liệu; outcome unknown phải reconcile.

Lock bảo vệ critical state trong process; không giữ monitor qua await. SemaphoreSlim có async wait theo contract và release finally nếu đã acquired; lock process không giữ database replicas consistency.

## 9. Invariants

Không synchronous wait trên request async path nếu worker không cần giữ. Mỗi work có bounded concurrency, completion/error owner và valid resource scope. GC live objects không leak business retention vô hạn; native resources release đúng. Cancellation không bị biến thành success hoặc rollback claim sai. Async shared mutation vẫn cần atomic invariant.

## 10. Ví dụ tối thiểu

Fragment C#12/.NET8:

```csharp
static async Task<int> ReadLater(CancellationToken ct)
{
    await Task.Delay(20, ct);
    return 42;
}
```

Caller `await ReadLater(ct)` observe result/throw; cancellation trước completion dự đoán OperationCanceledException nếu Delay observes. CPU `for(...)` sau await vẫn chạy trên continuation thread, không parallelize tự động.

Pool model: W1 và W2 đều `.Wait()` child tasks queued vào same pool bị giới hạn hai workers → không child nào chạy. Pool actual có adaptation nên triệu chứng có thể latency/starvation thay deadlock vĩnh viễn; evidence queue/waits quyết định.

### Timeline cancellation không đồng nghĩa transaction rollback

**Mô hình dự đoán**: request bắt đầu → DB commit → client disconnect → token được signal → response write thất bại. Kết quả durable đã tồn tại; retry cần cùng intent/idempotency key để reconcile. Nếu exception handler biến mọi OperationCanceledException thành “chưa làm gì”, client có thể tạo duplicate.

Phân biệt caller cancellation, dependency timeout và application shutdown bằng token/context phù hợp; không cần log token secrets. Dispose CancellationTokenSource giải phóng registrations/timer nó sở hữu, không undo callee state. Kiểm tra cancellation trước CPU loop và ở checkpoints có bound; một loop không observe token sẽ tiếp tục chạy.

## 11. Failure modes

Sync-over-async làm latency queue tăng CPU thấp; async void fault mất caller catch; context capture tạo deadlock trong UI nếu caller block context cần cho continuation; cancellation ignored tiếp I/O; unbounded Task.Run bão CPU/allocations; static/event roots giữ managed objects. Fix await chain, bounded work, scope và observe failure theo mechanism.

## 12. Debug / observability

Collect queue length/completed-work trend, worker stack waits, dependency latency, CPU/wall và allocation rate cùng load. `dotnet-counters`, trace/dump theo version tool và process synthetic, không inspect production secrets. Discriminating experiment giữ dependency delay, đổi sync wait sang await rồi so queue/latency; chỉ CPU thấp chưa đủ kết luận pool. GC heap roots khác private bytes/native leak.

## 13. Liên hệ với bug/lab hiện có

[BE-10](../labs/backend/BE-10.md): caller completion owner; [BE-11](../labs/backend/BE-11.md): worker wait; [BE-12](../labs/backend/BE-12.md): propagate cancellation; [OS-09](../labs/os/OS-09.md): same-pool wait. [CoreModels](../examples/CoreModels/Program.cs) chỉ host model, không Kestrel/load proof.

## 14. Sai lầm thường gặp

Task ≠ Thread; async ≠ parallel; await ≠ new thread. ConfigureAwait(false) không universal cure cho server/starvation và không guarantee pool thread. Force GC không sửa root retention; tăng threads không sửa unbounded blocking design. Exception không observed không đồng nghĩa operation thành công.

## 15. Câu hỏi tự kiểm tra

1. Pending I/O Task có giữ một worker không? Đáp án: không bắt buộc.
2. Await completed Task có luôn đổi thread? Đáp án: không.
3. GC gen2 object còn reachable có bị thu vì request hết không? Đáp án: không.
4. Task.Run mọi I/O có giải pool starvation? Đáp án: không, có thể thêm work.
5. Cancel sau commit cần phản hồi gì? Đáp án: contract unknown/committed, reconcile.
6. Async code có race không? Đáp án: có, interleaving/shared state vẫn tồn tại.

## 16. Nguồn

[Managed execution](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process), [GC fundamentals](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals), [C# async](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/), [thread pool](https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool), [cancellation](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads). Docs cơ chế giữ trong phạm vi .NET8; profiler output cần version thực.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
