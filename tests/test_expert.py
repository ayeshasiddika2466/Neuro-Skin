from backend.expert import run_rules


def test_case_a_low_everything():
    result = run_rules({"stress_level": "LOW", "skin_probability": 0.10})
    assert result["fired"] == []


def test_case_b_high_stress_high_impact():
    result = run_rules({"stress_level": "HIGH", "quality_of_life_impact": "HIGH"})
    assert result["facts"]["integrated_impact"] == "ELEVATED"
    assert "R1" in result["fired"]


def test_case_c_skin_only_no_psych_conclusion():
    result = run_rules({"skin_probability": 0.90})
    assert result["facts"]["skin_indicator"] == "SIGNIFICANT"
    assert "integrated_impact" not in result["facts"]
    assert "emotional_distress_indicator" not in result["facts"]


def test_case_d_high_stress_and_distress_text():
    result = run_rules({"stress_level": "HIGH", "text_distress": "ELEVATED"})
    assert result["facts"]["emotional_distress_indicator"] == "ELEVATED"


def test_case_e_incomplete_questionnaire():
    result = run_rules({"questionnaire_incomplete": True})
    assert result["facts"]["psychological_result"] == "INSUFFICIENT_DATA"


def test_chaining_r4_needs_r2_and_r3():
    result = run_rules({"stress_level": "HIGH", "text_distress": "ELEVATED",
                        "skin_probability": 0.87})
    assert result["facts"]["psychosocial_interaction"] == "POSSIBLE"
    assert result["fired"].index("R4") > result["fired"].index("R2")


def test_one_antecedent_missing():
    result = run_rules({"skin_probability": 0.87, "stress_level": "HIGH"})
    assert "R4" not in result["fired"]


def test_boundary_threshold():
    assert "R2" in run_rules({"skin_probability": 0.70})["fired"]
    assert "R2" not in run_rules({"skin_probability": 0.69})["fired"]


def test_optional_text_absent():
    result = run_rules({"stress_level": "HIGH"})
    assert "R3" not in result["fired"]


def test_input_not_changed():
    original = {"stress_level": "HIGH", "quality_of_life_impact": "HIGH"}
    run_rules(original)
    assert original == {"stress_level": "HIGH", "quality_of_life_impact": "HIGH"}


def test_safety_flag_rule():
    assert "R6" in run_rules({"safety_flag": True})["fired"]
    assert "R6" not in run_rules({"safety_flag": False})["fired"]

def test_conflict_high_stress_but_incomplete():
    result = run_rules({"stress_level": "HIGH", "questionnaire_incomplete": True})
    assert result["fired"] == ["R5"]
    assert result["facts"]["psychological_result"] == "INSUFFICIENT_DATA"
    assert "integrated_impact" not in result["facts"]

def test_incomplete_blocks_r1():
       result = run_rules({"stress_level": "HIGH", "quality_of_life_impact": "HIGH",
                           "questionnaire_incomplete": True})
       assert "R1" not in result["fired"]    