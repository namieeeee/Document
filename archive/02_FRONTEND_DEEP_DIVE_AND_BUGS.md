# 02 — Frontend: state, thời gian và ranh giới chạy

> Historical overview, superseded as a teaching source. Original content is retained for traceability; execution claims and snippets are not upgraded by this archive. [Current navigation](../02_FRONTEND_DEEP_DIVE_AND_BUGS.md).


## Học cơ chế trước lab — bổ sung 2026-10-06

Giữ phần overview dưới để ôn; phần học nền chi tiết ở các bài sau:

- [Web02 — JavaScript: execution, thời gian và memory](../web/02_JS_RUNTIME.md)
- [Web03 — TypeScript: mô hình tĩnh và dữ liệu thật](../web/03_TYPESCRIPT_BOUNDARIES.md)
- [Web04 — React: render, identity và lifetime](../web/04_REACT_MENTAL_MODEL.md)
- [Web05 — Next.js: nơi chạy và boundary dữ liệu](../web/05_NEXT_EXECUTION.md)

Mục tiêu: giải thích một render dùng dữ liệu nào, kiểm soát async và tìm lỗi browser bằng evidence. Tiền đề: JavaScript hàm/array, chương 01. Các snippet React cần dự án React có sẵn, không phải file chạy trực tiếp bằng Node.

## event loop khác React render

JavaScript trên một agent xử lý job lần lượt; browser cung cấp network/timer và event loop. `await` nhường continuation, không tự tạo thread cho code CPU nặng. Công việc tính toán 200 ms trong handler vẫn làm UI khựng. Worker có agent riêng; dùng worker cần thiết kế dữ liệu truyền và cancellation. Theo [MDN execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model), host và engine là hai phần của mô hình thực thi.

React render đọc một snapshot state. Handler được tạo trong render giữ snapshot ấy; gọi setter xếp update chứ không đổi biến của handler đang chạy. Đó là lý do ba lần `setN(n+1)` không tương đương ba phép tăng liên tiếp. Khi cần dựa trên state trước, dùng updater; khi async result thuộc request cũ, updater không giải quyết ownership của request. [React state snapshot](https://react.dev/learn/state-as-a-snapshot) và [effects](https://react.dev/learn/synchronizing-with-effects) là hai khái niệm riêng.

```jsx
// Trong component; n/setN đến từ useState(0).
function incrementThree() {
  setN(v => v + 1);
  setN(v => v + 1);
  setN(v => v + 1);
}
```

## effect là đồng bộ hóa

Dùng effect khi đồng bộ với hệ thống bên ngoài: subscription, timer, fetch. Giá trị tính được từ props/state thường tính trong render; thêm effect để cập nhật derived state tạo extra render và thời điểm lệch. Cleanup giải phóng chính resource của lần setup đó. Dev Strict Mode có thể chạy setup/cleanup thêm để tìm lỗi; không sửa bằng cách tắt Strict Mode.

Fetch query A mất 300 ms, B mất 20 ms; người dùng gõ A rồi B. Nếu mỗi response đều set state, A đến cuối ghi đè B. Có thể abort request cũ để giảm công việc, nhưng vẫn cần guard generation/ignore khi API hoặc continuation chưa được hủy. Chỉ cho request còn sở hữu UI cập nhật loading/error; nếu không spinner của B cũng bị A tắt. Đối chiếu Network timeline với request key trước khi nghi React cache.

Controlled input lấy value từ state; uncontrolled dùng DOM/defaultValue. Không đổi giữa undefined và string trong cùng vòng đời; khởi tạo `''` hoặc chọn uncontrolled có chủ đích. Key phải đại diện identity ổn định, không vị trí trong list có reorder. Mutation array/object có thể phá so sánh identity; copy phần thay đổi, tránh deep clone toàn tree nếu không cần.

## Next.js và browser boundary

App Router dùng Server Components mặc định cho page/layout theo tài liệu hiện hành. Client boundary cần khi dùng state, effect, event handler hoặc browser API; không đưa secret sang props client. Hydration cần HTML server và render đầu tiên client tương thích: thời gian, random và locale phải có chiến lược. `window` không tồn tại trong môi trường server. [Nguồn Next.js](https://nextjs.org/docs/app/getting-started/server-and-client-components).

Cache không chỉ có một tầng: browser HTTP, client query state, router/render và data cache có vòng đời khác nhau. Next.js thay đổi cách cấu hình qua phiên bản; đọc lockfile và trạng thái Cache Components trước khi áp dụng `revalidate`/`use cache`. [Hướng dẫn caching hiện hành](https://nextjs.org/docs/app/getting-started/caching) và [mô hình trước đó](https://nextjs.org/docs/app/guides/caching-without-cache-components) không nên trộn mặc định.

## dữ liệu vào là dữ liệu chưa tin cậy

TypeScript assertion `as Task` không validate JSON. Parse shape và domain boundary; hiện error khi payload sai, không silently chuyển mọi thứ thành string. [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) giải thích runtime checks thu hẹp type. Không render HTML user bằng API HTML trực tiếp nếu chưa có sanitization phù hợp. CORS là cơ chế browser kiểm soát đọc response, không thay authorization. Secret bundling là lỗi kiến trúc, không thể sửa bằng tên biến khó đoán.

Tiền nên tính minor unit phù hợp currency, có quy tắc rounding; ngày-only không tự biến thành instant UTC. Accessibility là hành vi: label gắn input, keyboard tới được nút, focus/error thông báo được; màu đẹp không chứng minh accessible.

## Thực hành

[25 lab FE](../labs/frontend/README.md) chia state/effect, async, boundary và UX. Dùng DevTools Network/Console/Elements, giữ cache setting và build mode trong biên bản. Đo cùng fixture trước/sau fix.

1. Stale closure khác stale response ở đâu?
2. Vì sao dependencies đúng vẫn có fetch race?
3. Type assertion có ngăn API trả null không?
4. Component chạy server được dùng loại dữ liệu nào?
5. Một loading boolean có đủ cho hai request song song không?

Hoàn thành khi tự dựng timeline render/request và chứng minh lab không tái diễn khi đảo thứ tự response. Tiếp [04](../04_FE_BE_INTEGRATION_AND_REAL_BUGS.md).

## Debug section — bài kiểm tra giải thích được cơ chế

- **SYMPTOM:** mô tả outcome quan sát của [FE-09](../labs/frontend/FE-09.md); không dùng tên bug làm triệu chứng.
- **EVIDENCE:** dùng mục Evidence/Reproduction trong lab; ghi build/version, raw state/owner và timeline.
- **POSSIBLE CAUSES:** React giữ instance theo key nhưng index đổi nghĩa sau khi xóa/reorder. Chỉ xem đây là một giả thuyết; thêm một nguyên nhân cạnh tranh từ bài nền.
- **DISTINGUISHING TEST:** replay trigger với thứ tự actors được điều khiển; so raw input/output với state sau từng boundary, giữ một yếu tố thay đổi mỗi lượt.
- **ROOT CAUSE:** chỉ kết luận khi thấy operation đầu phá invariant: Local state/focus thuộc đúng identity entity khi list thay đổi.
- **FIX:** thực hiện Fix của lab sau evidence; giữ contract/feature và scope thay đổi.
- **WRONG FIX:** Random key khiến toàn list remount và mất state/focus.
- **REGRESSION TEST:** replay trigger gốc và một case biên/đảo thứ tự, kiểm cleanup/error paths; báo chạy thật khác model/review tĩnh.

[Bài nền liên quan](../web/04_REACT_MENTAL_MODEL.md) · [Debug method](../debug/01_EVIDENCE_METHOD.md) · [Validation](../VALIDATION.md).