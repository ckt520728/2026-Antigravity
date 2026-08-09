# 🩺 臨床檢查紀錄與報告系統 (Google Spark 2026) 專案總結與陷阱避坑指南
> **Project Wrap-Up & Technical Pitfalls Guide**  
> *記錄者：朱國大醫師 (Dr. Kwo-Ta Chu, MD, PhD) x Antigravity AI Agent*

---

## 1. 專案概述 (Project Summary)

本專案旨在為臨床醫師打造一套高效、直覺且兼具法規/審計需求之**四合一臨床檢查報告系統**（涵蓋心臟超音波 Echo、腹部超音波 Abdominal Sono、上消化道內視鏡 UGI、下消化道內視鏡 LGI）。

### 核心三層式架構 (Three-Tier Architecture)
1. **前端診斷互動網頁 (Web App)**：
   - 全響應式深色微光玻璃美學 (Dark Glassmorphism UI)。
   - 結構化下拉選單、單複選標籤、數字保留空格與實時文字組合引擎 (Real-time Text Synthesis Engine)。
   - 臨床常用速填按鈕 (Preset Buttons) 與完全自由編輯區。
2. **後端資料庫 (Google Sheets 流水帳紀錄 Master Log)**：
   - 記錄操作醫師、檢查時間、病歷號/姓名、臨床診斷、檢查所見。
   - `Master_Exams` 總表 + 4 個獨立檢查分頁，自動生成歸檔。
3. **醫療報告文件產出 (Google Docs / PDF / Word)**：
   - 每筆紀錄送出時自動於 Google Drive 之 `臨床檢查報告_GoogleDocs` 資料夾內建立正規格式之 Google Doc。
   - 即時導出與轉換為 Word (`.docx`) 與 PDF (`.pdf`) 提供直連下載。

---

## 2. 遭遇之技術陷阱與解決方案 (Pitfalls & Lessons Learned)

在開發與部署 Google Apps Script (GAS) 結合 Google Sheets / Docs / Clasp 的過程中，我們歸納出以下關鍵避坑指南：

### 🛑 陷阱 1：Google Apps Script API 未開啟導致 `clasp push` 失敗
- **問題現象**：執行 `clasp push` 或 `clasp create-deployment` 時出現 `User has not enabled the Google Apps Script API` 錯誤。
- **原因分析**：Google 帳號預設關閉 Apps Script API 權限。
- **解決方案**：必須請使用者訪問 [https://script.google.com/home/usersettings](https://script.google.com/home/usersettings) 並將 **Google Apps Script API 設為 ON** 後，才能由 CLI 自動推播代碼與部署。

### 🛑 陷阱 2：Bounded Script 與 Standard Alone Script 的 `parentId` 綁定關係
- **問題現象**：在雲端硬碟建立獨立的 Script 後，無法直接用 `SpreadsheetApp.getActiveSpreadsheet()` 取得目標試算表。
- **原因分析**：Standalone Script 與試算表未進行容器綁定 (Container Bound)。
- **解決方案**：在 `.clasp.json` 中配置 `parentId: ["<Sheet_ID>"]` 重新進行 `clasp clone`，或者在程式碼中顯式使用 `SpreadsheetApp.openById('<Sheet_ID>')` 搭配 Drive 存取。

### 🛑 陷阱 3：Web App 發布存取權限 (ExecuteAs vs Access)
- **問題現象**：醫師存取 Web App 時出現 `Authorization Required` 或是普通使用者無法寫入 Sheets/Docs 的權限問題。
- **原因分析**：`appsscript.json` 缺少 `webapp` 設置，或是存取權限設為僅限自己。
- **解決方案**：在 `appsscript.json` 顯式設定：
  ```json
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE"
  }
  ```
  讓 Web App 透過部署者 (USER_DEPLOYING) 權限執行，使用者無須為 Sheets/Docs 額外申請開通寫入權限。

### 🛑 陷阱 4：Google Docs 轉換 Word/PDF 之 URL 匯出格式
- **問題現象**：直接調用 API 轉檔可能會遇到複雜的 Drive Service API 限制，或是調用速度過慢。
- **解決方案**：採用直連匯出 URL 語法（URL Export Scheme），由前端或後端傳回特定 URL：
  - 📄 **Google Doc 原檔**：`https://docs.google.com/document/d/{docId}/edit`
  - 📥 **Word 檔 (DOCX)**：`https://docs.google.com/document/d/{docId}/export?format=docx`
  - 📕 **PDF 檔**：`https://docs.google.com/document/d/{docId}/export?format=pdf`

### 🛑 陷阱 6：新增 Google API 服務後 Web App 轉址至 `script.google.com/home`
- **問題現象**：點擊發布的 Web App 網址（`/exec`）沒有載入 HTML 網頁，而是被重定向引導回 Google Apps Script 儀表板 (`script.google.com/home` "我的專案")。
- **原因分析**：專案引入了未授權的 Google API 服務（例如 `LanguageApp` 翻譯服務、`DocumentApp` 報告生成服務）。在專案擁有者授權前，GAS 會阻擋 Web App 執行。
- **解決方案**：
  1. 專案擁有者開啟 Apps Script 編輯器 (`script.google.com/d/<scriptId>/edit`)。
  2. 選擇任一函式點擊「執行 (Run)」。
  3. 於彈出視窗完成「審查權限 (Review Permissions)」➔「進階」➔「允許 (Allow)」。
  4. 重新存取 `/exec` 網址即可正常開啟互動網頁。

---

## 3. 系統資源與關鍵連結 (System Resources)

| 資源名稱 | 連結 / 路徑 |
| :--- | :--- |
| 🌐 **正式版 Web App 網頁 (公開連結)** | [開啟 Web App](https://script.google.com/macros/s/AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g/exec) |
| 📊 **Google Sheets 流水帳** | [開啟試算表](https://drive.google.com/open?id=1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY) |
| ⚙️ **Apps Script 編輯器** | [開啟 Script 專案](https://script.google.com/d/1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL/edit) |
| 📁 **Google Docs 報告資料夾** | Drive 內 `2026 Google Spark/臨床檢查報告_GoogleDocs` |
