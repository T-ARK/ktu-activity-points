"""Normalized Certificate Facts Schema."""

from datetime import date
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.verdict import Level, Verdict


class CertificateFacts(BaseModel):
    model_config = ConfigDict(frozen=True)

    certificate_id: str = Field(description="Unique certificate identifier")
    rule_id: str = Field(description="Candidate handbook rule ID e.g. '1.1', '2.21'")
    activity_title: str = Field(description="Title of activity or certificate description")
    event_name: str | None = Field(default=None, description="Event name for deduplication")
    organiser: str | None = Field(default=None, description="Organising body or institution")
    level: Level | None = Field(default=None, description="Verified or asserted level")
    position: str | None = Field(default=None, description="1st, 2nd, 3rd, participation, etc.")
    event_type: str | None = Field(default=None, description="'single' or 'group'")
    activity_date: date | None = Field(default=None, description="Date activity occurred")
    academic_year: str | None = Field(default=None, description="e.g. '2024-2025'")
    semester: str | None = Field(default=None, description="e.g. 'S1', 'S2', 'S5'")
    duration_days: int | None = Field(default=None, description="Duration in full days")
    duration_hours: int | None = Field(default=None, description="Duration in hours")
    duration_weeks: int | None = Field(default=None, description="Duration in weeks")
    duration_months: Decimal | None = Field(
        default=None, description="Duration in months (Decimal)"
    )
    score_value: Decimal | int | str | None = Field(
        default=None, description="Standardized test score / band (Decimal or int)"
    )
    score_details: dict[str, Any] | None = Field(
        default=None, description="GATE qualified/air details, etc."
    )
    issuer: str | None = Field(default=None, description="Issuing authority name/type")
    role: str | None = Field(default=None, description="Role title for leadership/club rules")
    verdict: Verdict = Field(default=Verdict.DOUBT, description="Verification status")
    doubt_codes: list[str] = Field(
        default_factory=list, description="Associated doubt code strings"
    )
    student_asserted: bool = Field(
        default=False,
        description="True if fact was asserted by student rather than extracted from cert",
    )
