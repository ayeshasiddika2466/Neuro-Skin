from backend.questionnaire import (
    score_phq9, score_gad7, phq9_band, to_level
)


def test_phq9_known_score():
    result = score_phq9([1, 2, 0, 3, 1, 1, 0, 2, 0])
    assert result["score"] == 10
    assert result["band"] == "moderate"


def test_same_answers_same_result():
    answers = [2, 2, 2, 2, 2, 2, 2, 2, 2]
    assert score_phq9(answers) == score_phq9(answers)


def test_incomplete_answers():
    result = score_phq9([1, 2, 0])
    assert result["complete"] is False
    assert result["score"] is None


def test_out_of_range_answer():
    assert score_phq9([1, 2, 0, 3, 1, 1, 0, 2, 9])["complete"] is False


def test_phq9_boundaries():
    assert phq9_band(4) == "minimal"
    assert phq9_band(5) == "mild"
    assert phq9_band(14) == "moderate"
    assert phq9_band(15) == "moderately severe"
    assert phq9_band(20) == "severe"


def test_safety_flag():
    assert score_phq9([0, 0, 0, 0, 0, 0, 0, 0, 1])["safety_flag"] is True
    assert score_phq9([1, 0, 0, 0, 0, 0, 0, 0, 0])["safety_flag"] is False


def test_gad7_max():
    assert score_gad7([3] * 7)["score"] == 21


def test_levels():
    assert to_level(0.1) == "LOW"
    assert to_level(0.5) == "MODERATE"
    assert to_level(0.9) == "HIGH"
    assert to_level(None) is None