# B-CORE Reproducibility Package

This repository contains the generated/anonymized benchmark data, fixed seeds, experiment configurations, scripts, and result summaries used in the computational evaluation of B-CORE, a low-latency online decision-support framework for coupled production-logistics rescheduling in AGV-integrated flexible manufacturing systems.

The package supports reproduction of the reported summary tables and figures from released CSV files. It does not require rerunning the full computational campaign.

## Contents

- `configs/`: experiment configuration summaries for the reported computational study.
- `data/`: released seed sets and notes on generated/anonymized benchmark construction.
- `results/csv/`: final result CSV files used for the manuscript tables and numerical claims.
- `results/plot_data/`: plotting-oriented CSV exports.
- `scripts/`: smoke test, table reproduction, figure reproduction, result summarization, and checksum verification.
- `figures/`: clean manuscript figures 4 to 8 and regenerated-figure output location.
- `docs/`: scope, data dictionary, claim boundary, and reproducibility notes.

## Environment

Python 3.10 or newer is recommended. The reproduction scripts require only CPU execution.

```bash
python -m pip install -r requirements.txt
```

## Quick Start

```bash
python scripts/run_smoke_test.py
python scripts/summarize_results.py
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
python scripts/verify_checksums.py
```

`run_smoke_test.py` checks row counts, status fields, and the manuscript-facing numerical values. `reproduce_tables.py` writes summary CSV files under `results/summary_tables/`. `reproduce_figures.py` writes regenerated Fig. 4 to Fig. 8 images under `figures/reproduced/`.

## Data Scope

The released package focuses on generated/anonymized dynamic FJSP-AGV benchmarks. Proprietary production-line records are not included. The benchmark objective is makespan; due-date and WIP extensions are reserved for future benchmark versions.

## Manuscript Correspondence

The package reproduces the following reported values from released CSV files: 1280 reference rows, 2250 fair-budget rows, 28101 weight-sensitivity rows, 1080 main-result rows, 450 ablation rows, B-CORE rank-first count of 96 out of 225 matched settings, B-CORE equal-budget mean objective of 94.906, B-CORE mean P95 latency of 0.000353 s, main-comparison B-CORE mean objective of 94.620, ablation degradations of 23.487%, 5.617%, and 0.278%, and calibration improvements of 2.905% and 5.781%.

## Citation

Please cite the associated manuscript and this repository if the released data or scripts are used.

## License

Unless otherwise stated, code is released under the MIT License. Generated/anonymized benchmark data and result summaries are released for academic reproducibility with attribution.

## Contact

Correspondence should follow the contact information in the associated manuscript. Author order and repository metadata should be confirmed before public upload.
