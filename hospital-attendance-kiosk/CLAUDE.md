# CLAUDE.md — 醫院員工出勤系統 專案作業規則

> 本檔為本專案的**強制作業規則**。任何 AI 代理或開發者在寫程式碼前必須先讀完本檔。
> 與 `handoff.md` 衝突時，以本檔為準；本檔未涵蓋者，回到 `handoff.md`。

---

## 1. 專案目標

為桃園市一家 128 床區域醫院（約 110 名員工）建置**網頁式、跨平台（桌機／筆電瀏覽器）**的醫護與非醫護人員**出勤、排班、工時與加班系統**。

Phase 1 為**沙盒試辦（pilot）**，與醫院現有 HIS／EMR **完全隔離**，不取代任何正式系統。

輸出需求：**Excel、Word、統計圖表**三種。

---

## 2. 紅線規則（禁止事項，不得以任何理由違反）

| # | 禁止 | 原因 |
|---|------|------|
| R1 | 儲存原始指紋影像、臉部影像，或任何可還原的生物特徵範本（biometric template） | handoff 決議 9 |
| R2 | 自行開發指紋／臉部辨識演算法 | handoff 決議 9 |
| R3 | 記錄病人姓名、病歷號、診斷或任何病人層級資料 | handoff 決議 11 |
| R4 | 將出勤或加班資料自動送入薪資系統（payroll） | handoff 決議 10 |
| R5 | 收集或重用 HIS 密碼 | handoff 決議 13 |
| R6 | 將可識別的員工／生物特徵／臨床資料送往外部 AI 服務 | handoff 決議 14 |
| R7 | 在開發或測試環境使用真實員工資料（僅可用合成或不可逆去識別化資料） | handoff 決議 14 |
| R8 | 宣稱已完成 HIS 整合（除非醫院 IT 與 HIS 廠商書面確認授權介面） | handoff 決議 13 |
| R9 | 讓 `Planned Shift` 與 `Attendance Event` 互相覆寫 | handoff 決議 12 |
| R10 | 產生診斷、處方、醫囑、檢傷分級或原始臨床紀錄 | handoff 決議 4 |

**違反紅線的程式碼一律不得合併，必須刪除重寫。**

---

## 3. 已鎖定的技術決策

| 項目 | 決定 |
|------|------|
| 架構 | **模組化單體（modular monolith）**，非微服務 |
| 後端 | Python 3.12 + FastAPI + SQLAlchemy 2.x + Alembic |
| 前端 | React 18 + TypeScript + Vite |
| 資料庫 | PostgreSQL 16 |
| 報表 | `openpyxl`（Excel）、`python-docx`（Word）、`matplotlib`（統計圖） |
| 身分驗證 | **WebAuthn passkey**（醫院自控 kiosk 上的 Windows Hello 指紋／臉部平台驗證器） |
| 部署 | 院內／地端優先（on-premises first），治理法域為**中華民國（台灣）** |
| 文件語言 | 繁體中文（技術名詞保留英文） |

架構理由：110 名員工的規模不足以支撐微服務的維運成本；以**模組邊界 + 功能開關（feature flag）**即可保留未來拆分的可能性，並直接滿足「各功能可依需要開啟／關閉」的需求。

---

## 4. 目錄結構

```
D:\2026 Hospital management system\
├─ CLAUDE.md              # 本檔，作業規則
├─ CONTEXT.md             # 純術語表（domain glossary），不放決策
├─ handoff.md             # 續作摘要
├─ docs/
│  └─ adr/                # 僅記錄難以回復的重大決策
├─ backend/
│  ├─ app/
│  │  ├─ modules/
│  │  │  ├─ attendance/   # 打卡事件、出勤／缺勤判定
│  │  │  ├─ scheduling/   # 排班、OPD 診次、班表版本
│  │  │  ├─ overtime/     # 工時彙總、加班候選計算
│  │  │  ├─ reporting/    # Excel / Word / 統計圖輸出
│  │  │  ├─ identity/     # WebAuthn、角色權限、名冊
│  │  │  ├─ audit/        # 稽核軌跡、更正流程
│  │  │  └─ governance/   # thinking_unknown 未知治理層
│  │  ├─ core/            # 設定、功能開關、資料庫、安全
│  │  └─ main.py
│  ├─ alembic/
│  └─ tests/
├─ frontend/
│  └─ src/{pages,components,api,features}/
└─ reference/             # 唯讀參考，禁止修改、禁止匯入production code
   ├─ php-hospital-hms/   # Ebo1996/PHP-Hospital-HMS
   └─ employer-checkin/   # yash-rana0101 SQL 彙總邏輯參考
```

**模組間只能透過各模組的 `service.py` 公開介面呼叫，禁止跨模組直接 import ORM model。**

---

## 5. 功能模組與功能開關

需求 a–j 對應到功能開關。**每一項都必須可獨立開關**，預設值定義於 `backend/app/core/features.py`，執行期由管理者於後台切換（不需重啟）。

| 需求 | 功能開關 | 說明 |
|------|----------|------|
| a | `FEATURE_BIOMETRIC_PRESENCE` | 以 WebAuthn 生物驗證確認在／缺勤 |
| b | `FEATURE_WORK_HOURS` | 上下班打卡與工時判定 |
| c | `FEATURE_OPD_SCHEDULE` | 醫師門診（OPD）診次排程控制 |
| d | `FEATURE_WARD_ROUND_SIGNIN` | 住院病房訪視醫師**病房層級**簽到 |
| e | `FEATURE_OPD_NURSE` | 門診護理師上下班 |
| f | `FEATURE_ER_INPATIENT_NURSE` | 急診與住院護理師上下班 |
| g | `FEATURE_NONMEDICAL_STAFF` | 非醫護（掛號、會計、醫務行政） |
| h | `FEATURE_NIGHT_DUTY` | 夜間值班醫師／專科護理師簽到退 |
| i | `FEATURE_HOLIDAY_DUTY` | 假日值班醫師／專科護理師簽到退 |
| j | `FEATURE_OVERTIME_AGGREGATION` | 工時與加班時數彙總 |

**規則**：關閉某開關時，對應 API 回 `404`、前端隱藏入口、**既有資料不得刪除**。

---

## 6. 核心術語與資料模型

術語定義（詳細版見 `CONTEXT.md`）：

- **Attendance Check-in/Check-out**：員工出勤事件的開始／結束。
- **On-duty Sign-in**：夜間、假日或 on-call 的到勤證據。
- **Clinical Round Sign-in**：**病房層級**醫師在場紀錄。**不是**病人層級紀錄，**不代表**已完成診療或病歷書寫。
- **Planned Shift**：已核准的預期班表。
- **Attendance Event**：實際觀測到的打卡證據。
- **Overtime Candidate**：已計算但**尚未完成核准**的加班時數。

核心資料表（最小集合）：

```
staff(id, employee_no, name, unit, role, employment_type, active)
planned_shift(id, staff_id, shift_date, shift_type, start_at, end_at,
              version_id, approved_by, approved_at)
attendance_event(id, staff_id, event_type, occurred_at, source,
                 verification_id, station_id, is_corrected)
verification_event(id, method, credential_id, signature_counter,
                   verified_at, station_id)   -- 絕不存原始生物特徵
work_hour_summary(id, staff_id, period, regular_minutes,
                  overtime_candidate_minutes, status)
correction_request(id, attendance_event_id, requested_by, reason,
                   state, supervisor_id, hr_id, timestamps...)
audit_log(id, actor_id, action, entity, before, after, occurred_at, reason)
```

**強制**：`attendance_event` 與 `planned_shift` 為兩張獨立表，任何寫入路徑都不得讓其中一方覆寫另一方（R9）。

---

## 7. 工時與加班計算規則

彙總邏輯參考 `reference/employer-checkin/` 的四項指標：

1. **首次上班時間**（該期間最早 check-in）
2. **最後下班時間**（該期間最晚 check-out）
3. **外出次數**（配對之間的離開次數）
4. **總工時**（配對後的時間總和）

台灣勞基法**預設參數**（寫在設定檔，不得寫死在程式中）：

| 參數 | 預設 | 出處 |
|------|------|------|
| 每日正常工時 | 8 小時 | 勞基法 §30 |
| 每週正常工時 | 40 小時 | 勞基法 §30 |
| 每日工時上限（含加班） | 12 小時 | 勞基法 §32 |
| 每月加班上限 | 46 小時 | 勞基法 §32 |
| 輪班間隔 | 11 小時 | 勞基法 §34 |

> ⚠️ **待確認**：上述參數之權責單位（HR／人事室）與台灣勞動法規複核**尚未指定**。程式必須將其視為**可設定的政策參數**，並在報表上標示「未經法規複核」浮水印，直到權責單位書面確認。

**Phase 1 影子模式（shadow mode）強制規定**：
- 與現有 HR／紙本紀錄**平行運作**；
- 加班一律先產生為 **Overtime Candidate**，核准後才轉為正式；
- **絕不**自動送入薪資（R4）。

---

## 8. 身分驗證與生物辨識

- 使用醫院自控 kiosk／終端上的 **WebAuthn platform authenticator**（Windows Hello 指紋／臉部）。
- 伺服器**只儲存**：`credential_id`、公鑰、`signature_counter`、驗證時間、站點 ID。
- **絕不**接收、傳輸或儲存原始生物特徵（R1）。
- Phase 1 由 HR 核可名冊**另行開設試辦帳號**，不重用 HIS 密碼（R5）。
- 必須提供**受治理的非生物辨識例外路徑**（主管代打卡 → 需理由 + 稽核）。
- 保留 OIDC／LDAP 整合邊界，但在醫院 IT 與 HIS 廠商確認前**不得宣稱已整合**（R8）。

---

## 9. 報表輸出

三種輸出皆由 `modules/reporting/` 產生：

| 格式 | 函式庫 | 用途 |
|------|--------|------|
| Excel | `openpyxl` | 工時明細、加班彙總、班表匯入／匯出範本 |
| Word | `python-docx` | 月報、部門簽核表 |
| 統計圖 | `matplotlib` | 工時分布、加班趨勢、單位別比較、出勤率 |

規則：
- 所有報表必須標示**產製時間、產製者、資料期間、影子模式聲明**。
- 排班採用**標準 Excel 範本匯入** + 授權網頁編輯（handoff 決議 12）。
- 報表存取受角色權限控管；下載行為必須寫入 `audit_log`。

---

## 10. 更正與例外狀態機

任何出勤紀錄更正必須走完整流程，**不得直接 UPDATE**：

```
DRAFT → SUBMITTED（員工提出，須填理由）
      → SUPERVISOR_APPROVED（主管核准）
      → HR_CONFIRMED（人事確認）
      → APPLIED
      ↘ REJECTED（任一關卡可退回，須填理由）
```

- 每次變更保留**原值、操作者、時間戳記、理由**（handoff 決議 12）。
- 班表換班／編輯同樣適用。
- 稽核紀錄為 **append-only**，禁止刪除或修改。

---

## 11. 開發工作流程（thinking_unknown 治理層）

`thinking_unknown` 是**治理與持續改善層**，不是臨床工具（R10）。每個開發循環必須包含：

1. **對映已知與未知** — 開工前列出 knowns / unknowns。
2. **blindspot pass** — 設計定案前執行盲點檢查。
3. **reference-anchor pass** — 對照參考資料驗證假設。
4. **decision-first plan** — 先寫決策再寫步驟。
5. **deviation log** — 偏離計畫必須記錄。
6. **verify against rubric** — 依預先定義的評分表驗收。
7. **comprehension before acceptance** — 使用者理解確認後才算完成。

可用技能對應：`blindspot-pass`、`reference-anchor`、`decision-first-plan`、`deviation-log`、`verify-with-rubric`、`comprehension-quiz`、`grilling`、`domain-modeling`、`codebase-design`。

**提問規則**：討論設計時**一次只問一個問題**，並附上建議答案（`grilling` 規範）。

---

## 12. 開發指令

```powershell
# 後端
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev

# 測試
cd backend; pytest
cd frontend; npm test
```

---

## 13. 資料處理與部署

- 治理法域：**中華民國（台灣）**。
- 正式敏感資料：**院內／地端優先**。
- 開發／測試：**僅用合成或不可逆去識別化資料**（R7）。
- 必備：加密、最小權限、稽核軌跡、備份、**離線／降級模式計畫**。
- Phase 1 **僅供員工使用**，非病人入口網站。
- Phase 1 與現有 HIS **保持隔離**。

---

## 14. 尚未決定事項（實作前需補齊）

以下項目仍為 open decision，遇到時**必須先問使用者**，不得自行假設：

- [ ] kiosk／終端整合合約細節與**離線佇列行為**（斷線時的暫存與補送規則）
- [ ] 工時／加班政策的**權責單位**與台灣勞動法規複核窗口
- [ ] **角色權限矩陣**與職責分離（segregation of duties）
- [ ] 報表範本、篩選條件、**保留年限**與存取權限
- [ ] 備份／復原目標（RPO／RTO）、監控與資安事件應變
- [ ] 試辦族群、期間、**成功評分表（rubric）**與 go／no-go 關卡

---

## 15. AI 代理注意事項

- 動工前先讀 `handoff.md` 的最新續作點。
- `reference/` 為**唯讀**：可讀取理解，**禁止修改，禁止複製進 production 程式碼**。
- 難以回復的決策必須寫入 `docs/adr/`。
- 不確定時**問使用者**，不要猜——尤其涉及紅線 R1–R10 時。
- 回報進度要據實以告：測試失敗就說失敗並附輸出，跳過的步驟要明講。
