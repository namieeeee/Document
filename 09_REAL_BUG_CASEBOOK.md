# 09 — Casebook: cơ chế lỗi có thể tái hiện

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Debug dùng chung hai track — bằng chứng trước kết luận](debug/01_EVIDENCE_METHOD.md)

121 educational reproduction/scenario-lab: 25 FE, 30 BE, 25 tích hợp, 30 embedded/RTOS, 11 OS. Mỗi lab có fixture, trigger, expected/actual dự đoán, evidence, fix và regression. **Đây là lab mô phỏng**, không gán tên công ty/CVE hoặc tuyên bố incident thật. Code/config ngữ cảnh phần lớn là pseudocode; cần chuyển thành fixture theo môi trường nêu trong lab.

## Chọn bài và đánh giá

Làm trước FE-05, BE-15, INT-20, EMB-13 và OS-09 để thấy cùng một vấn đề ownership/time ở nhiều tầng. Sau đó chọn nhánh và tăng độ khó. Bài dễ thành công tuần tự chưa đủ chứng minh concurrency đúng.

Rubric mỗi lab: tái hiện đúng trigger; ghi evidence trước fix; nêu giả thuyết cạnh tranh; giải thích invariant; regression buộc trigger gốc và một case biên; ghi kết quả thực/chưa chạy riêng. Không đánh giá chỉ theo screenshot xanh.

## Taxonomy và toàn bộ lab

### frontend

[Index nhóm](labs/frontend/README.md)

- [FE-01 — Stale closure](labs/frontend/FE-01.md)
- [FE-02 — Effect dependency thiếu](labs/frontend/FE-02.md)
- [FE-03 — Vòng effect vô hạn](labs/frontend/FE-03.md)
- [FE-04 — Thiếu cleanup](labs/frontend/FE-04.md)
- [FE-05 — Fetch race](labs/frontend/FE-05.md)
- [FE-06 — Response cũ tắt loading mới](labs/frontend/FE-06.md)
- [FE-07 — Double submit](labs/frontend/FE-07.md)
- [FE-08 — Controlled/uncontrolled](labs/frontend/FE-08.md)
- [FE-09 — Key dùng index](labs/frontend/FE-09.md)
- [FE-10 — Mutation state](labs/frontend/FE-10.md)
- [FE-11 — Derived state lệch](labs/frontend/FE-11.md)
- [FE-12 — Hydration mismatch](labs/frontend/FE-12.md)
- [FE-13 — Browser API ở server](labs/frontend/FE-13.md)
- [FE-14 — Server/client boundary](labs/frontend/FE-14.md)
- [FE-15 — Không xử lý error/loading](labs/frontend/FE-15.md)
- [FE-16 — Cache không invalidate](labs/frontend/FE-16.md)
- [FE-17 — Token hết hạn không recovery](labs/frontend/FE-17.md)
- [FE-18 — CORS bị hiểu là quyền](labs/frontend/FE-18.md)
- [FE-19 — XSS qua HTML](labs/frontend/FE-19.md)
- [FE-20 — Secret trong client bundle](labs/frontend/FE-20.md)
- [FE-21 — Timezone ngày lịch](labs/frontend/FE-21.md)
- [FE-22 — Float tiền](labs/frontend/FE-22.md)
- [FE-23 — Layout overflow](labs/frontend/FE-23.md)
- [FE-24 — Accessibility thiếu label](labs/frontend/FE-24.md)
- [FE-25 — TS không validate JSON](labs/frontend/FE-25.md)

### backend

[Index nhóm](labs/backend/README.md)

- [BE-01 — Thiếu authorization](labs/backend/BE-01.md)
- [BE-02 — BOLA](labs/backend/BE-02.md)
- [BE-03 — Mass assignment](labs/backend/BE-03.md)
- [BE-04 — Chỉ validate client](labs/backend/BE-04.md)
- [BE-05 — JWT validation thiếu](labs/backend/BE-05.md)
- [BE-06 — Refresh reuse](labs/backend/BE-06.md)
- [BE-07 — Expiry race](labs/backend/BE-07.md)
- [BE-08 — DI lifetime sai](labs/backend/BE-08.md)
- [BE-09 — Singleton giữ user](labs/backend/BE-09.md)
- [BE-10 — async void](labs/backend/BE-10.md)
- [BE-11 — Sync over async](labs/backend/BE-11.md)
- [BE-12 — Không propagate cancellation](labs/backend/BE-12.md)
- [BE-13 — Retry tạo duplicate](labs/backend/BE-13.md)
- [BE-14 — Idempotency key mới mỗi retry](labs/backend/BE-14.md)
- [BE-15 — Check then act](labs/backend/BE-15.md)
- [BE-16 — Lost update](labs/backend/BE-16.md)
- [BE-17 — Pagination không ổn định](labs/backend/BE-17.md)
- [BE-18 — Thiếu index](labs/backend/BE-18.md)
- [BE-19 — Index order sai](labs/backend/BE-19.md)
- [BE-20 — Query không bounded](labs/backend/BE-20.md)
- [BE-21 — Cache thiếu tenant](labs/backend/BE-21.md)
- [BE-22 — Swallow exception](labs/backend/BE-22.md)
- [BE-23 — Thiếu correlation](labs/backend/BE-23.md)
- [BE-24 — Secret trong log](labs/backend/BE-24.md)
- [BE-25 — Secret trong Git](labs/backend/BE-25.md)
- [BE-26 — Date thiếu timezone](labs/backend/BE-26.md)
- [BE-27 — Serialization sai shape](labs/backend/BE-27.md)
- [BE-28 — Status/error sai](labs/backend/BE-28.md)
- [BE-29 — CORS rộng có credentials](labs/backend/BE-29.md)
- [BE-30 — API abuse không giới hạn](labs/backend/BE-30.md)

### integration

[Index nhóm](labs/integration/README.md)

- [INT-01 — Tên field lệch](labs/integration/INT-01.md)
- [INT-02 — Casing lệch](labs/integration/INT-02.md)
- [INT-03 — Nullability lệch](labs/integration/INT-03.md)
- [INT-04 — Number/string lệch](labs/integration/INT-04.md)
- [INT-05 — Enum lệch](labs/integration/INT-05.md)
- [INT-06 — Timezone lệch](labs/integration/INT-06.md)
- [INT-07 — Pagination0/1](labs/integration/INT-07.md)
- [INT-08 — Sort contract lệch](labs/integration/INT-08.md)
- [INT-09 — Error envelope lệch](labs/integration/INT-09.md)
- [INT-10 — Status xử lý sai](labs/integration/INT-10.md)
- [INT-11 — Cookie không gửi](labs/integration/INT-11.md)
- [INT-12 — SameSite/Secure](labs/integration/INT-12.md)
- [INT-13 — Preflight bị chặn](labs/integration/INT-13.md)
- [INT-14 — Refresh race](labs/integration/INT-14.md)
- [INT-15 — Expiry giữa nhiều request](labs/integration/INT-15.md)
- [INT-16 — Optimistic rollback sai](labs/integration/INT-16.md)
- [INT-17 — FE cache stale](labs/integration/INT-17.md)
- [INT-18 — BE cache stale](labs/integration/INT-18.md)
- [INT-19 — Duplicate POST](labs/integration/INT-19.md)
- [INT-20 — Timeout nhưng commit](labs/integration/INT-20.md)
- [INT-21 — Upload mismatch](labs/integration/INT-21.md)
- [INT-22 — Real time reconnect mất event](labs/integration/INT-22.md)
- [INT-23 — Event out-of-order](labs/integration/INT-23.md)
- [INT-24 — Event duplicate](labs/integration/INT-24.md)
- [INT-25 — Contract version drift](labs/integration/INT-25.md)

### embedded_rtos

[Index nhóm](labs/embedded_rtos/README.md)

- [EMB-01 — ISR quá dài](labs/embedded_rtos/EMB-01.md)
- [EMB-02 — Shared data không đồng bộ](labs/embedded_rtos/EMB-02.md)
- [EMB-03 — Volatile không atomic](labs/embedded_rtos/EMB-03.md)
- [EMB-04 — ISR/main clear race](labs/embedded_rtos/EMB-04.md)
- [EMB-05 — Torn access](labs/embedded_rtos/EMB-05.md)
- [EMB-06 — IRQ priority sai RTOS](labs/embedded_rtos/EMB-06.md)
- [EMB-07 — Mất nhiều event](labs/embedded_rtos/EMB-07.md)
- [EMB-08 — Register read-modify-write](labs/embedded_rtos/EMB-08.md)
- [EMB-09 — Block trong ISR](labs/embedded_rtos/EMB-09.md)
- [EMB-10 — Nested ISR stack](labs/embedded_rtos/EMB-10.md)
- [EMB-11 — DMA buffer lifetime](labs/embedded_rtos/EMB-11.md)
- [EMB-12 — DMA cache coherence](labs/embedded_rtos/EMB-12.md)
- [EMB-13 — DMA CPU ownership](labs/embedded_rtos/EMB-13.md)
- [EMB-14 — DMA alignment](labs/embedded_rtos/EMB-14.md)
- [EMB-15 — DMA double buffer reuse](labs/embedded_rtos/EMB-15.md)
- [EMB-16 — RTOS race](labs/embedded_rtos/EMB-16.md)
- [EMB-17 — RTOS deadlock](labs/embedded_rtos/EMB-17.md)
- [EMB-18 — RTOS livelock](labs/embedded_rtos/EMB-18.md)
- [EMB-19 — RTOS starvation](labs/embedded_rtos/EMB-19.md)
- [EMB-20 — Priority inversion](labs/embedded_rtos/EMB-20.md)
- [EMB-21 — Mutex dùng như semaphore](labs/embedded_rtos/EMB-21.md)
- [EMB-22 — Queue overflow](labs/embedded_rtos/EMB-22.md)
- [EMB-23 — Lost notification event](labs/embedded_rtos/EMB-23.md)
- [EMB-24 — Task stack overflow](labs/embedded_rtos/EMB-24.md)
- [EMB-25 — Heap fragmentation](labs/embedded_rtos/EMB-25.md)
- [EMB-26 — Priority assignment sai](labs/embedded_rtos/EMB-26.md)
- [EMB-27 — Busy wait RTOS](labs/embedded_rtos/EMB-27.md)
- [EMB-28 — Block trong critical](labs/embedded_rtos/EMB-28.md)
- [EMB-29 — Tick wraparound](labs/embedded_rtos/EMB-29.md)
- [EMB-30 — Buffer ownership queue](labs/embedded_rtos/EMB-30.md)

### os

[Index nhóm](labs/os/README.md)

- [OS-01 — Deadlock lock order](labs/os/OS-01.md)
- [OS-02 — Data race](labs/os/OS-02.md)
- [OS-03 — FD leak](labs/os/OS-03.md)
- [OS-04 — Zombie process](labs/os/OS-04.md)
- [OS-05 — Memory leak](labs/os/OS-05.md)
- [OS-06 — Use after free](labs/os/OS-06.md)
- [OS-07 — Stack overflow](labs/os/OS-07.md)
- [OS-08 — Blocking event loop](labs/os/OS-08.md)
- [OS-09 — Thread pool starvation](labs/os/OS-09.md)
- [OS-10 — Priority inversion OS](labs/os/OS-10.md)
- [OS-11 — TOCTOU filesystem](labs/os/OS-11.md)

## Câu hỏi tổng hợp

1. Race request web và DMA ownership giống nhau ở invariant nào?
2. Queue lớn hơn có sửa được producer nhanh hơn consumer vô hạn không?
3. Khi nào timeout để lại trạng thái chưa biết?
4. Vì sao simulation không chứng minh realtime hoặc cache coherence?

Hoàn thành khi có ít nhất một biên bản đầy đủ ở mỗi nhóm và giải thích được chỗ mô hình khác môi trường thật. [Playbook](08_DEBUGGING_PLAYBOOK.md) · [Kết quả kiểm tra](VALIDATION.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [INT-20](labs/integration/INT-20.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Client deadline sớm hơn commit/response nên outcome là chưa biết. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Timeout không được giả định operation chưa commit; outcome được reconcile.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Khẳng định chưa tạo sau timeout rồi submit intent mới.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](web/01_HTTP_BROWSER.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).

## Theory trước bug

[Map đầy đủ121 bug](BUG_THEORY_MAP.md). Mỗi file có Invariant, Trigger, Root cause, Debug process và Wrong fixes riêng. Không thêm incident/CVE hay lab mới; các model đã chạy không được đổi nhãn thành production proof.
