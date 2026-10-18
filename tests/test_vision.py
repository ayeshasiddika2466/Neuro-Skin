import io
import os

import pytest
from PIL import Image

from backend.vision import predict_image, hide_corners, MODEL_PATH

needs_model = pytest.mark.skipif(not os.path.exists(MODEL_PATH),
                                 reason="model file not on this computer")

from backend.vision import MAX_BYTES

def test_too_large_file():
    assert predict_image(b"0" * (MAX_BYTES + 1))["valid"] is False


def make_png(size=(100, 100), color=(200, 120, 100)):
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, format="PNG")
    return buf.getvalue()


def test_case_f_not_an_image():
    result = predict_image(b"hello, I am not a picture")
    assert result["valid"] is False


def test_empty_file():
    assert predict_image(b"")["valid"] is False


def test_missing_path():
    assert predict_image("no_such_file.jpg")["valid"] is False


def test_too_small_image():
    assert predict_image(make_png(size=(10, 10)))["valid"] is False


def test_hide_corners_paints_black():
    img = hide_corners(Image.new("RGB", (100, 100), (255, 255, 255)))
    assert img.getpixel((5, 95)) == (0, 0, 0)
    assert img.getpixel((95, 95)) == (0, 0, 0)
    assert img.getpixel((50, 10)) == (255, 255, 255)


@needs_model
def test_valid_image_gives_probabilities():
    result = predict_image(make_png())
    assert result["valid"] is True
    assert abs(sum(result["probabilities"].values()) - 1.0) < 1e-4
    assert 0.0 <= result["psoriasis_probability"] <= 1.0


@needs_model
def test_same_image_same_result():
    data = make_png()
    assert predict_image(data) == predict_image(data)