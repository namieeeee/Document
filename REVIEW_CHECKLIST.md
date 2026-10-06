# Checklist cho reviewer độc lập

Các câu hỏi này kiểm tra phạm vi bằng chứng; checklist không phải chứng nhận nội dung đã đúng.

1. Claim có ghi phiên bản, môi trường và assumptions cần thiết không?
2. Nguồn chính thống có thực sự nói về claim, hay chỉ cùng chủ đề? URL truy cập được chưa chứng minh claim.
3. Invariant có giữ nguyên giữa bản lỗi và bản sửa không?
4. Trigger có buộc đúng thứ tự gây lỗi, hay phụ thuộc may rủi/timing?
5. Lệnh có chạy lại từ checkout với dependency/lockfile rõ ràng không?
6. Evidence có ngày, phiên bản, lệnh, exit code và raw output không?
7. FAIL được dự kiến có đúng assertion không, hay chỉ import/build thất bại?
8. Negative/boundary/conflicting-payload/cancellation paths đã được kiểm tra tới đâu?
9. Kết luận có vượt khỏi host model, jsdom, standalone DB hoặc một instance không?
10. Có gọi pseudocode, source review, demo Python là kiểm chứng compiler/MCU không?
11. Mục lục, anchors, 16 mục canonical và 121 dòng lab-map có qua `python scripts/check_links.py` không?
12. Outline có trích output từ evidence thật và chỉ ra phần demo còn BLOCKED không?

[Matrix claim/evidence](THEORY_COVERAGE_MATRIX.md) · [Review lần hai](audit/SELF_REVIEW.md) · [Validation](VALIDATION.md).
