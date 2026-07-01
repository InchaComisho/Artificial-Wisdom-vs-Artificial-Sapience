# Figures

This directory contains graphs generated from the civilization survival comparative scenario model.

**These are scenario model visualizations, not empirical data charts or scientific predictions.**
All figures are produced from normalized toy model outputs. They are designed to make the
logic of value-system differences visually inspectable and comparable.

---

## How to Regenerate

From the repository root:

```bash
python simulator/run_all_simulations.py
```

Or just regenerate figures from existing CSVs:

```bash
python simulator/generate_civilization_figures.py
```

Requires: `matplotlib` (`pip install matplotlib`)

---

## Figure Descriptions

### Survivability Line Graphs

| File | Description |
|---|---|
| `civilization_survival_warming.png` | Survivability over 2025–2200 under warming-only stress, three frameworks, with uncertainty bands |
| `civilization_survival_el_nino.png` | Survivability over 2025–2200 under El Nino-only stress, three frameworks |
| `civilization_survival_combined.png` | Survivability over 2025–2200 under combined warming + El Nino stress |

### Driver Breakdown Charts

| File | Description |
|---|---|
| `warming_driver_breakdown.png` | Relative contribution of each warming driver at 2050, 2100, 2200 by framework |
| `el_nino_driver_breakdown.png` | Relative contribution of each El Nino driver at 2050, 2100, 2200 by framework |

### Comparison Charts

| File | Description |
|---|---|
| `combined_risk_comparison.png` | Side-by-side bar charts comparing survivability at 2100 and 2200 across scenarios |
| `framework_radar_comparison.png` | Radar chart comparing the six key parameter dimensions across all three frameworks |

### Heatmaps

| File | Description |
|---|---|
| `warming_survival_heatmap.png` | Survivability index by framework and sampled year (warming scenario) |
| `el_nino_survival_heatmap.png` | Survivability index by framework and sampled year (El Nino scenario) |

---

*Author: Master (InchaComisho / inchacomusho)*
*License: Fully Open*

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and proposer of the academic framework of Natural Complementary Science.  
Definer of the Cooling Credit Framework, and founder and original author of the Natural Cooling Value Evaluation Protocol.  
Definer and systematizer of the causal structure of global warming and its complete solution.

Master presents global warming not merely as a problem of CO₂ concentration, but as an integrated failure involving forest loss, soil degradation, disruption of water circulation, weakening of water phase-transition processes, weakening of atmospheric circulation, ocean circulation, food circulation and organic matter circulation, weakening of evapotranspiration, cloud formation and rainfall circulation, and the shutdown of natural cooling feedbacks.  
The proposed solution connects emission reduction, recovery of carbon fixation sources, physical cooling, reactivation of natural cooling functions, MRV, Cooling Credit, and Civilization OS into an open public framework.

Master publicly develops and shares work through NOTE, GitHub, and other public media, centered on natural-law philosophy, planetary circulation restoration, and co-creation with AI.

## License

CC BY 4.0

This article is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
Sharing, redistribution, translation, adaptation, and reuse are permitted as long as proper attribution is given.