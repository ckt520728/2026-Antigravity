# 後端 — 醫院員工出勤系統 Phase 1

模組化單體（modular monolith）。動工前請先讀專案根目錄的 `CLAUDE.md`。

## 現況

骨架完成並可啟動：**29 個 API 端點、15 張資料表、19 項測試通過**。
業務邏輯已實作的部分：事件配對、工時／加班候選計算、更正流程狀態機、
功能開關、稽核寫入、報表產生。

尚未實作（等待 `CLAUDE.md` §14 的未決事項確認）：
kiosk 離線佇列、班表 Excel 匯入、完整角色權限矩陣。

## 環境需求

- Python **3.11 以上**（目標 3.12；已於 CPython 3.11.15 驗證）
- PostgreSQL 16

## 安裝與啟動

```powershell
cd backend

# 建立虛擬環境（擇一）
uv venv --python 3.11 .venv                       # 使用 uv（較快）
python -m venv .venv                              # 或標準 venv

.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt                # 或 pip install -r requirements.txt

# 設定
Copy-Item .env.example .env                       # 修改 DATABASE_URL 與 JWT_SECRET

# 建立資料表
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

# 啟動
uvicorn app.main:app --reload
```

API 文件：<http://localhost:8000/docs>

## 測試

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

目前涵蓋：事件配對邏輯（9 項）、更正流程狀態機（10 項）。
兩者皆為純函式測試，不需資料庫。

## 模組邊界

```
identity ──┐
           ├─→ attendance ──┐
scheduling ┘                ├─→ overtime ──→ reporting
                            │
audit ←──── 所有模組都寫稽核 ─┘
governance ── 功能開關 + 未知治理
```

**規則**：模組間只能呼叫對方的 `service.py`，
禁止跨模組直接 import ORM model（`CLAUDE.md` §4）。
`scheduling.shifts_for_staff()` 與 `identity.staff_directory()` 刻意回傳
dict 而非 ORM 物件，讓呼叫端在型別上就無法回寫。

## 紅線提醒

實作時最容易誤觸的三條（完整清單見 `CLAUDE.md` §2）：

- **R1** 不得儲存原始生物特徵。WebAuthn 只回傳簽章，`identity` 模組
  沒有、也不得新增處理生物特徵原始資料的程式碼。
- **R4** 加班只能是 Overtime Candidate。`overtime` 模組沒有任何
  送往薪資的函式，不得新增。
- **R9** `AttendanceEvent`（實際）與 `PlannedShift`（預期）永遠分開，
  任一方都不得覆寫另一方。

## 已知待辦

程式中以 `TODO(open-decision)` 標記，對應 `CLAUDE.md` §14：

| 位置 | 待確認事項 |
|------|------------|
| `attendance/models.py` | kiosk 離線佇列行為（最高風險） |
| `core/config.py` | 勞基法參數的權責單位與法規複核 |
| `core/deps.py` | 角色權限矩陣與職責分離 |
| `identity/service.py` | challenge 暫存（多 instance 部署時需改 Redis） |
| `scheduling/router.py` | 班表 Excel 匯入範本欄位 |
| `reporting/service.py` | 中文字型（Linux 容器需安裝 CJK 字型） |
| `reporting/router.py` | 報表範本、保留年限、存取權限 |
| `core/feature_store.py` | 多 instance 部署時的開關快取一致性 |
