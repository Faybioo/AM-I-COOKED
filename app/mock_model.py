import random

EXPECTED_FEATURES = [
    "gpa",
    "num_internships",
    "num_projects",
    "certifications",
    "extracurriculars",
    "year_in_school",
    "major_category",
    "soft_skills_rating",
    "part_time_work",
    "placement_training",
]


def predict_placement_score(user_inputs: dict) -> float:
    missing = [f for f in EXPECTED_FEATURES if f not in user_inputs]
    if missing:
        raise ValueError(f"Missing expected inputs: {missing}")
    return round(random.uniform(0, 1), 3)


def get_tier(score: float) -> dict:
    pct = score * 100
    sound = "yay" if pct > 70 else "oops"

    if pct >= 80:
        return {"tier": "GOLD", "label": "You're built different", "sound": sound}
    elif pct >= 60:
        return {"tier": "SILVER", "label": "You got a shot bestie", "sound": sound}
    elif pct >= 40:
        return {"tier": "BRONZE", "label": "It's giving participation trophy", "sound": sound}
    else:
        return {"tier": "LAST_PLACE", "label": "You are so cooked", "sound": sound}