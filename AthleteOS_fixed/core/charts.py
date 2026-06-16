"""AthleteOS - Plotly chart builders with bright, readable, non-overlapping styling."""

from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go

from core.theme import COLORS, PLOTLY_LAYOUT


def _base(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#FFFFFF")),
        height=320,
        hovermode="x unified",
    )
    return fig


def readiness_gauge(value: float) -> go.Figure:
    if value >= 75:
        color = COLORS["primary"]
    elif value >= 55:
        color = COLORS["yellow"]
    else:
        color = COLORS["danger"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"color": "#FFFFFF", "size": 40}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#AEB8CC", "tickfont": {"color": "#D6DEEC"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(255,255,255,0.04)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 55], "color": "rgba(255,84,112,0.18)"},
                {"range": [55, 75], "color": "rgba(255,210,63,0.18)"},
                {"range": [75, 100], "color": "rgba(0,230,118,0.18)"},
            ],
        },
    ))
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_layout(height=240, margin=dict(l=20, r=20, t=20, b=10))
    return fig


def readiness_trend(df: pd.DataFrame) -> go.Figure:
    fig = _base("Readiness \u2014 last 30 days")
    d = df.tail(30)
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["readiness"], mode="lines",
        line=dict(color=COLORS["primary"], width=3),
        fill="tozeroy", fillcolor="rgba(0,230,118,0.12)", name="Readiness",
    ))
    fig.update_yaxes(range=[0, 100], title="Readiness")
    return fig


def physical_chart(df: pd.DataFrame) -> go.Figure:
    """Training load (bars) vs recovery score (line) on dual axes."""
    fig = _base("Training load vs recovery")
    d = df.tail(30)
    fig.add_trace(go.Bar(
        x=d["date"], y=d["training_load"], name="Training load",
        marker_color="rgba(255,107,53,0.85)",
    ))
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["recovery_score"], name="Recovery", yaxis="y2",
        mode="lines+markers", line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=5),
    ))
    fig.update_layout(
        yaxis=dict(title="Load (AU)", range=[0, 110], gridcolor="rgba(255,255,255,0.08)",
                   tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
        yaxis2=dict(title="Recovery", overlaying="y", side="right", range=[0, 110],
                    showgrid=False, tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
        legend=dict(orientation="h", y=1.12, x=0),
    )
    return fig


def sleep_hrv_chart(df: pd.DataFrame) -> go.Figure:
    fig = _base("Sleep & HRV")
    d = df.tail(30)
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["sleep_hours"], name="Sleep (h)",
        mode="lines", line=dict(color=COLORS["blue"], width=3),
    ))
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["hrv"], name="HRV (ms)", yaxis="y2",
        mode="lines", line=dict(color=COLORS["yellow"], width=3),
    ))
    fig.update_layout(
        yaxis=dict(title="Sleep (h)", range=[0, 10], gridcolor="rgba(255,255,255,0.08)",
                   tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
        yaxis2=dict(title="HRV (ms)", overlaying="y", side="right",
                    showgrid=False, tickfont=dict(color="#D6DEEC"), title_font=dict(color="#F5F7FA")),
        legend=dict(orientation="h", y=1.12, x=0),
    )
    return fig


def mental_radar(df: pd.DataFrame) -> go.Figure:
    last = df.iloc[-1]
    cats = ["Stress (inv)", "Focus", "Confidence", "Motivation"]
    vals = [10 - last["stress"], last["focus"], last["confidence"], last["motivation"]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]], fill="toself",
        line=dict(color=COLORS["primary"], width=3),
        fillcolor="rgba(0,230,118,0.18)", name="Today",
    ))
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_layout(
        title=dict(text="Mental state (today)", font=dict(size=16, color="#FFFFFF")),
        height=320,
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(range=[0, 10], gridcolor="rgba(255,255,255,0.12)",
                            tickfont=dict(color="#D6DEEC")),
            angularaxis=dict(tickfont=dict(color="#F5F7FA")),
        ),
        showlegend=False,
    )
    return fig


def mental_trend(df: pd.DataFrame) -> go.Figure:
    fig = _base("Mental metrics \u2014 last 30 days")
    d = df.tail(30)
    series = [
        ("focus", COLORS["primary"], "Focus"),
        ("confidence", COLORS["blue"], "Confidence"),
        ("motivation", COLORS["yellow"], "Motivation"),
        ("stress", COLORS["danger"], "Stress"),
    ]
    for col, color, label in series:
        fig.add_trace(go.Scatter(
            x=d["date"], y=d[col], name=label, mode="lines",
            line=dict(color=color, width=2.5),
        ))
    fig.update_yaxes(range=[0, 10], title="Score (1-10)")
    fig.update_layout(legend=dict(orientation="h", y=1.14, x=0))
    return fig


def correlation_scatter(df: pd.DataFrame, x: str, y: str, xlabel: str, ylabel: str) -> go.Figure:
    fig = _base(f"{xlabel} vs {ylabel}")
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y], mode="markers",
        marker=dict(size=9, color=df["readiness"], colorscale="Tealgrn",
                    showscale=True, colorbar=dict(title="Readiness", tickfont=dict(color="#D6DEEC"),
                                                  title_font=dict(color="#F5F7FA"))),
        name="Days",
    ))
    fig.update_xaxes(title=xlabel)
    fig.update_yaxes(title=ylabel)
    return fig


def squad_readiness_bar(squad: list[dict]) -> go.Figure:
    names = [s["athlete"]["name"] for s in squad]
    vals = [s["latest"]["readiness"] for s in squad]
    colors = [COLORS["primary"] if v >= 75 else COLORS["yellow"] if v >= 55 else COLORS["danger"]
              for v in vals]
    fig = _base("Squad readiness today")
    fig.add_trace(go.Bar(
        x=vals, y=names, orientation="h",
        marker_color=colors,
        text=[f"{v:.0f}" for v in vals], textposition="outside",
        textfont=dict(color="#FFFFFF", size=13),
    ))
    fig.update_xaxes(range=[0, 110], title="Readiness")
    fig.update_layout(height=max(260, 52 * len(squad)))
    return fig
