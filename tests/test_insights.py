# Tests for the sentences on the results page (frontend/insights.py).
# Every sentence must match the real scores.

from backend.questionnaire import (
    score_phq9, score_gad7, score_stress, score_skin_impact
)
from frontend import insights


def parts(phq=None, gad=None, stress=None, skin=None):
    return (score_phq9(phq or [0] * 9), score_gad7(gad or [0] * 7),
            score_stress(stress or [0] * 4), score_skin_impact(skin or [0] * 4))


def test_severe_scores_are_named_with_their_real_numbers():
    s = insights.emotional_sentences(*parts(phq=[3] * 9, gad=[3] * 7))
    assert s[0] == ("Your responses indicate severe depression symptoms (PHQ-9: 27 of 27) "
                    "and severe anxiety symptoms (GAD-7: 21 of 21).")


def test_low_scores_are_not_called_elevated():
    text = " ".join(insights.emotional_sentences(*parts()))
    assert "minimal depression symptoms" in text
    assert "severe" not in text and "high" not in text


def test_skipped_questionnaire_is_never_scored():
    s = insights.emotional_sentences(*parts(phq=[1, 2]))
    text = " ".join(s)
    assert "The PHQ-9 could not be scored" in text
    assert "depression symptoms" not in text


def test_skin_impact_wording_follows_the_level():
    high = insights.emotional_sentences(*parts(skin=[3] * 4))
    low = insights.emotional_sentences(*parts(skin=[0] * 4))
    assert "affects you significantly" in " ".join(high)
    assert "affects you only a little" in " ".join(low)


def test_stress_level_word_matches():
    assert "You reported high stress." in insights.emotional_sentences(*parts(stress=[4] * 4))
    assert "You reported low stress." in insights.emotional_sentences(*parts())


def test_skin_headline_uses_the_models_real_label():
    assert insights.skin_headline({"valid": True, "label": "PSORIASIS"}) == \
        "The image most closely matches psoriasis."
    assert insights.skin_headline({"valid": True, "label": "NORMAL SKIN"}) == \
        "The image most closely matches normal skin."


def test_no_headline_when_the_image_failed_or_is_missing():
    assert insights.skin_headline(None) is None
    assert insights.skin_headline({"valid": False, "error": "bad"}) is None


def test_reflection_headline_follows_the_indicator():
    assert "signs of emotional distress" in insights.reflection_headline({"text_distress": "ELEVATED"})
    assert "does not show" in insights.reflection_headline({"text_distress": "NORMAL"})


def test_fact_text_formats_numbers_and_flags():
    assert insights._fact_text("skin_probability", 0.987) == "Skin model score: 0.99"
    assert insights._fact_text("safety_flag", True) == "PHQ-9 item 9 above zero: yes"