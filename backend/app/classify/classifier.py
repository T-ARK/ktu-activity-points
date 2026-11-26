"""Stage 5: Rule Classification & Level Detection (SPEC §7.5 & §7.6)."""

from typing import Any

from pydantic import BaseModel


class ClassificationCandidate(BaseModel):
    rule_id: str
    rule_name: str
    group: str
    confidence: float
    reasons: list[str]


def classify_document_to_rules(text: str, ruleset: dict[str, Any]) -> list[ClassificationCandidate]:
    """Identifies candidate Table 2 rules from document text."""
    t_lower = text.lower()
    candidates: list[ClassificationCandidate] = []

    # 1. Aptitude tests (2.22)
    if any(k in t_lower for k in ["gate 20", "graduate aptitude test in engineering", "gre test", "common admission test"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="2.22",
                rule_name="Aptitude Proficiency Certifications",
                group="II",
                confidence=0.95,
                reasons=["Matched standard national aptitude test keywords"],
            )
        )

    # 2. English Proficiency (2.21)
    if any(k in t_lower for k in ["ielts", "toefl", "pte academic", "cambridge bec"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="2.21",
                rule_name="English Proficiency Certifications",
                group="II",
                confidence=0.95,
                reasons=["Matched international language proficiency exam headers"],
            )
        )

    # 3. Blood donation (1.8)
    if any(k in t_lower for k in ["blood donation", "blood bank", "voluntary blood"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="1.8",
                rule_name="Blood donation",
                group="I",
                confidence=0.90,
                reasons=["Matched voluntary blood donation phrases"],
            )
        )

    # 4. NSS (1.11, 1.14)
    if "national service scheme" in t_lower or "nss" in t_lower:
        if "appreciation" in t_lower or "special service" in t_lower:
            candidates.append(
                ClassificationCandidate(
                    rule_id="1.14",
                    rule_name="Special Service Certificate / Appreciation (NSS/NCC)",
                    group="I",
                    confidence=0.85,
                    reasons=["Matched NSS special service appreciation"],
                )
            )
        else:
            candidates.append(
                ClassificationCandidate(
                    rule_id="1.11",
                    rule_name="NSS Volunteer (Two Years)",
                    group="I",
                    confidence=0.85,
                    reasons=["Matched NSS volunteer scheme"],
                )
            )

    # 5. NCC (1.19)
    if "national cadet corps" in t_lower or "ncc" in t_lower:
        candidates.append(
            ClassificationCandidate(
                rule_id="1.19",
                rule_name="NCC Certificates",
                group="I",
                confidence=0.90,
                reasons=["Matched NCC certificate keywords"],
            )
        )

    # 6. Four wheeler license (1.5)
    if any(k in t_lower for k in ["driving licence", "driving license", "light motor vehicle", "lmv"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="1.5",
                rule_name="Four-wheeler license",
                group="I",
                confidence=0.95,
                reasons=["Matched motor vehicles department driving license"],
            )
        )

    # 7. Hackathons (3.15, 3.16)
    if "smart india hackathon" in t_lower or "sih 20" in t_lower or "kavach" in t_lower:
        candidates.append(
            ClassificationCandidate(
                rule_id="3.15",
                rule_name="National Hackathons",
                group="III",
                confidence=0.95,
                reasons=["Matched MoE / AICTE National Hackathon"],
            )
        )
    elif "space apps" in t_lower or "imagine cup" in t_lower or "global hackathon" in t_lower:
        candidates.append(
            ClassificationCandidate(
                rule_id="3.16",
                rule_name="International Hackathons",
                group="III",
                confidence=0.95,
                reasons=["Matched International Hackathon series"],
            )
        )

    # 8. Start-up & Patents (3.9, 3.10)
    if any(k in t_lower for k in ["patent", "indian patent office", "patent journal"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="3.10",
                rule_name="Patents",
                group="III",
                confidence=0.90,
                reasons=["Matched Patent official publication/filing"],
            )
        )
    if any(k in t_lower for k in ["udyam", "msme", "kerala startup mission", "startup company"]):
        candidates.append(
            ClassificationCandidate(
                rule_id="3.9",
                rule_name="Start-up Company (Legally Registered)",
                group="III",
                confidence=0.90,
                reasons=["Matched registered startup registration"],
            )
        )

    # 9. Internships (2.20 vs 3.3)
    if "internship" in t_lower or "industrial training" in t_lower:
        if any(k in t_lower for k in ["4 months", "long term", "long-term", "16 weeks"]):
            candidates.append(
                ClassificationCandidate(
                    rule_id="3.3",
                    rule_name="Long-Term Internship",
                    group="III",
                    confidence=0.85,
                    reasons=["Matched long-term internship duration"],
                )
            )
        else:
            candidates.append(
                ClassificationCandidate(
                    rule_id="2.20",
                    rule_name="Short-Term Internship",
                    group="II",
                    confidence=0.85,
                    reasons=["Matched short-term industrial internship"],
                )
            )

    # 10. Tech fests & Technical Events (2.1, 2.2, 2.3, 2.4)
    if any(k in t_lower for k in ["tech fest", "tech-fest", "robotics challenge", "hackathon"]):
        if any(w in t_lower for w in ["1st prize", "first prize", "winner", "1st place"]):
            candidates.append(
                ClassificationCandidate(
                    rule_id="2.2",
                    rule_name="Tech-Fest-Winners",
                    group="II",
                    confidence=0.80,
                    reasons=["Matched tech-fest winner keywords"],
                )
            )
        else:
            candidates.append(
                ClassificationCandidate(
                    rule_id="2.1",
                    rule_name="Tech-Fest-Participation",
                    group="II",
                    confidence=0.80,
                    reasons=["Matched tech-fest participation keywords"],
                )
            )

    # 11. Sports & Arts (1.1, 1.2, 1.3)
    if any(k in t_lower for k in ["sports", "athletic", "basketball", "volleyball", "arts festival", "youth festival"]):
        if any(w in t_lower for w in ["1st prize", "winner", "first prize", "champion"]):
            candidates.append(
                ClassificationCandidate(
                    rule_id="1.2",
                    rule_name="Sports/Games/Arts (Winners) - Single Events",
                    group="I",
                    confidence=0.75,
                    reasons=["Matched sports/arts winner keywords"],
                )
            )
        else:
            candidates.append(
                ClassificationCandidate(
                    rule_id="1.1",
                    rule_name="Sports/Games/Arts (Participation)",
                    group="I",
                    confidence=0.75,
                    reasons=["Matched sports/arts participation keywords"],
                )
            )

    # Deduplicate candidates by rule_id
    unique_candidates: dict[str, ClassificationCandidate] = {}
    for c in candidates:
        if c.rule_id not in unique_candidates or c.confidence > unique_candidates[c.rule_id].confidence:
            unique_candidates[c.rule_id] = c

    return list(unique_candidates.values())
