from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Paths (project-root assets/)
# -----------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # scripts/ -> project root
ASSETS_DIR = PROJECT_ROOT / "assets"
RUN_SLUG = "woodcorp-otif-rootcause"  # <- ggf. anpassen

OUT_DIR = ASSETS_DIR / RUN_SLUG
PLOTS_DIR = OUT_DIR / "plots"
TABLES_DIR = OUT_DIR / "tables"
FLAGS_DIR = OUT_DIR / "flags"

for d in [PLOTS_DIR, TABLES_DIR, FLAGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CSV_PATH = PROJECT_ROOT / r"data\8c) Woodcorp O2C Case table.csv"

TOP_N = 15
MIN_CASES = 50


# -----------------------
# IO + Parsing
# -----------------------
def try_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV nicht gefunden: {path.resolve()}")
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(path, sep=sep, dtype=str, engine="python")
            if df.shape[1] > 3:
                return df
        except Exception:
            pass
    raise ValueError("Konnte CSV nicht robust lesen (Separator/Format prüfen).")


def parse_eu_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return float(x)
    s = str(x).strip().strip('"').replace(" ", "")
    if s == "":
        return np.nan
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan


def savefig(name: str):
    p = PLOTS_DIR / name
    plt.tight_layout()
    plt.savefig(p, dpi=160)
    plt.close()
    return p


def fmt_int(x) -> str:
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return "0"


# -----------------------
# KPI Engineering
# -----------------------
def engineer_kpis(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = [
        "ORDERED_QUANTITY", "DELIVERED_QUANTITY",
        "MIN_ORDER_TOLERANCE", "MAX_ORDER_TOLERANCE",
        "ORDER_VALUE", "UNIT_PRICE",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].apply(parse_eu_number), errors="coerce")

    for c in ["DELIVERED_DATE", "PROMISED_DATE"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    tmin = df.get("MIN_ORDER_TOLERANCE", pd.Series(np.nan, index=df.index)).fillna(0.0)
    tmax = df.get("MAX_ORDER_TOLERANCE", pd.Series(np.nan, index=df.index)).fillna(0.0)

    df["TOL_LOWER"] = df["ORDERED_QUANTITY"] * (1.0 + tmin / 100.0)
    df["TOL_UPPER"] = df["ORDERED_QUANTITY"] * (1.0 + tmax / 100.0)

    df["IS_TOL_VIOLATION"] = (
        (df["DELIVERED_QUANTITY"] < df["TOL_LOWER"]) |
        (df["DELIVERED_QUANTITY"] > df["TOL_UPPER"])
    ).fillna(False)

    df["OUTSIDE_TOL_QTY"] = 0.0
    low = df["DELIVERED_QUANTITY"] < df["TOL_LOWER"]
    high = df["DELIVERED_QUANTITY"] > df["TOL_UPPER"]
    df.loc[low, "OUTSIDE_TOL_QTY"] = (df.loc[low, "TOL_LOWER"] - df.loc[low, "DELIVERED_QUANTITY"])
    df.loc[high, "OUTSIDE_TOL_QTY"] = (df.loc[high, "DELIVERED_QUANTITY"] - df.loc[high, "TOL_UPPER"])

    if "DELIVERED_DATE" in df.columns and "PROMISED_DATE" in df.columns:
        df["DELTA_DAYS"] = (df["DELIVERED_DATE"] - df["PROMISED_DATE"]).dt.days
        df["IS_LATE"] = (df["DELTA_DAYS"] > 0).fillna(False)
    else:
        df["DELTA_DAYS"] = np.nan
        df["IS_LATE"] = False

    df["IS_OTIF_FAIL"] = (df["IS_LATE"] | df["IS_TOL_VIOLATION"]).fillna(False)
    return df


# -----------------------
# Group Tables + Ranking
# -----------------------
def group_table(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    g = df.groupby(dim, dropna=False, observed=False)
    out = pd.DataFrame({
        "dimension": dim,
        "member": g.size().index.astype(str),
        "cases": g.size().values,
        "late_rate_cases": g["IS_LATE"].mean().values,
        "tol_violation_rate_cases": g["IS_TOL_VIOLATION"].mean().values,
        "otif_fail_rate_cases": g["IS_OTIF_FAIL"].mean().values,
        "otif_fail_cases": g["IS_OTIF_FAIL"].sum().values,
    })

    if "ORDER_VALUE" in df.columns:
        total_val = g["ORDER_VALUE"].sum()
        fail_val = df.loc[df["IS_OTIF_FAIL"]].groupby(dim, dropna=False, observed=False)["ORDER_VALUE"].sum()
        out = out.merge(total_val.rename("sum_order_value"), left_on="member", right_index=True, how="left")
        out = out.merge(fail_val.rename("sum_order_value_otif_fail"), left_on="member", right_index=True, how="left")
        out["sum_order_value"] = out["sum_order_value"].fillna(0.0)
        out["sum_order_value_otif_fail"] = out["sum_order_value_otif_fail"].fillna(0.0)
        out["otif_fail_rate_value"] = np.where(
            out["sum_order_value"] != 0,
            out["sum_order_value_otif_fail"] / out["sum_order_value"],
            np.nan
        )

    return out


# -----------------------
# Plots
# -----------------------
def barh_rate(tbl: pd.DataFrame, metric: str, title: str, filename: str, top_n: int = TOP_N, min_cases: int = MIN_CASES):
    if tbl.empty or metric not in tbl.columns:
        return

    t = tbl.copy()
    t = t[t["cases"] >= min_cases] if min_cases is not None else t
    if t.empty:
        return

    t = t.sort_values(metric, ascending=False).head(top_n).copy()

    label = t["member"].astype(str) + " (N=" + t["cases"].astype(int).astype(str) + ")"
    if "sum_order_value" in t.columns:
        label = label + ", V=" + t["sum_order_value"].apply(fmt_int)

    plt.figure(figsize=(12, max(4, 0.35 * len(t) + 1)))
    plt.barh(label[::-1], t[metric].values[::-1])
    plt.title(title)
    plt.xlabel(metric)
    plt.grid(axis="x", alpha=0.3)
    savefig(filename)


# -----------------------
# Flags
# -----------------------
def export_flags(df: pd.DataFrame):
    def safe_sort(d: pd.DataFrame, cols, ascending):
        cols2 = [c for c in cols if c in d.columns]
        if not cols2:
            return d
        asc2 = ascending[:len(cols2)] if isinstance(ascending, list) else ascending
        return d.sort_values(cols2, ascending=asc2)

    if "UNIT_PRICE" in df.columns:
        m = df["UNIT_PRICE"].eq(0)
        if m.any():
            out = df.loc[m].copy()
            out.insert(0, "FLAG_REASON", "UNIT_PRICE==0")
            out = safe_sort(out, ["ORDER_VALUE", "CASE_KEY"], [False, True])
            out.to_csv(FLAGS_DIR / "flag_unit_price_zero.csv", index=False)

    if "ORDER_VALUE" in df.columns:
        m = df["ORDER_VALUE"].eq(0)
        if m.any():
            out = df.loc[m].copy()
            out.insert(0, "FLAG_REASON", "ORDER_VALUE==0")
            out = safe_sort(out, ["UNIT_PRICE", "CASE_KEY"], [False, True])
            out.to_csv(FLAGS_DIR / "flag_order_value_zero.csv", index=False)

    if all(c in df.columns for c in ["ORDER_VALUE", "UNIT_PRICE", "DELIVERED_QUANTITY"]):
        approx = df["UNIT_PRICE"] * df["DELIVERED_QUANTITY"]
        rel_err = (df["ORDER_VALUE"] - approx).abs() / approx.replace(0, np.nan)
        m = rel_err.gt(0.10) & rel_err.notna()
        if m.any():
            out = df.loc[m].copy()
            out["VALUE_REL_ERR"] = rel_err.loc[m]
            out.insert(0, "FLAG_REASON", "VALUE_REL_ERR>0.10")
            out = safe_sort(out, ["VALUE_REL_ERR", "ORDER_VALUE", "CASE_KEY"], [False, False, True])
            out.to_csv(FLAGS_DIR / "flag_value_mismatch_relerr_gt_10pct.csv", index=False)


# -----------------------
# Main
# -----------------------
def main():
    df = try_read_csv(CSV_PATH)
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].str.strip().str.strip('"')

    df = engineer_kpis(df)

    dim_candidates = [
        ("DELIVERY_COMPANY", "supplier"),
        ("FACTORY", "factory"),
        ("PRODUCT_TYPE", "product_type"),
        ("FACTORY_TYPE", "factory_type"),
        ("WAREHOUSE_TYPE", "warehouse_type"),
        ("CUST_MARKET", "cust_market"),
        ("CUST_COUNTRY", "cust_country"),
    ]

    dims = [(d, slug) for d, slug in dim_candidates if d in df.columns]

    all_rows = []
    for dim, slug in dims:
        tbl = group_table(df, dim)

        tbl.to_csv(TABLES_DIR / f"rates_{slug}.csv", index=False)
        all_rows.append(tbl)

        barh_rate(
            tbl,
            "tol_violation_rate_cases",
            f"{dim}: Quantity Tolerance Violation Rate (Cases) – Top {TOP_N} (N≥{MIN_CASES})",
            f"top{TOP_N}_{slug}_tol_violation_rate.png",
        )
        barh_rate(
            tbl,
            "late_rate_cases",
            f"{dim}: Late Rate (Cases) – Top {TOP_N} (N≥{MIN_CASES})",
            f"top{TOP_N}_{slug}_late_rate.png",
        )

    if all_rows:
        otif_all = pd.concat(all_rows, ignore_index=True)
        otif_all = otif_all.sort_values(["otif_fail_rate_cases", "cases"], ascending=[False, False], na_position="last")
        otif_all.to_csv(OUT_DIR / "otif_ranking_all_dimensions.csv", index=False)

    export_flags(df)

    print("Done:")
    print("Assets root:", ASSETS_DIR.resolve())
    print("Run folder:", OUT_DIR.resolve())


if __name__ == "__main__":
    main()
