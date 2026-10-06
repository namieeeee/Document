# Outlines cho kênh

Mỗi bài canonical có sáu phần. Chỉ những outline có demo evidence và claim VERIFIED/MODEL được dùng để xuất bản demo; UNVERIFIED có placeholder BLOCKED rõ ràng. Mức áp dụng cho claim được trích, không chứng nhận toàn chương.

| Bài | Claim level | Demo |
|---|---|---|
| [Bit, số và byte: từ ý nghĩa tới representation](foundations/01_DIGITAL_REPRESENTATION.md) | UNVERIFIED | BLOCKED |
| [Computer ↔ network ↔ browser: một URL đi đâu?](web/01_HTTP_BROWSER.md) | UNVERIFIED | BLOCKED |
| [JavaScript language: bindings, objects và reachable memory](foundations/02_JAVASCRIPT_LANGUAGE.md) | MODEL | Evidence có sẵn |
| [HTTP: semantics, representation, cache và partial failure](web/12_HTTP_SEMANTICS.md) | UNVERIFIED | BLOCKED |
| [Browser: từ parser tới pixels, events và storage](web/13_BROWSER_INTERNALS.md) | UNVERIFIED | BLOCKED |
| [JavaScript async runtime: jobs, host và thời gian](web/02_JS_RUNTIME.md) | MODEL | Evidence có sẵn |
| [TypeScript: mô hình tĩnh và runtime boundary](web/03_TYPESCRIPT_BOUNDARIES.md) | UNVERIFIED | BLOCKED |
| [React: render snapshots, identity và commit](web/04_REACT_MENTAL_MODEL.md) | VERIFIED | Evidence có sẵn |
| [Next.js: build, server, browser và boundary](web/05_NEXT_EXECUTION.md) | UNVERIFIED | BLOCKED |
| [C# language: value, reference và resource lifetime](web/06_CSHARP_RUNTIME.md) | MODEL | Evidence có sẵn |
| [.NET: IL/JIT/GC và async continuations](web/14_DOTNET_ASYNC_RUNTIME.md) | MODEL | Evidence có sẵn |
| [ASP.NET Core: lifecycle request và dependency scope](web/07_ASPNET_LIFECYCLE.md) | UNVERIFIED | BLOCKED |
| [API: resource, command, validation và version](web/08_API_CONTRACTS.md) | VERIFIED | Evidence có sẵn |
| [Database foundation: storage, relations và access paths](web/09_DATABASE_CONCURRENCY.md) | VERIFIED | Evidence có sẵn |
| [Concurrency và consistency: invariant nằm ở đâu?](web/15_DATABASE_TRANSACTIONS.md) | VERIFIED | Evidence có sẵn |
| [Security: identity, authority và trust boundaries](web/10_IDENTITY_SECURITY.md) | UNVERIFIED | BLOCKED |
| [Integration: wire meaning, intent và state owners](web/11_INTEGRATION_FLOW.md) | MODEL | Evidence có sẵn |
| [C17: object, expression, pointer và linkage](embedded_systems/01_C_REPRESENTATION.md) | UNVERIFIED | BLOCKED |
| [Memory: storage, layout và lifetime](embedded_systems/02_MEMORY_BUILD.md) | UNVERIFIED | BLOCKED |
| [Build/link: source tới ELF và flash](embedded_systems/11_BUILD_LINK_STARTUP.md) | UNVERIFIED | BLOCKED |
| [CPU execution: instructions, calls và ABI](embedded_systems/04_CPU_MCU_EXECUTION.md) | UNVERIFIED | BLOCKED |
| [C++ embedded: objects, RAII và chi phí](embedded_systems/03_CPP_OWNERSHIP.md) | UNVERIFIED | BLOCKED |
| [MCU và memory-mapped I/O](embedded_systems/13_MMIO_MCU.md) | UNVERIFIED | BLOCKED |
| [Cortex-M4: reset, exceptions và protection](embedded_systems/12_CORTEX_M.md) | UNVERIFIED | BLOCKED |
| [GPIO, timer và PWM: hardware state machines](embedded_systems/05_PERIPHERAL_STATE_MACHINES.md) | UNVERIFIED | BLOCKED |
| [UART, SPI và I2C: wire/state/service flow](embedded_systems/14_SERIAL_BUSES.md) | UNVERIFIED | BLOCKED |
| [ADC và CAN: sampling, arbitration và error states](embedded_systems/15_ADC_CAN.md) | UNVERIFIED | BLOCKED |
| [Interrupts: event, preemption và coherent state](embedded_systems/06_INTERRUPTS.md) | UNVERIFIED | BLOCKED |
| [DMA: independent bus actor và ownership handoff](embedded_systems/07_DMA_OWNERSHIP.md) | MODEL | Evidence có sẵn |
| [Embedded concurrency: CPU, ISR, DMA và tasks](embedded_systems/08_CONCURRENCY_BUFFERS.md) | MODEL | Evidence có sẵn |
| [RTOS scheduler: task states và context switch](embedded_systems/09_RTOS_SCHEDULER.md) | UNVERIFIED | BLOCKED |
| [Real-time: deadline, response time và interference](embedded_systems/16_REAL_TIME.md) | MODEL | Evidence có sẵn |
| [OS foundation: hardware, kernel, userspace và threads](os/01_KERNEL_PROCESS.md) | UNVERIFIED | BLOCKED |
| [Virtual memory: pages, faults, heap và mappings](os/02_VIRTUAL_MEMORY.md) | UNVERIFIED | BLOCKED |
| [I/O, IPC và resource acquire-use-release](os/03_IO_IPC_LIFETIME.md) | MODEL | Evidence có sẵn |
| [OS concurrency: happens-before, waits và progress](os/04_CONCURRENCY.md) | UNVERIFIED | BLOCKED |
| [Scientific debugging: chứng minh cơ chế phá invariant](debug/01_EVIDENCE_METHOD.md) | UNVERIFIED | BLOCKED |
| [Debug Web: evidence từ browser tới database](debug/02_WEB_OBSERVABILITY.md) | UNVERIFIED | BLOCKED |
| [Debug C/C++/Embedded: source, CPU, wire và scheduler](debug/03_SYSTEMS_OBSERVABILITY.md) | UNVERIFIED | BLOCKED |

[Matrix](../THEORY_COVERAGE_MATRIX.md) · [Review](../REVIEW_CHECKLIST.md) · [Index](../00_INDEX.md).
