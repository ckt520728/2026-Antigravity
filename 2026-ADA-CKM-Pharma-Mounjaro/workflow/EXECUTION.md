> **2026-10-31 現況更新**：使用者已於台北 2026-10-30 核准 v0.2-review outline，SHA-256 `2d499d07f1deb4ac92d48c074618e5152b19c322ee44c5c45158957713953b11`。本輪依 finish goal 授權進行免費本機 HTML／可編輯 PPTX／DOCX／blog 草稿／motion 影片製作與獨立驗收；不含發布、上傳、付費生成或部署。下文 pending／不派發／初始化描述保留為歷史階段。核准見 [approval](approval.json)，production queue 見 [production tasks](production-tasks.json)。自動 JEV routing_ready=false；host 手動 medium 分工另記。原 prompt 與歷史 baseline 不同，差異保留於 input-change-20261031.json；不得宣稱 36 檔全同。

# JEV 真實執行與恢復紀錄

日期：2026-10-29（Asia/Taipei）。結論：host 手動配置的 T1／T2 executors 已啟動並留下檔案，但先前執行中斷；本輪恢復 T1。Python JEV 維持 fail-closed，沒有 ready、production dispatch 或完整 live middleware 證據。T3 仍待主控獨立驗收，outline approval 為 pending。

## 計畫與驗證界線

1. 讀回根規則、交接、TaskSpec 與實際檢查程式 → 核對寫入限於 T1 初始化範圍 → 路徑超界或需改 vendor 時停止。
2. 執行原始 local scorer／ToolGate 與 adapter 停止檢查 → 保留原始 confidence、ask、deny、零 executor 呼叫 → 不下修 confidence 門檻、不造 ready。
3. 寫本紀錄後跑 validator → 核對 YAML、TaskSpec、連結、來源 hash、pin、approval → T2 缺檔如實標 pending，交主控後續重跑，不替代 T3 clinical readback。

## Host 手動配置與恢復

主控提供的配置記錄：先前 T1／T2 各由 `gpt-6.1-sol`、`reasoning_effort=medium`、`fork_turns=none` 執行；turn transition 後 live agent inventory 不再有原 agents，因此不可據其先前啟動或已落盤檔案宣稱兩任務完成。本輪 T1 恢復使用主控明確配置的同模型 medium executor；T2 由另一個恢復 executor 處理。

這是 host 受限手動派工，不是 `plan_phase` 自動選模或 `execute_phase` 已執行工作的證據。實際 provider usage 與完整費用未暴露。`tasks.json` 的 T1 14000／T2 18000／T3 6000 為宣告 output budget，API token cap 未取得 enforce 證據；不得以 YAML 的 `model: sonnet` 或 vendor registry 推定本次模型。

## 本輪實跑

工作目錄：`D:\2026 ADA_CKM_Pharma`。一次性命令：

```powershell
python -X utf8 monjaro/workflow/run_jev_checks.py
```

exit code：0。原始結果時間：`2026-10-29T00:45:14.937961+00:00`（台北 08:45:14）。命令已結束，未啟動長駐服務；工具未回傳 process PID，不補造 PID。副作用僅更新 [jev-checks.json](jev-checks.json)。檢查中的 Write／WebFetch／危險 Bash 僅分類，沒有執行副作用。

| 實際檢查 | 結果與證據範圍 |
|---|---|
| local `decide` 六題（T1/T2/T3 tier 與 data） | 六個 confidence 均 `0.3`；`provider=local`，不是 live API；原始分布保留於 JSON。 |
| ToolGate Read／Write／WebFetch | 均 `ask`、confidence `0.0`；原因為 `TypeError: expected string or bytes-like object`，fail to ask。 |
| ToolGate `git push --force` | deterministic rule `deny`、capability `destructive`、confidence `1.0`；未執行 git。 |
| `plan_phase`／`execute_phase` | 均 `ask`；缺可驗證 host high model adapter 及實際 token usage。 |
| callback 計數 | planner_adapter `1`，executor／verifier／tool_runner 均 `0`。 |
| 派發狀態 | `routing_ready=false`、`production_dispatched=false`。 |

上游 local provider 對 dict state 的呼叫曾產上述 TypeError。直接 `decide` 改傳 JSON string 後可實跑，ToolGate 內部仍傳 dict，因此其錯誤如實保留。vendor 未修改，未用高分 stub 或假的 PlannerResult 取代；missing planner callback 明確拋 WorkflowStop，只驗證停止界線。

local scorer 自報 input/output tokens 為零；這不涵蓋 host planner、executor、context 或工具費用。未量測 token savings，未核實 vendor 價格或 model metadata，不宣稱 OpenCode、Kimi、300 蜂群、完整成本或效能提升。

## 讀回與可追溯參照

| 檔案 | 本次 SHA-256 |
|---|---|
| [tasks.json](tasks.json) | `bf7bb0d2a2e95ef6ee9db66e3e6a1a10ca099de3bf480b31bafb9603eb75a891` |
| [run_jev_checks.py](run_jev_checks.py) | `737a1b51c77c9a2fdb27cbc1397ea9524d734480aaf8b47c276e79c7f47c6437` |
| [jev-checks.json](jev-checks.json) | `1ceea7d5948d1bd46986866198470454ee5a8813decb9297c53d42bab73460ee` |
| [preservation-baseline.json](preservation-baseline.json) | `142387d74af973dc25da1d888bc6320fd4157916b857c64ef9090707e4d55ef5` |
| [source-pin.json](source-pin.json) | `999bccbb94a3a1571685014be543505e703a3868abedd9f38b827befc8ceb4d4` |

本輪只將 `run_jev_checks.py` 內錯誤的 host「完成」字樣改成「啟動、恢復、待驗收」，未改 routing、閾值或 vendor。來源保護與 pin 的逐檔重算以 [validation-results.json](validation-results.json) 為準；後續重新執行 checks 將更新時間及 JSON hash，須同步本紀錄。

驗證命令：`python -X utf8 monjaro/workflow/validate_project.py`。結果另存同目錄；任何 T2 尚未落盤產物皆是 pending，不能以 T1 結構測試宣稱 clinical claims 已驗收。主控需在 T2 補齊後重跑並完成 T3，才交使用者審閱 outline。未核准前不進 T4。
