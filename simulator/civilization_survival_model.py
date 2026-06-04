"""
Civilization Survival Toy Model
================================
A transparent, inspectable system-dynamics-style comparative simulation.

This is NOT a scientific forecast or empirical prediction.
It is a structured scenario model designed to make the logic of
value-system differences (Intelligence vs. Sapience vs. Artificial Wisdom)
falsifiable and inspectable.

All parameters are explicit and documented. Change them to test sensitivity.

State variables (normalized 0-100):
  warming_stress        - accumulated thermal/greenhouse pressure
  el_nino_stress        - oscillatory climate shock load
  biosphere_integrity   - overall health of planetary life systems
  resource_pressure     - depletion and scarcity burden
  social_cohesion       - political and community stability
  adaptive_capacity     - institutional and technological flexibility
  survivability_index   - composite civilization continuity metric

Framework parameters (0-1 scale):
  extraction_bias              - rate of resource extraction relative to regeneration
  short_termism                - weight on short-term vs. long-term outcomes
  ecological_feedback_awareness- speed of response to ecological deterioration
  regeneration_investment      - investment in restoring biosphere capacity
  cooperation_level            - coordination capacity across scales
  mitigation_speed             - speed of response to warming signals
  resilience_orientation       - structural preparation for shocks
"""

import random
import math
import csv
import os

YEAR_START = 2025
YEAR_END = 2200

# --- Framework parameter sets ---

FRAMEWORKS = {
    "intelligence": {
        "extraction_bias": 0.80,
        "short_termism": 0.80,
        "ecological_feedback_awareness": 0.20,
        "regeneration_investment": 0.10,
        "cooperation_level": 0.35,
        "mitigation_speed": 0.25,
        "resilience_orientation": 0.25,
    },
    "sapience": {
        "extraction_bias": 0.55,
        "short_termism": 0.50,
        "ecological_feedback_awareness": 0.50,
        "regeneration_investment": 0.35,
        "cooperation_level": 0.60,
        "mitigation_speed": 0.50,
        "resilience_orientation": 0.50,
    },
    "artificial_wisdom": {
        "extraction_bias": 0.20,
        "short_termism": 0.10,
        "ecological_feedback_awareness": 0.90,
        "regeneration_investment": 0.80,
        "cooperation_level": 0.85,
        "mitigation_speed": 0.80,
        "resilience_orientation": 0.85,
    },
}

# --- Initial state ---

INITIAL_STATE = {
    "warming_stress": 15.0,
    "el_nino_stress": 5.0,
    "biosphere_integrity": 72.0,
    "resource_pressure": 28.0,
    "social_cohesion": 65.0,
    "adaptive_capacity": 50.0,
}


def clamp(val, lo=0.0, hi=100.0):
    return max(lo, min(hi, val))


def compute_survivability(state):
    """
    Weighted composite survivability index.

    Positive contributors: adaptive_capacity, biosphere_integrity, social_cohesion
    Negative contributors: warming_stress, resource_pressure, el_nino_stress
    """
    raw = (
        0.25 * state["adaptive_capacity"]
        + 0.25 * state["biosphere_integrity"]
        + 0.20 * state["social_cohesion"]
        - 0.15 * state["warming_stress"]
        - 0.10 * state["resource_pressure"]
        - 0.05 * state["el_nino_stress"]
    )
    # normalize so initial survivability is ~65-75
    return clamp(raw / 0.70 * 1.0)


def step(state, params, el_nino_active=False, noise_scale=0.0, rng=None):
    """
    Advance state by one year.

    Equations are transparent and linear-ish; compounding is achieved
    through state variable interaction rather than exponential terms.
    """
    if rng is None:
        rng = random

    def n():
        return rng.gauss(0, noise_scale) if noise_scale > 0 else 0.0

    s = dict(state)

    # Base warming trend: rises ~0.25/yr under intelligence, ~0.10 under AW
    warming_base_rise = 0.30 * params["extraction_bias"] - 0.15 * params["mitigation_speed"]
    warming_biosphere_feedback = 0.05 * max(0, (100 - s["biosphere_integrity"]) / 100)
    s["warming_stress"] = clamp(
        s["warming_stress"] + warming_base_rise + warming_biosphere_feedback + n()
    )

    # El Nino: oscillatory shock applied externally; here we model natural decay
    el_nino_base = 5.0
    if el_nino_active:
        el_nino_pulse = 20.0 * (1.0 - params["resilience_orientation"])
    else:
        el_nino_pulse = 0.0
    # stress decays toward baseline between events
    s["el_nino_stress"] = clamp(
        0.85 * s["el_nino_stress"] + el_nino_pulse + el_nino_base * 0.05 + n()
    )

    # Biosphere integrity: damaged by warming/resource, restored by regeneration
    bio_damage = (
        0.08 * s["warming_stress"] / 100
        + 0.05 * s["resource_pressure"] / 100
        + 0.04 * s["el_nino_stress"] / 100
    )
    bio_recovery = 0.06 * params["regeneration_investment"] * (s["biosphere_integrity"] < 85)
    # ecological awareness accelerates recovery detection
    recovery_boost = params["ecological_feedback_awareness"] * 0.02
    s["biosphere_integrity"] = clamp(
        s["biosphere_integrity"] - bio_damage * 4.0 + bio_recovery + recovery_boost + n()
    )

    # Resource pressure: rises with extraction, falls slightly with circular economy
    rp_rise = 0.12 * params["extraction_bias"] * (1 + s["warming_stress"] / 200)
    rp_relief = 0.06 * params["regeneration_investment"]
    s["resource_pressure"] = clamp(s["resource_pressure"] + rp_rise - rp_relief + n())

    # Social cohesion: eroded by stress, buffered by cooperation
    stress_load = (
        0.03 * s["warming_stress"] / 100
        + 0.04 * s["resource_pressure"] / 100
        + 0.05 * s["el_nino_stress"] / 100
    )
    cohesion_recovery = 0.04 * params["cooperation_level"]
    s["social_cohesion"] = clamp(
        s["social_cohesion"] - stress_load * 3.0 + cohesion_recovery + n()
    )

    # Adaptive capacity: built by cooperation and resilience; degraded by social collapse
    ac_build = (
        0.03 * params["cooperation_level"]
        + 0.03 * params["resilience_orientation"]
        - 0.02 * params["short_termism"]
    )
    ac_drag = 0.02 * max(0, (50 - s["social_cohesion"])) / 100
    s["adaptive_capacity"] = clamp(s["adaptive_capacity"] + ac_build - ac_drag * 5 + n())

    s["survivability_index"] = compute_survivability(s)
    return s


def run_scenario(params, el_nino_schedule=None, noise_scale=3.0, n_runs=200, rng_seed=42):
    """
    Run Monte Carlo ensemble for a single framework.

    Returns: list of dicts {year: ..., mean_surv: ..., p10: ..., p90: ...}
    """
    years = list(range(YEAR_START, YEAR_END + 1))

    if el_nino_schedule is None:
        el_nino_schedule = set()

    all_runs = []
    for run_i in range(n_runs):
        rng = random.Random(rng_seed + run_i * 17)
        state = dict(INITIAL_STATE)
        state["survivability_index"] = compute_survivability(state)
        run_data = []
        for year in years:
            el_nino_active = year in el_nino_schedule
            state = step(state, params, el_nino_active=el_nino_active,
                         noise_scale=noise_scale, rng=rng)
            run_data.append((year, state["survivability_index"], dict(state)))
        all_runs.append(run_data)

    results = []
    for i, year in enumerate(years):
        surv_vals = sorted(run[i][1] for run in all_runs)
        n = len(surv_vals)
        mean_surv = sum(surv_vals) / n
        p10 = surv_vals[int(n * 0.10)]
        p90 = surv_vals[int(n * 0.90)]
        # also collect mean state variables from last run (representative)
        last_state = all_runs[0][i][2]
        results.append({
            "year": year,
            "mean_survivability": round(mean_surv, 2),
            "p10_survivability": round(p10, 2),
            "p90_survivability": round(p90, 2),
            "warming_stress": round(last_state["warming_stress"], 2),
            "el_nino_stress": round(last_state["el_nino_stress"], 2),
            "biosphere_integrity": round(last_state["biosphere_integrity"], 2),
            "resource_pressure": round(last_state["resource_pressure"], 2),
            "social_cohesion": round(last_state["social_cohesion"], 2),
            "adaptive_capacity": round(last_state["adaptive_capacity"], 2),
        })
    return results


def make_el_nino_schedule(start=2025, end=2200, base_interval=7, intensification=True):
    """
    Generate a set of years in which El Nino events occur.
    Frequency slowly increases under intensification assumption.
    """
    years = set()
    year = start + base_interval
    interval = base_interval
    while year <= end:
        years.add(year)
        if intensification:
            # interval shrinks slightly over time (from ~7 to ~5 years)
            elapsed_frac = (year - start) / (end - start)
            interval = max(5, base_interval - int(elapsed_frac * 2))
        year += interval
    return years


def save_timeseries_csv(results_by_framework, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = [
        "framework", "year",
        "mean_survivability", "p10_survivability", "p90_survivability",
        "warming_stress", "el_nino_stress", "biosphere_integrity",
        "resource_pressure", "social_cohesion", "adaptive_capacity",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for framework, rows in results_by_framework.items():
            for row in rows:
                row_out = {"framework": framework}
                row_out.update(row)
                writer.writerow(row_out)
    print(f"  Saved: {filepath}")


def save_summary_csv(results_by_framework, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    checkpoints = [2050, 2100, 2150, 2200]
    fieldnames = ["framework"] + [f"surv_{y}" for y in checkpoints]
    rows_out = []
    for framework, rows in results_by_framework.items():
        row_out = {"framework": framework}
        year_map = {r["year"]: r["mean_survivability"] for r in rows}
        for y in checkpoints:
            row_out[f"surv_{y}"] = year_map.get(y, "N/A")
        rows_out.append(row_out)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"  Saved: {filepath}")


def run_combined_scenario(n_runs=200, noise_scale=3.0):
    """Run combined warming + El Nino scenario for all three frameworks."""
    el_nino_schedule = make_el_nino_schedule()
    results = {}
    for fw, params in FRAMEWORKS.items():
        print(f"  Running combined scenario: {fw} ({n_runs} runs)...")
        results[fw] = run_scenario(params, el_nino_schedule=el_nino_schedule,
                                   noise_scale=noise_scale, n_runs=n_runs)
    return results


if __name__ == "__main__":
    print("Running civilization survival combined scenario...")
    results = run_combined_scenario()
    save_timeseries_csv(
        results,
        os.path.join("simulator", "results", "civilization_survival_timeseries.csv")
    )
    save_summary_csv(
        results,
        os.path.join("simulator", "results", "civilization_survival_summary.csv")
    )
    print("Done.")
    for fw, rows in results.items():
        summary = {r["year"]: r["mean_survivability"]
                   for r in rows if r["year"] in [2050, 2100, 2200]}
        print(f"  {fw:20s}  2050={summary.get(2050, '?'):5.1f}  "
              f"2100={summary.get(2100, '?'):5.1f}  2200={summary.get(2200, '?'):5.1f}")
