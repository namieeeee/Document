# Lab backend

Các ví dụ đều là mô phỏng. Snippet ngữ cảnh/pseudocode cần fixture ghi trong lab; chưa phải ứng dụng/firmware độc lập. Xem [validation](../../VALIDATION.md) trước khi coi một kết quả là đã chạy.

| ID | Lỗi |
|---|---|
| BE-01 | [Thiếu authorization](BE-01.md) |
| BE-02 | [BOLA](BE-02.md) |
| BE-03 | [Mass assignment](BE-03.md) |
| BE-04 | [Chỉ validate client](BE-04.md) |
| BE-05 | [JWT validation thiếu](BE-05.md) |
| BE-06 | [Refresh reuse](BE-06.md) |
| BE-07 | [Expiry race](BE-07.md) |
| BE-08 | [DI lifetime sai](BE-08.md) |
| BE-09 | [Singleton giữ user](BE-09.md) |
| BE-10 | [async void](BE-10.md) |
| BE-11 | [Sync over async](BE-11.md) |
| BE-12 | [Không propagate cancellation](BE-12.md) |
| BE-13 | [Retry tạo duplicate](BE-13.md) |
| BE-14 | [Idempotency key mới mỗi retry](BE-14.md) |
| BE-15 | [Check then act](BE-15.md) |
| BE-16 | [Lost update](BE-16.md) |
| BE-17 | [Pagination không ổn định](BE-17.md) |
| BE-18 | [Thiếu index](BE-18.md) |
| BE-19 | [Index order sai](BE-19.md) |
| BE-20 | [Query không bounded](BE-20.md) |
| BE-21 | [Cache thiếu tenant](BE-21.md) |
| BE-22 | [Swallow exception](BE-22.md) |
| BE-23 | [Thiếu correlation](BE-23.md) |
| BE-24 | [Secret trong log](BE-24.md) |
| BE-25 | [Secret trong Git](BE-25.md) |
| BE-26 | [Date thiếu timezone](BE-26.md) |
| BE-27 | [Serialization sai shape](BE-27.md) |
| BE-28 | [Status/error sai](BE-28.md) |
| BE-29 | [CORS rộng có credentials](BE-29.md) |
| BE-30 | [API abuse không giới hạn](BE-30.md) |
