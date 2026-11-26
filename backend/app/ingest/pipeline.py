"""Stage 1-7 Unified Pipeline: Ingest -> Text/OCR -> Classify -> Extract -> Reconcile -> Facts."""

import io
import uuid
from typing import Any, BinaryIO

from app.authenticity.verifier import inspect_authenticity
from app.classify.classifier import classify_document_to_rules
from app.doubt.verify import can_verify
from app.extract.path_a.events_and_community import (
    extract_dates_from_text,
    extract_level_from_text,
    extract_position_from_text,
    extract_recipient_name,
)
from app.extract.path_a.language_aptitude import (
    extract_aptitude_test,
    extract_language_test,
)
from app.extract.reconcile import reconcile_certificate_facts
from app.ingest.validator import validate_document
from app.ocr.ocr_engine import perform_ocr
from app.schemas.facts import CertificateFacts
from app.schemas.profile import StudentProfile
from app.schemas.verdict import Verdict
from app.text.extractor import extract_native_pdf_text


def process_certificate_document(
    stream: BinaryIO,
    filename: str,
    content_type: str | None,
    profile: StudentProfile,
    ruleset: dict[str, Any],
    existing_hashes: set[str] | None = None,
) -> tuple[CertificateFacts, list[str]]:
    """Executes the full pipeline on an uploaded document stream."""
    stream_content = stream.read()
    stream_io = io.BytesIO(stream_content)

    # 1. Ingest validation
    ingest_res = validate_document(
        stream=stream_io,
        filename=filename,
        content_type=content_type,
        existing_hashes=existing_hashes,
    )
    if not ingest_res.is_valid:
        error_code = ingest_res.error_code or "Q-06"
        fact = CertificateFacts(
            certificate_id=f"cert-{uuid.uuid4().hex[:8]}",
            rule_id="1.1",  # Placeholder on invalid ingest
            activity_title=f"Rejected Upload: {filename}",
            verdict=Verdict.DOUBT,
            doubt_codes=[error_code],
            student_asserted=True,
        )
        return fact, [error_code]

    # 2. Text Extraction (Native PDF first, OCR fallback)
    text_content = ""
    is_ocr = False
    ocr_conf = 100.0

    if ingest_res.file_type == "pdf":
        native_res = extract_native_pdf_text(stream_content)
        if native_res.has_text_layer:
            text_content = native_res.full_text
        else:
            # Scanned PDF without text layer -> OCR fallback
            ocr_res = perform_ocr(stream_content)
            text_content = ocr_res.text
            is_ocr = True
            ocr_conf = ocr_res.average_confidence
    else:
        # Image upload (PNG/JPG) -> OCR
        ocr_res = perform_ocr(stream_content)
        text_content = ocr_res.text
        is_ocr = True
        ocr_conf = ocr_res.average_confidence

    # 3. Authenticity Inspection
    auth_res = inspect_authenticity(
        content=stream_content,
        text=text_content,
        existing_hashes=existing_hashes,
        file_hash=ingest_res.sha256,
    )

    # 4. Classification to Candidate Rules (Stage 5)
    candidates = classify_document_to_rules(text_content, ruleset)
    pipeline_doubts: list[str] = list(auth_res.flags)

    if not candidates:
        rule_id = "1.1"
        pipeline_doubts.append("C-02")  # No candidate rule found
    elif len(candidates) > 1:
        rule_id = candidates[0].rule_id
        pipeline_doubts.append("C-01")  # Ambiguous category
    else:
        rule_id = candidates[0].rule_id

    # 5. Fact Extraction (Path A)
    extracted_quotes: list[str] = []

    # Recipient name
    candidate_name, name_quote = extract_recipient_name(text_content)
    if name_quote:
        extracted_quotes.append(name_quote)

    # Level & Position
    level_val, level_quote = extract_level_from_text(text_content)
    if level_quote:
        extracted_quotes.append(level_quote)
    if not level_val and rule_id in {"1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4"}:
        pipeline_doubts.append("C-03")

    position_val, pos_quote = extract_position_from_text(text_content)
    if pos_quote:
        extracted_quotes.append(pos_quote)

    # Dates
    dates_found = extract_dates_from_text(text_content)
    activity_date = dates_found[0][0] if dates_found else None
    if dates_found:
        extracted_quotes.append(dates_found[0][1])

    # Language/Aptitude scores
    score_val = None
    lang_res = extract_language_test(text_content)
    if lang_res and "score" in lang_res:
        score_val = lang_res["score"].value
        extracted_quotes.append(lang_res["score"].quote)

    apt_res = extract_aptitude_test(text_content)
    if apt_res and "score" in apt_res:
        score_val = apt_res["score"].value
        extracted_quotes.append(apt_res["score"].quote)

    # 6. Reconciliation & Strict Allow-List (Stage 4 & 10)
    analysis, recon_doubts = reconcile_certificate_facts(
        candidate_name=candidate_name,
        activity_date=activity_date,
        rule_id=rule_id,
        document_text=text_content,
        profile=profile,
        quotes=extracted_quotes,
        is_ocr_sourced=is_ocr,
        ocr_confidence=ocr_conf,
    )

    all_doubts = sorted(set(pipeline_doubts + recon_doubts))

    # G2 Guarantee: Verdict can ONLY be VERIFIED if can_verify() passes and no open doubts exist
    if can_verify(analysis) and len(all_doubts) == 0 and not is_ocr:
        verdict = Verdict.VERIFIED
    else:
        verdict = Verdict.DOUBT
        if not all_doubts:
            all_doubts.append("Q-01")

    title_display = f"{filename} ({rule_id})"
    if candidates:
        title_display = f"{candidates[0].rule_name} - {filename}"

    fact = CertificateFacts(
        certificate_id=f"cert-{uuid.uuid4().hex[:8]}",
        rule_id=rule_id,
        activity_title=title_display,
        event_name=filename,
        organiser=None,
        level=level_val,
        position=position_val,
        activity_date=activity_date,
        score_value=score_val,
        verdict=verdict,
        doubt_codes=all_doubts,
        student_asserted=False,
    )

    return fact, all_doubts
