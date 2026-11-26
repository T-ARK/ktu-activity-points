"""Dashboard evaluation API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.doubt.messages import DOUBT_REGISTRY
from app.engine.aggregator import evaluate
from app.schemas.result import EngineResult
from app.storage import store

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class DoubtDetail(BaseModel):
    code: str
    category: str
    severity: str
    message: str
    how_to_resolve: str
    points_impact: str


class DashboardResponse(BaseModel):
    engine_result: EngineResult
    doubt_catalog: dict[str, DoubtDetail]
    disclaimer: str


@router.get("", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    """Evaluates the student's activities deterministically and returns full points brackets and credit status."""
    engine_res = evaluate(store.profile, store.activities, store.ruleset)

    # Collect details for all active doubt codes in the activities
    active_codes: set[str] = set()
    for act in engine_res.activities:
        active_codes.update(act.doubt_codes)

    catalog: dict[str, DoubtDetail] = {}
    doubt_by_str = {dm.code.value: dm for dm in DOUBT_REGISTRY.values()}
    for code in active_codes:
        if code in doubt_by_str:
            reg = doubt_by_str[code]
            catalog[code] = DoubtDetail(
                code=reg.code.value,
                category=reg.family,
                severity=reg.severity,
                message=reg.message_template,
                how_to_resolve=reg.resolve_guidance,
                points_impact=reg.points_impact,
            )
        else:
            catalog[code] = DoubtDetail(
                code=code,
                category="General",
                severity="warning",
                message=f"Flagged with condition {code}",
                how_to_resolve="Consult with your Staff Advisor (SFA).",
                points_impact="Treated as 0 points in pessimistic run.",
            )

    disclaimer = (
        "KTU Activity Points Checker is an independent student aid and is NOT an official "
        "portal of APJ Abdul Kalam Technological University. Points and credit eligibility "
        "shown are advisory estimates. The official Activity Points File endorsed by your "
        "Staff Advisor (SFA) and Head of Department is the final authority."
    )

    return DashboardResponse(
        engine_result=engine_res,
        doubt_catalog=catalog,
        disclaimer=disclaimer,
    )
