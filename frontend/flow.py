# frontend/flow.py
# One question at a time. Keeps the answers, shows progress, lets people go back.
# It stores answers but never calculates scores (the backend does that).

import html

import streamlit as st

from frontend import components as ui

GROUPS = [
    ("phq", "Mood (PHQ-9)",
     "Over the last 2 weeks, how often have you been bothered by the following problems?",
     ui.PHQ9, ui.LABELS_4),
    ("gad", "Worry (GAD-7)",
     "Over the last 2 weeks, how often have you been bothered by the following problems?",
     ui.GAD7, ui.LABELS_4),
    ("stress", "Stress",
     "In the last 2 weeks, how often did you feel this way?",
     ui.STRESS, ui.LABELS_STRESS),
    ("skin", "Your skin",
     "In the last 2 weeks, how much did your skin affect you?",
     ui.SKIN, ui.LABELS_SKIN),
]

QUESTIONS = []
OFFSETS = {}          # where each group starts in the flat list
for gid, title, intro, qs, labels in GROUPS:
    OFFSETS[gid] = (len(QUESTIONS), len(QUESTIONS) + len(qs))
    for n, text in enumerate(qs, 1):
        QUESTIONS.append({"title": title, "intro": intro, "text": text,
                          "labels": labels, "number": n, "of": len(qs)})

TOTAL = len(QUESTIONS)
SAFETY_INDEX = 8      # PHQ-9 item 9


def init():
    st.session_state.setdefault("answers", [None] * TOTAL)
    st.session_state.setdefault("qi", 0)


def collected():
    """Returns (phq answers, gad answers, stress answers, skin answers). None = unanswered."""
    a = st.session_state.answers
    return tuple(a[OFFSETS[g][0]:OFFSETS[g][1]] for g in ("phq", "gad", "stress", "skin"))


def unanswered_count():
    return sum(1 for a in st.session_state.answers if a is None)


# ---- button callbacks ----
def _pick(i):
    choice = st.session_state.get(f"qr{i}")
    if choice is None:
        return
    value = QUESTIONS[i]["labels"].index(choice)
    st.session_state.answers[i] = value
    st.session_state.pop("result", None)          # old results no longer match
    if i == SAFETY_INDEX and value > 0:
        return                                    # stay: show the support message first
    st.session_state.qi = min(i + 1, TOTAL)


def _back():
    st.session_state.qi = max(st.session_state.qi - 1, 0)


def _next():
    st.session_state.qi = min(st.session_state.qi + 1, TOTAL)


def _goto(i):
    st.session_state.qi = i


# ---- what the person sees ----
def question_card():
    i = st.session_state.qi
    answers = st.session_state.answers
    answered = TOTAL - unanswered_count()

    if i < TOTAL:
        st.progress(i / TOTAL, text=f"Question {i + 1} of {TOTAL}  ·  {answered} answered")
        q = QUESTIONS[i]
        with st.container(key=f"question_card_{i}"):
            st.markdown(
                f'<div class="ns-kicker">{html.escape(q["title"])} · {q["number"]} of {q["of"]}</div>',
                unsafe_allow_html=True)
            st.caption(q["intro"])
            st.markdown(f'<div class="ns-q-text">{html.escape(q["text"])}</div>',
                        unsafe_allow_html=True)
            st.radio(q["text"], q["labels"], index=answers[i], key=f"qr{i}",
                     on_change=_pick, args=(i,), label_visibility="collapsed")

            if i == SAFETY_INDEX and answers[i] is not None and answers[i] > 0:
                ui.support_message()
                st.button("Continue", key="continue9", type="primary", on_click=_next)

            back, nxt, _ = st.columns([1, 1.7, 1.3])
            back.button("Back", key=f"back{i}", on_click=_back, disabled=(i == 0))
            nxt.button("Next" if answers[i] is not None else "Skip for now",
                       key=f"next{i}", on_click=_next)
    else:
        st.progress(1.0, text="All questions seen")
        with st.container(key="question_card_done"):
            st.markdown('<div class="ns-kicker">Questionnaire</div>'
                        '<div class="ns-q-text">Thank you for taking your time.</div>',
                        unsafe_allow_html=True)
            if unanswered_count():
                st.write(f"{unanswered_count()} question(s) were skipped. "
                         "You can go back and answer them, or continue as you are.")
            else:
                st.write("You answered every question. You can still change any answer below.")
            st.button("Back", key="back_done", on_click=_back)


def review():
    with st.expander("Change an answer"):
        for k, q in enumerate(QUESTIONS):
            a = st.session_state.answers[k]
            label = "Not answered" if a is None else q["labels"][a]
            text_col, button_col = st.columns([5, 1])
            text_col.markdown(f"**{k + 1}.** {q['text']}  \n*{label}*")
            button_col.button("Change", key=f"chg{k}", on_click=_goto, args=(k,))