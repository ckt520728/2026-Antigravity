# Tirzepatide／Semaglutide 證據摘要

整理日：2026-10-30（Asia/Taipei）｜證據截止：2026-10-29  
結論：目前可交付的是**有來源邊界的教材規劃**，不是系統性回顧、個別處方或台灣完整用藥指引。正式 [source registry](source_registry.json) 收錄 27 筆（16 個 S sources、7 個 ZIP artifacts、4 個 NotebookLM original-text 介面紀錄）；[claim ledger](claim_ledger.csv) 有 21 個 C-claims 與 3 個 pending 項目。關鍵數字已回到原始研究全文、PubMed 原始摘要、正式 USPI 或 TFDA 公告抽核。

## 1. 藥物、品牌與 jurisdiction 必須分開

- **C001**：tirzepatide 是單一分子的 GIP／GLP-1 receptor dual agonist；semaglutide 是 GLP-1 receptor agonist。依據 Mounjaro USPI §12.1 與 SURMOUNT-5 Introduction。機制差異不能推導「療效兩倍」、全面抗炎或所有器官均受益。
- **C002（USA only）**：2026-08 USPI 將 Mounjaro 標示為 ≥10 歲 T2D 控糖，以及成人高 MACE 風險 T2D 的風險降低；Zepbound 則為成人體重控制與肥胖伴中重度 OSA。兩個品牌不能互換引用，美國標示也不能直接套用到台灣。
- **C003（scope only）**：TFDA 2025-11-10 公告概述猛健樂注射筆核准用途為血糖控制及肥胖／過重體重控制；公告不是完整仿單，不能補猜年齡、BMI、OSA、給付或其他細節。公告中的「GLP-1 藥品」概括用語不改變 C001 的分子分類。

## 2. 糖尿病與肥胖：head-to-head 結論只屬於原試驗設計

- **C004／SURPASS-2**：1879 位 metformin 治療仍控制不足的 T2D 成人，40 週 HbA1c 變化為 tirzepatide 5／10／15 mg −2.01／−2.24／−2.30 **百分點**，semaglutide **1 mg** −1.86 百分點。不能拿來代表 semaglutide 2.4 mg 的減重比較。
- **C009／SURPASS-CVOT**：T2D＋已確立 ASCVD，mITT 13,165；tirzepatide ≤15 mg vs dulaglutide 1.5 mg 的 MACE 為 12.2% vs 13.1%，HR 0.92（95.3% CI 0.83–1.01）。非劣性成立（界值 1.05，P=.003），優越性未達（P=.09）；不能寫成勝過 dulaglutide 或 semaglutide。
- **C005／SURMOUNT-5**：751 位**無 T2D** 肥胖／過重成人，72 週體重變化 tirzepatide 最大耐受 10／15 mg −20.2%（95% CI −21.4 至 −19.1）vs semaglutide 最大耐受 1.7／2.4 mg −13.7%（−14.9 至 −12.6），P<.001。此為 open-label、modified treatment-regimen estimand 的群體結果，不是 T2D／HFpEF 個案保證，也不是心腎 outcome 比較。
- **C019／SURMOUNT-4（abstract level）**：783 人進入 36 週 lead-in，670 人隨機；週 36–88 持續 tirzepatide −5.5%，改 placebo +14.0%。只支持「治療前規劃維持與追蹤」，不代表所有人停藥必然回升 14%，也不能阻礙急性警訊時停藥。

## 3. 肥胖相關 HFpEF：終點不能互相代換

- **C006／SUMMIT**：731 位 BMI≥30、HF、LVEF≥50% 患者（包含有／無 T2D），中位 104 週；CV death 或 HF 惡化複合終點 9.9% vs 15.3%，HR 0.62（95% CI 0.41–0.95）。CV death 單獨為 8 vs 5 件、HR 1.58（95% CI 0.52–4.83），因此只能陳述複合終點獲益，不能宣稱已證實降低 CV death，也不把寬 CI 解讀成證實死亡危害。KCCQ 是另一共同主要終點。
- **C007／STEP-HFpEF DM**：616 位 T2D、BMI≥30、LVEF≥45% 的有症狀 HF 患者，52 週 semaglutide 2.4 mg vs placebo；KCCQ-CSS 差 7.3 分（95% CI 4.1–10.4），體重 −9.8% vs −3.4%（差 −6.4 百分點）。重點是症狀／功能與體重，不能單獨宣稱 CV death 獲益或與 SUMMIT 跨試驗排名。

## 4. 腎臟：藥物歸屬、終點定義與探索性層級

- **C008／FLOW**：3533 位 T2D＋CKD 患者接受 semaglutide 1 mg 或 placebo，中位 3.4 年；主要腎複合 331 vs 410 件，HR 0.76（95% CI 0.66–0.88，P=.0003）。複合終點包含 CV death，且只適用於原收案條件；不能外推成 tirzepatide class effect、所有 CKD 或透析患者證據。
- **C010／SURPASS-CVOT kidney analysis（abstract level）**：2026 年 Lancet Diabetes Endocrinol 預定探索性分析，中位 4.0 年；腎複合 6.0% vs 7.6%，HR 0.77（95% CI 0.68–0.88，P=.0002）。腎複合含新發持續 macroalbuminuria，與 FLOW 定義不同；這不是新的獨立 RCT，尚未完成全文／SAP multiplicity 審核，不升格 confirmatory。
- **C013（USA only）**：嚴重 GI 反應、嘔吐／腹瀉與體液流失可導致 AKI；已有腎病或易脫水者需監測。renal PK 不需調量不等於「腎臟完全安全」。

## 5. 劑量與安全只按對應正式文件陳述

- **C011／C018（USA only）**：成人由 2.5 mg weekly 起始，需要時每次增加 2.5 mg，當前劑量至少 4 週，成人最大 15 mg weekly；USPI 列出每支 KwikPen 含 4 個標示劑量且單一病人使用、不得共享。這不是台灣劑量圖或個別處方。
- **C012–C017（USA only）**：禁忌、胰臟炎、嚴重過敏、併用 insulin／secretagogue 的低血糖、口服荷爾蒙避孕藥、麻醉／深鎮靜 aspiration 與急性警訊均按 2026-08 Mounjaro USPI 對應段落。沒有通用仿單麻醉停藥天數；不由半衰期自行推算臨床方案。
- S11 UK IFU 於本次 webfetch 不支援 PDF、直接 GET 回 HTTP 403，故降為 pending，不作主要依據；C018 已改由實際讀取的美國 USPI §2.2／3／5.10 支持。

## 6. 明確排除的二手素材推論

以下內容保留在 canonical ZIP 供稽核，但不進正式教材：

1. 「萬能鑰匙」、「手術般療效」、直接抗炎、GIP 止吐因果或心腎全面受益等超出臨床終點的說法。
2. 把 SUMMIT 或 STEP-HFpEF DM 改寫成「顯著減少 HF 住院」；兩試驗須依各自實際終點陳述。
3. 把 association、biomarker、動物或其他 GLP-1 RA 結果寫成 tirzepatide 人體因果證據。
4. 拆筆格數換算、抽殘藥、延長一筆使用週數、5→10 mg 跳級、同週拼筆與採購省錢方案；數學量相等不代表核准且安全的給藥方法。
5. 未附原始 locator 的額外比較數字不作教材主軸。SURMOUNT-5 Table 2／3 雖已核實部分安全性與 responder 數字，本輪大綱仍只保留必要主要結果，避免認知負荷與過度比較。

## 7. 尚待完成（不得視為已核准）

- **P001**：台灣現行各強度／器型完整仿單、核准版本與健保給付 `[TO CONFIRM]`。
- **P002**：原始 supplement、SAP、critical correspondence 與探索性 multiplicity 完整核讀 `[TO CONFIRM]`。
- **P003**：妊娠計畫停藥間隔、台灣現行麻醉／深鎮靜流程 `[TO CONFIRM]`。
- 作者、機構、COI、最終教材範圍與發布授權均 `[TO CONFIRM]`。目前 outline approval 為 pending，未進 T4。

詳細檢索 URL、NotebookLM source IDs、實際成功／失敗與 locator 見 [search_log.md](search_log.md) 及 [NotebookLM 紀錄](../sources/notebooklm_summary.md)。
