"""Engine Output and Totals Schema."""

from pydantic import BaseModel, ConfigDict, Field


class PointBracket(BaseModel):
    """The mandatory three-number bracket shown everywhere (agent.md §3 rule 4)."""

    model_config = ConfigDict(frozen=True)

    confirmed: int = Field(ge=0, description="Safe lower bound from VERIFIED activities only")
    pending: int = Field(ge=0, description="Upper bound minus Confirmed")
    upper_bound: int = Field(ge=0, description="Maximum possible outcome with DOUBT items")


class ActivityOutcome(BaseModel):
    model_config = ConfigDict(frozen=True)

    certificate_id: str
    rule_id: str
    group: str
    activity_title: str | None = None
    raw_points: int = Field(ge=0)
    counted_points_pessimistic: int = Field(ge=0)
    counted_points_optimistic: int = Field(ge=0)
    verdict: str
    doubt_codes: list[str]
    notes: list[str] = Field(default_factory=list)


class GroupResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    group_id: str = Field(description="'I', 'II', or 'III'")
    required_points: int = Field(description="40 for Regular, 30 for Lateral, 20 for PwD")
    bracket: PointBracket
    is_credit_achieved_confirmed: bool
    is_credit_achievable_upper: bool
    activities: list[ActivityOutcome]


class EngineResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    total_bracket: PointBracket
    required_total: int = Field(description="120 for Regular, 90 for Lateral, 60 for PwD")
    groups: dict[str, GroupResult]
    credit_status: str = Field(description="ACHIEVED, ACHIEVABLE_WITH_PENDING, or DEFICIT")
    credits_earned_confirmed: int = Field(ge=0, le=3)
    credits_earned_upper: int = Field(ge=0, le=3)
    activities: list[ActivityOutcome]
    ambiguity_flags: list[str] = Field(default_factory=list)
