# frontend/shell.py
# Page flow: welcome, "maybe later", and the quick exit button.
# Only moves the user between pages. No scoring here.

import os

import streamlit as st

VIDEO_FILE = os.path.join("static", "welcome.mp4")


def init():
    if "step" not in st.session_state:
        st.session_state.step = "welcome"


def _go(step):
    st.session_state.step = step


def _quick_exit():
    """Clears everything the person entered and returns to the welcome page."""
    for key in list(st.session_state.keys()):
        if key != "step":
            del st.session_state[key]
    st.session_state.step = "welcome"


def exit_button():
    st.button(
        "Quick exit",
        key="exit",
        on_click=_quick_exit,
        icon=":material/logout:",
        help="Leaves the check-in, clears what you entered, and returns to the welcome page.",
    )


def background_video(dim=False):
    """Uses static/welcome.mp4 only if the file really exists. Otherwise the CSS sky stays.
    dim=True is for pages with a lot of text: the video is darker and quieter."""
    if os.path.exists(VIDEO_FILE):
        cls = " dim" if dim else ""
        st.markdown(
            f'<video class="ns-video{cls}" autoplay muted loop playsinline preload="auto" '
            'aria-hidden="true" tabindex="-1" disablepictureinpicture '
            'src="/app/static/welcome.mp4"></video>'
            f'<div class="ns-video-veil{cls}"></div>',
            unsafe_allow_html=True,
        )


_background_video = background_video


def welcome():
    _background_video()
    st.markdown(
        '<div class="ns-preloader" aria-hidden="true"><span>NeuroSkin</span></div>'
        '<div class="ns-topbar"><span class="ns-wordmark">Neuro<em>Skin</em></span>'
        '<span class="ns-meta">Educational prototype · not a medical service</span></div>'
        '<div class="ns-marquee" aria-hidden="true"><div class="ns-track">'
        + ('<span>Your skin · Your mind · Your space · ' * 3 + '</span>') * 2 +
        '</div></div>',
        unsafe_allow_html=True,
    )
    with st.container(key="welcome_card"):
        st.markdown(
            '<div class="ns-kicker rv" style="--d:.1s">01 — Check-in</div>'
            '<h1 class="ns-hero-title">'
            '<span class="mask"><span class="line" style="--d:.15s">Welcome to</span></span>'
            '<span class="mask"><span class="line" style="--d:.3s">NeuroSkin 🌿</span></span></h1>'
            '<p class="ns-tagline rv" style="--d:.55s">Your skin, your mind, your space to feel understood.</p>'
            '<p class="ns-body rv" style="--d:.7s">Living with psoriasis can be more than skin deep. NeuroSkin is a '
            'gentle space to check in with your emotional wellbeing, explore your skin\'s condition, '
            'and reflect on your feelings, all at your own pace, without judgment.</p>'
            '<p class="ns-body rv" style="--d:.8s">Answer a few questions, check your skin, or simply write what\'s on your mind.</p>'
            '<p class="ns-closing rv" style="--d:.9s">No pressure, no judgment. Just start wherever you are.</p>',
            unsafe_allow_html=True,
        )
        a, b, _ = st.columns([1.3, 1, 1.1])
        a.button("Begin my check-in", type="primary", key="begin", on_click=_go, args=("assess",))
        b.button("Maybe later", key="maybe_later", on_click=_go, args=("later",))


def later():
    _background_video()
    with st.container(key="welcome_card"):
        st.markdown(
            '<h1 class="ns-welcome-title">That is completely fine.</h1>'
            '<p class="ns-tagline">NeuroSkin will be here whenever you feel ready.</p>'
            '<p class="ns-body">Take care of yourself. There is no deadline and nothing was saved.</p>',
            unsafe_allow_html=True,
        )
        a, b, _ = st.columns([1.25, 1, 1.2])
        a.button("Begin my check-in", type="primary", key="begin_late", on_click=_go, args=("assess",))
        b.button("Back to start", key="back_start", on_click=_go, args=("welcome",))