"""Verdict and Level Enums."""

from enum import StrEnum


class Verdict(StrEnum):
    VERIFIED = "VERIFIED"
    DOUBT = "DOUBT"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    MANUAL_ONLY = "MANUAL_ONLY"


class Level(StrEnum):
    COLLEGE = "college"
    ZONAL = "zonal"
    STATE = "state"
    NATIONAL = "national"
    INTERNATIONAL = "international"

    @property
    def rank(self) -> int:
        ranks = {
            Level.COLLEGE: 1,
            Level.ZONAL: 2,
            Level.STATE: 3,
            Level.NATIONAL: 4,
            Level.INTERNATIONAL: 5,
        }
        return ranks[self]
