# T3 主控獨立驗收

日期：2026-10-30（Asia/Taipei）  
結論：**T1／T2／T3 通過「交付使用者審閱 outline」的驗收；這不是 outline 核准，也不是 T4 製作或發布授權。** `outline_approval.status` 仍為 `pending`。

## 1. 驗收範圍與實際分工

主控依 `AGENTS.md`、`handoffs.md`、TaskSpec 與 JEV 契約，獨立讀回 T1／T2 產物、執行 validators、抽核 primary sources 與檢查 SOIL 頁面。沒有把 executor 自報 completed 當作驗收。

使用者要求 Kimi K3 平行處理後，host model inventory 實際回傳 `opencode-go/kimi-k3`、variant `max`。曾執行 3 個唯讀稽查 sessions：

- 結構／JEV：`ses_e7ac86fdbffeuwsi4wiwqzpHlY`
- 臨床證據：`ses_e7ac86fd8ffeszZYldv3YCaHzP`
- SOIL outline：`ses_e7ac86fd6ffeDoOxELA9n5QacA`

三份唯讀稽查均完成並指出 T2 缺件。其後證據與 outline 兩個 production continuations 都回 `Go usage limit exceeded`；outline 留有一份部分寫入檔，證據產物未生成。主控接續補齊、修正與驗收，**不宣稱 Kimi production swarm 已完成，也不另行呼叫 subagent**。以上為 host 手動分工，不是 JEV automatic routing；host token usage／完整費用未暴露。

## 2. T1 結構與 JEV 驗收：PASS

- Agent YAML frontmatter 可解析；必要欄位、合法 tools、`model: sonnet`、`permissionMode: default` 均通過。
- 根規則與 agent 均含 8 capabilities；TaskSpec 欄位、依賴、唯一輸出與預算檢查通過；未知 capability、不存在依賴、重複輸出均會被拒絕。
- 最新 `jev-checks.json`：6 個 local confidence 均 0.3；Read／Write／WebFetch 因真實 TypeError 保持 ask；危險 Bash deny；`plan_phase`／`execute_phase` 均 ask；planner callback=1，executor／verifier／tool_runner=0；`routing_ready=false`、`production_dispatched=false`。
- 這是 vendored local scorer／fail-closed 邊界，不是 live model adapter、完整 middleware 或 production dispatch。
- 36 個 preservation-baseline 檔案與 21 個 JEV source-pin 檔案的 SHA-256 全部相符；舊研究與 canonical ZIP 未改變。
- 先前 auditor 回報的 `jev-checks.json` hash 斷鏈發生在主控重跑與平行讀取期間。最終已以最新一次實際輸出重新計算並同步 `EXECUTION.md`，未以修改 hash 掩飾來源差異。

## 3. T2 證據鏈驗收：PASS（保留明示限制）

### 產物與關聯

- 9 項 T2 宣告產物全部存在；`source_registry.json/.csv` 均為 27 個唯一 sources，`claim_ledger.csv` 為 24 個唯一 rows（C001–C021、P001–P003）。
- 所有 claim→source IDs 均存在；所有 registry 非空 local paths 均存在；ZIP 7 個 extracted entries 與兩份 USPI 的 SHA-256 均與 manifests 相符。
- NotebookLM 實際唯讀取得 45-source inventory，並成功讀取 SURPASS-2、SURMOUNT-5、SUMMIT、STEP-HFpEF DM 四篇 original text；未把 NotebookLM AI 回答當 primary evidence。
- S06 期刊日／PubMed 收錄日與 S12 DOI／卷期已補；S11 UK IFU 因 webfetch 不支援 PDF、直接 GET 403，已降 pending。C018 改由實際核讀的美國 USPI §2.2／3／5.10 支持，未沿用未核實 UK 內容。

### 主控臨床抽核

| Claims | 主控實際核對 | 判定 |
|---|---|---|
| C001／C002 | Mounjaro USPI pp.1、3–6、10–11；Zepbound USPI p.1；SURMOUNT-5 Introduction | 分類與品牌適應症正確；USA-only 邊界保留。 |
| C003 | TFDA 2025-11-10 公告第一點 | 只支持概括用途，不作完整台灣仿單／給付依據。 |
| C004 | SURPASS-2 PubMed＋NotebookLM original text pp.503–515 | N、40 週、sema 1 mg、HbA1c 百分點與族群一致。 |
| C005 | SURMOUNT-5 original text Abstract／Methods／Tables | 無 T2D、72 週、劑量、−20.2% vs −13.7% 與 estimand 一致。 |
| C006／C007 | SUMMIT、STEP-HFpEF DM original text | 複合終點與 CV death 分界、KCCQ／體重終點及 LVEF 族群一致。 |
| C008／C009／C010 | PubMed 38785209／41406444／42114520 | FLOW 藥物歸屬與腎複合、CVOT 非劣／優越性、2026 腎探索性層級一致。 |
| C011–C018 | Mounjaro USPI 對應段落 | 劑量、禁忌、AKI、併藥、避孕、麻醉、警訊與 KwikPen 邊界一致；均標 USA-only。 |
| C019 | PubMed 38078870 | 783 lead-in、670 隨機、36–88 週 −5.5% vs +14.0% 一致；維持 abstract-level 限制。 |

未將 association 寫成 causation；未把 FLOW 外推 tirzepatide，未把 SUMMIT 複合終點寫成 CV death 單獨獲益，未混用 semaglutide 1 mg 與 1.7／2.4 mg。二手素材的拆筆／跳級／拼筆／採購與過度機制推論均明確排除。P001–P003 維持 pending。

## 4. SOIL 與 production brief 驗收：PASS（供審閱）

- `slide_outline.md` 為 v0.2-review，共 P01–P26 連續 26 頁；每頁都有標題／核心訊息／視覺策略／素材來源。
- SOIL 六引擎齊全：One Big Idea、Hook、分段 take-home、認知負荷控制、house style、P06／P14 Check-Points。
- 使用 C001–C020，全部能在 ledger 找到且 verification 屬允許類別；pending 的法規／給付／metadata 均標 `[TO CONFIRM]`。
- `production_brief.md` 只規劃 motion／document／HTML／PPTX／blog 的輸入、依賴、授權與獨立驗收，未派發或生成成品。

## 5. 最終指令與 gate

2026-10-30 實際執行：

```powershell
python -X utf8 monjaro/workflow/run_jev_checks.py
python -X utf8 monjaro/workflow/validate_project.py
```

最新 JEV timestamp：`2026-10-29T16:46:57.933914+00:00`（台北 2026-10-30 00:46:57）。Validator **17／17 checks passed**，包括 T1／T2 成品、全部本地 Markdown links、36 個 baseline hashes、21 個 pins、JEV ask／零 executor、outline pending 與 production 未派發。

另以主控一次性檢查確認：27 sources、24 claims、26 頁四要素、claim/source 關聯、本地路徑、允許的 claim statuses 與 pending gate 全數通過。

## 6. 交付審閱的版本

- Outline：`monjaro/specs/slide_outline.md`
- 版本：`v0.2-review`
- SHA-256：`2d499d07f1deb4ac92d48c074618e5152b19c322ee44c5c45158957713953b11`
- 核准狀態：**pending**。只有使用者對此版本／hash（或其後明確指定的新 hash）表示核准，才可記錄 approval 並另拆 T4；不得把本次交付、沉默或舊案授權視為核准。
