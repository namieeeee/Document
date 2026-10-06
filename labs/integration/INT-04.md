# BUG — INT-04 — Number/string lệch

**Educational reproduction — Mô phỏng để học.** Không phải documented production incident. Trigger/outcome dự đoán tách khỏi kết quả đã chạy ở [VALIDATION](../../VALIDATION.md). Giữ ID và mục tiêu bài cũ.

## Kiến thức nền

Đọc [cơ chế/flow/invariant: Web03 — TypeScript: mô hình tĩnh và dữ liệu thật](../../web/03_TYPESCRIPT_BOUNDARIES.md) và [debug methodology](../../debug/01_EVIDENCE_METHOD.md) trước bản sửa. Giải thích actor/owner/lifetime và vẽ flow theo bài nền, không chỉ học thuộc snippet.

Browser và API fixture .NET8 ở hai origin local; task 42 synthetic. Stub response/status/delay như trigger. Với cookie cần HTTPS local phù hợp, không đổi production policy.

## Invariant

Wire numeric type/range tương thích phép toán client.

## Bug

Snippet ngữ cảnh/pseudocode, không lệnh chạy độc lập; đặt trong handler/component/task tương ứng. Các helper không được định nghĩa là mô tả thao tác của fixture.

```text
FE '2'+1; BE count='2'
```

## Trigger

Fixture count string.

## Symptom

- Expected: 3.
- Actual dự đoán: số thành 21.

## Root cause

Wire type khác type phép toán client đang kỳ vọng.

## Reproduction

1. Tạo fixture theo môi trường trên; reset state/resource trước mỗi lượt.
2. Fixture count string.
3. Ghi outcome và timeline trước khi đọc bản sửa. Với race, buộc thứ tự bằng barrier/delay theo trigger; chạy tuần tự không đủ.

## Evidence

typeof payload; không blaming arithmetic alone. Chụp giá trị/status/ownership liên quan; nếu quan sát không khớp dự đoán, giữ evidence và kiểm lại điều kiện môi trường, không tuyên bố đã chứng minh root cause.

## Debug process

1. Ghi expected theo Invariant; capture raw input/status/ownership trước mapping hoặc fix.
2. Vẽ thứ tự actors từ Trigger; đối chiếu Root cause như giả thuyết cần chứng minh, không coi lời mô tả là evidence đã thu.
3. Dùng phép đo/phép thử nêu trong Evidence để phân biệt với nguyên nhân cạnh tranh trong bài nền. Giữ version/config và thay một yếu tố mỗi lượt.
4. Nếu quan sát không khớp dự đoán, ghi điều kiện khác và chưa kết luận. Khi xác nhận, tìm operation đầu phá invariant rồi chạy cùng fixture cho bản sửa.

## Fix

```text
Numeric wire field hoặc parse strict tại boundary
```

Áp dụng trong fixture có cùng input và invariant; ghi thêm API/phiên bản thực dùng khi chuyển pseudocode sang code. Tên helper trong bản sửa không phải API thư viện được bảo đảm tồn tại.

## Wrong fixes

Parse Int mọi input và chấp nhận truncated/NaN silently. Các cách này không giữ invariant hoặc thay đổi guarantee/feature cần thiết. Có thể dùng một số cách như phép thử cô lập, không dùng làm bằng chứng permanent fix.

## Regression

Wrong type/NaN/out of range reject. Kiểm failure path và resource cleanup. Ghi before/after cùng fixture; test không tái hiện trigger gốc không đủ để chốt đã sửa.

## Source

[Nguồn và giải thích cơ chế của bài](../../web/03_TYPESCRIPT_BOUNDARIES.md); [danh mục nguồn, phiên bản và giới hạn](../../REFERENCES.md). Nguồn giải thích cơ chế, không chứng minh fixture đã chạy.

[Index nhóm](README.md) · [Casebook](../../09_REAL_BUG_CASEBOOK.md).
