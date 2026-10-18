# backend/fusion.py
# Puts all results into one facts dictionary and runs the expert system.
# No Streamlit, no drawing.

from backend.expert import run_rules
from backend.questionnaire import to_level

# Documented weights, they add up to 1 (Section 10.2 of the proposal).
WEIGHTS = {"questionnaire": 0.5, "image": 0.3, "text": 0.2}


def _image_ok(image):
    return bool(image) and image.get("valid") is True


def _text_ok(text):
    return bool(text) and text.get("provided") is True and text.get("valid") is True


def build_facts(phq9, gad7, stress, skin_impact, image=None, text=None):
    """Turns the module results into the facts the rules read."""
    facts = {}

    parts = [phq9, gad7, stress, skin_impact]
    if all(p["complete"] for p in parts):
        facts["depression_level"] = phq9["level"]
        facts["anxiety_level"] = gad7["level"]
        facts["stress_level"] = stress["level"]
        facts["quality_of_life_impact"] = skin_impact["level"]
        facts["safety_flag"] = phq9["safety_flag"]
    else:
        facts["questionnaire_incomplete"] = True

    if _image_ok(image):
        facts["skin_probability"] = image["psoriasis_probability"]

    if _text_ok(text):
        facts["text_distress"] = text["text_distress"]

    return facts


def integrated_score(phq9, gad7, stress, skin_impact, image=None, text=None):
    """Weighted average of the parts that are available. None if nothing is."""
    available = {}

    parts = [phq9, gad7, stress, skin_impact]
    if all(p["complete"] for p in parts):
        available["questionnaire"] = sum(p["normalized"] for p in parts) / 4
    if _image_ok(image):
        available["image"] = image["psoriasis_probability"]
    if _text_ok(text):
        available["text"] = text["distress_score"]

    if not available:
        return None
    total_weight = sum(WEIGHTS[k] for k in available)
    return sum(WEIGHTS[k] * v for k, v in available.items()) / total_weight


def analyze(phq9, gad7, stress, skin_impact, image=None, text=None):
    facts = build_facts(phq9, gad7, stress, skin_impact, image, text)
    result = run_rules(facts)
    score = integrated_score(phq9, gad7, stress, skin_impact, image, text)
    return {
        "input_facts": facts,
        "facts": result["facts"],
        "fired": result["fired"],
        "trace": result["trace"],
        "integrated_score": score,
        "integrated_level": to_level(score),
    }