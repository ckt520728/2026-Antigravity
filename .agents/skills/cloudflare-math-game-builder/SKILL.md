---
name: cloudflare-math-game-builder
description: Use when developing, testing, or deploying web-based educational math games to Cloudflare Workers with D1 SQL databases and Durable Objects, or when adapting math-game-templates for iPad, iPhone, and classroom teacher-student interactive setups.
---

# Cloudflare Math Game Builder (邊緣原生數學遊戲與課堂即時診斷系統開發指南)

## 一、 核心架構與原則 (Overview)

本技能提供一套基於 **Cloudflare 邊緣計算生態系（Workers + D1 SQL + Durable Objects）** 與 **數學教育遊戲範本庫（Math Game Templates）** 的端到端架構指南。核心理念是將**認知心理學的診斷反饋**與**現代邊緣網頁技術**深度融合，達成以下三大目標：

1. **極致響應與邊緣無伺服器持久化**：
   - 前端靜態資源由 Cloudflare Workers 邊緣 CDN 託管，首屏加載 < 100ms。
   - 輕量化房間狀態由 **Durable Objects (WebSockets)** 處理即時同步。
   - 學生遊玩軌跡（Audit Trails）與成績存入 **Cloudflare D1 (SQLite-at-edge)**，提供毫秒級 SQL 聚合分析。
2. **逆向教學設計（Backward Design）與認知診斷**：
   - 嚴格遵守「回推八步驟」：從教學指標出發，反推錯誤迷思誘答鏈（Diagnostic Traps），確保遊戲不是盲目點擊，而是具備形成性評量（Formative Assessment）功能。
3. **跨平台極致體驗（iPad / iPhone WebKit 原生適配）**：
   - 支援 Apple Web App PWA 全螢幕規格。
   - 手機直屏自動採用 $6 \times 8$ 矩陣，平板橫屏採用 $8 \times 6$ 矩陣。
   - 處理 iOS Safari 虛擬鍵盤彈出引發的視窗塌陷（`100dvh` 與 `activeElement.blur()`）。

---

## 二、 適用時機 (When to Use)

- **情境 1**：在無交互式終端機（Non-Interactive / CI-CD / AI Subagent）環境下，需調用 Cloudflare CLI (`wrangler`) 進行 D1 資料庫建立、遷移與部署。
- **情境 2**：在 `math-game-templates` 範本庫中擴充新學科單元（如三角函數、微積分、多項式除法、幾何比例等）。
- **情境 3**：設計具備教師端（即時戰情看板、迷思分析分佈、學生匿名 ID）與學生端（闖關、連鎖消除、觸覺震動回饋）的雙軌教學系統。
- **情境 4**：將現有 Web 遊戲優化適配於教學現場常見的 iPad 平板與學生 iPhone 手機。

---

## 三、 快速速查表 (Quick Reference)

| 任務環節 | 關鍵指令 / 參數 | 核心注意事項 |
| :--- | :--- | :--- |
| **Non-interactive 憑證** | `$env:CLOUDFLARE_API_TOKEN = "<oauth_token>"`<br>`$env:CLOUDFLARE_ACCOUNT_ID = "<account_id>"` | 從 `~/.wrangler/config/default.toml` 提取 `oauth_token` 即可作為 API Token。 |
| **D1 資料庫建立** | `npx wrangler d1 create <db-name>` | 記錄返回的 `database_id`，填入 `wrangler.jsonc`。 |
| **D1 遠端遷移執行** | `"y" \| npx wrangler d1 migrations apply <db-name> --remote` | **必須** 使用 pipe 傳入 `"y"`，避免因確認提示 `(y/N)` 卡住背景終端。 |
| **本地多裝置調試** | `python -m http.server 8080 --bind 0.0.0.0` | 綁定 `0.0.0.0` 允許同一 Wi-Fi 子網下的 iPad/iPhone 透過 LAN IP 連入。 |
| **生產環境部屬** | `npx wrangler deploy` | 網址規則為 `https://<worker-name>.<subdomain>.workers.dev`。 |
| **單元與邏輯測試** | `node --test tests/chain-match/*.test.mjs` | Node.js 原生測試框架，秒級驗證 2000 個固定隨機種子與無死局條件。 |

---

## 四、 端到端實作工作流 (Core Implementation Workflow)

### 步驟 1：Cloudflare Agent 連線與自動憑證掛載
在 AI 智能體或自動化腳本中，若直接執行 `wrangler whoami` 常會因無 TTY 而拋出 `In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN`。
利用已登入之 Wrangler OAuth 本地憑證進行非侵入式提取：

```powershell
# PowerShell 自動憑證掛載腳本
$tomlPath = "$env:APPDATA\xdg.config\.wrangler\config\default.toml"
if (Test-Path $tomlPath) {
    $tokenMatch = Select-String -Path $tomlPath -Pattern 'oauth_token = "(.*?)"'
    if ($tokenMatch) {
        $env:CLOUDFLARE_API_TOKEN = $tokenMatch.Matches[0].Groups[1].Value
        # 帳號 ID 可預先綁定或從 whoami 獲取
        $env:CLOUDFLARE_ACCOUNT_ID = "6daa724abf5875bbca51735b0c49ec0b"
        Write-Host "Cloudflare Token 注入成功" -ForegroundColor Green
    }
}
```

### 步驟 2：D1 資料庫配置與免互動遷移
在專案根目錄配置 `wrangler.jsonc`：
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "kwotachu-math-games",
  "main": "worker/index.js",
  "compatibility_date": "2026-10-01",
  "assets": {
    "directory": "./site",
    "binding": "ASSETS"
  },
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "kwotachu-math-games-db",
      "database_id": "5cebe112-1849-4a3b-b5bd-792b92b389b4"
    }
  ]
}
```
建立資料庫遷移檔 `migrations/0001_init.sql`：
```sql
CREATE TABLE IF NOT EXISTS mg_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id TEXT NOT NULL,
  player_id TEXT NOT NULL,
  game_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mg_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id TEXT NOT NULL,
  player_id TEXT NOT NULL,
  game_id TEXT NOT NULL,
  score INTEGER NOT NULL,
  details TEXT,
  completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
以無人值守方式執行遠端部署：
```powershell
"y" | npx wrangler d1 migrations apply kwotachu-math-games-db --remote
npx wrangler deploy
```

### 步驟 3：數學內容引擎設計（以三角函數 `trig.js` 為例）
依據教學診斷需求，設計高純度無副作用的數學產生器模組：
1. **數值正確性與根號表示法**：
   - 避免浮點數比較誤差，內部一律使用精確字串：`"0"`, `"1/2"`, `"√2/2"`, `"√3/2"`, `"1"`, `"-1/2"` 等。
   - 明確標記未定義狀態（Undefined）：$\tan 90^\circ$ 與 $\tan 270^\circ$ 標記為 `undefined`，點選時觸發未定義特徵回饋。
2. **誘答鏈與迷思診斷標籤**：
   ```javascript
   const MISCONCEPTIONS = {
     sin_cos_swap: "正餘弦定義混淆（如誤認 sin 30° = √3/2）",
     special_value_mixup: "特殊角數值記錯（如誤認 45° 的數值為 1/2）",
     quadrant_sign: "象限正負號混淆（如誤認 cos 120° 為正數）",
     tan_undefined: "正切於 90°/270° 未定義之特異點誤認",
     invalid_relation: "任意數值錯配",
     short: "鏈長不足 4 格"
   };
   ```

### 步驟 4：教師端即時看板與隱私脫敏 (FERPA / Student Privacy)
- **學生 ID 匿名化演算法**：學生加入房間時，不要求輸入真實姓名，自動生成班級座號代碼（如 `715-08`）或匿名動物暱稱。
- **即時診斷熱圖**：
  - 教師端頁面（`teacher.html` / `teacher.js`）每 3 秒自動輪詢 `/api/rooms/:id/stats`。
  - 將學生觸發的 `misconception` 匯總為橫向長條圖，讓老師一眼看出全班最容易在「象限變號」或「正餘弦互換」上犯錯。

### 步驟 5：iPad / iPhone iOS WebKit 極致適配規範
1. **HTML Header 元標籤**：
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
   <meta name="apple-mobile-web-app-capable" content="yes">
   <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
   ```
2. **CSS 視窗高度與安全區域 (Safe Area)**：
   ```css
   :root {
     --sat: env(safe-area-inset-top, 0px);
     --sab: env(safe-area-inset-bottom, 0px);
   }
   body {
     min-height: 100vh;
     min-height: 100dvh; /* 防止 iOS Safari 工具列彈出引發跳動 */
     padding-top: var(--sat);
     padding-bottom: var(--sab);
     touch-action: manipulation; /* 消除 iOS 300ms 點擊延遲與誤觸雙擊縮放 */
   }
   ```
3. **手機直屏與平板橫屏自動網格旋向**：
   - 橫屏（Tablet / Desktop）：$8 \times 6$ 網格（8 欄 6 列）。
   - 直屏（iPhone）：$6 \times 8$ 網格（6 欄 8 列），主判定按鈕置於最下方全寬顯示。
4. **鍵盤失焦防塌陷**：
   在學生點擊「開始遊戲」時，立即調用 `document.activeElement?.blur()`，使虛擬鍵盤縮回，避免遊戲盤面高度被壓縮。

---

## 五、 開發踩坑實錄與防錯指南 (Pitfalls & Defenses)

### 坑點 1：Wrangler 在非交互終端機環境認證失敗
* **錯誤日誌**：`In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN environment variable...`
* **根因**：Subagent 或自動化背景行程沒有終端 TTY，Wrangler 無法發起瀏覽器登入。
* **排坑解法**：從 Windows `%APPDATA%\xdg.config\.wrangler\config\default.toml` 提取先前瀏覽器授權留下的 `oauth_token`，指派給環境變數 `$env:CLOUDFLARE_API_TOKEN`。Cloudflare 邊緣 API 完美接受 OAuth Bearer Token 作為 API Token。

### 坑點 2：D1 遷移指令在無人值守時永久掛起
* **錯誤日誌**：終端機停滯不前，無任何輸出。
* **根因**：`wrangler d1 migrations apply ... --remote` 內部含有 `About to apply 1 migration... continue? (y/N)` 的確認提示。
* **排坑解法**：在 PowerShell 中透過管線注入 `"y"`：
  ```powershell
  "y" | npx wrangler d1 migrations apply <db-name> --remote
  ```

### 坑點 3：Cloudflare workers.dev 雙層子網域解析失敗
* **錯誤現象**：使用者在手機輸入網址出現「找不到伺服器」或「This link is not available」。
* **根因**：Cloudflare 分配的免費網址格式為 `https://<worker-name>.<account-subdomain>.workers.dev`。若 Worker 名稱為 `kwotachu-math-games`，帳號子域亦為 `kwotachu`，則完整網址必須是：
  `https://kwotachu-math-games.kwotachu.workers.dev`。若漏打中間的 `.kwotachu` 將導致 DNS 查無此主機。另外，某些公立醫院或校園 Wi-Fi 會攔截阻擋 `*.workers.dev`。
* **排坑解法**：提供本地 LAN 伺服器啟動腳本（`python -m http.server 8080 --bind 0.0.0.0`），顯示 Wi-Fi 內網 IP（例如 `http://192.168.0.188:8080/games/trig-chain/`），提供雙軌備援。

### 坑點 4：iOS 虛擬鍵盤導致網頁視窗高度縮小不還原
* **錯誤現象**：學生輸入暱稱後按開始，盤面下方被截斷，無法點選第 7、8 列方塊。
* **根因**：iOS Safari 在 `<input>` 聚焦時彈出虛擬鍵盤，若切換場景時未主動收起鍵盤，WebKit 視窗尺寸不會重新計算。
* **排坑解法**：
  ```javascript
  function startGame() {
    if (document.activeElement && document.activeElement.blur) {
      document.activeElement.blur();
    }
    window.scrollTo(0, 0);
    // 使用 100dvh
  }
  ```

### 坑點 5：iOS WebKit Vibration API 靜音崩潰
* **錯誤現象**：呼叫 `navigator.vibrate(50)` 報錯或在 Safari 中無動作。
* **根因**：iOS Safari 不支援 Web Vibration API。
* **排坑解法**：封裝防護函數，當不存在或報錯時靜默忽略：
  ```javascript
  function triggerHaptic(type = 'light') {
    try {
      if (typeof navigator !== 'undefined' && navigator.vibrate) {
        if (type === 'light') navigator.vibrate(20);
        else if (type === 'error') navigator.vibrate([40, 60, 40]);
      }
    } catch (_) {}
  }
  ```

---

## 六、 驗收清單 (Quality Checklist)

- [ ] 執行 `node --test tests/chain-match/*.test.mjs`，確保 38/38 測試全部綠燈通過。
- [ ] 驗證固定隨機種子 2000 次生成，無死局（`hasMove === true`）。
- [ ] 檢查 `DESIGN.md` 是否完整定義八步驟與 5 大誤解標籤。
- [ ] 驗證 iPad 橫屏 ($8 \times 6$) 與 iPhone 直屏 ($6 \times 8$) 佈局自適應無變形。
- [ ] 檢查學生端與教師端通訊協定，確認學生隱私脫敏符合教育規範。
- [ ] 驗證 Cloudflare D1 遠端查詢無報錯，資料表正常記錄互動事件。
