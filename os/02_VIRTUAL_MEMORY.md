# Virtual memory: pages, faults, heap và mappings

Phạm vi: Linux/MMU conceptual model, page size/layout config-specific. Không áp MMU/page-fault model máy Linux vào mọi MCU Cortex-M.

## 1. Mục tiêu học

Vẽ virtual address→page table→physical frame/permissions, phân loại fault normal/fatal, hiểu mmap/COW và RSS/heap/virtual metrics.

## 2. Kiến thức tiên quyết

[Kernel/process](01_KERNEL_PROCESS.md), [source memory](../embedded_systems/02_MEMORY_BUILD.md), CPU load/store.

## 3. Vấn đề mà cơ chế này giải quyết

Processes cần isolated address spaces và flexible backing storage. Allocate virtual memory khác physical residency; protection và demand allocation phải giải qua mappings/fault handler thay every object contiguous physical RAM.

## 4. Khái niệm

Virtual address thuộc process mapping, MMU translates với page tables/permissions; page là unit mapping/protection, physical frame backing resident storage. TLB caches translations, không application values. Page fault xảy ra thiếu/invalid mapping hoặc permission violation; có thể resolved demand paging/COW hoặc fatal signal.

## 5. Thành phần bên trong

Virtual addr split virtual page number+offset; page-table lookup frame+permissions; translate giữ offset; TLB hit avoids full walk. Miss TLB khác page fault nếu page table valid. Fault trap→kernel examines mapping/cause→allocate/read/map/COW or signal→instruction retry khi resolved. Multi-level page tables reduce sparse metadata theo arch.

## 6. Data representation

```text
virtual address = VPN | offset
page table[VPN] = PFN + present/permission attributes
physical address = PFN | offset
```

Page size not always4KiB; example4KiB implies12bit offset. Heap allocator blocks inside mmap/brk-backed regions; free block not necessarily unmap/RSS drop. Shared mapping/file cache/COW pages may complicate per-process resident accounting.

### Ba cấp dữ liệu cần phân biệt

Một pointer trong chương trình là virtual address trong address space của process. Page-table entry mô tả translation/protection, không chứa object C. Physical frame chứa bytes; object semantics còn phụ thuộc type, bounds và lifetime. Hai process có cùng virtual address vẫn có thể trỏ hai frame khác; shared mapping có thể làm virtual addresses khác cùng trỏ một frame.

TLB lưu translation gắn với address-space context theo architecture. Khi sửa mapping, kernel phải giữ sự nhất quán của translation caches, có thể cần shootdown trên core khác. Application không tự sửa page table để “làm pointer hợp lệ”.

| Sự kiện | Kernel có thể làm gì? | Ý nghĩa ở application |
|---|---|---|
| TLB miss, PTE hợp lệ | Walk page table, nạp translation | Access tiếp tục |
| Trang demand-zero chưa resident | Cấp frame, zero và map | First touch bình thường |
| Write vào trang COW hợp lệ | Copy frame, đổi mapping | Private bytes tách ra |
| Access ngoài mapping | Báo lỗi không thể resolve | Có thể thành signal fatal |
| Write không có quyền | Resolve theo COW nếu đúng trường hợp, hoặc lỗi | Không mặc nhiên là thiếu RAM |

Ví dụ fault do COW khác segmentation violation dù đều bắt đầu bằng trap. Debug cần fault address, permissions và mapping purpose; chỉ đếm tổng page faults không tìm được root cause.

## 7. Control flow

Reserve/map address range→first touch→fault if demand backed→physical frame init/map→retry access. Mmap anonymous/file/shared/private choose backing/sharing. MAP_PRIVATE changes can COW not write back file; file truncation or invalid mapping access có distinct failures. Munmap removes mapping, later pointer invalid.

## 8. Lifetime / ownership / state

Mapping live until munmap/process exit; closing fd doesn't automatically unmap existing mapping per mmap API. COW shares until write creates private page, still source pointer lifetime contracts required. Allocator free ends object ownership but may retain pages in arena; reachability/native owners explain leak beyond RSS.

## 9. Invariants

Access permitted mapped region and live object, mapping/offset bounds đúng; process virtual pointer not transferable như physical address to DMA/device. Backing lifecycle/sharing aware, allocator live-byte counts and RSS interpreted separately. Page-fault handler success not pointer semantics proof.

## 10. Ví dụ tối thiểu

**Worked model** page4096: VA0x1234→VPN1, offset0x234; if VPN1 maps PFN0x20 then PA0x20234. Addresses illustrative, not Linux process capture.

Allocate100MiB but touch one page may reserve range while resident much smaller; after all pages touch RSS may grow; free may keep arena pages. This alone not leak proof, inspect live allocations/roots/mappings.

### Theo dấu fork và COW bằng ownership

**Mô hình dự đoán**: parent có một private writable page chứa x=7; fork tạo child cùng nội dung ban đầu. Kernel có thể cho hai page tables cùng tham chiếu frame và bảo vệ write để thực hiện COW. Child ghi x=8 → fault COW → frame riêng → parent vẫn đọc 7. Đây là sharing ở tầng physical storage, không phải hai process cùng có một C++ object để tùy ý trao pointer.

Nếu parent và child dùng shared mapping, write visibility và synchronization phải được thiết kế theo shared-memory contract. Đổi MAP_PRIVATE sang MAP_SHARED để “đỡ copy” thay đổi meaning và ownership, không chỉ performance.

Khi khảo sát memory, ghi bốn đại lượng riêng: virtual mappings, resident pages, allocator live bytes và resource owners. Một vùng mmap chưa touch làm virtual size tăng; một allocator giữ freed arena có thể giữ RSS; một list còn tham chiếu objects làm live bytes tăng. Ba hiện tượng đòi ba phép thử khác nhau.

## 11. Failure modes

Unmapped/protection fault, UAF still mapped so no fault despite invalid lifetime, stack guard hit, COW surprise memory pressure, mmap bounds/truncated file SIGBUS cases, allocator fragmentation/retention. Increasing swap/RAM doesn't fix source UAF.

## 12. Debug / observability

Maps/permissions/resident metrics/page-fault counts, heap allocation profile, native leak sanitizer, page tables/kernel docs when needed. Distinguish minor/major faults and steady-state cold load; snapshot virtual size/RSS alone insufficient. Controlled touch/free/mapping experiment expected trends no fixed bytes proof.

## 13. Liên hệ với bug/lab hiện có

[OS-05](../labs/os/OS-05.md) retention/leak, [OS-06](../labs/os/OS-06.md) UAF, [OS-07](../labs/os/OS-07.md) stack. No new VM lab; worked translation/touch examples illustrate theory.

## 14. Sai lầm thường gặp

Virtual address≠physical; TLB miss≠fatal fault; mapped≠live object; free≠RSS instant decrease. Demand fault≠bug. Kernel page size≠C sizeof object. MCU MPU region protection≠Linux MMU VM.

## 15. Câu hỏi tự kiểm tra

1. Offset for4KiB page? Đáp án:12bits.
2. TLB miss valid page table? Đáp án:translation walk, not necessarily page fault.
3. Close mapped fd unmaps? Đáp án:no.
4. UAF no fault still correct? Đáp án:no source lifetime violation.
5. High VSZ leak proof? Đáp án:no reservations/mappings need inspect.
6. Private file mapping writes persist? Đáp án:not as shared file write guarantee.

## 16. Nguồn

[OSTEP paging](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf), [TLB](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf), [Linux memory concepts](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html), [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), [proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html). Kernel docs rolling, layout not fixed release implementation.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
