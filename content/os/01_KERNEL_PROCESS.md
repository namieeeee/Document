# Outline — OS foundation: hardware, kernel, userspace và threads

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Runnable starvation vs blocked deadlock, invalid pointer syscall result/error, forgotten join/wait/resource refs, process isolation confused shared memory, thread stack overflow/use-after-return. Fix lifecycle/wait dependency/access contract.

Đặt câu hỏi: cơ chế trong [OS foundation: hardware, kernel, userspace và threads](../../os/01_KERNEL_PROCESS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
user function → optional syscall instruction → kernel operation
→ ready result return hoặc block wait
→ event wake runnable → scheduler dispatch → user resumes
```

Syscall may complete on same thread no other thread scheduled; preemption may occur outside syscall. Process exit releases many resources, parent still needs reap exit status theo wait semantics.

## 3. Demo chạy thật

Claim có phạm vi: User pointers validated/access permissions enforced, thread resumes correct context, shared state follows protocol, acquired kernel resources released appropriate owner. Runnable doesn't guarantee deadline; scheduler fairness/policy not hard-real-time proof.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../os/01_KERNEL_PROCESS.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Runnable starvation vs blocked deadlock, invalid pointer syscall result/error, forgotten join/wait/resource refs, process isolation confused shared memory, thread stack overflow/use-after-return. Fix lifecycle/wait dependency/access contract.

Thread states/stacks, process maps/FD/child state, syscall trace on synthetic fixture (Linux tool required). CPU time vs wall/wait and runnable-to-run timing separate; one snapshot state not full timeline. Exact build symbols for stack interpretation.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[intro(2)](https://man7.org/linux/man-pages/man2/intro.2.html), [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), [OSTEP processes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf).

1. Syscall creates thread? Đáp án:not normally.
2. Threads share descriptor table? Đáp án:process threads generally share resources per Linux model.
3. Blocked vs ready? Đáp án:waiting event vs eligible.
4. Zombie consumes execution CPU? Đáp án:already exited status awaiting reap.
5. Kernel policy source same Windows? Đáp án:no APIs/semantics distinct.

[Index](../../00_INDEX.md) · [Content](../README.md).
