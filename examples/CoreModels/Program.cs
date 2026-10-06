static void Check(bool condition, string name)
{
    if (!condition) throw new Exception("FAIL " + name);
    Console.WriteLine("PASS " + name);
}

// Actual ASP.NET/MongoDB HTTP fixture: ../MongoApi/README.md.
// This file remains a process-local MODEL; see its original scope comments.

// Deterministic schedule: both callers read before either writes.
var bothRead = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
int readers = 0, unsafeStock = 1, successes = 0;
async Task UnsafeBuy()
{
    var seen = unsafeStock;
    if (Interlocked.Increment(ref readers) == 2) bothRead.SetResult();
    await bothRead.Task;
    if (seen > 0)
    {
        Interlocked.Exchange(ref unsafeStock, seen - 1);
        Interlocked.Increment(ref successes);
    }
}
await Task.WhenAll(UnsafeBuy(), UnsafeBuy());
Check(successes == 2 && unsafeStock == 0, "forced check-then-act failure");

int stock = 1;
bool ConditionalBuy() => Interlocked.CompareExchange(ref stock, 0, 1) == 1;
var results = await Task.WhenAll(Task.Run(ConditionalBuy), Task.Run(ConditionalBuy));
Check(results.Count(x => x) == 1 && stock == 0, "conditional single-item purchase");
// CAS represents a process-local atomic invariant, not MongoDB distributed behavior.

var gate = new object();
var records = new Dictionary<string, (string Payload, int Order)>();
var orders = 0;
int Create(string key, string payload)
{
    lock (gate)
    {
        if (records.TryGetValue(key, out var old))
        {
            if (old.Payload != payload) throw new InvalidOperationException("key conflict");
            return old.Order;
        }
        var id = ++orders;
        records.Add(key, (payload, id));
        return id;
    }
}
var replay = await Task.WhenAll(Task.Run(() => Create("userA:intent1","item1")),
                               Task.Run(() => Create("userA:intent1","item1")));
Check(orders == 1 && replay[0] == replay[1], "idempotency concurrent replay");
bool conflict = false;
try { Create("userA:intent1", "different"); }
catch (InvalidOperationException) { conflict = true; }
Check(conflict && orders == 1, "same key different payload rejected");

bool overflow = false;
try { var max = int.MaxValue; _ = checked(max + 1); }
catch (OverflowException) { overflow = true; }
Check(overflow, "checked arithmetic boundary (C# not C UB)");

using var cts = new CancellationTokenSource();
var pending = Task.Delay(TimeSpan.FromSeconds(30), cts.Token);
cts.Cancel();
bool cancelled = false;
try { await pending; }
catch (OperationCanceledException) { cancelled = true; }
Check(cancelled, "propagated cancellation");
