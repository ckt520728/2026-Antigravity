# CLAUDE.md

臨床醫療紀錄與報告系統 (Clinical Documentation & Admission Note System) — Google Apps Script Web App。
給在這個 repo 工作的 AI agent 的指引。人類用的交接說明在 `handoff.md`。

## 這是什麼

單一 Google Apps Script 專案，部署成 Web App，供醫師撰寫**住院病歷 (Admission Note)** 與**四項臨床檢查報告** (心臟超音波 / 腹部超音波 / 胃鏡 / 大腸鏡)，一鍵寫入 Google Sheets 並產出 Google Doc + PDF + Word。

三層架構：

| 層 | 實體 | 檔案 |
|---|---|---|
| 前端 | 單頁 Web App（含密碼閘門） | `index.html` |
| 後端 | Apps Script 伺服端函式 | `Code.gs` |
| 資料 | Google Sheets 流水帳 + Drive 內的 Docs | 見下方 ID |

## 關鍵 ID 與網址

| 項目 | 值 |
|---|---|
| Script ID | `1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL` |
| Spreadsheet ID | `1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY` |
| 正式 Deployment ID | `AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g` |
| Web App URL | `https://script.google.com/macros/s/<上面的 Deployment ID>/exec` |
| GitHub remote | `https://github.com/ckt520728/2026-Antigravity.git` |

## 指令

`clasp` 沒有全域安裝，一律用 `npx`（帳號 `kwotachu@gmail.com` 已登入，credentials 在 `~/.clasprc.json`）：

```bash
cd "G:/我的雲端硬碟/2026 Google Spark"

npx @google/clasp@latest push --force          # 推送 Code.gs / index.html / appsscript.json
npx @google/clasp@latest list-deployments      # 列出所有 deployment
npx @google/clasp@latest create-deployment \
  -i AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g \
  -d "描述"                                     # 更新「同一個」網址的部署
```

**永遠用 `-i <既有 deploymentId>` 重新部署**，不要 `create-deployment` 不帶 `-i`。不帶 `-i` 會產生一個全新的 `/exec` 網址，醫師手上的舊連結就會停留在舊版本。

`.claspignore` 只允許推送 `Code.gs`、`index.html`、`appsscript.json`，其餘檔案（文件、skill、`docs/`）只存在於本機與 GitHub。

## 修改前必讀的三個約束

### 0. 密碼閘門目前是關的

`Code.gs` 最上面有 `var AUTH_ENABLED = false;`。關閉時 `authFail_()` 一律放行、`authenticate()` / `verifySession()` 直接回成功，前端 `getAuthConfig()` 拿到 `authEnabled:false` 就不顯示登入畫面。整套實作（加鹽 SHA-256、簽章 token、錯誤鎖定）都保留著，改成 `true` 並執行一次 `setAppPasscode` 就恢復。

**即使閘門是關的，下面第 1 條的 token-first 慣例仍然要遵守**，否則之後打開開關會漏掉未驗證的函式。

前端在 `google.script.run` 不存在時（例如有人直接開本機的 `index.html`）不會白屏：`hasBackend()` 會擋下呼叫，`showBackendWarning()` 顯示紅色橫幅並附上正確的 `/exec` 連結。

### 1. 每個前端可呼叫的伺服端函式，第一個參數一定是 session token

`index.html` 透過 `server('fnName', ...args)` 呼叫後端，這個 helper 會自動把 `session.token` 插到第一個參數。後端每個進入點都必須以 `authFail_(token)` 開頭：

```js
function myNewFunction(token, foo) {
  var gate = authFail_(token);
  if (gate) return gate;      // 回傳 {status:'auth_required'}，前端會跳回登入畫面
  ...
}
```

例外只有 `authenticate` 與 `verifySession`，前端用 `serverRaw()` 呼叫，不帶 token。

Token 是**無狀態簽章** `"<expiryMillis>.<sha256(salt|exp|passcodeHash)>"`，不存在伺服器上，所以 CacheService 被清空也不會踢人；反過來說，**改密碼會立刻讓所有既有 token 失效**（因為密碼 hash 是簽章的一部分）。這是刻意的設計。

### 2. Google Sheets 欄位只能往後加，不能插隊

`getOrCreateSheet()` 只在分頁「完全空的」時候才寫入表頭。線上的 `Master_Exams`（前 15 欄）與 `Master_AdmissionNotes`（前 18 欄）已經有真實資料，欄位順序是固定的。新欄位一律加在 headers 陣列**最後面**，並同步更新對應的 `mapExamRow_()` / `getRecentAdmissionNotes()` 索引。

### 3. 不要新增 OAuth scope，除非你打算要求使用者重新授權

`appsscript.json` 目前的 scope 是 spreadsheets / documents / drive / script.external_request。一旦引入需要新 scope 的服務，Web App 的 `/exec` 會**改為導向 `script.google.com/home`**，直到專案擁有者在編輯器手動執行一次任意函式並完成授權為止（這個坑踩過，記錄在 `01_專案文件/Project_WrapUp_and_Pitfalls.md`）。`PropertiesService`、`CacheService`、`Utilities`、`Session` 都不需要額外 scope，可以安心使用。

## index.html 的結構

單一檔案，約 3300 行，順序是：`<style>` → 鎖定畫面 → header → 三個 view → sticky action bar → modal/toast → 三個 `<script>` 區塊。

三個 script 區塊靠 `var` 與 function 宣告共享全域範圍，**順序不能調換**：

1. **core** — 登入、`server()` 橋接、主題、toast/modal、view 路由、草稿自動存檔、快速鍵
2. **admission** — 住院病歷的資料設定 (`ROS_SYSTEMS`, `PE_SYSTEMS`, `ADMISSION_SCENARIOS` …)、渲染、即時預覽、儲存
3. **exams** — 檢查報告產生器、範本、儀表板、語音、`bootApp()` 與進入點

**重複性的 UI 都是由 JS 設定物件產生的**（ROS 的 10 個系統、PE 的 10 個系統、各種速填晶片、問題清單、息肉列）。要加一個 ROS 系統或 PE 項目，改 `ROS_SYSTEMS` / `PE_SYSTEMS` 陣列即可，不要手寫 HTML。

### 一定要保留的行為

- **`manualEdits` 機制**：`findings` / `diagnosis` / `impression` / `recommendation` 只要被手動編輯過，`buildReportText()` 就不再覆寫（`setIfAuto()`）。v5.0 的舊版每次改下拉選單都會把醫師手打的內容洗掉，這是刻意修掉的 bug，不要退回去。
- **草稿自動存檔**：`localStorage` key `spark_draft_v6`，欄位輸入後 1 秒存一次。所有 `localStorage` 存取都要走 `lsGet/lsSet/lsDel`（包 try/catch，某些沙箱會擋）。
- **每個新的「完整性」區段都要配一顆一鍵按鈕**（全部否認 / 全部正常 / non-contributory）。補齊病歷完整性如果等於增加打字量，醫師就不會用。

## 語言與臨床內容慣例

- **UI 標籤：繁體中文 + 英文並列**（`主訴 (Chief Complaint, CC)`）。
- **產出的病歷與報告內容：英文**，符合國際病歷規範。
- 檢查所見用完整句子、句尾加句號，不要用縮寫堆疊。
- 臨床數值與品質指標要有依據，改動前先看 `docs/reference-templates.md`（RSNA 結構化報告、ASE 2025 echo 報告標準、ASGE/ACG 2024 大腸鏡品質指標、標準 H&P 區段）。例：退鏡時間門檻是 **8 分鐘**（2024 更新），不是舊的 6 分鐘。

## 測試

沒有自動化測試框架。改完 `index.html` 後至少跑這個靜態檢查：

```bash
node -e "
const fs=require('fs'); const s=fs.readFileSync('index.html','utf8');
[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{
  try{ new Function(m[1]); console.log('block',i+1,'OK'); }catch(e){ console.log('block',i+1,'ERR',e.message); }});
const called=new Set([...s.matchAll(/on(?:click|change|input|keyup)=\"([\w\$]+)\(/g)].map(m=>m[1]));
const defined=new Set([...s.matchAll(/function\s+([\w\$]+)\s*\(/g)].map(m=>m[1]));
console.log('missing handlers:', [...called].filter(f=>!defined.has(f)));
"
```

再實際開 `/exec` 走一次：登入 → 填最小必填 → 儲存 → 確認 Doc/PDF/Word 連結可開。

## 不要做的事

- 不要把密碼寫進原始碼。密碼只以加鹽 SHA-256 存在 Script Properties，透過編輯器執行 `setAppPasscode` 變更。
- 不要在 `createGoogleDocReport` / `createAdmissionNoteDocReport` 裡用 `SpreadsheetApp.getActiveSpreadsheet()`，要用 `getSpreadsheet()`（有 `openById` 的 fallback）。
- 不要把真實病患個資寫進 repo、測試資料或 commit 訊息。
