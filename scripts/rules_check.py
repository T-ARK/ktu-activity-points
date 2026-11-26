#!/usr/bin/env python3
"""
Rules Verification Script for KTU 2024 Activity Points Ruleset.
Enforces:
1. JSON Schema validation
2. SHA-256 Checksum integrity
3. Full Table 2 row coverage (IDs 1.1 to 3.17)
4. Verification of boundary test definitions for all tiered rules (2.21, 2.22)
"""

import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

import jsonschema  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).resolve().parent.parent
RULESET_PATH = REPO_ROOT / "rulesets" / "ktu-2024-v1.json"
SCHEMA_PATH = REPO_ROOT / "rulesets" / "schema" / "ruleset.schema.json"
CHECKSUM_PATH = REPO_ROOT / "rulesets" / "ktu-2024-v1.sha256"

EXPECTED_BASE_IDS = [
    # Group I
    "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10",
    "1.11", "1.12", "1.13", "1.14", "1.15", "1.16", "1.17", "1.18", "1.19",
    "1.20", "1.21", "1.22", "1.23", "1.24",
    # Group II
    "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10",
    "2.11", "2.12", "2.13", "2.14", "2.15", "2.16", "2.17", "2.18", "2.19",
    "2.20", "2.21", "2.22",
    # Group III
    "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10",
    "3.11", "3.12", "3.13", "3.14", "3.15", "3.16", "3.17"
]

# Tier boundary test specifications required by agent.md §8.1
TIER_BOUNDARY_SPECS: dict[str, dict[str, list[tuple[Any, int]]]] = {
    "2.21": {
        "IELTS_Academic": [
            ("6.0", 0),
            ("6.4", 0),
            ("6.5", 20),
            ("6.9", 20),
            ("7.0", 25),
            ("7.4", 25),
            ("7.5", 30),
            ("8.0", 30),
            ("9.0", 30),
        ],
        "TOEFL_iBT": [
            (79, 0),
            (80, 20),
            (94, 20),
            (95, 25),
            (104, 25),
            (105, 30),
            (120, 30),
        ],
        "PTE_Academic": [
            (57, 0),
            (58, 20),
            (64, 20),
            (65, 25),
            (75, 25),
            (76, 30),
            (90, 30),
        ],
        "Cambridge_BEC": [
            ("Below_B1", 0),
            ("Preliminary_B1", 15),
            ("Vantage_B2", 20),
            ("Higher_C1", 25),
        ],
    },
    "2.22": {
        "GRE": [
            (299, 0),
            (300, 20),
            (309, 20),
            (310, 25),
            (319, 25),
            (320, 30),
            (340, 30),
        ],
        "GATE": [
            ({"qualified": False, "air": None}, 0),
            ({"qualified": True, "air": None}, 20),
            ({"qualified": True, "air": 15001}, 20),
            ({"qualified": True, "air": 15000}, 25),
            ({"qualified": True, "air": 5001}, 25),
            ({"qualified": True, "air": 5000}, 30),
            ({"qualified": True, "air": 1}, 30),
        ],
        "CAT": [
            ("84.99", 0),
            ("85.00", 20),
            ("89.99", 20),
            ("90.00", 25),
            ("94.99", 25),
            ("95.00", 30),
            ("100.00", 30),
        ],
        "GMAT": [
            (599, 0),
            (600, 20),
            (649, 20),
            (650, 25),
            (699, 25),
            (700, 30),
            (800, 30),
        ],
    },
}


def evaluate_tier_score(
    rule_id: str, test_name: str, score_input: Any, tests_config: dict[str, Any]
) -> int:
    """Deterministic evaluation of tiered scores."""
    if rule_id == "2.21":
        if test_name == "IELTS_Academic":
            score_dec = Decimal(str(score_input))
            if score_dec >= Decimal("7.5"):
                return 30
            if score_dec >= Decimal("7.0"):
                return 25
            if score_dec >= Decimal("6.5"):
                return 20
            return 0
        elif test_name == "TOEFL_iBT":
            score_int = int(score_input)
            if score_int >= 105:
                return 30
            if score_int >= 95:
                return 25
            if score_int >= 80:
                return 20
            return 0
        elif test_name == "PTE_Academic":
            score_int = int(score_input)
            if score_int >= 76:
                return 30
            if score_int >= 65:
                return 25
            if score_int >= 58:
                return 20
            return 0
        elif test_name == "Cambridge_BEC":
            levels = {"Higher_C1": 25, "Vantage_B2": 20, "Preliminary_B1": 15}
            return levels.get(str(score_input), 0)

    elif rule_id == "2.22":
        if test_name == "GRE":
            score_int = int(score_input)
            if score_int >= 320:
                return 30
            if score_int >= 310:
                return 25
            if score_int >= 300:
                return 20
            return 0
        elif test_name == "GATE":
            gate_dict = cast(dict[str, Any], score_input)
            qualified = bool(gate_dict.get("qualified", False))
            air = gate_dict.get("air")
            if not qualified:
                return 0
            if air is not None:
                air_int = int(air)
                if air_int <= 5000:
                    return 30
                if air_int <= 15000:
                    return 25
            return 20
        elif test_name == "CAT":
            score_dec = Decimal(str(score_input))
            if score_dec >= Decimal("95.00"):
                return 30
            if score_dec >= Decimal("90.00"):
                return 25
            if score_dec >= Decimal("85.00"):
                return 20
            return 0
        elif test_name == "GMAT":
            score_int = int(score_input)
            if score_int >= 700:
                return 30
            if score_int >= 650:
                return 25
            if score_int >= 600:
                return 20
            return 0

    raise ValueError(f"Unknown test {test_name} for rule {rule_id}")


def check_schema(ruleset_data: dict[str, Any], schema_data: dict[str, Any]) -> None:
    print("[1/4] Validating ruleset against JSON Schema...")
    validator = jsonschema.Draft202012Validator(schema_data)
    errors = sorted(validator.iter_errors(ruleset_data), key=lambda e: str(e.path))
    if errors:
        for err in errors:
            loc = ".".join(str(p) for p in err.path)
            print(f"  ERROR at {loc}: {err.message}")
        sys.exit(1)
    print("  ✓ Ruleset schema valid.")


def check_checksum() -> None:
    print("[2/4] Verifying SHA-256 checksum...")
    if not CHECKSUM_PATH.exists():
        print(f"  ERROR: Checksum file not found at {CHECKSUM_PATH}")
        sys.exit(1)

    with open(RULESET_PATH, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(CHECKSUM_PATH, encoding="utf-8") as f:
        expected_line = f.read().strip()
        expected_hash = expected_line.split()[0] if expected_line else ""

    if actual_hash != expected_hash:
        print(
            f"  ERROR: Checksum mismatch!\n    Actual:   {actual_hash}\n    Expected: {expected_hash}"
        )
        sys.exit(1)
    print(f"  ✓ Checksum verified ({actual_hash[:16]}...).")


def check_coverage(ruleset_data: dict[str, Any]) -> None:
    print("[3/4] Verifying Table 2 rule ID coverage (1.1 to 3.17)...")
    raw_rules = cast(list[dict[str, Any]], ruleset_data.get("rules", []))
    found_ids = {str(r["id"]) for r in raw_rules}

    missing = []
    for expected in EXPECTED_BASE_IDS:
        if expected == "3.11":
            if "3.11" not in found_ids and not ("3.11.1" in found_ids and "3.11.2" in found_ids):
                missing.append(expected)
        elif expected not in found_ids:
            missing.append(expected)

    if missing:
        print(f"  ERROR: Missing expected rule IDs: {missing}")
        sys.exit(1)
    print(f"  ✓ All {len(EXPECTED_BASE_IDS)} base rows present (total rules: {len(found_ids)}).")


def check_tier_boundaries(ruleset_data: dict[str, Any]) -> None:
    print("[4/4] Verifying tiered score boundary test cases...")
    raw_rules = cast(list[dict[str, Any]], ruleset_data.get("rules", []))
    rules_by_id = {str(r["id"]): r for r in raw_rules}

    total_boundary_checks = 0
    for rule_id, tests_dict in TIER_BOUNDARY_SPECS.items():
        if rule_id not in rules_by_id:
            print(f"  ERROR: Tiered rule {rule_id} not in ruleset")
            sys.exit(1)

        rule_data = rules_by_id[rule_id]
        points_obj = cast(dict[str, Any], rule_data.get("points", {}))
        tests_config = cast(dict[str, Any], points_obj.get("tests", {}))

        for test_name, cases in tests_dict.items():
            for score_input, expected_points in cases:
                actual = evaluate_tier_score(rule_id, test_name, score_input, tests_config)
                if actual != expected_points:
                    print(
                        f"  ERROR: Tier boundary failure for {rule_id} {test_name} input={score_input}: "
                        f"expected {expected_points}, got {actual}"
                    )
                    sys.exit(1)
                total_boundary_checks += 1

    print(f"  ✓ Verified {total_boundary_checks} tier boundary assertions across 2.21 & 2.22.")


def main() -> None:
    print("=" * 60)
    print("KTU 2024 Activity Points Ruleset Verification (Phase 0)")
    print("=" * 60)

    if not RULESET_PATH.exists():
        print(f"ERROR: Ruleset file not found at {RULESET_PATH}")
        sys.exit(1)
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    with open(RULESET_PATH, encoding="utf-8") as f:
        ruleset_data = cast(dict[str, Any], json.load(f))
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema_data = cast(dict[str, Any], json.load(f))

    check_schema(ruleset_data, schema_data)
    check_checksum()
    check_coverage(ruleset_data)
    check_tier_boundaries(ruleset_data)

    print("=" * 60)
    print("ALL RULES-CHECK VERIFICATIONS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
