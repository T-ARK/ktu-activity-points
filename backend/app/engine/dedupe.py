"""Event Deduplication Engine implementing Handbook Rule i.

Rule i:
"Participation points and winning points cannot be combined for the same event.
If a student wins a position, only the points for winning will be awarded.
The highest level of achievement attained will be considered."

Guarantees:
- Confirmed points from a VERIFIED certificate can never be reduced by a DOUBT certificate.
- Shuffling certificates produces identical deduplication results.
- For every certificate: pessimistic_points <= optimistic_points.
"""

import re
from typing import Any, NamedTuple

from app.schemas.facts import CertificateFacts


def normalize_event_name(name: str | None) -> str:
    """Normalizes event title for deterministic equality check."""
    if not name:
        return ""
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", name.lower())
    return " ".join(cleaned.split())


def is_winner_position(pos: str | None) -> bool:
    if not pos:
        return False
    p = pos.lower()
    return any(w in p for w in ["1st", "2nd", "3rd", "first", "second", "third", "winner", "prize"])


class DedupeCandidate(NamedTuple):
    item_idx: int
    fact: CertificateFacts
    raw_points: int
    level_rank: int
    is_winner: bool


DEDUPE_FAMILY_MAP = {
    "1.1": "sports_arts",
    "1.2": "sports_arts",
    "2.1": "tech_fest",
    "2.2": "tech_fest",
    "2.3": "presentations",
    "2.4": "presentations",
    "3.9": "hackathons",
    "3.10": "hackathons",
    "3.11.1": "project_competitions",
    "3.11.2": "project_competitions",
}


def get_dedupe_family(rule_id: str) -> str:
    """Returns the rule family for Rule i deduplication (e.g. participation vs winner)."""
    return DEDUPE_FAMILY_MAP.get(rule_id, rule_id)


def deduplicate_events(
    facts_with_points: list[tuple[CertificateFacts, int]],
    rules_by_id: dict[str, Any] | None = None,
) -> tuple[list[tuple[CertificateFacts, int]], dict[int, str]]:
    """Applies Rule i deduplication across activities sharing the same event.

    Returns:
        - List of (CertificateFacts, points) with duplicates reduced to 0 points.
        - Dict of item_index -> deduplication explanation note.
    """
    event_groups: dict[str, list[DedupeCandidate]] = {}
    dedupe_notes: dict[int, str] = {}

    for idx, (fact, pts) in enumerate(facts_with_points):
        norm_event = normalize_event_name(fact.event_name)
        if not norm_event:
            continue

        family = get_dedupe_family(fact.rule_id)
        # Event deduplication key scopes to the specific activity family
        event_key = f"{family}::{norm_event}"

        level_rank = fact.level.rank if fact.level else 0
        is_winner = is_winner_position(fact.position)
        candidate = DedupeCandidate(
            item_idx=idx,
            fact=fact,
            raw_points=pts,
            level_rank=level_rank,
            is_winner=is_winner,
        )
        event_groups.setdefault(event_key, []).append(candidate)

    suppressed_indices: set[int] = set()

    for _event_key, candidates in event_groups.items():
        if len(candidates) <= 1:
            continue

        # Sort criteria:
        # (1) has raw_points > 0: A 0-point candidate (e.g. DOUBT in pessimistic pass)
        #     must NEVER suppress a candidate with points > 0.
        # (2) raw_points: Higher points win ("the better one" per SPEC §7.8)
        # (3) is_winner: Winning position beats participation (Rule i)
        # (4) level_rank: Highest level of achievement attained counts (Rule i)
        # (5) stable cert_id tie-breaker
        sorted_candidates = sorted(
            candidates,
            key=lambda c: (
                c.raw_points > 0,
                c.raw_points,
                c.is_winner,
                c.level_rank,
                c.fact.certificate_id,
            ),
            reverse=True,
        )

        winner = sorted_candidates[0]
        for inferior in sorted_candidates[1:]:
            suppressed_indices.add(inferior.item_idx)
            dedupe_notes[inferior.item_idx] = (
                f"Superseded by higher achievement in event '{inferior.fact.event_name}' "
                f"({winner.fact.certificate_id}) per Rule i."
            )

    result_list: list[tuple[CertificateFacts, int]] = []
    for idx, (fact, pts) in enumerate(facts_with_points):
        if idx in suppressed_indices:
            existing_doubts = list(fact.doubt_codes)
            if "D-DUP" not in existing_doubts:
                existing_doubts.append("D-DUP")
            updated_fact = fact.model_copy(update={"doubt_codes": existing_doubts})
            result_list.append((updated_fact, 0))
        else:
            result_list.append((fact, pts))

    return result_list, dedupe_notes
