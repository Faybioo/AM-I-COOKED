# Am I Cooked? 🍳

A binary classification project (CIS4930 — Intro to Machine Learning, Summer 2026) predicting
whether a US college student will land a job placement, wrapped in an interactive tool with
an Olympic podium reveal, tiered audio feedback, and personalized "How to Level Up" recs.

## Team

| Name | Role |
|---|---|
| NJ Lacambra | Team Lead — UX, interactive tool, slides, demo |
| Hubert Ferro | Data cleaning, EDA, 2 ML models, evaluation |
| Fabio E. Jorge Hernandez | 1 ML model, feature importance, audio/animation, results |

## Repo Structure

```
├── data/
│   ├── raw/            # original dataset, untouched (gitignored — see below)
│   └── processed/      # cleaned/feature-engineered data
├── notebooks/          # EDA + modeling notebooks (one per person, see workflow below)
├── src/                # shared, reusable Python (data loading, preprocessing, model utils)
├── app/                # interactive "Am I Cooked?" tool (UX layer)
└── slides/             # deck assets / exports
```

## Setup

```bash
git clone <repo-url>
cd am-i-cooked
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# one-time: keeps notebook diffs clean so merges don't turn into a nightmare
pip install nbstripout
nbstripout --install
```

## Notebook Workflow (read before you commit a notebook)

Raw `.ipynb` files are JSON — every time you *run* a cell, the output and execution
count change, which creates merge conflicts even if your code didn't change. Rules:

1. Work in your **own** notebook: `notebooks/eda_hubert.ipynb`, `notebooks/model_fabio.ipynb`, etc.
2. `nbstripout` (installed above) automatically strips outputs before each commit — don't fight it.
3. Once a notebook's logic is solid, move the reusable functions into `src/` so the rest
   of the team can import them instead of copy-pasting between notebooks.
4. Only merge into a shared/final notebook when it's demo-ready, and have one person
   run it top-to-bottom right before that merge.

## Branching

- `main` stays in a working state at all times.
- Branch per feature/person: `git checkout -b nj-interactive-tool`
- Small, frequent commits. PR into `main` when a piece works, not when it's "perfect."

## Dataset

[College Student Placement Factors Dataset](https://www.kaggle.com/datasets/sahilislam007/college-student-placement-factors-dataset)
— 10,000 samples, 10+ features, binary target (`Placement Status`).

Drop the raw CSV into `data/raw/` locally. It's gitignored — don't commit the dataset itself,
just the code that loads it.
