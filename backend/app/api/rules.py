"""Rules exploration API endpoints."""

from typing import Any, cast

from fastapi import APIRouter, HTTPException

from app.storage import store

router = APIRouter(prefix="/api/rules", tags=["rules"])


@router.get("")
def list_rules() -> dict[str, Any]:
    """Returns the full transcribed KTU 2024 activity points ruleset."""
    return store.ruleset


@router.get("/{rule_id}")
def get_rule(rule_id: str) -> dict[str, Any]:
    """Returns details for a specific handbook rule row."""
    for rule in store.ruleset.get("rules", []):
        if rule.get("id") == rule_id:
            return cast(dict[str, Any], rule)
    raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found")
