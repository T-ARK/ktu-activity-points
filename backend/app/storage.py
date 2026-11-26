"""In-memory data store for the Activity Points Checker (Phase 1 MVP).

Stores the active student profile and list of submitted activity certificates.
"""

import json
from datetime import date
from pathlib import Path
from typing import Any

from app.schemas.facts import CertificateFacts
from app.schemas.profile import EntryType, StudentProfile

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RULESET_PATH = REPO_ROOT / "rulesets" / "ktu-2024-v1.json"


class DataStore:
    def __init__(self) -> None:
        self.profile: StudentProfile = StudentProfile(
            student_id="KTU2024STU01",
            full_name="Synthetic Sample Student",
            programme="B.Tech Computer Science & Engineering",
            admission_date=date(2024, 8, 1),
            programme_end_date=date(2028, 6, 30),
            entry_type=EntryType.REGULAR,
            is_pwd=False,
            scheme="2024",
            aliases=[],
        )
        self.activities: list[CertificateFacts] = []
        self._ruleset: dict[str, Any] | None = None

    @property
    def ruleset(self) -> dict[str, Any]:
        if self._ruleset is None:
            with open(RULESET_PATH, encoding="utf-8") as f:
                self._ruleset = json.load(f)
        return self._ruleset

    def reset_to_defaults(self) -> None:
        self.profile = StudentProfile(
            student_id="KTU2024STU01",
            full_name="Synthetic Sample Student",
            programme="B.Tech Computer Science & Engineering",
            admission_date=date(2024, 8, 1),
            programme_end_date=date(2028, 6, 30),
            entry_type=EntryType.REGULAR,
            is_pwd=False,
            scheme="2024",
            aliases=[],
        )
        self.activities.clear()


store = DataStore()
