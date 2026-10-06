# React: render snapshots, identity và commit

Phạm vi: React 19, client renderer. Không dựa experimental Compiler hay scheduling internals như guarantee. [Next execution](05_NEXT_EXECUTION.md) bổ sung RSC/SSR.

## 1. Mục tiêu học

Vẽ event→update queue→render→reconciliation→commit→effects; giải thích snapshot nào handler đọc, state được giữ theo identity nào và cleanup thuộc setup nào. Chỉ dùng hooks sau khi mô hình component/render rõ.

## 2. Kiến thức tiên quyết

[JS bindings/closure](../foundations/02_JAVASCRIPT_LANGUAGE.md), [runtime](02_JS_RUNTIME.md), immutable snapshot và browser DOM. TypeScript hữu ích nhưng không bắt buộc React semantics.

## 3. Vấn đề mà cơ chế này giải quyết

UI là hàm của dữ liệu nhưng imperative DOM edits dễ lệch nhau khi nhiều events thay state. React giữ state và tính tree mô tả để cập nhật UI nhất quán. Scheduling có thể thử/bỏ render nên mọi business effect phải được đặt theo lifecycle thật, không theo số lần function được gọi.

## 4. Khái niệm

Component là function/type dùng tạo elements. Element là mô tả UI với type/props/key, không DOM node. Render đọc props/state snapshot và trả tree; reconciliation đối chiếu tree để chọn preserved/replaced instances; commit áp thay đổi lên host DOM. Render ≠ commit: một render có thể không được commit. State ≠ mutable local variable: setter enqueue update cho một render tương lai.

## 5. Thành phần bên trong

React giữ component instances và hooks/state theo identity trong rendered tree. Type, vị trí và key ở sibling scope ảnh hưởng preservation. Stable key đại diện entity giúp note/focus thuộc đúng item sau reorder; random key gây remount; index chỉ phù hợp nếu positions thực là identity không đổi.

Update queue có replacements hoặc updater functions. `setN(n+1)` dùng n của snapshot caller; ba calls enqueue cùng replacement. `setN(v=>v+1)` enqueue transformation trên queued previous state. Updater phải pure, có thể được kiểm/chạy lại trong development. Batching nhóm work theo framework/event rules, không hứa mọi async event là một batch.

## 6. Data representation

Props là input read-only theo contract. State stored React giữ values/references; mutate object cũ làm nhiều snapshots cùng thấy thay đổi và phá comparison assumptions. Copy changed branch tạo identity mới; nested alias vẫn phải có ownership.

Ref object tồn tại qua renders, `ref.current` mutable mà không trigger render; dùng DOM handle/timer/generation, không thay state hiển thị. Context truyền value theo provider tree; consumers update theo context value semantics, không biến value thành global synchronized memory. Memo/useMemo/useCallback giữ computation/function theo dependencies cho performance, không correctness guarantee.

## 7. Control flow

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

## 8. Lifetime / ownership / state

Effect setup owns đúng subscription của lần đó. Khi dependencies đổi, cleanup cũ trước setup mới; khi unmount, cleanup final. Dev StrictMode có extra setup/cleanup để phát hiện protocol không reversible. Cleanup invalidate request generation; abort tùy support, guard apply vẫn cần cho late success/error.

Controlled input: state owns current value, onChange cập nhật; uncontrolled: DOM owns value qua defaultValue/ref theo design. Không chuyển giữa undefined và string trong cùng lifecycle. Khi owner thay entity và muốn reset form, thiết kế key/reset explicit thay copy mọi props vào state.

## 9. Invariants

Render/updaters pure; snapshots không mutate; entity identity ổn định; external setup có cleanup và late result mất quyền apply. Memo có thể bị bỏ/recompute nên logic vẫn đúng nếu không memo. Context không được dùng để bypass authorization server. Source of truth cho field form/derived state phải một nơi rõ.

### Tính update queue bằng tay

Trong một handler thuộc render có n=0, ba lệnh setN(n+1) đều tính argument là 1 từ cùng snapshot. Queue chứa ba yêu cầu replace bằng 1; render kế tiếp có n=1. Ba lệnh setN(v=>v+1) chứa ba transformations; lần lượt 0→1→2→3. Trộn replace và updater phải giữ đúng thứ tự: replace 5, increment, replace 9 cho kết quả 9. Updater phải pure vì React có thể gọi lại trong quá trình kiểm tra/retry.

Render tạo element descriptions; reconciliation nối descriptions với identity state; commit mới áp thay đổi đã chọn. Một render bị bỏ không được tạo network side effect mà application coi đã xảy ra. Event handler thực hiện action từ user intent; effect đồng bộ với hệ thống ngoài sau commit theo lifecycle thích hợp.

### Key là một phần identity trong quan hệ siblings

**Mô hình dự đoán**: list [A,B] có input local state; dùng index làm key rồi insert X ở đầu. Identity position 0 có thể tiếp tục giữ state trước của A nhưng nay render X. Dữ liệu list đúng, local state gắn sai entity. Entity ID ổn định trong siblings giúp reconciliation giữ state theo đúng entity; đổi key có chủ ý sẽ reset subtree. Key không được truyền như ordinary prop và không phải global ID cho cả app.

## 10. Ví dụ tối thiểu

**Fixture đã chạy, phạm vi hẹp:** [React race regression/fix](../examples/react-race/README.md) render component bằng React DOM trong jsdom. Cùng một test hoàn tất B rồi A: bản lỗi hiển thị A và FAIL assertion cần B; bản sửa dùng cờ stale trong effect cleanup giữ B và PASS. [Evidence](../evidence/react-race/summary.json) chứa lệnh, phiên bản và raw logs. Counter và identity fragments dưới đây vẫn chưa chạy; fixture race không xác minh các fragments đó.

Fragment React19 trong component, **chưa chạy framework fixture**:

```jsx
function Counter() {
  const [n, setN] = useState(0);
  function addThree() {
    setN(v => v + 1);
    setN(v => v + 1);
    setN(v => v + 1);
  }
  return <button onClick={addThree}>{n}</button>;
}
```

Dự đoán mỗi click tăng 3; thay ba updater bằng `setN(n+1)` tạo +1 trong cùng handler snapshot.

Identity ví dụ: Rows A/B/C key 0/1/2 có note local. Bỏ A giữ instance key0 cho B, nên note A có thể theo B. Key ID ổn định sửa mapping state/entity; không đòi force remount toàn list.

## 11. Failure modes

Stale closure đọc render cũ; stale response hết owner apply; dependency thiếu giữ resource room cũ; effect loop vì dependency identity mới mỗi update; shared mutation làm old snapshot đổi; random keys mất focus; derived duplicate state lệch. Mỗi lỗi có invariant khác; useCallback không tự cho latest closure, functional update không tự cancel request.

### Một effect cần giữ protocol setup/cleanup

Effect subscribe source S: commit S → setup subscribe S; dependency đổi T → cleanup subscription S → setup T; unmount → cleanup T. Handler callback có closure của render tạo nó. Cleanup phải tháo chính listener/subscription đã đăng ký; mutable global “current listener” có thể tháo nhầm.

Với async response, cleanup có thể signal cancellation nhưng một callback đã tới vẫn cần kiểm owner/generation trước apply. Ref giữ mutable cell qua renders nhưng đổi ref.current không yêu cầu rerender; state dành cho thông tin phải hiện trên UI. Memo tối ưu work có thể được tính lại/bỏ cache; correctness phải đúng khi không có memo.

## 12. Debug / observability

React DevTools quan sát props/state/component identity; Profiler quan sát commits/render work theo fixture; browser Performance cho JS/layout/paint và Network cho request order. Discriminating test cố định raw items rồi reorder để phân biệt key bug với API data sai. Log setup/cleanup IDs để xem resource leak; đừng coi số render trong dev là số business actions.

## 13. Liên hệ với bug/lab hiện có

[FE-01](../labs/frontend/FE-01.md) snapshot; [FE-02](../labs/frontend/FE-02.md) dependency; [FE-04](../labs/frontend/FE-04.md) cleanup; [FE-05](../labs/frontend/FE-05.md) request owner; [FE-08](../labs/frontend/FE-08.md) input owner; [FE-09](../labs/frontend/FE-09.md) identity; [FE-10](../labs/frontend/FE-10.md) immutable state; [FE-11](../labs/frontend/FE-11.md) derived state.

## 14. Sai lầm thường gặp

Effect không là nơi đặt mọi logic; event intent thuộc handler, pure derivation thuộc render. Ref không là state nhanh hơn. Memo không sửa mutation/dependency/owner lỗi. Disable StrictMode không giữ setup/cleanup invariant. Key chỉ unique trong sibling scope phù hợp, không phải global ID bắt buộc.

## 15. Câu hỏi tự kiểm tra

1. Setter đổi n của handler đang chạy không? Đáp án: không.
2. Render không commit có được POST không? Đáp án: không, side effect sẽ không theo committed lifecycle.
3. Context value object mới ảnh hưởng gì? Đáp án: consumer update, cần đo trước memo.
4. useMemo giữ resource acquisition luôn một lần không? Đáp án: không.
5. Cleanup abort có đủ chống stale state? Đáp án: thêm ownership guard.
6. Input initial undefined rồi string có owner thế nào? Đáp án: chuyển mode ngoài contract.
7. Derived subtotal nên ở đâu? Đáp án: tính từ nguồn hiện hành, trừ khi state có semantics độc lập.

## 16. Nguồn

[React versions](https://react.dev/versions), [render/commit](https://react.dev/learn/render-and-commit), [snapshot](https://react.dev/learn/state-as-a-snapshot), [queue updates](https://react.dev/learn/queueing-a-series-of-state-updates), [identity](https://react.dev/learn/preserving-and-resetting-state), [effects](https://react.dev/learn/synchronizing-with-effects), [context](https://react.dev/learn/passing-data-deeply-with-context), [useMemo](https://react.dev/reference/react/useMemo). Docs hiện hành, bài giới hạn contracts React19 nêu trên.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
