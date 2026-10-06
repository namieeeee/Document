# TypeScript: mô hình tĩnh và runtime boundary

Phạm vi: TypeScript 5.x với `strict`/`strictNullChecks`; snippets không dùng feature phụ thuộc minor mới. Type erasure không có nghĩa mọi syntax TS đều không sinh JS, ví dụ enums có runtime output.

## 1. Mục tiêu học

Đọc type như tập khả năng và quan hệ input/output, giải thích assignability/narrowing và viết parser từ unknown. Phân biệt static guarantee nội bộ với runtime validation tại network boundary.

## 2. Kiến thức tiên quyết

[JS language](../foundations/02_JAVASCRIPT_LANGUAGE.md), object identity, modules và exception. TS kiểm JS source; không thay runtime execution model.

## 3. Vấn đề mà cơ chế này giải quyết

JS linh hoạt nhưng một property access sai có thể chỉ lộ khi chạy. Static type system phát hiện nhiều lỗi trước execution và giữ quan hệ qua refactor. Nó không nhìn network bytes tương lai hay tự chứng minh business invariant; runtime checks phải tạo cầu nối từ dữ liệu ngoài tới trusted model.

## 4. Khái niệm

Type mô tả giá trị/compiler operations được phép; runtime value là dữ liệu thật. Assignability kiểm một expression có thể dùng nơi đòi type nào. Structural typing dựa members phù hợp, không chỉ tên class/interface; TS có pragmatic unsound allowances nên không là mathematical proof toàn chương trình.

Inference suy từ initializer/context; widening có thể biến literal thành string/number. `const` binding và `as const` literal inference khác nhau; readonly là compile-time restriction qua type path, không deep runtime freeze.

## 5. Thành phần bên trong

Union `A|B` cho một trong các khả năng, nên access phải hợp mọi member hoặc narrow. Intersection `A&B` đòi thỏa cả hai constraints, không tự merge objects runtime; incompatible members có thể tạo type không inhabitable. Generic giữ relation: `T[]→T|undefined`, constraint `T extends {id:string}` chỉ giới hạn khả năng.

Narrowing theo typeof, null check, instanceof, discriminant và control flow giảm set khả năng trong branch. User-defined type predicate là lời hứa của function; compiler không chứng minh thân guard đúng. Null/undefined có ý nghĩa riêng dưới strictNullChecks.

## 6. Data representation

| Type facility | Compiler meaning | Runtime artifact |
|---|---|---|
| interface/type alias | Shape/relation | Bị xóa |
| `as T`/`!` | Developer assertion | Không validate/convert |
| unknown | Chưa biết, phải narrow trước dùng | Value vẫn nguyên |
| any | Bỏ nhiều checks, có thể lan | Value vẫn nguyên |
| never | Không có value hợp lệ / path không return | Không tự runtime throw |
| `.d.ts` | Mô tả external module/global APIs | Không cung cấp implementation |

Module resolution/type declarations cần khớp runtime import graph. Declaration khai báo function tồn tại không tạo function; compile xanh nhưng module file/version sai vẫn crash.

## 7. Control flow

```text
Source + declarations + compiler options
→ inference/assignability/control-flow checking
→ diagnostics hoặc emitted JS theo config
→ runtime JS + external values
```

Emit policy có thể vẫn tạo JS khi diagnostics nếu config cho phép; build pipeline phải định nghĩa fail criteria. Luồng data đúng: bytes→JSON.parse→unknown→shape parser→semantic/domain checks→DTO→UI. Generic `fetchJson<T>` dùng `json as T` không có parser chỉ đổi compiler belief.

## 8. Lifetime / ownership / state

Type information không kéo dài object lifetime và không synchronize asynchronous owners. Readonly reference có thể nhìn object được mutate qua alias khác. Control-flow narrowing có assumptions về code paths; callback/await có thể mở boundary thay state, nên snapshot local hoặc validate lại dữ liệu shared theo design. External module version phải cùng declaration version, không giữ stale types cho mới runtime.

## 9. Invariants

Không access raw external data trước guard; parser trả object normalized/whitelisted theo contract hoặc explicit error. Compile strict và runtime checks là hai lớp. Discriminated union states phải exhaustive và impossible transition được xử lý; invalid data không được silently cast thành valid state. Type assertion không bằng authorization hoặc domain validation.

## 10. Ví dụ tối thiểu

Fragment TS 5.x:

```ts
type Result = { kind: 'ok'; title: string } | { kind: 'error'; code: string };
function assertNever(x: never): never { throw Error('unexpected state'); }
function label(r: Result): string {
  switch (r.kind) {
    case 'ok': return r.title;
    case 'error': return r.code;
    default: return assertNever(r);
  }
}
function parseTask(raw: unknown): { title: string; done: boolean } {
  if (raw === null || typeof raw !== 'object' ||
      !('title' in raw) || typeof raw.title !== 'string' ||
      !('done' in raw) || typeof raw.done !== 'boolean') throw Error('shape');
  return { title: raw.title, done: raw.done };
}
```

Shape parser không giữ title length/business rules. Exhaustiveness giúp compiler khi Result union mở rộng; default throw còn hữu ích khi external invalid value vượt static assumptions.

## 11. Failure modes

Assertion che null tạo TypeError; any propagation bỏ kiểm; fake predicate narrow sai; declaration/runtime mismatch; intersection contradictory field; JSON string 'false' dùng như boolean; strictNullChecks tắt làm compiler nhận null sai expectation. Root fix là contract/parser/options/declaration phù hợp, không `as unknown as` mọi chỗ.

## 12. Debug / observability

Xem raw JSON/typeof trước mapper; chạy parser riêng với null/missing/wrong enum/type, ghi branch/error. Compiler diagnostics và resolved declaration location phân biệt type issue với network issue. JS emitted cho thấy annotations không còn. Breakpoint trước publish state xác định data validated và request owner; strict compilation không chứng minh latest response.

## 13. Liên hệ với bug/lab hiện có

[FE-25](../labs/frontend/FE-25.md) giữ runtime shape invariant; [INT-03](../labs/integration/INT-03.md), [INT-04](../labs/integration/INT-04.md), [INT-05](../labs/integration/INT-05.md) giữ null/type/enum meaning. Contract error tách empty data, không sửa source lab.

## 14. Sai lầm thường gặp

Structural compatibility không phải whitelist. `never` không tự kiểm exhaustiveness nếu chưa dùng tại impossible branch. `unknown` không bắt bạn validate nếu ngay sau đó cast bỏ check. Generic không tạo schema, `.d.ts` không là code chạy, TS nullable không giống validation JSON nullable của server.

## 15. Câu hỏi tự kiểm tra

1. Interface Task gửi tới browser có code validation không? Đáp án: không.
2. A&B có tạo merged object không? Đáp án: không.
3. Any khác unknown ở property access thế nào? Đáp án: unknown cần narrow, any bỏ check.
4. Type guard viết sai có compile không? Đáp án: có thể, thân guard cần regression.
5. Dữ liệu shape đúng có role/price đúng không? Đáp án: chưa, cần semantic/business/auth.
6. Declaration có bảo đảm module tồn tại? Đáp án: không.

## 16. Nguồn

[TS everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html), [narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [generics](https://www.typescriptlang.org/docs/handbook/2/generics.html), [compatibility](https://www.typescriptlang.org/docs/handbook/type-compatibility.html), [declaration files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html). Handbook là docs rolling; ví dụ giới hạn TS5.x, runtime framework không được tự nâng.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
