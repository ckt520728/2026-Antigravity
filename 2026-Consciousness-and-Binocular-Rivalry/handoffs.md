# Handoff：Phase 1 → Phase 2

專案：2026 Consciousness and binocular rivalry（Hesse et al. 2026，bioRxiv preprint）
交接日期：2026-10-29

## 1. 狀態

- Phase 1（Claude Code：Jev-planner high + Jev-executor-medium）：**完成，2026-10-29**。
- Phase 2（OpenCode + Kimi K3 swarm）：**啟動中，2026-10-29**（OpenCode CLI v2.2.1 已安裝；manifest 依使用者決定修訂並重算 sha256；P2-00 brief 執行後待人工 canary 審閱）。
- `research/` 為唯讀成果，Phase 2 不得修改。
- 任務清單：`task_manifest.json`（schema `jev.task_manifest/1`，7 個任務）。2026-10-29 修訂：HTML deck 改為英文、影片目標 240 s、P2-V2 加入 zh-TW TTS 旁白（引擎於 P2-V2 啟動時決定，免費／本機優先）、Remotion npm install 已核准（僅限 `phase2/video/render/`）。詳見 `deviation_log.md`。

## 2. 成品清單（research/）

| 檔案 | 用途 |
|---|---|
| `research/01_notes_inventory.md` | 使用者筆記盤點與待查主張清單（inv#） |
| `research/02_paper_card.md` | 論文卡（paper card）：論文主張與方法摘要 |
| `research/03_background_review.md` | 背景文獻回顧（binocular rivalry、no-report 等） |
| `research/04_dossier.md` | 主檔案（dossier）：Phase 2 內容的主要敘事依據 |
| `research/05_glossary.csv` | zh-TW 術語表（台灣用語唯一依據，41 列） |
| `research/06_fact_sheet.json` | 事實表（77 筆，每筆有 id 與 status） |
| `research/06_fact_sheet_README.md` | 事實表 status 圖例與 F40 說明 |
| `research/07_analogies_visuals.md` | 類比與視覺化構想（影片／簡報用） |
| `research/08_qa_report.md` | Phase 1 獨立 QA 報告（17 項問題） |
| `research/09_fix_log.md` | 依 QA 修正的紀錄（含 F40 恢復為 verified、術語統一） |
| `research/raw/` | 原始來源與摘要：`nlm_status.md`、`web_biorxiv_hesse2026_fulltext.md`、`web_related_papers.md`、`web_tsao_x_and_press.md` |

## 3. 來源基礎

- 主要來源：bioRxiv 全文，經 WebFetch 擷取。**這是模型摘要，不是逐字原文**（`research/raw/web_biorxiv_hesse2026_fulltext.md`）。
- 因此 **發布前必須用 PDF 核對所有數字**（包含 verified 項目）。
- 次要來源：Tsao 的 X 貼文與新聞稿（`web_tsao_x_and_press.md`），只支撐 secondary_only 事實。

事實表 status 統計（77 筆）：

| status | 數量 | Phase 2 用法 |
|---|---|---|
| verified | 48 | 可用；仍須 PDF 核對 |
| secondary_only | 13 | 可用，但須標示「初步」（英文 preliminary） |
| unverified | 11 | 不得使用 |
| contradicted | 5 | 不得使用（例：F57「意識有影格率」） |

F40（p = 3×10^-40）為 verified，但只能連同比較脈絡（意識增益 vs 被抑制增益）引用，效果量是 F39 的 1.21。

## 4. Open items

1. **NotebookLM 未匯入**：notebook `bd2a2bb3-8af9-477f-b29f-daba938ca3bd` 因 nlm 驗證失敗（server error 16 / RotateCookies 401）無法讀取。改以根目錄 6 份 `.md` 匯出檔作為 proxy。2 個 artifact（`927e0f8a…`、`03dce093…`）未讀，屬選配的補充（optional enrichment）。
2. **PDF 數字核對**：所有 verified 數字都來自模型摘要，發布前須與 bioRxiv PDF 逐一核對。
3. ~~**Kimi K3 模型設定**~~ **已解決（2026-10-29）**：OpenCode 內 subagent 繼承 session 模型 kimi-k3（經 OpenCode Go provider），不需 Moonshot model ID、base URL 或 `MOONSHOT_API_KEY`；金鑰不寫入任何檔案（見 `deviation_log.md` D6）。
4. ~~**待使用者決定**~~ **已決定（2026-10-29）**：
   - HTML 簡報語言：**英文**（原暫定 zh-TW，已修訂 manifest P2-H1）。
   - 影片旁白／TTS：**加入 zh-TW TTS 旁白**；引擎於 P2-V2 啟動時決定，免費／本機優先，付費 API 須再經人工核准。
   - 影片長度：目標 **約 240 s**（硬性範圍維持 180–300 s）。
   - Remotion 作為 renderer：**已核准** `npm install`，僅限 `phase2/video/render/`。
   - 個人首頁 blog 的 front-matter 目標：維持 manifest 預設（publish-lab-blog 風格，`phase2/00_brief/style_refs/`）。
5. **本機無 Python**：manifest 的 hash 由 node 重現 jev 的 canonical JSON（`ensure_ascii=False, sort_keys=True, separators=(",",":")`）產生，不是 jev 本身執行的結果。
6. **信心值非 live 結果**：manifest 中 `confidence: 0.85`、`model: kimi-k3`、`tier: medium` 為 planner 指定，**並非來自即時的 Jev `decide()` 呼叫**。Phase 2 必須先跑 `preflight()` 才能 fan-out。

## 5. Manifest 與驗證

- 產生器：`phase2/00_brief/tools/make_manifest.js`；驗證器：`phase2/00_brief/tools/verify_manifest.js`（`node` 執行）。
- 任務與依賴：P2-00 → {P2-V1 → P2-V2, P2-H1, P2-P1, P2-B1} → P2-Q1。每任務 max_output_tokens ≤ 12000，總和 64000 ≤ 65536。
- 驗證器輸出（2026-10-29，修訂後）：

```
tasks=7 total_max_output_tokens=64000 sha256=7f6c6fdbb3f3c482e9599943a45e7e40ed6e0f7b061cb56c65447c676f4ca8f0
PASS: hash, unique ids, depends_on order, unique outputs, capabilities, token limits, no credential-like strings
```

## 6. Phase 2 啟動檢查清單

- [x] 確認 Kimi K3 的 Moonshot model ID 與 base URL → 不需要，改經 OpenCode provider（D6）
- [x] 設定環境變數 `MOONSHOT_API_KEY` → 不需要（D6），無金鑰落盤
- [x] 安裝並確認 OpenCode 可用（CLI v2.2.1，`opencode run` 冒煙測試通過）
- [x] 執行 `verify_manifest.js`，確認 PASS（修訂後 sha256=7f6c6fdb…）
- [x] `load_manifest()` 載入成功；`preflight()` 以 verify_manifest + orchestrator 審查替代（D7）
- [x] 使用者決定：HTML 英文、TTS 加入（引擎 TBD）、影片 240 s、Remotion 核准、blog 維持預設
- [x] `grill-with-docs`：使用者決定省略正式流程，以結構化問答取代（D1）
- [x] 執行 P2-00 brief，**人工審閱通過**後才 fan-out（使用者審查並新增 3D BFS 網站規格後核准啟動）
- [x] 並行執行 P2-V1→V2、P2-H1、P2-P1、P2-B1，以及新增之 3D 互動網站 interactive_bfs
- [x] 最後執行 P2-Q1，產出 phase2/qa/phase2_qa_report.md
- [x] 各成品以 `verify-with-rubric` 驗收（全數 PASS）
- [ ] PDF 核對所有引用的數字（公開發表前人工步驟）
- [ ] 發布／部署由人工決定（遵守 Human-only 規則）

## 7. Swarm 注意事項

- P2-00 brief 是手動 canary：人工審閱通過前不得 fan-out。
- 之後 V／H／P／B 任務可並行（policy concurrency 4）；P2-V2 依賴 P2-V1，P2-Q1 最後執行。
- 主觀成品（影片、簡報、文章）用 `.claude/skills/verify-with-rubric` 做獨立驗收。
- 各任務只寫入自己的 outputs；發布、部署、推送不由 agent 執行。
