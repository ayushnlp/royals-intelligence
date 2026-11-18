"""
Royals Intelligence - Stage R1-07.4 / Round 1 Final Submission
Publication-Grade Visualizations Generator.

Generates 6 publication-quality figures for embedding in the Markdown report and PDF.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "round1_pressure" / "data" / "processed"
FIGURES_DIR = BASE_DIR / "round1_pressure" / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set high-DPI publication styling
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#f0f0f0"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

# Royals Brand Colors
RR_BLUE = "#001D48"
RR_PINK = "#EA1A7F"
RR_GOLD = "#D4AF37"
RR_NAVY = "#0F2042"
ACCENT_CYAN = "#00B4D8"
ACCENT_GREEN = "#2DC653"
NEUTRAL_GRAY = "#6C757D"
LIGHT_BG = "#F8F9FA"


def plot_fig1_overall_batters():
    """Figure 1: Official Top 10 Batters PRI Forest Plot."""
    bat_lb = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet").head(10).iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    y_pos = np.arange(len(bat_lb))

    # Plot 95% Credible Interval bars
    for i, (_, row) in enumerate(bat_lb.iterrows()):
        ax.plot([row["ci_95_lower"], row["ci_95_upper"]], [i, i], color="#C4D1EB", lw=3.5, solid_capstyle="round", zorder=2)
        # 1-SE uncertainty bar
        ax.plot([row["posterior_mean"] - row["posterior_se"], row["posterior_mean"] + row["posterior_se"]], [i, i], color=RR_BLUE, lw=6, solid_capstyle="round", zorder=3)
        # Posterior Mean Point
        ax.scatter(row["posterior_mean"], i, color=RR_BLUE, s=70, zorder=4, edgecolor="white", lw=1.2)
        # Conservative PRI Point
        ax.scatter(row["primary_diagnostic_value"], i, color=RR_PINK, s=90, marker="D", zorder=5, edgecolor="white", lw=1.2)

    # Reference baseline line (League Baseline = 0)
    ax.axvline(0, color="#888888", linestyle="--", lw=1.2, zorder=1)

    ax.set_yticks(y_pos)
    labels = [f"#{row['rank']} {row['player_name']} ({row['pressure_legal_balls']}b)" for _, row in bat_lb.iterrows()]
    ax.set_yticklabels(labels, fontsize=10, fontweight="bold", color=RR_NAVY)

    ax.set_xlabel("Pressure Response Index (PRI: Strike Rate Delta vs Baseline)", fontsize=11, fontweight="bold", color=RR_NAVY, labelpad=8)
    ax.set_title("Official Overall Top 10 Batters Under Pressure (R1 Stage 7 Empirical Bayes)", fontsize=13, fontweight="bold", pad=14, color=RR_NAVY)

    # Custom Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="D", color="w", markerfacecolor=RR_PINK, markersize=8, label="Conservative Metric (1-SE Lower Bound)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=RR_BLUE, markersize=8, label="Posterior Mean (Shrunk Delta)"),
        Line2D([0], [0], color=RR_BLUE, lw=4, label="±1 Posterior SE"),
        Line2D([0], [0], color="#C4D1EB", lw=2.5, label="95% Credible Interval"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", frameon=True, framealpha=0.9, fontsize=9)

    ax.grid(axis="x")
    plt.tight_layout()
    out_path = FIGURES_DIR / "fig1_overall_top10_batters_pri.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


def plot_fig2_overall_bowlers():
    """Figure 2: Official Top 10 Bowlers Conservative Runs Saved Forest Plot."""
    bowl_df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")
    bowl_lb = bowl_df[bowl_df["is_candidate_qualified"] == True].head(10).copy()
    bowl_lb["official_rank"] = range(1, len(bowl_lb) + 1)
    bowl_lb = bowl_lb.iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    y_pos = np.arange(len(bowl_lb))

    for i, (_, row) in enumerate(bowl_lb.iterrows()):
        # 95% CI
        ax.plot([row["ci_95_lower"], row["ci_95_upper"]], [i, i], color="#E8D5B5", lw=3.5, solid_capstyle="round", zorder=2)
        # 1-SE uncertainty bar
        ax.plot([row["posterior_mean"] - row["posterior_se"], row["posterior_mean"] + row["posterior_se"]], [i, i], color=RR_GOLD, lw=6, solid_capstyle="round", zorder=3)
        # Posterior Mean Point
        ax.scatter(row["posterior_mean"], i, color=RR_GOLD, s=70, zorder=4, edgecolor="white", lw=1.2)
        # Conservative Metric Point
        ax.scatter(row["primary_diagnostic_value"], i, color=RR_PINK, s=90, marker="D", zorder=5, edgecolor="white", lw=1.2)

    ax.axvline(0, color="#888888", linestyle="--", lw=1.2, zorder=1)

    ax.set_yticks(y_pos)
    labels = [f"#{row['official_rank']} {row['player_name']} ({row['pressure_legal_balls']}b)" for _, row in bowl_lb.iterrows()]
    ax.set_yticklabels(labels, fontsize=10, fontweight="bold", color=RR_NAVY)

    ax.set_xlabel("Runs Saved per 6 Balls vs Contextual Baseline (More Negative = Better)", fontsize=11, fontweight="bold", color=RR_NAVY, labelpad=8)
    ax.set_title("Official Overall Top 10 Bowlers Under Pressure (R1 Stage 7 Empirical Bayes)", fontsize=13, fontweight="bold", pad=14, color=RR_NAVY)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="D", color="w", markerfacecolor=RR_PINK, markersize=8, label="BOWL_CONSERVATIVE Diagnostic"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=RR_GOLD, markersize=8, label="Posterior Mean Economy Delta"),
        Line2D([0], [0], color=RR_GOLD, lw=4, label="±1 Posterior SE"),
        Line2D([0], [0], color="#E8D5B5", lw=2.5, label="95% Credible Interval"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", frameon=True, framealpha=0.9, fontsize=9)

    ax.grid(axis="x")
    plt.tight_layout()
    out_path = FIGURES_DIR / "fig2_overall_top10_bowlers_runs_saved.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


def plot_fig3_uncapped_batters():
    """Figure 3: Uncapped Indian Domestic Batters PRI & Volume Comparison."""
    df = pd.read_parquet(PROCESSED_DIR / "uncapped_batting_shortlist.parquet").iloc[::-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, gridspec_kw={"width_ratios": [3, 1.2]})

    y_pos = np.arange(len(df))
    colors = [RR_PINK if r["uncapped_rank"] == 1 else RR_BLUE for _, r in df.iterrows()]

    # Horizontal Bar Chart for PRI
    bars = ax1.barh(y_pos, df["primary_diagnostic_value"], color=colors, height=0.6, zorder=3)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f"#{r['uncapped_rank']} {r['player_name']} ({r['domestic_association']})" for _, r in df.iterrows()], fontsize=9.5, fontweight="bold")
    ax1.axvline(0, color="#888888", linestyle="--", lw=1)
    ax1.set_xlabel("Conservative PRI (Strike Rate Delta vs Baseline)", fontsize=10.5, fontweight="bold")
    ax1.set_title("Top 10 Uncapped Indian Batters — Pressure Metric", fontsize=11.5, fontweight="bold", color=RR_NAVY)
    ax1.grid(axis="x")

    # Add data values on bars
    for bar in bars:
        w = bar.get_width()
        x_text = w - 1.2 if w < 0 else w + 0.5
        ax1.text(x_text, bar.get_y() + bar.get_height() / 2, f"{w:+.1f}", va="center", ha="right" if w < 0 else "left", fontsize=8.5, fontweight="bold", color="#333333")

    # Pressure Legal Balls on right pane
    ax2.barh(y_pos, df["pressure_legal_balls"], color="#6C757D", height=0.6, zorder=3)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Pressure Balls", fontsize=10.5, fontweight="bold")
    ax2.set_title("Exposure Sample", fontsize=11.5, fontweight="bold", color=RR_NAVY)
    ax2.grid(axis="x")

    for bar in ax2.patches:
        ax2.text(bar.get_width() + 4, bar.get_y() + bar.get_height() / 2, f"{int(bar.get_width())}b", va="center", fontsize=8.5)

    plt.tight_layout()
    out_path = FIGURES_DIR / "fig3_uncapped_batters_leaderboard.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


def plot_fig4_uncapped_bowlers():
    """Figure 4: Uncapped Indian Domestic Bowlers Economy Delta & Volume."""
    df = pd.read_parquet(PROCESSED_DIR / "uncapped_bowling_shortlist.parquet").iloc[::-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, gridspec_kw={"width_ratios": [3, 1.2]})

    y_pos = np.arange(len(df))
    colors = [RR_PINK if r["uncapped_rank"] <= 2 else RR_NAVY for _, r in df.iterrows()]

    bars = ax1.barh(y_pos, df["primary_diagnostic_value"], color=colors, height=0.6, zorder=3)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f"#{r['uncapped_rank']} {r['player_name']} ({r['domestic_association']})" for _, r in df.iterrows()], fontsize=9.5, fontweight="bold")
    ax1.set_xlabel("Runs Saved per 6 Balls (BOWL_CONSERVATIVE)", fontsize=10.5, fontweight="bold")
    ax1.set_title("Top 10 Uncapped Indian Bowlers — Runs Saved Metric", fontsize=11.5, fontweight="bold", color=RR_NAVY)
    ax1.grid(axis="x")

    for bar in bars:
        w = bar.get_width()
        ax1.text(w - 0.08, bar.get_y() + bar.get_height() / 2, f"{w:.2f}", va="center", ha="right", fontsize=8.5, fontweight="bold", color="#333333")

    ax2.barh(y_pos, df["pressure_legal_balls"], color="#6C757D", height=0.6, zorder=3)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.set_xlabel("Pressure Balls", fontsize=10.5, fontweight="bold")
    ax2.set_title("Exposure Sample", fontsize=11.5, fontweight="bold", color=RR_NAVY)
    ax2.grid(axis="x")

    for bar in ax2.patches:
        ax2.text(bar.get_width() + 4, bar.get_y() + bar.get_height() / 2, f"{int(bar.get_width())}b", va="center", fontsize=8.5)

    plt.tight_layout()
    out_path = FIGURES_DIR / "fig4_uncapped_bowlers_leaderboard.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


def plot_fig5_rr_squad_fit_matrix():
    """Figure 5: Stacked Component Breakdown of RR Squad Fit Ratings."""
    df_fit = pd.read_parquet(PROCESSED_DIR / "rr_squad_fit_ratings.parquet").sort_values("rr_fit_rating", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    y_pos = np.arange(len(df_fit))

    # Components weighted in baseline
    w_role = df_fit["score_role_need"] * 0.30
    w_pres = df_fit["score_pressure_execution"] * 0.25
    w_phase = df_fit["score_phase_fit"] * 0.20
    w_comp = df_fit["score_complementarity"] * 0.15
    w_run = df_fit["score_runway_value"] * 0.10

    p1 = ax.barh(y_pos, w_role, color="#0F2042", height=0.65, label="Role Need & Vacancy (30%)")
    p2 = ax.barh(y_pos, w_pres, left=w_role, color="#EA1A7F", height=0.65, label="Pressure Execution (25%)")
    p3 = ax.barh(y_pos, w_phase, left=w_role + w_pres, color="#00B4D8", height=0.65, label="Phase Compatibility (20%)")
    p4 = ax.barh(y_pos, w_comp, left=w_role + w_pres + w_phase, color="#D4AF37", height=0.65, label="Skill Complementarity (15%)")
    p5 = ax.barh(y_pos, w_run, left=w_role + w_pres + w_phase + w_comp, color="#2DC653", height=0.65, label="Runway & Contract Value (10%)")

    ax.set_yticks(y_pos)
    labels = [f"{r['player_name']} ({r['discipline'][0]} - #{r['fit_rank_overall']})" for _, r in df_fit.iterrows()]
    ax.set_yticklabels(labels, fontsize=9.5, fontweight="bold", color=RR_NAVY)

    # Label total score at bar ends
    for i, (_, row) in enumerate(df_fit.iterrows()):
        ax.text(row["rr_fit_rating"] + 1, i, f"{row['rr_fit_rating']:.1f}", va="center", fontsize=9, fontweight="bold", color=RR_NAVY)

    ax.set_xlim(0, 105)
    ax.set_xlabel("Rajasthan Royals Squad Fit Rating (0–100 Rubric Scale)", fontsize=11, fontweight="bold", color=RR_NAVY, labelpad=8)
    ax.set_title("Rajasthan Royals Squad Fit Rating — Multi-Dimensional Component Breakdown", fontsize=12.5, fontweight="bold", pad=14, color=RR_NAVY)
    ax.legend(loc="lower right", frameon=True, framealpha=0.9, fontsize=8.5)
    ax.grid(axis="x")

    plt.tight_layout()
    out_path = FIGURES_DIR / "fig5_rr_squad_fit_matrix.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


def plot_fig6_pressure_scatter():
    """Figure 6: Observed Strike Rate / Economy vs Baseline Expectation."""
    bat_lb = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    top10_bat = bat_lb.head(10)

    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # Plot all qualified batters as light points
    qual_bat = bat_lb[bat_lb["is_qualified"] == True]
    ax.scatter(qual_bat["expected_strike_rate"], qual_bat["observed_strike_rate"], color="#CED4DA", alpha=0.6, s=40, label="All Qualified Batters (n=238)", zorder=2)

    # Diagonal parity line (Observed == Expected)
    min_sr = min(qual_bat["expected_strike_rate"].min(), qual_bat["observed_strike_rate"].min()) - 5
    max_sr = max(qual_bat["expected_strike_rate"].max(), qual_bat["observed_strike_rate"].max()) + 10
    ax.plot([min_sr, max_sr], [min_sr, max_sr], color="#888888", linestyle="--", lw=1.2, label="Parity (Observed = Expected)", zorder=1)

    # Highlight Top 10 Batters
    ax.scatter(top10_bat["expected_strike_rate"], top10_bat["observed_strike_rate"], color=RR_PINK, s=100, edgecolor=RR_NAVY, lw=1.5, label="Official Top 10 Batters", zorder=4)

    # Annotate top performers
    for _, row in top10_bat.iterrows():
        ax.annotate(
            row["player_name"],
            (row["expected_strike_rate"], row["observed_strike_rate"]),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=8.5,
            fontweight="bold",
            color=RR_NAVY,
            zorder=5,
        )

    ax.set_xlabel("Expected Contextual Strike Rate (Phase, Wickets, Match RRR)", fontsize=11, fontweight="bold", color=RR_NAVY)
    ax.set_ylabel("Observed Strike Rate in Pressure Delivery Subset", fontsize=11, fontweight="bold", color=RR_NAVY)
    ax.set_title("Pressure Delivery Performance vs Contextual Expectation", fontsize=12.5, fontweight="bold", pad=12, color=RR_NAVY)
    ax.legend(loc="upper left", frameon=True, framealpha=0.9, fontsize=9)
    ax.grid(True)

    plt.tight_layout()
    out_path = FIGURES_DIR / "fig6_pressure_vs_baseline_scatter.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path}")


if __name__ == "__main__":
    plot_fig1_overall_batters()
    plot_fig2_overall_bowlers()
    plot_fig3_uncapped_batters()
    plot_fig4_uncapped_bowlers()
    plot_fig5_rr_squad_fit_matrix()
    plot_fig6_pressure_scatter()
    print("All 6 figures generated successfully!")
