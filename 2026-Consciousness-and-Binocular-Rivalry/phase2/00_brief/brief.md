# Phase 2 共用 Brief（P2-00，canary v1）

> 本文件是四個下游 worker（影片、HTML deck、PPTX、blog）的唯一共同依據。**未經人工審閱通過前，任何 worker 不得開工。**
> 內容規則以 `CLAUDE.md` 第 4 節與 `AGENTS.md` 第 5 節為準；本文件不重複定義，只負責落地成可執行規格。
> 事實的完整文字以 `research/06_fact_sheet.json` 為準；此處只列 id 與一句提示，方便查找。

## 1. 一句話故事與關鍵訊息

**一句話：** 在雙眼閃光抑制中，獼猴下顳葉與前額葉的同一群神經元，約每秒 15 次在「看見的臉」與「被抑制的臉」的表徵之間快速交替（每段約 60 ms），這可能解釋為何過去研究平均起來看不到清楚的意識訊號。

**關鍵訊息（每件成品都要傳達，至多五點）：**
1. 大腦對「看不見的圖」並非沒有反應：群體活動在極短時間內輪流表徵兩張臉；觀察者的知覺本身沒有跟著變。
2. 切換約每秒 15 次、每段約 60 ms（數十毫秒），遠快於主觀的知覺切換。
3. 這可能解釋為何過去用平均活動找意識訊號時，調變看起來很弱（本資料集內的作者解釋）。
4. 這是預印本，尚未同儕審查；只有兩隻猴子、只測臉。
5. 這不等於「意識有影格率」，作者自己也這麼說。

## 2. 閱聽眾與語氣

- 閱聽眾：一般大眾，無神經科學背景。
- 語氣：引人入勝但準確；對預印本狀態保持謙遜。可以好奇，不可以驚悚。
- 可用 `research/07_analogies_visuals.md` 的類比（A1–A5、A7、A8），但每個類比必須自帶防線（「這個類比會誤導之處是……」）。A6（影格/翻頁書）只能當反面教材，主動說明為什麼不能這樣想。
- 慎用字眼：「證明」「揭開意識之謎」「推翻」一律不用。安全動詞：發現、顯示、暗示、可能解釋。

## 3. 範式框架（固定說法）

- zh-TW：「雙眼閃光抑制（binocular flash suppression），雙眼競爭的一種變體」。
- English： "binocular flash suppression, a variant of binocular rivalry"。
- 不得簡稱為「雙眼競爭」或 "classic binocular rivalry"（F09）。
- 猴子沒有回報看到什麼；「看見」的標籤由神經活動推論，並由 14 位人類受試者按鍵驗證（82% 試次報告看到閃現圖）（F23、F25）。
- Before process to phase 2, Use the skill:https://github.com/ckt520728/2026-Antigravity/tree/main/.agents/skills/cloudflare-math-game-builder , connect BLENDER to build a 3D-feauture interactive website, the Binocular Flash Suppression task, which can be a isolated website and also be used in HTML slide deck and blog post. 

## 4. 事實使用規則與允許清單

規則：
- **只用 status = verified 的事實。** verified 是「與 raw 摘要一致」，非逐字；公開發表前每一筆仍須對照 PDF（人類發布階段的工作，但寫作時不得加油添醋）。
- **secondary_only 可用，但出現處必須標「初步」；英文成品標 "preliminary"。**
- **unverified 與 contradicted 永遠不得出現**，包括當反例、當「有人說……但錯了」的靶子。
- **F40（p = 3×10^-40）只能與 F39 一起引用**，並註明比較對象是「意識增益 vs 被抑制增益」；效果量是 F39 的比值 1.21，不是 p 值。
- 資料缺口標「待證實」或直接刪除，不得補寫。

### 4.1 允許的 verified fact id（共 48 筆，依主題分組）

**A. 論文身份（5）：** F01（bioRxiv 預印本，2026-10-16，未同儕審查）・F02（題名 "Rapid alternation of conscious and suppressed stimulus representations in the primate brain"）・F03（作者 Hesse、Lanfranchi、McGrory、Shi、Engel、Tsao）・F05（DOI 10.64898/2026.10.15.759299）・F06（單位：UC Berkeley、Caltech BBE、Princeton、HHMI）

**B. 範式與人類驗證（8）：** F09（雙眼閃光抑制，雙眼競爭的變體）・F11（前導刺激 1 或 2 s 後向另一眼閃現，閃現圖通常占優）・F12（實驗一：前導 2 s/測試 4 s，10 張臉 25 對）・F13（實驗二：1 s/1 s，1500 張臉 750 對）・F14（紅青立體眼鏡，刺激 7°）・F23（猴子無報告，狀態由 LLR+HMM 推論）・F25（14 位人類驗證，82% 報告閃現圖）・F26（人類統計細節：t(13)=9.4 等）

**C. 記錄規模（8）：** F15（2 隻雄性恆河猴）・F16（Neuropixels 1.0 NHP 探針）・F17（記錄 ML、AM、PO、PVL 四個斑塊）・F18（跨場次 3501 個視覺反應神經元）・F19（PFC 分析 661 個）・F20（範例放電點陣圖 429 個細胞）・F21（增益分析 543 個細胞）・F22（場次數：狀態分析 9、雙對單狀態 19、解碼 10、跨區 7）

**D. 核心發現：微時段交替（7）：** F27（平均雙眼調變弱：斜率 0.23）・F28（群體約每秒 15 次交替）・F29（單次試驗分析：10 ms 時間窗 Poisson LLR + 雙狀態 HMM；10 ms 是分析時間窗，不是狀態長度）・F30（停留時間：平均 67 ms、中位約 46 ms→說「約 60 ms」）・F31（HMM 中位停留：狀態一 64 ms、狀態二 59 ms）・F32（比競爭切換約 0.5 Hz 快一個數量級以上）・F67（狀態一表徵看見的臉、狀態二表徵被抑制的臉，約 60 ms 狀態）

**E. 解碼、重建與對照（7）：** F33（狀態一意識臉解釋變異「部分特徵」>80%，須保留「部分特徵」）・F35（全視窗十類解碼：意識 40%、被抑制 34%，機率 10%）・F36（狀態一解碼：意識 >61% 對被抑制 4%）・F37（留出神經元統計）・F38（雙狀態模型 19/19 場次勝過單狀態）・F45（對照：打亂模板 EV<0；平均/僅意識/不協調模型各至少 4 項檢驗失敗 3 項）・F46（最初重建分析具循環性，作者以留出神經元處理）

**F. 增益與單細胞（5）：** F39（調諧增益比 1.21，r=0.90——這才是效果量）・F40（p = 3×10^-40，只能連同 F39 的比較脈絡引用，須註明是意識增益對被抑制增益）・F41（狀態二平均放電率略高；線性解碼 66% 區分兩狀態——與 F39 不矛盾，是不同量測）・F42（同一批神經元切換內容，沒有分開的兩群）・F43（增益等化後殘餘相關消失 r=-0.02：平均效應可解釋本資料集的微弱調變）

**G. PFC 與跨區（5）：** F47（ML–AM 切換協調弱，作者稱證據不強）・F48（IT 與 PFC 都交替，PFC 為定性相似）・F50（PFC 重建品質較低：前導 EV<80%、形狀特徵<30%）・F51（PFC 狀態統計）・F52（作者：「因此可能是廣泛的皮質現象」——保留「可能」）

**H. 限制、開放問題與理論脈絡（3）：** F53（被抑制刺激並非微弱殘影，在自己的時段占據相同的臉空間）・F54（開放問題：為何有些微時段進入意識；切換機制未知；路由至報告/行動是推測）・F55（討論連結注意力取樣、theta 相位等；預印本未引用 GNWT/IIT，也未討論 alpha；15 Hz 不在 theta 頻段）

### 4.2 secondary_only（13 筆，出現處必須標「初步」/ "preliminary"）

F07（Tsao 任 Astera 神經科學首席）・F08（Engel 負責計算分析）・F56（Tsao 澄清：「我們並未證明意識有影格率」——這句**可以引**，標初步）・F58（意識依賴多腦區，本文只報告少數節點）・F59（Tsao 發文宣傳語「推翻數十年想法」等——只可作為「作者的宣傳措辭」引用並標初步，不可當中立事實）・F60（作者稱結果揭示在平均活動中尋找 NCC 的限制）・F61（Glitchwire 的提醒：「timing, not area」超出預印本）・F68（2020 eLife：無報告、眼動推論知覺——屬 2020，不是 2026）・F69（Shi et al. 2026 Nature：<20 ms 協同事件切換編碼，僅限臉；只寫 2026，不寫月份）・F71（Kingir et al. 2025 預印本）・F72（Cogitate 2025：256 人，fMRI/MEG/iEEG，預先註冊）・F73（Cogitate：兩理論皆未被決定性證實或否證）・F76（Tsao 的 Mindscape 訪談，僅存在性）

### 4.3 禁用事實 id（16 筆，永遠不得出現）

- contradicted（5）：F04（錯誤題名）、F10（「直接稱雙眼競爭」）、F24（「2026 由眼動推論知覺」）、F44（「過去 30 年完全是平均造成」）、F57（「意識有影格率」）
- unverified（11）：F34（700 ms 模糊疊加）、F49（IT–PFC 15 Hz 同步）、F62（「職涯最重要突破」）、F63（「證據中等至強」評分）、F64（2020 的 93/57/73 數字）、F65（700 ms 感知穩定期）、F66（「恢復到單獨呈現水平」）、F70（Shi 2026 發表日期）、F74、F75（記憶中文獻）、F77（注意力 4 Hz 取樣文獻數字）

## 5. 禁用說法清單（逐條檢查）

1. 「意識有影格率」「意識的幀率」「意識是每秒 15 次的閃爍」——永久禁止（F57 contradicted）。可替代：「IT/PFC 群體表徵的內容約每秒 15 次交替，這不等於意識本身分成離散影格。」
2. 把 2020 eLife 的數字（93/57/73）歸給 2026——禁止；且這組數字本身 unverified（F64），完全不引用。2026 的人類驗證數字是 82%（F25）。
3. 把 GNWT/IIT 的裁決或連結歸給 Tsao 或 Hesse 等作者——預印本未引用這些理論（F55）。若成品要談 GNWT/IIT，必須明確標為「我們的詮釋，並非作者主張」。
4. 過度宣稱：「解決意識問題」「揭開意識之謎」「推翻數十年思維」「純粹的意識相關物」「timing, not area」「適用所有感知」。
5. 「IT 與 PFC 以約 15 Hz 同步切換」（F49 unverified）。正確：兩區各自交替；ML–AM 協調弱（F47、F48）。
6. 「過去 30 年的微弱調變完全是平均造成」（F44）。正確：「平均效應可解釋本資料集中的微弱調變」（F43）。
7. 「10 ms 微時段」——10 ms 是分析時間窗（bin）；狀態長度是約 60 ms（F29、F30、F31）。
8. 「700 ms 感知穩定期」「700 ms 平均是模糊疊加」（F34、F65）。
9. 孤立引用 p = 3×10^-40，或把它當效果量（見第 4 節 F40 規則）。
10. 錯誤題名 "A temporal multiplexing mechanism for conscious perception"（F04）；正確題名見 F02。
11. 「2026 年猴子的知覺由眼動推論」（F24）——眼動推論屬 2020 eLife（F68，初步）。
12. 簡體字與中國大陸用語（信息、算法、皮层、颞叶、视频等）——zh-TW 成品一律台灣用語（見第 8 節）。
13. 把 15 Hz 說成 theta 或 alpha 振盪，或引「注意力 4 Hz」當印證（F55、F77）。

## 6. 預印本聲明（逐字使用）

- zh-TW：「本研究為 bioRxiv 預印本、尚未經同儕審查。」
- English： "bioRxiv preprint, not yet peer reviewed."

每件成品必須出現一次以上，位置見第 7 節。

## 7. 各成品限制（人類已決定，不得更改）

### 7.1 影片（P2-V1 腳本分鏡 → P2-V2 渲染）| zh-TW
- 產出：zh-TW 旁白稿 + 逐鏡 storyboard（含每鏡對應 fact id）。
- 長度：目標約 240 s，硬性範圍 180–300 s。
- 後續渲染：Remotion，1920×1080，30 fps，Noto Sans TC 字幕 + zh-TW TTS 旁白軌（TTS 引擎在渲染啟動時才決定）。
- **旁白稿必須 TTS-friendly：** 口語短句；避免難讀符號（×、^、≈、p 值、t 值、括號統計）；數字在旁白中拼讀（「約每秒十五次」「約六十毫秒」「三千五百個神經元」），字幕可保留阿拉伯數字與單位；p 值與統計量只進字幕或不提。
- 預印本聲明進旁白或結尾卡。
- 類比建議自 07_analogies_visuals.md 選用（A6 僅作反面教材）；每個類比附防線。

### 7.2 HTML deck（P2-H1）| English
- 單一 HTML 檔、離線可用、12–18 頁 slides。
- 風格以 `phase2/00_brief/style_refs/soil-html-deck_SKILL.md` 為參照（reference-anchor，不用文字描述風格）。
- 鍵盤導覽；speaker notes 引用 fact id。
- "bioRxiv preprint, not yet peer reviewed." 放第一頁或最後一頁。
- **zh-TW 用語檢查不適用於本成品**；但事實規則（第 4、5 節）全部照舊，secondary_only 標 "preliminary"。

### 7.3 PPTX（P2-P1）| English
- 風格以 `phase2/00_brief/style_refs/soil-deck-pipeline_SKILL.md` 為參照。
- 可重現的 build script 放在 `phase2/pptx/build/`（本機無 Python，用 node）。
- speaker notes 引用 fact id；含英文預印本聲明。
- 事實規則同上，secondary_only 標 "preliminary"。

### 7.4 Blog（P2-B1）| zh-TW
- 2000–3500 字。
- front-matter 與結構依 `phase2/00_brief/style_refs/publish-lab-blog_SKILL.md` 與 `publish-lab-blog_PITFALLS.md`；行文語氣參考 `personal-blog-post-writing_SKILL.md`。
- 圖片放 `phase2/blog/images/`。
- **絕不執行 publish/deploy/push**；不執行 style_refs 中任何發布步驟。

### 7.5 全部成品共通
- 各自附 `sources.md`：列出用到的每個 fact id、status、出現位置（段落/鏡頭/頁碼）。
- 只寫自己的資料夾；可讀 `research/` 與本 brief；不可讀寫他組產出（P2-Q1 除外）。
- 交付前必過 `verify-with-rubric` 獨立驗收；producer 不得自評。
- 非顯然的假設用保守選項並記 deviation-log，不要停下等答案。

## 8. 術語速查表（zh-TW，摘自 research/05_glossary.csv）

| 英文 | zh-TW（台灣用語） | 備註 |
|---|---|---|
| binocular flash suppression (BFS) | 雙眼閃光抑制（BFS） | 雙眼競爭的變體，勿簡稱雙眼競爭 |
| binocular rivalry | 雙眼競爭 | |
| priming stimulus | 前導刺激 | 先呈現 1 或 2 秒的圖 |
| percept | 知覺內容 | |
| micro-epoch | 微時段 | 約數十毫秒的狀態時段 |
| conscious state / suppressed state | 有意識狀態 / 受抑制狀態 | 標籤由神經資料推論 |
| inferotemporal (IT) cortex | 下顳葉皮質 | |
| prefrontal cortex (PFC) | 前額葉皮質 | PO = 眶額葉、PVL = 腹外側 |
| face patch ML / AM | ML 臉部斑塊（中外側）/ AM 臉部斑塊（前內側） | |
| Neuropixels probe | Neuropixels 探針 | 型號 1.0 NHP |
| hidden Markov model (HMM) | 隱馬可夫模型 | 雙狀態 Poisson HMM |
| log-likelihood ratio (LLR) | 對數概似比 | 10 ms 時間窗（bin）上計算 |
| bin | 時間窗 | 勿把 10 ms bin 說成狀態長度 |
| dwell time | 停留時間 | 平均 67 ms、中位約 46–64 ms |
| decoding / single-trial decoding | 解碼 / 單次試驗解碼 | |
| reconstruction | 重建 | |
| explained variance (EV) | 解釋變異量 | |
| face space | 臉空間 | |
| spike raster | 放電點陣圖 | |
| circular analysis / held-out neurons | 循環分析 / 保留神經元（留出神經元） | |
| permutation test | 置換檢定 | sign-flip，1e5 次 |
| no-report paradigm / report confound | 無報告範式 / 報告混淆 | |
| neural correlates of consciousness (NCC) | 意識的神經相關物 | |
| time multiplexing | 時間多工 | 專案用語，非論文用詞 |
| global neuronal workspace theory (GNWT) | 全域神經工作空間理論 | 屬我方詮釋脈絡，不歸給作者 |
| integrated information theory (IIT) | 整合資訊理論 | 同上 |
| ignition | 點燃 | GNWT 術語 |
| theta rhythm / alpha rhythm | θ 節律（約 4–8 Hz）/ α 節律（約 8–12 Hz） | 15 Hz 不屬任一頻段 |
| preprint / peer review | 預印本 / 同儕審查 | |
| frame rate | 影格率 | 只用於否定句脈絡，見第 5 節第 1 條 |

禁用的大陸用語對照：信息→資訊、算法→演算法、皮层→皮質、颞叶→顳葉、视频→影片。

## 9. 單位與數字寫法

- 頻率用 Hz，時間用 ms；首次出現可雙寫：「約每秒 15 次（約 15 Hz）」、「每段約 60 毫秒（約 60 ms）」。
- 安全說法：「約每秒 15 次」「每段約 60 ms（數十毫秒）」。避免「精確 15 Hz」「剛好 67 ms」。
- 「兩隻獼猴、跨場次共記錄約三千五百個有視覺反應的神經元」（3501，F18；勿說「每次數千」）。
- 「在『意識』時段，十選一的單次辨識率超過 61%（隨機為 10%），被抑制那張臉僅約 4%」（F36）。
- 效果量只講 1.21（F39）；p 值規則見第 4 節。

## 10. 驗收提醒（引用 CLAUDE.md 第 8 節）

每件成品交付前須同時滿足：（a） 通過 verify-with-rubric；（b） 含預印本聲明；（c） 只引用 verified 事實（secondary_only 已標初步/preliminary）；（d） 附 sources.md；（e） zh-TW 用語檢查通過（英文成品不適用）。任一項未過即退回。
