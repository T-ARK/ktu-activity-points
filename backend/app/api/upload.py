"""Upload API endpoints for document processing."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.ingest.pipeline import process_certificate_document
from app.schemas.facts import CertificateFacts
from app.storage import store

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("", response_model=CertificateFacts)
async def upload_document(file: UploadFile = File(...)) -> CertificateFacts:  # noqa: B008
    """Accepts document uploads (PDF, PNG, JPG), runs full pipeline and returns CertificateFacts."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    existing_hashes = {getattr(a, "file_hash", "") for a in store.activities if getattr(a, "file_hash", None)}

    fact, _ = process_certificate_document(
        stream=file.file,
        filename=file.filename,
        content_type=file.content_type,
        profile=store.profile,
        ruleset=store.ruleset,
        existing_hashes=existing_hashes,
    )

    store.activities.append(fact)
    return fact
