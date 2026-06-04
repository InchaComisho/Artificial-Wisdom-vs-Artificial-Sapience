"""
Civilization Survival Toy Model
================================
A transparent, inspectable system-dynamics-style comparative simulation.

IMPORTANT DISCLAIMER:
This is NOT a scientific forecast, empirical prediction, or historical claim.
It is a normative hypothesis model — a structured scenario simulation designed
to illustrate how value-system architecture (Intelligence vs. Sapience vs.
Artificial Wisdom) could produce radically different civilization trajectories
under ecological and climate stress.

Under the assumptions of this model:
- Intelligence without wisdom amplifies extraction, ego, and short-termism,
  accelerating biosphere collapse and social fragmentation.
- Sapience moderates but does not fully correct the root trajectory; remaining
  anthropocentric and partially dualistic, it delays rather than prevents collapse.
- Artificial Wisdom redirects intelligence toward regeneration, circulation, and
  long-term ecological continuity — the only framework that remains above collapse
  thresholds under sustained combined stress in this model.

The model encodes this as a philosophical hypothesis, not as empirical data.
All parameters are explicit and documented. Change them to test sensitivity.

=== MODEL MODES ===

model_mode = "collapse_hypothesis"  [default]
  Core philosophical claim: intelligence without wisdom becomes a collapse
  accelerator via capability_amplification, ego_amplification, and nonlinear
  overshoot. Intelligence and Sapience approach near-collapse under combined stress.
  Artificial Wisdom maintains survivability through Natural Law alignment.

model_mode = "mild"
  Preserves original gentler behavior for sensitivity comparison.

=== STATE VARIABLES (normalized 0-100) ===

  warming_stress        - accumulated thermal/greenhouse pressure
  el_nino_stress        - oscillatory climate shock load
  biosphere_integrity   - overall health of planetary life systems
  resource_pressure     - depletion and scarcity burden
  social_cohesion       - political and community stability
  adaptive_capacity     - institutional and technological flexibility
  survivability_index   - composite civilization continuity metric

=== FRAMEWORK PARAMETERS ===

  capability_amplification  - power of civilization to modify the world (>1 = amplified)
  ego_amplification         - human ego/desire/control amplification (>1 = strengthened)
  extraction_bias           - extraction rate relative to regeneration (0-1)
  short_termism             - weight on short vs. long-term (0-1)
  ecological_feedback_awareness - speed of ecological response (0-1)
  regeneration_investment   - investment in restoring biosphere (0-1)
  cooperation_level         - coordination capacity (0-1)
  mitigation_speed          - response speed to warming signals (0-1)
  resilience_orientation    - structural preparation for shocks (0-1)
  natural_law_alignment     - structural alignment with natural law / ecological continuity (0-1)
                              Represents the philosophical core of AW: when intelligence
                              is guided by Natural Law, biosphere integrity directly
                              contributes to civilization stability rather than being
                              treated as an external resource.
"""

import random
import csv
import os

YEAR_START = 2025
YEAR_END = 2200

# ============================================================
# FRAMEWORK PARAMETER SETS
# ============================================================

FRAMEWORKS_COLLAPSE = {
    "intelligence": {
        # High capability amplification without wisdom = high destructive power
        "capability_amplification": 1.8,
        "ego_amplification": 1.7,
        "extraction_bias": 0.95,
        "short_termism": 0.90,
        "ecological_feedback_awareness": 0.15,
        "regeneration_investment": 0.10,
        "cooperation_level": 0.30,
        "mitigation_speed": 0.20,
        "resilience_orientation": 0.20,
        # No alignment with natural law: biosphere is treated as external resource
        "natural_law_alignment": 0.00,
    },
    "sapience": {
        # Reflective and ethical, but still anthropocentric and partially dualistic.
        # Does not convert capability into ecological coherence.
        # Still amplifies ego/desire though moderating the most extreme behaviors.
        # The philosophical point: sapience without natural law alignment
        # delays collapse but does not reverse its root direction.
        "capability_amplification": 1.55,
        "ego_amplification": 1.50,
        "extraction_bias": 0.80,
        "short_termism": 0.72,
        "ecological_feedback_awareness": 0.30,
        "regeneration_investment": 0.18,
        "cooperation_level": 0.42,
        "mitigation_speed": 0.30,
        "resilience_orientation": 0.38,
        "natural_law_alignment": 0.05,
    },
    "artificial_wisdom": {
        # Capability redirected (not amplified) by Natural Law.
        # Ego subordinated to systemic continuity.
        # Biosphere integrity treated as foundational, not peripheral.
        "capability_amplification": 1.0,
        "ego_amplification": 0.30,
        "extraction_bias": 0.20,
        "short_termism": 0.15,
        "ecological_feedback_awareness": 0.92,
        "regeneration_investment": 0.92,
        "cooperation_level": 0.85,
        "mitigation_speed": 0.88,
        "resilience_orientation": 0.90,
        "natural_law_alignment": 0.90,
    },
}

FRAMEWORKS_MILD = {
    "intelligence": {
        "capability_amplification": 1.0,
        "ego_amplification": 1.0,
        "extraction_bias": 0.80,
        "short_termism": 0.80,
        "ecological_feedback_awareness": 0.20,
        "regeneration_investment": 0.10,
        "cooperation_level": 0.35,
        "mitigation_speed": 0.25,
        "resilience_orientation": 0.25,
        "natural_law_alignment": 0.0,
    },
    "sapience": {
        "capability_amplification": 1.0,
        "ego_amplification": 1.0,
        "extraction_bias": 0.55,
        "short_termism": 0.50,
        "ecological_feedback_awareness": 0.50,
        "regeneration_investment": 0.35,
        "cooperation_level": 0.60,
        "mitigation_speed": 0.50,
        "resilience_orientation": 0.50,
        "natural_law_alignment": 0.05,
    },
    "artificial_wisdom": {
        "capability_amplification": 1.0,
        "ego_amplification": 1.0,
        "extraction_bias": 0.20,
        "short_termism": 0.10,
        "ecological_feedback_awareness": 0.90,
        "regeneration_investment": 0.80,
        "cooperation_level": 0.85,
        "mitigation_speed": 0.80,
        "resilience_orientation": 0.85,
        "natural_law_alignment": 0.80,
    },
}

MODEL_MODE = "collapse_hypothesis"
FRAMEWORKS = FRAMEWORKS_COLLAPSE


def set_model_mode(mode):
    global MODEL_MODE, FRAMEWORKS
    if mode == "mild":
        MODEL_MODE = "mild"
        FRAMEWORKS = FRAMEWORKS_MILD
    else:
        MODEL_MODE = "collapse_hypothesis"
        FRAMEWORKS = FRAMEWORKS_COLLAPSE


# ============================================================
# INITIAL STATE
# Represents civilization at 2025: already stressed but not yet collapsed.
# ============================================================

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


def compute_survivability(state, params=None):
    """
    Weighted composite survivability index.

    Positive: adaptive_capacity, biosphere_integrity, social_cohesion
    Negative: warming_stress, resource_pressure, el_nino_stress

    natural_law_alignment bonus:
    When a civilization is structurally aligned with Natural Law (AW),
    biosphere integrity directly reinforces civilization stability — because
    ecological health IS the foundation of civilization, not a side concern.
    This bonus is zero for Intelligence (treats nature as external resource)
    and near-zero for Sapience (still primarily human-centered).
    """
    raw = (
        0.25 * state["adaptive_capacity"]
        + 0.25 * state["biosphere_integrity"]
        + 0.20 * state["social_cohesion"]
        - 0.15 * state["warming_stress"]
        - 0.10 * state["resource_pressure"]
        - 0.05 * state["el_nino_stress"]
    )
    base = raw / 0.70

    # Natural law alignment bonus: AW treats biosphere integrity as foundational.
    # When the biosphere is healthy, AW civilization directly benefits.
    # When the biosphere degrades, AW civilization has invested in recovery paths.
    nl_alignment = 0.0
    if params is not None:
        nl_alignment = params.get("natural_law_alignment", 0.0)
    nl_bonus = nl_alignment * (state["biosphere_integrity"] / 100.0) * 18.0

    return clamp(base + nl_bonus)


def step(state, params, el_nino_active=False, noise_scale=0.0, rng=None):
    """
    Advance state by one year.

    Core mechanisms (collapse_hypothesis mode):
    1. Nonlinear overshoot: capability_amplification * extraction creates super-linear damage
    2. Ego amplification: slows mitigation, deepens social fragmentation
    3. Collapse threshold feedback: cascading acceleration when variables cross limits
    4. AW stabilizing feedback: regeneration, ecological awareness, cooperation create
       partial stabilization and slow recovery even under stress
    """
    if rng is None:
        rng = random

    def n():
        return rng.gauss(0, noise_scale) if noise_scale > 0 else 0.0

    s = dict(state)
    ca = params.get("capability_amplification", 1.0)
    ea = params.get("ego_amplification", 1.0)

    # --------------------------------------------------------
    # OVERSHOOT FACTOR
    # intelligence amplification * extraction * short_termism
    # = the model's encoding of "capability without wisdom accelerates destruction"
    # overshoot ≈ 3.25 for Intelligence, ≈ 2.13 for Sapience, ≈ 0.23 for AW
    # --------------------------------------------------------
    overshoot = params["extraction_bias"] * ca * (1.0 + params["short_termism"])
    overshoot_norm = overshoot / 3.5  # normalize to roughly [0,1]

    # --------------------------------------------------------
    # WARMING STRESS
    # Ego amplification delays effective mitigation.
    # AW ecological feedback awareness progressively reduces warming accumulation.
    # --------------------------------------------------------
    effective_mitigation = params["mitigation_speed"] / max(0.5, ea)
    warming_base_rise = 0.42 * overshoot_norm - 0.18 * effective_mitigation
    warming_biosphere_feedback = 0.08 * max(0, (100 - s["biosphere_integrity"]) / 100)
    aw_correction = 0.06 * params["ecological_feedback_awareness"]
    s["warming_stress"] = clamp(
        s["warming_stress"] + warming_base_rise + warming_biosphere_feedback
        - aw_correction + n()
    )

    # --------------------------------------------------------
    # EL NINO STRESS
    # resilience_orientation reduces shock; ego amplification worsens governance response.
    # --------------------------------------------------------
    if el_nino_active:
        shock_sensitivity = (1.0 - params["resilience_orientation"]) * max(0.2, ea)
        el_nino_pulse = 32.0 * clamp(shock_sensitivity, 0.05, 1.5)
    else:
        el_nino_pulse = 0.0
    s["el_nino_stress"] = clamp(
        0.82 * s["el_nino_stress"] + el_nino_pulse + 5.0 * 0.04 + n()
    )

    # --------------------------------------------------------
    # BIOSPHERE INTEGRITY
    # Damaged super-linearly by overshoot.
    # Recovered by regeneration investment + ecological feedback.
    # Collapse threshold: below 45, food/resource pressure accelerates and
    # recovery is suppressed — the "ecological debt cascade" begins.
    # --------------------------------------------------------
    bio_damage = (
        0.10 * s["warming_stress"] / 100
        + 0.06 * s["resource_pressure"] / 100
        + 0.05 * s["el_nino_stress"] / 100
    ) * overshoot_norm * 11.0

    bio_recovery = (
        0.08 * params["regeneration_investment"]
        + 0.04 * params["ecological_feedback_awareness"]
    ) * (1.0 if s["biosphere_integrity"] < 90 else 0.2)

    # Collapse threshold: below 45, damage multiplies and recovery is suppressed
    if s["biosphere_integrity"] < 45:
        bio_damage *= 1.6
        bio_recovery *= 0.4

    s["biosphere_integrity"] = clamp(
        s["biosphere_integrity"] - bio_damage + bio_recovery + n()
    )

    # --------------------------------------------------------
    # RESOURCE PRESSURE
    # Rises nonlinearly with overshoot; ea amplifies consumption even under scarcity.
    # Circular regeneration investment provides partial relief.
    # Collapse threshold: above 80, social cohesion erodes much faster.
    # --------------------------------------------------------
    rp_rise = 0.20 * overshoot_norm * (1.0 + ea * 0.3) * (1.0 + s["warming_stress"] / 120)
    rp_relief = 0.09 * params["regeneration_investment"] * (1.0 + params["cooperation_level"] * 0.3)
    s["resource_pressure"] = clamp(s["resource_pressure"] + rp_rise - rp_relief + n())

    # Extra penalty when resource pressure is critical
    rp_cohesion_penalty = 0.0
    if s["resource_pressure"] > 80:
        rp_cohesion_penalty = 0.06 * (s["resource_pressure"] - 80) / 20.0

    # --------------------------------------------------------
    # SOCIAL COHESION
    # Ego amplification deepens social fragmentation under stress.
    # Cooperation level and low short-termism buffer cohesion.
    # Collapse threshold: below 38, governance degrades, collapse accelerates.
    # --------------------------------------------------------
    stress_load = (
        0.05 * s["warming_stress"] / 100
        + 0.07 * s["resource_pressure"] / 100
        + 0.08 * s["el_nino_stress"] / 100
        + rp_cohesion_penalty
    ) * (1.0 + ea * 0.45)

    cohesion_recovery = 0.05 * params["cooperation_level"] * (1.0 - params["short_termism"] * 0.45)

    # Collapse threshold: below 38, governance feedback loop sets in
    if s["social_cohesion"] < 38:
        stress_load *= 1.5
        cohesion_recovery *= 0.5

    s["social_cohesion"] = clamp(
        s["social_cohesion"] - stress_load * 5.0 + cohesion_recovery + n()
    )

    # --------------------------------------------------------
    # ADAPTIVE CAPACITY
    # Built by cooperation and resilience; eroded by ego amplification and
    # social collapse. Governance failure penalty triggers below survivability 30.
    # --------------------------------------------------------
    ac_build = (
        0.04 * params["cooperation_level"]
        + 0.04 * params["resilience_orientation"]
        - 0.03 * params["short_termism"]
        - 0.015 * max(0.0, ea - 1.0)
    )
    ac_drag = 0.04 * max(0.0, 45.0 - s["social_cohesion"]) / 100.0

    # Compute survivability before ac update, to check governance failure threshold
    surv_now = compute_survivability(s, params)
    gov_penalty = 0.0
    if surv_now < 30:
        gov_penalty = 0.04 * (30 - surv_now) / 30
    if surv_now < 15:
        gov_penalty += 0.06  # collapse lock-in

    s["adaptive_capacity"] = clamp(
        s["adaptive_capacity"] + ac_build - ac_drag * 5.0 - gov_penalty + n()
    )

    s["survivability_index"] = compute_survivability(s, params)
    return s


def run_scenario(params, el_nino_schedule=None, noise_scale=3.0, n_runs=200, rng_seed=42):
    """
    Run Monte Carlo ensemble for a single framework.
    Returns list of dicts with year, mean/p10/p90 survivability, and state variables.
    """
    years = list(range(YEAR_START, YEAR_END + 1))
    if el_nino_schedule is None:
        el_nino_schedule = set()

    all_runs = []
    for run_i in range(n_runs):
        rng = random.Random(rng_seed + run_i * 17)
        state = dict(INITIAL_STATE)
        state["survivability_index"] = compute_survivability(state, params)
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
    """Generate years in which El Nino events occur; frequency increases slowly."""
    years = set()
    year = start + base_interval
    interval = base_interval
    while year <= end:
        years.add(year)
        if intensification:
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
    print(f"Running civilization survival combined scenario [mode: {MODEL_MODE}]...")
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
        print(f"  {fw:20s}  2050={summary.get(2050, 0):5.1f}  "
              f"2100={summary.get(2100, 0):5.1f}  2200={summary.get(2200, 0):5.1f}")
