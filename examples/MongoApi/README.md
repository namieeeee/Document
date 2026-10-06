# ASP.NET Core 8 + MongoDB concurrency fixture

API dùng MongoDB.Driver 3.5.0; database tên `document_fixture_<random GUID>`, chỉ dữ liệu giả. Một order document chứa key/payload/result; ví dụ không thực hiện inventory decrement và order creation trong một transaction.

- Conditional update: `_id` và `available > 0` cùng nằm trong filter; `$inc: -1` trả success khi `ModifiedCount == 1`.
- Unique index: hai request insert cùng key; một success, một HTTP 409, count trong DB bằng 1.
- Idempotency: tám concurrent requests cùng key/payload, retry và conflicting payload; tất cả replay hợp lệ trả cùng orderId, conflicting payload trả 409 và DB chứa một order.
- Bản lỗi buộc hai read trước write; hai purchases success khi stock ban đầu chỉ có một. Assert invariant success-count sẽ FAIL; test ghi outcome lỗi riêng.

## Native local run

Node không cần thiết. Cần Python 3.11, .NET SDK 8 và MongoDB Community 8.0.15 standalone executable:

```text
python examples/MongoApi/verify.py --mongod <absolute-path-to-mongod>
```

Runner build API, khởi động hai process ẩn, chỉ bind loopback, dùng MongoDB data directory tạm và dừng các process đã tạo. Không dùng database/service có sẵn. API endpoint không phải thiết kế deployment production.

## Docker Compose alternative

```text
cd examples/MongoApi
docker compose up --build --wait
python verify.py --external
docker compose down
```

Compose definition được cung cấp để CI chạy. Kết quả native và Docker phải được phân biệt; xem [summary](../../evidence/mongo-api/summary.json) và [raw verification](../../evidence/mongo-api/verification.log). Docker local chưa được chạy nếu không có engine; cung cấp workflow không tự chứng minh CI PASS.

Scope: standalone DB, một API instance, concurrency qua HTTP. Chưa kiểm chứng replica set, nhiều API instance, failover, majority write concern, distributed transactions, crash recovery hay idempotency cho external side effects. Không ngoại suy 20 lượt stress thành proof cho mọi schedule.

Nguồn: [MongoDB atomicity](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/), [unique indexes](https://www.mongodb.com/docs/v8.0/core/index-unique/), [C# driver](https://www.mongodb.com/docs/drivers/csharp/current/).

[Validation](../../VALIDATION.md) · [Index](../../00_INDEX.md).
