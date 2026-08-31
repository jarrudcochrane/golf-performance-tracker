"""
dashboard.py

Interactive Streamlit dashboard for the golf performance tracker.

Reuses the data loading and stat-derivation logic from golf_analysis.py so
the console script and the dashboard always agree on the numbers, then adds
filtering, interactive Plotly charts, and a form for logging new rounds
straight from the browser.

Usage:
    streamlit run dashboard.py
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from golf_analysis import (
    DATA_PATH,
    ROLLING_WINDOW,
    compute_trend,
    derive_stats,
    estimate_handicap_index,
    load_data,
)

st.set_page_config(page_title="Golf Performance Tracker", page_icon="⛳", layout="wide")


@st.cache_data
def get_data() -> pd.DataFrame:
    """Load and derive stats for all logged rounds, cached across reruns."""
    return derive_stats(load_data())


def add_round(new_row: dict) -> None:
    """Append a new round to the CSV on disk and clear the data cache.

    Args:
        new_row: Mapping of raw CSV column names to values for one round.
    """
    df_raw = pd.read_csv(DATA_PATH)
    df_raw = pd.concat([df_raw, pd.DataFrame([new_row])], ignore_index=True)
    df_raw.to_csv(DATA_PATH, index=False)
    get_data.clear()


def main() -> None:
    st.title("⛳ Golf Performance Tracker")
    st.caption("Personal round log — filter, explore, and log new rounds below.")

    df = get_data()

    # ---- Sidebar filters -------------------------------------------------
    st.sidebar.header("Filters")
    courses = sorted(df["course"].unique())
    selected_courses = st.sidebar.multiselect("Courses", courses, default=courses)

    min_date, max_date = df["date"].min().date(), df["date"].max().date()
    date_range = st.sidebar.date_input(
        "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)

    filtered = df[
        df["course"].isin(selected_courses)
        & (df["date"].dt.date >= start_date)
        & (df["date"].dt.date <= end_date)
    ].reset_index(drop=True)

    if filtered.empty:
        st.warning("No rounds match the current filters.")
        return

    # ---- KPI row -----------------------------------------------------------
    slope, _ = compute_trend(filtered) if len(filtered) > 1 else (0.0, 0.0)
    handicap_est = estimate_handicap_index(filtered)

    kpi_cols = st.columns(5)
    kpi_cols[0].metric("Rounds", len(filtered))
    kpi_cols[1].metric("Avg Score", f"{filtered['score'].mean():.1f}")
    kpi_cols[2].metric("Avg vs Par", f"{filtered['score_to_par'].mean():+.1f}")
    kpi_cols[3].metric("Trend", f"{slope:+.2f} strokes/round")
    kpi_cols[4].metric("Est. Handicap", f"{handicap_est:+.1f}")

    st.divider()

    # ---- Score trend --------------------------------------------------------
    st.subheader("Score Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered["date"], y=filtered["score"], mode="lines+markers",
        name="Score", line=dict(color="#2c6e49", width=1.5), opacity=0.6,
    ))
    fig.add_trace(go.Scatter(
        x=filtered["date"], y=filtered["rolling_score"], mode="lines",
        name=f"{ROLLING_WINDOW}-round rolling avg", line=dict(color="#1b4332", width=3),
    ))
    fig.add_hline(
        y=filtered["par"].mean(), line_dash="dash", line_color="gray",
        annotation_text="Avg par",
    )
    fig.update_layout(height=420, hovermode="x unified", legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

    # ---- Key stats + course comparison side by side --------------------------
    left, right = st.columns(2)

    with left:
        st.subheader("Key Stats Over Time")
        stat_choice = st.selectbox(
            "Stat", ["fairway_pct", "gir_pct", "putts", "penalties"], index=0
        )
        fig2 = px.line(filtered, x="date", y=stat_choice, markers=True)
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.subheader("Average Score vs. Par by Course")
        course_avg = (
            filtered.groupby("course")["score_to_par"].mean().sort_values().reset_index()
        )
        fig3 = px.bar(
            course_avg, x="score_to_par", y="course", orientation="h",
            color="score_to_par", color_continuous_scale="RdYlGn_r",
        )
        fig3.update_layout(height=350, coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    # ---- Correlations ------------------------------------------------------
    st.subheader("What's Driving Your Score?")
    corr_cols = ["score", "fairway_pct", "gir_pct", "putts", "penalties"]
    corr = filtered[corr_cols].corr()
    fig4 = px.imshow(
        corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        aspect="auto",
    )
    fig4.update_layout(height=420)
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ---- Raw data table -----------------------------------------------------
    st.subheader("Round Log")
    st.dataframe(
        filtered[[
            "date", "course", "par", "score", "score_to_par", "fairway_pct",
            "gir_pct", "putts", "penalties",
        ]].sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered rounds as CSV", csv_bytes, "rounds_filtered.csv", "text/csv")

    st.divider()

    # ---- Add a new round -----------------------------------------------------
    st.subheader("Log a New Round")
    with st.form("add_round_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        round_date = c1.date_input("Date", value=date.today())
        course = c2.text_input("Course", placeholder="e.g. Riverside Golf Club")
        par = c3.selectbox("Par", [70, 71, 72, 73])

        c4, c5, c6 = st.columns(3)
        score = c4.number_input("Score", min_value=50, max_value=150, value=85)
        fairways_hit = c5.number_input("Fairways hit", min_value=0, max_value=14, value=7)
        fairways_total = c6.number_input("Fairways total", min_value=1, max_value=18, value=14)

        c7, c8 = st.columns(2)
        gir = c7.number_input("Greens in regulation", min_value=0, max_value=18, value=6)
        putts = c8.number_input("Putts", min_value=18, max_value=60, value=32)
        penalties = st.number_input("Penalties", min_value=0, max_value=20, value=1)

        submitted = st.form_submit_button("Add round")
        if submitted:
            if not course.strip():
                st.error("Please enter a course name.")
            else:
                add_round({
                    "date": round_date.isoformat(),
                    "course": course.strip(),
                    "par": par,
                    "score": score,
                    "fairways_hit": fairways_hit,
                    "fairways_total": fairways_total,
                    "greens_in_regulation": gir,
                    "putts": putts,
                    "penalties": penalties,
                })
                st.success(f"Added round: {score} at {course.strip()} on {round_date.isoformat()}")
                st.rerun()


if __name__ == "__main__":
    main()
