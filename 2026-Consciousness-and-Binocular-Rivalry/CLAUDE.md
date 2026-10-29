# CLAUDE.md — 2026 Consciousness and binocular rivalry

本檔為 Claude Code 與所有 agent 在本專案的共同規則。`AGENTS.md`（OpenCode / Kimi K3）必須與本檔一致；若衝突，以本檔為準並回報。

## 1. 專案目標

研究 Doris Tsao 實驗室 2026 年 10 月發表的預印本（bioRxiv，Hesse et al. 2026）：意識與雙眼閃光抑制（binocular flash suppression，雙眼競爭 binocular rivalry 的變體）的關鍵發現、方法與意涵。面向一般讀者，產出四種成品：

- 動態解說影片 motion-explainer video（zh-TW）
- HTML 簡報 HTML deck（zh-TW）
- PowerPoint 簡報 PPTX（English）
- 個人首頁部落格文章 blog（zh-TW）

## 2. 資料夾地圖

| 路徑 | 用途 |
|---|---|
| `2026 Consciousness and binocular rivalry.txt` | 原始目標（goal）與工作流程說明 |
| `research/raw/` | 原始來源與摘要（ground truth），含 `nlm_status.md`、`web_*.md`、Hesse 2026 全文摘要 |
| `research/01_notes_inventory.md` … `research/08_qa_report.md` | Phase 1 產出（01–08） |
| `research/09_fix_log.md`、`research/06_fact_sheet_README.md` | Phase 1 修正紀錄（QA 修正與 F40 恢復）；事實表欄位與 status 說明 |
| `research/05_glossary.csv` | zh-TW 術語表（台灣用語的唯一依據） |
| `research/06_fact_sheet.json` | 事實來源（77 筆，每筆有 id 與 status） |
| `phase2/00_brief/` | Phase 2 brief；`style_refs/` 放風格參照 |
| `phase2/video/`、`phase2/html_deck/`、`phase2/pptx/`、`phase2/blog/`、`phase2/qa/` | Phase 2 成品，各自一個資料夾 |
| `.claude/skills/` | skills（路徑見第 6 節） |
| `handoffs.md`、`task_manifest.json` | Phase 2 交接與任務清單（尚未建立，由主控建立） |

`research/` 為 Phase 1 唯讀成果：Phase 2 不得修改。

## 3. 工作流程：Jev-engineering 兩階段

- **Phase 1（已在 Claude Code 完成）**：Jev-planner（high tier）規劃；Jev-executor-medium（medium tier）文獻與分析（Gemini notebook 與網路來源）；獨立 QA 產出 `research/08_qa_report.md`。Phase 1 完成後停止，等待 Phase 2 部署。
- **Phase 2（OpenCode + Kimi K3 swarm）**：依 `handoffs.md` 與 `task_manifest.json` 執行，角色與產出歸屬見 `AGENTS.md`。
  1. 先以 `grill-with-docs` 與使用者逐題 stress-test brief（P2-00）與計畫。
  2. P2-00 brief 為 canary，**必須由人工審閱通過後**才能 fan-out。
  3. 並行生成四種成品；每件成品通過 `verify-with-rubric` 獨立驗收後才算完成。
  4. 發布、部署、推送一律由人工決定，agent 不執行。

## 4. 內容規則（硬性）

1. **事實來源**：只能使用 `research/06_fact_sheet.json` 中 `status: "verified"` 的事實，並在內文或 `sources.md` 註明 fact id（如 F39）。
2. **secondary_only**：僅來自次要來源（新聞稿、摘要、轉述），可使用，但必須標示為「初步」或「待證實」。
3. **unverified / contradicted**：一律不得使用，包括作為反面論述。例：F57「意識有影格率」（contradicted）不得出現。F40（`p = 3×10^-40`）已於 `research/09_fix_log.md` 更正為 verified，但只能連同其比較脈絡（意識增益 vs 被抑制增益）引用，不可當作效果量（效果量為 F39 的 1.21）。
4. **預印本聲明**：每件成品都必須明確寫出「bioRxiv 預印本、尚未經同儕審查」。英文 PPTX 寫 "bioRxiv preprint, not yet peer reviewed"。
5. **範式**：描述為雙眼閃光抑制（binocular flash suppression），定位為雙眼競爭（binocular rivalry）的變體。
6. **禁用說法**：不得說「意識有影格率」或「意識的幀率」（Tsao 已否定）；不得說「解決意識問題」等過度宣稱。
7. **2020 數字**：2020 eLife 的數字（如 93 / 57 / 73）只能標註為 2020 年研究，不得歸給 2026 的 Hesse et al. 研究。
8. **GNWT / IIT**：為我們的詮釋，不得歸給 Tsao 或 Hesse 等作者。
9. **zh-TW 用語**：依 `research/05_glossary.csv`。使用台灣慣用詞（資訊、演算法、皮質、顳葉），不用簡體字與中國大陸用語。
10. **單位**：頻率用 Hz，時間用 ms（如 15 Hz、約 60 ms）。
11. **sources.md**：每件成品必須附 `sources.md`，列出所用的每個 fact id、其 status，以及對應段落或畫面。
12. **不得發明事實**：資料缺口標記為「待證實」或移除，不得補寫。

## 5. 環境事實

- 本機無 Python：腳本一律用 node 執行。
- NotebookLM CLI 認證目前有問題（見 `research/raw/nlm_status.md`）：遇到認證錯誤要回報，不得自行改寫或保存 token。
- 本機不自動安裝套件；需要安裝時回報主控。

## 6. Skills（路徑：`.claude/skills/<name>/SKILL.md`）

Phase 2 前置（pre-work）：

- `grill-with-docs`（`.claude/skills/grill-with-docs/SKILL.md`）：fan-out 前與使用者逐題 stress-test brief 與計畫，同時產出 ADR 與 GLOSSARY。`disable-model-invocation: true`，需由使用者呼叫。依賴 `grilling` 與 `domain-modeling`。
- `grilling`（`.claude/skills/grilling/SKILL.md`）：由 `grill-with-docs` 使用的壓力測試訪談流程。
- `domain-modeling`（`.claude/skills/domain-modeling/SKILL.md`）：撰寫或修改 GLOSSARY 與 ADR。
- `map-vs-territory`（`.claude/skills/map-vs-territory/SKILL.md`）：任務模糊，或前次產出看似對但錯時，診斷 brief 缺口。
- `blindspot-pass`（`.claude/skills/blindspot-pass/SKILL.md`）：開工前掃描 brief 的隱含假設與未定義邊界；只產出清單，不產出內容。
- `reference-anchor`（`.claude/skills/reference-anchor/SKILL.md`）：風格以 `phase2/00_brief/style_refs/` 中的具體檔案為參照，不用文字描述風格。
- `decision-first-plan`（`.claude/skills/decision-first-plan/SKILL.md`）：計畫依決策易變性排序，決策項目放前面。

執行期間：

- `deviation-log`（`.claude/skills/deviation-log/SKILL.md`）：swarm 執行時記錄每個非顯然假設與偏離，保守處理並留下紀錄，不無限停下等待。

驗收前：

- `comprehension-quiz`（`.claude/skills/comprehension-quiz/SKILL.md`）：驗收前由人類理解每件成品的主要判斷，特別是 judgment calls。
- `verify-with-rubric`（`.claude/skills/verify-with-rubric/SKILL.md`）：**主觀成品（影片、簡報、文章）的必經閘門**。必須由與產出者隔離 context 的獨立 sub-agent 依 rubric 評分，producer 不得自評。

來源說明：`grill-with-docs`、`grilling`、`domain-modeling` 取自 mattpocock/skills（MIT License）；其餘 finding_unknown skills 取自 Thariq 的 finding_unknown 系列。

## 7. 禁止事項（所有 agent）

- 發布、部署、推送（publish / deploy / push）：禁止，須由人工決定。
- 花費金錢、申請付費服務或付費 API：禁止，須由人工決定。
- 修改 `research/` 任何檔案。
- 發送訊息或外部通知。
- 自動安裝、設定權限，或修改本檔與 `AGENTS.md`。
- 在未獲人工核准前 fan-out。

## 8. 驗收摘要

每件成品在交付前須同時滿足：(a) 通過 `verify-with-rubric`；(b) 含預印本聲明；(c) 內容只引用 verified 事實（secondary_only 已標示）；(d) 附 `sources.md`；(e) 通過 zh-TW 用語檢查（英文 PPTX 除外）。任一項未通過即退回，不得由 agent 自行宣告完成。
