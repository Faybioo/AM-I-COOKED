# notebooks/

One notebook per person/task while exploring — avoids 3 people editing the same
`.ipynb` at once (which is a merge-conflict nightmare, see root README).

Naming convention:
- `eda_<name>.ipynb` — exploratory data analysis
- `model_<name>_<algo>.ipynb` — e.g. `model_hubert_logreg.ipynb`
- `final_pipeline.ipynb` — the clean, merged, run-top-to-bottom notebook for the
  actual submission/demo (create this near the end, don't build in it from day one)

Reminder: run `nbstripout --install` (see root README) before your first commit so
outputs don't pollute every diff.
