# Outline — React: render snapshots, identity và commit

Mức của claim minh họa: **VERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Stale closure đọc render cũ; stale response hết owner apply; dependency thiếu giữ resource room cũ; effect loop vì dependency identity mới mỗi update; shared mutation làm old snapshot đổi; random keys mất focus; derived duplicate state lệch. Mỗi lỗi có invariant khác; useCallback không tự cho latest closure, functional update không tự cancel request.

Đặt câu hỏi: cơ chế trong [React: render snapshots, identity và commit](../../web/04_REACT_MENTAL_MODEL.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Event handler của render R đọc propsR/stateR
→ enqueue updates → React chọn render R+1
→ tính elements → reconciliation
→ commit DOM + layout effect lifecycle
→ passive effect lifecycle theo scheduling
→ browser layout/paint theo pipeline
```

Event handler tương ứng user action, ví dụ submit POST theo explicit intent. Effect đồng bộ external resource với committed reactive values: subscription/timer/network. Derived total từ price×qty tính trong render; copy total vào state qua effect tạo hai nguồn sự thật và một render lệch.

Passive effect không có luật tuyệt đối luôn sau paint trong mọi circumstance; useLayoutEffect trước repaint có thể block paint. Chọn effect theo cần đo/đồng bộ, không giữ CPU lâu.

## 3. Demo chạy thật

Claim có phạm vi: Effect cleanup stale guard giữ B khi phản hồi A tới sau B trong React DOM fixture.

```text
cd examples/react-race && python verify.py
```

Output quan sát trích nguyên từ [evidence](../../evidence/react-race/fixed.log):

```text

 RUN  v5.0.3 C:/Users/Trann/Work_Space/Document_Code/knowledge_base/examples/react-race

 × race.test.js > keeps latest result when B completes before stale A 38ms
   → expected 'A' to be 'B' // Object.is equality
 ✓ race.test.js > publishes B when responses complete in request order 6ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  race.test.js > keeps latest result when B completes before stale A
AssertionError: expected 'A' to be 'B' // Object.is equality

Expected: "B"
Received: "A"

 ❯ race.test.js:29:62
     27|   await settle('A');
     28|   // This invariant is identical for both implementations. Broken obse…
     29|   expect(screen.getByLabelText('search result').textContent).toBe('B');
       |                                                              ^
     30| });
     31|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 1 passed (2)
   Start at  10:48:33
   Duration  13.54s (environment 86%, import 13%)

JSON report written to C:/Users/Trann/Work_Space/Document_Code/knowledge_base/evidence/react-race/broken.json


 RUN  v5.0.3 C:/Users/Trann/Work_Space/Document_Code/knowledge_base/examples/react-race

 ✓ race.test.js > keeps latest result when B completes before stale A 30ms
 ✓ race.test.js > publishes B when responses complete in request order 4ms

 Test Files  1 passed (1)
      Tests  2 passed (2)
   Start at  10:48:49
   Duration  1.65s (environment 81%, import 13%, transform 3%, tests 2%)

JSON report written to C:/Users/Trann/Work_Space/Document_Code/knowledge_base/evidence/react-race/fixed.json

```

## 4. Cách nó hỏng và cách phát hiện

Stale closure đọc render cũ; stale response hết owner apply; dependency thiếu giữ resource room cũ; effect loop vì dependency identity mới mỗi update; shared mutation làm old snapshot đổi; random keys mất focus; derived duplicate state lệch. Mỗi lỗi có invariant khác; useCallback không tự cho latest closure, functional update không tự cancel request.

### Một effect cần giữ protocol setup/cleanup

Effect subscribe source S: commit S → setup subscribe S; dependency đổi T → cleanup subscription S → setup T; unmount → cleanup T. Handler callback có closure của render tạo nó. Cleanup phải tháo chính listener/subscription đã đăng ký; mutable global “current listener” có thể tháo nhầm.

Với async response, cleanup có thể signal cancellation nhưng một callback đã tới vẫn cần kiểm owner/generation trước apply. Ref giữ mutable cell qua renders nhưng đổi ref.current không yêu cầu rerender; state dành cho thông tin phải hiện trên UI. Memo tối ưu work có thể được tính lại/bỏ cache; correctness phải đúng khi không có memo.

React DevTools quan sát props/state/component identity; Profiler quan sát commits/render work theo fixture; browser Performance cho JS/layout/paint và Network cho request order. Discriminating test cố định raw items rồi reorder để phân biệt key bug với API data sai. Log setup/cleanup IDs để xem resource leak; đừng coi số render trong dev là số business actions.

## 5. Giới hạn trung thực

React DOM/jsdom với hai Promise schedules; không phải HTTP, browser paint, StrictMode hay kiểm chứng toàn bộ React.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[React versions](https://react.dev/versions), [render/commit](https://react.dev/learn/render-and-commit), [snapshot](https://react.dev/learn/state-as-a-snapshot), [queue updates](https://react.dev/learn/queueing-a-series-of-state-updates), [identity](https://react.dev/learn/preserving-and-resetting-state), [effects](https://react.dev/learn/synchronizing-with-effects), [context](https://react.dev/learn/passing-data-deeply-with-context), [useMemo](https://react.dev/reference/react/useMemo). Docs hiện hành, bài giới hạn contracts React19 nêu trên.

1. Setter đổi n của handler đang chạy không? Đáp án: không.
2. Render không commit có được POST không? Đáp án: không, side effect sẽ không theo committed lifecycle.
3. Context value object mới ảnh hưởng gì? Đáp án: consumer update, cần đo trước memo.
4. useMemo giữ resource acquisition luôn một lần không? Đáp án: không.
5. Cleanup abort có đủ chống stale state? Đáp án: thêm ownership guard.
6. Input initial undefined rồi string có owner thế nào? Đáp án: chuyển mode ngoài contract.
7. Derived subtotal nên ở đâu? Đáp án: tính từ nguồn hiện hành, trừ khi state có semantics độc lập.

[Index](../../00_INDEX.md) · [Content](../README.md).
