# frontend/theme.py
# Design tokens and global style. Only the look: no calculations.

import html

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
  /* colour tokens */
  --ns-night: #0b1026;
  --ns-indigo: #151a3d;
  --ns-slate: #243049;
  --ns-ivory: #ece6d8;
  --ns-silver: #b4b8c8;
  --ns-lavender: #a9a6d6;
  --ns-teal: #5fa8a0;
  --ns-amber: #d9a441;
  --ns-red: #d9645c;
  /* surfaces */
  --ns-glass: rgba(236, 230, 216, 0.055);
  --ns-glass-strong: rgba(21, 26, 61, 0.72);
  --ns-line: rgba(236, 230, 216, 0.14);
  /* shape and motion */
  --ns-radius: 20px;
  --ns-radius-pill: 999px;
  --ns-shadow: 0 14px 40px rgba(0, 0, 0, 0.35);
  --ns-ease: cubic-bezier(.22, .61, .36, 1);
  --ns-font-display: 'Cormorant Garamond', Georgia, serif;
  --ns-font-body: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

/* text: set on the page only, so icon fonts keep their own font */
.stApp { font-family: var(--ns-font-body); color: var(--ns-ivory); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: var(--ns-font-display) !important;
  font-weight: 600; letter-spacing: 0.2px; color: var(--ns-ivory);
}
[data-testid="stIconMaterial"], span[class*="material"] {
  font-family: "Material Symbols Rounded", "Material Icons" !important;
}

/* quiet night-sky background */
.stApp {
  background:
    radial-gradient(900px 520px at 14% 6%, rgba(169, 166, 214, .14), transparent 62%),
    radial-gradient(800px 520px at 90% 20%, rgba(95, 168, 160, .09), transparent 62%),
    linear-gradient(165deg, #080c20 0%, #0b1026 45%, #121a3a 100%);
  background-attachment: fixed;
}
.stApp::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image:
    radial-gradient(1px 1px at 8% 18%, rgba(236,230,216,.55), transparent),
    radial-gradient(1px 1px at 17% 62%, rgba(236,230,216,.35), transparent),
    radial-gradient(1.5px 1.5px at 26% 33%, rgba(236,230,216,.5), transparent),
    radial-gradient(1px 1px at 38% 80%, rgba(236,230,216,.3), transparent),
    radial-gradient(1px 1px at 47% 12%, rgba(236,230,216,.45), transparent),
    radial-gradient(1.5px 1.5px at 58% 52%, rgba(236,230,216,.35), transparent),
    radial-gradient(1px 1px at 66% 27%, rgba(236,230,216,.5), transparent),
    radial-gradient(1px 1px at 74% 74%, rgba(236,230,216,.3), transparent),
    radial-gradient(1.5px 1.5px at 83% 41%, rgba(236,230,216,.45), transparent),
    radial-gradient(1px 1px at 92% 88%, rgba(236,230,216,.35), transparent),
    radial-gradient(1px 1px at 96% 14%, rgba(236,230,216,.4), transparent);
  animation: ns-twinkle 14s ease-in-out infinite alternate;
}
@keyframes ns-twinkle { from { opacity: .45; } to { opacity: .95; } }

header[data-testid="stHeader"] { background: transparent; pointer-events: none; }
header[data-testid="stHeader"] [data-testid="stToolbar"] { pointer-events: auto; }
.block-container {
  max-width: 1120px; padding-top: 3.2rem; position: relative; z-index: 1;
  animation: ns-rise .8s var(--ns-ease) both;
}
@keyframes ns-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }

/* panels: restrained glass, used only on bordered containers */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--ns-glass);
  border: 1px solid var(--ns-line) !important;
  border-radius: var(--ns-radius);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--ns-shadow);
}
[data-testid="stForm"] { background: transparent; border: none; padding: 0; }

/* welcome card: glass with a softly highlighted border */
.st-key-welcome_card {
  background: rgba(14, 20, 50, .56);
  border: 1px solid rgba(169, 166, 214, .52);
  border-radius: 28px;
  padding: 2.8rem 2.8rem 2.2rem;
  max-width: 820px; margin: 5vh 0 0 0;
  backdrop-filter: blur(16px) saturate(1.15); -webkit-backdrop-filter: blur(16px) saturate(1.15);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .14),
    0 0 0 1px rgba(236, 230, 216, .05),
    0 0 42px rgba(169, 166, 214, .20),
    0 24px 70px rgba(0, 0, 0, .50);
}
.ns-kicker { letter-spacing: .28em; text-transform: uppercase; font-size: .72rem; color: var(--ns-lavender); margin-bottom: .6rem; }
.ns-welcome-title { font-family: var(--ns-font-display); font-size: 2.9rem; line-height: 1.1; margin: 0 0 .5rem; color: var(--ns-ivory); }
.ns-tagline { font-family: var(--ns-font-display); font-size: 1.45rem; font-style: italic; color: var(--ns-lavender); margin: 0 0 1.4rem; }
.ns-body { color: var(--ns-silver); line-height: 1.75; font-size: 1.02rem; margin: 0 0 .9rem; }
.ns-closing { color: var(--ns-ivory); font-weight: 500; margin: 1.2rem 0 1.4rem; }
.ns-fine { color: #8d93aa; font-size: .8rem; margin-top: 1.6rem; }

/* small wordmark on inner pages */
.ns-brand { font-family: var(--ns-font-display); font-size: 2rem; color: var(--ns-ivory); margin: 0 0 .2rem; letter-spacing: .5px; }
.ns-brand span { color: var(--ns-lavender); }

/* buttons: pill, with a fill that slides in on hover */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
  position: relative; overflow: hidden; isolation: isolate;
  background: transparent; color: var(--ns-ivory);
  border: 1px solid rgba(236, 230, 216, .38); border-radius: var(--ns-radius-pill);
  padding: .65rem 1.9rem; font-weight: 500; letter-spacing: .02em;
  transition: color .35s var(--ns-ease), border-color .35s var(--ns-ease);
}
.stButton > button::before, [data-testid="stFormSubmitButton"] > button::before {
  content: ""; position: absolute; inset: 0; z-index: -1; border-radius: inherit;
  background: var(--ns-ivory); transform: translateY(101%);
  transition: transform .5s var(--ns-ease);
}
.stButton > button:hover::before, [data-testid="stFormSubmitButton"] > button:hover::before { transform: translateY(0); }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { color: #0b1026; border-color: var(--ns-ivory); }
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--ns-ivory) !important; color: #0b1026 !important; border-color: var(--ns-ivory) !important;
  font-weight: 600;
}
[data-testid="stBaseButton-primary"]::before, [data-testid="stBaseButton-primaryFormSubmit"]::before { background: var(--ns-teal) !important; }
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover { color: #08101c !important; border-color: var(--ns-teal) !important; }
button:focus-visible, [role="radio"]:focus-visible, textarea:focus-visible {
  outline: 2px solid var(--ns-lavender) !important; outline-offset: 2px;
}

/* button text must never be cut off */
.stButton > button { white-space: nowrap; }
.stButton > button p { white-space: nowrap; overflow: visible; text-overflow: clip; }
[class*="st-key-question_card"] .stButton > button { padding: .55rem 1.1rem; }

/* quick exit: in the page flow, top right */
.st-key-exit { display: flex; justify-content: flex-end; }
.st-key-exit button {
  background: rgba(11, 16, 38, .8); border: 1px solid rgba(217, 164, 65, .6);
  color: var(--ns-amber); padding: .4rem 1.1rem; font-size: .88rem;
}
.st-key-exit button:hover { background: rgba(217, 164, 65, .14); border-color: var(--ns-amber); color: #f0c46c; }

/* one-question-at-a-time card */
[class*="st-key-question_card"] {
  background: var(--ns-glass-strong); border: 1px solid var(--ns-line);
  border-radius: 24px; padding: 1.6rem 1.8rem; min-height: 340px;
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--ns-shadow); animation: ns-rise .5s var(--ns-ease) both;
}
.ns-q-text {
  font-family: var(--ns-font-display); font-size: 1.7rem; line-height: 1.3;
  margin: .4rem 0 1.1rem; color: var(--ns-ivory);
}
.ns-note { color: #8d93aa; font-size: .82rem; margin: .3rem 0 .8rem; }

/* inputs */
textarea, [data-baseweb="textarea"] {
  background: rgba(236, 230, 216, .05) !important; color: var(--ns-ivory) !important;
  border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: rgba(236, 230, 216, .04); border: 1.5px dashed rgba(236, 230, 216, .28);
  border-radius: 16px; min-height: 150px; padding: 1.4rem;
}
[data-testid="stFileUploaderDropzone"] button { white-space: nowrap; }

/* results furniture */
[data-testid="stMetric"] {
  background: var(--ns-glass); border: 1px solid var(--ns-line);
  border-radius: 16px; padding: 14px 16px;
}
[data-testid="stAlert"] { border-radius: 16px; }
[data-testid="stExpander"] {
  background: var(--ns-glass); border: 1px solid var(--ns-line); border-radius: 16px;
}
.stProgress > div > div > div > div { background: linear-gradient(90deg, #5fa8a0, #a9a6d6); }

/* results */
.ns-result-line { font-family: var(--ns-font-display); font-size: 1.65rem; line-height: 1.3; color: var(--ns-ivory); margin: .2rem 0 .5rem; }
.ns-stat { background: var(--ns-glass); border: 1px solid var(--ns-line); border-radius: 14px; padding: 10px 12px; }
.ns-stat-label { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--ns-lavender); }
.ns-stat-value { font-family: var(--ns-font-display); font-size: 1.9rem; line-height: 1.1; color: var(--ns-ivory); }
.ns-stat-note { font-size: .78rem; color: var(--ns-silver); }

/* ---------- editorial layer ---------- */
/* film grain */
.stApp::after {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 3; opacity: .09;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='.6'/></svg>");
}

@keyframes ns-reveal { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes ns-line { from { transform: translateY(112%); } to { transform: none; } }
@keyframes ns-marquee { to { transform: translateX(-50%); } }
@keyframes ns-pre { 0%, 72% { opacity: 1; visibility: visible; } 100% { opacity: 0; visibility: hidden; } }
@keyframes ns-pre-text { from { opacity: 0; letter-spacing: .75em; } to { opacity: 1; letter-spacing: .35em; } }

.rv { animation: ns-reveal .9s var(--ns-ease) both; animation-delay: calc(var(--d, 0s) + 1.1s); }
.mask { display: block; overflow: hidden; padding-bottom: .1em; }
.line { display: block; animation: ns-line 1s var(--ns-ease) both; animation-delay: calc(var(--d, 0s) + 1.1s); }

.ns-hero-title {
  font-family: var(--ns-font-display); font-weight: 600; color: var(--ns-ivory);
  font-size: clamp(2.8rem, 7vw, 5.6rem); line-height: .98; letter-spacing: -.01em; margin: .2rem 0 1rem;
}

/* top bar and the moving line of words */
.ns-topbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: .3rem 0 1rem; border-bottom: 1px solid var(--ns-line);
  animation: ns-reveal .9s var(--ns-ease) both; animation-delay: 1.1s;
}
.ns-wordmark { font-family: var(--ns-font-display); font-size: 1.55rem; letter-spacing: .04em; }
.ns-wordmark em { font-style: normal; color: var(--ns-lavender); }
.ns-meta { font-size: .7rem; letter-spacing: .2em; text-transform: uppercase; color: var(--ns-silver); }
.ns-marquee { position: fixed; left: 0; right: 0; bottom: 1vh; overflow: hidden; z-index: -1; pointer-events: none; white-space: nowrap; }
.ns-track { display: inline-flex; animation: ns-marquee 40s linear infinite; }
.ns-track span {
  font-family: var(--ns-font-display); font-style: italic; padding-right: .4em;
  font-size: clamp(3rem, 9vw, 7.5rem); color: transparent;
  -webkit-text-stroke: 1px rgba(236, 230, 216, .30);
}
.ns-preloader {
  position: fixed; inset: 0; z-index: 99999; background: #070a1c; display: grid; place-items: center;
  pointer-events: none; animation: ns-pre 1.9s var(--ns-ease) forwards;
}
.ns-preloader span {
  font-family: var(--ns-font-display); font-size: clamp(2rem, 6vw, 4rem); text-transform: uppercase;
  color: var(--ns-ivory); animation: ns-pre-text 1.5s var(--ns-ease) both;
}

/* numbered section titles */
.ns-section { display: flex; align-items: baseline; gap: 1rem; margin: 1.4rem 0 .9rem; }
.ns-num { font-size: .78rem; letter-spacing: .2em; color: var(--ns-lavender); }
.ns-rule { flex: 0 0 56px; height: 1px; background: rgba(236, 230, 216, .35); transform: translateY(-5px); }
.ns-h2 { font-family: var(--ns-font-display) !important; font-weight: 600; font-size: clamp(1.9rem, 3.6vw, 3rem); line-height: 1.05; margin: 0; color: var(--ns-ivory); }

/* reveal on scroll (Chrome and Edge; others simply show everything) */
@supports (animation-timeline: view()) {
  .ns-section, [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {
    animation: ns-reveal linear both; animation-timeline: view(); animation-range: entry 0% entry 45%;
  }
}
@media (prefers-reduced-motion: reduce) {
  .rv, .line, .ns-topbar, .ns-section, [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] {
    animation: none !important; opacity: 1; transform: none;
  }
  .ns-preloader { display: none; }
  .ns-track { animation: none; }
}

/* mobile */
@media (max-width: 640px) {
  .st-key-welcome_card { padding: 1.7rem 1.3rem; margin-top: 3vh; }
  .ns-welcome-title { font-size: 2.2rem; }
  .block-container { padding-top: 4rem; }
}

/* reduced motion: no animation at all */
@media (prefers-reduced-motion: reduce) {
  .stApp::before, .block-container, .ns-video, [class*="st-key-question_card"] { animation: none !important; }
  .stButton > button { transition: none; }
}

/* optional background video (only used if static/welcome.mp4 exists) */
.ns-video {
  position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover;
  z-index: -1; opacity: .8; pointer-events: none;
}
.ns-video-veil {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(ellipse at 30% 40%, rgba(8,12,32,.15), rgba(8,12,32,.78) 85%), linear-gradient(180deg, rgba(8,12,32,.35), rgba(11,16,38,.7));
}
.ns-video.dim { opacity: .45; }
.ns-video-veil.dim { background: linear-gradient(180deg, rgba(8,12,32,.60), rgba(11,16,38,.80)); }
@media (prefers-reduced-motion: reduce) { .ns-video { display: none; } }
@media (max-width: 640px) { .ns-video { display: none; } }
</style>
"""


def apply():
    st.markdown(CSS, unsafe_allow_html=True)


def brand():
    st.markdown('<div class="ns-brand">Neuro<span>Skin</span></div>', unsafe_allow_html=True)


def section(number, title):
    st.markdown(
        f'<div class="ns-section"><span class="ns-num">{html.escape(number)}</span>'
        f'<span class="ns-rule"></span><h2 class="ns-h2">{html.escape(title)}</h2></div>',
        unsafe_allow_html=True,
    )