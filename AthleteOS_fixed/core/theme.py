"""AthleteOS - global styling, colour palette and reusable UI helpers."""

from __future__ import annotations
import streamlit as st

# Core palette -- dark, modern, sporty. Bright text everywhere for visibility.
COLORS = {
    "bg": "#0B0F1A",
    "surface": "#151B2B",
    "surface_2": "#1E2740",
    "text": "#F5F7FA",
    "muted": "#AEB8CC",
    "primary": "#00E676",   # electric green
    "accent": "#FF6B35",    # energetic orange
    "blue": "#29B6F6",
    "yellow": "#FFD23F",
    "danger": "#FF5470",
    "ok": "#00E676",
    "warn": "#FFD23F",
}

# Plotly template colours used by charts.py
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#F5F7FA", size=13, family="Inter, sans-serif"),
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#F5F7FA")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.15)",
               tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.15)",
               tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
)


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

        .stApp {
            background:
                radial-gradient(1200px 600px at 100% -10%, rgba(0,230,118,0.10), transparent 60%),
                radial-gradient(900px 500px at -10% 10%, rgba(255,107,53,0.10), transparent 55%),
                #0B0F1A;
        }

        h1, h2, h3, h4 { font-family: 'Sora', sans-serif; color: #F5F7FA !important; letter-spacing: -0.01em; }
        p, span, label, li { color: #F5F7FA; }

        /* Selectbox fixes for Streamlit Cloud */
        div[data-baseweb="select"], div[data-baseweb="select"] * { color:#FFFFFF !important; }
        ul[role="listbox"], ul[role="listbox"] li { background:#151B2B !important; color:#FFFFFF !important; }


        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #121829 0%, #0B0F1A 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, #1A2236 0%, #151B2B 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.35);
        }
        div[data-testid="stMetricLabel"] p { color: #AEB8CC !important; font-weight: 600; }
        div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 800; }

        /* Tabs */
        button[data-baseweb="tab"] { font-weight: 700; }
        .stTabs [aria-selected="true"] { color: #00E676 !important; }

        /* Buttons */
        .stButton > button {
            border-radius: 12px; font-weight: 700; border: 1px solid rgba(0,230,118,0.4);
            background: linear-gradient(90deg, #00E676, #00C2A8); color: #06210F;
        }
        .stButton > button:hover { filter: brightness(1.08); border-color: #00E676; color:#06210F; }

        /* Generic card */
        .aos-card {
            background: linear-gradient(180deg, #1A2236 0%, #151B2B 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px; padding: 20px 22px; margin-bottom: 14px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }

        /* Hero header */
        .aos-hero {
            background: linear-gradient(120deg, rgba(0,230,118,0.18), rgba(255,107,53,0.16));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 22px; padding: 26px 30px; margin-bottom: 18px;
        }
        .aos-hero h1 { margin: 0; font-size: 2.0rem; }
        .aos-hero p  { margin: 6px 0 0; color: #DCE3F0; font-size: 1.02rem; }

        /* Recommendation box -- made to POP */
        .aos-rec {
            border-radius: 18px; padding: 18px 20px; margin: 10px 0 16px;
            border: 1px solid rgba(0,230,118,0.45);
            background: linear-gradient(135deg, rgba(0,230,118,0.16), rgba(41,182,246,0.10));
            box-shadow: 0 0 0 1px rgba(0,230,118,0.15), 0 10px 30px rgba(0,230,118,0.12);
        }
        .aos-rec-title {
            display:flex; align-items:center; gap:10px;
            font-family:'Sora',sans-serif; font-weight:800; font-size:1.05rem;
            color:#00E676; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;
        }
        .aos-rec-pill {
            background:#00E676; color:#06210F; font-weight:800; font-size:0.7rem;
            padding:3px 10px; border-radius:999px; letter-spacing:0.08em;
        }
        .aos-rec-item {
            display:flex; gap:12px; align-items:flex-start;
            padding:12px 14px; margin:8px 0; border-radius:12px;
            background: rgba(11,15,26,0.55); border:1px solid rgba(255,255,255,0.08);
        }
        .aos-rec-item .dot { width:10px; height:10px; border-radius:50%; margin-top:6px; flex:0 0 auto; }
        .aos-rec-item .body { color:#F5F7FA; }
        .aos-rec-item .body b { color:#FFFFFF; }
        .aos-rec-item .body small { color:#AEB8CC; }

        /* Badges / chips */
        .aos-chip {
            display:inline-flex; align-items:center; gap:8px;
            padding:6px 12px; border-radius:999px; font-weight:700; font-size:0.82rem;
            border:1px solid rgba(255,255,255,0.14); background: rgba(255,255,255,0.04); color:#F5F7FA;
        }
        .aos-chip .dot { width:8px;height:8px;border-radius:50%; }

        .aos-device {
            display:inline-flex; align-items:center; gap:10px;
            padding:8px 14px; border-radius:12px; font-weight:700;
            border:1px solid rgba(41,182,246,0.5);
            background: linear-gradient(90deg, rgba(41,182,246,0.18), rgba(0,230,118,0.10));
            color:#EAF6FF;
        }
        .aos-device.off { border-color: rgba(255,255,255,0.14); background: rgba(255,255,255,0.03); color:#AEB8CC; }

        .aos-muted { color:#AEB8CC !important; }
        .aos-section-title { font-family:'Sora',sans-serif; font-weight:800; color:#FFFFFF; font-size:1.15rem; margin:6px 0 4px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    st.markdown(
        f"""<div class="aos-hero"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def chip(label: str, color: str) -> str:
    return f'<span class="aos-chip"><span class="dot" style="background:{color}"></span>{label}</span>'


def device_badge(wearable):
    if wearable:
        return (f'<span class="aos-device"><span style="font-weight:800">●</span> '
                f'Connected device&nbsp;·&nbsp;<b style="color:#fff">{wearable}</b> &nbsp;·&nbsp; Syncing</span>')
    return ('<span class="aos-device off"><span>○</span> No wearable connected '
            '&nbsp;·&nbsp; manual logging only</span>')


def section_title(text: str):
    st.markdown(f'<div class="aos-section-title">{text}</div>', unsafe_allow_html=True)
