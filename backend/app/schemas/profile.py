"""Student Profile Pydantic Schemas."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class EntryType(StrEnum):
    REGULAR = "regular"
    LATERAL = "lateral"


class StudentProfile(BaseModel):
    model_config = ConfigDict(frozen=True)

    student_id: str = Field(description="Unique identifier for student")
    full_name: str = Field(description="Full name as printed on certificates")
    programme: str = Field(default="B.Tech", description="B.Tech, B.Des, BBA, BCA")
    admission_date: date = Field(description="Date of admission into programme")
    programme_end_date: date = Field(description="Expected or actual programme completion date")
    entry_type: EntryType = Field(default=EntryType.REGULAR, description="Regular or Lateral entry")
    is_pwd: bool = Field(default=False, description="Person with Disabilities status")
    scheme: str = Field(default="2024", description="Curriculum scheme, must be 2024")
    aliases: list[str] = Field(default_factory=list, description="Verified student name variations")
