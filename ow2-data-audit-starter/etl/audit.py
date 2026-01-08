"""
OW2 dataset: Data Audit
Run:
  python etl/audit.py --input data/raw/ow2_quickplay_heroes_stats__2023-05-06.csv
Outputs:
  reports/audit_summary.json
  reports/missingness.csv
  reports/column_dictionary.csv
  docs/data_audit.md
"""
import argparse, json, os, datetime
import pandas as pd

def infer_unit(col: str) -> str:
    if col in ["Hero", "Skill Tier", "Role"]:
        return "categorical"
    if "%" in col:
        return "percent (0-100)"
    if "/ 10min" in col:
        return "per 10 minutes"
    return "unknown"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw CSV")
    parser.add_argument("--outdir", default=".", help="Project root (default: .)")
    args = parser.parse_args()

    root = args.outdir
    df = pd.read_csv(args.input)

    # Ensure folders exist
    os.makedirs(os.path.join(root, "reports"), exist_ok=True)
    os.makedirs(os.path.join(root, "docs"), exist_ok=True)

    rows, cols = df.shape
    heroes = int(df["Hero"].nunique())
    tiers = int(df["Skill Tier"].nunique())
    role_list = sorted(df["Role"].unique().tolist())

    # Grain check
    dup_count = int(df.duplicated(["Hero", "Skill Tier"]).sum())
    combo_counts = df.groupby(["Hero", "Skill Tier"]).size()
    grain_violations = int((combo_counts != 1).sum())

    # Completeness
    tier_set = set(df["Skill Tier"].unique())
    missing_by_hero = {}
    for hero, g in df.groupby("Hero"):
        miss = sorted(list(tier_set - set(g["Skill Tier"].unique())))
        if miss:
            missing_by_hero[hero] = miss

    # Missingness
    missing_pct = (df.isna().mean() * 100).round(2).sort_values(ascending=False)
    missing_pct.to_frame("missing_pct").to_csv(os.path.join(root, "reports", "missingness.csv"))

    # Column dictionary
    col_dict = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "missing_pct": (df.isna().mean() * 100).round(2).values,
        "unit_inferred": [infer_unit(c) for c in df.columns],
    })
    col_dict["is_core"] = col_dict["missing_pct"].eq(0.0)
    col_dict.sort_values(["is_core","missing_pct"], ascending=[False, True]).to_csv(
        os.path.join(root, "reports", "column_dictionary.csv"),
        index=False
    )

    # Validity checks
    pct_cols = [c for c in df.columns if "%" in c]
    pct_out = []
    for c in pct_cols:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        mn, mx = float(s.min()), float(s.max())
        if mn < 0 or mx > 100:
            pct_out.append({"column": c, "min": mn, "max": mx})

    per10_cols = [c for c in df.columns if "/ 10min" in c]
    neg_out = []
    for c in per10_cols:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        mn = float(s.min())
        if mn < 0:
            neg_out.append({"column": c, "min": mn})

    role_incons = []
    for hero, g in df.groupby("Hero"):
        if g["Role"].nunique() != 1:
            role_incons.append({"hero": hero, "roles": g["Role"].unique().tolist()})

    core_cols = [c for c in df.columns if df[c].isna().mean() == 0]

    summary = {
        "dataset_file": args.input,
        "rows": rows,
        "columns": cols,
        "heroes": heroes,
        "skill_tiers": tiers,
        "skill_tier_values": df["Skill Tier"].unique().tolist(),
        "role_values": role_list,
        "grain": "Hero x Skill Tier",
        "duplicate_hero_tier_rows": dup_count,
        "grain_violations": grain_violations,
        "missing_tiers_by_hero_count": len(missing_by_hero),
        "percent_columns_count": len(pct_cols),
        "per10_columns_count": len(per10_cols),
        "percent_out_of_range_columns": pct_out,
        "negative_per10_columns": neg_out,
        "role_inconsistencies": role_incons,
        "core_columns_count": len(core_cols),
        "core_columns": core_cols,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    with open(os.path.join(root, "reports", "audit_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Minimal markdown report
    top_missing = missing_pct.head(15)
    md = f"""# OW2 Quickplay Heroes Stats — Data Audit

## Snapshot
- Rows: {rows}
- Columns: {cols}
- Heroes: {heroes}
- Skill tiers: {tiers} ({", ".join(df["Skill Tier"].unique())})
- Roles: {", ".join(role_list)}
- Grain: Hero × Skill Tier

## Checks
- Duplicate (Hero, Skill Tier): {dup_count}
- Grain violations: {grain_violations}
- Percent range [0,100]: {"PASS" if len(pct_out)==0 else "FAIL"}
- Per-10-min non-negative: {"PASS" if len(neg_out)==0 else "FAIL"}
- Role consistent per hero: {"PASS" if len(role_incons)==0 else "FAIL"}

## Missingness (top 15)
""" + "\n".join([f"- {k}: {v:.2f}%" for k,v in top_missing.items()]) + "\n"
    with open(os.path.join(root, "docs", "data_audit.md"), "w", encoding="utf-8") as f:
        f.write(md)

    print("Done. See docs/data_audit.md and reports/")

if __name__ == "__main__":
    main()
