"""陽明醫院附設護理之家員工名冊匯入腳本 (依照選項 A 編碼規則)。

嚴格遵守 CLAUDE.md 紅線規則：
- R1/R5：不儲存密碼或生物特徵
- R7：建立沙盒試辦帳號，保留稽核軌跡
- 機構對象：僅限「陽明醫院附設護理之家 (YM-)」，排除其他非本案機構
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
import openpyxl
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.enums import AuditAction, EmploymentType, StaffRole, Unit
from app.modules.audit import service as audit
from app.modules.identity.models import Staff


def parse_job_role_and_unit(
    job_title: str, is_supervisor: bool = False
) -> tuple[StaffRole, Unit]:
    """解析職務名稱對應到系統角色與單位。"""
    job = str(job_title).strip()
    unit = Unit.INPATIENT  # 陽明醫院附設護理之家 (3F 病房/長照)

    if is_supervisor:
        role = StaffRole.SUPERVISOR
    elif "護理" in job:
        role = StaffRole.NURSE
    elif "照顧服務員" in job:
        role = StaffRole.NURSE
    elif "醫師" in job:
        role = StaffRole.DOCTOR
    elif "營養" in job:
        role = StaffRole.MEDICAL_ADMIN
    elif "藥師" in job or "復健" in job or "物理" in job:
        role = StaffRole.MEDICAL_ADMIN
    elif "社工" in job:
        role = StaffRole.MEDICAL_ADMIN
    elif "行政" in job or "總務" in job or "廚工" in job:
        role = StaffRole.REGISTRATION
    else:
        role = StaffRole.REGISTRATION

    return role, unit


def load_nursing_roster(file_path: Path) -> list[dict[str, Any]]:
    """解析 Excel 檔案中「陽明醫院附設護理之家」的名冊資料 (共 28 筆)。"""
    wb = openpyxl.load_workbook(file_path, data_only=True)
    records: list[dict[str, Any]] = []
    role_counters: dict[str, int] = {}

    # Sheet 0: 全員名冊 (陽明醫院附設護理之家)
    ws = wb.worksheets[0]
    for row in list(ws.iter_rows(values_only=True))[3:]:
        if not row or not row[0] or not row[3]:
            continue
        seq, emp_type_raw, job, name, pid, gender = (
            str(row[0]).strip(),
            str(row[1]).strip() if row[1] else "正職",
            str(row[2]).strip(),
            str(row[3]).strip(),
            str(row[4]).strip() if row[4] else "",
            str(row[5]).strip() if row[5] else "",
        )

        prefix = "YM"
        is_sup = "負責人" in job

        if "護理" in job:
            cat = "NUR"
        elif "外籍" in job:
            cat = "FCNA"
        elif "照顧服務員" in job:
            cat = "CNA"
        elif "醫師" in job:
            cat = "DOC"
        elif "營養" in job:
            cat = "NUT"
        elif "廚工" in job:
            cat = "KIT"
        elif "總務" in job or "行政" in job:
            cat = "ADM"
        elif "復健" in job or "物理" in job:
            cat = "PT"
        elif "藥師" in job:
            cat = "PHAR"
        elif "社工" in job:
            cat = "SW"
        elif "居家" in job:
            cat = "HN"
        else:
            cat = "STAFF"

        cnt = role_counters.get(cat, 0) + 1
        role_counters[cat] = cnt
        emp_no = f"{prefix}-{cat}-{cnt:02d}"

        role, unit = parse_job_role_and_unit(job, is_supervisor=is_sup)
        emp_type = (
            EmploymentType.PART_TIME
            if "兼任" in emp_type_raw
            else EmploymentType.FULL_TIME
        )

        records.append({
            "employee_no": emp_no,
            "name": name,
            "facility": "陽明醫院附設護理之家",
            "job_title": job,
            "unit": unit,
            "role": role,
            "employment_type": emp_type,
            "active": True,
            "gender": gender,
        })

    return records


def import_to_db(records: list[dict[str, Any]], db: Session) -> dict[str, int]:
    """將名冊資料寫入資料庫 Staff 表。"""
    created = 0
    updated = 0

    for r in records:
        existing = db.execute(
            select(Staff).where(Staff.employee_no == r["employee_no"])
        ).scalar_one_or_none()

        if existing is None:
            staff = Staff(
                employee_no=r["employee_no"],
                name=r["name"],
                unit=r["unit"],
                role=r["role"],
                employment_type=r["employment_type"],
                active=r["active"],
            )
            db.add(staff)
            db.flush()
            audit.record(
                db,
                action=AuditAction.CREATE,
                entity_type="staff",
                entity_id=staff.id,
                actor_id=staff.id,
                after={
                    "employee_no": r["employee_no"],
                    "name": r["name"],
                    "facility": r["facility"],
                    "job_title": r["job_title"],
                },
                reason="陽明護理之家名冊初次匯入",
            )
            created += 1
        else:
            existing.name = r["name"]
            existing.unit = r["unit"]
            existing.role = r["role"]
            existing.employment_type = r["employment_type"]
            existing.active = r["active"]
            updated += 1

    db.commit()
    return {"created": created, "updated": updated, "total": len(records)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="匯入陽明醫院附設護理之家員工名冊")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("護理之家員工名冊.xlsx"),
        help="Excel 名冊路徑",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="是否實際寫入資料庫 (預設為乾跑 dry-run)",
    )
    args = parser.parse_args()

    parsed_records = load_nursing_roster(args.file)
    print(f"成功解析【陽明醫院附設護理之家】名冊紀錄共 {len(parsed_records)} 筆：")
    for r in parsed_records:
        print(f"  [{r['employee_no']}] {r['name']:<6} | {r['job_title']:<18} | {r['employment_type'].value:<10} | {'在職' if r['active'] else '離職'}")

    if args.commit:
        from app.core.database import Base, engine
        from app import models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as session:
            res = import_to_db(parsed_records, session)
            print(f"\n[資料庫寫入完成] 新增: {res['created']}, 更新: {res['updated']}, 總計: {res['total']}")
    else:
        print("\n[Dry-run] 未指定 --commit，尚未變更資料庫。")
