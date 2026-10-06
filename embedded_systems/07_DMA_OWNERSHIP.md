# DMA: independent bus actor và ownership handoff

Phạm vi: generic DMA hardware; M4 no architectural D-cache maintenance recipe, M7 cache topic separated as comparison with CMSIS6. Target memory reachability/errata chưa chosen.

## 1. Mục tiêu học

Vẽ source/destination/count/trigger/complete state và ownership lifetime; tính reuse budget circular/double buffers, phân biệt memory complete/wire complete/coherency.

## 2. Kiến thức tiên quyết

[MMIO](13_MMIO_MCU.md), [interrupt](06_INTERRUPTS.md), [memory](02_MEMORY_BUILD.md), peripheral state machines.

## 3. Vấn đề mà cơ chế này giải quyết

CPU copying từng byte tốn instruction time; DMA bus master transfers khi triggers mà CPU làm việc khác. Actor độc lập vẫn tranh bus và đọc memory ngoài function scope, cần quiescence/ownership/cache contracts.

## 4. Khái niệm

CPU copy thực thi load/store instructions dưới control flow CPU. DMA engine nhận source/destination/length/mode, rồi thực hiện transfers qua bus khi có request/trigger theo device. CPU có thể làm công việc khác nhưng bus vẫn chịu contention. DMA không “copy ngay khi gọi start”; completion/error status quyết định operation xong tới mức nào theo engine/peripheral. DMA memory-complete có thể khác peripheral wire-complete.

Flow: software validate buffer/region/alignment → configure khi engine state cho phép → handoff/start → DMA owns transfer regions → IRQ/poll completion/error → reclaim sau status đúng. Interrupt là notification, buffer lifetime phải được bảo đảm ngay cả khi completion trễ hoặc cancel/error. Local automatic buffer không được trả scope trong khi DMA còn refer.

## 5. Thành phần bên trong

Engine source/destination addresses, increment modes, transfer width/count, peripheral request handshake, arbitration/errors/interrupts. Memory-to-peripheral destination fixed data register/source advance; peripheral-to-memory inverse; exact support manual. Transfer count can count elements not bytes; validate width/count multiplication overflow.

## 6. Data representation

```text
FREE → CPU_FILL → DMA_TX_OWNED → DONE → FREE
FREE → DMA_RX_OWNED → DONE → CPU_CONSUME → FREE
```

TX buffer không bị CPU thay khi DMA đang đọc; RX buffer không bị CPU đọc như frame hoàn chỉnh khi DMA đang ghi. Transfer start/completion phải bao ownership transitions; errors/cancel cần policy khi nào engine thật ngừng access. Một token state không đủ nếu caller có raw pointer và bypass protocol.

Circular DMA quay lại vùng memory, không chờ consumer tự nguyện xong. Half/full transfer events là mốc producer tiến, không guarantee consumer đủ nhanh. Double buffer cũng không tự safe: consumer3 ms, producer quay lại mỗi2 ms thì vùng cũ bị overwrite. Đo worst-case service time/capacity và chọn backpressure/drop/extra-buffer policy. Sequence/generation giúp phát hiện overrun, không tự ngăn overwrite.

### Giao thức ownership cho một buffer

| State | CPU được làm gì? | DMA được làm gì? | Transition |
|---|---|---|---|
| FREE | Claim buffer | Không access | CPU claim |
| CPU_FILL | Ghi payload/length | Không access | Publish và start |
| DMA_OWNED | Không sửa/giải phóng payload | Đọc/ghi theo direction | Completion hoặc abort đã quiesce |
| CPU_CONSUME | Đọc RX hoặc thu hồi TX | Không còn access | Release về FREE |

Completion flag phải gắn với đúng transfer generation. Một callback trễ của transfer cũ không được free buffer mà transfer mới đang dùng. Disable một request source chưa chứng minh DMA đã ngừng mọi bus access; abort cần sequence và completion contract của engine.

Với circular RX, DMA vẫn sở hữu vùng nó đang ghi. Half/full notifications chỉ xác định một window để CPU đọc nửa vừa hoàn tất trước khi DMA quay lại. Nếu CPU chậm hơn window, tăng semaphore count không lưu được bytes đã bị ghi đè; cần capacity/drop policy hoặc copy sang owner riêng.

## 7. Control flow

Validate regions/length/alignment/live storage→stop/config when allowed→prepare cache/order if target needs→handoff/start→hardware transfers→complete/error→verify quiescent/peripheral wire state→reclaim. Cancel request isn't reclaim permission until engine stops references. Circular half/full events expose completed region before producer revisits it, not indefinite snapshot.

## 8. Lifetime / ownership / state

TX buffer immutable through DMA reads; RX CPU consume only finished region; pointers/tokens carry generation to reject late completion on recycled slot. Error path may partial data, no full frame publish. Double buffer producer revisit period imposes hard service bound; if consumer delayed beyond bound use extra pool/drop/backpressure per system.

## 9. Invariants

Storage accessible/aligned/live through last transfer; one writer/owner, correct count/width, completed coherent data only published, no reuse before reclaim. Cache/RAM publication correct per target; CPU lock not DMA synchronization.

## 10. Ví dụ tối thiểu

**Model** DMA fills A/B alternately every2ms, CPU consume takes3ms worst: A completed t2, CPU done t5, DMA starts A reuse t4→overlap1ms. Two buffers do not satisfy invariant. Need adjust rate/service/storage/full policy, sequence detects loss but doesn't stop overwrite.

### Coherence và lifetime là hai phép kiểm tra độc lập

**Mô hình TX**: CPU viết payload B vào cache; RAM còn A. Buffer không bị tái sử dụng nhưng DMA đọc A → ownership đúng, coherence sai. Clean đúng vùng trước handoff giải trường hợp này theo target recipe.

Trường hợp khác: RAM đã có B, DMA bắt đầu đọc, CPU sửa thành C trước completion. Không có stale cache vẫn có thể gửi hỗn hợp B/C → coherence không thay ownership.

Cache maintenance thường thao tác theo cache line. Nếu payload chia sẻ dirty line với state khác, invalidate line có thể mất CPU writes ngoài payload. Alignment và padding để tách line là một phần layout contract, không merely optimization. Với M4 tham chiếu không có D-cache, không thêm cache API M7 vào fix; vẫn cần memory reachability, bus ordering và completion theo MCU manual.

## 11. Failure modes

CPU cache có thể giữ bytes chưa ghi RAM; DMA đọc RAM thấy bản cũ. TX clean trước handoff làm data phù hợp cho DMA theo target contract. RX DMA ghi RAM trong khi CPU cache còn dữ liệu cũ; invalidate đúng timing/hướng để CPU thấy mới. Invalidate dirty line không đúng có thể làm mất CPU writes; sharing line với dữ liệu khác cần isolation/alignment và recipe manual. [CMSIS6.0 cache implementation](https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.0.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h).

Compiler barrier, CPU memory barrier và cache maintenance không thay nhau: một cái ảnh hưởng optimization/order, một cái ordering/visibility theo architecture, một cái cache contents. Không cache target vẫn có lifetime/ownership/race. Memory region nào DMA access được, alignment/length và coherency guarantee phải từ MCU manual/errata chưa chọn. Chưa có board nên không đưa address hay declare buffers “DMA safe” chỉ bằng macro alignment.

Invariant: region accessible/aligned, lifetime dài hơn transfer, một owner writer đúng lúc, completion thật trước reuse, cache/RAM phù hợp theo hardware. Software test model kiểm ownership chứ không bus/cache ordering.

Buffer lifetime/reuse race exists even no cache. Transfer alignment/region inaccessible error differs cache stale data, separate evidence.

## 12. Debug / observability

- **SYMPTOM:** prefixF1/suffixF2 hoặc gửi lại bytes cũ dù CPU buffer mới.
- **EVIDENCE:** captured bytes, owner/generation, DMA status, completion timestamps, CPU writes, cache enabled/region policy.
- **POSSIBLE CAUSES:** buffer reuse, lifetime, partial transfer/error, wrong region/alignment hoặc cache coherence.
- **DISTINGUISHING TEST:** giữ buffer bất biến tới completion để phân biệt race; cache-controlled isolated experiment đúng manual để phân biệt visibility. Không tắt cache rồi gọi permanent fix.
- **ROOT CAUSE:** owner/lifetime vi phạm nếu immutable buffer giải quyết với cùng config; coherence chỉ kết luận khi cache/RAM evidence hỗ trợ.
- **FIX:** ownership state/pool và error handshake; target correct clean/invalidate/region policy.
- **WRONG FIX:** volatile buffer, sleep chờ đoán completion, double buffer không full policy, invalidate mọi memory.
- **REGRESSION TEST:** late completion, producer burst, error/cancel/full buffers, line boundary và cache target actual.

## 13. Liên hệ với bug/lab hiện có

[EMB-11](../labs/embedded_rtos/EMB-11.md), [EMB-12](../labs/embedded_rtos/EMB-12.md), [EMB-13](../labs/embedded_rtos/EMB-13.md), [EMB-14](../labs/embedded_rtos/EMB-14.md), [EMB-15](../labs/embedded_rtos/EMB-15.md). Python model tests owner only, not bus/coherence proof.

## 14. Sai lầm thường gặp

Volatile buffer≠cache clean; compiler barrier≠CPU ordering≠cache maintenance; DMA completion≠last UART/SPI bit sent; aligned macro≠DMA accessible region; sleep≠quiescence handshake.

## 15. Câu hỏi tự kiểm tra

1. DMA runs while CPU locked? Đáp án: can.
2. Count16 transfers width2 nghĩa16bytes? Đáp án: often32bytes per stated count convention.
3. Double buffer automatic safe? Đáp án: no revisit/service bound.
4. Error done returns full frame? Đáp án: partial/error state must classify.
5. M4 compare M7 clean/invalidate use same? Đáp án: no target capabilities.

## 16. Nguồn

[ST AN4839 Rev2 — cache trên STM32F7/H7](https://www.st.com/resource/en/application_note/DM00272913-.pdf). Đây là đối chiếu cache cho M7, không gán D-cache vào M4. Trang API D-cache CMSIS6.0 không trả nội dung; đã đọc header cache đúng tag 6.0 thay thế, không dùng latest làm authority. Actual DMA engine/manual chưa khóa, không bảo đảm địa chỉ hoặc maintenance sequence cho target cụ thể.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
