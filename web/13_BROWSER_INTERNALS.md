# Browser: từ parser tới pixels, events và storage

Phạm vi: HTML/DOM standards và mô hình rendering phổ biến. Pipeline là mô hình trách nhiệm; engine có thể gộp/skip các bước, không một implementation cycle cố định.

## 1. Mục tiêu học

Vẽ DOM/CSSOM→style/render tree→layout→paint→composite; dự đoán thay đổi nào có thể gây layout. Theo event qua capture/target/bubble/default action và chọn store theo lifetime/trust boundary.

## 2. Kiến thức tiên quyết

[HTTP](12_HTTP_SEMANTICS.md) và [JavaScript language](../foundations/02_JAVASCRIPT_LANGUAGE.md). Event-loop scheduling học ở [JS runtime](02_JS_RUNTIME.md), không giả mọi frame chạy sau mỗi event.

## 3. Vấn đề mà cơ chế này giải quyết

Bytes HTML/CSS không tự là pixels. Browser phải parse, tính style, vị trí và vẽ; cùng lúc nó phải dispatch input, chạy script và cách ly origins. UI chậm có thể đến từ layout/paint hoặc JS, không chỉ component renders.

## 4. Khái niệm

DOM là tree objects biểu diễn document; parser tiêu thụ HTML token và áp rules tree construction, có thể sửa cấu trúc invalid. CSSOM biểu diễn stylesheet/rules. Style resolution/cascade chọn computed styles theo selector, specificity, inheritance và layout inputs. Render tree/layout tree chứa đối tượng cần rendering; node display:none không tham gia layout như node visible; accessibility tree có mapping khác DOM.

## 5. Thành phần bên trong

HTML parser có thể bị parser-blocking script tác động; script có thể sửa DOM khi parse đang diễn ra. Stylesheet loading/cascade ảnh hưởng thời điểm style/script trong từng trường hợp. Sau style, layout tính geometry; paint tạo drawing instructions; raster tạo pixels; composite ghép layers. Scroll/transform trên composited layer có thể tránh full layout nhưng không hứa mọi transform miễn main-thread work.

Reflow là công việc layout lại; repaint là thay pixels mà geometry có thể giữ; composite đổi cách ghép. Đổi width thường dirty layout, đổi color thường dirty paint, engine quyết định phạm vi invalidation.

## 6. Data representation

DOM node giữ properties/listeners và liên kết parent/child. CSSOM giữ rules; computed style/layout caches giữ kết quả tới invalidation. Bitmap/layers dùng memory CPU/GPU theo implementation. `getBoundingClientRect()` trả geometry ở hệ tọa độ viewport tại thời điểm query, không số layout của React.

Storage: cookie là record với attributes và có thể tự gửi HTTP; localStorage là string key/value sync theo origin; sessionStorage theo origin và page session/tab rules, không server session; IndexedDB là object store/index/transaction async theo origin. Quota, eviction và partitioning chịu browser policy; dữ liệu client không tự trusted.

## 7. Control flow

```text
HTML bytes → tokens → DOM
CSS bytes → rules → CSSOM
DOM + CSSOM → computed style/render objects → layout → paint → composite
input event → event path → listeners → default action nếu chưa canceled
```

Capture đi từ ancestors tới target; target phase gọi listeners phù hợp; bubble đi ngược khi event có bubbles. `stopPropagation()` ảnh hưởng traversal, không tự cancel default action; `preventDefault()` cần event cancelable và listener không passive theo rules. Không mọi event bubble, ví dụ focus behavior cần chọn event/registration đúng.

## 8. Lifetime / ownership / state

Browser owns document tree đến navigation/destruction; script references có thể giữ detached nodes. Component remove DOM không tự unregister listener ở window; callback vẫn reachable. Cache layout có lifetime tới dirty operation. Store dữ liệu client có lifecycle độc lập component, có thể sống qua reload; logout phải xem caches/storage quyền nhạy cảm theo design.

Same-origin policy hạn chế cross-origin script access, CORS có thể nới read policy theo response. Origin isolation không chữa XSS code đang chạy cùng origin. Cookie HttpOnly hạn chế script đọc credential nhưng không mọi authenticated actions.

## 9. Invariants

DOM/render/accessibility state phải tương ứng cùng UI intent; input có accessible name/focus/error path. Listener và subscription được cleanup đúng identity. Không trust localStorage/IndexedDB để quyết định quyền server. Khi đo performance, workload và viewport/device phải được giữ để so sánh. Storage writes success không phải durability guarantee cho business server.

## 10. Ví dụ tối thiểu

Fragment browser **chưa chạy riêng**:

```js
const widths = rows.map(row => row.getBoundingClientRect().width);
rows.forEach((row, i) => { row.style.width = `${widths[i] + 1}px`; });
```

Batch reads rồi writes giảm read-after-write layout forcing. Vòng `row.style.width=...; row.offsetWidth` từng element có thể buộc sync layout nhiều lần; cần Performance trace chứng minh, không hứa exact số reflows.

Form submit event có thể `preventDefault()` để dùng custom submit; click propagation stop riêng không bảo đảm form không submit. Một input placeholder không thay label liên kết bằng for/id.

## 11. Failure modes

Layout thrashing do geometry read khi style/layout dirty; long JS task trì hoãn input/frame; detached-node retention qua listener; quota/blocked storage tạo exception; event handler vừa custom submit vừa default submit tạo duplicate. XSS đọc client storage khi same-origin malicious script chạy. Sửa theo bước đầu sai: layout batching, cleanup, canceled default action hoặc boundary encoding.

## 12. Debug / observability

Elements kiểm DOM/computed box; Performance phân biệt scripting/style/layout/paint và long tasks; heap snapshot retained path cho detached nodes; Application panel cho stores/quota/cookies; accessibility tree và keyboard cho usable flow. Network không chứng minh layout. Logic measurement: giữ API fixture cố định, đổi geometry access pattern, so trace cùng viewport/zoom/input dài.

## 13. Liên hệ với bug/lab hiện có

[FE-23](../labs/frontend/FE-23.md): content-box width+padding vượt viewport; invariant controls còn reachable. [FE-24](../labs/frontend/FE-24.md): accessible name không được phụ thuộc placeholder. [FE-04](../labs/frontend/FE-04.md): lifetime listener/timer. [FE-19](../labs/frontend/FE-19.md): HTML sink/trust boundary.

## 14. Sai lầm thường gặp

DOM không bằng render tree hay accessibility tree. `display:none` khác opacity:0 về layout/access behavior. localStorage không gửi tự động như cookie và không tự là session. `preventDefault` không stop propagation; async await trước cancel có thể quá trễ trong dispatch. Hide overflow có thể che bug và control, cần fix box constraints.

## 15. Câu hỏi tự kiểm tra

1. Vì sao color change có thể repaint mà không reflow? Đáp án: geometry không đổi.
2. Đọc offsetWidth sau write style có thể tốn gì? Đáp án: flush layout để trả geometry hiện tại.
3. Stop bubble có tự ngăn form default submit? Đáp án: không.
4. Store client có cho role đáng tin không? Đáp án: không, server authority riêng.
5. DOM node bị remove nhưng heap còn tăng cần xem gì? Đáp án: retained roots/listeners.
6. Origin isolation có bảo vệ khỏi XSS cùng origin? Đáp án: không.

## 16. Nguồn

[WHATWG HTML](https://html.spec.whatwg.org/multipage/), [DOM event dispatch](https://dom.spec.whatwg.org/#concept-event-dispatch), [MDN critical rendering path](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path), [MDN storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API), [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API), [MDN box sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
