"""DoubtCode Enum Register as defined in SPEC §8."""

from enum import StrEnum


class DoubtCode(StrEnum):
    # Quality (Q-)
    Q_01 = "Q-01"  # Low resolution
    Q_02 = "Q-02"  # Blur / skew / glare / cropped edges
    Q_03 = "Q-03"  # OCR confidence below threshold on a critical field
    Q_04 = "Q-04"  # Handwriting on a critical field
    Q_05 = "Q-05"  # Missing pages
    Q_06 = "Q-06"  # Corrupt / password-protected

    # Extraction (E-)
    E_01 = "E-01"  # A critical field is missing from the document
    E_02 = "E-02"  # Extracted quote not found in text layer (possible hallucination)
    E_03 = "E-03"  # Regex extractor and LLM extractor disagree
    E_04 = "E-04"  # Multiple conflicting candidate values
    E_05 = "E-05"  # Recipient name differs from profile
    E_06 = "E-06"  # Date format ambiguous (dd/mm vs mm/dd)
    E_07 = "E-07"  # Critical text in unsupported language

    # Classification & Interpretation (C-)
    C_01 = "C-01"  # More than one rule could apply
    C_02 = "C-02"  # No rule applies (activity not listed in handbook)
    C_03 = "C-03"  # Level not explicitly stated ("inter-college", "regional", "open")
    C_04 = "C-04"  # Position/role ambiguous ("runner-up", "finalist", "top 10")
    C_05 = "C-05"  # Prize type not in handbook table ("special mention", "consolation")
    C_06 = "C-06"  # Individual vs group event cannot be determined (1.2 vs 1.3)
    C_07 = "C-07"  # Institution class unknown (NIRF / IIT / NIT status unconfirmed)

    # Eligibility (R-)
    R_01 = "R-01"  # Activity date outside study period
    R_02 = "R-02"  # No activity date on certificate (issue date ≠ activity date)
    R_03 = "R-03"  # Required duration not stated or not provable
    R_04 = "R-04"  # Issuer is not one of the accepted issuers for that row
    R_05 = "R-05"  # No signature/seal where the row demands an authority
    R_06 = "R-06"  # Required second authority missing (e.g. NSS PO for blood donation)
    R_07 = "R-07"  # Approved-course list not loaded / course not found (3.17)
    R_08 = "R-08"  # Institution-level quota can't be verified
    R_09 = "R-09"  # Test variant doesn't match the handbook (General Training etc.)
    R_10 = "R-10"  # Score validity unknown (e.g. GATE valid-score window)

    # Authenticity (F-)
    F_01 = "F-01"  # No verifiable QR/ID/URL available
    F_02 = "F-02"  # Verification link/ID checked and failed or mismatched
    F_03 = "F-03"  # PDF metadata/visual tamper signals
    F_04 = "F-04"  # Duplicate certificate uploaded

    # Ruleset / System (S-)
    S_01 = "S-01"  # Student's scheme ≠ ruleset (blocking)
    S_02 = "S-02"  # Result depends on handbook ambiguity (A-01 to A-20)
    S_03 = "S-03"  # Engine invariant violation (blocking)

    # Event Deduplication (D-DUP)
    D_DUP = "D-DUP"  # Potential duplicate or superseded event achievement
