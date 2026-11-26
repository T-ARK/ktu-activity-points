"""Tests for the can_verify explicit allow-list function (agent.md §7.3).

Verifies:
- All 13 predicates must be True to earn VERIFIED status.
- Flipping any single predicate to False immediately results in False (mutation resistance).
- Default verdict is never VERIFIED.
"""

import pytest

from app.doubt.verify import can_verify
from app.schemas.analysis import CertificateAnalysis


@pytest.fixture
def perfect_analysis() -> CertificateAnalysis:
    """Fixture with all 13 allow-list predicates passing."""
    return CertificateAnalysis(
        certificate_id="cert_001",
        quality_ok=True,
        fields_grounded=True,
        extractors_agree=True,
        name_exact_match=True,
        date_certain=True,
        date_in_study_period=True,
        exactly_one_rule_candidate=True,
        issuer_accepted=True,
        duration_ok_or_not_required=True,
        cosign_ok_or_not_required=True,
        approved_list_ok_or_not_required=True,
        no_ambiguity_flag=True,
        no_open_doubts=True,
    )


def test_can_verify_all_pass(perfect_analysis: CertificateAnalysis):
    """When all checks pass, can_verify returns True."""
    assert can_verify(perfect_analysis) is True


@pytest.mark.parametrize(
    "failing_predicate",
    [
        "quality_ok",
        "fields_grounded",
        "extractors_agree",
        "name_exact_match",
        "date_certain",
        "date_in_study_period",
        "exactly_one_rule_candidate",
        "issuer_accepted",
        "duration_ok_or_not_required",
        "cosign_ok_or_not_required",
        "approved_list_ok_or_not_required",
        "no_ambiguity_flag",
        "no_open_doubts",
    ],
)
def test_can_verify_single_predicate_failure(
    perfect_analysis: CertificateAnalysis, failing_predicate: str
):
    """Mutation resistance: if any single check is False, can_verify MUST be False."""
    mutated = perfect_analysis.model_copy(update={failing_predicate: False})
    assert can_verify(mutated) is False, f"can_verify must fail when {failing_predicate}=False"
