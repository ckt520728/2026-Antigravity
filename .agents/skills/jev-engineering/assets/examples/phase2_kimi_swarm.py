"""phase2_kimi_swarm.py - 兩階段架構之 Phase 2：Kimi-k3 蜂群平行執行與單次批次驗收 (OpenCode Go 版)

本腳本讀取 Phase 1 產出的 JSON 任務規格，透過 OpenCode Go 平台存取 Kimi-k3 模型，
支援高達 300 個並發子代理人平行執行，並整合 JEV Single-Pass 批次審查進行成果驗收，
消除 KV Cache Tax 與序列等待延遲。
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

# 將 jev 套件路徑加入 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jev import (
    SwarmConfig,
    SwarmTask,
    execute_kimi_swarm,
    load_queue_tasks,
    register_provider,
    run_two_phase_pipeline,
    save_task_spec,
    single_pass_batch_verify,
)


@register_provider("swarm_demo")
def demo_provider(state, questions, model, timeout):
    """離線驗收示範 Provider：模擬 JEV 決策層對蜂群產出進行 Single-Pass 批次審查。"""
    answers = {}
    for key, spec in questions.items():
        # 示範中模擬前 4 個任務質量優異給予 0.96 高分，第 5 個給予 0.72 觸發退回重跑收斂機制
        if key.endswith("005"):
            score = 0.72
        else:
            score = 0.96
        answers[key] = {"type": "noul", "noul": score}
    return {
        "model": "jev-1.13.0-demo",
        "answers": answers,
        "usage": {"input_tokens": 12, "output_tokens": 0},
    }


def run_demo():
    print("=" * 70)
    print("🚀 JEV 兩階段架構 Phase 2：OpenCode Kimi-k3 蜂群平行執行示範")
    print("=" * 70)

    with tempfile.TemporaryDirectory(prefix="jev-swarm-demo-") as tmpdir:
        queue_dir = Path(tmpdir) / "queue"
        queue_dir.mkdir(parents=True, exist_ok=True)

        # 模擬 Phase 1 產生 5 個獨立任務落盤至 queue (涵蓋醫療與神經計算學術範疇)
        sample_tasks = [
            SwarmTask(
                task_id=f"TSK-20261028-00{i+1}",
                clean_goal=f"分析第 {i+1} 組巴金森氏症 STN-GPe 網絡在 {100 + i*20}Hz DBS 刺激下的極限環吸引子抑制動力學。",
                assigned_worker="researcher" if i % 2 == 0 else "coder",
                filtered_context=(f"模型參數: 突觸強度 J={0.5 + i*0.1}, 膜時間常數 tau=20ms",),
                constraints=("繁體中文輸出", "包含常微分方程 (ODE) 數值穩定性考量", "使用校準之審慎語彙"),
                is_urgent=True if i == 0 else False,
                confidence=0.96,
            )
            for i in range(5)
        ]

        print(f"📦 [Phase 1 落盤] 寫入 {len(sample_tasks)} 項 TaskSpec JSON 至 {queue_dir} (零對話歷史負擔)...")
        for st in sample_tasks:
            spec_path = save_task_spec(st, queue_dir)
            print(f"  └─ 產生規格: {spec_path.name}")

        # Phase 2 讀取佇列
        print("\n🔍 [Phase 2 掃描] 讀取佇列中待執行任務 (Zero KV Cache Tax)...")
        loaded_tasks = load_queue_tasks(queue_dir)
        print(f"  └─ 成功讀取 {len(loaded_tasks)} 個有效任務規格。")

        # 配置 Kimi-k3 蜂群 (設定最大並發度為 300)
        config = SwarmConfig(
            max_concurrency=300,
            model_name="kimi-k3",
            tau_verify=0.85,
            timeout_seconds=30.0,
            queue_dir=str(queue_dir),
        )

        print(f"\n⚡ [Phase 2 蜂群並發] 啟動 Kimi-k3 平行蜂群 (Max Concurrency: {config.max_concurrency})...")
        t_start = time.time()
        
        # 執行蜂群
        results = execute_kimi_swarm(loaded_tasks, config)
        swarm_elapsed = time.time() - t_start
        print(f"  └─ 蜂群執行完成！耗時: {swarm_elapsed:.3f} 秒 (平均每任務 {swarm_elapsed/len(results):.3f}s)")
        for res in results:
            print(f"     * [{res.task_id}] 狀態: {res.status} | 延遲: {res.latency_s:.3f}s | 模型: {res.model}")

        # Phase 1 離線 Single-Pass 批次驗收 (Single-Pass Batch Review)
        print("\n🛡️ [JEV 批次驗收] 執行 Single-Pass 批次審查 (打包所有輸出，單次判斷消弭排隊瓶頸)...")
        t_verify = time.time()
        provider = os.environ.get("JEV_PROVIDER", "swarm_demo")
        passed, requeued, scores = single_pass_batch_verify(results, config, provider=provider)
        verify_elapsed = time.time() - t_verify
        print(f"  └─ 批次驗收完成！耗時: {verify_elapsed:.3f} 秒 (單次搞定全部 {len(results)} 項產出)")

        print("\n📊 [兩階段執行成效矩陣]:")
        print(f"  - 總派發任務數: {len(sample_tasks)}")
        print(f"  - 蜂群成功完成: {len([r for r in results if r.status == 'completed'])}")
        print(f"  - 驗收合格通過: {len(passed)} 項")
        print(f"  - 退回重跑標記: {len(requeued)} 項")
        for tid, score in scores.items():
            verdict = "PASS (核可出庫)" if score >= config.tau_verify else "REQUEUE (留佇重跑)"
            print(f"     * {tid}: JEV 信心分 {score:.2f} -> {verdict}")

        remaining_in_queue = list(queue_dir.glob("*.json"))
        print(f"\n🧹 [佇列自動清理] 驗收通過之規格已自動移出 queue，目前佇列剩餘: {len(remaining_in_queue)} 檔 (待下輪收斂)。")
        print("=" * 70)
        print("✅ 兩階段無延遲跨平台管線 (Phase 1 High Planner -> Phase 2 Kimi-k3 Swarm) 驗證成功！")
        print("=" * 70)


if __name__ == "__main__":
    run_demo()
