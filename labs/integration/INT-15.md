# BUG — INT-15 — Expiry giữa nhiều request

**Educational reproduction — Mô phỏng để học.** Không phải documented production incident. Trigger/outcome dự đoán tách khỏi kết quả đã chạy ở [VALIDATION](../../VALIDATION.md). Giữ ID và mục tiêu bài cũ.

## Kiến thức nền

Đọc [cơ chế/flow/invariant: Web10 — Identity, credentials và quyền](../../web/10_IDENTITY_SECURITY.md) và [debug methodology](../../debug/01_EVIDENCE_METHOD.md) trước bản sửa. Giải thích actor/owner/lifetime và vẽ flow theo bài nền, không chỉ học thuộc snippet.

Browser và API fixture .NET8 ở hai origin local; task 42 synthetic. Stub response/status/delay như trigger. Với cookie cần HTTPS local phù hợp, không đổi production policy.

## Invariant

Response401 cũ không xóa session mới hơn.

## Bug

Snippet ngữ cảnh/pseudocode, không lệnh chạy độc lập; đặt trong handler/component/task tương ứng. Các helper không được định nghĩa là mô tả thao tác của fixture.

```text
RequestA tokenold, B tokennew, A401 logout
```

## Trigger

Delay A tới sau successful refresh.

## Symptom

- Expected: giữ session mới.
- Actual dự đoán: A xóa session.

## Root cause

Response401 cũ được phép xóa session mới hơn.

## Reproduction

1. Tạo fixture theo môi trường trên; reset state/resource trước mỗi lượt.
2. Delay A tới sau successful refresh.
3. Ghi outcome và timeline trước khi đọc bản sửa. Với race, buộc thứ tự bằng barrier/delay theo trigger; chạy tuần tự không đủ.

## Evidence

Time line token generation/token ownership. Chụp giá trị/status/ownership liên quan; nếu quan sát không khớp dự đoán, giữ evidence và kiểm lại điều kiện môi trường, không tuyên bố đã chứng minh root cause.

## Debug process

1. Ghi expected theo Invariant; capture raw input/status/ownership trước mapping hoặc fix.
2. Vẽ thứ tự actors từ Trigger; đối chiếu Root cause như giả thuyết cần chứng minh, không coi lời mô tả là evidence đã thu.
3. Dùng phép đo/phép thử nêu trong Evidence để phân biệt với nguyên nhân cạnh tranh trong bài nền. Giữ version/config và thay một yếu tố mỗi lượt.
4. Nếu quan sát không khớp dự đoán, ghi điều kiện khác và chưa kết luận. Khi xác nhận, tìm operation đầu phá invariant rồi chạy cùng fixture cho bản sửa.

## Fix

```text
401cũ chỉ xử lý nếu còn current generation
```

Áp dụng trong fixture có cùng input và invariant; ghi thêm API/phiên bản thực dùng khi chuyển pseudocode sang code. Tên helper trong bản sửa không phải API thư viện được bảo đảm tồn tại.

## Wrong fixes

401 từ generation nào cũng logout toàn session. Các cách này không giữ invariant hoặc thay đổi guarantee/feature cần thiết. Có thể dùng một số cách như phép thử cô lập, không dùng làm bằng chứng permanent fix.

## Regression

Stale401 không xóa credentials mới. Kiểm failure path và resource cleanup. Ghi before/after cùng fixture; test không tái hiện trigger gốc không đủ để chốt đã sửa.

## Source

[Nguồn và giải thích cơ chế của bài](../../web/10_IDENTITY_SECURITY.md); [danh mục nguồn, phiên bản và giới hạn](../../REFERENCES.md). Nguồn giải thích cơ chế, không chứng minh fixture đã chạy.

[Index nhóm](README.md) · [Casebook](../../09_REAL_BUG_CASEBOOK.md).
