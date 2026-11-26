"""Activity submission and management API endpoints."""

import uuid
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.facts import CertificateFacts
from app.schemas.verdict import Level, Verdict
from app.storage import store

router = APIRouter(prefix="/api/activities", tags=["activities"])


class ManualActivityRequest(BaseModel):
    rule_id: str
    activity_title: str
    event_name: str | None = None
    organiser: str | None = None
    level: Level | None = None
    position: str | None = None
    event_type: str | None = None
    activity_date: date | None = None
    academic_year: str | None = None
    semester: str | None = None
    duration_days: int | None = None
    duration_hours: int | None = None
    duration_weeks: int | None = None
    duration_months: Decimal | None = None
    score_value: Decimal | int | None = None
    verdict: Verdict = Verdict.DOUBT
    is_verified_by_sfa: bool = False


@router.get("", response_model=list[CertificateFacts])
def list_activities() -> list[CertificateFacts]:
    """Returns all submitted student activities."""
    return store.activities


@router.post("", response_model=CertificateFacts)
def add_activity(req: ManualActivityRequest) -> CertificateFacts:
    """Adds a new activity entry with deterministic validation."""
    rule_found = False
    for r in store.ruleset.get("rules", []):
        if r.get("id") == req.rule_id:
            rule_found = True
            break
    if not rule_found:
        raise HTTPException(status_code=400, detail=f"Invalid rule_id '{req.rule_id}'")

    doubt_codes: list[str] = []
    verdict = req.verdict

    # Check date within study period (Rule vi)
    if req.activity_date:
        if req.activity_date < store.profile.admission_date:
            doubt_codes.append("R-01")
            verdict = Verdict.DOUBT
        elif req.activity_date > store.profile.programme_end_date:
            doubt_codes.append("R-02")
            verdict = Verdict.DOUBT

    if req.is_verified_by_sfa:
        verdict = Verdict.VERIFIED
    elif verdict == Verdict.VERIFIED and not req.is_verified_by_sfa:
        # Self-asserted without SFA check must remain DOUBT (G2 guarantee)
        verdict = Verdict.DOUBT
        doubt_codes.append("Q-01")

    fact = CertificateFacts(
        certificate_id=f"act-{uuid.uuid4().hex[:8]}",
        rule_id=req.rule_id,
        activity_title=req.activity_title,
        event_name=req.event_name,
        organiser=req.organiser,
        level=req.level,
        position=req.position,
        event_type=req.event_type,
        activity_date=req.activity_date,
        academic_year=req.academic_year,
        semester=req.semester,
        duration_days=req.duration_days,
        duration_hours=req.duration_hours,
        duration_weeks=req.duration_weeks,
        duration_months=req.duration_months,
        score_value=req.score_value,
        verdict=verdict,
        doubt_codes=doubt_codes,
        student_asserted=not req.is_verified_by_sfa,
    )
    store.activities.append(fact)
    return fact


@router.delete("/{cert_id}")
def delete_activity(cert_id: str) -> dict[str, str]:
    """Deletes an activity entry by ID."""
    initial_len = len(store.activities)
    store.activities = [a for a in store.activities if a.certificate_id != cert_id]
    if len(store.activities) == initial_len:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"status": "deleted", "certificate_id": cert_id}


@router.post("/load-sample", response_model=list[CertificateFacts])
def load_sample_activities() -> list[CertificateFacts]:
    """Loads a synthetic sample batch of activities spanning Groups I, II, III for evaluation."""
    store.activities.clear()
    samples = [
        # Group I
        CertificateFacts(
            certificate_id="sample-1",
            rule_id="1.1",
            activity_title="KTU Interzone Basketball Tournament",
            event_name="KTU Interzone Basketball 2024",
            organiser="KTU Sports Council",
            level=Level.ZONAL,
            position="Participation",
            activity_date=date(2024, 11, 10),
            academic_year="2024-2025",
            semester="S1",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-2",
            rule_id="1.2",
            activity_title="State Inter-Collegiate Arts Festival (Classical Music)",
            event_name="Kerala State Youth Fest 2025",
            organiser="Kerala Cultural Affairs",
            level=Level.STATE,
            position="1st Prize",
            activity_date=date(2025, 2, 14),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-3",
            rule_id="1.8",
            activity_title="Blood Donation Camp - NSS Unit 142",
            event_name="Voluntary Blood Donation 2025",
            organiser="Government Medical College Blood Bank",
            level=Level.COLLEGE,
            position=None,
            activity_date=date(2025, 1, 20),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-4",
            rule_id="1.22",
            activity_title="College Union Executive Committee Member",
            event_name="College Union 2024-2025",
            organiser="College Election Commission",
            level=Level.COLLEGE,
            position="Executive Committee Members (Excluding Office Bearers)",
            activity_date=date(2024, 9, 15),
            academic_year="2024-2025",
            semester="S1",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        # Group II
        CertificateFacts(
            certificate_id="sample-5",
            rule_id="2.2",
            activity_title="National Tech Fest - Robotics Challenge Winner",
            event_name="Daksha 2025 National Tech Fest",
            organiser="College of Engineering Trivandrum",
            level=Level.NATIONAL,
            position="1st Prize",
            activity_date=date(2025, 3, 5),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-6",
            rule_id="2.21",
            activity_title="IELTS Academic Examination (Score 7.5)",
            event_name="IELTS Academic Test",
            organiser="IDP Education",
            level=Level.INTERNATIONAL,
            score_value=Decimal("7.5"),
            activity_date=date(2025, 1, 15),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-7",
            rule_id="2.3",
            activity_title="Paper Presentation on Edge AI in Healthcare",
            event_name="International Conference on Computing (ICC 2025)",
            organiser="IEEE Kerala Section",
            level=Level.INTERNATIONAL,
            position="Participation",
            activity_date=date(2025, 4, 12),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.DOUBT,
            doubt_codes=["C-01"],
            student_asserted=True,
        ),
        # Group III
        CertificateFacts(
            certificate_id="sample-8",
            rule_id="3.15",
            activity_title="Smart India Hackathon 2024 - 1st Prize",
            event_name="Smart India Hackathon 2024 (MoE)",
            organiser="Ministry of Education Innovation Cell (MIC)",
            level=Level.NATIONAL,
            position="1st Prize",
            activity_date=date(2024, 12, 19),
            academic_year="2024-2025",
            semester="S1",
            verdict=Verdict.VERIFIED,
            doubt_codes=[],
            student_asserted=False,
        ),
        CertificateFacts(
            certificate_id="sample-9",
            rule_id="3.14",
            activity_title="Research Publication in Q1 Journal (Co-author)",
            event_name="IEEE Transactions on Software Engineering",
            organiser="IEEE Computer Society",
            level=Level.INTERNATIONAL,
            position="SCI/SCIE/Scopus Q1–Q2 Journals",
            activity_date=date(2025, 2, 28),
            academic_year="2024-2025",
            semester="S2",
            verdict=Verdict.DOUBT,
            doubt_codes=["E-04"],
            student_asserted=True,
        ),
    ]
    store.activities.extend(samples)
    return store.activities
