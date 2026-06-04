"""
Warming Factor Model
====================
Runs the warming-only scenario using the civilization survival toy model.

Warming-specific drivers are modeled as multipliers on the baseline
warming stress trajectory. No El Nino events are applied here.

Output:
  simulator/results/warming_factor_timeseries.csv
  simulator/results/warming_factor_summary.csv
  simulator/results/warming_driver_breakdown.csv
"""

import os
import csv
import sys

# Allow running from repo root
sys.path.insert(0, os.path.dirname(__file__))
from civilization_survival_model import (
    FRAMEWORKS, INITIAL_STATE, YEAR_START, YEAR_END,
    run_scenario, save_timeseries_csv, save_summary_csv, clamp
)

RESULTS_DIR = os.path.join("simulator", "results")

# Warming driver contribution weights (per framework, relative to baseline)
# These represent the proportional severity of each warming-related stressor
# under each value system. Values are qualitative estimates, not empirical data.

WARMING_DRIVERS = [
    "greenhouse_pressure",
    "carbon_sink_decline",
    "land_degradation",
    "ocean_heat_stress",
    "hydrological_disruption",
    "food_system_fragility",
    "social_strain",
]

# Driver contribution to total warming stress at three checkpoints
# (2050, 2100, 2200) — relative weights, not absolute values
DRIVER_CONTRIBUTIONS = {
    "intelligence": {
        2050: [0.30, 0.22, 0.18, 0.12, 0.08, 0.06, 0.04],
        2100: [0.28, 0.24, 0.20, 0.13, 0.08, 0.05, 0.02],
        2200: [0.25, 0.26, 0.22, 0.13, 0.07, 0.04, 0.03],
    },
    "sapience": {
        2050: [0.28, 0.20, 0.16, 0.12, 0.10, 0.09, 0.05],
        2100: [0.26, 0.21, 0.18, 0.12, 0.10, 0.08, 0.05],
        2200: [0.24, 0.22, 0.19, 0.13, 0.10, 0.07, 0.05],
    },
    "artificial_wisdom": {
        2050: [0.22, 0.16, 0.12, 0.12, 0.13, 0.14, 0.11],
        2100: [0.20, 0.16, 0.13, 0.12, 0.14, 0.14, 0.11],
        2200: [0.18, 0.16, 0.13, 0.13, 0.15, 0.14, 0.11],
    },
}


def run_warming_scenarios(n_runs=200, noise_scale=3.0):
    """Run warming-only scenarios (no El Nino events)."""
    results = {}
    for fw, params in FRAMEWORKS.items():
        print(f"  Running warming-only scenario: {fw} ({n_runs} runs)...")
        # No El Nino schedule
        results[fw] = run_scenario(
            params,
            el_nino_schedule=set(),
            noise_scale=noise_scale,
            n_runs=n_runs,
        )
    return results


def save_driver_breakdown_csv(filepath):
    """Save per-driver contribution estimates at 2050, 2100, 2200."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = ["framework", "year"] + WARMING_DRIVERS
    rows_out = []
    for fw in ["intelligence", "sapience", "artificial_wisdom"]:
        for year in [2050, 2100, 2200]:
            weights = DRIVER_CONTRIBUTIONS[fw][year]
            row = {"framework": fw, "year": year}
            for driver, w in zip(WARMING_DRIVERS, weights):
                row[driver] = round(w, 4)
            rows_out.append(row)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    print("Running warming factor simulation...")
    results = run_warming_scenarios()

    save_timeseries_csv(
        results,
        os.path.join(RESULTS_DIR, "warming_factor_timeseries.csv")
    )
    save_summary_csv(
        results,
        os.path.join(RESULTS_DIR, "warming_factor_summary.csv")
    )
    save_driver_breakdown_csv(
        os.path.join(RESULTS_DIR, "warming_driver_breakdown.csv")
    )

    print("\nWarming factor summary (mean survivability):")
    for fw, rows in results.items():
        summary = {r["year"]: r["mean_survivability"]
                   for r in rows if r["year"] in [2050, 2100, 2200]}
        print(f"  {fw:20s}  2050={summary.get(2050, '?'):5.1f}  "
              f"2100={summary.get(2100, '?'):5.1f}  2200={summary.get(2200, '?'):5.1f}")
    print("Done.")
