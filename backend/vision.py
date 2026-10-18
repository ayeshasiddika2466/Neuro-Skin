# backend/vision.py
# Loads the trained skin model and predicts. No Streamlit, no drawing.

import io
import json
import os

import torch
import torch.nn as nn
from PIL import Image, ImageDraw
from torchvision import models, transforms

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE, "models", "skin_model.pth")
CLASSES_PATH = os.path.join(BASE, "models", "classes.json")

IMG = 224
MIN_SIDE = 32
MAX_BYTES = 50 * 1024 * 1024   

_tf = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
_cache = {}


def hide_corners(img):
    """Same logo hiding as in training. Must stay identical."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(h * 0.80), int(w * 0.30), h], fill=(0, 0, 0))
    d.rectangle([int(w * 0.70), int(h * 0.80), w, h], fill=(0, 0, 0))
    return img


def load_model():
    """Loads the model once, then reuses it."""
    if "model" not in _cache:
        with open(CLASSES_PATH) as f:
            classes = json.load(f)
        model = models.mobilenet_v3_small(weights=None)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, len(classes))
        model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        model.eval()
        _cache["model"] = model
        _cache["classes"] = classes
    return _cache["model"], _cache["classes"]


def _open_image(source):
    """Accepts a file path, bytes, or a file-like object (like a Streamlit upload)."""
    if isinstance(source, (str, os.PathLike)):
        img = Image.open(source)
    elif isinstance(source, bytes):
        img = Image.open(io.BytesIO(source))
    else:
        img = Image.open(io.BytesIO(source.read()))
    img.load()                      # forces a full read, so broken files fail here
    return img.convert("RGB")


def predict_image(source):
    """Returns a dictionary. Never crashes on a bad image."""
    if isinstance(source, bytes) and len(source) > MAX_BYTES:
        return {"valid": False, "error": "The image is too large (maximum 50 MB)."}
    try:
        img = _open_image(source)
    except Exception:
        return {"valid": False, "error": "This file is not a readable image."}

    if min(img.size) < MIN_SIDE:
        return {"valid": False, "error": "The image is too small."}

    model, classes = load_model()
    img = hide_corners(img.resize((IMG, IMG)))
    x = _tf(img).unsqueeze(0)

    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1)[0].tolist()

    best = max(range(len(classes)), key=lambda i: probs[i])
    by_class = {classes[i]: probs[i] for i in range(len(classes))}
    return {
        "valid": True,
        "label": classes[best],
        "confidence": probs[best],
        "probabilities": by_class,
        "psoriasis_probability": by_class["PSORIASIS"],
    }