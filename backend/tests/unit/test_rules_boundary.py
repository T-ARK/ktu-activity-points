"""
Boundary unit tests for tiered scoring rules in KTU 2024 Scheme (Rows 2.21 & 2.22).
Enforces:
- IELTS Academic: 6.0, 6.4, 6.5, 6.9, 7.0, 7.4, 7.5, 8.0, 9.0
- TOEFL iBT: 79, 80, 94, 95, 104, 105, 120
- PTE Academic: 57, 58, 64, 65, 75, 76, 90
- Cambridge BEC: Preliminary B1, Vantage B2, Higher C1, Below B1
- GRE: 299, 300, 309, 310, 319, 320, 340
- GATE: Qualified score, AIR 15001, AIR 15000, AIR 5001, AIR 5000, Not qualified
- CAT: 84.99, 85.00, 89.99, 90.00, 94.99, 95.00, 100.00
- GMAT: 599, 600, 649, 650, 699, 700, 800
Strictly uses Decimal for decimal comparisons, never float.
"""

from decimal import Decimal

import pytest
from rules_check import evaluate_tier_score


class TestEnglishProficiencyTiers:
    """Row 2.21 English Proficiency Certifications boundary tests."""

    @pytest.mark.parametrize(
        "band_str,expected_points",
        [
            ("0.0", 0),
            ("6.0", 0),
            ("6.4", 0),
            ("6.5", 20),
            ("6.9", 20),
            ("7.0", 25),
            ("7.4", 25),
            ("7.5", 30),
            ("8.0", 30),
            ("8.5", 30),
            ("9.0", 30),
        ],
    )
    def test_ielts_academic_boundaries(self, band_str: str, expected_points: int):
        score = Decimal(band_str)
        points = evaluate_tier_score("2.21", "IELTS_Academic", score, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "score,expected_points",
        [
            (0, 0),
            (79, 0),
            (80, 20),
            (85, 20),
            (94, 20),
            (95, 25),
            (100, 25),
            (104, 25),
            (105, 30),
            (115, 30),
            (120, 30),
        ],
    )
    def test_toefl_ibt_boundaries(self, score: int, expected_points: int):
        points = evaluate_tier_score("2.21", "TOEFL_iBT", score, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "score,expected_points",
        [
            (10, 0),
            (57, 0),
            (58, 20),
            (60, 20),
            (64, 20),
            (65, 25),
            (70, 25),
            (75, 25),
            (76, 30),
            (85, 30),
            (90, 30),
        ],
    )
    def test_pte_academic_boundaries(self, score: int, expected_points: int):
        points = evaluate_tier_score("2.21", "PTE_Academic", score, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "level,expected_points",
        [
            ("A2", 0),
            ("Below_B1", 0),
            ("Preliminary_B1", 15),
            ("Vantage_B2", 20),
            ("Higher_C1", 25),
        ],
    )
    def test_cambridge_bec_levels(self, level: str, expected_points: int):
        points = evaluate_tier_score("2.21", "Cambridge_BEC", level, {})
        assert points == expected_points


class TestAptitudeProficiencyTiers:
    """Row 2.22 Aptitude Proficiency Certifications boundary tests."""

    @pytest.mark.parametrize(
        "score,expected_points",
        [
            (260, 0),
            (299, 0),
            (300, 20),
            (305, 20),
            (309, 20),
            (310, 25),
            (315, 25),
            (319, 25),
            (320, 30),
            (330, 30),
            (340, 30),
        ],
    )
    def test_gre_boundaries(self, score: int, expected_points: int):
        points = evaluate_tier_score("2.22", "GRE", score, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "gate_input,expected_points",
        [
            ({"qualified": False, "air": None}, 0),
            ({"qualified": False, "air": 100}, 0),  # Not qualified
            ({"qualified": True, "air": None}, 20),   # Qualified with valid score
            ({"qualified": True, "air": 25000}, 20),
            ({"qualified": True, "air": 15001}, 20),
            ({"qualified": True, "air": 15000}, 25),
            ({"qualified": True, "air": 10000}, 25),
            ({"qualified": True, "air": 5001}, 25),
            ({"qualified": True, "air": 5000}, 30),
            ({"qualified": True, "air": 100}, 30),
            ({"qualified": True, "air": 1}, 30),
        ],
    )
    def test_gate_boundaries(self, gate_input: dict, expected_points: int):
        points = evaluate_tier_score("2.22", "GATE", gate_input, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "percentile_str,expected_points",
        [
            ("50.00", 0),
            ("84.99", 0),
            ("85.00", 20),
            ("87.50", 20),
            ("89.99", 20),
            ("90.00", 25),
            ("92.50", 25),
            ("94.99", 25),
            ("95.00", 30),
            ("99.90", 30),
            ("100.00", 30),
        ],
    )
    def test_cat_percentile_boundaries(self, percentile_str: str, expected_points: int):
        score = Decimal(percentile_str)
        points = evaluate_tier_score("2.22", "CAT", score, {})
        assert points == expected_points

    @pytest.mark.parametrize(
        "score,expected_points",
        [
            (200, 0),
            (599, 0),
            (600, 20),
            (625, 20),
            (649, 20),
            (650, 25),
            (675, 25),
            (699, 25),
            (700, 30),
            (750, 30),
            (800, 30),
        ],
    )
    def test_gmat_boundaries(self, score: int, expected_points: int):
        points = evaluate_tier_score("2.22", "GMAT", score, {})
        assert points == expected_points
