"""Regenerate Fig. 4 to Fig. 8 from released CSV files."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CSV_ROOT = ROOT / "results" / "csv"
OUT_DIR = ROOT / "figures" / "reproduced"

EVENT_ORDER = ["static", "breakdown", "rush_job", "mixed"]
EVENT_LABELS = {"static": "Static", "breakdown": "Breakdown", "rush_job": "Rush job", "mixed": "Mixed"}
REFERENCE_LABELS = {
    "complete_simulator_branch_bound_agv_path_tiny": "Tiny complete-simulator exact",
    "cpsat_transport_capacity_relaxation_empty_repositioning_relaxed": "CP-SAT transport-capacity relaxed",
}
ALGORITHM_ORDER = ["B-CORE", "B-CORE-no-graph", "B-CORE-no-bottleneck", "DCGA", "GA", "LNS", "MOEA-NSGA2", "MachineRank", "MOR", "SA"]
ALGORITHM_COLORS = {
    "B-CORE": "#1f77b4", "B-CORE-no-graph": "#4c78a8", "B-CORE-no-bottleneck": "#72b7b2",
    "DCGA": "#f58518", "GA": "#e45756", "LNS": "#54a24b", "MOEA-NSGA2": "#b279a2",
    "MachineRank": "#9d755d", "MOR": "#bab0ac", "SA": "#ff9da6",
}

def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def save_png(fig: plt.Figure, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

def draw_fig4() -> None:
    rows = read_rows(CSV_ROOT / "optimality_gap" / "optimality_gap_raw.csv")
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    offsets = [-0.18, 0.18]
    handles = []
    for ref_index, (model_type, label) in enumerate(REFERENCE_LABELS.items()):
        values, positions = [], []
        for event_index, event_type in enumerate(EVENT_ORDER):
            values.append([float(r["gap_pct_vs_exact_or_relaxed"]) for r in rows if r["model_type"] == model_type and r["event_type"] == event_type])
            positions.append(event_index + 1 + offsets[ref_index])
        box = ax.boxplot(values, positions=positions, widths=0.28, whis=(5, 95), showfliers=False, patch_artist=True, medianprops={"color": "black", "linewidth": 1.1})
        for patch in box["boxes"]:
            patch.set_facecolor(["#4c78a8", "#f58518"][ref_index])
            patch.set_alpha(0.72)
        handles.append(box["boxes"][0])
    ax.set_xticks(range(1, len(EVENT_ORDER) + 1))
    ax.set_xticklabels([EVENT_LABELS[e] for e in EVENT_ORDER])
    ax.set_ylabel("Gap to reference (%)")
    ax.set_xlabel("Event type")
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.6, alpha=0.8)
    ax.legend(handles, list(REFERENCE_LABELS.values()), frameon=False, loc="upper left")
    ax.set_ylim(bottom=-3)
    fig.tight_layout()
    save_png(fig, "fig4_reference_gap_distribution_reproduced")

def draw_fig5() -> None:
    rows = read_rows(CSV_ROOT / "fair_budget" / "fair_budget_raw.csv")
    acc = defaultdict(lambda: {"n": 0.0, "objective": 0.0, "latency": 0.0})
    for row in rows:
        alg = row["algorithm"]
        acc[alg]["n"] += 1
        acc[alg]["objective"] += float(row["objective"])
        acc[alg]["latency"] += float(row["p95_event_latency"])
    summary = [{"algorithm": alg, "objective": acc[alg]["objective"] / acc[alg]["n"], "latency": acc[alg]["latency"] / acc[alg]["n"]} for alg in ALGORITHM_ORDER]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    markers = ["o", "s", "^", "D", "P", "X", "v", "<", ">", "h"]
    for marker, row in zip(markers, summary):
        ax.scatter(row["latency"], row["objective"], s=58, marker=marker, color=ALGORITHM_COLORS[row["algorithm"]], edgecolor="white", linewidth=0.5, label=row["algorithm"])
    ax.set_xscale("log")
    ax.set_xlabel("Mean P95 event latency (s, log scale)")
    ax.set_ylabel("Mean objective")
    ax.grid(True, which="both", color="#d9d9d9", linewidth=0.55, alpha=0.8)
    ax.legend(ncol=5, fontsize=7.3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.20))
    fig.tight_layout()
    save_png(fig, "fig5_quality_latency_tradeoff_reproduced")

def draw_fig6() -> None:
    rows = read_rows(CSV_ROOT / "fair_budget" / "fair_budget_best_by_setting.csv")
    budgets = sorted({float(row["budget_sec"]) for row in rows})
    counts = {budget: {alg: 0 for alg in ALGORITHM_ORDER} for budget in budgets}
    for row in rows:
        if row["best_algorithm"] in ALGORITHM_ORDER:
            counts[float(row["budget_sec"])][row["best_algorithm"]] += 1
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    x = np.arange(len(budgets))
    bottom = np.zeros(len(budgets))
    for alg in ALGORITHM_ORDER:
        vals = np.array([counts[b][alg] for b in budgets])
        ax.bar(x, vals, bottom=bottom, width=0.68, label=alg, color=ALGORITHM_COLORS[alg], edgecolor="white", linewidth=0.45)
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels([f"{budget:g}" for budget in budgets])
    ax.set_xlabel("Event-time budget (s)")
    ax.set_ylabel("Rank-first count")
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.55, alpha=0.8)
    ax.legend(ncol=5, fontsize=7.3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    fig.tight_layout()
    save_png(fig, "fig6_rank_first_counts_reproduced")

def draw_fig7() -> None:
    rows = read_rows(CSV_ROOT / "main_results" / "ablation_summary.csv")
    order = ["B-CORE", "B-CORE-no-transport", "B-CORE-no-bottleneck", "B-CORE-no-qp", "B-CORE-no-graph"]
    means = {alg: np.mean([float(r["objective_mean"]) for r in rows if r["algorithm"] == alg]) for alg in order}
    base = means["B-CORE"]
    vals = [(means[alg] - base) / base * 100.0 for alg in order]
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    labels = ["B-CORE", "No transport", "No bottleneck", "No qp", "No graph"]
    colors = ["#1f77b4", "#e45756", "#72b7b2", "#f58518", "#4c78a8"]
    bars = ax.bar(np.arange(len(order)), vals, color=colors, edgecolor="#333333", linewidth=0.45)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.6, f"{val:.3f}%", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(np.arange(len(order)))
    ax.set_xticklabels(labels, rotation=18, ha="right")
    ax.set_ylabel("Relative objective change (%)")
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.55, alpha=0.8)
    fig.tight_layout()
    save_png(fig, "fig7_ablation_reproduced")

def draw_fig8() -> None:
    rows = read_rows(CSV_ROOT / "weight_sensitivity" / "weight_calibration_validation_summary.csv")
    order = ["default", "calibrated-top5-average", "calibrated-best-901227"]
    labels = ["Default", "Calibrated top-5 avg.", "Calibrated best"]
    by_alg = {row["algorithm"]: row for row in rows}
    means = np.array([float(by_alg[alg]["objective_mean"]) for alg in order])
    stds = np.array([float(by_alg[alg]["objective_std"]) for alg in order])
    improvements = (means[0] - means) / means[0] * 100.0
    fig, ax = plt.subplots(figsize=(6.3, 3.7))
    bars = ax.bar(np.arange(len(order)), means, yerr=stds, capsize=5, color=["#8c8c8c", "#4c78a8", "#f58518"], edgecolor="#333333", linewidth=0.5, width=0.58)
    for idx, (bar, improvement, std) in enumerate(zip(bars, improvements, stds)):
        label = f"{improvement:.3f}%"
        if idx > 0:
            label += " improvement"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 5.2, label, ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(np.arange(len(order)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Validation objective")
    ax.set_ylim(0, max(means + stds) + 24)
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.55, alpha=0.8)
    fig.tight_layout()
    save_png(fig, "fig8_weight_calibration_reproduced")

def main() -> int:
    draw_fig4()
    draw_fig5()
    draw_fig6()
    draw_fig7()
    draw_fig8()
    print(f"Wrote reproduced figures under {OUT_DIR.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
