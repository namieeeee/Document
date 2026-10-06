# OS foundation: hardware, kernel, userspace và threads

Phạm vi: Linux/POSIX conceptual user model; không Windows API equivalence, RTOS MCU khác capabilities/config.

## 1. Mục tiêu học

Theo user call tới kernel và về, phân biệt privilege transition/context switch, process resources/thread execution/scheduling.

## 2. Kiến thức tiên quyết

[CPU](../embedded_systems/04_CPU_MCU_EXECUTION.md), [memory](../embedded_systems/02_MEMORY_BUILD.md). Không cần thuộc RTOS API trước OS.

## 3. Vấn đề mà cơ chế này giải quyết

Nhiều chương trình cần chia CPU/devices/memory nhưng không tự ghi state của nhau/kernel. OS cung services và isolation cùng scheduler; userspace dùng controlled entry thay arbitrary privileged instruction.

## 4. Khái niệm

Kernel là privileged resource manager, userspace có restricted execution. Library API có thể pure user code hoặc syscall; syscall entry vào kernel kiểm parameters/permissions rồi returns result/error. Mode transition không luôn scheduling switch. Process holds address-space/resources/security context, thread có registers/stack/scheduling state trong process.

## 5. Thành phần bên trong

CPU privilege/trap entry→kernel dispatch→validate user memory/arguments→service/driver→return. Scheduler chọn runnable threads theo policy; blocked thread waiting I/O/time/lock không eligible until wake. Context switch preserves execution state và có address-space/TLB/cache effects tùy same/different process.

## 6. Data representation

Process address mappings/file-descriptor table/credentials, threads share many process resources nhưng stacks/registers/thread-local state riêng. PID/TID identifiers distinct; handles duplicate/reference same kernel object. fork-like creation/exec replacement/thread creation có semantics riêng Linux, not just copy code objects.

## 7. Control flow

```text
user function → optional syscall instruction → kernel operation
→ ready result return hoặc block wait
→ event wake runnable → scheduler dispatch → user resumes
```

Syscall may complete on same thread no other thread scheduled; preemption may occur outside syscall. Process exit releases many resources, parent still needs reap exit status theo wait semantics.

## 8. Lifetime / ownership / state

Thread stack owned to termination/join lifecycle; returning pointer local invalid before thread exit too. Process resource shared references may remain via dup/fork/other process. Child exited zombie holds exit status until parent wait, not running user instructions. Detached/joinable thread cleanup contracts khác.

## 9. Invariants

User pointers validated/access permissions enforced, thread resumes correct context, shared state follows protocol, acquired kernel resources released appropriate owner. Runnable doesn't guarantee deadline; scheduler fairness/policy not hard-real-time proof.

## 10. Ví dụ tối thiểu

**Conceptual trace** read(fd,buf,n): if data ready kernel copies available count≤n and returns; if blocking empty pipe with writer alive, thread blocked; writer sends→wake→runnable→dispatch→read returns partial count. Caller must framing loop, not assume n bytes.

## 11. Failure modes

Runnable starvation vs blocked deadlock, invalid pointer syscall result/error, forgotten join/wait/resource refs, process isolation confused shared memory, thread stack overflow/use-after-return. Fix lifecycle/wait dependency/access contract.

## 12. Debug / observability

Thread states/stacks, process maps/FD/child state, syscall trace on synthetic fixture (Linux tool required). CPU time vs wall/wait and runnable-to-run timing separate; one snapshot state not full timeline. Exact build symbols for stack interpretation.

## 13. Liên hệ với bug/lab hiện có

[OS-04](../labs/os/OS-04.md) child reaping, [OS-07](../labs/os/OS-07.md) stack, [OS-09](../labs/os/OS-09.md) workers/waits. [RTOS](../embedded_systems/09_RTOS_SCHEDULER.md) comparison after foundation.

## 14. Sai lầm thường gặp

Process≠large thread; syscall≠always context switch; private stacks don't prohibit other thread accessing shared pointer if valid. RTOS can have MPU/protection, Linux can realtime config; labels not guarantees.

## 15. Câu hỏi tự kiểm tra

1. Syscall creates thread? Đáp án:not normally.
2. Threads share descriptor table? Đáp án:process threads generally share resources per Linux model.
3. Blocked vs ready? Đáp án:waiting event vs eligible.
4. Zombie consumes execution CPU? Đáp án:already exited status awaiting reap.
5. Kernel policy source same Windows? Đáp án:no APIs/semantics distinct.

## 16. Nguồn

[intro(2)](https://man7.org/linux/man-pages/man2/intro.2.html), [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), [OSTEP processes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
