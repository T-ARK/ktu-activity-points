"""Stage 7: Authenticity & Provenance Verifiers (SPEC §7.1 & agent.md §6.5)."""

import re

from pydantic import BaseModel


class AuthenticityResult(BaseModel):
    verification_url: str | None = None
    has_digital_signature: bool = False
    is_duplicate: bool = False
    soft_tamper_flag: bool = False
    flags: list[str] = []


def inspect_authenticity(content: bytes, text: str, existing_hashes: set[str] | None = None, file_hash: str = "") -> AuthenticityResult:
    """Performs read-only authenticity inspection on document bytes and text."""
    flags: list[str] = []

    # 1. Verification URL extraction (QR / text patterns)
    url_match = re.search(r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)", text)
    verification_url = url_match.group(0) if url_match else None

    # 2. Check for PDF digital signatures (ByteByte check for /ByteRange and /Sig)
    has_sig = b"/ByteRange" in content and b"/Type /Sig" in content

    # 3. Duplicate check (F-04)
    is_dup = False
    if existing_hashes and file_hash and file_hash in existing_hashes:
        is_dup = True
        flags.append("F-04")

    # 4. Soft tamper detection (multiple conflicting revision timestamps or font alterations)
    tamper_flag = False
    if content.count(b"%%EOF") > 3:  # Excessive incremental PDF updates
        tamper_flag = True
        flags.append("F-01")

    return AuthenticityResult(
        verification_url=verification_url,
        has_digital_signature=has_sig,
        is_duplicate=is_dup,
        soft_tamper_flag=tamper_flag,
        flags=flags,
    )
