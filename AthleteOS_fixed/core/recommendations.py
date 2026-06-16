"""
AthleteOS - rule-based recommendation engine.

Generates clear, evidence-style guidance from an athlete's latest metrics and
recent trends. No external API required. Each recommendation has a severity
that drives its colour in the UI.
"""

from __future__ import annotations
import pandas as pd

from core.theme import COLORS

SEV_COLOR = {
    "critical": COLORS["danger"],
    "warning": COLORS["yellow"],
    "good": COLORS["primary"],
    "info": COLORS["blue"],
}


def _trend(df: pd.DataFrame, column: str, window: int = 7) -> float:
    """Return change of a column's mean over the last `window` days vs the prior window."""
    if len(df) < window * 2:
        return 0.0
    recent = df[column].tail(window).mean()
    prior = df[column].tail(window * 2).head(window).mean()
    return float(recent - prior)


def athlete_recommendations(df: pd.DataFrame) -> list[dict]:
    """Recommendations shown on the ATHLETE dashboard."""
    last = df.iloc[-1]
    recs: list[dict] = []

    readiness = last["readiness"]
    if readiness < 45:
        recs.append({
            "severity": "critical",
            "title": "Prioritise recovery today",
            "text": f"Your readiness is <b>{readiness:.0f}/100</b>. Swap today's high-intensity work "
                    "for active recovery, mobility, or a full rest day.",
        })
    elif readiness < 65:
        recs.append({
            "severity": "warning",
            "title": "Train smart, not hard",
            "text": f"Readiness is moderate at <b>{readiness:.0f}/100</b>. Keep intensity controlled "
                    "and cap session volume to protect adaptation.",
        })
    else:
        recs.append({
            "severity": "good",
            "title": "Green light for quality work",
            "text": f"Readiness is strong at <b>{readiness:.0f}/100</b>. This is a good window for a "
                    "key session or testing a personal benchmark.",
        })

    if last["sleep_hours"] < 6.5:
        recs.append({
            "severity": "warning",
            "title": "Protect your sleep",
            "text": f"Last logged sleep was <b>{last['sleep_hours']:.1f}h</b>. Aim for 8h tonight; "
                    "sleep debt is the fastest way to drop sprint output and focus.",
        })

    if last["stress"] >= 7:
        recs.append({
            "severity": "warning",
            "title": "Down-regulate stress",
            "text": f"Stress is elevated at <b>{last['stress']:.0f}/10</b>. Try 5 minutes of slow "
                    "breathing before training and after your evening check-in.",
        })

    hrv_trend = _trend(df, "hrv")
    if hrv_trend < -6:
        recs.append({
            "severity": "warning",
            "title": "HRV trending down",
            "text": f"Your 7-day HRV is down <b>{abs(hrv_trend):.0f} ms</b>. This often precedes "
                    "fatigue \u2014 add an easy day this week.",
        })
    elif hrv_trend > 6:
        recs.append({
            "severity": "good",
            "title": "Recovery is improving",
            "text": f"HRV is up <b>{hrv_trend:.0f} ms</b> over the last week \u2014 your body is "
                    "adapting well to the current load.",
        })

    if last["confidence"] < 5:
        recs.append({
            "severity": "info",
            "title": "Confidence dip detected",
            "text": f"Confidence is at <b>{last['confidence']:.0f}/10</b>. Revisit recent wins and "
                    "consider flagging this to your coach or psychologist.",
        })

    return recs


def coach_squad_recommendations(squad: list[dict]) -> list[dict]:
    """
    Squad-level recommendations for the COACH dashboard.
    `squad` is a list of dicts: {athlete, df, latest}.
    """
    recs: list[dict] = []

    at_risk = [s for s in squad if s["latest"]["readiness"] < 50]
    monitor = [s for s in squad if 50 <= s["latest"]["readiness"] < 65]
    high_stress = [s for s in squad if s["latest"]["stress"] >= 7]
    ready = [s for s in squad if s["latest"]["readiness"] >= 75]

    if at_risk:
        names = ", ".join(s["athlete"]["name"] for s in at_risk)
        recs.append({
            "severity": "critical",
            "title": "Overtraining risk \u2014 intervene now",
            "text": f"<b>{names}</b> {'is' if len(at_risk)==1 else 'are'} below 50 readiness. "
                    "Reduce load and check in directly before the next hard session.",
        })

    if high_stress:
        names = ", ".join(s["athlete"]["name"] for s in high_stress)
        recs.append({
            "severity": "warning",
            "title": "Elevated mental load",
            "text": f"<b>{names}</b> reported stress \u2265 7/10. Consider a lighter mental cue, "
                    "shorter session, or a brief 1:1.",
        })

    if monitor:
        recs.append({
            "severity": "info",
            "title": "Hold steady & monitor",
            "text": f"<b>{len(monitor)}</b> athlete(s) are in the moderate band. Keep intensity "
                    "controlled and re-check readiness tomorrow morning.",
        })

    if ready:
        names = ", ".join(s["athlete"]["name"] for s in ready)
        recs.append({
            "severity": "good",
            "title": "Primed for key work",
            "text": f"<b>{names}</b> {'is' if len(ready)==1 else 'are'} highly recovered \u2014 a good "
                    "window to schedule quality or benchmark sessions.",
        })

    if not recs:
        recs.append({
            "severity": "good",
            "title": "Squad is balanced",
            "text": "No readiness or stress flags across the squad today. Maintain the current plan.",
        })

    return recs
