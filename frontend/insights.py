# frontend/insights.py
# "Your Combined Insights". It only shows results.
# Every sentence is built from the real scores, model outputs and rule results.

import html

import streamlit as st

from backend.questionnaire import PHQ9_MAX, GAD7_MAX, STRESS_MAX
from frontend import components as ui
from frontend import crawler, flow, theme

LEVEL_WORDS = {"LOW": "low", "MODERATE": "moderate", "HIGH": "high"}

FACT_NAMES = {
    "stress_level": "Stress level",
    "quality_of_life_impact": "Skin impact",
    "skin_probability": "Skin model score",
    "text_distress": "Emotional language indicator",
    "skin_indicator": "Skin indicator (from rule R2)",
    "emotional_distress_indicator": "Emotional distress indicator (from rule R3)",
    "questionnaire_incomplete": "Questionnaire incomplete",
    "safety_flag": "PHQ-9 item 9 above zero",
}
RULE_INPUTS = {
    "R1": ["stress_level", "quality_of_life_impact"],
    "R2": ["skin_probability"],
    "R3": ["stress_level", "text_distress"],
    "R4": ["skin_indicator", "emotional_distress_indicator"],
    "R5": ["questionnaire_incomplete"],
    "R6": ["safety_flag"],
}
RULE_NOTES = {"R2": "The threshold is 0.70. It is a documented choice, not tuned to look good."}


# ---------- sentences (pure functions, easy to test) ----------
def skin_headline(image):
    if image is None or not image.get("valid"):
        return None
    return f"The image most closely matches {image['label'].lower()}."


def emotional_sentences(phq9, gad7, stress, skin):
    out, found = [], []
    if phq9["complete"]:
        found.append(f"{phq9['band']} depression symptoms (PHQ-9: {phq9['score']} of {PHQ9_MAX})")
    if gad7["complete"]:
        found.append(f"{gad7['band']} anxiety symptoms (GAD-7: {gad7['score']} of {GAD7_MAX})")
    if found:
        out.append("Your responses indicate " + " and ".join(found) + ".")
    missing = [n for n, r in (("PHQ-9", phq9), ("GAD-7", gad7)) if not r["complete"]]
    if missing:
        out.append("The " + " and ".join(missing) +
                   " could not be scored because some questions were skipped.")
    if stress["complete"]:
        out.append(f"You reported {LEVEL_WORDS[stress['level']]} stress.")
    if skin["complete"]:
        out.append({
            "HIGH": "You reported that psoriasis affects you significantly.",
            "MODERATE": "You reported that psoriasis affects you moderately.",
            "LOW": "You reported that psoriasis affects you only a little.",
        }[skin["level"]])
    return out


def reflection_headline(text):
    if text.get("text_distress") == "ELEVATED":
        return "Your writing contains signs of emotional distress."
    return "Your writing does not show strong signs of emotional distress."


def _fact_text(name, value):
    label = FACT_NAMES.get(name, name)
    if isinstance(value, bool):
        return f"{label}: {'yes' if value else 'no'}"
    if isinstance(value, float):
        return f"{label}: {value:.2f}"
    return f"{label}: {value}"


def _stat(label, r, note_if_done):
    score = r["score"] if r["complete"] else "—"
    note = note_if_done if r["complete"] else "skipped"
    return (f'<div class="ns-stat"><div class="ns-stat-label">{html.escape(label)}</div>'
            f'<div class="ns-stat-value">{score}</div>'
            f'<div class="ns-stat-note">{html.escape(str(note))}</div></div>')


def _kicker(text):
    st.markdown(f'<div class="ns-kicker">{html.escape(text)}</div>', unsafe_allow_html=True)


# ---------- cards ----------
def _skin_card(image):
    with st.container(border=True):
        _kicker("Skin")
        if image is None:
            st.write("No photo was added, so there is no skin result.")
            return
        if not image.get("valid"):
            st.error(image["error"])
            st.write("You can choose a different photo above and analyse again.")
            return
        st.markdown(f'<div class="ns-result-line">{html.escape(skin_headline(image))}</div>',
                    unsafe_allow_html=True)
        st.caption("Skin Image Assessment · Model prediction")
        if image["label"] == "PSORIASIS":
            st.write("The image model detected patterns associated with psoriasis.")
        st.write(f"Model score for this match: **{image['confidence']:.0%}**")
        for name, p in image["probabilities"].items():
            st.progress(p, text=f"{name.capitalize()}: {p:.0%}")
        st.caption("The three scores add up to 100% across the options the model knows. "
                   "A high score is not the chance that you have the condition.")
        st.caption("These scores reflect the model's predictions, not diagnostic certainty. "
                   "A dermatologist can assess your skin more reliably.")


def _emotional_card(phq9, gad7, stress, skin):
    with st.container(border=True):
        _kicker("Emotional wellbeing")
        for line in emotional_sentences(phq9, gad7, stress, skin):
            st.write(line)
        cols = st.columns(4)
        cols[0].markdown(_stat("PHQ-9", phq9, phq9["band"]), unsafe_allow_html=True)
        cols[1].markdown(_stat("GAD-7", gad7, gad7["band"]), unsafe_allow_html=True)
        cols[2].markdown(_stat("Stress", stress, LEVEL_WORDS.get(stress["level"], "")),
                         unsafe_allow_html=True)
        cols[3].markdown(_stat("Skin impact", skin, LEVEL_WORDS.get(skin["level"], "")),
                         unsafe_allow_html=True)
        st.caption("PHQ-9 and GAD-7 are screening questionnaires, not diagnoses. "
                   "The stress and skin impact questions were written for this project "
                   "and are not validated.")


def _reflection_card(text):
    with st.container(border=True):
        _kicker("Your reflection")
        st.subheader("Your Journal Reflection")
        st.caption("Emotional language indicator · prototype model")
        st.markdown(f'<div class="ns-result-line">{html.escape(reflection_headline(text))}</div>',
                    unsafe_allow_html=True)
        st.write(f"Indicator score: **{text['distress_score']:.0%}**")
        st.caption("The wording above is shown when the score is 60% or higher. "
                   "That cut-off is a simple documented choice. The model was trained on short "
                   "social-media posts.")
        st.caption("This score reflects patterns in the words you used. It cannot determine "
                   "exactly how you feel or diagnose a mental health condition.")


def _connection_card(pattern_found):
    with st.container(border=True):
        _kicker("Possible connection")
        st.write("Skin concerns and emotional wellbeing may influence each other, but these "
                 "results cannot establish a cause-and-effect relationship.")
        if pattern_found:
            st.write("These results show a possible pattern, not a proven connection.")


def _combined_card(result):
    score = result["integrated_score"]
    with st.container(border=True):
        _kicker("Experimental combined indicator")
        if score is None:
            st.write("There was not enough information to form a combined indicator.")
        else:
            st.markdown(f'<div class="ns-result-line">{score:.2f} <span class="ns-note">out of 1</span></div>',
                        unsafe_allow_html=True)
            if result["input_facts"].get("questionnaire_incomplete"):
                st.caption("The questionnaire was incomplete, so this uses only the photo and/or journal.")
        st.caption("An exploratory summary of the available indicators. This score has not been "
                   "clinically validated and should not be interpreted as a diagnosis or a "
                   "measure of disease severity.")


# ---------- the four expandable sections ----------
def _how_we_reached(result):
    with st.expander("How we reached these insights"):
        st.write("Every insight on this page comes from a written rule or a model output. "
                 "Nothing is hidden.")
        facts = result["facts"]
        if not result["trace"]:
            st.write("No rule found an elevated indicator. That is a result too.")
        for step in result["trace"]:
            st.markdown(f"**{step['rule']}**. {step['text']}")
            used = [_fact_text(n, facts[n]) for n in RULE_INPUTS.get(step["rule"], []) if n in facts]
            if used:
                st.caption("Based on: " + " · ".join(used))
            if step["rule"] in RULE_NOTES:
                st.caption(RULE_NOTES[step["rule"]])
        st.markdown("**Where the inputs come from**")
        st.write("- Questionnaires: PHQ-9 and GAD-7 are scored with their published severity bands.\n"
                 "- Skin photo: a small image model fine-tuned on one public dataset "
                 "(psoriasis, lichen planus and normal skin).\n"
                 "- Journal: a small word-pattern model trained on short social-media posts.")


def _what_it_means():
    with st.expander("What these results mean"):
        st.write(
            "- These are screening results, not a diagnosis. Only a qualified professional can diagnose.\n"
            "- The image model was checked on 663 held-out photos from one public dataset "
            "(95.3% correct). Real photos can look different, and logos, watermarks, lighting "
            "and skin tone can change its answer.\n"
            "- A model score is not the chance that you have a condition.\n"
            "- The journal model reads emotional wording only. Negative words do not always "
            "mean distress.\n"
            "- The stress and skin impact questions are not validated, and the combined "
            "indicator is experimental.\n"
            "- Seeing a pattern between skin and mood does not show that one causes the other.")


def _next_steps(phq9, gad7, flagged):
    with st.expander("What you can do next"):
        st.write("- A dermatologist or your doctor can assess your skin properly. It is worth a visit "
                 "if your skin is changing, painful, spreading, or affecting your daily life.")
        moderate_up = ((phq9["complete"] and phq9["score"] >= 10) or
                       (gad7["complete"] and gad7["score"] >= 10))
        if moderate_up:
            st.write("- Scores at this level are usually a good reason to speak with a doctor or a "
                     "mental health professional. You can bring this page with you if it helps.")
        else:
            st.write("- If you start to feel worse, or things do not improve, it is okay to reach "
                     "out to a doctor or someone you trust at any time.")
        if flagged:
            st.write("- You indicated thoughts of hurting yourself. Please contact your local "
                     "emergency services or a person you trust right now.")
        st.write("- Small steps can help, such as regular sleep, time outside, and talking to "
                 "someone you trust. You can return to this check-in whenever you like.")
        st.caption("NeuroSkin does not replace medical care.")


def _review(journal, word_weights):
    with st.expander("Review my responses"):
        answers = st.session_state.get("answers", [])
        paras = []
        for k, q in enumerate(flow.QUESTIONS):
            a = answers[k] if k < len(answers) else None
            if a is not None:
                paras.append({"kind": "answer", "text": f"{k + 1}. {q['text']} — {q['labels'][a]}"})
        if journal and journal.strip():
            paras.append({"kind": "journal", "text": journal.strip()})
        st.write("Here are your responses. The neuron moves across your own words. It starts "
                 "by itself, follows your cursor a little, and you can stop it any time.")
        crawler.show(paras, word_weights)
        st.caption("This is a way to look at your words, not an analysis. The neuron cannot "
                   "read how you feel. Your words stay in this browser and are not sent anywhere.")
        if word_weights:
            st.caption("Amber underlined words pushed the journal indicator up, according to the model.")


# ---------- the page ----------
def show(result, phq_a, phq9, gad7, stress, skin, image, text, journal="", word_weights=None):
    facts = result["facts"]
    item9 = phq_a[8] if len(phq_a) > 8 else None
    flagged = bool(facts.get("show_support_message") or (item9 is not None and item9 > 0))

    st.divider()
    if flagged:
        ui.support_message()

    theme.section("04", "Your Combined Insights")
    st.write("Your responses and assessments highlight a few areas worth paying attention to.")

    left, right = st.columns(2, gap="large")
    with left:
        _skin_card(image)
    with right:
        _emotional_card(phq9, gad7, stress, skin)

    has_reflection = bool(text and text.get("provided") and text.get("valid"))
    has_skin = bool(image and image.get("valid"))
    has_emotion = phq9["complete"] or gad7["complete"] or stress["complete"] or has_reflection
    pattern = facts.get("psychosocial_interaction") == "POSSIBLE"

    if has_reflection and has_skin and has_emotion:
        a, b = st.columns(2, gap="large")
        with a:
            _reflection_card(text)
        with b:
            _connection_card(pattern)
    else:
        if has_reflection:
            _reflection_card(text)
        elif text and text.get("provided") and not text.get("valid"):
            st.warning(text.get("error", "The journal could not be read."))
        if has_skin and has_emotion:
            _connection_card(pattern)

    _combined_card(result)

    _how_we_reached(result)
    _what_it_means()
    _next_steps(phq9, gad7, flagged)
    _review(journal, word_weights)