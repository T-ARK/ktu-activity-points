"""Pure deterministic rule scoring functions.

Zero probabilistic or AI logic. Exhaustively covered by boundary tests.
Uses Decimal/int for all score representations (agent.md §3 rule 6).
"""

from decimal import Decimal
from typing import Any

from app.schemas.facts import CertificateFacts


def score_leveled(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for 'leveled' rules (1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4)."""
    if not fact.level:
        return 0

    points_map = rule.get("points", {})
    level_key = fact.level.value  # "college", "zonal", "state", "national", "international"
    return int(points_map.get(level_key, 0))


def score_flat(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for 'flat' rules."""
    points = rule.get("points")
    if isinstance(points, int):
        return points
    return 0


def score_per_unit(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for 'per_unit' rules."""
    points_obj = rule.get("points", {})
    if not isinstance(points_obj, dict):
        return 0

    points_each = points_obj.get("points_each", 0)
    rule_id = rule.get("id")

    # Special case: 3.17 Skilling (1 point per hour of approved course)
    if rule_id == "3.17":
        hours = fact.duration_hours or 0
        return int(max(0, hours * int(points_each)))

    # Standard per-event / per-semester / per-year unit
    return int(points_each)


def score_tiered_score(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for tiered score rules (2.21 English, 2.22 Aptitude).

    Tier semantics: lower bounds are inclusive (>=).
    Scores below lowest tier receive 0 points (agent.md §6.3).
    """
    rule_id = rule.get("id")
    if not fact.score_value and not fact.score_details:
        return 0

    if rule_id == "2.21":
        # Check tests in 2.21
        test_title = fact.activity_title.upper()
        if "IELTS" in test_title:
            try:
                band = Decimal(str(fact.score_value))
            except Exception:
                return 0
            if band >= Decimal("7.5"):
                return 30
            if band >= Decimal("7.0"):
                return 25
            if band >= Decimal("6.5"):
                return 20
            return 0

        elif "TOEFL" in test_title:
            try:
                score = int(fact.score_value)  # type: ignore[arg-type]
            except Exception:
                return 0
            if score >= 105:
                return 30
            if score >= 95:
                return 25
            if score >= 80:
                return 20
            return 0

        elif "PTE" in test_title:
            try:
                score = int(fact.score_value)  # type: ignore[arg-type]
            except Exception:
                return 0
            if score >= 76:
                return 30
            if score >= 65:
                return 25
            if score >= 58:
                return 20
            return 0

        elif "BEC" in test_title or "CAMBRIDGE" in test_title:
            val_str = str(fact.score_value or fact.role or "")
            if "HIGHER" in val_str.upper() or "C1" in val_str.upper():
                return 25
            if "VANTAGE" in val_str.upper() or "B2" in val_str.upper():
                return 20
            if "PRELIMINARY" in val_str.upper() or "B1" in val_str.upper():
                return 15
            return 0

    elif rule_id == "2.22":
        test_title = fact.activity_title.upper()
        if "GRE" in test_title:
            try:
                score = int(fact.score_value)  # type: ignore[arg-type]
            except Exception:
                return 0
            if score >= 320:
                return 30
            if score >= 310:
                return 25
            if score >= 300:
                return 20
            return 0

        elif "GATE" in test_title:
            details = fact.score_details or {}
            qualified = bool(details.get("qualified", False))
            air = details.get("air")
            if air is None and fact.score_value is not None:
                air = fact.score_value
            if not qualified and air is None:
                return 0
            if air is not None:
                try:
                    air_int = int(air)
                    if air_int <= 5000:
                        return 30
                    if air_int <= 15000:
                        return 25
                except Exception:
                    pass
            return 20 if qualified else 0

        elif "CAT" in test_title:
            try:
                percentile = Decimal(str(fact.score_value))
            except Exception:
                return 0
            if percentile >= Decimal("95.00"):
                return 30
            if percentile >= Decimal("90.00"):
                return 25
            if percentile >= Decimal("85.00"):
                return 20
            return 0

        elif "GMAT" in test_title:
            try:
                score = int(fact.score_value)  # type: ignore[arg-type]
            except Exception:
                return 0
            if score >= 700:
                return 30
            if score >= 650:
                return 25
            if score >= 600:
                return 20
            return 0

    return 0


def score_role_based(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for 'role_based' rules by matching position/role title."""
    roles = rule.get("points", [])
    if not isinstance(roles, list):
        return 0

    target = (fact.role or fact.position or fact.activity_title or "").strip().lower()
    if not target:
        return 0

    # 1. Exact match first
    for r in roles:
        title = r.get("title", "").strip().lower()
        if target == title:
            return int(r.get("points", 0))

    # 2. Prefer most specific matching title (longest title length)
    matches: list[tuple[int, int]] = []
    for r in roles:
        title = r.get("title", "").strip().lower()
        pts = int(r.get("points", 0))
        if target in title or title in target:
            matches.append((len(title), pts))

    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0][1]

    return 0


def score_milestone_based(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Calculates points for 'milestone_based' rules (patents, YIP, STRIDE)."""
    milestones = rule.get("points", [])
    if not isinstance(milestones, list):
        return 0

    target = (fact.position or fact.role or fact.activity_title or "").strip().lower()
    if not target:
        return 0

    # 1. Exact match first
    for m in milestones:
        title = m.get("title", "").strip().lower()
        if target == title:
            return int(m.get("points", 0))

    # 2. Prefer most specific matching title (longest title length)
    matches: list[tuple[int, int]] = []
    for m in milestones:
        title = m.get("title", "").strip().lower()
        pts = int(m.get("points", 0))
        if target in title or title in target:
            matches.append((len(title), pts))

    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0][1]

    return 0


def calculate_raw_points(fact: CertificateFacts, rule: dict[str, Any]) -> int:
    """Dispatches raw points computation based on rule kind."""
    kind = rule.get("kind", "")
    if kind == "leveled":
        return score_leveled(fact, rule)
    elif kind == "flat":
        return score_flat(fact, rule)
    elif kind == "per_unit":
        return score_per_unit(fact, rule)
    elif kind == "tiered_score":
        return score_tiered_score(fact, rule)
    elif kind == "role_based":
        return score_role_based(fact, rule)
    elif kind == "milestone_based":
        return score_milestone_based(fact, rule)
    elif kind == "manual":
        # Manual rules (3.1, 3.2) award 0 in automated engine unless certified
        return 0
    return 0
