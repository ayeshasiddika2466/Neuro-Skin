import os
import pytest

from backend.nlp import predict_text, clean, MODEL_PATH

needs_model = pytest.mark.skipif(not os.path.exists(MODEL_PATH),
                                 reason="model file not on this computer")


def test_empty_text_is_ok():
    result = predict_text("")
    assert result["provided"] is False
    assert result["text_distress"] is None


def test_none_and_spaces():
    assert predict_text(None)["provided"] is False
    assert predict_text("     ")["provided"] is False


def test_too_short():
    assert predict_text("sad")["valid"] is False


def test_clean_removes_links_and_symbols():
    assert clean("Hello!!! http://x.com WORLD") == "hello world"


@needs_model
def test_same_text_same_score():
    t = "I feel tired and worried about everything lately"
    assert predict_text(t) == predict_text(t)


@needs_model
def test_score_between_0_and_1():
    s = predict_text("I feel nervous and I cannot sleep")["distress_score"]
    assert 0.0 <= s <= 1.0


@needs_model
def test_sad_text_scores_higher_than_happy_text():
    sad = predict_text("I feel hopeless and scared and completely alone")
    happy = predict_text("I am so happy and excited about today")
    assert sad["distress_score"] > happy["distress_score"]