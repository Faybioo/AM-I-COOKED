# app/

The interactive "Am I Cooked?" tool — NJ's lane.

- `mock_model.py` — fake scoring function so the UI can be built and tested without
  waiting on the real trained model. Swap `predict_placement_score` for the real
  `model.predict_proba()` call once it exists; nothing else should need to change.
- `app.py` — bare-bones Streamlit shell proving the pipeline works end to end
  (inputs → score → tier → reveal). Replace with your real design (podium graphics,
  audio triggers, "How to Level Up" recs) — this just proves the wiring.

Run it:
```bash
cd app
streamlit run app.py
```

If you end up wanting a different stack (React app instead of Streamlit, etc.), that's
fine — `mock_model.py` doesn't care what calls it. Just keep the same function signature
so swapping in the real model later is a one-line change.
