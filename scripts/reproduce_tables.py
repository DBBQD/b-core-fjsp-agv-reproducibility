"""Reproduce manuscript-facing summary tables from released CSV files."""

from __future__ import annotations

import csv
from common import EXPECTED, ROOT, compute_key_metrics

def write_table(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main() -> int:
    metrics = compute_key_metrics()
    summary_dir = ROOT / "results" / "summary_tables"
    write_table(
        summary_dir / "experiment_completeness.csv",
        [
            {"experiment": "exact benchmark", "rows": metrics["exact_benchmark_rows"], "expected": EXPECTED["exact_benchmark_rows"]},
            {"experiment": "fair budget", "rows": metrics["fair_budget_rows"], "expected": EXPECTED["fair_budget_rows"]},
            {"experiment": "weight sensitivity", "rows": metrics["weight_sensitivity_rows"], "expected": EXPECTED["weight_sensitivity_rows"]},
            {"experiment": "main results", "rows": metrics["main_results_rows"], "expected": EXPECTED["main_results_rows"]},
            {"experiment": "ablation", "rows": metrics["ablation_rows"], "expected": EXPECTED["ablation_rows"]},
        ],
        ["experiment", "rows", "expected"],
    )
    write_table(
        summary_dir / "manuscript_key_numbers.csv",
        [{"metric": key, "value": metrics[key], "expected": expected} for key, expected in EXPECTED.items()],
        ["metric", "value", "expected"],
    )
    print(f"Wrote summary tables under {summary_dir.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
