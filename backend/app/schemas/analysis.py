"""Certificate Analysis Schema for Verification Allow-List."""

from pydantic import BaseModel, ConfigDict, Field


class CertificateAnalysis(BaseModel):
    model_config = ConfigDict(frozen=True)

    certificate_id: str
    quality_ok: bool = Field(description="Resolution, blur, skew, page completeness all pass")
    fields_grounded: bool = Field(description="Every extracted quote found verbatim in text layer")
    extractors_agree: bool = Field(
        description="Independent regex and LLM extractors agreed on critical fields"
    )
    name_exact_match: bool = Field(
        description="Recipient name matches student profile or approved alias"
    )
    date_certain: bool = Field(
        description="Date format unambiguous and activity date explicitly evidenced"
    )
    date_in_study_period: bool = Field(
        description="Activity date strictly within admission to completion window"
    )
    exactly_one_rule_candidate: bool = Field(
        description="Precisely one handbook rule applies without ambiguity"
    )
    issuer_accepted: bool = Field(
        description="Issuing authority matches accepted issuers for the rule"
    )
    duration_ok_or_not_required: bool = Field(
        description="Required duration evidenced or not required by rule"
    )
    cosign_ok_or_not_required: bool = Field(
        description="Mandatory co-signatures/recommendations present or not required"
    )
    approved_list_ok_or_not_required: bool = Field(
        description="Course on university approved list or not required"
    )
    no_ambiguity_flag: bool = Field(
        description="Rule interpretation is free of handbook ambiguity flags (S-02)"
    )
    no_open_doubts: bool = Field(description="No open doubt triggers of any family")
