# Outline — MCU và memory-mapped I/O

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Wrong map/bus width, gate clock off, pin alternate function wrong, RMW clear event, reconfigure running engine, snapshot side-effect reads, invalid reserved bits. Fix correct manual sequence và owner, không arbitrary delay/volatile every variable.

Đặt câu hỏi: cơ chế trong [MCU và memory-mapped I/O](../../embedded_systems/13_MMIO_MCU.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Clock/reset enable→configure mux/rate/mode khi inactive→clear relevant stale events theo manual→enable engine/IRQ→hardware progresses→status/data→ack/recover. IRQ enable before state ready có thể call default/invalid owner. HAL functions wrap operations, không thay physical/clock/ownership contract.

## 3. Demo chạy thật

Claim có phạm vi: Address/width/region accessible target, clock/reset/config valid trước active, write semantics đúng, unrelated pending events không mất, one configuration owner. Reserved bits theo manual không assume always write0.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/13_MMIO_MCU.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Wrong map/bus width, gate clock off, pin alternate function wrong, RMW clear event, reconfigure running engine, snapshot side-effect reads, invalid reserved bits. Fix correct manual sequence và owner, không arbitrary delay/volatile every variable.

Manual access-type/clock tree/mux, register snapshot only safe-read fields, logic scope physical signals, bus/fault status/core exact. Compare software expects vs hardware state before/after one access. HAL debug stepping có observer effects.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html), [CMSIS6 core](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html). **Vendor verification còn thiếu:** RM0090 fetch failed, không cite nó như read evidence. Concepts general; electrical/register-specific implementation cần actual RM/errata.

1. CPU clock giống timer clock? Đáp án: no, tree/domains.
2. W1C OR RMW safe? Đáp án: có thể ack unrelated bits.
3. CPU mutex stops DMA? Đáp án: không.
4. HAL start success nghĩa wire completed? Đáp án: no.
5. Core manual đủ UART pin/address? Đáp án: vendor manual cần.

[Index](../../00_INDEX.md) · [Content](../README.md).
