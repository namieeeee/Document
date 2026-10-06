# 04 — FE↔BE: hợp đồng trên dây

> Historical overview, superseded as a teaching source. Original content is retained for traceability; execution claims and snippets are not upgraded by this archive. [Current navigation](../04_FE_BE_INTEGRATION_AND_REAL_BUGS.md).


## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Web11 — Integration như luồng dữ liệu có owner](../web/11_INTEGRATION_FLOW.md)
- [Web08 — API: invariant trước endpoint shape](../web/08_API_CONTRACTS.md)

Mục tiêu: tìm lỗi qua Browser → Network → API → DB → Response → UI. Tiền đề chương 02–03. “Real bugs” ở đây là cơ chế lỗi tái hiện được; mọi lab tự xây là mô phỏng, không tuyên bố incident production.

## JSON không tự tạo hợp đồng

FE gửi `done:true`, BE đọc `isDone`: request hợp lệ cú pháp nhưng sai ý nghĩa. Một type TS và một class C# cùng tên chưa chứng minh wire format giống nhau. Chốt required/optional/null, enum representation, date format, precision và error envelope. Viết fixture success/error rồi cho cả hai phía đọc; test contract quan trọng hơn chỉ screenshot UI.

Với date-only như ngày sinh, truyền chuỗi `YYYY-MM-DD` và giữ nghĩa ngày lịch. Với event instant, dùng timestamp có offset/UTC rõ; khi hiển thị mới chuyển timezone. Với tiền, ghi currency và rounding; minor-unit không luôn là nhân 100 với mọi currency. Object ID là string; không ép ID dài sang JS number rồi mất precision.

## cookie và CORS

Cookie gửi theo domain/path, Secure, SameSite và browser policy. Cross-origin không đồng nghĩa cross-site. Khi dùng credentials, cấu hình origin cụ thể phù hợp và chống CSRF cho cookie-auth; không tự cho rằng CORS đủ bảo vệ. Preflight OPTIONS kiểm phương thức/header; không tháo auth của nghiệp vụ chỉ để OPTIONS qua. Dùng DevTools quan sát request có Cookie/Authorization không và response header thực tế. [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).

401 có thể vì token hết hạn; 403 thường không được sửa bằng refresh. Nếu nhiều request đồng thời nhận401, chỉ một refresh được sở hữu tại client, các request khác chờ kết quả. Server phải có chính sách rotation/reuse hợp lý; client single-flight không bảo đảm nhiều tab/thiết bị không cùng refresh.

## retry và optimistic UI

Một request timeout sau commit có trạng thái chưa biết. Idempotency key phải ổn định cho cùng thao tác, khác cho thao tác mới; server lưu key + hash payload + kết quả theo phạm vi user/tenant, có atomic claim và retention. Không sinh key mới mỗi retry. Response replay phải đúng chính sách dữ liệu/quyền, không chỉ “trả200”. Theo [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), tính idempotent nói về hiệu ứng dự kiến của request lặp, không hứa response byte giống nhau.

Optimistic rollback cần version/generation. A sửa title, B sửa title tiếp; A lỗi không được restore snapshot trước B. Event realtime cũng có thể duplicate hoặc out-of-order: mỗi event có ID/version, client dedup và phát hiện gap rồi resync snapshot. Reconnect không mặc nhiên phục hồi đầy đủ lịch sử.

## contract migration

Deploy FE và BE không đồng thời tuyệt đối. Field mới optional trước; server hỗ trợ old/new trong cửa sổ rõ; quan sát traffic để bỏ contract cũ. Schema validation giúp phát hiện drift nhưng không thay business validation. OpenAPI phải xuất phát từ code chạy thực tế và được kiểm tra bằng response fixture, không dựa tài liệu cũ.

Upload giới hạn ở nhiều tầng: proxy, server, parser, nghiệp vụ. Content-Type do client khai báo chưa chứng minh file an toàn; kiểm size, loại nội dung và xử lý trong vùng cách ly. Demo chỉ dùng file giả nhỏ, không đưa file riêng tư vào log.

## Lab và rubric debug

[25 lab tích hợp](../labs/integration/README.md) đều có trace sáu tầng. Khi gặp lỗi, ghi payload gửi và payload nhận trước khi sửa mapper. Dùng endpoint fixture có delay/status có chủ đích; không cần production để học.

1. Payload parse được có nghĩa contract đúng không?
2. Tại sao retry timeout tạo đơn đôi?
3. Cross-origin khác cross-site ở đâu?
4. Khi nào rollback phải bỏ qua?
5. Reconnect cần dữ liệu gì để biết đã bỏ lỡ event?

Hoàn thành khi cùng một fixture chạy qua cả hai phía, test cả lỗi/migration, và chỉ ra tầng gây lỗi bằng evidence. Đọc [08 playbook](../08_DEBUGGING_PLAYBOOK.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [INT-16](../labs/integration/INT-16.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** Rollback dùng snapshot cũ không kiểm mutation nào đã cập nhật state tiếp. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Rollback chỉ tác động state còn thuộc mutation đó.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Restore snapshot trướcA vô điều kiện.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](../web/11_INTEGRATION_FLOW.md) · [Debug method](../debug/01_EVIDENCE_METHOD.md) · [Validation](../VALIDATION.md).