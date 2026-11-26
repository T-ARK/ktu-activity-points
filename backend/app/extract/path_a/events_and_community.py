"""Path A: Deterministic Extractors for Events, Community & Technical Activities."""

import re
from datetime import date

from app.schemas.verdict import Level


def extract_level_from_text(text: str) -> tuple[Level | None, str | None]:
    """Extracts explicit activity level per SPEC §7.6."""
    t_lower = text.lower()
    if re.search(r"\binternational\b", t_lower):
        m = re.search(r"\binternational\b", text, re.IGNORECASE)
        return Level.INTERNATIONAL, m.group(0) if m else "international"
    if re.search(r"\b(national|all india|inter-university|inter university)\b", t_lower):
        m = re.search(r"\b(national|all india|inter-university|inter university)\b", text, re.IGNORECASE)
        return Level.NATIONAL, m.group(0) if m else "national"
    if re.search(r"\b(state level|state|kerala state)\b", t_lower):
        m = re.search(r"\b(state level|state|kerala state)\b", text, re.IGNORECASE)
        return Level.STATE, m.group(0) if m else "state"
    if re.search(r"\b(zonal|ktu zone|interzone|inter-zone)\b", t_lower):
        m = re.search(r"\b(zonal|ktu zone|interzone|inter-zone)\b", text, re.IGNORECASE)
        return Level.ZONAL, m.group(0) if m else "zonal"
    if re.search(r"\b(college|intra-college|institution|department)\b", t_lower):
        m = re.search(r"\b(college|intra-college|institution|department)\b", text, re.IGNORECASE)
        return Level.COLLEGE, m.group(0) if m else "college"
    return None, None


def extract_position_from_text(text: str) -> tuple[str, str]:
    """Extracts position/role achieved (1st Prize, 2nd Prize, 3rd Prize, Participation)."""
    t_lower = text.lower()
    if re.search(r"\b(1st prize|first prize|winner|first place|1st place)\b", t_lower):
        m = re.search(r"\b(1st prize|first prize|winner|first place|1st place)\b", text, re.IGNORECASE)
        return "1st Prize", m.group(0) if m else "1st Prize"
    if re.search(r"\b(2nd prize|second prize|runner up|second place|2nd place)\b", t_lower):
        m = re.search(r"\b(2nd prize|second prize|runner up|second place|2nd place)\b", text, re.IGNORECASE)
        return "2nd Prize", m.group(0) if m else "2nd Prize"
    if re.search(r"\b(3rd prize|third prize|third place|3rd place)\b", t_lower):
        m = re.search(r"\b(3rd prize|third prize|third place|3rd place)\b", text, re.IGNORECASE)
        return "3rd Prize", m.group(0) if m else "3rd Prize"
    if re.search(r"\b(participated|participation|attended|participant)\b", t_lower):
        m = re.search(r"\b(participated|participation|attended|participant)\b", text, re.IGNORECASE)
        return "Participation", m.group(0) if m else "Participation"
    return "Participation", "Participation"


def extract_dates_from_text(text: str) -> list[tuple[date, str]]:
    """Extracts ISO and formatted dates from document text."""
    found: list[tuple[date, str]] = []

    # Format 1: YYYY-MM-DD
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            found.append((d, m.group(0)))
        except ValueError:
            pass

    # Format 2: DD-MM-YYYY or DD/MM/YYYY
    for m in re.finditer(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", text):
        try:
            day = int(m.group(1))
            month = int(m.group(2))
            year = int(m.group(3))
            d = date(year, month, day)
            found.append((d, m.group(0)))
        except ValueError:
            pass

    # Format 3: Month DD, YYYY
    months = {
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }
    month_regex = r"\b(" + "|".join(months.keys()) + r")\s+(\d{1,2}),?\s+(\d{4})\b"
    for m in re.finditer(month_regex, text, re.IGNORECASE):
        try:
            m_name = m.group(1).lower()
            month_num = months[m_name]
            day_num = int(m.group(2))
            year_num = int(m.group(3))
            d = date(year_num, month_num, day_num)
            found.append((d, m.group(0)))
        except (KeyError, ValueError):
            pass

    return found


def extract_recipient_name(text: str) -> tuple[str | None, str | None]:
    """Extracts recipient name using standard certificate phrases."""
    patterns = [
        r"(?:certified that|awarded to|presented to|certify that)\s+([A-Z][a-zA-Z\s\.\-]{3,40}?)(?:,|\s+has|\s+of|\s+for|\s+bearing|\s+bearing)",
        r"(?:name of candidate|candidate name|student name)[:\s]+([A-Z][a-zA-Z\s\.\-]{3,40})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            # Clean trailing words like 'has' or punctuation
            candidate = re.sub(r"\s+(?:has|of|for|bearing|from)$", "", candidate, flags=re.IGNORECASE)
            return candidate, m.group(0)
    return None, None
