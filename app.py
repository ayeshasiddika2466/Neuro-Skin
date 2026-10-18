# app.py
# Only connects the backend and the frontend.

import streamlit as st

from backend.questionnaire import (
    score_phq9, score_gad7, score_stress, score_skin_impact
)
from backend.vision import predict_image
from backend.nlp import predict_text
from backend.fusion import analyze
from frontend import components as ui

st.set_page_config(page_title="NeuroSkin", page_icon="🧠")
st.title("NeuroSkin")
st.caption("A multimodal AI and expert-system screening prototype")
ui.disclaimer()

with st.form("neuroskin"):
    st.header("1. Questionnaire")
    st.write("Over the last 2 weeks, how often have you been bothered by the following problems?")
    phq_a = ui.ask("phq", ui.PHQ9, ui.LABELS_4)
    st.write("Still over the last 2 weeks:")
    gad_a = ui.ask("gad", ui.GAD7, ui.LABELS_4)
    st.write("In the last 2 weeks, how often did you feel this way?")
    stress_a = ui.ask("stress", ui.STRESS, ui.LABELS_STRESS)
    st.write("In the last 2 weeks, how much did your skin affect you?")
    skin_a = ui.ask("skin", ui.SKIN, ui.LABELS_SKIN)

    st.header("2. Skin image")
    upload = st.file_uploader("Upload a skin photo (jpg or png)", type=["jpg", "jpeg", "png"])

    st.header("3. Journal (optional)")
    journal = st.text_area("Write a few sentences about how you feel.", max_chars=1000)

    submitted = st.form_submit_button("Analyse")

if submitted:
    phq9 = score_phq9(phq_a)
    gad7 = score_gad7(gad_a)
    stress = score_stress(stress_a)
    skin = score_skin_impact(skin_a)

    image = None
    if upload is not None:
        with st.spinner("Reading the image..."):
            image = predict_image(upload.getvalue())

    text = predict_text(journal)
    result = analyze(phq9, gad7, stress, skin, image, text)

    st.divider()
    st.header("Results")

    item9 = phq_a[8]
    if result["facts"].get("show_support_message") or (item9 is not None and item9 > 0):
        ui.support_message()

    ui.show_questionnaire(phq9, gad7, stress, skin)
    ui.show_image(image)
    ui.show_text(text)
    ui.show_expert(result)
    ui.show_limits()