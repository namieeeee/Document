# Outline — DMA: independent bus actor và ownership handoff

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

CPU cache có thể giữ bytes chưa ghi RAM; DMA đọc RAM thấy bản cũ. TX clean trước handoff làm data phù hợp cho DMA theo target contract. RX DMA ghi RAM trong khi CPU cache còn dữ liệu cũ; invalidate đúng timing/hướng để CPU thấy mới. Invalidate dirty line không đúng có thể làm mất CPU writes; sharing line với dữ liệu khác cần isolation/alignment và recipe manual. [CMSIS6.0 cache implementation](https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.0.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h).

Đặt câu hỏi: cơ chế trong [DMA: independent bus actor và ownership handoff](../../embedded_systems/07_DMA_OWNERSHIP.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Validate regions/length/alignment/live storage→stop/config when allowed→prepare cache/order if target needs→handoff/start→hardware transfers→complete/error→verify quiescent/peripheral wire state→reclaim. Cancel request isn't reclaim permission until engine stops references. Circular half/full events expose completed region before producer revisits it, not indefinite snapshot.

## 3. Demo chạy thật

Claim có phạm vi: Python handoff giữ reference tới buffer mutable, khác immutable snapshot; không mô phỏng cache/DMA hardware.

```text
python examples/systems_models.py
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/systems.log):

```text
PASS queued buffer reference vs immutable snapshot
```

## 4. Cách nó hỏng và cách phát hiện

CPU cache có thể giữ bytes chưa ghi RAM; DMA đọc RAM thấy bản cũ. TX clean trước handoff làm data phù hợp cho DMA theo target contract. RX DMA ghi RAM trong khi CPU cache còn dữ liệu cũ; invalidate đúng timing/hướng để CPU thấy mới. Invalidate dirty line không đúng có thể làm mất CPU writes; sharing line với dữ liệu khác cần isolation/alignment và recipe manual. [CMSIS6.0 cache implementation](https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.0.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h).

Compiler barrier, CPU memory barrier và cache maintenance không thay nhau: một cái ảnh hưởng optimization/order, một cái ordering/visibility theo architecture, một cái cache contents. Không cache target vẫn có lifetime/ownership/race. Memory region nào DMA access được, alignment/length và coherency guarantee phải từ MCU manual/errata chưa chọn. Chưa có board nên không đưa address hay declare buffers “DMA safe” chỉ bằng macro alignment.

Invariant: region accessible/aligned, lifetime dài hơn transfer, một owner writer đúng lúc, completion thật trước reuse, cache/RAM phù hợp theo hardware. Software test model kiểm ownership chứ không bus/cache ordering.

Buffer lifetime/reuse race exists even no cache. Transfer alignment/region inaccessible error differs cache stale data, separate evidence.

- **SYMPTOM:** prefixF1/suffixF2 hoặc gửi lại bytes cũ dù CPU buffer mới.
- **EVIDENCE:** captured bytes, owner/generation, DMA status, completion timestamps, CPU writes, cache enabled/region policy.
- **POSSIBLE CAUSES:** buffer reuse, lifetime, partial transfer/error, wrong region/alignment hoặc cache coherence.
- **DISTINGUISHING TEST:** giữ buffer bất biến tới completion để phân biệt race; cache-controlled isolated experiment đúng manual để phân biệt visibility. Không tắt cache rồi gọi permanent fix.
- **ROOT CAUSE:** owner/lifetime vi phạm nếu immutable buffer giải quyết với cùng config; coherence chỉ kết luận khi cache/RAM evidence hỗ trợ.
- **FIX:** ownership state/pool và error handshake; target correct clean/invalidate/region policy.
- **WRONG FIX:** volatile buffer, sleep chờ đoán completion, double buffer không full policy, invalidate mọi memory.
- **REGRESSION TEST:** late completion, producer burst, error/cancel/full buffers, line boundary và cache target actual.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[ST AN4839 Rev2 — cache trên STM32F7/H7](https://www.st.com/resource/en/application_note/DM00272913-.pdf). Đây là đối chiếu cache cho M7, không gán D-cache vào M4. Trang API D-cache CMSIS6.0 không trả nội dung; đã đọc header cache đúng tag 6.0 thay thế, không dùng latest làm authority. Actual DMA engine/manual chưa khóa, không bảo đảm địa chỉ hoặc maintenance sequence cho target cụ thể.

1. DMA runs while CPU locked? Đáp án: can.
2. Count16 transfers width2 nghĩa16bytes? Đáp án: often32bytes per stated count convention.
3. Double buffer automatic safe? Đáp án: no revisit/service bound.
4. Error done returns full frame? Đáp án: partial/error state must classify.
5. M4 compare M7 clean/invalidate use same? Đáp án: no target capabilities.

[Index](../../00_INDEX.md) · [Content](../README.md).
