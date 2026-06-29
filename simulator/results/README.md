# Simulation Results

This directory contains CSV outputs from the civilization survival comparative scenario model.

**These are scenario model outputs, not empirical data or scientific predictions.**
All values are normalized (0–100 scale) estimates produced by a transparent toy model.
Parameters can be inspected and modified in the simulator scripts.

---

## How to Reproduce

From the repository root:

```bash
python simulator/run_all_simulations.py
```

Or run individual scenarios:

```bash
python simulator/warming_factor_model.py
python simulator/el_nino_factor_model.py
python simulator/civilization_survival_model.py
```

---

## CSV File Descriptions

| File | Description |
|---|---|
| `civilization_survival_timeseries.csv` | Combined (warming + El Nino) scenario: yearly survivability index per framework |
| `civilization_survival_summary.csv` | Combined scenario: survivability at key checkpoints (2050, 2100, 2150, 2200) |
| `warming_factor_timeseries.csv` | Warming-only scenario: yearly survivability index per framework |
| `warming_factor_summary.csv` | Warming-only scenario: survivability at key checkpoints |
| `warming_driver_breakdown.csv` | Per-framework relative contribution of each warming driver at 2050, 2100, 2200 |
| `el_nino_factor_timeseries.csv` | El Nino-only scenario: yearly survivability index per framework |
| `el_nino_factor_summary.csv` | El Nino-only scenario: survivability at key checkpoints |
| `el_nino_driver_breakdown.csv` | Per-framework relative contribution of each El Nino driver at 2050, 2100, 2200 |

---

## Column Descriptions (Timeseries Files)

| Column | Description |
|---|---|
| `framework` | `intelligence`, `sapience`, or `artificial_wisdom` |
| `year` | Simulated year (2025–2200) |
| `mean_survivability` | Mean survivability index across Monte Carlo runs (0–100) |
| `p10_survivability` | 10th percentile survivability |
| `p90_survivability` | 90th percentile survivability |
| `warming_stress` | Warming stress state variable |
| `el_nino_stress` | Oscillatory stress state variable |
| `biosphere_integrity` | Biosphere health state variable |
| `resource_pressure` | Resource depletion state variable |
| `social_cohesion` | Social stability state variable |
| `adaptive_capacity` | Adaptive flexibility state variable |

---

*Author: Master (InchaComisho / inchacomusho)*
*License: Fully Open*

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and advocate of the academic framework of Natural Complementary Science.  
Publicly active in natural-law philosophy, planetary circulation restoration, and co-creation with AI.

---

## License

CC BY 4.0

This article is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
Sharing, redistribution, translation, adaptation, and reuse are permitted as long as proper attribution is given.
