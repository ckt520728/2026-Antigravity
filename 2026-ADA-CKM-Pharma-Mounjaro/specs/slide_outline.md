# SOIL 逐頁大綱：Tirzepatide／Mounjaro 與 Semaglutide 的證據對齊教材

版本：v0.2-review｜日期：2026-10-30（Asia/Taipei）｜證據截止：2026-10-29｜狀態：**待使用者審閱，未取得 outline 核准**
受眾：醫療專業人員（臨床醫師、藥師、糖尿病與心腎照護團隊）
範圍：糖尿病、肥胖、肥胖相關 HFpEF、腎臟風險與用藥邊界；嚴格區分 tirzepatide（GIP／GLP-1 dual agonist）與 semaglutide（GLP-1 RA）

> 本大綱對應 `monjaro/evidence/claim_ledger.csv` 與 `source_registry.json`。臨床內容只採 verification 屬於 verified／verified_US_only／verified_abstract／verified_scope_only／verified_boundary 的 C-claims；P001–P003、台灣完整仿單與給付、作者／機構／COI 一律標 [TO CONFIRM]，不寫成事實。

---

## 引擎一：概念定位（One Big Idea）

**「先對齊藥物、族群與終點，再談選擇。」**

本教材不是藥物促銷，而是證據邊界訓練：同一個藥名出現在糖尿病、肥胖、HFpEF、腎臟四個脈絡時，背後是不同分子、不同試驗族群、不同終點定義。全篇 26 頁只做一件事——示範如何把每一句臨床宣稱拆回「哪個藥、哪個族群、哪個終點、哪個 jurisdiction」再決定能不能說。

## 引擎二：脈絡定位（Hook）

以診間四個通用臨床情境開場（P02）：四位病人都問「猛健樂能不能用」，但四個問題的證據來自四個不同試驗、兩個不同分子、兩種不同 jurisdiction。Hook 的任務是讓專業觀眾在前 60 秒承認：直覺回答會出錯，對齊是必要動作。

## 引擎三：頁面架構（分段與 take-home）

八個分段，每段末附 take-home；每頁一個概念；兩個正式 Check-Point（P06、P14）。分段：§0 開場（P01–P02）｜§1 分子與身份對齊（P03–P06）｜§2 糖尿病（P07–P08）｜§3 肥胖（P09–P10）｜§4 肥胖相關 HFpEF（P11–P14）｜§5 腎臟（P15–P17）｜§6 用藥邊界與安全（P18–P22）｜§7 證據邊界與收尾（P23–P26）。

## 引擎四：認知編修（每頁一概念與負荷控制）

- 每頁一概念；數字頁最多 2 組核心數字＋1 個邊界註記，其餘細節收入講者備註。
- 所有 HR／CI 以 SVG forest plot 呈現，不並排超過 2 個試驗於同一圖；跨試驗比較一律改用「對齊表」而非排名圖。
- 單位明確：HbA1c 為「百分點」；體重為「百分比變化」；CI 保留原始 95% 或 95.3% 標示，不四捨五入改寫。
- 每個數字旁固定附「族群一行標籤」（如：無 T2D 肥胖成人），防止脫族群引用。

## 引擎五：風格建構

- 基底採 kidney-cognition-lab house style（S16）：深色底（#0a0f1e）、卡片 #111d3c、主色 teal #4dd9cf、輔色 purple #8b5cf6、警示 gold #f4a261；字體 Noto Sans TC＋Inter＋JetBrains Mono（數字）；圓角 12px 卡片、teal 漸層分隔線。
- 邊界／排除內容統一使用「紅色邊界卡」（gold 轉 red 系，文字不變色以保持對比）；[TO CONFIRM] 統一灰色 pending 徽章。
- 動畫版（後續 T4 另議）依 S15 motion-design 規則：單一主色＋強調色、字幕子句化；本輪不製作。
- 全篇禁用「萬能鑰匙」「手術般療效」等比喻（見 P23 邊界頁）。

## 引擎六：檢核（Check-Point 設計）

- **Check-Point 1（P06）**：分子／品牌／jurisdiction 對齊，3 題快答。
- **Check-Point 2（P14）**：終點對齊，3 題快答（含 SUMMIT 複合終點、FLOW 藥物歸屬、SURPASS-2 與 SURMOUNT-5 comparator 劑量辨析）。
- 兩個 Check-Point 均設計為「答錯即回指對應頁」，HTML 版以 details/summary 實作，PPTX 版以動畫出現順序實作（T4 另議）。

---

## 逐頁大綱

### §0 開場

---

**P01｜封面**

- 標題：先對齊，再選擇——Tirzepatide 與 Semaglutide 的證據邊界
- 核心訊息：這是一份給醫療專業人員的證據對齊教材；不是處方建議；台灣完整仿單與給付 [TO CONFIRM]。副標註明證據截止 2026-10-29、作者／機構／COI [TO CONFIRM]。
- 視覺策略：純 CSS/SVG 封面；深色底＋teal 漸層線；三軸圖示（molecule／population／endpoint）縮圖預告 One Big Idea。
- 素材來源：純 CSS/SVG；house style S16。

---

**P02｜Hook：四位病人，一個藥名**

- 標題：同一個藥名，四個不同的問題
- 核心訊息：四位病人都問「猛健樂能不能用」——(a) metformin 控制不足的 T2D、(b) 無糖尿病的肥胖、(c) 肥胖伴 HFpEF、(d) T2D 合併 CKD。藥名相同 ≠ 問題相同；答案分別藏在不同分子、不同試驗、不同終點裡。
- 視覺策略：2×2 CSS grid 四張情境卡（每卡一個剪影 icon＋一行情境），第四張卡角落先露出「先對齊」teal 標籤作為懸念。
- 素材來源：純 CSS/SVG；情境為通用臨床描述，不引試驗數據。

### §1 分子與身份對齊

---

**P03｜One Big Idea**

- 標題：先對齊藥物、族群與終點，再談選擇
- 核心訊息：任何一句「這藥有沒有效」都必須先通過三個對齊：哪個分子（tirzepatide 還是 semaglutide）、哪個族群（T2D／肥胖／HFpEF／CKD，各有定義）、哪個終點（HbA1c／體重／複合 CV-HF／腎複合）。三軸缺一，結論不成立。
- 視覺策略：SVG 三層對齊漏斗——molecule → population → endpoint → 才能進入「選擇」；四個脈絡在漏斗出口各連一條線，預告全篇架構。
- 素材來源：純 CSS/SVG。

---

**P04｜分子分類：兩個分子，不是同一類藥的兩個名字**

- 標題：Tirzepatide 是 GIP／GLP-1 雙受體促效劑；Semaglutide 是 GLP-1 受體促效劑
- 核心訊息：tirzepatide 是單一分子的 GIP／GLP-1 dual agonist；semaglutide 是 GLP-1 RA。機制差異存在，但**不能由此推導「療效兩倍」或「所有器官均受益」**；class effect 不可互套。
- 視覺策略：SVG 受體示意——左側 tirzepatide 分子接 GIP＋GLP-1 兩個 receptor box，右側 semaglutide 只接 GLP-1；下方一行 boundary 註記「機制示意，不是療效證明」。
- 素材來源：C001（verified）｜S07（Mounjaro USPI §12.1）、S02（SURMOUNT-5 Introduction）。

---

**P05｜品牌與管轄：適應症要分品牌、分國家**

- 標題：Mounjaro ≠ Zepbound；美國標示 ≠ 台灣標示
- 核心訊息：美國 USPI 下 Mounjaro 標示為 ≥10 歲 T2D 控糖及成人高 MACE 風險 T2D 的風險降低；Zepbound 標示為成人體重控制及肥胖伴中重度 OSA——兩品牌不可互換引用。台灣 TFDA 2025-11-10 公告確認猛健樂注射筆有血糖控制與肥胖過重體重控制用途，但詳細年齡／BMI／OSA 條件與完整仿單 [TO CONFIRM]（P001）；台灣健保給付 [TO CONFIRM]。
- 視覺策略：三欄表（品牌／美國 USPI 標示／台灣現況），台灣欄位蓋灰色 pending 徽章；表尾一行「不得由美國標示推導台灣 MACE／兒科適用」。
- 素材來源：C002（verified_US_only）｜S07、S08（Zepbound USPI）；C003（verified_scope_only）｜S09（TFDA 公告）；P001 標 [TO CONFIRM]。

---

**P06｜Check-Point 1：分子、品牌、管轄**

- 標題：Check-Point 1——對齊了嗎？
- 核心訊息：3 題快答自我檢核：① tirzepatide 的受體分類？（GIP／GLP-1 dual agonist）② 美國體重控制適應症掛在哪個品牌？（Zepbound）③ TFDA 公告能不能當台灣完整仿單用？（不能，詳細條件 [TO CONFIRM]）。答錯回指 P04／P05。
- 視覺策略：三張 quiz 卡（HTML details/summary 展開答案）；卡片邊框 teal，錯誤選項不列干擾記憶的偽數字。
- 素材來源：題目依 C001、C002、C003 出題；純 CSS/SVG 實作。

> **§1 take-home：** 分子（C001）、品牌（C002）、jurisdiction（C003）是三個獨立軸；任何一句適應症宣稱都要說出它站在哪三個座標上。

### §2 糖尿病脈絡

---

**P07｜SURPASS-2：控糖 head-to-head，對手是 semaglutide 1 mg**

- 標題：SURPASS-2——T2D 控糖比較，comparator 是 semaglutide 1 mg
- 核心訊息：metformin 治療仍控制不足的 T2D 成人（1879 隨機），40 週 HbA1c 變化 tirzepatide 5／10／15 mg 為 -2.01／-2.24／-2.30 百分點，semaglutide 1 mg 為 -1.86 百分點。**這是控糖試驗、對手是 1 mg，不能當作與 semaglutide 2.4 mg 的減重比較**；HbA1c 是百分點，不是相對百分比。
- 視覺策略：SVG 長條圖四支 bar（3 劑量＋comparator），comparator bar 用紫色並加粗標籤「sema 1 mg」；右上角族群標籤「T2D，metformin 控制不足」。
- 素材來源：C004（verified）｜S01（SURPASS-2，NEJM 2021，DOI 10.1056/NEJMoa2107519）。

---

**P08｜SURPASS-CVOT：MACE 非劣性成立，優越性未達**

- 標題：SURPASS-CVOT——對 dulaglutide 非劣，不等於優越
- 核心訊息：T2D＋已確立 ASCVD（mITT 13165），tirzepatide ≤15 mg vs dulaglutide 1.5 mg：MACE 12.2% vs 13.1%，HR 0.92（95.3% CI 0.83–1.01）；非劣性成立（界值 1.05，P=.003），優越性未達顯著（P=.09）。**不能說勝過 dulaglutide，更不能說勝過 semaglutide**；這是 active-comparator 試驗，不是 placebo 試驗。
- 視覺策略：SVG forest plot 單點 HR＋CI 橫線，畫出 1.0 與 1.05 兩條參考線並標註「非劣界值」；P 值雙標（NI／superiority）。
- 素材來源：C009（verified）｜S06（SURPASS-CVOT，NEJM 2025，DOI 10.1056/NEJMoa2505928）。

> **§2 take-home：** 糖尿病證據先問 comparator 是誰、劑量多少：SURPASS-2 的對手是 semaglutide 1 mg（C004），SURPASS-CVOT 的對手是 dulaglutide 且只證明非劣（C009）。

### §3 肥胖脈絡

---

**P09｜SURMOUNT-5：無糖尿病肥胖族群的減重比較**

- 標題：SURMOUNT-5——這次的 semaglutide 是 1.7／2.4 mg
- 核心訊息：無 T2D 的肥胖／過重成人（751 隨機），72 週體重變化 tirzepatide 10／15 mg -20.2%（95% CI -21.4 至 -19.1）vs semaglutide 1.7／2.4 mg -13.7%（-14.9 至 -12.6），P<.001。這是**無糖尿病人群的群體平均**，不能保證 T2D／HFpEF 個案同幅減重；本試驗不是心腎 outcome 比較。與 P07 並排提醒：SURPASS-2 用 sema 1 mg、SURMOUNT-5 用 sema 1.7／2.4 mg，兩個 comparator 不可混用。
- 視覺策略：左右並排雙 bar（tirzepatide teal、semaglutide purple），bar 下各自標劑量；右下角小圖示「SURPASS-2 = sema 1 mg ≠ 本頁」防混標籤；註記 modified treatment-regimen estimand、Lilly 資助。
- 素材來源：C005（verified）｜S02（SURMOUNT-5，NEJM 2025，DOI 10.1056/NEJMoa2416394）。

---

**P10｜SURMOUNT-4：停藥是治療決策，不是治療結束**

- 標題：停藥後會發生什麼事——SURMOUNT-4 randomized withdrawal
- 核心訊息：無糖尿病肥胖／過重者在 36 週 tirzepatide lead-in 後隨機（670 人）：繼續 tirzepatide 組週 36–88 再減 -5.5%，改安慰劑組回升 +14.0%。訊息不是「停藥必回升 14%」（這是耐受 lead-in 的選擇人群），而是**開始治療前就要規劃維持與追蹤策略**；也不可用此阻礙急性警訊時的停藥判斷（見 P20）。
- 視覺策略：SVG 雙線圖（週 0–88），週 36 處分歧，teal 線續降、gold 線回升；分歧點標「隨機」；註記 verified_abstract 層級。
- 素材來源：C019（verified_abstract）｜S13（SURMOUNT-4，JAMA 2023，DOI 10.1001/jama.2023.24945）。

> **§3 take-home：** 減重數字永遠綁族群與劑量（C005：無 T2D、sema 1.7／2.4 mg）；療程規劃包含「如何維持、如何停」（C019）。

### §4 肥胖相關 HFpEF 脈絡

---

**P11｜SUMMIT：複合終點獲益 ≠ CV death 單獨獲益**

- 標題：SUMMIT——降的是「CV death 或 HF 惡化」複合終點
- 核心訊息：BMI≥30、HF、LVEF≥50%（731 人，包含有／無 T2D），中位 104 週：複合終點 9.9% vs 15.3%，HR 0.62（95% CI 0.41–0.95）。但 CV death 單獨為 8 vs 5 件，HR 1.58（95% CI 0.52–4.83）——**只能說複合終點獲益，不能說已證實降低 CV 死亡**；52 週 KCCQ 是另一共同主要終點。
- 視覺策略：SVG 終點分解圖——複合終點 HR 一條 forest line，下方 CV death 單獨 HR 一條（CI 明顯跨 1），兩條並列讓「寬 CI」自己說話。
- 素材來源：C006（verified）｜S03（SUMMIT，NEJM，DOI 10.1056/NEJMoa2410027）。

---

**P12｜STEP-HFpEF DM：semaglutide 的 HFpEF 證據重點是症狀、功能與體重**

- 標題：STEP-HFpEF DM——不同藥、不同試驗、不同終點
- 核心訊息：T2D＋BMI≥30＋LVEF≥45% 有症狀 HF（616 人），52 週 semaglutide 2.4 mg vs placebo：KCCQ 差 7.3 分（95% CI 4.1–10.4）、體重差 -6.4 百分點（-9.8% vs -3.4%）。證據重點是**症狀／功能／體重**；不能以此單一試驗宣稱降低 CV 死亡，也不能與 SUMMIT 跨試驗排名。
- 視覺策略：雙指標卡（KCCQ 分數卡＋體重百分比卡），卡片頂部紫色 semaglutide 標籤與 P11 的 teal tirzepatide 標籤形成分子區分。
- 素材來源：C007（verified）｜S04（STEP-HFpEF DM，NEJM 2024，DOI 10.1056/NEJMoa2313917）。

---

**P13｜HFpEF 對讀：一藥、一族群、一終點**

- 標題：把兩個 HFpEF 試驗放回各自的座標
- 核心訊息：SUMMIT＝tirzepatide／肥胖 HFpEF（可有或無 T2D）／CV-HF 複合＋KCCQ；STEP-HFpEF DM＝semaglutide 2.4 mg／T2D＋HFpEF／症狀功能體重。兩者**並存而非互斥**，對齊後才知道各自能回答什麼；跨試驗排名在此沒有證據基礎。
- 視覺策略：三列對齊表（藥物／族群／終點），兩試驗各一列欄位；表尾 teal 一行「對齊後，選擇才有意義」。
- 素材來源：C006＋C007（均 verified）｜S03、S04；純 CSS/SVG 表格。

---

**P14｜Check-Point 2：終點對齊**

- 標題：Check-Point 2——終點對齊了嗎？
- 核心訊息：3 題快答：① SUMMIT 能不能說「已證實降低 CV 死亡」？（不能，複合終點獲益，CV death CI 跨 1——回指 P11）② FLOW 是哪個藥的腎臟試驗？（semaglutide——回指 P15）③ SURPASS-2 與 SURMOUNT-5 的 semaglutide 劑量各是多少？（1 mg vs 1.7／2.4 mg，不可混用——回指 P07／P09）。
- 視覺策略：同 P06 quiz 卡規格；答對後顯示對應 claim ID，示範「每句話都有 ledger 座標」。
- 素材來源：題目依 C006、C008、C004＋C005 出題；純 CSS/SVG。

> **§4 take-home：** HFpEF 證據是「一藥一試驗一終點」：SUMMIT 看複合終點（C006），STEP-HFpEF DM 看症狀功能體重（C007）；對齊前不排名。

### §5 腎臟脈絡

---

**P15｜FLOW：這是 semaglutide 的腎臟試驗，不是 tirzepatide 的**

- 標題：FLOW——腎臟 outcome 證據屬於 semaglutide 1 mg
- 核心訊息：T2D＋CKD（3533 人，eGFR／UACR 雙軌收案），中位 3.4 年：腎主要複合（含 CV death）HR 0.76（95% CI 0.66–0.88，P=.0003）。**這個結果不能轉成 tirzepatide 的 class effect**；也不代表所有 CKD 或透析患者的證據。
- 視覺策略：SVG「證據歸屬卡」——FLOW 卡上紫色 semaglutide 標籤，旁邊 tirzepatide 卡蓋「FLOW 非本藥試驗」灰章；下方一行腎複合終點組成小字。
- 素材來源：C008（verified）｜S05（FLOW，NEJM 2024，DOI 10.1056/NEJMoa2403347）。

---

**P16｜SURPASS-CVOT 腎臟分析：探索性訊號，不是 confirmatory 證據**

- 標題：Tirzepatide 的腎臟訊號——有，但屬探索性
- 核心訊息：2026 出刊的 SURPASS-CVOT 預定探索性腎臟分析（mITT 13165，中位 4.0 年）：腎複合 6.0% vs 7.6%，HR 0.77（95% CI 0.68–0.88，P=.0002）。但它是**探索性分析**、腎複合定義與 FLOW 不同（含新發持續 macroalbuminuria）、不是新的獨立 RCT——可以報告訊號，不能升格 confirmatory。
- 視覺策略：HR forest line 上壓半透明「EXPLORATORY」浮水印；側欄小卡對照「FLOW 定義 ≠ 本分析定義」。
- 素材來源：C010（verified_abstract）｜S12（SURPASS-CVOT 腎臟探索性分析，PubMed 2026）。

---

**P17｜腎臟安全邊界：脫水與 AKI 的真實風險**

- 標題：別只盯 outcome 試驗——GI 反應、體液流失與 AKI
- 核心訊息：美國 USPI 警示：嚴重 GI 反應（持續嘔吐／腹瀉）或攝水不足可致體液流失與急性腎損傷（AKI），已有腎病或易脫水者需評估體液與腎功能；嚴重 gastroparesis 不建議使用。**「renal PK 不調量」不等於「腎臟完全安全」**；台灣版本文句 [TO CONFIRM]（P001）。
- 視覺策略：SVG 警示流程鏈（嘔吐／腹瀉 → 體液流失 → AKI 評估），末端接「補液與腎功能評估」行動框；gold 警示色。
- 素材來源：C013（verified_US_only）｜S07（Mounjaro USPI §5.5–5.6）。

> **§5 take-home：** 腎臟 outcome 證據目前是 semaglutide 的（C008）；tirzepatide 只有探索性訊號（C010）；安全端主動管理脫水風險（C013）。

### §6 用藥邊界與安全

---

**P18｜劑量原則與明確排除：仿單滴定，不是格數算術**

- 標題：2.5 mg 起、每階至少 4 週——以及本教材「不教」的事
- 核心訊息：美國 USPI 成人劑量 2.5 mg weekly 起始，需要時每次增 2.5 mg、當前劑量至少維持 4 週，最大 15 mg weekly；KwikPen 為固定劑量設計（每筆 4 個固定 weekly doses），格數算術不等於核准可拆劑方法。**明確排除**：原研讀素材中的拆筆格數換算、跳級（如 5→10 mg 跳過 7.5 mg）、同週拼筆、採購省錢方案，均不進入本教材。台灣劑量圖與器型 IFU [TO CONFIRM]（P001）；不是人人需達 15 mg。
- 視覺策略：SVG 滴定階梯（2.5→5→7.5→…→15，每階標「≥4 週」）；階梯下方紅色邊界卡列出四項排除（拆筆格數／跳級／同週拼筆／省錢採購）。
- 素材來源：C011（verified_US_only）｜S07（§2.1）；C018（verified_US_only）｜S07（§2.2／3／5.10）；P001 [TO CONFIRM]。

---

**P19｜禁忌：誰不該用**

- 標題：MTC、MEN2、嚴重過敏——美國標示禁忌
- 核心訊息：美國 USPI 禁忌為 MTC（medullary thyroid carcinoma）個人／家族史、MEN2 與嚴重過敏；人類 MTC 風險尚未確立（rodent 訊號，不得寫成人類已證實）。「禁忌」與「不建議使用」（如嚴重 gastroparesis）不能混同；台灣禁忌文句以核准仿單為準 [TO CONFIRM]（P001）。
- 視覺策略：三張禁忌卡（MTC／MEN2／過敏）紅邊設計，下方一行 rodent→human 邊界註記。
- 素材來源：C012（verified_US_only）｜S07（§4／5.1）。

---

**P20｜急性警訊：何時停藥、何時就醫**

- 標題：疑似胰臟炎、嚴重過敏——停藥並立即就醫
- 核心訊息：持續嚴重腹痛（疑胰臟炎）或呼吸／顏面腫脹（嚴重過敏）應停藥並立即接受評估；急性膽囊疾病與視網膜病變併發亦需說明。警訊語句用於專業溝通，病人版措辭需醫師審核；不提供自我診斷或自行重啟建議；台灣文句 [TO CONFIRM]（P001）。
- 視覺策略：紅色警訊卡＋「停藥 → 就醫」兩步驟流程 SVG；與 P10 停藥規劃互連（急性停藥不受體重回升考量阻礙）。
- 素材來源：C017（verified_US_only）｜S07（§5.2／5.4）；急性膽囊疾病與視網膜病變併發另見 S07（§5.7–5.8）。

---

**P21｜併藥風險：胰島素與 secretagogue 的低血糖**

- 標題：併用 insulin 或 sulfonylurea——低血糖風險上升
- 核心訊息：合併 insulin 或 sulfonylurea 等 secretagogue 會增加低血糖風險，可能需要減少併藥劑量，且調整應由醫療團隊決定；不能說單藥零低血糖，也不提供通用減量百分比，病人勿自行減藥；台灣文句 [TO CONFIRM]（P001）。
- 視覺策略：SVG 併藥示意（tirzepatide＋insulin／SU 兩線交會 → 低血糖警示 icon）；底部一行「調整權在醫療團隊」。
- 素材來源：C014（verified_US_only）｜S07（§5.3）。

---

**P22｜胃排空延遲的臨床後果：避孕藥與麻醉**

- 標題：同一個機制，兩個臨床場景
- 核心訊息：胃排空延遲有兩個具體後果——(a) 口服荷爾蒙避孕藥效力可能降低：開始用藥及每次升量後 4 週應改非口服方法或加屏障法；(b) 麻醉／深鎮靜有吸入（aspiration）風險，應預先告知手術／麻醉團隊，且**沒有通用仿單停藥天數**（USPI 稱資料不足以判定暫停藥能否降低風險），不得自行套用固定停藥規則。妊娠計畫停藥間隔與台灣麻醉流程 [TO CONFIRM]（P003）。
- 視覺策略：中央「胃排空延遲」機制圓，左右分出避孕藥卡與麻醉卡；麻醉卡標「無固定停藥天數」邊界章。
- 素材來源：C015（verified_US_only）｜S07（§7.2／8.3）；C016（verified_US_only）｜S07（§5.9）；P003 [TO CONFIRM]。

> **§6 take-home：** 劑量走仿單階梯（C011），格數算術、跳級、拼筆、省錢方案一律排除（C018）；禁忌（C012）、急性警訊（C017）、併藥（C014）、胃排空後果（C015／C016）各就各位，台灣文句全部待 P001。

### §7 證據邊界與收尾

---

**P23｜不能說的事：證據邊界總表**

- 標題：這份教材刻意不說的五件事
- 核心訊息：① 直接抗炎／心腎全面受益等機制推論不升格為臨床結論（biomarker 與 clinical outcome 分層；動物或其他 GLP-1 RA 結果不當 tirzepatide 人體證據）；② 「手術般療效」比喻不用；③ FLOW 結果不外推 tirzepatide；④ SUMMIT 複合終點不寫成 CV death 獲益；⑤ SURPASS-2（sema 1 mg）與 SURMOUNT-5（sema 1.7／2.4 mg）的 comparator 不混用。
- 視覺策略：紅色邊界總表（五行，每行一條禁令＋對應正確說法）；表頭「邊界不是缺點，是教材的一部分」。
- 素材來源：C020（verified_boundary）｜S01–S05 方法學對照；C008、C006、C004＋C005 交叉引用；純 CSS/SVG。

---

**P24｜待核與未決：[TO CONFIRM] 清單**

- 標題：上線前必須完成的查核
- 核心訊息：P001 台灣目前各強度／器型完整仿單與核准版本（年齡、BMI、OSA、劑量、禁忌、交互作用、妊娠、麻醉警示、保存／漏打）及健保給付——未過 gate 前不做個別處方或台灣劑量圖；P002 原始補充資料／SAP／critical correspondence 核讀（涉及安全性優劣、心腎途徑、探索性 multiplicity）；P003 妊娠計畫停藥間隔與台灣現行麻醉流程。作者／機構／COI 亦 [TO CONFIRM]。
- 視覺策略：灰色 pending checklist（每項 checkbox 未勾），右欄標「gate：未過前不發布對應內容」。
- 素材來源：P001、P002、P003（均 pending）｜S14 為台灣仿單候選入口（pending，不作依據）；純 CSS/SVG。

---

**P25｜總結：三行帶走**

- 標題：先對齊，再選擇
- 核心訊息：① 分子、品牌、jurisdiction 是三個獨立軸（C001／C002／C003）；② 每個療效數字綁定試驗族群與 comparator 劑量（C004／C005／C006／C007／C008／C009）；③ 邊界（探索性、複合終點、US-only、[TO CONFIRM]）本身就是要傳達的內容。
- 視覺策略：三行大卡卡組，每行卡角標對應 claim ID；收尾回到 P03 三軸漏斗縮圖。
- 素材來源：全篇 claim 回指；純 CSS/SVG。

---

**P26｜來源與版本**

- 標題：證據來源與版本
- 核心訊息：列出本教材使用的來源與 jurisdiction 標籤：S01 SURPASS-2、S02 SURMOUNT-5、S03 SUMMIT、S04 STEP-HFpEF DM、S05 FLOW、S06 SURPASS-CVOT、S07 Mounjaro USPI（USA）、S08 Zepbound USPI（USA）、S09 TFDA 公告（台灣，scope-only）、S12 SURPASS-CVOT 腎臟探索性分析、S13 SURMOUNT-4；證據截止 2026-10-29；各頁 claim ID 與正式 claim ledger 對應。
- 視覺策略：reference table（source ID／試驗或文件／jurisdiction 徽章／DOI 或 locator）；頁尾版本行 v0.2-review。
- 素材來源：正式 source registry 中實際使用的 S01–S09、S12、S13；S10／S11／S14 不作主要依據；house style S16 註明。

---

## 排除與邊界聲明（全篇適用）

1. 不採用原 ZIP 研讀素材中的拆筆格數換算、跳級（5→10 mg）、同週拼筆、採購省錢方案（對應 P18 紅色邊界卡；相關素材僅保留於 archive 供稽核，不進教材）。
2. 不使用「直接抗炎」「心腎全面受益」「手術般療效」「萬能鑰匙」等語句作為臨床結論（C020 邊界）。
3. 不混用 SURPASS-2 semaglutide 1 mg 與 SURMOUNT-5 semaglutide 1.7／2.4 mg；不把 SUMMIT 複合終點寫成 CV death 單獨獲益；不把 FLOW（semaglutide）外推 tirzepatide；不把 SURPASS-CVOT 探索性腎分析升格 confirmatory。
4. 美國 USPI 內容一律標 USA jurisdiction；台灣完整仿單、給付、妊娠與麻醉流程、作者／機構／COI 一律 [TO CONFIRM]，未過 P001–P003 gate 前不補寫。

## 核准狀態

outline approval：**pending**（`monjaro/workflow/tasks.json` L5）。本檔為可審閱大綱，不是核准版本；核准需使用者對指定版本／SHA-256 明確同意並記錄日期與範圍。核准前不製作 HTML／PPTX／影片／blog（見 `production_brief.md`）。
