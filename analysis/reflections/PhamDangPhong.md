# Báo cáo Cá nhân (Reflection) - Lab Day 14

**Họ và tên:** Phạm Đăng Phong
**Mã sinh viên:** 2A202600254
**Vai trò trong nhóm:** AI Engineer / Lead

## 1. Đóng góp kỹ thuật (Engineering Contribution)
- **Xây dựng Evaluation Engine:** Trực tiếp thiết kế và triển khai module `RetrievalEvaluator` để tính toán chính xác Hit Rate và MRR (Mean Reciprocal Rank) cho hệ thống RAG.
- **Triển khai Multi-Judge Consensus:** Tích hợp logic đánh giá song song sử dụng cả GPT-4o-mini và Claude-3-Haiku để giảm thiểu bias của model đơn lẻ, đạt tỉ lệ đồng thuận (Agreement Rate) trung bình 68%.
- **Quy trình Regression Testing:** Xây dựng script so sánh tự động giữa phiên bản Base (V1) và Optimized (V2), triển khai "Release Gate" để tự động ngăn chặn việc đẩy code nếu các chỉ số chất lượng bị sụt giảm.

## 2. Bài học chuyên môn (Technical Depth)
- **Ưu điểm của MRR:** Qua quá trình lab, em nhận thấy MRR phản ánh chất lượng tìm kiếm thực tế tốt hơn Hit Rate vì nó ưu tiên các tài liệu đúng nằm ở vị trí top 1, top 2 thay vì chỉ kiểm tra sự tồn tại đơn thuần.
- **Vấn đề Position Bias:** Hiểu được rằng các model LLM Judge thường có xu hướng thiên vị câu trả lời xuất hiện đầu tiên hoặc cuối cùng trong context. Việc đảo vị trí các câu trả lời khi đánh giá là cần thiết để đảm bảo tính khách quan.
- **Tối ưu Cost/Quality:** Việc phối hợp các model nhỏ (Haiku, GPT-4o-mini) làm Judge mang lại hiệu quả chi phí cực tốt mà vẫn đảm bảo được độ tin cậy thông qua cơ chế Consensus.

## 3. Khó khăn & Giải pháp (Problem Solving)
- **Khó khăn:** Quá trình đánh giá 50 test cases với nhiều model Judge tốn nhiều thời gian nếu chạy tuần tự, dễ gặp lỗi Rate Limit của API.
- **Giải pháp:** Sử dụng `asyncio.gather` để thực thi song song các task, kết hợp với cơ chế batching trong `BenchmarkRunner` để kiểm soát lưu lượng request, giúp toàn bộ pipeline hoàn thành trong thời gian ngắn (< 1 phút).
