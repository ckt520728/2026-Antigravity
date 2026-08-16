# 陽明醫院附設護理之家 員工出勤與打卡系統 (Hospital Staff Attendance & Kiosk System)

> 專案主導與架構：朱國大醫師 (Kwo-Ta Chu, MD, PhD)  
> 雲端正式版網址：[https://my-teaching-tools-ckt520728.web.app](https://my-teaching-tools-ckt520728.web.app)  

---

## 專案簡介

本系統為專為**陽明醫院附設護理之家（3F 護理站）**設計之電腦網頁版員工打卡、出勤追蹤、醫師巡診簽到與統計報表系統。

### 核心功能
1. **護理站電腦人體工學打卡（Kiosk Console）**：全鍵盤快捷支援（`[Enter]` 選擇、`[1]` 上班、`[2]` 下班、`[3]` 巡診、`[4]` 外出、`[5]` 返回、`[M]` 主管例外備註）。
2. **朱國大醫師巡診專用通道**：兼任主治醫師病房巡診在場簽到（遵守紅線 R3/R10 不碰病人個資，僅留病房層級在場證據）。
3. **Dark / Light 雙主題切換**：高質感毛玻璃微透光介面，自適應夜間與日間照明環境。
4. **4 國語系 i18n 支援**：繁體中文、Tiếng Việt (越南文)、Bahasa Indonesia (印尼文)、English。
5. **統計報表一鍵匯出**：
   - Excel (`.xlsx`)：出勤統計總表、打卡流水、朱醫師巡診專區多工作表。
   - Word (`.docx`)：醫療合規排版、工時總覽、醫師巡診紀錄、主管與醫師簽核欄。
6. **離線容錯與自動同步**：斷網自動暫存於本機 LocalStorage，復網後背景批次補送。

---

## 目錄架構

```
hospital-attendance-kiosk/
├── backend/                        # FastAPI 模組化單體架構 (Modular Monolith)
│   ├── app/
│   │   ├── core/                  # 設定、資料庫、枚舉與功能開關 (Feature Flag)
│   │   ├── modules/
│   │   │   ├── attendance/        # 打卡端點、配對引擎、更正狀態機
│   │   │   ├── identity/          # 28名在職同仁名冊與身分管理
│   │   │   ├── overtime/          # 工時四指標與加班候選計算
│   │   │   ├── reporting/         # Excel (openpyxl) 與 Word (python-docx) 產製
│   │   │   └── audit/             # 不可篡改 AuditLog 審計日誌
│   │   └── scripts/               # 名冊解析與匯入腳本 (import_nursing_roster.py)
│   └── tests/                     # 23 項 pytest 自動化測試 (100% PASS)
├── frontend/                       # React 18 + TypeScript + Vite 前端
│   ├── src/
│   │   ├── App.tsx                # 主程式 (雙主題、三大分頁、鍵盤導航)
│   │   ├── App.css / index.css    # 醫療級 Glassmorphism 設計系統
│   │   ├── i18n.ts                # 4 國語言字典
│   │   └── api.ts                 # API 客戶端與離線佇列管理
│   └── dist/                      # 生產建置打包產物
├── firebase.json / .firebaserc    # Firebase Hosting 雲端部署配置
├── CLAUDE.md                       # 系統架構守則與紅線規範 R1~R10
└── handoff.md                      # 專案進度與決策記錄
```

---

## 啟動與使用說明

### 本地啟動
```powershell
# 1. 啟動後端
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --port 8000 --reload

# 2. 啟動前端
cd ../frontend
npm run dev
```
瀏覽器開啟 `http://localhost:5173` 即可操作。

### 雲端正式版
直接瀏覽：[https://my-teaching-tools-ckt520728.web.app](https://my-teaching-tools-ckt520728.web.app)
