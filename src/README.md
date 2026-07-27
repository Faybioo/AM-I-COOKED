# src/

Shared, reusable code — anything more than one notebook or the app needs.

Suggested split as the project grows:
- `data.py` — loading/cleaning the raw CSV into a clean DataFrame
- `features.py` — feature engineering shared across models
- `model_utils.py` — train/eval helpers (e.g. a `evaluate(model, X_test, y_test)` that
  returns macro F1, accuracy, balanced accuracy, confusion matrix — so Hubert and Fabio
  report metrics the same way for all 3 models)

Import from a notebook like:
```python
import sys
sys.path.append("..")
from src.data import load_clean_data
```
