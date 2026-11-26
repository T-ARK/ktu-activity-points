# Project Progress Log — KTU Activity Points Checker

This file is an append-only log of development sessions, decisions, command evidence, and milestone reviews.

---

## Session 0: Phase 0 — Rules Digitisation & Verification Gate
**Date:** 2026-11-26
**Lead Engineer:** Antigravity AI Agent

### Plan
- Task: Establish repository skeleton, transcribe all Table 2 rows (1.1–3.17) to `rulesets/ktu-2024-v1.json`, create strict schema in `rulesets/schema/ruleset.schema.json`, document ambiguities in `docs/AMBIGUITIES.md`, implement `make rules-check`, and enforce G1/G2 constraints.
- Files: `rulesets/ktu-2024-v1.json`, `rulesets/ktu-2024-v1.sha256`, `rulesets/schema/ruleset.schema.json`, `docs/AMBIGUITIES.md`, `Makefile`, `scripts/rules_check.py`, `backend/pyproject.toml`, `README.md`, `docker-compose.yml`, `.github/workflows/ci.yml`.
- Tests: Schema validation, checksum verification, 100% rule ID coverage (1.1 to 3.17), boundary test inventory for all tiered rules (2.21, 2.22).
- Risks: Table formatting ambiguities in handbook PDF (caps spanning multiple rows, typo in STRIDE levels, missing hackathon participation tiers). Mitigated by conservative handling, dual-reading, and raising `S-02`.

### Work Log
- Initialized git repository on branch `main`.
- Created repository directories matching `agent.md` §5 structure.
- Copied KTU 2024 Scheme Handbook PDF to `docs/source/handbook-2024.pdf`.
- Migrated engineering spec to `docs/SPEC.md`.
- Documented known handbook ambiguities (A-01 to A-20) in `docs/AMBIGUITIES.md`.
- Implemented `rulesets/schema/ruleset.schema.json` using Draft 2020-12 JSON Schema specification.
- Transcribed all 64 rule rows (IDs 1.1 to 3.17, including 3.11.1 and 3.11.2) into `rulesets/ktu-2024-v1.json` with exact printed handbook page numbers and PDF page mappings.
- Computed and pinned ruleset cryptographic hash `f4abbcbe575db89d88b1995c8bade2ef1e5f0071db10c79d34fa35876fa7a370` in `rulesets/ktu-2024-v1.sha256`.
- Authored verification engine `scripts/rules_check.py` validating schema, hash, 100% Table 2 ID coverage, and 55 tier boundary assertions.
- Created unit boundary test suite `backend/tests/unit/test_rules_boundary.py` (82 passing test cases covering IELTS, TOEFL, PTE, BEC, GRE, GATE, CAT, GMAT).
- Configured `.importlinter` enforcing engine/doubt purity and API isolation.
- Created `Makefile`, `backend/pyproject.toml`, `README.md`, `docker-compose.yml`, `.github/workflows/ci.yml`, and `.gitignore`.

### Verification Evidence (`make gate`)
```text
==> Running ruff lint and format check...
All checks passed!
==> Running mypy strict type check on scripts & backend...
Success: no issues found in 1 source file
Success: no issues found in 12 source files
==> Running pytest test suite...
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- /home/ark123/Downloads/act/.venv/bin/python3
rootdir: /home/ark123/Downloads/act/backend
configfile: pyproject.toml
plugins: hypothesis-6.170.17
collected 82 items

backend/tests/unit/test_rules_boundary.py::TestEnglishProficiencyTiers::test_ielts_academic_boundaries[0.0-0] PASSED
... [82/82 boundary tests passed] ...
backend/tests/unit/test_rules_boundary.py::TestAptitudeProficiencyTiers::test_gmat_boundaries[800-30] PASSED

============================== 82 passed in 0.25s ==============================
==> Running golden & adversarial test suite...
    [Phase 0 Stub] Golden tests will activate in Phase 2/3.
==> Running KTU 2024 ruleset checks...
============================================================
KTU 2024 Activity Points Ruleset Verification (Phase 0)
============================================================
[1/4] Validating ruleset against JSON Schema...
  ✓ Ruleset schema valid.
[2/4] Verifying SHA-256 checksum...
  ✓ Checksum verified (f4abbcbe575db89d...).
[3/4] Verifying Table 2 rule ID coverage (1.1 to 3.17)...
  ✓ All 63 base rows present (total rules: 64).
[4/4] Verifying tiered score boundary test cases...
  ✓ Verified 55 tier boundary assertions across 2.21 & 2.22.
============================================================
ALL RULES-CHECK VERIFICATIONS PASSED
============================================================
==> Checking architectural boundaries with import-linter...

---------
Contracts
---------

Analyzed 12 files, 0 dependencies.
----------------------------------

Engine and doubt layer purity KEPT
API routers must not contain raw engine rule implementations KEPT

Contracts: 2 kept, 0 broken.

============================================================
                 ALL CI GATE CHECKS PASSED                  
============================================================
```

### Review State: Phase 0 Complete — Awaiting Approval Gate
Phase 0 deliverables are complete and verified. Ready for user inspection against `docs/source/handbook-2024.pdf`. Phase 1 deterministic engine work is held pending explicit user approval.
