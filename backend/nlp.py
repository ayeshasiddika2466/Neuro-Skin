# backend/nlp.py
# Reads a short journal text and gives a distress indicator. No Streamlit.

import os
import re

import joblib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE, "models", "nlp_model.joblib")

DISTRESS_THRESHOLD = 0.60   # documented choice, not tuned to look good
MIN_WORDS = 3
MAX_WORDS = 200

_cache = {}


def clean(text):
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z' ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_model():
    if "bundle" not in _cache:
        _cache["bundle"] = joblib.load(MODEL_PATH)
    return _cache["bundle"]


def predict_text(text):
    """Returns a dictionary. Text is optional, so empty text is not an error."""
    if text is None or not str(text).strip():
        return {"provided": False, "valid": True,
                "distress_score": None, "text_distress": None}

    words = clean(str(text)).split()
    if len(words) < MIN_WORDS:
        return {"provided": True, "valid": False,
                "error": "The text is too short.",
                "distress_score": None, "text_distress": None}

    words = words[:MAX_WORDS]
    bundle = load_model()
    X = bundle["vectorizer"].transform([" ".join(words)])
    score = float(bundle["model"].predict_proba(X)[0][1])

    return {
        "provided": True,
        "valid": True,
        "distress_score": score,
        "text_distress": "ELEVATED" if score >= DISTRESS_THRESHOLD else "NORMAL",
    }