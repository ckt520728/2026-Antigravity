"""保存 JEV 原始程式與來源 pin；只寫本專案 workflow 目錄。"""
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = Path(r"D:\2026 JEV Engineering\skills\jev-engineering")
URL = "https://raw.githubusercontent.com/ckt520728/2026-Antigravity/main/.agents/skills/jev-engineering/SKILL.md"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    vendor = HERE / "vendor"
    vendor.mkdir(exist_ok=True)
    copied = []
    for path in (SOURCE / "assets" / "jev").rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        target = vendor / "jev" / path.relative_to(SOURCE / "assets" / "jev")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        copied.append({"path": target.relative_to(ROOT).as_posix(), "sha256": sha(target)})
    for relative in ("SKILL.md", "references/18-two-phase-workflow.md"):
        target = vendor / "local" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / relative, target)
        copied.append({"path": target.relative_to(ROOT).as_posix(), "sha256": sha(target)})
    request = urllib.request.Request(URL, headers={"User-Agent": "Mounjaro-project-initialization"})
    with urllib.request.urlopen(request, timeout=30) as response:
        remote_bytes = response.read()
    remote = vendor / "github-SKILL.md"
    remote.write_bytes(remote_bytes)
    copied.append({"path": remote.relative_to(ROOT).as_posix(), "sha256": sha(remote)})
    pin = {"date": "2026-10-29", "local_source": str(SOURCE), "github_url": URL,
           "pin_kind": "原始 bytes 的 SHA-256；main 可變，未宣稱 Git commit pin",
           "local_remote_identical": (vendor / "local/SKILL.md").read_bytes() == remote_bytes,
           "files": copied,
           "warning": "vendor registry 的 API ID、價格與 swarm 宣稱是上游資料，未驗證、未用於本次派工或費用報告。"}
    (HERE / "source-pin.json").write_text(json.dumps(pin, ensure_ascii=False, indent=2), encoding="utf-8")
    preserved = list(ROOT.glob("*.zip")) + [ROOT / n for n in ("CLAUDE.md", "handoff.md", "RESEARCH_STATE.md", "2026 GLP-1 RA Monjaro.txt")]
    for folder in ("analysis", "blog", "evidence", "paper", "publication", "scripts", "sources"):
        preserved.extend(p for p in (ROOT / folder).rglob("*") if p.is_file())
    baseline = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "size": p.stat().st_size} for p in preserved]
    baseline_path = HERE / "preservation-baseline.json"
    if baseline_path.exists():
        raise RuntimeError("來源基線已存在；不得用重跑覆蓋初始基線")
    baseline_path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"vendor_files": len(copied), "preserved_sources": len(baseline),
                      "local_remote_identical": pin["local_remote_identical"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
