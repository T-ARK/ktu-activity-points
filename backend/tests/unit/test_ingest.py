"""Unit tests for Stage 1: Document Ingest & Validation (SPEC §7.1)."""

import io

from app.ingest.validator import validate_document


def test_validate_valid_pdf():
    # Minimal 1-page valid PDF header/footer
    content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000124 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n178\n%%EOF"
    stream = io.BytesIO(content)
    res = validate_document(stream, "cert.pdf", "application/pdf")

    assert res.is_valid is True
    assert res.file_type == "pdf"
    assert res.page_count == 1
    assert len(res.sha256) == 64


def test_validate_oversized_file():
    # 16 MB stream
    big_content = b"0" * (16 * 1024 * 1024)
    stream = io.BytesIO(big_content)
    res = validate_document(stream, "big.pdf", "application/pdf")

    assert res.is_valid is False
    assert res.error_code == "Q-06"
    assert "exceeds maximum allowed size" in (res.error_message or "")


def test_validate_unsupported_mime_type():
    stream = io.BytesIO(b"executable content")
    res = validate_document(stream, "cert.exe", "application/x-msdownload")

    assert res.is_valid is False
    assert res.error_code == "Q-06"
    assert "Unsupported file type" in (res.error_message or "")


def test_validate_duplicate_upload_detection():
    content = b"Sample certificate binary content"
    stream = io.BytesIO(content)
    res1 = validate_document(stream, "cert1.png", "image/png")
    assert res1.is_valid is True

    existing_hashes = {res1.sha256}
    stream2 = io.BytesIO(content)
    res2 = validate_document(stream2, "cert2.png", "image/png", existing_hashes=existing_hashes)

    assert res2.is_valid is False
    assert res2.error_code == "F-04"
    assert "Duplicate certificate upload" in (res2.error_message or "")
