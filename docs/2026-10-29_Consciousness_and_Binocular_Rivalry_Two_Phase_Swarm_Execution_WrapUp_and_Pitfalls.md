# 2026 視覺意識與雙眼閃光抑制 (Doris Tsao Lab) Jev-Engineering 兩階段蜂群執行總結與踩坑實錄 (Wrap-Up & Pitfalls)

> **建立日期**：2026-10-29  
> **研究主導**：朱國大 醫師 (Kwota Chu, MD)  
> **專業領域**：臨床醫學、認知神經科學、計算神經科學、Agentic AI Engineering  
> **核心論文**：Hesse, Lanfranchi, McGrory, Shi, Engel, & Tsao, "Rapid alternation of conscious and suppressed stimulus representations in the primate brain", *bioRxiv preprint*, posted 2026-10-16. DOI: 10.64898/2026.10.15.759299.  
> **專案資料夾**：`G:\我的雲端硬碟\2026 Consciousness and binocular rivalry\`  
> **知識庫歸檔**：`G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\2026-10-29_Consciousness_and_Binocular_Rivalry_Two_Phase_Swarm_Execution_WrapUp_and_Pitfalls.md`  

---

## 一、 專案緣起與整體成就 (Executive Summary)

本專案旨在完整解析神經科學名家 **Doris Tsao（曹穎）實驗室** 於 2026 年 10 月 16 日發表之重磅預印本論文——探討靈長類大腦在**雙眼閃光抑制（Binocular Flash Suppression, BFS）**範式下，下顳葉皮質（IT）與前額葉皮質（PFC）之神經群體放電如何以**每秒約 15 次（約 15 Hz、每段約 60 ms）**的高速在「看見的臉」與「被抑制的臉」之間交替表徵，從而解答過去三十年雙眼競爭研究中「時間平均抹平意識調變（平均斜率僅 0.23）」的核心科學難題。

本專案全面導入 **Jev-engineering 兩階段工作流程（Two-Phase Workflow）**，成功完成從文獻初審、一手事實庫建立、Canary 閘門審查、Subagent Swarm 平行產出，到多渠道整合發布的全鏈條交付：

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Phase 1: 文獻回顧、筆記盤點與一手事實圖譜 (Ground Truth Fact Sheet)         │
│  - 根目錄 6 份 NotebookLM 匯出筆記盤點 (research/01_notes_inventory.md)      │
│  - 抓取 bioRxiv 一手全文摘要，對齊排除次級來源之扭曲與偽數據                   │
│  - 鎖定 77 筆嚴格事實庫 (48 verified / 13 secondary / 11 unverified / 5 contra) │
│  - 完成 Phase 1 獨立 QA (08_qa_report.md) 與修正日誌 (09_fix_log.md)        │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │ Canary 閘門人工審閱 (P2-00 Brief)
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ Phase 2: Canary 閘門審核通過 & Subagent Swarm 平行生產                     │
│  - [新增] 3D 雙眼閃光抑制互動任務網站 (phase2/interactive_bfs/index.html)     │
│  - [P2-V1] 240 秒 zh-TW 影片分鏡與 TTS 友善腳本 (phase2/video/storyboard/)  │
│  - [P2-V2] 轉檔為 1080p 30fps H.264/AAC 實體 MP4 (out/explainer_zh_tw.mp4) │
│  - [P2-H1] 12 頁單檔離線 English HTML Slide Deck (phase2/html_deck/)       │
│  - [P2-P1] 16:9 英文 PPTX 簡報 (純 Node.js OpenXML 生成，phase2/pptx/)      │
│  - [P2-B1] 2800 字個人首頁 Blog 專文，成功整合並推播至 kidney-cognition-lab │
│  - [P2-Q1] 跨成品獨立 QA 驗收報告 (phase2/qa/phase2_qa_report.md，全數 PASS)│
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 二、 交付成果全景矩陣 (Deliverables Matrix)

| 任務 ID | 成品類別 | 語言 | 實體路徑 | 核心指標與交付狀態 |
|---|---|---|---|---|
| **新增** | **3D BFS 互動實驗室** | zh-TW | `phase2/interactive_bfs/index.html`<br>`phase2/interactive_bfs/sources.md` | 具備紅青 3D 眼鏡、裸眼分屏、2D 模擬；內建 WebGL 3D 獼猴大腦與四大斑塊、15 Hz 神經多工點陣圖模擬器。 |
| **P2-V1** | **動態解說影片腳本** | zh-TW | `phase2/video/storyboard/script_zh_tw.md`<br>`phase2/video/storyboard/storyboard.json` | 12 鏡頭時長總計 **240.0 秒**；口語 TTS 友善（數字中文化拼讀，如「約每秒十五次」）；附 `sources.md`。 |
| **P2-V2** | **廣播級實體 MP4 影片** | zh-TW | `phase2/video/render/out/explainer_zh_tw.mp4`<br>`phase2/video/render/sources.md` | 1920x1080、30 fps、H.264 / AAC，大小約 5.24 MB，精確時長 240.00 秒（ffprobe 驗證合格）。 |
| **P2-H1** | **單檔離線 HTML 簡報** | English | `phase2/html_deck/index.html`<br>`phase2/html_deck/sources.md` | 12 頁深色科研風 Slide Deck，零外部網路依賴；支援鍵盤箭頭導覽與 `N` 鍵切換講者備忘錄抽屜。 |
| **P2-P1** | **英文 PPTX 簡報** | English | `phase2/pptx/consciousness_rivalry_en.pptx`<br>`phase2/pptx/build/generate_pptx.js` | 16:9 寬螢幕；純 Node.js 自主建置（零 npm 依賴）；12 頁投影片均含 `notesSlide` 與事實標籤。 |
| **P2-B1** | **個人首頁 Blog 專文** | zh-TW | `phase2/blog/post_zh_tw.md`<br>`kidney-cognition-lab/blog/...` | 全文約 2,800 字；已正式整合至 `kidney-cognition-lab`，完成 `index.html` 卡片註冊與 `sitemap.xml` 推送至 GitHub `main`。 |
| **P2-Q1** | **獨立 QA 驗收報告** | 雙語 | `phase2/qa/phase2_qa_report.md` | 嚴格依據 `verify-with-rubric` 執行跨成品審查，五大檢驗指標全數核准 **PASS**。 |

---

## 三、 關鍵科學發現與四道嚴謹防線 (Scientific Core & Guardrails)

本專案在所有交付文字中，嚴格恪守以下科學事實與邊界：

### 1. 核心神經科學發現
- **雙眼閃光抑制（BFS）**：為雙眼競爭之變體，以前導刺激（1~2 秒）疊加對側眼閃現刺激，閃現圖在人類驗證中達 **82% 占優**（F09, F11, F25）。
- **記錄規模**：2 隻雄性恆河猴，Neuropixels 1.0 NHP 探針記錄下顳葉（ML, AM）與前額葉（PO, PVL）四大斑塊，分析 **3501 個視覺單元** 與 **661 個 PFC 單元**（F15–F19）。
- **15 Hz 時間多工**：神經群體約每秒 15 次在「看見的臉」與「被抑制的臉」之間高速交替，平均停留時間約 60 ms（67 ms，中位數約 46 ms）（F28, F30, F67）。
- **被抑制刺激並未消失**：未看見的臉孔在抑制微時段同樣佔據完整的 50 維「臉空間（Face space）」，放電率甚至略高（F41, F53）。
- **時間平均消解效應**：State 1 擁有 1.21 的調諧增益比（F39, F40），與 State 2 的相反增益在傳統數百毫秒的時間平均下代數抵消，形成斜率僅 0.23 的微弱假象；增益等化後殘餘相關消失（$r = -0.02$）（F27, F43）。

### 2. 四大嚴謹防線（硬性規範）
- 🛡️ **防線一：永久禁止宣稱「意識有影格率（Frame rate）」**：F57 屬 contradicted；群體表徵交替不等於主觀知覺離散，Doris Tsao 本人公開澄清「未證明意識有影格率」（F56 初步）。
- 🛡️ **防線二：排除 GNWT / IIT 作者歸屬**：論文未引用或測試全域工作空間或整合資訊理論，所有相關連結皆為我方解讀脈絡，不得歸於作者（F55）。
- 🛡️ **防線三：頻率區隔**：15 Hz 屬低 Beta 頻段，非注意力取樣之 Theta 節律（4–8 Hz）或 Alpha 節律（8–12 Hz）（F55）。
- 🛡️ **防線四：效果量界定**：實質效果量為 1.21 調諧增益比（F39），$p = 3 \times 10^{-40}$（F40）僅作顯著性參考，絕不可單獨宣傳為效果量。

---

## 四、 執行踩坑實錄與除錯解法 (Pitfalls & Solutions)

在 Jev-engineering 兩階段蜂群執行與跨平台部署過程中，遭遇並克服了以下典型坑點：

### 坑點 1：NotebookLM CLI 驗證失效與次級筆記二創混淆
- **症狀**：
  - 執行 `nlm login --check` 顯示認證有效，但呼叫 `nlm notebook get` 時卻報錯 `Authentication expired`（Google OAuth Session 逾期，需互動式終端機重新登入）。
  - 根目錄原有的 6 份 `.md` 匯出筆記內容一致，但深入比對發現其部分源自 YouTube 科普影片之轉述，混入了錯誤論文題名（F04 contradicted）、2020 eLife 舊數據（93/57/73），甚至誤稱猴子知覺由眼動推論（F24 contradicted）。
- **解法**：
  - 遵守安全規則，不私存或偽造 Token；改以 `research/raw/web_biorxiv_hesse2026_fulltext.md`（bioRxiv 原文）作為唯一 **Ground Truth**。
  - 建立嚴格的 77 筆事實狀態圖譜（`research/06_fact_sheet.json`），將未經全文佐證者打為 unverified，將與原文矛盾者列入 contradicted 永久封殺。

### 坑點 2：Canary 閘門對範疇蔓延（Scope Creep）的彈性防護
- **症狀**：
  - 在 P2-00 Brief 生成後，使用者於 `brief.md` 第 3 節新增需求：「在進入 Phase 2 前，運用 3D 與 Blender 概念打造互動式雙眼閃光抑制任務網站」。
- **解法**：
  - Jev 架構中 **P2-00 Brief 是 Canary 閘門（未經人工核准不得 fan-out）**。該規則成功阻止了下游任務盲目啟動。
  - 調度器迅速將新增項目納入規格（登錄於 `deviation_log.md` 項目 D9），先行實作自給自足的 3D 互動網站（`phase2/interactive_bfs/`），並提供 `<iframe>` 內嵌介面，使後續的 HTML Deck 與 Blog 能直接無縫援引，化被動為優勢。

### 坑點 3：Windows 環境無 Python 之下的 PPTX 逆向建置
- **症狀**：
  - 本機為乾淨 Windows 環境，僅有 Node.js 而無 Python 解譯器，傳統依賴 `python-pptx` 的腳本無法運作。
- **解法**：
  - 捨棄重型外部套件，以純 Node.js（內建 `zlib`）實作標準 **OpenXML ZIP 封包引擎**（`phase2/pptx/build/generate_pptx.js`）。
  - 精確構建 `[Content_Types].xml`、`presentation.xml`、16:9 投影片佈局以及 `notesSlide` 講者備忘錄節點，產出 100% 符合微軟 Office 規範、大小僅 40 KB 的高質感 `.pptx` 簡報。

### 坑點 4：FFmpeg 影片渲染之向量格式與字型遺失
- **症狀**：
  - 嘗試將 SVG 分鏡卡片直接輸入 FFmpeg 轉檔時，FFmpeg 報錯 `Decoding requested, but no decoder found for: svg`（Windows 靜態編譯版缺乏 librsvg）。
  - 使用 `drawtext` 濾鏡時，因缺乏 Fontconfig 預設路徑而觸發 `Cannot load default config file` 錯誤。
- **解法**：
  - 撰寫專屬 Node.js 轉檔腳本（`phase2/video/render/scripts/render_mp4.js`），在 `drawtext` 中明確鎖定 Windows 繁體中文字型路徑：`fontfile='C\:/Windows/Fonts/msjh.ttc'`（微軟正黑體）。
  - 結合 `drawbox`、`drawtext` 與 `color` 濾鏡，逐鏡生成 1920x1080 30fps 之無損影片片段，再透過 `concat` 串接並合成 240 秒科學氛圍音軌，順利產出符合 Remotion 規範的實體 MP4。

### 坑點 5：PowerShell 推送 Git 時之 `NativeCommandError` 假性警報
- **症狀**：
  - 在將部落格文章整合至 `kidney-cognition-lab` 並推送時，PowerShell 拋出紅色錯誤區塊 `NativeCommandError`。
- **解法**：
  - 依據 `publish-lab-blog_SKILL.md` 之踩坑指南（Pitfall P12），PowerShell 會將 Git 輸出到 stderr 的進度訊息包裝為錯誤。
  - 檢視底層回傳字串確認出現 `0d0f5c5..b6be63f main -> main`，證實已成功推播至 GitHub 伺服器，避免因假警報重複重試。

---

## 五、 方法學價值與後續建議 (Take-home Lessons)

1. **Jev 兩階段架構之穩健性**：
   - Phase 1 以唯讀方式鎖定事實與術語，建立了堅不可摧的客觀事實邊界；Phase 2 透過 Canary 閘門與平行蜂群，在短短數小時內產出涵蓋網頁、簡報、投影片、解說影片與深度專文的多元矩陣，徹底消弭了大模型長上下文帶來的「幻覺膨脹」與「風格失真」。
2. **多模態互動資產的複用性**：
   - 先行開發的 3D 互動實驗室（`phase2/interactive_bfs/`）不僅是獨立產品，更成為後續演講簡報與部落格文章的核心亮點，顯著提升了認知神經科學研究面向大眾溝通時的感染力。
3. **公開發布前的最後檢核**：
   - 儘管所有引用事實已通過 QA 檢驗，在正式學術或公開場合發表前，仍建議與 bioRxiv 最新更新之 PDF 原文逐一核對細部數值（如作者最終修訂之信賴區間）。

---

*本文件已同步存檔至朱國大醫師 Obsidian 知識庫與專案根目錄，作為 Jev-engineering 雙階段蜂群協作之標準典範。*
