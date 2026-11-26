# KTU 2024 Scheme Activity Points Handbook — Ambiguity Register

This document tracks every ambiguity, omission, or typographical defect discovered in *APJ Abdul Kalam Technological University Activity Points Handbook – 2024 Scheme*.

Under the **Non-Negotiable Prime Directive** (agent.md §1 & §9), the system never chooses silently when the handbook is unclear. For every listed item, the engine implements the **conservative handling** and raises doubt code `S-02` (Result depends on handbook ambiguity) whenever the ambiguity affects a certificate's points or eligibility.

---

## Register of Ambiguities

### A-01: Activity Group Allocation Mismatch (Summary Table vs Table 2)
- **Handbook Location:** Page 1 summary table (PDF p. 4) vs Table 2 (PDF pp. 6–20).
- **Issue:** The summary table lists *hackathon participation* under Group II ("Participation in University level/State Level/ National Level Hackathons", 1 Credit / 40 Points) and *hackathon winners* under Group III ("Winners of National/ International Level Hackathons", 1 Credit / 40 Points). However, Table 2 places **all** hackathons (3.15 National, 3.16 International) under Group III. Furthermore, Table 2 includes Group II rows (tech competitions, FOSS, leadership) not mentioned in the summary.
- **Conservative Handling:** Table 2 is treated as authoritative for rule definition and group placement. Any certificate whose group attribution differs between the summary table and Table 2 raises `S-02`.

### A-02: National Hackathons — Missing Participation Tier
- **Handbook Location:** Table 2, Row 3.15 (PDF p. 20, printed p. 17).
- **Issue:** Row 3.15 lists point awards for 1st Prize (40), 2nd Prize (35), and 3rd Prize (30). There is **no row for participation**, despite Page 1 summary table explicitly citing "Participation in University level/State Level/ National Level Hackathons".
- **Conservative Handling:** National hackathon participation certificates cannot be automatically awarded points and are classified as `C-02` (No matching rule) with an `S-02` flag directing the student to SFA evaluation, rather than guessing a point value.

### A-03: International Hackathons — Participation Points Divergence
- **Handbook Location:** Table 2, Row 3.16 (PDF p. 20, printed p. 17).
- **Issue:** Row 3.16 explicitly provides 30 points for "Participation" in International Hackathons, whereas Row 3.15 (National) has no participation points.
- **Conservative Handling:** Applied strictly as written: 3.16 participation awards 30 points (subject to 40-point cap); 3.15 participation remains non-awardable in automated engine.

### A-04: Cap Placement for Rows 2.5 and 2.6 (Conferences vs Poster Presentations)
- **Handbook Location:** Table 2, Rows 2.5 & 2.6 (PDF p. 11, printed p. 8).
- **Issue:** The rightmost column shows "Maximum-15 points" vertically aligned with Row 2.5 (Attending conferences/workshops). Row 2.6 (Poster presentation) has no cap in its row, and visually flows into the "Maximum-40 points" bracket spanning Paper Presentations (2.7–2.10) on printed page 9.
- **Conservative Handling:** The engine computes both readings: (1) Row 2.5 capped at 15 and Row 2.6 sharing the 40-point cap with 2.7–2.10; (2) Rows 2.5 and 2.6 sharing the 15-point cap. If the candidate claim differs between the two, `S-02` is raised and the conservative (lower) value is taken for Confirmed points, and higher for Upper bound.

### A-05: Category Cap Scope for Rows 2.1–2.4 (Technical Events)
- **Handbook Location:** Table 2, Rows 2.1–2.4 (PDF p. 11, printed p. 8).
- **Issue:** A single "Maximum-40 points" block spans all four sub-heads: Tech-Fest Participation (2.1), Tech-Fest Winners (2.2), Professional Society Competitions Participation (2.3), and Professional Society Winners (2.4). It is ambiguous whether participation and winning across *different* events aggregate to 40 or if there are unstated sub-head caps.
- **Conservative Handling:** A combined category cap of 40 points is applied across rows 2.1–2.4. When total raw points exceed 40, `S-02` is attached to the capped total.

### A-06: Shared Cap for Rows 1.6 and 1.7 (Community Service)
- **Handbook Location:** Table 2, Rows 1.6 & 1.7 (PDF p. 7, printed p. 4).
- **Issue:** A single "Maximum-10 points" cell spans Row 1.6 (Two Days - 5 pts) and Row 1.7 (Up to One Week - 10 pts).
- **Conservative Handling:** Treated as a shared cap of 10 points across 1.6 and 1.7.

### A-07: Shared Cap for Rows 1.20 and 1.21 (Health, Safety & Essential Life Skills)
- **Handbook Location:** Table 2, Rows 1.20 & 1.21 (PDF p. 9, printed p. 6).
- **Issue:** The "Maximum-10 points" cell vertically spans Row 1.20 (Emergency Response/First Aid - 5 pts/training) and Row 1.21 (Basic Swimming - 5 pts).
- **Conservative Handling:** Treated as a shared cap of 10 points across 1.20 and 1.21.

### A-08: Shared Cap for Rows 1.23 and 1.24 (Magazine Editorial Board & Hobby Clubs)
- **Handbook Location:** Table 2, Rows 1.23 & 1.24 (PDF p. 10, printed p. 7).
- **Issue:** A single "Maximum-10 points" block spans Row 1.23 (Magazine Editorial Board) and Row 1.24 (Hobby Clubs under College Union).
- **Conservative Handling:** Shared cap of 10 points applied across 1.23 and 1.24. If combined claims exceed 10, the cap binds and `S-02` is logged.

### A-09: Group I Category-Level Cap Ambiguity
- **Handbook Location:** Table 2, Group I (PDF pp. 6–10, printed pp. 3–7).
- **Issue:** NSS/NCC (Rows 1.11–1.19) explicitly specifies "Maximum - 40 points" and displays a red "40 Points" category badge. Sports/Arts (1.1–1.5), Community Outreach (1.6–1.10), Health/Safety (1.20–1.21), and Union/Club (1.22–1.24) only display sub-head caps. It is ambiguous whether Group I overall is capped at 40 points towards the 120-point degree requirement, or whether excess points in Group I count towards the 120 total.
- **Conservative Handling:** The system maintains and displays both: (1) Total Points Earned in Group I, and (2) Points Counted towards the 40-per-group requirement. For total degree qualification, any points in Group I beyond 40 are treated as Pending/Doubtful until KTU clarifies if inter-group surplus offsets other groups.

### A-10: Typographical Error in Row 2.18 STRIDE Project Levels
- **Handbook Location:** Table 2, Row 2.18 (PDF p. 13, printed p. 10).
- **Issue:** The points for High Impact Project Team are printed as: `"L1-10 Points, L2-15 Points, L5-20 Points"`. Levels L3 and L4 are absent, jumping directly to L5. L5 is almost certainly a typographical error for L3.
- **Conservative Handling:** Only L1 (10 pts) and L2 (15 pts) are automatically evaluated. Any certificate asserting L3, L4, or L5 triggers `C-04` (Ambiguous level/role) and `S-02`, requiring SFA determination.

### A-11: Numbering Typo for Row 1.11
- **Handbook Location:** Table 2, Row 1.11 (PDF p. 7, printed p. 4).
- **Issue:** Numbered as `"1. 1.11"` in Table 2.
- **Conservative Handling:** Normalized to canonical ID `1.11`.

### A-12: KTU-Approved Precondition Evidence (Rows 2.1–2.2)
- **Handbook Location:** Table 2, Rows 2.1 & 2.2 Remarks (PDF p. 11, printed p. 8).
- **Issue:** Requires Tech-Fest to be "Organized or Approved by KTU". Certificates rarely quote KTU approval numbers.
- **Conservative Handling:** Unless KTU organization/approval is explicitly stated on the certificate or matched against an admin-approved event list, verdict is `DOUBT` (`R-04`/`C-07`).

### A-13: Shared Category Cap for Rows 3.9–3.13 (Innovation & Entrepreneurship)
- **Handbook Location:** Table 2, Rows 3.9–3.13 (PDF pp. 18–19, printed pp. 15–16).
- **Issue:** Start-up (3.9: 30 pts), Patents (3.10: up to 40 pts), Prototype (3.11: 40 pts), Tech Adopted (3.11: 40 pts), VC Funding (3.12: 40 pts), and Societal Innovations (3.13: 40 pts) are framed by a combined "Maximum- 40 points" bracket and a red "40 Points" banner.
- **Conservative Handling:** A shared ceiling of 40 points is enforced across the entire cluster 3.9–3.13.

### A-14: Unspecified Approved Skilling Course List (Row 3.17)
- **Handbook Location:** Table 2, Row 3.17 (PDF p. 20, printed p. 17).
- **Issue:** Mentions that lists of approved courses from KTU, K-DISC, SWAYAM/NPTEL, and Spoken Tutorial (IIT Bombay) will be published separately. No list is provided in the handbook.
- **Conservative Handling:** All skilling submissions receive `DOUBT` (`R-07`: Approved-course list not loaded / course not found) until an administrator loads a verified university course register.

### A-15: Definition of "Zonal" (Level 2)
- **Handbook Location:** Table 2 column headers and Rule iii.b (PDF p. 6 & p. 21).
- **Issue:** "Zonal" is a KTU-specific jurisdictional level. Certificates from outside KTU often use "zonal" to mean multi-state or district cluster.
- **Conservative Handling:** Level 2 is only assigned if KTU Zone is explicitly identified. Non-KTU "zonal" or "regional" defaults to `C-03` (`DOUBT`).

### A-16: Institutional / Departmental Certification Rows (Rows 3.1 & 3.2)
- **Handbook Location:** Table 2, Rows 3.1 & 3.2 (PDF p. 16, printed p. 13).
- **Issue:** 3.1 (Industrial Visit Report) and 3.2 (Best Project/Seminar) require internal college signatures (SFA, Evaluation Committee, HoD) and departmental evaluation.
- **Conservative Handling:** Classified as `MANUAL ONLY`. The engine allows logging but does not auto-award points without explicit SFA sign-off in the system.

### A-17: Level 5 (International) Scoring Across Sports/Arts (Rows 1.1–1.3)
- **Handbook Location:** Table 2, Rows 1.1, 1.2, 1.3 (PDF p. 6, printed p. 3).
- **Issue:** Column "International Events (Level 5)" assigns 40 points for Participation (1.1), 40 points for Single Winner (1.2), and 40 points for Group Winner (1.3). It is unclear whether each is an independent award or if a single event cap of 40 applies.
- **Conservative Handling:** Deduplication ensures participation is superseded by winning for the same event (Rule i). For different events, points are computed subject to the overall Sports/Arts/Group I cap.

### A-18: Dual Entries Under Row 3.11
- **Handbook Location:** Table 2, Row 3.11 (PDF p. 18, printed p. 15).
- **Issue:** Row 3.11 contains two separate entries in the table: (1) "Prototype Development & Testing" (40 points) and (2) "Innovative Technologies Adopted by Industry" (40 points), each with distinct evidence requirements.
- **Conservative Handling:** Modelled as distinct sub-rules `3.11.1` and `3.11.2` under rule head 3.11, both subject to the 40-point shared innovation cap (A-13).

### A-19: NCC Progression Milestones (Row 1.19)
- **Handbook Location:** Table 2, Row 1.19 (PDF p. 8, printed p. 5).
- **Issue:** Lists NCC "B" (20 pts), NCC "C" (30 pts), and One Year + Attendance (10 pts). Unclear whether a student can accumulate 10 + 20 + 30 = 60 (capped at 40) or if "C" certificate subsumes "B" and 1-year attendance.
- **Conservative Handling:** An NCC "C" certificate is treated as subsuming "B" and 1-year attendance unless explicitly separate academic years are proven; flagged with `S-02` if multiple claims are made.

### A-20: Preconditions for Row 2.11 Professional Society Coordinator
- **Handbook Location:** Table 2, Row 2.11 (PDF p. 12, printed p. 9).
- **Issue:** Row 2.11 title specifies "Minimum Period of 2 Academic Years", but lists "Student Coordinator for an event - 5/Event" alongside Member, Execom, and Secretary roles. Unclear if the 2-year tenure applies to single-event student coordinators.
- **Conservative Handling:** Student coordinator points require evidence of student society membership; cap of 15 points applies across all 2.11 activities.
