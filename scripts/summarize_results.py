"""Summarize released B-CORE result CSV files."""

from __future__ import annotations

import csv
from common import EXPECTED, ROOT, compute_key_metrics

def main() -> int:
    metrics = compute_key_metrics()
    out = ROOT / "results" / "summary_tables" / "reproduced_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "expected"])
        writer.writeheader()
        for key in sorted(EXPECTED):
            writer.writerow({"metric": key, "value": metrics[key], "expected": EXPECTED[key]})
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
