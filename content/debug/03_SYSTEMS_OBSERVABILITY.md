# Outline — Debug C/C++/Embedded: source, CPU, wire và scheduler

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Stale ELF, wrong core fault registers, optimized source variable assumptions, CPU watchpoint missed DMA, printf extends ISR, stack invalid makes fault decoder fault again, sanitizer changes race timing, analyzer wrong protocol mode. Fix evidence reliability plus root invariant, not claim 'debugger shows no bug'.

Đặt câu hỏi: cơ chế trong [Debug C/C++/Embedded: source, CPU, wire và scheduler](../../debug/03_SYSTEMS_OBSERVABILITY.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
warning/source contract → exact ELF/map/instruction path
→ target register/frame/memory snapshot
→ peripheral waveform + event/service timing
→ ISR/DMA/task owner transitions → first broken invariant
```

Not every case needs all tools. Suspected parser UB start host fixture; suspected baud capture wire; suspected priority inversion RTOS wait graph; fault symbolize exact PC but investigate producer write earlier.

## 3. Demo chạy thật

Claim có phạm vi: Symbols match image/core, frame validated before decode, measurement layer matches claim, instrumentation overhead/loss documented, synthetic scope. Sanitizer pass only paths executed; stack watermark observed not maximum proof; waveform correct doesn't prove buffer ownership.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../debug/03_SYSTEMS_OBSERVABILITY.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Stale ELF, wrong core fault registers, optimized source variable assumptions, CPU watchpoint missed DMA, printf extends ISR, stack invalid makes fault decoder fault again, sanitizer changes race timing, analyzer wrong protocol mode. Fix evidence reliability plus root invariant, not claim 'debugger shows no bug'.

Freeze artifact IDs→capture reset/fault context safely→check stack bounds/frame variant→symbolize PC→disassemble previous operations/caller→trace owner/source pointer→wire/scheduler measurement if hardware interaction. Force host bounds/error fixtures, then target burden needed explicitly; no mock output mislabeled measured.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[GDB breakpoints/watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Breakpoints.html), [GCC warnings](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html), [ASan](https://clang.llvm.org/docs/AddressSanitizer.html), [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html), [TSan](https://clang.llvm.org/docs/ThreadSanitizer.html), [CMSIS6 core](https://arm-software.github.io/CMSIS_6/v6.0.0/Core/index.html). Tool/target versions phải record khi thực hành.

1. Map proves stack max? Đáp án:no reserved region not dynamic peak.
2. ASan host proves DMA cache? Đáp án:no.
3. CPU watchpoint DMA write? Đáp án:depends debug system, no guarantee.
4. Fault PC different build ELF? Đáp án:invalid symbolization.
5. GPIO pulse handler duration equals event latency? Đáp án:no need event timestamp.
6. Scope vs analyzer? Đáp án:levels/rise/noise vs decoded edges.

[Index](../../00_INDEX.md) · [Content](../README.md).
