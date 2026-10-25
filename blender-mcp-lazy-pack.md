# Blender MCP 跨平台設定懶人包

> 本懶人包根據 2026-10-16 在 Windows 11 上實際完成的設定流程整理、驗證。
> 方案:**MCP for Blender**(Siddharth Ahuja,<https://mcp-for-blender.com/>),
> MCP server 用 `uvx mcp-for-blender` 啟動,Blender 端裝 `blender_mcp.py` addon(v1.8+)。

---

## 架構(30 秒理解)

```
AI client (opencode / Claude / Cursor ...)
   │  MCP 協議 (stdio)
   ▼
uvx mcp-for-blender          ← MCP server,client 啟動時自動拉起
   │  localhost socket(預設 port 9876)
   ▼
Blender addon「MCP for Blender」 ← 必須開著 Blender 且按下 Connect
```

**關鍵觀念**:MCP server 只是橋;**Blender 本人必須開著、addon 必須按 Connect**,AI 才控制得到。

---

## 前置需求

| 需求 | 說明 |
|------|------|
| Blender 4.x | 3.0+ 即可,建議最新 LTS |
| uv | Astral 的 Python 套件/工具管理器,提供 `uvx` 指令 |
| 任一 MCP client | opencode、Claude Code、Claude Desktop、Cursor、Codex... |
| 網路 | 第一次跑 `uvx mcp-for-blender` 會下載套件 |

---

## Step 1:安裝 Blender(已裝就跳過)

| 平台 | 指令 / 方式 |
|------|------------|
| Windows | `winget install BlenderFoundation.Blender`,或 blender.org 下載安裝檔 |
| macOS | `brew install --cask blender`,或 blender.org 下載 dmg |
| Linux | `sudo snap install blender --classic`,或 flatpak / 官網 tarball |

---

## Step 2:安裝 uv(已裝就跳過)

```powershell
# Windows(PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# macOS 也可以:brew install uv
```

裝完**重開 terminal**,確認:

```bash
uv --version && uvx --version
```

---

## Step 3:一鍵設定(官方自動化,推薦)

```bash
uvx mcp-for-blender setup --yes
```

這一條指令會自動:
1. 把 addon `blender_mcp.py` 複製到偵測到的 Blender addons 目錄
2. 嘗試在 Blender 偏好設定中啟用 addon
3. 設定所有偵測到的 MCP client(opencode、Claude、Cursor 等)

先看它會動什麼再決定:`uvx mcp-for-blender setup --dry-run`
只裝 addon、不碰 client 設定:`uvx mcp-for-blender install-addon`

> 昨天這台機器就是用這條路徑完成的:addon 落在
> `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\blender_mcp.py`。

---

## Step 4:手動設定 client(`setup` 沒涵蓋你的 client 時)

### opencode — `~/.config/opencode/opencode.json(c)`

```jsonc
"mcp": {
  "blender": {
    "type": "local",
    "command": ["uvx", "mcp-for-blender"],
    "enabled": true
  }
}
```

### Claude Code(terminal 一條指令)

```bash
claude mcp add blender -- uvx mcp-for-blender
```

### Claude Desktop / Cursor — 設定檔

macOS:`~/Library/Application Support/Claude/claude_desktop_config.json`
Windows:`%APPDATA%\Claude\claude_desktop_config.json`
Cursor:`~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"]
    }
  }
}
```

### Codex — `~/.codex/config.toml`

```toml
[mcp_servers.blender]
command = "uvx"
args = ["mcp-for-blender"]
```

---

## Step 5:啟動連線(每次使用都要做)

1. 開 Blender
2. 若是手動裝 addon:Edit → Preferences → Add-ons → 搜 `MCP for Blender` → 打勾
3. 3D Viewport 按 `N` 開側欄 → **MCP for Blender** 分頁
4. 按 **Connect to MCP server**(預設 port 9876)
5. 再開你的 AI client,開始下指令

> 順序建議:先開 Blender + Connect,再開 client。client 的工具呼叫才有東西可連。

---

## 驗證(30 秒)

- client 裡叫 `get_addon_status`:回傳 Blender 版本、addon 版本、開著的 libraries/generators → 成功
- 回傳 `Could not connect to Blender` → Blender 沒開或沒按 Connect(見疑難排解)
- CLI 檢查 addon 安裝位置:

```bash
uvx mcp-for-blender addon-paths
```

---

## 更新

```bash
uvx mcp-for-blender update
```

一次更新 MCP server 本身 + 已安裝的 Blender addon 到最新 release。

> **Blender 升級版本後**(例如 4.5 → 4.6),addon 目錄會換,需重跑
> `uvx mcp-for-blender install-addon` 再到 Preferences 啟用一次。

---

## 疑難排解

| 症狀 | 原因 / 解法 |
|------|------------|
| `Could not connect to Blender` | ① Blender 沒開 ② 開了但側欄沒按 **Connect to MCP server** ③ addon 沒啟用 |
| Port 9876 被佔用 | addon 面板改 port,MCP server 端用 `uvx mcp-for-blender --port 9999` 或環境變數 `BLENDER_PORT=9999`,兩邊要一致 |
| 第一次跑 `uvx` 卡很久 | 在下載套件,正常;之後有 cache 就快 |
| Windows 跑 uv 安裝腳本被擋 | PowerShell 執行政策,用上面的 `ByPass` 參數版本 |
| `uvx` 找不到指令 | 裝完 uv 沒重開 terminal;或手動把 `~/.local/bin`(Win:`%USERPROFILE%\.local\bin`)加進 PATH |
| client 工具列表沒有 blender_* | client 設定檔沒存到 / JSON 語法錯 / 改完沒重啟 client |
| Addon 版本跟 server 不匹配 | 跑 `uvx mcp-for-blender update` 讓兩邊同步 |
| 不想被收集使用數據 | Blender → Preferences → Add-ons → Blender MCP 關掉 telemetry |

### 安全性提醒

`execute_blender_code` 能在 Blender 裡跑任意 Python。socket 只聽 localhost,風險有限,
但**不要**把 port 對外暴露,也不要在不信任的專案裡讓 agent 自由發揮。

---

## 跨平台路徑速查表

| 東西 | Windows | macOS | Linux |
|------|---------|-------|-------|
| Blender user addons | `%APPDATA%\Blender Foundation\Blender\<ver>\scripts\addons\` | `~/Library/Application Support/Blender/<ver>/scripts/addons/` | `~/.config/blender/<ver>/scripts/addons/` |
| addon 檔案 | 上列目錄下的 `blender_mcp.py` | 同左 | 同左 |
| uv / uvx 位置 | `%USERPROFILE%\.local\bin` | `~/.local/bin`(或 brew) | `~/.local/bin` |
| opencode 設定 | `%USERPROFILE%\.config\opencode\opencode.json(c)` | `~/.config/opencode/` | `~/.config/opencode/` |
| Claude Desktop 設定 | `%APPDATA%\Claude\claude_desktop_config.json` | `~/Library/Application Support/Claude/` | — |

> 不確定 Blender addons 目錄在哪,直接問:`uvx mcp-for-blender addon-paths`

---

## 附錄:昨天(2026-10-16)這台 Windows 機器的實際狀態

| 項目 | 值 |
|------|---|
| Blender | 4.5 |
| uv | 0.11.28 |
| MCP server | `mcp-for-blender`(uvx 啟動,`setup/install-addon/addon-paths/update` 四個子指令) |
| Addon | `blender_mcp.py` v1.8,protocol v13,10:40 安裝 |
| 註冊的 client | opencode(`opencode.jsonc`,`"command": ["uvx", "mcp-for-blender"]`) |

## 指令總覽(複製用)

```bash
# 安裝 uv 後,一路到底:
uvx mcp-for-blender setup --yes        # 裝 addon + 設 client(自動)
uvx mcp-for-blender addon-paths        # 檢查 addon 裝在哪
uvx mcp-for-blender update             # 日後更新
# Blender 裡:側欄 N → MCP for Blender → Connect to MCP server
```
