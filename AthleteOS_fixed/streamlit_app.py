"""
AthleteOS - Athlete Performance Intelligence Platform (mock-up).

A Streamlit demo that unifies physical + mental performance data for athletes
and coaches. Built for GitHub + Streamlit Community Cloud hosting.

Run locally:   streamlit run streamlit_app.py
"""

from __future__ import annotations
import os
import streamlit as st

from core import data
from core.theme import inject_css, COLORS
from views import athlete as athlete_view
from views import coach as coach_view

st.set_page_config(
    page_title="AthleteOS",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "athleteos_logo.png")
LOGIN = data.build_login_table()


# ----------------------------------------------------------------------------
# Auth helpers
# ----------------------------------------------------------------------------

def _authenticate(username: str, password: str) -> bool:
    user = LOGIN.get(username.strip().lower())
    if user and user["password"] == password:
        st.session_state["auth"] = {
            "username": username.strip().lower(),
            "role": user["role"],
            "id": user["id"],
            "name": user["name"],
        }
        return True
    return False


def _logout():
    st.session_state.pop("auth", None)
    st.rerun()


# ----------------------------------------------------------------------------
# Login screen
# ----------------------------------------------------------------------------

def login_screen():
    left, mid, right = st.columns([1, 1.4, 1])
    with mid:
        if os.path.exists(LOGO_PATH):
            lc1, lc2, lc3 = st.columns([1, 1, 1])
            with lc2:
                st.image(LOGO_PATH, width=120)
        st.markdown(
            """
            <div style="text-align:center; margin-top:-6px">
                <h1 style="font-size:2.6rem; margin-bottom:0; background:linear-gradient(90deg,#00E676,#29B6F6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">AthleteOS</h1>
                <p style="color:#AEB8CC; font-size:1.05rem; margin-top:4px;">
                    The Athlete Performance Intelligence Platform — one view for body & mind.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown('<div class="aos-card">', unsafe_allow_html=True)
            st.markdown("#### Sign in")
            username = st.text_input("Username", placeholder="e.g. alex or maria")
            password = st.text_input("Password", type="password", placeholder="athlete123 / coach123")
            if st.button("Log in", use_container_width=True):
                if _authenticate(username, password):
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try a demo account below.")
            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Demo accounts (mock login)"):
            st.markdown("**Coaches** — password `coach123`")
            st.markdown(
                " · ".join(f"`{c['username']}` ({c['sport']})" for c in data.get_coaches())
            )
            st.markdown("**Athletes** — password `athlete123`")
            st.markdown(
                " · ".join(f"`{a['username']}`" for a in data.get_athletes())
            )
            st.caption("Some athletes (e.g. alex, jordan, mia, omar, andre, eva, raj) have a "
                       "connected wearable; others log manually.")


# ----------------------------------------------------------------------------
# Authenticated shell
# ----------------------------------------------------------------------------

def app_shell():
    auth = st.session_state["auth"]

    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=84)
        st.markdown(
            f"""<div style="margin-top:-4px">
            <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:1.4rem;
                background:linear-gradient(90deg,#00E676,#29B6F6);-webkit-background-clip:text;
                -webkit-text-fill-color:transparent;">AthleteOS</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.divider()
        role_label = "Coach" if auth["role"] == "coach" else "Athlete"
        st.markdown(
            f'<span class="aos-chip"><span class="dot" style="background:{COLORS["primary"]}"></span>'
            f'{role_label}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"#### {auth['name']}")

        if auth["role"] == "athlete":
            a = data.get_athlete(auth["id"])
            c = data.get_coach(a["coach_id"])
            st.caption(f"{a['sport']} · {c['name']}")
        else:
            c = data.get_coach(auth["id"])
            st.caption(f"{c['sport']} program")

        st.divider()
        st.caption("AthleteOS v1.0 — mock-up build")
        if st.button("Log out", use_container_width=True):
            _logout()

    if auth["role"] == "athlete":
        athlete_view.render(auth["id"])
    else:
        coach_view.render(auth["id"])


# ----------------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------------

if "auth" not in st.session_state:
    login_screen()
else:
    app_shell()
