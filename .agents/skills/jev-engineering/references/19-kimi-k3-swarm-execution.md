# 19 — Kimi-k3 300 平行蜂群執行與無延遲跨階段接軌

Phase 2 執行階段透過 **OpenCode Go** 平台的標準 OpenAI 相容 API 介面調用 `kimi-k3` 超長脈絡（1M Context）、高性價比模型，啟動高達 300 個並發 Subagents 蜂群平行處理 Phase 1 派發之任務規格，並透過 **JEV Single-Pass 批次驗收** 實現兩階段零延遲（Zero-Lag）閉環收斂。

---

## 一、 核心架構與無延遲接軌機制 (Zero-Lag Bridge Architecture)

傳統多代理人系統常見的效能瓶頸在於：
1. **重載對話歷史引起的 KV Cache Tax**：回傳至大模型時重複解析數萬 token，導致 80% 以上成本浪費於非生成判斷。
2. **序列排隊審查延遲 (Serial Queue Latency)**：若蜂群平行產出數百個結果，卻在驗收時一個接一個排隊調用大模型審核，產生數分鐘的無謂等待。

本模組透過四重解耦徹底消弭延遲：

```
[Phase 1: High Planner (Opus 5.5 / GPT-6 Astra / Sol-high)]
                      │
                      ▼ (純決策 / 零文字生成 / <300 tokens)
         [寫入 ./queue/{task_id}.json]  <-- 零歷史上下文負擔 (Zero KV Cache Tax)
                      │
                      ▼ (無延遲平行拉取)
[Phase 2: OpenCode Go Kimi-k3 蜂群 (高達 300 個並發 Subagents)]
    ├── Worker 001 (文獻實證檢索)
    ├── Worker 002 (代碼重構與單元測試)
    └── Worker 300 (動力學流形分析)
                      │
                      ▼ (輸出至記憶體/檔案，耗時取決於最長子任務)
[JEV Single-Pass 批次驗收 (Single-Pass Batch Review)]
    └── 一次性將 300 項產出摘要打包為單一 State，150ms 內完成整體審查
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
[通過 (Score >= 0.85)]       [未通過 (Score < 0.85)]
自動移出 queue，產出核可      保留於 queue，供下輪定向微調重跑
```

---

## 二、 環境變數與端點設定 (Environment & Endpoint)

OpenCode Go 提供標準的 OpenAI-compatible REST API 端點，支援透過環境變數無縫接入：

| 環境變數 | 預設值 | 說明 |
|---|---|---|
| `OPENCODE_API_KEY` | (優先讀取) 或 `OPENAI_API_KEY` | OpenCode Go 平台存取憑證 (Bearer token) |
| `OPENCODE_API_URL` / `OPENCODE_BASE_URL` | `https://api.opencode.ai/v1` | OpenCode Go API Base URL (支援如 `http://localhost:8080/v1`) |
| `KIMI_MODEL_NAME` | `kimi-k3` | 指定呼叫之 Kimi-k3 模型名稱 |
| `JEV_PROVIDER` | `llm` (或 `typesafe`, `local`, `stub`) | JEV 決策層之後端提供者 |

無金鑰離線模式下，`execute_kimi_swarm()` 自動切換至高保真 Deterministic Stub 模式，確保本機測試與 CI/CD 流程能以 0 成本、毫秒級速度完整走通。

---

## 三、 Python API 介面

所有蜂群執行元件封裝於 `assets/jev/swarm.py`，遵循 Python 3.9+ 標準庫實作（stdlib-only，無強迫外部 pip 套件）：

```python
from jev import (
    SwarmConfig, SwarmTask, execute_kimi_swarm,
    single_pass_batch_verify, run_two_phase_pipeline,
    load_queue_tasks, save_task_spec,
)

# 1. 配置蜂群參數 (支援至 300 並發)
config = SwarmConfig(
    max_concurrency=300,
    model_name="kimi-k3",
    tau_verify=0.85,
    timeout_seconds=60.0,
)

# 2. 讀取 Phase 1 寫入 queue 的任務規格 (完全不帶對話歷史)
tasks = load_queue_tasks("queue")

# 3. 啟動兩階段無延遲端到端管線
report = run_two_phase_pipeline(tasks, config=config)

print(f"總任務數: {report.total_tasks}")
print(f"通過數量: {report.passed_count}")
print(f"退回重跑數量: {report.requeue_count}")
print(f"整體耗時: {report.wall_clock_s:.3f} 秒")
```

---

## 四、 JEV Single-Pass 批次驗收機制

為解決 300 個 Subagents 回傳後的序列等待瓶頸，`single_pass_batch_verify()` 採用單次問詢打包：

1. **狀態精簡 (State Compaction)**：僅截取每個任務產出的前 1,000 字元與核心數值，建構為 `eval_state = {task_id: snippet}`。
2. **多題並發問詢 (Batched Questions Map)**：為每個任務構建專屬 `Noul(instructions="...")`。
3. **單次呼叫 JEV**：調用 `decide(state=eval_state, questions=questions_map)`，在單次來回中完成 300 項任務之真實性、無幻覺與約束符合度判定。
4. **自動收斂閉環 (Auto-Convergence Loop)**：
   - 得分 $\ge 0.85$ 之任務自動自 `./queue/` 清除或移至成品區。
   - 得分 $< 0.85$ 之任務保留於 `./queue/`，下輪僅重跑失敗項目，避免已完成項目重複消耗算力。

---

## 五、 角色規範與朱國大醫師人設對齊

在 Phase 2 產出醫學與計算神經科學相關內容時，必須依循以下全域準則：
- **雙重視角結合**：結合腎臟科臨床實務與動態神經網絡模擬（STN-GPe、LIF 模型、FORCE 演算法）。
- **校準之不確定性陳述 (Hedging Calibration)**：使用「應該」、「可能」、「不見得」、「高度相關」、「其實」等審慎詞彙；嚴禁主觀斷言「我認為」。
- **專業尊稱**：一律使用「您」，禁用非正式代詞。
- **繁體中文輸出**：學術報告與分析一律採用繁體中文（Traditional Chinese），代碼與技術識別碼保留英文。
