"""Phase 5: Staff Advisor (SFA) Workspace & Adjudication Queue (agent.md §11)."""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.facts import CertificateFacts
from app.schemas.verdict import Verdict


class AdjudicationAction(StrEnum):
    VERIFY = "verify"
    REJECT = "reject"
    OVERRIDE = "override"


class SfaAuditEntry(BaseModel):
    audit_id: str
    certificate_id: str
    action: AdjudicationAction
    previous_verdict: str
    new_verdict: str
    sfa_name: str
    reason: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class SfaWorkspace:
    """Manages the SFA review queue and adjudication audit log."""

    def __init__(self) -> None:
        self.audit_log: list[SfaAuditEntry] = []

    def adjudicate_activity(
        self,
        activity: CertificateFacts,
        action: AdjudicationAction,
        sfa_name: str,
        reason: str,
        override_rule_id: str | None = None,
    ) -> tuple[CertificateFacts, SfaAuditEntry]:
        prev_verdict = activity.verdict.value
        updates: dict[str, Any] = {}

        if action == AdjudicationAction.VERIFY:
            updates = {
                "verdict": Verdict.VERIFIED,
                "doubt_codes": [],
                "student_asserted": False,
            }
        elif action == AdjudicationAction.REJECT:
            updates = {
                "verdict": Verdict.NOT_ELIGIBLE,
                "student_asserted": False,
            }
        elif action == AdjudicationAction.OVERRIDE:
            updates = {
                "verdict": Verdict.VERIFIED,
                "doubt_codes": [],
                "student_asserted": False,
            }
            if override_rule_id:
                updates["rule_id"] = override_rule_id

        updated_activity = activity.model_copy(update=updates)
        entry = SfaAuditEntry(
            audit_id=f"audit-{len(self.audit_log) + 1}",
            certificate_id=activity.certificate_id,
            action=action,
            previous_verdict=prev_verdict,
            new_verdict=updated_activity.verdict.value,
            sfa_name=sfa_name,
            reason=reason,
        )
        self.audit_log.append(entry)
        return updated_activity, entry


sfa_workspace = SfaWorkspace()
