# 交接說明 Handoff — 臨床醫療紀錄與報告系統 v6.0

> 更新日期：2026-08-10 ｜ 上一版：v5.0 ｜ 本版：v6.1（病歷完整性升級；**密碼入口目前關閉**）

---

## 1. 怎麼開啟

**網址（與舊版相同，不用換連結）**
<https://script.google.com/macros/s/AKfycbyucGUOYz9eS9IrLWohMtYJ8Hm-oZmhgyhmKXZJjE1gf8DZj_Ra9r9_lzuUHgVVf2zL5g/exec>

**目前不需要密碼**，開啟連結直接進入系統。右下角狀態列會顯示「密碼保護：關閉中」。

### ⚠️ 一定要用 `/exec` 網址開啟

**不要**直接點開雲端硬碟資料夾裡的 `index.html` 檔案。那是原始碼，不是執行中的網頁，`google.script.run` 不存在，會出現「無法連線至伺服器：google is not defined」。v6.1 已加上偵測：真的開錯檔案時，畫面上方會出現紅色提示並附上正確網址的連結。

### 之後要把密碼打開時

1. 開 [Apps Script 編輯器](https://script.google.com/d/1vmdg7x6X6kHzRnh1gA7u2GlRk_lnDW6Mvaava0SD-qdsdoowh4AhzyTL/edit)
2. `Code.gs` 最上面把 `var AUTH_ENABLED = false;` 改成 `true`
3. 找到 `setAppPasscode()`，把 `var NEW_PASSCODE = '請在這裡填入新密碼';` 改成你要的密碼（至少 6 個字），函式下拉選單選 `setAppPasscode` → 按 **執行 (Run)**，看到「✅ 密碼已更新」即可
4. **把 `NEW_PASSCODE` 改回 `'請在這裡填入新密碼'` 並存檔**，避免密碼留在程式碼裡
5. 重新部署：`部署 → 管理部署作業 → 編輯 → 版本選「新版本」→ 部署`
   （或在本機執行 `npx @google/clasp@latest push --force` 再 `create-deployment -i <deploymentId>`）

整套密碼機制（加鹽 SHA-256、12 小時簽章 token、每支後端函式驗證、錯誤鎖定）都還在程式碼裡，只是被 `AUTH_ENABLED` 這個開關關掉，打開就會恢復。密碼本身不會存在程式碼或試算表中。

---

## 2. v6.0 做了什麼

先上網調研了醫學中心／教學醫院的病歷與報告範本，再依調研結果補齊缺口。完整調研筆記與出處在 **`docs/reference-templates.md`**。

### A. 入口密碼（已實作，但目前以 `AUTH_ENABLED = false` 關閉）

打開後的行為：

- 開啟網址先出現密碼畫面，通過才看得到系統。
- 密碼以**加鹽 SHA-256** 存在 Script Properties。
- 登入後拿到 12 小時的**簽章式 session token**；每一支後端函式（存病歷、讀紀錄、搜尋、翻譯）都會驗證，光靠瀏覽器 console 也繞不過去。
- 連續輸錯 8 次會鎖 15 分鐘，每次錯誤延遲 0.7 秒，防暴力猜測。

**目前的狀態是關閉**：連結一開就是系統本體，後端也不檢查 token。開啟方式見第 1 節。

### B. 住院病歷：補齊標準 H&P 缺的區段

v5.0 只有 CC / HPI / PMH / 過敏 / PE / A&P。對照教學醫院範本後補上：

| 新增區段 | 說明 |
|---|---|
| **手術史 (PSH)** | 速填晶片：膽囊切除、闌尾切除、PCI、動靜脈瘻管… |
| **目前用藥 (Medications)** | 用藥整合 (reconciliation)，常用藥速填 |
| **家族史 (Family History)** | 可複選晶片自動組句 |
| **個人社會史 (Social History)** | 菸 (pack-year) / 酒 / **檳榔** / 職業 / TOCC / 生活功能。檳榔欄位是台灣在地必要項目 |
| **系統回顧 (ROS)** | 10 大系統、約 55 個症狀的**三態晶片**：點 1 次 ＋（陽性）、2 次 －（陰性）、3 次取消 |
| **入院檢驗與影像** | CBC / 生化 / 發炎指標 / 尿液 / CXR / EKG / 其他 |
| **病史提供者與可信度** | Informant / Reliability |
| **BMI、疼痛評分、GCS** | BMI 自動計算 |

### C. 理學檢查：從一個大方塊改成分系統

10 個系統（General / HEENT / Neck / Chest / Heart / Abdomen / Back / Extremities / Neuro / Skin），每個都有標準正常敘述與常見異常速填晶片。

**「全部填入正常」一鍵**填好 10 個系統，再改有問題的那幾項就好——這是讓「更完整」不等於「更花時間」的關鍵。ROS 也有對應的「全部否認」。

### D. 問題導向 A&P（Problem-based）

初步診斷與治療計畫不再是兩個各自為政的大方塊，改成**一個 problem 對應一段 plan** 的條列，可新增／刪除。

內建 6 個常用入院情境一鍵帶入完整問題清單與計畫：急性闌尾炎、社區型肺炎、AKI on CKD、急性心衰竭、腎盂腎炎、上消化道出血。

### E. 檢查報告：對齊國際結構化報告標準

- **RSNA 結構化報告**：四個檢查模組都補上「臨床適應症 (Indication) → 檢查技術 (Technique) → 比較影像 (Comparison) → 所見 (Findings) → 結論 (Impression) → 建議」的固定順序；切換檢查項目會自動帶入該項目的預設技術描述。
- **心臟超音波（ASE 2025 報告標準）**：新增右心室功能 / TAPSE、IVC 與容積狀態、估計 PASP、**檢查當下血壓**、**顯影劑與 bubble study**，並依 LVEF 自動分級（<40% / 40–49% / ≥50%）給出不同結論與建議。
- **大腸鏡（ASGE/ACG 2024 品質指標）**：
  - 退鏡時間門檻由舊的 6 分鐘更新為 **8 分鐘**，低於 8 分鐘即時警示
  - 新增**盲腸標誌照相記錄**勾選（闌尾開口 / 迴盲瓣 / 末端回腸）
  - 息肉改為可新增多筆的結構化列：**部位 × 大小 × 形態 (Paris/Yamada) × 切除方式**；4–9 mm 未選 cold snare 會提示
- **腹部超音波**：新增慢性腎病變 (CKD pattern) 範本與腎臟大小欄位（配合腎臟科需求）。

### F. 操作性改善

| 項目 | 說明 |
|---|---|
| **修掉會洗掉手打內容的 bug** | v5.0 只要動一下下拉選單，醫師手打在 Findings 的補充就會被覆寫。現在只要手動編輯過就永久保護，要重新套用選項請按「依選項重新生成」 |
| **草稿自動保存** | 每次輸入 1 秒後自動存在瀏覽器，關掉分頁再開會自動還原並提示 |
| **一鍵複製全文** | 預覽區右上角，直接貼回院內 HIS |
| **淺色／深色模式** | 右上角切換，長時間看文字建議淺色 |
| **列印樣式** | 列印時自動隱藏按鈕與導覽列 |
| **必填檢查** | 缺 MRN / CC / HPI / 至少一個 problem 時會標紅並捲到該欄位 |
| **快速鍵** | `Ctrl/⌘+S` 儲存、`Ctrl/⌘+P` 列印、`Esc` 關視窗 |
| **歷史紀錄雙分頁** | 可切換檢查報告／住院病歷兩種紀錄 |
| **手機版面** | 表單、分頁、底部操作列都改成單欄自適應 |
| **24 小時期限提示** | 依 CMS 規範，顯示距離入院後 24 小時完成 H&P 還剩多久 |

---

## 3. 資料存在哪裡

| 內容 | 位置 |
|---|---|
| 住院病歷流水帳 | 試算表分頁 `Master_AdmissionNotes`（原 18 欄不動，v6.0 新欄位加在第 19–26 欄） |
| 檢查報告流水帳 | 試算表分頁 `Master_Exams`（原 15 欄不動，新欄位加在 16–19 欄）+ 四個檢查別分頁 |
| 住院病歷 Doc | Drive → `2026 Google Spark` → `住院病歷報告_GoogleDocs` |
| 檢查報告 Doc | Drive → `2026 Google Spark` → `臨床檢查報告_GoogleDocs` |

[開啟試算表](https://drive.google.com/open?id=1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY)

舊資料完全相容，不需要搬移。

---

## 4. 已驗證與尚待你確認的

**已驗證**

- `clasp push` 成功，三個檔案（`Code.gs` / `index.html` / `appsscript.json`）已上線
- 已重新部署到**原本那個 deployment ID**，網址沒有變，目前版本 `@20`
- `/exec` 直接回應 200，不再被導向 Google 登入頁（`ANYONE_ANONYMOUS` 生效）
- `index.html` 三個 script 區塊與 `Code.gs` 語法檢查通過；所有 inline 事件處理器都有對應函式；所有 `getElementById` 目標都存在於 HTML

**尚待你確認（我這邊的瀏覽器自動化視窗卡住無法截圖）**

請開啟 `/exec` 網址，確認：

1. 直接進入系統，不再要求密碼
2. 住院病歷填最小必填（MRN、主訴、現在病史、一個 problem）→ 按底部「儲存」→ 跳出 Doc / PDF / Word 三個連結且都能開
3. 檢查報告選一個項目 → 套用快速範本 → 儲存 → 三個連結都能開
4. 歷史紀錄分頁能看到剛才那兩筆

若第 2、3 步出現 `Authorization required` 或被導回 `script.google.com/home`，代表需要重新授權：開 Apps Script 編輯器 → 隨便選一個函式 → 執行 → 完成「審查權限 → 進階 → 允許」。（本次沒有新增 OAuth scope，理論上不會發生。）

---

## 5. 使用注意

- 本系統會把病歷內容寫入 Google Sheets 與 Google Docs（存在部署者 `kwotachu@gmail.com` 的雲端硬碟）。請依所屬機構的個資與資安規範使用，避免輸入非必要的可識別個資。
- 密碼閘門擋的是「拿到連結的路人」，不是稽核等級的存取控制；沒有分帳號、沒有逐人操作軌跡。若要正式臨床使用，建議另外評估院內資安要求。
- 中文轉英文使用 Apps Script 內建 `LanguageApp`，是**通用翻譯不是醫學專用翻譯**，翻完務必人工檢查醫學用語。

---

## 6. 給下一位開發者

技術細節、修改約束與陷阱寫在 **`CLAUDE.md`**；外部範本調研與出處寫在 **`docs/reference-templates.md`**；v5.0 之前踩過的部署坑寫在 **`01_專案文件/Project_WrapUp_and_Pitfalls.md`**。

最重要的三條：

1. 重新部署一律用 `-i <既有 deploymentId>`，否則會產生新網址、舊連結停在舊版
2. 新的後端函式第一個參數必須是 token，並以 `authFail_(token)` 開頭
3. 試算表欄位只能往後加，不能插隊
