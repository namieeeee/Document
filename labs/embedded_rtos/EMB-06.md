# BUG — EMB-06 — IRQ priority sai RTOS

**Educational reproduction — Mô phỏng để học.** Không phải documented production incident. Trigger/outcome dự đoán tách khỏi kết quả đã chạy ở [VALIDATION](../../VALIDATION.md). Giữ ID và mục tiêu bài cũ.

## Kiến thức nền

Đọc [cơ chế/flow/invariant: Systems06 — Interrupt: chuyển control flow, giữ invariant](../../embedded_systems/06_INTERRUPTS.md) và [debug methodology](../../debug/01_EVIDENCE_METHOD.md) trước bản sửa. Giải thích actor/owner/lifetime và vẽ flow theo bài nền, không chỉ học thuộc snippet.

Trước hết vẽ timeline CPU/IRQ/task và buffer. Chạy code thật cần board/core, manual, compiler, RTOS release/port; tên REG/IRQ/buffer trong snippet là ký hiệu, không địa chỉ hay API portable.

## Invariant

IRQ gọi kernel API đúng context/urgency threshold theo port.

## Bug

Snippet ngữ cảnh/pseudocode, không lệnh chạy độc lập; đặt trong handler/component/task tương ứng. Các helper không được định nghĩa là mô tả thao tác của fixture.

```text
IRQurgency cao gọi API RTOS tráiport
```

## Trigger

Configure IRQ ngoài ngưỡng syscall port.

## Symptom

- Expected: đúng contract.
- Actual dự đoán: assert/corruption possible.

## Root cause

ISR urgency nằm ngoài ngưỡng được phép gọi kernel API theo port.

## Reproduction

1. Tạo fixture theo môi trường trên; reset state/resource trước mỗi lượt.
2. Configure IRQ ngoài ngưỡng syscall port.
3. Ghi outcome và timeline trước khi đọc bản sửa. Với race, buộc thứ tự bằng barrier/delay theo trigger; chạy tuần tự không đủ.

## Evidence

Config priority bits và port restriction, không assert mọi boardcrash. Chụp giá trị/status/ownership liên quan; nếu quan sát không khớp dự đoán, giữ evidence và kiểm lại điều kiện môi trường, không tuyên bố đã chứng minh root cause.

## Debug process

1. Ghi expected theo Invariant; capture raw input/status/ownership trước mapping hoặc fix.
2. Vẽ thứ tự actors từ Trigger; đối chiếu Root cause như giả thuyết cần chứng minh, không coi lời mô tả là evidence đã thu.
3. Dùng phép đo/phép thử nêu trong Evidence để phân biệt với nguyên nhân cạnh tranh trong bài nền. Giữ version/config và thay một yếu tố mỗi lượt.
4. Nếu quan sát không khớp dự đoán, ghi điều kiện khác và chưa kết luận. Khi xác nhận, tìm operation đầu phá invariant rồi chạy cùng fixture cho bản sửa.

## Fix

```text
ĐưaIRQ vào allowedrange hoặc defer signal
```

Áp dụng trong fixture có cùng input và invariant; ghi thêm API/phiên bản thực dùng khi chuyển pseudocode sang code. Tên helper trong bản sửa không phải API thư viện được bảo đảm tồn tại.

## Wrong fixes

Disable kernel assert hoặc đổi priority số mà không hiểu encoding/threshold. Các cách này không giữ invariant hoặc thay đổi guarantee/feature cần thiết. Có thể dùng một số cách như phép thử cô lập, không dùng làm bằng chứng permanent fix.

## Regression

Maxnest và FromISR APIs theo release port. Kiểm failure path và resource cleanup. Ghi before/after cùng fixture; test không tái hiện trigger gốc không đủ để chốt đã sửa.

## Source

[Nguồn và giải thích cơ chế của bài](../../embedded_systems/06_INTERRUPTS.md); [danh mục nguồn, phiên bản và giới hạn](../../REFERENCES.md). Nguồn giải thích cơ chế, không chứng minh fixture đã chạy. Register, timing, cache và RTOS port phải đối chiếu manual/config đúng target; chưa có board được xác minh.

[Index nhóm](README.md) · [Casebook](../../09_REAL_BUG_CASEBOOK.md).
