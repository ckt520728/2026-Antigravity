# 📋 臨床醫療紀錄與住院病歷系統 v6.0 (Clinical Documentation & Admission Note System)
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

> ⚠️ **請務必使用上方 `/exec` 網址開啟**。直接點開雲端硬碟資料夾裡的 `index.html` 只會開到原始碼，`google.script.run` 不存在，畫面會顯示「無法連線到後端」的紅色提示。

---

## 🔐 存取方式與密碼

- 系統目前設定為 **`ANYONE_ANONYMOUS`**：**任何人有連結即可開啟，不需要 Google 帳號**。
- **密碼入口目前為關閉狀態**，開啟連結直接進入系統，底部狀態列顯示「密碼保護：關閉中」。
- 密碼機制已完整實作（加鹽 SHA-256 雜湊存於 Script Properties、12 小時無狀態簽章 session token、每支後端函式驗證、連續輸錯 8 次鎖 15 分鐘），只是被 `Code.gs` 最上方的總開關關掉。

要啟用密碼：`Code.gs` 的 `var AUTH_ENABLED = false;` 改成 `true` → 執行一次 `setAppPasscode` 設定密碼 → 重新部署（務必帶 `-i <既有 deploymentId>`）。詳細步驟見 `handoff.md`。

---

## 📄 三層式架構設計 (Sheets / Docs / Web App)

1. **互動式 Web App**：醫師打報告與病歷使用的前端互動網頁，支援中文語音轉英文、結構化單複選標籤、數字留白填空與實時文字組合引擎。
2. **Google Sheets 流水帳紀錄**：後端資料庫（`Master_AdmissionNotes` 與 `Master_Exams` 頁籤），記錄操作醫師、時間、病歷號/姓名、臨床診斷、病史與檢查所見，以及自動生成之 Docs / PDF / Word 下載連結。
3. **Google Docs 醫療報告**：送出報告時自動於 Google Drive 之 `住院病歷報告_GoogleDocs` / `臨床檢查報告_GoogleDocs` 資料夾內建立正規格式的 Google Doc 醫療報告，並即時提供轉存 **Word (`.docx`)** 與 **PDF (`.pdf`)** 之直連下載連結。

---

## 🏥 住院病歷撰寫系統 (Admission Note)

v6.0 依教學醫院標準 H&P 範本重整為 **9 個區段**，並全面中英並列。

### 1. 病患基本資料 (Patient Demographics)
病歷號 (MRN)、姓名、年齡與性別、入院日期、病房床號、主治醫師、診斷科別，以及 **病史提供者 (Informant)** 與 **可信度 (Reliability)**。
右上角顯示 **距入院後 24 小時 H&P 完成期限**還剩多久（依 CMS 規範），剩 6 小時內轉為警示色。

### 2. 主訴 (Chief Complaint, CC)
- `🎙️ 語音輸入 (中文)`：口述中文（如「右下腹劇痛伴隨發燒三天」）。
- `🌐 轉為英文`：呼叫 `LanguageApp` 轉譯為英文病歷描述。
- 10 組常用主訴速填晶片。

### 3. 現在病史 (History of Present Illness, HPI)
同樣支援語音與英譯，並提供 **LQQOPERA 結構化速填晶片**，分五組：Onset、Location/Quality、Severity/Associated、Relieving/Aggravating、**ED course（急診經過）**。

### 4. 過去病史、手術史、用藥與過敏
- **PMH**：12 項常見慢性病複選（HTN、T2DM、CKD、CAD、Stroke、Dyslipidemia、Gout、Asthma/COPD、AF、HF、Cirrhosis、Malignancy），可自由補充。
- **手術史 (PSH)** 🆕：速填晶片（否認、膽囊切除、闌尾切除、PCI、動靜脈瘻管、剖腹產）。
- **目前用藥 (Medications)** 🆕：用藥整合 (reconciliation)，8 組常用藥速填。
- **過敏史 (Allergies)**：預設 NKDA，另提供 Penicillin／NSAIDs／Sulfa／顯影劑／海鮮等速填。
- 一鍵 **「全部 non-contributory」**。

### 5. 家族史與個人社會史 🆕
- **家族史**：8 項可複選晶片自動組句。
- **社會史**：吸菸（含 pack-year）、飲酒、**嚼檳榔**、職業、**TOCC 旅遊接觸史**、生活功能 (ADL)。
- 一鍵 **「菸酒檳榔皆否認」**。

### 6. 系統回顧 (Review of Systems, ROS) 🆕
**10 大系統、約 55 個症狀**，採**三態晶片**：點 1 次 ＋（陽性）、2 次 －（陰性）、3 次取消。
一鍵 **「全部否認」**把 10 系統標成陰性，再把陽性症狀點成 ＋ 即可。
系統：General／HEENT／Respiratory／Cardiovascular／Gastrointestinal／Genitourinary／Musculoskeletal／Neurological／Skin／Endocrine-Hematologic。

### 7. 生命徵象與理學檢查 (Vital Signs & Physical Examination)
- **生命徵象**：BP、HR、RR、Temp、SpO2、體重、身高、**BMI 自動計算**、疼痛評分、GCS。
- **分系統理學檢查** 🆕：General／HEENT／Neck／Chest／Heart／Abdomen／Back／Extremities／Neurological／Skin 共 10 個系統，每個都有標準正常敘述與常見異常速填晶片。
- 一鍵 **「全部填入正常」**，再修改有異常的系統。

### 8. 入院檢驗與影像 (Admission Laboratory & Imaging) 🆕
CBC、生化、發炎指標、尿液檢查、胸部 X 光、心電圖、其他檢查。一鍵 **「標記為 pending」**。

### 9. 問題導向初步診斷與處置計畫 (Problem-based Assessment & Plan) 🆕
不再是兩個各自為政的文字方塊，改為**一個 problem 對應一段 plan** 的條列，可自由新增／刪除。
內建 6 個常用入院情境一鍵帶入：急性闌尾炎、社區型肺炎 (CAP)、AKI on CKD、急性心衰竭 (ADHF)、腎盂腎炎／UTI、上消化道出血 (UGIB)。

### 實時預覽與匯出
底部提供完整英文病歷的實時預覽，可 **一鍵複製全文**（直接貼回院內 HIS）或 **列印**。
按「儲存」後自動寫入 `Master_AdmissionNotes`，並產出 Google Doc、PDF、Word 三個連結。

---

## ✨ 選擇性醫學報告生成器與數字填空

四大檢查項目全部採**結構化下拉選單、單複選標籤與數字保留空格**；醫師點選選單或填入數值時，底部 `Findings`、`Diagnosis`、`Impression`、`Recommendation` **即時自動組合生成**。

v6.0 依 **RSNA 結構化報告**標準，四個模組共用固定段落順序：
**臨床適應症 (Indication) → 檢查技術 (Technique) → 比較影像 (Comparison) → 詳細所見 (Findings) → 結論 (Impression) → 建議 (Recommendation)**。
切換檢查項目時會自動帶入該項目的預設檢查技術描述。

> 🔒 **手動編輯保護**：`Findings` 等四個自動產生的欄位，只要你手動改過就**不會再被覆寫**，畫面會顯示「N 個欄位已手動編輯，不會被覆寫」。要重新套用選項請按「依選項重新生成」。

### 1. ❤️ 心臟超音波 (Echocardiogram) — 依 ASE 報告標準化建議
- **數值填空**：`LVEF %`、`LVEDD / LVESD (mm)`、`IVS / LVPW (mm)`、`LA Diameter (mm)`、`PASP (mmHg)`、**檢查當下血壓** 🆕
- **可選項目**：
  - LV 壁運動 (Normal global / Global hypokinesia / RWMA — Anteroseptal, Inferior, Apical)
  - 舒張功能 (Normal / Grade I-III)
  - **右心室功能 (RV / TAPSE)** 🆕、**下腔靜脈 IVC 與容積狀態** 🆕
  - 瓣膜評估 (AV / MV / TV)
  - 心包膜積液 (None / Trivial / Mild / Moderate)
  - **顯影劑與 Bubble study (UEA / agitated saline)** 🆕
- **自動結論分級** 🆕：LVEF <40%（HFrEF）／40–49%（輕度下降）／≥50%（保留）各自給出不同結論與追蹤建議。
- **快速範本**：正常、高血壓心臟病 (HHD)、缺血性 (IHD/RWMA)、收縮功能下降 (HFrEF)

### 2. 🩺 腹部超音波 (Abdominal Sonography)
- **數值填空**：`CBD Diameter (mm)`、`脾指數 (cm)`、**`腎臟大小 R/L (cm)`** 🆕、腎結石／囊腫尺寸
- **可選項目**：肝臟實質（正常／輕中重度脂肪肝／肝硬化樣）、肝臟局部病灶、肝內膽管、膽囊與膽管、胰臟脾臟、雙腎（含 **CKD 慢性腎病變 pattern** 🆕）、腹水、膀胱
- **快速範本**：正常、脂肪肝、膽結石與腎囊腫、肝硬化脾腫大、**慢性腎病變 (CKD pattern)** 🆕

### 3. 🔍 上消化道內視鏡 (UGI Endoscopy / 胃鏡)
- **數值填空**：**`Z-line 距切齒 (cm)`** 🆕、潰瘍／病灶尺寸、切片片數
- **可選項目**：食道與 GEJ（正常／GERD LA Grade A–D 🆕 補齊 D 級／Candidiasis／Varices／Hiatal Hernia）、胃底胃體、胃竇、胃潰瘍分期 (A1/A2, H1/H2, S1/S2)、十二指腸、CLO Test
- **自動結論**：CLO test 陽性時自動在診斷加註 H. pylori 感染並帶入 14 天除菌療程建議 🆕
- **快速範本**：正常胃鏡、GERD LA-A、糜爛性胃炎、胃潰瘍 A2

### 4. 🌀 下消化道內視鏡 (LGI Endoscopy / 大腸鏡) — 依 ASGE/ACG 2024 品質指標 🆕
- **進鏡最遠範圍**：Cecum & TI／Cecum／Splenic Flexure／Sigmoid
- **清腸評分 (BBPS)**：9/9、7-8/9、6/9、<6（標示建議提早重做）
- **退鏡時間**：目標由舊版的 6 分鐘 **上調為 ≥ 8 分鐘**（ASGE/ACG 2024 更新），低於 8 分鐘即時警示
- **盲腸標誌照相記錄** 🆕：闌尾開口 / 迴盲瓣 / 末端回腸進鏡
- **息肉結構化紀錄** 🆕：可新增多筆，每筆記載 **部位 × 大小 (mm) × 形態 (Paris / Yamada) × 切除方式**；4–9 mm 未選 cold snare 時提示（2024 目標 ≥90%）
- **其他病灶**：憩室與大腸炎、痔瘡、其他處置（如 tattooing）
- **快速範本**：正常大腸鏡、息肉冷剪切除 (CSP)、憩室與內痔

---

## 📈 歷史紀錄與匯出

- **雙分頁**：可切換 **檢查報告** 與 **住院病歷** 兩種紀錄。
- **統計卡片**：總檢查數與四項檢查各自筆數。
- **關鍵字搜尋**：兩種紀錄皆支援。檢查報告可搜尋編號、日期、項目、醫師、病歷代碼、症狀、診斷、所見、結論；住院病歷可搜尋病歷編號、入院日期、MRN、姓名、年齡性別、病房、主治醫師、科別、主訴、現在病史、初步診斷。搜尋後會提示找到幾筆。
- **每筆可檢視詳情**，並直接開啟 Google Doc、下載 PDF 與 Word。

---

## 🎨 介面美學與流暢互動

- **選單＋自動組合**：點選任何選項或填入數字，底部 Findings / Diagnosis / Impression / Recommendation 同步實時更新。
- **完整性配一鍵排除**：每個新增的完整性區段都有對應的一鍵按鈕（全部否認／全部填入正常／non-contributory／標記 pending），確保「更完整」不等於「更花時間」。
- **草稿自動保存** 🆕：每次輸入 1 秒後自動存在這台瀏覽器，關掉分頁再回來會自動還原並提示。
- **一鍵複製全文** 🆕：預覽區右上角，直接貼回院內 HIS。
- **淺色／深色模式** 🆕：右上角切換，長時間閱讀文字建議淺色。
- **列印樣式** 🆕：列印時自動隱藏按鈕與導覽列。
- **必填檢查** 🆕：缺 MRN／主訴／現在病史／至少一個 problem 時標紅並自動捲到該欄位。
- **快速鍵** 🆕：`Ctrl/⌘ + S` 儲存、`Ctrl/⌘ + P` 列印、`Esc` 關閉視窗。
- **手機版面** 🆕：表單、分頁與底部操作列全部單欄自適應。
- **一鍵導出文件**：儲存後跳出成功視窗，直接提供 Google Doc、PDF、Word 的預覽與下載。

---

## ⚠️ 使用注意

- 本系統會將病歷內容寫入 Google Sheets 與 Google Docs（存放於部署者帳號的雲端硬碟）。請依所屬機構的個資與資安規範使用，避免輸入非必要的可識別個資。
- 中文轉英文使用 Apps Script 內建 `LanguageApp`，屬**通用翻譯而非醫學專用翻譯**，翻譯後務必人工檢查醫學用語。
- 語音辨識使用 Web Speech API，僅 Chrome / Edge 等支援的瀏覽器可用；不支援時會顯示提示訊息，可改用鍵盤輸入。

---

## 📚 相關文件

| 文件 | 內容 |
|---|---|
| `handoff.md` | 交接說明：怎麼開、v6 改了什麼、資料在哪、待確認清單 |
| `CLAUDE.md` | 給 AI agent：架構、clasp 指令、修改約束、禁止事項 |
| `docs/reference-templates.md` | 外部範本調研與出處（H&P / RSNA / ASE / ASGE） |
| `01_專案文件/Project_WrapUp_and_Pitfalls.md` | v5.0 以前的部署陷阱與解法 |
