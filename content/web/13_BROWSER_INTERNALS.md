# Outline — Browser: từ parser tới pixels, events và storage

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Layout thrashing do geometry read khi style/layout dirty; long JS task trì hoãn input/frame; detached-node retention qua listener; quota/blocked storage tạo exception; event handler vừa custom submit vừa default submit tạo duplicate. XSS đọc client storage khi same-origin malicious script chạy. Sửa theo bước đầu sai: layout batching, cleanup, canceled default action hoặc boundary encoding.

Đặt câu hỏi: cơ chế trong [Browser: từ parser tới pixels, events và storage](../../web/13_BROWSER_INTERNALS.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
HTML bytes → tokens → DOM
CSS bytes → rules → CSSOM
DOM + CSSOM → computed style/render objects → layout → paint → composite
input event → event path → listeners → default action nếu chưa canceled
```

Capture đi từ ancestors tới target; target phase gọi listeners phù hợp; bubble đi ngược khi event có bubbles. `stopPropagation()` ảnh hưởng traversal, không tự cancel default action; `preventDefault()` cần event cancelable và listener không passive theo rules. Không mọi event bubble, ví dụ focus behavior cần chọn event/registration đúng.

## 3. Demo chạy thật

Claim có phạm vi: DOM/render/accessibility state phải tương ứng cùng UI intent; input có accessible name/focus/error path. Listener và subscription được cleanup đúng identity. Không trust localStorage/IndexedDB để quyết định quyền server. Khi đo performance, workload và viewport/device phải được giữ để so sánh. Storage writes success không phải durability guarantee cho business server.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../web/13_BROWSER_INTERNALS.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Layout thrashing do geometry read khi style/layout dirty; long JS task trì hoãn input/frame; detached-node retention qua listener; quota/blocked storage tạo exception; event handler vừa custom submit vừa default submit tạo duplicate. XSS đọc client storage khi same-origin malicious script chạy. Sửa theo bước đầu sai: layout batching, cleanup, canceled default action hoặc boundary encoding.

Elements kiểm DOM/computed box; Performance phân biệt scripting/style/layout/paint và long tasks; heap snapshot retained path cho detached nodes; Application panel cho stores/quota/cookies; accessibility tree và keyboard cho usable flow. Network không chứng minh layout. Logic measurement: giữ API fixture cố định, đổi geometry access pattern, so trace cùng viewport/zoom/input dài.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[WHATWG HTML](https://html.spec.whatwg.org/multipage/), [DOM event dispatch](https://dom.spec.whatwg.org/#concept-event-dispatch), [MDN critical rendering path](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path), [MDN storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API), [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API), [MDN box sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing).

1. Vì sao color change có thể repaint mà không reflow? Đáp án: geometry không đổi.
2. Đọc offsetWidth sau write style có thể tốn gì? Đáp án: flush layout để trả geometry hiện tại.
3. Stop bubble có tự ngăn form default submit? Đáp án: không.
4. Store client có cho role đáng tin không? Đáp án: không, server authority riêng.
5. DOM node bị remove nhưng heap còn tăng cần xem gì? Đáp án: retained roots/listeners.
6. Origin isolation có bảo vệ khỏi XSS cùng origin? Đáp án: không.

[Index](../../00_INDEX.md) · [Content](../README.md).
