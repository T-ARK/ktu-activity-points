"""Path A: Deterministic Extractors for Language & Aptitude Proficiency (2.21 & 2.22)."""

import re
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class ExtractedField(BaseModel):
    value: Any
    quote: str
    confidence: float = 1.0


def extract_language_test(text: str) -> dict[str, ExtractedField] | None:
    """Extracts test scores from IELTS, TOEFL iBT, PTE, or Cambridge BEC certificates."""
    t_lower = text.lower()

    # 1. IELTS Academic
    if "ielts" in t_lower or "international english language testing system" in t_lower:
        variant = "Academic" if "academic" in t_lower else "General"
        # Match overall band score e.g. "Overall Band Score 7.5" or "Band Score: 7.0"
        m = re.search(r"(?:overall\s+band\s+score|band\s+score|overall\s+score)[:\s]+(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if m:
            val_str = m.group(1)
            return {
                "test_name": ExtractedField(value="IELTS Academic", quote=m.group(0)),
                "variant": ExtractedField(value=variant, quote=variant),
                "score": ExtractedField(value=Decimal(val_str), quote=m.group(0)),
            }

    # 2. TOEFL iBT
    if "toefl" in t_lower:
        m = re.search(r"(?:total\s+score|score)[:\s]+(\d{2,3})", text, re.IGNORECASE)
        if m:
            val_int = int(m.group(1))
            return {
                "test_name": ExtractedField(value="TOEFL iBT", quote=m.group(0)),
                "score": ExtractedField(value=Decimal(str(val_int)), quote=m.group(0)),
            }

    # 3. PTE Academic
    if "pte" in t_lower or "pearson" in t_lower:
        m = re.search(r"(?:overall\s+score|score)[:\s]+(\d{2,3})", text, re.IGNORECASE)
        if m:
            return {
                "test_name": ExtractedField(value="PTE Academic", quote=m.group(0)),
                "score": ExtractedField(value=Decimal(m.group(1)), quote=m.group(0)),
            }

    return None


def extract_aptitude_test(text: str) -> dict[str, ExtractedField] | None:
    """Extracts GATE, CAT, GRE, or GMAT scorecards."""
    t_lower = text.lower()

    # 1. GATE
    if "gate" in t_lower or "graduate aptitude test" in t_lower:
        # Check AIR
        m_air = re.search(r"(?:all\s+india\s+rank|air)[:\s]+(\d+)", text, re.IGNORECASE)
        air_val = int(m_air.group(1)) if m_air else None
        quote_str = m_air.group(0) if m_air else "GATE"
        qualified = "qualified" in t_lower or air_val is not None
        return {
            "test_name": ExtractedField(value="GATE", quote=quote_str),
            "air": ExtractedField(value=air_val, quote=quote_str) if air_val else None,  # type: ignore[dict-item]
            "qualified": ExtractedField(value=qualified, quote="qualified" if qualified else "gate"),
            "score": ExtractedField(value=Decimal(str(air_val)) if air_val else Decimal("0"), quote=quote_str),
        }

    # 2. CAT
    if "common admission test" in t_lower or "cat 20" in t_lower:
        m_cat = re.search(r"(?:percentile|overall\s+percentile)[:\s]+(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if m_cat:
            return {
                "test_name": ExtractedField(value="CAT", quote=m_cat.group(0)),
                "score": ExtractedField(value=Decimal(m_cat.group(1)), quote=m_cat.group(0)),
            }

    # 3. GRE
    if "gre" in t_lower or "graduate record examination" in t_lower:
        m_gre = re.search(r"(?:total\s+score|score)[:\s]+(\d{3})", text, re.IGNORECASE)
        if m_gre:
            return {
                "test_name": ExtractedField(value="GRE", quote=m_gre.group(0)),
                "score": ExtractedField(value=Decimal(m_gre.group(1)), quote=m_gre.group(0)),
            }

    return None
