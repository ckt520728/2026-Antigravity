"""測試 Excel 與 Word 報表匯出功能。"""

from __future__ import annotations

import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_reporting.db"

from app.core.config import get_settings
get_settings.cache_clear()

from app.core.database import Base, engine, SessionLocal
from app.core.feature_store import FeatureFlagService
from app.main import app
from app.scripts.import_nursing_roster import load_nursing_roster, import_to_db


@pytest.fixture(scope="module", autouse=True)
def setup_reporting_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        FeatureFlagService.seed_defaults(db)
        excel_path = Path("護理之家員工名冊.xlsx")
        if not excel_path.exists():
            excel_path = Path("../護理之家員工名冊.xlsx")
        records = load_nursing_roster(excel_path)
        import_to_db(records, db)
    yield
    Base.metadata.drop_all(bind=engine)


def test_kiosk_excel_export():
    client = TestClient(app)
    response = client.get("/api/v1/reports/kiosk/excel?period_start=2026-08-01&period_end=2026-08-31")
    assert response.status_code == 200
    assert "spreadsheetml.sheet" in response.headers["content-type"]
    assert len(response.content) > 1000
    assert response.content[:4] == b"PK\x03\x04"  # Zip header for XLSX


def test_kiosk_word_export():
    client = TestClient(app)
    response = client.get("/api/v1/reports/kiosk/word?period_start=2026-08-01&period_end=2026-08-31")
    assert response.status_code == 200
    assert "wordprocessingml.document" in response.headers["content-type"]
    assert len(response.content) > 1000
    assert response.content[:4] == b"PK\x03\x04"  # Zip header for DOCX
