import asyncio
import json
import os
import time
from engine.runner import BenchmarkRunner
from agent.main_agent import MainAgent
from engine.retrieval_eval import RetrievalEvaluator
from engine.llm_judge import LLMJudge
from dotenv import load_dotenv

load_dotenv()

async def run_benchmark_with_results(agent_version: str):
    print(f"🚀 Khởi động Benchmark cho {agent_version}...")

    if not os.path.exists("data/golden_set.jsonl"):
        print("❌ Thiếu data/golden_set.jsonl. Hãy chạy 'python data/synthetic_gen.py' trước.")
        return None, None

    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        print("❌ File data/golden_set.jsonl rỗng. Hãy tạo ít nhất 1 test case.")
        return None, None

    # Khởi tạo các Core Components
    agent = MainAgent(version=agent_version)
    evaluator = RetrievalEvaluator()
    judge = LLMJudge()
    
    runner = BenchmarkRunner(agent, evaluator, judge)
    
    start_time = time.time()
    results = await runner.run_all(dataset, batch_size=10)
    duration = time.time() - start_time

    total = len(results)
    
    # Tính toán thông số
    avg_score = sum(r["judge"]["final_score"] for r in results) / total
    hit_rate = sum(r["ragas"]["retrieval"]["hit_rate"] for r in results) / total
    mrr = sum(r["ragas"]["retrieval"]["mrr"] for r in results) / total
    agreement_rate = sum(r["judge"]["agreement_rate"] for r in results) / total
    tokens_used = sum(r.get("metadata", {}).get("tokens_used", 0) for r in results)
    
    # Tính Cost ước tính (Ví dụ GPT-4o-mini price)
    estimated_cost = (tokens_used / 1000) * 0.00015
    
    summary = {
        "metadata": {
            "version": agent_version, 
            "total": total, 
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_sec": round(duration, 2),
            "tokens_used": tokens_used,
            "estimated_cost_usd": round(estimated_cost, 4)
        },
        "metrics": {
            "avg_score": round(avg_score, 2),
            "hit_rate": round(hit_rate, 2),
            "mrr": round(mrr, 2),
            "agreement_rate": round(agreement_rate, 2)
        }
    }
    return results, summary

async def run_benchmark(version):
    _, summary = await run_benchmark_with_results(version)
    return summary

async def main():
    print("--- CHẠY PIPELINE BENCHMARK ---")
    v1_summary = await run_benchmark("Agent_V1_Base")
    if not v1_summary: return
    
    print("\n--- CHẠY PIPELINE OPTIMIZED ---")
    v2_results, v2_summary = await run_benchmark_with_results("Agent_V2_Optimized")
    
    if not v1_summary or not v2_summary:
        print("❌ Không thể lập báo cáo.")
        return

    print("\n📊 --- KẾT QUẢ SO SÁNH (REGRESSION) ---")
    delta_score = v2_summary["metrics"]["avg_score"] - v1_summary["metrics"]["avg_score"]
    delta_hr = v2_summary["metrics"]["hit_rate"] - v1_summary["metrics"]["hit_rate"]
    
    print(f"| Chỉ số | Agent V1 | Agent V2 | Delta |")
    print(f"|---|---|---|---|")
    print(f"| Điểm (Score) | {v1_summary['metrics']['avg_score']} | {v2_summary['metrics']['avg_score']} | {delta_score:+.2f} |")
    print(f"| Hit Rate | {v1_summary['metrics']['hit_rate'] * 100:.1f}% | {v2_summary['metrics']['hit_rate'] * 100:.1f}% | {delta_hr * 100:+.1f}% |")
    print(f"| Agreement | {v1_summary['metrics']['agreement_rate'] * 100:.1f}% | {v2_summary['metrics']['agreement_rate'] * 100:.1f}% | - |")
    print(f"| Cost | ${v1_summary['metadata']['estimated_cost_usd']} | ${v2_summary['metadata']['estimated_cost_usd']} | - |")

    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(v2_summary, f, ensure_ascii=False, indent=2)
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)

    # Autogate Release Decision
    passed_gate = True
    reasons = []
    
    if delta_score < 0:
        passed_gate = False
        reasons.append("Chất lượng câu trả lời giảm")
    if delta_hr < 0:
        passed_gate = False
        reasons.append("Chất lượng tìm kiếm (Retrieval) giảm")
        
    print("\n")
    if passed_gate:
        print("✅ QUYẾT ĐỊNH: CHẤP NHẬN BẢN CẬP NHẬT (APPROVE)")
    else:
        print(f"❌ QUYẾT ĐỊNH: TỪ CHỐI (BLOCK RELEASE). Lý do: {', '.join(reasons)}")
        
    print("\n📁 Files được tạo:")
    print("   - reports/summary.json")
    print("   - reports/benchmark_results.json")

if __name__ == "__main__":
    asyncio.run(main())
