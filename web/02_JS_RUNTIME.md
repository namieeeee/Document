# JavaScript async runtime: jobs, host và thời gian

Phạm vi: browser HTML event loop và ECMAScript Promise; Node có phases/I/O policy riêng. Không dùng kết quả Node để chứng minh browser rendering.

## 1. Mục tiêu học

Giải thích vì sao Promise reaction trước timer trong fixture, CPU loop làm UI treo, await không tạo thread, và races tồn tại dù jobs chạy lần lượt. Vẽ launch/settle/continuation/apply để tìm owner đúng.

## 2. Kiến thức tiên quyết

[JavaScript language](../foundations/02_JAVASCRIPT_LANGUAGE.md) và [browser pipeline](13_BROWSER_INTERNALS.md); closure/bindings phải rõ trước async. Worker và server scheduling là host facilities khác.

## 3. Vấn đề mà cơ chế này giải quyết

Network/timers không thể giữ call stack JS chờ từng operation vì UI cần tiếp tục nhận input. Host tổ chức completion và engine chạy callbacks khi phù hợp. Promise cho cách biểu diễn completion/failure và kết hợp operations, không đảm bảo chúng xong theo thứ tự launch.

## 4. Khái niệm

Call stack chứa contexts đang chạy. Host APIs như timer/fetch đăng ký work ngoài language execution hiện tại. Task là đơn vị host schedule, có nhiều task sources chứ không một FIFO toàn browser universal. Microtask queue chứa Promise reactions và các callbacks được xếp như queueMicrotask; checkpoint xử lý đến khi queue rỗng. Event loop điều phối tasks/checkpoints và rendering opportunities.

## 5. Thành phần bên trong

Promise có pending/fulfilled/rejected; settlement một lần, resolved có thể đang adopt Promise khác nên không đồng nghĩa fulfilled ngay. Executor trong `new Promise(executor)` chạy đồng bộ. `.then` tạo Promise mới và đăng ký reaction; returned value/Promise quyết định fulfillment/adoption; throw quyết định rejection. Không return child Promise làm parent chain không chờ child.

Async function chạy sync tới await và trả Promise. Await thao tác với awaited value/thenable, suspension kết thúc lượt execution hiện tại của function; phần tiếp là continuation/reaction. Ngay cả await resolved Promise continuation cũng deferred theo Promise jobs; không tự schedule CPU work sang thread mới.

## 6. Data representation

Host giữ timer record/deadline, network state và callbacks; Promise giữ state/result/reactions; closure giữ lexical bindings cho continuation. Async function có logical suspended state gồm locals và resume location; engine layout không bị bài này quy định. Kết quả response đúng shape vẫn có thể thuộc generation cũ.

## 7. Control flow

```text
task T bắt đầu → JS call stack chạy hết → stack rỗng
→ microtask checkpoint (drain cả jobs mới được thêm)
→ rendering opportunity khi host quyết định
→ chọn task tiếp theo
```

Timer delay là minimum scheduling eligibility có constraints/clamping, không deadline gọi đúng millisecond. Microtask liên tục enqueue chính nó có thể khiến timer/render không tiến. `await Promise.resolve()` trong CPU loop vẫn tạo microtask continuations, không bảo đảm nhường một rendering opportunity. Chunk qua task scheduling hoặc worker cần design riêng.

## 8. Lifetime / ownership / state

Owner của request/query giữ generation đang được phép update UI. Network completion không tự thu owner cũ; khi query đổi, invalidate generation trước áp result/error/loading. Abort giảm work theo support nhưng continuation đã xếp hoặc operation khác có thể vẫn chạy; check ownership ở apply boundary.

Promise chưa settle có thể giữ closures; listener/timer phải unregister/cancel đúng handle. Worker có agent riêng, trao data qua messages/transfer/shared memory đúng APIs; không trực tiếp DOM main thread. Transfer ownership của ArrayBuffer khác copy; shared memory đòi synchronization riêng.

## 9. Invariants

Mỗi Promise cần failure observation nếu caller cần biết outcome; child work không bị detached ngoài contract. Chỉ generation hiện hành đổi visible state và loading/error. Main-thread task duration phải có budget để input/render tiến. Cancelled owner không được publish state dù underlying operation đã settle success. Queues/backpressure phải bounded nếu producer nhanh.

### Theo dấu stack và microtask checkpoint

**Mô hình browser**, script tạo Promise reaction P và timer T. Script hiện tại chạy tới hết; timer có đủ thời gian chờ cũng chưa thể chen giữa cùng job. Khi host thực hiện microtask checkpoint, P chạy; nếu P tạo microtask Q thì Q cũng được drain theo checkpoint. Sau đó event loop mới có thể chọn task khác như T và có rendering opportunity theo host rules.

Đừng suy “mỗi task chắc chắn có một frame paint”. Browser có thể không render ở mọi lượt. Chuỗi microtasks liên tục tạo thêm microtasks có thể trì hoãn task/render; đổi loop CPU sang Promise recursion không tự tạo responsiveness.

Await trong async function suspend continuation khi phù hợp semantics, không tạo thread. CPU loop sau await vẫn chiếm execution của job đang resume. Worker tạo execution environment khác để chạy work phù hợp, nhưng message transfer/copy/shared-memory synchronization là protocol riêng.

### Race là interleaving của operations qua nhiều jobs

Request A bắt đầu, request B bắt đầu sau, B hoàn tất trước, A hoàn tất sau. Mỗi callback chạy riêng hoàn toàn tuần tự vẫn có thể ghi kết quả cũ đè mới. Boundary cần bảo vệ là “response thuộc intent active”, không “callback không chạy đồng thời”. Mô hình owner/generation làm prediction rõ: callback A nhìn generation khác thì bỏ apply; cancel tiết kiệm work nhưng không thay owner check.

## 10. Ví dụ tối thiểu

Đoạn JS độc lập, **dự đoán** A B M T trong fixture không có work khác:

```js
console.log('A');
setTimeout(() => console.log('T'), 0);
Promise.resolve().then(() => console.log('M'));
console.log('B');
```

Race timeline: launch A(g1), launch B(g2), complete B→apply g2, complete A→reject apply g1. Từng callback có thể chạy trọn vẹn nhưng final value vẫn sai nếu không guard. Minimal guard fragment:

```js
let generation = 0;
async function load(query) {
  const mine = ++generation;
  const data = await read(query); // read là dependency fixture
  if (mine === generation) publish(data);
}
```

Fragment chưa xử lý error/loading/disposal; các paths ấy phải cùng owner check. `read/publish` là helpers application, không APIs JS chuẩn.

## 11. Failure modes

Unobserved rejection do forgot return/await; synchronous executor CPU làm block trước pending; microtask starvation; timer delayed bởi long task; stale success hoặc error ghi đè generation mới; cleanup thiếu giữ memory graph. Stale closure là binding/context cũ; stale response là permission apply hết hạn. Functional update chữa queue dependence, không chữa response owner.

## 12. Debug / observability

Console/debugger xem stack/rejection; Network ghi launch/complete và initiator; apply trace ghi requestID/generation/outcome; Performance chỉ ra long task/render delay; heap retained paths chỉ ra closure roots. Discriminating experiment buộc Bcomplete→Acomplete bằng deferred, rồi đảo thứ tự; giữ payload đúng để tách mapper/cache. Stress không fail không proof race absent.

## 13. Liên hệ với bug/lab hiện có

[FE-05](../labs/frontend/FE-05.md), [FE-06](../labs/frontend/FE-06.md): owner applies result/loading. [FE-04](../labs/frontend/FE-04.md): cleanup releases timer. [OS-08](../labs/os/OS-08.md): CPU callback chiếm agent. [Host model](../examples/web_models.mjs) có deferred fixture; phạm vi thực thi ở [VALIDATION](../VALIDATION.md).

## 14. Sai lầm thường gặp

Không gọi async là parallel, Promise là background thread, await là CPU preemption. Không bọc synchronous work trong Promise rồi suy nó không block. Timeout 0 không bảo đảm chạy trước Promise reaction. Catch rồi trả empty data có thể biến failure thành success; state machine cần thể hiện error rõ.

## 15. Câu hỏi tự kiểm tra

1. Promise executor chạy lúc tạo hay lúc event loop? Đáp án: sync lúc tạo.
2. Vì sao Promise.resolve().then trước timer0? Đáp án: reaction qua microtask checkpoint trước task timer trong fixture.
3. Race có cần hai callbacks cùng instruction không? Đáp án: không, interleaving operations đủ.
4. Abort có thay owner guard? Đáp án: không.
5. Await resolved Promise trong CPU loop có đảm bảo paint? Đáp án: không, microtasks có thể drain mãi.
6. `.then(()=>start())` khác `.then(()=>{start();})` khi start trả Promise thế nào? Đáp án: return giữ chain completion/failure.

## 16. Nguồn

[WHATWG event loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops), [ECMAScript Promise objects](https://tc39.es/ecma262/2023/multipage/control-abstraction-objects.html#sec-promise-objects), [MDN microtask guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide), [MDN async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function), [MDN execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model).

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
