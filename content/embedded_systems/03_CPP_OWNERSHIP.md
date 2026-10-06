# Outline — C++ embedded: objects, RAII và chi phí

Mức của claim minh họa: **UNVERIFIED**. Không phải mức chứng nhận toàn bài.

## 1. Hook

Double-free shallow copied owner, dangling reference sau realloc, asynchronous destructor sớm, strong cycles, exception disabled nhưng library expects unwind, template bloat/stack alloc lớn. Fix owner/protocol/capacity/build flags thay reserve khổng lồ.

Đặt câu hỏi: cơ chế trong [C++ embedded: objects, RAII và chi phí](../../embedded_systems/03_CPP_OWNERSHIP.md) giải thích failure này bằng invariant nào?

## 2. Mô hình trong 60 giây

```text
representation -> actor/control flow -> ownership/lifetime -> invariant -> evidence
```

Construction base→members theo declaration order→constructor body; failure cleanup đã constructed subobjects theo rules. Scope ends→destructor body/members/bases reverse order. Copy creates distinct object theo copy operations; move chooses move overload, có thể fallback copy tùy type. Templates instantiated theo types, compile-time dispatch trade code size; explicit instantiation hỗ trợ definitions tổ chức khác header-only.

## 3. Demo chạy thật

Claim có phạm vi: Owner release đúng một lần, views không vượt lifetime/reallocation; constructor establishes valid state; copy/move/destructor giữ resource semantics. Worst-path code/allocation/locks có budget, exception/RTTI ABI flags khớp libraries.

**BLOCKED — chưa có demo thực thi riêng cho claim này.** Không có output để trích; không dùng kết quả của bài khác thay thế. Chưa sẵn sàng xuất bản phần demo. Xem [bài nguồn](../../embedded_systems/03_CPP_OWNERSHIP.md) và [matrix](../../THEORY_COVERAGE_MATRIX.md).

## 4. Cách nó hỏng và cách phát hiện

Double-free shallow copied owner, dangling reference sau realloc, asynchronous destructor sớm, strong cycles, exception disabled nhưng library expects unwind, template bloat/stack alloc lớn. Fix owner/protocol/capacity/build flags thay reserve khổng lồ.

- **SYMPTOM:** pointer/reference tới vector element đọc sai sau app end hoặc pool buffer release hai lần.
- **EVIDENCE:** owner/copy/move/destructor timeline, old/new buffer address/capacity, allocation counter, host sanitizer nếu có.
- **POSSIBLE CAUSES:** realloc invalidates, wrong copy ownership, callback borrow retained hoặc delayed DMA completion.
- **DISTINGUISHING TEST:** app end qua capacity boundary; compare address; force callback buffer reuse và completion late.
- **ROOT CAUSE:** observer/reference dùng object/storage đã hết guarantee lifetime.
- **FIX:** stable ownership/handles hoặc copy data; bound capacity/full policy; async release sau completion.
- **WRONG FIX:** reserve rất lớn rồi coi không thể realloc, leak resource để tránh UAF, sharedptr bọc raw buffer nhưng không giữ DMA protocol.
- **REGRESSION TEST:** capacity boundary, copy/move/error cleanup, late completion và double-release failure path.

## 5. Giới hạn trung thực

Source/pseudocode review only; no topic-specific executable record. Demo remains BLOCKED.

Outline này trích nội dung hiện có; không bổ sung bảo đảm về target chưa đo. Chỉ công bố demo khi mức/evidence phù hợp.

## 6. Nguồn và câu hỏi tự kiểm tra

[C++ Core Guidelines resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii), [public C++17 draft N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [current lifetime draft](https://eel.is/c++draft/basic.life), [vector draft](https://eel.is/c++draft/vector.capacity). Current drafts chỉ đối chiếu core behavior giữ C++17, không blanket current standard.

1. RAII bắt buộc heap? Đáp án: không.
2. Reference giữ owner sống? Đáp án: không.
3. Std::move tự transfer? Đáp án: cast chọn operations.
4. Reserve cấm grow? Đáp án: không.
5. Template giảm runtime đổi cost gì? Đáp án: instantiation/code size.
6. Delete derived qua base C++17? Đáp án: conventional polymorphic deletion cần virtual destructor.

[Index](../../00_INDEX.md) · [Content](../README.md).
