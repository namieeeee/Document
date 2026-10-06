# Đối chiếu tài liệu nội bộ

## Phase theory-first — 2026-10-06

- Decode LE16 trong digital foundation cast sang uint32_t **trước** shift; uint8_t có thể promote sang signed int16, nên cast kết quả sau shift không sửa overflow/UB. Example yêu cầu exact-width types tồn tại và buffer length/lifetime hợp lệ.
- Raw struct không portable wire format: padding/alignment/endian và representation cần explicit encoding. Volatile không giữ atomicity/publication/owner giữa CPU/ISR/DMA.
- FreeRTOS11.1 timer callback chạy trong service task; Zephyr3.7 k_timer expiry callback chạy clock ISR. Không dùng một mô tả callback chung cho hai kernel.
- CMSIS6/Zephyr3.7 sources được pin thay latest; C17 dùng nền N1570 C11 draft với nhãn giới hạn, C++17 N4659 không đồng nhất rolling draft.
- Corrections nội bộ trước về pointer.c/%s width, INT_MIN/-1, STL vector size/capacity/invalidation và performance/WCET vẫn giữ. Standard/vendor sources ưu tiên trên ZIP; [source ledger](THEORY_SOURCE_VERIFICATION.md) ghi nguồn thay đường lỗi.

Giữ ZIP gốc. Đây là correction/nuance dùng trong giáo trình, không phải chứng nhận audit toàn bộ code hay chuẩn safety. Nguồn `documents.zip` chủ yếu C/C++ embedded; không dùng nó làm bằng chứng framework web hiện hành.

| Vị trí trong ZIP | Vấn đề có thể dẫn tới lỗi | Cách dạy đúng |
|---|---|---|
| `Base_C/CD1_c_core/pointer.c`, `bai_3` | `%s` không width cho `op_name[10]` | Giới hạn9 ký tự + null hoặc đọc line/parse có bounds; kiểm input quá dài. Width chưa giải quyết mọi parse/overflow case. |
| Cùng file, `div_op` | Trả0 khi chia0 che lỗi; `INT_MIN / -1` vẫn có thể overflow | Status riêng và kiểm operand range trước division; arithmetic khác cũng cần overflow policy. [CERT](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/) |
| Cùng file, `find_minmax` | n<=0 trả nhưng không báo output invalid; pointer contract thiếu | Bool/status, output chỉ hợp lệ khi success; caller bảo đảm buffer length. Hàm mẫu ở chương 05. |
| `Base_CPP/CD2/vector.cpp`, comment đầu | Vector có `length()`; push_back luônO(1) | Dùng size(); push_back amortized, realloc có cost/invalidations. [Vector draft](https://eel.is/c++draft/vector.capacity) |
| `documents/C_CPP_BASIC/phan2_cpp_essentials.md` và tổng hợp | Virtual destructor được mô tả như bắt buộc mọi trường hợp | Cần khi delete derived qua base theo cách dùng; không tự thêm virtual cho mọi class. Xem lifetime/ownership ở chương 05. |
| `documents/C_CPP_EMB_AUTOSAR/04_Functions_Passing_Variables/material.md`, Pattern1 | Flag volatile không bảo vệ rxBuf khi ISR tiếp tục ghi; index thiếu bounds | Ownership buffer, bounds và completion protocol; coalescing chỉ dùng khi mục tiêu cho phép. |
| Cùng material, Pattern3 | ISR ++s_qCount và task --s_qCount là RMW cạnh tranh dù volatile | Atomic/critical section đúng port hoặc SPSC thiết kế đúng memory semantics; không coi count volatile là queue an toàn. [GCC](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html) |
| Cùng material, `Abs_s32` | `-x` với INT32_MIN không representable | Kiểm boundary, trả status/unsigned magnitude theo contract; inline không tự sửa overflow. |
| Cùng material, critical section | Enable IRQ vô điều kiện có thể phá trạng thái mask trước đó | Save/restore mask đúng port; không block; nguồn đã có cảnh báo nhưng ví dụ cần dùng nhất quán. |
| Cùng material, `XorChecksum`/PARSE_STATUS_CRC | XOR checksum được đặt tên/status CRC | Gọi checksum XOR đúng nghĩa hoặc triển khai CRC định nghĩa đầy đủ; XOR không thay CRC polynomial. |
| `documents/C_CPP_EMB_AUTOSAR/05_File_IO_Debugging/material.md` | Mọi binary artifact “phải” magic/version/CRC | Chọn format/integrity theo use case; CRC không auth và không mọi file cần cùng header. |
| `documents/QB_Audit_1-5.xlsx` | Rubric có CRC-16/CCITT nhưng thiếu variant/coverage; offset bit field dễ bị hiểu nhầm | Ghi poly/init/reflection/xorout/endian/coverage/test vector; không dùng offsetof trên bit field như member addressable bình thường. |
| Cùng workbook, magic `0x46554C54` | Comment “FAULT” không tương ứng bốn byte magic | Định nghĩa byte sequence và endian; năm ký tự không nằm đủ trong giá trị bốn byte. |
| Cùng workbook, CH5-H-20, app end+read | Cập nhật header trong app end mode có thể ghi vào cuối; chuyển đọc/ghi thiếu sequencing | Dùng mode/positioning phù hợp format, kiểm fflush/fseek và lỗi theo contract stream; không giả a+b cho phép sửa header tùy ý. |
| Tổng hợp `tonghop.md`/`tonghop.pdf` | reserve/fixed container được liên hệ deterministic quá mạnh | Capacity bound không tự chứng minh WCET; overflow policy, allocator/call path và hardware measurement vẫn cần. |
| Tổng hợp, temp-file+rename | Có thể bị hiểu như power-loss guarantee hoàn chỉnh | Xét fsync file/directory và storage/filesystem. [fsync](https://man7.org/linux/man-pages/man2/fsync.2.html) |
| Tổng hợp, hot/cold split | Tốc độ10–20 x không có benchmark đủ điều kiện | Không mang con số thành cam kết; đo cùng input/build/hardware và cache/memory behavior. |
| Nội dung nhắc MISRA/AUTOSAR | Gợi ý review có thể bị đọc thành compliance | Không bịa số rule hay tuyên bố compliant; cần version, scope và tài liệu chuẩn truy cập được. |

Không sửa mọi ví dụ nguồn vì mục tiêu hiện tại là xây giáo trình riêng. Compiler C/C++ chưa có nên các lỗi arithmetic/bounds trên được review tĩnh; chưa tuyên bố đã chạy sanitizer. Các điểm đúng đã giữ: context callback, tách ISR khỏi parse, input/output contract, deferred processing và chú ý stack.

[Nguồn](REFERENCES.md) · [Chương05](05_EMBEDDED_C_CPP_FOUNDATION.md) · [Chương06](06_MCU_FIRMWARE_RTOS.md).
