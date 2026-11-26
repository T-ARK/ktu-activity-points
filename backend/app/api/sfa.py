"""Staff Advisor (SFA) Workspace API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.facts import CertificateFacts
from app.schemas.verdict import Verdict
from app.sfa.workspace import AdjudicationAction, SfaAuditEntry, sfa_workspace
from app.storage import store

router = APIRouter(prefix="/api/sfa", tags=["sfa"])


class AdjudicateRequest(BaseModel):
    certificate_id: str
    action: AdjudicationAction
    sfa_name: str
    reason: str
    override_rule_id: str | None = None


@router.get("/queue", response_model=list[CertificateFacts])
def get_sfa_review_queue() -> list[CertificateFacts]:
    """Returns activities routed to DOUBT requiring SFA review."""
    return [a for a in store.activities if a.verdict == Verdict.DOUBT]


@router.post("/adjudicate", response_model=SfaAuditEntry)
def adjudicate_activity(req: AdjudicateRequest) -> SfaAuditEntry:
    """Adjudicates a pending activity (verify, reject, override) with mandatory reason."""
    activity = next((a for a in store.activities if a.certificate_id == req.certificate_id), None)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    updated_activity, audit_entry = sfa_workspace.adjudicate_activity(
        activity=activity,
        action=req.action,
        sfa_name=req.sfa_name,
        reason=req.reason,
        override_rule_id=req.override_rule_id,
    )

    # Replace activity in store with updated version
    store.activities = [
        updated_activity if a.certificate_id == req.certificate_id else a for a in store.activities
    ]
    return audit_entry


@router.get("/audit-log", response_model=list[SfaAuditEntry])
def get_sfa_audit_log() -> list[SfaAuditEntry]:
    """Returns the persistent audit log of SFA adjudications."""
    return sfa_workspace.audit_log
