"""Phase 6: Multi-Scheme Ruleset Registry & Validator (agent.md §11)."""

import json
from pathlib import Path
from typing import Any, cast

from app.schemas.profile import StudentProfile


class SchemeMismatchError(ValueError):
    """Raised when curriculum scheme does not match ruleset (S-01)."""

    pass


class MultiSchemeRegistry:
    """Loads and caches curriculum rulesets by scheme version."""

    def __init__(self, rulesets_dir: Path | None = None) -> None:
        self.rulesets_dir = rulesets_dir or Path("rulesets")
        self._cache: dict[str, dict[str, Any]] = {}

    def get_ruleset(self, scheme: str) -> dict[str, Any]:
        """Loads and returns ruleset for the requested scheme."""
        normalized_scheme = str(scheme).strip()
        if normalized_scheme in self._cache:
            return self._cache[normalized_scheme]

        filename = f"ktu-{normalized_scheme}-v1.json"
        path = self.rulesets_dir / filename
        if not path.exists():
            # Check default 2024
            path = self.rulesets_dir / "ktu-2024-v1.json"
            if not path.exists():
                raise FileNotFoundError(f"Ruleset file not found for scheme '{scheme}'")

        with open(path) as f:
            data = cast(dict[str, Any], json.load(f))

        ruleset_scheme = str(data.get("curriculum_scheme", "2024"))
        if ruleset_scheme != normalized_scheme:
            raise SchemeMismatchError(
                f"S-01: Incompatible curriculum scheme '{normalized_scheme}'. Ruleset is {ruleset_scheme}."
            )

        self._cache[normalized_scheme] = data
        return data

    def validate_profile_scheme(self, profile: StudentProfile, ruleset: dict[str, Any]) -> None:
        """Validates that student profile matches ruleset scheme."""
        ruleset_scheme = str(ruleset.get("curriculum_scheme", "2024")).strip()
        profile_scheme = str(profile.scheme).strip()
        if profile_scheme != ruleset_scheme:
            raise SchemeMismatchError(
                f"S-01: Profile scheme '{profile_scheme}' does not match ruleset '{ruleset_scheme}'"
            )


scheme_registry = MultiSchemeRegistry()
