# AthleteOS

**The Athlete Performance Intelligence Platform** — a Streamlit mock-up that unifies an athlete's *physical* and *mental* performance data into one decision surface for athletes and coaches.

Built to run with **zero external services** (all data is generated in-app) so it deploys cleanly to **GitHub + Streamlit Community Cloud**.

---

## Features

- **Mock login** with preset coach & athlete accounts (no real auth).
- **Athlete dashboard**
  - Unified readiness, recovery, sleep, HRV, resting HR + mental metrics.
  - **Connected wearable status** (WHOOP / Garmin / Apple Watch / Polar) — shown only for athletes who have connected a device; others log manually.
  - **Manual entry** of *both* physical and mental metrics — updates the dashboard instantly.
  - Readiness gauge, training-load vs recovery, sleep/HRV, mental radar & trends.
- **Coach dashboard**
  - Squad is **single-sport** — a coach only ever sees athletes of their own sport.
  - Squad readiness ranking, overtraining/stress alerts, correlation analytics, per-athlete detail.
- **AthleteOS Recommendations** — a standout, branded box on both dashboards, with rule-based guidance derived from the latest metrics.
- Modern, sporty dark theme with bright, high-contrast text and clean, non-overlapping charts.

## Demo accounts

| Role | Usernames | Password |
|------|-----------|----------|
| Coaches | `maria` (Sprinting), `david` (Swimming), `tara` (Basketball), `leo` (Cycling) | `coach123` |
| Athletes | `alex`, `jordan`, `sam`, `nina`, `mia`, `omar`, `lena`, `andre`, `kiara`, `tom`, `eva`, `raj`, `finn` | `athlete123` |

Athletes **with** a connected wearable: `alex`, `jordan`, `mia`, `omar`, `andre`, `eva`, `raj`. The rest log manually.

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open http://localhost:8501

## Deploy to Streamlit Community Cloud

1. Push this folder to a **GitHub repository**.
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **New app**, pick your repo/branch, and set the main file to **`streamlit_app.py`**.
4. Click **Deploy**. Streamlit installs `requirements.txt` automatically.

The theme is pre-configured in `.streamlit/config.toml`.

---

## Project structure

```
streamlit_app.py        # entry point: login + routing + sidebar
requirements.txt
.streamlit/config.toml   # dark sporty theme
assets/athleteos_logo.png
core/
  data.py               # in-app mock data (athletes, coaches, 60-day metrics)
  theme.py              # CSS, palette, UI helpers
  recommendations.py    # rule-based AthleteOS recommendations
  charts.py             # Plotly charts
  ui.py                 # recommendations panel renderer
views/
  athlete.py            # athlete dashboard
  coach.py              # coach dashboard
```

> This is a mock-up / prototype based on the APIP PRD v1.0. Data is synthetic and for demonstration only.
