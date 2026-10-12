# Jev-Engineering 平行 Subagent Swarm 在 Antigravity 環境之落地實作指南

> **建立日期**：2026-10-12  
> **系統架構**：Google Antigravity / Multi-Agent Swarm / Jev Engineering v1.2  
> **目標倉庫**：`https://github.com/ckt520728/2026-Antigravity`  
> **知識庫存檔**：`G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\`  

---

## 1. 核心理念：為何需要 Jev-Engineering 兩階段蜂群？

傳統的大型語言模型（LLM）單一代理人（Single Agent）架構存在兩大痛點：
1. **Context 膨脹與 KV Cache 稅 (The KV Cache Tax)**：
   讓單一 Agent 處理整套研究，對話歷程會迅速累積至數萬乃至數十萬 tokens。每次工具呼叫往返都需要重建整個 KV Cache，造成延遲呈指數上升、API 費用暴增。
2. **算力錯配與發散風險**：
   使用最高階模型（如 Opus / Pro）去進行廉價的文字格式排版、表格轉換或重複資料抓取；一旦執行出錯，高階模型容易在同一個 context 中過度修正而陷入幻覺。

**Jev-Engineering v1.2 的解法：嚴格兩階段分離（Two-Phase Separation）**：
```text
  【Phase 1: High Planner (高階決策)】
  輸入使用者需求 ──> 深度推理解構 ──> 產出結構化任務規格 (Task DAG)
  ★ 鐵律：只讀取來源、定義驗收準則；嚴禁撰寫最終代碼、文章或 patch！
                        │
                        ▼
  【Phase 2: Parallel Subagent Swarm (平行蜂群執行)】
  主控透過 Antigravity 並發派發任務（每個 Worker 享有乾淨獨立 Context）：
     ├─► Worker 1 (Medium Executor, Flash): 執行調控基因體分析 (AlphaGenome)
     ├─► Worker 2 (Medium Executor, Flash): 執行文獻與臨床致病性探勘 (PubMed / ClinVar)
     ├─► Worker 3 (Medium Executor, Flash): 執行蛋白質結構比對 (AlphaFold / Foldseek)
     └─► Worker 4 (Low Executor, Flash-Lite): 輕量資料提取與 BibTeX 引用排版
                        │
                        ▼
  【客觀獨立驗收 (Independent Acceptance)】
  各 Worker 僅回傳成品檔案參照與驗收證據，主控彙整驗收，完成整個研究工作流！
```

---

## 2. Google Antigravity 原生 Subagent Swarm 架構

在 Google Antigravity 中，我們將 Jev 角色正式定義為具體的可呼叫 Subagent，並透過 Antigravity 的底層原生並發工具實現平行蜂群調度：

### 2.1 已註冊的 Jev 角色清單

| 角色名稱 (TypeName) | 權限模式 | 推薦模型層級 (Tier) | 核心任務與職責 |
| :--- | :--- | :--- | :--- |
| **`jev-planner`** | 唯讀 (Read-only) | High (`pro` / inherit) | 需求剖析、依賴拓撲分析、制定包含 `task_id`、`objective`、`inputs`、`outputs`、`acceptance` 的 JSON 規格。不持有檔案寫入工具。 |
| **`jev-executor-medium`** | 寫入與執行 (Full Write) | Medium (`flash`) | 承接具體多步驟任務（如執行 Python 分析腳本、生成特定模組代碼、撰寫章節），並進行自我驗收。 |
| **`jev-executor-low`** | 寫入與執行 (Full Write) | Low (`flash_lite`) | 承接快速、輕量之單元任務（資料抽取、格式轉換、BibTeX 整理、摘要微調），極速且成本極低。 |

---

## 3. 平行蜂群派發範例 (How Antigravity Invokes the Swarm)

主控 Agent 可透過 `invoke_subagent` 工具，在**單一次工具呼叫中同時發射多個 Subagent**：

```json
{
  "Subagents": [
    {
      "TypeName": "jev-executor-medium",
      "Role": "Genomics Variant Analyst",
      "Prompt": "執行 task-1：使用 AlphaGenome 分析變異株 chr9:128225994:G>A，輸出 AVI 分數與剪接特徵權重至 results/alphagenome_chr9.json，並驗證結果。",
      "Model": "flash",
      "Workspace": "inherit"
    },
    {
      "TypeName": "jev-executor-medium",
      "Role": "ClinVar Evidence Researcher",
      "Prompt": "執行 task-2：查詢 ClinVar 與 dbSNP 關於該變異株之臨床評級與人群頻率，輸出至 results/clinvar_chr9.json。",
      "Model": "flash",
      "Workspace": "inherit"
    },
    {
      "TypeName": "jev-executor-low",
      "Role": "Literature Citation Formatter",
      "Prompt": "執行 task-3：自 PubMed 檢索該基因近期 3 篇文獻，將 PMID 轉為標準 BibTeX 格式存於 references.bib。",
      "Model": "flash_lite",
      "Workspace": "inherit"
    }
  ]
}
```

### 工作區隔離模式 (`Workspace`)：
- **`inherit`**：共享同一個工作目錄（適合各 worker 產出不同檔名的場景）。
- **`branch`**：由 Antigravity 自動為各 worker 建立獨立 Git 分支，防止並行修改衝突。
- **`share`**：使用類似 Git worktree 的共享倉庫架構。

---

## 4. 如何在日常對話中使用 Jev 蜂群？

現在你在 Antigravity 的對話介面中，可以用以下方式直接指示 Agent 啟動 Jev 工作流：

### 提示詞範例 1：全自動兩階段研究專案
> 「請依照 Jev-Engineering 兩階段工作流：先由 `jev-planner` 規劃本次 APOL1 腎病基因研究的任務 DAG 與驗收條件，規劃完成後，立即啟動平行 Subagent Swarm 由 `jev-executor-medium` 與 `low` 分別同時處理變異預測、文獻檢索與引用整理。」

### 提示詞範例 2：多篇論文或文獻批次分析
> 「我有 5 篇重要文獻需要精讀，請派發 5 個平行 `jev-executor-medium` Subagent 分別閱讀並萃取各自的創新點、限制與臨床意涵，最後由主控統整。」

### 提示詞範例 3：搭配 Antigravity 斜線指令
- 你可以直接在聊天視窗鍵入 `/teamwork-preview`，啟動 Antigravity 團隊協作預覽功能。
- 鍵入 `/plan`，讓系統在執行前先進入結構化嚴謹規劃模式。
