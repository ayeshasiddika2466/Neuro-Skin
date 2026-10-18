# frontend/components.py
# Only shows things. It does not calculate scores.

import streamlit as st

LABELS_4 = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
LABELS_STRESS = ["Never", "Rarely", "Sometimes", "Often", "Very often"]
LABELS_SKIN = ["Not at all", "A little", "A lot", "Very much"]

PHQ9 = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself, or that you are a failure or have let yourself or your family down",
    "Trouble concentrating on things, such as reading or watching television",
    "Moving or speaking so slowly that other people could have noticed, or the opposite: being so fidgety or restless that you have been moving around a lot more than usual",
    "Thoughts that you would be better off dead, or of hurting yourself in some way",
]
GAD7 = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid, as if something awful might happen",
]
STRESS = [
    "I felt that I could not control the important things in my life.",
    "I felt under too much pressure.",
    "I felt that problems were piling up and I could not deal with them.",
    "I felt tense or on edge because of daily demands.",
]
SKIN = [
    "My skin made me feel embarrassed or self-conscious.",
    "My skin made daily activities (work, study, housework) harder.",
    "My skin affected my choice of clothes or going out and meeting people.",
    "My skin itched, hurt or felt uncomfortable.",
]


def disclaimer():
    st.warning(
        "NeuroSkin is an educational course project. Its results are "
        "screening-oriented and are NOT a medical diagnosis. "
        "Please talk to a doctor about any health concern."
    )


def ask(prefix, questions, labels):
    """Shows radio buttons. Unanswered questions give None."""
    answers = []
    for i, q in enumerate(questions, 1):
        choice = st.radio(f"{i}. {q}", labels, index=None, key=f"{prefix}{i}")
        answers.append(None if choice is None else labels.index(choice))
    return answers


def support_message():
    st.info(
        "You answered that you may have had thoughts of hurting yourself. "
        "You are not alone. Please talk to someone you trust or a health "
        "professional soon. If you feel in danger, contact your local "
        "emergency services right now."
    )


def show_questionnaire(phq9, gad7, stress, skin):
    st.subheader("Questionnaire (screening scores)")
    cols = st.columns(4)
    items = [("PHQ-9", phq9), ("GAD-7", gad7), ("Stress", stress), ("Skin impact", skin)]
    for col, (name, r) in zip(cols, items):
        with col:
            if r["complete"]:
                col.metric(name, r["score"], r["band"] or r["level"])
            else:
                col.metric(name, "-", "incomplete")


def show_image(image):
    st.subheader("Skin image (model prediction)")
    if image is None:
        st.write("No image was uploaded.")
        return
    if not image["valid"]:
        st.error(image["error"])
        return
    st.write(f"Most likely class: **{image['label']}** "
             f"(model probability {image['confidence']:.0%})")
    for name, p in image["probabilities"].items():
        st.progress(p, text=f"{name}: {p:.0%}")
    st.caption("A model probability is not certainty and not a diagnosis.")


def show_text(text):
    st.subheader("Journal text (model indicator)")
    if not text["provided"]:
        st.write("No text was written. This part is optional.")
    elif not text["valid"]:
        st.warning(text["error"])
    else:
        st.write(f"Distress-language score: **{text['distress_score']:.0%}** "
                 f"({text['text_distress']})")
        st.caption("This is one weak signal from emotional wording only.")


def summary_lines(facts):
    lines = []
    if facts.get("psychological_result") == "INSUFFICIENT_DATA":
        lines.append("The questionnaire is incomplete, so no psychological result is given.")
    if facts.get("integrated_impact") == "ELEVATED":
        lines.append("High stress and high skin impact were both reported.")
    if facts.get("skin_indicator") == "SIGNIFICANT":
        lines.append("The image model gave a high psoriasis probability.")
    if facts.get("emotional_distress_indicator") == "ELEVATED":
        lines.append("High stress and distress wording in the text appear together.")
    if facts.get("psychosocial_interaction") == "POSSIBLE":
        lines.append("A skin indicator and emotional distress appear together. "
                     "A possible link is only a pattern, not a conclusion.")
    if not lines:
        lines.append("No rule found an elevated indicator.")
    return lines


def show_expert(result):
    st.subheader("Expert system (rule-based interpretation)")
    for line in summary_lines(result["facts"]):
        st.write("- " + line)

    score = result["integrated_score"]
    if score is not None:
        st.write(f"Integrated score (illustrative): **{score:.2f}** "
                 f"({result['integrated_level']})")
        st.caption("A weighted mix of the available parts. It is not validated.")

    with st.expander("Why? Rules that fired"):
        if not result["trace"]:
            st.write("No rule fired.")
        for step in result["trace"]:
            st.write(f"**{step['rule']}**: {step['text']}")
            st.caption(f"Added: {step['added']}")


def show_limits():
    with st.expander("Limitations"):
        st.write(
            "- Not a medical diagnosis and not clinically validated.\n"
            "- The image model was trained on one public dataset. Logos, "
            "watermarks, lighting and skin tone can affect it.\n"
            "- The text model reads emotional wording only.\n"
            "- The stress and skin-impact questions were written by the "
            "author and are not validated.\n"
            "- Uploaded images and text are not saved."
        )