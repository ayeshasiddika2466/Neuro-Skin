PHQ9_MAX = 27
GAD7_MAX = 21
STRESS_MAX = 16
SKIN_IMPACT_MAX = 12


def is_valid(answers, count, max_value):
    """True only if answers is a full list of whole numbers in range."""
    if answers is None:
        return False
    if len(answers) != count:
        return False
    for a in answers:
        if not isinstance(a, int):
            return False
        if a < 0 or a > max_value:
            return False
    return True


def phq9_band(score):
    if score <= 4:
        return "minimal"
    elif score <= 9:
        return "mild"
    elif score <= 14:
        return "moderate"
    elif score <= 19:
        return "moderately severe"
    else:
        return "severe"


def gad7_band(score):
    if score <= 4:
        return "minimal"
    elif score <= 9:
        return "mild"
    elif score <= 14:
        return "moderate"
    else:
        return "severe"


def to_level(normalized):
    """Turn a 0-1 number into LOW / MODERATE / HIGH for the expert system."""
    if normalized is None:
        return None
    if normalized < 0.34:
        return "LOW"
    elif normalized < 0.67:
        return "MODERATE"
    else:
        return "HIGH"


def incomplete_result():
    return {"complete": False, "score": None, "band": None,
            "normalized": None, "level": None}


def score_phq9(answers):
    if not is_valid(answers, 9, 3):
        return incomplete_result()
    score = sum(answers)
    normalized = score / PHQ9_MAX
    return {
        "complete": True,
        "score": score,
        "band": phq9_band(score),
        "normalized": normalized,
        "level": to_level(normalized),
        "safety_flag": answers[8] > 0,   # item 9: thoughts of self-harm
    }


def score_gad7(answers):
    if not is_valid(answers, 7, 3):
        return incomplete_result()
    score = sum(answers)
    normalized = score / GAD7_MAX
    return {
        "complete": True,
        "score": score,
        "band": gad7_band(score),
        "normalized": normalized,
        "level": to_level(normalized),
    }


def score_stress(answers):
    if not is_valid(answers, 4, 4):
        return incomplete_result()
    score = sum(answers)
    normalized = score / STRESS_MAX
    return {"complete": True, "score": score, "band": None,
            "normalized": normalized, "level": to_level(normalized)}


def score_skin_impact(answers):
    if not is_valid(answers, 4, 3):
        return incomplete_result()
    score = sum(answers)
    normalized = score / SKIN_IMPACT_MAX
    return {"complete": True, "score": score, "band": None,
            "normalized": normalized, "level": to_level(normalized)}