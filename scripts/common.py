"""Shared helpers for the B-CORE reproducibility scripts."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_ROOT = ROOT / "results" / "csv"
PLOT_ROOT = ROOT / "results" / "plot_data"

EXPECTED = {
    "exact_benchmark_rows": 1280,
    "fair_budget_rows": 2250,
    "weight_sensitivity_rows": 28101,
    "main_results_rows": 1080,
    "ablation_rows": 450,
    "bcore_rank_first": 96,
    "matched_settings": 225,
    "bcore_equal_budget_mean_objective": 94.906,
    "bcore_mean_p95_latency": 0.000353,
    "main_bcore_mean_objective": 94.620,
    "no_transport_degradation_pct": 23.487,
    "no_bottleneck_degradation_pct": 5.617,
    "no_qp_degradation_pct": 0.278,
    "calibrated_top5_improvement_pct": 2.905,
    "calibrated_best_improvement_pct": 5.781,
    "tiny_exact_rows": 40,
    "cpsat_relaxed_rows": 1240,
}

def read_rows(rel_path: str) -> list[dict[str, str]]:
    path = ROOT / rel_path
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def mean(values: list[float]) -> float:
    return sum(values) / len(values)

def close(value: float, target: float, tol: float) -> bool:
    return abs(value - target) <= tol

def compute_key_metrics() -> dict[str, float | int]:
    fair = read_rows("results/csv/fair_budget/fair_budget_raw.csv")
    best = read_rows("results/csv/fair_budget/fair_budget_best_by_setting.csv")
    main = read_rows("results/csv/main_results/main_results_raw.csv")
    ablation_raw = read_rows("results/csv/main_results/ablation_raw.csv")
    ablation_summary = read_rows("results/csv/main_results/ablation_summary.csv")
    opt = read_rows("results/csv/optimality_gap/optimality_gap_raw.csv")
    weight_random = read_rows("results/csv/weight_sensitivity/weight_random_search_raw.csv")
    weight_single = read_rows("results/csv/weight_sensitivity/weight_single_factor_raw.csv")
    weight_validation = read_rows("results/csv/weight_sensitivity/weight_validation_raw.csv")
    weight_cal = read_rows("results/csv/weight_sensitivity/weight_calibration_validation_summary.csv")

    bcore_fair = [row for row in fair if row["algorithm"] == "B-CORE"]
    bcore_main = [row for row in main if row["algorithm"] == "B-CORE"]
    by_alg = {}
    for row in ablation_summary:
        by_alg.setdefault(row["algorithm"], []).append(float(row["objective_mean"]))
    ablation_mean = {alg: mean(vals) for alg, vals in by_alg.items()}
    base = ablation_mean["B-CORE"]
    cal_by_alg = {row["algorithm"]: float(row["objective_mean"]) for row in weight_cal}
    default = cal_by_alg["default"]

    return {
        "exact_benchmark_rows": len(opt),
        "fair_budget_rows": len(fair),
        "weight_sensitivity_rows": len(weight_random) + len(weight_single) + len(weight_validation),
        "main_results_rows": len(main),
        "ablation_rows": len(ablation_raw),
        "bcore_rank_first": sum(1 for row in best if row["best_algorithm"] == "B-CORE"),
        "matched_settings": len(best),
        "bcore_equal_budget_mean_objective": mean([float(row["objective"]) for row in bcore_fair]),
        "bcore_mean_p95_latency": mean([float(row["p95_event_latency"]) for row in bcore_fair]),
        "main_bcore_mean_objective": mean([float(row["objective"]) for row in bcore_main]),
        "no_transport_degradation_pct": (ablation_mean["B-CORE-no-transport"] - base) / base * 100.0,
        "no_bottleneck_degradation_pct": (ablation_mean["B-CORE-no-bottleneck"] - base) / base * 100.0,
        "no_qp_degradation_pct": (ablation_mean["B-CORE-no-qp"] - base) / base * 100.0,
        "calibrated_top5_improvement_pct": (default - cal_by_alg["calibrated-top5-average"]) / default * 100.0,
        "calibrated_best_improvement_pct": (default - cal_by_alg["calibrated-best-901227"]) / default * 100.0,
        "tiny_exact_rows": sum(1 for row in opt if row["model_type"] == "complete_simulator_branch_bound_agv_path_tiny"),
        "cpsat_relaxed_rows": sum(1 for row in opt if row["model_type"] == "cpsat_transport_capacity_relaxation_empty_repositioning_relaxed"),
        "failed_rows": sum(1 for row in fair + main + ablation_raw + opt if row.get("status") not in {"solved", ""}),
        "timeout_rows": sum(1 for row in opt if row.get("timeout", "").lower() == "true"),
        "unavailable_rows": sum(1 for row in fair + main + ablation_raw + opt if row.get("feasible", "true").lower() == "false"),
    }
