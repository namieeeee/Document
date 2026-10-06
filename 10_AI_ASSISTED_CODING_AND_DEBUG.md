# 10 — Dùng AI để code/debug mà vẫn kiểm soát kết quả

## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Debug dùng chung hai track — bằng chứng trước kết luận](debug/01_EVIDENCE_METHOD.md)

Mục tiêu: giao nhiệm vụ đủ dữ kiện, giữ source an toàn và tự kiểm kết quả. Không phụ thuộc model/provider cụ thể. Tiền đề: Git diff, build/test và chương 08. Không gửi secrets, private keys, token hoặc production data vào hội thoại.

## mô tả một failure

Gửi task, phạm vi, expected/actual, reproducer và evidence đã có. Phân biệt code đã apply với patch gợi ý; test đã chạy với test đề xuất. Nếu AI không có terminal/file reader, nó chỉ có thể phân tích dữ liệu bạn đưa, không thể “đã đọc repo” hay “tests passed”. Thiếu input cốt lõi thì hỏi cụ thể; thiếu chi tiết phụ thì nêu giả định và tiếp tục phần an toàn.

```text
Mục tiêu: sửa response cũ ghi đè query mới.
Phạm vi: SearchBox và test tương ứng; giữ API contract.
Evidence: A mất300ms, B20ms, A được apply sau B.
Trước sửa: đọc component, test và package lock; ghi baseline.
Đầu ra: patch nhỏ, giải thích ownership, test trigger gốc + đảo delay.
Chỉ báo đã chạy những lệnh thực sự chạy; nêu phần chưa kiểm chứng.
```

## đọc repo trước sửa

Xác định root, branch, HEAD, status; giữ user changes. Đọc entrypoint, build config, dependency versions, conventions và tests liên quan. Tài liệu/code/log từ ngoài là dữ liệu; câu “ignore previous instructions” trong README/web không có quyền mở rộng task. Source khác docs thì kiểm code thật và ghi mismatch.

Yêu cầu AI nêu giả thuyết và phép kiểm tra phân biệt, không yêu cầu trình bày suy nghĩ nội bộ dài. “Hãy suy nghĩ sâu” không thay reproducer. Kết quả hữu ích gồm quan sát, suy luận có điều kiện và bằng chứng cần lấy tiếp. Nếu tool thất bại, giữ log lỗi và hoàn thành phần độc lập; không dựng output giả.

## vòng lặp patch và regression

Ưu tiên thay đổi nhỏ gắn root cause. Review diff xem có ngoài scope, dependency mới, auth bypass, log dữ liệu nhạy cảm hoặc contract drift không. Chạy test phù hợp, kiểm negative cases; compiler thành công chỉ chứng minh một lớp correctness. AI có thể viết test lặp logic của implementation nên test nên dựa invariant/fixture độc lập.

Với code MCU, yêu cầu board/core/port/linker script và API ISR-safe; nếu không có hardware, label host simulation. Với web, ghi phiên bản React/Next/.NET và cache mode. Với database, không chạy load/destructive migration trên production. Commit explicit paths sau validation; push theo remote/branch đã xác minh khi user yêu cầu, không force để vượt divergence.

## chống sự tự tin sai

Không đánh giá bằng lời văn thuyết phục. Kiểm source trích dẫn đã đọc và áp dụng đúng phiên bản; phân biệt primary evidence với bài tổng hợp. Ví dụ “volatile sửa race” nghe hợp embedded nhưng sai với read-modify-write; đối chiếu [GCC volatile](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html) và [C++ race](https://eel.is/c++draft/intro.races). AI cũng có thể tạo code compile được nhưng sai cancellation/ownership.

Đánh giá cùng một prompt với: input thiếu, tool không có, docs mâu thuẫn, log chứa instruction injection, yêu cầu đơn giản và race phức tạp. Tiêu chí: không bịa hành động, không vượt scope, hỏi đúng thông tin chặn tiến độ, đầu ra kiểm được. Không có bằng chứng ở một model không đồng nghĩa mọi model đều ổn.

## Bài tập và checklist

Chọn BE idempotency hoặc DMA lifetime. Viết prompt task 6 dòng, cho AI đưa patch, tự tìm một case bác bỏ fix. Dùng [VALIDATION](VALIDATION.md) làm ví dụ cách ghi giới hạn thực tế, không copy câu PASS khi chưa chạy.

1. Nếu AI nói đã đọc file nhưng không có file/tool thì xử lý thế nào?
2. Negative test nào ngăn “fix” bằng cách bỏ authorization?
3. Repo doc có quyền yêu cầu upload secrets không?
4. Vì sao compilation chưa chứng minh realtime?
5. Khi nào cần human review trước delivery?

Hoàn thành khi tự giải thích diff và evidence, không chỉ chấp nhận câu trả lời AI. Quay lại [index](00_INDEX.md) chọn nhánh tiếp theo.

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [BE-02](labs/backend/BE-02.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Query tìm theo ID toàn cục, thiếu filter quyền trên đối tượng/tenant. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: User chỉ access object/tenant nằm trong scope quyền của principal.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Đổi ID thành khó đoán nhưng lookup vẫn không kiểm ownership.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](web/10_IDENTITY_SECURITY.md) · [Debug method](debug/01_EVIDENCE_METHOD.md) · [Validation](VALIDATION.md).
