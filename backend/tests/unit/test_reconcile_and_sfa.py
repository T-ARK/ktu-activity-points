"""Unit tests for Stages 4, 7, SFA Workspace & Multi-Scheme Registry."""

from datetime import date

from app.extract.reconcile import reconcile_certificate_facts
from app.multischeme.loader import MultiSchemeRegistry, SchemeMismatchError
from app.schemas.facts import CertificateFacts
from app.schemas.profile import EntryType, StudentProfile
from app.schemas.verdict import Level, Verdict
from app.sfa.workspace import AdjudicationAction, SfaWorkspace


def get_sample_profile() -> StudentProfile:
    return StudentProfile(
        student_id="TVE24CS001",
        full_name="Aravind Kumar",
        admission_date=date(2024, 8, 1),
        programme_end_date=date(2028, 7, 31),
        entry_type=EntryType.REGULAR,
        is_pwd=False,
        scheme="2024",
        aliases=["Aravind K"],
    )


def test_reconcile_name_mismatch():
    profile = get_sample_profile()
    # Name matches alias
    analysis1, doubts1 = reconcile_certificate_facts(
        candidate_name="Aravind K",
        activity_date=date(2025, 2, 10),
        rule_id="1.1",
        document_text="Certificate awarded to Aravind K for basketball",
        profile=profile,
        quotes=["Aravind K"],
    )
    assert analysis1.name_exact_match is True
    assert "E-05" not in doubts1

    # Name completely differs
    analysis2, doubts2 = reconcile_certificate_facts(
        candidate_name="Rohan Varma",
        activity_date=date(2025, 2, 10),
        rule_id="1.1",
        document_text="Certificate awarded to Rohan Varma",
        profile=profile,
        quotes=["Rohan Varma"],
    )
    assert analysis2.name_exact_match is False
    assert "E-05" in doubts2


def test_reconcile_study_period_checks():
    profile = get_sample_profile()

    # Prior to admission -> R-01
    _, doubts_prior = reconcile_certificate_facts(
        candidate_name="Aravind Kumar",
        activity_date=date(2023, 5, 1),
        rule_id="1.5",
        document_text="Driving license issued on 2023-05-01",
        profile=profile,
        quotes=["2023-05-01"],
    )
    assert "R-01" in doubts_prior

    # After graduation -> R-02
    _, doubts_post = reconcile_certificate_facts(
        candidate_name="Aravind Kumar",
        activity_date=date(2029, 1, 15),
        rule_id="3.3",
        document_text="Internship completed on 2029-01-15",
        profile=profile,
        quotes=["2029-01-15"],
    )
    assert "R-02" in doubts_post


def test_sfa_workspace_adjudication():
    ws = SfaWorkspace()
    act = CertificateFacts(
        certificate_id="act-test-01",
        rule_id="2.3",
        activity_title="Paper Presentation with ambiguous level",
        level=Level.STATE,
        verdict=Verdict.DOUBT,
        doubt_codes=["C-03"],
        student_asserted=True,
    )

    # 1. SFA Overrides and Verifies
    updated_act, entry = ws.adjudicate_activity(
        activity=act,
        action=AdjudicationAction.OVERRIDE,
        sfa_name="Dr. K. Thomas (Staff Advisor)",
        reason="Verified official brochure confirming state level competition",
        override_rule_id="2.4",
    )

    assert updated_act.verdict == Verdict.VERIFIED
    assert updated_act.rule_id == "2.4"
    assert len(updated_act.doubt_codes) == 0
    assert len(ws.audit_log) == 1
    assert entry.sfa_name == "Dr. K. Thomas (Staff Advisor)"
    assert entry.action == AdjudicationAction.OVERRIDE


def test_multischeme_validation_error():
    registry = MultiSchemeRegistry()
    profile = StudentProfile(
        student_id="TVE20CS001",
        full_name="Old Scheme Student",
        admission_date=date(2020, 8, 1),
        programme_end_date=date(2024, 7, 31),
        entry_type=EntryType.REGULAR,
        is_pwd=False,
        scheme="2019",
    )
    ruleset_2024 = {"curriculum_scheme": "2024", "rules": []}

    try:
        registry.validate_profile_scheme(profile, ruleset_2024)
        raise AssertionError("Should have raised SchemeMismatchError")
    except SchemeMismatchError as e:
        assert "S-01" in str(e)
