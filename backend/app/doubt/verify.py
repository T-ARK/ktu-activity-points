"""Explicit allow-list for VERIFIED status (agent.md §7.3)."""

from app.schemas.analysis import CertificateAnalysis


def check_quality(r: CertificateAnalysis) -> bool:
    return bool(r.quality_ok)


def check_grounding(r: CertificateAnalysis) -> bool:
    return bool(r.fields_grounded)


def check_extractor_agreement(r: CertificateAnalysis) -> bool:
    return bool(r.extractors_agree)


def check_name_match(r: CertificateAnalysis) -> bool:
    return bool(r.name_exact_match)


def check_date_certainty(r: CertificateAnalysis) -> bool:
    return bool(r.date_certain)


def check_study_period(r: CertificateAnalysis) -> bool:
    return bool(r.date_in_study_period)


def check_rule_candidate_uniqueness(r: CertificateAnalysis) -> bool:
    return bool(r.exactly_one_rule_candidate)


def check_issuer_accepted(r: CertificateAnalysis) -> bool:
    return bool(r.issuer_accepted)


def check_duration(r: CertificateAnalysis) -> bool:
    return bool(r.duration_ok_or_not_required)


def check_cosign(r: CertificateAnalysis) -> bool:
    return bool(r.cosign_ok_or_not_required)


def check_approved_list(r: CertificateAnalysis) -> bool:
    return bool(r.approved_list_ok_or_not_required)


def check_no_ambiguity(r: CertificateAnalysis) -> bool:
    return bool(r.no_ambiguity_flag)


def check_no_open_doubts(r: CertificateAnalysis) -> bool:
    return bool(r.no_open_doubts)


def can_verify(r: CertificateAnalysis) -> bool:
    """Explicit allow-list function for awarding VERIFIED status.

    VERIFIED is NEVER reachable through a default or fallthrough branch.
    Every single predicate must evaluate to True.
    """
    return all(
        [
            check_quality(r),
            check_grounding(r),
            check_extractor_agreement(r),
            check_name_match(r),
            check_date_certainty(r),
            check_study_period(r),
            check_rule_candidate_uniqueness(r),
            check_issuer_accepted(r),
            check_duration(r),
            check_cosign(r),
            check_approved_list(r),
            check_no_ambiguity(r),
            check_no_open_doubts(r),
        ]
    )
