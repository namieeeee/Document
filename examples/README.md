# Ví dụ chạy độc lập

## React renderer fixture

[React race: bản lỗi và bản sửa](react-race/README.md) dùng React DOM, Vitest và Testing Library thật. Bản lỗi FAIL khi A về sau B; bản sửa PASS với cùng invariant. [Log và phiên bản](../evidence/react-race/summary.json) ghi kết quả đã chạy. Phạm vi là jsdom với Promise fixture, chưa phải HTTP/browser integration. Backend ASP.NET/MongoDB còn [BLOCKED](../audit/PHASE_STATUS.md).

## Host models

Không cần cài React/MongoDB/RTOS để chạy ba bộ này. Đây là **mô hình cơ chế** và test core language, không thay integration test/framework/board. Chạy từ thư mục `examples`:

```powershell
node web_models.mjs
python systems_models.py
dotnet run --project CoreModels/CoreModels.csproj
```

Node: snapshot queue, response race với deferred promise, stale rollback, runtime shape, tiền minor-unit, event-loop blocking. Python: buffer ownership, queue overflow policy, tick wrap, file lifecycle và retention. .NET: lost update với barrier, conditional update, idempotency, checked arithmetic, cancellation.

Đọc code và tự dự đoán assertions trước chạy. Mỗi test kiểm một invariant độc lập; demo lỗi phải cho outcome sai được dự đoán, bản sửa phải giữ expected. Không dùng race ngẫu nhiên làm bằng chứng duy nhất. Các file chỉ dùng dữ liệu giả và thư mục temp được quản lý bởi standard library.

Các lab liên quan: [FE-05](../labs/frontend/FE-05.md), [BE-15](../labs/backend/BE-15.md), [INT-16](../labs/integration/INT-16.md), [EMB-30](../labs/embedded_rtos/EMB-30.md), [OS-08](../labs/os/OS-08.md). [Kết quả thực](../VALIDATION.md).
