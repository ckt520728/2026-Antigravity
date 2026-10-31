"""讀回驗證本輪初始化契約；不測量臨床正確性或假裝完整 live routing。"""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import unquote
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / "vendor"))
from jev.toolgate import CAPABILITIES
from jev.workflow import _tasks, Limits, WorkflowStop
from run_jev_checks import parse_task


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def approval_allows_production(approval, current_hash):
    return approval.get("status") == "approved" and approval.get("sha256") == current_hash


def main():
    checks = []

    def check(name, condition, detail=""):
        checks.append({"check": name, "passed": bool(condition), "detail": detail})

    agent_path = ROOT / ".claude/agents/mounjaro-research.md"
    agent = agent_path.read_text(encoding="utf-8")
    front = re.match(r"\A---\s*\n(.*?)\n---\s*\n", agent, flags=re.S)
    metadata = yaml.safe_load(front.group(1)) if front else {}
    check("agent YAML 必要欄位", set(("name", "description", "tools", "model", "permissionMode")) <= set(metadata))
    builtin = {"Read", "Glob", "Grep", "Edit", "Write", "Bash", "WebSearch", "WebFetch"}
    mcp = {"mcp__notebooklm__" + name for name in ("notebook_list", "notebook_get", "notebook_describe", "notebook_query", "source_get_content", "studio_status", "download_artifact")}
    declared = {t.strip() for t in metadata.get("tools", "").split(",") if t.strip()}
    check("tools 僅合法 builtin 與 inventory MCP", declared == builtin | mcp)
    check("agent 權限與模型為 Claude Code 正規欄位", metadata.get("permissionMode") == "default" and metadata.get("model") == "sonnet")
    check("agent 含八類 ToolGate", all(cap in agent for cap in CAPABILITIES))
    rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    check("根規則含八類 ToolGate", all(cap in rules for cap in CAPABILITIES))
    queue = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    tasks = tuple(parse_task(item) for item in queue["tasks"])
    limits = Limits(max_tasks=4, max_worker_output_tokens=18000, max_total_output_tokens=50000)
    _tasks(tasks, limits)
    check("TaskSpec 欄位、依賴、唯一輸出與預算", True)
    approval = json.loads((HERE / "approval.json").read_text(encoding="utf-8"))
    current_hash = sha(ROOT / approval["outline"])
    approval_ok = approval_allows_production(approval, current_hash)
    check("outline 核准狀態與 hash 一致", queue["outline_approval"] == approval and (approval_ok or approval.get("status") == "pending"))
    production = json.loads((HERE / "production-tasks.json").read_text(encoding="utf-8"))
    _tasks(tuple(parse_task({k:v for k,v in item.items() if k != "status"}) for item in production["tasks"]), Limits(max_tasks=5, max_worker_output_tokens=18000, max_total_output_tokens=70000))
    check("production TaskSpec 八欄、依賴、唯一輸出與預算", True)
    def no_corruption(value):
        if isinstance(value, dict):
            return all(no_corruption(v) for k, v in value.items() if k != "scope_original_corrupted")
        if isinstance(value, list):
            return all(no_corruption(v) for v in value)
        return not isinstance(value, str) or "??" not in value
    check("新控制字串不得有連續問號損毀", no_corruption(queue) and no_corruption(production) and no_corruption(approval))
    check("production 只在核准 hash 相符後啟動；無發布與花費授權", (approval_ok or not production["production_dispatched"]) and not production["publication_authorized"] and not production["spend_authorized"])
    for label, bad in (
        ("未知能力必須拒絕", (replace(tasks[0], capabilities=("invented",)),)),
        ("未出現依賴必須拒絕", (replace(tasks[0], depends_on=("T2",)),)),
        ("重複成品必須拒絕", (tasks[0], replace(tasks[1], outputs=tasks[0].outputs))),
    ):
        try:
            _tasks(bad, limits)
        except WorkflowStop:
            check(label, True)
        else:
            check(label, False)
    baseline = json.loads((HERE / "preservation-baseline.json").read_text(encoding="utf-8"))
    changed = [item["path"] for item in baseline if not (ROOT / item["path"]).is_file() or sha(ROOT / item["path"]) != item["sha256"]]
    protected = [p for p in changed if p != "2026 GLP-1 RA Monjaro.txt"]
    check("原 ZIP／舊成果 hash 不變", not protected, f"{len(baseline)-1} 個受保護檔；差異：{protected}")
    input_record = json.loads((HERE / "input-change-20261031.json").read_text(encoding="utf-8"))
    check("原 baseline 差異誠實保留且當前 prompt 有記錄", changed == input_record["baseline_differences"] and sha(ROOT / input_record["path"]) == input_record["current_sha256"], str(changed))
    pin = json.loads((HERE / "source-pin.json").read_text(encoding="utf-8"))
    changed_pin = [item["path"] for item in pin["files"] if not (ROOT / item["path"]).is_file() or sha(ROOT / item["path"]) != item["sha256"]]
    check("JEV vendor 原始 bytes pin 不變", not changed_pin, f"{len(pin['files'])} 檔；差異：{changed_pin}")
    authored = [ROOT / p for p in ("AGENTS.md", "handoffs.md", ".claude/agents/mounjaro-research.md", "monjaro/README.md", "monjaro/workflow/WORKFLOW.md", "monjaro/workflow/TOOL_CONTRACT.md", "monjaro/workflow/EXECUTION.md")]
    missing = []
    for path in authored:
        if not path.is_file():
            missing.append(str(path))
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*://", target) or target.startswith("#"):
                continue
            cleaned = unquote(target.split("#", 1)[0].strip("<>"))
            resolved = Path(cleaned) if re.match(r"^[A-Za-z]:[/\\]", cleaned) else path.parent / cleaned
            if not resolved.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    check("自撰初始化文件的本地 Markdown links", not missing, str(missing))
    for task in tasks[:2]:
        absent = [p for p in task.outputs if not (ROOT / p).exists()]
        check(f"{task.task_id} 宣告的成品存在", not absent, str(absent))
    results = json.loads((HERE / "jev-checks.json").read_text(encoding="utf-8"))
    check("真實 JEV checks：保持 ask 與 executor 零呼叫", results["plan_phase"]["status"] == "ask" and results["execute_phase"]["status"] == "ask" and results["adapter_calls"]["executor"] == 0)
    check("JEV 自動 production 未派發；host 手動派發另記", not results["routing_ready"] and not results["production_dispatched"])
    payload = {"status": "passed" if all(c["passed"] for c in checks) else "failed", "checks": checks,
               "scope": "初始化結構、來源完整性與執行邊界；clinical claims 及 T3 獨立主控驗收另計"}
    (HERE / "validation-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
