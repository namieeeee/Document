# C++ embedded: objects, RAII và chi phí

Phạm vi: C++17 freestanding/embedded constraints; không áp destroying-delete/newer draft features vào C++17. Host facilities không mặc định available MCU.

## 1. Mục tiêu học

Thiết kế object invariant/owner, phân tích copy/move/virtual/template/container costs và cleanup qua asynchronous work.

## 2. Kiến thức tiên quyết

[C](01_C_REPRESENTATION.md), [memory](02_MEMORY_BUILD.md), [build](11_BUILD_LINK_STARTUP.md).

## 3. Vấn đề mà cơ chế này giải quyết

Raw resources có cleanup/error paths phức tạp; C++ gắn cleanup với lifetime, nhưng abstraction vẫn cần memory/timing/ABI budget target.

## 4. Khái niệm

Constructor thiết lập invariant object; destructor kết thúc ownership/resource khi lifetime kết thúc theo semantics. Base/member construction order theo khai báo/class rules, không tùy thứ tự bạn viết initializer list. RAII gắn resource với object owner: lock/file/buffer có cleanup tại scope exit/exception paths, không nhất thiết heap allocation. Reference là alias tới object, không owning handle mặc định; reference/pointer còn tên không giữ borrowed object sống. [Lifetime draft](https://eel.is/c++draft/basic.life).

Copy object owner có thể nhân bản resource hoặc phải bị cấm; raw pointer copy chỉ copy địa chỉ. Move chuyển ownership theo implementation và để source trạng thái valid theo contract type. Không gọi object moved from như còn payload cũ mà không biết guarantee. Smart pointer diễn tả ownership nhưng shared reference count có overhead/lifetime nondeterminism của release actor; không dùng sharedptr mọi chỗ để chữa design ownership.

## 5. Thành phần bên trong

Virtual dispatch cho caller dùng interface chọn implementation runtime, thường có indirect call/object metadata theo ABI; cost phụ thuộc target/compiler/devirtualization. Conventional delete derived qua base cần virtual destructor theo rules; class không dùng kiểu delete đó có design khác, không mọi class đều phải virtual. [Delete draft](https://eel.is/c++draft/expr.delete).

Template tạo code theo types ở compile time; có thể tránh runtime dispatch nhưng code-size instantiations tăng. Definition thường phải visible khi instantiate, explicit instantiation/modules là nuance, không khẳng định tuyệt đối “template chỉ header”. STL algorithms/containers chọn theo allocation/iterator invalidations/bounds và library available. Vector capacity không fixed maximum; push_back có realloc/amortized cost. Reference tới element có thể invalid saurealloc. [Vector capacity draft](https://eel.is/c++draft/vector.capacity).

Allocator là policy cấp/release storage cho containers; resource construction/lifetime khác allocate bytes. Pool/bounded container cần capacity/full/error contract. Deallocation và destructor có thể ở actor cuối release shared ownership; không mặc định deterministic timing theo owner đầu.

## 6. Data representation

Class object chứa subobjects/base/members/padding; virtual metadata theo ABI, không standard fixed layout. Reference là alias không own; unique owner move-only ngăn copy resource; shared_ptr reference counting có overhead và cycle retention nếu strong graph cycle. std::array inline fixed extent, vector owns variable storage; iterator/reference invalidation theo operations.

## 7. Control flow

Construction base→members theo declaration order→constructor body; failure cleanup đã constructed subobjects theo rules. Scope ends→destructor body/members/bases reverse order. Copy creates distinct object theo copy operations; move chooses move overload, có thể fallback copy tùy type. Templates instantiated theo types, compile-time dispatch trade code size; explicit instantiation hỗ trợ definitions tổ chức khác header-only.

## 8. Lifetime / ownership / state

DMA pending không kết thúc chỉ vì RAII wrapper function scope kết thúc. Buffer owner phải sống tới engine completion/quiescence; async callback borrowed span không lưu vượt guarantee. Moved-from object valid theo type contract nhưng payload không assumed same; std::move là cast cho overload resolution, không tự transfer bytes.

## 9. Invariants

Owner release đúng một lần, views không vượt lifetime/reallocation; constructor establishes valid state; copy/move/destructor giữ resource semantics. Worst-path code/allocation/locks có budget, exception/RTTI ABI flags khớp libraries.

## 10. Ví dụ tối thiểu

Fragment C++17 **chưa compile**:

```cpp
struct BufferOwner {
    BufferOwner(const BufferOwner&) = delete;
    BufferOwner& operator=(const BufferOwner&) = delete;
    // Constructor/move/destructor cần resource contract cụ thể.
};
```

Đây là interface sketch, không usable complete buffer class. Vector reserve4 rồi append5 có thể realloc; reference element cũ invalid. Capacity bound không fixed maximum, phải enforce full policy.

### Ví dụ move-only RAII có ownership thật

Fragment C++17, **chưa compile** trong môi trường này. Lease sở hữu một token đã acquire từ pool; callback release là hàm noexcept đã tồn tại suốt lifetime lease. Token −1 nghĩa empty. Pool và storage vẫn phải sống lâu hơn mọi lease; ví dụ không tự đồng bộ ISR/DMA hoặc giải phóng token khi device còn dùng.

```cpp
#include <utility>

class Lease {
    using Release = void (*)(int) noexcept;
    int token_ = -1;
    Release release_ = nullptr;

public:
    Lease() = default;
    // Contract: token >= 0; release != nullptr.
    Lease(int token, Release release) noexcept
        : token_(token), release_(release) {}
    Lease(const Lease&) = delete;
    Lease& operator=(const Lease&) = delete;

    Lease(Lease&& other) noexcept
        : token_(std::exchange(other.token_, -1)),
          release_(std::exchange(other.release_, nullptr)) {}

    Lease& operator=(Lease&& other) noexcept {
        if (this != &other) {
            reset();
            token_ = std::exchange(other.token_, -1);
            release_ = std::exchange(other.release_, nullptr);
        }
        return *this;
    }

    ~Lease() { reset(); }
    void reset() noexcept {
        if (token_ >= 0) release_(token_);
        token_ = -1;
        release_ = nullptr;
    }
};
```

**Mô hình dự đoán**: a giữ token3, b giữ token4. Move-assign b=std::move(a) trả token4 rồi b giữ3; a empty. Scope kết thúc chỉ b trả3. Copy bị cấm vì hai destructors không được cùng trả một token. Self move được guard; release phải bounded, không reenter cùng lease và không throw.

RAII giữ cleanup trên return/exception unwind theo language, không chạy destructor sau mọi fatal reset/power loss. Nếu exceptions bị tắt trong embedded build, error-code paths vẫn cần owner release. Khi chuyển lease vào work async/DMA, destructor chỉ được chạy sau completion/quiescence; move semantics không biết hardware đã xong.

### Chọn abstraction theo cost và invariant

Virtual dispatch cần object lifetime và dynamic type đúng; cost còn phụ thuộc layout/codegen/cache, không có số cycles chung. Templates có thể specialize bỏ runtime branches nhưng nhân code size. STL containers có allocation/invalidation/complexity contract; reserve không là capacity limit. Custom allocator giúp placement/allocation policy, không sửa dangling views hoặc synchronization. Đo image/map/stack và worst paths trên build thực trước quyết định bỏ hay giữ abstraction.

## 11. Failure modes

Double-free shallow copied owner, dangling reference sau realloc, asynchronous destructor sớm, strong cycles, exception disabled nhưng library expects unwind, template bloat/stack alloc lớn. Fix owner/protocol/capacity/build flags thay reserve khổng lồ.

## 12. Debug / observability

- **SYMPTOM:** pointer/reference tới vector element đọc sai sau app end hoặc pool buffer release hai lần.
- **EVIDENCE:** owner/copy/move/destructor timeline, old/new buffer address/capacity, allocation counter, host sanitizer nếu có.
- **POSSIBLE CAUSES:** realloc invalidates, wrong copy ownership, callback borrow retained hoặc delayed DMA completion.
- **DISTINGUISHING TEST:** app end qua capacity boundary; compare address; force callback buffer reuse và completion late.
- **ROOT CAUSE:** observer/reference dùng object/storage đã hết guarantee lifetime.
- **FIX:** stable ownership/handles hoặc copy data; bound capacity/full policy; async release sau completion.
- **WRONG FIX:** reserve rất lớn rồi coi không thể realloc, leak resource để tránh UAF, sharedptr bọc raw buffer nhưng không giữ DMA protocol.
- **REGRESSION TEST:** capacity boundary, copy/move/error cleanup, late completion và double-release failure path.

## 13. Liên hệ với bug/lab hiện có

[EMB-11](../labs/embedded_rtos/EMB-11.md), [EMB-30](../labs/embedded_rtos/EMB-30.md), [OS-06](../labs/os/OS-06.md); Base_CPP vector correction size/amortized ở [CORRECTIONS](../CORRECTIONS.md).

## 14. Sai lầm thường gặp

Exceptions/error status đều cần failure contract. Exception support có metadata/unwinding và toolchain constraints; disable exception mà giữ code/library phụ thuộc nó có thể tạo behavior khác. RTTI/runtime query có costs; compile flags và libraryABI phải khớp. Không hứa “no exceptions” tự làm deterministic: allocation, locks, I/O và unbounded algorithm vẫn phá deadline.

## 15. Câu hỏi tự kiểm tra

1. RAII bắt buộc heap? Đáp án: không.
2. Reference giữ owner sống? Đáp án: không.
3. Std::move tự transfer? Đáp án: cast chọn operations.
4. Reserve cấm grow? Đáp án: không.
5. Template giảm runtime đổi cost gì? Đáp án: instantiation/code size.
6. Delete derived qua base C++17? Đáp án: conventional polymorphic deletion cần virtual destructor.

## 16. Nguồn

[C++ Core Guidelines resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii), [public C++17 draft N4659](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf), [current lifetime draft](https://eel.is/c++draft/basic.life), [vector draft](https://eel.is/c++draft/vector.capacity). Current drafts chỉ đối chiếu core behavior giữ C++17, không blanket current standard.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
