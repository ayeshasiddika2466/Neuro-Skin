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