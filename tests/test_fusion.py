from backend.questionnaire import (
    score_phq9, score_gad7, score_stress, score_skin_impact
)
from backend.fusion import build_facts, integrated_score, analyze, WEIGHTS


def parts(phq=None, gad=None, stress=None, skin=None):
    return (
        score_phq9(phq if phq is not None else [0] * 9),
        score_gad7(gad if gad is not None else [0] * 7),
        score_stress(stress if stress is not None else [0] * 4),
        score_skin_impact(skin if skin is not None else [0] * 3 + [0]),
    )


IMG_HIGH = {"valid": True, "psoriasis_probability": 0.90}
TEXT_HIGH = {"provided": True, "valid": True,
             "distress_score": 0.80, "text_distress": "ELEVATED"}


def test_weights_add_up_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_case_a_everything_low():
    result = analyze(*parts())
    assert result["fired"] == []
    assert result["facts"]["stress_level"] == "LOW"


def test_case_b_high_stress_high_impact():
    result = analyze(*parts(stress=[4, 4, 4, 4], skin=[3, 3, 3, 3]))
    assert result["facts"]["integrated_impact"] == "ELEVATED"


def test_case_c_image_only_no_psych_conclusion():
    result = analyze(*parts(phq=[1] * 3, gad=None), image=IMG_HIGH)
    assert result["facts"]["skin_indicator"] == "SIGNIFICANT"
    assert "integrated_impact" not in result["facts"]
    assert "emotional_distress_indicator" not in result["facts"]


def test_case_d_high_stress_and_distress_text():
    result = analyze(*parts(stress=[4, 4, 4, 4]), text=TEXT_HIGH)
    assert result["facts"]["emotional_distress_indicator"] == "ELEVATED"


def test_case_e_missing_questionnaire():
    result = analyze(*parts(phq=[1, 2]))
    assert result["facts"]["psychological_result"] == "INSUFFICIENT_DATA"
    assert "integrated_impact" not in result["facts"]


def test_case_f_invalid_image_gives_no_skin_fact():
    facts = build_facts(*parts(), image={"valid": False, "error": "bad"})
    assert "skin_probability" not in facts


def test_chain_to_psychosocial_interaction():
    result = analyze(*parts(stress=[4, 4, 4, 4]), image=IMG_HIGH, text=TEXT_HIGH)
    assert result["facts"]["psychosocial_interaction"] == "POSSIBLE"


def test_text_missing_does_not_break():
    facts = build_facts(*parts(stress=[4, 4, 4, 4]), text={"provided": False, "valid": True})
    assert "text_distress" not in facts


def test_safety_flag_fires_support_message():
    result = analyze(*parts(phq=[0] * 8 + [1]))
    assert result["facts"]["show_support_message"] is True


def test_integrated_score_questionnaire_only():
    score = integrated_score(*parts(stress=[4, 4, 4, 4]))
    assert 0.0 < score < 1.0


def test_integrated_score_none_when_nothing():
    assert integrated_score(*parts(phq=[1])) is None