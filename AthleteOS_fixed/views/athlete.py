"""AthleteOS - Athlete dashboard view."""

from __future__ import annotations
import datetime as _dt
import streamlit as st

from core import data
from core.theme import hero, device_badge, section_title, COLORS, chip
from core.recommendations import athlete_recommendations
from core.ui import render_recommendations
from core import charts


def _kpi_row(last: dict):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Readiness", f"{last['readiness']:.0f}/100")
    c2.metric("Recovery", f"{last['recovery_score']:.0f}", help="Composite physiological recovery")
    c3.metric("Sleep", f"{last['sleep_hours']:.1f} h")
    c4.metric("Stress", f"{last['stress']:.0f}/10")
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("HRV", f"{last['hrv']:.0f} ms")
    c6.metric("Resting HR", f"{last['resting_hr']:.0f} bpm")
    c7.metric("Focus", f"{last['focus']:.0f}/10")
    c8.metric("Motivation", f"{last['motivation']:.0f}/10")


def _manual_entry_form(athlete_id: str):
    section_title("Log today's metrics")
    st.markdown(
        '<p class="aos-muted">Manually enter your physical and mental metrics. '
        'Entries instantly update your dashboard, trends and recommendations.</p>',
        unsafe_allow_html=True,
    )

    with st.form("manual_entry", clear_on_submit=False):
        st.markdown("**Physical**")
        p1, p2, p3 = st.columns(3)
        entry_date = p1.date_input("Date", value=_dt.date.today())
        training_load = p2.slider("Training load (AU)", 0, 100, 60)
        sleep_hours = p3.slider("Sleep (hours)", 0.0, 12.0, 7.5, 0.1)
        p4, p5, p6 = st.columns(3)
        hrv = p4.slider("HRV (ms)", 20, 140, 70)
        resting_hr = p5.slider("Resting HR (bpm)", 35, 90, 52)
        recovery_score = p6.slider("Recovery score", 0, 100, 65)

        st.markdown("**Mental**")
        m1, m2, m3, m4 = st.columns(4)
        stress = m1.slider("Stress", 1, 10, 4)
        focus = m2.slider("Focus", 1, 10, 7)
        confidence = m3.slider("Confidence", 1, 10, 7)
        motivation = m4.slider("Motivation", 1, 10, 8)

        submitted = st.form_submit_button("Save entry")
        if submitted:
            data.add_manual_entry(athlete_id, {
                "date": entry_date,
                "training_load": float(training_load),
                "sleep_hours": float(sleep_hours),
                "hrv": float(hrv),
                "resting_hr": float(resting_hr),
                "recovery_score": float(recovery_score),
                "stress": float(stress),
                "focus": float(focus),
                "confidence": float(confidence),
                "motivation": float(motivation),
            })
            st.success(f"Saved metrics for {entry_date:%b %d}. Dashboard updated.")
            st.rerun()


def render(athlete_id: str):
    athlete = data.get_athlete(athlete_id)
    coach = data.get_coach(athlete["coach_id"])
    df = data.get_combined_history(athlete_id)
    last = df.iloc[-1].to_dict()

    hero(
        f"Welcome back, {athlete['name'].split()[0]}",
        f"{athlete['sport']} · Coached by {coach['name']} · Age {athlete['age']}",
    )

    # Wearable / external device connection status -- only some athletes have one.
    st.markdown(device_badge(athlete["wearable"]), unsafe_allow_html=True)
    st.write("")

    # Recommendations -- standout box right at the top of the athlete view.
    recs = athlete_recommendations(df)
    render_recommendations(recs, subtitle=f"Personalised for {athlete['name']} · based on your latest readiness & check-in")

    tabs = st.tabs(["Overview", "Physical", "Mental", "Log metrics"])

    with tabs[0]:
        _kpi_row(last)
        st.write("")
        a, b = st.columns([1, 1.4])
        with a:
            section_title("Readiness")
            st.plotly_chart(charts.readiness_gauge(last["readiness"]), use_container_width=True)
        with b:
            st.plotly_chart(charts.readiness_trend(df), use_container_width=True)

    with tabs[1]:
        st.plotly_chart(charts.physical_chart(df), use_container_width=True)
        st.plotly_chart(charts.sleep_hrv_chart(df), use_container_width=True)

    with tabs[2]:
        a, b = st.columns([1, 1.2])
        with a:
            st.plotly_chart(charts.mental_radar(df), use_container_width=True)
        with b:
            st.plotly_chart(charts.mental_trend(df), use_container_width=True)

    with tabs[3]:
        _manual_entry_form(athlete_id)
        manual = st.session_state.get("manual_entries", {}).get(athlete_id, [])
        if manual:
            section_title("Your manual entries this session")
            st.dataframe(
                [{"Date": m["date"], "Load": m["training_load"], "Sleep": m["sleep_hours"],
                  "Stress": m["stress"], "Focus": m["focus"]} for m in manual],
                use_container_width=True, hide_index=True,
            )
