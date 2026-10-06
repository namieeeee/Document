using MongoDB.Bson;
using MongoDB.Driver;
using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var host = Environment.GetEnvironmentVariable("MONGO_HOST") ?? "127.0.0.1";
if (host != "127.0.0.1" && host != "mongo") throw new InvalidOperationException("Fixture hosts only");
var port = host == "mongo" ? 27017 : 27029;
var client = new MongoClient($"mongodb://{host}:{port}/?serverSelectionTimeoutMS=3000");
var db = client.GetDatabase("document_fixture_" + Guid.NewGuid().ToString("N"));
var stock = db.GetCollection<BsonDocument>("stock");
var items = db.GetCollection<BsonDocument>("items");
var orders = db.GetCollection<BsonDocument>("orders");
foreach (var col in new[] { items, orders })
    await col.Indexes.CreateOneAsync(new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys.Ascending("key"), new CreateIndexOptions { Unique = true }));
var gates = new ConcurrentDictionary<string, ReadGate>();

app.MapGet("/health", () => Results.Ok(new { database = db.DatabaseNamespace.DatabaseName }));
app.MapPut("/stock/{id}", async (string id) => {
    await stock.InsertOneAsync(new BsonDocument { { "_id", id }, { "available", 1 } });
    return Results.Ok();
});
app.MapGet("/stock/{id}", async (string id) => {
    var doc = await stock.Find(new BsonDocument("_id", id)).FirstAsync();
    return Results.Ok(new { available = doc["available"].AsInt32 });
});
app.MapPost("/buy/{id}", async (string id) => {
    var filter = new BsonDocument { { "_id", id }, { "available", new BsonDocument("$gt", 0) } };
    var result = await stock.UpdateOneAsync(filter, new BsonDocument("$inc", new BsonDocument("available", -1)));
    return result.ModifiedCount == 1 ? Results.Ok(new { purchased = true }) : Results.Conflict(new { purchased = false });
});
// Educational broken implementation. A two-request gate forces both reads
// before either write; it is not a random timing experiment.
app.MapPost("/unsafe/buy/{id}", async (string id) => {
    var doc = await stock.Find(new BsonDocument("_id", id)).FirstAsync();
    var gate = gates.GetOrAdd(id, _ => new ReadGate());
    if (Interlocked.Increment(ref gate.Readers) == 2) gate.Ready.TrySetResult();
    await gate.Ready.Task.WaitAsync(TimeSpan.FromSeconds(10));
    if (doc["available"].AsInt32 <= 0) return Results.Conflict();
    await stock.UpdateOneAsync(new BsonDocument("_id", id),
        new BsonDocument("$set", new BsonDocument("available", doc["available"].AsInt32 - 1)));
    return Results.Ok(new { purchased = true });
});
app.MapPost("/items/{key}", async (string key) => {
    try { await items.InsertOneAsync(new BsonDocument { { "key", key } }); return Results.Ok(); }
    catch (MongoWriteException e) when (e.WriteError.Category == ServerErrorCategory.DuplicateKey) { return Results.Conflict(); }
});
app.MapGet("/items/{key}", async (string key) => Results.Ok(new {
    count = await items.CountDocumentsAsync(new BsonDocument("key", key)) }));
app.MapPost("/orders/{key}", async (string key, OrderRequest request) => {
    if (string.IsNullOrWhiteSpace(request.Payload)) return Results.BadRequest();
    var orderId = Guid.NewGuid().ToString("N");
    try {
        await orders.InsertOneAsync(new BsonDocument { { "key", key }, { "payload", request.Payload }, { "orderId", orderId } });
    } catch (MongoWriteException e) when (e.WriteError.Category == ServerErrorCategory.DuplicateKey) {
        var existing = await orders.Find(new BsonDocument("key", key)).FirstAsync();
        if (existing["payload"].AsString != request.Payload) return Results.Conflict();
        orderId = existing["orderId"].AsString;
    }
    return Results.Ok(new { orderId });
});
app.MapGet("/orders/{key}", async (string key) => Results.Ok(new {
    count = await orders.CountDocumentsAsync(new BsonDocument("key", key)) }));
await app.RunAsync();

record OrderRequest(string Payload);
sealed class ReadGate {
    public int Readers;
    public TaskCompletionSource Ready { get; } = new(TaskCreationOptions.RunContinuationsAsynchronously);
}
