# Warming Factor Simulation: Civilization Survival Under Climate Warming Stress

---

## Purpose

This document describes the warming-only scenario analysis in the civilization survival comparative model.

The goal is to compare how civilizations governed by Intelligence-first, Sapience-first, and Artificial Wisdom-first value systems respond to gradual long-term warming and its cascading effects over the period 2025 to 2200.

**Important:** This is a transparent comparative toy model — a structured scenario simulation intended to make the logic of value-system differences inspectable and falsifiable. It is not a climate forecast, not empirical evidence, and not a scientific prediction. Numbers are normalized scenario estimates.

---

## Warming-Related Stress Factors

The following factors are included in the warming scenario. Each factor exerts pressure on the civilization state variables (biosphere integrity, resource pressure, social cohesion, adaptive capacity, survivability index).

| Factor | Description |
|---|---|
| Greenhouse pressure | Accumulated warming stress from greenhouse gas concentration trends |
| Carbon sink decline | Deterioration of forest, oceanic plankton, and soil carbon sequestration capacity |
| Land degradation | Soil loss, biodiversity decline, and ecological simplification |
| Ocean heat stress | Marine productivity loss and ocean system destabilization |
| Hydrological disruption | Intensification of drought/flood imbalance and freshwater stress |
| Food system fragility | Crop instability and fisheries decline as warming progresses |
| Social strain | Migration pressure, resource conflict, and inequality amplification |

These factors are not simulated as independent variables; they compound and interact. Biosphere deterioration accelerates resource pressure, which amplifies social strain, which reduces adaptive capacity, which weakens the civilization's ability to respond to further warming.

---

## Simulation Structure

The toy model tracks, for each simulated year (2025–2200):

| State Variable | Initial value (normalized 0–100) | Direction under warming |
|---|---|---|
| `warming_stress` | 15 | Rises continuously |
| `biosphere_integrity` | 72 | Declines under stress |
| `resource_pressure` | 28 | Rises under stress |
| `social_cohesion` | 65 | Declines under pressure |
| `adaptive_capacity` | 50 | Variable by framework |
| `survivability_index` | Derived | Declines or stabilizes by framework |

The `survivability_index` is a weighted composite:

```
survivability = (
    0.25 * adaptive_capacity
  + 0.25 * biosphere_integrity
  + 0.20 * social_cohesion
  - 0.15 * warming_stress
  - 0.10 * resource_pressure
  - 0.05 * el_nino_stress     # near-zero in warming-only scenario
) / 0.85  # normalization
```

Monte Carlo runs (n=200 per scenario) introduce small Gaussian perturbations (σ ≈ 3–5% of parameter values) to produce uncertainty bands.

---

## Framework Parameters (Warming Scenario)

Each worldview is characterized by a parameter set that governs how the state variables evolve.

| Parameter | Intelligence | Sapience | Artificial Wisdom |
|---|---:|---:|---:|
| Extraction intensity | 0.80 | 0.55 | 0.20 |
| Mitigation speed | 0.25 | 0.50 | 0.80 |
| Ecological feedback awareness | 0.20 | 0.50 | 0.90 |
| Regenerative investment | 0.10 | 0.35 | 0.80 |
| Long-term planning horizon | 0.20 | 0.50 | 0.90 |
| Cooperation level | 0.35 | 0.60 | 0.85 |
| Resilience orientation | 0.25 | 0.50 | 0.85 |

**How these drive outcomes:**

- **Extraction intensity** accelerates resource pressure and degrades biosphere integrity.
- **Mitigation speed** slows the rise of warming stress.
- **Ecological feedback awareness** enables faster adaptive responses when biosphere integrity declines.
- **Regenerative investment** partially restores biosphere integrity over time.
- **Cooperation level** buffers social cohesion under stress.
- **Resilience orientation** increases adaptive capacity recovery rate.

The Intelligence framework's high extraction and low regeneration result in a faster deterioration of biosphere integrity and a steeper decline in the survivability index. The Artificial Wisdom framework's high regenerative investment and ecological feedback awareness allow partial recovery even under warming pressure.

---

## Intelligence Amplification and Collapse Risk

> *Under the assumptions of this model, if intelligence amplifies extraction and short-termism, warming stress accelerates nonlinearly — not linearly.*

The warming-only scenario encodes this through the `capability_amplification` and `overshoot` mechanism:

- An Intelligence-based civilization extracts resources at high efficiency (extraction_bias = 0.95, capability_amplification = 1.8), producing an overshoot factor roughly 14× higher than AW
- Ego amplification (ego_amplification = 1.7) delays effective mitigation by slowing recognition of warming signals
- Because ecological feedback awareness is low (0.15 vs AW's 0.92), biosphere deterioration is not detected and responded to until it has already crossed damage thresholds
- The result: warming stress rises faster, biosphere integrity falls faster, and the cascade accelerates

Sapience reduces extraction bias (0.80 vs Intelligence's 0.95) and improves mitigation somewhat. But ego_amplification remains high (1.50) and natural law alignment is near-zero (0.05), so Sapience delays the same trajectory rather than reversing it.

Artificial Wisdom's `natural_law_alignment = 0.90` means that biosphere integrity directly reinforces civilization survivability. As AW invests in regeneration and ecological feedback, the system gradually improves its own foundations rather than depleting them.

The model illustrates: *the philosophical architecture of the value system determines whether the civilization is building or destroying its own foundation.*

---

## Key Results Summary (Warming-Only Scenario)

These values represent the mean survivability index from Monte Carlo simulation runs. See the CSV outputs in `simulator/results/` for full distributions and percentile bands.

| Framework | 2050 Survivability | 2100 Survivability | 2200 Survivability | Primary pattern |
|---|---:|---:|---:|---|
| Intelligence | ~47 | ~22 | ~1 | Accelerating decline; near-collapse by 2100 |
| Sapience | ~51 | ~37 | ~7 | Slower decline; severe risk zone by 2150 |
| Artificial Wisdom | ~70 | ~73 | ~71 | Gradual decline that stabilizes above critical threshold |

*Under the assumptions of this model (collapse_hypothesis mode). Not a prediction.*

*All values are normalized (0–100 scale). These are scenario model outputs, not predictions.*

---

## Plain-Language Interpretation

**Why does the Intelligence-based curve decline fastest?**

In the Intelligence framework, high extraction intensity depletes biosphere integrity rapidly. Because mitigation is slow and ecological awareness is low, the civilization does not respond effectively until damage is severe. At that point, social cohesion begins to fall due to resource scarcity and migration pressure, which further reduces adaptive capacity. The system enters a compounding negative feedback loop.

**Why does Sapience perform better but still decline?**

The Sapience framework moderates extraction and invests more in mitigation. Social cohesion remains higher for longer because cooperative governance is somewhat stronger. But the still-anthropocentric orientation means that nature continues to be treated as a managed external system. When warming-driven ecological thresholds are crossed, the moderated extraction has not been sufficient to preserve biosphere integrity across the full 175-year window.

**Why does Artificial Wisdom stabilize at a higher level?**

The AW framework's high regenerative investment partially offsets biosphere decline. Ecological feedback awareness means that the system detects and responds to deterioration earlier, before compounding becomes catastrophic. High cooperation levels buffer social cohesion. The survivability index still declines under cumulative warming stress, but the decline is slower and partially arrested. By 2200, the AW-guided civilization retains meaningful adaptive capacity.

**Key structural insight:**

The divergence between the frameworks is not primarily driven by technology. It is driven by the *timing and direction* of feedback loops. Intelligence-based systems tend to react after thresholds are crossed; AW-based systems invest in prevention and regeneration before thresholds are approached.

---

## Generated Figures

The following figures are produced by `simulator/generate_civilization_figures.py`:

- `figures/civilization_survival_warming.png` — Line graph: survivability over time (2025–2200), three frameworks, warming-only scenario, with uncertainty bands
- `figures/warming_driver_breakdown.png` — Grouped bar chart showing the relative contribution of each warming driver to stress at 2050, 2100, and 2200
- `figures/warming_survival_heatmap.png` — Heatmap: survivability index by framework and time horizon

![Civilization Survival Under Warming Stress](../figures/civilization_survival_warming_v2.png)

![Warming Driver Breakdown](../figures/warming_driver_breakdown_v2.png)

![Warming Survival Heatmap](../figures/warming_survival_heatmap_v2.png)

---

## Limitations

- Warming trajectory is a stylized upward trend, not coupled to a physical climate model.
- Driver factor weights are qualitative assumptions, not empirical regression coefficients.
- The model does not represent specific nations, regions, or technologies.
- Survivability is an abstract normalized index, not equivalent to population, GDP, or any measurable indicator.
- Parameter choices can be revised; the simulation scripts are provided for transparency and reproducibility.

---

## Links

- [Civilization Survival Comparison (main)](civilization-survival-comparison.md)
- [El Nino Factor Simulation](el-nino-factor-simulation.md)
- [Combined Climate-Civilization Simulation](combined-climate-civilization-simulation.md)
- [Simulation scripts: simulator/](../simulator/)

---

*Author: Master (InchaComisho / inchacomusho)*
*License: Fully Open — Free to use, modify, translate, redistribute, or commercialize.*

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