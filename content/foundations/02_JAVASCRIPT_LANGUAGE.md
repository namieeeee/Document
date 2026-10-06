# Outline — JavaScript language: bindings, objects và reachable memory

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Detached method mất receiver; shallow copy vẫn shared nested state; var loop callbacks cùng binding cuối; parse ``'false'` theo truthiness cho true; exception swallowed che parser failure; static array/listener giữ graph hết hữu ích. Cách sửa theo mechanism là receiver/binding/snapshot/cleanup đúng, không thêm timer tùy ý.

Đặt câu hỏi: cơ chế trong [JavaScript language: bindings, objects và reachable memory](../../foundations/02_JAVASCRIPT_LANGUAGE.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Call tạo execution context; argument values được truyền vào parameters. Reference tới object là một value nên callee mutate pointee có thể ảnh hưởng caller, nhưng reassign parameter không reassign binding caller. Return đưa value về caller; throw chuyển điều khiển tới catch gần nhất theo stack unwind, finally thực hiện cleanup theo semantics và có thể override return/throw nếu tự return/throw.

ES modules có static import/export bindings; exported binding là live binding, không bản JSON snapshot. Module instance theo host/module graph, top-level initialization có lifecycle riêng. Circular imports có thể nhìn binding chưa initialized. Dynamic import trả Promise và belongs runtime/host.

## 3. Demo chạy thật

Claim có phạm vi: Snapshot replacement và functional update queue cho kết quả khác trong host model.

```text
node examples/web_models.mjs
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/web.log):

```text
PASS snapshot/functional queue model
```

## 4. Cách nó hỏng và cách phát hiện

Detached method mất receiver; shallow copy vẫn shared nested state; var loop callbacks cùng binding cuối; parse ``'false'` theo truthiness cho true; exception swallowed che parser failure; static array/listener giữ graph hết hữu ích. Cách sửa theo mechanism là receiver/binding/snapshot/cleanup đúng, không thêm timer tùy ý.

Console kiểm typeof/own keys/descriptors để phân biệt raw value với assumption. Breakpoint cho lexical scope và call site; heap snapshot retained paths cho biết ai còn giữ object. Đo heap sau cùng workload và cleanup, không so một lần allocation peak. Snapshot retained object cần đọc root chain; việc object còn trong console inspection cũng có thể giữ nó.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[ECMAScript specification](https://tc39.es/ecma262/2023/multipage/) cho language semantics; phần types/environments/ordinary objects. [MDN closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures), [this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this), [memory management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management) cho giải thích từng cơ chế. Không suy stack/heap vật lý từ mô hình dạy học.

1. Copy object assignment có copy graph không? Đáp án: copy reference value.
2. Closure n còn sống sau makeCounter return bằng cơ chế gì? Đáp án: reachable environment qua function.
3. Tại sao `obj.f` và detached `f()` có this khác? Đáp án: call site.
4. Hai objects có cùng fields có `===` không? Đáp án: chỉ nếu cùng identity.
5. Cycle object có phải leak? Đáp án: chỉ cần nhìn reachability/retention, cycle riêng không đủ.
6. `finally` return có thể làm mất throw không? Đáp án: có; tránh override outcome khi cleanup.

[Index](../../00_INDEX.md) · [Content](../README.md).
