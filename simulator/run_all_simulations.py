"""
Run All Simulations
===================
Orchestrates all simulation scripts and figure generation.

Usage:
  python simulator/run_all_simulations.py

Or from the simulator/ directory:
  python run_all_simulations.py
"""

import os
import sys
import importlib

# Resolve paths so this works whether run from repo root or simulator/
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(THIS_DIR)
RESULTS_DIR = os.path.join(REPO_ROOT, "simulator", "results")
FIGURES_DIR = os.path.join(REPO_ROOT, "figures")

# Ensure working directory is repo root so relative paths in modules resolve
os.chdir(REPO_ROOT)
sys.path.insert(0, THIS_DIR)


def ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    print(f"  Directories ready:")
    print(f"    {RESULTS_DIR}")
    print(f"    {FIGURES_DIR}")


def run_warming():
    print("\n=== [1/4] Warming Factor Simulation ===")
    import warming_factor_model
    importlib.reload(warming_factor_model)
    results = warming_factor_model.run_warming_scenarios(n_runs=200)
    warming_factor_model.save_timeseries_csv(
        results, os.path.join("simulator", "results", "warming_factor_timeseries.csv")
    )
    warming_factor_model.save_summary_csv(
        results, os.path.join("simulator", "results", "warming_factor_summary.csv")
    )
    warming_factor_model.save_driver_breakdown_csv(
        os.path.join("simulator", "results", "warming_driver_breakdown.csv")
    )
    return results


def run_el_nino():
    print("\n=== [2/4] El Nino Factor Simulation ===")
    import el_nino_factor_model
    importlib.reload(el_nino_factor_model)
    results = el_nino_factor_model.run_el_nino_scenarios(n_runs=200)
    el_nino_factor_model.save_timeseries_csv(
        results, os.path.join("simulator", "results", "el_nino_factor_timeseries.csv")
    )
    el_nino_factor_model.save_summary_csv(
        results, os.path.join("simulator", "results", "el_nino_factor_summary.csv")
    )
    el_nino_factor_model.save_driver_breakdown_csv(
        os.path.join("simulator", "results", "el_nino_driver_breakdown.csv")
    )
    return results


def run_combined():
    print("\n=== [3/4] Combined Stress Simulation ===")
    import civilization_survival_model
    importlib.reload(civilization_survival_model)
    results = civilization_survival_model.run_combined_scenario(n_runs=200)
    civilization_survival_model.save_timeseries_csv(
        results, os.path.join("simulator", "results", "civilization_survival_timeseries.csv")
    )
    civilization_survival_model.save_summary_csv(
        results, os.path.join("simulator", "results", "civilization_survival_summary.csv")
    )
    return results


def run_figures():
    print("\n=== [4/4] Generating Figures ===")
    import generate_civilization_figures
    importlib.reload(generate_civilization_figures)
    generate_civilization_figures.main()


def print_file_summary():
    print("\n=== Generated Files ===")

    csv_files = []
    for fname in os.listdir(RESULTS_DIR):
        if fname.endswith(".csv"):
            csv_files.append(os.path.join(RESULTS_DIR, fname))
    print(f"\nCSV outputs ({len(csv_files)}):")
    for f in sorted(csv_files):
        size = os.path.getsize(f)
        print(f"  {os.path.relpath(f, REPO_ROOT)}  ({size:,} bytes)")

    png_files = []
    for fname in os.listdir(FIGURES_DIR):
        if fname.endswith(".png"):
            png_files.append(os.path.join(FIGURES_DIR, fname))
    print(f"\nPNG figures ({len(png_files)}):")
    for f in sorted(png_files):
        size = os.path.getsize(f)
        print(f"  {os.path.relpath(f, REPO_ROOT)}  ({size:,} bytes)")

    print(f"\nTotal: {len(csv_files)} CSV files, {len(png_files)} PNG figures")


def main():
    print("=" * 60)
    print("Civilization Survival Comparative Simulation")
    print("Transparent toy model / scenario model")
    print("NOT a scientific prediction or empirical claim")
    print("=" * 60)

    ensure_dirs()
    run_warming()
    run_el_nino()
    run_combined()
    run_figures()
    print_file_summary()

    print("\n=== Summary Table (Mean Survivability) ===")
    print(f"{'Scenario':<22} {'Framework':<22} {'2050':>6} {'2100':>6} {'2200':>6}")
    print("-" * 68)

    try:
        import civilization_survival_model as csm
        import warming_factor_model as wfm
        import el_nino_factor_model as enm

        scenarios = [
            ("Warming-only", wfm.run_warming_scenarios(n_runs=50, noise_scale=2.0)),
            ("El Nino-only", enm.run_el_nino_scenarios(n_runs=50, noise_scale=2.0)),
            ("Combined", csm.run_combined_scenario(n_runs=50, noise_scale=2.0)),
        ]
        for scenario_name, results in scenarios:
            for fw, rows in results.items():
                s = {r["year"]: r["mean_survivability"]
                     for r in rows if r["year"] in [2050, 2100, 2200]}
                print(f"  {scenario_name:<20} {fw:<22} "
                      f"{s.get(2050, 0):6.1f} {s.get(2100, 0):6.1f} {s.get(2200, 0):6.1f}")
    except Exception as e:
        print(f"  (Summary table unavailable: {e})")

    print("\nDone. All simulations and figures complete.")
    print("\nNOTE: These are normalized scenario model outputs.")
    print("      Parameters are transparent and can be modified in the simulator scripts.")


if __name__ == "__main__":
    main()
