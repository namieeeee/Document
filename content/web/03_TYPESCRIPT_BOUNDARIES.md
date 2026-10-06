# Outline — TypeScript: mô hình tĩnh và runtime boundary

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Assertion che null tạo TypeError; any propagation bỏ kiểm; fake predicate narrow sai; declaration/runtime mismatch; intersection contradictory field; JSON string 'false' dùng như boolean; strictNullChecks tắt làm compiler nhận null sai expectation. Root fix là contract/parser/options/declaration phù hợp, không `as unknown as` mọi chỗ.

Đặt câu hỏi: cơ chế trong [TypeScript: mô hình tĩnh và runtime boundary](../../web/03_TYPESCRIPT_BOUNDARIES.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

```text
Source + declarations + compiler options
→ inference/assignability/control-flow checking
→ diagnostics hoặc emitted JS theo config
→ runtime JS + external values
```

Emit policy có thể vẫn tạo JS khi diagnostics nếu config cho phép; build pipeline phải định nghĩa fail criteria. Luồng data đúng: bytes→JSON.parse→unknown→shape parser→semantic/domain checks→DTO→UI. Generic `fetchJson<T>` dùng `json as T` không có parser chỉ đổi compiler belief.

## 3. Demo chạy thật

Claim có phạm vi: Không access raw external data trước guard; parser trả object normalized/whitelisted theo contract hoặc explicit error. Compile strict và runtime checks là hai lớp. Discriminated union states phải exhaustive và impossible transition được xử lý; invalid data không được silently cast thành valid state. Type assertion không bằng authorization hoặc domain validation.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../web/03_TYPESCRIPT_BOUNDARIES.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Assertion che null tạo TypeError; any propagation bỏ kiểm; fake predicate narrow sai; declaration/runtime mismatch; intersection contradictory field; JSON string 'false' dùng như boolean; strictNullChecks tắt làm compiler nhận null sai expectation. Root fix là contract/parser/options/declaration phù hợp, không `as unknown as` mọi chỗ.

Xem raw JSON/typeof trước mapper; chạy parser riêng với null/missing/wrong enum/type, ghi branch/error. Compiler diagnostics và resolved declaration location phân biệt type issue với network issue. JS emitted cho thấy annotations không còn. Breakpoint trước publish state xác định data validated và request owner; strict compilation không chứng minh latest response.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[TS everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html), [narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [generics](https://www.typescriptlang.org/docs/handbook/2/generics.html), [compatibility](https://www.typescriptlang.org/docs/handbook/type-compatibility.html), [declaration files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html). Handbook là docs rolling; ví dụ giới hạn TS5.x, runtime framework không được tự nâng.

1. Interface Task gửi tới browser có code validation không? Đáp án: không.
2. A&B có tạo merged object không? Đáp án: không.
3. Any khác unknown ở property access thế nào? Đáp án: unknown cần narrow, any bỏ check.
4. Type guard viết sai có compile không? Đáp án: có thể, thân guard cần regression.
5. Dữ liệu shape đúng có role/price đúng không? Đáp án: chưa, cần semantic/business/auth.
6. Declaration có bảo đảm module tồn tại? Đáp án: không.

[Index](../../00_INDEX.md) · [Content](../README.md).
