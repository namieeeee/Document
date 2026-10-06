# Outline — Virtual memory: pages, faults, heap và mappings

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Unmapped/protection fault, UAF still mapped so no fault despite invalid lifetime, stack guard hit, COW surprise memory pressure, mmap bounds/truncated file SIGBUS cases, allocator fragmentation/retention. Increasing swap/RAM doesn't fix source UAF.

Đặt câu hỏi: cơ chế trong [Virtual memory: pages, faults, heap và mappings](../../os/02_VIRTUAL_MEMORY.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Reserve/map address range→first touch→fault if demand backed→physical frame init/map→retry access. Mmap anonymous/file/shared/private choose backing/sharing. MAP_PRIVATE changes can COW not write back file; file truncation or invalid mapping access có distinct failures. Munmap removes mapping, later pointer invalid.

## 3. Demo chạy thật

Claim có phạm vi: Access permitted mapped region and live object, mapping/offset bounds đúng; process virtual pointer not transferable như physical address to DMA/device. Backing lifecycle/sharing aware, allocator live-byte counts and RSS interpreted separately. Page-fault handler success not pointer semantics proof.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../os/02_VIRTUAL_MEMORY.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Unmapped/protection fault, UAF still mapped so no fault despite invalid lifetime, stack guard hit, COW surprise memory pressure, mmap bounds/truncated file SIGBUS cases, allocator fragmentation/retention. Increasing swap/RAM doesn't fix source UAF.

Maps/permissions/resident metrics/page-fault counts, heap allocation profile, native leak sanitizer, page tables/kernel docs when needed. Distinguish minor/major faults and steady-state cold load; snapshot virtual size/RSS alone insufficient. Controlled touch/free/mapping experiment expected trends no fixed bytes proof.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[OSTEP paging](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf), [TLB](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf), [Linux memory concepts](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html), [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), [proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html). Kernel docs rolling, layout not fixed release implementation.

1. Offset for4KiB page? Đáp án:12bits.
2. TLB miss valid page table? Đáp án:translation walk, not necessarily page fault.
3. Close mapped fd unmaps? Đáp án:no.
4. UAF no fault still correct? Đáp án:no source lifetime violation.
5. High VSZ leak proof? Đáp án:no reservations/mappings need inspect.
6. Private file mapping writes persist? Đáp án:not as shared file write guarantee.

[Index](../../00_INDEX.md) · [Content](../README.md).
