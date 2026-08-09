# 🩺 臨床檢查紀錄與報告系統 v4.0 (Clinical Examination System)
> **2026 Google Spark x Google Apps Script Cloud Engine**  
> *專為臨床醫師打造的選單化、模組化、數字空格快速報告生成、Google Sheets 流水帳與 Google Docs/PDF/Word 自動產出系統*

---

## 🔗 線上系統與資源連結

- 🌐 **最新版 Web App 網頁應用程式網址 (公開連結 / 免登入即可存取)**：  
  [https://script.google.com/macros/s/AKfycbxCBy06wQFcy9GwjN_7e-5keX7_SeXudpWi7YTHkBkCJUhZ29XBK0ZeUPifkpyTOcI7Rw/exec](https://script.google.com/macros/s/AKfycbxCBy06wQFcy9GwjN_7e-5keX7_SeXudpWi7YTHkBkCJUhZ29XBK0ZeUPifkpyTOcI7Rw/exec)
- 📊 **Google 雲端試算表 (主資料庫 / 流水帳紀錄)**：  
  [開啟 2026 Google Spark 試算表](https://drive.google.com/open?id=1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY)
- ⚙️ **Google Apps Script 腳本編輯器**：  
  [開啟 Apps Script 線上編輯器](https://script.google.com/d/1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL/edit)

---

## 📄 三層式架構設計 (Sheets / Docs / Web App)

1. **互動式 Web App**：醫師打報告使用的前端互動網頁，支援結構化單複選標籤、數字留白填空與實時文字組合引擎。
2. **Google Sheets 流水帳紀錄**：後端資料庫（`Master_Exams` 與四大檢查分頁），記錄操作醫師、檢查時間、病歷號/姓名、臨床診斷、檢查所見，以及自動生成之 Docs / PDF / Word 下載連結。
3. **Google Docs 醫療報告**：送出報告時自動於 Google Drive 之 `臨床檢查報告_GoogleDocs` 資料夾內建立正規格式的 Google Doc 醫療報告，並即時提供轉存 **Word (`.docx`)** 與 **PDF (`.pdf`)** 之直連下載連結。

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
