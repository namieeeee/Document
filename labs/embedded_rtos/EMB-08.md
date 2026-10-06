# BUG — EMB-08 — Register read-modify-write

**Educational reproduction — Mô phỏng để học.** Không phải documented production incident. Trigger/outcome dự đoán tách khỏi kết quả đã chạy ở [VALIDATION](../../VALIDATION.md). Giữ ID và mục tiêu bài cũ.

## Kiến thức nền

Đọc [cơ chế/flow/invariant: Systems05 — Peripheral là state machine phần cứng](../../embedded_systems/05_PERIPHERAL_STATE_MACHINES.md) và [debug methodology](../../debug/01_EVIDENCE_METHOD.md) trước bản sửa. Giải thích actor/owner/lifetime và vẽ flow theo bài nền, không chỉ học thuộc snippet.

Trước hết vẽ timeline CPU/IRQ/task và buffer. Chạy code thật cần board/core, manual, compiler, RTOS release/port; tên REG/IRQ/buffer trong snippet là ký hiệu, không địa chỉ hay API portable.

## Invariant

Register write chỉ acknowledge/change các bits được chủ ý theo manual.

## Bug

Snippet ngữ cảnh/pseudocode, không lệnh chạy độc lập; đặt trong handler/component/task tương ứng. Các helper không được định nghĩa là mô tả thao tác của fixture.

```text
REG = REG OR MASK với W1C bits
```

## Trigger

Fixture W1 C bit pending khi set config bit.

## Symptom

- Expected: giữ pending.
- Actual dự đoán: accidental clear.

## Root cause

Read-modify-write ghi lại bit1 vào W1 C và vô tình acknowledge event.

## Reproduction

1. Tạo fixture theo môi trường trên; reset state/resource trước mỗi lượt.
2. Fixture W1 C bit pending khi set config bit.
3. Ghi outcome và timeline trước khi đọc bản sửa. Với race, buộc thứ tự bằng barrier/delay theo trigger; chạy tuần tự không đủ.

## Evidence

Register semantics manual + observed write value. Chụp giá trị/status/ownership liên quan; nếu quan sát không khớp dự đoán, giữ evidence và kiểm lại điều kiện môi trường, không tuyên bố đã chứng minh root cause.

## Debug process

1. Ghi expected theo Invariant; capture raw input/status/ownership trước mapping hoặc fix.
2. Vẽ thứ tự actors từ Trigger; đối chiếu Root cause như giả thuyết cần chứng minh, không coi lời mô tả là evidence đã thu.
3. Dùng phép đo/phép thử nêu trong Evidence để phân biệt với nguyên nhân cạnh tranh trong bài nền. Giữ version/config và thay một yếu tố mỗi lượt.
4. Nếu quan sát không khớp dự đoán, ghi điều kiện khác và chưa kết luận. Khi xác nhận, tìm operation đầu phá invariant rồi chạy cùng fixture cho bản sửa.

## Fix

```text
Dedicatedset/clear registers hoặc maskedwrite đúngmanual
```

Áp dụng trong fixture có cùng input và invariant; ghi thêm API/phiên bản thực dùng khi chuyển pseudocode sang code. Tên helper trong bản sửa không phải API thư viện được bảo đảm tồn tại.

## Wrong fixes

RMW register như RAM và ghi lại pending W1 C bits. Các cách này không giữ invariant hoặc thay đổi guarantee/feature cần thiết. Có thể dùng một số cách như phép thử cô lập, không dùng làm bằng chứng permanent fix.

## Regression

Concurrent flags không clear ngoài ý định. Kiểm failure path và resource cleanup. Ghi before/after cùng fixture; test không tái hiện trigger gốc không đủ để chốt đã sửa.

## Source

[Nguồn và giải thích cơ chế của bài](../../embedded_systems/05_PERIPHERAL_STATE_MACHINES.md); [danh mục nguồn, phiên bản và giới hạn](../../REFERENCES.md). Nguồn giải thích cơ chế, không chứng minh fixture đã chạy. Register, timing, cache và RTOS port phải đối chiếu manual/config đúng target; chưa có board được xác minh.

[Index nhóm](README.md) · [Casebook](../../09_REAL_BUG_CASEBOOK.md).
