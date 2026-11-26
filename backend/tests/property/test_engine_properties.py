"""Hypothesis Property-Based Tests for Deterministic Rules Engine (agent.md §8.1).

Invariants Asserted Across >= 100,000 Random Cases:
1. Confirmed <= Upper bound (Always holds)
2. Caps are never exceeded under any permutation or volume
3. Order independence (shuffling certificates yields identical totals)
4. Rule i: Winner beats participation for the same event
5. Rule i: Highest level achievement wins for the same event
6. Monotonicity: Adding an activity never decreases Upper bound
"""

import json
import os
import random
from datetime import date
from decimal import Decimal
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from app.engine.aggregator import evaluate
from app.schemas.facts import CertificateFacts
from app.schemas.profile import EntryType, StudentProfile
from app.schemas.verdict import Level, Verdict

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RULESET_PATH = REPO_ROOT / "rulesets" / "ktu-2024-v1.json"

with open(RULESET_PATH, encoding="utf-8") as f:
    RULESET_DATA = json.load(f)

ALL_RULE_IDS = [r["id"] for r in RULESET_DATA["rules"]]

# Configure Hypothesis profiles
NUM_EXAMPLES = 100_000 if os.getenv("RUN_100K") == "1" else 1_000
settings.register_profile("thorough", max_examples=100_000, deadline=None)
settings.register_profile("default", max_examples=NUM_EXAMPLES, deadline=None)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))

# Custom Strategies
profile_strategy = st.builds(
    StudentProfile,
    student_id=st.text(min_size=3, max_size=10, alphabet="abcdef0123456789"),
    full_name=st.just("Test Student"),
    programme=st.sampled_from(["B.Tech", "B.Des", "BBA", "BCA"]),
    admission_date=st.just(date(2024, 8, 1)),
    programme_end_date=st.just(date(2028, 6, 30)),
    entry_type=st.sampled_from([EntryType.REGULAR, EntryType.LATERAL]),
    is_pwd=st.booleans(),
    scheme=st.just("2024"),
)

level_strategy = st.sampled_from(
    [Level.COLLEGE, Level.ZONAL, Level.STATE, Level.NATIONAL, Level.INTERNATIONAL, None]
)
verdict_strategy = st.sampled_from(
    [Verdict.VERIFIED, Verdict.DOUBT, Verdict.NOT_ELIGIBLE, Verdict.MANUAL_ONLY]
)
position_strategy = st.sampled_from(
    ["1st Prize", "2nd Prize", "3rd Prize", "First", "Second", "Participation", None]
)

facts_strategy = st.builds(
    CertificateFacts,
    certificate_id=st.uuids().map(str),
    rule_id=st.sampled_from(ALL_RULE_IDS),
    activity_title=st.sampled_from(
        [
            "Sports Meet",
            "Tech Fest",
            "IELTS Academic",
            "TOEFL iBT",
            "Blood Donation",
            "NSS Camp",
            "Paper Presentation",
            "Community Service",
            "FOSS Hackathon",
        ]
    ),
    event_name=st.sampled_from(["KTU Techfest 2025", "Annual Sports Meet", "Robotics Expo", None]),
    organiser=st.sampled_from(["Host College", "KTU", "IIT Madras", None]),
    level=level_strategy,
    position=position_strategy,
    event_type=st.sampled_from(["single", "group", None]),
    activity_date=st.just(date(2025, 3, 15)),
    academic_year=st.sampled_from(["2024-2025", "2025-2026", None]),
    semester=st.sampled_from(["S1", "S2", "S3", "S4", "S5", None]),
    duration_days=st.integers(min_value=1, max_value=30),
    duration_hours=st.integers(min_value=1, max_value=120),
    duration_weeks=st.integers(min_value=1, max_value=16),
    duration_months=st.sampled_from([Decimal("3.5"), Decimal("4.0"), None]),
    score_value=st.sampled_from(
        [
            Decimal("7.5"),
            Decimal("7.0"),
            Decimal("6.5"),
            105,
            95,
            80,
            320,
            310,
            300,
            700,
            Decimal("95.00"),
            None,
        ]
    ),
    verdict=verdict_strategy,
)


@given(
    profile=profile_strategy,
    certs=st.lists(facts_strategy, min_size=0, max_size=20, unique_by=lambda f: f.certificate_id),
)
def test_confirmed_le_upper_bound(profile: StudentProfile, certs: list[CertificateFacts]):
    """Invariant 1: Confirmed <= Upper bound across all groups, events, and total."""
    result = evaluate(profile, certs, RULESET_DATA)

    # Event level
    event_pess: dict[str, int] = {}
    event_opt: dict[str, int] = {}
    for act, raw_cert in zip(result.activities, certs, strict=False):
        from app.engine.dedupe import get_dedupe_family

        family = get_dedupe_family(act.rule_id)
        ename = f"{family}::{raw_cert.event_name or act.certificate_id}"
        event_pess[ename] = event_pess.get(ename, 0) + act.counted_points_pessimistic
        event_opt[ename] = event_opt.get(ename, 0) + act.counted_points_optimistic

    for ename in event_pess:
        assert event_pess[ename] <= event_opt[ename]

    # Group level
    for grp in result.groups.values():
        assert grp.bracket.confirmed <= grp.bracket.upper_bound
        assert grp.bracket.pending == grp.bracket.upper_bound - grp.bracket.confirmed

    # Total level
    assert result.total_bracket.confirmed <= result.total_bracket.upper_bound
    assert (
        result.total_bracket.pending
        == result.total_bracket.upper_bound - result.total_bracket.confirmed
    )


@given(
    profile=profile_strategy,
    certs=st.lists(facts_strategy, min_size=1, max_size=25, unique_by=lambda f: f.certificate_id),
)
def test_caps_never_exceeded(profile: StudentProfile, certs: list[CertificateFacts]):
    """Invariant 2: No subhead, shared, or category cap is ever breached."""
    result = evaluate(profile, certs, RULESET_DATA)

    # Subhead caps
    blood_donation_pts = sum(
        a.counted_points_optimistic for a in result.activities if a.rule_id == "1.8"
    )
    assert blood_donation_pts <= 10

    driving_license_pts = sum(
        a.counted_points_optimistic for a in result.activities if a.rule_id == "1.5"
    )
    assert driving_license_pts <= 5

    english_pts = sum(a.counted_points_optimistic for a in result.activities if a.rule_id == "2.21")
    assert english_pts <= 30

    aptitude_pts = sum(
        a.counted_points_optimistic for a in result.activities if a.rule_id == "2.22"
    )
    assert aptitude_pts <= 30

    # Shared Category Caps
    comm_service_pts = sum(
        a.counted_points_optimistic for a in result.activities if a.rule_id in ["1.6", "1.7"]
    )
    assert comm_service_pts <= 10

    health_safety_pts = sum(
        a.counted_points_optimistic for a in result.activities if a.rule_id in ["1.20", "1.21"]
    )
    assert health_safety_pts <= 10

    tech_events_pts = sum(
        a.counted_points_optimistic
        for a in result.activities
        if a.rule_id in ["2.1", "2.2", "2.3", "2.4"]
    )
    assert tech_events_pts <= 40

    innovation_pts = sum(
        a.counted_points_optimistic
        for a in result.activities
        if a.rule_id in ["3.9", "3.10", "3.11.1", "3.11.2", "3.12", "3.13"]
    )
    assert innovation_pts <= 40


@given(
    profile=profile_strategy,
    certs=st.lists(facts_strategy, min_size=2, max_size=15, unique_by=lambda f: f.certificate_id),
)
def test_order_independence(profile: StudentProfile, certs: list[CertificateFacts]):
    """Invariant 3: Shuffling input certificates yields identical results."""
    shuffled = list(certs)
    random.seed(42)
    random.shuffle(shuffled)

    res1 = evaluate(profile, certs, RULESET_DATA)
    res2 = evaluate(profile, shuffled, RULESET_DATA)

    assert res1.total_bracket.confirmed == res2.total_bracket.confirmed
    assert res1.total_bracket.upper_bound == res2.total_bracket.upper_bound
    assert res1.credit_status == res2.credit_status
    for gid in ["I", "II", "III"]:
        assert res1.groups[gid].bracket.confirmed == res2.groups[gid].bracket.confirmed
        assert res1.groups[gid].bracket.upper_bound == res2.groups[gid].bracket.upper_bound


def test_rule_i_winner_beats_participation():
    """Rule i: For same event, winning certificate suppresses participation."""
    profile = StudentProfile(
        student_id="s1",
        full_name="Alice",
        admission_date=date(2024, 8, 1),
        programme_end_date=date(2028, 6, 30),
    )
    part_cert = CertificateFacts(
        certificate_id="cert_part",
        rule_id="1.1",
        activity_title="State Badminton",
        event_name="KTU Badminton Tournament 2025",
        level=Level.STATE,
        position="Participation",
        verdict=Verdict.VERIFIED,
    )
    winner_cert = CertificateFacts(
        certificate_id="cert_win",
        rule_id="1.2",
        activity_title="State Badminton Winner",
        event_name="KTU Badminton Tournament 2025",
        level=Level.STATE,
        position="1st Prize",
        verdict=Verdict.VERIFIED,
    )
    res = evaluate(profile, [part_cert, winner_cert], RULESET_DATA)
    outcomes = {a.certificate_id: a for a in res.activities}

    # Winner gets 20 points (State level winner in 1.2)
    assert outcomes["cert_win"].counted_points_pessimistic == 20
    # Participation gets 0 points and has D-DUP
    assert outcomes["cert_part"].counted_points_pessimistic == 0
    assert "D-DUP" in outcomes["cert_part"].doubt_codes


def test_rule_i_highest_level_wins():
    """Rule i: For same event, higher level achievement supersedes lower level."""
    profile = StudentProfile(
        student_id="s1",
        full_name="Bob",
        admission_date=date(2024, 8, 1),
        programme_end_date=date(2028, 6, 30),
    )
    college_win = CertificateFacts(
        certificate_id="cert_col",
        rule_id="1.2",
        activity_title="College Level Debate",
        event_name="Annual Debate Competition",
        level=Level.COLLEGE,
        position="1st Prize",
        verdict=Verdict.VERIFIED,
    )
    state_win = CertificateFacts(
        certificate_id="cert_state",
        rule_id="1.2",
        activity_title="State Level Debate",
        event_name="Annual Debate Competition",
        level=Level.STATE,
        position="1st Prize",
        verdict=Verdict.VERIFIED,
    )
    res = evaluate(profile, [college_win, state_win], RULESET_DATA)
    outcomes = {a.certificate_id: a for a in res.activities}

    # State winner (20 pts) wins; college winner (5 pts) is suppressed (0 pts)
    assert outcomes["cert_state"].counted_points_pessimistic == 20
    assert outcomes["cert_col"].counted_points_pessimistic == 0
    assert "D-DUP" in outcomes["cert_col"].doubt_codes


@given(
    profile=profile_strategy,
    certs=st.lists(facts_strategy, min_size=0, max_size=10, unique_by=lambda f: f.certificate_id),
    extra=facts_strategy,
)
def test_monotonicity_adding_certificate(
    profile: StudentProfile, certs: list[CertificateFacts], extra: CertificateFacts
):
    """Monotonicity: Adding an activity never decreases total Upper bound or Confirmed points."""
    # Ensure extra has distinct id not present in certs
    existing_ids = {c.certificate_id for c in certs}
    extra_id = "extra_unique_id_999"
    counter = 1
    while extra_id in existing_ids:
        extra_id = f"extra_unique_id_{counter}"
        counter += 1
    extra_distinct = extra.model_copy(update={"certificate_id": extra_id})
    res_before = evaluate(profile, certs, RULESET_DATA)
    res_after = evaluate(profile, certs + [extra_distinct], RULESET_DATA)

    assert res_after.total_bracket.upper_bound >= res_before.total_bracket.upper_bound
    assert res_after.total_bracket.confirmed >= res_before.total_bracket.confirmed
