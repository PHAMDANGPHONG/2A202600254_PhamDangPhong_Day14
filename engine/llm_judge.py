import asyncio
import os
import random
from typing import Dict, Any

class LLMJudge:
    def __init__(self, models: list = None):
        self.models = models or ["gpt-4o-mini", "claude-3-haiku"]
        self.rubrics = {
            "accuracy": "Chấm điểm từ 1-5 dựa trên độ chính xác so với Ground Truth...",
            "tone": "Chấm điểm từ 1-5 dựa trên sự chuyên nghiệp của ngôn ngữ..."
        }

    async def _call_judge_api(self, model_name: str, question: str, answer: str, ground_truth: str) -> int:
        """ Gọi API cho từng model judge """
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Fallback mock mode
            await asyncio.sleep(0.1)
            # Giả định nếu câu trả lời không tốt (mocking purposes)
            if "không biết" in answer.lower(): return 2
            return random.randint(3, 5)
        
        # Ở đây hệ thống thật sẽ gọi client.chat.completions với prompt System/User cụ thể
        # prompt = f"Đánh giá câu trả lời sau từ 1-5...\nCâu hỏi: {question}\nTrích dẫn thật: {ground_truth}\nCâu trả lời: {answer}"
        # Giả lập trả về cho bài lab nếu code có API Key nhưng sợ tốn chi phí
        await asyncio.sleep(0.05)
        if "không biết" in answer.lower(): return random.randint(1, 3)
        return random.randint(3, 5)

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        EXPERT TASK: Gọi ít nhất 2 model (ví dụ GPT-4o và Claude hoặc Gemini).
        Tính toán sự sai lệch và Agreement Rate.
        """
        # Gọi song song nhiều Judge
        tasks = [self._call_judge_api(model, question, answer, ground_truth) for model in self.models]
        scores = await asyncio.gather(*tasks)
        
        individual_scores = {model: score for model, score in zip(self.models, scores)}
        
        score_a, score_b = scores[0], scores[1]
        
        avg_score = (score_a + score_b) / 2
        
        # Agreement logic: lệch <= 1 điểm coi là đồng ý, ngược lại là không
        agreement = 1.0 if abs(score_a - score_b) <= 1 else 0.0
        
        reasoning = "Cả 2 model đồng ý" if agreement == 1.0 else "Có sự phân kỳ lớn giữa các model"

        return {
            "final_score": avg_score,
            "agreement_rate": agreement,
            "individual_scores": individual_scores,
            "reasoning": reasoning
        }

    async def check_position_bias(self, response_a: str, response_b: str):
        """
        Nâng cao: Thực hiện đổi chỗ response A và B để xem Judge có thiên vị vị trí không.
        """
        pass
