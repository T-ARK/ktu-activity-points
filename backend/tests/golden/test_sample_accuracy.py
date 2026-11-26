"""Golden evaluation tests: asserts 100% arithmetic accuracy and 0% VERIFIED errors."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from app.engine.aggregator import evaluate
from app.engine.scoring import calculate_raw_points
from app.schemas.facts import CertificateFacts
from app.schemas.profile import EntryType, StudentProfile
from app.schemas.verdict import Level, Verdict


def load_golden_samples() -> tuple[dict, list[dict]]:
    ruleset_path = Path("rulesets/ktu-2024-v1.json")
    with open(ruleset_path) as f:
        ruleset = json.load(f)

    golden_path = Path("golden/sample_certificates.json")
    with open(golden_path) as f:
        golden_data = json.load(f)

    return ruleset, golden_data["samples"]


def build_fact(d: dict) -> CertificateFacts:
    fd = dict(d["facts"])
    if fd.get("level"):
        fd["level"] = Level(fd["level"])
    if fd.get("verdict"):
        fd["verdict"] = Verdict(fd["verdict"])
    if fd.get("activity_date") and isinstance(fd["activity_date"], str):
        fd["activity_date"] = date.fromisoformat(fd["activity_date"])
    if fd.get("score_value") is not None:
        fd["score_value"] = Decimal(str(fd["score_value"]))
    if fd.get("duration_months") is not None:
        fd["duration_months"] = Decimal(str(fd["duration_months"]))
    return CertificateFacts(**fd)


def test_golden_sample_arithmetic_accuracy():
    """G1 Guarantee: Asserts 100% points arithmetic accuracy across all golden sample certificates."""
    ruleset, samples = load_golden_samples()
    rules_by_id = {r["id"]: r for r in ruleset["rules"]}

    errors = []
    for s in samples:
        fact = build_fact(s)
        expected = s["expected"]
        rule = rules_by_id[fact.rule_id]

        actual_points = calculate_raw_points(fact, rule)
        expected_points = expected["raw_points"]

        if actual_points != expected_points:
            errors.append(
                f"Sample {s['id']} ({fact.rule_id}): expected {expected_points} pts, got {actual_points} pts"
            )

    assert len(errors) == 0, "Arithmetic errors found in golden set:\n" + "\n".join(errors)


def test_golden_sample_verdict_safety():
    """G2 Guarantee: Asserts zero false VERIFIED verdicts on golden samples with doubts or flaws."""
    _, samples = load_golden_samples()

    verified_errors = []
    missed_doubts = []

    for s in samples:
        fact = build_fact(s)
        expected = s["expected"]

        # 1. Zero VERIFIED errors on doubted samples
        if expected["verdict"] == "DOUBT":
            if fact.verdict == Verdict.VERIFIED:
                verified_errors.append(
                    f"Sample {s['id']} marked VERIFIED but expected DOUBT (codes: {expected['doubt_codes']})"
                )
            for dc in expected["doubt_codes"]:
                if dc not in fact.doubt_codes:
                    missed_doubts.append(
                        f"Sample {s['id']} missing expected doubt code '{dc}' (got: {fact.doubt_codes})"
                    )

        # 2. Verified samples must have no doubt codes
        if expected["verdict"] == "VERIFIED":
            if fact.verdict != Verdict.VERIFIED:
                verified_errors.append(
                    f"Sample {s['id']} expected VERIFIED but got {fact.verdict.value}"
                )
            if len(fact.doubt_codes) > 0:
                verified_errors.append(
                    f"Sample {s['id']} marked VERIFIED but has doubt codes: {fact.doubt_codes}"
                )

    assert len(verified_errors) == 0, "VERIFIED errors in golden set:\n" + "\n".join(verified_errors)
    assert len(missed_doubts) == 0, "Missed doubts in golden set:\n" + "\n".join(missed_doubts)


def test_golden_portfolio_aggregation_invariants():
    """Validates that running the complete golden sample portfolio satisfies all engine invariants."""
    ruleset, samples = load_golden_samples()

    profile = StudentProfile(
        student_id="KTU-GOLDEN-001",
        full_name="Golden Test Student",
        admission_date=date(2024, 8, 1),
        programme_end_date=date(2028, 7, 31),
        entry_type=EntryType.REGULAR,
        is_pwd=False,
        scheme="2024",
    )

    facts = [build_fact(s) for s in samples]
    result = evaluate(profile, facts, ruleset)

    # Invariant 1: Confirmed <= Upper bound
    assert result.total_bracket.confirmed <= result.total_bracket.upper_bound
    assert result.total_bracket.pending == (
        result.total_bracket.upper_bound - result.total_bracket.confirmed
    )

    # Invariant 2: Group sums match total
    group_confirmed_sum = sum(g.bracket.confirmed for g in result.groups.values())
    group_upper_sum = sum(g.bracket.upper_bound for g in result.groups.values())
    assert result.total_bracket.confirmed == group_confirmed_sum
    assert result.total_bracket.upper_bound == group_upper_sum

    # Invariant 3: Per-activity bounds
    for a in result.activities:
        assert a.counted_points_pessimistic <= a.counted_points_optimistic
        assert a.counted_points_optimistic <= a.raw_points
        if a.verdict == Verdict.DOUBT.value:
            assert a.counted_points_pessimistic == 0
