# Dataset candidates

## Candidate 1
- Name: Autoimmune - Lichen Planus, Psoriasis, Normal Skin (Kaggle, aditipathak17)
- Link: https://www.kaggle.com/datasets/aditipathak17/autoimmune-lichen-planus-psoriasis-normal-skin
- Licence: Unknown
- Size: 1.03 GB
- Classes: PSORIASIS 1586, NORMAL SKIN ~1404, LICHEN PLANUS (count to check)
- Labels: not documented
- Risks: logo/watermark differences between classes, skin tone mismatch, no severity labels
- Decision: binary psoriasis vs non-psoriasis; add lichen only if count is OK
## Candidate 2
(same list)

## Candidate 3
(same list)

## Decision
- First choice:
- Name: Autoimmune - Lichen Planus, Psoriasis, Normal Skin (Kaggle, aditipathak17)
- Link: https://www.kaggle.com/datasets/aditipathak17/autoimmune-lichen-planus-psoriasis-normal-skin
- Licence: Unknown
- Size: 1.03 GB
- Classes: PSORIASIS 1586, NORMAL SKIN ~1404, LICHEN PLANUS (count to check)
- Labels: not documented
- Risks: logo/watermark differences between classes, skin tone mismatch, no severity labels
- Decision: binary psoriasis vs non-psoriasis; add lichen only if count is OK

## Cleaning (Day 4)
- Before: PSORIASIS 1586, LICHEN PLANUS 1565, NORMAL SKIN 1404 (total 4555)
- Unreadable files: 0
- Exact duplicate rows: 276
- Same picture in different classes: 0
- After cleaning: (add the numbers from the next cell)
- Limitation: only exact copies are found. Resized or re-saved copies may still be there.
- Finding: psoriasis photos often have a small logo in the bottom-left. Lichen planus photos sometimes have a Dermnet watermark. Normal skin photos have no logos. The model might learn these marks instead of the disease.
- Plan: hide the logo corner during training (Day 5), and report this limitation.
- after: {'PSORIASIS': 1586, 'LICHEN PLANUS': 1565, 'NORMAL SKIN': 1266} | total: 4417

## Split (Day 4)
- After cleaning: PSORIASIS 1586, LICHEN PLANUS 1565, NORMAL SKIN 1266 (total 4417)
- 138 exact duplicates removed, all from NORMAL SKIN
- Stratified split, random_state=42: train 3091, val 663, test 663
- Test set stays untouched until Day 6

## Day 5: training
- Model: MobileNetV3-Small, pretrained on ImageNet, last layer changed to 3 classes
- Bottom-left and bottom-right corners painted black on all images (logo cheating)
- 3 epochs head only (lr 1e-3), then 5 epochs fine-tuning (lr 1e-4), seed 42
- Best validation accuracy: 0.9608 (finetune epoch 4)
- Train acc 0.986 vs val acc 0.958 at the end: small gap, slight overfitting
- Limitation: Dermnet watermarks in the middle of some pictures cannot be removed
- The validation score is not the final score. The test set is used on Day 6.

## Day 6: test results
- Test set: 663 images, run once, after training was finished
- Accuracy / macro F1 / psoriasis precision / psoriasis recall: (your real numbers)
- Main mistakes: (what you saw in the confusion matrix)
- The score is partly helped by dataset style (clean normal skin, watermarks). It is not clinical performance.