# KTU Activity Points Checker

A transparent, deterministic self-assessment web application for students under APJ Abdul Kalam Technological University (**KTU 2024 Scheme**) to evaluate their Activity Points and degree credit eligibility (120 points with ≥ 40 per group; lateral entry 90/30; PwD 60/20).

> **CRITICAL DISCLAIMER**
> This tool is a self-assessment and preparation aid. It does not replace official verification by Senior Faculty Advisors (SFAs) or official KTU portal submissions. The system makes NO claim of 100% OCR or AI extraction accuracy. Any uncertain or unverifiable data is strictly flagged as `DOUBT`. Submitting fake or altered documents cancels points and incurs university disciplinary action (Handbook §2 rule vii).

---

## Non-Negotiable Guarantees
- **G1 (Arithmetic Correctness)**: All point calculations, tiers, caps, event deduplication, and group totals are computed by a pure, deterministic rules engine. No AI is ever involved in calculating points.
- **G2 (No Silent Errors)**: The default verdict for any certificate is `DOUBT`. `VERIFIED` must be earned through an explicit allow-list of verifiable hard checks (`can_verify()`).
- **Three-Number Display**: Points are never presented as a single bare number; totals are strictly displayed as `{ Confirmed, Pending, Upper bound }`.

---

## Repository Structure
```
ktu-activity-points/
├── agent.md                        # Operating manual for the AI agent
├── Makefile                        # Development and gate verification targets
├── docs/
│   ├── SPEC.md                     # Complete product & engineering specification
│   ├── AMBIGUITIES.md              # Living handbook ambiguity register (A-01 to A-20)
│   ├── DOUBT_CODES.md              # Machine-generated doubt code register
│   ├── PROGRESS.md                 # Append-only session progress log
│   └── source/handbook-2024.pdf    # Source of truth KTU 2024 Handbook PDF
├── rulesets/
│   ├── ktu-2024-v1.json            # Machine-readable rules transcribed from Table 2
│   ├── ktu-2024-v1.sha256          # Cryptographic checksum for ruleset integrity
│   └── schema/ruleset.schema.json  # JSON schema for ruleset validation
├── backend/                        # FastAPI backend & pure deterministic engine
└── frontend/                       # React + Vite + TypeScript (strict)
```

---

## Development & Verification Commands
```bash
make setup          # Install dependencies
make lint           # Run ruff and mypy strict checks
make test           # Run unit and property tests
make rules-check    # Verify ruleset schema, checksum, Table 2 coverage & tier boundaries
make gate           # Execute mandatory CI quality gate before commit
```
