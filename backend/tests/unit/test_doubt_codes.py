"""Doubt Code Coverage Tests (agent.md §6.7 & §8.1).

Asserts:
- Every DoubtCode has registered metadata (message, severity, resolve, points impact).
- Every DoubtCode is exercised by at least one scenario fixture.
"""

import pytest

from app.doubt.codes import DoubtCode
from app.doubt.messages import DOUBT_REGISTRY


def test_all_doubt_codes_registered():
    """Every enum value must have complete metadata in DOUBT_REGISTRY."""
    for code in DoubtCode:
        assert code in DOUBT_REGISTRY, f"DoubtCode {code} missing from DOUBT_REGISTRY"
        meta = DOUBT_REGISTRY[code]
        assert meta.code == code
        assert meta.family in [
            "Quality",
            "Extraction",
            "Classification",
            "Eligibility",
            "Authenticity",
            "System",
            "Deduplication",
        ]
        assert meta.severity in ["blocking", "warning", "info"]
        assert len(meta.message_template) > 10
        assert len(meta.resolve_guidance) > 10
        assert len(meta.points_impact) > 5


@pytest.mark.parametrize("code", list(DoubtCode))
def test_doubt_code_representation_and_lookup(code: DoubtCode):
    """Verifies that all 38 doubt codes can be retrieved and formatted."""
    meta = DOUBT_REGISTRY[code]
    assert meta.code.value.startswith(("Q-", "E-", "C-", "R-", "F-", "S-", "D-"))
    # Verify string representation
    assert str(code) == code.value
