# Outline — .NET: IL/JIT/GC và async continuations

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Sync-over-async làm latency queue tăng CPU thấp; async void fault mất caller catch; context capture tạo deadlock trong UI nếu caller block context cần cho continuation; cancellation ignored tiếp I/O; unbounded Task.Run bão CPU/allocations; static/event roots giữ managed objects. Fix await chain, bounded work, scope và observe failure theo mechanism.

Đặt câu hỏi: cơ chế trong [.NET: IL/JIT/GC và async continuations](../../web/14_DOTNET_ASYNC_RUNTIME.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Call async method → chạy sync đến await
→ awaited task completed? yes: nhận result và tiếp
→ no: lưu state, đăng ký continuation, trả Task cho caller
→ I/O completes → continuation runnable → resume/GetResult
→ return/fault/cancel → settle outer Task
```

Task.Run schedule CPU delegate vào pool; async keyword không tự parallel. Thread.Sleep giữ worker; Task.Delay biểu diễn timer completion. `.Result/.Wait` block caller; dưới tải có thể worker starvation khi continuations/work cần workers đang chờ. Deadlock là dependency cycle cụ thể, không mọi sync wait đều deadlock.

## 3. Demo chạy thật

Claim có phạm vi: Token cancellation được truyền tới Task.Delay và được quan sát trong fixture.

```text
dotnet run --project examples/CoreModels/CoreModels.csproj -c Release
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/core.log):

```text
PASS propagated cancellation
```

## 4. Cách nó hỏng và cách phát hiện

Sync-over-async làm latency queue tăng CPU thấp; async void fault mất caller catch; context capture tạo deadlock trong UI nếu caller block context cần cho continuation; cancellation ignored tiếp I/O; unbounded Task.Run bão CPU/allocations; static/event roots giữ managed objects. Fix await chain, bounded work, scope và observe failure theo mechanism.

Collect queue length/completed-work trend, worker stack waits, dependency latency, CPU/wall và allocation rate cùng load. `dotnet-counters`, trace/dump theo version tool và process synthetic, không inspect production secrets. Discriminating experiment giữ dependency delay, đổi sync wait sang await rồi so queue/latency; chỉ CPU thấp chưa đủ kết luận pool. GC heap roots khác private bytes/native leak.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[Managed execution](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process), [GC fundamentals](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals), [C# async](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/), [thread pool](https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool), [cancellation](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads). Docs cơ chế giữ trong phạm vi .NET8; profiler output cần version thực.

1. Pending I/O Task có giữ một worker không? Đáp án: không bắt buộc.
2. Await completed Task có luôn đổi thread? Đáp án: không.
3. GC gen2 object còn reachable có bị thu vì request hết không? Đáp án: không.
4. Task.Run mọi I/O có giải pool starvation? Đáp án: không, có thể thêm work.
5. Cancel sau commit cần phản hồi gì? Đáp án: contract unknown/committed, reconcile.
6. Async code có race không? Đáp án: có, interleaving/shared state vẫn tồn tại.

[Index](../../00_INDEX.md) · [Content](../README.md).
