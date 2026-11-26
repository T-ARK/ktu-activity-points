"""Unit tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import store

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    store.reset_to_defaults()
    yield
    store.reset_to_defaults()


def test_healthcheck():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_profile_endpoints():
    # GET default
    res = client.get("/api/profile")
    assert res.status_code == 200
    data = res.json()
    assert data["student_id"] == "KTU2024STU01"
    assert data["scheme"] == "2024"

    # POST update
    data["full_name"] = "Jane Doe"
    data["is_pwd"] = True
    update_res = client.post("/api/profile", json=data)
    assert update_res.status_code == 200
    assert update_res.json()["full_name"] == "Jane Doe"
    assert update_res.json()["is_pwd"] is True


def test_rules_endpoints():
    res = client.get("/api/rules")
    assert res.status_code == 200
    data = res.json()
    assert len(data["rules"]) == 64

    # Single rule
    single_res = client.get("/api/rules/1.1")
    assert single_res.status_code == 200
    assert single_res.json()["id"] == "1.1"

    # Non-existent
    bad_res = client.get("/api/rules/99.99")
    assert bad_res.status_code == 404


def test_activities_and_dashboard():
    # Initially empty
    act_res = client.get("/api/activities")
    assert act_res.status_code == 200
    assert act_res.json() == []

    # Load sample
    sample_res = client.post("/api/activities/load-sample")
    assert sample_res.status_code == 200
    assert len(sample_res.json()) == 8

    # Check dashboard evaluation
    dash_res = client.get("/api/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()

    engine_res = dash_data["engine_result"]
    assert "total_bracket" in engine_res
    assert engine_res["total_bracket"]["confirmed"] > 0
    assert engine_res["total_bracket"]["upper_bound"] >= engine_res["total_bracket"]["confirmed"]
    assert "I" in engine_res["groups"]
    assert "II" in engine_res["groups"]
    assert "III" in engine_res["groups"]
    assert "disclaimer" in dash_data


def test_export_endpoints():
    # Load sample activities first
    client.post("/api/activities/load-sample")

    # CSV Export
    csv_res = client.get("/api/export?format=csv")
    assert csv_res.status_code == 200
    assert csv_res.headers["content-type"].startswith("text/csv")
    csv_text = csv_res.text
    assert "APJ ABDUL KALAM TECHNOLOGICAL UNIVERSITY" in csv_text
    assert "SUMMARY BRACKETS" in csv_text
    assert "Staff Advisor (SFA)" in csv_text

    # PDF Export
    pdf_res = client.get("/api/export?format=pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content.startswith(b"%PDF")
