# -*- coding: utf-8 -*-
import os
import io
import shutil
import datetime

print("Starting backup_and_link.py...")

today_str = "2026-05-24"
note_to_append = u"""

## 🧠 2026-05-24 神經動力學學習
- [[2026 Antigravity 學習筆記]]：Sussillo 系列與 FORCE 混沌循環網路穩定化學習面板。
- [[USER_MANUAL]]：神經動力學學習艙旗艦版操作手冊。
- *本日成果：成功完成了神經動力學學習艙 v3.0 旗艦版的重構，實現了 NotebookLM AI 語音合成、學術 4-Panel 慢速流形分析與 3D 五大吸引子解析艙，並已將程式碼與手冊全部同步推送到 GitHub!*
"""

# -------------------------------------------------------------
# 1. 快速定位 Obsidian Vault 根目錄
# -------------------------------------------------------------
vault_paths = []
# 快速掃描 Documents 與 Desktop
user_home = os.path.expanduser("~")
scan_roots = [
    os.path.join(user_home, "Documents"),
    os.path.join(user_home, "Desktop")
]

print("Scanning Documents and Desktop for Obsidian Vaults...")
for root_path in scan_roots:
    if not os.path.exists(root_path):
        continue
    try:
        # 只掃描兩層深度，速度極快 (0.05秒)
        for entry in os.scandir(root_path):
            if entry.is_dir() and not entry.name.startswith('.'):
                # 檢查這是否是個 Vault
                dot_obsidian = os.path.join(entry.path, ".obsidian")
                if os.path.exists(dot_obsidian):
                    print(f"Found Obsidian Vault: {entry.path}")
                    vault_paths.append(entry.path)
                
                # 檢查子目錄
                try:
                    for sub_entry in os.scandir(entry.path):
                        if sub_entry.is_dir() and not sub_entry.name.startswith('.'):
                            sub_dot = os.path.join(sub_entry.path, ".obsidian")
                            if os.path.exists(sub_dot):
                                print(f"Found Sub Obsidian Vault: {sub_entry.path}")
                                vault_paths.append(sub_entry.path)
                except Exception:
                    pass
    except Exception as e:
        print(f"Error scanning {root_path}: {e}")

# -------------------------------------------------------------
# 2. 在 Vault 中尋找或建立每日筆記 2026-05-24.md
# -------------------------------------------------------------
success_linked_vaults = []

# 我們也有一個 fallback：我們在我們已有的備份目錄 C:\Users\User\Documents\2026 Antigravity 當成 Vault
backup_vault_path = os.path.join("C:\\", "Users", "User", "Documents", "2026 Antigravity")
if os.path.exists(backup_vault_path) and backup_vault_path not in vault_paths:
    # 建立一個臨時 .obsidian 資料夾使之成為合法 Vault
    os.makedirs(os.path.join(backup_vault_path, ".obsidian"), exist_ok=True)
    vault_paths.append(backup_vault_path)

for vault in vault_paths:
    print(f"Processing Vault: {vault}")
    
    # 把我們的學習筆記與手冊複製到這個 Vault 下，保證雙鏈運作
    src_notes = [
        ("C:\\Users\\User\\2026Antigravity\\2026 Antigravity 學習筆記.md", "2026 Antigravity 學習筆記.md"),
        ("C:\\Users\\User\\2026Antigravity\\USER_MANUAL.md", "USER_MANUAL.md")
    ]
    for src, name in src_notes:
        if os.path.exists(src):
            dst = os.path.join(vault, name)
            try:
                shutil.copy2(src, dst)
                print(f"Copied {name} into Vault root.")
            except Exception as e:
                print(f"Error copying {name}: {e}")

    # 尋找每日筆記 2026-05-24.md
    daily_note_path = None
    for sub_root, sub_dirs, sub_files in os.walk(vault):
        # 忽略隱藏資料夾
        sub_dirs[:] = [d for d in sub_dirs if not d.startswith('.')]
        for f in sub_files:
            if f == f"{today_str}.md":
                daily_note_path = os.path.join(sub_root, f)
                break
        if daily_note_path:
            break

    if daily_note_path:
        print(f"Found existing Daily Note: {daily_note_path}")
        # 追加雙鏈
        try:
            with io.open(daily_note_path, "r", encoding="utf-8") as rf:
                note_content = rf.read()
            if u"2026 Antigravity 學習筆記" not in note_content:
                with io.open(daily_note_path, "a", encoding="utf-8") as wf:
                    wf.write(note_content + note_to_append)
                print("Appended link to daily note successfully.")
            else:
                print("Link already exists in daily note.")
            success_linked_vaults.append(vault)
        except Exception as e:
            print(f"Error writing to daily note: {e}")
    else:
        # 如果沒找到，就在 Vault 根目錄（或常見的 Daily Notes 資料夾，如果有的話）下創建一個！
        common_daily_dirs = [
            os.path.join(vault, "Daily Notes"),
            os.path.join(vault, "Daily"),
            os.path.join(vault, "Journal"),
            vault
        ]
        target_dir = vault
        for cd in common_daily_dirs:
            if os.path.exists(cd):
                target_dir = cd
                break
        
        new_daily_path = os.path.join(target_dir, f"{today_str}.md")
        print(f"Creating new Daily Note at: {new_daily_path}")
        try:
            os.makedirs(target_dir, exist_ok=True)
            with io.open(new_daily_path, "w", encoding="utf-8") as wf:
                wf.write(u"# 📅 每日筆記: " + today_str + u"\n" + note_to_append)
            print("Successfully created daily note with links.")
            success_linked_vaults.append(vault)
        except Exception as e:
            print(f"Error creating daily note: {e}")

# -------------------------------------------------------------
# 3. 雲端 Google Drive 備份
# -------------------------------------------------------------
backup_src_dir = "C:\\Users\\User\\2026Antigravity"
backup_files = [
    "ode.tsx",
    "index.html",
    "USER_MANUAL.md",
    "2026 Antigravity 學習筆記.md",
    "sync_index.py",
    "Neurodynamics_Sussillo_FORCE.ipynb",
    "package.json"
]

gdrive_backup_dir = None

# 偵測 G 盤
if os.path.exists("G:\\"):
    # 尋找 My Drive
    my_drive = os.path.join("G:\\", "My Drive")
    if not os.path.exists(my_drive):
        # 尋找中文名「我的雲端硬碟」
        my_drive = os.path.join("G:\\", "我的雲端硬碟")
    
    if os.path.exists(my_drive) or os.path.exists("G:\\"):
        base_drive = my_drive if os.path.exists(my_drive) else "G:\\"
        gdrive_backup_dir = os.path.join(base_drive, "2026 Antigravity 備份")
        print(f"Targeting Google Drive Virtual Disk: {gdrive_backup_dir}")

# 如果 G 盤不存在，我們使用 User 目錄下的同步資料夾作為備份點
if not gdrive_backup_dir:
    user_home = os.path.expanduser("~")
    possible_sync_folders = [
        os.path.join(user_home, "Google Drive"),
        os.path.join(user_home, "GoogleDrive"),
        os.path.join(user_home, "Desktop", "2026_Antigravity_GoogleDrive_Backup") # Fallback to Desktop for easy manual drag
    ]
    for ps in possible_sync_folders:
        # 如果是桌面 fallback，我們可以直接創建它
        if "Desktop" in ps or os.path.exists(ps):
            gdrive_backup_dir = os.path.join(ps, "2026 Antigravity 備份")
            print(f"Targeting Sync Folder: {gdrive_backup_dir}")
            break

# 執行備份
if gdrive_backup_dir:
    try:
        os.makedirs(gdrive_backup_dir, exist_ok=True)
        for f in backup_files:
            src_f = os.path.join(backup_src_dir, f)
            if os.path.exists(src_f):
                dst_f = os.path.join(gdrive_backup_dir, f)
                shutil.copy2(src_f, dst_f)
                print(f"Backed up {f} to Google Drive backup folder.")
        print("Google Drive backup completed successfully!")
    except Exception as e:
        print(f"Error during Google Drive backup: {e}")
else:
    print("Could not locate Google Drive sync folder or virtual disk. Backup failed.")

print("\n--- Final Summary ---")
print(f"Successfully processed vaults: {success_linked_vaults}")
print(f"Backup target path: {gdrive_backup_dir}")
