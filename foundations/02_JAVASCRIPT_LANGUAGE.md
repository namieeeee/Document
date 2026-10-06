# JavaScript language: bindings, objects và reachable memory

Phạm vi: semantics ECMAScript thông dụng, browser modules; không cam kết layout memory của engine. [Async runtime](../web/02_JS_RUNTIME.md) học sau bài này.

## 1. Mục tiêu học

Giải thích một assignment copy gì, lookup tên/property đi đâu, closure giữ gì, `this` được chọn thế nào và object nào còn reachable. Phải tự dự đoán một đoạn JS trước khi đọc component React.

## 2. Kiến thức tiên quyết

Biến, điều kiện, vòng lặp và gọi hàm ở mức nhận biết. [Network foundation](../web/01_HTTP_BROWSER.md) giúp hiểu module/fetch nhưng không quyết định semantics ngôn ngữ.

## 3. Vấn đề mà cơ chế này giải quyết

JS cho phép biểu diễn dữ liệu động và hàm như giá trị. Để hiểu mutation, callback, module và memory retention cần tách binding với object identity. Runtime không kiểm ý nghĩa nghiệp vụ của object, và GC không biết người dùng đã đóng trang chức năng nào.

## 4. Khái niệm

Primitives gồm undefined, null, boolean, number, bigint, string, symbol. Primitive value bất biến; assignment tạo binding khác chứa cùng value. Number thường theo IEEE 754 binary64; số nguyên vượt safe range mất precision, BigInt không tự serialize thành JSON Number. Object là tập properties có identity; arrays/functions cũng là objects, không phải primitive.

`===` không coercion nhưng `NaN!==NaN` và `+0===-0`; `Object.is` nhận ra NaN bằng chính nó và phân biệt hai zero. `==` dùng coercion nên `0==false` có thể true; khi contract đòi boolean thật phải kiểm type, không đổi tất cả sang truthiness.

## 5. Thành phần bên trong

Binding thuộc lexical environment. Khi đọc tên, lookup từ môi trường hiện tại ra các outer environments; block `let/const` khác function-scoped `var`. Trước initialization trong temporal dead zone, binding không dùng được. `const` cấm reassign binding, vẫn cho phép mutate object mà binding trỏ tới.

Function object chứa code và môi trường lexical cần thiết. Closure có thể tồn tại sau return vì callback còn reachable, không vì stack frame vật lý luôn nằm nguyên. `this` của function thường do call site: `obj.method()` khác `const f=obj.method; f()`. Arrow lấy `this` lexical từ nơi tạo; `call/bind` không đổi `this` lexical của arrow.

## 6. Data representation

`const a={n:1}; const b=a` tạo hai bindings tham chiếu cùng object. `b.n=2` làm `a.n` thành 2. `{...a}` tạo object mới nhưng chỉ copy property values; nested object vẫn shared. Array là object có cơ chế length/index, holes khác explicit undefined ở một số operations.

Property lookup trước tìm own property, sau đi prototype chain tới null. `class` cung cấp syntax methods/prototype và construction; không copy mọi method vào từng instance. Private fields có rules riêng; không dùng inheritance như cách tự động deep-copy state.

## 7. Control flow

Call tạo execution context; argument values được truyền vào parameters. Reference tới object là một value nên callee mutate pointee có thể ảnh hưởng caller, nhưng reassign parameter không reassign binding caller. Return đưa value về caller; throw chuyển điều khiển tới catch gần nhất theo stack unwind, finally thực hiện cleanup theo semantics và có thể override return/throw nếu tự return/throw.

ES modules có static import/export bindings; exported binding là live binding, không bản JSON snapshot. Module instance theo host/module graph, top-level initialization có lifecycle riêng. Circular imports có thể nhìn binding chưa initialized. Dynamic import trả Promise và belongs runtime/host.

## 8. Lifetime / ownership / state

Stack là mô hình execution contexts đang hoạt động; heap là mô hình object động, không quy tắc mọi primitive luôn stack. GC bắt đầu từ roots như globals, executing contexts và host references tới listeners; traverse reachable graph rồi có thể thu phần không reachable. Cycles không tự là leak nếu cả cycle không reachable.

Ownership nghiệp vụ: module tạo listener phải unregister đúng callback khi hết dùng; listener giữ closure, closure giữ array lớn làm retention. Garbage collection không có deadline release file/socket từ API native. Shared object cần policy mutation hoặc snapshot; lifetime live không đồng nghĩa owner được quyền sửa.

## 9. Invariants

Không mutate snapshot mà actor khác đang coi là immutable. Lookup phải theo environment/property model đúng; callback dùng `this` phù hợp contract. External value phải được kiểm type/shape trước operations. Resource subscriptions có setup/cleanup theo cùng identity; error không bị nuốt thành success. Code có thể đúng type nhưng sai đơn vị hoặc state transition.

## 10. Ví dụ tối thiểu

Chạy trong console hoặc Node; kết quả là **dự đoán**, không terminal output:

```js
const makeCounter = () => {
  let n = 0;
  return () => ++n;
};
const next = makeCounter();
console.log(next(), next()); // 1 2: closure giữ binding n
const a = { nested: { done: false } };
const b = { ...a };
b.nested.done = true;
console.log(a.nested.done); // true: shallow copy
```

Hàm tạo counter khác sẽ có environment n khác. Freeze object bên ngoài không tự deep-freeze nested object; chốt immutable contract tới độ sâu cần thiết.

## 11. Failure modes

Detached method mất receiver; shallow copy vẫn shared nested state; var loop callbacks cùng binding cuối; parse ``'false'` theo truthiness cho true; exception swallowed che parser failure; static array/listener giữ graph hết hữu ích. Cách sửa theo mechanism là receiver/binding/snapshot/cleanup đúng, không thêm timer tùy ý.

## 12. Debug / observability

Console kiểm typeof/own keys/descriptors để phân biệt raw value với assumption. Breakpoint cho lexical scope và call site; heap snapshot retained paths cho biết ai còn giữ object. Đo heap sau cùng workload và cleanup, không so một lần allocation peak. Snapshot retained object cần đọc root chain; việc object còn trong console inspection cũng có thể giữ nó.

## 13. Liên hệ với bug/lab hiện có

[FE-10](../labs/frontend/FE-10.md): identity và mutation snapshot. [FE-01](../labs/frontend/FE-01.md): closure trong React cần thêm [render snapshot](../web/04_REACT_MENTAL_MODEL.md). [OS-05](../labs/os/OS-05.md): retention có model dùng chung, không đồng nhất managed GC với malloc.

## 14. Sai lầm thường gặp

Closure không luôn là giá trị đóng băng; nó giữ binding lexical. `const`, spread và `class` không tự cho immutable/ownership. Prototype chain không phải scope chain. Try/catch quanh một function không bắt lỗi async chưa được await; phần đó học ở runtime.

## 15. Câu hỏi tự kiểm tra

1. Copy object assignment có copy graph không? Đáp án: copy reference value.
2. Closure n còn sống sau makeCounter return bằng cơ chế gì? Đáp án: reachable environment qua function.
3. Tại sao `obj.f` và detached `f()` có this khác? Đáp án: call site.
4. Hai objects có cùng fields có `===` không? Đáp án: chỉ nếu cùng identity.
5. Cycle object có phải leak? Đáp án: chỉ cần nhìn reachability/retention, cycle riêng không đủ.
6. `finally` return có thể làm mất throw không? Đáp án: có; tránh override outcome khi cleanup.

## 16. Nguồn

[ECMAScript specification](https://tc39.es/ecma262/2023/multipage/) cho language semantics; phần types/environments/ordinary objects. [MDN closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures), [this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this), [memory management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management) cho giải thích từng cơ chế. Không suy stack/heap vật lý từ mô hình dạy học.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
