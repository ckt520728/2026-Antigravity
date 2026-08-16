"""Kiosk 電腦網頁版打卡 API 測試。"""

from __future__ import annotations

import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_kiosk.db"

from app.core.config import get_settings
get_settings.cache_clear()

from app.core.database import Base, engine, SessionLocal
from app.core.feature_store import FeatureFlagService
from app.main import app
from app.scripts.import_nursing_roster import load_nursing_roster, import_to_db
from pathlib import Path


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        FeatureFlagService.seed_defaults(db)
        # 匯入名冊
        excel_path = Path("護理之家員工名冊.xlsx")
        if not excel_path.exists():
            excel_path = Path("../護理之家員工名冊.xlsx")
        records = load_nursing_roster(excel_path)
        import_to_db(records, db)
    yield
    Base.metadata.drop_all(bind=engine)


def test_kiosk_staff_list():
    client = TestClient(app)
    response = client.get("/api/v1/attendance/kiosk/staff")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 28
    emp_nos = [d["employee_no"] for d in data]
    assert "YM-DOC-01" in emp_nos
    assert "YM-NUR-01" in emp_nos


def test_kiosk_punch_check_in_and_out():
    client = TestClient(app)
    
    # 護理師上班打卡
    payload_in = {
        "employee_no": "YM-NUR-01",
        "event_type": "CHECK_IN",
        "station_id": "YM-3F-KIOSK",
    }
    res_in = client.post("/api/v1/attendance/kiosk/punch", json=payload_in)
    assert res_in.status_code == 201
    data_in = res_in.json()
    assert "林玟亭" in data_in["message"]
    assert data_in["event_type"] == "CHECK_IN"

    # 朱醫師巡診簽到
    payload_doc = {
        "employee_no": "YM-DOC-01",
        "event_type": "CLINICAL_ROUND_SIGN_IN",
        "station_id": "YM-3F-KIOSK",
        "ward_code": "3F-NH",
    }
    res_doc = client.post("/api/v1/attendance/kiosk/punch", json=payload_doc)
    assert res_doc.status_code == 201
    data_doc = res_doc.json()
    assert "朱國大" in data_doc["message"]
    assert data_doc["event_type"] == "CLINICAL_ROUND_SIGN_IN"
    assert data_doc["ward_code"] == "3F-NH"

    # 查詢打卡流水
    res_history = client.get("/api/v1/attendance/kiosk/recent-punches")
    assert res_history.status_code == 200
    history = res_history.json()
    assert len(history) >= 2
