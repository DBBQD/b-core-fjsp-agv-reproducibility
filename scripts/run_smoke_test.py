"""Smoke-test the released B-CORE result package."""

from __future__ import annotations

from pathlib import Path
from common import EXPECTED, ROOT, close, compute_key_metrics

REQUIRED_FILES = [
    "README.md",
    "results/csv/fair_budget/fair_budget_raw.csv",
    "results/csv/fair_budget/fair_budget_best_by_setting.csv",
    "results/csv/main_results/main_results_raw.csv",
    "results/csv/main_results/ablation_raw.csv",
    "results/csv/optimality_gap/optimality_gap_raw.csv",
    "results/csv/weight_sensitivity/weight_random_search_raw.csv",
    "results/csv/weight_sensitivity/weight_single_factor_raw.csv",
    "results/csv/weight_sensitivity/weight_validation_raw.csv",
    "figures/fig4_reference_gap_distribution_final.pdf",
    "figures/fig5_quality_latency_tradeoff_final.pdf",
    "figures/fig6_rank_first_counts_final.pdf",
    "figures/fig7_ablation_final.pdf",
    "figures/fig8_weight_calibration_final.pdf",
]

TOLERANCES = {
    "bcore_equal_budget_mean_objective": 0.001,
    "bcore_mean_p95_latency": 0.000001,
    "main_bcore_mean_objective": 0.001,
    "no_transport_degradation_pct": 0.001,
    "no_bottleneck_degradation_pct": 0.001,
    "no_qp_degradation_pct": 0.001,
    "calibrated_top5_improvement_pct": 0.001,
    "calibrated_best_improvement_pct": 0.001,
}

def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        print("FAIL missing files:")
        for path in missing:
            print(f"  - {path}")
        return 1

    metrics = compute_key_metrics()
    failures = []
    for key, expected in EXPECTED.items():
        value = metrics[key]
        if isinstance(expected, int):
            ok = int(value) == expected
        else:
            ok = close(float(value), float(expected), TOLERANCES.get(key, 1e-9))
        if not ok:
            failures.append((key, value, expected))
    for key in ["failed_rows", "timeout_rows", "unavailable_rows"]:
        if int(metrics[key]) != 0:
            failures.append((key, metrics[key], 0))

    if failures:
        print("FAIL metric mismatches:")
        for key, value, expected in failures:
            print(f"  - {key}: got {value}, expected {expected}")
        return 1

    print("PASS B-CORE reproducibility smoke test")
    for key in sorted(EXPECTED):
        print(f"{key}: {metrics[key]}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
