# KTU Activity Points Checker - Accuracy Report

> **Last Generated:** 2026-11-26  
> **Evaluator:** Deterministic Rules Engine (`ktu-2024-v1`)  
> **Evaluation Dataset:** `golden/sample_certificates.json` (N = 40)

---

## 1. Statutory Guarantees & Principle

In strict accordance with `agent.md` and `docs/SPEC.md`:
- **G1 (Points Arithmetic):** 100% deterministic code. No floating point math (`Decimal`/`int` only). No AI in scoring.
- **G2 (No Silent Errors):** Default verdict is `DOUBT`. `VERIFIED` must be earned by satisfying every predicate in the explicit allow-list `can_verify()`.
- **Honest Accuracy Disclosure:** We never claim "100% accurate AI". In accordance with the statistical **Rule of Three**, observing 0 errors in $n=29$ independent VERIFIED decisions establishes a 95% confidence upper bound of $\approx \frac{3}{29} = 10.3\%$ on the true error rate.

---

## 2. Accuracy Scorecard (SPEC §14.3)

| Metric | Target | Measured Value | Status |
|---|---|---|---|
| **VERIFIED Error Rate** | **0.0%** | **0.00%** (0 errors / 29 verified) | **PASS** |
| **VERIFIED Precision** | **100.0%** | **100.00%** | **PASS** |
| **Missed Doubt Rate** | **0.0%** | **0.00%** (0 missed doubts) | **PASS** |
| **Points Arithmetic Accuracy (G1)** | **100.0%** | **100.00%** (40/40 match) | **PASS** |
| **Over-Claim Rate** | **< 1.0%** | **0.00%** (0 over-claims) | **PASS** |
| **DOUBT Rate** | 15–35% (clean) | **27.50%** (includes adversarial set) | **EXPECTED** |
| **95% Confidence Upper Bound** | Statistical | **< 10.34%** (Rule of Three, $n=29$) | **VERIFIED** |

---

## 3. Adjudicated Sample Portfolio Evaluation

Evaluation of the standard synthetic student activity portfolio (`sample-1` to `sample-9`):

### Summary Brackets
- **Total Points:** Confirmed: **435** | Pending: **56** | Upper Bound: **491**
- **Degree Requirement Status:** **ACHIEVED**
- **Credits Earned:** Confirmed: **3 / 3** | Upper Bound: **3 / 3**

### Group Totals
| Group | Confirmed | Pending | Upper Bound | Required | Credit Achieved |
|---|---|---|---|---|---|
| **Group I (Sports, Arts, NSS/NCC, Society)** | 135 | 11 | 146 | 40 | YES |
| **Group II (Tech Fests, Papers, Internships, Exams)** | 110 | 0 | 110 | 40 | YES |
| **Group III (Projects, Startups, Hackathons, MOOCs)** | 190 | 45 | 235 | 40 | YES |

---

## 4. Itemised Sample Audit Log

| Sample ID | Group | Rule | Description | Expected | System | Raw Pts | Counted (Pess/Opt) | Doubts |
|---|---|---|---|---|---|---|---|---|
| `GOLDEN-G1-01` | I | `1.1` | KTU Interzone Basketball Tournament 2024 - Participant | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-02` | I | `1.2` | Kerala State Inter-Collegiate Arts Festival - Classical Music | VERIFIED | VERIFIED | 20 | 20 / 20 | None |
| `GOLDEN-G1-03` | I | `1.3` | All India Inter-University Volleyball Championship - 2nd Prize | VERIFIED | VERIFIED | 30 | 30 / 30 | None |
| `GOLDEN-G1-04` | I | `1.4` | Poem Published in College Annual Magazine | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-05` | I | `1.5` | Four-Wheeler Light Motor Vehicle Driving License | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-06` | I | `1.8` | Voluntary Blood Donation at District Hospital | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-07` | I | `1.11` | NSS Volunteer Completion (Two Full Years) | VERIFIED | VERIFIED | 30 | 10 / 10 | None |
| `GOLDEN-G1-08` | I | `1.19` | NCC 'C' Certificate - Army Wing | VERIFIED | VERIFIED | 30 | 30 / 30 | None |
| `GOLDEN-G1-09` | I | `1.20` | CPR & Basic Life Support (BLS) Certification | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-10` | I | `1.21` | Basic Swimming Proficiency Certificate | VERIFIED | VERIFIED | 5 | 5 / 5 | None |
| `GOLDEN-G1-11` | I | `1.22` | College Union Executive Committee Member | VERIFIED | VERIFIED | 15 | 15 / 15 | None |
| `GOLDEN-G2-01` | II | `2.1` | State Tech Fest - Line Follower Robotics Participant | VERIFIED | VERIFIED | 10 | 0 / 0 | None |
| `GOLDEN-G2-02` | II | `2.2` | National Tech Fest - Autonomous Drone Challenge 1st Prize | VERIFIED | VERIFIED | 40 | 40 / 40 | None |
| `GOLDEN-G2-03` | II | `2.3` | IEEE Student Branch Paper Presentation Participant | VERIFIED | VERIFIED | 20 | 0 / 0 | None |
| `GOLDEN-G2-04` | II | `2.20` | Short-Term Industrial Internship at Keltron (2 Weeks) | VERIFIED | VERIFIED | 10 | 10 / 10 | None |
| `GOLDEN-G2-05` | II | `2.21` | IELTS Academic Test Result Form - Overall Band 7.5 | VERIFIED | VERIFIED | 30 | 30 / 30 | None |
| `GOLDEN-G2-06` | II | `2.21` | TOEFL iBT Score Report - Total 102 | VERIFIED | VERIFIED | 25 | 0 / 0 | None |
| `GOLDEN-G2-07` | II | `2.22` | GATE 2025 Scorecard - All India Rank 4200 | VERIFIED | VERIFIED | 30 | 30 / 30 | None |
| `GOLDEN-G3-01` | III | `3.3` | Long-Term Industrial Internship at Bosch Global Software (4 Months) | VERIFIED | VERIFIED | 15 | 15 / 15 | None |
| `GOLDEN-G3-02` | III | `3.8` | Working FOSS Solution Innovation Certified by ICFOSS | VERIFIED | VERIFIED | 25 | 25 / 25 | None |
| `GOLDEN-G3-03` | III | `3.9` | Start-up Registration Certificate under MSME / KSUM | VERIFIED | VERIFIED | 30 | 0 / 0 | None |
| `GOLDEN-G3-04` | III | `3.10` | Patent Application Published in Indian Patent Office Official Journal | VERIFIED | VERIFIED | 30 | 0 / 0 | None |
| `GOLDEN-G3-05` | III | `3.11.1` | Prototype Development & Performance Testing Validated by IEDC | VERIFIED | VERIFIED | 40 | 40 / 40 | None |
| `GOLDEN-G3-06` | III | `3.14` | Research Paper Published in Scopus Q1 Journal | VERIFIED | VERIFIED | 40 | 40 / 40 | None |
| `GOLDEN-G3-07` | III | `3.15` | Smart India Hackathon (SIH) 2024 - 1st Prize Winner | VERIFIED | VERIFIED | 40 | 40 / 40 | None |
| `GOLDEN-G3-08` | III | `3.16` | NASA International Space Apps Challenge - Global Finalist Participation | VERIFIED | VERIFIED | 30 | 30 / 30 | None |
| `DOUBT-Q01` | I | `1.1` | College Football Championship - Blurry Mobile Photo | DOUBT | DOUBT | 1 | 0 / 1 | Q-01 |
| `DOUBT-E05` | I | `1.14` | State NSS Cell Appreciation Letter - Name Spelling Discrepancy | DOUBT | DOUBT | 15 | 0 / 0 | E-05 |
| `DOUBT-E06` | II | `2.3` | Robotics Seminar with Ambiguous Date Format (04/05/2025) | DOUBT | DOUBT | 15 | 0 / 0 | E-06 |
| `DOUBT-R01` | I | `1.5` | Driving License Issued Prior to University Admission | DOUBT | DOUBT | 5 | 0 / 0 | R-01 |
| `DOUBT-R02` | III | `3.3` | Internship Completed After Programme End Date | DOUBT | DOUBT | 15 | 0 / 15 | R-02 |
| `DOUBT-R03` | II | `2.20` | Short-Term Internship Lasting Only 5 Days (Insufficient Duration) | DOUBT | DOUBT | 10 | 0 / 0 | R-03 |
| `DOUBT-R04` | III | `3.17` | Python Bootcamp from Unapproved Private Online Academy | DOUBT | DOUBT | 30 | 0 / 30 | R-04 |
| `DOUBT-C01` | II | `2.3` | Paper Presentation on Edge AI - Subhead Ambiguous | DOUBT | DOUBT | 20 | 0 / 0 | C-01 |
| `DOUBT-C03` | I | `1.1` | District Athletic Meet - Ambiguous Tier Level | DOUBT | DOUBT | 5 | 0 / 5 | C-03 |
| `DOUBT-V01` | I | `1.8` | Blood Donation Certificate Missing NSS Officer Signature | DOUBT | DOUBT | 5 | 0 / 5 | V-01 |
| `BOUNDARY-IELTS-6.5` | II | `2.21` | IELTS Academic Test - Band 6.5 (Minimum Tier) | VERIFIED | VERIFIED | 20 | 0 / 0 | None |
| `BOUNDARY-GATE-5000` | II | `2.22` | GATE Examination - All India Rank 5000 (Boundary) | VERIFIED | VERIFIED | 30 | 0 / 0 | None |
| `BOUNDARY-GATE-5001` | II | `2.22` | GATE Examination - All India Rank 5001 (Boundary Step-down) | VERIFIED | VERIFIED | 25 | 0 / 0 | None |
| `BOUNDARY-TOEFL-79` | II | `2.21` | TOEFL iBT Test - Score 79 (Sub-threshold) | DOUBT | DOUBT | 0 | 0 / 0 | C-03 |

---

## 5. Statistical Note (Rule of Three)

As mandated by `SPEC §14.3`:
Observing **0 errors in $n$ independent VERIFIED decisions** gives a 95% confidence upper bound on the true error rate of $\approx \frac{3}{n}$.
- With current golden cohort $n=29$, the measured error rate is **0.0%** and the 95% statistical upper bound is **< 10.3%**.
- To mathematically prove a true production error rate of $< 0.1\%$, at least $n \ge 3,000$ error-free consecutive verified certificates must be audited.
