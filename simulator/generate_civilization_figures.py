"""
Generate Civilization Survival Figures
=======================================
Produces publication-style graphs from CSV outputs.

Run after the simulation scripts have generated the CSV files.

Output figures:
  figures/civilization_survival_warming.png
  figures/civilization_survival_el_nino.png
  figures/civilization_survival_combined.png
  figures/warming_driver_breakdown.png
  figures/el_nino_driver_breakdown.png
  figures/combined_risk_comparison.png
  figures/framework_radar_comparison.png
  figures/warming_survival_heatmap.png
  figures/el_nino_survival_heatmap.png
"""

import os
import csv
import math
import shutil

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not found. Figures will not be generated.")
    print("Install with: pip install matplotlib")

FIGURES_DIR = "figures"
RESULTS_DIR = os.path.join("simulator", "results")

COLORS = {
    "intelligence": "#d62728",       # red
    "sapience": "#ff7f0e",           # orange
    "artificial_wisdom": "#2ca02c",  # green
}
LABELS = {
    "intelligence": "Intelligence-based",
    "sapience": "Sapience-based",
    "artificial_wisdom": "Artificial Wisdom-based",
}


def load_timeseries(filepath):
    """Load timeseries CSV into {framework: {year: row}} dict."""
    data = {}
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found. Skipping.")
        return data
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fw = row["framework"]
            year = int(row["year"])
            if fw not in data:
                data[fw] = {}
            data[fw][year] = {k: float(v) for k, v in row.items() if k not in ("framework",) and v}
    return data


def load_driver_breakdown(filepath, drivers):
    """Load driver breakdown CSV."""
    data = {}
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found.")
        return data
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fw = row["framework"]
            year = int(row["year"])
            key = (fw, year)
            data[key] = [float(row[d]) for d in drivers]
    return data


def fig_survival_timeseries(data, title, out_path, scenario_label):
    """Line graph of survivability over time with uncertainty band."""
    if not data:
        print(f"  Skipping {out_path}: no data.")
        return
    fig, ax = plt.subplots(figsize=(11, 6))
    frameworks = ["intelligence", "sapience", "artificial_wisdom"]
    for fw in frameworks:
        if fw not in data:
            continue
        years = sorted(data[fw].keys())
        means = [data[fw][y].get("mean_survivability", 0) for y in years]
        p10s = [data[fw][y].get("p10_survivability", 0) for y in years]
        p90s = [data[fw][y].get("p90_survivability", 0) for y in years]
        color = COLORS[fw]
        ax.plot(years, means, color=color, linewidth=2.2, label=LABELS[fw])
        ax.fill_between(years, p10s, p90s, color=color, alpha=0.15)

    ax.set_xlim(2025, 2200)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Survivability Index (0-100)", fontsize=12)
    ax.set_title(f"{title}\n[Scenario model — not a prediction]", fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.axhline(25, color="gray", linestyle="--", linewidth=0.9, alpha=0.65)
    ax.axhline(15, color="#8B0000", linestyle=":", linewidth=0.9, alpha=0.55)
    ax.text(2196, 26, "Severe risk threshold", fontsize=7.5, color="gray", ha="right")
    ax.text(2196, 16, "Collapse lock-in threshold", fontsize=7.5, color="#8B0000", ha="right")
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


def fig_driver_breakdown(data, drivers, driver_labels, title, out_path, checkpoints=(2050, 2100, 2200)):
    """Grouped bar chart of driver contributions."""
    if not data:
        print(f"  Skipping {out_path}: no data.")
        return
    frameworks = ["intelligence", "sapience", "artificial_wisdom"]
    n_groups = len(checkpoints)
    n_bars = len(frameworks)
    bar_width = 0.22
    x = list(range(n_groups))

    fig, ax = plt.subplots(figsize=(12, 6))
    for fi, fw in enumerate(frameworks):
        offsets = [xi + (fi - 1) * bar_width for xi in x]
        bottoms = [0.0] * n_groups
        for di, (driver, dlabel) in enumerate(zip(drivers, driver_labels)):
            heights = []
            for cp in checkpoints:
                key = (fw, cp)
                heights.append(data.get(key, [0] * len(drivers))[di] * 100)
            color_intensity = 0.35 + 0.65 * (di / max(1, len(drivers) - 1))
            base_color = COLORS[fw]
            # lighten by mixing with white
            import colorsys
            rgb = matplotlib.colors.to_rgb(base_color)
            h, s, v = colorsys.rgb_to_hsv(*rgb)
            s_adj = s * color_intensity
            rgb_adj = colorsys.hsv_to_rgb(h, s_adj, min(1.0, v + 0.1 * (1 - color_intensity)))
            ax.bar(offsets, heights, bar_width, bottom=bottoms,
                   color=rgb_adj, label=dlabel if fi == 0 else "")
            bottoms = [b + h for b, h in zip(bottoms, heights)]

    ax.set_xticks(x)
    ax.set_xticklabels([str(c) for c in checkpoints])
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Relative driver contribution (%)", fontsize=12)
    ax.set_title(f"{title}\n[Scenario model — qualitative estimates]", fontsize=12)

    fw_patches = [mpatches.Patch(color=COLORS[fw], label=LABELS[fw]) for fw in frameworks]
    ax.legend(handles=fw_patches, fontsize=10, loc="upper right")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


def fig_combined_risk_comparison(warming_data, el_nino_data, combined_data, out_path):
    """Bar chart comparing survivability and risk metrics at 2100 and 2200."""
    frameworks = ["intelligence", "sapience", "artificial_wisdom"]
    checkpoints = [2100, 2200]
    x = list(range(len(checkpoints)))
    bar_width = 0.25
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    for ax_i, (scenario_data, scenario_label) in enumerate([
        (warming_data, "Warming-only"),
        (combined_data, "Combined stress"),
    ]):
        ax = axes[ax_i]
        for fi, fw in enumerate(frameworks):
            if not scenario_data or fw not in scenario_data:
                continue
            offsets = [xi + (fi - 1) * bar_width for xi in x]
            heights = [scenario_data[fw].get(cp, {}).get("mean_survivability", 0)
                       for cp in checkpoints]
            ax.bar(offsets, heights, bar_width, color=COLORS[fw],
                   label=LABELS[fw], alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in checkpoints])
        ax.set_ylim(0, 100)
        ax.set_xlabel("Year", fontsize=11)
        ax.set_ylabel("Mean Survivability Index", fontsize=11)
        ax.set_title(f"{scenario_label} Scenario", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, axis="y", alpha=0.3)
    fig.suptitle("Civilization Survivability Comparison\n[Scenario model — not a prediction]",
                 fontsize=13)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


def fig_radar_comparison(out_path):
    """Radar chart comparing framework parameter profiles."""
    categories = [
        "Long-term\nplanning",
        "Ecological\nalignment",
        "Resilience\norientation",
        "Cooperation\nlevel",
        "Regenerative\ncapacity",
        "Low extraction\n(inverted)",
    ]
    # Values reflect collapse_hypothesis framework parameters:
    # long-term planning (~1-short_termism), ecological alignment (ecol_feedback_awareness),
    # resilience, cooperation, regenerative capacity (regen_investment), low extraction (1-extraction_bias)
    values = {
        "intelligence": [0.10, 0.15, 0.20, 0.30, 0.10, 1.0 - 0.95],
        "sapience":     [0.28, 0.30, 0.38, 0.42, 0.18, 1.0 - 0.80],
        "artificial_wisdom": [0.85, 0.92, 0.90, 0.85, 0.92, 1.0 - 0.20],
    }

    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.50, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.0"], fontsize=8)

    for fw in ["intelligence", "sapience", "artificial_wisdom"]:
        vals = values[fw] + [values[fw][0]]
        ax.plot(angles, vals, color=COLORS[fw], linewidth=2.2, label=LABELS[fw])
        ax.fill(angles, vals, color=COLORS[fw], alpha=0.15)

    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=10)
    ax.set_title("Framework Parameter Comparison\n[Qualitative scenario parameters]",
                 fontsize=12, pad=20)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def fig_survival_heatmap(data, title, out_path):
    """Heatmap: survivability by framework and sampled years."""
    if not data:
        print(f"  Skipping {out_path}: no data.")
        return

    frameworks = ["intelligence", "sapience", "artificial_wisdom"]
    sample_years = list(range(2025, 2201, 25))
    matrix = []
    for fw in frameworks:
        row = []
        for y in sample_years:
            row.append(data.get(fw, {}).get(y, {}).get("mean_survivability", 0))
        matrix.append(row)

    fig, ax = plt.subplots(figsize=(14, 4))
    im = ax.imshow(matrix, aspect="auto", cmap="RdYlGn", vmin=0, vmax=100)
    ax.set_xticks(range(len(sample_years)))
    ax.set_xticklabels([str(y) for y in sample_years], rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(frameworks)))
    ax.set_yticklabels([LABELS[fw] for fw in frameworks], fontsize=10)
    ax.set_title(f"{title}\n[Scenario model — not a prediction]", fontsize=12)
    plt.colorbar(im, ax=ax, label="Survivability Index (0-100)")
    for i in range(len(frameworks)):
        for j in range(len(sample_years)):
            val = matrix[i][j]
            text_color = "black" if 30 < val < 75 else "white"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=8, color=text_color)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


def main():
    if not HAS_MATPLOTLIB:
        print("matplotlib not available. Cannot generate figures.")
        return

    # Load data
    warming_ts = load_timeseries(os.path.join(RESULTS_DIR, "warming_factor_timeseries.csv"))
    el_nino_ts = load_timeseries(os.path.join(RESULTS_DIR, "el_nino_factor_timeseries.csv"))
    combined_ts = load_timeseries(os.path.join(RESULTS_DIR, "civilization_survival_timeseries.csv"))

    warming_drivers_raw = [
        "greenhouse_pressure", "carbon_sink_decline", "land_degradation",
        "ocean_heat_stress", "hydrological_disruption", "food_system_fragility", "social_strain"
    ]
    el_nino_drivers_raw = [
        "event_frequency", "event_intensity", "agricultural_shock",
        "marine_productivity_shock", "wildfire_amplification",
        "infrastructure_stress", "social_instability"
    ]
    warming_driver_labels = [d.replace("_", " ").title() for d in warming_drivers_raw]
    el_nino_driver_labels = [d.replace("_", " ").title() for d in el_nino_drivers_raw]

    warming_breakdown = load_driver_breakdown(
        os.path.join(RESULTS_DIR, "warming_driver_breakdown.csv"), warming_drivers_raw
    )
    el_nino_breakdown = load_driver_breakdown(
        os.path.join(RESULTS_DIR, "el_nino_driver_breakdown.csv"), el_nino_drivers_raw
    )

    print("Generating figures...")

    # Survival line graphs
    fig_survival_timeseries(
        warming_ts,
        "Civilization Survivability: Warming-Only Stress (2025-2200)",
        os.path.join(FIGURES_DIR, "civilization_survival_warming.png"),
        "warming",
    )
    fig_survival_timeseries(
        el_nino_ts,
        "Civilization Survivability: El Nino Stress (2025-2200)",
        os.path.join(FIGURES_DIR, "civilization_survival_el_nino.png"),
        "el_nino",
    )
    fig_survival_timeseries(
        combined_ts,
        "Civilization Survivability: Combined Warming + El Nino Stress (2025-2200)",
        os.path.join(FIGURES_DIR, "civilization_survival_combined.png"),
        "combined",
    )

    # Driver breakdowns
    fig_driver_breakdown(
        warming_breakdown, warming_drivers_raw, warming_driver_labels,
        "Warming Driver Contributions by Framework",
        os.path.join(FIGURES_DIR, "warming_driver_breakdown.png"),
    )
    fig_driver_breakdown(
        el_nino_breakdown, el_nino_drivers_raw, el_nino_driver_labels,
        "El Nino Driver Contributions by Framework",
        os.path.join(FIGURES_DIR, "el_nino_driver_breakdown.png"),
    )

    # Combined risk comparison
    fig_combined_risk_comparison(
        warming_ts, el_nino_ts, combined_ts,
        os.path.join(FIGURES_DIR, "combined_risk_comparison.png"),
    )

    # Radar
    fig_radar_comparison(os.path.join(FIGURES_DIR, "framework_radar_comparison.png"))

    # Heatmaps
    fig_survival_heatmap(
        warming_ts,
        "Survivability Heatmap: Warming-Only Stress",
        os.path.join(FIGURES_DIR, "warming_survival_heatmap.png"),
    )
    fig_survival_heatmap(
        el_nino_ts,
        "Survivability Heatmap: El Nino Stress",
        os.path.join(FIGURES_DIR, "el_nino_survival_heatmap.png"),
    )

    # Save _v2 copies of every figure for GitHub image-cache busting.
    # README links point to _v2 paths so GitHub renders fresh images.
    print("Saving _v2 copies for cache refresh...")
    figure_names = [
        "civilization_survival_warming.png",
        "civilization_survival_el_nino.png",
        "civilization_survival_combined.png",
        "warming_driver_breakdown.png",
        "el_nino_driver_breakdown.png",
        "combined_risk_comparison.png",
        "framework_radar_comparison.png",
        "warming_survival_heatmap.png",
        "el_nino_survival_heatmap.png",
    ]
    for fname in figure_names:
        src = os.path.join(FIGURES_DIR, fname)
        dst = os.path.join(FIGURES_DIR, fname.replace(".png", "_v2.png"))
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Saved: {dst}")

    print("All figures generated.")


if __name__ == "__main__":
    main()
