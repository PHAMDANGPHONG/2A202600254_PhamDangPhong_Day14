import asyncio
import random
from typing import List, Dict

class MainAgent:
    """
    Đây là Agent mẫu sử dụng kiến trúc RAG.
    Đã được nâng cấp để trả về `retrieved_ids` phục vụ bài toán AI Evaluation.
    """
    def __init__(self, version: str = "V1"):
        self.name = f"SupportAgent-{version}"
        self.version = version

    async def query(self, question: str, ground_truth_id: str = None) -> Dict:
        """
        Mô phỏng quy trình RAG:
        1. Retrieval: Tìm kiếm context liên quan.
        2. Generation: Gọi LLM.
        """
        await asyncio.sleep(0.01) # Faster simulation for async batching
        
        # Mô phỏng việc lấy Document IDs
        # Nếu là bản V2 (Tối ưu), tỷ lệ lấy trúng ID xịn cao hơn V1
        hit_chance = 0.95 if "V2" in self.version else 0.60
        
        retrieved_ids = []
        if ground_truth_id and random.random() < hit_chance:
            # Lấy trúng
            retrieved_ids.append(ground_truth_id)
        
        # Thêm vài ID nhiễu để ra top_k
        while len(retrieved_ids) < 3:
            fake_id = f"doc_{random.randint(11, 100)}"
            if fake_id not in retrieved_ids:
                retrieved_ids.append(fake_id)
                
        random.shuffle(retrieved_ids) # Xáo trộn ngẫu nhiên

        # Nếu V2, câu trả lời cũng gãy gọn mạnh mẽ hơn.
        answer = f"Dựa trên tài liệu hệ thống, tôi xin trả lời câu hỏi '{question}' như sau: [Câu trả lời tốt]."
        if hit_chance < 0.7 and random.random() < 0.3:
            answer = "Tôi không biết câu trả lời cho vấn đề này."

        return {
            "answer": answer,
            "contexts": [
                "Đoạn văn bản trích dẫn 1 dùng để trả lời...",
                "Đoạn văn bản trích dẫn 2 dùng để trả lời..."
            ],
            "metadata": {
                "model": "gpt-4o-mini",
                "tokens_used": random.randint(100, 200),
                "sources": ["policy_handbook.pdf"],
                "retrieved_ids": retrieved_ids
            }
        }

if __name__ == "__main__":
    agent = MainAgent("V2")
    async def test():
        resp = await agent.query("Làm thế nào để đổi mật khẩu?", "doc_1")
        print(resp)
    asyncio.run(test())
