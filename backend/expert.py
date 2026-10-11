SKIN_PROBABILITY_THRESHOLD = 0.70   # from Section 9.1, rule R2


# Each rule has: an id, a plain-English text, a condition, and the facts it adds.
# "condition" is a small function: it receives the facts and returns True or False.
RULES = [
    {
        "id": "R1",
        "text": "High stress and high skin quality-of-life impact -> elevated integrated impact",
           "condition": lambda f: f.get("stress_level") == "HIGH"
                          and f.get("quality_of_life_impact") == "HIGH"
                          and f.get("questionnaire_incomplete") is not True,
        "then": {"integrated_impact": "ELEVATED"},
    },
    {
        "id": "R2",
        "text": "Skin model probability is at or above the threshold -> significant skin indicator",
        "condition": lambda f: f.get("skin_probability") is not None
                               and f["skin_probability"] >= SKIN_PROBABILITY_THRESHOLD,
        "then": {"skin_indicator": "SIGNIFICANT"},
    },
    {
        "id": "R3",
        "text": "High stress and elevated distress language -> elevated emotional distress indicator",
        "condition": lambda f: f.get("stress_level") == "HIGH"
                               and f.get("text_distress") == "ELEVATED",
        "then": {"emotional_distress_indicator": "ELEVATED"},
    },
    {
        "id": "R4",
        "text": "Significant skin indicator and elevated emotional distress -> possible psychosocial interaction",
        "condition": lambda f: f.get("skin_indicator") == "SIGNIFICANT"
                               and f.get("emotional_distress_indicator") == "ELEVATED",
        "then": {"psychosocial_interaction": "POSSIBLE"},
    },
    {
        "id": "R5",
        "text": "Questionnaire incomplete -> psychological result has insufficient data",
        "condition": lambda f: f.get("questionnaire_incomplete") is True,
        "then": {"psychological_result": "INSUFFICIENT_DATA"},
    },
    {
        "id": "R6",
        "text": "Item 9 of PHQ-9 above zero -> show a support message",
        "condition": lambda f: f.get("safety_flag") is True,
        "then": {"show_support_message": True},
    },
]


def run_rules(initial_facts):
    """Forward chaining. Returns the final facts and a trace of fired rules."""
    facts = dict(initial_facts)      # copy, so the caller's dictionary is not changed
    fired = []                       # rule ids that have already fired
    trace = []                       # readable explanation of each firing

    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if rule["id"] in fired:
                continue                         # each rule fires at most once
            if rule["condition"](facts):
                facts.update(rule["then"])       # add the new facts
                fired.append(rule["id"])
                trace.append({"rule": rule["id"], "text": rule["text"],
                              "added": rule["then"]})
                changed = True                   # something new -> go round again

    return {"facts": facts, "fired": fired, "trace": trace}