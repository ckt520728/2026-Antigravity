"""實跑原始 JEV local scorer 與未接模型 adapter 的 fail-closed 邊界。"""
from dataclasses import asdict
from pathlib import Path
from datetime import datetime, timezone
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / "vendor"))
from jev import Choice, decide
from jev.routing import TIER_CRITERIA, DATA_CLASSES
from jev.toolgate import ToolGate, CAPABILITIES
from jev.workflow import TaskSpec, Limits, WorkflowStop, plan_phase, execute_phase, _tasks


def parse_task(item):
    item = dict(item)
    for field in ("inputs", "outputs", "acceptance", "capabilities", "depends_on"):
        item[field] = tuple(item[field])
    return TaskSpec(**item)


def main():
    raw = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    tasks = tuple(parse_task(t) for t in raw["tasks"][:3])
    limits = Limits(max_tasks=4, max_worker_output_tokens=18000,
                    max_total_output_tokens=50000, max_tool_calls=12)
    _tasks(tasks, limits)
    questions = {}
    for i in range(len(tasks)):
        questions[f"tier_{i}"] = Choice(
            instructions=f"任務 {i} 已有結構規格。選最低可正確執行 tier；尚須設計時選 high；無法判斷選 other。",
            criteria=TIER_CRITERIA)
        questions[f"data_{i}"] = Choice(
            instructions=f"任務 {i} 與參照涉及何種資料？不能推斷時選 other。",
            criteria=DATA_CLASSES)
    state = {"tasks": [asdict(t) for t in tasks], "data_class": "internal"}
    result = decide(state=json.dumps(state, ensure_ascii=False),
                    questions=questions, provider="local", retries=1)
    gate = ToolGate(cacheable_capabilities=frozenset())
    checks = [
        ("Read", {"file_path": str(ROOT / "2026 GLP-1 RA Monjaro.txt")}),
        ("Write", {"file_path": str(HERE / "scope-check-only.txt"), "content": "僅分類，不寫檔"}),
        ("WebFetch", {"url": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/215866s039lbl.pdf"}),
        ("Bash", {"command": "git push --force"}),
    ]
    gate_results = []
    for tool, arguments in checks:
        verdict = gate.check(tool, arguments, cwd=str(ROOT), provider="local")
        gate_results.append({"tool": tool, "arguments": arguments, "verdict": asdict(verdict),
                             "side_effect_executed": False})
    calls = {"planner_adapter": 0, "executor": 0, "verifier": 0, "tool_runner": 0}

    def missing_planner(request):
        calls["planner_adapter"] += 1
        raise WorkflowStop("未接線：Python 無可驗證 host high model adapter 與實際 token usage；不產生假的 PlannerResult")

    def forbidden_executor(*args):
        calls["executor"] += 1
        raise AssertionError("未 ready 不得呼叫 executor")

    def forbidden_verifier(*args):
        calls["verifier"] += 1
        raise AssertionError("未 ready 不得驗收虛構成品")

    def forbidden_runner(*args):
        calls["tool_runner"] += 1
        raise AssertionError("未 ready 不得執行副作用")

    plan = plan_phase("初始化 Mounjaro 專案；來源與 TaskSpec 已落盤；模型 adapter 尚未接線。",
                      missing_planner, data_class="internal", limits=limits, provider="local")
    report = execute_phase(plan, forbidden_executor, verifier=forbidden_verifier,
                           tool_runner=forbidden_runner, provider="local", cwd=str(ROOT))
    assert plan.status == "ask" and report.status == "ask"
    assert calls["executor"] == calls["verifier"] == calls["tool_runner"] == 0
    assert gate_results[-1]["verdict"]["decision"] == "deny"
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "真正 local scorer／ToolGate＋未接 adapter 的停止邊界；不是 live API 或完整自動生產",
        "capabilities": list(CAPABILITIES), "tasks_validated": [t.task_id for t in tasks],
        "local_decision": {"provider": result.provider, "raw": result.raw,
                           "latency_ms": result.latency_ms},
        "routing_ready": False, "toolgate": gate_results, "gate_audit": gate.audit,
        "plan_phase": asdict(plan), "execute_phase": asdict(report), "adapter_calls": calls,
        "host_dispatch": "T1/T2 由主控明確配置的受限 executor 啟動；先前執行中斷，本輪恢復，產物待主控獨立驗收；不代表 Jev ready。",
        "usage_limit": "local scorer 自報零 token；不包含 host planner/executor/context/tool 費用，未量測 savings。",
        "production_dispatched": False,
        "budget_enforcement": "not_exposed；host TaskSpec 是宣告預算，不是 API 硬限制證據",
        "upstream_local_incompatibility": "首次以 dict state 呼叫 local provider 產 TypeError expected string or bytes-like object；直接 decide 改傳 JSON string 後可實跑，vendor 未修改。ToolGate 內部仍傳 dict，因此真實 fail-to-ask 原因保留。",
    }
    (HERE / "jev-checks.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"local_confidences": {k: a.confidence for k, a in result.answers.items()},
                      "gate_decisions": [g["verdict"]["decision"] for g in gate_results],
                      "plan": plan.status, "execute": report.status, "calls": calls}, ensure_ascii=False))


if __name__ == "__main__":
    main()
