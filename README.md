# NeuroSkin

A calm space to look at skin and emotional wellbeing together.
NeuroSkin is an educational course project for *AI and Expert System (4385)*,
Northern University Bangladesh. It combines a screening questionnaire, a skin-image
model, an optional journal model and a rule-based expert system.

> **NeuroSkin is not a medical service. It cannot diagnose any condition.**
> Its results are screening-oriented and are not clinically validated.

## What it does

1. **Welcome** page, with a Quick exit button on every later page. Quick exit clears what you entered.
2. **Questionnaire**, one question at a time: PHQ-9 (depression symptoms), GAD-7 (anxiety symptoms),
   plus short stress and skin-impact questions written for this project (not validated).
   You can skip, go back and change answers. A compassionate support message appears if
   PHQ-9 item 9 is above zero.
3. **Skin photo** (JPG or PNG, up to 50 MB) with preview. A MobileNetV3 model returns scores for
   psoriasis, lichen planus and normal skin.
4. **Journal** (optional). A TF-IDF and logistic-regression model gives an emotional-language indicator.
5. **Your Combined Insights**. A rule-based expert system (forward chaining, rules R1 to R6)
   turns the scores into short statements. Each statement can be traced to its rule.
6. **Review my responses**. A small neuron animation walks across your own words, follows the
   cursor a little and can be stopped. It runs only in the browser.

## Results so far (held-out test sets, each used once)

| Part | Result |
|---|---|
| Skin image model (663 photos, 3 classes) | 95.3% accuracy, macro F1 0.954 |
| Journal model (2000 short texts, 2 groups) | 93.5% accuracy, macro F1 0.935 |

These numbers come from single public datasets. They are not clinical performance.
The image data has logos and watermarks that differ between classes, so part of the score
may come from dataset style. Bottom corners were masked during training to reduce this.

## Run it

Python 3.12 is recommended.

```
python -m venv .venv
.venv\Scripts\activate          (Windows)
pip install -r requirements.txt
streamlit run app.py
```

The trained models are **not in this repository**. Put them in `models/`:

- `models/skin_model.pth` and `models/classes.json`
- `models/nlp_model.joblib`

They are made by the notebooks in `notebooks/` (Kaggle). Without them the app still opens and shows
a clear message instead of a prediction.

The background video is `static/welcome.mp4`. The app uses a plain night-sky background.

## Tests

```
python -m pytest
```

77 tests cover scoring, the rule engine, fusion, error handling, the question flow,
the result wording and the neuron page. The model-based tests skip themselves if the
model files are missing.

## Privacy

- Photos and journal text are processed on the computer running the app. They are not written to disk
  by NeuroSkin and are not sent to any service. They stay only while the page is open.
- The neuron page makes no network requests. Only the fonts load from Google Fonts.
- There are no analytics and no accounts. NeuroSkin makes no claim of compliance with any
  healthcare privacy standard.

## Project structure

```
app.py               page flow and wiring only
backend/             questionnaire, expert system, vision, nlp, fusion (no drawing)
frontend/            theme, welcome, question flow, results page, neuron (no calculations)
tests/               automated tests
notebooks/           data preparation and training notebooks
data_splits/         the train/validation/test file list (no images)
docs/                questions, results, notes
```

## Limitations

- Not a diagnosis, not validated clinically, no paired multimodal data.
- The experimental combined indicator is an unvalidated weighted mix.
- The stress and skin-impact questions are not validated instruments.
- Image data: licence "unknown" on Kaggle, no documented labelling source, limited skin-tone range.
- Journal data: short social-media posts, not clinical writing.

## Data and references

- Skin images: Kaggle, aditipathak17, *Autoimmune - Lichen Planus, Psoriasis, Normal Skin* (licence unknown). Not included.
- Journal text: Kaggle, praveengovi, *Emotions dataset for NLP* (CC BY-SA 4.0). Not included.
- Background video: "(clip title)" by (creator name), Pexels. Used under the Pexels License.
- Kroenke, Spitzer and Williams (2001). The PHQ-9. *J Gen Intern Med* 16(9).
- Spitzer, Kroenke, Williams and Lowe (2006). The GAD-7. *Arch Intern Med* 166(10).

