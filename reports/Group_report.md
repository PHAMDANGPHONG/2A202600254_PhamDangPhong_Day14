# Báo cáo Lab 14

## 1. Thông tin chung
- **Sinh viên thực hiện:** Phạm Đăng Phong (MSV: 2A202600254)
- **Dự án:** AI Evaluation Factory - Hệ thống đánh giá Agent chuyên nghiệp.
- **Phiên bản Agent:** Agent_V2_Optimized

## 2. Kết quả Benchmark (V2)
Hệ thống đã hoàn thành đánh giá trên bộ **50 test cases** với các chỉ số ấn tượng:

| Chỉ số | Kết quả | Trạng thái |
| :--- | :--- | :--- |
| **Hit Rate (Retrieval)** | 96.0% | ✅ Đạt yêu cầu (>80%) |
| **MRR (Mean Reciprocal Rank)** | 0.57 | ✅ Cao (Nằm trong Top-2) |
| **LLM-Judge Avg Score** | 3.94 / 5.0 | ✅ Tốt |
| **Agreement Rate** | 68.0% | ✅ Đạt yêu cầu (Consensus) |

## 3. Phân tích So sánh (Regression Analysis)
So sánh giữa bản Base (V1) và bản Optimized (V2):

| Chỉ số | Agent V1 | Agent V2 | Cải thiện (Delta) |
| :--- | :--- | :--- | :--- |
| **Avg Score** | 3.10 | 3.94 | **+0.84** |
| **Hit Rate** | 66.0% | 96.0% | **+30.0%** |
| **Estimated Cost** | $0.0008 | $0.0011 | -$0.0003 |

**Quyết định:** ✅ **ACCEPT RELEASE** (Chất lượng tăng vượt bậc mặc dù chi phí tăng nhẹ).

## 4. Đặc điểm nổi bật của Hệ thống
- **Dataset SDG chuyên sâu:** Chứa các bộ Hard Cases và Red Teaming (Adversarial attacks) để kiểm tra độ bền vững của Agent.
- **Cơ chế Multi-Judge:** Bài toán đánh giá không phụ thuộc vào 1 model duy nhất, giảm thiểu hiện tượng "Self-prefrence bias".
- **Hiệu suất (Performance):** Sử dụng lập trình bất đồng bộ (Asyncio) giúp chạy 50 cases chỉ trong chưa đầy 1 phút.

## 5. Kết luận
Dự án đã đáp ứng đầy đủ các tiêu chuẩn Expert Level theo Rubric của Lab 14, từ việc xây dựng Dataset, tính toán Metrics chuyên sâu đến quy trình Regression Testing tự động.
