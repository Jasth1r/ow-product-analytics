# OW2 Data Audit (Quickplay Heroes Stats)

This repo is the **Data Audit** step for an OW2 analytics project.

## What you get
- Reproducible audit script: `etl/audit.py`
- Audit outputs:
  - `docs/data_audit.md` (human-readable report)
  - `reports/audit_summary.json`
  - `reports/missingness.csv`
  - `reports/column_dictionary.csv`

## How to run (local)
1) Put the raw CSV here:
- `data/raw/ow2_quickplay_heroes_stats__2023-05-06.csv`

2) Install deps:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3) Run audit:
```bash
python etl/audit.py --input data/raw/ow2_quickplay_heroes_stats__2023-05-06.csv
```

## Notes
- Raw data is ignored by default via `.gitignore` (recommended for large files).
- Missing values are mostly **hero-specific stats** (treat as Not Applicable).
