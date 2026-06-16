"""AthleteOS - shared UI components (the standout recommendations box)."""

from __future__ import annotations
import streamlit as st

from core.recommendations import SEV_COLOR


def render_recommendations(recs: list[dict], subtitle: str = ""):
    """Render the branded, eye-catching 'AthleteOS Recommendations' panel."""
    items_html = ""
    for r in recs:
        color = SEV_COLOR.get(r["severity"], "#00E676")
        items_html += (
            f'<div class="aos-rec-item">'
            f'<span class="dot" style="background:{color}"></span>'
            f'<span class="body"><b>{r["title"]}</b><br>{r["text"]}</span>'
            f'</div>'
        )

    sub = f'<div class="aos-muted" style="margin:-4px 0 8px;font-size:0.86rem">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="aos-rec">
            <div class="aos-rec-title">
                <span>AthleteOS Recommendations</span>
                <span class="aos-rec-pill">AI&nbsp;INSIGHTS</span>
            </div>
            {sub}
            {items_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
