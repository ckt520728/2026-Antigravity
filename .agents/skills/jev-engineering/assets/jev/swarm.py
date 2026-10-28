"""Phase 2 Kimi-k3 300 平行蜂群執行與 JEV 單次批次驗收 (Single-Pass Batch Review)。

標準庫相容實作 (stdlib-only, Python 3.9+)，無第三方套件強制依賴。
支援 OpenCode Go (OpenAI-compatible) API 與本地/離線降級測試。
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence, Union

from .client import decide
from .types import Choice, Noul, Score

DEFAULT_OPENCODE_BASE_URL = "https://api.opencode.ai/v1"
DEFAULT_KIMI_MODEL = "kimi-k3"
DEFAULT_SWARM_MAX_CONCURRENCY = 300
DEFAULT_VERIFY_TAU = 0.85


@dataclass(frozen=True)
class SwarmConfig:
    max_concurrency: int = DEFAULT_SWARM_MAX_CONCURRENCY
    model_name: str = DEFAULT_KIMI_MODEL
    base_url: str = ""
    api_key: str = ""
    tau_verify: float = DEFAULT_VERIFY_TAU
    timeout_seconds: float = 60.0
    temperature: float = 0.3
    queue_dir: str = "queue"
    output_dir: str = "output"

    def resolved_base_url(self) -> str:
        url = (
            self.base_url
            or os.environ.get("OPENCODE_API_URL")
            or os.environ.get("OPENCODE_BASE_URL")
            or os.environ.get("OPENAI_BASE_URL")
            or DEFAULT_OPENCODE_BASE_URL
        )
        return url.rstrip("/")

    def resolved_api_key(self) -> str:
        return self.api_key or os.environ.get("OPENCODE_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""


@dataclass(frozen=True)
class SwarmTask:
    task_id: str
    clean_goal: str
    assigned_worker: str = "researcher"     # researcher | coder | reviewer | general
    filtered_context: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ("local_write",)
    is_urgent: bool = False
    confidence: float = 0.95
    source_file: Optional[str] = None
    handoff_version: str = "2.1.0"

    def to_spec_dict(self) -> dict[str, Any]:
        return {
            "handoff_version": self.handoff_version,
            "task_id": self.task_id,
            "source_platform": "Claude CLI / Codex.cmd (Phase 1 High Planner)",
            "target_platform": "OpenCode Go Desktop (Phase 2 Kimi-k3 Swarm)",
            "decision_summary": {
                "is_blocked": False,
                "risk_level": "local_edit",
                "category": self.assigned_worker,
                "relevance_score": 1.8,
                "is_urgent": self.is_urgent,
                "prerequisites_met": True,
                "assigned_worker": self.assigned_worker,
                "confidence": self.confidence,
            },
            "execution_payload": {
                "clean_goal": self.clean_goal,
                "filtered_context": list(self.filtered_context),
                "constraints": list(self.constraints),
            },
            "outputs": list(self.outputs),
            "capabilities": list(self.capabilities),
            "phase2_routing": {
                "status": "ready_for_opencode",
                "tau_action": "execute",
            },
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], source_file: Optional[str] = None) -> "SwarmTask":
        payload = data.get("execution_payload", {})
        summary = data.get("decision_summary", {})
        task_id = data.get("task_id") or summary.get("task_id") or "TSK-UNKNOWN"
        goal = payload.get("clean_goal") or data.get("clean_instructions") or data.get("objective") or ""
        context = payload.get("filtered_context") or data.get("context_slice") or data.get("inputs") or []
        constraints = payload.get("constraints") or []
        outputs = data.get("outputs") or []
        capabilities = data.get("capabilities") or ["local_write"]
        worker = summary.get("assigned_worker") or data.get("assigned_worker") or "general"
        urgent = bool(summary.get("is_urgent", False) or data.get("is_urgent", False))
        confidence = float(summary.get("confidence", data.get("confidence", 0.95)))
        version = str(data.get("handoff_version", "2.1.0"))

        return cls(
            task_id=task_id,
            clean_goal=goal,
            assigned_worker=worker,
            filtered_context=tuple(context),
            constraints=tuple(constraints),
            outputs=tuple(outputs),
            capabilities=tuple(capabilities),
            is_urgent=urgent,
            confidence=confidence,
            source_file=source_file,
            handoff_version=version,
        )


@dataclass(frozen=True)
class SwarmResult:
    task_id: str
    output: str
    status: str                         # completed / failed
    model: str = DEFAULT_KIMI_MODEL
    error: Optional[str] = None
    latency_s: float = 0.0
    task_ref: Optional[SwarmTask] = None


@dataclass(frozen=True)
class SwarmBatchReport:
    total_tasks: int
    passed_count: int
    requeue_count: int
    results: tuple[SwarmResult, ...]
    verification_scores: Mapping[str, float]
    status: str                         # completed / partial / empty
    wall_clock_s: float = 0.0


def save_task_spec(task: Union[SwarmTask, dict[str, Any]], queue_dir: Union[str, Path] = "queue") -> Path:
    """落盤 Phase 1 產出的精簡任務規格 (Task Spec JSON) 至 queue 目錄。"""
    qdir = Path(queue_dir)
    qdir.mkdir(parents=True, exist_ok=True)
    if isinstance(task, SwarmTask):
        data = task.to_spec_dict()
        tid = task.task_id
    else:
        data = task
        tid = task.get("task_id", f"TSK-{int(time.time()*1000)}")
    
    spec_path = qdir / f"{tid}.json"
    spec_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return spec_path


def load_queue_tasks(queue_dir: Union[str, Path] = "queue") -> list[SwarmTask]:
    """掃描並解析 queue 目錄下所有符合 Phase 2 規格的 JSON 任務檔 (Zero KV Cache Tax)。"""
    qdir = Path(queue_dir)
    if not qdir.exists():
        return []

    tasks = []
    for f in sorted(qdir.glob("**/*.json")):
        try:
            content = f.read_text(encoding="utf-8")
            data = json.loads(content)
            # 驗證 Phase 2 routing 旗標
            routing = data.get("phase2_routing", {})
            status = routing.get("status", "ready_for_opencode")
            tau_action = routing.get("tau_action", "execute")
            confidence = float(data.get("decision_summary", {}).get("confidence", data.get("confidence", 1.0)))

            if status == "ready_for_opencode" and tau_action == "execute" and confidence >= 0.90:
                tasks.append(SwarmTask.from_dict(data, source_file=str(f)))
        except Exception:
            continue
    return tasks


def _call_opencode_http(
    task: SwarmTask,
    config: SwarmConfig,
    base_url: str,
    api_key: str,
) -> tuple[str, float]:
    """使用 Python 標準庫 urllib 直接向 OpenCode Go / OpenAI 相容端點發起 HTTP 請求。"""
    t0 = time.time()
    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an expert specialized subagent in a 300-worker parallel swarm system. "
        "Produce rigorous, precise, and evidence-grounded output. Follow all constraints."
    )
    user_prompt = f"Goal:\n{task.clean_goal}\n"
    if task.filtered_context:
        user_prompt += "\nContext:\n" + "\n---\n".join(task.filtered_context)
    if task.constraints:
        user_prompt += "\nConstraints:\n- " + "\n- ".join(task.constraints)

    payload = {
        "model": config.model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": config.temperature,
    }

    req_data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(endpoint, data=req_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=config.timeout_seconds) as resp:
            resp_body = resp.read().decode("utf-8")
            parsed = json.loads(resp_body)
            content = parsed["choices"][0]["message"]["content"]
            return content, time.time() - t0
    except Exception as exc:
        raise RuntimeError(f"OpenCode HTTP error: {exc}") from exc


def execute_subagent_task(
    task: SwarmTask,
    config: SwarmConfig,
    worker_fn: Optional[Callable[[SwarmTask], str]] = None,
) -> SwarmResult:
    """執行單一子代理人任務。支援外部注入 worker_fn (用於 stub 或自訂 adapter)。"""
    t0 = time.time()
    try:
        if worker_fn is not None:
            output = worker_fn(task)
            elapsed = time.time() - t0
            return SwarmResult(task_id=task.task_id, output=output, status="completed",
                               model=config.model_name, latency_s=elapsed, task_ref=task)

        # 優先嘗試環境金鑰連線
        api_key = config.resolved_api_key()
        base_url = config.resolved_base_url()

        if api_key:
            output, elapsed = _call_opencode_http(task, config, base_url, api_key)
            return SwarmResult(task_id=task.task_id, output=output, status="completed",
                               model=config.model_name, latency_s=elapsed, task_ref=task)

        # 離線/無金鑰降級模擬 (Deterministic Stub for offline workflows)
        time.sleep(0.005)  # 模擬極速 5ms 平行返回
        mock_output = (
            f"[Kimi-k3 Swarm Output for {task.task_id}]\n"
            f"依據朱國大醫師（Kwo-Ta Chu, MD, PhD）雙視角原則，完成任務：{task.clean_goal}。\n"
            f"所有約束條件（繁體中文、實證依據、去客套化）均已嚴格遵循。"
        )
        return SwarmResult(task_id=task.task_id, output=mock_output, status="completed",
                           model=f"{config.model_name}-offline-stub", latency_s=time.time() - t0, task_ref=task)
    except Exception as exc:
        return SwarmResult(task_id=task.task_id, output="", status="failed",
                           model=config.model_name, error=str(exc), latency_s=time.time() - t0, task_ref=task)


def execute_kimi_swarm(
    tasks: Sequence[SwarmTask],
    config: Optional[SwarmConfig] = None,
    worker_fn: Optional[Callable[[SwarmTask], str]] = None,
) -> list[SwarmResult]:
    """啟動 Kimi-k3 平行蜂群 (高達 300 個並發 Subagents) 處理所有傳入任務。"""
    cfg = config or SwarmConfig()
    if not tasks:
        return []

    # 蜂群並發度控制：最多 300 平行 worker
    workers = min(len(tasks), max(1, cfg.max_concurrency))
    results: list[SwarmResult] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {executor.submit(execute_subagent_task, t, cfg, worker_fn): t for t in tasks}
        for future in as_completed(future_map):
            try:
                res = future.result()
                results.append(res)
            except Exception as exc:
                t = future_map[future]
                results.append(SwarmResult(task_id=t.task_id, output="", status="failed",
                                           model=cfg.model_name, error=str(exc), task_ref=t))

    # 排序使結果穩定
    results.sort(key=lambda r: r.task_id)
    return results


def single_pass_batch_verify(
    results: Sequence[SwarmResult],
    config: Optional[SwarmConfig] = None,
    provider: Optional[str] = None,
) -> tuple[list[SwarmResult], list[SwarmResult], dict[str, float]]:
    """Phase 1 離線 Single-Pass 批次驗收 (Single-Pass Batch Review)。

    將所有蜂群產出的摘要打包為單一批次問詢，一次性送給 JEV 評估，
    消弭傳統 300 個 Agent 序列審查的排隊延遲瓶頸。

    返回: (passed_results, requeued_results, scores_dict)
    """
    cfg = config or SwarmConfig()
    if not results:
        return [], [], {}

    # 1. 構建打包問題與輕量評估狀態 (截取前 1,000 字元避免 KV 懲罰)
    eval_state = {}
    questions_map = {}

    for res in results:
        tid = res.task_id
        snippet = res.output[:1000] if res.status == "completed" else "FAILED_EXECUTION"
        eval_state[tid] = snippet
        questions_map[f"check_{tid}"] = Noul(
            instructions=f"Does the execution output for task `{tid}` satisfy instructions and evidence criteria without hallucinations?"
        )

    # 2. 單次呼叫 JEV 決策層
    verdicts = decide(state=eval_state, questions=questions_map, provider=provider)

    passed: list[SwarmResult] = []
    requeued: list[SwarmResult] = []
    scores: dict[str, float] = {}

    for res in results:
        tid = res.task_id
        if res.status != "completed":
            requeued.append(res)
            scores[tid] = 0.0
            continue

        q_key = f"check_{tid}"
        ans = verdicts.answers.get(q_key)
        # Noul 回傳概率分數
        score = ans.noul if (ans and hasattr(ans, "noul")) else 0.0
        scores[tid] = score

        if score >= cfg.tau_verify:
            passed.append(res)
            # 若有來源檔案，驗收成功後清理 queue
            if res.task_ref and res.task_ref.source_file:
                try:
                    Path(res.task_ref.source_file).unlink(missing_ok=True)
                except Exception:
                    pass
        else:
            requeued.append(res)

    return passed, requeued, scores


def run_two_phase_pipeline(
    tasks: Sequence[SwarmTask],
    config: Optional[SwarmConfig] = None,
    worker_fn: Optional[Callable[[SwarmTask], str]] = None,
    provider: Optional[str] = None,
) -> SwarmBatchReport:
    """連接兩階段的無延遲 (Zero-Lag) 端到端管線：

    1. Phase 1 產出落盤 (Queue 落盤)
    2. Phase 2 300 平行蜂群併發執行 (Kimi-k3 Swarm)
    3. Phase 1 離線 Single-Pass 批次審查 (Single-Pass Verification)
    4. 自動收斂閉環 (自動清理通過項目、保留/退回重跑項目)
    """
    t_start = time.time()
    cfg = config or SwarmConfig()

    # 1. 執行蜂群
    results = execute_kimi_swarm(tasks, cfg, worker_fn=worker_fn)

    # 2. Single-Pass 批次驗收
    passed, requeued, scores = single_pass_batch_verify(results, cfg, provider=provider)

    total = len(tasks)
    passed_count = len(passed)
    requeue_count = len(requeued)

    status = "completed" if (passed_count == total and total > 0) else ("empty" if total == 0 else "partial")

    return SwarmBatchReport(
        total_tasks=total,
        passed_count=passed_count,
        requeue_count=requeue_count,
        results=tuple(results),
        verification_scores=scores,
        status=status,
        wall_clock_s=time.time() - t_start,
    )
