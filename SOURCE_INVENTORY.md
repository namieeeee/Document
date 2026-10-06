# Inventory nguồn nội bộ

## Phase theory-first — 2026-10-06

Inventory baseline của curriculum:167 Markdown+bốn code/project files,661.534 ký tự text;121 lab. Lượt này đọc text md/c/cpp/h/txt trong ba ZIP: documents98, Base_C30, Base_CPP45. Catalog cũ bên dưới vẫn giữ247 file entries; số100 text của documents ở phase trước còn gồm PDF/XLSX, không nói lượt này đọc lại toàn PDF/workbook. Chỉ dùng code/tài liệu nội bộ làm context và corrections; không chạy EXE/DLL từ ZIP. Hash archives được kiểm lại trong [validation](VALIDATION.md).

Discovery đọc archive directory và trích xuất text, không chạy EXE, không mở dữ liệu production. Instruction nằm trong tài liệu nguồn được coi là nội dung học liệu, không lệnh có quyền đổi task.

## Tổng hợp

| Archive | File không phải directory | Text trích xuất | Vai trò |
|---|---:|---:|---|
| documents.zip | 117 | 100 | C/C++ cơ bản, 15 topic embedded/ECU, assignments, workshops, PDF tổng hợp20 trang và workbook100 câu hỏi. |
| Base_C.zip | 53 | 30 | Bài C: arithmetic, pointer, array, bitwise, control flow, struct/file. |
| Base_CPP.zip | 77 | 45 | Bài C++/STL và một bản Base_C trùng; không tính thành nguồn độc lập. |

Tổng 247 entry file; 175 text entry trích xuất; 141 nội dung text khác nhau sau chuẩn hóa. Đếm text không có nghĩa toàn bộ đã được audit semantics hoặc compile. Đã đọc sâu các tài liệu/case dùng cho corrections; các file còn lại dùng làm catalog/bài tập, không chứng nhận code đúng.

## Nối nguồn với chương và khoảng trống

- C core, pointer và workbook CH1–5 → chương 05: kiểu, bounds, qualifier, lifetime, representation/file.
- CPP/STL, topic01–15, workshops/assignments → chương 05–06 và bài ownership, tooling/debug.
- PDF tổng hợp → lộ trình và correction về capacity, timing, durability; không sao chép claim tốc độ thiếu benchmark.
- Web FE/BE/integration và OS chuyên sâu thiếu trong ZIP → bổ sung nguồn chính thức ở REFERENCES.
- Chưa có board/port/release cụ thể → cache/DMA/IRQ timing và register-specific cần kiểm tiếp trên target.

## Archive gốc và SHA-256

| Đường dẫn | SHA-256 baseline |
|---|---|
| `C:\Trann\18_Fresher_Fsoft\emb_for_c_cpp\emb_for_c_cpp\documents.zip` | `5db2ae9ed354715e91df6a545c3db1bdc9bfa284429bafa7fd9055c843d36be6` |
| `C:\Trann\18_Fresher_Fsoft\Code_base_C_or_CPP\Base_C.zip` | `4a5669022c3f19f2942283109e714b2f62a877a500931018cff9ca57d190db3d` |
| `C:\Trann\18_Fresher_Fsoft\Code_base_C_or_CPP\Base_CPP.zip` | `5e9759ef4087954783a817d3ddd2b98ffc700cb0980cd9140d10bed0c1531c1c` |

## Catalog đầy đủ

Type/byte là metadata archive; Text đánh dấu trích xuất được. PDF dùng pypdf trong thư mục discovery riêng; XLSX đọc XML cells, không chạy macro/formula. Binary/INI không được thực thi hoặc coi là nội dung giáo trình.

| Archive | Entry | Bytes | Type | Text |
|---|---|---:|---|---|
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai01_bien_kieu_du_lieu.c` | 4517 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai02_dieu_kien_vong_lap.c` | 5125 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai03_ham_va_con_tro.c` | 6454 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai04_mang_va_chuoi.c` | 7234 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai05_struct_enum.c` | 5531 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/bai06_quan_ly_bo_nho.c` | 6260 | .c | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_c/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_cpp/bai08_oop_co_ban.cpp` | 8088 | .cpp | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_cpp/bai09_stl_lambda_templates.cpp` | 9103 | .cpp | Có |
| documents.zip | `documents/C_CPP_BASIC/bai_tap_cpp/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_BASIC/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_BASIC/phan0_moi_truong.md` | 11235 | .md | Có |
| documents.zip | `documents/C_CPP_BASIC/phan1_c_core.md` | 28598 | .md | Có |
| documents.zip | `documents/C_CPP_BASIC/phan2_cpp_essentials.md` | 22347 | .md | Có |
| documents.zip | `documents/C_CPP_BASIC/phan3_dsa.md` | 23833 | .md | Có |
| documents.zip | `documents/C_CPP_BASIC/phan4_5_tools_mindset.md` | 16683 | .md | Có |
| documents.zip | `documents/C_CPP_BASIC/README.md` | 8117 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/01_Variables_Data_Types/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/01_Variables_Data_Types/example.md` | 8170 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/01_Variables_Data_Types/material.md` | 15610 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/01_Variables_Data_Types/README.md` | 2218 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/02_Memory_Layout_Compile/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/02_Memory_Layout_Compile/example.md` | 8133 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/02_Memory_Layout_Compile/material.md` | 16524 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/02_Memory_Layout_Compile/README.md` | 4107 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/03_Arrays_Pointers_Reference/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/03_Arrays_Pointers_Reference/example.md` | 10173 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/03_Arrays_Pointers_Reference/material.md` | 16186 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/03_Arrays_Pointers_Reference/README.md` | 2510 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/04_Functions_Passing_Variables/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/04_Functions_Passing_Variables/example.md` | 5785 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/04_Functions_Passing_Variables/material.md` | 14828 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/04_Functions_Passing_Variables/README.md` | 2185 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/05_File_IO_Debugging/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/05_File_IO_Debugging/example.md` | 6162 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/05_File_IO_Debugging/material.md` | 9639 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/05_File_IO_Debugging/README.md` | 2320 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/06_OOP_Basics/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/06_OOP_Basics/example.md` | 16002 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/06_OOP_Basics/material.md` | 36246 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/06_OOP_Basics/README.md` | 3189 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/07_OOP_Features/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/07_OOP_Features/example.md` | 10106 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/07_OOP_Features/material.md` | 22873 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/07_OOP_Features/README.md` | 2393 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/08_Namespace_Templates/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/08_Namespace_Templates/example.md` | 5655 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/08_Namespace_Templates/material.md` | 13331 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/08_Namespace_Templates/README.md` | 2475 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/09_Data_Structures_Algorithms/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/09_Data_Structures_Algorithms/example.md` | 15083 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/09_Data_Structures_Algorithms/material.md` | 15620 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/09_Data_Structures_Algorithms/README.md` | 2468 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/10_Unit_Test/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/10_Unit_Test/example.md` | 5581 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/10_Unit_Test/material.md` | 7223 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/10_Unit_Test/README.md` | 2235 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/11_Advanced_CPP_Features/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/11_Advanced_CPP_Features/example.md` | 22594 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/11_Advanced_CPP_Features/material.md` | 32132 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/11_Advanced_CPP_Features/README.md` | 4263 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/12_Optimization_Common_Defects/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/12_Optimization_Common_Defects/example.md` | 11968 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/12_Optimization_Common_Defects/material.md` | 21511 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/12_Optimization_Common_Defects/README.md` | 2798 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/13_Design_Patterns_Pattern_MCU_Base/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/13_Design_Patterns_Pattern_MCU_Base/example.md` | 15571 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/13_Design_Patterns_Pattern_MCU_Base/material.md` | 32504 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/13_Design_Patterns_Pattern_MCU_Base/README.md` | 3085 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/14_UML_Modeling/example.md` | 7900 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/14_UML_Modeling/material.md` | 17219 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/14_UML_Modeling/README.md` | 4033 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/15_Practical_Tooling/example.md` | 5826 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/15_Practical_Tooling/material.md` | 17934 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/15_Practical_Tooling/README.md` | 3716 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/ADVANCED_MCU_ECU_KNOWLEDGE.md` | 47249 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 01_Opt 1.md` | 4062 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 02_Opt 1.md` | 3409 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 03_Opt 1.md` | 3108 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 04_Opt 1.md` | 3882 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 05_Opt 1.md` | 2951 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 06_Opt 1.md` | 2988 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 07_Opt 1.md` | 3103 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 08_Opt 1.md` | 2950 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 09_Opt 1.md` | 3759 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 10_Opt 1.md` | 4363 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 11_Opt 1.md` | 5760 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 12_Opt 1.md` | 3496 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 13_Opt 1.md` | 3392 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 14_Opt 1.md` | 3241 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 15_Opt 1.md` | 3240 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 16_Opt 1.md` | 4336 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 17.md` | 5608 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 18.md` | 3690 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 19.md` | 3347 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 20.md` | 4169 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.Assignment 21_Remedial_CS10.md` | 11208 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/CPP.MiniProject.md` | 10038 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/desktop.ini` | 106 | .ini | Không |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/Assignments/INDEX.md` | 6215 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/CASE_STUDIES.md` | 2661 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/InterviewQuestions_CPP.md` | 21021 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/InterviewQuestions_CPP_Fundamentals_Part3.md` | 12678 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/InterviewQuestions_EmbeddedC_CPP_Part2.md` | 34471 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/InterviewQuestions_Junior_FullProgram.md` | 28508 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/README.md` | 12731 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/SETUP_CPP_VSCODE.md` | 16289 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/tonghop.md` | 7590 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/tonghop.pdf` | 228428 | .pdf | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/workshop1.md` | 30529 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/workshop2.md` | 34963 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/workshop3.md` | 64177 | .md | Có |
| documents.zip | `documents/C_CPP_EMB_AUTOSAR/workshop4_remedial_1day.md` | 24293 | .md | Có |
| documents.zip | `documents/QB_Audit_1-5.xlsx` | 39450 | .xlsx | Có |
| documents.zip | `documents/workshop1.md` | 30529 | .md | Có |
| documents.zip | `documents/workshop2.md` | 34963 | .md | Có |
| documents.zip | `documents/workshop3.md` | 64177 | .md | Có |
| Base_C.zip | `Base_C/c_core/ex_01.c` | 1367 | .c | Có |
| Base_C.zip | `Base_C/c_core/ex_all.c` | 5961 | .c | Có |
| Base_C.zip | `Base_C/c_core/ex_all.exe` | 140172 | .exe | Không |
| Base_C.zip | `Base_C/c_test.c` | 2096 | .c | Có |
| Base_C.zip | `Base_C/CD_10/bai4.c` | 1119 | .c | Có |
| Base_C.zip | `Base_C/CD_10/bai4.exe` | 132818 | .exe | Không |
| Base_C.zip | `Base_C/CD_10/ex1.c` | 1696 | .c | Có |
| Base_C.zip | `Base_C/CD_10/ex1.exe` | 136082 | .exe | Không |
| Base_C.zip | `Base_C/CD_10/ex5.c` | 1638 | .c | Có |
| Base_C.zip | `Base_C/CD_10/ex5.exe` | 132470 | .exe | Không |
| Base_C.zip | `Base_C/CD_10/main.c` | 88 | .c | Có |
| Base_C.zip | `Base_C/CD_10/main.exe` | 139948 | .exe | Không |
| Base_C.zip | `Base_C/CD_10/student.c` | 240 | .c | Có |
| Base_C.zip | `Base_C/CD_10/student.h` | 13 | .h | Có |
| Base_C.zip | `Base_C/cd_3/cd_3.c` | 2089 | .c | Có |
| Base_C.zip | `Base_C/cd_3/cd_3.exe` | 135764 | .exe | Không |
| Base_C.zip | `Base_C/CD_7/ex1.c` | 2248 | .c | Có |
| Base_C.zip | `Base_C/CD_7/ex1.exe` | 140912 | .exe | Không |
| Base_C.zip | `Base_C/CD_8/ex1.c` | 1500 | .c | Có |
| Base_C.zip | `Base_C/CD_8/ex1.exe` | 140410 | .exe | Không |
| Base_C.zip | `Base_C/CD_8/ex4.c` | 2668 | .c | Có |
| Base_C.zip | `Base_C/CD_9/data.bin` | 20 | .bin | Không |
| Base_C.zip | `Base_C/CD_9/data.txt` | 36 | .txt | Có |
| Base_C.zip | `Base_C/CD_9/ex1.c` | 1700 | .c | Có |
| Base_C.zip | `Base_C/CD_9/ex1.exe` | 137817 | .exe | Không |
| Base_C.zip | `Base_C/CD1_c_core/ccc.c` | 1751 | .c | Có |
| Base_C.zip | `Base_C/CD1_c_core/cd1_c_core_all.c` | 1665 | .c | Có |
| Base_C.zip | `Base_C/CD1_c_core/pointer.c` | 3617 | .c | Có |
| Base_C.zip | `Base_C/CD1_c_core/pointer.exe` | 141509 | .exe | Không |
| Base_C.zip | `Base_C/cd4_Bitwise/bai_4.c` | 560 | .c | Có |
| Base_C.zip | `Base_C/cd4_Bitwise/bai4.exe` | 139673 | .exe | Không |
| Base_C.zip | `Base_C/cd4_Bitwise/bai5.c` | 1542 | .c | Có |
| Base_C.zip | `Base_C/cd4_Bitwise/bai5.exe` | 136044 | .exe | Không |
| Base_C.zip | `Base_C/cd4_Bitwise/Bitwise.c` | 2389 | .c | Có |
| Base_C.zip | `Base_C/cd4_Bitwise/Bitwise.exe` | 136860 | .exe | Không |
| Base_C.zip | `Base_C/cd5controlflow/bai1.c` | 1254 | .c | Có |
| Base_C.zip | `Base_C/cd5controlflow/bai1.exe` | 142201 | .exe | Không |
| Base_C.zip | `Base_C/cd5controlflow/bai5.c` | 2490 | .c | Có |
| Base_C.zip | `Base_C/cd5controlflow/bai5.exe` | 140330 | .exe | Không |
| Base_C.zip | `Base_C/CD6/bai5.c` | 357 | .c | Có |
| Base_C.zip | `Base_C/CD6/bai5.exe` | 136100 | .exe | Không |
| Base_C.zip | `Base_C/CD6/ex1.c` | 638 | .c | Có |
| Base_C.zip | `Base_C/CD6/ex1.exe` | 139525 | .exe | Không |
| Base_C.zip | `Base_C/CD6/ex3.c` | 370 | .c | Có |
| Base_C.zip | `Base_C/CD6/ex3.exe` | 139505 | .exe | Không |
| Base_C.zip | `Base_C/ex_02.c` | 1864 | .c | Có |
| Base_C.zip | `Base_C/ex_02.exe` | 132131 | .exe | Không |
| Base_C.zip | `Base_C/ex_03.c` | 1905 | .c | Có |
| Base_C.zip | `Base_C/ex_03.exe` | 132131 | .exe | Không |
| Base_C.zip | `Base_C/ex_04.c` | 1789 | .c | Có |
| Base_C.zip | `Base_C/ex_04.exe` | 136255 | .exe | Không |
| Base_C.zip | `Base_C/helloword.c` | 270 | .c | Có |
| Base_C.zip | `Base_C/helloword.exe` | 132131 | .exe | Không |
| Base_CPP.zip | `Base_C/c_core/ex_01.c` | 1367 | .c | Có |
| Base_CPP.zip | `Base_C/c_core/ex_all.c` | 5961 | .c | Có |
| Base_CPP.zip | `Base_C/c_core/ex_all.exe` | 140172 | .exe | Không |
| Base_CPP.zip | `Base_C/c_test.c` | 2096 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/bai4.c` | 1119 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/bai4.exe` | 132818 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_10/ex1.c` | 1696 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/ex1.exe` | 136082 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_10/ex5.c` | 1638 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/ex5.exe` | 132470 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_10/main.c` | 88 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/main.exe` | 139948 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_10/student.c` | 240 | .c | Có |
| Base_CPP.zip | `Base_C/CD_10/student.h` | 13 | .h | Có |
| Base_CPP.zip | `Base_C/cd_3/cd_3.c` | 2089 | .c | Có |
| Base_CPP.zip | `Base_C/cd_3/cd_3.exe` | 135764 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_7/ex1.c` | 2248 | .c | Có |
| Base_CPP.zip | `Base_C/CD_7/ex1.exe` | 140912 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_8/ex1.c` | 1500 | .c | Có |
| Base_CPP.zip | `Base_C/CD_8/ex1.exe` | 140410 | .exe | Không |
| Base_CPP.zip | `Base_C/CD_8/ex4.c` | 2668 | .c | Có |
| Base_CPP.zip | `Base_C/CD_9/data.bin` | 20 | .bin | Không |
| Base_CPP.zip | `Base_C/CD_9/data.txt` | 36 | .txt | Có |
| Base_CPP.zip | `Base_C/CD_9/ex1.c` | 1700 | .c | Có |
| Base_CPP.zip | `Base_C/CD_9/ex1.exe` | 137817 | .exe | Không |
| Base_CPP.zip | `Base_C/CD1_c_core/ccc.c` | 1751 | .c | Có |
| Base_CPP.zip | `Base_C/CD1_c_core/cd1_c_core_all.c` | 1665 | .c | Có |
| Base_CPP.zip | `Base_C/CD1_c_core/pointer.c` | 3617 | .c | Có |
| Base_CPP.zip | `Base_C/CD1_c_core/pointer.exe` | 141509 | .exe | Không |
| Base_CPP.zip | `Base_C/cd4_Bitwise/bai_4.c` | 560 | .c | Có |
| Base_CPP.zip | `Base_C/cd4_Bitwise/bai4.exe` | 139673 | .exe | Không |
| Base_CPP.zip | `Base_C/cd4_Bitwise/bai5.c` | 1542 | .c | Có |
| Base_CPP.zip | `Base_C/cd4_Bitwise/bai5.exe` | 136044 | .exe | Không |
| Base_CPP.zip | `Base_C/cd4_Bitwise/Bitwise.c` | 2389 | .c | Có |
| Base_CPP.zip | `Base_C/cd4_Bitwise/Bitwise.exe` | 136860 | .exe | Không |
| Base_CPP.zip | `Base_C/cd5controlflow/bai1.c` | 1254 | .c | Có |
| Base_CPP.zip | `Base_C/cd5controlflow/bai1.exe` | 142201 | .exe | Không |
| Base_CPP.zip | `Base_C/cd5controlflow/bai5.c` | 2490 | .c | Có |
| Base_CPP.zip | `Base_C/cd5controlflow/bai5.exe` | 140330 | .exe | Không |
| Base_CPP.zip | `Base_C/CD6/bai5.c` | 357 | .c | Có |
| Base_CPP.zip | `Base_C/CD6/bai5.exe` | 136100 | .exe | Không |
| Base_CPP.zip | `Base_C/CD6/ex1.c` | 638 | .c | Có |
| Base_CPP.zip | `Base_C/CD6/ex1.exe` | 139525 | .exe | Không |
| Base_CPP.zip | `Base_C/CD6/ex3.c` | 370 | .c | Có |
| Base_CPP.zip | `Base_C/CD6/ex3.exe` | 139505 | .exe | Không |
| Base_CPP.zip | `Base_C/ex_02.c` | 1864 | .c | Có |
| Base_CPP.zip | `Base_C/ex_02.exe` | 132131 | .exe | Không |
| Base_CPP.zip | `Base_C/ex_03.c` | 1905 | .c | Có |
| Base_CPP.zip | `Base_C/ex_03.exe` | 132131 | .exe | Không |
| Base_CPP.zip | `Base_C/ex_04.c` | 1789 | .c | Có |
| Base_CPP.zip | `Base_C/ex_04.exe` | 136255 | .exe | Không |
| Base_CPP.zip | `Base_C/helloword.c` | 270 | .c | Có |
| Base_CPP.zip | `Base_C/helloword.exe` | 132131 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD1/ex1.cpp` | 496 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD1/ex1.exe` | 151281 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD1/ex2.cpp` | 560 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD1/ex3.cpp` | 1323 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD1/ex3.exe` | 135617 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD1/ex5.cpp` | 2724 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD1/ex5.exe` | 187289 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD2/ex1.cpp` | 1265 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD2/ex1.exe` | 154475 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD2/ex2.cpp` | 2837 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD2/ex3.cpp` | 745 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD2/vector.cpp` | 1002 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/CD2/vector.exe` | 162030 | .exe | Không |
| Base_CPP.zip | `Base_CPP/CD4/ex1.cpp` | 175 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/EX_B/ex1.cpp` | 2344 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/EX_B/ex1.exe` | 159092 | .exe | Không |
| Base_CPP.zip | `Base_CPP/EX_B/ex2.cpp` | 560 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/EX_B/ex2.exe` | 146646 | .exe | Không |
| Base_CPP.zip | `Base_CPP/ex1.cpp` | 762 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/ex1.exe` | 148657 | .exe | Không |
| Base_CPP.zip | `Base_CPP/ex2.cpp` | 114 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/hello.cpp` | 115 | .cpp | Có |
| Base_CPP.zip | `Base_CPP/hello_cpp.exe` | 133371 | .exe | Không |
| Base_CPP.zip | `Base_CPP/test.cpp` | 2419 | .cpp | Có |

[Corrections](CORRECTIONS.md) · [References](REFERENCES.md) · [Index](00_INDEX.md).

## Map nguồn vào bài nền mở rộng —2026-10-06

| Nguồn nội bộ | Bài nền | Cách kế thừa |
|---|---|---|
| Base_C pointer/bitwise/struct/file | [C representation](embedded_systems/01_C_REPRESENTATION.md), [memory/build](embedded_systems/02_MEMORY_BUILD.md) | Giữ min/max/callback examples, giải thích bounds/overflow/status và byte order |
| Base_CPP vector/OOP/STL | [C++ ownership](embedded_systems/03_CPP_OWNERSHIP.md) | Thêm lifetime/realloc/copy/move/cost, giữ correction size/amortized |
| documents topics01–04 | [C/memory](embedded_systems/01_C_REPRESENTATION.md), [concurrency](embedded_systems/08_CONCURRENCY_BUFFERS.md) | Qualifier/shared count/borrowed callback chỉ dùng sau đối chiếu compiler/port |
| documents topics05–15/workshops/assignments | [peripherals](embedded_systems/05_PERIPHERAL_STATE_MACHINES.md), [ISR](embedded_systems/06_INTERRUPTS.md), [debug](debug/01_EVIDENCE_METHOD.md) | Dùng làm exercises/flow, không chứng nhận MISRA/AUTOSAR/safety compliance |
| PDF/workbook | [memory](embedded_systems/02_MEMORY_BUILD.md), [RTOS](embedded_systems/09_RTOS_SCHEDULER.md) | Giữ ý tưởng bounded resource, bổ sung ownership/deadline và nuance đã ghi corrections |

Ba SHA-256 archive khớp baseline khi kiểm lại2026-10-06. Reuse175 text entries đã trích xuất; không chạy binary, không sửa ZIP và không coi duplicate Base_C trong Base_CPP là nguồn độc lập. Web/runtime/OS gaps được bổ sung bằng official sources, không gán chúng cho nội dung ZIP chưa có.
