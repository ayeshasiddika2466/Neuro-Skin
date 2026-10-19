# app.py
# Only connects the backend and the frontend.

import streamlit as st

from backend.questionnaire import (
    score_phq9, score_gad7, score_stress, score_skin_impact
)
from backend.vision import predict_image
from backend.nlp import predict_text
from backend.fusion import analyze

try:                      # optional: word weights for the journal colouring
    from backend.nlp import explain_text
except ImportError:
    explain_text = None
from frontend import components as ui
from frontend import flow, insights, shell, theme

st.set_page_config(page_title="NeuroSkin", page_icon="🌿", layout="wide")
theme.apply()
shell.init()


def show_results(phq_a, phq9, gad7, stress, skin, image, text, journal="", word_weights=None):
    result = analyze(phq9, gad7, stress, skin, image, text)
    insights.show(result, phq_a, phq9, gad7, stress, skin, image, text, journal, word_weights)


def skin_upload():
    st.write("Choose a photo of the area you would like to check.")
    upload = st.file_uploader("Skin photo", type=["jpg", "jpeg", "png"], key="upload",
                              label_visibility="collapsed")
    st.markdown('<div class="ns-note">JPG or PNG, up to 50 MB. NeuroSkin does not save your photo. '
                'Use the x to remove it, or choose another to replace it.</div>',
                unsafe_allow_html=True)
    if upload is not None:
        st.image(upload, caption="Your selected photo", width="stretch")
    return upload


def journal_box():
    st.write("Entirely optional. Only write if it feels helpful.")
    st.caption("A gentle prompt: what has been on your mind about your skin or your mood lately?")
    journal = st.text_area("Your journal", key="journal", max_chars=1000, height=170,
                           label_visibility="collapsed",
                           placeholder="Write whatever is on your mind, or leave this empty.")
    st.markdown('<div class="ns-note">A small model reads your words on this computer. '
                'NeuroSkin does not store them. They are kept only while this page is open, '
                'and Quick exit clears them. You can edit your words until you press Analyse.</div>',
                unsafe_allow_html=True)
    return journal


def run_analysis(upload, journal):
    phq_a, gad_a, stress_a, skin_a = flow.collected()
    phq9 = score_phq9(phq_a)
    gad7 = score_gad7(gad_a)
    stress = score_stress(stress_a)
    skin = score_skin_impact(skin_a)

    image = None
    if upload is not None:
        try:
            image = predict_image(upload.getvalue())
        except FileNotFoundError:
            image = {"valid": False,
                     "error": "The image model file is missing on this computer."}

    try:
        text = predict_text(journal)
    except FileNotFoundError:
        text = {"provided": True, "valid": False,
                "error": "The text model file is missing on this computer.",
                "distress_score": None, "text_distress": None}

    weights = None
    if explain_text is not None and text.get("provided") and text.get("valid"):
        try:
            weights = explain_text(journal)
        except Exception:
            weights = None          # the words simply stay uncoloured

    st.session_state.result = dict(phq_a=phq_a, phq9=phq9, gad7=gad7, stress=stress,
                                   skin=skin, image=image, text=text,
                                   journal=journal or "", word_weights=weights)


def assessment():
    flow.init()
    shell.background_video(dim=True)

    top_left, top_right = st.columns([3, 1])
    with top_left:
        theme.brand()
    with top_right:
        shell.exit_button()
    ui.disclaimer()

    left, right = st.columns([1.2, 1], gap="large")
    with left:
        theme.section("01", "How have you been feeling?")
        flow.question_card()
        flow.review()
    with right:
        theme.section("02", "Your skin")
        upload = skin_upload()
        theme.section("03", "Your journal")
        journal = journal_box()

    st.divider()
    skipped = flow.unanswered_count()
    if skipped:
        st.caption(f"{skipped} question(s) not answered yet. You can still analyse what you have shared.")
    nothing_yet = (skipped == flow.TOTAL and upload is None and not (journal or "").strip())
    if st.button("Analyse my check-in", type="primary", key="analyse"):
        if nothing_yet:
            st.info("There is nothing to analyse yet. Answer a question, add a photo, or write "
                    "a few words, then try again.")
        else:
            with st.spinner("Reading your responses..."):
                run_analysis(upload, journal)

    if "result" in st.session_state:
        show_results(**st.session_state.result)


step = st.session_state.step
if step == "welcome":
    shell.welcome()
elif step == "later":
    shell.later()
else:
    assessment()