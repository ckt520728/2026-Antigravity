# 📋 臨床醫療紀錄與住院病歷系統 v5.0 (Clinical Documentation & Admission Note System)
> **2026 Google Spark x Google Apps Script Cloud Engine**  
> *專為朱國大醫師 (Dr. Kwo-Ta Chu) 及臨床團隊打造之住院病歷撰寫 (Admission Note)、中文語音轉英文醫療翻譯、選單化檢查報告生成、Google Sheets 流水帳與 Google Docs/PDF/Word 自動產出系統*

---

## 🔗 線上系統與資源連結

- 🌐 **正式版 Web App 網頁應用程式網址 (公開存取入口)**：  
  [https://script.google.com/macros/s/AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g/exec](https://script.google.com/macros/s/AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g/exec)
- 📊 **Google 雲端試算表 (主資料庫 / 流水帳紀錄)**：  
  [開啟 2026 Google Spark 試算表](https://drive.google.com/open?id=1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY)
- ⚙️ **Google Apps Script 腳本編輯器**：  
  [開啟 Apps Script 線上編輯器](https://script.google.com/d/1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL/edit)

---

## 📋 住院病歷撰寫系統 (Admission Note & Speech-to-Text Translation)

本系統新增全新**住院病歷 (Admission Note) 模組**，支援下列臨床核心功能：

1. **中文語音輸入轉英文文字 (Speech-to-Text + Machine Translation)**：
   - 在主訴 (CC) 與現在病史 (HPI) 欄位旁提供 `🎙️ 語音輸入 (中文)` 按鈕，醫師可直接口述中文（如「右下腹劇痛伴隨發燒三天」）。
   - 點擊 `🌐 轉為英文醫學描述` 按鈕，調用 Google Cloud Language Engine 自動轉譯為符合國際病歷規範之英文描述 (e.g., "Right lower quadrant abdominal pain for 3 days accompanied by fever")。
2. **三核心病患資料結構**：
   - **基本資料 (Demographics)**：病歷號 (MRN)、病患姓名、年齡與性別、入院日期、病房與床號、主治醫師、診斷科別。
   - **主訴 (Chief Complaint, CC)**：文字輸入 / 語音轉譯 / 常用主訴速填標籤。
   - **現在病史 (History of Present Illness, HPI)**：支援 **LQQOPERA** (Onset, Location, Quality, Severity, Associated Symptoms, Relieving/Aggravating Factors) 結構化速填晶片。
3. **延伸完整臨床評估**：
   - **過去病史與過敏史 (PMH & Allergies)**：單複選高血壓、糖尿病、CKD、CAD、Stroke 等慢性病晶片，過敏史預設 NKDA。
   - **理學檢查 (Physical Examination & Vital Signs)**：生命徵象 (BP, HR, RR, Temp, SpO2) 與器官系統理學檢查評估。
   - **初步診斷與處置計畫 (Impression & Admission Plan)**：問題清單、鑑別診斷與入院治療處置計畫。
4. **一鍵跨平台匯出**：
   - 自動將病歷寫入 Google Sheets `Master_AdmissionNotes` 頁籤。
   - 自動於 Google Drive 建立正規格式之 **Google Doc 病歷報告**。
   - 即時提供 **Word 檔 (.docx)** 與 **PDF 檔 (.pdf)** 直連下載連結。

---

## 📄 三層式架構設計 (Sheets / Docs / Web App)

1. **互動式 Web App**：醫師打報告與病歷使用的前端互動網頁，支援中文語音轉英文、結構化單複選標籤、數字留白填空與實時文字組合引擎。
2. **Google Sheets 流水帳紀錄**：後端資料庫（`Master_AdmissionNotes` 與 `Master_Exams` 頁籤），記錄操作醫師、時間、病歷號/姓名、臨床診斷、病史與檢查所見，以及自動生成之 Docs / PDF / Word 下載連結。
3. **Google Docs 醫療報告**：送出報告時自動於 Google Drive 之 `住院病歷報告_GoogleDocs` / `臨床檢查報告_GoogleDocs` 資料夾內建立正規格式的 Google Doc 醫療報告，並即時提供轉存 **Word (`.docx`)** 與 **PDF (`.pdf`)** 之直連下載連結。


---

## ✨ 選擇性醫學報告生成器與數字填空

本系統已全數完成四大檢查項目的**結構化下拉選單、單複選標籤與數字保留空格**。醫師點選選單或於空格填入數值時，系統將**即時自動組合生成符合醫學標準規範之英文與中文臨床報告**：

### 1. ❤️ 心臟超音波 (Echocardiogram)
- **數值填空**：`LVEF %`、`LVEDD / LVESD (mm)`、`IVS / LVPW (mm)`、`LA Diameter (mm)`、`PASP (mmHg)`
- **可選項目**：
  - LV 壁運動 (Normal global / Global hypokinesia / Regional wall motion abnormality)
  - 舒張功能 (Normal / Grade I-III Diastolic dysfunction)
  - 瓣膜評估 (Aortic Sclerosis, Mild/Mod/Sev AR, MR, MS, TR)
  - 心包膜積液 (None / Trivial / Mild / Moderate)
- **快速診斷範本**：`正常心音圖 (Normal)`、`高血壓心臟病 (HHD)`、`缺血性心臟病 (IHD/RWMA)`、`收縮功能下降 (HFrEF, EF<40%)`

### 2. 🩺 腹部超音波 (Abdominal Sonography)
- **數值填空**：`膽總管 CBD Diameter (mm)`、`脾指數/長度 (cm)`、`腎臟大小 (cm)`、`腎結石/囊腫尺寸 (cm/mm)`
- **可選項目**：
  - 肝臟實質 (Normal / Mild, Mod, Sev Fatty Liver / Cirrhotic pattern)
  - 肝臟局部病灶 (Cyst, Hemangioma, Hypoechoic nodule, Calcification)
  - 膽囊與膽管 (Normal, GB Stone, GB Polyp, GB Wall thickening, Post-cholecystectomy)
  - 雙腎與腹水 (Normal, Renal Cysts, Hydronephrosis Gr I-IV, Ascites)
- **快速診斷範本**：`正常腹超 (Normal)`、`輕/中度脂肪肝 (Fatty Liver)`、`膽結石與雙腎囊腫 (GB Stone & Cysts)`、`肝硬化脾腫大 (Cirrhosis & Splenomegaly)`

### 3. 🔍 上消化道內視鏡 (UGI Endoscopy / 胃鏡)
- **數值填空**：`切齒至 GEJ 距離 (cm)`、`潰瘍/病灶尺寸 (cm/mm)`、`切片片數`
- **可選項目**：
  - 食道與 GEJ (Normal / GERD LA Grade A/B/C/D / Candidiasis / Varices / Hiatal Hernia)
  - 胃部 (Superficial, Erosive, Atrophic, Hemorrhagic Gastritis)
  - 胃潰瘍分期 (Gastric Ulcer Active A1/A2, Healing H1/H2, Scar S1/S2)
  - 十二指腸與 CLO Test (Duodenitis, Duodenal Ulcer, CLO test +/-)
- **快速診斷範本**：`正常胃鏡 (Normal EGD)`、`胃食道逆流 A 級 (GERD LA Grade A)`、`糜爛性胃炎 (Erosive Gastritis)`、`胃潰瘍 A2 期 (Gastric Ulcer A2)`

### 4. 🌀 下消化道內視鏡 (LGI Endoscopy / 大腸鏡)
- **數值填空**：`退鏡時間 (mins)`、`息肉尺寸 (mm)`、`切片/切除個數`
- **可選項目**：
  - 進鏡最遠範圍 (Cecum & TI / Cecum / Splenic Flexure / Sigmoid)
  - 清腸評分 (Boston Bowel Prep Score BBPS 9/9, 7-8/9, 6/9)
  - 息肉型態與部位 (Yamada I-IV / Sigmoid, Rectum, Colon polyps)
  - 息肉切除處置 (Cold Snare Polypectomy CSP, EMR, Biopsy)
  - 憩室、大腸炎與痔瘡 (Diverticulosis, Proctitis/IBD, Internal/External Hemorrhoids)
- **快速診斷範本**：`正常大腸鏡 (Normal Colonoscopy)`、`大腸息肉冷剪切除 (Polypectomy S/P)`、`憩室與內痔 (Diverticulosis & Hemorrhoids)`

---

## 🎨 介面美學與流暢互動
- **選單＋自動組合**：醫師點選任何下拉選項或填入數字，底部 `影像詳細所見 (Findings)`、`初步診斷 (Diagnosis)` 與 `檢查結論 (Impression)` 將同步實時更新。
- **完全自由編修**：自動生成的文字可自由在文字框內進行人工補充修改，兼具速度與靈活性。
- **一鍵導出文件**：儲存後跳出成功視窗，直接提供 **Google Doc**、**PDF 檔** 與 **Word 檔** 的點擊預覽與下載，兼顧臨床記錄與論文/列印需求。
