"""
golf_analysis.py

Analyses personal golf round data logged in data/rounds.csv and produces
summary statistics plus performance charts saved to charts/.

Beyond basic averages, this script computes a rolling scoring average, a
linear improvement trend (strokes gained per round), score consistency,
and correlations between score and the underlying stats (fairways, GIR,
putts, penalties) so it's clear which parts of the game are actually
driving results.

Usage:
    python golf_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DATA_PATH = Path("data/rounds.csv")
CHARTS_DIR = Path("charts")
ROLLING_WINDOW = 3

sns.set_theme(style="whitegrid")


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load round data from CSV, parse dates, and sort chronologically.

    Args:
        path: Path to the rounds CSV file.

    Returns:
        A DataFrame sorted by date in ascending order.
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def derive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived performance columns to the rounds DataFrame.

    Adds:
        score_to_par: Strokes over (positive) or under (negative) par.
        fairway_pct: Percentage of fairways hit.
        gir_pct: Greens in regulation, as a percentage of 18 holes.
        putts_per_hole: Average putts taken per hole.
        rolling_score: Trailing rolling average score (window of
            ROLLING_WINDOW rounds) to smooth out round-to-round noise.
        round_number: 1-indexed sequence number, used as the x-value for
            trend regression.

    Args:
        df: Raw rounds DataFrame.

    Returns:
        DataFrame with derived columns appended.
    """
    df = df.copy()
    df["score_to_par"] = df["score"] - df["par"]
    df["fairway_pct"] = (df["fairways_hit"] / df["fairways_total"]) * 100
    df["gir_pct"] = (df["greens_in_regulation"] / 18) * 100
    df["putts_per_hole"] = df["putts"] / 18
    df["round_number"] = np.arange(1, len(df) + 1)
    df["rolling_score"] = (
        df["score"].rolling(window=ROLLING_WINDOW, min_periods=1).mean()
    )
    return df


def compute_trend(df: pd.DataFrame) -> tuple[float, float]:
    """Fit a linear trend line to score over round number.

    Args:
        df: DataFrame with a `round_number` and `score` column.

    Returns:
        A (slope, intercept) tuple. Slope is strokes per round; negative
        means the scoring average is improving (going down).
    """
    slope, intercept = np.polyfit(df["round_number"], df["score"], 1)
    return float(slope), float(intercept)


def estimate_handicap_index(df: pd.DataFrame, n_best: int = 8) -> float:
    """Estimate a simplified handicap index from the best recent rounds.

    This is a simplified stand-in for the USGA handicap formula: it
    averages score-to-par across the best `n_best` (or fewer, if not
    enough rounds are logged) of the most recent rounds and multiplies
    by 0.96, which is the same scaling factor the official formula uses.
    It is meant as a rough, directional estimate only.

    Args:
        df: DataFrame with a `score_to_par` column, sorted chronologically.
        n_best: Number of best recent rounds to average.

    Returns:
        Estimated handicap index, rounded to one decimal place.
    """
    recent = df.tail(max(n_best * 2, len(df)))
    best_rounds = recent.nsmallest(min(n_best, len(recent)), "score_to_par")
    return round(best_rounds["score_to_par"].mean() * 0.96, 1)


def print_summary(df: pd.DataFrame) -> str:
    """Print (and return) a console summary of overall performance.

    Args:
        df: DataFrame with derived stats already computed.

    Returns:
        The summary text that was printed, so it can be reused elsewhere
        (e.g. embedded in the README).
    """
    lines: list[str] = []

    def emit(text: str = "") -> None:
        print(text)
        lines.append(text)

    rounds_logged = len(df)
    avg_score = df["score"].mean()
    avg_to_par = df["score_to_par"].mean()
    score_std = df["score"].std()
    avg_fairway_pct = df["fairway_pct"].mean()
    avg_gir_pct = df["gir_pct"].mean()
    avg_putts = df["putts"].mean()
    avg_penalties = df["penalties"].mean()

    best_round = df.loc[df["score"].idxmin()]
    worst_round = df.loc[df["score"].idxmax()]

    half = rounds_logged // 2
    first_half_avg = df.iloc[:half]["score"].mean()
    second_half_avg = df.iloc[half:]["score"].mean()
    stroke_diff = first_half_avg - second_half_avg
    trend_word = "improving" if stroke_diff > 0 else "declining"

    slope, _ = compute_trend(df)
    projected_next = df["score"].iloc[-1] + slope

    handicap_est = estimate_handicap_index(df)

    corr = df[["score", "fairway_pct", "gir_pct", "putts", "penalties"]].corr()
    score_corrs = corr["score"].drop("score").sort_values()

    emit("=" * 50)
    emit("GOLF PERFORMANCE SUMMARY")
    emit("=" * 50)
    emit(f"Rounds logged:              {rounds_logged}")
    emit(f"Average score:               {avg_score:.1f}  (std dev {score_std:.1f})")
    emit(f"Average vs. par:             {avg_to_par:+.1f}")
    emit(
        f"Best round:                  {int(best_round['score'])} "
        f"({best_round['course']}, {best_round['date'].strftime('%Y-%m-%d')})"
    )
    emit(
        f"Worst round:                 {int(worst_round['score'])} "
        f"({worst_round['course']}, {worst_round['date'].strftime('%Y-%m-%d')})"
    )
    emit(f"Average fairways hit:        {avg_fairway_pct:.1f}%")
    emit(f"Average greens in reg.:      {avg_gir_pct:.1f}%")
    emit(f"Average putts per round:     {avg_putts:.1f}")
    emit(f"Average penalties per round: {avg_penalties:.1f}")
    emit(
        f"Trend (1st half vs 2nd):     {trend_word} by "
        f"{abs(stroke_diff):.1f} strokes on average "
        f"({first_half_avg:.1f} -> {second_half_avg:.1f})"
    )
    emit(
        f"Linear trend slope:          {slope:+.2f} strokes/round "
        f"(projected next round: {projected_next:.1f})"
    )
    emit(f"Estimated handicap index:    {handicap_est:+.1f} (simplified estimate)")
    emit("")
    emit("What's correlated with a lower score (most to least helpful):")
    for stat, value in score_corrs.items():
        direction = "higher score" if value > 0 else "lower score"
        emit(f"  {stat:<12} r = {value:+.2f}  (more {stat} -> {direction})")
    emit("=" * 50)

    return "\n".join(lines)


def plot_score_trend(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> Path:
    """Plot score over time with rolling average and a linear trend line.

    Args:
        df: DataFrame with derived stats.
        out_dir: Directory to save the chart PNG into.

    Returns:
        Path to the saved PNG file.
    """
    slope, intercept = compute_trend(df)
    trend_line = slope * df["round_number"] + intercept

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        df["date"], df["score"], marker="o", linewidth=1.5,
        color="#2c6e49", alpha=0.5, label="Score",
    )
    ax.plot(
        df["date"], df["rolling_score"], linewidth=2.5,
        color="#1b4332", label=f"{ROLLING_WINDOW}-round rolling avg",
    )
    ax.plot(
        df["date"], trend_line, linestyle=":", linewidth=2,
        color="#bc4749", label="Linear trend",
    )

    avg_par = df["par"].mean()
    ax.axhline(avg_par, linestyle="--", color="#a3a3a3", linewidth=1.5, label=f"Par ({avg_par:.0f})")

    ax.set_title("Score Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()

    out_path = out_dir / "score_trend.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_key_stats(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> Path:
    """Plot fairway %, GIR %, and putts per round over time as subplots.

    Args:
        df: DataFrame with derived stats.
        out_dir: Directory to save the chart PNG into.

    Returns:
        Path to the saved PNG file.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    axes[0].plot(df["date"], df["fairway_pct"], marker="o", color="#1d4e89")
    axes[0].set_title("Fairways Hit (%)")
    axes[0].set_ylabel("%")

    axes[1].plot(df["date"], df["gir_pct"], marker="o", color="#e07a5f")
    axes[1].set_title("Greens in Regulation (%)")
    axes[1].set_ylabel("%")

    axes[2].plot(df["date"], df["putts"], marker="o", color="#6a4c93")
    axes[2].set_title("Putts per Round")
    axes[2].set_ylabel("Putts")

    for ax in axes:
        ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Key Stats Over Time", fontsize=14, fontweight="bold")
    fig.tight_layout()

    out_path = out_dir / "key_stats.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_score_by_course(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> Path:
    """Plot average score-vs-par by course, sorted from best to worst.

    Args:
        df: DataFrame with derived stats.
        out_dir: Directory to save the chart PNG into.

    Returns:
        Path to the saved PNG file.
    """
    course_avg = (
        df.groupby("course")["score_to_par"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(
        data=course_avg,
        x="score_to_par",
        y="course",
        hue="course",
        palette="crest",
        legend=False,
        ax=ax,
    )

    ax.set_title("Average Score vs. Par by Course", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Score vs. Par (strokes)")
    ax.set_ylabel("")
    ax.axvline(0, color="#444444", linewidth=1)
    fig.tight_layout()

    out_path = out_dir / "score_by_course.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_correlation_heatmap(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> Path:
    """Plot a correlation heatmap between score and key underlying stats.

    Args:
        df: DataFrame with derived stats.
        out_dir: Directory to save the chart PNG into.

    Returns:
        Path to the saved PNG file.
    """
    cols = ["score", "fairway_pct", "gir_pct", "putts", "penalties"]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
        vmin=-1, vmax=1, square=True, ax=ax, cbar_kws={"label": "Correlation"},
    )
    ax.set_title("What Correlates with Score?", fontsize=14, fontweight="bold")
    fig.tight_layout()

    out_path = out_dir / "correlation_heatmap.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_putts_vs_score(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> Path:
    """Plot a scatter of putts vs. score with a regression line.

    Args:
        df: DataFrame with derived stats.
        out_dir: Directory to save the chart PNG into.

    Returns:
        Path to the saved PNG file.
    """
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.regplot(
        data=df, x="putts", y="score", ax=ax,
        scatter_kws={"color": "#1d4e89", "s": 60},
        line_kws={"color": "#bc4749"},
    )
    ax.set_title("Putts vs. Score", fontsize=14, fontweight="bold")
    ax.set_xlabel("Putts per Round")
    ax.set_ylabel("Score")
    fig.tight_layout()

    out_path = out_dir / "putts_vs_score.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def main() -> None:
    """Load data, print a summary, and generate all performance charts."""
    CHARTS_DIR.mkdir(exist_ok=True)

    df = load_data()
    df = derive_stats(df)

    print_summary(df)

    plot_score_trend(df)
    plot_key_stats(df)
    plot_score_by_course(df)
    plot_correlation_heatmap(df)
    plot_putts_vs_score(df)

    print(f"\nCharts saved to {CHARTS_DIR.resolve()}/")


if __name__ == "__main__":
    main()
