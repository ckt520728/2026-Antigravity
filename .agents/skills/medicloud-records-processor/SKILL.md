---
name: medicloud-records-processor
description: >
  Process, categorize, and standardize Taiwan National Health Insurance (NHI) MediCloud
  (健保醫療資訊雲端查詢系統) patient data into two distinct clinical formats:
  Format A (Diagnostic & Laboratory Reports: 檢驗數據、成人健檢、放射影像、病理報告、西醫用藥)
  and Format B (Hospital Discharge Summaries: 跨院出院病歷摘要、重症病程時間軸、手術處置、出院帶藥與跨專科照護計畫).
  Use whenever asked to organize raw MediCloud text/files, generate medical Word reports,
  format clinical histories, or produce bilingual (Traditional Chinese / English) medical summaries.
---

# 健保雲端資料庫雙軌資訊處理與病歷摘要技能 (medicloud-records-processor)

本技能封裝了將 **衛生福利部中央健康保險署「健保醫療資訊雲端查詢系統 (NHI MediCloud)」** 所擷取之多元巨量醫療資訊，自動判讀、歸納、分類為**兩大標準化臨床資訊體系 (Format A / Format B)**，並產出符合高階醫學中心標準之出版級 Word (`.docx`) 繁體中文與專業英文雙語摘要的完整標準作業程序 (SOP)。

---

## 1. 健保雲端資訊雙軌分類矩陣 (Classification Matrix)

健保雲端系統涵蓋病患於各級醫療院所之跨院就醫紀錄。在臨床病史整理與整合照護時，**必須明確區分為兩大獨立之資訊處理架構**：

| 維度項目 | **Format A：檢驗檢查與診斷報告類**<br>(Diagnostic & Lab Reports) | **Format B：跨院出院病歷摘要類**<br>(Hospital Discharge Summaries) |
| :--- | :--- | :--- |
| **資料本質** | 橫斷面與歷程性之客觀檢驗數值與診斷影像 | 住院期間完整重大急重症病程、介入處置與出院計畫 |
| **涵蓋雲端項目** | • 檢驗檢查結果 (成人健檢、生化、血液、尿液)<br>• 放射影像診斷報告 (X-ray, CT, MRI, 超音波)<br>• 組織病理報告 (Pathology / Biopsy)<br>• 內視鏡報告 (胃鏡、大腸鏡、支氣管鏡)<br>• 西醫門診用藥紀錄與慢性病連續處方箋<br>• 過敏藥物與不良反應紀錄 | • 跨院住院/出院病歷摘要 (ICU/病房)<br>• 住院臆斷 (Admission Impressions)<br>• 出院診斷 (Discharge Diagnoses)<br>• 主訴與現病史 (CC & HPI)<br>• 重大處置與手術 (PTMC, 支架, 氣切, CVVH/HD)<br>• 各階段病程演變時間軸 (Timeline)<br>• 出院帶藥 (Discharge Medications)<br>• 出院照護與跨科追蹤計畫 |
| **臨床核心目的** | 慢性病追蹤、三高代謝指標評估、動脈硬化心血管風險 (ASCVD) 分級、用藥交互作用檢查 | 急重症轉銜照護、重大器官衰竭復原評估、重大傷病追蹤、術後與中風復健規劃 |
| **標準範本檔名** | `MediCloud-檢驗檢查與診斷報告範本.docx` | `MediCloud-跨院出院病歷摘要範本.docx` |
| **典型代表病患** | 林淑美（成人健檢、高血脂追蹤、門診照護） | 曾詠聖（義大醫院 58 天多重器官衰竭出院摘要） |

---

## 2. Format A：檢驗檢查與診斷報告類處理規範

### 2.1 適用情境
當原始檔案主要包含：**成人預防保健結果、門診血液生化追蹤、慢性病指標、影像檢查文字報告或常規處方箋**時採用。

### 2.2 標準章節架構
1. **病人基本資訊表 (Header Table, 3×4)**：
   - 病人姓名、病歷號、性別／年齡、查詢日期（國曆/西元）、查詢院所/醫師、查詢目的。
2. **一、重點摘要 (Clinical Executive Summary)**：
   - 以高密度 Callout 框 (`#1B365D` 左邊粗框 + `#F4F7FA` 底色) 條列：
     * **過敏／不良反應**：無紀錄需明確宣告。
     * **目前用藥重點**：近三個月慢箋與常規西藥。
     * **重要檢驗／檢查重點**：標註主要異常（如 LDL-C、eGFR、AC Glucose、AST/ALT）。
     * **近期檢查／影像結論**：超音波、X-ray 關鍵發現。
     * **臨床綜合觀察與處置指引**：ASCVD 風險評估、生活型態介入（飲食/運動/減重目標）、藥物介入時機與年度複查指標。
3. **二、結構化檢驗數據歷程追蹤比較表 (Laboratory Tracking Table)**：
   - 採 **6 欄位標準表格**：`[檢查類別 | 檢驗/檢查項目 | 最近一次檢查值 | 上一次檢查值 | 參考標準值/單位 | 臨床判讀與趨勢分析]`
   - **異常數值顯著化**：異常值以深紅粗體字 (`#B40000`) 搭配淡紅底色 (`#FFF0F0`)；改善數值以綠字 (`#006400`) 標示。
4. **三、西醫用藥紀錄**：條列處方明細，無紀錄則標註「［近三個月無慢箋申報紀錄］」。
5. **四、放射影像與病理報告**：整理報告之 Findings 與 Impression。
6. **五、過敏藥物**：登載之藥物過敏史。
7. **六、近期住院/出院病歷**：確認近期是否有重大住院。

---

## 3. Format B：跨院出院病歷摘要類處理規範

### 3.1 適用情境
當原始檔案為**醫學中心/區域醫院上傳之出院病歷摘要 (Discharge Summary)**，包含住院經過、重症加護、侵入性手術或重大傷病時採用。

### 3.2 標準章節架構
1. **病人與住院基本資訊表 (Header Table, 3×4)**：
   - 姓名、身分證字號、病歷號、性別/年齡/生日、住院日期～出院日期（總住院天數）、出院科別與床號、主治醫師、轉入/轉出醫院代碼。
2. **一、重大住院與出院核心綱要 (Executive Hospital Summary)**：
   - **過敏與不良反應史**：含住院期間藥物疹與處置。
   - **重大器官功能演變與恢復**：如急性腎損傷 KDIGO III 透析起訖與恢復、呼吸衰竭氣切脫離、腦中風、多重菌血症治癒。
   - **關鍵手術與介入處置**：如 PTMC 瓣膜擴張術、心導管支架、氣切、CVVH/HD。
   - **出院帶藥核心方向**：抗血小板、心衰竭、利尿劑、甲狀腺素、氣道支持。
   - **出院照護與整合追蹤要點**：跨科回診、氣切造口、鼻胃管灌食與水分管控。
3. **二、臨床診斷與主訴現病史 (Diagnoses & Presentation)**：
   - **出院診斷 (Discharge Diagnoses)**：完整標註中文與英文醫學術語、重大傷病發卡狀況。
   - **主訴與現病史**：發病原因、轉院經過、急診生命徵象、初始關鍵檢驗與影像。
4. **三、住院治療經過時間軸 (Chronological Hospital Course Timeline)**：
   - **嚴格按時間與照護場域分階段重構**（如：MICU 階段 1 → MICU 階段 2 → RCC 呼吸照護中心 → MICU 重症救援 → 普通病房復健與出院）。
5. **四、檢驗數據與微生物培養追蹤 (Laboratories & Microbiology)**：
   - 出院前動態檢驗對照表（CBC, BUN/Cr, eGFR, K, Na, CRP, 肝膽指標）。
   - 微生物培養表（採檢日、檢體種類、分離菌種、藥敏與抗生素處置）。
6. **五、影像與特殊檢查總結表 (Imaging & Special Procedures)**：
   - 包含 Brain CT/CTA/CTP、心臟超音波 (TTE/TEE)、PTMC 手術、腹部 CT、大腸鏡、CXR。
7. **六、出院帶藥明細表 (Discharge Medications Table, 7 欄位)**：
   - `[項次 | 藥品名稱與規格 | 單次劑量 | 用法頻率 | 給藥途徑 | 總量 | 臨床適應症與藥理機轉說明]`
8. **七、出院指示與跨專科追蹤照護計畫 (Discharge Care Plan)**：
   - 條列心臟、神經中風復健、新陳代謝、胸腔氣切門診回診時間與居家照護警訊。

---

## 4. Word 排版美學與技術規範 (Document Architecture)

為確保產出具備醫療專業感與權威性，所有 Word 檔案必須遵循以下規範：

1. **色彩系統 (Medical Navy Palette)**：
   - 主要標題與抬頭表格底色：`#1B365D` (Pantone Classic Navy)
   - 次級標題與副標：`#2E5B82` / `#43547E`
   - 表格格線：`#B0C4DE` (Light Steel Blue)
   - 斑馬紋交替底色：`#F4F7FA`
   - 異常指標警示：字體深紅 `#B40000`，背景淡紅 `#FFF0F0`
   - 改善指標提示：字體綠色 `#006400`，背景淡綠 `#F0FFF0`
2. **字型設定**：
   - 中文版：標題與內文以 `微軟正黑體` 為主，西文/數字搭配 `Calibri`。
   - 英文版：全篇統一採用 `Calibri`，大小適中（大標 16pt、一級標題 13.5pt、二級標題 11.5pt、表格內文 8.5-9pt）。
3. **表格與儲存格邊界 (Cell Padding)**：
   - 必須透過 XML 設定 `w:tcMar`（Top/Bottom: 80-100 dxa, Left/Right: 100-140 dxa），嚴禁文字緊貼邊線。
4. **版面配置防護 (XML sectPr Protection)**：
   - 在清除範本段落時，必須保留最後之 `<w:sectPr>`，以確保範本原有邊界、頁首頁尾與橫式/直式設定完整無損。

---

## 5. 雙語翻譯與醫學名詞對照標準 (Bilingual Guidelines)

當使用者要求「翻譯為英文」或產出英文版時：
1. **專有名詞規範**：
   - 健保雲端：`National Health Insurance MediCloud System (NHI MediCloud)`
   - 成人健檢：`Adult Preventive Health Screening`
   - 經皮二尖瓣氣球成型術：`Percutaneous Transvenous Mitral Commissurotomy (PTMC)`
   - 氣切造口術：`Tracheostomy`
   - 連續靜脈-靜脈血液濾過：`Continuous Veno-Venous Hemofiltration (CVVH)`
   - 血液透析：`Intermittent Hemodialysis (HD)`
   - 呼吸照護中心：`Respiratory Care Center (RCC)`
   - 重大傷病證明：`Catastrophic Illness Certificate`
2. **陰性與無紀錄陳述標準**：
   - 無過敏：`No known drug allergies (NKDA) registered in the NHI database.`
   - 無慢箋：`No active chronic refill prescriptions within the past 3 months.`
   - 無住院：`No inpatient hospitalizations recorded within the past year.`
3. **藥品名稱**：採用國際非專利學名 (Generic Name) 搭配常用商品名，如 `Clopidogrel (Plavix)`, `Levothyroxine (Eltroxin)`.

---

## 6. 自動化處理工具與腳本

本技能包含自動化 CLI 腳本：
`C:\Users\YangminRoom1\.agents\skills\medicloud-records-processor\scripts\process_medicloud.py`

### 常用命令指令：
```bash
# 自動判斷分類並產生中英雙語 Word 檔
python "C:\Users\YangminRoom1\.agents\skills\medicloud-records-processor\scripts\process_medicloud.py" --input "<檔案路徑>" --category auto --lang both

# 強制以 Format A (檢驗檢查類) 處理
python "C:\Users\YangminRoom1\.agents\skills\medicloud-records-processor\scripts\process_medicloud.py" --input "<檔案路徑>" --category lab --lang zh

# 強制以 Format B (出院病歷摘要類) 處理並產出英文版
python "C:\Users\YangminRoom1\.agents\skills\medicloud-records-processor\scripts\process_medicloud.py" --input "<檔案路徑>" --category discharge --lang en
```

### 範本實體路徑：
- Format A: `C:\Users\YangminRoom1\Documents\Dr Chu's file\Word Documents\_Templates\MediCloud-檢驗檢查與診斷報告範本.docx`
- Format B: `C:\Users\YangminRoom1\Documents\Dr Chu's file\Word Documents\_Templates\MediCloud-跨院出院病歷摘要範本.docx`
- 基礎母範本: `C:\Users\YangminRoom1\Documents\Dr Chu's file\Word Documents\_Templates\MediCloud-健保雲端摘要範本.docx`
