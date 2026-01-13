import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ACTIVITY_CSV = r"data\8c) Woodcorp O2C Activity table.csv"

CASE = "CASE_KEY"
ACT = "ACTIVITY_EN"
TIME = "EVENTTIME"

CORE_CHAIN = [
    "Order received",
    "Confirm sale",
    "Start production",
    "Finished production",
    "Load shipment",
    "Goods delivered",
]

OUT_DIR = Path(__file__).resolve().parent
OUT_CASE = OUT_DIR / "out_core_sequence_check_case_level.csv"
OUT_DIST = OUT_DIR / "out_core_sequence_check_violation_distribution.csv"
OUT_CHART = OUT_DIR / "first_violation_transition_top10.png"
OUT_KPI = OUT_DIR / "kpi_first_violation_summary.txt"


def first_violation(row: pd.Series) -> pd.Series:
    available = [a for a in CORE_CHAIN if pd.notna(row.get(a))]
    if len(available) < 2:
        return pd.Series({"has_violation": False, "first_violation_between": None})

    prev = available[0]
    for curr in available[1:]:
        if row[curr] < row[prev]:
            return pd.Series({"has_violation": True, "first_violation_between": f"{prev} -> {curr}"})
        prev = curr

    return pd.Series({"has_violation": False, "first_violation_between": None})


df = pd.read_csv(ACTIVITY_CSV, usecols=[CASE, ACT, TIME])
df[TIME] = pd.to_datetime(df[TIME], errors="coerce")
df = df.dropna(subset=[TIME])

df = df[df[ACT].isin(CORE_CHAIN)]

first_times = (
    df.groupby([CASE, ACT], sort=False)[TIME]
      .min()
      .unstack(ACT)
)

res = first_times.apply(first_violation, axis=1)

total_cases = int(len(res))
viol_cases = int(res["has_violation"].sum())
share = (viol_cases / total_cases * 100.0) if total_cases else 0.0

print(f"Total cases (with at least 1 core event): {total_cases}")
print(f"Cases with timestamp violating core sequence: {viol_cases}")
print(f"Share: {share:.2f}%")

dist = (
    res.loc[res["has_violation"], "first_violation_between"]
      .value_counts()
      .rename_axis("first_violation_between")
      .reset_index(name="case_count")
)
dist["share_pct_of_all_cases"] = (dist["case_count"] / total_cases * 100.0).round(2)

print("\nTop first-violation transitions:")
print(dist.head(10).to_string(index=False))

res.to_csv(OUT_CASE, index=True)
dist.to_csv(OUT_DIST, index=False)

topn = 10
plot_df = dist.head(topn)

plt.figure(figsize=(11, 6))
plt.bar(plot_df["first_violation_between"].astype(str),
        plot_df["share_pct_of_all_cases"].astype(float))
plt.xticks(rotation=35, ha="right")
plt.ylabel("Share of all cases (%)")
plt.title(f"First timestamp sequence violation by transition (Top {topn})")
plt.tight_layout()
plt.savefig(OUT_CHART, dpi=200)
plt.close()

OUT_KPI.write_text(
    "Total cases (with at least 1 core event): {0}\n"
    "Cases with timestamp violating core sequence: {1}\n"
    "Share: {2:.2f}%\n".format(total_cases, viol_cases, share),
    encoding="utf-8",
)

print(f"\nSaved chart: {OUT_CHART}")
print(f"Saved KPI summary: {OUT_KPI}")
