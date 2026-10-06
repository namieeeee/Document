# Outline — JavaScript async runtime: jobs, host và thời gian

Mức của claim minh họa: **MODEL**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Unobserved rejection do forgot return/await; synchronous executor CPU làm block trước pending; microtask starvation; timer delayed bởi long task; stale success hoặc error ghi đè generation mới; cleanup thiếu giữ memory graph. Stale closure là binding/context cũ; stale response là permission apply hết hạn. Functional update chữa queue dependence, không chữa response owner.

Đặt câu hỏi: cơ chế trong [JavaScript async runtime: jobs, host và thời gian](../../web/02_JS_RUNTIME.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
task T bắt đầu → JS call stack chạy hết → stack rỗng
→ microtask checkpoint (drain cả jobs mới được thêm)
→ rendering opportunity khi host quyết định
→ chọn task tiếp theo
```

Timer delay là minimum scheduling eligibility có constraints/clamping, không deadline gọi đúng millisecond. Microtask liên tục enqueue chính nó có thể khiến timer/render không tiến. `await Promise.resolve()` trong CPU loop vẫn tạo microtask continuations, không bảo đảm nhường một rendering opportunity. Chunk qua task scheduling hoặc worker cần design riêng.

## 3. Demo chạy thật

Claim có phạm vi: Request completion đảo thứ tự có thể publish stale result; model có ownership guard.

```text
node examples/web_models.mjs
```

Output quan sát trích nguyên từ [evidence](../../evidence/host-models/web.log):

```text
PASS forced response race / both completion orders
```

## 4. Cách nó hỏng và cách phát hiện

Unobserved rejection do forgot return/await; synchronous executor CPU làm block trước pending; microtask starvation; timer delayed bởi long task; stale success hoặc error ghi đè generation mới; cleanup thiếu giữ memory graph. Stale closure là binding/context cũ; stale response là permission apply hết hạn. Functional update chữa queue dependence, không chữa response owner.

Console/debugger xem stack/rejection; Network ghi launch/complete và initiator; apply trace ghi requestID/generation/outcome; Performance chỉ ra long task/render delay; heap retained paths chỉ ra closure roots. Discriminating experiment buộc Bcomplete→Acomplete bằng deferred, rồi đảo thứ tự; giữ payload đúng để tách mapper/cache. Stress không fail không proof race absent.

## 5. Giới hạn trung thực

Chỉ invariant nêu trên trong host fixture; không xác minh toàn bài, MCU/native C/C++, framework hoặc production target.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[WHATWG event loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops), [ECMAScript Promise objects](https://tc39.es/ecma262/2023/multipage/control-abstraction-objects.html#sec-promise-objects), [MDN microtask guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide), [MDN async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function), [MDN execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model).

1. Promise executor chạy lúc tạo hay lúc event loop? Đáp án: sync lúc tạo.
2. Vì sao Promise.resolve().then trước timer0? Đáp án: reaction qua microtask checkpoint trước task timer trong fixture.
3. Race có cần hai callbacks cùng instruction không? Đáp án: không, interleaving operations đủ.
4. Abort có thay owner guard? Đáp án: không.
5. Await resolved Promise trong CPU loop có đảm bảo paint? Đáp án: không, microtasks có thể drain mãi.
6. `.then(()=>start())` khác `.then(()=>{start();})` khi start trả Promise thế nào? Đáp án: return giữ chain completion/failure.

[Index](../../00_INDEX.md) · [Content](../README.md).
