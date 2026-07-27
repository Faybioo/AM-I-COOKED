"""
"Am I Cooked?" interactive tool — Neon Tokyo palette + real logo.

Run with:  streamlit run app/app.py

Assumes app/assets/logo.png exists (the skull-in-a-pan mark, black bg made transparent).
"""

import base64
import time
import random
import streamlit as st
from pathlib import Path
from mock_model import predict_placement_score, get_tier

st.set_page_config(page_title="Am I Cooked?", page_icon="🍳", layout="centered")

# ---- Neon Tokyo palette (matches the Group SEvEN wordmark layering) ----
BG_DARK = "#0A0A0F"
BG_DARK_2 = "#120A14"
MAGENTA = "#FF28EE"
CYAN = "#00F0FF"
ACID = "#D4FF3F"

TIER_THEME = {
    "GOLD": {"color": ACID, "emoji": "🥇", "glow": "rgba(212,255,63,0.55)"},
    "SILVER": {"color": CYAN, "emoji": "🥈", "glow": "rgba(0,240,255,0.45)"},
    "BRONZE": {"color": "#FF9E2C", "emoji": "🥉", "glow": "rgba(255,158,44,0.45)"},
    "LAST_PLACE": {"color": MAGENTA, "emoji": "💀", "glow": "rgba(255,40,238,0.6)"},
}

SUSPENSE_LINES = [
    "Reading your GPA...",
    "Cross-checking your internships against everyone else's...",
    "Judging your soft skills rating (be so for real)...",
    "Comparing you to a CS major with 6 internships...",
    "Consulting the job market. It's not going well out there...",
    "Calculating your Cooked-O-Meter...",
]


def load_logo_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()


SOUNDS_DIR = Path(__file__).resolve().parent / "assets" / "sounds"


def play_tier_sound(sound_key: str) -> None:
    """
    Looks for assets/sounds/<sound_key>.mp3 (or .wav/.ogg) and autoplays it.
    Silently does nothing if the file isn't there yet — missing audio
    never breaks the reveal, it just plays without sound.
    """
    for ext in ("mp3", "wav", "ogg"):
        path = SOUNDS_DIR / f"{sound_key}.{ext}"
        if path.exists():
            st.audio(str(path), format=f"audio/{ext}", autoplay=True)
            return


logo_b64 = load_logo_base64(str(Path(__file__).resolve().parent / "assets" / "logo.png"))

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(ellipse 900px 600px at 80% 15%, rgba(255,40,238,0.14), transparent 60%),
            radial-gradient(ellipse 700px 500px at 10% 90%, rgba(0,240,255,0.10), transparent 60%),
            linear-gradient(160deg, {BG_DARK} 0%, {BG_DARK} 45%, {BG_DARK_2} 100%);
    }}

    .logo-wrap {{
        text-align: center;
        margin-top: 8px;
        margin-bottom: 4px;
    }}
    .logo-wrap img {{
        width: 150px;
        filter: drop-shadow(0 0 18px rgba(255,40,238,0.35)) drop-shadow(0 0 30px rgba(0,240,255,0.18));
    }}

    .neon-title {{
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 6px;
        margin-bottom: 0px;
        color: #f4f8f9;
        text-shadow: 0 0 16px rgba(0,240,255,0.5), 0 0 36px rgba(0,240,255,0.22);
    }}
    .neon-title .q {{
        color: {CYAN};
        text-shadow: 0 0 16px rgba(255,40,238,0.7), 0 0 36px rgba(255,40,238,0.3);
    }}
    .neon-sub {{
        text-align: center;
        color: rgba(245,240,230,0.6);
        font-size: 14px;
        letter-spacing: 1px;
        margin-bottom: 24px;
    }}

    @keyframes revealPop {{
        0%   {{ transform: scale(0.85); opacity: 0; }}
        60%  {{ transform: scale(1.03); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 20px var(--glow); }}
        50%      {{ box-shadow: 0 0 45px var(--glow); }}
    }}
    .reveal-card {{
        animation: revealPop 0.5s ease-out, pulseGlow 2s ease-in-out infinite;
        border-radius: 16px;
        padding: 36px 28px;
        text-align: center;
        border: 1px solid var(--glow);
        margin-top: 12px;
        background: linear-gradient(160deg, {BG_DARK}, {BG_DARK_2});
    }}
    .reveal-tier {{
        font-size: 46px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }}
    .reveal-score {{
        font-size: 20px;
        opacity: 0.85;
        margin-top: 4px;
        color: #f4f8f9;
    }}
    .reveal-quote {{
        font-style: italic;
        font-size: 18px;
        margin-top: 18px;
        opacity: 0.9;
        color: #f4f8f9;
    }}
    </style>

    <div class="logo-wrap">
        <img src="data:image/png;base64,{logo_b64}">
    </div>
    <div class="neon-title">Am I <span class="q">Cooked?</span></div>
    <div class="neon-sub">GROUP SEvEN &nbsp;·&nbsp; ANSWER HONESTLY. THE PODIUM DOESN'T LIE.</div>
    """,
    unsafe_allow_html=True,
)

with st.form("cooked_form"):
    gpa = st.slider("GPA", 0.0, 4.0, 3.0, 0.1)
    internships = st.number_input("Number of internships", 0, 10, 0)
    projects = st.number_input("Number of projects", 0, 20, 0)
    certifications = st.number_input("Certifications", 0, 10, 0)
    soft_skills = st.slider("Soft skills rating (self-assessed)", 0, 10, 5)
    extracurriculars = st.selectbox("Extracurricular activities", ["None", "Some", "A lot"])
    year = st.selectbox("Year in school", ["Freshman", "Sophomore", "Junior", "Senior"])
    major = st.selectbox("Major category", ["CS/Engineering", "Business", "Other"])
    part_time = st.selectbox("Part-time work experience", ["None", "Some"])
    training = st.selectbox("Completed placement training?", ["Yes", "No"])

    submitted = st.form_submit_button("Am I cooked?")

if submitted:
    user_inputs = {
        "gpa": gpa,
        "num_internships": internships,
        "num_projects": projects,
        "certifications": certifications,
        "extracurriculars": extracurriculars,
        "year_in_school": year,
        "major_category": major,
        "soft_skills_rating": soft_skills,
        "part_time_work": part_time,
        "placement_training": training,
    }

    status_box = st.empty()
    progress = st.progress(0)

    lines = SUSPENSE_LINES.copy()
    random.shuffle(lines)
    for i, line in enumerate(lines):
        status_box.markdown(f"**{line}**")
        progress.progress(int((i + 1) / len(lines) * 100))
        time.sleep(random.uniform(0.35, 0.7))

    status_box.empty()
    progress.empty()

    score = predict_placement_score(user_inputs)
    result = get_tier(score)
    theme = TIER_THEME[result["tier"]]

    st.markdown(
        f"""
        <div class="reveal-card" style="--glow:{theme['glow']};">
            <div class="reveal-tier" style="color:{theme['color']};">
                {theme['emoji']} {result['tier'].replace('_', ' ')}
            </div>
            <div class="reveal-score">{score * 100:.0f}% placement probability</div>
            <div class="reveal-quote">&ldquo;{result['label']}&rdquo;</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    play_tier_sound(result["sound"])

    if result["tier"] == "GOLD":
        st.balloons()
