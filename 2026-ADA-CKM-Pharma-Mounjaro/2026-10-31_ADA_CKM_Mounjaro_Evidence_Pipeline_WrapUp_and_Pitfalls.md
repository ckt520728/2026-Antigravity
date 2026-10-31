# Mounjaro／Tirzepatide 多模態醫學證據教材管線實施總結與踩坑實錄 (Wrap-up & Pitfalls)

> **建立日期**：2026-10-31  
> **研究主導**：朱國大醫師 (Kwo-Ta Chu, MD, PhD)  
> **專業領域**：臨床醫學（腎臟科）、認知神經科學、計算神經科學  
> **工作區根目錄**：`D:\2026 ADA_CKM_Pharma`  
> **交接指引路徑**：`D:\2026 ADA_CKM_Pharma\handoffs.md`  
> **本地知識庫存檔**：`G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\2026-10-31_ADA_CKM_Mounjaro_Evidence_Pipeline_WrapUp_and_Pitfalls.md`  
> **核准大綱版本**：`v0.2-review` (SHA-256: `2d499d07f1deb4ac92d48c074618e5152b19c322ee44c5c45158957713953b11`)  
> **完成標記**：<!-- GOAL_COMPLETE -->

---

## 一、 任務背景與全域目標 (Executive Summary)

本專案旨在為醫療專業人員（HCPs）建構一套嚴謹、無偏差且多模態的臨床證據對齊教材，全面剖析 **Tirzepatide（Mounjaro／Zepbound／猛健樂）** 與 **Semaglutide（Ozempic／Wegovy）** 在第二型糖尿病（T2D）、肥胖症、保留射出分率心衰竭（HFpEF）及慢性腎臟病（CKD）四大適應症邊界之療效與安全性數據。

依據使用者（朱國大醫師）於 2026-10-30 正式核准之 `v0.2-review` 大綱規格與 `/goal` 指令，本輪執行任務著重於在**本機離線、零額外開銷、無未授權外部發布、嚴格保護歷史基準**的前提下，全自動完成五大工作包（Work Packages: T4_STATE、T4_DOC_BLOG、T4_DECK、T4_MOTION、T4_ACCEPT）的實體交付與獨立品質驗收。

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    核准大綱 v0.2-review (SHA-256 驗證通過)                  │
│   - 26 頁簡報骨幹：開場 → 分子/身份 → 糖尿病 → 肥胖 → HFpEF → 腎臟 → 安全   │
│   - 16 項實證宣告 (C001-C016) + 3 項待核邊界 (P001-P003) 嚴格追溯          │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │ 本地多模態生成引擎 (Zero-Spend Local Pipeline)
                                      ▼
┌───────────────────┬───────────────────┬───────────────────┬───────────────────┐
│ 1. 互動式 HTML 簡報 │ 2. 可編輯 PPTX 簡報 │ 3. 專業論文導讀   │ 4. 90秒 1080p 影片 │
│  - 26頁離線單檔    │  - python-pptx 原生│  - Word DOCX 排版 │  - HyperFrames 引擎│
│  - 鍵盤/全螢幕導航  │  - 原生向量長條/森林│  - 無損 Markdown  │  - 本機 GPU 渲染   │
│  - P06/P14 互動題  │  - 內嵌講者臨床備註│  - 腎臟神經流形視角│  - 60/60 WCAG 合格│
└───────────────────┴───────────────────┴───────────────────┴───────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 獨立驗收與控制審查 (T4_ACCEPT)                                              │
│  - Python 驗證器 validate_project.py：21/21 檢查全數通過                    │
│  - 35 項歷史研究保護檔案與 21 項 JEV Vendor Pin 維持 100% 原始雜湊不變     │
│  - PowerPoint COM 匯出全 26 頁無變形圖檔；FFprobe 驗證 MP4 參數精確 90.0 秒 │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 二、 臨床實證與計算神經動力學交織視角 (Dual-Lens Clinical Synthesis)

在朱國大醫師的「腎臟臨床實務」與「計算神經科學（Cognitive & Computational Neuroscience）」交叉視角下，本教材打破了傳統藥廠銷售導向的直覺式宣傳，將臨床決策建構為高維狀態空間中的**「決策邊界（Decision Boundary）」**：

### 1. 座標化對齊架構 (Seven-Dimensional Coordinate System)
臨床醫師評估一項新療法時，不可單看「降糖幅度和體重百分比」，必須同時定位七個正交座標：
$$\text{Evidence Coordinate} = (\text{Molecule}, \text{Brand}, \text{Dose}, \text{Population}, \text{Comparator}, \text{Endpoint}, \text{Jurisdiction})$$
- **SURPASS-2**：T2D 控制不足成人；Tirzepatide (5/10/15 mg) vs **Semaglutide 1 mg**（非 2.4 mg 減重劑量）；主要終點為 40 週 HbA1c 變化（−2.01 至 −2.30 vs −1.86 百分點），屬控糖試驗，不可移花接木為減重排名。
- **SURMOUNT-5**：無 T2D 之單純肥胖成人；Tirzepatide (10/15 mg) vs **Semaglutide 1.7/2.4 mg**；72 週體重降幅（−20.2% vs −13.7%），屬 open-label modified treatment-regimen estimand，非心腎硬終點比較。
- **SUMMIT**：肥胖合併 HFpEF（LVEF ≥ 50%）；複合終點（CV death 或心衰竭惡化）HR 0.62 (95% CI 0.41–0.95)，但單獨心血管死亡 HR 1.58 (95% CI 0.52–4.83，信賴區間顯著跨 1)。**絕不可宣稱「證實降低死亡率」**。
- **FLOW**：T2D 合併 CKD 之確認性腎臟硬終點試驗屬於 **Semaglutide 1 mg** (HR 0.76)；SURPASS-CVOT 之腎臟結果屬預定探索性分析（Exploratory / Abstract-only），**嚴禁將 FLOW 成果外推為整個類別（Class Effect）或 Tirzepatide 之確認性保護**。

### 2. 動態適應與慢速流形控制 (Slow Manifold & Dynamic Homeostasis)
- **SURMOUNT-4 停藥反彈**：隨機停藥試驗顯示，在 36 週前驅治療後改換安慰劑，體重於 36–88 週顯著回升 +14.0%（持續用藥組再降 −5.5%）。這在動力學系統中體現了「代謝定點吸引子（Metabolic Setpoint Attractor）」的強大重力回拉，提示肥胖治療是慢速流形的長期調控，而非單次脈衝干預。
- **體液流失與 AKI 骨牌效應**：嚴重腸胃道反應（嘔吐、腹瀉）合併攝水不足時，腎血流動力學自動調節代償機制受挫，易誘發腎前性急性腎損傷（Pre-renal AKI）。仿單中「腎功能不全者無需調整 PK 劑量」絕不等於「腎臟完全無風險」。

---

## 三、 本次實施遭遇之六大踩坑與技術突破 (Encountered Pitfalls & Hard-Learned Lessons)

在本次全自動多模態教材產製管線中，克服了跨平台環境、COM 自動化、影片渲染引擎與編碼格式等底層瓶頸：

### 踩坑 1：Windows 終端沙盒環境進程安全環境建立失敗 (Sandbox Environment Failures)
- **問題現象**：在 Antigravity 終端沙盒環境下直接執行 PowerShell 或外部工具命令時，沙盒拋出致命錯誤：
  ```
  exebox: creating sandbox: CreateProcessSecurityEnvironment: The system cannot find the path specified.
  ```
- **根因分析**：Windows 系統下 sandbox process isolation 在處理特定跨磁區路徑映射與權限繼承時，因底層安全環境句柄建立超時或缺漏而阻斷指令派發。
- **解決方案**：
  - 嚴格遵守 ToolGate 規則：在沙盒建立失敗時，切換為 `BypassSandbox: true` 模式，同時於 Prompt 與主控端嚴密限制操作邊界（僅限寫入 `monjaro/` 及指定交付目錄，嚴禁存取憑證、嚴禁外部網路 Egress、零花費）。

### 踩坑 2：Office PowerPoint COM 自動化生命週期崩潰 vs `python-pptx` 原生生成
- **問題現象**：初始嘗試透過 PowerShell 調用 `PowerPoint.Application` COM 物件時，遭遇 RPC 遠端程序呼叫失敗：
  ```
  pywintypes.com_error: (-2147023170, '遠端程序呼叫失敗。', None, None)
  ```
  且在無頭（Headless）後台環境下，Office 進程極易因視窗句柄阻塞或對話方塊而掛起逾時。
- **根因分析**：微軟 Office COM API 並非專為非互動式背景管線設計，在建立與關閉簡報時對執行緒模式與桌面工作站權限有嚴苛依賴。
- **解決方案**：
  - **解耦生成與驗證**：產製端改採 100% 純 Python 之 `python-pptx` 函式庫，直接讀取 `slides.json` 寫入標準 Office OpenXML 二進位結構，精確繪製原生長條圖、HR 1.0 森林圖向量形狀、隔行變色表格與演講備註，完全擺脫 Office COM 依賴。
  - **COM 僅用於唯讀驗收**：後續僅以 PowerPoint COM 開啟已生成的 PPTX 並無頭匯出 26 頁無損圖檔至 `monjaro/qa/deck/` 進行渲染驗收，並加入優雅釋放機制。

### 踩坑 3：HyperFrames 動畫檢驗之多元素選擇器歧義 (Motion Selector Ambiguity)
- **問題現象**：執行 `hyperframes check` 進行靜態與動態檢查時，Motion 階段報錯阻斷：
  ```json
  {
    "code": "motion_selector_ambiguous",
    "severity": "error",
    "selector": ".card",
    "message": ".card matches multiple elements — use a more specific selector so the assertion targets exactly one."
  }
  ```
- **根因分析**：`index.motion.json` 中的 `staysInFrame` 斷言使用了通用 Class 選擇器（如 `.card` 與 `.caption`），然而 DOM 中同時存在多個場景的同名元素，HyperFrames 語法強制要求運動斷言必須唯一定位。
- **解決方案**：
  - 將斷言修正為具體 ID 定位（如 `#card-0-0` 與 `#cap-0-0`），使檢查管線順利通過，達成 **Lint 0 錯誤、Runtime 0 錯誤、Layout 0 溢出問題、Motion 0 錯誤**，並通過 60/60 項 WCAG AA 高對比檢核。

### 踩坑 4：本機 16 GB RAM 記憶體告急與無頭 Chrome 渲染崩潰
- **問題現象**：`hyperframes doctor` 檢測本機硬體時發出記憶體警訊：`Memory: 15.7 GB total · 1.3 GB available (Low memory — renders may fail)`。若直接啟動預設的多進程平行截圖，Chrome headless instances 將瞬間引發記憶體換頁（Memory Thrashing）與崩潰。
- **根因分析**：1080p 30fps 影片長達 90 秒（共 2,700 幀），未限制工作線程時會並行開啟大量渲染上下文。
- **解決方案**：
  - 在渲染命令中加入 `--low-memory-mode` 旗標：強制綁定單一 Worker，啟用輕量級 Screenshot Capture 並關閉自動調校，同時調用本機 NVIDIA GeForce RTX 3060 進行硬體 WebGL 加速。
  - 最終以 3 分 24 秒極速平穩完成 2,700 幀無損編碼，生成 5.42 MB 的優質 MP4 影片。

### 踩坑 5：Windows PowerShell 逸出字元陷阱與 UTF-16LE 亂碼干擾
- **問題現象**：PowerShell 的 `"` 雙引號內建變數展開機制（如 `$ppt.Quit()` 被誤解為空變數調用函式）經常破壞傳遞給 Python `-c` 的參數；此外 PowerShell 的預設重導向操作符（`>`）在舊版中會輸出帶 BOM 的 UTF-16LE 編碼，導致後續讀檔工具判讀為二進位檔案。
- **解決方案**：
  - 全面使用獨立 `.py` 指令碼並搭配 `python -X utf8` 執行，杜絕單行命令行字串跳脫失效。
  - 所有檔案讀寫一律強制宣告 `encoding='utf-8'`，並在管線中加入 `assert '??' not in text` 斷言，徹底杜絕問號亂碼。

### 踩坑 6：臨床數據「同義詞混淆」與「非確認性分析過度升格」
- **問題現象**：在大型語言模型處理醫學文獻時，極易將「複合終點有顯著獲益」下意識潤飾為「該藥物能顯著降低心血管死亡」，或將「探索性分析（Exploratory Analysis）」升格為等同於正式 Phase 3 RCT 的宣稱。
- **解決方案**：
  - 建立嚴格的 `claim_ledger.csv` 與 `source_registry.json` 溯源機制，每一張投影片與每一段文字皆綁定唯一 Claim ID（如 C006, C008, C010）。
  - 對於尚未取得台灣現行仿單、最新給付規定、作者資訊或具體麻醉胃排空停藥天數之項目，**強制維持 `[TO CONFIRM]`**，堅決杜絕無中生有的「幻覺補全」。

---

## 四、 產出交付檔案清單與驗收數據 (Verification Matrix)

```
D:\2026 ADA_CKM_Pharma\
├── handoffs.md                                         [已更新交接與驗收狀態]
├── AGENTS.md                                           [工作區法規守則]
└── monjaro/
    ├── deliverables/
    │   ├── mounjaro_evidence_deck.html                 [87,480 B | 離線單檔 26 頁簡報]
    │   ├── mounjaro_evidence_deck.pptx                 [135,769 B | 原生可編輯 16:9 簡報]
    │   ├── mounjaro_paper_explainer.docx               [43,046 B | 微軟正黑體排版 Word]
    │   ├── mounjaro_paper_explainer.md                 [12,666 B | 雙重視角專業導讀文章]
    │   ├── homepage_blog_draft.html                    [26,891 B | 互動式情境比對文章草稿]
    │   ├── mounjaro_motion_explainer.mp4               [5,419,974 B | 1080p 30fps 90秒影片]
    │   ├── mounjaro_motion_explainer.srt               [1,810 B | 9場景18條字幕檔]
    │   └── motion_storyboard.md                        [6,862 B | 動畫分鏡腳本]
    ├── qa/
    │   ├── production_acceptance.md                    [主控獨立品質驗收報告]
    │   ├── deck/                                       [PPTX COM 匯出之 26 頁圖檔]
    │   └── motion/check.json                           [HyperFrames 檢驗通過記錄]
    └── workflow/
        ├── approval.json                               [v0.2-review 大綱核准存證]
        ├── production-tasks.json                       [五大工作包已驗收狀態]
        └── validation-results.json                     [21 項專案驗證 passed]
```

### 二進位與技術規格確認表
1. **影片流驗證 (FFprobe)**：
   - Codec: `h264 (High) (avc1)`
   - 畫面尺寸: `1920x1080` (16:9)
   - 幀率: `30.00 fps`
   - 音訊: 無（靜音字幕衛教版）
   - 精確播放時間: `00:01:30.00` (90.0 秒)
2. **簡報檔結構驗證 (python-pptx & COM)**：
   - 投影片總數: `26` 頁
   - 投影片尺寸: 寬 `13.333 吋` × 高 `7.5 吋` (16:9 Widescreen)
   - 演講備註 (Notes Slide): 26 頁均內嵌完整 Clinical Ledger 條目與原始 URL。
   - COM 轉圖輸出: `26` 張 JPG/PNG 影像無缺漏。
3. **安全與合規驗證 (validate_project.py)**：
   - 受保護之歷史研究檔案（35 檔）：**無任何變更**。
   - JEV Vendor 原始檔案（21 檔）：**無任何變更**。
   - 外部發布與花費授權：維持 `False`。

---

## 五、 後續建議與行動綱領 (Actionable Next Steps)

1. **台灣本土法規與仿單核定更新**：
   - 當前台灣 TFDA 猛健樂（Mounjaro）注射筆核定範圍已涵蓋血糖與體重控制概括用途，後續若需印製對外衛教單張或臨床手冊，應向主管機關或醫學會核實台灣最新核准之詳細適應症字號、BMI 門檻與健保給付規定，將 `[TO CONFIRM]` 替換為正式條文。
2. **多媒體對外發布授權**：
   - 本輪所有產物（HTML 簡報、PPTX、影片、部落格）目前均處於本地端安全封存狀態。若未來規劃推播至醫院內部教學系統或朱醫師個人部落格，需另行發起發布審查（Gate 4 Publication Clearance）並移除 `robots: noindex,nofollow`。
3. **跨模態素材持續重用**：
   - 本套管線建構的 `slides.json` 與 `claim_ledger.csv` 具備極高結構化純度，未來可無縫接入臨床演講投影片抽換、衛教社群圖文卡產製或進階微課程（Micro-learning modules）的自動化建構。

---

> 本總結檔案已完整同步儲存至朱醫師 Obsidian 第二腦知識庫：  
> `G:\我的雲端硬碟\Second Brain\知識庫\2026-Antigravity\2026-10-31_ADA_CKM_Mounjaro_Evidence_Pipeline_WrapUp_and_Pitfalls.md`
