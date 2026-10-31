> **2026-10-31 現況更新**：使用者已於台北 2026-10-30 核准 v0.2-review outline，SHA-256 `2d499d07f1deb4ac92d48c074618e5152b19c322ee44c5c45158957713953b11`。本輪依 finish goal 授權進行免費本機 HTML／可編輯 PPTX／DOCX／blog 草稿／motion 影片製作與獨立驗收；不含發布、上傳、付費生成或部署。下文 pending／不派發／初始化描述保留為歷史階段。核准見 [approval](approval.json)，production queue 見 [production tasks](production-tasks.json)。自動 JEV routing_ready=false；host 手動 medium 分工另記。原 prompt 與歷史 baseline 不同，差異保留於 input-change-20261031.json；不得宣稱 36 檔全同。

# JEV 兩階段執行契約

日期：2026-10-29。結論：本輪已實際依 host 的結構化分工啟動 medium executor；Python JEV 自動模型派發尚未接線。兩者分開留證，不能互相冒充。

## 計畫、驗證與停止條件

1. 盤點原始 prompt、舊規則、JEV 與 SOIL → 驗證原始 bytes SHA-256／TaskSpec 欄位 → 缺來源、路徑超界或發現舊案授權混用時停止。
2. medium executors 依分工分別建立初始化與證據／outline → 主控讀回 YAML／claim／outline／8 capabilities 與保護來源 hash → 未核准 outline 時不進最終製作。
3. 實跑 JEV local scorer、ToolGate、plan_phase／execute_phase 邊界 → 保存原始 probability／confidence／ask 原因，確認 blocked executor 不會呼叫 → 不得修改分數或補造使用量。
4. 主控獨立驗收 T1/T2 → 讀回成品與 validator 結果 → 失敗回傳 task ID／檔案參照／精簡錯誤及已完成副作用，重新規劃，不盲目重做。

## 控制資料

[tasks.json](tasks.json) 保存 T1 初始化、T2 證據與大綱、T3 獨立驗收、T4 核准後另拆 production。T1/T2 輸出互斥，可以由 host 分別配置；T3 依賴兩者；T4 依賴 T3 且有額外未滿足的 outline approval gate。本輪 active queue 只有 T1/T2/T3；T4 為 backlog，不能送 execute_phase。

Phase 1 planner 只讀規劃必要來源，回傳 TaskSpec；不產文章、程式、patch 或最終答案。Phase 2 executor 由 host 指定 model／effort／scope／token cap，僅接自己的必要輸入與依賴參照。YAML 自訂 agent 是工具與行為設定，不是模型執行證明。

本輪 `max_output_tokens` 是 host manifest 宣告預算（T1 14000、T2 18000、T3 6000），`budget_enforcement=not_exposed`；沒有 API 硬限制證據。Python 結構測試顯式配置 Limits(max_worker_output_tokens=18000, max_total_output_tokens=50000)，不把這些任務硬塞入預設 4096，亦不表示已 ready。

## Python 套件與 adapter

原始 JEV stdlib package 位於 [vendor/jev](vendor/jev)，原始 skill 位於 [vendor/local/SKILL.md](vendor/local/SKILL.md)，原始兩階段介面位於 [vendor/local/references/18-two-phase-workflow.md](vendor/local/references/18-two-phase-workflow.md)。[source-pin.json](source-pin.json) 包含每個來源檔 SHA-256 與直接 GitHub bytes pin；未宣稱 main 是固定 commit。

`plan_phase(request, planner_adapter, registry, data_class, limits, provider)` 需要真正 high planner adapter，回報實際 model key／tokens；`execute_phase(plan, executor_adapter, verifier, tool_runner, approve)` 需要 host 模型派發、sandbox 與獨立 artifact verifier。每次 executor tool call 必須走 `ExecutionContext.call`。Python callback 本身不是 sandbox。

本輪未取得能從 Python 呼叫 host high／medium 模型並回報真實 token usage 的 adapter，也沒有確認 JEV paid API 設定或額外費用授權。因此 [run_jev_checks.py](run_jev_checks.py) 不製造 PlannerResult／Model／confidence，而是：

- 以真正 local provider 批次 `decide()` T1/T2/T3 所需 tier／data，保存全部原始分布及 confidence；它不是 live JEV API。
- 以真正 ToolGate 檢查具體 Read／Write／WebFetch／危險 Bash，但不執行其副作用；保存 gate 結果。
- 呼叫真實 `plan_phase`，由 missing host adapter 明確丟 WorkflowStop，保留 ask；再呼叫 `execute_phase`，驗證它不會啟動 executor、verifier 或 tool runner。
- 以 package 原始 TaskSpec checker 驗證 active queue 的 tuple／依賴／輸出互斥／預算；T4 backlog 另做結構檢查而不派發。

這是實際接線邊界與 local scorer 檢查，不是 stub routing，也不是已完成的自動兩階段生產。host 受限派發的 T1/T2 產物由主控另外獨立驗收；其真實模型證據屬 host 配置記錄，不從 vendor models.json 推導。

## 授權與觀測

八類 capability、授權與資料政策以 [根規則](../../AGENTS.md) 為準。`approve` callback 只可對具體工具及參數代表已存在且涵蓋該動作的人工授權；不能以固定 true 代替。other、費用、外部發布、私有資料外送不可自動核准；gate 故障 fail to ask。

低信心維持原值。不得以 local confidence 冷啟動為由下修門檻、寫假校準資料或註冊高分 stub。上游 models.json 的模型 ID／價格／swarm 只是來源資料，未做 live 查核，不作真實呼叫與節省費用的依據。

每次交接記錄：task ID、artifact refs、來源／產物 hash、執行命令、actual status、完成副作用、失敗原因、pending approvals。不能宣稱沒有記錄的 full costs、token savings、效能提升、OpenCode／Kimi 或 300 蜂群。
