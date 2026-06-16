"""AthleteOS - Coach dashboard view. Squad is single-sport by construction."""

from __future__ import annotations
import streamlit as st

from core import data, charts
from core.theme import hero, section_title, COLORS, device_badge
from core.recommendations import coach_squad_recommendations
from core.ui import render_recommendations


def _build_squad(coach_id: str):
    squad = []
    for a in data.get_athletes_for_coach(coach_id):
        df = data.get_combined_history(a["id"])
        squad.append({"athlete": a, "df": df, "latest": df.iloc[-1].to_dict()})
    return squad


def _status_color(readiness: float) -> str:
    if readiness >= 75:
        return COLORS["primary"]
    if readiness >= 55:
        return COLORS["yellow"]
    return COLORS["danger"]


def _alerts(squad):
    section_title("Recovery & overtraining alerts")
    flagged = [s for s in squad if s["latest"]["readiness"] < 50 or s["latest"]["stress"] >= 7]
    if not flagged:
        st.markdown(
            '<div class="aos-card" style="border-color:rgba(0,230,118,0.4)">'
            '<b style="color:#00E676">All clear.</b> No athletes crossed the alert thresholds today.</div>',
            unsafe_allow_html=True,
        )
        return
    for s in flagged:
        a = s["athlete"]
        last = s["latest"]
        reason = []
        if last["readiness"] < 50:
            reason.append(f"readiness {last['readiness']:.0f}")
        if last["stress"] >= 7:
            reason.append(f"stress {last['stress']:.0f}/10")
        st.markdown(
            f'<div class="aos-card" style="border-color:rgba(255,84,112,0.5)">'
            f'<b style="color:#FF5470">⚠ {a["name"]}</b> '
            f'<span class="aos-muted">— {", ".join(reason)}. Recommend reduced load + direct check-in.</span></div>',
            unsafe_allow_html=True,
        )


def _squad_table(squad):
    section_title("Squad overview")
    rows = []
    for s in squad:
        a, last = s["athlete"], s["latest"]
        rows.append({
            "Athlete": a["name"],
            "Readiness": round(last["readiness"]),
            "Recovery": round(last["recovery_score"]),
            "Sleep (h)": round(last["sleep_hours"], 1),
            "Stress": round(last["stress"]),
            "Motivation": round(last["motivation"]),
            "Device": a["wearable"] or "—",
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)


def render(coach_id: str):
    coach = data.get_coach(coach_id)
    squad = _build_squad(coach_id)

    hero(
        f"{coach['name']}'s Squad",
        f"{coach['sport']} program · {len(squad)} athletes · all {coach['sport'].lower()} specialists",
    )

    # Reinforce that every athlete shown shares the coach's sport.
    st.markdown(
        f'<p class="aos-muted">Showing only your <b style="color:#fff">{coach["sport"]}</b> athletes. '
        'Squads in AthleteOS are sport-specific.</p>',
        unsafe_allow_html=True,
    )

    avg_ready = sum(s["latest"]["readiness"] for s in squad) / len(squad)
    n_risk = sum(1 for s in squad if s["latest"]["readiness"] < 50)
    n_ready = sum(1 for s in squad if s["latest"]["readiness"] >= 75)
    connected = sum(1 for s in squad if s["athlete"]["wearable"])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Squad readiness", f"{avg_ready:.0f}/100")
    k2.metric("At-risk athletes", n_risk)
    k3.metric("Primed for quality", n_ready)
    k4.metric("Devices connected", f"{connected}/{len(squad)}")
    st.write("")

    # Standout recommendations box.
    recs = coach_squad_recommendations(squad)
    render_recommendations(recs, subtitle=f"Squad-level guidance for {coach['name']} · {coach['sport']}")

    tabs = st.tabs(["Squad", "Alerts", "Correlation analytics", "Athlete detail"])

    with tabs[0]:
        st.plotly_chart(charts.squad_readiness_bar(squad), use_container_width=True)
        _squad_table(squad)

    with tabs[1]:
        _alerts(squad)

    with tabs[2]:
        section_title("How mental state relates to physical output")
        st.markdown(
            '<p class="aos-muted">Each point is one athlete-day across your squad, '
            'coloured by readiness.</p>', unsafe_allow_html=True,
        )
        import pandas as pd
        combined = pd.concat([s["df"] for s in squad], ignore_index=True)
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                charts.correlation_scatter(combined, "stress", "recovery_score",
                                           "Stress (1-10)", "Recovery score"),
                use_container_width=True,
            )
        with c2:
            st.plotly_chart(
                charts.correlation_scatter(combined, "sleep_hours", "readiness",
                                           "Sleep (h)", "Readiness"),
                use_container_width=True,
            )
        corr = combined[["sleep_hours", "stress", "hrv", "recovery_score", "readiness"]].corr()["readiness"]
        section_title("Correlation with readiness")
        st.dataframe(
            [{"Metric": k, "Correlation w/ readiness": round(v, 2)}
             for k, v in corr.items() if k != "readiness"],
            use_container_width=True, hide_index=True,
        )

    with tabs[3]:
        names = {s["athlete"]["name"]: s for s in squad}
        pick = st.selectbox("Select an athlete", list(names.keys()))
        s = names[pick]
        st.markdown(device_badge(s["athlete"]["wearable"]), unsafe_allow_html=True)
        st.write("")
        a, b = st.columns([1, 1.4])
        with a:
            st.plotly_chart(charts.readiness_gauge(s["latest"]["readiness"]), use_container_width=True)
        with b:
            st.plotly_chart(charts.readiness_trend(s["df"]), use_container_width=True)
        st.plotly_chart(charts.physical_chart(s["df"]), use_container_width=True)
        st.plotly_chart(charts.mental_trend(s["df"]), use_container_width=True)
