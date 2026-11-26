"""Unit tests for Document Upload & SFA API endpoints."""

import io

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.facts import CertificateFacts
from app.schemas.verdict import Verdict
from app.storage import store

client = TestClient(app)


def test_upload_api_pdf_pipeline():
    # Setup test PDF
    pdf_content = (
        b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000124 00000 n \n"
        b"trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n178\n%%EOF"
    )

    files = {"file": ("test_cert.pdf", io.BytesIO(pdf_content), "application/pdf")}
    res = client.post("/api/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "certificate_id" in data
    assert data["verdict"] in [Verdict.VERIFIED.value, Verdict.DOUBT.value]


def test_sfa_api_workflow():
    store.activities.clear()

    # Add a doubtful activity
    fact = CertificateFacts(
        certificate_id="sfa-review-01",
        rule_id="1.8",
        activity_title="Blood Donation Camp - Missing Counter Signature",
        verdict=Verdict.DOUBT,
        doubt_codes=["V-01"],
        student_asserted=True,
    )
    store.activities.append(fact)

    # 1. Fetch SFA Review Queue
    queue_res = client.get("/api/sfa/queue")
    assert queue_res.status_code == 200
    queue_data = queue_res.json()
    assert len(queue_data) == 1
    assert queue_data[0]["certificate_id"] == "sfa-review-01"

    # 2. Adjudicate (Verify)
    adj_payload = {
        "certificate_id": "sfa-review-01",
        "action": "verify",
        "sfa_name": "Prof. S. Nair",
        "reason": "Counter-signed copy verified in department records",
    }
    adj_res = client.post("/api/sfa/adjudicate", json=adj_payload)
    assert adj_res.status_code == 200
    adj_data = adj_res.json()
    assert adj_data["new_verdict"] == "VERIFIED"
    assert adj_data["sfa_name"] == "Prof. S. Nair"

    # 3. Check Audit Log
    audit_res = client.get("/api/sfa/audit-log")
    assert audit_res.status_code == 200
    log_data = audit_res.json()
    assert len(log_data) >= 1
    assert log_data[-1]["certificate_id"] == "sfa-review-01"
