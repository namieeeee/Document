# Validation — mở rộng giáo trình ngày 2026-10-06

## Cập nhật Phase 2 — 2026-10-06

Phase 1 được **SKIPPED theo yêu cầu trực tiếp của người dùng**; không coi các tiêu chí compiler/sanitizer của phase đó đã đạt. [Trạng thái](audit/PHASE_STATUS.md) ghi phạm vi và phần còn chặn.

| Claim | Lệnh từ `examples/react-race` | Quan sát thực tế | Evidence | Mức độ |
|---|---|---|---|---|
| Phản hồi A cũ ghi đè B trong component lỗi | `python verify.py` chạy Vitest với `RACE_VARIANT=broken` | exit 1; assertion nhận A, cần B; 1 failed / 1 passed | [Log](evidence/react-race/broken.log), [report](evidence/react-race/broken.json) | VERIFIED trong fixture jsdom |
| Effect cleanup đánh dấu stale giữ B | Cùng runner, `RACE_VARIANT=fixed` | exit 0; 2 tests passed | [Log](evidence/react-race/fixed.log), [report](evidence/react-race/fixed.json) | VERIFIED trong fixture jsdom |

[Bản ghi thực thi](evidence/react-race/summary.json) có timestamp UTC, Python và toàn bộ lệnh/exit codes. [Node](evidence/react-race/node-version.log), [npm](evidence/react-race/npm-version.log) và [dependency versions](evidence/react-race/package-versions.log) ghi phiên bản thật. Runner trả exit 0 chỉ khi đúng test regression thất bại và cả hai test bản sửa thành công. Cài dependency bằng `npm ci`; [hướng dẫn](examples/react-race/README.md) mô tả chạy lại và giới hạn.

Backend ASP.NET Core/MongoDB **BLOCKED**: chưa tìm được Docker/Podman/mongod trong môi trường hiện tại. Chưa chạy conditional update, unique-index concurrency hay replay bằng MongoDB. C# process-local models vẫn là MODEL; không dùng kết quả React để tuyên bố hoàn tất Phase 2. Theo prompt, Phases 3–5 còn chờ Phase 2.

## Phase theory-first hiện tại — 2026-10-06

Phần này là kết quả của đợt hoàn thiện lý thuyết; các blocks bên dưới giữ kết quả/lịch sử phase trước. [Report hiện tại](THEORY_COMPLETION_REPORT.md) và [matrix](THEORY_COVERAGE_MATRIX.md) quyết định coverage mới. Không gộp tests hai phase để tăng số kiểm tra đã chạy.

### Static validation: PASS

- UTF8 strict, H1, fences cân bằng/có language label, tables hợp lệ và không mục rỗng trong 39 bài canonical. Mỗi bài có16 H2, scope/version, nguồn và self-check có đáp án.
- Relative links **và anchors** hợp lệ; toàn bộ188 Markdown reachable từ index. Đếm file/link chỉ là inventory kỹ thuật, không chứng minh depth/COMPLETE.
- Catalog39 nodes/74 prerequisite edges là DAG; index order phù hợp. Đã review forward-reading links riêng và sửa build↔CPU, API↔database để chúng không thành prerequisites ngược.
- Map121 rows bijective với121 lab IDs; invariant mỗi row khớp mục Invariant gốc. SHA256 xác nhận toàn bộ lab/README lab,10 chương gốc và bốn source/project mẫu giữ nguyên. Không xóa file gốc.
- Không canonical files trùng toàn nội dung; review semantic split phân định authority: network/HTTP/browser; C#/runtime; DB foundation/transactions; memory/build/CPU/MMIO/core; OS1–4. Systems10 giữ overview tương thích.
- Hash ba ZIP khớp baseline; không execute binaries từ nguồn. [Source ledger](THEORY_SOURCE_VERIFICATION.md) có evidence truy cập cho153 URL hiện dùng, cùng substitutions/version limits; availability không nghĩa review toàn body.

Validator và JSON kết quả được lưu ngoài curriculum tại `Document_Code/theory_review_20261006/validate_curriculum.py` và `validation_result.json`; baseline, source access metadata và dependency manifest nằm cùng thư mục.

### Host execution: PASS trong phạm vi đã chạy

Môi trường quan sát: Windows, Node v24.20.0, Python3.11.9, .NET SDK8.0.424. Code mẫu gốc đã đọc trước execute; artifacts của hai projects .NET nằm ngoài curriculum.

| Run của phase này | Kết quả thực | Phạm vi |
|---|---|---|
| Node web_models.mjs | Exit0,6 nhóm PASS | Host snapshot/race/rollback/parser/money/event-loop model |
| Python systems_models.py | Exit0,5 nhóm PASS | Copy/buffer/queue/tick/file/retention host model |
| CoreModels build + DLL | Build0 warnings/errors; DLL exit0,6 nhóm PASS | Check-then-act/conditional write/dedup/key conflict/arithmetic/cancel model |
| Web02 task/microtask snippet trích nguyên code | PASS A B M T trong Node | Không chứng minh browser rendering |
| Web02 generation guard + read/publish fixture | PASS reversed completion B rồi A | Chỉ generation active được publish trong fixture |
| Web06 C# console snippet + assertions | PASS struct copy/reference field/boxing và stream payload | .NET8/C#12; không dùng object placement quan sát làm language guarantee |
| Web14 ReadLater + caller/assertions | PASS42 và OperationCanceledException | Cooperative cancellation trong Task.Delay fixture |

17 nhóm cũ chạy lại, cùng hai JS snippet checks và ba C# checks bổ sung. Các code blocks được trích từ bài hiện tại; caller/usings/assertions được thêm ngoài curriculum. Chưa chạy UI/HTTP server/board cho các fragments ngữ cảnh.

Lần build CoreModels với no-restore và artifacts directory mới **FAIL NETSDK1004** vì assets chưa có. Recovery dùng restore source là local empty feed, build thành công với framework đã cài, rồi chạy DLL trực tiếp. Không gọi attempt thất bại là PASS; không tải packages từ ZIP hoặc network feeds.

### Semantic/version second pass

Đối chiếu goals, examples, self-check và sources của các bài; bổ sung state tables/schedules/happens-before, counterexamples và assumptions thay headings rỗng. Sửa timer context FreeRTOS vs Zephyr, CMSIS6/Zephyr3.7 pinned links, Next15 defaults và URL, decode shift trước promotion, deadline từ release khác deadline từ event. Ví dụ số/địa chỉ/wire là model hoặc prediction, không output hardware.

[CORRECTIONS](CORRECTIONS.md) giữ nuances của nguồn nội bộ. TS/C/C++ không có compiler trên PATH nên không đánh compile PASS. Code/pseudocode/context fragments có labels và dependencies; GDB/HAL/database commands không được coi runnable độc lập.

### Chưa thực thi / giới hạn hiện tại

Không có121 integration tests đã chạy: labs là educational reproductions. Chưa dựng browser/React19/Next15, Kestrel/API/auth/database/proxy/realtime, Linux process/kernel lab hay M4/DMA/ISR/FreeRTOS/Zephyr target. Chưa đo WCET, cache coherence, electrical timing hoặc power-loss durability. Không access secrets/production.

Arm core manual/RM0090 chưa đọc được; peripheral registers, port/config và actual target guarantees phải khóa theo board. N1570 là C11 public draft dùng cho C17 nền được ghi rõ; rolling docs không là exact release proof. Review của tác giả chưa có reviewer/học viên độc lập. Các giới hạn ấy giữ domain ở GOOD, không gọi cả curriculum COMPLETE.

---


Giáo trình đích: `C:\Users\Trann\Work_Space\Document_Code\knowledge_base`. Kiểm tra ứng viên trong staging riêng trước khi áp dụng; đối chiếu SHA-256 baseline để bảo vệ chỉnh sửa đồng thời. Không thay code ví dụ cũ, không chạy binary từ ZIP, không sửa repository ứng dụng/prompt.

## Static và second pass

- UTF-8 strict, H1, file không rỗng, fence cân bằng, không trailing whitespace mới: PASS. Một dòng trắng đầu README frontend do chỉnh sửa đồng thời có whitespace sẵn có; giữ nguyên để bảo toàn file của người dùng.
- Relative links và anchors: PASS; không reference tới file bị thiếu. Toàn bộ Markdown reachable từ index.
- Không file trùng nội dung nguyên vẹn hoặc đoạn dài lặp nhầm trong một file: PASS. Các nhãn/hướng dẫn kiểm chứng dùng chung giữa lab là chủ ý.
- Giữ đủ 121 lab/ID; mỗi lab có 13 mục H2 yêu cầu dưới H1 BUG, liên kết lý thuyết và nhãn educational reproduction: PASS.
- 10 chương cũ và 22 module mới có đủ tám trường debug: PASS.
- Second pass: đọc lại flow/invariant/trigger/root cause/fix, sửa câu ghép khó đọc, nguồn dẫn không đúng cơ chế và mô tả sai capability. Không dùng Basic/Advanced/Expert thay cho giải thích cơ chế.
- Ba archive nguồn: SHA-256 khớp baseline, PASS unchanged. Không có file cũ bị xóa; bốn file code/project giữ nguyên bytes.

Số lượng cuối được ghi trong [báo cáo](EXPANSION_REPORT.md) sau validator. Đây là static review của tác giả; chưa có đánh giá độc lập từ người học hoặc nhiều model.

## Thực thi lại trên host

Môi trường Windows, Node 24.20.0, Python 3.11, .NET SDK 8.0.424; ngày chạy 2026-10-06.

| Kiểm tra | Kết quả quan sát | Phạm vi chứng minh |
|---|---|---|
| `node web_models.mjs` | PASS, exit 0, 6 nhóm | Snapshot, forced race hai thứ tự, rollback owner, shape, integer money fixture, event-loop delay |
| `python systems_models.py` | PASS, exit 0, 5 nhóm | Copy/reference, queue full/drop, tick wrap, file close và bounded retention |
| Build .NET 8 rồi chạy CoreModels DLL | PASS, exit 0, 6 nhóm | Forced lost update, conditional purchase, concurrent replay, key/payload conflict, arithmetic/cancellation |
| Snippet JavaScript trích từ Web02 | PASS, quan sát `A B M T` | Thứ tự trong Node fixture; không chứng minh browser rendering |
| Hàm C# trích từ Web06, thêm caller và usings | PASS, return 42 và cancellation | Biên dịch/chạy trên .NET 8; không chứng minh API server |

Tổng **17 nhóm kiểm tra cũ và hai snippet mới**. Node timer được quan sát sau khoảng 40.4 ms trong fixture blocking; đó không phải benchmark ứng dụng thật. Race được điều khiển bằng deferred/barrier, không lấy chạy ngẫu nhiên làm proof.

Để tránh đưa build output vào giáo trình, dùng `dotnet build --artifacts-path <thư mục ngoài giáo trình>` rồi `dotnet <đường dẫn CoreModels.dll>`. Lần thử `dotnet run --artifacts-path` đã build nhưng CLI tìm executable ở đường mặc định và báo không tìm thấy; chạy trực tiếp DLL đã thành công. Không gọi lệnh thất bại là PASS.

## Nguồn và tính trung thực

33 URL official/primary bổ sung có body đọc được ngày 2026-10-06; nguồn giữ từ lần trước giữ ngày kiểm tra cũ. [REFERENCES](REFERENCES.md) ghi nguồn thất bại/giới hạn và version; không coi link chưa đọc hoặc trang index là bằng chứng đã đọc toàn sách/manual. Lab truy nguồn qua bài nền hoặc nguồn trực tiếp theo cơ chế.

121 lab đều là **educational reproduction**, không gán production incident/CVE/postmortem. Kết quả trong lab là dự đoán và quy trình thu evidence, trừ kết quả được ghi là đã thực thi ở bảng trên. Không có documented real-world incident được thêm.

## Chưa thực thi / giới hạn

121 scenario-lab không phải 121 integration test đã chạy. Snippet C và TypeScript mới chưa biên dịch: không tìm thấy compiler C/C++ hoặc tsc trên PATH. Các fragment còn lại có thể cần project/framework/helper cụ thể.

Chưa dựng browser React/Next.js, API/auth/MongoDB/proxy/realtime, Linux process/FD/kernel lab hoặc MCU/DMA/ISR/FreeRTOS/Zephyr thật. Chưa xác minh WCET, cache coherence, power-loss durability hay workload production. Python/C# ownership model không chứng minh C UB hoặc ARM memory ordering.

Chưa chọn board/MCU/port và chưa đọc được RM0090: web tool từ chối PDF vượt giới hạn kích thước. Phần ngoại vi chỉ là mô hình state machine; register, electrical setup và timing cần reference manual đúng target. Chưa kiểm toàn bộ exercise bằng học viên thực tế.

## Lịch sử kiểm tra

Lần 2026-10-05: 142 Markdown, 676 relative links, 17 nhóm host checks; giáo trình khi đó ở `Tool/knowledge_base`. Đây là số lịch sử, không phải số của bản mở rộng hiện tại. Tài liệu nay ở Document_Code.

[Index](00_INDEX.md) · [Examples](examples/README.md) · [Casebook](09_REAL_BUG_CASEBOOK.md).
