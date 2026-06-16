"""
AthleteOS - Mock data layer.

Generates realistic, deterministic mock data entirely in-app so the project
runs on Streamlit Community Cloud with zero external services.

Key domain rules:
  * Each coach manages athletes of a SINGLE sport (no mixed-sport squads).
  * Only SOME athletes have a connected wearable (WHOOP / Garmin / Apple Watch).
  * Every athlete has 60 days of physical + mental daily metrics.
"""

from __future__ import annotations

import datetime as _dt
import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Static configuration
# ----------------------------------------------------------------------------

HISTORY_DAYS = 60

# Sport -> emoji-free icon label + accent colour used across charts/cards.
SPORTS = {
    "Sprinting": {"accent": "#00E676", "unit": "sprint time (s)"},
    "Swimming": {"accent": "#29B6F6", "unit": "100m time (s)"},
    "Basketball": {"accent": "#FF6B35", "unit": "vertical (cm)"},
    "Cycling": {"accent": "#FFD23F", "unit": "FTP (w)"},
}

WEARABLES = ["WHOOP", "Garmin", "Apple Watch", "Polar"]

# Coaches each own ONE sport. Athletes are grouped strictly under that sport.
COACHES = [
    {"id": "c_maria", "name": "Coach Maria", "sport": "Sprinting", "username": "maria", "password": "coach123"},
    {"id": "c_david", "name": "Coach David", "sport": "Swimming", "username": "david", "password": "coach123"},
    {"id": "c_tara", "name": "Coach Tara", "sport": "Basketball", "username": "tara", "password": "coach123"},
    {"id": "c_leo", "name": "Coach Leo", "sport": "Cycling", "username": "leo", "password": "coach123"},
]

# Athlete roster. `wearable` is None for athletes who have NOT connected a device.
# username/password are simple mock credentials for the demo login.
ATHLETES = [
    # --- Sprinting (Coach Maria) ---
    {"id": "a_alex", "name": "Alex Carter", "sport": "Sprinting", "coach_id": "c_maria", "age": 24, "wearable": "WHOOP", "username": "alex", "password": "athlete123"},
    {"id": "a_jordan", "name": "Jordan Lee", "sport": "Sprinting", "coach_id": "c_maria", "age": 22, "wearable": "Garmin", "username": "jordan", "password": "athlete123"},
    {"id": "a_sam", "name": "Sam Rivera", "sport": "Sprinting", "coach_id": "c_maria", "age": 26, "wearable": None, "username": "sam", "password": "athlete123"},
    {"id": "a_nina", "name": "Nina Kovac", "sport": "Sprinting", "coach_id": "c_maria", "age": 23, "wearable": None, "username": "nina", "password": "athlete123"},
    # --- Swimming (Coach David) ---
    {"id": "a_mia", "name": "Mia Tanaka", "sport": "Swimming", "coach_id": "c_david", "age": 21, "wearable": "Garmin", "username": "mia", "password": "athlete123"},
    {"id": "a_omar", "name": "Omar Haddad", "sport": "Swimming", "coach_id": "c_david", "age": 25, "wearable": "Apple Watch", "username": "omar", "password": "athlete123"},
    {"id": "a_lena", "name": "Lena Schmidt", "sport": "Swimming", "coach_id": "c_david", "age": 24, "wearable": None, "username": "lena", "password": "athlete123"},
    # --- Basketball (Coach Tara) ---
    {"id": "a_dre", "name": "Andre Brooks", "sport": "Basketball", "coach_id": "c_tara", "age": 27, "wearable": "WHOOP", "username": "andre", "password": "athlete123"},
    {"id": "a_kia", "name": "Kiara Jones", "sport": "Basketball", "coach_id": "c_tara", "age": 23, "wearable": None, "username": "kiara", "password": "athlete123"},
    {"id": "a_tom", "name": "Tom Becker", "sport": "Basketball", "coach_id": "c_tara", "age": 28, "wearable": None, "username": "tom", "password": "athlete123"},
    # --- Cycling (Coach Leo) ---
    {"id": "a_eva", "name": "Eva Moreau", "sport": "Cycling", "coach_id": "c_leo", "age": 29, "wearable": "Garmin", "username": "eva", "password": "athlete123"},
    {"id": "a_raj", "name": "Raj Patel", "sport": "Cycling", "coach_id": "c_leo", "age": 26, "wearable": "Polar", "username": "raj", "password": "athlete123"},
    {"id": "a_finn", "name": "Finn O'Brien", "sport": "Cycling", "coach_id": "c_leo", "age": 22, "wearable": None, "username": "finn", "password": "athlete123"},
]


# ----------------------------------------------------------------------------
# Lookups
# ----------------------------------------------------------------------------

def get_coaches():
    return COACHES


def get_athletes():
    return ATHLETES


def get_coach(coach_id):
    return next((c for c in COACHES if c["id"] == coach_id), None)


def get_athlete(athlete_id):
    return next((a for a in ATHLETES if a["id"] == athlete_id), None)


def get_athletes_for_coach(coach_id):
    """Return athletes managed by a coach. By construction they share one sport."""
    return [a for a in ATHLETES if a["coach_id"] == coach_id]


def build_login_table():
    """Return {username: {role, id, password, name}} for the mock login."""
    table = {}
    for c in COACHES:
        table[c["username"]] = {"role": "coach", "id": c["id"], "password": c["password"], "name": c["name"]}
    for a in ATHLETES:
        table[a["username"]] = {"role": "athlete", "id": a["id"], "password": a["password"], "name": a["name"]}
    return table


# ----------------------------------------------------------------------------
# Time-series generation
# ----------------------------------------------------------------------------

def _athlete_seed(athlete_id: str) -> int:
    return abs(hash(athlete_id)) % (2**31)


def _generate_series(athlete: dict) -> pd.DataFrame:
    """Generate a deterministic 60-day metric history for one athlete."""
    rng = np.random.default_rng(_athlete_seed(athlete["id"]))
    n = HISTORY_DAYS
    today = _dt.date.today()
    dates = [today - _dt.timedelta(days=(n - 1 - i)) for i in range(n)]

    # Per-athlete baseline personality so squads look varied but stable.
    base_recovery = rng.uniform(58, 78)
    base_sleep = rng.uniform(6.4, 8.0)
    base_hrv = rng.uniform(55, 95)
    base_rhr = rng.uniform(44, 58)
    base_stress = rng.uniform(3.0, 5.5)
    base_motivation = rng.uniform(6.0, 8.5)

    # A gentle wave + noise to simulate training cycles.
    t = np.arange(n)
    wave = np.sin(t / 7.0)

    rows = []
    for i in range(n):
        load = float(np.clip(rng.normal(60, 18) + 12 * max(0, wave[i]), 10, 100))
        sleep = float(np.clip(base_sleep + rng.normal(0, 0.7) - 0.01 * load, 4.0, 9.5))
        hrv = float(np.clip(base_hrv + 8 * wave[i] + rng.normal(0, 6) - 0.08 * load, 25, 130))
        rhr = float(np.clip(base_rhr - 3 * wave[i] + rng.normal(0, 2) + 0.04 * load, 38, 72))
        recovery = float(np.clip(base_recovery + 0.25 * (hrv - base_hrv) - 0.2 * (rhr - base_rhr)
                                 + 4 * (sleep - base_sleep) - 0.15 * (load - 60) + rng.normal(0, 4), 10, 100))

        # Mental metrics on a 1-10 scale, loosely coupled to physical state.
        stress = float(np.clip(base_stress + 0.04 * (load - 60) - 0.05 * (recovery - 65) + rng.normal(0, 0.8), 1, 10))
        focus = float(np.clip(8.0 - 0.4 * (stress - 4) + 0.02 * (recovery - 65) + rng.normal(0, 0.7), 1, 10))
        confidence = float(np.clip(7.0 + 0.03 * (recovery - 65) - 0.3 * (stress - 4) + rng.normal(0, 0.7), 1, 10))
        motivation = float(np.clip(base_motivation - 0.2 * (stress - 4) + rng.normal(0, 0.7), 1, 10))

        rows.append({
            "date": dates[i],
            "training_load": round(load, 1),
            "sleep_hours": round(sleep, 1),
            "hrv": round(hrv, 1),
            "resting_hr": round(rhr, 1),
            "recovery_score": round(recovery, 1),
            "stress": round(stress, 1),
            "focus": round(focus, 1),
            "confidence": round(confidence, 1),
            "motivation": round(motivation, 1),
        })

    df = pd.DataFrame(rows)
    df["readiness"] = _compute_readiness(df)
    df["source"] = "Generated"
    return df


def _compute_readiness(df: pd.DataFrame) -> pd.Series:
    """Composite readiness 0-100 from recovery, sleep, hrv and (inverse) stress."""
    sleep_score = np.clip((df["sleep_hours"] / 8.0) * 100, 0, 100)
    hrv_score = np.clip((df["hrv"] / 100.0) * 100, 0, 100)
    stress_score = np.clip((10 - df["stress"]) / 10.0 * 100, 0, 100)
    readiness = (0.45 * df["recovery_score"] + 0.20 * sleep_score
                 + 0.20 * hrv_score + 0.15 * stress_score)
    return readiness.round(1)


@st.cache_data(show_spinner=False)
def get_history(athlete_id: str) -> pd.DataFrame:
    """Cached base history for an athlete (generated once per session)."""
    athlete = get_athlete(athlete_id)
    return _generate_series(athlete)


# ----------------------------------------------------------------------------
# Manual entries (athlete-logged) merged on top of generated history
# ----------------------------------------------------------------------------

def _manual_store():
    if "manual_entries" not in st.session_state:
        st.session_state["manual_entries"] = {}
    return st.session_state["manual_entries"]


def add_manual_entry(athlete_id: str, entry: dict):
    """Store a manually logged day for an athlete in session state."""
    store = _manual_store()
    store.setdefault(athlete_id, [])
    store[athlete_id].append(entry)


def get_combined_history(athlete_id: str) -> pd.DataFrame:
    """Generated history with any manually-logged entries overlaid by date."""
    df = get_history(athlete_id).copy()
    manual = _manual_store().get(athlete_id, [])
    if not manual:
        return df

    mdf = pd.DataFrame(manual)
    mdf["readiness"] = _compute_readiness(mdf)
    mdf["source"] = "Manual"

    combined = pd.concat([df, mdf], ignore_index=True)
    # Keep the latest record per date (manual overrides generated).
    combined = combined.sort_values(["date", "source"]).drop_duplicates("date", keep="last")
    combined = combined.sort_values("date").reset_index(drop=True)
    return combined


def latest_metrics(athlete_id: str) -> dict:
    df = get_combined_history(athlete_id)
    return df.iloc[-1].to_dict()
