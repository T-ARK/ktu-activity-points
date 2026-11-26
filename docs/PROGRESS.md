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

### Review State: Phase 0 Complete — Approved by User
Phase 0 deliverables were approved by the user ("approved for phase 1") on 2026-11-26.

---

## Session 1: Phase 1 — Deterministic MVP with No AI
**Date:** 2026-11-26
**Lead Engineer:** Antigravity AI Agent

### Plan
- Implement pure deterministic engine: schemas, scoring, deduplication (Rule i), fixed-order caps (§7.9), pessimistic/optimistic aggregation passes, dual-reading ambiguity checks (A-04).
- Implement Doubt Engine: `DoubtCode` enum (38 codes), `can_verify()` allow-list, documentation generator.
- Implement FastAPI backend: profile, rules explorer, manual activities, dashboard evaluation, CSV and PDF export with SFA signature block and mandatory disclaimer.
- Implement React + Vite + TypeScript strict frontend: dashboard with mandatory 3-number display, group cards, activity ledger with interactive doubt drawers, rules explorer, manual activity modal with live point estimator, and persistent disclaimer banner.
- Test-first verification: Hypothesis property tests (invariants: Confirmed <= Upper bound, caps never exceeded, upload order independence, winner beats participation, highest level wins, monotonicity), mutation-resistant allow-list tests, API tests, boundary tests, import-linter architecture contracts.

### Work Log
- **Schemas (`backend/app/schemas/`):**
  - Defined `StudentProfile`, `EntryType` (regular 120/40, lateral 90/30, PwD 60/20).
  - Defined `Level` (rank 1..5) and `Verdict` (VERIFIED, DOUBT, NOT_ELIGIBLE, MANUAL_ONLY).
  - Defined `CertificateFacts` with Decimal scores and immutable frozen models.
  - Defined `PointBracket` (confirmed, pending, upper_bound), `ActivityOutcome`, `GroupResult`, `EngineResult`.
  - Defined `CertificateAnalysis` with 13 boolean predicates for allow-list verification.
- **Doubt Engine (`backend/app/doubt/`):**
  - Transcribed all 38 doubt codes into `DoubtCode` enum (`backend/app/doubt/codes.py`).
  - Authored `DOUBT_REGISTRY` with templates, severity, resolve guidance, and points impact (`backend/app/doubt/messages.py`).
  - Implemented `can_verify()` explicit allow-list evaluating all 13 verification predicates (`backend/app/doubt/verify.py`).
  - Created `scripts/gen_doubt_codes.py` generating `docs/DOUBT_CODES.md`.
- **Deterministic Rules Engine (`backend/app/engine/`):**
  - `scoring.py`: Pure scoring for leveled, flat, per_unit, tiered_score, role_based, milestone_based, and manual activities.
  - `dedupe.py`: Implemented Rule i event deduplication scoped to activity families (sports/arts, tech fest, presentations, hackathons, project competitions) with points/level prioritization.
  - `caps.py`: Enforced fixed sequence: period limits (per AY / per semester) -> subhead caps -> shared & category caps. Prioritizes VERIFIED activities for caps.
  - `aggregator.py`: `evaluate()` orchestrator running pessimistic and optimistic passes, dual-reading for A-04, group aggregation, and credit checks.
- **FastAPI Backend (`backend/app/api/` & `backend/app/main.py`):**
  - `app/api/profile.py`: Profile setup and threshold management.
  - `app/api/rules.py`: Rules exploration endpoint.
  - `app/api/activities.py`: Activity submission, deletion, and sample portfolio loading.
  - `app/api/dashboard.py`: Dashboard evaluation endpoint returning 3-number brackets, group totals, and doubt details.
  - `app/api/export.py`: Activity Points File export in CSV and PDF formats (using `fpdf2`) with student details, activity ledger, summary brackets, SFA/HoD signature block, and mandatory statutory disclaimer.
  - `app/main.py`: CORS middleware, mounted routers, healthcheck.
- **Frontend Application (`frontend/`):**
  - Initialized React 19 + Vite 6 + TypeScript (strict) + Tailwind CSS v4 in `frontend/`.
  - Created `DisclaimerBanner`: Persistent statutory disclaimer banner per SPEC §12.2 and agent.md §1.2.
  - Created `PointDisplay`: Mandatory 3-number display: Confirmed (Green) + Pending (Amber) / Upper Bound (Slate).
  - Created `DashboardView`: Degree credit progress card, 3 Group cards with required vs earned brackets, Activity ledger table with interactive doubt drawers.
  - Created `RulesExplorerView`: Searchable, filterable catalog of all 64 Table 2 rules with points, tiers, caps, and documentary evidence.
  - Created `ManualEntryModal`: Rule picker with search, level/position selectors, score inputs, and live point preview.
  - Created `ProfileModal`: Profile setup with real-time threshold recalculation (Regular, Lateral, PwD).
  - Tested production build: `npm run build` completed with zero TypeScript errors.

### Verification Evidence (`make gate`)
```text
==> Running ruff lint and format check...
All checks passed!
==> Running mypy strict type check on scripts & backend...
Success: no issues found in 1 source file
Success: no issues found in 31 source files
==> Running pytest test suite (unit + property)...
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- /home/ark123/Downloads/act/.venv/bin/python3
cachedir: .pytest_cache
hypothesis profile 'default'
rootdir: /home/ark123/Downloads/act/backend
configfile: pyproject.toml
plugins: hypothesis-6.170.17, anyio-4.16.0
collected 146 items

backend/tests/unit/test_api.py::test_healthcheck PASSED                  [  0%]
backend/tests/unit/test_api.py::test_profile_endpoints PASSED            [  1%]
backend/tests/unit/test_api.py::test_rules_endpoints PASSED              [  2%]
backend/tests/unit/test_api.py::test_activities_and_dashboard PASSED     [  2%]
backend/tests/unit/test_api.py::test_export_endpoints PASSED             [  3%]
backend/tests/unit/test_can_verify.py::test_can_verify_all_pass PASSED   [  4%]
... [14/14 can_verify allow-list tests passed] ...
backend/tests/unit/test_doubt_codes.py::test_all_doubt_codes_registered PASSED [ 17%]
... [39/39 doubt code registry tests passed] ...
backend/tests/unit/test_rules_boundary.py::TestEnglishProficiencyTiers::test_ielts_academic_boundaries PASSED [ 45%]
... [82/82 boundary tests passed] ...
backend/tests/property/test_engine_properties.py::test_confirmed_le_upper_bound PASSED [ 96%]
backend/tests/property/test_engine_properties.py::test_caps_never_exceeded PASSED [ 97%]
backend/tests/property/test_engine_properties.py::test_order_independence PASSED [ 97%]
backend/tests/property/test_engine_properties.py::test_rule_i_winner_beats_participation PASSED [ 98%]
backend/tests/property/test_engine_properties.py::test_rule_i_highest_level_wins PASSED [ 99%]
backend/tests/property/test_engine_properties.py::test_monotonicity_adding_certificate PASSED [100%]

======================= 146 passed, 1 warning in 10.25s ========================
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

╔══╗─────────▶╔╗ ╔╗      ╔╗◀───┐
╚╣╠╝◀─────┐  ╔╝╚╗║║────▶╔╝╚╗   │
 ║║   ╔══╦══╦╩╗╔╝║║  ╔╦═╩╗╔╝╔═╦══╗
 ║║╔══╣╔╗║╔╗║╔╣║ ║║ ╔╬╣╔╗║║ ║│║╔═╝
╔╣╠╣║║║╚╝║╚╝║║║╚╗║╚═╝║║║║║╚╗║═╣║
╚══╩╩╩╣╔═╩══╩╝╚═╝╚═══╩╩╝╚╩═╩╩═╩╝
  └──▶║║                    ▲ 
      ╚╝────────────────────┘

---------
Contracts
---------

Analyzed 44 files, 76 dependencies.
-----------------------------------

Engine and doubt layer purity KEPT
API routers must not contain raw engine rule implementations KEPT

Contracts: 2 kept, 0 broken.

============================================================
                 ALL CI GATE CHECKS PASSED                  
============================================================
```

### Review State: Phase 1 Deterministic MVP Complete
All Phase 1 requirements from `agent.md` §11 and `docs/SPEC.md` are complete, verified by tests, and packaged with zero AI dependencies in scoring. Ready for user testing and transition to Phase 2 (Document Ingestion & Multi-Engine Fact Extraction).
