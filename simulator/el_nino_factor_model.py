"""
El Nino Factor Model
====================
Runs the El Nino-only scenario using the civilization survival toy model.

El Nino events are applied as periodic oscillatory shocks. Warming stress
is suppressed to near-baseline to isolate El Nino effects.

Output:
  simulator/results/el_nino_factor_timeseries.csv
  simulator/results/el_nino_factor_summary.csv
  simulator/results/el_nino_driver_breakdown.csv
"""

import os
import csv
import sys

sys.path.insert(0, os.path.dirname(__file__))
from civilization_survival_model import (
    FRAMEWORKS, INITIAL_STATE, YEAR_START, YEAR_END,
    run_scenario, save_timeseries_csv, save_summary_csv,
    make_el_nino_schedule, clamp
)

RESULTS_DIR = os.path.join("simulator", "results")

EL_NINO_DRIVERS = [
    "event_frequency",
    "event_intensity",
    "agricultural_shock",
    "marine_productivity_shock",
    "wildfire_amplification",
    "infrastructure_stress",
    "social_instability",
]

# Driver contribution weights at three checkpoints
# These represent how each El Nino stressor contributes to total
# oscillatory stress under each framework
DRIVER_CONTRIBUTIONS = {
    "intelligence": {
        2050: [0.20, 0.18, 0.22, 0.15, 0.10, 0.10, 0.05],
        2100: [0.18, 0.18, 0.23, 0.15, 0.11, 0.10, 0.05],
        2200: [0.17, 0.18, 0.24, 0.15, 0.11, 0.10, 0.05],
    },
    "sapience": {
        2050: [0.20, 0.17, 0.19, 0.14, 0.11, 0.11, 0.08],
        2100: [0.19, 0.17, 0.19, 0.14, 0.12, 0.11, 0.08],
        2200: [0.18, 0.17, 0.20, 0.14, 0.12, 0.11, 0.08],
    },
    "artificial_wisdom": {
        2050: [0.19, 0.16, 0.16, 0.13, 0.13, 0.12, 0.11],
        2100: [0.18, 0.16, 0.17, 0.13, 0.13, 0.12, 0.11],
        2200: [0.17, 0.16, 0.17, 0.14, 0.14, 0.12, 0.10],
    },
}


def run_el_nino_scenarios(n_runs=200, noise_scale=3.0):
    """
    Run El Nino-only scenarios.

    Warming stress rise is suppressed (mitigation_speed set to max for
    this isolated analysis) so that we isolate El Nino effects.
    """
    el_nino_schedule = make_el_nino_schedule()
    results = {}

    for fw, params in FRAMEWORKS.items():
        print(f"  Running El Nino-only scenario: {fw} ({n_runs} runs)...")
        # Suppress warming accumulation to isolate El Nino effect
        modified_params = dict(params)
        modified_params["mitigation_speed"] = min(1.0, params["mitigation_speed"] + 0.20)
        modified_params["extraction_bias"] = max(0.0, params["extraction_bias"] - 0.15)

        results[fw] = run_scenario(
            modified_params,
            el_nino_schedule=el_nino_schedule,
            noise_scale=noise_scale,
            n_runs=n_runs,
        )
    return results


def save_driver_breakdown_csv(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = ["framework", "year"] + EL_NINO_DRIVERS
    rows_out = []
    for fw in ["intelligence", "sapience", "artificial_wisdom"]:
        for year in [2050, 2100, 2200]:
            weights = DRIVER_CONTRIBUTIONS[fw][year]
            row = {"framework": fw, "year": year}
            for driver, w in zip(EL_NINO_DRIVERS, weights):
                row[driver] = round(w, 4)
            rows_out.append(row)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    print("Running El Nino factor simulation...")
    results = run_el_nino_scenarios()

    save_timeseries_csv(
        results,
        os.path.join(RESULTS_DIR, "el_nino_factor_timeseries.csv")
    )
    save_summary_csv(
        results,
        os.path.join(RESULTS_DIR, "el_nino_factor_summary.csv")
    )
    save_driver_breakdown_csv(
        os.path.join(RESULTS_DIR, "el_nino_driver_breakdown.csv")
    )

    print("\nEl Nino factor summary (mean survivability):")
    for fw, rows in results.items():
        summary = {r["year"]: r["mean_survivability"]
                   for r in rows if r["year"] in [2050, 2100, 2200]}
        print(f"  {fw:20s}  2050={summary.get(2050, '?'):5.1f}  "
              f"2100={summary.get(2100, '?'):5.1f}  2200={summary.get(2200, '?'):5.1f}")
    print("Done.")
