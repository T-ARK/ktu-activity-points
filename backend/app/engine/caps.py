"""Cap Enforcement Engine in strict fixed order of SPEC §7.9.

Fixed Order:
1. Per-item scoring
2. Event de-duplication
3. Per-year / per-semester limits
4. Sub-head caps
5. Shared / Category caps
6. Group totals
"""

from typing import Any

from app.schemas.facts import CertificateFacts
from app.schemas.verdict import Verdict


def apply_period_limits(
    items: list[tuple[CertificateFacts, int]], rules_by_id: dict[str, Any]
) -> list[tuple[CertificateFacts, int]]:
    """Applies annual/semester limits (e.g. max 5 points per magazine per academic year)."""
    # Key: (rule_id, period_key) -> total points accumulated in period
    period_usage: dict[tuple[str, str], int] = {}
    adjusted: list[tuple[CertificateFacts, int]] = []

    # Sort items deterministically: VERIFIED items first, then higher points, then cert_id
    indexed_items = list(enumerate(items))
    sorted_items = sorted(
        indexed_items,
        key=lambda x: (x[1][0].verdict == Verdict.VERIFIED, x[1][1], x[1][0].certificate_id),
        reverse=True,
    )

    allocated: dict[int, int] = {}

    for orig_idx, (fact, pts) in sorted_items:
        rules_by_id.get(fact.rule_id, {})
        rule_id = fact.rule_id

        # Rules with per-academic-year limits
        if rule_id in ["1.4", "1.23", "1.24", "2.12", "2.13", "2.16"]:
            ay = fact.academic_year or "default_year"
            period_key = (rule_id, ay)
            current = period_usage.get(period_key, 0)
            max_per_ay = 5  # 5 points per academic year for these roles/magazine
            allowed = max(0, max_per_ay - current)
            give = min(pts, allowed)
            period_usage[period_key] = current + give
            allocated[orig_idx] = give

        # Rules with per-semester limits
        elif rule_id == "1.9":
            sem = fact.semester or "default_sem"
            period_key = (rule_id, sem)
            current = period_usage.get(period_key, 0)
            max_per_sem = 10  # 10 points per semester
            allowed = max(0, max_per_sem - current)
            give = min(pts, allowed)
            period_usage[period_key] = current + give
            allocated[orig_idx] = give

        else:
            allocated[orig_idx] = pts

    for idx, (fact, _) in enumerate(items):
        adjusted.append((fact, allocated[idx]))

    return adjusted


def apply_subhead_caps(
    items: list[tuple[CertificateFacts, int]], rules_by_id: dict[str, Any]
) -> list[tuple[CertificateFacts, int]]:
    """Applies sub-head level caps (e.g. 1.8 Blood Donation cap 10)."""
    subhead_usage: dict[str, int] = {}
    indexed_items = list(enumerate(items))
    # Stable sort: VERIFIED items first, then higher points, then cert_id
    sorted_items = sorted(
        indexed_items,
        key=lambda x: (x[1][0].verdict == Verdict.VERIFIED, x[1][1], x[1][0].certificate_id),
        reverse=True,
    )

    allocated: dict[int, int] = {}

    for orig_idx, (fact, pts) in sorted_items:
        rule = rules_by_id.get(fact.rule_id, {})
        cap = rule.get("cap_subhead")
        if cap is not None:
            rule_id = fact.rule_id
            current = subhead_usage.get(rule_id, 0)
            allowed = max(0, cap - current)
            give = min(pts, allowed)
            subhead_usage[rule_id] = current + give
            allocated[orig_idx] = give
        else:
            allocated[orig_idx] = pts

    return [(fact, allocated[idx]) for idx, (fact, _) in enumerate(items)]


def apply_shared_and_category_caps(
    items: list[tuple[CertificateFacts, int]],
    rules_by_id: dict[str, Any],
    reading_mode: str = "standard",
) -> tuple[list[tuple[CertificateFacts, int]], list[str]]:
    """Applies shared multi-rule caps and category caps.

    Supports reading_mode:
      - 'standard': standard conservative handling (SPEC §9)
      - 'a04_shared': Row 2.6 sharing 15 pt cap with 2.5
      - 'a04_presentations': Row 2.6 sharing 40 pt cap with 2.7–2.10
    """
    shared_usage: dict[str, int] = {}
    ambiguity_flags: list[str] = []

    indexed_items = list(enumerate(items))
    sorted_items = sorted(
        indexed_items,
        key=lambda x: (x[1][0].verdict == Verdict.VERIFIED, x[1][1], x[1][0].certificate_id),
        reverse=True,
    )

    allocated: dict[int, int] = {}

    for orig_idx, (fact, pts) in sorted_items:
        rule = rules_by_id.get(fact.rule_id, {})
        shared_cap_id = rule.get("shared_cap_id")
        shared_cap_max = rule.get("shared_cap_max")

        # Handle A-04 cap variations for 2.6
        if fact.rule_id == "2.6":
            if reading_mode == "a04_shared":
                shared_cap_id = "shared_conf_poster_2_5_2_6"
                shared_cap_max = 15
            else:
                shared_cap_id = "shared_presentations_2_6_2_10"
                shared_cap_max = 40

        if shared_cap_id and shared_cap_max is not None:
            current = shared_usage.get(shared_cap_id, 0)
            allowed = max(0, shared_cap_max - current)
            give = min(pts, allowed)
            if pts > allowed:
                # Cap bound!
                if "A-05" in rule.get("ambiguity_refs", []):
                    ambiguity_flags.append("A-05")
                if "A-08" in rule.get("ambiguity_refs", []):
                    ambiguity_flags.append("A-08")
                if "A-13" in rule.get("ambiguity_refs", []):
                    ambiguity_flags.append("A-13")
            shared_usage[shared_cap_id] = current + give
            allocated[orig_idx] = give
        else:
            allocated[orig_idx] = pts

    return [(fact, allocated[idx]) for idx, (fact, _) in enumerate(items)], list(
        set(ambiguity_flags)
    )
