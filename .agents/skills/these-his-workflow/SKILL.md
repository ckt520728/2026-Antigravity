---
name: these-his-workflow
description: >
  Operate, configure, and maintain the THESE (杏翔) Hospital Information System (HIS) on Windows workstations.
  Use when asked to configure test panels, maintain order sets, edit form templates (frmForm020 / frmOC011),
  set up clinical batteries (Nephrology, Cardiology, Neurology, Rheumatology) under Laboratory directory / #001 院長專用,
  or troubleshoot THESE HIS outpatient and inpatient workflows.
---

# THESE (杏翔) 醫療資訊系統工作流程與診斷套組配置技能 (these-his-workflow)

本技能封裝了在 Windows 醫療工作站上操作、逆向分析與維護 **杏翔 (THESE) 醫療資訊系統 (HIS)** 的完整工作流程與踩坑知識庫。

---

## 1. 系統環境與二進位架構規範

* **主要執行檔位置**：`C:\THESE\`
  * 門診看診主程式：`RoomNew.exe` (或 `Room.exe`)
  * 系統總主選單：`ThisMenu.exe` (桌面捷徑 `ThisMenu.lnk` -> `Version.exe`)
  * 住院醫囑與表單模組：`Fdg200k.exe` / `Ids2.exe` / `IdsRoom.exe`
  * 檢驗維護程式：`FexEdit.exe` / `Fex.exe`
  * 影像調閱：`TSDicomViewer.exe`
  * 健保 IC 卡控制軟體：`CS 5.1.5.7`
* **後端資料庫連線**：配置於 `C:\THESE\TheseHIS.ini`，通常連線至區網 Oracle 伺服器 (`192.168.22.1:1521`，帳號 `a114` 或 `ipd`)。

---

## 2. 關鍵表單模型與對照關係 (Form & Database Schema)

在 THESE HIS 中，醫令與檢查分為兩大完全不同的體系，維護時切勿混淆：

| 體系名稱 | 臨床開立視窗 | 後台維護視窗 | 快捷鍵 | 後端主要資料表 | 適用場景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **表單輸入體系 (Form)** | `frmForm020` / `frmForm` (表單輸入) | **`frmOC011` (表單資料維護)** | <kbd>Alt</kbd> + <kbd>G</kbd> | `FOC006K` (表單大類)<br>`FOC012K` (明細項目) | **本案採用**：頁籤式「檢驗單 / #001 院長專用」、「檢查單」、「處置單」等整頁式複選開立。 |
| **常用組套體系 (Series)** | `frmSeries` (組套輸入) | `frmGroup` (新增組套) / `CmdOC007` (組套維護) | <kbd>Alt</kbd> + <kbd>I</kbd> | `FOC008K` (組套主檔) | 處方格鍵入組套代碼（如 `*GN`）呼叫之傳統處方醫令組套。 |
| **片語理由體系 (Phrase)** | 送單理由輸入 | `FrmFOC057K` (檢查理由片語檔維護) | <kbd>Alt</kbd> + <kbd>J</kbd> | `FOC057K` / `FOC057K2` | 檢查/檢驗送單時之臨床適應症理由。 |

---

## 3. 在「檢驗單 / #001 院長專用」配置套組的 SOP

當使用者要求在 **「檢驗單 (Laboratory Directory)」** 或 **「#001 院長專用」** 下新增檢驗項目或套組時，依照以下步驟引導或執行：

1. **進入維護視窗**：
   * 進入 `RoomNew.exe` 門診看診主畫面。
   * 點擊頂端選單 **「維護」** ➔ **「表單資料維護[&G]」**（或按快捷鍵 <kbd>Alt</kbd> + <kbd>G</kbd>），啟動 `frmOC011`。
2. **查詢定位**：
   * 上方查詢條件區：點選單選鈕 ⦿ **「檢驗單」**。
   * 在「代碼」欄鍵入：`#001`，點擊 **「查詢[&Q]」**。
   * 中間表格會列出 `#001 院長專用` 現存項目。
3. **輸入檢驗項目**：
   * 下方資料維護區：單選鈕確認為 ⦿ **「檢驗單」**，代碼為 `#001`。
   * 於「醫令代碼」欄鍵入健保代碼，按 <kbd>Enter</kbd> 系統自動帶出名稱。
   * 點擊 **「確定[&O]」**（快捷鍵 <kbd>Alt</kbd> + <kbd>O</kbd>），新增至項目清單。
4. **完成退出**：
   * 全數建檔完畢後，點擊右下角 **「離開[&X]」**。
5. **門診開立驗證**：
   * 在看診主畫面開啟 `表單輸入--[frmForm020]`。
   * 點選 **「檢驗單」** 頁籤 ➔ 點選 **`#001 院長專用`**。
   * 右側檢驗清單即可進行勾選或 **「全部選取[S]」** ➔ **「加入患者醫令[A]」**。

---

## 4. 四大專科診斷套組代碼速查表 (Diagnostic Battery Registry)

### A. 腎絲球腎炎鑑別套組 (Glomerulonephritis Battery)
* `06012C` 尿液一般常規檢查
* `06013C` 尿沉渣顯微鏡檢查 (RBC casts, Dysmorphic RBC)
* `06014C` + `06015C` 尿蛋白定量 + 尿肌酸酐 (UPCR)
* `09040C` 尿中微量白蛋白 (Microalbumin)
* `09002C` 尿素氮 (BUN)
* `09015C` 肌酸酐 (Creatinine + eGFR)
* `09021C` 電解質 (Na, K, Cl)
* `09025C` 鈣 (Calcium) / `09026C` 磷 (Phosphate)
* `09038C` 白蛋白 (Albumin) / `09039C` 總蛋白 (Total Protein)
* `09001C` 總膽固醇 / `09006C` 低密度脂蛋白 (LDL)
* `12015C` 補體 C3 / `12016C` 補體 C4
* `12038B` 抗核抗體 (ANA)
* `12053B` 雙股去氧核糖核酸抗體 (Anti-dsDNA)
* `12156C` 抗嗜中性白血球細胞質抗體 (ANCA)
* `12185C` 抗腎絲球基底膜抗體 (Anti-GBM)
* `12197C` 抗 PLA2R 抗體 (Anti-PLA2R)
* `12003C` 抗鏈球菌溶血素 O 效價 (ASLO)
* `12014C` 冷凝球蛋白檢查 (Cryoglobulin)
* `12001C` 蛋白電泳分析 (SPEP/UPEP)
* `14001C` B 型肝炎表面抗原 (HBsAg) / `14032C` C 型肝炎抗體 (Anti-HCV)

### B. 急性冠心症／心肌梗塞套組 (ACS / AMI Battery)
* `09099C` (或 `12115C`) 高敏感度心肌肌鈣蛋白 (hs-Troponin I)
* `09031C` 肌酸磷化酶 (CK / CPK)
* `09032C` 肌酸磷化酶同功酶 (CK-MB)
* `12071C` 肌紅蛋白 (Myoglobin)
* `08011C` 全血球計數及分類 (CBC / Platelet)
* `08026C` 凝血酶原時間 (PT / INR)
* `08036C` 部分凝血活酶時間 (aPTT)
* `09002C` BUN / `09015C` Creatinine
* `09021C` 電解質 (Na, K) / `09027C` 鎂 (Magnesium)
* `09005C` 隨機急測血糖 (Glucose STAT)
* `09001C` 總膽固醇 / `09006C` 低密度脂蛋白 (LDL)
* `18001` (或 `18001C`) 十二導程心電圖 (12-Lead ECG)
* `04001C` (或 `34001C`) 胸部 X 光檢查 (Chest X-ray)

### C. 急性腦梗塞缺血性中風急評套組 (Acute Stroke Battery)
* `33001B` 無顯影劑腦部電腦斷層攝影 (Brain CT non-contrast)
* `08011C` 全血球計數及分類 (CBC with diff & Platelet)
* `08026C` 凝血酶原時間 (PT / INR)
* `08036C` 部分凝血活酶時間 (aPTT)
* `09005C` 急測血糖 (Glucose STAT，排除中風擬態)
* `09006C` 糖化血色素 (HbA1c)
* `09002C` BUN / `09015C` Creatinine + eGFR
* `09021C` 電解質 (Na, K, Cl)
* `09001C` 總膽固醇 / `09006C` LDL-C
* `08006C` 紅血球沉降率 (ESR) / `12019C` 高敏感度 C 反應蛋白 (hs-CRP)
* `18001C` 十二導程心電圖 (12-Lead ECG，篩檢心房顫動 AF)
* `09099C` 心肌肌鈣蛋白 (Troponin-I)
* `19001C` 頸動脈超音波檢查 (Carotid Duplex)

### D. 風濕免疫自體免疫疾病套組 (RA, SLE, Sjögren, MCTD Battery)
* `08006C` 紅血球沉降率 (ESR)
* `12019C` 高敏感度 C 反應蛋白 (hs-CRP)
* `08011C` 全血球計數及分類 (CBC with differential)
* `12040C` 類風濕性因子 (Rheumatoid Factor - RF)
* `12152C` 抗環瓜氨酸抗體 (Anti-CCP antibody)
* `12038B` 抗核抗體 (ANA)
* `12053B` 雙股去氧核糖核酸抗體 (Anti-dsDNA)
* `12015C` 補體 C3 / `12016C` 補體 C4
* `12062C` 提取性核抗原抗體譜 (ENA Panel，涵蓋 Anti-Ro/SSA, Anti-La/SSB, Anti-Sm, Anti-U1-RNP, Anti-Scl-70, Anti-Jo-1)
* `06012C` + `06013C` 尿液一般常規與沉渣 (篩檢狼瘡性腎炎)
* `12011C` 免疫球蛋白 G (IgG)
* `08038C` 狼瘡抗凝血因子 (Lupus Anticoagulant - LA)
* `12117C` 抗心脂抗體 (Anti-cardiolipin antibody - aCL)

---

## 5. 常見陷阱 (Pitfalls Checklist)

* **陷阱 1**：切勿將 `frmForm020` 的表單維護誤導至 `CmdOC007` (常用組套)。`CmdOC007` 儲存於 `FOC008K`，無法於 `frmForm020` 的「檢驗單」樹狀目錄顯示。必須使用 **`CmdOC011` / `frmOC011` (表單資料維護，快捷鍵 <kbd>Alt</kbd>+<kbd>G</kbd>)**。
* **陷阱 2**：本地無純文字設定檔。所有分類代碼 (`FOC006K`) 與明細項目 (`FOC012K`) 皆即時連線至區網 Oracle 伺服器，直接在本地搜尋純文字將無法檢索到動態內容。
* **陷阱 3**：程式為 32-bit VB6 架構，終端解析二進位檔必須使用 `cp950` 解碼。
