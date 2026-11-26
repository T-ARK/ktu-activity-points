"""Unit tests for Stage 2 & 4: Text Extraction, Grounding & Path A Extractors."""

from decimal import Decimal

from app.classify.classifier import classify_document_to_rules
from app.extract.path_a.events_and_community import (
    extract_level_from_text,
    extract_position_from_text,
    extract_recipient_name,
)
from app.extract.path_a.language_aptitude import (
    extract_aptitude_test,
    extract_language_test,
)
from app.schemas.verdict import Level
from app.text.extractor import is_quote_grounded


def test_quote_grounding_normalization():
    doc_text = "This is to certify that Rahul Nair has won First Prize in Inter-College debate."

    # Exact match
    assert is_quote_grounded("First Prize", doc_text) is True
    # Case insensitive
    assert is_quote_grounded("first prize", doc_text) is True
    # Hyphen & whitespace normalization
    assert is_quote_grounded("inter - college", doc_text) is True
    # Missing / Hallucinated quote
    assert is_quote_grounded("Second Prize", doc_text) is False


def test_extract_language_test():
    ielts_text = "Test Report Form - International English Language Testing System. Overall Band Score 7.5 (Academic)"
    res = extract_language_test(ielts_text)
    assert res is not None
    assert res["test_name"].value == "IELTS Academic"
    assert res["score"].value == Decimal("7.5")
    assert res["variant"].value == "Academic"

    toefl_text = "Test of English as a Foreign Language TOEFL iBT. Total Score: 104"
    res_toefl = extract_language_test(toefl_text)
    assert res_toefl is not None
    assert res_toefl["test_name"].value == "TOEFL iBT"
    assert res_toefl["score"].value == Decimal("104")


def test_extract_aptitude_test():
    gate_text = "Graduate Aptitude Test in Engineering GATE 2025 Scorecard. All India Rank: 4200. Qualified."
    res = extract_aptitude_test(gate_text)
    assert res is not None
    assert res["test_name"].value == "GATE"
    assert res["air"].value == 4200
    assert res["qualified"].value is True

    cat_text = "Common Admission Test (CAT 2024). Overall Percentile: 96.50"
    res_cat = extract_aptitude_test(cat_text)
    assert res_cat is not None
    assert res_cat["test_name"].value == "CAT"
    assert res_cat["score"].value == Decimal("96.50")


def test_extract_level_and_position():
    text1 = "Awarded to Akhil for securing 1st Prize in the National Level Robotics Challenge."
    lvl, _ = extract_level_from_text(text1)
    pos, _ = extract_position_from_text(text1)
    assert lvl == Level.NATIONAL
    assert pos == "1st Prize"

    text2 = "Certified that Ananya participated in the KTU Interzone Arts Festival."
    lvl2, _ = extract_level_from_text(text2)
    pos2, _ = extract_position_from_text(text2)
    assert lvl2 == Level.ZONAL
    assert pos2 == "Participation"


def test_extract_recipient_name():
    text = "This is to certify that Sreehari Menon has successfully completed two years as NSS Volunteer."
    name, quote = extract_recipient_name(text)
    assert name is not None
    assert "Sreehari Menon" in name


def test_rule_classification():
    ruleset = {"rules": []}
    text = "Ministry of Education Innovation Cell - Smart India Hackathon 2024 Grand Finale Winners"
    candidates = classify_document_to_rules(text, ruleset)
    assert len(candidates) >= 1
    assert candidates[0].rule_id == "3.15"
