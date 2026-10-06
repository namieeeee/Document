# Knowledge Base — Web, Embedded và Systems

Giáo trình kỹ thuật tiếng Việt theo hướng **theory first**: nền tảng → cơ chế bên trong → data/control flow → lifetime và ownership → invariant → failure → evidence/debug → lab.

**Bắt đầu tại [00_INDEX.md](00_INDEX.md)** để chọn lộ trình và xem kiến thức tiên quyết.

## Nội dung

- **Web/FE/BE:** HTTP, browser, JavaScript, TypeScript, React19, Next15, C#12/.NET8, ASP.NET Core8, API, database và security.
- **Embedded/Systems:** representation, C17/C++17, memory/build, CPU/ABI, Cortex-M4, MMIO, peripheral, IRQ, DMA, concurrency, RTOS và real-time.
- **OS:** kernel/userspace, syscall, process/thread, virtual memory, I/O/IPC và resource lifetime.
- **Debugging:** scientific debugging và cách chọn evidence/tools theo tầng.

## Hồ sơ giáo trình

| Tài liệu | Vai trò |
|---|---|
| [Index](00_INDEX.md) | Lộ trình học theo dependency |
| [Theory coverage matrix](THEORY_COVERAGE_MATRIX.md) | Before/after, evidence và phạm vi từng nhóm |
| [Theory → invariant → lab](BUG_THEORY_MAP.md) | Ánh xạ tới121 lab hiện có |
| [Nguồn và phiên bản](REFERENCES.md) | Tài liệu chính thống và giới hạn |
| [Source verification](THEORY_SOURCE_VERIFICATION.md) | Kết quả truy cập và đối chiếu nguồn |
| [Validation](VALIDATION.md) | Kiểm tra đã chạy và phần chưa xác minh |
| [Theory completion report](THEORY_COMPLETION_REPORT.md) | Báo cáo đợt mở rộng lý thuyết |
| [Ví dụ trên host](examples/README.md) | Cách chạy các models minh họa |

## Phạm vi kiểm chứng

Labs là **educational reproductions**, không phải các incidents production. Ví dụ model/pseudocode và kết quả dự đoán được phân biệt với code đã thực thi trong validation. Host models không thay kiểm tra browser/framework, Linux hoặc MCU/RTOS trên target thật.

Nguồn nội bộ được ghi nhận trong inventory nhưng các ZIP và build output không nằm trong repository này. Sources, version labels và assumptions trong từng bài quyết định phạm vi áp dụng.
