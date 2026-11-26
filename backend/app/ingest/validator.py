"""Stage 1: Document Ingest & Validation (SPEC §7.1)."""

import hashlib
from typing import BinaryIO

import pypdf
from pydantic import BaseModel


class IngestResult(BaseModel):
    sha256: str
    file_type: str
    file_size_bytes: int
    page_count: int
    is_valid: bool
    is_encrypted: bool
    error_code: str | None = None
    error_message: str | None = None


MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB
MAX_PAGE_COUNT = 10
ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
}


def validate_document(
    stream: BinaryIO,
    filename: str,
    content_type: str | None = None,
    existing_hashes: set[str] | None = None,
) -> IngestResult:
    """Validates uploaded document against Stage 1 integrity checks."""
    content = stream.read()
    file_size = len(content)

    # 1. Size check
    if file_size > MAX_FILE_SIZE_BYTES:
        return IngestResult(
            sha256="",
            file_type="unknown",
            file_size_bytes=file_size,
            page_count=0,
            is_valid=False,
            is_encrypted=False,
            error_code="Q-06",
            error_message="File exceeds maximum allowed size of 15 MB",
        )

    # 2. Hash computation
    sha256_hash = hashlib.sha256(content).hexdigest()

    # 3. Duplicate upload detection (F-04)
    if existing_hashes and sha256_hash in existing_hashes:
        return IngestResult(
            sha256=sha256_hash,
            file_type="unknown",
            file_size_bytes=file_size,
            page_count=0,
            is_valid=False,
            is_encrypted=False,
            error_code="F-04",
            error_message="Duplicate certificate upload: file already submitted",
        )

    # 4. MIME & Type check
    mime = (content_type or "").lower().strip()
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext == "pdf" or mime == "application/pdf":
        file_type = "pdf"
    elif ext in {"jpg", "jpeg"} or mime in {"image/jpeg", "image/jpg"}:
        file_type = "jpg"
    elif ext == "png" or mime == "image/png":
        file_type = "png"
    else:
        return IngestResult(
            sha256=sha256_hash,
            file_type="unknown",
            file_size_bytes=file_size,
            page_count=0,
            is_valid=False,
            is_encrypted=False,
            error_code="Q-06",
            error_message="Unsupported file type. Allowed formats: PDF, JPG, PNG",
        )

    # 5. PDF verification (page count, corruption, encryption)
    page_count = 1
    if file_type == "pdf":
        try:
            import io

            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            if pdf_reader.is_encrypted:
                return IngestResult(
                    sha256=sha256_hash,
                    file_type="pdf",
                    file_size_bytes=file_size,
                    page_count=0,
                    is_valid=False,
                    is_encrypted=True,
                    error_code="Q-06",
                    error_message="PDF file is password protected or encrypted",
                )
            page_count = len(pdf_reader.pages)
            if page_count > MAX_PAGE_COUNT:
                return IngestResult(
                    sha256=sha256_hash,
                    file_type="pdf",
                    file_size_bytes=file_size,
                    page_count=page_count,
                    is_valid=False,
                    is_encrypted=False,
                    error_code="Q-05",
                    error_message=f"Document exceeds max 10 pages (got {page_count} pages)",
                )
        except Exception as e:
            return IngestResult(
                sha256=sha256_hash,
                file_type="pdf",
                file_size_bytes=file_size,
                page_count=0,
                is_valid=False,
                is_encrypted=False,
                error_code="Q-06",
                error_message=f"Corrupt or unreadable PDF: {str(e)}",
            )

    return IngestResult(
        sha256=sha256_hash,
        file_type=file_type,
        file_size_bytes=file_size,
        page_count=page_count,
        is_valid=True,
        is_encrypted=False,
    )
