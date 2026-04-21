# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 50
- **Tỉ lệ Pass/Fail:** 42 / 8 (Tỉ lệ Pass: 84%)
- **Điểm RAGAS trung bình:**
    - Faithfulness: 0.85
    - Relevancy: 0.80
- **Chỉ số Retrieval:**
    - Hit Rate V2: 98.0% (Tăng từ 66.0% ở V1)
    - Muti Judge Agreement: 72.0%
- **Điểm LLM-Judge trung bình (V2):** 3.87 / 5.0

## 2. Phân nhóm lỗi (Failure Clustering)
| Nhóm lỗi | Số lượng | Nguyên nhân dự kiến |
|----------|----------|---------------------|
| Hallucination | 4 | Có cung cấp Context nhưng thông tin vẫn bị sinh ảo (LLM quá tự do ngụy tạo). |
| Incomplete | 3 | Prompt Agent chưa ép LLM đi vào trọng tâm, câu trả lời còn cụt lủn. |
| Position Bias | 1 | Hệ logic Judge hoặc Agent dễ bị loạn khi ID nằm quá xa trong bảng xếp hạng. |

## 3. Phân tích 5 Whys (Chọn 3 case tệ nhất)

### Case #1: Lỗi Hallucination trong câu trả lời (Final Score: 2.0)
1. **Symptom:** AI Agent bịa ra một quyền lợi nghỉ phép không có trong chính sách.
2. **Why 1:** LLM đã bịa câu trả lời khi tổng hợp từ các đoạn tài liệu tìm thấy.
3. **Why 2:** Mặc dù lấy trúng `ground_truth_id` nhưng lại lấy kèm thêm các văn bản nhiễu (Retrieved Noise).
4. **Why 3:** Hệ thống tính điểm Retrieval Evaluator chủ yếu đánh giá `Hit Rate` chứ chưa lọc kỹ `Precision`.
5. **Why 4:** Top-K truyền cho LLM quá lớn (top_k=3), khiến context lộn xộn.
6. **Root Cause:** Cần tinh chỉnh System Prompt của Agent: "Bám sát tài liệu một cách tuyệt đối, nếu tài liệu không nhắc tới thì báo Không Biết".

## 4. Kế hoạch cải tiến (Action Plan)
- [ ] Bật `Temperature = 0` cho phần sinh câu trả lời trong quá trình RAG.
- [ ] Cập nhật System Prompt để nhấn mạnh vào việc "Chỉ trả lời dựa trên context".
- [ ] Mở rộng thử nghiệm thư viện đánh giá chuyên sâu hơn ngoài Relevancy và Faithfulness.
